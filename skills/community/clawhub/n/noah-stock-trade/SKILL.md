---
name: noah-stock-trade
description: 用于股票交易相关的订单、成交、可买可卖数量、订单详情、订单费用、下单前费用预估，以及账户、持仓、证券资产、资金流水等场景。当用户询问今日订单、历史订单、今日成交、历史成交、订单状态、订单详情、费用明细、可买可卖数量、融资最大可买数量、账户信息、当前持仓、证券资产、资金流水、组合概览、交易前评估时使用。优先通过统一 CLI / 脚本入口执行查询与评估，不要让 agent 直接手拼交易接口。当前默认只开放只读查询与交易前评估；真实下单、改单、撤单属于高风险写操作，当前不对外承诺。
---

# Noah Stock Trade

股票交易、账户与持仓查询 skill。默认把交易能力视为**高风险域**：先走统一脚本入口，先做只读，先做结构化错误，再考虑写操作。

## Quick Start

先读取：
- `references/auth-and-preflight.md`
- `references/current-availability.md`

根据任务再按需读取：
- 订单状态/成交状态解释 → `references/order-status-mapping.md`
- 输出风格与用户态表达 → `references/output-policy.md`
- 常见错误与排障 → `references/error-catalog.md`
- 示例与调用习惯 → `references/usage-guide.md`

## Runtime Rule

优先使用统一 CLI / 脚本入口，而不是直接在对话里拼接交易 OpenAPI。

推荐入口：
- `python3 scripts/noah_trade_cli.py account-info`
- `python3 scripts/noah_trade_cli.py positions --market HK`
- `python3 scripts/noah_trade_cli.py sec-asset`
- `python3 scripts/noah_trade_cli.py sec-capital-flow --start-date 20250401 --end-date 20260415`
- `python3 scripts/noah_trade_cli.py today-orders --market HK --page 1 --page-size 20`
- `python3 scripts/noah_trade_cli.py today-deals`
- `python3 scripts/noah_trade_cli.py history-orders --start-date 20250401 --end-date 20260415`
- `python3 scripts/noah_trade_cli.py finished-orders --start-date 20250401 --end-date 20260415 --page 1 --page-size 20`
- `python3 scripts/noah_trade_cli.py order-detail --order-id <id> --is-history`
- `python3 scripts/noah_trade_cli.py order-fee-detail --order-id <id> --is-history`
- `python3 scripts/noah_trade_cli.py fee-estimate --symbol HK.00700 --side BUY --order-type LIMIT --price 320 --qty 100`
- `python3 scripts/noah_trade_cli.py stock-amount --symbol HK.00700 --order-type LO`

如果脚本返回 `ok=false`：
1. 先向用户说明失败原因
2. 优先使用结构化错误中的 `message` / `hint`
3. 不要编造订单、成交、费用、账户、持仓或资产信息

## Supported Scope

当前优先支持：
- 账户信息
- 按市场查询当前持仓
- 证券资产
- 证券资金流水
- 今日订单 / 当日未完成订单
- 历史订单 / 已完成订单
- 今日成交 / 历史成交
- 订单详情
- 订单费用详情
- 下单费用预估
- 可买可卖数量
- 融资最大可买数量
- 推送数据查询

暂不开放：
- 真实下单 / 改单 / 撤单

## Routing Boundary

适用于：
- 账户信息 / 持仓 / 证券资产 / 资金流水
- 订单列表 / 订单状态 / 订单详情
- 成交列表 / 成交状态
- 费用预估 / 费用详情
- 可买可卖数量 / 最大可买数量
- 交易前评估

不适用于：
- 行情数据查询（交给 `noah-stock-market`）
- 条件选股（交给 `noah-stock-screener`）
- 主观投资建议

## Symbol Rule

交易模块内部优先使用 `MARKET.CODE` 格式：
- `HK.00700`
- `US.AAPL`

如果用户输入的是：
- `HK-00700`
- `US-AAPL`
- `00700`
- 股票名称

先做代码标准化，再进入交易脚本。
若标的存在歧义，不要猜，先要求用户澄清市场或代码。

## Output Rule

默认输出顺序：
1. 一句话结论
2. 关键字段
3. 状态解释
4. 必要时补充错误原因或限制说明

对用户展示时：
- 优先说人话，不直接倾倒整个原始 JSON
- 把订单状态、成交状态、方向、费用项翻译成人能看懂的话
- 对空结果要明确说明“未查到”还是“接口失败”

在开发/调试场景下，可以额外说明：
- 使用了哪个 CLI 命令
- 调用了哪个 endpoint
- 返回了什么结构化错误

如果用户询问“`noah-stock-trade` 有什么功能”“交易 skill 支持什么”“这个交易 skill 能做什么”等能力范围问题，优先使用下面这套标准口径回答：

`noah-stock-trade` 当前支持以下交易相关功能：
- 查询账户信息
- 按市场查询当前持仓
- 查询证券资产
- 查询证券资金流水
- 查询今日订单
- 查询当日未完成订单
- 查询历史订单
- 查询已完成订单
- 查询今日成交
- 查询历史成交
- 查询订单详情
- 查询订单费用详情
- 查询证券可买可卖数量
- 查询融资最大可买数量
- 查询下单前费用预估
- 查询推送数据

当前暂不开放：
- 下单
- 改单
- 撤单

## 多币种持仓 / 资产展示规则

当用户查询持仓、证券资产、总资产、账户资产时，必须注意不同市场和账户可能涉及多种计价货币（如 HKD、USD、CNY）。

规则如下：
- 不对不同计价货币的持仓市值、资产金额做直接加总
- 如果用户问“总资产是多少”，默认按币种分别列出，并明确说明“以下为各货币资产，未做汇率换算”
- 如果接口本身已经返回换算后的汇总值，可以原样展示，但必须注明“该汇总值由接口按当日汇率换算”
- 如果用户明确要求折算，必须说明需要汇率依据，并引导用户提供汇率口径，或改用行情数据作为换算依据

禁止：
- 直接把 HKD、USD、CNY 等金额相加后当作“总资产”返回给用户
- 在没有汇率依据时自行做跨币种折算

## Risk Rule

- 默认按只读模式处理
- 当前不直接承诺真实下单、改单、撤单
- 若未来开放写操作，必须：
  1. 明确市场、标的、方向、价格、数量
  2. 明确实盘/测试盘环境
  3. 做二次确认
  4. 防止重复提交

## Preflight Checklist

执行前至少确认：
1. 已配置 `NOAH_TRADE_API_BASE_URL`
2. 已由用户自行配置统一 Bearer token（`NOAH_MARKET_APIKEY`）
3. Bearer token 对当前 trade 接口有访问权限
4. 当前环境是测试还是正式已明确
5. 当前任务是否属于只读查询或交易前评估

若以上任一项不满足，先返回缺失项，不要继续假设可交易。

## Implementation Direction

本 skill 的实现原则：
- Skill 负责路由和风险边界
- `scripts/noah_trade_cli.py` 负责统一执行入口
- `scripts/trade_client.py` / `scripts/portfolio_client.py` 负责 HTTP / header / 错误封装
- 参数校验、symbol 转换、状态码映射尽量下沉到脚本层

不要让 agent 在每次任务里重新发明交易接口调用逻辑。

## Notes

- 当前阶段以查询和评估为主，不以写操作为主承诺
- 若 `references/current-availability.md` 与脚本实际能力不一致，以脚本真实可执行结果为准
- 若用户提到“之前已经能调”，优先检查现有脚本和调用链路，而不是只看文档状态
