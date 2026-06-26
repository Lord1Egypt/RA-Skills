---
name: ifind-excel-plugin
description: iFinD 同花顺 Excel 插件函数参考手册，包含股票、港股、美股、债券、基金、期货等全部金融数据指标的函数表达式、参数代码和使用说明。生成 Excel 数据文件时可参考此 skill 的指标描述。
metadata:
  author: laigen
  version: "10.1"
  source: iFinD Excel 数据插件帮助手册
---

# iFinD Excel 插件函数参考

## 简介

iFinD（同花顺）Excel 数据插件是同花顺机构版金融数据终端的外挂模块，可在 Excel 中直接提取金融数据。

本 skill 包含全部指标函数表达式参考，用于指导生成带 iFinD 公式的 Excel 文件。

## thsiFinD 函数详解

### 函数概述

Excel 插件的核心功能是 Excel 函数表达式。**thsiFinD** 是同花顺最新研发的函数，函数命名表明是同花顺 iFinD 的函数。机构版终端各交易品种的数据浏览器指标在 Excel 中的函数表达式统一使用 thsiFinD 函数，新函数的数据提取更趋稳定快速。

插件总共自定义了约 **14000 个指标代码**，用于提取各种证券的指标数据。

### 函数格式

```
=thsiFinD("指标代码", "证券代码", 参数1, 参数2, ...)
```

函数参数由 **"指标代码"** 和 **"指标参数"** 两部分组成。

### 指标代码命名规则

指标代码的命名逻辑：`THS_指标名称_证券品种`

- **指标名称**：采用指标英文名称组合
- **证券品种**：采用证券英文名称

| 证券品种 | 英文名称 | 示例 |
|----------|----------|------|
| 股票 | STOCK | `ths_close_stock`、`ths_pe_stock` |
| 债券 | BOND | `ths_yield_bond` |
| 可转债 | CBOND | `ths_close_cbond` |
| 基金 | FUND | `ths_nav_fund` |
| 指数 | INDEX | `ths_close_index` |
| 期货 | FUTURES | `ths_close_futures` |
| 港股 | HK | `ths_close_hk` |
| 美股 | US | `ths_close_us` |

**示例**：
```
=thsiFinD("ths_stock_short_name_stock", "")  // 获取股票简称（基本资料）
=thsiFinD("ths_close_stock", "300033", "2024-01-01")  // 获取收盘价
```

### 指标参数详解

指标参数涉及 **5 个常用变量**：

| 参数名称 | 参数变量 | 说明 |
|----------|----------|------|
| 代码 | thsCode | 证券代码（交易代码或同花顺代码） |
| 日期 | Date | 交易日、区间首日(StartDate)、区间尾日(EndDate) |
| 报告期 | ReportDate | 定期报告截止日（年报、中报、一季报、三季报） |
| 类型参数 | Type | 对指标的进一步描述和说明 |
| 指标编码 | ItemsCode | 主要应用于报表科目 |

#### 1. 代码参数 (thsCode)

在机构版终端，证券代码可以是 **交易代码**，也可以是 **同花顺代码**。

**交易代码**：一串数字（整型数据），在 Excel 中可以直接引用：
```
=thsiFinD("ths_stock_short_name_stock", 300033)  // 整型，无需引号
```

**同花顺代码**：字符串格式，在 Excel 中必须用双引号引用：
```
=thsiFinD("ths_stock_short_name_stock", "300033")  // 字符串，必须带引号
=thsiFinD("ths_close_stock", "000001.SZ", "2024-01-01")
```

#### 2. 日期参数 (Date)

日期参数具体分为：
- **交易日 (Date)**：单个日期
- **区间首日 (StartDate)**：日期区间起始
- **区间尾日 (EndDate)**：日期区间结束

支持 **3 种日期格式**：

| 格式类型 | 格式示例 | Excel 引用方式 |
|----------|----------|----------------|
| 整型 YYYYMMDD | `20130109` | 直接引用，无需引号 |
| 字符串 YYYY-MM-DD | `"2013-01-09"` | 必须带双引号 |
| 字符串 YYYY/MM/DD | `"2013/01/09"` | 必须带双引号 |

**示例**：
```
=thsiFinD("ths_close_price_stock", "300033", 20130109, 100, "")  // 整型日期
=thsiFinD("ths_close_price_stock", "300033", "2013-01-09", 100, "")  // 字符串日期
=thsiFinD("ths_close_stock", "000001.SZ", "2024-01-01", "2024-12-31")  // 日期区间
```

#### 3. 报告期/截止日期参数 (ReportDate)

**重要说明**：报告期/截止日期参数需要包含在**每一个函数调用示例中**，并非只有财务报告才有该参数。

- 对于**财务类指标**：报告期就是定期报告截止日（年报、中报、一季报、三季报）
- 对于**行情类指标**：报告期就是行情日期
- 对于**估值类指标**：报告期就是估值日期

**核心原理**：所有公式都是提取**时序指标**，报告期参数对应于时序值的时间点。

**财务报告期代码对照表**：

| 报告类型 | 截止日期 | 代码 |
|----------|----------|------|
| 年报 | 12月31日 | 100 |
| 一季报 | 3月31日 | 101 |
| 中报 | 6月30日 | 102 |
| 三季报 | 9月30日 | 103 |

#### 绝对日期格式（优先推荐）

**重要**：报告期/截止日期/交易日期**推荐使用绝对日期格式**，优先级高于相对代码格式。

**绝对日期格式**即直接指定具体日期，格式与日期参数一致：
- YYYYMMDD（整型）：如 `20241231`、`20240630`
- YYYY-MM-DD（字符串）：如 `"2024-12-31"`、`"2024-06-30"`
- YYYY/MM/DD（字符串）：如 `"2024/12/31"`、`"2024/06/30"`

**绝对日期示例**：
```
// 财务类指标 - 使用绝对日期指定报告期
=thsiFinD("ths_revenue_stock", "000001.SZ", "2024-12-31", 100)  // 2024年报
=thsiFinD("ths_net_profit_stock", "000001.SZ", "2024-06-30", 100)  // 2024中报

// 行情类指标 - 使用绝对日期指定交易日期
=thsiFinD("ths_close_stock", "000001.SZ", "2024-12-31")  // 2024年12月31日收盘价
=thsiFinD("ths_close_stock", "000001.SZ", 20241231)  // 整型日期格式

// 估值类指标 - 使用绝对日期指定估值日期
=thsiFinD("ths_pe_stock", "000001.SZ", "2024-12-31", 100)  // 2024年12月31日PE
```

**相对代码格式**（仅限财务类指标）：
| 代码 | 含义 |
|------|------|
| 100 | 去年年报 |
| 101 | 今年一季 |
| 102 | 今年中报 |
| 103 | 今年三季 |
| 104 | 最新一期 (MRQ) |
| 105 | 去年一季 |
| 106 | 去年中报 |
| 107 | 去年三季 |

**建议**：优先使用绝对日期格式，避免相对代码的时间歧义问题。

**注意**：港股财务报告期可能有特殊情况。

#### 4. 类型参数 (Type)

类型参数是对指标的进一步描述和说明，不同指标的类型参数指向的内容不同。使用时需参考函数搜索里面的参数定义说明。

常见类型参数：

| 类型代码 | 含义 |
|----------|------|
| 100 | 合并报表 |
| 101 | 母公司报表 |
| 102 | 合并报表(调整) |
| 103 | 母公司报表(调整) |

#### 5. 指标编码参数 (ItemsCode)

主要应用于报表科目，具体详见下方"编码表"。

### 参数默认规则

一般而言，函数表达式中的参数设置规则：

| 参数 | 是否必须设置 | 默认值 |
|------|--------------|--------|
| thsCode（代码） | **必须设置** | 无默认 |
| ItemsCode（指标编码） | **必须设置** | 无默认 |
| ReportDate（报告期/截止日期） | **必须设置** | 无默认 |
| Date（日期） | 可不设置 | 当前机器日期 |
| Type（类型） | 可不设置 | 默认取一个数值 |

**说明**：报告期参数对应时序指标的时间点，所有指标（行情、估值、财务）都需要设置该参数以获取特定时点的数据。

具体情况可查看函数搜索里面的参数定义说明。

## 指标数值单位说明

### 金额类指标单位

**重要**：金额类指标（如营业收入、净利润、总资产等）的数值单位一般为**元**，需要根据场景自行换算。

**常见金额指标及单位**：

| 指标类型 | 单位 | 换算示例 |
|----------|------|----------|
| 营业收入 | 元 | 除以10000 = 万元，除以100000000 = 亿元 |
| 净利润 | 元 | 除以10000 = 万元，除以100000000 = 亿元 |
| 总资产 | 元 | 除以10000 = 万元，除以100000000 = 亿元 |
| 总市值 | 元 | 除以100000000 = 亿元 |
| 流通市值 | 元 | 除以100000000 = 亿元 |

**Excel 公式换算示例**：
```
// 获取营业收入并转换为亿元
=thsiFinD("ths_revenue_stock", "000001.SZ", "2024-12-31", 100)/100000000

// 使用单元格引用换算
=thsiFinD("ths_revenue_stock", $B$1, 参数设置!$B$2, 参数设置!$B$4)/100000000

// 设置单元格格式显示（亿元）
// 在Excel中设置单元格格式为：0.00"亿"
```

**建议**：
1. 对于大型公司财务数据，建议转换为**亿元**显示
2. 对于中小型公司财务数据，建议转换为**万元**显示
3. 使用 Excel 单元格格式或公式进行换算，保持原始数据不变

### 其他指标单位

| 指标类型 | 单位 |
|----------|------|
| 收盘价 | 元/股 |
| 成交量 | 股 |
| 成交额 | 元 |
| 市盈率 PE | 倍 |
| 市净率 PB | 倍 |
| ROE | 百分比（%） |
| 涨跌幅 | 百分比（%） |
| 基金净值 | 元/份 |
| 期货持仓量 | 手 |

## 参数代码对照表

### 报告期代码 (100-107)

| 代码 | 含义 |
|------|------|
| 100 | 去年年报 |
| 101 | 今年一季 |
| 102 | 今年中报 |
| 103 | 今年三季 |
| 104 | 最新一期 (MRQ) |
| 105 | 去年一季 |
| 106 | 去年中报 |
| 107 | 去年三季 |

### 报表类型代码 (100-103)

| 代码 | 含义 |
|------|------|
| 100 | 合并报表 |
| 101 | 母公司报表 |
| 102 | 合并报表(调整) |
| 103 | 母公司报表(调整) |

### 数据类别代码 (100-103)

| 代码 | 含义 |
|------|------|
| 100 | 账面余额 |
| 101 | 跌价准备 |
| 102 | 账面价值 |
| 103 | 占合计百分比 |

## 常用指标速查

### 股票行情类

| 指标名称 | 指标代码 | 公式示例 |
|----------|----------|----------|
| 股票简称 | ths_stock_short_name_stock | `=thsiFinD("ths_stock_short_name_stock", "000001.SZ")` |
| 收盘价 | ths_close_stock | `=thsiFinD("ths_close_stock", "000001.SZ", "2024-01-01")` ※ 报告期=行情日期 |
| 开盘价 | ths_open_stock | `=thsiFinD("ths_open_stock", "000001.SZ", "2024-01-01")` ※ 报告期=行情日期 |
| 最高价 | ths_high_stock | `=thsiFinD("ths_high_stock", "000001.SZ", "2024-01-01")` ※ 报告期=行情日期 |
| 最低价 | ths_low_stock | `=thsiFinD("ths_low_stock", "000001.SZ", "2024-01-01")` ※ 报告期=行情日期 |
| 成交量 | ths_vol_stock | `=thsiFinD("ths_vol_stock", "000001.SZ", "2024-01-01")` ※ 报告期=行情日期 |
| 成交额 | ths_amt_stock | `=thsiFinD("ths_amt_stock", "000001.SZ", "2024-01-01")` ※ 报告期=行情日期 |
| 涨跌幅 | ths_chg_stock | `=thsiFinD("ths_chg_stock", "000001.SZ", "2024-01-01")` ※ 报告期=行情日期 |

**说明**：行情类指标的"报告期"参数即为行情日期，表示提取该交易日的时序数据。

### 股票估值类

| 指标名称 | 指标代码 | 公式示例 |
|----------|----------|----------|
| 市盈率 PE | ths_pe_stock | `=thsiFinD("ths_pe_stock", "000001.SZ", 104, 100)` ※ 报告期=估值日期(104=最新) |
| 市净率 PB | ths_pb_stock | `=thsiFinD("ths_pb_stock", "000001.SZ", 104, 100)` ※ 报告期=估值日期(104=最新) |
| 市销率 PS | ths_ps_stock | `=thsiFinD("ths_ps_stock", "000001.SZ", 104, 100)` ※ 报告期=估值日期(104=最新) |
| 总市值 | ths_mv_stock | `=thsiFinD("ths_mv_stock", "000001.SZ", "2024-01-01")` ※ 报告期=估值日期 |
| 流通市值 | ths_free_mv_stock | `=thsiFinD("ths_free_mv_stock", "000001.SZ", "2024-01-01")` ※ 报告期=估值日期 |

**说明**：估值类指标的"报告期"参数即为估值日期，表示提取该日期的估值时序数据。

### 股票财务类

| 指标名称 | 指标代码 | 公式示例 |
|----------|----------|----------|
| 营业收入 | ths_revenue_stock | `=thsiFinD("ths_revenue_stock", "000001.SZ", 104, 100)` ※ 报告期=财务报告期(104=最新) |
| 净利润 | ths_net_profit_stock | `=thsiFinD("ths_net_profit_stock", "000001.SZ", 104, 100)` ※ 报告期=财务报告期 |
| 总资产 | ths_total_assets_stock | `=thsiFinD("ths_total_assets_stock", "000001.SZ", 104, 100)` ※ 报告期=财务报告期 |
| 总负债 | ths_total_liab_stock | `=thsiFinD("ths_total_liab_stock", "000001.SZ", 104, 100)` ※ 报告期=财务报告期 |
| 净资产 | ths_total_owner_equity_stock | `=thsiFinD("ths_total_owner_equity_stock", "000001.SZ", 104, 100)` ※ 报告期=财务报告期 |
| ROE | ths_roe_stock | `=thsiFinD("ths_roe_stock", "000001.SZ", 104, 100)` ※ 报告期=财务报告期 |
| ROA | ths_roa_stock | `=thsiFinD("ths_roa_stock", "000001.SZ", 104, 100)` ※ 报告期=财务报告期 |
| 毛利率 | ths_gross_margin_stock | `=thsiFinD("ths_gross_margin_stock", "000001.SZ", 104)` ※ 报告期=财务报告期 |
| 净利率 | ths_net_margin_stock | `=thsiFinD("ths_net_margin_stock", "000001.SZ", 104)` ※ 报告期=财务报告期 |

**说明**：财务类指标的"报告期"参数为定期报告截止日（100=去年年报、104=最新一期等）。

### 证券公司业务收入类

| 指标名称 | 指标代码 | 公式示例 |
|----------|----------|----------|
| 营业收入 | ths_revenue_stock | `=thsiFinD("ths_revenue_stock", "600030.SH", 104, 100)` |
| 经纪业务手续费净收入 | ths_brokerage_charge_net_income_stock | `=thsiFinD("ths_brokerage_charge_net_income_stock", "600030.SH", 104, 100)` |
| 投资银行业务手续费净收入 | ths_net_income_from_invest_banking_stock | `=thsiFinD("ths_net_income_from_invest_banking_stock", "600030.SH", 104, 100)` |
| 资产管理业务手续费净收入 | ths_ams_charge_net_income_stock | `=thsiFinD("ths_ams_charge_net_income_stock", "600030.SH", 104, 100)` |
| 利息净收入 | ths_interest_net_income_stock | `=thsiFinD("ths_interest_net_income_stock", "600030.SH", 104, 100)` |
| 投资收益 | ths_invest_income_stock | `=thsiFinD("ths_invest_income_stock", "600030.SH", 104, 100)` |
| 公允价值变动收益 | ths_fv_chg_income_stock | `=thsiFinD("ths_fv_chg_income_stock", "600030.SH", 104, 100)` |
| 其他业务收入 | ths_other_bussiness_income_stock | `=thsiFinD("ths_other_bussiness_income_stock", "600030.SH", 104, 100)` |

### 基金类

| 指标名称 | 指标代码 | 公式示例 |
|----------|----------|----------|
| 基金净值 | ths_nav_fund | `=thsiFinD("ths_nav_fund", "000001.OF", "2024-01-01")` ※ 报告期=净值日期 |
| 基金累计净值 | ths_acc_nav_fund | `=thsiFinD("ths_acc_nav_fund", "000001.OF", "2024-01-01")` ※ 报告期=净值日期 |
| 基金份额 | ths_share_fund | `=thsiFinD("ths_share_fund", "000001.OF", "2024-01-01")` ※ 报告期=份额日期 |

**说明**：基金类指标的"报告期"参数即为净值/份额公布日期。

### 指数类

| 指标名称 | 指标代码 | 公式示例 |
|----------|----------|----------|
| 指数收盘 | ths_close_index | `=thsiFinD("ths_close_index", "000001.SH", "2024-01-01")` ※ 报告期=行情日期 |
| 指数涨跌幅 | ths_chg_index | `=thsiFinD("ths_chg_index", "000001.SH", "2024-01-01")` ※ 报告期=行情日期 |

**说明**：指数类指标的"报告期"参数即为指数行情日期。

### 期货类

| 指标名称 | 指标代码 | 公式示例 |
|----------|----------|----------|
| 期货收盘价 | ths_close_futures | `=thsiFinD("ths_close_futures", "IF2401", "2024-01-01")` ※ 报告期=行情日期 |
| 期货结算价 | ths_settle_futures | `=thsiFinD("ths_settle_futures", "IF2401", "2024-01-01")` ※ 报告期=行情日期 |
| 期货持仓量 | ths_open_interest_futures | `=thsiFinD("ths_open_interest_futures", "IF2401", "2024-01-01")` ※ 报告期=行情日期 |

**说明**：期货类指标的"报告期"参数即为期货行情日期。

## 证券代码格式

| 市场 | 格式示例 |
|------|----------|
| A股 | 000001.SZ, 600000.SH |
| 港股 | 00700.HK, 09988.HK |
| 美股 | AAPL.US, MSFT.US |
| 债券 | 110000.SH (上证债券) |
| 基金 | 000001.OF (开放式基金) |
| 指数 | 000001.SH (上证指数) |
| 期货 | IF2401 (沪深300期货) |

## Excel 公式生成最佳实践

### 批量应用时的单元格引用（重要建议）

**重要**：批量生成 Excel 文件时，证券代码、报告期等参数项**建议使用单元格引用的形式**，便于快速调整。

**单元格引用的优势**：

| 优势 | 说明 |
|------|------|
| 快速调整 | 修改一个单元格即可更新整张表格 |
| 减少错误 | 避免逐个修改公式时的遗漏或错误 |
| 便于切换 | 可快速切换报告期、股票标的等参数 |
| 参数集中 | 所有参数集中在一处，便于管理和审核 |

**推荐结构**：

1. **创建参数设置页**：将证券代码、报告期、报表类型、换算系数等参数集中存放
2. **使用绝对引用**：公式中使用 `$` 符号锁定参数单元格
3. **分离数据与参数**：股票代码放在数据表首行，其他参数放在参数设置页

**参数设置页示例**：

| 行 | A列（参数名称） | B列（参数值） | C列（说明） |
|----|-----------------|---------------|-------------|
| 1 | 参数名称 | 参数值 | 说明 |
| 2 | 报告期_当年 | 2025-12-31 | 当年报告期 |
| 3 | 报告期_上年 | 2024-12-31 | 同比基数 |
| 4 | 报表类型 | 100 | 合并报表 |
| 5 | 金额换算 | 100000000 | 换算到亿元 |

**公式示例（单元格引用版）**：

```
// 传统方式（不推荐）：参数硬编码在公式中
=thsiFinD("ths_revenue_stock", "600030.SH", "2024-12-31", 100)/100000000

// 推荐方式：使用单元格引用
=thsiFinD("ths_revenue_stock", $B$1, 参数设置!$B$2, 参数设置!$B$4)/参数设置!$B$5

// 说明：
$B$1 = 数据表第1行的股票代码（绝对引用）
参数设置!$B$2 = 报告期（2025-12-31）
参数设置!$B$4 = 报表类型（100=合并报表）
参数设置!$B$5 = 换算系数（100000000=亿元）
```

**快速调整示例**：

| 场景 | 操作 | 效果 |
|------|------|------|
| 切换报告期 | 修改参数设置!B2 | 所有公式自动更新为新报告期 |
| 调整金额单位 | 修改参数设置!B5 | 改为10000显示万元 |
| 更换股票标的 | 修改数据表第1行 | 替换股票代码 |
| 切换报表类型 | 修改参数设置!B4 | 改为101获取母公司报表 |

## Excel 公式生成示例

### Python + openpyxl 生成带 iFinD 公式的 Excel（单元格引用版）

```python
import openpyxl

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "股票数据"

# 表头
ws['A1'] = '股票代码'
ws['B1'] = '收盘价'
ws['C1'] = '市盈率'
ws['D1'] = '净利润(最新)'

# 数据 + iFinD 公式（统一使用 thsiFinD 格式）
stocks = ['000001.SZ', '600000.SH', '000002.SZ']
for i, stock in enumerate(stocks, start=2):
    ws.cell(row=i, column=1, value=stock)
    # 日期参数：字符串格式必须带引号
    ws.cell(row=i, column=2, value=f'=thsiFinD("ths_close_stock", "{stock}", "2024-01-01")')
    # 报告期+报表类型参数
    ws.cell(row=i, column=3, value=f'=thsiFinD("ths_pe_stock", "{stock}", 104, 100)')
    ws.cell(row=i, column=4, value=f'=thsiFinD("ths_net_profit_stock", "{stock}", 104, 100)')

wb.save('stock_data.xlsx')
```

### 批量生成证券公司业务收入对比表

```python
import openpyxl
from openpyxl.chart import PieChart, Reference

# 证券Ⅲ股票列表
stocks = [
    ("600030.SH", "中信证券"),
    ("601688.SH", "华泰证券"),
    ("000776.SZ", "广发证券"),
    # ... 更多股票
]

# 业务条线指标
metrics = [
    ("ths_revenue_stock", "营业收入"),
    ("ths_brokerage_charge_net_income_stock", "经纪业务手续费净收入"),
    ("ths_net_income_from_invest_banking_stock", "投行手续费净收入"),
    ("ths_ams_charge_net_income_stock", "资管手续费净收入"),
    ("ths_interest_net_income_stock", "利息净收入"),
]

wb = openpyxl.Workbook()
ws = wb.active

# 表头
ws.cell(row=1, column=1, value="指标")
for j, (code, name) in enumerate(stocks, start=2):
    ws.cell(row=1, column=j, value=name)

# 数据行 - 使用 thsiFinD 公式
for i, (metric_code, metric_name) in enumerate(metrics, start=2):
    ws.cell(row=i, column=1, value=metric_name)
    for j, (stock_code, _) in enumerate(stocks, start=2):
        formula = f'=thsiFinD("{metric_code}", "{stock_code}", 104, 100)'
        ws.cell(row=i, column=j, value=formula)

wb.save('证券业务收入对比.xlsx')
```

## 指标代码参考文件

按金融品类分组的指标代码文件（位于 `ref/` 目录）：

| 品类 | 文件 | 数量 |
|------|------|------|
| 股票 | `ref/codes_stock.json` | 4579 |
| 港股 | `ref/codes_hk.json` | 1388 |
| 美股 | `ref/codes_us.json` | 953 |
| 债券 | `ref/codes_bond.json` | 3758 |
| 回购 | `ref/codes_repo.json` | 46 |
| 可转债 | `ref/codes_cbond.json` | 240 |
| 基金 | `ref/codes_fund.json` | 657 |
| 香港基金 | `ref/codes_hkf.json` | 120 |
| 美国基金 | `ref/codes_usf.json` | 12 |
| 券商集合理财 | `ref/codes_bcm.json` | 77 |
| 阳光私募 | `ref/codes_sp.json` | 39 |
| 指数 | `ref/codes_index.json` | 313 |
| 现货 | `ref/codes_spot.json` | 168 |
| 期货 | `ref/codes_future.json` | 280 |
| 期权 | `ref/codes_option.json` | 186 |
| 信托产品 | `ref/codes_trust.json` | 15 |
| 其他理财 | `ref/codes_obcm.json` | 28 |
| **全部指标** | `ref/codes_all.json` | **12859** |

### JSON 文件格式

每个指标包含四个字段：

```json
{
  "code": "ths_close_stock",
  "name": "收盘价",
  "description": "行情指标",
  "params": "日期区间参数说明"
}
```

**字段说明**：
- `code`: 指标代码（如 `ths_pe_stock`）
- `name`: 指标名称（如 `市盈率`）
- `description`: 指标分类/路径（如 `报表附注/应收账款明细`）
- `params`: 参数说明（如 `报告期(100-去年年报,...),报表类型(100-合并报表,...)`）

## 使用说明

1. **查阅指标代码**：根据品种选择对应的 `codes_xxx.json` 文件
2. **查看指标详情**：打开 JSON 文件，检查名称和说明与需求匹配
3. **生成 Excel 公式**：按照统一格式 `=thsiFinD("指标代码", "证券代码", 参数...)` 生成公式
4. **参数注意事项**：
   - 同花顺代码必须用双引号引用
   - 日期字符串格式必须用双引号引用
   - 整型日期和整型代码可直接引用

---

**使用注意**：
- iFinD Excel 插件需要同花顺机构版终端登录后才能使用
- 批量提取时建议控制证券数量，避免服务器负载过高
- 公式格式统一为 `=thsiFinD("指标代码", "证券代码", 参数...)`
- thsiFinD 是同花顺最新研发的函数，数据提取更稳定快速
- **报告期/截止日期参数必须设置**：所有指标（行情、估值、财务）都需要设置该参数，对应时序指标的时间点