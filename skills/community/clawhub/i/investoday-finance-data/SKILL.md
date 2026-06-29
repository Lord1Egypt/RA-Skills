---
name: investoday-finance-data
title: 今日投资金融数据
version: 1.8.34
description: "获取中国市场金融数据与投研信息，覆盖 A股、港股、基金、指数、财务、公告、研报和宏观经济等 200+ 接口。Use when: 用户要查股票走势、基金净值、指数行情、财务报表、估值指标、公告研报、机构观点、宏观数据、板块主题、产业链、市场统计，或要拉取、导出、对比结构化金融数据。Do not use when: 用户要直接买卖建议、自动下单、交易执行、非金融数据查询、系统运维排查，或在无数据时要求编造结论。"
tags:
  - stock
  - fund
  - etf
  - index
  - bond
  - a-share
  - hk-stock
  - china-market
  - financial-data
  - market-data
  - quote
  - realtime-quote
  - financial-statement
  - balance-sheet
  - income-statement
  - cash-flow
  - valuation
  - dividend
  - ipo
  - announcement
  - research-report
  - macro-economics
  - quantitative
  - investment-research
  - portfolio
  - backtesting
  - data-api
  - finance-api
  - 股票
  - 基金
  - 行情
  - 财务
  - A股
  - 港股
  - 指数
  - 宏观经济
  - 研报
  - 公告
  - 量化
  - 投研
metadata:
  clawdbot:
    emoji: "📈"
    category: "finance"
requirements:
  node: 18+
  packages:
    - name: "@investoday/investoday-api"
  network_access: true
---
# 今日投资金融数据 Skill

获取中国金融市场数据与投研信息，覆盖 A 股、港股、基金、指数、行情、财务、公告、研报、新闻、宏观经济等数据。

## 典型场景

适合用这个 skill 的常见任务：

- 看某只股票、港股、指数或基金最近走势
- 查公司基本资料、财务趋势、估值和经营表现
- 梳理公告、研报、新闻和机构观点
- 看板块、主题、产业链和市场热度
- 查看宏观经济和市场数据
- 导出研究数据，供后续分析、对比或回测使用

先判断用户要解决的问题，再决定是浏览分组、搜索接口，还是直接调用具体接口。

## 何时使用

当用户表达以下意图时，优先使用本 skill：

- 行情 / 趋势：看最近走势、涨跌表现、成交活跃度、相对强弱
- 财务 / 估值：看财报、利润趋势、估值水平、现金流、分红、指标变化
- 公告 / 研报 / 新闻：查最近公告、催化、机构关注点、研究观点
- 基金 / ETF / 指数：查净值、行情、成分、基金资料、基金业绩
- 板块 / 主题 / 产业链：看哪些板块更强、主题热度、产业链关系和经营分析
- 宏观 / 市场：看 CPI、PPI、PMI、利率、市场统计和其他宏观数据
- 数据导出 / 研究准备：拉一份结构化数据，供后续分析、比较或回测

典型用户话术：

- 帮我查下某只股票最近走势
- 看下基金净值或 ETF 表现
- 我想导出财务数据
- 查一下最近公告、研报或机构观点
- 对比几家公司财务指标
- 看看最近哪个板块更强
- 拉一份宏观经济或市场统计数据

## 不适合什么

这个 skill 不适合：

- 直接给出买卖建议或替代投资顾问
- 自动下单或执行交易
- 查询非金融数据、系统端口、服务器状态或其他运维问题
- 在数据不可得、时间范围不合理或接口无结果时硬编结论
- 实现复杂回测引擎、组合优化系统或交易系统本身

如果数据权限、时间范围或接口能力有限，要明确说出限制。

## 决策流程

按以下顺序执行：

1. 先识别用户要的是行情、财务、公告研报、基金指数、宏观、数据导出，还是不属于本 skill 的请求。
2. 如果接口不明确，先用 `investoday-api list` 浏览分组，或用 `investoday-api search-api` 按关键词搜索接口。
3. 如果接口明确但参数不明确，先用 `investoday-api search-api` 查询接口说明、参数和示例。
4. 如果接口和参数都明确，再执行 `investoday-api <endpoint> [key=value ...]`。
5. 如果查询结果为空或受限，说明查询口径、时间范围、权限或网络限制，不要编造数据结论。

用户说自然语言时，先理解任务，不要先回到接口名和字段名。优先把：

- “最近” 解释成合理时间窗
- “财报” 解释成最近几个季度或最近年度
- “强不强” 解释成走势、相对表现和活跃度
- “催化” 解释成公告、研报、新闻、政策等可用口径

## 安装 & 使用

需要 Node.js 18+ 和 Node 包 `@investoday/investoday-api`。

`investoday-api init` 用于初始化 CLI 的本地运行环境配置，可能会创建或更新 CLI 使用的本地配置文件。

## CLI命令参考
```bash
# 初始化运行环境
investoday-api init

# 非交互式一次性初始化
investoday-api init --api-key "<API_KEY>" --auto-update --skip-verify

# 用于浏览多级分组和叶子菜单
investoday-api list <group/subgroup/leaf>

#用于按关键词搜索接口(其中query、tool_ids支持多个入参，以英文逗号隔开)
investoday-api search-api query=<query> tool_ids=<tool_ids>

#发起请求
investoday-api <endpoint> [key=value ...]

#POST 接口如 references 区分 Query 参数与 Body JSON 参数：
#Query 参数使用 key=value；Body JSON 参数使用 --body-json，数组/对象不要写成普通 key=value 字符串。
investoday-api <endpoint> --method POST [queryKey=value ...] --body-json '{"bodyKey":[]}'
```

示例：
```bash
# 初始化运行环境
investoday-api init

# 非交互式一次性初始化
investoday-api init --api-key "<API_KEY>" --auto-update --skip-verify

# 列举
investoday-api list
investoday-api list 沪深京数据
investoday-api list 沪深京数据/公司行为/基本信息

# 关键词搜索
investoday-api search-api query=股票,基本面分析
# 工具信息搜索
investoday-api search-api tool_ids=list_stock_violation_penalt,list_stock_report_schema

# 调用数据
investoday-api search key=贵州茅台 type=11
investoday-api stock/basic-info stockCode=600519
investoday-api fund/daily-quotes --method POST fundCode=000001 beginDate=2024-01-01 endDate=2024-12-31
investoday-api industry-quote/realtime-v2 --method POST industryLevel=1 industryType=SW sortColumn=changeRatio order=desc pageSize=10 --body-json '{"industryCodes":[]}'
```

## 使用策略
- 未明确接口：使用 `list` 或 `search-api` 查找。
- 明确接口但不明确参数：使用 `search-api` 获取接口使用方式。
- 明确接口和参数：直接调用目标接口。
- POST 接口如 references 区分 `Query 参数` 和 `Body JSON 参数`，Query 使用 `key=value`，Body 使用 `--body-json`；不要把数组或对象 Body 写成普通字符串参数。

## 失败处理

- 如果 `investoday-api init` 尚未执行或本地配置缺失，先提示执行 `investoday-api init`，再继续数据查询。
- 如果用户缺少证券代码、基金代码、时间范围、市场类型等必要参数，先说明缺少哪些参数，并给出可继续查询的最小参数。
- 如果接口无结果，说明当前查询口径、时间范围或数据覆盖可能不支持，不要把空结果解释成确定性结论。
- 如果网络、权限或服务不可用，明确说明当前无法取得数据，并停止基于该数据继续推断。

## 辅助文档
- 文档版接口索引见：`docs/references-index.md`
