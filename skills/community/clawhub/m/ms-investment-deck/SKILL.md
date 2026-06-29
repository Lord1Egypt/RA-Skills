---
name: "ms-investment-deck"
description: "生成摩根士丹利风格的投资演示PPTX。当用户需要创建投资演示、路演PPT、投行Pitch Book、投资委员会 memo、股票覆盖启动演示、季度业绩更新演示时调用。适用于CGMA/ACCA/CFA持证人及投行/买方/卖方分析师。"
---

# Morgan Stanley 风格投资演示生成器

## 适用场景

| 场景 | 说明 |
|------|------|
| 首次覆盖启动 | Initiation of Coverage — 公司/行业首次研究报告 |
| 季度业绩更新 | Quarterly Earnings Update — 财报发布后的更新演示 |
| 投资委员会 Memo | Investment Committee Memo — IC 审批材料 |
| 路演演示 | Roadshow / Non-Deal Roadshow — 面向机构投资者 |
| 管理层会议 | Management Meeting Prep — 与公司管理层交流材料 |
| 并购推介 | M&A Pitch Book — 买方/卖方财务顾问材料 |

## 核心能力

本技能可生成 **18 种专业页面类型**，覆盖投行研究演示的全流程：

### 页面类型一览

| # | 页面类型 | 函数 | 说明 |
|---|---------|------|------|
| 1 | 封面页 | `slide_cover()` | 公司名、评级、目标价、行业观点、What's Changed 摘要 |
| 2 | Key Takeaways | `slide_key_takeaways()` | 3-5 条核心要点，金色数字放大 |
| 3 | Section Divider | `slide_section_divider()` | 章节分隔页，深蓝背景 |
| 4 | Content 内容页 | `slide_content()` | 左文右图布局，支持饼图/数据卡片 |
| 5 | Metric Blocks | `slide_metric_blocks()` | KPI 指标块（2x3 网格） |
| 6 | Rating Table | `slide_rating_table()` | 投资评级表格（Ticker/Rating/TP/Company） |
| 7 | Value Chain | `slide_value_chain()` | 产业链/价值链可视化 |
| 8 | What's Changed | `slide_whats_changed()` | 变动追踪（评级/TP/观点变动） |
| 9 | Thesis in Charts | `slide_thesis_in_charts()` | 核心论点图表（2x2 网格） |
| 10 | Shovel Stocks | `slide_shovel_stocks()` | 铲子股/概念股列表 |
| 11 | Market Monitor | `slide_market_monitor()` | 市场监测（四色卡片） |
| 12 | Financial Chart | `slide_financial_chart()` | 财务图表（柱+折线叠加，含预测路径） |
| 13 | Executive Summary | `slide_executive_summary()` | 执行摘要（四象限：论点/TP/风险/催化剂） |
| 14 | Scenario Comparison | `slide_scenario_comparison()` | DCF 情景对比（Bear/Base/Bull） |
| 15 | WACC Breakdown | `slide_wacc_breakdown()` | WACC 拆解表格 |
| 16 | Valuation Bridge | `slide_valuation_bridge()` | 估值桥（从 NOPAT 到 Equity Value） |
| 17 | Sensitivity Heatmap | `slide_sensitivity_heatmap()` | 敏感性热力图（WACC x TGR 矩阵） |
| 18 | Disclosure | `slide_disclosure()` | 免责声明页 |

## 快速开始

### Python API

```python
from ms_investment_deck import make_deck, sample_data

# 使用内置样例数据生成演示文稿
data = sample_data()
make_deck(data, "output/my_deck.pptx", theme="classic", language="zh")

# 自定义数据
my_data = {
    "company_name": "示例公司",
    "title_cn": "投资标题",
    "title_en": "Investment Title",
    "subtitle": "副标题说明",
    "rating": "Overweight",
    "target_price": "$125",
    "current_price": "$98.5",
    "date_str": "2026-06-13",
    "analyst": "张三 · CFA",
    "research_type": "Foundation",
    "key_takeaways": [
        "要点一：核心投资逻辑",
        "要点二：关键数据支撑",
        "要点三：风险提示",
    ],
    "metrics": [
        {"value": "$600B", "unit": "Market Size 2026E", "label": "市场规模"},
        {"value": "+38%", "unit": "YoY", "label": "同比增速"},
    ],
    "content_pages": [
        {
            "title_cn": "行业分析",
            "title_en": "Industry Analysis",
            "body": ["分析正文段落一", "", "分析正文段落二"],
        },
    ],
}
make_deck(my_data, "output/custom.pptx")
```

### CLI

```bash
# 使用内置样例数据生成
python scripts/run.py -o output/demo.pptx

# 指定语言
python scripts/run.py -o output/demo_en.pptx --lang en

# 指定主题
python scripts/run.py -o output/demo.pptx --theme classic
```

## 页面结构

标准演示文稿的页面顺序（数据字段存在时自动插入）：

```
1.  封面页（Cover）                          — 始终生成
2.  What's Changed                            — whats_changed 字段存在时
3.  Key Takeaways                            — key_takeaways 字段存在时
4.  Section Divider: 分析内容                 — content_pages 存在时
5.  Content Pages (x N)                      — 每个内容页
6.  Section Divider: 关键指标                 — metrics 存在时
7.  Metric Blocks                            — KPI 指标块
8.  Financial Chart                         — financial_chart 存在时
9.  WACC Breakdown                           — scenarios 存在时
10. Valuation Bridge                         — scenarios 存在时
11. Sensitivity Heatmap                      — sensitivity 存在时
12. Section Divider: 投资评级总览             — rating_table 存在时
13. Rating Table                             — 评级表格
14. Section Divider: 铲子股清单             — shovel_stocks 存在时
15. Shovel Stocks                            — 铲子股列表
16. Market Monitor                           — market_monitor 存在时
17. Executive Summary                        — executive_summary 存在时
18. Thesis in Charts                         — thesis_charts 存在时
19. Scenario Comparison                      — scenarios 存在时
20. Value Chain                              — value_chain 存在时
21. Disclosure                               — 始终生成
```

## 数据字典

### 顶层字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `company_name` | str | 否 | 公司名称（封面显示） |
| `title_cn` | str | 否 | 中文标题 |
| `title_en` | str | 否 | 英文标题 |
| `subtitle` | str | 否 | 副标题 |
| `rating` | str | 否 | 投资评级：Overweight / Equal-weight / Underweight |
| `target_price` | str | 否 | 目标价，如 "$125" |
| `current_price` | str | 否 | 当前价格，如 "$98.5" |
| `date_str` | str | 否 | 日期字符串 |
| `analyst` | str | 否 | 分析师姓名 |
| `research_type` | str | 否 | 研究类型：Foundation / Update / Flash |
| `industry_view` | str | 否 | 行业观点：Attractive / In-Line / Cautious |
| `disclosure_text` | str | 否 | 自定义免责声明文本 |

### 内容字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `key_takeaways` | List[str] | 3-5 条核心要点 |
| `metrics` | List[dict] | KPI 指标块数组 |
| `content_pages` | List[dict] | 内容页数组 |
| `rating_table` | List[List] 或 List[Dict] | 评级表格 |
| `shovel_stocks` | List[dict] | 铲子股列表 |
| `shovel_stocks_list` | List[dict] | shovel_stocks 别名 |
| `market_monitor` | List[dict] | 市场监测卡片 |
| `financial_chart` | dict | 财务图表数据 |
| `executive_summary` | dict | 执行摘要数据 |
| `scenarios` | dict | DCF 情景数据 |
| `sensitivity` | dict | 敏感性矩阵数据 |
| `whats_changed` | List[dict] | 变动摘要 |
| `thesis_charts` | List[dict] | 核心论点图表 |
| `value_chain` | List[dict] | 产业链数据 |

### metrics 条目格式

```python
{
    "value": "~$600B",       # 核心数字（金色放大）
    "unit": "AI CapEx 2026E", # 单位/时间
    "label": "全球 AI 相关资本开支",  # 说明文字
}
```

### content_pages 条目格式

```python
{
    "title_cn": "中文标题",
    "title_en": "English Title",
    "section_cn": "章节中文名",   # 可选，用于 Section Divider
    "section_en": "Section Name",
    "body": ["段落一", "", "段落二"],  # 空字符串表示换行
    "chart_img": "",             # 图片路径（留空则显示占位卡片）
    "data": {"sectors_allocation": [...]},  # 可选，饼图数据
    "source": "Source: Company Data",
}
```

### rating_table 格式

```python
# List[List] 格式
[
    ["NVDA.O", "Overweight", "$126.5", "NVIDIA", "AI compute 领导者"],
    ["TSM.N",  "Overweight", "$178.2", "Taiwan Semiconductor", "先进制程"],
]

# List[Dict] 格式（自动转换）
[
    {"ticker": "NVDA.O", "rating": "Overweight", "target_price": "$126.5",
     "company": "NVIDIA", "reason": "AI compute 领导者"},
]
```

### shovel_stocks 条目格式

```python
{
    "rank": 1,
    "company": "Aurora Power Co.",
    "ticker": "AUR.N",
    "product": "高压直流输电与数据中心电力模块",
    "analyst": "S. Lee",
    "market_cap_mn": 3200.5,    # 市值（百万）
    "perf_1y_pct": 142.3,       # 一年涨幅（%）
    "rating": "Overweight",      # 可选，触发评级列
}
```

### financial_chart 格式

```python
{
    "years": ["FY22", "FY23", "FY24", "FY25E", "FY26E", "FY27E", "FY28E"],
    "revenue": [1200.0, 1450.0, 1780.0, 2120.0, 2460.0, 2810.0, 3180.0],
    "ebitda":  [280.0, 348.0, 442.0, 550.0, 665.0, 780.0, 910.0],
    "margins": {
        "gross":  [55.0, 56.5, 58.2, 60.0, 61.5, 62.8, 63.9],
        "ebitda": [23.3, 24.0, 24.8, 25.9, 27.0, 27.8, 28.6],
        "net":    [14.2, 15.0, 16.1, 17.0, 17.8, 18.5, 19.1],
    },
    "takeaways": ["要点一", "要点二", "要点三"],
    "title_cn": "收入 / 利润率一览",   # 可选
    "title_en": "Revenue & EBITDA",    # 可选
}
```

### executive_summary 格式

```python
{
    "thesis": "核心投资论点...",
    "tp_and_upside": "TP $125 (+27% upside)...",
    "key_risks": ["风险一", "风险二"],
    "catalysts": ["催化剂一", "催化剂二"],
    "title_cn": "执行摘要",   # 可选
    "title_en": "Executive Summary",  # 可选
}
```

### scenarios 格式（DCF 情景分析）

```python
{
    "bear":  {"label": "Bear",  "wacc": 12.5, "tgr": 1.5, ...},
    "base":  {"label": "Base",  "wacc": 10.0, "tgr": 2.5, ...},
    "bull":  {"label": "Bull",  "wacc": 8.5,  "tgr": 3.5, ...},
}
```

### sensitivity 格式

```python
{
    "wacc_range": [8.0, 9.0, 10.0, 11.0, 12.0, 13.0],
    "tgr_range":  [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0],
    "matrix": [
        [120.0, 135.0, 152.0, 172.0, 198.0, 230.0],
        [110.0, 123.0, 138.0, 155.0, 176.0, 202.0],
        ...
    ],
}
```

### whats_changed 条目格式

```python
{
    "action": "Initiated",       # Initiated / Reiterated / Upgraded / Downgraded
    "ticker": "NVDA.O",
    "company": "NVIDIA Corp",
    "prev_rating": "",
    "new_rating": "Overweight",
    "prev_tp": "",
    "new_tp": "$126.5",
    "reason": "AI compute 需求超预期",
}
```

### thesis_charts 条目格式

```python
{
    "title": "AI CapEx 加速",
    "subtitle": "全球 AI 资本开支（$B）",
    "chart_type": "bar",       # bar / line / pie
    "data": {"labels": [...], "values": [...]},
    "takeaway": "2026E 预计达 $600B",
}
```

### value_chain 条目格式

```python
{
    "stage": "上游",
    "items": [
        {"name": "HBM 内存", "companies": ["SK Hynix", "Samsung"], "share": "45%"},
    ],
}
```

## 主题配色

当前内置 1 套经典主题（classic），采用 Morgan Stanley 品牌色系：

| 色彩 | Hex | 用途 |
|------|-----|------|
| MS Navy | `#0B2C5C` | 主色 / 标题栏 / 章节底色 |
| MS Gold | `#C8A951` | 辅助强调 / 关键数字 |
| OW Green | `#1F7A3E` | Overweight 评级 |
| EW Orange | `#D97706` | Equal-weight 评级 |
| UW Red | `#B91C1C` | Underweight 评级 |
| MS Brand Blue | `#00559F` | 品牌蓝 |
| Chart Blue | `#3B81B9` | 图表主色 |
| Chart Red | `#FB0301` | 图表辅助色 |

## API 参考

### 主入口

```python
make_deck(data: Dict[str, Any], output_path: str,
          theme: str = "classic", language: str = "zh") -> str
```

构建并保存一份 Morgan Stanley 风格的研究演示文稿。所有数据字段均为可选，缺失则跳过对应页面。

**参数：**
- `data` — 结构化数据字典（参见数据字典）
- `output_path` — 输出 .pptx 文件路径
- `theme` — 主题名称（当前支持 "classic"）
- `language` — 语言："zh" / "en" / "bilingual"

**返回：** 成功保存的文件路径

### 示例数据

```python
sample_data() -> Dict[str, Any]
```

返回一份完整的样例数据字典，可直接传入 `make_deck()`。

```python
sample_data_financial() -> Dict[str, Any]
```

返回一份财务图表专用样例数据（`financial_chart` 字段）。

### 公共页面函数

所有 `slide_*` 函数接受一个 `pptx.slide.Slide` 对象作为第一个参数，其余通过关键字参数传入。可直接调用以构建自定义页面序列。

| 函数 | 关键参数 |
|------|---------|
| `slide_cover(slide, *, title_cn, title_en, subtitle, rating, target_price, current_price, company_name, analyst, date_str, research_type, industry_view, whats_changed, language)` | 封面页 |
| `slide_key_takeaways(slide, *, items, language, page_number, total_pages)` | 核心要点 |
| `slide_section_divider(slide, *, title_cn, title_en, category, language)` | 章节分隔 |
| `slide_content(slide, *, title_cn, title_en, body, chart_img, data, source, language, page_number, total_pages)` | 内容页 |
| `slide_metric_blocks(slide, *, metrics, language, page_number, total_pages)` | KPI 指标块 |
| `slide_rating_table(slide, *, rows, language, page_number, total_pages)` | 评级表格 |
| `slide_value_chain(slide, *, data, language, page_number, total_pages)` | 产业链 |
| `slide_whats_changed(slide, *, data, language, page_number, total_pages)` | 变动追踪 |
| `slide_thesis_in_charts(slide, *, data, language, page_number, total_pages)` | 论点图表 |
| `slide_shovel_stocks(slide, *, stocks, language, page_number, total_pages)` | 铲子股列表 |
| `slide_market_monitor(slide, *, blocks, language, page_number, total_pages)` | 市场监测 |
| `slide_disclosure(slide, *, text, language, page_number, total_pages)` | 免责声明 |
| `slide_financial_chart(slide, *, years, revenue, ebitda, margins, takeaways, scenarios, title_cn, title_en, language, page_number, total_pages)` | 财务图表 |
| `slide_executive_summary(slide, *, thesis, tp_and_upside, key_risks, catalysts, title_cn, title_en, language, page_number, total_pages)` | 执行摘要 |
| `slide_scenario_comparison(slide, *, data, theme, language, page_number, total_pages)` | 情景对比 |
| `slide_wacc_breakdown(slide, *, data, theme, language, page_number, total_pages)` | WACC 拆解 |
| `slide_valuation_bridge(slide, *, data, theme, language, page_number, total_pages)` | 估值桥 |
| `slide_sensitivity_heatmap(slide, *, data, theme, language, page_number, total_pages)` | 敏感性热力图 |

## 依赖

| 依赖 | 版本 | 说明 |
|------|------|------|
| Python | >= 3.9 | 运行时 |
| python-pptx | >= 0.6.21 | PPTX 文件生成 |

安装依赖：

```bash
pip install python-pptx
```

## 设计规范

- **比例**：16:9 宽屏（13.333" x 7.5"）
- **字体**：英文 Arial，中文 微软雅黑 / Source Han Sans SC
- **关键数字**：金色放大字号（36-48pt）
- **正文**：13pt，深棕黑色 `#251A1A`
- **页码**：右下角，9pt 灰色
- **标题栏**：深蓝背景 + 白色文字
- **表格**：交替行底色，评级颜色编码

---

**Author**: WANG DONG JIE ([@yjkj999999](https://github.com/yjkj999999) | [Clawhub](https://clawhub.ai/user/yjkj999999))

**Version**: 1.1.0 | **License**: MIT | **Category**: Investment Presentation

> 适用于 CGMA/ACCA/CFA 持证人及投行/买方/卖方分析师。生成符合摩根士丹利品牌标准的投资演示文稿。
