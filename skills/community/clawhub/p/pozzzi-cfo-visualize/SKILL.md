---
name: pozzzi-cfo-visualize
description: 噗滋（pozzzi）报表官 - 图表代码生成工具。接收 pozzzi-cfo-analyze 返回的 viz_specs，生成目标工具（Excel/WPS/钉钉/腾讯文档）的图表代码。48 个图表模板（4 种工具 × 12 种 chart 类型），代码可直接粘贴回原报表。
---

# 可视化生成工具 (visualize)

> 基于已分析数据集，生成目标工具（Excel/WPS/钉钉/腾讯文档）的图表代码

## 工具描述

接受 `dataset_id` 和可视化规格，调用 `/api/visualize`，返回可直接贴入目标工具的图表代码（公式/VBA/Apps Script/宏脚本等）。

## 触发方式

```
/visualize [图表类型] [维度说明]
```

或自然语言触发：
- "帮我画个柱状图"
- "做个对比表"
- "生成图表代码"

## 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `dataset_id` | string | 是 | 来自上传步骤的数据集 ID |
| `chart_type` | enum | 是 | bar/line/pie/pivot/heatmap/waterfall/scatter/area/radar/funnel/gauge/sankey（共 12 种，详见下方"支持图表类型"） |
| `x_axis` | string | 是 | X 轴字段名（来自数据集列名） |
| `y_metrics` | string[] | 是 | Y 轴指标，最多 5 个 |
| `target_tool` | enum | 是 | excel/wps/dingtalk/tencent-docs |
| `title` | string | 否 | 图表标题 |

## 输出格式

根据 `target_tool` 返回对应代码：

### Excel（VBA / Office Scripts）
```vba
' [图表标题] - Excel VBA
Sub CreateChart()
    ' 自动生成，可直接运行
    ...
End Sub
```

### WPS（WPS JSAPI）
```javascript
// [图表标题] - WPS JSAPI
const chart = Application.ActiveSheet.Charts.Add();
...
```

### 钉钉智能表格（钉钉宏脚本）
```javascript
// [图表标题] - 钉钉宏
...
```

### 腾讯文档（Sheets API）
```javascript
// [图表标题] - 腾讯文档
...
```

## 支持图表类型（v1.5.2 共 12 种 × 4 工具 = 48 模板）

| 类型 | 中文名 | 适用场景 |
|------|--------|---------|
| `bar` | 柱状图 | 维度对比、同比环比 |
| `line` | 折线图 | 趋势分析、时间序列 |
| `pie` | 饼图 | 占比分析 |
| `pivot` | 透视表 | 多维汇总 |
| `heatmap` | 热力图 | 相关性分析 / 二维矩阵 |
| `waterfall` | 瀑布图 | 利润归因、增减分析 |
| `scatter` | 散点图 | 相关性 / 客户分布 |
| `area` | 面积图 | 累积趋势 |
| `radar` | 雷达图 | 多维评估（部门绩效） |
| `funnel` | 漏斗图 | 销售漏斗 / 转化分析 |
| `gauge` | 仪表盘 | 目标达成度（部分工具用 Donut 模拟） |
| `sankey` | 桑基图 | 流向 / 客户流转（部分工具用堆叠条模拟） |

## 约束

- 图表代码仅基于用户上传的数据集生成，不硬编码数值
- 每次 `/api/visualize` 调用从 viz_templates 表中选最匹配模板
- 代码已做基本错误处理，但需用户在目标工具中实际运行验证
- 输出附"AI 辅助生成，请在目标工具中测试后使用"免责说明
