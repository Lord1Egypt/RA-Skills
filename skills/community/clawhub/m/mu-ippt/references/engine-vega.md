# Vega 数据图表引擎

> 适用：柱状图/折线图/散点图/热力图/面积图/饼图/雷达图/词云

## 渲染流程

1. 编写 vega-lite JSON（90% 场景）或 vega JSON（雷达/词云）
2. 用 Markdown 代码块包裹（` ```vega-lite ` 或 ` ```vega `）
3. 写入 `/tmp/vega_{timestamp}.md`，browser automation tool 打开 Markdown Viewer 渲染
4. 截图 PNG → 嵌入幻灯片（同 infographic 引擎流程）

## 语法要点

- 必须包含 `"$schema": "https://vega.github.io/schema/vega-lite/v5.json"`（vega 用 v6）
- 必须用合法 JSON（双引号、无尾逗号、无注释）
- field 名称大小写敏感，必须与 data 中 key 精确匹配
- type 只能是：`quantitative` | `nominal` | `ordinal` | `temporal`
- Vega-Lite 用 `mark` + `encoding`；Vega 用 `marks` + `scales` + `signals`

## 常用图表模式

### 柱状图（横向排序）

```vega-lite
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "data": {"values": [
    {"item": "Alpha", "value": 28},
    {"item": "Beta", "value": 55},
    {"item": "Gamma", "value": 43}
  ]},
  "mark": "bar",
  "encoding": {
    "y": {"field": "item", "type": "nominal", "sort": "-x"},
    "x": {"field": "value", "type": "quantitative"}
  }
}
```

### 折线图（多系列）

```vega-lite
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "data": {"values": [
    {"month": 1, "series": "A", "value": 28},
    {"month": 2, "series": "A", "value": 55},
    {"month": 1, "series": "B", "value": 35},
    {"month": 2, "series": "B", "value": 48}
  ]},
  "mark": "line",
  "encoding": {
    "x": {"field": "month", "type": "ordinal"},
    "y": {"field": "value", "type": "quantitative"},
    "color": {"field": "series", "type": "nominal"}
  }
}
```

### 饼图/环形图

```vega-lite
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "data": {"values": [
    {"category": "A", "value": 30},
    {"category": "B", "value": 45},
    {"category": "C", "value": 25}
  ]},
  "mark": {"type": "arc", "innerRadius": 50},
  "encoding": {
    "theta": {"field": "value", "type": "quantitative"},
    "color": {"field": "category", "type": "nominal"}
  }
}
```

### 散点图

```vega-lite
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "data": {"values": [
    {"x": 10, "y": 28, "cat": "A"},
    {"x": 20, "y": 55, "cat": "B"},
    {"x": 30, "y": 43, "cat": "A"}
  ]},
  "mark": "point",
  "encoding": {
    "x": {"field": "x", "type": "quantitative"},
    "y": {"field": "y", "type": "quantitative"},
    "color": {"field": "cat", "type": "nominal"}
  }
}
```

### 热力图

```vega-lite
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "data": {"values": [
    {"x": "A", "y": "1", "value": 10},
    {"x": "A", "y": "2", "value": 20},
    {"x": "B", "y": "1", "value": 25},
    {"x": "B", "y": "2", "value": 30}
  ]},
  "mark": "rect",
  "encoding": {
    "x": {"field": "x", "type": "nominal"},
    "y": {"field": "y", "type": "nominal"},
    "color": {"field": "value", "type": "quantitative", "scale": {"scheme": "blues"}}
  }
}
```

### 雷达图（需完整 vega 语法）

```vega
{
  "$schema": "https://vega.github.io/schema/vega/v6.json",
  "width": 400, "height": 400, "padding": 40,
  "autosize": {"type": "none", "contains": "padding"},
  "signals": [{"name": "radius", "update": "width / 2"}],
  "data": [{"name": "table", "values": [
    {"dim": "沟通", "val": 85, "cat": "甲"},
    {"dim": "执行", "val": 72, "cat": "甲"},
    {"dim": "创新", "val": 90, "cat": "甲"},
    {"dim": "沟通", "val": 70, "cat": "乙"},
    {"dim": "执行", "val": 88, "cat": "乙"},
    {"dim": "创新", "val": 75, "cat": "乙"}
  ]}],
  "scales": [
    {"name": "angular", "type": "point", "range": {"signal": "[-PI, PI]"}, "padding": 0.5, "domain": {"data": "table", "field": "dim"}},
    {"name": "radial", "type": "linear", "range": {"signal": "[0, radius]"}, "zero": true, "domain": [0, 100]},
    {"name": "color", "type": "ordinal", "domain": {"data": "table", "field": "cat"}, "range": ["#3b82f6", "#f59e0b"]}
  ],
  "encode": {"enter": {"x": {"signal": "radius"}, "y": {"signal": "radius"}}},
  "marks": [{"type": "group", "from": {"facet": {"data": "table", "name": "facet", "groupby": ["cat"]}},
    "marks": [{"type": "line", "from": {"data": "facet"}, "encode": {"enter": {
      "interpolate": {"value": "linear-closed"},
      "x": {"signal": "scale('radial', datum.val) * cos(scale('angular', datum.dim))"},
      "y": {"signal": "scale('radial', datum.val) * sin(scale('angular', datum.dim))"},
      "stroke": {"scale": "color", "field": "cat"},
      "strokeWidth": {"value": 2},
      "fill": {"scale": "color", "field": "cat"},
      "fillOpacity": {"value": 0.1}
    }}}]
  }]
}
```

### 词云（需完整 vega 语法）

```vega
{
  "$schema": "https://vega.github.io/schema/vega/v6.json",
  "width": 500, "height": 300,
  "data": [{"name": "table", "values": [
    {"word": "协作", "count": 85},
    {"word": "创新", "count": 78},
    {"word": "执行力", "count": 65},
    {"word": "学习", "count": 52}
  ], "transform": [
    {"type": "wordcloud", "size": [500, 300], "text": {"field": "word"}, "fontSize": {"field": "count"}, "fontSizeRange": [16, 60], "padding": 2}
  ]}],
  "marks": [{"type": "text", "from": {"data": "table"}, "encode": {"enter": {
    "text": {"field": "word"}, "x": {"field": "x"}, "y": {"field": "y"},
    "angle": {"field": "angle"}, "fontSize": {"field": "fontSize"},
    "fill": {"value": "#3b82f6"}, "align": {"value": "center"}
  }}}]
}
```

## 常见错误

| 问题 | 解决方案 |
|------|----------|
| 图表不渲染 | 检查 JSON 合法性、确认包含 `$schema` |
| 数据不显示 | field 名必须与 data 中 key 大小写精确匹配 |
| 图表类型错误 | mark 类型要与数据结构匹配（arc→饼图、rect→热力图） |
| 颜色不可见 | 检查 color scale 对比度，可指定 `"scheme": "category10"` |
| 双轴显示异常 | 添加 `"resolve": {"scale": {"y": "independent"}}` |
| 饼图无 innerRadius | `"mark": {"type": "arc", "innerRadius": 50}` 才是环形图 |
| 雷达图/词云用 vega-lite | 这两种必须用完整 vega 语法，不支持 vega-lite |
