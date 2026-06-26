# Advanced Features Reference

## Table of Contents
1. [Conditional Formatting](#conditional-formatting)
2. [Data Validation](#data-validation)
3. [Worksheet Tables](#worksheet-tables)
4. [Filters & Sorting](#filters--sorting)
5. [Images](#images)
6. [Print Settings](#print-settings)
7. [Defined Names](#defined-names)
8. [Worksheet Properties](#worksheet-properties)
9. [Rich Text](#rich-text)
10. [Pivot Tables](#pivot-tables)
11. [Optimized Modes](#optimized-modes)
12. [Comments](#comments)

---

## Conditional Formatting

### Color Scales

```python
from openpyxl.formatting.rule import ColorScaleRule

# Two-color scale
ws.conditional_formatting.add("A1:A10",
    ColorScaleRule(start_type="min", start_color="AA0000",
                   end_type="max", end_color="00AA00"))

# Three-color scale
ws.conditional_formatting.add("B1:B10",
    ColorScaleRule(start_type="percentile", start_value=10, start_color="FFAA0000",
                   mid_type="percentile", mid_value=50, mid_color="FF0000AA",
                   end_type="percentile", end_value=90, end_color="FF00AA00"))
```

### Icon Sets & Data Bars

```python
from openpyxl.formatting.rule import IconSetRule, DataBarRule

ws.conditional_formatting.add("C1:C10",
    IconSetRule("3TrafficLights1", "percent", [0, 33, 67]))

ws.conditional_formatting.add("D1:D10",
    DataBarRule(start_type="percentile", start_value=10,
                end_type="percentile", end_value="90", color="FF638EC6"))
```

### Cell Value & Formula Rules

```python
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import PatternFill, Font
from openpyxl.styles.differential import DifferentialStyle

red_fill = PatternFill(start_color="EE1111", end_color="EE1111", fill_type="solid")

# Cell value comparison
ws.conditional_formatting.add("C2:C10",
    CellIsRule(operator="lessThan", formula=["C$1"], stopIfTrue=True, fill=red_fill))

ws.conditional_formatting.add("D2:D10",
    CellIsRule(operator="between", formula=["1", "5"], stopIfTrue=True, fill=red_fill))

# Formula-based
ws.conditional_formatting.add("E1:E10",
    FormulaRule(formula=["ISBLANK(E1)"], stopIfTrue=True, fill=red_fill))

# Contains text (using Rule directly)
from openpyxl.formatting import Rule
dxf = DifferentialStyle(font=Font(color="9C0006"),
                        fill=PatternFill(bgColor="FFC7CE"))
rule = Rule(type="containsText", operator="containsText", text="highlight", dxf=dxf)
rule.formula = ['NOT(ISERROR(SEARCH("highlight",A1)))']
ws.conditional_formatting.add("A1:F40", rule)
```

CellIsRule operators: `lessThan`, `lessThanOrEqual`, `greaterThan`, `greaterThanOrEqual`, `equal`, `notEqual`, `between`, `notBetween`.

---

## Data Validation

```python
from openpyxl.worksheet.datavalidation import DataValidation

# Dropdown list
dv = DataValidation(type="list", formula1='"Dog,Cat,Bat"', allow_blank=True)
dv.error = "Invalid entry"
dv.errorTitle = "Error"
dv.prompt = "Select from list"
dv.promptTitle = "Selection"
ws.add_data_validation(dv)
dv.add(ws["A1"])
dv.add("B1:B100")  # range string also works

# Whole number
dv = DataValidation(type="whole", operator="greaterThan", formula1=100)

# Decimal between 0 and 1
dv = DataValidation(type="decimal", operator="between", formula1=0, formula2=1)

# Text length
dv = DataValidation(type="textLength", operator="lessThanOrEqual", formula1=15)

# Date / Time
dv = DataValidation(type="date")
dv = DataValidation(type="time")

# Custom formula
dv = DataValidation(type="custom", formula1="=SOMEFORMULA")

# List from another sheet
from openpyxl.utils import quote_sheetname
dv = DataValidation(type="list",
    formula1="{0}!$B$1:$B$10".format(quote_sheetname("Sheet2")))
```

**Note:** Validations without cell ranges are ignored when saving.

---

## Worksheet Tables

```python
from openpyxl.worksheet.table import Table, TableStyleInfo

# Add data first (headers must be strings)
ws.append(["Fruit", "2023", "2024"])
ws.append(["Apples", 10000, 12000])
ws.append(["Pears", 2000, 3000])

tab = Table(displayName="Table1", ref="A1:C3")
style = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False,
                       showLastColumn=False, showRowStripes=True, showColumnStripes=True)
tab.tableStyleInfo = style
ws.add_table(tab)

# Access tables
ws.tables["Table1"]       # by name
ws.tables["A1:C3"]        # by range
del ws.tables["Table1"]   # delete
```

**Important:** Table names must be unique across the workbook. Column headings must be strings. Each table must have a unique `displayName`.

---

## Filters & Sorting

```python
from openpyxl.worksheet.filters import FilterColumn, Filters, CustomFilter, CustomFilters, DateGroupItem

# Set filter range
ws.auto_filter.ref = "A1:B15"

# Filter by specific values
col = FilterColumn(colId=0)  # column A (0-indexed within filter range)
col.filters = Filters(filter=["Kiwi", "Apple", "Mango"])
ws.auto_filter.filterColumn.append(col)

# Sort
ws.auto_filter.add_sort_condition("B2:B15")

# Custom filter (numeric comparison)
flt1 = CustomFilter(operator="lessThan", val=10)
flt2 = CustomFilter(operator="greaterThan", val=90)
cfs = CustomFilters(customFilter=[flt1, flt2])
col = FilterColumn(colId=2, customFilters=cfs)
cfs.and_ = True  # AND condition (default is OR)

# Date filter
df = DateGroupItem(month=3, dateTimeGrouping="month")
col = FilterColumn(colId=1)
col.filters.dateGroupItem.append(df)
```

**Note:** openpyxl only sets filter/sort instructions; they are applied when opened in Excel.

---

## Images

```python
from openpyxl.drawing.image import Image

img = Image("logo.png")
ws.add_image(img, "A1")
```

Requires `pillow`. Confirm `PIL` can be imported before using image features. Supports jpeg, png, bmp formats.

---

## Print Settings

```python
# Page centering
ws.print_options.horizontalCentered = True
ws.print_options.verticalCentered = True

# Headers/footers
ws.oddHeader.left.text = "Page &[Page] of &N"
ws.oddHeader.left.size = 14
ws.oddHeader.left.font = "Tahoma,Bold"
ws.oddHeader.left.color = "CC3366"

# Print titles (repeat on every page)
ws.print_title_cols = "A:B"   # repeat columns
ws.print_title_rows = "1:1"   # repeat rows

# Print area
ws.print_area = "A1:F10"

# Page setup
ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE
ws.page_setup.paperSize = ws.PAPERSIZE_A4  # also PAPERSIZE_LETTER, PAPERSIZE_TABLOID, etc.
ws.page_setup.fitToHeight = 0
ws.page_setup.fitToWidth = 1
```

---

## Defined Names

```python
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.utils import quote_sheetname, absolute_coordinate

# Global named range
ref = f"{quote_sheetname(ws.title)}!{absolute_coordinate('A1:A5')}"
defn = DefinedName("my_range", attr_text=ref)
wb.defined_names.add(defn)

# Local named range (worksheet-scoped)
defn = DefinedName("local_range", attr_text=ref)
ws.defined_names.add(defn)

# Read defined names
for name in wb.defined_names.values():
    for title, coord in name.destinations:
        print(title, coord)
```

**Note:** Cell references must use absolute coordinates and include worksheet name.

---

## Worksheet Properties

```python
from openpyxl.worksheet.properties import WorksheetProperties, PageSetupProperties

# Tab color
ws.sheet_properties.tabColor = "1072BA"

# Page setup properties
ws.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True, autoPageBreaks=False)

# Outline
ws.sheet_properties.outlinePr.summaryBelow = False

# Zoom
ws.sheet_view.zoomScale = 85

# Show formulas
ws.sheet_view.showFormulas = True

# Group columns/rows
ws.column_dimensions.group("A", "D", hidden=True)
ws.row_dimensions.group(1, 10, hidden=True)

# Freeze panes
ws.freeze_panes = "B2"  # freeze row 1 and column A
```

---

## Rich Text

```python
from openpyxl.cell.text import InlineFont
from openpyxl.cell.rich_text import TextBlock, CellRichText

# Create rich text with mixed formatting
rich = CellRichText(
    "Normal text ",
    TextBlock(InlineFont(b=True), "bold text"),
    " and ",
    TextBlock(InlineFont(color="00FF0000", sz=14), "red large text")
)
ws["A1"] = rich

# InlineFont params: rFont (name), sz (size), b (bold), i (italic),
#   strike, color, u (underline), vertAlign
```

**Note:** Load existing rich text with `load_workbook(filename, rich_text=True)`. `InlineFont` uses `rFont` for font name (not `name`). No whitespace is added between elements automatically.

---

## Pivot Tables

openpyxl provides **read-only** support for pivot tables (preserved in existing files, cannot create new ones).

```python
from openpyxl import load_workbook
wb = load_workbook("file.xlsx")
ws = wb["Sheet1"]
pivot = ws._pivots[0]
pivot.cache.refreshOnLoad = True  # refresh on open
```

---

## Optimized Modes

### Read-Only Mode (large files, constant memory)

```python
wb = load_workbook("large.xlsx", read_only=True)
ws = wb["Sheet1"]
for row in ws.rows:
    for cell in row:
        print(cell.value)
wb.close()  # MUST close explicitly
```

### Write-Only Mode (streaming large datasets)

```python
wb = Workbook(write_only=True)
ws = wb.create_sheet()
for i in range(100000):
    ws.append([i, i * 2, i * 3])
wb.save("large_output.xlsx")  # can only save once
```

Write-only limitations: only `append()` for adding rows, no random cell access, freeze panes must be set before adding data.

For styled cells in write-only mode:
```python
from openpyxl.cell import WriteOnlyCell
from openpyxl.styles import Font
cell = WriteOnlyCell(ws, value="styled")
cell.font = Font(bold=True, size=20)
ws.append([cell, 3.14, None])
```

---

## Comments

```python
from openpyxl.comments import Comment

comment = Comment("Comment text", "Author Name")
comment.width = 300   # pixels
comment.height = 50   # pixels
ws["A1"].comment = comment
```

**Note:** Only comment text is preserved; formatting is lost on read. Not supported in `read_only=True` mode.
