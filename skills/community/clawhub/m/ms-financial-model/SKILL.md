---
name: "ms-financial-model"
description: "生成摩根士丹利风格的DCF/SOTP投资级财务模型Excel。当用户需要创建财务模型、DCF估值、SOTP分部估值、敏感性分析、PE Band分析、可比公司分析时调用。适用于CGMA/ACCA/CPA/CFA持证人及200万全球专业会员。"
---

# Morgan Stanley 风格财务模型生成器

## 适用场景

| 场景 | 说明 | 典型输出 |
|------|------|----------|
| 首次覆盖 (Initiation) | 卖方研究团队首次覆盖标的，需完整 DCF + SOTP + Comps | 全套 12+ Sheet 投资级模型 |
| 季度业绩更新 (Earnings Update) | 财报季后更新预测假设与估值结论 | 更新 Forecast + Sensitivity |
| 并购估值 (M&A Valuation) | 收购方/财务顾问对目标公司进行独立估值 | Bear/Base/Bull 三情景 DCF + SOTP |
| IPO 定价 (IPO Pricing) | 承销商对拟上市公司进行估值锚定 | DCF + PE Band + Comps 多维交叉验证 |
| 内部审议 (Internal Review) | 投资委员会/风控委员会审议项目 | 敏感性矩阵 + 情景对比摘要 |
| 压力测试 (Stress Test) | 风险管理团队进行极端情景模拟 | WACC/TGR 双维敏感性矩阵 |

## 核心能力

### 1. 三情景 DCF 估值模型 (Bear / Base / Bull)
- 按 **业务分部** (Segment) 逐行预测收入，支持 9 个独立分部
- 每个分部独立设置 FY25 基数 + 5 年复合增长率 (CAGR)
- EBITDA Margin 逐年递进，支持利润率扩张/收缩假设
- UFCF 完整拆解：EBITDA → D&A → EBIT → Tax → NOPAT → CapEx → ΔNWC → UFCF
- Terminal Value 双重计算：Gordon Growth Model + Exit Multiple Method
- Equity Bridge：EV → Net Debt → Equity Value → Per Share

### 2. WACC 加权平均资本成本拆解
- CAPM 驱动的 Cost of Equity：Rf + Beta x ERP + Size Premium + Country Risk
- Cost of Debt 税后调整
- 可自定义 E/D 权重结构
- 公式驱动（非硬编码），修改假设后自动联动

### 3. 敏感性分析矩阵 (4 组)
| 矩阵 | X 轴 | Y 轴 | 输出 |
|------|------|------|------|
| WACC x TGR → Implied EV | Terminal Growth Rate (2.0%~4.0%) | WACC (8%~14%) | Enterprise Value |
| WACC x Exit Multiple → Implied EV | Exit Multiple (6x~18x) | WACC (8%~14%) | Enterprise Value |
| WACC x TGR → Implied PPS | Terminal Growth Rate | WACC | Price Per Share |
| Scenario Comparison | Bear / Base / Bull | Key Metrics | 三情景对比摘要 |

- 基准情景交叉点黄色高亮 (Cross-highlight)
- 每个单元格均为 Excel 公式，支持实时联动

### 4. SOTP 分部估值 (Sum-of-the-Parts)
- 按业务分部独立估值，支持 EV/EBITDA 和 EV/Revenue 两种方法
- 每个分部可设置不同估值倍数和方法
- Corporate-level 调整：Net Debt、Minority Interest
- 饼图可视化各分部 EV 占比

### 5. PE Band 历史估值区间
- 3~5 年 PE 历史轨迹（High / Low / Close）
- 中位数 (Median) 标注线
- 当前 PE vs Forward PE 对比
- 面积图可视化历史估值区间

### 6. 可比公司分析 (Comparable Companies)
- 多市场分组：US / HK (港股) / A (A股)
- 每组独立计算中位数 (Median)
- 估值指标：EV/Revenue LTM & NTM、EV/EBITDA LTM & NTM、3Y CAGR
- 支持备注 (Note) 字段标注可比逻辑

### 7. 运营 KPI 仪表板
- 交付量、用户数、发射次数、订阅数等多维运营指标
- 历史 (Historical) + 预测 (Forecast) 并列展示
- 支持自定义单位 (K units / M / Times)

### 8. 出版级图表 (5 种)
| 图表类型 | 数据源 | 说明 |
|----------|--------|------|
| Revenue & EBITDA 双柱图 | DCF Sheet | 收入与 EBITDA 并列柱状对比 |
| EBITDA Margin 折线图 | DCF Sheet | 利润率趋势折线 |
| SOTP 饼图 | SOTP Sheet | 各分部 EV 占比 |
| PE Band 面积图 | PE Band Sheet | 历史估值区间面积 |

## 快速开始

### Python API 调用

```python
from ms_financial_model import make_financial_model, sample_data

# 使用内置示例数据快速生成
data = sample_data()
output = make_financial_model(data, "output/my_model.xlsx", theme="classic", language="zh")
print(f"模型已生成: {output}")

# 使用自定义数据
my_data = {
    "company_name": "My Corp",
    "ticker": "MYCO",
    "report_date": "2026-06-13",
    "analyst": "Research Team",
    "currency": "USD",
    "shares_outstanding": 500,
    "historical": {
        "years": ["FY22A", "FY23A", "FY24A", "FY25A"],
        "revenue": [3000, 4000, 5500, 7000],
        "ebitda": [450, 640, 935, 1260],
    },
    "forecast_years": ["FY26E", "FY27E", "FY28E", "FY29E", "FY30E"],
    "scenarios": {
        "base": {
            "label_zh": "基准情景",
            "label_en": "Base Case",
            "core_assumptions": "Steady growth",
            "ebitda_margin": [0.20, 0.21, 0.22, 0.23, 0.24],
            "da_pct_revenue": 0.035,
            "capex_pct_revenue": 0.055,
            "nwc_pct_rev_change": 0.08,
            "tax_rate": 0.21,
            "wacc": {
                "rf": 0.044, "erp": 0.055, "beta": 1.5,
                "size_premium": 0.003, "country_risk": 0.0,
                "kd": 0.055, "tax_rate": 0.21,
                "e_weight": 0.92, "d_weight": 0.08,
            },
            "terminal_growth_rate": 0.03,
            "exit_multiple_ebitda": 12.0,
            "net_debt": 2000,
        },
        "bear": { ... },
        "bull": { ... },
    },
}
output = make_financial_model(my_data, "output/custom_model.xlsx")
```

### CLI 命令行

```bash
# 使用示例数据生成中文模型
python scripts/run.py output/model_zh.xlsx

# 生成英文模型
python scripts/run.py output/model_en.xlsx --lang en

# 指定主题
python scripts/run.py output/model.xlsx --theme classic
```

## 输出结构

生成的 `.xlsx` 文件包含以下 Sheet（按顺序）：

| # | Sheet 名称 | 内容 |
|---|-----------|------|
| 1 | Cover | 封面：公司概览、业务分部摘要、情景估值对比、投资要点 |
| 2 | DCF - Bear Case | 熊市情景 DCF：收入预测 → UFCF → Terminal Value → Equity Value |
| 3 | DCF - Base Case | 基准情景 DCF（同上结构） |
| 4 | DCF - Bull Case | 牛市情景 DCF（同上结构） |
| 5 | WACC | 加权平均资本成本拆解（公式驱动） |
| 6 | Sensitivity | 4 组敏感性分析矩阵 |
| 7 | SOTP | 分部估值（Sum-of-the-Parts） |
| 8 | KPIs | 运营关键指标仪表板 |
| 9 | PE Band | 历史市盈率区间分析 |
| 10 | Comps | 可比公司分析（多市场分组） |

## 数据字典

### 必选字段 (Required)

| 字段 | 类型 | 说明 |
|------|------|------|
| `company_name` | `str` | 公司名称 |
| `ticker` | `str` | 股票代码 |
| `report_date` | `str` | 报告日期 (YYYY-MM-DD) |
| `currency` | `str` | 货币代码 (USD/CNY/HKD/EUR) |
| `shares_outstanding` | `float` | 流通股数（百万） |
| `historical` | `dict` | 历史财务数据（见下） |
| `forecast_years` | `list[str]` | 预测年份标签，如 `["FY26E", "FY27E", ...]` |
| `scenarios` | `dict` | 三情景数据 (bear/base/bull) |

### historical 子结构

```python
"historical": {
    "years": ["FY21A", "FY22A", "FY23A", "FY24A", "FY25A"],  # 历史年份标签
    "revenue": [5300, 7800, 11200, 15600, 20000],             # 收入 (百万)
    "ebitda": [530, 1014, 1680, 2500, 3600],                  # EBITDA (百万)
}
```

### scenarios 子结构（每个情景）

```python
"scenarios": {
    "bear": {
        "label_zh": "熊市情景",          # 中文标签
        "label_en": "Bear Case",         # 英文标签
        "core_assumptions": "...",        # 核心假设描述
        "ebitda_margin": [0.18, 0.19, 0.19, 0.20, 0.20],  # 5年 EBITDA 利润率
        "da_pct_revenue": 0.045,          # D&A 占收入比
        "capex_pct_revenue": 0.07,        # CapEx 占收入比
        "nwc_pct_rev_change": 0.12,       # ΔNWC 占收入变动比
        "tax_rate": 0.21,                 # 企业所得税率
        "wacc": {                         # WACC 参数
            "rf": 0.044,                  # 无风险利率
            "erp": 0.055,                 # 股权风险溢价
            "beta": 1.80,                 # Beta 系数
            "size_premium": 0.005,         # 规模溢价
            "country_risk": 0.0,           # 国家风险溢价
            "kd": 0.065,                  # 债务成本
            "tax_rate": 0.21,             # 债务税盾税率
            "e_weight": 0.90,              # 权重占比
            "d_weight": 0.10,              # 债务占比
        },
        "terminal_growth_rate": 0.020,    # 永续增长率
        "exit_multiple_ebitda": 8.0,       # 退出 EBITDA 倍数
        "net_debt": 5000,                  # 净债务 (百万)
    },
    "base": { ... },
    "bull": { ... },
}
```

### 可选字段 (Optional)

| 字段 | 类型 | 说明 | 触发模块 |
|------|------|------|----------|
| `analyst` | `str` | 分析师/机构名称 | Cover |
| `business_overview` | `list[dict]` | 业务分部概览 `[{name, description, revenue_estimate}]` | Cover |
| `historical.segments` | `dict` | 分部历史收入 `{segment_name: {revenue: [...]}}` | DCF |
| `scenarios.*.segments` | `dict` | 分部预测 `{segment_name: {fy25_base, growth_rates}}` | DCF |
| `comparable_companies` | `list[dict]` | 可比公司列表（见下） | Comps |
| `sotp` | `dict` | SOTP 分部估值数据（见下） | SOTP |
| `operational_kpis` | `dict` | 运营 KPI 数据（见下） | KPIs |
| `pe_band` | `dict` | PE Band 数据（见下） | PE Band |
| `cover_subtitle` | `str` | 封面副标题 | Cover |
| `key_takeaways` | `list[str]` | 关键要点列表 | Cover |
| `investment_thesis` | `str` | 投资逻辑摘要 | Cover |
| `risk_factors` | `list[str]` | 风险因素列表 | Cover |

### comparable_companies 子结构

```python
"comparable_companies": [
    {
        "name": "Tesla", "ticker": "TSLA", "market": "US",
        "mcap": 800000, "ev": 750000,
        "ev_rev_ltm": 5.2, "ev_rev_ntm": 4.8,
        "ev_ebitda_ltm": 25.0, "ev_ebitda_ntm": 20.0,
        "cagr_3y": 0.35, "note": "Closest comp",
    },
    # market 字段: "US" / "HK" / "A" 用于分组
]
```

### sotp 子结构

```python
"sotp": {
    "segments": [
        {
            "name": "Tesla Auto",
            "revenue_ltm": 77000, "ebitda_ltm": 15400,
            "ev_multiple": 8.0, "ev": 123200,
            "method": "EV/EBITDA", "note": "Comparable median",
        },
    ],
    "net_debt": -28000,
    "minority_interest": 0,
    "shares_outstanding": 3200,
}
```

### operational_kpis 子结构

```python
"operational_kpis": {
    "metrics": [
        {
            "name": "Tesla Deliveries",
            "unit": "K units",
            "historical": [1310, 1390, 1810, 1636, 1790],
            "forecast": [2000, 2200, 2400, 2600, 2800],
        },
    ],
}
```

### pe_band 子结构

```python
"pe_band": {
    "current_pe": 35.0,
    "forward_pe": 28.0,
    "median_pe": 55.0,
    "pe_history": [
        {"period": "FY2021", "high": 120, "low": 45, "close": 95, "eps": 2.5},
    ],
}
```

## 主题配色

| 主题 | 说明 |
|------|------|
| `classic` | 摩根士丹利经典深蓝 (Deep Navy #1F3864) + 金色点缀 |

> 当前版本默认使用 `classic` 主题。更多主题（如 `dark`, `light`, `print`）将在后续版本中扩展。

## 语言支持

| 语言代码 | 说明 | 影响范围 |
|----------|------|----------|
| `zh` | 简体中文（默认） | 所有 Sheet 标题、标签、注释 |
| `en` | 英文 | 所有 Sheet 标题、标签、注释 |

通过 `t(key, lang)` 函数实现 i18n，覆盖 100+ 标签键值对。

## API 参考

### `make_financial_model(data, output_path, theme="classic", language="zh")`

生成摩根士丹利风格 DCF 财务模型 Excel 文件。

**参数：**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `data` | `dict` | — | 模型数据字典（参见 `sample_data()` 返回结构） |
| `output_path` | `str` | — | 输出 `.xlsx` 文件路径 |
| `theme` | `str` | `"classic"` | 颜色主题 |
| `language` | `str` | `"zh"` | 语言：`"zh"` 或 `"en"` |

**返回值：** `str` — 生成文件的绝对路径

### `sample_data() -> dict`

返回完整的示例数据字典（Musk Empire Holdings 演示数据），包含全部可选字段。可直接传入 `make_financial_model()` 用于快速测试。

## 依赖

| 依赖 | 最低版本 | 说明 |
|------|----------|------|
| Python | >= 3.9 | 类型注解支持 |
| openpyxl | >= 3.1 | Excel 读写、图表、样式 |

安装依赖：

```bash
pip install openpyxl>=3.1
```

## 字体颜色规范

模型遵循华尔街标准配色规范，便于快速识别单元格性质：

| 颜色 | 色值 | 含义 | 使用场景 |
|------|------|------|----------|
| 蓝色 (Blue) | `#2F75B6` | **输入假设** (Input) | 可手动修改的假设单元格 |
| 黑色 (Black) | `#000000` | **公式计算** (Formula) | 自动计算的公式单元格 |
| 绿色 (Green) | `#006100` | **实际数据** (Actual) | 已公告的历史实际值 |
| 红色 (Red) | `#C00000` | **警示/负值** (Alert) | 负数或需关注的数据 |
| 灰色 (Gray) | `#595959` | **注释说明** (Note) | 说明性文字 |

### 背景填充规范

| 填充色 | 色值 | 含义 |
|--------|------|------|
| 浅黄 | `#FFF2CC` | 输入假设区域 |
| 浅绿 | `#E2EFDA` | 关键计算行 (UFCF) |
| 浅蓝紫 | `#D9E1F2` | 汇总行 |
| 浅橙 | `#FCE4D6` | CapEx / ΔNWC 行 |
| 纯黄 | `#FFFF00` | 敏感性矩阵基准交叉点 |

---

**Author**: WANG DONG JIE ([@yjkj999999](https://github.com/yjkj999999) | [Clawhub](https://clawhub.ai/user/yjkj999999))

**Version**: 1.1.0 | **License**: MIT | **Category**: Financial Modeling

> 适用于 CGMA/ACCA/CPA/CFA 持证人及全球 200 万专业会员。生成符合投行标准的 DCF/SOTP 投资级财务模型。
