# informat.ftp FTP Operations

## Overview

Use `informat.ftp` to implement FTP client related functionality.

## createClient

Initialize an FTP client instance

```javascript
informat.ftp.createClient()
```

**Return Value**
Type [FtpClient](/guide/script/ftp.md#ftpclient)

## FtpClient

### connect

Establish a connection to the FTP server

```js
client.connect(host, port)
```

| Parameter | Type      | Description     |
|-----------|-----------|-----------------|
| host      | `String`  | FTP server host |
| port      | `Integer` | FTP server port |

**Example**

```js
client.connect('127.0.0.1', 21)
```

### login

Log in to the FTP server with username and password

```js
client.login(username, password)
```

| Parameter | Type     | Description |
|-----------|----------|-------------|
| username  | `String` | Username    |
| password  | `String` | Password    |

**Return Value**

Type `Boolean`
Returns whether the login was successful

**Example**

```js
client.login('ftpuser', '123456')
```

### printWorkingDirectory

Returns the current working directory path

```js
client.printWorkingDirectory()
```

**Return Value**

Type `String`
Returns the current working directory path

### changeToParentDirectory

Change the current working directory to its parent directory

```js
client.changeToParentDirectory()
```

**Return Value**

Type `Boolean`
Returns whether the change to parent directory was successful

### changeWorkingDirectory

Change the working directory of the current FTP server connection

```js
client.changeWorkingDirectory(path)
```

| Parameter | Type     | Description                          |
|-----------|----------|--------------------------------------|
| path      | `String` | The path of the directory to change to |

**Return Value**

Type `Boolean`
Returns whether the working directory change was successful

**Example**

```js
client.changeWorkingDirectory('/')
```

### uploadFile

Upload a file to the FTP server

```js
client.uploadFile(localPath, remotePath)
```

| Parameter  | Type     | Description                           |
|------------|----------|---------------------------------------|
| localPath  | `String` | Path of the file in the app sandbox   |
| remotePath | `String` | File path on the FTP server           |

**Return Value**

Type `Boolean`
Returns whether the upload was successful

**Example**

```js
client.uploadFile('demo.png', 'test/demo.png');
```

### downloadFile

Download a specified file from the FTP server to the local app sandbox

```js
client.downloadFile(remotePath, localPath)
```

| Parameter  | Type     | Description                         |
|------------|----------|-------------------------------------|
| remotePath | `String` | Remote file path                    |
| localPath  | `String` | Local app sandbox file path         |

**Return Value**

Type `Boolean`
Returns whether the download was successful

**Example**

```js
client.downloadFile("test/demo.png", "ftp/demo.png");
```

### makeDirectory

Create a directory on the FTP server

```js
client.makeDirectory(path)
```

| Parameter | Type     | Description          |
|-----------|----------|----------------------|
| path      | `String` | Remote directory path |

**Return Value**

Type `Boolean`
Returns whether the creation was successful

**Example**

```js
client.makeDirectory('test');
```

### listFiles

List files and directories in the current working directory on the FTP server

```js
client.listFiles()
```

**Return Value**

Type `Array<FtpFile>`
Returns the file list

::: warning If the result is empty but the directory contains files, you need to enable passive transfer mode

```js
let client = null;
try {
    // Create connection
    client = informat.ftp.createClient();
    client.connect('127.0.0.1', 21);
    // Login
    let login = client.login('ftpuser', '123456');
    console.log('login:', login);
    // Get current path
    console.log(client.printWorkingDirectory());
    // Enable passive transfer mode              // [!code focus]     
    client.getFtpClient().enterLocalPassiveMode(); // [!code focus]
    // Get files and directories in the current directory
    let files = client.listFiles();
    files.forEach(f => {
        console.log(f);
        console.log(f.getGroup()); // File group
        console.log(f.getName()); // File name
        console.log(f.getSize()); // File size
        console.log(f.isDirectory()); // Is directory
        console.log(f.isFile()); // Is file
    })

} finally {
    if (client != null) {
        // Close connection
        client.disconnect();
    }
}
```

:::

### disconnect

Close the connection to the FTP server

```js
client.disconnect()
```

***Full Example***

```js
let client = null;
try {
    // Create connection
    client = informat.ftp.createClient();
    client.connect('127.0.0.1', 21);
    // Login
    let login = client.login('ftpuser', '123456');
    console.log('login:', login);
    // Get current path
    console.log(client.printWorkingDirectory());
    // Get files and directories in the current directory
    let files = client.listFiles();
    files.forEach(f => {
        console.log(f);
        console.log(f.getGroup()); // File group
        console.log(f.getName()); // File name
        console.log(f.getSize()); // File size
        console.log(f.isDirectory()); // Is directory
        console.log(f.isFile()); // Is file
    })
    // Create directory
    client.makeDirectory('test');
    // Upload file
    var ret = client.uploadFile('demo.png', 'test/demo.png');
    console.log('uploadFile ret:', ret)
    // Download file
    ret = client.downloadFile("test/demo.png", "ftp/demo.png");
    console.log('downloadFile ret:', ret)
} finally {
    if (client != null) {
        // Close connection
        client.disconnect();
    }
}
```
