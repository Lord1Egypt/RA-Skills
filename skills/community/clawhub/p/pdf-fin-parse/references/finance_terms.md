# 财务术语词表

> 供 `--extract_statement` 章节定位与表格 schema 推断使用。按需加载，避免 system prompt 膨胀。

## 三大主表关键词

### 资产负债表 (balance_sheet)
- 中文：资产负债表 / 合并资产负债表 / 母公司资产负债表
- 英文：Balance Sheet / Consolidated Statement of Financial Position
- 行项关键词：流动资产、非流动资产、流动负债、所有者权益、Total Assets、Total Liabilities

### 利润表 (income_statement)
- 中文：利润表 / 合并利润表 / 综合收益表
- 英文：Income Statement / Statement of Profit or Loss / Consolidated Statement of Operations
- 行项关键词：营业收入、营业成本、毛利、净利润、Revenue、Operating Income、Net Income

### 现金流量表 (cash_flow)
- 中文：现金流量表 / 合并现金流量表
- 英文：Cash Flow Statement / Consolidated Statement of Cash Flows
- 行项关键词：经营活动、投资活动、筹资活动、Cash Flows from Operating / Investing / Financing

## 单位标识

| 文本 | 倍率（→ 元） |
|------|------------|
| 元 / yuan / RMB | 1 |
| 千元 | 1,000 |
| 万元 / 万 | 10,000 |
| 百万元 / 百万 / million | 1,000,000 |
| 亿元 / 亿 | 100,000,000 |

## 负数表示

- `(1,234)` / `（1,234）` → -1234
- `-1,234` → -1234
- `1,234-` （财务格式后缀） → -1234
