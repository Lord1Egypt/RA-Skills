# informat.excel Excel File Operations

## Overview

Use the `informat.excel` object to perform Excel file read and write operations

::: info Reference
The file path must be in the local sandbox path. For file path details, refer to [informat.file](/guide/script/file.md)
:::

### openExistFile

Open an existing Excel file in the sandbox environment
::: warning Note
An exception will be thrown if the file does not exist
:::

```javascript
informat.excel.openExistFile(file)
```

| Parameter | Type       | Description |
|------|----------|----------------|
| file | `String` | File path in the app sandbox environment |

**Return Value**

Returns a [Workbook](/guide/script/excel.md#workbook) object

**Example**

```javascript
informat.excel.openExistFile('gzb.xlsx')
```

---

### openExistStorageFile

Open an existing Excel file stored in shared storage
::: warning Note
An exception will be thrown if the file does not exist
:::

```javascript
informat.excel.openExistStorageFile(file)
```

| Parameter | Type       | Description |
|------|----------|----------------|
| file | `String` | File path in shared storage |

**Return Value**

Returns a [Workbook](/guide/script/excel.md#workbook) object

**Example**

```javascript
informat.excel.openExistStorageFile('automatic/n3uiy48tig3ch538lwxej.xlsx')
```

---

### openNewFile

Create a new Excel file

```javascript
informat.excel.openNewFile(file)
```

::: tip
If the file exists, saving will overwrite the original file content
:::

| Parameter | Type       | Description |
|------|----------|----------------|
| file | `String` | File path in the app sandbox environment |

**Return Value**

Returns a [Workbook](/guide/script/excel.md#workbook) object

**Example**

```javascript
informat.excel.openNewFile('gzb2.xlsx')
```

---

### openWithTemplate

Create a Workbook based on a [template](./excel-easyPoi).

```javascript
informat.excel.openWithTemplate(file, templateFile, data);
```

| Parameter      | Type       | Description |
|--------------|----------|-------------|
| file         | `String` | Generated Excel file |
| templateFile | `String` | Template file path |
| data         | `Object` | Variables passed to the template file |

**Return Value**

Returns a [Workbook](/guide/script/excel.md#workbook) object

---

### openWithTemplateWithSheets

Create a Workbook based on a multi-sheet [template](./excel-easyPoi).

```javascript
informat.excel.openWithTemplateWithSheets(file, templateFile, sheetNums, data);
```

::: tip
If sheetNums is empty, all worksheets will be exported.
:::

| Parameter      | Type               | Description |
|--------------|------------------|---------------------------------------|
| file         | `String`         | Generated Excel file |
| templateFile | `String`         | Template file path |
| sheetNums    | `Array<Integer>` | Worksheet number list, starting from 0; to export only the 2nd and 3rd worksheets, enter [1,2] |
| data         | `Object`         | Variables passed to the template file |

**Return Value**

Returns a [Workbook](/guide/script/excel.md#workbook) object

[Template Expressions](./excel-easyPoi)

### createTemplatePicture

Create a template picture object

```javascript
informat.excel.createTemplatePicture(pic);
```

| Parameter | Type                     | Description |
|-------|------------------------|------|
| image | `ExcelTamplatePicture` | Picture configuration |

**Return Value**

Returns a picture for use in templates

**Example**

::: code-group

```javascript [Picture]
informat.excel.createTemplatePicture({
    type: 'file', // Local storage
    content: 'pathto/img.jpg', // File path in local storage
    width: 100, // Width
    height: 100, // Height
});

informat.excel.createTemplatePicture({
    type: 'storage', // Shared storage
    content: 'pathto/img.jpg', // File path in shared storage
});
```

```javascript [Barcode]
informat.excel.createTemplatePicture({
    type: 'barcode', // Barcode
    content: '1234557', // Content
    width: 100, // Width
    height: 100 // Height
});
```

```javascript [QR Code]
informat.excel.createTemplatePicture({
    type: 'qrcode', // QR code
    content: 'https://informat.cn', // Content
    width: 100, // Width
    height: 100 // Height
});

```

:::


---

### createTemplateCell

Create a template cell

```javascript
informat.excel.createTemplateCell(cell);
```

| Parameter | Type                                                            | Description |
|------|---------------------------------------------------------------|-------|
| cell | [ExcelTamplateCell](/guide/script/model.md#exceltamplatecell) | Cell configuration |

**Return Value**

Returns a cell for use in templates

**Example**

```js
const companyCell = informat.excel.createTemplateCell({
    content: 'Shenzhen Cornerstone Collaboration Co., Ltd.', // Cell content
    rowspan: 2, // Row cell count, defaults to 1
    colspan: 2  // Column cell count, defaults to 1
});
```

## Workbook

### createSheet

Create a new Sheet

```javascript
workbook.createSheet(sheetName)
```

::: tip
sheetName cannot contain `0x0000` `0x0003` `:` `\` `*` `?` `/` `[``]`
:::

| Parameter   | Type       | Description |
|-----------|----------|----------|
| sheetName | `String` | Sheet name |

**Return Value**

Returns a [Sheet](/guide/script/excel.md#sheet) object

**Example**

```js
workbook.createSheet('sheet1')
```

---

### createSafeSheetName

Create a valid sheet name

```javascript
workbook.createSafeSheetName(sheetName)
```

::: tip
Certain special characters are not allowed in sheet names. Calling this method will automatically filter out these disallowed special characters
:::

| Parameter   | Type       | Description |
|-----------|----------|----------|
| sheetName | `String` | Sheet name |

**Return Value**

Returns `String`, the sheet name with special characters filtered out

**Example**

```js
workbook.createSafeSheetName('sheet1')
```

---

### getSheet

Get a Sheet by name

```javascript
workbook.getSheet(sheetName)
```

| Parameter   | Type       | Description |
|-----------|----------|----------|
| sheetName | `String` | Sheet name |

**Return Value**

Returns a [Sheet](/guide/script/excel.md#sheet) object, or `null` if sheetName does not exist

**Example**

```js
workbook.getSheet('sheet1')
```

---

### getSheetAt

Get a Sheet by position index

```javascript
workbook.getSheetAt(sheetIdx)
```

| Parameter  | Type        | Description |
|----------|-----------|---------------|
| sheetIdx | `Integer` | Sheet index, starting from 0 |

**Return Value**

Returns a [Sheet](/guide/script/excel.md#sheet) object, or `null` if the sheet does not exist

**Example**

```js
workbook.getSheetAt(0)
```

---

### getNumberOfSheets

Get the number of sheets

```javascript
workbook.getNumberOfSheets()
```

**Return Value**
Returns an `Integer` object, the number of sheets

---

### write

Write content to the file

```javascript
workbook.write()
```

::: tip
After calling write, the sheet content is written to the file and the workbook is closed. The write method cannot be called repeatedly. If an error occurs during writing (insufficient disk space, etc.), an exception will be thrown
:::


---

### createFont

Create a font configuration

::: tip
Used to set cell formatting
:::

```javascript
workbook.createFont()
```

**Return Value**

Returns a [Font](/guide/script/excel.md#font) object that describes the font

---

### createCellStyle

Create a cell style configuration

```javascript
workbook.createCellStyle()
```

::: tip
Cell style configuration can set cell color, background color, borders, alignment, and other styles
:::

**Return Value**
Returns a [CellStyle](/guide/script/excel.md#style) object that describes the cell style

## Sheet

### getSheetName

Get the sheet name

```javascript
sheet.getSheetName()
```

**Return Value**

Returns a `String` object, the sheet name

---

### createRow

Create a row

```javascript
sheet.createRow(row)
```

| Parameter | Type        | Description |
|-----|-----------|-----------|
| row | `Integer` | Row index, starting from 0 |

**Return Value**

Returns a [Row](/guide/script/excel.md#row) object

**Example**

```js
sheet.createRow(0)
```

---

### getRow

Get a row

```javascript
sheet.getRow(row)
```

| Parameter | Type        | Description |
|-----|-----------|-----------|
| row | `Integer` | Row index, starting from 0 |

**Return Value**

Returns a [Row](/guide/script/excel.md#row) object

**Example**

```js
sheet.getRow(0)
```

---

### removeRow

Remove a row

```javascript
sheet.removeRow(row)
```

| Parameter | Type      | Description |
|-----|---------|-----------|
| row | Integer | Row index, starting from 0 |

**Example**

```js
sheet.removeRow(0)
```

---

### getFirstRowNum

Get the index of the first row in the sheet

```javascript
sheet.getFirstRowNum()
```

**Return Value**

Returns `Integer`, the index of the first row


---

### getLastRowNum

Get the index of the last row in the sheet

```javascript
sheet.getLastRowNum()
```

**Return Value**

Returns `Integer`, the index of the last row


---

### getDefaultRowHeightInPoints

Get the default row height

```javascript
sheet.getDefaultRowHeightInPoints()
```

**Return Value**
Returns `Double`, the default row height


---

### setDefaultRowHeightInPoints

Set the default row height

```javascript
sheet.setDefaultRowHeightInPoints(height)
```

| Parameter | Type       | Description |
|--------|----------|------------|
| height | `Double` | Default row height, in pixels |

---

### getDefaultColumnWidth

Get the default column width

```javascript
sheet.getDefaultColumnWidth()
```

**Return Value**

Returns `Integer`, the default column width


---

### setDefaultColumnWidth

Set the default column width

```javascript
sheet.setDefaultColumnWidth(width)
```

| Parameter | Type        | Description |
|-------|-----------|------|
| width | `Integer` | Default column width |

---

### setColumnWidth

Set column width

```javascript
sheet.setColumnWidth(colIdx, width)
```

| Parameter | Type        | Description |
|--------|-----------|-----|
| colIdx | `Integer` | Column index |
| width  | `Integer` | Column width |

---

### autoSizeColumn

Automatically set column width based on content

```javascript
sheet.autoSizeColumn(colIdx)
```

::: tip
The auto column width function only takes effect after data insertion is complete
:::

| Parameter | Type        | Description |
|--------|-----------|-----|
| colIdx | `Integer` | Column index |

---

### setDefaultColumnStyle

Set the default cell style for a column

```javascript
sheet.setDefaultColumnStyle(colIdx, cellStyle)
```

| Parameter   | Type                                         | Description |
|-----------|--------------------------------------------|-----------|
| colIdx    | `Integer`                                  | Column index, starting from 0 |
| cellStyle | [CellStyle](/guide/script/excel.md#style) | Cell style |

---

### getColumnStyle

Get the default cell style for a column

```javascript
sheet.getColumnStyle(colIdx)
```

| Parameter | Type      | Description |
|--------|---------|-----------|
| colIdx | Integer | Column index, starting from 0 |

**Return Value**

Returns [CellStyle](/guide/script/excel.md#style), the default cell style


---

### addMergedRegion

Merge cells

```javascript
sheet.addMergedRegion(firstRow, lastRow, firstColumn, lastColumn)
```

| Parameter     | Type        | Description |
|-------------|-----------|-----------|
| firstRow    | `Integer` | First row, starting from 0 |
| lastRow     | `Integer` | Last row, starting from 0 |
| firstColumn | `Integer` | First column, starting from 0 |
| lastColumn  | `Integer` | Last column, starting from 0 |

---

### addPicture

Insert a picture from the local sandbox into a cell

```javascript
sheet.addPicture(col, row, filePath)
```

| Parameter  | Type        | Description |
|----------|-----------|--------------------------|
| col      | `Integer` | Column to insert, starting from 0 |
| row      | `Integer` | Row to insert, starting from 0 |
| filePath | `String`  | Picture path, file path in the app sandbox |

**Return Value**

Returns a [Picture](/guide/script/excel.md#picture) object

---

### addPictureStorage

Insert a picture from shared storage into a cell

```javascript
sheet.addPictureStorage(col, row, filePath)
```

| Parameter  | Type        | Description |
|----------|-----------|------------------------|
| col      | `Integer` | Column to insert, starting from 0 |
| row      | `Integer` | Row to insert, starting from 0 |
| filePath | `String`  | Picture path, file path in shared storage |

**Return Value**
Returns a [Picture](/guide/script/excel.md#picture) object


---

### addPictureBarcode

Insert a barcode image into a cell

```javascript
sheet.addPictureBarcode(col, row, setting)
```

| Parameter | Type               | Description |
|---------|------------------|-----------|
| col     | `Integer`        | Column to insert, starting from 0 |
| row     | `Integer`        | Row to insert, starting from 0 |
| setting | `PictureSetting` | Picture configuration |

**Return Value**

Returns a [Picture](/guide/script/excel.md#picture) object

---

### addPictureQrcode

Insert a QR code image into a cell

```javascript
sheet.addPictureQrcode(col, row, setting)
```

| Parameter | Type               | Description |
|---------|------------------|-----------|
| col     | `Integer`        | Column to insert, starting from 0 |
| row     | `Integer`        | Row to insert, starting from 0 |
| setting | `PictureSetting` | Picture configuration |

**Return Value**

Returns a [Picture](/guide/script/excel.md#picture) object

---

### getPictures

Get all pictures in the sheet

```javascript
sheet.getPictures()
```

**Return Value**

Returns Array<[Picture](/guide/script/excel.md#picture)> object

---

### getObjectDatas

Get all attachments in the sheet

```javascript
sheet.getObjectDatas()
```

**Return Value**
Returns Array<[ExcelObjectData](/guide/script/excel.md#excelobjectdata)> object

## Row

---

### createCell

Create a cell

```javascript
row.createCell(colIdx)
```

| Parameter | Type        | Description |
|--------|-----------|-----------|
| colIdx | `Integer` | Column to insert, starting from 0 |

**Return Value**
Returns a [Cell](/guide/script/excel.md#cell) object


---

### createCellWithValue

Create a cell with a value

```javascript
row.createCellWithValue(colIdx, value)
```

| Parameter | Type        | Description |
|--------|-----------|-------------------------------------------------------|
| colIdx | `Integer` | Column to insert, starting from 0 |
| value  | `Object`  | Value to insert; `Date`, `Boolean`, `Number` types are saved as their original types, other types are converted to strings |

**Return Value**
Returns a [Cell](/guide/script/excel.md#cell) object

---

### getCell

Get a cell

```javascript
row.getCell(colIdx)
```

| Parameter | Type        | Description |
|--------|-----------|-----------|
| colIdx | `Integer` | Column index, starting from 0 |

**Return Value**

Returns a [Cell](/guide/script/excel.md#cell) object, or `null` if the cell does not exist


---

### removeCell

Remove a cell

```javascript
row.removeCell(colIdx)
```

| Parameter | Type        | Description |
|--------|-----------|-----------|
| colIdx | `Integer` | Column to remove, starting from 0 |

---

### getFirstCellNum

Get the index of the first column

```javascript
row.getFirstCellNum()
```

**Return Value**

Returns `Integer`, the index of the first column


---

### getLastCellNum

Get the index of the last column

```javascript
row.getLastCellNum()
```

**Return Value**

Returns `Integer`, the index of the last column


---

### getRowNum

Get the row index

```javascript
row.getRowNum()
```

**Return Value**

Returns `Integer`, the row index


---

### getHeightInPoints

Get the row height

```javascript
row.getHeightInPoints()
```

**Return Value**

Returns `Double`, the row height


---

### setHeightInPoints

Set the row height

```javascript
row.setHeightInPoints(height)
```

| Parameter | Type       | Description |
|--------|----------|----------|
| height | `Double` | Row height, in pixels |

---

### setStyle

Set the row's cell style

```javascript
row.setStyle(cellStyle)
```

| Parameter   | Type                                        | Description |
|-----------|-------------------------------------------|-------|
| cellStyle | [CellStyle](/guide/script/excel.md#style) | Cell style |

---

### getStyle

Get the row's cell style

```javascript
row.getStyle()
```

**Return Value**

Returns [CellStyle](/guide/script/excel.md#style)

### createCellComment

Create a comment

```javascript
row.createCellComment(colIndex)
```

**Return Value**

Returns [ExcelComment](/guide/script/excel.md#excelcomment)


### getCellComment

Get a comment

```javascript
row.getCellComment(colIndex)
```

**Return Value**

Returns [ExcelComment](/guide/script/excel.md#excelcomment)

## Cell

### setValue

Set the cell value

```javascript
cell.setValue(value)
```

::: tip
Cells support `String` `Boolean` `Double` `Date` type values. Other types will be converted to strings for storage
:::

| Parameter | Type     | Description |
|-------|--------|-------|
| value | Object | Cell value |

---

### getValue

Get the cell value

```javascript
cell.getValue()
```

---

### getValueEvaluated

Get the cell value after formula evaluation

```javascript
cell.getValueEvaluated()
```

---

### setStyle

Set the cell style

```javascript
cell.setStyle(cs)
```

| Parameter   | Type                                         | Description |
|-----------|--------------------------------------------|-------|
| cellStyle | [CellStyle](/guide/script/excel.md#style) | Cell style |

---

### getStyle

Get the cell style

```javascript
cell.getStyle()
```

**Return Value**

Returns [CellStyle](/guide/script/excel.md#style)

---

### setHyperlink

Set a cell hyperlink

```javascript
cell.setHyperlink(link)
```

| Parameter | Type       | Description |
|------|----------|------|
| link | `String` | Link URL |

---

### getHyperlink

Get the cell hyperlink

```javascript
cell.getHyperlink()
```

**Return Value**

Returns `String`, the hyperlink URL, or `null` if the hyperlink does not exist

## Style
---

### setAlignment

Set horizontal alignment

```javascript
cellStyle.setAlignment(align)
```

| Parameter | Type       | Description |
|-------|----------|----------------------------------------------------------------------------------------|
| align | `String` | Options: `CENTER` `CENTER_SELECTION` `DISTRIBUTED` `FILL` `GENERAL` `JUSTIFY` `LEFT` `RIGHT` |

---

### getAlignment

Get horizontal alignment

```javascript
cellStyle.getAlignment()
```

**Return Value**

Type `String`

---

### setVerticalAlignment

Set vertical alignment

```javascript
cellStyle.setVerticalAlignment(align)
```

| Parameter | Type       | Description |
|-------|----------|----------------------------------------------------|
| align | `String` | Options: `BOTTOM` `CENTER` `DISTRIBUTED` `JUSTIFY` `TOP` |

---

### getVerticalAlignment

Get vertical alignment

```javascript
cellStyle.getVerticalAlignment()
```

**Return Value**

Type `String`


---

### getDataFormatString

Get the cell data format

```javascript
cellStyle.getDataFormatString()
```

**Return Value**

Type `String`

---

### setWrapText

Set whether cell text can wrap

```javascript
cellStyle.setWrapText(wrap)
```

| Parameter | Type        | Description |
|------|-----------|--------|
| wrap | `Boolean` | Whether text wraps |

---

### getWrapText

Get whether cell text wraps

```javascript
cellStyle.getWrapText()
```

**Return Value**

Returns `String`


---

### setFont

Set the cell text font

```javascript
cellStyle.setFont(font)
```

| Parameter | Type     | Description |
|------|--------|----|
| font | [Font](/guide/script/excel.md#font) | Font |

---

### setFillForegroundColor

Set the cell fill foreground color

```javascript
cellStyle.setFillForegroundColor(color)
```

| Parameter | Type       | Description |
|-------|----------|--------------------------|
| color | `String` | Hexadecimal color code, e.g. `#ff0000` for red |

---

### setFillBackgroundColor

Set the cell fill background color

```javascript
cellStyle.setFillBackgroundColor(color)
```

| Parameter | Type       | Description |
|-------|----------|--------------------------|
| color | `String` | Hexadecimal color code, e.g. `#ff0000` for red |

---

### setFillPattern

Set the fill pattern

```javascript
cellStyle.setFillPattern(type)
```

| Parameter | Type       | Description |
|------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| type | `String` | Options: `ALT_BARS`; `BIG_SPOTS`; `BRICKS`; `DIAMONDS`; `FINE_DOTS`; `LEAST_DOTS`; `LESS_DOTS`; `NO_FILL`; `SOLID_FOREGROUND`; `SPARSE_DOTS`; `SQUARES`; `THICK_BACKWARD_DIAG`;`THICK_FORWARD_DIAG`; `THICK_HORZ_BANDS`; `THICK_VERT_BANDS`; `THIN_VERT_BANDS`; |

---

### setHidden

Set hidden state

```javascript
cellStyle.setHidden(hidden)
```

| Parameter | Type        | Description |
|--------|-----------|--------|
| hidden | `Boolean` | Whether to hide |

---

### setIndention

Set indentation

```javascript
cellStyle.setIndention(indent)
```

| Parameter | Type        | Description |
|--------|-----------|-----|
| indent | `Integer` | Indentation value |

---

### setBorderTop

Set top border style

```js
cellStyle.setBorderTop(borderStyle);
```

| Parameter     | Type       | Description |
|-------------|----------|------|
| borderStyle | `String` | Border style |

Border style options:

- NONE: No border
- THIN: Thin border
- MEDIUM: Medium border
- DASHED: Dashed border
- DOTTED: Dotted border
- THICK: Thick border
- DOUBLE: Double line border
- HAIR: Hairline border
- MEDIUM_DASHED: Medium dashed border
- DASH_DOT: Dash-dot border
- MEDIUM_DASH_DOT: Medium dash-dot border
- DASH_DOT_DOT: Dash-dot-dot border
- MEDIUM_DASH_DOT_DOT: Medium dash-dot-dot border
- SLANTED_DASH_DOT: Slanted dash-dot border

---

### setBorderBottom

Set bottom border style

```js
cellStyle.setBorderBottom(borderStyle);
```

| Parameter     | Type       | Description |
|-------------|----------|------|
| borderStyle | `String` | Border style |

---

### setBorderLeft

Set left border style

```js
cellStyle.setBorderLeft(borderStyle);
```

| Parameter     | Type       | Description |
|-------------|----------|------|
| borderStyle | `String` | Border style |

---

### setBorderRight

Set right border style

```js
cellStyle.setBorderRight(borderStyle);
```

| Parameter     | Type       | Description |
|-------------|----------|------|
| borderStyle | `String` | Border style |

---

### setLeftBorderColor

Set left border color

```javascript
cellStyle.setLeftBorderColor(color)
```

| Parameter | Type       | Description |
|-------|----------|-----------------|
| color | `String` | Color, e.g. `#f0f0f0` |

---

### setRightBorderColor

Set right border color

```javascript
cellStyle.setRightBorderColor(color)
```

| Parameter | Type       | Description |
|-------|----------|-----------------|
| color | `String` | Color, e.g. `#f0f0f0` |

---

### setTopBorderColor

Set top border color

```javascript
cellStyle.setTopBorderColor(color)
```

| Parameter | Type       | Description |
|-------|----------|-----------------|
| color | `String` | Color, e.g. `#f0f0f0` |

---

### setBottomBorderColor

Set bottom border color

```javascript
cellStyle.setBottomBorderColor(color)
```

| Parameter | Type       | Description |
|-------|----------|-----------------|
| color | `String` | Color, e.g. `#f0f0f0` |

---

### setRotation

Set text rotation angle

```javascript
cellStyle.setRotation(rotation)
```

| Parameter  | Type        | Description |
|----------|-----------|-------------|
| rotation | `Integer` | Rotation angle, e.g. `90` |

---

### setDataFormat

Set cell format

```javascript
cellStyle.setDataFormat(fmt)
```

| Parameter | Type       | Description |
|-----|----------|-----------------|
| fmt | `String` | Cell format, e.g. `#0.00` |

## Font

### setBold

Set whether text is bold

```javascript
font.setBold(bold)
```

| Parameter | Type        | Description |
|------|-----------|------|
| bold | `Boolean` | Whether bold |

---

### setItalic

Set whether text is italic

```javascript
font.setItalic(italic)
```

| Parameter | Type        | Description |
|--------|-----------|------|
| italic | `Boolean` | Whether italic |

---

### setUnderline

Set whether text has underline

```javascript
font.setUnderline(underline)
```

| Parameter   | Type        | Description |
|-----------|-----------|--------|
| underline | `Boolean` | Whether underlined |

---

### setFontHeightInPoints

Set font size

```javascript
font.setFontHeightInPoints(size)
```

| Parameter | Type        | Description |
|------|-----------|------|
| size | `Integer` | Font size |

---

### setFontName

Set font name

```javascript
font.setFontName(name)
```

| Parameter | Type       | Description |
|------|----------|------|
| name | `String` | Font name |

## Picture
---

### getRow

Get the row where the picture is located

```javascript
picture.getRow()
```

**Return Value**

Returns `Integer`

---

### getColumn

Get the column where the picture is located

```javascript
picture.getColumn()
```

**Return Value**

Returns `Integer`

---

### save

Save the picture content to the local sandbox

```javascript
picture.save(path)
```

| Parameter | Type       | Description |
|------|----------|-------------|
| path | `String` | File path in the local sandbox |

---

### saveStorage

Save the picture content to shared storage

```javascript
picture.saveStorage(path)
```

| Parameter | Type       | Description |
|------|----------|-------------|
| path | `String` | File path in shared storage |

---

### saveAttachment

Save the picture content as an attachment field

```javascript
picture.saveAttachment(tableId, fieldId)
```

| Parameter | Type       | Description |
|---------|----------|----------|
| tableId | `String` | Data table identifier |
| fieldId | `String` | Attachment field identifier |

**Return Value**

Returns a [TableAttachment](/guide/script/model.md#tableattachment) object

---

### setScale

Set the picture scale ratio

```javascript
picture.setScale(wScale, hScale)
```

| Parameter | Type       | Description |
|--------|----------|---------|
| wScale | `Double` | Width scale ratio |
| hScale | `Double` | Height scale ratio |

---

### setSize

Set the picture dimensions

```javascript
picture.setSize(width, height)
```

| Parameter | Type        | Description |
|--------|-----------|------|
| width  | `Integer` | Picture width |
| height | `Integer` | Picture height |

---

### fitWidth

Scale the picture to fit the cell width

```javascript
picture.fitWidth()
```

::: tip
After scaling, the picture width will be less than or equal to the cell width, and the picture height will scale proportionally with the width
:::

---

### fitHeight

Scale the picture to fit the cell height

```javascript
picture.fitHeight()
```

::: tip
After scaling, the picture height will be less than or equal to the cell height, and the picture width will scale proportionally with the height
:::

---

### resetSize

Reset the picture size to its original dimensions

```javascript
picture.resetSize()
```

## ExcelObjectData

Excel attachment

---

### getRow

Get the row where the attachment is located

```javascript
objectData.getRow()
```

**Return Value**

Returns `Integer`

---

### getColumn

Get the column where the attachment is located

```javascript
objectData.getColumn()
```

**Return Value**

Returns `Integer`

---

### save

Save the file content to the local sandbox

```javascript
objectData.save(path)
```

| Parameter | Type       | Description |
|------|----------|-------------|
| path | `String` | File path in the local sandbox |

---

### saveStorage

Save the file content to shared storage

```javascript
objectData.saveStorage(path)
```

| Parameter | Type       | Description |
|------|----------|-------------|
| path | `String` | File path in shared storage |

---

### saveAttachment

Save the file content as an attachment field

```javascript
objectData.saveAttachment(tableId, fieldId)
```

| Parameter | Type       | Description |
|---------|----------|----------|
| tableId | `String` | Data table identifier |
| fieldId | `String` | Attachment field identifier |

**Return Value**

Returns a [TableAttachment](/guide/script/model.md#tableattachment) object

---

### hasDirectoryEntry

Whether there is an associated POIFS directory entry

```javascript
objectData.hasDirectoryEntry()
```

---

### getOLE2ClassName

Get the OLE2 class object name

```javascript
objectData.getOLE2ClassName()
```

---

### getFileName

Get the file name

```javascript
objectData.getFileName()
```

---

### getContentType

Get the file type

```javascript
objectData.getContentType()
```

## Examples

### Example 1: Read All Cell Data from an Excel File

```js
const workbook = informat.excel.openExistFile('test.xlsx');
for (var sheetIdx = 0; sheetIdx < workbook.getNumberOfSheets(); sheetIdx++) {
    const sheet = workbook.getSheetAt(sheetIdx);
    console.log("sheet name is " + sheet.getSheetName());
    // Return all cell data
    for (var rowIndex = sheet.getFirstRowNum(); rowIndex <= sheet.getLastRowNum(); rowIndex++) {
        const row = sheet.getRow(rowIndex);
        for (var colIndex = row.getFirstCellNum(); colIndex < row.getLastCellNum(); colIndex++) {
            const cell = row.getCell(colIndex);
            if (cell != null) {
                console.log(cell.getValueEvaluated());
            }
        }
    }
    // Return all pictures
    sheet.getPictures().forEach(p => {
        console.log("picture " + p.getRow() + " " + p.getColumn());
    });
    // After reading pictures, you can use picture's save(localPath), saveStorage(path), saveAttachment(tableKey, fieldKey, fieldName) to save the file content to the local sandbox or shared storage
}

```

### Example 2: Write Data to an Excel File

```js
const workbook = informat.excel.openNewFile('test.xlsx');
const sheet = workbook.createSheet("sheet1");
const style = workbook.createCellStyle();
const font = workbook.createFont();
font.setBold(true);
font.setItalic(true);
font.setFontHeightInPoints(14);
//
style.setFont(font);
style.setFillBackgroundColor("#fafafa"); // Set gray background
style.setAlignment("CENTER"); // Horizontal center
style.setVerticalAlignment("CENTER"); // Vertical center
style.setFillPattern("SOLID_FOREGROUND");
//
for (var i = 0; i < 10; i++) {
    const row = sheet.createRow(i);
    const cell = row.createCellWithValue(0, "String");
    cell.setStyle(style);
    row.createCellWithValue(1, "https://informat.cn/").setHyperlink("https:/informat.cn");
    row.createCellWithValue(2, true);
    row.createCellWithValue(3, 3.14);
    row.createCellWithValue(4, new Date());
}
//
sheet.addMergedRegion(0, 2, 0, 3); // Merge cells
// The auto column width function only takes effect after data insertion is complete
sheet.autoSizeColumn(0); // Auto-adjust width for the first and second columns
sheet.autoSizeColumn(1);
//
workbook.write(); // Write to file
//

```

### Example 3: Generate Excel Using a Template File

```js
const templateFilePath = 'excel_template.xlsx';
const outputFilePath = 'result.xlsx';
informat.website.download('website', 'excel/excel_template.xlsx', templateFilePath);
const workbook = informat.excel.openWithTemplate(outputFilePath, templateFilePath, {
    'orgName': 'Company Name XXX',
    'goodAtProduct': 'Product XXX',
    'addresss': 'Company Address XXXXXXX',
    'reviewUser': '张三',
    'reviewTime': new Date(),
    'list': [
        { 'sort': 1, 'question': 'Item 1', 'standard': 'Excellent', 'score': 95, 'realScore': 98, 'realTotalScore': 99 },
        { 'sort': 2, 'question': 'Item 2', 'standard': 'Good', 'score': 78, 'realScore': 79, 'realTotalScore': 80 },
        { 'sort': 3, 'question': 'Item 3', 'standard': 'Pass', 'score': 65, 'realScore': 62, 'realTotalScore': 66 },
    ]
});
workbook.write(); // Write to file
```

:::tip
**Template Download**
<a href="/doc/template/excel_template.xlsx" target="_blank">excel_template.xlsx</a>

In this example, the template file export_muti_sheet_template.xlsx is uploaded to the excel folder under the Resource & Component Designer module with the identifier website
:::


### Example 4: Insert Pictures

```js
const workbook = informat.excel.openNewFile('test-pic.xlsx');
const sheet = workbook.createSheet("sheet1");
//
for (var i = 0; i < 5; i++) {
    const row = sheet.createRow(i);
    row.createCellWithValue(0, 'Column 1');
    row.createCellWithValue(1, 'Column 2');
}
//
sheet.addPicture(0, 0, "path/to/image.png").setSize(60, 60);
sheet.addPicture(1, 0, "path/to/image.png").setSize(60, 60);
//
workbook.write(); // Write to file
//
```

### Example 5: Export Using Multi-Sheet Excel Template

```js

// Download template file
export function exportMutiSheetTemplate() {
  // Define template file path
  const templateFilePath = 'mutiSheetTemplate.xlsx';
  const outputFilePath = 'result.xlsx';
  informat.website.download('website', 'excel/export_muti_sheet_template.xlsx', templateFilePath);
  
  // Define the sheet number list to export, starting from 0. If empty, all sheets are exported
  const sheetNums = [0, 1, 2]; // Export the 1st, 2nd, and 3rd sheets
  
  // Define data to pass to the template
  const data = {
    'orgName': 'Company Name XXX',
    'goodAtProduct': 'Product XXX',
    'addresss': 'Company Address XXXXXXX',
    'reviewUser': '张三',
    'reviewTime': new Date(),
    'list': [
      {'sort': 1, 'question': 'Item 1', 'standard': 'Excellent', 'score': 95, 'realScore': 98, 'realTotalScore': 99},
      {'sort': 2, 'question': 'Item 2', 'standard': 'Good', 'score': 78, 'realScore': 79, 'realTotalScore': 80},
      {'sort': 3, 'question': 'Item 3', 'standard': 'Pass', 'score': 65, 'realScore': 62, 'realTotalScore': 66},
    ]
  };
  
  // Create a new Excel file using the template file and export specified sheets
  const workbook = informat.excel.openWithTemplateWithSheets(outputFilePath, templateFilePath, sheetNums, data);
  
  // Write to file
  workbook.write();
  return outputFilePath
}
```

:::tip
**Template Download**
<a href="/doc/template/export_muti_sheet_template.xlsx" target="_blank">export_muti_sheet_template.xlsx</a>
In this example, the template file export_muti_sheet_template.xlsx is uploaded to the excel folder under the Resource & Component Designer module with the identifier website
:::


### Example 6: Create Comments

```js
const workbook = informat.excel.openNewFile('test.xlsx');
const sheet = workbook.createSheet("sheet1");
let row = sheet.createRow(0);
row.createCellWithValue(0, "This is a test comment")
let comment = row.createCellComment(0);
comment.setAuthor("System Administrator");
comment.setContent("This is a test comment to demonstrate the Excel comment feature!\nLine breaks are supported~");
workbook.write();
```

### Example 7: Get Comments

```js
const workbook = informat.excel.openExistFile('test.xlsx');
const sheet = workbook.getSheetAt(0);
let row = sheet.getRow(0);
let comment = row.getCellComment(0);
console.log('comment content',comment.getContent());
console.log('comment author',comment.getAuthor());

// Output:
comment content This is a test comment to demonstrate the Excel comment feature!
Line breaks are supported~
comment author System Administrator
```
