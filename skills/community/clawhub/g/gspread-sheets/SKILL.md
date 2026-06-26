---
name: gspread-sheets
description: "Batch read/write Google Sheets using the gspread Python library with service account authentication. Use when the user needs to: (1) read/write/update/clear Google Sheets data in bulk, (2) batch update multiple cells/ranges at once, (3) append rows, (4) manage worksheets, (5) work with Google Sheets via API without browser automation. Triggers: Google Sheets, gspread, batch update, sheet data, spreadsheet API."
---

# gspread-sheets

## Prerequisites

```bash
pip install gspread google-auth
```

Service account JSON key file required. Set path via:
- Environment variable: `export GOOGLE_SERVICE_ACCOUNT_JSON=/path/to/key.json`
- Or pass explicitly in scripts

Share the target spreadsheet with the service account email (found in the JSON key file).

## Quick Start

### Initialize Client

```python
import gspread
from google.oauth2.service_account import Credentials

SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

# Option 1: From JSON file path
creds = Credentials.from_service_account_file('key.json', scopes=SCOPES)
gc = gspread.authorize(creds)

# Option 2: From JSON string (e.g. env var)
import json, os
creds_info = json.loads(os.environ['GOOGLE_SERVICE_ACCOUNT_JSON'])
creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
gc = gspread.authorize(creds)
```

### Open Spreadsheet

```python
# By name
sh = gc.open("My Spreadsheet")

# By URL
sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit")

# By key
sh = gc.open_by_key("SPREADSHEET_ID")
```

## Core Operations

### Read Data

```python
ws = sh.sheet1  # or sh.worksheet("Sheet Name")

# All values as list of lists
data = ws.get_all_values()

# All records (first row = headers)
records = ws.get_all_records()

# Specific range
subset = ws.get("A1:D10")

# Single cell
val = ws.acell("B2").value
val = ws.cell(row=2, col=2).value

# Column or row as list
col_a = ws.col_values(1)
row_1 = ws.row_values(1)
```

### Write Data (Batch)

```python
# Update a range (list of lists)
ws.update("A1:D3", [["a1","b1","c1","d1"],
                      ["a2","b2","c2","d2"],
                      ["a3","b3","c3","d3"]])

# Append rows (at the bottom)
ws.append_rows([["new1","row1"],["new2","row2"]])

# Append single row
ws.append_row(["val1","val2","val3"])

# Batch update multiple ranges at once (most efficient)
ws.batch_update([
    {"range": "A1:B2", "values": [["a","b"],["c","d"]]},
    {"range": "D1:E2", "values": [["x","y"],["z","w"]]},
])
```

### Cell-Level Batch Update

```python
# Update specific cells by row/col
cell_list = ws.range("A1:C2")
for i, cell in enumerate(cell_list):
    cell.value = f"data_{i}"
ws.update_cells(cell_list)
```

### Clear & Format

```python
# Clear specific range
ws.clear()

# Clear range
ws.batch_clear(["A1:D10", "F1:G5"])

# Format cells
ws.format("A1:D1", {"textFormat": {"bold": True}})
```

### Worksheet Management

```python
# List all worksheets
worksheets = sh.worksheets()

# Add worksheet
new_ws = sh.add_worksheet(title="New Sheet", rows=100, cols=20)

# Delete worksheet
sh.del_worksheet(ws)

# Rename
ws.update_title("New Name")

# Duplicate
ws.duplicate(new_sheet_name="Copy")
```

### Find & Replace

```python
# Find all matches
cells = ws.findall("search_term")

# Find with regex
import re
cells = ws.findall(re.compile(r"^prefix_.*"))

# Replace all
ws.replace("old_value", "new_value")
```

## Batch Operation Patterns

### Pattern 1: Read-Modify-Write

```python
data = ws.get_all_records()  # list of dicts
for row in data:
    row["status"] = "processed"
# Write back (need headers + data as list of lists)
header = list(data[0].keys())
rows = [list(r.values()) for r in data]
ws.update("A1", [header] + rows)
```

### Pattern 2: Efficient Large Upload (>1000 rows)

```python
import math
BATCH_SIZE = 1000
for i in range(0, len(all_rows), BATCH_SIZE):
    batch = all_rows[i:i+BATCH_SIZE]
    ws.append_rows(batch, value_input_option="USER_ENTERED")
```

### Pattern 3: Multi-Sheet Batch Sync

```python
for ws_name in ["Sheet1", "Sheet2", "Sheet3"]:
    ws = sh.worksheet(ws_name)
    records = ws.get_all_records()
    # process...
    ws.batch_update(processed_ranges)
```

### Pattern 4: Conditional Formatting

```python
ws.add_conditional_formatting("A1:A100", {
    "type": "NUMBER_GREATER",
    "value": 100,
    "format": {"backgroundColor": {"red": 0.8, "green": 0.2, "blue": 0.2}}
})
```

## Error Handling

```python
import gspread
from gspread.exceptions import APIError, WorksheetNotFound

try:
    ws = sh.worksheet("NonExistent")
except WorksheetNotFound:
    ws = sh.add_worksheet("NonExistent", rows=100, cols=20)

# Rate limit handling
import time
from gspread.exceptions import APIError

def safe_batch_update(ws, data, retries=3):
    for attempt in range(retries):
        try:
            return ws.batch_update(data)
        except APIError as e:
            if "429" in str(e) and attempt < retries - 1:
                time.sleep(2 ** attempt)
            else:
                raise
```

## Tips

- Use `batch_update` over multiple `update` calls — fewer API requests
- `value_input_option="USER_ENTERED"` parses formulas and number formats
- `value_input_option="RAW"` writes literal strings
- Default `include_empty=False` in `get_all_values` omits trailing empty cells
- Service account has its own Drive; share sheets with its email to access
- For shared drives, use `gc.open_by_key()` (more reliable than name)
