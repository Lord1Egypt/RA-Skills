# informat.xml XML Operations

## Overview

Use `informat.xml` to perform XML read and write operations


## parse

Read XML content and return a Document object. If the XML content is null or an empty string, null will be returned. If the content structure is not valid XML format, an exception will be thrown

```javascript
informat.xml.parse(xml)
```

| Parameter | Type     | Description |
|-----|--------|-------|
| xml | String | XML content |

**Return Value**
Type is `org.w3c.dom.Document`

For w3c Document API methods, refer to https://docs.oracle.com/javase/7/docs/api/org/w3c/dom/Document.html

Here is an example

```js
let doc = informat.xml.parse("<root name='test'>text content</root>");
let name = doc.getDocumentElement().getAttribute("name");
console.log(name);//test
```

## createDocument

Create a new Document object

```javascript
informat.xml.createDocument()
```

**Return Value**
Type is `org.w3c.dom.Document`

For w3c Document API methods, refer to https://docs.oracle.com/javase/7/docs/api/org/w3c/dom/Document.html


## doc2xml

Convert a Document object to an XML string

```javascript
informat.xml.doc2xml(doc, config)
```

| Parameter | Type       | Description |
|--------|----------|---------|
| doc    | Document | XML document object |
| config | Config   | Output configuration |

The config object structure is as follows

```
{
    doctypeSystem:String,//
    doctypePublic:String
    indent:Boolean,// Defaults to false, whether to indent XML
    indentAmount:Integer,// Indentation length, defaults to 0
    standalone:Boolean, standalone value in the XML element
    version:String, version value in the XML element
    encoding:String, encoding value in the XML element
    omitXmlDeclaration:Boolean,// Whether to omit the XML header
}
```

**Return Value**
Type is `String`

Here is an example

:::code-group
```js[Call]
let doc = informat.xml.createDocument();
let rootElement = doc.createElement("company");
doc.appendChild(rootElement);
doc.createElement("staff");
rootElement.appendChild(doc.createElement("staff"));
//
let config = {};
config.doctypeSystem = "doctype system";
config.doctypePublic = "doctype public";
config.indent = true;
config.indentAmount=2;
config.standalone = false;
config.version = "1.1";
config.encoding = "utf-8";
//
let xml = informat.xml.doc2xml(doc, config);
console.log(xml);
```

```xml[Return Value]
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE company PUBLIC "doctype public" "doctype system">
<company>
    <staff/>
</company>
```
:::

If `config` is set as follows

```
config.omitXmlDeclaration=true;
config.indent=true;
```

The output will be

```xml
<!DOCTYPE company PUBLIC "doctype public" "doctype system">
<company>
    <staff/>
</company>
```
