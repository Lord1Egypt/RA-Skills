# Chart Creation Guide

## Table of Contents

1. [Column and Bar Charts](#column-and-bar-charts)
2. [Line Charts](#line-charts)
3. [Pie Charts](#pie-charts)
4. [Scatter Charts](#scatter-charts)
5. [Bubble Charts](#bubble-charts)
6. [Chart Customization](#chart-customization)
7. [Common Chart Type Enums](#common-chart-type-enums)

## Column and Bar Charts

```python
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Inches

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[5])

chart_data = CategoryChartData()
chart_data.categories = ["East", "West", "Central"]
chart_data.add_series("Q1 Sales", (19.2, 21.4, 16.7))
chart_data.add_series("Q2 Sales", (22.3, 28.6, 15.2))

chart_frame = slide.shapes.add_chart(
    XL_CHART_TYPE.COLUMN_CLUSTERED,
    Inches(1), Inches(1.5), Inches(8), Inches(5),
    chart_data
)
chart = chart_frame.chart

# Use BAR_CLUSTERED for a horizontal bar chart
# Use COLUMN_STACKED for a stacked column chart
# Use COLUMN_STACKED_100 for a 100% stacked column chart
```

## Line Charts

```python
chart_data = CategoryChartData()
chart_data.categories = ["Jan", "Feb", "Mar", "Apr"]
chart_data.add_series("Product A", (32.2, 28.4, 34.7, 30.1))
chart_data.add_series("Product B", (24.3, 30.6, 20.2, 25.8))

chart = slide.shapes.add_chart(
    XL_CHART_TYPE.LINE, Inches(1), Inches(1.5), Inches(8), Inches(5),
    chart_data
).chart

chart.has_legend = True
chart.legend.include_in_layout = False
chart.series[0].smooth = True  # smooth curve
```

## Pie Charts

```python
chart_data = CategoryChartData()
chart_data.categories = ["East China", "North China", "South China", "West", "Other"]
chart_data.add_series("Market Share", (0.135, 0.324, 0.180, 0.235, 0.126))

chart = slide.shapes.add_chart(
    XL_CHART_TYPE.PIE, Inches(2), Inches(1.5), Inches(6), Inches(5),
    chart_data
).chart

from pptx.enum.chart import XL_LEGEND_POSITION, XL_LABEL_POSITION

chart.has_legend = True
chart.legend.position = XL_LEGEND_POSITION.BOTTOM
chart.legend.include_in_layout = False

plot = chart.plots[0]
plot.has_data_labels = True
data_labels = plot.data_labels
data_labels.number_format = "0%"
data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
```

## Scatter Charts

```python
from pptx.chart.data import XyChartData

chart_data = XyChartData()

series_1 = chart_data.add_series("Model 1")
series_1.add_data_point(0.7, 2.7)
series_1.add_data_point(1.8, 3.2)
series_1.add_data_point(2.6, 0.8)

series_2 = chart_data.add_series("Model 2")
series_2.add_data_point(1.3, 3.7)
series_2.add_data_point(2.7, 2.3)
series_2.add_data_point(1.6, 1.8)

chart = slide.shapes.add_chart(
    XL_CHART_TYPE.XY_SCATTER, Inches(1), Inches(1.5), Inches(8), Inches(5),
    chart_data
).chart
```

## Bubble Charts

```python
from pptx.chart.data import BubbleChartData

chart_data = BubbleChartData()

series_1 = chart_data.add_series("Series 1")
series_1.add_data_point(0.7, 2.7, 10)  # x, y, bubble size
series_1.add_data_point(1.8, 3.2, 4)
series_1.add_data_point(2.6, 0.8, 8)

chart = slide.shapes.add_chart(
    XL_CHART_TYPE.BUBBLE, Inches(1), Inches(1.5), Inches(8), Inches(5),
    chart_data
).chart
```

## Chart Customization

### Axes

```python
from pptx.enum.chart import XL_TICK_MARK
from pptx.util import Pt

# Category axis
category_axis = chart.category_axis
category_axis.has_major_gridlines = True
category_axis.minor_tick_mark = XL_TICK_MARK.OUTSIDE
category_axis.tick_labels.font.italic = True
category_axis.tick_labels.font.size = Pt(10)

# Value axis
value_axis = chart.value_axis
value_axis.maximum_scale = 50.0
value_axis.minimum_scale = 0.0
value_axis.minor_tick_mark = XL_TICK_MARK.OUTSIDE
value_axis.has_minor_gridlines = True

tick_labels = value_axis.tick_labels
tick_labels.number_format = '0"%"'
tick_labels.font.bold = True
tick_labels.font.size = Pt(10)
```

### Data Labels

```python
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_LABEL_POSITION

plot = chart.plots[0]
plot.has_data_labels = True
data_labels = plot.data_labels

data_labels.font.size = Pt(10)
data_labels.font.color.rgb = RGBColor(0x0A, 0x42, 0x80)
data_labels.position = XL_LABEL_POSITION.INSIDE_END
data_labels.number_format = "#,##0"
```

### Legend

```python
from pptx.enum.chart import XL_LEGEND_POSITION

chart.has_legend = True
chart.legend.position = XL_LEGEND_POSITION.BOTTOM
chart.legend.include_in_layout = False
chart.legend.font.size = Pt(10)
```

### Series Colors

```python
from pptx.dml.color import RGBColor

series = chart.series[0]
fill = series.format.fill
fill.solid()
fill.fore_color.rgb = RGBColor(0x4F, 0x81, 0xBD)
```

## Common Chart Type Enums

| Enum Value | Description |
|------------|-------------|
| `COLUMN_CLUSTERED` | Clustered column chart |
| `COLUMN_STACKED` | Stacked column chart |
| `COLUMN_STACKED_100` | 100% stacked column chart |
| `BAR_CLUSTERED` | Clustered bar chart |
| `BAR_STACKED` | Stacked bar chart |
| `LINE` | Line chart |
| `LINE_MARKERS` | Line chart with markers |
| `LINE_STACKED` | Stacked line chart |
| `PIE` | Pie chart |
| `PIE_EXPLODED` | Exploded pie chart |
| `DOUGHNUT` | Doughnut chart |
| `XY_SCATTER` | Scatter chart |
| `XY_SCATTER_LINES` | Scatter chart with lines |
| `XY_SCATTER_SMOOTH` | Smoothed scatter chart |
| `BUBBLE` | Bubble chart |
| `AREA` | Area chart |
| `AREA_STACKED` | Stacked area chart |
| `RADAR` | Radar chart |
