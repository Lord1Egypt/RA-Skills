# Pandas & NumPy Integration

`pandas` is an optional dependency, not a core dependency of this skill. Only use this file when the task explicitly involves DataFrames, Pandas-based table processing, time-series export, or similar scenarios. Confirm that `pandas` can be imported first. If it is missing, report that `pandas` is required and do not install it automatically.

openpyxl has built-in support for NumPy types such as floats, integers, booleans, and Pandas timestamps.

## DataFrame -> Worksheet

```python
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd

df = pd.DataFrame({"Name": ["Alice", "Bob"], "Score": [95, 87]})

wb = Workbook()
ws = wb.active

for r in dataframe_to_rows(df, index=True, header=True):
    ws.append(r)

# Style the header and index
for cell in ws["A"] + ws[1]:
    cell.style = "Pandas"

wb.save("from_pandas.xlsx")
```

`dataframe_to_rows(df, index=True, header=True)` parameters:
- `index`: include the DataFrame index as the first column
- `header`: include column headers as the first row

## DataFrame -> Write-Only Worksheet

```python
from openpyxl import Workbook
from openpyxl.cell.cell import WriteOnlyCell
from openpyxl.utils.dataframe import dataframe_to_rows

wb = Workbook(write_only=True)
ws = wb.create_sheet()

cell = WriteOnlyCell(ws)
cell.style = "Pandas"

def format_first_row(row, cell):
    for c in row:
        cell.value = c
        yield cell

rows = dataframe_to_rows(df)
first_row = format_first_row(next(rows), cell)
ws.append(first_row)

for row in rows:
    row = list(row)
    cell.value = row[0]
    row[0] = cell
    ws.append(row)

wb.save("stream_pandas.xlsx")
```

## Worksheet -> DataFrame

```python
import pandas as pd
from itertools import islice

# Simple conversion without headers or index
df = pd.DataFrame(ws.values)

# With headers and index
data = ws.values
cols = next(data)[1:]          # skip the index column in the header row
data = list(data)
idx = [r[0] for r in data]     # first column becomes the index
data = (islice(r, 1, None) for r in data)
df = pd.DataFrame(data, index=idx, columns=cols)
```
