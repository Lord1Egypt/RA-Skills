# Usage Guide

## 1. What This Module Is For
`noah-stock-trade` 当前用于：
- 账户信息查询
- 持仓查询
- 证券资产查询
- 证券资金流水查询
- 当日未完成订单查询
- 当日成交查询
- 历史成交查询
- 订单详情查询
- 订单费用查询
- 下单前费用预估
- 可买可卖数量查询
- 融资最大可买数量查询

当前阶段**不用于**：
- 真实下单
- 改单
- 撤单

## 2. Access Prerequisites
当前口径下，需要：
- `NOAH_TRADE_API_BASE_URL`
- `NOAH_MARKET_APIKEY`

其中：
- `NOAH_MARKET_APIKEY` 为 market / trade 共用通用 token
- token 不内置，需由用户安装后自行配置

当前交易侧接入前提：
- Base URL：`https://stock-open-api.noahgroup.com`
- Header：`Authorization: Bearer <token>`

## 3. Suitable Query Scenarios
适合的场景包括：
- 看账户信息
- 查当前持仓
- 看证券资产
- 查资金流水
- 看今天的未完成订单
- 看今天的成交
- 查历史成交
- 看某笔订单详情
- 看某笔订单费用
- 查询某只股票可买可卖数量
- 查询某只股票融资最大可买数量
- 查询某笔拟下单的预估费用

## 4. Recommended CLI Commands
### 账户 / 持仓 / 资产
```bash
python3 scripts/noah_trade_cli.py account-info
python3 scripts/noah_trade_cli.py positions --market HK
python3 scripts/noah_trade_cli.py positions --market US
python3 scripts/noah_trade_cli.py sec-asset
python3 scripts/noah_trade_cli.py sec-capital-flow --start-date 20260401 --end-date 20260413
```

### 订单 / 成交 / 费用 / 可交易能力
```bash
python3 scripts/noah_trade_cli.py today-orders --market HK --page 1 --page-size 20
python3 scripts/noah_trade_cli.py unfinished-orders
python3 scripts/noah_trade_cli.py today-deals
python3 scripts/noah_trade_cli.py history-orders --start-date 20250401 --end-date 20260415
python3 scripts/noah_trade_cli.py history-deals --start-date 20250401 --end-date 20260415
python3 scripts/noah_trade_cli.py finished-orders --start-date 20250401 --end-date 20260415 --page 1 --page-size 20
python3 scripts/noah_trade_cli.py query-push-data --init-date 20260415 --begin-serial-no 1 --end-serial-no 100
python3 scripts/noah_trade_cli.py order-detail --order-id 2025101600HK0000000001 --is-history
python3 scripts/noah_trade_cli.py order-fee-detail --order-id 2025101600HK0000000001 --is-history
python3 scripts/noah_trade_cli.py fee-estimate --symbol HK.00700 --side BUY --order-type LIMIT --price 320 --qty 100
python3 scripts/noah_trade_cli.py stock-amount --symbol HK.00700 --order-type LO
python3 scripts/noah_trade_cli.py max-enable-buy-amt --symbol HK.00700 --order-type LO --entrust-price 320
```

> 注意：当前 `max-enable-buy-amt` 实际联调时还需要额外价格参数，后续脚本将继续对齐到服务端要求。

## 5. Symbol Format Note
交易接口当前使用的证券代码格式是：
- `HK.00700`
- `US.AAPL`

这与 market 模块常用的：
- `HK-00700`
- `US-AAPL`

不同，脚本层已开始做统一转换，但用户态展示仍可继续优化。

## 6. Order Status Note
订单查询结果中可能同时包含：
- OpenAPI 统一状态
- sec-trade 原始状态码

建议优先向最终用户展示统一状态；如需补充解释，再结合：
- `references/order-status-mapping.md`

## 7. Current Limitations
当前已知限制包括：
- 写操作接口（下单 / 改单 / 撤单）当前不对外承诺
- `get_positions` 与 `get_order_list` 已按新版文档切换到 `market` 必填口径，旧参数理解不再适用
- `max_enable_buy_amt` 需要传 `entrust_price`
- 多币种资产展示时不得直接跨币种加总；如无汇率依据，应按币种分别展示

## 8. Relationship with Other Modules
- 行情 / K线 / 分时 / 摆盘 → `noah-stock-market`
- 条件选股 → 后续可并入 `noah-stock-market` 或单独保留
- 原 `noah-stock-portfolio` 能力已逐步合并到本模块
