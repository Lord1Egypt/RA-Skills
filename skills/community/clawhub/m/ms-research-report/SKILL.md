---
name: "ms-research-report"
description: "生成摩根士丹利风格的股票研究报告Word文档。当用户需要创建卖方研究报告、买方投资备忘录、行业深度报告、股票首次覆盖报告、季度业绩点评、估值深度分析时调用。适用于CGMA/ACCA/CFA持证人及卖方/买方分析师、基金经理。"
---

# Morgan Stanley 风格研究报告生成器

## 适用场景

| 报告类型 | 典型用途 | 关键章节 |
|---------|---------|---------|
| **首次覆盖报告** (Initiation) | 新覆盖公司首份深度报告 | 全部章节 + DCF 估值 |
| **季度业绩点评** (Earnings Update) | 财报发布后快速更新 | 执行摘要 + KPI + 财务表 + 评级表 |
| **行业深度报告** (Industry Deep Dive) | 子行业/赛道全景分析 | 产业链 + 铲子股 + 情景分析 |
| **买方投资备忘录** (Buy-side Memo) | PM/IC 会议前简报 | 论点图表 + 估值桥 + 敏感性 |
| **估值专题** (Valuation Deep Dive) | DCF / SOTP / 可比公司深度 | WACC + 敏感性 + 可比公司 + 估值桥 |
| **管理层会前简报** (Pre-meeting Brief) | 路演/管理层会议准备 | 论点图表 + 关键问题 + 风险 |

## 核心能力

### 完整报告结构（17 个标准章节）

本生成器按照 Morgan Stanley 卖方研究报告标准模板，按以下顺序渲染全部章节（缺失数据字段自动跳过）：

1. **封面页** -- 公司名 / 分析师 / 评级 / 目标价 / 日期 / 研究类型
2. **目录** -- 自动生成章节导航
3. **Our Thesis in N Charts** -- 论点图表摘要（含 KPI 卡片）
4. **执行摘要** -- 投资论点 + 目标价 + 风险 + 催化剂 + Key Takeaways
5. **正文章节** -- 自定义多级章节（支持子章节、要点列表）
6. **KPI 指标块** -- TAM / CAGR / Upside 等核心指标卡片
7. **财务数据表** -- 收入 / 利润率 / EBITDA / CAPEX / EPS（支持 YoY 自动计算）
8. **财务图表** -- 收入&EBITDA 双柱图 + 利润率折线图 + 行业配置饼图
9. **评级表格** -- Ticker / Rating / Last Close / Company / Reason
10. **60 铲子股列表** -- 排名 / 公司 / 产品 / 分析师 / 市值 / 年度涨幅
11. **产业链/价值链** -- 上中下游结构化展示
12. **铲子股详细列表** -- 含推荐逻辑的详细铲子股表格
13. **情景对比分析** -- Bear / Base / Bull 三情景财务对比
14. **WACC 拆解** -- 权益成本 / 债务成本 / 资本结构（含堆叠柱状图）
15. **敏感性分析矩阵** -- 双变量敏感性表格（含交叉高亮）
16. **可比公司分析** -- EV/Revenue / EV/EBITDA / P/E 等多维度对比
17. **估值桥（Waterfall）** -- 当前价到目标价的归因拆解（含瀑布图）
18. **Exhibit 附录图表** -- 自定义图表页
19. **附录** -- 方法论 / 假设 / 免责声明
20. **免责声明** -- 法律披露文本

### 出版级图表系统

基于 matplotlib 的出版级图表渲染引擎：

- **DPI 300** 高清输出
- **MS 8色调色板**：Deep Navy / Medium Blue / Gold / Green / Orange / Red / Purple / Light Blue
- **4 种图表类型**：
  - `bar` -- 收入&EBITDA 双柱对比图（含均值参考线 + 数值标签）
  - `line` -- 毛利率/EBITDA利润率/净利率折线图（含面积填充 + 数据标签）
  - `pie` -- 行业配置饼图（含最大扇区突出 + 图例）
  - `waterfall` -- 估值桥梁图（当前价 -> 目标价归因拆解，含连接线）
- **Source 水印**：每张图表底部自动添加 "Source: Morgan Stanley Research"
- **降级机制**：matplotlib 未安装时自动降级为文字占位

### Exhibit 自动编号

全局 Exhibit 计数器，按渲染顺序自动编号：

- 格式：`Exhibit 1: 标题` / `Exhibit 2: 标题` ...
- 覆盖：财务图表、WACC 图表、估值桥图表、附录图表
- 每次调用 `make_report()` 自动重置

### 品牌主题系统

| 主题 | 主色 | 辅助色 | 风格 |
|------|------|--------|------|
| **classic** | `#0B2C5C` 深蓝 | `#C8A951` 金色 | MS 传统深蓝+金 |

颜色体系包含 30+ 语义化颜色常量，覆盖：
- 品牌色（navy / gold / brand_blue）
- 评级色（OW 绿 / EW 橙 / UW 红）
- DCF 语义色（输入假设黄 / 计算行绿 / 汇总行蓝紫 / CapEx 橙）
- 情景色（Bear 棕橙 / Base 深绿 / Bull 深蓝）
- 图表色（8 色调色板）

### 多语言支持

- `zh` -- 中文报告（章节标题中文）
- `en` -- 英文报告（章节标题英文）
- `bilingual` -- 双语报告（章节标题中英双语）

## 快速开始

### Python API

```python
from ms_research_report import make_report

data = {
    "company_name": "极光资本控股",
    "title_cn": "为下一个10倍科技周期，资本是瓶颈吗？",
    "title_en": "Financing the Next 10x Tech Cycle",
    "subtitle": "关键论点一句话：算力军备竞赛将重塑上游资本开支结构。",
    "rating": "Overweight",
    "target_price": 125.0,
    "current_price": 98.5,
    "date_str": "2026-06-12",
    "analyst": "陈嘉怡 CFA",
    "research_type": "Foundation",
    "currency": "USD",
    "key_takeaways": [
        "算力需求在未来三年预计以 35% CAGR 扩张。",
        "上游芯片与光模块厂商最受益。",
        "估值溢价将集中于具备专有硅片与供应渠道的企业。",
    ],
    "executive_summary": {
        "thesis": ["论点1", "论点2", "论点3"],
        "tp_and_upside": ["目标价 $125.0，上行 +27%。"],
        "risks": ["风险1", "风险2"],
        "catalysts": ["催化剂1", "催化剂2"],
    },
    "sections": [
        {
            "title_cn": "一、算力需求：结构性扩张",
            "title_en": "I. Compute Demand",
            "paragraphs": ["段落1", "段落2"],
            "subsections": [
                {"title": "1.1 子章节", "paragraphs": ["子段落1"]},
            ],
        },
    ],
    "metrics": [
        {"value": "$5.2T", "unit": "TAM 2026E", "label": "市场规模"},
        {"value": "35%", "unit": "CAGR '24-'28", "label": "复合增长"},
    ],
    "financial_table": {
        "headers": ["指标", "FY24", "FY25E", "FY26E", "FY27E"],
        "rows": [
            ["营业收入 ($M)", "4,810", "5,230", "5,750", "6,520"],
            ["毛利率 (%)", "52.1", "54.0", "55.5", "56.8"],
            ["EBITDA ($M)", "1,210", "1,405", "1,580", "1,820"],
        ],
        "highlight_rows": [3],
        "auto_yoy": True,
        "source": "Source: Morgan Stanley Research.",
    },
    "rating_table": [
        ["Ticker", "Rating", "Last Close", "Company", "Reason"],
        ["NVDA.O", "OW", "198.35", "Nvidia", "AI compute leader"],
    ],
}

make_report(data, "output/report.docx", theme="classic", language="zh")
```

### CLI

```bash
# 使用内置示例数据生成报告
python scripts/run.py -o output/test_report.docx

# 使用自定义 JSON 数据文件
python scripts/run.py -o output/my_report.docx -d data.json
```

## 报告结构

标准报告的章节渲染顺序（缺失数据自动跳过）：

```
封面页 (Cover Page)
  |
目录 (Table of Contents)
  |
Our Thesis in N Charts [可选]
  |
执行摘要 (Executive Summary)
  |
正文章节 (Sections) x N
  |
KPI 指标块 (Key Metrics)
  |
财务数据表 (Financial Table)
  |
财务图表 (Financial Charts) [可选，需 matplotlib]
  |
评级表格 (Rating Table)
  |
60 铲子股列表 (Shovel Stocks)
  |
产业链/价值链 (Value Chain) [可选]
  |
铲子股详细列表 (Shovel Stocks List) [可选]
  |
情景对比分析 (Scenario Comparison) [可选]
  |
WACC 拆解 (WACC Breakdown) [可选]
  |
敏感性分析矩阵 (Sensitivity Analysis) [可选]
  |
可比公司分析 (Comparable Companies) [可选]
  |
估值桥 (Valuation Bridge / Waterfall) [可选]
  |
Exhibit 附录图表 [可选]
  |
附录 (Appendix)
  |
免责声明 (Disclosure)
```

## 数据字典

### 顶层字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `company_name` | str | 否 | 公司名称（封面） |
| `title_cn` | str | 推荐* | 中文标题（封面） |
| `title_en` | str | 推荐* | 英文标题（封面） |
| `subtitle` | str | 否 | 副标题/一句话论点 |
| `rating` | str | 否 | 评级：Overweight / Equal-weight / Underweight |
| `target_price` | float | 否 | 目标价 |
| `current_price` | float | 否 | 当前价格 |
| `date_str` | str | 否 | 报告日期（YYYY-MM-DD） |
| `analyst` | str | 否 | 分析师姓名 |
| `analyst_title` | str | 否 | 分析师头衔 |
| `analyst_email` | str | 否 | 分析师邮箱 |
| `industry` | str | 否 | 行业名称 |
| `entity` | str | 否 | 实体/部门名称 |
| `research_type` | str | 否 | 研究类型：Foundation / Update / Flash |
| `currency` | str | 否 | 货币单位（默认 USD） |
| `language` | str | 否 | 语言：zh / en / bilingual |

> *`title_cn` 和 `title_en` 至少提供一个。

### 执行摘要

| 字段 | 类型 | 说明 |
|------|------|------|
| `key_takeaways` | list[str] | Key Takeaways 要点列表 |
| `executive_summary.thesis` | list[str] | 投资论点 |
| `executive_summary.tp_and_upside` | list[str] | 目标价与上行空间 |
| `executive_summary.risks` | list[str] | 风险因素 |
| `executive_summary.catalysts` | list[str] | 催化剂 |

### 正文章节

| 字段 | 类型 | 说明 |
|------|------|------|
| `sections` | list[dict] | 章节列表 |
| `sections[].title_cn` | str | 中文标题 |
| `sections[].title_en` | str | 英文标题 |
| `sections[].paragraphs` | list[str] | 段落文本（支持 `•` 要点） |
| `sections[].subsections` | list[dict] | 子章节（同结构） |

### KPI 指标

| 字段 | 类型 | 说明 |
|------|------|------|
| `metrics` | list[dict] | KPI 卡片列表 |
| `metrics[].value` | str | 指标值（如 "$5.2T"） |
| `metrics[].unit` | str | 单位（如 "TAM 2026E"） |
| `metrics[].label` | str | 标签（如 "市场规模"） |

### 财务数据表

| 字段 | 类型 | 说明 |
|------|------|------|
| `financial_table.headers` | list[str] | 表头（指标 + 年份） |
| `financial_table.rows` | list[list] | 数据行 |
| `financial_table.highlight_rows` | list[int] | 需高亮的行索引（0-based） |
| `financial_table.auto_yoy` | bool | 是否自动计算 YoY 变化 |
| `financial_table.source` | str | 数据来源注释 |

### 评级表格

| 字段 | 类型 | 说明 |
|------|------|------|
| `rating_table` | list[list] | 二维表格，首行为表头 |

### 铲子股

| 字段 | 类型 | 说明 |
|------|------|------|
| `shovel_stocks` | list[dict] | 铲子股列表 |
| `shovel_stocks[].rank` | int | 排名 |
| `shovel_stocks[].company` | str | 公司名称 |
| `shovel_stocks[].ticker` | str | 股票代码 |
| `shovel_stocks[].product` | str | 产品/服务 |
| `shovel_stocks[].analyst` | str | 覆盖分析师 |
| `shovel_stocks[].market_cap_mn` | float | 市值（百万） |
| `shovel_stocks[].perf_1y_pct` | float | 年度涨幅（%） |

### 财务图表

| 字段 | 类型 | 说明 |
|------|------|------|
| `financial_chart.labels` | list[str] | 年份标签 |
| `financial_chart.revenue` | list[float] | 收入数据 |
| `financial_chart.ebitda` | list[float] | EBITDA 数据 |
| `financial_chart.gross_margin` | list[float] | 毛利率 |
| `financial_chart.ebitda_margin` | list[float] | EBITDA 利润率 |
| `financial_chart.net_margin` | list[float] | 净利率 |

### 行业配置

| 字段 | 类型 | 说明 |
|------|------|------|
| `sectors_allocation.title` | str | 标题 |
| `sectors_allocation.labels` | list[str] | 行业标签 |
| `sectors_allocation.values` | list[float] | 配置比例 |

### 论点图表

| 字段 | 类型 | 说明 |
|------|------|------|
| `thesis_charts` | list[dict] | 论点图表列表 |
| `thesis_charts[].title` | str | 图表标题 |
| `thesis_charts[].type` | str | 图表类型（bar/line/pie/waterfall） |
| `thesis_charts[].kpi_cards` | list[dict] | KPI 卡片 |
| `thesis_charts[].kpi_cards[].value` | str | 卡片值 |
| `thesis_charts[].kpi_cards[].label` | str | 卡片标签 |

### 产业链/价值链

| 字段 | 类型 | 说明 |
|------|------|------|
| `value_chain.title` | str | 标题 |
| `value_chain.layers` | list[dict] | 产业链层级 |
| `value_chain.layers[].name` | str | 层级名称 |
| `value_chain.layers[].items` | list[str] | 层级内项目 |

### DCF 章节

| 字段 | 类型 | 说明 |
|------|------|------|
| `scenario_comparison` | dict | Bear/Base/Bull 情景数据 |
| `wacc` | dict | WACC 拆解数据 |
| `sensitivity` | dict | 敏感性分析矩阵数据 |
| `comps` | dict | 可比公司数据 |
| `valuation_bridge` | dict | 估值桥数据 |

### 附录与披露

| 字段 | 类型 | 说明 |
|------|------|------|
| `exhibits` | list[dict] | Exhibit 图表列表 |
| `exhibits[].image_path` | str | 图片路径 |
| `exhibits[].title` | str | 图表标题 |
| `appendix.content` | str | 附录内容 |
| `disclosure.text` | str | 免责声明文本 |

## 图表系统

### MS 8 色调色板

```python
MS_PALETTE = [
    '#1F3864',  # Deep Navy    -- 主色
    '#2E75B6',  # Medium Blue  -- 辅色
    '#C8A951',  # Gold         -- 强调
    '#00AF50',  # Green        -- 正面
    '#E37C2B',  # Orange       -- 中性
    '#B91C1C',  # Red          -- 负面
    '#6B4C9A',  # Purple       -- 辅助
    '#4A90D9',  # Light Blue   -- 辅助
]
```

### 图表类型与数据格式

**bar（双柱对比图）**
```python
{"type": "bar", "title": "Revenue vs EBITDA",
 "labels": ["FY24", "FY25E", "FY26E"],
 "revenue": [4810, 5230, 5750],
 "ebitda": [1210, 1405, 1580]}
```

**line（利润率折线图）**
```python
{"type": "line", "title": "Margin Trends",
 "labels": ["FY24", "FY25E", "FY26E"],
 "gross_margin": [52.1, 54.0, 55.5],
 "ebitda_margin": [25.2, 26.9, 27.5],
 "net_margin": [18.5, 19.8, 21.0]}
```

**pie（行业配置饼图）**
```python
{"type": "pie", "title": "Sector Allocation",
 "labels": ["半导体", "光模块", "IDC"],
 "values": [40.0, 25.0, 10.0]}
```

**waterfall（估值桥瀑布图）**
```python
{"type": "waterfall", "title": "Valuation Bridge",
 "labels": ["Base Business", "Growth", "Multiple Expansion", "FX"],
 "values": [15.0, 8.5, 3.0, 0.0],
 "current": 98.5, "target": 125.0}
```

### 出版级样式配置

- DPI: 300（屏幕与打印均清晰）
- 字体: Noto Sans CJK SC / DejaVu Sans / Arial
- 网格: 虚线，浅灰 `#E8E8E8`
- 坐标轴: 隐藏上/右边框，保留左/下
- 数值标签: 自动添加在柱顶/数据点旁
- Source 水印: 每张图表底部

## Exhibit 编号

Exhibit 编号系统使用全局计数器，按渲染顺序自动递增：

```
Exhibit 1: 收入与 EBITDA 对比
Exhibit 2: 利润率趋势
Exhibit 3: 行业配置
Exhibit 4: WACC 拆解
Exhibit 5: 估值桥
Exhibit 6: [附录图表标题]
```

- 每次调用 `make_report()` 时计数器自动重置为 1
- 编号函数：`_next_exhibit_label(title)` -> `"Exhibit N: title"`
- Source 行自动追加：`"Source: Morgan Stanley Research"`

## 主题配色

当前支持 1 套主题，颜色体系包含 30+ 语义化常量：

| 颜色类别 | 色值 | 用途 |
|---------|------|------|
| MS Navy | `#0B2C5C` | 品牌主色、封面背景 |
| MS Gold | `#C8A951` | 强调色、分隔线 |
| Brand Blue | `#00559F` | 标题强调 |
| OW Green | `#1F7A3E` | Overweight 评级 |
| EW Orange | `#D97706` | Equal-weight 评级 |
| UW Red | `#B91C1C` | Underweight 评级 |
| Deep Navy | `#1F3864` | DCF 主标题背景 |
| Medium Blue | `#2E75B6` | DCF 表头背景 |
| Input BG | `#FFF2CC` | 输入假设行背景 |
| Calc BG | `#E2EFDA` | 关键计算行背景 |
| Summary BG | `#D9E1F2` | 汇总行背景 |
| CapEx BG | `#FCE4D6` | CapEx 行背景 |

## API 参考

### `make_report(data, output_path, theme, language)`

主入口函数，生成完整的 MS 风格研究报告 DOCX。

```python
def make_report(
    data: Dict[str, Any],       # 报告数据字典（所有字段可选）
    output_path: str,           # 输出 .docx 文件路径（需确保父目录存在）
    theme: str = "classic",     # 主题名称（当前仅支持 "classic"）
    language: str = "zh",       # 语言：zh / en / bilingual
) -> str:                       # 返回 output_path
```

**参数说明：**
- `data` -- 完整数据字典，字段均为可选。缺失字段对应章节自动跳过。
- `output_path` -- 输出路径。**调用者需确保父目录已存在**。
- `theme` -- 主题名称，默认 `"classic"`（深蓝+金）。
- `language` -- 语言设置，默认 `"zh"`。章节标题按语言显示。

**返回值：** 写入成功后返回 `output_path`。

### 内部函数（60+ 个）

核心渲染函数（供高级用户扩展参考）：

| 函数 | 功能 |
|------|------|
| `_cover_page(doc, data, colors)` | 封面页 |
| `_toc_page(doc, data, colors)` | 目录页 |
| `_thesis_charts_section(doc, data, colors, paths)` | 论点图表 |
| `_executive_summary(doc, data, colors)` | 执行摘要 |
| `_section(doc, section, colors, ...)` | 正文章节 |
| `_kpi_blocks(doc, data, colors)` | KPI 指标块 |
| `_financial_table(doc, data, colors)` | 财务数据表 |
| `_rating_table(doc, data, colors)` | 评级表格 |
| `_shovel_stocks(doc, data, colors)` | 铲子股列表 |
| `_value_chain_section(doc, data, colors)` | 产业链 |
| `_shovel_stocks_list(doc, data, colors)` | 铲子股详细列表 |
| `_scenario_comparison_section(doc, data, colors, lang)` | 情景对比 |
| `_wacc_section(doc, data, colors, lang)` | WACC 拆解 |
| `_sensitivity_section(doc, data, colors, lang)` | 敏感性分析 |
| `_comps_section(doc, data, colors, lang)` | 可比公司 |
| `_valuation_bridge_section(doc, data, colors, lang)` | 估值桥 |
| `_exhibits_section(doc, data, colors)` | Exhibit 附录 |
| `_appendix(doc, data, colors)` | 附录 |
| `_disclosure(doc, data, colors)` | 免责声明 |
| `_add_chart_image(doc, chart_data, colors, width)` | 图表渲染+嵌入 |

## 依赖

| 包 | 版本要求 | 用途 |
|----|---------|------|
| `python-docx` | >= 0.8.11 | DOCX 文件生成（必需） |
| `matplotlib` | >= 3.5 | 出版级图表渲染（可选，缺失时降级） |
| Python | >= 3.9 | 类型注解支持 |

安装依赖：

```bash
pip install python-docx>=0.8.11 matplotlib>=3.5
```

## 示例输出

`scripts/_sample_out/` 目录包含 3 份示例报告：

- `achp_report_zh.docx` -- 中文版
- `achp_report_en.docx` -- 英文版
- `achp_report_bilingual.docx` -- 双语版

## 文件结构

```
ms-research-report/
  SKILL.md                          # 本文档
  scripts/
    ms_research_report.py           # 核心生成模块（~3600 行）
    run.py                           # CLI 入口
    _sample_out/                     # 示例输出
      achp_report_zh.docx
      achp_report_en.docx
      achp_report_bilingual.docx
  output/                            # 默认输出目录
```

---

**Author**: WANG DONG JIE ([@yjkj999999](https://github.com/yjkj999999) | [Clawhub](https://clawhub.ai/user/yjkj999999))

**Version**: 1.1.0 | **License**: MIT | **Category**: Equity Research

> 适用于 CGMA/ACCA/CFA 持证人及卖方/买方分析师、基金经理。生成符合摩根士丹利出版标准的股票研究报告。
