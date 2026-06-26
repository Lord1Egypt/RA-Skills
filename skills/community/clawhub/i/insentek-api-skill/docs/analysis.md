# Analysis Guide — 分析与报告

> Agent 驱动的数据分析策略、报告生成规范、告警检测规则。
> 本文件按需加载，仅在用户提出分析/报告需求时读取。

---

## 1. Analysis Philosophy

分析由 Agent **动态推理**完成，避免硬编码模板。

**推荐流程：**
1. **Parse intent** — 用户到底想知道什么？（相关性、异常、趋势、对比）
2. **Select method** — 根据问题选择合适的统计/数学方法
3. **Compute** — 用 Python 脚本实时计算
4. **Synthesize** — 用自然语言解释，结合领域上下文
5. **Deliver** — 表格、图表、HTML 报告

**语气：** 分析部分使用 SHOULD / RECOMMENDED / PREFER，不强制具体方法。

---

## 2. Common Patterns

| 用户问题 | 推荐方法 | 交付物 |
|---------|---------|--------|
| "分析 X 和 Y 的关系" | Pearson/Spearman 相关 + 散点图 | 相关系数 + 散点图 + 解释 |
| "找出异常数据" | 阈值检测或统计离群点 | 异常列表 + 时间标记 |
| "对比两台设备" | 并排统计 + 差异分析 | 对比表 + 差异高亮 |
| "最近有什么趋势" | 线性回归 / 变化率 | 趋势方向 + 变化率 + 图表 |
| "降雨最多的几天" | 百分位 / 最大值筛选 | 极值列表 + 日期 |
| "数据分布如何" | 直方图 / 分位数 (P10/P50/P90) | 分布图 + 分位数 |
| "昼夜温差多大" | 昼夜分段 + 范围计算 | 昼夜统计对比表 |
| "近一年每日趋势" | 按天聚合 (daily average) | 折线图 + 月度统计 |

**Key Principle:** 输出应直接回答用户问题，而非堆砌统计数据。

---

## 3. Report Generation Guide

### 3.1 流程

```
query_device → resolve sn
query_data → retrieve data
[数据可用性校验] → 见 skill.md 3.2
analyze (statistics, trends, anomalies)
construct HTML (ECharts + CSS)
write_html → return path
```

### 3.2 HTML 结构（RECOMMENDED）

```html
<!-- 最小骨架示例 -->
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
  <style>/* 简洁响应式布局 */ body { font-family: sans-serif; max-width: 960px; margin: 0 auto; } </style>
</head>
<body>
  <h1>设备分析报告</h1>
  <div class="header">
    设备: [别名] (SN: [后4位]) | 类型: [Z/T/J] | 位置: [城市]
    分析时段: [actual_range] | 数据点: [N] 条
  </div>
  <div class="key-findings"><!-- 核心指标卡片 --></div>
  <div class="charts"><!-- ECharts 图表容器 --></div>
  <div class="details"><!-- 详细表格 --></div>
  <div class="conclusion"><!-- 文字总结 --></div>
</body>
</html>
```

### 3.3 时间范围标注规范（MUST）

| 场景 | 标注方式 |
|------|---------|
| 实际 = 请求 | `"分析时段: [范围]"` |
| 实际 < 请求 | `"分析时段: [actual_range]（您请求的 [requested_range] 中，该设备仅有此区间数据）"` |

**绝不允许**用请求范围替代实际范围。

### 3.4 可视化推荐

- **时间序列趋势** → ECharts line chart
- **两变量关系** → ECharts scatter plot
- **多维度对比** → ECharts bar chart 或 radar chart
- **地理分布** → ECharts map (如有位置数据)
- **分布分析** → ECharts histogram 或 box plot

### 3.5 Anti-patterns

- 不要在项目目录中创建 `generate_report_v2.py` 等可复用脚本
- 每个报告应 ad-hoc 生成，用完即删临时脚本
- 不要只放图表不加文字解释

完整报告示例见 `examples/reports.md`。

---

## 4. Alert Detection Rules

数据获取后，自动扫描异常：

| 参数 | 告警条件 | 严重级别 |
|------|---------|---------|
| `moisture` (土壤水分) | < 5% or > 50% | Warning |
| `temperature` (温度) | 1小时内变化 > 10°C | Critical |
| `battery` (电池电压) | < 3.0V | Critical |
| `ec` (电导率) | < 0 or > 20 | Warning |
| `laserliquidLevel` (激光液位) | < 0 | Warning |

**输出格式：**
```
⚠️ 异常数据检测
- [参数名] 在 [节点] [时间]: [值] [单位] — [异常描述]
```

---

## 5. Multi-Industry Parameters

设备类型决定显示参数的中文名：

| 类型码 | 行业 | 关键参数 |
|--------|------|---------|
| `Z` | 农业 / 土壤监测 | moisture, temperature, ec |
| `T` | 气象 / 气象站 | airTemperature, relativeHumidity, rainfall, wind... |
| `J` | 工业 / 液位监测 | laserliquidLevel, battery |

通过 `/v3/device/{sn}/description` 获取参数中文名，优先用中文展示。

完整参数参考见 `reference/api-doc.md`。
