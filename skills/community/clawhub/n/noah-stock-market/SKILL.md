---
name: noah-stock-market
description: 用于港股和美股市场数据查询与结构化行情摘要。当用户询问股票当前价格、最新行情、市场快照、分时走势、K线、盘口摆盘、逐笔成交、经纪队列、市场是否开盘、个股资金流向、板块与板块成分股、股票基础信息、期权到期日或期权链等场景时使用。适用于 HK-00700、US-AAPL 这类标准代码，也适用于用户直接输入股票名称或简写代码。仅用于只读查询，不用于下单、账户、持仓、交易执行或投资建议。
---

# Noah Stock Market

港股 / 美股只读市场数据 skill。通过公司内部证券 Open API 获取市场数据，并将原始结果整理成适合聊天场景阅读的结构化摘要。

> **Usage notice**：本 skill 只提供市场数据查询与整理，不提供下单、持仓、账户或投资建议。

## Installation / Usage Prerequisite

本 skill 依赖公司内部证券 Open API。通过 ClawHub / OpenClaw 安装后，用户仍需补充 market token。

推荐配置文件：

```text
~/.openclaw/.secrets/noah-market.env
```

推荐最小配置：

```bash
NOAH_MARKET_APIKEY=your_common_token
NOAH_API_BASE_URL=https://securities-open-api.noahgroup.com
```

说明：
- 当前生产 market 域名已固定为 `https://securities-open-api.noahgroup.com`
- `noah-stock-market` 与 `noah-stock-trade` 共用同一个通用 token
- token 不内置；安装后用户需自行补充 `NOAH_MARKET_APIKEY`
- 不要让用户额外提供与 market 查询无关的配置项

## Skill Routing

当前环境已验证支持：
- 个股快照 / 最新行情
- 实时分时 / K线（含时间范围 K 线）
- 逐笔成交 / 经纪队列
- 市场状态 / 全局市场状态
- 交易日历
- 个股资金流向
- 股票基础信息
- IPO 列表 / 排行榜 / 条件选股
- 美股分析（US analysis）
- 港美股财务数据
- 股东增减持榜单
- 财富类查询：余额、总资产、现金类资产、固收资产、私募资产、银行定存详情

不支持：
- 下单 / 撤单 / 改单
- 账户 / 持仓 / 资金查询
- 任何交易写操作
- 主观投资建议或收益承诺

## Preflight

1. 先读取 `references/auth-and-preflight.md`，确认 API 配置与 token 读取方式。
2. 再根据用户意图，按需读取对应 reference：
   - 标的识别 / 代码标准化 → `references/symbol-resolution.md`
   - 快照 / 最新行情 → `references/snapshot-and-quote.md`
   - 分时 / K线 → `references/kline-and-intraday.md`
   - 逐笔 / 经纪队列 → `references/orderbook-ticker-broker.md`
   - 市场状态 / 交易日 → `references/market-status.md`
   - 资金流向 → `references/capital-flow.md`
   - 基本信息 → `references/plates-and-basicinfo.md`
   - API 意图映射 → `references/api-mapping.md`
   - 使用方式总览 → `references/usage-guide.md`
   - 当前限制 → `references/known-limitations.md`

## Execution Rules

- 默认只走只读接口。
- 优先使用标准代码发请求：港股 `HK-00700`，美股 `US-AAPL`。
- 用户输入名称、简称或裸代码时，先做标准化，再请求接口。
- 如标的存在歧义，不要猜；先返回候选或要求用户澄清市场 / 代码。
- 默认返回结构化摘要，不直接倾倒整段原始 JSON。
- 仅当用户明确要求“明细”“完整逐笔”时，才展开更多原始字段。
- 排行榜、IPO 列表属于扩展能力；只有当用户明确问到时才使用。

- 对 `wealth_total_asset` 与 `wealth_private_contract_asset_list`：
  - 如果用户明确给出币种，则按用户指定币种查询
  - 如果用户未给出币种，则默认按 `USD` 查询

## Recommended Script Entry

优先通过 `scripts/run_query.py` 调用已验证能力：

协议规则（重要）：
- `references/openapi.yaml`、`references/enum.yaml`、`references/entity.yaml` 是本 skill 的协议源文件。
- 凡是 openapi 参数声明为枚举引用（`enum.yaml#/...`），调用时必须从 `references/enum.yaml` 取值并校验，禁止按语义猜测枚举值。
- 若协议源缺失、解析失败或传入值不在 enum 中，应直接报错，不要构造猜测参数继续请求。

- `snapshot`
- `market_state`
- `global_state`
- `intraday`
- `ticker`
- `broker_queue`
- `kline`
- `capital_flow`
- `basicinfo`
- `trading_days`
- `us_analysis`
- `rank`
- `ipo_list`
- `financial_hk`
- `financial_us`
- `shareholder_inc_red_hold`
- `shareholder_inc_red_hold_by_ucode`
- `wealth_balance_list`
- `wealth_cash_total_asset`
- `wealth_fixed_income`
- `wealth_private_contract_asset_list`
- `wealth_total_asset`

示例：

```bash
python3 scripts/run_query.py snapshot HK-00700
python3 scripts/run_query.py market_state HK-00700
python3 scripts/run_query.py global_state HK-00700
python3 scripts/run_query.py intraday HK-00700
python3 scripts/run_query.py ticker HK-00700 num=10
python3 scripts/run_query.py broker_queue HK-00700
python3 scripts/run_query.py kline HK-00700 num=10 ktype=K_DAY
python3 scripts/run_query.py kline HK-00700 from=20260401000000000 to=20260413235959999 ktype=K_DAY autype=NONE
python3 scripts/run_query.py capital_flow HK-00700 num=5
python3 scripts/run_query.py basicinfo HK-00700
python3 scripts/run_query.py trading_days HK-00700 start=20260401 end=20260430
python3 scripts/run_query.py us_analysis US-AAPL
python3 scripts/run_query.py rank HK market_codes=HK rank_field=raisePercent page=1 page_size=10
python3 scripts/run_query.py ipo_list HK market=HK
python3 scripts/run_query.py financial_hk HK-00700 type_code=DT4 year=2024
python3 scripts/run_query.py financial_us US-AAPL type_code=DT4 year=2024
python3 scripts/run_query.py shareholder_inc_red_hold HK market=HK shareholder=EVENT_DATE order_code=DESCEND page=1 page_size=10
python3 scripts/run_query.py shareholder_inc_red_hold_by_ucode HK-00700 shareholder=EVENT_DATE order_code=DESCEND page=1 page_size=10
python3 scripts/run_query.py wealth_balance_list HK
python3 scripts/run_query.py wealth_cash_total_asset HK
python3 scripts/run_query.py wealth_fixed_income HK productTypeList=NOTE,DEPOSIT_COM toCcy=HKD showTotalAsset=true
python3 scripts/run_query.py wealth_private_contract_asset_list HK toCurrency=HKD queryType=ALL positionStatus=HOLDING isPaging=true
python3 scripts/run_query.py wealth_total_asset HK toCurrency=HKD
```

如果脚本返回 `ok=false`，先直接向用户说明失败原因，不要编造数据。
如果用户没有指定 K 线周期与数量，`kline` 默认使用 `num=5`、`ktype=K_DAY`、`autype=NONE`。
如果用户直接用自然语言提问，可优先尝试 `scripts/route_query.py` 做第一轮意图识别，再落到 `scripts/run_query.py`。
当前 `route_query.py` 已支持基础的 K 线周期识别（如日K、周K、月K、5分钟K）与数量识别（如“最近10根”）。

## Output Style

默认输出顺序：
1. 一句话结论
2. 关键数据
3. 补充观察
4. 数据时间 / 状态说明

要求：
- 把枚举值翻译成人话，不直接输出原始枚举代码。
- 对港股 / 美股盘前盘后状态做明确说明。
- 对停牌、退市、无权限订阅、空数据等情况直接说明原因。
- 保持客观，不给买卖建议。

## Response Mode Rule

### 开发模式
当用户在开发、调试、设计或排查这个 skill 时，可以说明：
- 使用了哪个接口
- 请求参数
- 返回结构
- 当前实现逻辑与已知问题

### 股票帮手模式
当 skill 面向最终用户实际使用时：
- 只回答用户需求与结果
- 只展示清晰、简洁、业务化的数据结果
- 不暴露接口 URL、路径、token、脚本名、内部实现逻辑
- 不把开发调试信息带给最终用户
- 如果用户询问“`noah-stock-market` 有什么功能”“你支持什么功能”“这个 skill 能做什么”等能力范围问题，优先用下面这套标准口径回答：

  `noah-stock-market` 目前支持港股和美股的只读市场数据查询，主要包括：
  - 个股快照 / 最新行情
  - 分时走势 / K线
  - 逐笔成交 / 经纪队列
  - 市场状态 / 全局市场状态
  - 交易日历
  - 个股资金流向
  - 股票基础信息
  - IPO 列表 / 排行榜
  - 美股分析
  - 港美股财务数据
  - 股东增减持信息
    - 财富类查询（余额、总资产、固收、私募、现金、银行定存详情）

  你可以直接用自然语言提问，比如：
  - 看一下腾讯现在的股价
  - 看腾讯最近 10 根日 K
  - 查一下腾讯资金流向
  - 现在港股开盘了吗
  - 看港股涨跌幅排行榜
  - 查一下苹果的美股分析
  - 看一下腾讯的财务数据
  - 查一下腾讯最近的股东增减持

  一句话概括就是：
  `noah-stock-market` 已经覆盖港股 / 美股常用行情查询、结构化分析，以及财务和股东增减持这两类扩展数据能力。

## Notes

- 市场代码当前一期只重点支持港股和美股。
- 港股标准代码格式：`HK-00700`
- 美股标准代码格式：`US-AAPL`
- token 与 base URL 不写入 skill 正文，从本地 secrets 配置读取。
