# informat.storage File Shared Storage Operations

## Overview
Use the `informat.storage` object to perform file shared storage operations. Shared storage uses the S3 protocol to store files on the file server. All files below will be stored in shared storage.

## Terminology

- Shared Storage: Please refer to the [Shared Storage](/guide/app/storage.md) documentation

## exists
Check whether a file exists
```javascript
informat.storage.exists(path)
```
| Parameter | Type   | Description |
| --------- | ------ |-------------|
| path      | String | File path   |

#### Return Value `Boolean`
Returns whether the file exists

***Example***
```javascript
// Check whether a file exists for a specified module attachment field in the current app
const path = 'moduleId/fieldId/fileId';
var result = informat.storage.exists(path);
if (result) {
  console.log('File exists');
} else {
  console.log('File does not exist');
}
```

***

## listFile
Returns the list of files in a directory
```javascript
informat.storage.listFile(path)
```

| Parameter | Type   | Description |
| --------- | ------ |-------------|
| path      | String | File path   |

#### Return Value `Array<String>`
Returns the list of files in the directory

***Example***
```javascript
// Get all files in the current app
const fileList = informat.storage.listFile('/');
console.log('fileList',fileList);
```

Return data as follows:

```javascript
[
    'fileId',
    'moduleId/fieldId/fileId',
    'moduleId/fieldId/fileId2',
    ...
]
```

## move
Move a file from the specified path to the target path. **Note: If a file with the same name exists at the target path, it will be overwritten**
```javascript
informat.storage.move(source,target)
```
| Parameter | Type   | Description      |
|-----------|--------|------------------|
| source    | String | Source file path  |
| target    | String | Target path       |
#### Return Value
None

***Example***
```javascript
// Move a specified file to the app root directory
const source = 'moduleId/fieldId/fileId';
const target = 'fileId';
informat.storage.move(source, target);
```

***

## copy
Copy a file from the specified path to the target path. **Note: If a file with the same name exists at the target path, it will be overwritten**

```javascript
informat.storage.copy(source,target)
```

| Parameter | Type   | Description      |
|-----------|--------|------------------|
| source    | String | Source file path  |
| target    | String | Target path       |

#### Return Value
None

***Example***
```javascript
// Copy a specified file to create a duplicate
const source = 'moduleId/fieldId/fileId';
const target = 'moduleId/fieldId/fileIdCopy';
informat.storage.copy(source, target);
```

***

## delete
Delete a file

If the file corresponding to path does not exist, the system will throw a `File does not exist` error;
If the path corresponds to a directory instead of a file, the system will throw a `File does not exist` error;

```javascript
informat.storage.delete(path)
```
| Parameter | Type   | Description |
| --------- | ------ |-------------|
| path      | String | File path   |
#### Return Value
None

***Example***
```javascript
// Delete a file from a specified module attachment field in the current app
const path = 'moduleId/fieldId/fileId';
informat.storage.delete(path);
```


***

## deleteDirectory
Delete a directory

If the directory corresponding to path does not exist, the system will throw a `File does not exist` error;
If the path corresponds to a file instead of a directory, the system will throw a `File does not exist` error;

```javascript
informat.storage.deleteDirectory(path)
```
| Parameter | Type   | Description    |
| --------- | ------ |----------------|
| path      | String | Directory path |
#### Return Value
None

***Example***
```javascript
// Delete all files from a specified module attachment field in the current app
const path = 'moduleId/fieldId';
informat.storage.deleteDirectory(path);
```

## download
Download a file from shared storage to the local sandbox environment. **Note: If a file with the same name exists locally, it will be overwritten**
```javascript
informat.storage.download(path,localPath)
```
| Parameter | Type   | Description                    |
| --------- |--------|--------------------------------|
| path      | String | File path                      |
| localPath | String | Local sandbox environment file path |

#### Return Value
None

***Example***
```javascript
// Download a specified shared storage file to the local root directory in the current app
const path = 'moduleId/fieldId/fileId';
const localPath = 'local.png';
informat.storage.download(path, localPath);
```

## upload
Upload a local file to shared storage. **Note: If a file with the same name exists, it will be overwritten**
```javascript
informat.storage.upload(localPath,remotePath)
```
| Parameter  | Type   | Description         |
|------------|--------|---------------------|
| localPath  | String | Local file path     |
| remotePath | String | Shared storage path |

#### Return Value
None

***Example***
```javascript
// Upload a specified local file to the shared storage root directory in the current app
const localPath = 'local.png';
const remotePath = 'remote.png';
informat.storage.upload(localPath, remotePath);
```

## uploadFromURL
Upload a file from a remote URL to shared storage
```javascript
informat.storage.uploadFromURL(url,remotePath)
```
| Parameter  | Type   | Description         |
|------------|--------|---------------------|
| url        | String | Remote URL          |
| remotePath | String | Shared storage path |

#### Return Value
None

***Example***
```javascript
// Upload a remote file to the shared storage root directory in the current app
const url = 'https:/example.com/file.jpg';
const remotePath = 'file.jpg';
informat.storage.uploadFromURL(url, remotePath);
```

## getFilePath

Get the file path

```javascript
informat.storage.getFilePath(tableKey,fieldKey,fileId)
```
| Parameter | Type   | Description          |
|-----------|--------|----------------------|
| tableKey  | String | Data table identifier |
| fieldKey  | String | Field identifier      |
| fileId    | String | File ID               |

#### Return Value `String`
Shared storage file path

***Example***

```javascript
// Get the file path for data table identifier 'goods', field identifier 'pic', and file ID 'fileId'
const filePath = informat.storage.getFilePath('goods', 'pic', 'fileId');
console.log('File path---->', filePath); // File path---->goodsmoduleId/picFieldId/fileId
```

# createFileToken
Create a file access token

```javascript
informat.storage.createFileToken(path, fileName, expireTime)
```

| Parameter  | Type    | Description                        |
|------------|---------|-------------------------------------|
| path       | String  | Shared storage file path            |
| fileName   | String  | File name, can be empty             |
| expireTime | Integer | Expiration time, unit: seconds      |


# createS3FileToken
Create an S3 standard temporary file access token. Returns the presigned access token with the S3 endpoint removed.

```javascript
informat.storage.createS3FileToken(path, expireTime)
```

| Parameter  | Type    | Description                        |
|------------|---------|-------------------------------------|
| path       | String  | Shared storage file path            |
| expireTime | Integer | Expiration time, unit: seconds      |


# createFileDownloadUrl
Create a file download URL

```javascript
informat.storage.createFileDownloadUrl(fileToken)
```

| Parameter | Type   | Description       |
|-----------|--------|-------------------|
| fileToken | String | File access TOKEN |


# createFileDownloadUrl
Create a file download URL

```javascript
informat.storage.createFileDownloadUrl(fileToken, host)
```

| Parameter | Type   | Description                                                        |
|-----------|--------|--------------------------------------------------------------------|
| fileToken | String | File access TOKEN                                                  |
| host      | String | Web service address, can be empty, defaults to external access URL |


## convertFormat
Document format conversion

```javascript
informat.storage.convertFormat(sourcePath,targetPath,setting)
```
| Parameter  | Type              | Description                              |
|------------|-------------------|------------------------------------------|
| sourcePath | String            | Path of the document to convert          |
| targetPath | String            | Target document path after conversion    |
| setting    | `ConvertSetting`  | Conversion settings                      |

## convertFormat
Document format conversion

```javascript
informat.storage.convertFormat(sourcePath,targetPath,onlyofficeServiceUrl,setting)
```
| Parameter            | Type              | Description                                                                  |
|----------------------|-------------------|------------------------------------------------------------------------------|
| sourcePath           | String            | Path of the document to convert                                              |
| targetPath           | String            | Target document path after conversion                                        |
| onlyofficeServiceUrl | String            | OnlyOffice service URL, defaults to the file preview URL configured in admin |
| setting              | `ConvertSetting`  | Conversion settings                                                          |

`ConvertSetting` structure is as follows
```js
{
    async:Boolean,// Defines the conversion request type: asynchronous or not
    fileType:String,// Defines the type of the document file to be converted
    outputtype:String,// Defines the resulting converted document type
    password:String,// Defines the password for the file if the document is password-protected
    region:String,// Defines the default display format for currency, date and time when converting from spreadsheet format to pdf. Set using four-letter (en-US, fr-FR, etc.) language codes. Default value is en-US.
    title:String,// Defines the converted file name
    spreadsheetLayout:{
        fitToHeight:Integer,// Sets the height of the conversion area in number of pages. Default value is 0.
        fitToWidth:Integer,// Sets the width of the conversion area in number of pages. Default value is 0.
        gridLines:Boolean,// Allows including or excluding grid lines in the output PDF file. Default value is false.
        headings:Boolean,// Allows including or excluding headings in the output PDF file. Default value is false.
        ignorePrintArea:Boolean,// Determines whether to ignore the print area selected for the spreadsheet file. Default value is true.
        margins:{
            bottom:String,// Sets the bottom margin of the output PDF file. Default value is 19.1mm.
            right:String,// Sets the right margin of the output PDF file. Default value is 19.1mm.
            left:String,// Sets the left margin of the output PDF file. Default value is 19.1mm.
            top:String,// Sets the top margin of the output PDF file. Default value is 19.1mm.
        },
        orientation:String,// Sets the orientation of the output PDF file. Possible values are landscape, portrait. Default value is portrait.
        pageSize:{
            height:String,// Sets the page height of the output PDF file. Default value is 297mm.
            width:String// Sets the page width of the output PDF file. Default value is 210mm.
        },
        scale:Integer,// Allows setting the scale of the output PDF file. Default value is 100.
    },
    thumbnail:{
        /*
        Defines the mode to fit the image to the specified height and width. Supported values: 0 - stretch the file to fit the height and width; 1 - keep the image aspect ratio; 2 - in this case, the width and height settings are not used. Instead, the metric dimensions of the page are converted to pixels at 96dpi. For example, an A4 (210x297mm) page will become an image with dimensions 794x1123px. Default value is 2.
        */
        aspect:Integer,
        /*
        Defines whether to generate thumbnails for only the first page or for all document pages.
        If false, a zip archive containing thumbnails of all pages will be created.
        Default value is true.
        */
        first:Boolean,
        height:Integer,// Defines the thumbnail height in pixels. Default value is 100.
        width:Integer,// Defines the thumbnail width in pixels. Default value is 100.
    }
}
```
### Supported File Conversion Table

**Symbol Legend**:
- ⬤ indicates the format conversion is fully supported
- 〇 indicates the format conversion is not supported

#### Text Document File Formats

| Input Format | bmp | docm | docx | dotm | dotx | epub | fb2 | gif | html | jpg | odt | ott | pdf | pdfa | png | rtf | txt |
|----------|-----|------|------|------|------|------|-----|-----|------|-----|-----|-----|-----|------|-----|-----|-----|
| djvu     | ⬤  | 〇   | 〇   | 〇   | 〇   | 〇   | 〇  | ⬤  | 〇   | ⬤  | 〇  | 〇  | ⬤  | ⬤   | ⬤  | 〇  | 〇  |
| doc      | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  |
| docm     | ⬤  | 〇   | ⬤   | ⬤   | ⬤   | ⬤   | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  |
| docx     | ⬤  | ⬤   | 〇   | ⬤   | ⬤   | ⬤   | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  |
| dot      | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  |
| dotm     | ⬤  | ⬤   | ⬤   | 〇   | ⬤   | ⬤   | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  |
| dotx     | ⬤  | ⬤   | ⬤   | ⬤   | 〇   | ⬤   | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  |
| epub     | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | 〇   | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  |
| fb2      | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   | 〇  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  |
| fodt     | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  |
| htm      | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  |
| html     | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   | ⬤  | ⬤  | 〇   | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  |
| hwp      | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  |
| hwpx     | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  |
| mht      | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  |
| mhtml    | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  |
| odt      | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   | ⬤  | ⬤  | ⬤   | ⬤  | 〇  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  |
| ott      | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   | ⬤  | ⬤  | ⬤   | 〇  | ⬤  | 〇  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  |
| oxps     | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  |
| pages    | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  |
| pdf      | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  | 〇  | ⬤   | ⬤  | ⬤  | ⬤  |
| rtf      | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | 〇  | ⬤  |
| stw      | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  |
| sxw      | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  |
| txt      | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | 〇  |
| wps      | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  |
| wpt      | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  |
| xml      | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  |
| xps      | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤  | ⬤  |

#### Spreadsheet File Formats

| Input Format | bmp | csv | gif | jpg | ods | ots | pdf | pdfa | png | xlsm | xlsx | xltm | xltx |
|----------|-----|-----|-----|-----|-----|-----|-----|------|-----|------|------|------|------|
| csv      | ⬤  | 〇  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   |
| et       | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   |
| ett      | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   |
| fods     | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   |
| numbers  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   |
| ods      | ⬤  | ⬤  | ⬤  | ⬤  | 〇  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   |
| ots      | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | 〇  | ⬤  | ⬤   | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   |
| sxc      | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   |
| xls      | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   |
| xlsb     | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   |
| xlsm     | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | 〇   | ⬤   | ⬤   | ⬤   |
| xlsx     | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤   | 〇   | ⬤   | ⬤   |
| xlt      | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   |
| xltm     | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤   | ⬤   | 〇   | ⬤   |
| xltx     | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤   | ⬤   | ⬤   | 〇   |
| xml      | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   |

#### Presentation File Formats

| Input Format | bmp | gif | jpg | odp | otp | pdf | pdfa | png | potm | potx | ppsm | ppsx | pptm | pptx |
|----------|-----|-----|-----|-----|-----|-----|------|-----|------|------|------|------|------|------|
| dps      | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   |
| dpt      | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   |
| fodp     | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   |
| key      | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   |
| odp      | ⬤  | ⬤  | ⬤  | 〇  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   |
| otp      | ⬤  | ⬤  | ⬤  | ⬤  | 〇  | ⬤  | ⬤   | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   |
| pot      | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   |
| potm     | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | 〇   | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   |
| potx     | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤   | 〇   | ⬤   | ⬤   | ⬤   | ⬤   |
| pps      | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   |
| ppsm     | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤   | ⬤   | 〇   | ⬤   | ⬤   | ⬤   |
| ppsx     | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤   | ⬤   | ⬤   | 〇   | ⬤   | ⬤   |
| ppt      | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   |
| pptm     | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | 〇   | ⬤   |
| pptx     | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   | 〇   |
| sxi      | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤  | ⬤   | ⬤  | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   | ⬤   |

**Examples:**

**Convert a file from docx format to pdf format**
```js
informat.storage.convertFormat('table/field/fileId','table/field/fileId_converted',{
    "filetype": "docx",
    "outputtype": "pdf",
    "title": "test.pdf",
})
```

**Convert a file from docx format to png thumbnail**
```js
informat.storage.convertFormat('table/field/fileId','table/field/fileId_converted',{
    "filetype": "docx",
    "outputtype": "png",
    "title": "test.png",
    "thumbnail": {
        "aspect": 0,
        "first": true,
        "height": 150,
        "width": 100
    }
})
```
**Convert a file from xlsx format to pdf format**
```js
informat.storage.convertFormat('table/field/fileId','table/field/fileId_converted',{
    "filetype": "xlsx",
    "outputtype": "pdf",
    "title": "test.pdf",
    "region": "en-US",
    "spreadsheetLayout": {
        "ignorePrintArea": true,
        "orientation": "portrait",
        "fitToWidth": 0,
        "fitToHeight": 0,
        "scale": 100,
        "headings": false,
        "gridLines": false,
        "pageSize": {
            "width": "210mm",
            "height": "297mm"
        },
        "margins": {
            "left": "17.8mm",
            "right": "17.8mm",
            "top": "19.1mm",
            "bottom": "19.1mm"
        }
    }
})
```


## convertFormatFromURL
Convert document format from a remote URL

```javascript
informat.storage.convertFormatFromURL(sourceURL,targetPath,setting)
```
| Parameter  | Type              | Description                           |
|------------|-------------------|---------------------------------------|
| sourceURL  | String            | Remote URL of the document to convert |
| targetPath | String            | Target document path after conversion |
| setting    | `ConvertSetting`  | Conversion settings                   |

Below is an example of converting a docx document to pdf format via a remote document URL
```js
informat.storage.convertFormatFromURL('https://xxx.xxx.xx/file/example.docx','table/field/example.pdf',{
    "filetype": "docx",
    "outputtype": "pdf",
    "title": "test.pdf",
})
```

## convertFormatFromURL
Convert document format from a remote URL

```javascript
informat.storage.convertFormatFromURL(sourceURL, targetPath, onlyofficeServiceUrl, setting)
```
| Parameter            | Type              | Description                                                                  |
|----------------------|-------------------|------------------------------------------------------------------------------|
| sourceURL            | String            | Remote URL of the document to convert                                        |
| targetPath           | String            | Target document path after conversion                                        |
| onlyofficeServiceUrl | String            | OnlyOffice service URL, defaults to the file preview URL configured in admin |
| setting              | `ConvertSetting`  | Conversion settings                                                          |

Below is an example of converting a docx document to pdf format via a remote document URL
```js
informat.storage.convertFormatFromURL('https://xxx.xxx.xx/file/example.docx','table/field/example.pdf',null,{
    "filetype": "docx",
    "outputtype": "pdf",
    "title": "test.pdf",
})
```

## getContent
Get file string content from shared storage

```javascript
informat.storage.getContent(path)
```
| Parameter | Type   | Description         |
|-----------|--------|---------------------|
| path      | String | Shared storage path |

```js
informat.storage.getContent('d97x4vygqxxt4/h9fdepr09gw2h/wddvtgi7md7x47du59sd0.png');
```

## getBase64Content
Get file base64-encoded content from shared storage

```javascript
informat.storage.getBase64Content(path)
```
| Parameter | Type   | Description         |
|-----------|--------|---------------------|
| path      | String | Shared storage path |

```js
informat.storage.getBase64Content('d97x4vygqxxt4/h9fdepr09gw2h/wddvtgi7md7x47du59sd0.png');
```
