# informat.file Local Files

## Overview

Use the `informat.file` object to perform file operations. All files are stored in the app sandbox environment.

::: info Terminology
- App sandbox environment: The runtime environment of an app. Each app runs in its own sandbox and cannot directly access resource files and data of other apps.
- File path in the app sandbox: A file path using the app directory as the root directory. For example, the root directory of the app sandbox environment is `/`
  :::

## getFile

Get file information

```javascript
informat.file.getFile(path)
```

| Parameter | Type     | Description |
|-----------|----------|-------------|
| path      | `String` | File path   |

**Return Value**

Returns file information [File](/guide/script/model.md#file)

**Example**

::: code-group

```javascript [Call]
informat.file.getFile('gzb.xlsx');
```
```json [Return Value]
{
  "absolute": true,
  "absolutePath": "/home/appadmin/informat_home/file_storage/localfiles/g09aj7cus3d8s/ey89pc358ousw/gzb.xlsx",
  "canRead": true,
  "canWrite": true,
  "directory": false,
  "file": true,
  "isAbsolute": true,
  "isDirectory": false,
  "isFile": true,
  "lastModified": 1683602289249,
  "length": 10317,
  "name": "gzb.xlsx",
  "path": "/home/appadmin/informat_home/file_storage/localfiles/g09aj7cus3d8s/ey89pc358ousw/gzb.xlsx",
  "totalSpace": 211243687936,
  "usableSpace": 80439672832
}

```

:::

## getRealPath

Get the full file path

```javascript
informat.file.getRealPath(path)
```

| Parameter | Type     | Description |
|-----------|----------|-------------|
| path      | `String` | File path   |

**Return Value**

Type `String`, full local file path

**Example**

::: code-group

```javascript [Call]
informat.file.getRealPath('gzb.xlsx');
```
```text [Return Value]
/home/appadmin/informat_home/file_storage/localfiles/g09aj7cus3d8s/ey89pc358ousw/gzb.xlsx
```
:::

## md5

Get the MD5 hash of a file

```javascript
informat.file.md5(path)
```

| Parameter | Type     | Description |
|-----------|----------|-------------|
| path      | `String` | File path   |

**Return Value**

Type `String`, returns the MD5 hash of the local file

**Example**

::: code-group

```javascript [Call]
informat.file.md5('gzb.xlsx');
```
```text [Return Value]
eb5958522b1043d715ecf076d5ff3dc9
```
:::

## create

Create a file in the app sandbox environment

```javascript
informat.file.create(path)
```

| Parameter | Type     | Description |
|-----------|----------|-------------|
| path      | `String` | File path   |

**Return Value**

Type `String`, returns whether the creation was successful

**Example**

::: code-group

```javascript [Call]
informat.file.create('a.txt');
```
```text [Return Value]
true
```
:::

## mkdirs

Create a directory in the app sandbox environment

```javascript
informat.file.mkdirs(path)
```

| Parameter | Type     | Description    |
|-----------|----------|----------------|
| path      | `String` | Directory path |

**Return Value**

Type `Boolean`, returns whether the creation was successful

**Example**

::: code-group

```javascript [Call]
informat.file.mkdirs('a/b/c');
```
```text [Return Value]
true
```

:::

## delete

Delete a file in the app sandbox environment

If the file corresponding to the path does not exist, the system will report a `file not found` error;
If the path corresponds to a directory instead of a file, the system will report a `file not found` error;

```javascript
informat.file.delete(path)
```

| Parameter | Type     | Description |
|-----------|----------|-------------|
| path      | `String` | File path   |

**Return Value**

Type `Boolean`, returns whether the deletion was successful

**Example**

::: code-group

```javascript [Call]
informat.file.delete('a.txt');
```
```text [Return Value]
true
```
:::


## deleteDirectory

Delete a directory in the app sandbox environment. If the directory contains subdirectories and files, they will also be deleted.

If the directory corresponding to the path does not exist, the system will report a `file not found` error;
If the path corresponds to a file instead of a directory, the system will report a `file not found` error;

```javascript
informat.file.deleteDirectory(path)
```

| Parameter | Type     | Description    |
|-----------|----------|----------------|
| path      | `String` | Directory path |

**Return Value**

Type `Boolean`, returns whether the deletion was successful

**Example**

::: code-group

```javascript [Call]
informat.file.deleteDirectory('a');
```
```text [Return Value]
true
```

:::


## exists

Check whether a file exists in the app sandbox environment

```javascript
informat.file.exists(path)
```

| Parameter | Type     | Description |
|-----------|----------|-------------|
| path      | `String` | File path   |

**Return Value**

Type `Boolean`, returns whether the file exists

**Example**

::: code-group

```javascript [Call]
informat.file.exists('a.txt');
```
```text [Return Value]
true
```
:::

## isDirectory

Check whether a file is a directory

```javascript
informat.file.isDirectory(path)
```

| Parameter | Type     | Description |
|-----------|----------|-------------|
| path      | `String` | File path   |

**Return Value**

Type `Boolean`, returns whether it is a directory

**Example**

::: code-group

```javascript [Call]
informat.file.isDirectory('a.txt');
```
```text [Return Value]
false
```
:::


## listFile

Returns the list of files in a directory

```javascript
informat.file.listFile(path)
```

| Parameter | Type     | Description |
|-----------|----------|-------------|
| path      | `String` | File path   |

**Return Value**

Type `Array<String>`, returns the list of files in the directory

**Example**

::: code-group

```javascript [Call]
informat.file.listFile('');
```
```json [Return Value]
[
  "xxxx123.txt",
  "1234444",
  "gzb2.xlsx",
  "a",
  "gzb.xlsx"
]
```
:::

## move

Move the source file to the target path

```javascript
informat.file.move(source, target)
```

::: tip
If the target path already exists, the file will be moved to a subdirectory of the target path
:::

| Parameter | Type     | Description      |
|-----------|----------|------------------|
| source    | `String` | Source file path  |
| target    | `String` | Target path       |

**Return Value**

Type `Boolean`, returns whether the operation was successful

**Example**
::: code-group

```javascript [Call]
informat.file.move('a', 'b');
```
```text [Return Value]
true
```

:::

## copy

Copy the source file to the target path

```javascript
informat.file.copy(source, target)
```

| Parameter | Type     | Description      |
|-----------|----------|------------------|
| source    | `String` | Source file path  |
| target    | `String` | Target path       |

**Return Value**

Type `Boolean`, returns whether the operation was successful

**Example**

::: code-group

```javascript [Call]
informat.file.copy('a.txt', 'b.txt');
```
```text [Return Value]
true
```

:::

::: warning Note
The source file cannot be a directory
:::

## zip

Compress files

```javascript
informat.file.zip(sourcePath, targetPath, charsetName, withSrcDir)
```

| Parameter   | Type      | Description                          |
|-------------|-----------|--------------------------------------|
| sourcePath  | `String`  | Path of the files to compress        |
| targetPath  | `String`  | Target directory for the compressed file |
| charsetName | `String`  | Encoding, default `UTF-8`, optional  |
| withSrcDir  | `Boolean` | Whether to include the source directory, optional |

**Example**

```javascript
const result1 = informat.file.exists("file_content/test_content.jpg");
const result2 = informat.file.exists("file_content/test_content1.txt");
informat.file.zip('file_content', 'compressed_path/archive.zip');
informat.file.zip('file_content', 'compressed_path/archive.zip', 'GB2312', true);
```

**Download attachment field data and compress the directory**

```javascript
/**
 * Attachment download and compression script for XXX table
 * Function: Download attachments from 2 attachment fields across multiple records and compress them into a zip file
 */

export function downloadAndZip(recordList) {
    if(recordList.length==0){
        return null;
    }
    const idList = recordList.map(item => item.id);
    const downloadDir=informat.utils.randomUUID();
    const zipPath = downloadDir+`.zip`;
    try {
        console.log("Starting XXX table attachment download and compression script...");
        
        // 1. Query all records from the table
        console.log("Querying table records...");
        const records = informat.table.queryList('testTable',{
            pageSize: -1,
            returnOptionName:true,
            filter: {
                opt: "and",
                conditionList: [{ fieldId: "id", opt: "in", value: idList }]
            }
        });
        
        console.log(`Found ${records.length} records`);
        
        if (records.length === 0) {
            console.log("No records found, script execution finished");
            return;
        }
        
        informat.file.mkdirs(downloadDir);
        
        // 2. Process each record
        for (let i = 0; i < records.length; i++) {
            const record = records[i];
            console.log(`\nProcessing record ${i + 1} (ID: ${record.id})`);
            
            // Define 2 attachment fields
            const attachmentFields = [
                { field: "floorPhoto", name: "Empty vehicle floor photo" },
                { field: "frontPhoto", name: "Front photo" }
            ];
            
            // Create a dedicated folder for the record
            const recordFolder = downloadDir+`/${record.plateNumber_name}/`;
            informat.file.mkdirs(recordFolder);
            
            const downloadedFiles = [];
            
            // 3. Download files for each attachment field
            for (const attachmentField of attachmentFields) {
                const attachment = record[attachmentField.field];
                
                if (attachment && attachment.id) {
                    console.log(`  Downloading ${attachmentField.name}...`);
                    
                    try {
                        let localPath=`${recordFolder}${attachment.name}`;
                        // Download file from shared storage to local sandbox
                        informat.storage.download(
                            attachment.path,
                            localPath
                        );
                        
                        downloadedFiles.push(localPath);
                        console.log(`    Download successful: ${localPath}`);
                    } catch (error) {
                        console.log(`    Download failed: ${attachmentField.name} - ${error.message}`);
                    }
                } else {
                    console.log(`  Skipping ${attachmentField.name} - no attachment`);
                }
            }
            
            // 4. Compress files
            if (downloadedFiles.length > 0) {
                console.log(`  Starting file compression...${downloadDir}`);
                try {
                    informat.file.zip(downloadDir,zipPath);
                    console.log(`  Compression successful: ${zipPath}`);
                    console.log(`  Compressed ${downloadedFiles.length} files`);
                } catch (error) {
                    console.log(`  Compression failed: ${error.message}`);
                }
            } else {
                console.log(`No attachments to compress, skipping this record`);
            }
        }
        informat.file.deleteDirectory(downloadDir);
        console.log("\nScript execution completed!");
        
    } catch (error) {
        informat.file.deleteDirectory(downloadDir);
        console.error("Script execution error:", error);
        throw error;
    }
    return zipPath;
}

```

## unzip

Decompress files

```javascript
informat.file.unzip(sourcePath, targetPath, charsetName)
```

| Parameter   | Type     | Description                                              |
|-------------|----------|----------------------------------------------------------|
| sourcePath  | `String` | Path of the file to decompress                           |
| targetPath  | `String` | Target directory for decompression, auto-created if it does not exist |
| charsetName | `String` | Encoding, default `UTF-8`, optional                      |

**Example**

```javascript
informat.file.unzip("compressed_path/archive.zip", 'decompressed_path/all_files');
informat.file.unzip("compressed_path/archive.zip", 'decompressed_path/all_files', 'GB2312');
```

## readAsBytes

Read a file and return its binary content

```javascript
informat.file.readAsBytes(path)
```

| Parameter | Type     | Description |
|-----------|----------|-------------|
| path      | `String` | File path   |

**Return Value**

Type `Array<byte>`, the file content. Returns `null` if the file does not exist.

**Example**

```javascript
informat.file.readAsBytes('a.txt');
```

## readAsString

Read a file and return its content as a string

```javascript
informat.file.readAsString(path, charset)
```

| Parameter | Type     | Description              |
|-----------|----------|--------------------------|
| path      | `String` | File path                |
| charset   | `String` | Charset for the returned content |

**Return Value**

Type `String`, the file content. Returns `null` if the file does not exist.

**Example**
::: code-group

```javascript [Call]
informat.file.readAsString('a.txt', 'utf-8');
```
```text [Return Value]
hello informat
```

:::

## readAsBase64String

Read file binary content and return it as a base64-encoded string

```javascript
informat.file.readAsBase64String(path)
```

| Parameter | Type     | Description |
|-----------|----------|-------------|
| path      | `String` | File path   |

**Return Value**

Type `String`, the file content. Returns `null` if the file does not exist.

**Example**
::: code-group

```javascript [Call]
const file = 'a.txt';
informat.file.writeString(file, 'hello informat', 'utf-8');
informat.file.readAsBase64String(file);
```
```text [Return Value]
aGVsbG8gaW5mb3JtYXQ=
```

:::

## readAsBase64Bytes

Read file binary content and return it as base64-encoded binary content

```javascript
informat.file.readAsBase64Bytes(path)
```

| Parameter | Type     | Description |
|-----------|----------|-------------|
| path      | `String` | File path   |

**Return Value**

Type `Array<byte>`, the file content. Returns `null` if the file does not exist.

**Example**
::: code-group

```javascript [Call]
const file = 'a.txt';
informat.file.writeString(file, 'hello informat', 'utf-8');
informat.file.readAsBase64Bytes(file);
```

:::

## writeBytes

Write binary content to a file

```javascript
informat.file.writeBytes(path, content)
```

| Parameter | Type          | Description    |
|-----------|---------------|----------------|
| path      | `String`      | File path      |
| content   | `Array<byte>` | Binary content |

**Example**

```javascript
const readResult = informat.file.readAsBytes('x90.txt');
informat.file.writeBytes('b.txt', readResult);
```

## writeString

Write a string to a file

```javascript
informat.file.writeString(path, content, charset)
```

| Parameter | Type     | Description |
|-----------|----------|-------------|
| path      | `String` | File path   |
| content   | `String` | Content     |
| charset   | `String` | Charset     |

**Example**

```javascript
informat.file.writeString('c.txt', 'hello informat', 'utf-8');
```
