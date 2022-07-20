import os
from serial import Serial

serialDevDir='/dev/serial/by-id' 

if ( os.path.isdir(serialDevDir) ):
    serialDevices = os.listdir(serialDevDir) 

    if (len(serialDevices) > 0 ):

        serialDevicePath = os.path.join(serialDevDir, serialDevices[0])

        serial = Serial(port=serialDevicePath, baudrate=9600, timeout=0.2) 
        serial.write(b'EMO:0\n')

        command=''
        while(command != 'Q'):

            command = input('Enter EEMOTES command number (Q for quit): ')
            com=command[0]
            sendMsg = b'EMO:' + com.encode('ascii')
            serial.write(sendMsg + b'\n')
            receivedMsg = serial.readline() 

            if ( (len(receivedMsg) >= 4) and (receivedMsg[3] == b':'[0])):

                msgType = receivedMsg[0:3]
                msgData = receivedMsg[4:]
                
                if ( msgType == b'REC' ):
                    print('Message Received: ' + msgData.decode('ascii'))
                elif ( msgType == b'ERR' ):
                    print('ERROR:  ' + msgData.decode('ascii'))
            else:
             	print('Unrecognised Command')
    else:

        print('No serial devices connected') 

else:

    print(serialDevDir + ' does not exist')
