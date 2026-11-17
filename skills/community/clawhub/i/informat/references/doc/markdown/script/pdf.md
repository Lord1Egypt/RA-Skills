# informat.pdf PDF File Operations

## Overview

Use the `informat.pdf` object to read PDF files

::: info Reference
The file path must be in the local sandbox path. For file path details, refer to [informat.file](/guide/script/file.md)
:::

### toImages

Use toImages to convert a PDF to a base64 image array

| Parameter | Type     | Description |
| ---- | -------- | -------------------- |
| path | `String` | Path of the PDF file in the sandbox |

**Return Value**
base64 file stream

**_Example_**

```js
informat.pdf.toImages(localPath);
```

### getText

Use getText to get the text content of a PDF file

| Parameter | Type     | Description |
| ---- | -------- | -------------------- |
| path | `String` | Path of the PDF file in the sandbox |

**Return Value**
json

**_Example_**

```js
informat.pdf.getText(localPath);
```

### Automation: Upload PDF File and Parse with AI to Insert Data into Table

Please refer to [PDF Intelligent Parsing](/guide/aiagent/agent_pdf.md)
