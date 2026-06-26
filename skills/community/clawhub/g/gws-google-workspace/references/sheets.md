# Sheets Reference

Sheet names are not always "Sheet1" — retrieve actual names first:

```bash
SHEET=$(gws sheets spreadsheets get --params '{"spreadsheetId":"ID"}' 2>/dev/null | tail -n +2 | jq -r '.sheets[0].properties.title')
```

## Create, Read, Write

```bash
SHEET_ID=$(gws sheets spreadsheets create --json '{"properties":{"title":"My Sheet"}}' --params '{}' 2>/dev/null | tail -n +2 | jq -r '.spreadsheetId')

# Read
gws sheets spreadsheets values get --params '{"spreadsheetId":"ID","range":"Sheet1!A1:B2"}'

# Write raw values
gws sheets spreadsheets values update --params '{"spreadsheetId":"ID","range":"Sheet1!A1","valueInputOption":"RAW"}' --json '{"values":[["Value"]]}'

# Write formulas (must use USER_ENTERED)
gws sheets spreadsheets values update --params '{"spreadsheetId":"ID","range":"Sheet1!C1","valueInputOption":"USER_ENTERED"}' --json '{"values":[["=AVERAGE(B2:B10)"]]}'

# Append rows
gws sheets spreadsheets values append --params '{"spreadsheetId":"ID","range":"Sheet1!A1","valueInputOption":"RAW"}' --json '{"values":[["col1","col2"]]}'

# Clear (preserves formatting)
gws sheets spreadsheets values clear --params '{"spreadsheetId":"ID","range":"Sheet1!A1:C10"}'
```

## Row/Column Operations

```bash
# Delete row
gws sheets spreadsheets batchUpdate --params '{"spreadsheetId":"ID"}' --json '{"requests":[{"deleteDimension":{"range":{"sheetId":0,"dimension":"ROWS","startIndex":2,"endIndex":3}}}]}'

# Insert column
gws sheets spreadsheets batchUpdate --params '{"spreadsheetId":"ID"}' --json '{"requests":[{"insertDimension":{"range":{"sheetId":0,"dimension":"COLUMNS","startIndex":1,"endIndex":2},"inheritFromBefore":true}}]}'

# Merge cells
gws sheets spreadsheets batchUpdate --params '{"spreadsheetId":"ID"}' --json '{"requests":[{"mergeCells":{"range":{"sheetId":0,"startRowIndex":0,"endRowIndex":1,"startColumnIndex":0,"endColumnIndex":3},"mergeType":"MERGE_ALL"}}]}'

# Set column width
gws sheets spreadsheets batchUpdate --params '{"spreadsheetId":"ID"}' --json '{"requests":[{"updateDimensionProperties":{"range":{"sheetId":0,"dimension":"COLUMNS","startIndex":0,"endIndex":1},"properties":{"pixelSize":200},"fields":"pixelSize"}}]}'
```

## Formatting

```bash
# Cell background color
gws sheets spreadsheets batchUpdate --params '{"spreadsheetId":"ID"}' --json '{"requests":[{"repeatCell":{"range":{"sheetId":0,"startRowIndex":0,"endRowIndex":1},"cell":{"userEnteredFormat":{"backgroundColor":{"red":0.2,"green":0.6,"blue":1}}},"fields":"userEnteredFormat.backgroundColor"}}]}'

# Conditional formatting
gws sheets spreadsheets batchUpdate --params '{"spreadsheetId":"ID"}' --json '{"requests":[{"addConditionalFormatRule":{"rule":{"ranges":[{"sheetId":0,"startRowIndex":1,"endRowIndex":100}],"booleanRule":{"condition":{"type":"NUMBER_GREATER","values":[{"userEnteredValue":"90"}]},"format":{"backgroundColor":{"red":0,"green":1,"blue":0}}}},"index":0}}]}'

# Freeze rows/columns
gws sheets spreadsheets batchUpdate --params '{"spreadsheetId":"ID"}' --json '{"requests":[{"updateSheetProperties":{"properties":{"sheetId":0,"gridProperties":{"frozenRowCount":1,"frozenColumnCount":1}},"fields":"gridProperties.frozenRowCount,gridProperties.frozenColumnCount"}}]}'
```
