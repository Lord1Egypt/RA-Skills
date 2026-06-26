# Google Sheets Operations

Use `drivectl` to read and update data in Google Sheets. Always use `-O json` for programmatic parsing where applicable.

## Reading Data

**Export a full sheet as CSV:**
```bash
drivectl sheets get <spreadsheet-id> --sheet "Sheet1"
```
*(This outputs raw CSV data to stdout. Do not use `-O json` here if you just want the CSV).*

**Read a specific cell range (A1 notation):**
```bash
drivectl sheets get-range <spreadsheet-id> --sheet "Sheet1" --range "A1:C5" -O json
```
*(Outputs a JSON array of arrays containing the cell values).*

## Updating Data

**Update a specific cell or range:**
```bash
drivectl sheets update-range <spreadsheet-id> "New Value" --sheet "Sheet1" --range "B2" -O json
```

If you are updating a range, the "New Value" is typically applied starting at the top-left of the range.
