# informat.website Website Resource Hosting

## Overview

Use the `informat.website` object to perform operations related to resource and component designer modules. Website resource storage is similar to a file system directory structure.

## WebsiteResource Structure

```ts
{
    name:String;//Resource file name
    path:String;//Full path of the resource,
    isDirectory:Boolean;//Whether it is a directory
}
```

## list

Get the resource list of a website by parent directory

```javascript
informat.website.list(moduleId, path, recursion)
```

| Parameter        | Type      | Description                                       |
|-----------|---------|------------------------------------------|
| moduleId  | String  | Website module identifier                                 |
| path      | String  | Resource path. If path is null, returns resources under the root directory              |
| recursion | Boolean | Whether to recursively return all sub-levels. If recursion is false, only the first-level subdirectories are returned |

**Return Value**
Type is Array<[WebsiteResource](/guide/script/model.md#websiteresource)>
Returns the resource list

**Example - Get all resources of a website resource hosting module**

:::code-group

```js[Call]
informat.website.list('scriptResource',null,true);
```

```json[Return Value]
[
  {
    "directory": true,
    "isDirectory": true,
    "name": "mpp",
    "path": "mpp"
  },
  {
    "directory": false,
    "isDirectory": false,
    "name": "软件开发.mpp",
    "path": "mpp/软件开发.mpp"
  },
  {
    "directory": true,
    "isDirectory": true,
    "name": "excel",
    "path": "excel"
  },
  {
    "directory": false,
    "isDirectory": false,
    "name": "excelFileToDataList.xlsx",
    "path": "excel/excelFileToDataList.xlsx"
  },
  {
    "directory": true,
    "isDirectory": true,
    "name": "word",
    "path": "word"
  },
  {
    "directory": false,
    "isDirectory": false,
    "name": "template.docx",
    "path": "word/template.docx"
  },
  {
    "directory": false,
    "isDirectory": false,
    "name": "logo.png",
    "path": "word/logo.png"
  }
]
```

:::

## getByPath

Get a resource by path

```javascript
informat.website.getByPath(moduleId, path)
```

| Parameter       | Type     | Description       |
|----------|--------|----------|
| moduleId | String | Website module identifier |
| path     | String | Resource path     |

**Return Value**
Type is [WebsiteResource](/guide/script/model.md#websiteresource)
Returns the resource

**Example**

:::code-group

```js[Call]
informat.website.getByPath('scriptResource','word/logo.png');;
```

```json[Return Value]
{
  "directory": false,
  "fileId": "238aa17dbf054a11a7573f8d80d27c08.png",
  "id": "jy64cjyec9lnq",
  "isDirectory": false,
  "name": "logo.png",
  "path": "word/logo.png"
}
```

:::

## download

Download a resource to local file shared storage

```javascript
informat.website.download(moduleId, path, localPath)
```

| Parameter        | Type     | Description         |
|-----------|--------|------------|
| moduleId  | String | Website module identifier   |
| path      | String | Resource path       |
| localPath | String | Path in local storage sandbox |

**Example**

```javascript
// Download the word/logo.png resource from the specified website module to the local file localPath
informat.website.download('scriptResource', 'word/logo.png', 'local/logo.png');
```

## getStroagePath

Get the shared storage path of a website resource by its resource path

```javascript
informat.website.getStroagePath(moduleId, path)
```

| Parameter       | Type     | Description       |
|----------|--------|----------|
| moduleId | String | Website module identifier |
| path     | String | Resource path     |

**Example**

:::code-group

```js[Call]
informat.website.getStroagePath('scriptResource','word/logo.png');
```

```json[Return Value]
"icxt9rsd1f0ai/demoApp/oryesvrjpy6rp/238aa17dbf054a11a7573f8d80d27c08.png"
```

:::

**Return Value Explanation**

- icxt9rsd1f0ai: Team ID
- demoApp: Application identifier
- oryesvrjpy6rp: Website resource hosting module ID
- 238aa17dbf054a11a7573f8d80d27c08.png: Resource file ID
