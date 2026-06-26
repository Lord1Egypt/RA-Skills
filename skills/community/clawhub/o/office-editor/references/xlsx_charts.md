# Charts Reference

## Table of Contents
1. [Basic Chart Creation](#basic-chart-creation)
2. [Chart Types](#chart-types)
3. [Chart Customization](#chart-customization)
4. [Data References](#data-references)
5. [Complete Example](#complete-example)

## Basic Chart Creation

```python
from openpyxl.chart import BarChart, Reference, Series

values = Reference(ws, min_col=1, min_row=1, max_col=1, max_row=10)
chart = BarChart()
chart.add_data(values)
ws.add_chart(chart, "E15")  # anchor cell
```

Default chart size: 15 x 7.5 cm. Modify with `chart.width` and `chart.height`.

## Chart Types

All chart classes are in `openpyxl.chart`:

| Class | Type | Notes |
|-------|------|-------|
| `BarChart` | Bar/Column | Set `chart.type = "col"` for column, `"bar"` for horizontal |
| `LineChart` | Line | |
| `PieChart` | Pie | |
| `AreaChart` | Area | |
| `ScatterChart` | Scatter/XY | Requires both x and y `Reference` objects |
| `DoughnutChart` | Doughnut | |
| `RadarChart` | Radar | |
| `BubbleChart` | Bubble | Uses `Series` with x, y, and size values |
| `StockChart` | Stock | Requires open/high/low/close data |
| `BarChart3D` | 3D Bar | |
| `LineChart3D` | 3D Line | |
| `PieChart3D` | 3D Pie | |
| `AreaChart3D` | 3D Area | |
| `SurfaceChart` | Surface | |
| `SurfaceChart3D` | 3D Surface | |
| `ProjectedPieChart` | Bar of Pie / Pie of Pie | |

## Chart Customization

```python
chart = BarChart()
chart.type = "col"                    # "col" or "bar"
chart.grouping = "stacked"            # "standard", "stacked", "percentStacked"
chart.title = "Sales Report"
chart.y_axis.title = "Revenue ($)"
chart.x_axis.title = "Quarter"
chart.legend = None                   # remove legend
chart.style = 10                      # built-in style (1-48)
chart.width = 20                      # cm
chart.height = 10                     # cm
```

### Axis Configuration

```python
chart.y_axis.scaling.min = 0
chart.y_axis.scaling.max = 100
chart.y_axis.majorGridlines = None    # remove gridlines
chart.x_axis.tickLblPos = "low"       # label position
chart.y_axis.numFmt = "0.00"          # number format
chart.y_axis.delete = True            # hide axis
```

### Series Styling

```python
from openpyxl.chart.series import DataPoint
from openpyxl.drawing.fill import PatternFillProperties, ColorChoice

series = chart.series[0]
series.graphicalProperties.solidFill = "FF0000"  # fill color
series.graphicalProperties.line.solidFill = "0000FF"  # line color
```

## Data References

```python
from openpyxl.chart import Reference

# Reference(worksheet, min_col, min_row, max_col, max_row)
data = Reference(ws, min_col=2, min_row=1, max_col=4, max_row=10)
cats = Reference(ws, min_col=1, min_row=2, max_row=10)

chart.add_data(data, titles_from_data=True)  # first row as series titles
chart.set_categories(cats)
```

## Complete Example

```python
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference

wb = Workbook()
ws = wb.active

# Add data
ws.append(["Category", "Q1", "Q2", "Q3", "Q4"])
ws.append(["Product A", 100, 150, 130, 180])
ws.append(["Product B", 80, 120, 110, 140])
ws.append(["Product C", 60, 90, 95, 120])

# Create chart
chart = BarChart()
chart.type = "col"
chart.title = "Quarterly Sales"
chart.y_axis.title = "Revenue"
chart.x_axis.title = "Product"

data = Reference(ws, min_col=2, min_row=1, max_col=5, max_row=4)
cats = Reference(ws, min_col=1, min_row=2, max_row=4)
chart.add_data(data, titles_from_data=True)
chart.set_categories(cats)

ws.add_chart(chart, "A6")
wb.save("chart_example.xlsx")
```

### Line Chart Example

```python
from openpyxl.chart import LineChart, Reference

chart = LineChart()
chart.title = "Trend"
data = Reference(ws, min_col=2, min_row=1, max_col=2, max_row=10)
chart.add_data(data, titles_from_data=True)
chart.style = 13
ws.add_chart(chart, "E1")
```

### Pie Chart Example

```python
from openpyxl.chart import PieChart, Reference

pie = PieChart()
pie.title = "Market Share"
data = Reference(ws, min_col=2, min_row=1, max_row=5)
cats = Reference(ws, min_col=1, min_row=2, max_row=5)
pie.add_data(data, titles_from_data=True)
pie.set_categories(cats)
ws.add_chart(pie, "E1")
```

### Scatter Chart Example

```python
from openpyxl.chart import ScatterChart, Reference, Series

chart = ScatterChart()
chart.title = "XY Scatter"
xvalues = Reference(ws, min_col=1, min_row=2, max_row=10)
yvalues = Reference(ws, min_col=2, min_row=2, max_row=10)
series = Series(yvalues, xvalues, title="Data")
chart.series.append(series)
ws.add_chart(chart, "E1")
```

### Combining Charts

```python
from openpyxl.chart import BarChart, LineChart, Reference

# Create bar chart
bar = BarChart()
data1 = Reference(ws, min_col=2, min_row=1, max_col=2, max_row=10)
bar.add_data(data1, titles_from_data=True)

# Create line chart on secondary axis
line = LineChart()
data2 = Reference(ws, min_col=3, min_row=1, max_col=3, max_row=10)
line.add_data(data2, titles_from_data=True)
line.y_axis.axId = 200

# Combine
bar.y_axis.crosses = "min"
bar += line

ws.add_chart(bar, "E1")
```
