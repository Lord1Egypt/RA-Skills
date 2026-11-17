# informat.csv CSV Related

## Overview
Use `informat.csv` to perform read and write operations on CSV files

## CsvReader

### reader
Read a CSV file from the local sandbox. An exception will be thrown if the file does not exist

```javascript
informat.csv.reader(file)
```

| Parameter | Type     | Description                          |
| --------- | -------- |--------------------------------------|
| file      | `String` | File path in the app sandbox environment |

**Return Value**

Type is `CsvReader`

**Example**
```javascript
const reader = informat.csv.reader('path/to/file.csv')
```

### setFieldSeparator
Set the field separator

```js
reader.setFieldSeparator(c)
```
::: tip Note
- The default separator is comma `,`
:::

| Parameter | Type | Description     |
| --------- | ---- |-----------------|
| c         | char | Field separator |

**Example**

```js
reader.setFieldSeparator(',')
```


### setQuoteCharacter
Set the quote character

```js
reader.setQuoteCharacter(c)
```

::: tip Note
- The default is double quote `"`
:::

| Parameter | Type | Description     |
| --------- | ---- |-----------------|
| c         | char | Quote character |

**Example**
```js
reader.setQuoteCharacter('\"')
```

### setCommentCharacter
Set the comment character
```js
reader.setCommentCharacter(c)
```

::: tip Note
Default comment character is `#`
:::

| Parameter | Type | Description       |
| --------- | ---- |-------------------|
| c         | char | Comment character |

**Example**
```js
reader.setCommentCharacter('#')
```


### setCommentStrategy
Set the comment strategy
```js
reader.setCommentStrategy(s)
```
| Parameter | Type   | Description            |
| --------- | ------ |------------------------|
| s         | String | NONE, SKIP, READ       |

Strategy descriptions:

| Strategy | Description                                                                                            |
| -------- |--------------------------------------------------------------------------------------------------------|
| NONE     | Do not detect comments - treat all content as regular cell content. Default value                       |
| SKIP     | Detect comments but do not return comment lines                                                        |
| READ     | Detect comments and return comment lines (entire line as one field). The comment character itself will be stripped |

**Example**
```js
reader.setCommentStrategy('NONE')
```

### setSkipEmptyRows
Set whether to skip empty rows
```js
reader.setSkipEmptyRows(f)
```
| Parameter | Type    | Description              |
| --------- | ------- |--------------------------|
| f         | Boolean | Whether to skip empty rows |

**Example**
```js
reader.setSkipEmptyRows(true)
```

### setErrorOnDifferentFieldCount
Set whether to throw an exception when field counts are inconsistent
```js
reader.setErrorOnDifferentFieldCount(f)
```
| Parameter | Type    | Description                  |
| --------- | ------- |------------------------------|
| f         | Boolean | Whether to throw an exception |

**Example**
```js
reader.setErrorOnDifferentFieldCount(true)
```

### setCharset
Set the character set (default: UTF-8)

```js
reader.setCharset(charset)
```

| Parameter | Type   | Description                |
| --------- | ------ |----------------------------|
| charset   | String | Character set, e.g.: UTF-8, GBK |

**Example**
```js
reader.setCharset('UTF-8')
```

### read
Read the CSV file
```js
reader.read(accept)
```
| Parameter | Type               | Description                    |
| --------- |-------------------|--------------------------------|
| accept    | `Function(CsvRow)` | Handler function for each row |

**Example**
```js
let reader = informat.csv.reader('path/to/file.csv');
reader.read((csvRow)=>{
    for(let i = 0; i < csvRow.getFieldCount(); i++){
        console.log(csvRow.getField(i))
    }
})
```

## CsvRow

### getOriginalLineNumber
Returns the line number
```js
csvRow.getOriginalLineNumber()
```

### getField
Returns a field
```js
csvRow.getField(index)
```

| Parameter | Type      | Description |
| --------- |-----------|-------------|
| index     | `Integer` | Index       |

### getFields
Returns the field list
```js
csvRow.getFields()
```

### getFieldCount
Returns the field count
```js
csvRow.getFieldCount()
```

### isComment
Whether this line is a comment
```js
csvRow.isComment()
```

### isEmpty
Whether this line is empty
```js
csvRow.isEmpty()
```

## CsvWriter

### writer
Get a writer object to write content to a CSV file in the local sandbox

```javascript
informat.csv.writer(file)
```

| Parameter | Type     | Description                          |
| --------- |--------|--------------------------------------|
| file      | `String` | File path in the app sandbox environment |

**Return Value**

Type is `CsvWriter`

**Example**
```js
let writer=informat.csv.writer('path/to/file.csv');
writer.writeRow(['a','b','c','d']);
writer.writeRow(['1','2','3','4']);
writer.close();
```

### setCharset
Set the character set
```js
writer.setCharset(charset)
```
::: tip Note
Default character set: `UTF-8`
:::

| Parameter | Type   | Description                |
| --------- | ------ |----------------------------|
| charset   | String | Character set, e.g.: UTF-8, GBK |

**Example**
```js
writer.setCharset('UTF-8')
```

### setFieldSeparator
Set the field separator
```js
writer.setFieldSeparator(c)
```

::: tip Note
The default separator is comma `,`
:::

| Parameter | Type | Description     |
| --------- | ---- |-----------------|
| c         | char | Field separator |

**Example**
```js
writer.setFieldSeparator()
```

### setQuoteCharacter
Set the quote character, default is double quote (")
```js
writer.setQuoteCharacter(c)
```

::: tip Note
Default is double quote `"`
:::

| Parameter | Type | Description     |
| --------- | ---- |-----------------|
| c         | char | Quote character |

**Example**
```js
writer.setQuoteCharacter()
```

### setQuoteStrategy
Set the quote strategy
```js
writer.setQuoteStrategy(s)
```
| Parameter | Type   | Description                  |
| --------- | ------ |------------------------------|
| s         | String | REQUIRED, EMPTY, ALWAYS      |

Strategy descriptions:

| Strategy | Description                                                                           |
| -------- |---------------------------------------------------------------------------------------|
| REQUIRED | This strategy requires all fields to use quotes. Default value                        |
| EMPTY    | This strategy requires quotes only when a field contains a comma or newline character |
| ALWAYS   | This strategy requires all fields to always use quotes                                |

**Example**
```js
writer.setQuoteStrategy('REQUIRED')
```

### setCommentCharacter
Set the comment character, default comment character is (#)
```js
writer.setCommentCharacter(c)
```
| Parameter | Type | Description       |
| --------- | ---- |-------------------|
| c         | char | Comment character |


### setLineDelimiter
Set the line delimiter, default is (CRLF)
```js
writer.setLineDelimiter(s)
```

| Parameter | Type   | Description    |
|-----------|--------|----------------|
| s         | String | Line delimiter |

**Line Delimiters**

| Delimiter | Description                    |
|-----------|--------------------------------|
| CRLF      | Corresponds to \r\n, default   |
| CR        | Corresponds to \r              |
| LF        | Corresponds to \n              |
| PLATFORM  | System default                 |

**Example**
```js
writer.setLineDelimiter('CRLF')
```

### writeRow
Write a row of data
```js
writer.writeRow(row)
```
| Parameter | Type            | Description       |
| --------- |-----------------|-------------------|
| row       | `Array<String>` | Array of content |

### writeComment
Write a comment line
```js
writer.writeComment(comment)
```
| Parameter | Type   | Description     |
| --------- | ------ |-----------------|
| comment   | String | Comment content |

**Example**
```js
writer.writeComment('Comment content')
```

### close
Close the output stream
```js
writer.close()
```
