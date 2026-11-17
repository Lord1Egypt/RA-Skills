# Sheets

`Sheets(auth)` from `gsuite_sheets`. Opening by title and listing also use
Drive (in the default login).

## Opening

```python
from gsuite_core import GoogleAuth
from gsuite_sheets import Sheets

auth = GoogleAuth()
sheets = Sheets(auth)

spreadsheet = sheets.open_by_key("1AbC...")               # by ID (preferred)
spreadsheet = sheets.open_by_url("https://docs.google.com/spreadsheets/d/1AbC.../edit")
spreadsheet = sheets.open("Budget 2026")                  # by exact title; ValueError if none
new = sheets.create("Report")
for item in sheets.list_spreadsheets():
    print(item["id"], item["name"])

ws = spreadsheet.sheet1                                   # first tab, any name
ws = spreadsheet.worksheet("Data")                        # None if there is no such tab
ws = spreadsheet.worksheet_or_create("Data")
```

The first tab's name depends on the account's language ("Sheet1", "Hoja 1",
...): use `sheet1` or `get_worksheet(0)`, not a hard-coded name.

## Reading

```python
values = ws.get("A1:D20")                 # list of rows (lists of strings)
everything = ws.get_all_values()
records = ws.get_all_records()            # [{"Name": "Ana", "Score": "42"}, ...] — strings
batches = ws.batch_get(["A1:B5", "D1:D5"])
cell = ws.find("Ana")                     # (row, col) or None
for record in ws.iter_records(page_size=500):   # streams big sheets
    print(record)
```

## Writing

`update` and `append_rows` take a **2D list**; one row is a list of lists.

```python
ws.update("A1", [["Name", "Score"], ["Ana", 42]])
ws.update_cell(2, 2, 43)                  # row, column (1-based)
ws.append_row(["Bob", 7])
ws.append_rows([["Cy", 9], ["Di", 11]])
ws.update("C2", [["=B2*2"]])              # formulas are evaluated (USER_ENTERED)
ws.update("D2", [["=not a formula"]], value_input="RAW")   # store text as typed
ws.clear("A2:D100")
ws.replace("2025", "2026")
```

## Table operations (header row = column names)

```python
ws.upsert([{"Name": "Ana", "Score": 50}, {"Name": "Eve", "Score": 3}], key="Name")
# -> {"updated": 1, "appended": 1}
ws.update_where({"Name": "Bob"}, {"Score": 8})
ws.delete_where({"Score": "0"})
```

Typed rows with a dataclass (or a Pydantic model):

```python
from dataclasses import dataclass

@dataclass
class Row:
    name: str
    score: int

ws.ensure_schema(Row)                     # writes the header if the sheet is empty
rows = ws.read_as(Row)                    # list[Row] with converted types
ws.append_models([Row("Fay", 5)])
ws.upsert_models([Row("Ana", 51)], key="name")
```

## Formatting, validation and protection

```python
from gsuite_sheets import CellFormat, Color, TextFormat

ws.format_header()                                        # bold, colored first row
ws.format("B2:B100", CellFormat(text_format=TextFormat(bold=True)))
ws.freeze(rows=1)
ws.add_dropdown("C2:C100", ["todo", "doing", "done"])
ws.add_checkbox("D2:D100")
ws.add_conditional_format("B2:B100", "NUMBER_LESS", [0],
                          CellFormat(background_color=Color.from_hex("#F4CCCC")))
ws.merge("A1:D1")
ws.protect("A1:D1", description="Header", warning_only=True)
```

## Exporting, CSV and DataFrames

```python
pdf = spreadsheet.export("pdf")           # pdf, xlsx, ods, csv, tsv, html -> bytes
spreadsheet.share("ana@example.com", role="writer")
ws.import_csv("data.csv")                 # replaces the sheet; clear=False appends
df = ws.to_dataframe()                    # needs pip install "gsuite-sdk[pandas]"
```

## Async

```python
from gsuite_sheets import AsyncSheets

async def main():
    async with AsyncSheets(auth) as sheets:
        spreadsheet = await sheets.open_by_key("1AbC...")
        ws = spreadsheet.worksheet("Data")
        await ws.append_rows([["Ana", 42]])
        rows = await ws.get_all_records()
```

Needs `pip install "gsuite-sdk[async]"`. Same methods as the sync classes,
awaited.

## CLI

`SPREADSHEET` is a title, an ID or a URL.

```bash
gsuite sheets list -o json
gsuite sheets read "Budget 2026" --range "A1:D20" -o json      # -o table | json | csv
gsuite sheets read SPREADSHEET --sheet Data -o csv
gsuite sheets write SPREADSHEET --cell B2 --value 42
gsuite sheets append SPREADSHEET --value Ana --value 42 --sheet Data
gsuite sheets upsert SPREADSHEET rows.csv --key Name
gsuite sheets import-csv SPREADSHEET data.csv --sheet Data
gsuite sheets export SPREADSHEET --format pdf --out ./budget.pdf
gsuite sheets replace SPREADSHEET 2025 2026
gsuite sheets freeze SPREADSHEET --rows 1
gsuite sheets add-tab SPREADSHEET Archive
gsuite sheets share SPREADSHEET ana@example.com --role writer
gsuite sheets create "Report"
```
