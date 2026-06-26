---
name: obsidian-charts-layout
description: |
  Obsidian Charts View plugin (caronchen/obsidian-chartsview-plugin) setup,
  using G2Plot (AntV) code-block syntax for Pie/Bar/Column/Line/Scatter charts
  in Obsidian, with always-visible annotation labels, and bilingual Markdown
  layout rules for AI daily reports and PDF export.
  Use when:
  (1) Installing/configuring/troubleshooting Charts View plugin in Obsidian,
  (2) Creating Pie/Bar/Column/Line/Scatter charts in Obsidian notes,
  (3) Adding always-visible annotation labels on chart elements,
  (4) Generating charts via code (Python/CLI) into the Obsidian vault,
  (5) Formatting bilingual (CN/EN) Markdown notes for Obsidian + PDF output.
---

# Obsidian Charts & Layout Skill

## ⚠️ Before You Start — Critical Facts

This skill is for `caronchen/obsidian-chartsview-plugin` (Charts View).

| Fact | Detail |
|------|--------|
| Plugin ID | `caronchen/obsidian-chartsview-plugin` |
| Code block tag | ````chartsview` — **NOT** ````chart` |
| Chart engine | AntV G2Plot — **NOT** Chart.js |
| Data format | Array of objects (`data:` with named fields) |
| Field mapping | `xField: "name"` / `yField: "value"` / `angleField: "value"` |

**If you use ````chart` or `labels/datasets` format, the chart will NOT render.**

### 命名对照表

| 英文术语 | 中文说法 | 含义 |
|---------|---------|------|
| Annotation | **标注** | 一直显示在图表上的文字（柱子顶端数字、饼图旁边的名称和百分比） |
| Data label / Tooltip | 数据标签 | 鼠标悬停时弹出的提示框（无需配置，默认就有） |

### 历史踩坑总结（一定要看）

1. ❌ **用了 ````chart` 标签** → 图表不显示，显示为源代码 ✅ **必须用 ````chartsview`**
2. ❌ **用了 Chart.js 格式（`labels/datasets`）** → 图表不显示 ✅ **必须用 G2Plot 格式（`data` 对象数组）**
3. ❌ **字段名没加双引号（`xField: price`）** → 部分情况能工作但不可靠 ✅ **必须加引号 `xField: "price"`**
4. ❌ **通过 PowerShell 传中文内容建模板** → 引号被吃掉、内容被截断 ✅ **直接用 Python 写文件到 vault 目录**
5. ❌ **通过 `obsidian eval` 传超大 JS 代码** → Obsidian IPC 崩溃、插件列表丢失 ✅ **用简单的 CLI 命令或重启 Obsidian**
6. ❌ **通过 `obsidian create name=... content=...` 传带中文/`$`/引号的内容** → PowerShell 可能截断或转义 ✅ **直接用 Python 写文件到 vault 目录**

---

## 1. Plugin Installation

### 1.1 CLI 安装

```powershell
obsidian plugin:install id=obsidian-chartsview-plugin
obsidian plugin:enable id=obsidian-chartsview-plugin
```

### 1.2 查看图表

- 必须在 **阅读模式/预览模式**（Reading/Preview Mode）下才能看到图表
- 快捷键：`Ctrl+E`（Windows/Linux）或 `Cmd+E`（Mac）
- 编辑模式（Source/Edit Mode）下只会显示代码块

### 1.3 插件丢失后的恢复

If `obsidian plugins` no longer lists `obsidian-chartsview-plugin` (this can happen after a broken IPC call):

```powershell
# Step 1: Reinstall (it says "already installed" — that's OK)
obsidian plugin:install id=obsidian-chartsview-plugin

# Step 2: Enable it
obsidian plugin:enable id=obsidian-chartsview-plugin

# Step 3: Verify
obsidian plugins | Select-String "chartsview"
```

If charts still don't render after this, fully close and reopen Obsidian.

---

## 2. Chart Syntax — Complete Reference

A chart is a fenced code block with language `chartsview`:

````
```chartsview
type: Pie          # REQUIRED: Pie/Bar/Column/Line/Scatter
data:               # REQUIRED: array of objects
  - field1: value1  # each data item is one object with named fields
    field2: value2
options:            # REQUIRED: chart configuration
  xField: "field1"  # which field maps to X axis
  yField: "field2"  # which field maps to Y axis
```
````

### 2.1 数据格式详解

The `data:` section is an array of YAML objects. Each object has fields that you NAME yourself.

```yaml
data:
  - type: OpenAI     # field name = "type", value = "OpenAI"
    value: 45        # field name = "value", value = 45
  - type: DeepSeek   # second data item
    value: 30
```

**Key rule:** Whatever field names you use in `data:`, you must reference them consistently in:
- `options.xField`, `options.yField`, `options.angleField`, `options.colorField`
- `options.label.formatter` function body (via `datum.fieldName`)

### 2.2 options 字段说明

```yaml
options:
  xField: "fieldName"       # X轴映射的字段名（必须加双引号）
  yField: "fieldName"       # Y轴映射的字段名（必须加双引号）
  angleField: "fieldName"   # 饼图：扇形大小映射的字段
  colorField: "fieldName"   # 按字段值自动分配颜色
  seriesField: "fieldName"  # 按字段值分组（多系列对比时用。只有一组数据可以省略）
  radius: 0.7               # 饼图半径比例
  smooth: true              # 折线是否平滑
  legend:
    display: true            # 是否显示图例
    position: "bottom"       # "top"|"bottom"|"left"|"right"
  label:                     # 标注配置（一直显示在图表上的文字）
    position: "top"          # "top"/"right"/"outer"/"inner"
    formatter:
      function formatter(datum) {
        return datum.fieldName + " " + datum.otherField;
      }
    offset: 5
    style:
      fill: "#333"
      fontSize: 11
  xAxis:
    title:
      text: "轴标题"
  yAxis:
    max: 20                  # Y轴最大值（Column必须设，给顶端标注留空间）
  point:
    size: 4                  # 折线图/散点图数据点大小
```

### 2.3 formatter 函数详解

The formatter function is written as a JavaScript function inside YAML:

```yaml
label:
  formatter:
    function formatter(datum) {
      return datum.fieldName + " " + datum.fieldName2;
    }
```

**`datum` 对象** = data 数组中的每一个元素。你的 data 有什么字段，`datum` 就有什么属性。

例如如果 data 是：
```yaml
data:
  - model: GPT-5
    price: 15.00
```
那么 `datum.model` = `"GPT-5"`, `datum.price` = `15.00`。

**常见 formatter 写法（全部已验证可工作）：**
```
return datum.type + ' ' + datum.value + '%';          # 饼图：OpenAI 45%
return '$' + datum.price.toFixed(2);                  # 柱状图：$15.00
return datum.price;                                   # 折线图：15
return datum.model + ': $' + datum.price.toFixed(2);  # 组合字段：GPT-5: $15.00
```

**`$` 符号说明：** 单引号 `'$'` 和双引号 `"$"` 在 YAML 中都能正常工作。
已验证的参考模板（W21-市场图谱）使用的是 `'$'`。两种写法都 OK。

---

## 3. Chart Templates（已全部在 Obsidian 中验证通过）

### 3.1 Pie（饼图）— 有标注

```chartsview
type: Pie
data:
  - type: 极低价($0.05-0.30/M)
    value: 42
  - type: 中端($0.30-1.00/M)
    value: 38
  - type: 高端($1.00-5.00/M)
    value: 15
  - type: 超旗舰($5+/M)
    value: 5
options:
  angleField: "value"       # 扇形大小 = value 字段
  colorField: "type"        # 每个 type 分配不同颜色
  radius: 0.7               # 饼图半径比例
  label:
    type: "outer"           # 标注在饼图外部
    formatter:
      function formatter(datum) {
        return datum.type + ' ' + datum.value + '%';
      }
    offset: 15              # 标注离饼图边缘的距离
    style:
      fontSize: 10
  legend:
    position: "bottom"
```

**Pie 特殊说明：**
- 不用 `xField`/`yField`，改用 `angleField`（数值）和 `colorField`（分类）
- `type: "outer"` 把标注摆在饼图外部，由引线与饼图连接
- formatter 的 `datum.type` 引用 data 里的 `type` 字段，`datum.value` 引用 `value` 字段

---

### 3.2 Bar（横向柱状图）— 柱子右端有标注

```chartsview
type: Bar
data:
  - model: DeepSeek V4 Flash
    price: 0.11
  - model: DeepSeek V3.2
    price: 0.25
  - model: Llama 4 Maverick
    price: 0.15
  - model: Qwen3.6 Flash
    price: 0.19
  - model: Qwen3.6 Plus
    price: 0.33
  - model: GLM-4.7 Flash
    price: 0.06
  - model: Kimi K2.6
    price: 0.73
  - model: GLM-5.1
    price: 0.98
  - model: DeepSeek V4 Pro
    price: 0.43
  - model: o3-mini
    price: 1.10
  - model: GPT-5 Chat
    price: 1.25
  - model: Gemini 2.5 Pro
    price: 1.25
  - model: Claude Sonnet 4
    price: 3.00
options:
  xField: "price"            # X轴（横向）= price 字段（数值）
  yField: "model"            # Y轴（纵向）= model 字段（分类标签）
  seriesField: "model"       # 按 model 分组（只有一组数据时可以省略）
  colorField: "model"        # 每个 model 分配不同颜色
  label:
    position: "right"        # 标注在柱子右端
    formatter:
      function formatter(datum) {
        return '$' + datum.price.toFixed(2);
      }
    offset: 5
    style:
      fill: "#333"
      fontSize: 11
  xAxis:
    title:
      text: "价格 ($/Mtoken)"
```

**Bar 特殊说明：**
- G2Plot 的 `Bar` = **横向柱状图**（Y轴是分类标签，X轴是数值）
- 如果要做纵向柱状图，用 `type: Column`（见下一节）
- `yField` 放分类字段（model），`xField` 放数值字段（price）
- `position: "right"` 让标注出现在每个柱子的右端
- `seriesField` 和 `colorField` 设为同一个字段时，每个不同的值自动分配不同颜色
- 如果只有一组数据（不需要多系列对比），`seriesField` 和 `colorField` 可以省略

---

### 3.3 Column（纵向柱状图）— 柱子顶端有标注

```chartsview
type: Column
data:
  - model: GPT-5
    price: 15.00
  - model: DeepSeek
    price: 0.43
  - model: Claude
    price: 3.00
  - model: GLM
    price: 0.98
options:
  xField: "model"            # X轴（横向）= model 字段（分类标签）
  yField: "price"            # Y轴（纵向）= price 字段（数值）
  label:
    position: "top"          # 标注在柱子顶端
    formatter:
      function formatter(datum) {
        return '$' + datum.price.toFixed(2);
      }
    offset: 5
    style:
      fill: "#333"
      fontSize: 11
  yAxis:
    max: 20                  # ⚠️ 必须设！给最高柱子的标注留空间
```

**Column 特殊说明：**
- `Column` = **纵向柱状图**（X轴是分类，Y轴是数值），与 `Bar` 的轴相反
- **⚠️ 必须设置 `yAxis.max`** 为比最大数据值大的数值，否则最高柱子的标注会被裁掉
- 比如最大 price 是 15，就设 `max: 20`；最大 value 是 100，就设 `max: 120`
- `position: "top"` 把标注放在柱子顶端

---

### 3.4 Line（折线图）— 数据点上有标注

```chartsview
type: Line
data:
  - month: Jan
    price: 10
  - month: Feb
    price: 12
  - month: Mar
    price: 8
  - month: Apr
    price: 15
  - month: May
    price: 13
options:
  xField: "month"            # X轴 = month 字段
  yField: "price"            # Y轴 = price 字段
  smooth: true               # 平滑曲线
  point:
    size: 4                  # 数据点的大小
  label:
    formatter:
      function formatter(datum) {
        return datum.price;
      }
```

**Line 特殊说明：**
- `smooth: true` 让折线变为平滑曲线（false 则为折线）
- `point.size` 控制数据点圆点大小
- Bar/Column 需要 `position` 指定标注位置，Line 不需要

---

### 3.5 Scatter（散点图）— **不支持标注**，只有鼠标悬停

```chartsview
type: Scatter
data:
  - x: 0.11
    y: 10
  - x: 0.43
    y: 50
  - x: 1.25
    y: 100
  - x: 3.00
    y: 200
  - x: 0.98
    y: 80
options:
  xField: "x"
  yField: "y"
  point:
    size: 5
```

**⚠️ 限制：** Scatter 图表类型不支持一直显示的标注（annotation）。数据标签（鼠标悬停）是默认有的，不需要额外配置。如果需要一直显示标注，改用 Pie/Bar/Column。

---

## 4. How to Write Charts into Obsidian Notes

### 4.1 通过 Python 写文件到 vault（✅ 推荐，不会编码问题）

```python
# vault_path = 你的 Obsidian vault 根目录
note_content = '''# My Chart Note

## Price Comparison

```chartsview
type: Bar
data:
  - model: GPT-5
    price: 15.00
  - model: DeepSeek
    price: 0.43
options:
  xField: "price"
  yField: "model"
  seriesField: "model"
  colorField: "model"
  label:
    position: "right"
    formatter:
      function formatter(datum) {
        return '$' + datum.price.toFixed(2);
      }
```

'''

import os
vault = r"C:\Users\用户名\你的Vault"
path = os.path.join(vault, "My Chart Note.md")
with open(path, 'w', encoding='utf-8') as f:
    f.write(note_content)
```

写完之后，Obsidian 会自动检测到新文件。

### 4.2 通过 `obsidian append` 给已有笔记追加图表

```python
# 用 Python 读取现有笔记，追加图表代码，再写回
vault_note_path = r"C:\Users\...\vault\my note.md"
with open(vault_note_path, 'r', encoding='utf-8') as f:
    content = f.read()

chart_block = '''

## New Chart

```chartsview
type: Pie
data:
  - type: OpenAI
    value: 45
options:
  angleField: "value"
  colorField: "type"
  label:
    type: "outer"
    formatter:
      function formatter(datum) {
        return datum.type + ' ' + datum.value + '%';
      }
```

'''

with open(vault_note_path, 'w', encoding='utf-8') as f:
    f.write(content + chart_block)
```

### 4.3 通过 Obsidian CLI（仅限简单内容）

```powershell
obsidian append path="my note.md" content="Hello World"
obsidian create name="test" content="Hello World"
```

**⚠️ 不要通过 `obsidian eval` 发大段代码**，会崩 IPC。
**⚠️ 不要通过 PowerShell `-c` 传中文/引号/`$` 内容建模板**，会被截断或转义。

---

## 5. Troubleshooting

| 现象 | 原因 | 解决方法 |
|------|------|---------|
| 图表显示为源代码（```代码块） | 在编辑模式 | 切到阅读模式：`Ctrl+E` |
| 整个图表区域空白 | 代码块标签写成了 ````chart` | 改为 ````chartsview` |
| 空白或报错 | 用了 `labels/datasets` 格式 | 改为 G2Plot 的 `data` 对象数组格式 |
| 字段名报错 | `xField: price` 没加双引号 | 改为 `xField: "price"` |
| 柱状图顶端标注被裁掉 | `yAxis.max` 没设置 | 添加 `yAxis: max: 大于最大值的数` |
| 散点图没有标注 | 散点图不支持 annotation | 这是正常限制，改用 Pie/Bar/Column |
| 饼图标注看不到 | `label.type` 没设或设错了 | 设置为 `type: "outer"` |
| 插件列表找不到 chartsview | IPC 管道崩了 | `obsidian plugin:install` 重装 + 启用 |
| 写入的模板内容不对 | PowerShell 吃了引号/截断了 | 用 Python 直接写文件到 vault |
| Obsidian 报 JSON parse 错误 | eval 传了超长载荷 | 完全关闭重开 Obsidian |

---

## 6. Bilingual Layout Rules

For Chinese-English AI daily report layout in Obsidian, see [references/bilingual-layout.md](references/bilingual-layout.md).

> **核心原则：所有中英文成对出现的地方，统一用 `- ` 列表 + 行末双空格 `<br>`，不要用段落、分隔线或其他格式。**
