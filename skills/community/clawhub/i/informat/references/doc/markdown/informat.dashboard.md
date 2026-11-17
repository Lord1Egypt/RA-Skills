# Line Chart

A **line chart** is a graph formed by connecting data points with straight line segments. It can intuitively display data change trends. Line charts are commonly used to analyze data trends over time, and can also be used to analyze the interaction and mutual influence of multiple data sets over time.

For example, we can use a line chart to analyze the sales performance of a certain type of product or several related products over time, and further predict future sales. In a line chart, the horizontal axis (X-axis) generally represents the passage of time with equal intervals, while the vertical axis (Y-axis) represents the magnitude of data at different moments.

**Advantages:** Line charts are easy to understand, can be used to analyze the interaction and mutual influence of multiple data sets over time, and provide an immediate sense of trends.

**Disadvantages:** Using multiple lines in a line chart can make it cluttered and difficult to interpret. Therefore, avoid using more than two or three measures.

## Configuration Structure Mapping

The following settings correspond to `_save_dashboard_prochart_card` document's `proChartSetting.series[n].lineSetting` and related configuration fields:

| UI Setting | Corresponding JSON Field Path | Type/Enum Values | Description |
|----------------|-------------------|-------------|------|
| **Data Settings** | | | |
| Data Source | `proChartSetting.dataset[n].id`<br>`proChartSetting.series[n].lineSetting.datasetIndex` | `integer` | Select data source index, must correspond to the `dataset` array index |
| Coordinate System Type | `proChartSetting.series[n].xAxisIndex`<br>`proChartSetting.series[n].yAxisIndex` | `integer` | Reference the corresponding axis configuration via index |
| Name Field | `proChartSetting.series[n].lineSetting.encode.seriesName` | `array<string>` | Field name for legend display |
| X-Axis Field | `proChartSetting.series[n].lineSetting.encode.x` | `array<string>` | Must match the `id` in `dataset.dimensionList` |
| Y-Axis Field | `proChartSetting.series[n].lineSetting.encode.y` | `array<string>` | Must match the `id` in `dataset.dimensionList` |
| **Chart Settings** | | | |
| X-Axis | `proChartSetting.xAxis` | `array<object>` | Supports multiple X-axis configurations |
| Y-Axis | `proChartSetting.yAxis` | `array<object>` | Supports multiple Y-axis configurations |
| Color Assignment Type | `proChartSetting.series[n].colorBy` | `string` | `'data'` or `'series'` |
| Show Symbol | `proChartSetting.series[n].lineSetting.showSymbol` | `boolean` | Whether to show data point markers |
| Symbol Style | `proChartSetting.series[n].lineSetting.symbol` | `string` | `'circle'`, `'rect'`, `'roundRect'`, `'triangle'`, `'diamond'`, `'pin'`, `'arrow'`, `'none'` |
| Symbol Size | `proChartSetting.series[n].lineSetting.symbolSize` | `number` | Marker symbol size |
| Symbol Rotation Angle | `proChartSetting.series[n].lineSetting.symbolRotate` | `number` | (Can be configured in extensions if needed) |
| Display as Step Chart | `proChartSetting.series[n].lineSetting.step` | `string` | `'start'`, `'middle'`, `'end'` (if needed) |
| Smooth Curve Display | `proChartSetting.series[n].lineSetting.smooth` | `boolean` | Whether to display as a smooth curve |
| **Label Settings** | | | |
| Show Label | `proChartSetting.series[n].lineSetting.label.show` | `boolean` | Whether to show data labels |
| Display Content Expression | `proChartSetting.series[n].lineSetting.label.formatter` | `string` | ECharts format string, e.g., `'{c}'` |
| Position | `proChartSetting.series[n].lineSetting.label.position` | `string` | `'top'`, `'left'`, `'right'`, `'bottom'`, `'inside'`, etc. |
| Distance from Symbol | `proChartSetting.series[n].lineSetting.label.distance` | `number` | Distance between label and data point |
| Label Rotation | `proChartSetting.series[n].lineSetting.label.rotate` | `number` | Label rotation angle |
| Text Offset X | `proChartSetting.series[n].lineSetting.label.offset[0]` | `number` | Horizontal offset |
| Text Offset Y | `proChartSetting.series[n].lineSetting.label.offset[1]` | `number` | Vertical offset |
| Color | `proChartSetting.series[n].lineSetting.label.color` | `string` | Label text color |
| Background Color | `proChartSetting.series[n].lineSetting.label.backgroundColor` | `string` | Label background color |
| Font Weight | `proChartSetting.series[n].lineSetting.label.fontWeight` | `string` | `'normal'`, `'bold'`, `'bolder'`, `'lighter'` |
| Font | `proChartSetting.series[n].lineSetting.label.fontFamily` | `string` | Font family |
| Font Size | `proChartSetting.series[n].lineSetting.label.fontSize` | `number/string` | Font size |
| Horizontal Alignment | `proChartSetting.series[n].lineSetting.label.align` | `string` | `'left'`, `'center'`, `'right'` |
| Vertical Alignment | `proChartSetting.series[n].lineSetting.label.verticalAlign` | `string` | `'top'`, `'middle'`, `'bottom'` |
| Border Width | `proChartSetting.series[n].lineSetting.label.borderWidth` | `number` | Label border width |
| Border Color | `proChartSetting.series[n].lineSetting.label.borderColor` | `string` | Label border color |
| Border Radius | `proChartSetting.series[n].lineSetting.label.borderRadius` | `number` | Label border radius |
| Shadow Color | `proChartSetting.series[n].lineSetting.label.shadowColor` | `string` | Shadow color |
| Shadow Blur | `proChartSetting.series[n].lineSetting.label.shadowBlur` | `number` | Shadow blur size |
| Shadow Offset X | `proChartSetting.series[n].lineSetting.label.shadowOffsetX` | `number` | Shadow horizontal offset |
| Shadow Offset Y | `proChartSetting.series[n].lineSetting.label.shadowOffsetY` | `number` | Shadow vertical offset |
| **Line Style** | | | |
| Symbol Color | `proChartSetting.series[n].itemStyle.color` | `string` | Line color |
| Border Color | `proChartSetting.series[n].itemStyle.borderColor` | `string` | Line border color |
| Stroke Type | `proChartSetting.series[n].lineSetting.lineStyle.type` | `string` | `'solid'`, `'dashed'`, `'dotted'` |
| Stroke Width | `proChartSetting.series[n].lineSetting.lineStyle.width` | `number` | Line width |
| Opacity | `proChartSetting.series[n].itemStyle.opacity` | `number` | Opacity (0-1) |
| **Label Layout** | | | |
| Hide Overlapping Labels | `proChartSetting.series[n].labelLayout.hideOverlap` | `boolean` | Whether to hide overlapping labels |
| Overlap Offset Direction | `proChartSetting.series[n].labelLayout.moveOverlap` | `string` | Move direction when overlapping |
| **Emphasis Settings** | | | |
| Disable Emphasis | `proChartSetting.series[n].emphasis.disabled` | `boolean` | Whether to disable emphasis |
| Emphasis Behavior | `proChartSetting.series[n].emphasis.focus` | `string` | `'self'`, `'series'`, `'none'` |
| Blur Scope | `proChartSetting.series[n].emphasis.blurScope` | `string` | `'coordinateSystem'`, `'series'`, `'global'` |
| **Area Chart Settings** | | | |
| Enable Area | `proChartSetting.series[n].lineSetting.areaStyle` | `object` | Area fill is enabled when not empty |
| Fill Mode | `proChartSetting.series[n].lineSetting.areaStyle.origin` | `string` | `'auto'`, `'start'`, `'end'` |
| Color | `proChartSetting.series[n].lineSetting.areaStyle.color` | `string/object` | Fill color or gradient |
| Opacity | `proChartSetting.series[n].lineSetting.areaStyle.opacity` | `number` | Fill opacity (0-1) |
| **Stack Settings** | | | |
| Stack Identifier | `proChartSetting.series[n].lineSetting.stack` | `string` | Charts with the same identifier will be stacked |
| Stack Strategy | `proChartSetting.series[n].lineSetting.stackStrategy` | `string` | `'all'`, `'positive'`, `'negative'` (if needed) |

## Stack Configuration

### Stack Rules

Stacking refers to overlaying multiple chart values together to form a new chart display. Stacking is commonly used in `bar chart stacking` and `line chart area stacking`. Compared to bar chart stacking, line chart area stacking is more suitable for scenarios with a large number of groups. Note that line chart area stacking `is not suitable for datasets with negative values`.

Line chart area stacking refers to drawing multiple datasets as vertically stacked areas. Stacked area charts are the same as basic area charts, with the only difference being that each dataset starts from a different point - it is based on the previous dataset. This is used to show trends in the size of each value over time or category, displaying the relationship between parts and the whole.

**Important Rule:** When implementing a stacking effect, you must create a separate data source and a corresponding chart instance for each stacking series. In the chart list `series`, each item's `datasetIndex` corresponds to the data source index, and each chart's `datasetIndex` value should correspond one-to-one with the data source subscript.

### Stack Configuration Items
| Setting | Description | Corresponding Field Identifier |
|--------|------|--------------|
| Stack Identifier | Set the stack identifier for each chart separately. The system will stack chart shapes with the same identifier together. | `stack` |
| Stack Strategy | Set different value strategies for stacking based on positive/negative chart values. | `stackStrategy` |

### Stack Example
**Example:** To display "monthly sales for each department" using a line chart, you need to create separate data sources and charts for "Department A", "Department B", etc.:
- Department A data source has index 0 in `dataset`, Department B data source has index 1
- The corresponding line chart configuration's `datasetIndex` needs to be set to 0 and 1 respectively
- Set the same `stack` value to achieve the stacking effect

## Event Configuration
| Setting | Description | Corresponding Field Identifier |
|--------|------|--------------|
| Non-clickable | When enabled, all label data in the chart cannot be clicked. When disabled, corresponding data click interaction events can be set | `silent` |
| Click to Trigger Automation | Select the corresponding automation to implement data label click interaction events, such as opening the corresponding data form details or other web links after clicking | `eventHandlers.click` |
| Double-click to Trigger Automation | Same function as click trigger, but interaction changes from single click to double click. Click and double-click events can be set simultaneously | `eventHandlers.dblclick` |

## Polar Coordinate Supplement
Polar coordinates simply describe position using angle and length. It has a significantly different display effect compared to line charts and bar charts in Cartesian coordinate systems. Polar coordinate systems can generally be used with bar charts, line charts, and scatter charts.

When using polar coordinates, you need to understand the following:
Polar coordinate systems generally have two axes, called `radius axis` and `angle axis`, corresponding to the radial (radius) axis and angle (arc) axis of the polar coordinate system respectively. There are also four types of axis measurement types: `value axis`, `category axis`, `time axis`, and `log axis`. Selecting different axis types will result in different data scales displayed on the chart. The usage scenarios for the four axis types are as follows:

| Setting | Description | Corresponding Field Identifier |
|--------|------|--------------|
| Value Axis | 'value': Value axis, suitable for continuous data, representing values through the length of the radius. | `radiusAxis.type: 'value'` |
| Category Axis | 'category': Category axis, suitable for discrete categorical data, representing each category value through fixed radius lengths | `angleAxis.type: 'category'` |
| Time Axis | 'time': Time axis, suitable for continuous time-series data. Compared to value axis, the time axis has time formatting, and the radius reflects the sequential change of time points. | `radiusAxis.type: 'time'` |
| Log Axis | 'log': Logarithmic axis, suitable for logarithmic data, commonly used in line charts for dual value axis presentation. | `radiusAxis.type: 'log'` |

## Important Rules

### 1. Data Source Field Matching Rules
- **Field Source**: Fields used in `encode` must exist in the corresponding `dataset`'s `dimensionList`
- **Aggregation Field Naming**: If aggregation query is enabled (`aggregation=true`), the field ID format is `fieldID_functionName`, e.g., `sales_sum`
- **Prohibited Aggregation Fields**: `id` and `seq` fields cannot be used for aggregation

### 2. Stacked Chart Implementation
- Each stacking series needs an independent data source and chart instance
- Example: To display "quantity of each check-in type per employee", you need to create an independent data source for each check-in type
- The data source index in the `dataset` array must correspond to `series.lineSetting.datasetIndex`

### 3. Multi-Coordinate System Support
- Supports Cartesian coordinate system (X/Y axes) and polar coordinate system (angle/radius axes)
- Polar coordinate configuration is in `proChartSetting.angleAxis` and `proChartSetting.radiusAxis`
- Line charts can reference specific axes via `xAxisIndex` and `yAxisIndex`

### 4. Style Priority
- Chart title position must be explicitly set to avoid overlapping with the legend
- `cardStyle.titlePosition` controls the card title position
- `proChartSetting.title.left/top` controls the chart title position


# Bar Chart

A **bar chart** is a statistical chart that uses the length of rectangles with equal widths as variables.

Generally, a bar chart has only one variable and is more suitable for analyzing smaller datasets. Rectangular bars are generally used to display the count values of different levels of a variable. By observing the length and variation of the bars, you can obtain the differences between one or more bar data variables, providing feedback on data stability, variance, etc., to guide and optimize actual business operations.

**Advantages:** Bar charts are simple and intuitive. It is easy to see the magnitude of values based on the length of bars, making it easy to compare differences between data groups.

**Disadvantages:** Bar charts are not suitable for expressing trend data (line charts or area charts are more appropriate), nor for expressing proportional data (pie charts are more suitable).

## Configuration Structure Mapping

The following settings correspond to `_save_dashboard_prochart_card` document's `proChartSetting.series[n].barSetting` and related configuration fields:

| UI Setting | Corresponding JSON Field Path | Type/Enum Values | Description |
|----------------|-------------------|-------------|------|
| **Data Settings** | | | |
| Data Source | `proChartSetting.dataset[n].id`<br>`proChartSetting.series[n].barSetting.datasetIndex` | `integer` | Select data source index, must correspond to the `dataset` array index |
| Coordinate System Type | `proChartSetting.series[n].xAxisIndex`<br>`proChartSetting.series[n].yAxisIndex` | `integer` | Reference the corresponding axis configuration via index |
| Name Field | `proChartSetting.series[n].barSetting.encode.seriesName` | `array<string>` | Field name for legend display |
| X-Axis Field | `proChartSetting.series[n].barSetting.encode.x` | `array<string>` | Must match the `id` in `dataset.dimensionList` |
| Y-Axis Field | `proChartSetting.series[n].barSetting.encode.y` | `array<string>` | Must match the `id` in `dataset.dimensionList` |
| **Chart Settings** | | | |
| X-Axis | `proChartSetting.xAxis` | `array<object>` | Supports multiple X-axis configurations |
| Y-Axis | `proChartSetting.yAxis` | `array<object>` | Supports multiple Y-axis configurations |
| Color Assignment Type | `proChartSetting.series[n].colorBy` | `string` | `'data'` or `'series'` |
| Bar Width | `proChartSetting.series[n].barSetting.barWidth` | `string/number` | Bar width (e.g., `'40%'` or pixel value) |
| Maximum Bar Width | `proChartSetting.series[n].barSetting.barMaxWidth` | `string/number` | Maximum bar width |
| Minimum Bar Width | `proChartSetting.series[n].barSetting.barMinWidth` | `string/number` | Minimum bar width |
| Minimum Bar Height | `proChartSetting.series[n].barSetting.barMinHeight` | `number` | Minimum bar height (pixels) |
| Gap Between Different Charts | `proChartSetting.series[n].barSetting.barGap` | `string` | Gap between bars of different series (e.g., `'30%'`) |
| Gap Within Same Chart | `proChartSetting.series[n].barSetting.barCategoryGap` | `string` | Gap between bars of the same series (e.g., `'20%'`) |
| **Label Settings** | | | |
| Show Label | `proChartSetting.series[n].barSetting.label.show` | `boolean` | Whether to show data labels |
| Display Content Expression | `proChartSetting.series[n].barSetting.label.formatter` | `string` | ECharts format string, e.g., `'{c}'` |
| Position | `proChartSetting.series[n].barSetting.label.position` | `string` | `'top'`, `'insideTop'`, `'inside'`, `'right'`, etc. |
| Distance from Symbol | `proChartSetting.series[n].barSetting.label.distance` | `number` | Distance between label and bar |
| Label Rotation | `proChartSetting.series[n].barSetting.label.rotate` | `number` | Label rotation angle |
| Text Offset X | `proChartSetting.series[n].barSetting.label.offset[0]` | `number` | Horizontal offset |
| Text Offset Y | `proChartSetting.series[n].barSetting.label.offset[1]` | `number` | Vertical offset |
| Color | `proChartSetting.series[n].barSetting.label.color` | `string` | Label text color |
| Background Color | `proChartSetting.series[n].barSetting.label.backgroundColor` | `string` | Label background color |
| Font Weight | `proChartSetting.series[n].barSetting.label.fontWeight` | `string` | `'normal'`, `'bold'`, `'bolder'`, `'lighter'` |
| Font | `proChartSetting.series[n].barSetting.label.fontFamily` | `string` | Font family |
| Font Size | `proChartSetting.series[n].barSetting.label.fontSize` | `number/string` | Font size |
| Horizontal Alignment | `proChartSetting.series[n].barSetting.label.align` | `string` | `'left'`, `'center'`, `'right'` |
| Vertical Alignment | `proChartSetting.series[n].barSetting.label.verticalAlign` | `string` | `'top'`, `'middle'`, `'bottom'` |
| Border Width | `proChartSetting.series[n].barSetting.label.borderWidth` | `number` | Label border width |
| Border Color | `proChartSetting.series[n].barSetting.label.borderColor` | `string` | Label border color |
| Border Radius | `proChartSetting.series[n].barSetting.label.borderRadius` | `number` | Label border radius |
| Shadow Color | `proChartSetting.series[n].barSetting.label.shadowColor` | `string` | Shadow color |
| Shadow Blur | `proChartSetting.series[n].barSetting.label.shadowBlur` | `number` | Shadow blur size |
| Shadow Offset X | `proChartSetting.series[n].barSetting.label.shadowOffsetX` | `number` | Shadow horizontal offset |
| Shadow Offset Y | `proChartSetting.series[n].barSetting.label.shadowOffsetY` | `number` | Shadow vertical offset |
| **Bar Style** | | | |
| Color | `proChartSetting.series[n].barSetting.itemStyle.color` | `string` | Bar color |
| Border Color | `proChartSetting.series[n].barSetting.itemStyle.borderColor` | `string` | Bar border color |
| Stroke Type | `proChartSetting.series[n].barSetting.itemStyle.borderType` | `string` | `'solid'`, `'dashed'`, `'dotted'` |
| Stroke Width | `proChartSetting.series[n].barSetting.itemStyle.borderWidth` | `number` | Bar border width |
| Border Radius | `proChartSetting.series[n].barSetting.itemStyle.borderRadius` | `number/array` | Bar border radius |
| Opacity | `proChartSetting.series[n].barSetting.itemStyle.opacity` | `number` | Bar opacity (0-1) |
| **Label Layout** | | | |
| Hide Overlapping Labels | `proChartSetting.series[n].labelLayout.hideOverlap` | `boolean` | Whether to hide overlapping labels |
| Overlap Offset Direction | `proChartSetting.series[n].labelLayout.moveOverlap` | `string` | Move direction when overlapping |
| **Emphasis Settings** | | | |
| Disable Emphasis | `proChartSetting.series[n].emphasis.disabled` | `boolean` | Whether to disable emphasis |
| Emphasis Behavior | `proChartSetting.series[n].emphasis.focus` | `string` | `'self'`, `'series'`, `'none'` |
| Blur Scope | `proChartSetting.series[n].emphasis.blurScope` | `string` | `'coordinateSystem'`, `'series'`, `'global'` |
| **Background Settings** | | | |
| Show Bar Background | `proChartSetting.series[n].barSetting.showBackground` | `boolean` | Whether to show bar background |
| Background Color | `proChartSetting.series[n].barSetting.backgroundStyle.color` | `string` | Bar background color |
| Background Border Color | `proChartSetting.series[n].barSetting.backgroundStyle.borderColor` | `string` | Background border color |
| Background Border Width | `proChartSetting.series[n].barSetting.backgroundStyle.borderWidth` | `number` | Background border width |

## Stack Configuration

### Stack Rules

Stacking refers to overlaying multiple chart values together to form a new chart display. In bar chart stacking, bars are stacked on top of each other to form a new bar. Stacked bar charts can vividly display the data of each sub-category contained in a main category, as well as the proportion of each sub-category, showing the relationship between individual items and the whole.

**Important Rule:** When implementing a stacking effect, you must create a separate data source and a corresponding chart instance for each stacking series. In the chart list `series`, each item's `datasetIndex` corresponds to the data source index, and each chart's `datasetIndex` value should correspond one-to-one with the data source subscript.

### Stack Configuration Items
| Setting | Description | Corresponding Field Identifier |
|--------|------|--------------|
| Stack Identifier | Set the stack identifier for each chart separately. The system will stack chart shapes with the same identifier together. | `stack` |
| Stack Strategy | Set different value strategies for stacking based on positive/negative chart values. | `stackStrategy` |

### Stack Example
**Example:** To display "monthly sales for each department" using a bar chart, you need to create separate data sources and charts for "Department A", "Department B", etc.:
- Department A data source has index 0 in `dataset`, Department B data source has index 1
- The corresponding bar chart configuration's `datasetIndex` needs to be set to 0 and 1 respectively
- Set the same `stack` value to achieve the stacking effect

## Event Configuration
| Setting | Description | Corresponding Field Identifier |
|--------|------|--------------|
| Non-clickable | When enabled, all label data in the chart cannot be clicked. When disabled, corresponding data click interaction events can be set | `silent` |
| Click to Trigger Automation | Select the corresponding automation to implement data label click interaction events, such as opening the corresponding data form details or other web links after clicking | `eventHandlers.click` |
| Double-click to Trigger Automation | Same function as click trigger, but interaction changes from single click to double click. Click and double-click events can be set simultaneously | `eventHandlers.dblclick` |

## Polar Coordinate Supplement

Polar coordinates simply describe position using angle and length. It has a significantly different display effect compared to line charts and bar charts in Cartesian coordinate systems. Polar coordinate systems can generally be used with bar charts, line charts, and scatter charts.

### Polar Coordinate Axis Types
| Setting | Description | Corresponding Field Identifier |
|--------|------|--------------|
| Value Axis | Value axis, suitable for continuous data, representing values through the length of the radius | `radiusAxis.type: 'value'` |
| Category Axis | Category axis, suitable for discrete categorical data, representing each category value through fixed radius lengths | `angleAxis.type: 'category'` |
| Time Axis | Time axis, suitable for continuous time-series data, the radius reflects the sequential change of time points | `radiusAxis.type: 'time'` |
| Log Axis | Logarithmic axis, suitable for logarithmic data, commonly used in line charts for dual value axis presentation | `radiusAxis.type: 'log'` |


# Pie Chart

A **pie chart**, also called a pie graph, uses the area of sectors (i.e., the central angle) to represent the count or percentage of variables. Pie charts are mainly used to represent the internal composition of data with few categories or discrete quantitative data, and the percentages of all parts must sum to 100%.

Pie charts are primarily used for nominal or categorical data, making it easy for users to understand the relationship between parts and the whole of a variable. By looking at the size of each sector area in the circle, you can determine how much a particular part accounts for in the total. When variables have many levels, bar charts or stacked filled bar charts can provide better visualization.

**Advantages:** Due to the special nature of the graphical method, pie charts display graphic effects more intuitively and are easier to show proportional relationships.

**Disadvantages:** Pie charts are not suitable for displaying data with too many categories, negative values, or zero values. When the proportions of data are very close, human eye judgment becomes difficult, so ring charts or 3D pie charts are recommended.

## Configuration Structure Mapping

The following settings correspond to `_save_dashboard_prochart_card` document's `proChartSetting.series[n].pieSetting` and related configuration fields:

| UI Setting | Corresponding JSON Field Path | Type/Enum Values | Description |
|----------------|-------------------|-------------|------|
| **Data Settings** | | | |
| Data Source | `proChartSetting.dataset[n].id`<br>`proChartSetting.series[n].pieSetting.datasetIndex` | `integer` | Select data source index, must correspond to the `dataset` array index |
| Name Field | `proChartSetting.series[n].pieSetting.encode.itemName` | `string` | Must match the `id` in `dataset.dimensionList` |
| Value Field | `proChartSetting.series[n].pieSetting.encode.value` | `array<string>` | Must match the `id` in `dataset.dimensionList` |
| **Chart Settings** | | | |
| Color Assignment Type | `proChartSetting.series[n].colorBy` | `string` | `'data'` or `'series'` |
| Clockwise Arrangement | `proChartSetting.series[n].pieSetting.clockwise` | `boolean` | Whether to arrange sectors clockwise |
| Rose Chart Style | `proChartSetting.series[n].pieSetting.roseType` | `string` | `'radius'` (sector central angle shows data percentage), `'area'` (all sectors have equal central angle), `null` (normal pie chart) |
| Prevent Label Overlap | `proChartSetting.series[n].pieSetting.avoidLabelOverlap` | `boolean` | Whether to enable adaptive layout to prevent label overlap |
| Inner Radius | `proChartSetting.series[n].pieSetting.radius[0]` | `string` | Inner circle radius (e.g., `'0%'`, `'40%'`) |
| Outer Radius | `proChartSetting.series[n].pieSetting.radius[1]` | `string` | Outer circle radius (e.g., `'75%'`, `'100%'`) |
| Center X | `proChartSetting.series[n].pieSetting.center[0]` | `string` | Circle center horizontal position (e.g., `'50%'`, `'200'`) |
| Center Y | `proChartSetting.series[n].pieSetting.center[1]` | `string` | Circle center vertical position (e.g., `'50%'`, `'300'`) |
| Z-index | `proChartSetting.series[n].z` | `number` | Chart display priority level |
| Left | `proChartSetting.series[n].left` | `string/number` | Distance from chart to container left |
| Right | `proChartSetting.series[n].right` | `string/number` | Distance from chart to container right |
| Top | `proChartSetting.series[n].top` | `string/number` | Distance from chart to container top |
| Bottom | `proChartSetting.series[n].bottom` | `string/number` | Distance from chart to container bottom |
| Width | `proChartSetting.series[n].width` | `string/number` | Chart width, auto-adaptive if not set |
| Height | `proChartSetting.series[n].height` | `string/number` | Chart height, auto-adaptive if not set |
| Show Label Line | `proChartSetting.series[n].pieSetting.labelLine.show` | `boolean` | Whether to show label guide lines |
| Show Above Symbol | `proChartSetting.series[n].pieSetting.label.position` | `string` | `'inside'`, `'outside'`, `'center'` |
| Smooth Line | `proChartSetting.series[n].pieSetting.labelLine.smooth` | `boolean` | Whether label guide lines have smooth effect |
| **Label Settings** | | | |
| Show Label | `proChartSetting.series[n].pieSetting.label.show` | `boolean` | Whether to show data labels |
| Display Content Expression | `proChartSetting.series[n].pieSetting.label.formatter` | `string` | ECharts format string, e.g., `'{b}: {c} ({d}%)'` |
| Position | `proChartSetting.series[n].pieSetting.label.position` | `string` | `'inside'`, `'outside'`, `'center'` |
| Distance from Symbol | `proChartSetting.series[n].pieSetting.label.distance` | `number` | Distance between label and sector |
| Label Rotation | `proChartSetting.series[n].pieSetting.label.rotate` | `number` | Label rotation angle |
| Text Offset X | `proChartSetting.series[n].pieSetting.label.offset[0]` | `number` | Horizontal offset |
| Text Offset Y | `proChartSetting.series[n].pieSetting.label.offset[1]` | `number` | Vertical offset |
| Color | `proChartSetting.series[n].pieSetting.label.color` | `string` | Label text color |
| Background Color | `proChartSetting.series[n].pieSetting.label.backgroundColor` | `string` | Label background color |
| Font Weight | `proChartSetting.series[n].pieSetting.label.fontWeight` | `string` | `'normal'`, `'bold'`, `'bolder'`, `'lighter'` |
| Font | `proChartSetting.series[n].pieSetting.label.fontFamily` | `string` | Font family |
| Font Size | `proChartSetting.series[n].pieSetting.label.fontSize` | `number/string` | Font size |
| Horizontal Alignment | `proChartSetting.series[n].pieSetting.label.align` | `string` | `'left'`, `'center'`, `'right'` |
| Vertical Alignment | `proChartSetting.series[n].pieSetting.label.verticalAlign` | `string` | `'top'`, `'middle'`, `'bottom'` |
| Border Width | `proChartSetting.series[n].pieSetting.label.borderWidth` | `number` | Label border width |
| Border Color | `proChartSetting.series[n].pieSetting.label.borderColor` | `string` | Label border color |
| Border Radius | `proChartSetting.series[n].pieSetting.label.borderRadius` | `number` | Label border radius |
| Shadow Color | `proChartSetting.series[n].pieSetting.label.shadowColor` | `string` | Shadow color |
| Shadow Blur | `proChartSetting.series[n].pieSetting.label.shadowBlur` | `number` | Shadow blur size |
| Shadow Offset X | `proChartSetting.series[n].pieSetting.label.shadowOffsetX` | `number` | Shadow horizontal offset |
| Shadow Offset Y | `proChartSetting.series[n].pieSetting.label.shadowOffsetY` | `number` | Shadow vertical offset |
| **Sector Style** | | | |
| Color | `proChartSetting.series[n].itemStyle.color` | `string` | Sector color |
| Border Color | `proChartSetting.series[n].itemStyle.borderColor` | `string` | Sector border color |
| Stroke Type | `proChartSetting.series[n].itemStyle.borderType` | `string` | `'solid'`, `'dashed'`, `'dotted'` |
| Stroke Width | `proChartSetting.series[n].itemStyle.borderWidth` | `number` | Sector border width |
| Border Radius | `proChartSetting.series[n].itemStyle.borderRadius` | `number` | Sector border radius |
| Shadow Color | `proChartSetting.series[n].itemStyle.shadowColor` | `string` | Sector shadow color |
| Shadow Blur | `proChartSetting.series[n].itemStyle.shadowBlur` | `number` | Sector shadow blur size |
| Shadow Offset X | `proChartSetting.series[n].itemStyle.shadowOffsetX` | `number` | Sector shadow horizontal offset |
| Shadow Offset Y | `proChartSetting.series[n].itemStyle.shadowOffsetY` | `number` | Sector shadow vertical offset |
| Opacity | `proChartSetting.series[n].itemStyle.opacity` | `number` | Sector opacity (0-1) |
| **Label Layout** | | | |
| Hide Overlapping Labels | `proChartSetting.series[n].labelLayout.hideOverlap` | `boolean` | Whether to hide overlapping labels |
| Overlap Offset Direction | `proChartSetting.series[n].labelLayout.moveOverlap` | `string` | Move direction when overlapping |
| **Emphasis Settings** | | | |
| Disable Emphasis | `proChartSetting.series[n].emphasis.disabled` | `boolean` | Whether to disable emphasis |
| Emphasis Behavior | `proChartSetting.series[n].emphasis.focus` | `string` | `'self'`, `'series'`, `'none'` |
| Blur Scope | `proChartSetting.series[n].emphasis.blurScope` | `string` | `'coordinateSystem'`, `'series'`, `'global'` |

## Doughnut Chart and Rose Chart Configuration

### Doughnut Chart Configuration
A doughnut chart is a variant of the pie chart, achieved by setting the inner radius greater than 0:
```json
{
  "proChartSetting": {
    "series": [{
      "type": "pie",
      "pieSetting": {
        "radius": ["40%", "70%"],  // Inner radius 40%, outer radius 70%
        "center": ["50%", "50%"]
      }
    }]
  }
}
```

### Rose Chart Configuration

Rose charts are configured through the `roseType` parameter:

- **Area Rose Chart**: `roseType: 'area'` - All sectors have the same central angle, different radii
- **Radius Rose Chart**: `roseType: 'radius'` - Sector central angle shows data percentage

```json
{
  "proChartSetting": {
    "series": [{
      "type": "pie",
      "pieSetting": {
        "roseType": "radius",
        "radius": ["30%", "90%"]
      }
    }]
  }
}
```

## Important Rules

### 1. Data Source Field Matching Rules
- **Field Source**: `itemName` and `value` fields used in `encode` must exist in the corresponding `dataset`'s `dimensionList`
- **Aggregation Field Naming**: If aggregation query is enabled (`aggregation=true`), the value field ID format is `fieldID_functionName`, e.g., `sales_sum`
- **Prohibited Aggregation Fields**: `id` and `seq` fields cannot be used for aggregation
- **Data Type Requirements**: Pie chart value fields should be numeric types

### 2. Multi-Pie Configuration
- Multiple pie chart series can be configured in one card
- Each pie chart series can reference different data sources (specified via `datasetIndex`)
- Control the position and size of each pie chart via `center`, `radius`, `width`, `height`, and other parameters

### 3. Label and Guide Line Configuration
- Pie chart labels are displayed outside the sector by default
- When `label.position` is set to `'inside'`, labels are displayed inside the sector
- `labelLine` configures the style and display of label guide lines
- `avoidLabelOverlap` can automatically adjust label positions to avoid overlap

### 4. Style Configuration Rules
- Chart title position must be explicitly set to avoid overlapping with the legend
- `cardStyle.titlePosition` controls the card title position
- `proChartSetting.title.left/top` controls the chart title position
- Pie chart colors can be individually set via `itemStyle.color` or uniformly configured via the color palette

## Best Practice Recommendations

### 1. Data Volume Control
- Pie charts are suitable for displaying **3-8** data categories
- Too many categories will result in sectors that are too small, affecting readability
- For too many categories, consider:
    - Merging small-proportion data into an "Other" category
    - Using a bar chart instead
    - Using multiple pie charts for grouped display

### 2. Percentage Display
- It is recommended to display percentages in labels, format: `{b}: {c} ({d}%)`
- Ensure the sum of all sector percentages is 100% (the system calculates this automatically)

### 3. Color Usage
- Use contrasting colors to distinguish different sectors
- Avoid similar colors for adjacent sectors
- Colors can be uniformly configured through the color palette theme

### 4. Doughnut Chart Usage Scenarios
- Use doughnut charts when you need to emphasize the center area
- The center of a doughnut chart can display total data or other important information
- Control the width of the ring by adjusting the inner radius

### 5. Interaction Optimization
- Enable `tooltip` by default to display detailed information
- Consider enabling selection effects (`selectedMode`) to highlight key data
- For complex pie charts, you can enable emphasis and fade effects

# Scatter Chart

A **scatter chart**, also called a correlation chart, plots data of two potentially related variables as points on a coordinate graph. By observing the general trend of how the dependent variable (Y-axis values) changes with the independent variable (X-axis values), it is used to study the relationship between one variable and other variables.

When the relationship between two factors is unknown or the understanding of the relationship is vague and needs investigation and confirmation, scatter charts can be used to determine the relationship between them. It is important to note that when using scatter charts to investigate the relationship between two factors, other factors that affect these two factors should be fixed as much as possible to ensure more accurate results.

**Advantages:** Scatter charts are ideal for handling value distributions and data point clustering.

**Disadvantages:** Scatter charts look relatively cluttered and can basically only show correlation, distribution, and aggregation. Other information cannot be well represented.

## Configuration Structure Mapping

The following settings correspond to `_save_dashboard_prochart_card` document's `proChartSetting.series[n].scatterSetting` and related configuration fields:

| UI Setting | Corresponding JSON Field Path | Type/Enum Values | Description |
|----------------|-------------------|-------------|------|
| **Data Settings** | | | |
| Data Source | `proChartSetting.dataset[n].id`<br>`proChartSetting.series[n].scatterSetting.datasetIndex` | `integer` | Select data source index, must correspond to the `dataset` array index |
| Coordinate System Type | `proChartSetting.series[n].xAxisIndex`<br>`proChartSetting.series[n].yAxisIndex` | `integer` | Reference the corresponding axis configuration via index |
| Name Field | `proChartSetting.series[n].scatterSetting.encode.seriesName` | `array<string>` | Field name for legend display |
| X-Axis Field | `proChartSetting.series[n].scatterSetting.encode.x` | `array<string>` | Must match the `id` in `dataset.dimensionList` |
| Y-Axis Field | `proChartSetting.series[n].scatterSetting.encode.y` | `array<string>` | Must match the `id` in `dataset.dimensionList` |
| **Chart Settings** | | | |
| X-Axis | `proChartSetting.xAxis` | `array<object>` | Supports multiple X-axis configurations |
| Y-Axis | `proChartSetting.yAxis` | `array<object>` | Supports multiple Y-axis configurations |
| Color Assignment Type | `proChartSetting.series[n].colorBy` | `string` | `'data'` or `'series'` |
| Symbol Style | `proChartSetting.series[n].scatterSetting.symbol` | `string` | `'circle'`, `'rect'`, `'roundRect'`, `'triangle'`, `'diamond'`, `'pin'`, `'arrow'`, `'none'` |
| Symbol Size | `proChartSetting.series[n].scatterSetting.symbolSize` | `number` | Scatter symbol size |
| Symbol Rotation Angle | `proChartSetting.series[n].scatterSetting.symbolRotate` | `number` | Scatter symbol rotation angle |
| **Label Settings** | | | |
| Show Label | `proChartSetting.series[n].scatterSetting.label.show` | `boolean` | Whether to show data labels |
| Display Content Expression | `proChartSetting.series[n].scatterSetting.label.formatter` | `string` | ECharts format string |
| Position | `proChartSetting.series[n].scatterSetting.label.position` | `string` | `'top'`, `'left'`, `'right'`, `'bottom'`, `'inside'`, etc. |
| Distance from Symbol | `proChartSetting.series[n].scatterSetting.label.distance` | `number` | Distance between label and scatter point |
| Label Rotation | `proChartSetting.series[n].scatterSetting.label.rotate` | `number` | Label rotation angle |
| Text Offset X | `proChartSetting.series[n].scatterSetting.label.offset[0]` | `number` | Horizontal offset |
| Text Offset Y | `proChartSetting.series[n].scatterSetting.label.offset[1]` | `number` | Vertical offset |
| Color | `proChartSetting.series[n].scatterSetting.label.color` | `string` | Label text color |
| Background Color | `proChartSetting.series[n].scatterSetting.label.backgroundColor` | `string` | Label background color |
| Font Weight | `proChartSetting.series[n].scatterSetting.label.fontWeight` | `string` | `'normal'`, `'bold'`, `'bolder'`, `'lighter'` |
| Font | `proChartSetting.series[n].scatterSetting.label.fontFamily` | `string` | Font family |
| Font Size | `proChartSetting.series[n].scatterSetting.label.fontSize` | `number/string` | Font size |
| Horizontal Alignment | `proChartSetting.series[n].scatterSetting.label.align` | `string` | `'left'`, `'center'`, `'right'` |
| Vertical Alignment | `proChartSetting.series[n].scatterSetting.label.verticalAlign` | `string` | `'top'`, `'middle'`, `'bottom'` |
| Border Width | `proChartSetting.series[n].scatterSetting.label.borderWidth` | `number` | Label border width |
| Border Color | `proChartSetting.series[n].scatterSetting.label.borderColor` | `string` | Label border color |
| Border Radius | `proChartSetting.series[n].scatterSetting.label.borderRadius` | `number` | Label border radius |
| Shadow Color | `proChartSetting.series[n].scatterSetting.label.shadowColor` | `string` | Shadow color |
| Shadow Blur | `proChartSetting.series[n].scatterSetting.label.shadowBlur` | `number` | Shadow blur size |
| Shadow Offset X | `proChartSetting.series[n].scatterSetting.label.shadowOffsetX` | `number` | Shadow horizontal offset |
| Shadow Offset Y | `proChartSetting.series[n].scatterSetting.label.shadowOffsetY` | `number` | Shadow vertical offset |
| **Scatter Style** | | | |
| Color | `proChartSetting.series[n].itemStyle.color` | `string` | Scatter color |
| Border Color | `proChartSetting.series[n].itemStyle.borderColor` | `string` | Scatter border color |
| Stroke Type | `proChartSetting.series[n].itemStyle.borderType` | `string` | `'solid'`, `'dashed'`, `'dotted'` |
| Stroke Width | `proChartSetting.series[n].itemStyle.borderWidth` | `number` | Scatter border width |
| Border Radius | `proChartSetting.series[n].itemStyle.borderRadius` | `number` | Scatter border radius |
| Shadow Color | `proChartSetting.series[n].itemStyle.shadowColor` | `string` | Scatter shadow color |
| Shadow Blur | `proChartSetting.series[n].itemStyle.shadowBlur` | `number` | Scatter shadow blur size |
| Shadow Offset X | `proChartSetting.series[n].itemStyle.shadowOffsetX` | `number` | Scatter shadow horizontal offset |
| Shadow Offset Y | `proChartSetting.series[n].itemStyle.shadowOffsetY` | `number` | Scatter shadow vertical offset |
| Opacity | `proChartSetting.series[n].itemStyle.opacity` | `number` | Scatter opacity (0-1) |
| **Label Layout** | | | |
| Hide Overlapping Labels | `proChartSetting.series[n].labelLayout.hideOverlap` | `boolean` | Whether to hide overlapping labels |
| Overlap Offset Direction | `proChartSetting.series[n].labelLayout.moveOverlap` | `string` | Move direction when overlapping |
| **Emphasis Settings** | | | |
| Disable Emphasis | `proChartSetting.series[n].emphasis.disabled` | `boolean` | Whether to disable emphasis |
| Emphasis Behavior | `proChartSetting.series[n].emphasis.focus` | `string` | `'self'`, `'series'`, `'none'` |
| Blur Scope | `proChartSetting.series[n].emphasis.blurScope` | `string` | `'coordinateSystem'`, `'series'`, `'global'` |

## Bubble Chart Configuration

### Bubble Chart Implementation Principle
Scatter charts can achieve bubble chart effects through the `symbolSize` field:
- **Fixed Size**: `symbolSize: 10` - All scatter points have the same size
- **Dynamic Size**: `symbolSize` bound to a data field to achieve bubble chart

### Bubble Chart Configuration Example
```json
{
  "proChartSetting": {
    "series": [{
      "type": "scatter",
      "scatterSetting": {
        "datasetIndex": 0,
        "encode": {
          "x": ["sales"],
          "y": ["profit"],
          "value": ["market_share"]  // Used to control bubble size
        },
        "symbolSize": function(data) {
          return Math.sqrt(data[2]) * 5;  // Calculate bubble size based on market share
        }
      }
    }]
  }
}
```

## Polar Coordinate Supplement

Polar coordinates simply describe position using angle and length. It has a significantly different display effect compared to line charts and bar charts in Cartesian coordinate systems. Polar coordinate systems can generally be used with bar charts, line charts, and scatter charts.

### Polar Coordinate Axis Types

| Setting | Description | Corresponding Field Identifier |
|--------|------|--------------|
| Value Axis | Value axis, suitable for continuous data, representing values through the length of the radius | `radiusAxis.type: 'value'` |
| Category Axis | Category axis, suitable for discrete categorical data, representing each category value through fixed radius lengths | `angleAxis.type: 'category'` |
| Time Axis | Time axis, suitable for continuous time-series data, the radius reflects the sequential change of time points | `radiusAxis.type: 'time'` |
| Log Axis | Logarithmic axis, suitable for logarithmic data, commonly used in line charts for dual value axis presentation | `radiusAxis.type: 'log'` |

## Important Rules

### 1. Data Source Field Matching Rules
- **Field Source**: `x` and `y` fields used in `encode` must exist in the corresponding `dataset`'s `dimensionList`
- **Aggregation Field Naming**: If aggregation query is enabled (`aggregation=true`), the field ID format is `fieldID_functionName`, e.g., `sales_avg`
- **Prohibited Aggregation Fields**: `id` and `seq` fields cannot be used for aggregation
- **Data Type Requirements**: Scatter chart X-axis and Y-axis fields are typically numeric types

### 2. Multi-Data Source Configuration
- Multiple data sources can be referenced in one scatter chart series
- Specify the data source used by each series via `datasetIndex`
- Supports displaying scatter distributions from multiple datasets in the same coordinate system

### 3. Bubble Chart Implementation
- Achieve bubble chart effects by binding `symbolSize` to a data field
- `symbolSize` can be a fixed value, data field reference, or function
- Bubble charts are suitable for displaying three-dimensional data (X, Y, size)

### 4. Style Configuration Rules
- Chart title position must be explicitly set to avoid overlapping with the legend
- `cardStyle.titlePosition` controls the card title position
- `proChartSetting.title.left/top` controls the chart title position
- Scatter colors can be individually set via `itemStyle.color` or uniformly configured via the color palette

## Best Practice Recommendations

### 1. Data Volume Control
- Scatter charts are suitable for displaying **100-1000** data points
- Too many data points will cause severe overlap, affecting readability
- For large data volumes, consider:
    - Using opacity (`opacity`) to avoid complete overlap
    - Enabling data filtering and zoom (`dataZoom`)
    - Displaying after cluster analysis

### 2. Correlation Analysis
- Scatter charts are mainly used to analyze correlation between variables
- Trends can be shown through regression lines
- Use different colors or shapes to distinguish data categories

### 3. Bubble Chart Application
- Bubble charts are suitable for displaying three-dimensional data
- Bubble size should be proportional to data values
- Avoid excessively large differences in bubble size, which affect visualization

### 4. Polar Coordinate Application
- Polar coordinate scatter charts are suitable for displaying periodic data distributions
- The angle axis usually represents time or categories
- The radius axis represents numerical magnitude

### 5. Interaction Optimization
- Enable `tooltip` by default to display detailed information
- Enable data point selection and emphasis effects
- For dense data, you can enable fading of non-selected points

# Radar Chart

A **radar chart** is a chart that displays multi-dimensional data, composed of coordinate axes, points, lines, and polygons.

Radar charts map multi-dimensional data to coordinate axes, where each dimension corresponds to a separate axis. These axes are evenly spaced along the radial direction with the same scale. Connecting the data points on each axis with lines forms a polygon, which ultimately reflects the relative weight of related variables. It is particularly suitable for displaying various performance indicator data.

**Advantages:** Radar charts can intuitively display multi-dimensional datasets, showing which variables have similar values, whether there are outliers among variables. They are suitable for viewing which variables score higher or lower in a dataset, can effectively showcase performance and strengths, and are particularly suitable for displaying multiple key characteristics of a dataset or comparing multiple key characteristics with standard values. They are generally applicable for comparing values across multiple dimensions for multiple data entries.

**Disadvantages:** Radar charts are not suitable for data with too many categories, which would cause excessive deformation and make the overall chart too cluttered. Especially with color-filled polygons, upper layers will cover lower polygons. Additionally, too many variables will also reduce readability.

## Configuration Structure Mapping

The following settings correspond to `_save_dashboard_prochart_card` document's `proChartSetting.series[n].radarSetting` and related configuration fields:

| UI Setting | Corresponding JSON Field Path | Type/Enum Values | Description |
|----------------|-------------------|-------------|------|
| **Data Settings** | | | |
| Data Source | `proChartSetting.dataset[n].id`<br>`proChartSetting.series[n].radarSetting.datasetIndex` | `integer` | Select data source index, must correspond to the `dataset` array index |
| Name Field | `proChartSetting.series[n].radarSetting.encode.seriesName` | `array<string>` | Field name for legend display |
| Value Field | `proChartSetting.series[n].radarSetting.encode.value` | `array<string>` | Must match the `id` in `dataset.dimensionList`, order must correspond to radar indicators |
| **Chart Settings** | | | |
| Radar | `proChartSetting.radar[n].id`<br>`proChartSetting.series[n].radarIndex` | `integer/string` | Reference radar coordinate system configuration |
| Color Assignment Type | `proChartSetting.series[n].colorBy` | `string` | `'data'` or `'series'` |
| Symbol Style | `proChartSetting.series[n].radarSetting.symbol` | `string` | `'circle'`, `'rect'`, `'roundRect'`, `'triangle'`, `'diamond'`, `'pin'`, `'arrow'`, `'none'` |
| Symbol Size | `proChartSetting.series[n].radarSetting.symbolSize` | `number` | Data point symbol size |
| Symbol Rotation Angle | `proChartSetting.series[n].radarSetting.symbolRotate` | `number` | Data point symbol rotation angle |
| **Label Settings** | | | |
| Show Label | `proChartSetting.series[n].radarSetting.label.show` | `boolean` | Whether to show data labels |
| Display Content Expression | `proChartSetting.series[n].radarSetting.label.formatter` | `string` | ECharts format string |
| Position | `proChartSetting.series[n].radarSetting.label.position` | `string` | `'top'`, `'left'`, `'right'`, `'bottom'`, `'inside'`, etc. |
| Distance from Symbol | `proChartSetting.series[n].radarSetting.label.distance` | `number` | Distance between label and data point |
| Label Rotation | `proChartSetting.series[n].radarSetting.label.rotate` | `number` | Label rotation angle |
| Text Offset X | `proChartSetting.series[n].radarSetting.label.offset[0]` | `number` | Horizontal offset |
| Text Offset Y | `proChartSetting.series[n].radarSetting.label.offset[1]` | `number` | Vertical offset |
| Color | `proChartSetting.series[n].radarSetting.label.color` | `string` | Label text color |
| Background Color | `proChartSetting.series[n].radarSetting.label.backgroundColor` | `string` | Label background color |
| Font Weight | `proChartSetting.series[n].radarSetting.label.fontWeight` | `string` | `'normal'`, `'bold'`, `'bolder'`, `'lighter'` |
| Font | `proChartSetting.series[n].radarSetting.label.fontFamily` | `string` | Font family |
| Font Size | `proChartSetting.series[n].radarSetting.label.fontSize` | `number/string` | Font size |
| Horizontal Alignment | `proChartSetting.series[n].radarSetting.label.align` | `string` | `'left'`, `'center'`, `'right'` |
| Vertical Alignment | `proChartSetting.series[n].radarSetting.label.verticalAlign` | `string` | `'top'`, `'middle'`, `'bottom'` |
| Border Width | `proChartSetting.series[n].radarSetting.label.borderWidth` | `number` | Label border width |
| Border Color | `proChartSetting.series[n].radarSetting.label.borderColor` | `string` | Label border color |
| Border Radius | `proChartSetting.series[n].radarSetting.label.borderRadius` | `number` | Label border radius |
| Shadow Color | `proChartSetting.series[n].radarSetting.label.shadowColor` | `string` | Shadow color |
| Shadow Blur | `proChartSetting.series[n].radarSetting.label.shadowBlur` | `number` | Shadow blur size |
| Shadow Offset X | `proChartSetting.series[n].radarSetting.label.shadowOffsetX` | `number` | Shadow horizontal offset |
| Shadow Offset Y | `proChartSetting.series[n].radarSetting.label.shadowOffsetY` | `number` | Shadow vertical offset |
| **Line Style** | | | |
| Color | `proChartSetting.series[n].itemStyle.color` | `string` | Radar chart line color |
| Border Color | `proChartSetting.series[n].itemStyle.borderColor` | `string` | Polygon border color |
| Stroke Type | `proChartSetting.series[n].lineStyle.type` | `string` | `'solid'`, `'dashed'`, `'dotted'` |
| Stroke Width | `proChartSetting.series[n].lineStyle.width` | `number` | Line width |
| Border Radius | `proChartSetting.series[n].itemStyle.borderRadius` | `number` | Data point border radius |
| Shadow Color | `proChartSetting.series[n].itemStyle.shadowColor` | `string` | Shadow color |
| Shadow Blur | `proChartSetting.series[n].itemStyle.shadowBlur` | `number` | Shadow blur size |
| Shadow Offset X | `proChartSetting.series[n].itemStyle.shadowOffsetX` | `number` | Shadow horizontal offset |
| Shadow Offset Y | `proChartSetting.series[n].itemStyle.shadowOffsetY` | `number` | Shadow vertical offset |
| Opacity | `proChartSetting.series[n].itemStyle.opacity` | `number` | Opacity (0-1) |
| **Label Layout** | | | |
| Hide Overlapping Labels | `proChartSetting.series[n].labelLayout.hideOverlap` | `boolean` | Whether to hide overlapping labels |
| Overlap Offset Direction | `proChartSetting.series[n].labelLayout.moveOverlap` | `string` | Move direction when overlapping |
| **Emphasis Settings** | | | |
| Disable Emphasis | `proChartSetting.series[n].emphasis.disabled` | `boolean` | Whether to disable emphasis |
| Emphasis Behavior | `proChartSetting.series[n].emphasis.focus` | `string` | `'self'`, `'series'`, `'none'` |
| Blur Scope | `proChartSetting.series[n].emphasis.blurScope` | `string` | `'coordinateSystem'`, `'series'`, `'global'` |
| **Area Fill** | | | |
| Enable Area Fill | `proChartSetting.series[n].radarSetting.areaStyle` | `object` | Area fill is enabled when not empty |
| Fill Color | `proChartSetting.series[n].radarSetting.areaStyle.color` | `string` | Area fill color |
| Fill Opacity | `proChartSetting.series[n].radarSetting.areaStyle.opacity` | `number` | Fill opacity (0-1) |

## Radar Coordinate System Configuration

The radar coordinate system is configured in `proChartSetting.radar`, supporting multiple radar coordinate systems:

### Radar Configuration Items
| Configuration Item | Corresponding Field | Type/Enum Values | Description |
|--------|---------|-------------|------|
| Radar ID | `id` | `string` | Radar coordinate system unique identifier |
| Name | `name` | `string` | Radar name (for display) |
| Shape | `shape` | `string` | `'polygon'` (polygon) or `'circle'` (circle) |
| Radius | `radius` | `string` | Radar radius (e.g., `'75%'` or `'200'`) |
| Center | `center` | `array<string>` | Radar center position (e.g., `['50%', '50%']`) |
| Start Angle | `startAngle` | `number` | Start angle (degrees) |
| Split Number | `splitNumber` | `number` | Number of radar split segments |
| Indicator Configuration | `indicator` | `array<object>` | Radar chart dimension indicator array |

### Indicator Configuration Example
```json
{
  "proChartSetting": {
    "radar": [{
      "id": "radar1",
      "name": "Capability Assessment",
      "shape": "polygon",
      "radius": "75%",
      "indicator": [
        {"name": "Sales Ability", "max": 100},
        {"name": "Communication Ability", "max": 100},
        {"name": "Technical Ability", "max": 100},
        {"name": "Teamwork", "max": 100},
        {"name": "Innovation Ability", "max": 100}
      ]
    }]
  }
}
```

## Important Rules

### 1. Data Source Field Matching Rules
- **Field Source**: `value` fields used in `encode` must exist in the corresponding `dataset`'s `dimensionList`
- **Field Order**: The order of the `value` field array must exactly match the order of the radar `indicator` array
- **Aggregation Field Naming**: If aggregation query is enabled (`aggregation=true`), the field ID format is `fieldID_functionName`, e.g., `score_avg`
- **Prohibited Aggregation Fields**: `id` and `seq` fields cannot be used for aggregation
- **Data Type Requirements**: Radar chart value fields should be numeric types

### 2. Multi-Radar Configuration
- Multiple radar coordinate systems can be configured in one card
- Each radar chart series references the corresponding radar coordinate system via `radarIndex`
- Supports displaying multiple data series performance on different radar coordinate systems in the same chart

### 3. Indicator Configuration Requirements
- The `indicator` array must contain the `name` field
- It is recommended to set a `max` value for each indicator to standardize the data range
- A `min` value can be set to define the minimum value range
- The number of indicators is recommended to be **3-8**; too many will affect readability

### 4. Style Configuration Rules
- Chart title position must be explicitly set to avoid overlapping with the legend
- `cardStyle.titlePosition` controls the card title position
- `proChartSetting.title.left/top` controls the chart title position
- Radar chart colors can be individually set via `itemStyle.color` or uniformly configured via the color palette

## Best Practice Recommendations

### 1. Data Volume Control
- Radar charts are suitable for comparing **2-5** data series
- Each series should have **3-8** indicator dimensions
- Too many data series will cause severe overlap, affecting readability

### 2. Indicator Standardization
- All indicators should use the same unit of measurement or be standardized to the same range
- Unify the data upper limit by setting `indicator.max`
- For data with different dimensions, standardization processing is recommended first

### 3. Shape Selection
- **Polygon Radar Chart**: More suitable for displaying categorical data comparisons
- **Circular Radar Chart**: More suitable for displaying continuous data distributions
- Polygon radar charts have better visual effects when there are fewer indicators

### 4. Color and Transparency
- Use different colors to distinguish different data series
- When area fill is enabled, set appropriate transparency to avoid occlusion
- Recommended transparency setting between **0.3-0.6**

### 5. Interaction Optimization
- Enable `tooltip` by default to display detailed indicator values
- Enable data series emphasis and fade effects
- For complex radar charts, animation effects can be enabled to enhance the experience

# Box Plot (Box-and-Whisker Chart)

A **box plot**, also called a box-and-whisker chart, is a chart that displays the data distribution of continuous variables. Box plots can show the center and spread of data, and serve as an intuitive tool for checking normality or identifying potential outlier points, used to reflect the characteristics of raw data distribution and identify data anomalies.

Box plots are suitable for comparing the distribution characteristics of multiple data groups, commonly used in numerical statistics, providing key information about data position and dispersion. They are especially useful when comparing different populations of data. When using box plots, please check if the data has extreme values. If the dataset is small, use with caution; if there are categorical or nominal variables, use charts like bar charts instead.

**Advantages:** Not affected by outliers, can describe the discrete distribution of data in a relatively stable manner.

**Disadvantages:** Cannot precisely measure the skewness and tail weight of data distribution, and for large batches of data, the information it reflects becomes more ambiguous.

## Key Data Points

- **Minimum**: The smallest value in the data
- **Lower Quartile (Q1)**: The median of data below the overall median
- **Median (Q2)**: The center point of the data
- **Upper Quartile (Q3)**: The median of data above the overall median
- **Maximum**: The largest value in the data

## Configuration Structure Mapping

The following settings correspond to `_save_dashboard_prochart_card` document's `proChartSetting.series[n].boxplotSetting` and related configuration fields:

| UI Setting | Corresponding JSON Field Path | Type/Enum Values | Description |
|----------------|-------------------|-------------|------|
| **Data Settings** | | | |
| Data Source | `proChartSetting.dataset[n].id`<br>`proChartSetting.series[n].boxplotSetting.datasetIndex` | `integer` | Select data source index, must correspond to the `dataset` array index |
| Name Field | `proChartSetting.series[n].boxplotSetting.encode.seriesName` | `array<string>` | Field name for legend display |
| X-Axis Field | `proChartSetting.series[n].boxplotSetting.encode.x` | `array<string>` | Must match the `id` in `dataset.dimensionList` |
| Y-Axis Field | `proChartSetting.series[n].boxplotSetting.encode.y` | `array<string>` | Must be 5 fields, in order of `[min, q1, median, q3, max]` |
| **Chart Settings** | | | |
| X-Axis | `proChartSetting.xAxis` | `array<object>` | Supports multiple X-axis configurations |
| Y-Axis | `proChartSetting.yAxis` | `array<object>` | Supports multiple Y-axis configurations |
| Color Assignment Type | `proChartSetting.series[n].colorBy` | `string` | `'data'` or `'series'` |
| Layout | `proChartSetting.series[n].boxplotSetting.layout` | `string` | `'horizontal'`, `'vertical'` |
| Box Width Lower Limit | `proChartSetting.series[n].boxplotSetting.boxWidth[0]` | `number` | Minimum box width |
| Box Width Upper Limit | `proChartSetting.series[n].boxplotSetting.boxWidth[1]` | `number` | Maximum box width |
| **Label Settings** | | | |
| Show Label | `proChartSetting.series[n].boxplotSetting.label.show` | `boolean` | Whether to show data labels |
| Display Content Expression | `proChartSetting.series[n].boxplotSetting.label.formatter` | `string` | ECharts format string |
| Position | `proChartSetting.series[n].boxplotSetting.label.position` | `string` | `'top'`, `'left'`, `'right'`, `'bottom'`, `'inside'`, etc. |
| Distance from Symbol | `proChartSetting.series[n].boxplotSetting.label.distance` | `number` | Distance between label and box |
| Label Rotation | `proChartSetting.series[n].boxplotSetting.label.rotate` | `number` | Label rotation angle |
| Text Offset X | `proChartSetting.series[n].boxplotSetting.label.offset[0]` | `number` | Horizontal offset |
| Text Offset Y | `proChartSetting.series[n].boxplotSetting.label.offset[1]` | `number` | Vertical offset |
| Color | `proChartSetting.series[n].boxplotSetting.label.color` | `string` | Label text color |
| Background Color | `proChartSetting.series[n].boxplotSetting.label.backgroundColor` | `string` | Label background color |
| Font Weight | `proChartSetting.series[n].boxplotSetting.label.fontWeight` | `string` | `'normal'`, `'bold'`, `'bolder'`, `'lighter'` |
| Font | `proChartSetting.series[n].boxplotSetting.label.fontFamily` | `string` | Font family |
| Font Size | `proChartSetting.series[n].boxplotSetting.label.fontSize` | `number/string` | Font size |
| Horizontal Alignment | `proChartSetting.series[n].boxplotSetting.label.align` | `string` | `'left'`, `'center'`, `'right'` |
| Vertical Alignment | `proChartSetting.series[n].boxplotSetting.label.verticalAlign` | `string` | `'top'`, `'middle'`, `'bottom'` |
| Border Width | `proChartSetting.series[n].boxplotSetting.label.borderWidth` | `number` | Label border width |
| Border Color | `proChartSetting.series[n].boxplotSetting.label.borderColor` | `string` | Label border color |
| Border Radius | `proChartSetting.series[n].boxplotSetting.label.borderRadius` | `number` | Label border radius |
| Shadow Color | `proChartSetting.series[n].boxplotSetting.label.shadowColor` | `string` | Shadow color |
| Shadow Blur | `proChartSetting.series[n].boxplotSetting.label.shadowBlur` | `number` | Shadow blur size |
| Shadow Offset X | `proChartSetting.series[n].boxplotSetting.label.shadowOffsetX` | `number` | Shadow horizontal offset |
| Shadow Offset Y | `proChartSetting.series[n].boxplotSetting.label.shadowOffsetY` | `number` | Shadow vertical offset |
| **Box Style** | | | |
| Color | `proChartSetting.series[n].itemStyle.color` | `string` | Box color |
| Border Color | `proChartSetting.series[n].itemStyle.borderColor` | `string` | Box border color |
| Stroke Type | `proChartSetting.series[n].itemStyle.borderType` | `string` | `'solid'`, `'dashed'`, `'dotted'` |
| Stroke Width | `proChartSetting.series[n].itemStyle.borderWidth` | `number` | Box border width |
| Stroke Color | `proChartSetting.series[n].itemStyle.borderColor` | `string` | Box stroke color |
| Border Radius | `proChartSetting.series[n].itemStyle.borderRadius` | `number` | Box border radius |
| Shadow Color | `proChartSetting.series[n].itemStyle.shadowColor` | `string` | Box shadow color |
| Shadow Blur | `proChartSetting.series[n].itemStyle.shadowBlur` | `number` | Box shadow blur size |
| Shadow Offset X | `proChartSetting.series[n].itemStyle.shadowOffsetX` | `number` | Box shadow horizontal offset |
| Shadow Offset Y | `proChartSetting.series[n].itemStyle.shadowOffsetY` | `number` | Box shadow vertical offset |
| Opacity | `proChartSetting.series[n].itemStyle.opacity` | `number` | Box opacity (0-1) |
| **Label Layout** | | | |
| Hide Overlapping Labels | `proChartSetting.series[n].labelLayout.hideOverlap` | `boolean` | Whether to hide overlapping labels |
| Overlap Offset Direction | `proChartSetting.series[n].labelLayout.moveOverlap` | `string` | Move direction when overlapping |
| **Emphasis Settings** | | | |
| Disable Emphasis | `proChartSetting.series[n].emphasis.disabled` | `boolean` | Whether to disable emphasis |
| Emphasis Behavior | `proChartSetting.series[n].emphasis.focus` | `string` | `'self'`, `'series'`, `'none'` |
| Blur Scope | `proChartSetting.series[n].emphasis.blurScope` | `string` | `'coordinateSystem'`, `'series'`, `'global'` |
| **Outlier Style** | | | |
| Outlier Color | `proChartSetting.series[n].boxplotSetting.itemStyle.outlierColor` | `string` | Outlier point color |
| Outlier Size | `proChartSetting.series[n].boxplotSetting.itemStyle.outlierSize` | `number` | Outlier point size |
| Outlier Shape | `proChartSetting.series[n].boxplotSetting.itemStyle.outlierSymbol` | `string` | Outlier point shape |

## Event Configuration
| Setting | Description | Corresponding Field Identifier |
|--------|------|--------------|
| Non-clickable | When enabled, all label data in the chart cannot be clicked. When disabled, corresponding data click interaction events can be set | `silent` |
| Click to Trigger Automation | Select the corresponding automation to implement data label click interaction events, such as opening the corresponding data form details or other web links after clicking | `eventHandlers.click` |
| Double-click to Trigger Automation | Same function as click trigger, but interaction changes from single click to double click. Click and double-click events can be set simultaneously | `eventHandlers.dblclick` |

## Important Rules

### 1. Data Source Field Matching Rules
- **Field Source**: `x` and `y` fields used in `encode` must exist in the corresponding `dataset`'s `dimensionList`
- **Field Order**: The `y` field array must contain **5 fields**, in order of `[min, q1, median, q3, max]`
- **Aggregation Field Naming**: If aggregation query is enabled (`aggregation=true`), the field ID format is `fieldID_functionName`, e.g., `score_avg`
- **Prohibited Aggregation Fields**: `id` and `seq` fields cannot be used for aggregation
- **Data Type Requirements**: All value fields must be numeric types

### 2. Data Preprocessing Requirements
- The data source needs to pre-calculate five key statistics: minimum, Q1, median, Q3, maximum
- These statistics can be calculated through SQL queries or application programs
- The data format must comply with the five-number summary requirements of box plots

### 3. Layout and Direction Configuration
- Control the arrangement direction of box plots via the `layout` parameter
- `'horizontal'`: Horizontal arrangement, X-axis for categories, Y-axis for values
- `'vertical'`: Vertical arrangement, Y-axis for categories, X-axis for values
- `boxWidth` controls the width range of boxes to avoid overlap

### 4. Outlier Handling
- Box plots can automatically identify and display outliers
- Outliers are typically defined as data points less than Q1-1.5*IQR or greater than Q3+1.5*IQR
- Outlier styles can be configured via `itemStyle.outlier*`

### 5. Style Configuration Rules
- Chart title position must be explicitly set to avoid overlapping with the legend
- `cardStyle.titlePosition` controls the card title position
- `proChartSetting.title.left/top` controls the chart title position
- Box colors can be individually set via `itemStyle.color` or uniformly configured via the color palette

## Best Practice Recommendations

### 1. Data Volume Control
- Box plots are suitable for displaying **3-10** groups of data distributions
- Each group should have sufficient data points (recommended > 20) to ensure reliable statistics
- Too many groups will cause boxes to be too narrow, affecting readability

### 2. Outlier Analysis
- One of the main purposes of using box plots is to identify outliers
- Outliers need to be analyzed in the context of business background; they are not necessarily erroneous data
- Different colors and shapes can be configured to highlight outliers

### 3. Data Preprocessing
- Ensure data has been aggregated to calculate five key statistics by group
- For large datasets, aggregation calculation at the database level is recommended
- Data grouping can be done via `groupByFieldList`

### 4. Comparative Analysis
- Box plots are most suitable for comparing distributions of multiple data groups
- Visually compare distribution characteristics of different groups through side-by-side box plots
- Observe median position, box length, outlier distribution, etc.

### 5. Interaction Optimization
- Enable `tooltip` by default to display specific values of five key statistics
- Click interactions can be configured to view detailed data
- For multiple data groups, emphasis and fade effects can be enabled

## Configuration Example

### Basic Box Plot Configuration
```json
{
  "proChartSetting": {
    "dataset": [{
      "id": "performance_data",
      "name": "Performance Data",
      "type": "table",
      "tableId": "employee_performance",
      "dimensionList": [
        {"id": "department", "name": "Department"},
        {"id": "min_score", "name": "Minimum Score"},
        {"id": "q1_score", "name": "Lower Quartile"},
        {"id": "median_score", "name": "Median"},
        {"id": "q3_score", "name": "Upper Quartile"},
        {"id": "max_score", "name": "Maximum Score"}
      ]
    }],
    "series": [{
      "name": "Department Performance Distribution",
      "type": "boxplot",
      "boxplotSetting": {
        "datasetIndex": 0,
        "encode": {
          "x": ["department"],
          "y": ["min_score", "q1_score", "median_score", "q3_score", "max_score"]
        },
        "layout": "vertical",
        "boxWidth": [10, 30],
        "itemStyle": {
          "color": "#c23531",
          "borderColor": "#c23531",
          "borderWidth": 2
        }
      }
    }],
    "tooltip": {
      "trigger": "item",
      "formatter": function(params) {
        return `Department: ${params.name}<br/>
                Minimum: ${params.data[0]}<br/>
                Q1: ${params.data[1]}<br/>
                Median: ${params.data[2]}<br/>
                Q3: ${params.data[3]}<br/>
                Maximum: ${params.data[4]}`;
      }
    }
  }
}
```

# Candlestick Chart (K-Line Chart)

A **candlestick chart**, also called a K-line chart, represents the price changes of financial products such as stocks and futures, including open price, close price, high price, and low price in graphical form.

The thin line at the top of the candlestick is called the upper shadow, the thick line in the middle is the body, and the thin line at the bottom is the lower shadow. When the close price is higher than the open price, meaning the stock price trend is upward, we call this a bullish candle, and the middle body is shown as hollow or red. In this case, the length of the upper shadow represents the price difference between the high and close price, the length of the body represents the price difference between the close and open price, and the length of the lower shadow represents the difference between the open and low price.

**Advantages:** Candlestick charts can show both data change trends and data volatility patterns, making them ideal for displaying time-series price changes.

**Disadvantages:** The drawing method of candlestick charts is relatively complex, with many variations of bullish and bearish candles, requiring users to have a certain understanding of financial charts.

## Key Data Points

- **Open**: The price at the beginning of the trading day
- **Close**: The price at the end of the trading day
- **High**: The highest price during the trading day
- **Low**: The lowest price during the trading day

## Configuration Structure Mapping

The following settings correspond to `_save_dashboard_prochart_card` document's `proChartSetting.series[n].candlestickSetting` and related configuration fields:

| UI Setting | Corresponding JSON Field Path | Type/Enum Values | Description |
|----------------|-------------------|-------------|------|
| **Data Settings** | | | |
| Data Source | `proChartSetting.dataset[n].id`<br>`proChartSetting.series[n].candlestickSetting.datasetIndex` | `integer` | Select data source index, must correspond to the `dataset` array index |
| Name Field | `proChartSetting.series[n].candlestickSetting.encode.seriesName` | `array<string>` | Field name for legend display |
| X-Axis Field | `proChartSetting.series[n].candlestickSetting.encode.x` | `array<string>` | Usually a time field, must match the `id` in `dataset.dimensionList` |
| Y-Axis Field | `proChartSetting.series[n].candlestickSetting.encode.y` | `array<string>` | Must be 4 fields, in order of `[open, close, high, low]` |
| **Chart Settings** | | | |
| X-Axis | `proChartSetting.xAxis` | `array<object>` | Supports multiple X-axis configurations, usually time axis |
| Y-Axis | `proChartSetting.yAxis` | `array<object>` | Supports multiple Y-axis configurations, usually value axis |
| Color Assignment Type | `proChartSetting.series[n].colorBy` | `string` | `'data'` or `'series'` |
| Layout | `proChartSetting.series[n].candlestickSetting.layout` | `string` | `'horizontal'`, `'vertical'` |
| Bar Width | `proChartSetting.series[n].candlestickSetting.barWidth` | `number/string` | Default width of K-line bars |
| Maximum Bar Width | `proChartSetting.series[n].candlestickSetting.barMaxWidth` | `number/string` | Maximum width of K-line bars |
| Minimum Bar Width | `proChartSetting.series[n].candlestickSetting.barMinWidth` | `number/string` | Minimum width of K-line bars |
| **Label Settings** | | | |
| Show Label | `proChartSetting.series[n].candlestickSetting.label.show` | `boolean` | Whether to show data labels |
| Display Content Expression | `proChartSetting.series[n].candlestickSetting.label.formatter` | `string` | ECharts format string |
| Position | `proChartSetting.series[n].candlestickSetting.label.position` | `string` | `'top'`, `'left'`, `'right'`, `'bottom'`, `'inside'`, etc. |
| Distance from Symbol | `proChartSetting.series[n].candlestickSetting.label.distance` | `number` | Distance between label and K-line bar |
| Label Rotation | `proChartSetting.series[n].candlestickSetting.label.rotate` | `number` | Label rotation angle |
| Text Offset X | `proChartSetting.series[n].candlestickSetting.label.offset[0]` | `number` | Horizontal offset |
| Text Offset Y | `proChartSetting.series[n].candlestickSetting.label.offset[1]` | `number` | Vertical offset |
| Color | `proChartSetting.series[n].candlestickSetting.label.color` | `string` | Label text color |
| Background Color | `proChartSetting.series[n].candlestickSetting.label.backgroundColor` | `string` | Label background color |
| Font Weight | `proChartSetting.series[n].candlestickSetting.label.fontWeight` | `string` | `'normal'`, `'bold'`, `'bolder'`, `'lighter'` |
| Font | `proChartSetting.series[n].candlestickSetting.label.fontFamily` | `string` | Font family |
| Font Size | `proChartSetting.series[n].candlestickSetting.label.fontSize` | `number/string` | Font size |
| Horizontal Alignment | `proChartSetting.series[n].candlestickSetting.label.align` | `string` | `'left'`, `'center'`, `'right'` |
| Vertical Alignment | `proChartSetting.series[n].candlestickSetting.label.verticalAlign` | `string` | `'top'`, `'middle'`, `'bottom'` |
| Border Width | `proChartSetting.series[n].candlestickSetting.label.borderWidth` | `number` | Label border width |
| Border Color | `proChartSetting.series[n].candlestickSetting.label.borderColor` | `string` | Label border color |
| Border Radius | `proChartSetting.series[n].candlestickSetting.label.borderRadius` | `number` | Label border radius |
| Shadow Color | `proChartSetting.series[n].candlestickSetting.label.shadowColor` | `string` | Shadow color |
| Shadow Blur | `proChartSetting.series[n].candlestickSetting.label.shadowBlur` | `number` | Shadow blur size |
| Shadow Offset X | `proChartSetting.series[n].candlestickSetting.label.shadowOffsetX` | `number` | Shadow horizontal offset |
| Shadow Offset Y | `proChartSetting.series[n].candlestickSetting.label.shadowOffsetY` | `number` | Shadow vertical offset |
| **K-Line Style** | | | |
| Color | `proChartSetting.series[n].itemStyle.color` | `string` | K-line bar color (bullish) |
| Border Color | `proChartSetting.series[n].itemStyle.borderColor` | `string` | K-line bar border color |
| Stroke Type | `proChartSetting.series[n].itemStyle.borderType` | `string` | `'solid'`, `'dashed'`, `'dotted'` |
| Stroke Width | `proChartSetting.series[n].itemStyle.borderWidth` | `number` | K-line bar border width |
| Stroke Color | `proChartSetting.series[n].itemStyle.borderColor0` | `string` | K-line bar stroke color (bearish border) |
| Border Radius | `proChartSetting.series[n].itemStyle.borderRadius` | `number` | K-line bar border radius |
| Shadow Color | `proChartSetting.series[n].itemStyle.shadowColor` | `string` | K-line bar shadow color |
| Shadow Blur | `proChartSetting.series[n].itemStyle.shadowBlur` | `number` | K-line bar shadow blur size |
| Shadow Offset X | `proChartSetting.series[n].itemStyle.shadowOffsetX` | `number` | K-line bar shadow horizontal offset |
| Shadow Offset Y | `proChartSetting.series[n].itemStyle.shadowOffsetY` | `number` | K-line bar shadow vertical offset |
| Opacity | `proChartSetting.series[n].itemStyle.opacity` | `number` | K-line bar opacity (0-1) |
| **Label Layout** | | | |
| Hide Overlapping Labels | `proChartSetting.series[n].labelLayout.hideOverlap` | `boolean` | Whether to hide overlapping labels |
| Overlap Offset Direction | `proChartSetting.series[n].labelLayout.moveOverlap` | `string` | Move direction when overlapping |
| **Emphasis Settings** | | | |
| Disable Emphasis | `proChartSetting.series[n].emphasis.disabled` | `boolean` | Whether to disable emphasis |
| Emphasis Behavior | `proChartSetting.series[n].emphasis.focus` | `string` | `'self'`, `'series'`, `'none'` |
| Blur Scope | `proChartSetting.series[n].emphasis.blurScope` | `string` | `'coordinateSystem'`, `'series'`, `'global'` |
| **Bullish/Bearish Colors** | | | |
| Bullish Color | `proChartSetting.series[n].itemStyle.color` | `string` | K-line color when close > open |
| Bearish Color | `proChartSetting.series[n].itemStyle.color0` | `string` | K-line color when close < open |
| Bullish Border Color | `proChartSetting.series[n].itemStyle.borderColor` | `string` | Bullish candle border color |
| Bearish Border Color | `proChartSetting.series[n].itemStyle.borderColor0` | `string` | Bearish candle border color |

## Event Configuration
| Setting | Description | Corresponding Field Identifier |
|--------|------|--------------|
| Non-clickable | When enabled, all label data in the chart cannot be clicked. When disabled, corresponding data click interaction events can be set | `silent` |
| Click to Trigger Automation | Select the corresponding automation to implement data label click interaction events, such as opening the corresponding data form details or other web links after clicking | `eventHandlers.click` |
| Double-click to Trigger Automation | Same function as click trigger, but interaction changes from single click to double click. Click and double-click events can be set simultaneously | `eventHandlers.dblclick` |

## Important Rules

### 1. Data Source Field Matching Rules
- **Field Source**: `x` and `y` fields used in `encode` must exist in the corresponding `dataset`'s `dimensionList`
- **Field Order**: The `y` field array must contain **4 fields**, in order of `[open, close, high, low]`
- **Aggregation Field Naming**: If aggregation query is enabled (`aggregation=true`), the field ID format is `fieldID_functionName`, e.g., `price_avg`
- **Prohibited Aggregation Fields**: `id` and `seq` fields cannot be used for aggregation
- **Data Type Requirements**: All price fields must be numeric types, and time fields should be date/time types

### 2. Bullish/Bearish Color Rules
- **Bullish (Rising)**: When `close > open`, uses `itemStyle.color` and `itemStyle.borderColor`
- **Bearish (Falling)**: When `close < open`, uses `itemStyle.color0` and `itemStyle.borderColor0`
- **Flat**: When `close = open`, usually treated as bullish or uses a special color

### 3. Time Series Requirements
- Candlestick charts are typically used to display time-series data
- The X-axis should be a time axis type: `xAxis.type: 'time'`
- Data should be sorted in chronological order, which can be ensured via `orderByList`
- Supports daily, weekly, monthly, and other time period data

### 4. Style Configuration Rules
- Chart title position must be explicitly set to avoid overlapping with the legend
- `cardStyle.titlePosition` controls the card title position
- `proChartSetting.title.left/top` controls the chart title position
- Bullish/bearish colors should use contrasting colors, such as red/green or red/blue

### 5. Data Completeness Requirements
- Each data point must contain all four complete price fields
- Missing data may cause abnormal candlestick display
- It is recommended to use data filtering to exclude incomplete data records

## Best Practice Recommendations

### 1. Data Volume Control
- Candlestick charts are suitable for displaying **50-200** periods of data
- Too many data points will make candlesticks too dense, affecting readability
- Too few data points make it difficult to observe trends and patterns
- The `dataZoom` component can be used for data range zoom

### 2. Time Period Selection
- **Daily K-line**: Displays daily price changes, suitable for short-term analysis
- **Weekly K-line**: Displays weekly price changes, suitable for medium-term analysis
- **Monthly K-line**: Displays monthly price changes, suitable for long-term analysis
- Choose the appropriate time period based on analysis requirements

### 3. Color Configuration
- Use traditional financial chart colors: red for rising/green for falling or red for rising/blue for falling
- Ensure distinct contrast between bullish and bearish colors
- Consider using hollow/solid to distinguish bullish and bearish candles
- Bullish candles typically use red or hollow, bearish candles use green or solid

### 4. Technical Indicator Overlay
- Candlestick charts are commonly used with other technical indicators
- Moving averages (MA) can be overlaid to show trends
- Volume bar charts can be overlaid to analyze price-volume relationships
- Comprehensive analysis through multi-chart combinations

### 5. Interaction Optimization
- Enable `tooltip` by default to display detailed values of four prices
- Enable data zoom (`dataZoom`) to view different time periods
- Crosshair (`axisPointer`) can be configured for precise viewing
- For high-frequency data, animation effects can be enabled to enhance the experience

## Configuration Example

### Basic Candlestick Chart Configuration
```json
{
  "proChartSetting": {
    "dataset": [{
      "id": "stock_data",
      "name": "Stock Data",
      "type": "table",
      "tableId": "stock_prices",
      "dimensionList": [
        {"id": "date", "name": "Date"},
        {"id": "open", "name": "Open"},
        {"id": "close", "name": "Close"},
        {"id": "high", "name": "High"},
        {"id": "low", "name": "Low"},
        {"id": "volume", "name": "Volume"}
      ],
      "orderByList": [
        {"field": "date", "type": "asc"}
      ]
    }],
    "xAxis": [{
      "type": "time",
      "scale": true,
      "boundaryGap": false
    }],
    "yAxis": [{
      "type": "value",
      "scale": true,
      "splitLine": {
        "show": true
      }
    }],
    "series": [{
      "name": "Stock K-Line",
      "type": "candlestick",
      "candlestickSetting": {
        "datasetIndex": 0,
        "encode": {
          "x": ["date"],
          "y": ["open", "close", "high", "low"]
        },
        "barWidth": 10,
        "itemStyle": {
          "color": "#c23531",      // Bullish color
          "color0": "#314656",     // Bearish color
          "borderColor": "#c23531", // Bullish border
          "borderColor0": "#314656" // Bearish border
        }
      }
    }],
    "tooltip": {
      "trigger": "axis",
      "axisPointer": {
        "type": "cross"
      },
      "formatter": function(params) {
        var data = params[0].data;
        return `Date: ${data[0]}<br/>
                Open: ${data[1]}<br/>
                Close: ${data[2]}<br/>
                High: ${data[3]}<br/>
                Low: ${data[4]}`;
      }
    },
    "dataZoom": [{
      "type": "inside",
      "xAxisIndex": 0,
      "start": 70,
      "end": 100
    }, {
      "type": "slider",
      "xAxisIndex": 0,
      "start": 70,
      "end": 100
    }]
  }
}
```

# _save_dashboard_prochart_card Documentation
```json
{
  "type": "function",
  "function": {
    "name": "_save_dashboard_prochart_card",
    "description": "Create a ProChart card in the dashboard, or edit an existing card. Can only create or modify cards of type ProChart. Special notes: 1. Data source rules: When type=\"table\", the field id in dimensionList must be the actual column name in the SQL query result. Fabricating or using non-existent field names is strictly prohibited. 1.1 If aggregation query is not enabled, the field source is the original fields returned from directly querying the data table, naming rule: id must exactly match the column name in the database table. 1.2 If aggregation query is enabled, the aggregation column format is fieldName_functionName, and aggregation on id and seq fields is prohibited, meaning aggregationQueryList fieldId cannot be id or seq, other fields must be used; When type=\"expression\", static variables must be wrapped in single quotes and placed inside, format like {'key':'A'}, non-existent non-static variables must not be fabricated here, available non-static variables are: filterRecord and filterFieldList, provided that the card definition or dashboard definition has filtering enabled. 2. Stacked chart rules: When implementing stacking effect, you must create a separate data source and a corresponding chart instance for each stacking series. In the chart list series, each item's datasetIndex corresponds to the data source index, and each chart's datasetIndex value should correspond one-to-one with the data source subscript. Example: To display 'quantity of each check-in type per employee' using a bar chart, you need to create independent data sources and charts for 'Check-in Type A', 'Check-in Type B', etc. Check-in Type A data source has index 0 in dataset, Check-in Type B has index 1, so the chart datasetIndex needs to be set to 0 and 1 respectively. Before each card creation or modification, you need to plan which data sources and charts are needed to set the correct datasetIndex. 3. Style rules: The chart title position must be set to ensure it does not overlap with the legend area.",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Card ID. Not required when creating, required when editing."
        },
        "name": {
          "type": "string",
          "description": "Card name"
        },
        "type": {
          "type": "string",
          "description": "Card type (currently only supports 'ProChart').",
          "enum": ["ProChart"]
        },
        "scope": {
          "type": "string",
          "description": "Dashboard ID that the card belongs to."
        },
        "width": {
          "type": "number",
          "description": "Card width, maximum is 24 representing 24 grid units, cannot be less than 12.",
          "default": 12
        },
        "height": {
          "type": "number",
          "description": "Card height, also represented by grid units, no maximum limit of 24. Minimum is 12.",
          "default": 12
        },
        "remark": {
          "type": ["string", "null"],
          "description": "Card remark."
        },
        "isInTab": {
          "type": "boolean",
          "description": "Whether to display within a Tab."
        },
        "cardStyle": {
          "type": "object",
          "description": "Card style, controlling background, padding, border, title position, etc.",
          "properties": {
            "bgType": { "type": "string", "description": "Background type, e.g., 'image', 'color', or 'transparent', default is image." },
            "bgColor": { "type": ["string", "null"], "description": "Background color (CSS color value), only effective when bgType is appropriate." },
            "bgImageId": { "type": ["string", "null"], "description": "Background image ID (if using image)." },
            "padding": { "type": "number", "description": "Padding on all sides (pixels)." },
            "paddingTop": { "type": "number", "description": "Top padding" },
            "paddingRight": { "type": "number", "description": "Right padding" },
            "paddingBottom": { "type": "number", "description": "Bottom padding" },
            "paddingLeft": { "type": "number", "description": "Left padding" },
            "overflow": { "type": "string", "description": "Overflow strategy, e.g., 'auto', 'hidden', 'visible'." },
            "borderWidth": { "type": "number", "description": "Border width" },
            "borderRadius": { "type": "number", "description": "Border radius" },
            "titleFontSize": { "type": "string", "description": "Title font size (CSS string, e.g., '13px')." },
            "titlePosition": { "type": "string", "description": "Title position, e.g., 'left', 'center', 'right'." },
            "subTitleFontSize": { "type": "string", "description": "Subtitle font size (e.g., '12px')." },
            "subTitlePosition": { "type": "string", "description": "Subtitle position, e.g., 'titleBottom'." },
            "enableBorderImage": { "type": "boolean", "description": "Whether to enable border image. Only use borderImage* fields when true." },
            "borderImageId": { "type": ["string", "null"], "description": "Border image ID (optional)." },
            "borderImageIsFill": { "type": "boolean", "description": "Whether the border image fills the content area." },
            "borderImageSlice": { "type": "array", "items": { "type": "number" }, "description": "Border image slice settings (per CSS border-image-slice)." },
            "borderImageRepeatX": { "type": "string", "description": "Border image horizontal repeat strategy, e.g., 'round', 'repeat', 'stretch'." },
            "borderImageRepeatY": { "type": "string", "description": "Border image vertical repeat strategy." }
          }
        },
        "buttonList": {
          "type": "array",
          "items": { "type": "object" },
          "description": "Card top or toolbar button configuration array. Button objects should contain id, label, action, and other fields."
        },
        "buttonStyle": {
          "type": "object",
          "description": "Top button style and layout configuration.",
          "properties": {
            "size": { "type": "string", "description": "Button size, e.g., 'small', 'medium', 'large'." },
            "orient": { "type": "string", "description": "Arrangement direction, e.g., 'horizontal' or 'vertical'." },
            "vertical": { "type": "string", "description": "Vertical alignment, e.g., 'top', 'middle', 'bottom'." },
            "horizontal": { "type": "string", "description": "Horizontal alignment, e.g., 'left', 'center', 'right'." }
          }
        },
        "refreshTime": {
          "type": "integer",
          "description": "Auto-refresh interval (seconds). 0 or unset means no auto-refresh."
        },
        "enableButton": {
          "type": "boolean",
          "description": "Whether to enable buttons"
        },
        "enableRefresh": {
          "type": "boolean",
          "description": "Whether to enable auto-refresh"
        },
        "disableToolbar": {
          "type": "boolean",
          "description": "Whether to disable the card toolbar"
        },
        "enableCardStyle": {
          "type": "boolean",
          "description": "Whether to apply styles from cardStyle"
        },
        "filterFieldList": {
          "type": "array",
          "items": { "type": "object" },
          "description": "Card-level filter field configuration array. Each item should contain fieldId, label, type, etc."
        },
        "proChartSetting": {
          "type": "object",
          "description": "Chart rendering configuration. Structure is compatible with ECharts option.",
          "properties": {
            "grid": {
              "type": "array",
              "items": { "type": "object" },
              "description": "Grid configuration array (refer to ECharts grid)."
            },
            "polar": {
              "type": "array",
              "items": { "type": "object" },
              "description": "Polar coordinate system configuration array (refer to ECharts polar)."
            },
            "radar": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "id": { "type": "string", "description": "Radar configuration unique id (optional)." },
                  "name": { "type": "string", "description": "Radar name (for display, optional)." },
                  "shape": { "type": "string", "enum": ["polygon", "circle"], "description": "Radar shape. 'polygon' or 'circle'." },
                  "radius": { "type": "string", "description": "Radar radius (e.g., '75%' or '200')." },
                  "indicator": {
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "name": { "type": "string", "description": "Indicator name." },
                        "max": { "type": "number", "description": "Maximum allowed value for this indicator (numeric)." },
                        "min": { "type": "number", "description": "Minimum allowed value for this indicator (numeric)." },
                        "color": { "type": ["string", "null"], "description": "Indicator text color (optional)." }
                      },
                      "required": ["name"]
                    },
                    "description": "Radar chart dimension indicator array (must contain name, max recommended)."
                  },
                  "axisLine": { "type": "object", "description": "Axis line style configuration (refer to ECharts axisLine)." },
                  "axisLabel": { "type": "object", "description": "Axis label style configuration." },
                  "splitLine": { "type": "object", "description": "Split line style configuration." },
                  "axisName": { "type": "object", "description": "Axis name style configuration (text style, etc.)." }
                },
                "required": ["indicator"]
              },
              "description": "Radar configuration list."
            },
            "xAxis": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "id": { "type": "string", "description": "xAxis id (optional)." },
                  "name": { "type": "string", "description": "Axis name (display)." },
                  "show": { "type": "boolean", "description": "Whether to show this axis." },
                  "type": { "type": "string", "description": "Axis type, e.g., 'category', 'value', 'time', or 'log'." },
                  "position": { "type": "string", "description": "Axis position, e.g., 'bottom', 'top'." },
                  "axisLine": { "type": "object", "description": "Axis line style configuration." },
                  "axisTick": { "type": "object", "description": "Tick mark configuration." },
                  "axisLabel": { "type": "object", "description": "Tick label configuration, including rotate, formatter, etc." },
                  "splitLine": { "type": "object", "description": "Split line configuration." },
                  "boundaryGap": { "type": ["array", "boolean"], "description": "boundaryGap configuration, category type usually uses ['0','0'] or true/false." }
                },
                "required": ["type"]
              },
              "description": "X-axis configuration array (supports multiple X-axes)."
            },
            "yAxis": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "id": { "type": "string", "description": "yAxis id (optional)." },
                  "name": { "type": "string", "description": "Axis name (display)." },
                  "show": { "type": "boolean", "description": "Whether to show this axis." },
                  "type": { "type": "string", "description": "Axis type, e.g., 'value', 'category', 'time', etc." },
                  "position": { "type": "string", "description": "Axis position, e.g., 'left', 'right'." },
                  "axisLine": { "type": "object", "description": "Axis line style configuration." },
                  "axisTick": { "type": "object", "description": "Tick mark configuration." },
                  "axisLabel": { "type": "object", "description": "Tick label configuration." },
                  "splitLine": { "type": "object", "description": "Split line configuration." },
                  "boundaryGap": { "type": ["array", "boolean"], "description": "boundaryGap configuration." }
                }
              },
              "description": "Y-axis configuration array (supports multiple Y-axes)."
            },
            "legend": {
              "type": "object",
              "description": "Legend configuration, refer to ECharts legend (show, orient, data, etc.)."
            },
            "title": {
              "type": "object",
              "description": "Title configuration (text, subtext, left, top, textStyle, etc.)."
            },
            "dataset": {
              "type": "array",
              "description": "Chart data source configuration array. When type='table', supports dynamic filtering and aggregation queries, returned fields are defined by dimensionList, chart encode must reference field IDs declared here. Since chart configuration can only configure specific values (grouping during query cannot be used as it produces multiple values per field, e.g., grouping by status field produces multiple status values, which does not meet requirements), when chart stacking is needed, create as many data sources and charts as there are stacking charts, with one-to-one correspondence, each chart using its corresponding data source. For example, to display the quantity of each check-in type per employee using a bar chart, an independent data source needs to be created for each check-in type.",
              "items": {
                "type": "object",
                "properties": {
                  "id": {
                    "type": "string",
                    "description": "Data source identifier"
                  },
                  "name": {
                    "type": "string",
                    "description": "Data source name"
                  },
                  "type": {
                    "type": "string",
                    "enum": ["table", "expression"],
                    "description": "Data source type: 'table' - dynamic table query, 'expression' - static expression data"
                  },
                  "tableId": {
                    "type": "string",
                    "description": "Required when type='table', must be a real table ID existing in the system"
                  },
                  "expression": {
                    "type": "string",
                    "description": "Required when type='expression', must be a valid JS expression string (e.g., `${[...]}`)"
                  },
                  "filter": {
                    "type": "object",
                    "description": "Dynamic filter condition configuration (only effective when type='table'). When field type is Checkbox, value is true/false",
                    "properties": {
                      "opt": {
                        "type": "string",
                        "enum": ["and", "or"],
                        "description": "Root condition combination logic"
                      },
                      "children": {
                        "type": "array",
                        "items": {
                          "type": "object",
                          "description": "Nested condition group, leave empty when not needed",
                          "properties": {
                            "opt": { "type": "string", "enum": ["and", "or"] },
                            "conditionList": {
                              "type": "array",
                              "items": {
                                "type": "object",
                                "properties": {
                                  "fieldId": { "type": "string" },
                                  "opt": { "type": "string" },
                                  "value": { "type": "string" },
                                  "var": { "type": "boolean" }
                                },
                                "required": ["fieldId", "opt", "value", "var"]
                              }
                            }
                          }
                        }
                      },
                      "conditionList": {
                        "type": "array",
                        "items": {
                          "type": "object",
                          "description": "Filter conditions, leave empty when not needed",
                          "properties": {
                            "fieldId": {
                              "type": "string",
                              "description": "Filter field ID, special value '$expression' indicates a function is used"
                            },
                            "opt": {
                              "type": "string",
                              "enum": ["eq","ne","gt","ge","lt","le","contains","notcontains","startswith","endswith","isnull","isnotnull","in","notin"],
                              "description": "Comparison operator, available values: \"eq\",\"ne\",\"gt\",\"ge\",\"lt\",\"le\",\"contains\",\"notcontains\",\"startswith\",\"endswith\",\"isnull\",\"isnotnull\",\"in\",\"notin\""
                            },
                            "value": {
                              "type": "string",
                              "description": "Comparison value or expression (e.g., '1=${filterRecord.name == null ? 1 : 0}'); when value is boolean or numeric type, wrap with ${}, e.g., ${true} or ${100}"
                            },
                            "var": {
                              "type": "boolean",
                              "description": "Flag indicating whether value is an expression"
                            }
                          },
                          "required": ["fieldId", "opt", "value", "var"]
                        }
                      }
                    },
                    "required": ["opt", "children", "conditionList"]
                  },
                  "aggregation": {
                    "type": "boolean",
                    "description": "Whether to enable aggregation calculation",
                    "default": false
                  },
                  "aggregationQueryList": {
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "fieldId": {
                          "type": "string",
                          "description": "Field ID to be aggregated. id and seq fields must not be used for aggregation"
                        },
                        "func": {
                          "type": "string",
                          "enum": ["count", "avg", "sum", "max", "min"],
                          "description": "Aggregation function, options: \"count\", \"avg\", \"sum\", \"max\", \"min\". Note: avg, sum, max, min functions require the field to be numeric type, only fields of type Integer or Double can use these functions"
                        },
                        "distinct": {
                          "type": "boolean",
                          "description": "Whether to deduplicate",
                          "default": false
                        }
                      },
                      "required": ["fieldId", "func"]
                    },
                    "description": "Aggregation calculation configuration (required when aggregation=true)"
                  },
                  "groupByFieldList": {
                    "type": "array",
                    "items": { "type": "string" },
                    "description": "Group by field ID list (e.g., ['name']), using grouping requires enabling aggregation - aggregation=true"
                  },
                  "dimensionList": {
                    "type": "array",
                    "description": "Final output data field list, must contain fields referenced in chart encode. Encode can only use fields from this list, non-existent data fields must not be fabricated. If aggregation fields are used, the field ID format is: 'fieldID_functionName', e.g.: name_count",
                    "items": {
                      "type": "object",
                      "properties": {
                        "id": {
                          "type": "string",
                          "description": "Field ID"
                        },
                        "name": {
                          "type": "string",
                          "description": "Field name"
                        }
                      },
                      "required": ["id", "name"]
                    }
                  },
                  "orderByList": {
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "field": { "type": "string", "description": "Sort field ID" },
                        "type": { "type": "string", "enum": ["asc", "desc"] }
                      },
                      "required": ["field", "type"]
                    },
                    "description": "Sorting"
                  }
                },
                "required": ["id", "name", "type"],
                "allOf": [
                  {
                    "if": { "properties": { "type": { "const": "table" } } },
                    "then": { "required": ["tableId"] }
                  },
                  {
                    "if": { "properties": { "type": { "const": "expression" } } },
                    "then": { "required": ["expression"] }
                  },
                  {
                    "if": { "properties": { "aggregation": { "const": true } } },
                    "then": {
                      "required": ["aggregationQueryList", "groupByFieldList"],
                      "properties": {
                        "dimensionList": {
                          "items": {
                            "properties": {
                              "id": {
                                "pattern": "^(?!.*_count$|.*_avg$|.*_sum$|.*_max$|.*_min$).*$",
                                "description": "Non-aggregation field IDs must not contain function suffixes"
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                ]
              }
            },
            "series": {
              "type": "array",
              "description": "Chart array, must be provided (at least one). Each object in the array must contain id, name, type, and the corresponding type's setting configuration (e.g., barSetting, etc.).",
              "items": {
                "type": "object",
                "properties": {
                  "id": { "type": "string", "description": "Chart unique id" },
                  "name": { "type": "string", "description": "Chart name" },
                  "type": {
                    "type": "string",
                    "description": "Chart type (must match chartType), e.g., 'bar', 'line', 'pie', 'scatter', 'radar', 'gauge', 'boxplot', 'candlestick', 'heatmap', 'funnel', etc.",
                    "enum": ["bar","line","pie","scatter","radar","gauge","boxplot","candlestick","heatmap","funnel"]
                  },
                  "xAxisIndex": { "type": "integer", "description": "Reference xAxis index (if multiple X-axes)" },
                  "yAxisIndex": { "type": "integer", "description": "Reference yAxis index (if multiple Y-axes)" },
                  "barSetting": {
                    "type": "object",
                    "description": "Bar chart configuration, required when type==='bar'",
                    "properties": {
                      "datasetIndex": { "type": "integer", "description": "Data source index, referencing the index in the data source array (0, 1, 2...). When there is only one data source, defaults to 0; when there are multiple data sources, fill in the corresponding data source array subscript based on function." },
                      "encode": {
                        "type": "object",
                        "description": "Chart data configuration, values are taken from the field ID in the corresponding dataset's dimensionList or expression field ID, must not be fabricated",
                        "properties": {
                          "x": {
                            "type": "array",
                            "items": { "type": "string" },
                            "description": "X-axis field"
                          },
                          "y": {
                            "type": "array",
                            "items": { "type": "string" },
                            "description": "Y-axis field"
                          },
                          "seriesName": {
                            "type": "array",
                            "items": { "type": "string" },
                            "description": "Chart name field"
                          }
                        },
                        "required": ["x", "y"]
                      },
                      "barGap": {
                        "type": "string",
                        "description": "Gap between bars (e.g., '20%' or pixel value)",
                        "default": "30%"
                      },
                      "barCategoryGap": {
                        "type": "string",
                        "description": "Category gap between bars (e.g., '20%')",
                        "default": "20%"
                      },
                      "barWidth": {
                        "type": ["string", "number"],
                        "description": "Bar width (e.g., '40%' or pixel value)"
                      },
                      "showBackground": {
                        "type": "boolean",
                        "description": "Whether to show bar background",
                        "default": false
                      },
                      "backgroundStyle": {
                        "type": "object",
                        "properties": {
                          "color": { "type": "string", "description": "Background color" },
                          "borderColor": { "type": "string", "description": "Border color" },
                          "borderWidth": { "type": "number", "description": "Border width" }
                        }
                      },
                      "itemStyle": {
                        "type": "object",
                        "properties": {
                          "color": { "type": "string", "description": "Bar color" },
                          "borderColor": { "type": "string", "description": "Border color" },
                          "borderWidth": { "type": "number", "default": 0 },
                          "borderType": {
                            "type": "string",
                            "enum": ["solid", "dashed", "dotted"],
                            "default": "solid"
                          },
                          "opacity": {
                            "type": "number",
                            "minimum": 0,
                            "maximum": 1,
                            "default": 1
                          }
                        }
                      },
                      "label": {
                        "type": "object",
                        "properties": {
                          "show": { "type": "boolean", "default": true },
                          "position": {
                            "type": "string",
                            "enum": ["top", "right", "bottom", "left", "inside", "insideLeft", "insideRight"],
                            "default": "top"
                          },
                          "formatter": {
                            "type": "string",
                            "description": "Label content formatter (e.g., '{c}')"
                          }
                        }
                      },
                      "stack": {
                        "type": "string",
                        "description": "Stack identifier (charts with the same stack value will be stacked)"
                      }
                    },
                    "required": ["encode","datasetIndex"]
                  },
                  "lineSetting": {
                    "type": "object",
                    "description": "Line chart specific configuration, required when type==='line'",
                    "properties": {
                      "datasetIndex": { "type": "integer", "description": "Data source index, referencing the index in the data source array (0, 1, 2...). When there is only one data source, defaults to 0; when there are multiple data sources, fill in the corresponding data source array subscript based on function." },
                      "encode": {
                        "type": "object",
                        "description": "Chart data configuration, values are taken from the field ID in the corresponding dataset's dimensionList or expression field ID, must not be fabricated",
                        "properties": {
                          "x": { "type": "array", "items": { "type": "string" }, "description": "X-axis field" },
                          "y": { "type": "array", "items": { "type": "string" }, "description": "Y-axis field" },
                          "seriesName": { "type": "array", "items": { "type": "string" }, "description": "Chart name field" }
                        },
                        "required": ["x", "y"]
                      },
                      "smooth": { "type": "boolean", "description": "Whether to display smoothly", "default": false },
                      "symbol": {
                        "type": "string",
                        "enum": ["circle", "rect", "roundRect", "triangle", "diamond", "pin", "arrow", "none"],
                        "description": "Marker symbol",
                        "default": "emptyCircle"
                      },
                      "symbolSize": { "type": "number", "description": "Marker size", "default": 4 },
                      "showSymbol": { "type": "boolean", "description": "Whether to show markers", "default": true },
                      "areaStyle": {
                        "type": "object",
                        "description": "Area fill style",
                        "properties": {
                          "color": { "type": "string", "description": "Fill color" },
                          "opacity": { "type": "number", "minimum": 0, "maximum": 1, "default": 0.6 }
                        }
                      },
                      "lineStyle": {
                        "type": "object",
                        "description": "Line style",
                        "properties": {
                          "width": { "type": "number", "default": 1 },
                          "type": { "type": "string", "enum": ["solid", "dashed", "dotted"], "default": "solid" }
                        }
                      }
                    },
                    "required": ["encode","datasetIndex"]
                  },
                  "pieSetting": {
                    "type": "object",
                    "description": "Pie chart specific configuration, required when type==='pie'",
                    "properties": {
                      "datasetIndex": { "type": "integer", "description": "Data source index, referencing the index in the data source array (0, 1, 2...). When there is only one data source, defaults to 0; when there are multiple data sources, fill in the corresponding data source array subscript based on function." },
                      "encode": {
                        "type": "object",
                        "description": "Chart data configuration, values are taken from the field ID in the corresponding dataset's dimensionList or expression field ID, must not be fabricated",
                        "properties": {
                          "value": { "type": "array", "items": { "type": "string" }, "description": "Value field" },
                          "itemName": { "type": "string", "description": "Item name field" }
                        },
                        "required": ["value", "itemName"]
                      },
                      "radius": {
                        "type": "array",
                        "items": { "type": "string" },
                        "description": "Radius configuration (e.g., ['0%','70%'])",
                        "default": ["0%", "75%"]
                      },
                      "center": {
                        "type": "array",
                        "items": { "type": "string" },
                        "description": "Center position (e.g., ['50%','50%'])",
                        "default": ["50%", "50%"]
                      },
                      "label": {
                        "type": "object",
                        "properties": {
                          "show": { "type": "boolean", "default": true },
                          "position": { "type": "string", "enum": ["inside", "outside", "center"], "default": "outside" }
                        }
                      },
                      "labelLine": { "type": "object", "description": "Label guide line configuration" }
                    },
                    "required": ["encode","datasetIndex"]
                  },
                  "scatterSetting": {
                    "type": "object",
                    "description": "Scatter chart specific configuration, required when type==='scatter'",
                    "properties": {
                      "datasetIndex": { "type": "integer", "description": "Data source index, referencing the index in the data source array (0, 1, 2...). When there is only one data source, defaults to 0; when there are multiple data sources, fill in the corresponding data source array subscript based on function." },
                      "encode": {
                        "type": "object",
                        "description": "Chart data configuration, values are taken from the field ID in the corresponding dataset's dimensionList or expression field ID, must not be fabricated",
                        "properties": {
                          "x": { "type": "array", "items": { "type": "string" }, "description": "X-axis field" },
                          "y": { "type": "array", "items": { "type": "string" }, "description": "Y-axis field" },
                          "value": { "type": "array", "items": { "type": "string" }, "description": "Value field" }
                        },
                        "required": ["x", "y"]
                      },
                      "symbolSize": { "type": "number", "default": 4 },
                      "symbol": {
                        "type": "string",
                        "enum": ["circle", "rect", "triangle", "diamond", "pin"],
                        "default": "circle"
                      }
                    },
                    "required": ["encode","datasetIndex"]
                  },
                  "radarSetting": {
                    "type": "object",
                    "description": "Radar chart specific configuration, required when type==='radar'",
                    "properties": {
                      "datasetIndex": { "type": "integer", "description": "Data source index, referencing the index in the data source array (0, 1, 2...). When there is only one data source, defaults to 0; when there are multiple data sources, fill in the corresponding data source array subscript based on function." },
                      "encode": {
                        "type": "object",
                        "description": "Chart data configuration, values are taken from the field ID in the corresponding dataset's dimensionList or expression field ID, must not be fabricated",
                        "properties": {
                          "value": { "type": "array", "items": { "type": "string" }, "description": "Value field" }
                        },
                        "required": ["value"]
                      },
                      "areaStyle": { "type": "object", "description": "Area fill style" },
                      "lineStyle": { "type": "object", "description": "Line style" }
                    },
                    "required": ["encode","datasetIndex"]
                  },
                  "gaugeSetting": {
                    "type": "object",
                    "description": "Gauge chart specific configuration, required when type==='gauge'",
                    "properties": {
                      "datasetIndex": { "type": "integer", "description": "Data source index, referencing the index in the data source array (0, 1, 2...). When there is only one data source, defaults to 0; when there are multiple data sources, fill in the corresponding data source array subscript based on function." },
                      "encode": {
                        "type": "object",
                        "description": "Chart data configuration, values are taken from the field ID in the corresponding dataset's dimensionList or expression field ID, must not be fabricated",
                        "properties": {
                          "value": { "type": "array", "items": { "type": "string" }, "description": "Value field" }
                        },
                        "required": ["value"]
                      },
                      "min": { "type": "number", "default": 0 },
                      "max": { "type": "number", "default": 100 },
                      "axisLine": {
                        "type": "object",
                        "properties": {
                          "lineStyle": {
                            "type": "object",
                            "properties": {
                              "color": {
                                "type": "array",
                                "items": {
                                  "type": "array",
                                  "items": [
                                    { "type": "number" },
                                    { "type": "string" }
                                  ],
                                  "minItems": 2,
                                  "maxItems": 2
                                },
                                "description": "Color segments (e.g., [[0.3,'#67e0e3'],[0.7,'#37a2da'],[1,'#fd666d']])"
                              }
                            }
                          }
                        }
                      },
                      "detail": {
                        "type": "object",
                        "properties": {
                          "formatter": { "type": "string", "description": "Format string (e.g., '{value}%')" }
                        }
                      }
                    },
                    "required": ["encode","datasetIndex"]
                  },
                  "boxplotSetting": {
                    "type": "object",
                    "description": "Box plot specific configuration, required when type==='boxplot'",
                    "properties": {
                      "datasetIndex": { "type": "integer", "description": "Data source index, referencing the index in the data source array (0, 1, 2...). When there is only one data source, defaults to 0; when there are multiple data sources, fill in the corresponding data source array subscript based on function." },
                      "encode": {
                        "type": "object",
                        "description": "Chart data configuration, values are taken from the field ID in the corresponding dataset's dimensionList or expression field ID, must not be fabricated",
                        "properties": {
                          "x": { "type": "array", "items": { "type": "string" }, "description": "Category field" },
                          "y": {
                            "type": "array",
                            "items": { "type": "string" },
                            "minItems": 5,
                            "maxItems": 5,
                            "description": "Value field array (must be in [min,q1,median,q3,max] order)"
                          }
                        },
                        "required": ["x", "y"]
                      },
                      "boxWidth": { "type": "array", "items": { "type": "number" }, "description": "Box width range (e.g., [10,30])" }
                    },
                    "required": ["encode","datasetIndex"]
                  },
                  "candlestickSetting": {
                    "type": "object",
                    "description": "Candlestick chart specific configuration, required when type==='candlestick'",
                    "properties": {
                      "datasetIndex": { "type": "integer", "description": "Data source index, referencing the index in the data source array (0, 1, 2...). When there is only one data source, defaults to 0; when there are multiple data sources, fill in the corresponding data source array subscript based on function." },
                      "encode": {
                        "type": "object",
                        "description": "Chart data configuration, values are taken from the field ID in the corresponding dataset's dimensionList or expression field ID, must not be fabricated",
                        "properties": {
                          "x": { "type": "array", "items": { "type": "string" }, "description": "X-axis field" },
                          "y": {
                            "type": "array",
                            "items": { "type": "string" },
                            "minItems": 4,
                            "maxItems": 4,
                            "description": "Price fields (in [open,close,high,low] order)"
                          }
                        },
                        "required": ["x", "y"]
                      },
                      "barWidth": { "type": "number", "description": "K-line bar width", "default": 10 }
                    },
                    "required": ["encode","datasetIndex"]
                  },
                  "heatmapSetting": {
                    "type": "object",
                    "description": "Heatmap specific configuration, required when type==='heatmap'",
                    "properties": {
                      "datasetIndex": { "type": "integer", "description": "Data source index, referencing the index in the data source array (0, 1, 2...). When there is only one data source, defaults to 0; when there are multiple data sources, fill in the corresponding data source array subscript based on function." },
                      "encode": {
                        "type": "object",
                        "description": "Chart data configuration",
                        "properties": {
                          "x": { "type": "array", "items": { "type": "string" }, "description": "X-axis category field" },
                          "y": { "type": "array", "items": { "type": "string" }, "description": "Y-axis category field" },
                          "value": { "type": "array", "items": { "type": "string" }, "description": "Value field" }
                        },
                        "required": ["x", "y", "value"]
                      },
                      "label": {
                        "type": "object",
                        "properties": {
                          "show": { "type": "boolean", "default": true },
                          "formatter": { "type": "string", "description": "Display format (e.g., '{@[1]}')" }
                        }
                      }
                    },
                    "required": ["encode","datasetIndex"]
                  },
                  "funnelSetting": {
                    "type": "object",
                    "description": "Funnel chart specific configuration, required when type==='funnel'",
                    "properties": {
                      "datasetIndex": { "type": "integer", "description": "Data source index, referencing the index in the data source array (0, 1, 2...). When there is only one data source, defaults to 0; when there are multiple data sources, fill in the corresponding data source array subscript based on function." },
                      "encode": {
                        "type": "object",
                        "description": "Chart data configuration, values are taken from the field ID in the corresponding dataset's dimensionList or expression field ID",
                        "properties": {
                          "value": { "type": "array", "items": { "type": "string" }, "description": "Value field" },
                          "itemName": { "type": "string", "description": "Item name field" }
                        },
                        "required": ["value", "itemName"]
                      },
                      "sort": { "type": "string", "enum": ["ascending", "descending", "none"], "default": "descending" },
                      "gap": { "type": "number", "description": "Gap between data items", "default": 0 }
                    },
                    "required": ["encode","datasetIndex"]
                  },
                  "labelLayout": { "type": "object", "description": "Label layout conflict resolution strategy" },
                  "silent": { "type": "boolean", "description": "Whether silent" },
                  "colorBy": { "type": "string", "description": "Color usage strategy, e.g., 'data' or 'series', etc." },
                  "emphasis": { "type": "object", "description": "Emphasis/focus configuration (refer to ECharts emphasis)." },
                  "itemStyle": { "type": "object", "description": "Item style (borderWidth, borderColor, opacity, etc.)." },
                  "showSymbol": { "type": "boolean", "description": "Whether to show symbol for line/scatter (boolean)." }
                },
                "required": ["name","type"]
              }
            },
            "tooltip": {
              "type": "object",
              "description": "General tooltip configuration"
            },
            "dataZoom": {
              "type": "array",
              "items": { "type": "object" },
              "description": "dataZoom configuration array"
            },
            "visualMap": {
              "type": "array",
              "items": { "type": "object" },
              "description": "visualMap configuration array (used for heatmap/color mapping)"
            },
            "angleAxis": {
              "type": "array",
              "items": { "type": "object" },
              "description": "Polar coordinate angle axis configuration"
            },
            "radiusAxis": {
              "type": "array",
              "items": { "type": "object" },
              "description": "Polar coordinate radius axis configuration"
            },
            "style": {
              "type": "object",
              "description": "Custom style fragment"
            }
          },
          "required": ["series", "dataset", "tooltip"]
        },
        "disableFilterCache": {
          "type": "boolean",
          "description": "Whether to disable filter cache"
        },
        "filterLabelPosition": {
          "type": "string",
          "description": "Filter label position, e.g., 'top', 'left', 'right', etc."
        }
      },
      "required": ["name", "type", "scope", "width", "height", "cardStyle", "proChartSetting"]
    }
  }
}
```
