# informat.word Word Operations

## Overview
Use the `informat.word` object to generate a new Word file using a Docx format Word document template and data. This is very useful in scenarios such as generating contracts, reports, certificates, etc.

> File paths must be in the local sandbox path. For more information about file paths, refer to [informat.file](/guide/script/file.md)

All tags start with `{{` and end with `}}`. Tags can appear in any position, including headers, footers, inside tables, text boxes, etc. Table layouts can be used to design many excellent professional documents, so table layouts are recommended. Templates follow a "what you see is what you get" design - the styles of templates and tags will be fully preserved.

A tag consists of two pairs of curly braces. `{{title}}` is a tag, `{{?title}}` is also a tag. "title" is the name of this tag, and the question mark identifies the tag type.
## Text Tag
The format of a text tag is `{{text}}`. The rendered content will be the value of the `text` variable.
## Image Tag
The format of an image tag is `{{@pic}}`. The rendered content will be the image described in `pic`. The `pic` object needs to be generated using the informat.word.createPicture() method.
Example data
```javascript
{
    pic:informat.word.createPicture({
        path:'logo.png'
    })
}
```
Template
```
{{@pic}}
```

## List Tag
The format of a list tag is `{{*var}}`. The rendered content will be a list.
## Block Pair
A block pair consists of two tags: the opening tag identified with ? and the closing tag identified with /: `{{?sections}}{{/sections}}`
A block pair can contain multiple images, tables, paragraphs, lists, charts, etc. between the opening and closing tags. The opening and closing tags can span multiple paragraphs or be in the same paragraph. However, if a block pair is used inside a table, the opening and closing tags must be within the same cell, because the rendering behavior across multiple cells is undefined.
Block pairs are very useful when processing a series of document elements. Document elements within a block pair can be rendered zero times, once, or N times, depending on the value of the block pair.
- False or empty collection: Hides all document elements in the block
- Not false and not a collection: Displays the document elements in the block, rendered once
- Non-empty collection: Iteratively renders the document elements in the block based on the size of the collection

***If the value of the block pair is null, false, or an empty collection, all document elements within the block will not be displayed. This is equivalent to the condition of an if statement being false.***
Input data
```json
{
    "value": false
}
```

Template
```text
Test{{?value}}will not appear{{/value}}
```

Rendered result
```javascript
Test
```

***If the value of the block pair is not null, not false, and not a collection, all document elements within the block will be rendered once. This is equivalent to the condition of an if statement being true.***
Input data
```json
{
  "person": { "name": "张三" }
}
```

Template
```text
{{?person}}
Hi {{name}}!
{{/person}}
```

Rendered result
```text
Hi 张三!
```

***If the value of the block pair is a non-empty collection, the document elements in the block will be iteratively rendered once or N times depending on the size of the collection, similar to a foreach loop.***
Input data
```json
{
  "users": [
    { "name": "张三" },
    { "name": "李四" },
    { "name": "王五" }
  ]
}
```

Template
```text
{{?users}}
{{name}}
{{/users}}
```

Rendered result
```javascript
张三
李四
王五
```

## Built-in Variables in Block Pair Loops

| Variable      | Type    | Description                                                    |
|---------------|---------|----------------------------------------------------------------|
| _index        | Integer | Returns the zero-based index of the current iteration          |
| _is_first     | Boolean | Identifies whether the loop item is the first item in the current iteration |
| _is_last      | Boolean | Identifies whether the loop item is the last item in the current iteration |
| _has_next     | Boolean | Identifies whether the loop item has a next item               |
| _is_even_item | Boolean | Identifies whether the loop item is an odd item at interval 1 in the current iteration |
| _is_odd_item  | Boolean | Identifies whether the loop item is an even item at interval 1 in the current iteration |
| #this         | Object  | References the current object. Since # conflicts with the existing table tag identifier, the = identifier must be used in text tags to output text |

Example data
```json
{
  "users": [
    "张三",
    "李四"
  ]
}
```
Template
```
{{?users}}
{{_index + 1}}. {{=#this}}
{{/users}}
```
Result
```
1. 张三
2. 李四
```

## Table Row Loop
When declaring a variable, adding a `-` symbol before the variable name enables the table row loop feature. Place {{list}} on the same row as the loop row. The loop row sets the tags and content to be looped.
Note that tags should use [] at this point to implement row looping in tables. Here is an example:

Example data
```json
{
  "-users": [
    {"id":1,"name":"张三","age":18},
    {"id":2,"name":"李四","age":20},
    {"id":3,"name":"王五","age":30}
  ]
}
```
Template

| No. | Name | Age |
|--|--|--|
|`{{users}}`[_index+1]|[name]|[age]|

Result

| No. | Name | Age |
|--|--|--|
|1|张三|18|
|2|李四|20|
|3|王五|30|


## Table Column Loop
When declaring a variable, adding a `|` symbol before the variable name enables the table column loop feature. Place {{list}} in the loop column. The rest is similar to row looping. Here is an example:

Example data
```json
{
  "|users": [
    {"id":1,"name":"张三","age":18},
    {"id":2,"name":"李四","age":20},
    {"id":3,"name":"王五","age":30}
  ]
}
```

| User |
|--|
|`{{users}}`[_index+1]|
|[name]|
|[age]|

Result

| User | User | User |
|--|--|--|
|1|2|3|
|张三|李四|王五|
|18|20|30|


## createWithTemplate
Generate a Word file using a template and data
```javascript
informat.word.createWithTemplate(template,file,data)
```

| Parameter | Type   | Description                           |
|-----------|--------|---------------------------------------|
| template  | String | Path of the template file in the local sandbox |
| file      | String | Path of the generated file in the local sandbox |
| data      | Object | Data passed to the template           |

## createPicture
Generate image data to be inserted into a Word document
```javascript
informat.word.createPicture(pic)
```

| Parameter | Type        | Description        |
|-----------|-------------|--------------------|
| pic       | WordPicture | Image configuration |

***Return Value: Returns the template data for inserting an image***

The structure of WordPicture is as follows:
```text
{
    url:String,// URL of the image
    path:String,// Path of the image in the local sandbox
    storagePath:String,// Path of the image in shared storage
    width:Integer,// Width of the image. If not set, the original size is used
    height:Integer,// Height of the image. If not set, the original size is used
}
```
> Both `width` and `height` must be set together when specifying image size

**Example**

The following is an example of generating a Word file using a Word template and data:

```javascript
const data = {
    text: 'Text data',
    list: [
        { id: 1, name: '张三' },
        { id: 2, name: '李四' },
        { id: 3, name: '王五' }
    ],
    pic: informat.word.createPicture({
        path: 'logo.png'
    })
}
informat.word.createWithTemplate('template.docx', 'out.docx', data);
```

## Replacing Images in Word
The reference image tag is text: `{{var}}`. The tag location is at: Format Picture - Alt Text - Title or Description (in newer versions of Microsoft Office, the tag location is at: Edit Alt Text - Alt Text).

![Operation](images/word-1.png)
The reference image tag only replaces the image without changing the image size and layout. The data model is the same as the image tag.

::: tip Note
The alt text image tag does not need the `@` symbol
:::
