# informat.sftp SFTP Operations

## Overview
Use `informat.sftp` to implement SFTP client related functionality.

***
## createClient 
Initialize an SFTP client instance

```javascript
informat.sftp.createClient()
```

**Return Value**
Type is `SftpClient`

## SftpClient

### login
Log in to an SFTP server with username and password
```js
client.login(username,password,host,port)
```
| Parameter  | Type        | Description      |
| ----  |-----------|---------|
| username  | `String`  | Username |
| password  | `String`  | Password |
| host  | `String`  | SFTP server host |
| port  | `Integer` | SFTP server port |

### loginWithPrivateKey
Log in to an SFTP server with a private key
```js
client.loginWithPrivateKey(username,privateKey,host,port)
```
| Parameter  | Type  | Description      |
| ----  | ----  |---------|
| username  | String | Username |
| privateKey  | String | Private key |
| host  | String | SFTP server host |
| port  | int | SFTP server port |

### logout
Log out
```js
client.logout()
```

### cd

Change the current working directory

```js
client.cd(path)
```
| Parameter  | Type  | Description      |
| ----  | ----  |---------|
| path  | String | Path of the directory to change to |

### put
Upload a file to the SFTP server
```js
client.put(localPath, dst)
```
| Parameter  | Type  | Description      |
| ----  | ----  |---------|
| localPath  | String | Path of the file in the app sandbox environment |
| remotePath  | String | File path on the SFTP server |

### put
Upload a file to the SFTP server
```js
client.put(localPath, dst, mode)
```
| Parameter  | Type  | Description      |
| ----  | ----  |---------|
| localPath  | String | Path of the file in the app sandbox environment |
| remotePath  | String | File path on the SFTP server |
| mode  | int | Mode, available values:<br />0: If the destination file already exists, it will be overwritten. This is the default mode<br />1: If the transfer is interrupted, it will resume from where it left off instead of starting over <br />2: If the destination file already exists, the uploaded data will be appended to the end of the file|

### downloadFile
Download a specified file from the SFTP server to the local app sandbox environment
```js
client.downloadFile(remotePath, localPath)
```
| Parameter  | Type  | Description      |
| ----  | ----  |---------|
| remotePath  | String | Remote file path |
| localPath  | String | Local app sandbox environment path |

### ls
List files and directories in a specified directory on the SFTP server
```js
client.ls(path)
```
| Parameter  | Type  | Description      |
| ----  | ----  |---------|
| path  | String | Path of the remote directory to list contents of |

**Return Value**
Type is `Array<SftpFile>`
Returns the file list

### mkdir
Create a new directory on the SFTP server
```js
client.mkdir(path)
```
| Parameter  | Type  | Description      |
| ----  | ----  |---------|
| path | String | Path of the new directory to create |

### pwd
Get the current working directory in the SFTP session
```js
client.pwd()
```

**Return Value**
Type is `String`
Returns the current working directory in the SFTP session

### disconnect
End the session with the remote SSH server.

```js
client.disconnect()
```

>This is critical for preventing network resource and file descriptor leaks. Failing to call this method may cause long-running applications to accumulate unclosed connections, which can affect performance or lead to resource exhaustion.


**Below is a complete example**
```js
var host = "192.168.1.120";
var port = 22;
var userName = "sftpuser";
var password = "<sftp-password>";
var client=null;
try{
    client=informat.sftp.createClient();
    client.login(userName, password, host, port);
    console.log(client.pwd())
    client.mkdir('test/d');
    client.put("logo.jpg", 'test/d/logo.jpg');//Note: You need to upload a file to the app sandbox environment first
    client.downloadFile("test/d/logo.jpg", "sftp/logo.jpg");
}finally{
    if (client!= null) {
        client.disconnect();
    }
}
```
