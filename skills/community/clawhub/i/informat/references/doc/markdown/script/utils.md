# informat.utils Other Utility Functions

## Overview

Use `informat.utils` to perform utility operations

***

## getPinyin

Returns pinyin

```javascript
informat.utils.getPinyin(str, separator)
```

| Parameter | Type   | Description          |
|-----------|--------|----------------------|
| str       | String | String to convert    |
| separator | String | Separator            |

#### Return Value

Returns pinyin

:::code-group

```js[Call]
informat.utils.getPinyin('你好，世界',',');
```

```json[Return Value]
"ni,hao,，,shi,jie"
```

:::tip
Note: Symbols will not be parsed and will be preserved in the output, such as the comma above
:::

## getShortPinyin

Returns pinyin initials

```javascript
informat.utils.getShortPinyin(str, separator)
```

| Parameter | Type   | Description          |
|-----------|--------|----------------------|
| str       | String | String to convert    |
| separator | String | Separator            |

#### Return Value

Returns pinyin initials

***Example***

:::code-group

```js[Call]
informat.utils.getShortPinyin('你好,世界',',');
```

```json[Return Value]
"n,h,，,s,j"
```

:::

## randomUUID

Returns a random UUID

```javascript
informat.utils.randomUUID()
```

#### Return Value

Returns a random UUID

Example: Randomly generate a UUID

:::code-group

```js[Call]
informat.utils.randomUUID();
```

```json
"abeb540f-b4ff-45e3-89a0-151ed4d38a40"
```

:::

## getEnv

Returns system environment variables

```javascript
informat.utils.getEnv()
```

#### Return Value Type `Object<String,String>`

Returns system environment variables

Example: Returns the current user's system environment variables
:::code-group

```js[Call]
informat.utils.getEnv();
```

```json[Return Value]
{
  "PATH": "/usr/local/bin:/usr/bin",
  "LESSOPEN": "||/usr/bin/lesspipe.sh %s",
  "SHELL": "/bin/bash",
  "HISTSIZE": "3000",
  "SSH_TTY": "/dev/pts/4"
}
```

:::

## toJSON

Converts an object to a JSON string

```javascript
informat.utils.toJSON(obj)
```

| Parameter | Type   | Description          |
|-----------|--------|----------------------|
| obj       | Object | Object to convert    |

#### Return Value

Returns a JSON string

Example: Query a data table record and convert the result to a JSON string

:::code-group

```js[Call]
let record=informat.table.queryById('staffs','yhg8b23ej2gt6');
informat.utils.toJSON(record);
```

```json[Return Value]
{
  "id": "yhg8b23ej2gt6",
  "seq": 1,
  "createTime": 1700796135362,
  "grade": 5,
  "name": "李四",
  "updateUser_avatar": "pic7.png",
  "createUser": "skydu",
  "createUser_avatar": "79a487eb7f384321bfaed16eb9e020d8.jpg",
  "deptRel": "fh1snm1k18kqc",
  "age": 28,
  "status": "onjob"
}
```

:::

***

## html2text

Converts HTML formatted text to plain text

```javascript
informat.utils.html2text(html)
```

| Parameter | Type   | Description        |
|-----------|--------|--------------------|
| html      | String | HTML formatted text |

#### Return Value

Returns plain text

Example:

:::code-group

```js[Call]
let html='<html><script></script><body><h1>Hello World</h1></body>'
informat.utils.html2text(html); 
```

```json[Return Value]
"Hello World"
```

:::

## stringToBytes

Converts a string to a byte array

```javascript
informat.utils.stringToBytes(str, charset)
```

| Parameter | Type   | Description                              |
|-----------|--------|------------------------------------------|
| str       | String | String to convert                        |
| charset   | String | Charset, options include UTF-8, ISO-8859-1, GBK, etc. |

#### Return Value

Returns `Array<Byte>`

**Example**

:::code-group

```js[Call]
var bytes=informat.utils.stringToBytes('测试','UTF-8');
bytes.forEach(item=>{
    console.log(item)
})
```

```js[Return Value]
-26
-75 
-117
-24 
-81
-107
```

:::

## bytesToString

Converts a byte array to a String

```javascript
informat.utils.bytesToString(data, charset)
```

| Parameter | Type          | Description                              |
|-----------|---------------|------------------------------------------|
| data      | `Array<Byte>` | Byte array to convert                    |
| charset   | String        | Charset, options include UTF-8, ISO-8859-1, GBK, etc. |

#### Return Value

Returns `String`

**Example**

:::code-group

```js[Call]
let bytes=informat.utils.stringToBytes('测试','UTF-8');
informat.utils.bytesToString(bytes, 'UTF-8');
```

```json[Return Value]
测试
```

:::

## jsonDiff

Calculates the difference between two JSON strings

```javascript
informat.utils.jsonDiff(jsonA, jsonB)
```

| Parameter | Type   | Description    |
|-----------|--------|----------------|
| jsonA     | String | JSON string a  |
| jsonB     | String | JSON string b  |

#### Return Value

Returns `String`

**Example**

:::code-group

```js[Call]
informat.utils.jsonDiff('{\"a\": 0,\"b\": [1,2]}','{\"b\": [1,2,0]}');
```

```json[Return Value]
[{"op":"move","path":"/b/-","from":"/a"}] 
```

:::

## jsonPatch

JSON patch

```javascript
informat.utils.jsonPatch(json, patch)
```

| Parameter | Type   | Description   |
|-----------|--------|---------------|
| json      | String | JSON string   |
| patch     | String | JSON patch    |

#### Return Value

Returns `String`

**Example**

:::code-group

```js[Call]
informat.utils.jsonPatch('{\"a\": 0,\"b\": [1,2]}','[{"op":"move","path":"/b/-","from":"/a"}]');
```

```json[Return Value]
newJson {"b":[1,2,0]}
```

:::

## urlEncode

URL encoding, converts special characters to a format that can be safely transmitted in URLs

```javascript
informat.utils.urlEncode(url)
```

| Parameter | Type   | Description |
|-----------|--------|-------------|
| url       | String | URL address |

#### Return Value

Returns `String`

**Example**

:::code-group

```js[Call]
const originalUrl = "https://www.example.com/search?q=hello world&category=programming";
informat.utils.urlEncode(originalUrl);
```

```json[Return Value]
https%3A%2F%2Fwww.example.com%2Fsearch%3Fq%3Dhello+world%26category%3Dprogramming
```

:::

## urlDecode

URL decoding, restores a URL-encoded string to its original form

```javascript
informat.utils.urlDecode(encodedUrl)
```

| Parameter  | Type   | Description        |
|------------|--------|--------------------|
| encodedUrl | String | Encoded URL address |

#### Return Value

Returns `String`

**Example**

:::code-group

```js[Call]
const encodedUrl = "https%3A%2F%2Fwww.example.com%2Fsearch%3Fq%3Dhello%20world%26category%3Dprogramming";
informat.utils.urlDecode(encodedUrl);
```

```json[Return Value]
https://www.example.com/search?q=hello world&category=programming
```

:::

## escape

String escaping

```javascript
informat.utils.escape(content)
```

| Parameter | Type   | Description |
|-----------|--------|-------------|
| content   | String | String      |

#### Return Value

Returns `String`

**Example**

:::code-group

```js[Call]
// Assume the input string contains special characters that need to be escaped
let inputString = 'This is a <div> tag';
informat.utils.escape(inputString);
```

```[Return Value]
This%20is%20a%20%3cdiv%3e%20tag
```

:::

## unescape

String unescaping

```javascript
informat.utils.unescape(escapedString)
```

| Parameter     | Type   | Description      |
|---------------|--------|------------------|
| escapedString | String | Escaped string   |

#### Return Value

Returns `String`

**Example**

:::code-group

```js[Call]
// Assume the input string contains escaped characters that need to be unescaped
var escapedString = 'This%20is%20a%20%3cdiv%3e%20tag';
informat.utils.unescape(escapedString);
```

```json[Return Value]
This is a <div> tag
```

:::

## js2java

Converts a JavaScript object to a Java object

```javascript
informat.utils.js2java(jsObject)
```

| Parameter | Type   | Description       |
|-----------|--------|-------------------|
| jsObject  | Object | JavaScript object |

#### Return Value

Returns `Object`

**Example**

:::code-group

```js[Call]
informat.utils.js2java({
    id:"1",
    name:"test"
});
```

```json[Return Value]
{name=test, id=1}
```

:::

***

## sleep

Pauses the current thread

```javascript
informat.utils.sleep(millis)
```

| Parameter | Type    | Description  |
|-----------|---------|--------------|
| millis    | Integer | Milliseconds |

**Example**

```javascript
informat.utils.sleep(5000);// Sleep for 5 seconds
```

***

## htmlToMarkdown

Converts HTML to Markdown

```javascript
informat.utils.htmlToMarkdown(html)
```

| Parameter | Type   | Description  |
|-----------|--------|--------------|
| html      | String | HTML content |

**Example**

:::code-group

```js[Call]
let html='<h3>Hello Informat!</h3>';
informat.utils.htmlToMarkdown(html);
```

```json[Return Value]
### Hello Informat!
```

:::

***

## markdownToHtml

Converts Markdown to HTML

```javascript
informat.utils.markdownToHtml(markdown)
```

| Parameter | Type   | Description      |
|-----------|--------|------------------|
| markdown  | String | Markdown content |

**Example 1 Text**

:::code-group

```js[Call]
let markdown='This is *Sparta*';
informat.utils.markdownToHtml(markdown);
```

```json[Return Value]
<p>This is <em>Sparta</em></p>
```

:::

**Example 2 Table**

:::code-group

```js[Call]
let md = `| Title1 | Title2 |
|---|---|
|Content1|Content2|
`
informat.utils.markdownToHtml(md);
```

```json[Return Value]
<table> <thead> <tr><th>Title1</th><th>Title2</th></tr> </thead> <tbody> <tr><td>Content1</td><td>Content2</td></tr> </tbody> </table>
```

:::
