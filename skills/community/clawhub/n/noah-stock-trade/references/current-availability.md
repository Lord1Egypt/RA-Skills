# Current Availability

## Trade Module Capability Status

| Capability | Status | Notes |
|---|---|---|
| Account Info | Scripted / Verified | 已联调成功 |
| Positions | Scripted / Verified | 已按最新文档口径验证；当前使用 `market` 必填 |
| Securities Asset | Scripted / Verified | 已联调成功 |
| Securities Capital Flow | Scripted / Verified | 已联调成功；日期范围查询可用 |
| Stock Amount (Buy/Sell Availability) | Scripted / Verified | 已联调成功；需 `code` + `order_type` |
| Margin Max Buy Amount | Scripted / Verified | 已联调成功；需 `code` + `order_type` + `entrust_price` |
| Today Deal List | Scripted / Verified | 已联调成功 |
| History Deal List | Scripted / Verified | 已联调成功；需 `start_date` + `end_date` |
| Today Unfinished Order List | Scripted / Verified | 对应 `/trade/get_today_order_list`，已联调成功 |
| Today Order List | Scripted / Verified | 已按最新文档口径验证；当前使用 `market` 必填 |
| History Order List | Scripted / Verified | 已联调成功；当前按最新文档需传 `start_date` + `end_date` |
| Finished Order List | Scripted / Verified | 已联调成功 |
| Order Detail | Scripted / Verified | 已用真实 `order_id` 联调成功 |
| Order Fee Detail | Scripted / Verified | 已用真实 `order_id` 联调成功 |
| Order Fee Query | Scripted / Verified | 已联调成功；需 POST + JSON body |
| Push Data Query | Scripted / Verified | 当前按最新文档需传 `init_date` + `begin_serial_no` + `end_serial_no` |
| Place Order | Deferred / Not enabled | 当前阶段不对外承诺写操作 |
| Modify Order | Deferred / Not enabled | 当前阶段不对外承诺写操作 |
| Cancel Order | Deferred / Not enabled | 当前阶段不对外承诺写操作 |

## Access Prerequisites

当前 trade 模块使用：
- Base URL：`https://stock-open-api.noahgroup.com`
- Header：`Authorization: Bearer <token>`

推荐本地变量名：
- `NOAH_TRADE_API_BASE_URL`
- `NOAH_MARKET_APIKEY`

## Notes

- 当前 `noah-stock-trade` 已吸收原 `noah-stock-portfolio` 的账户、持仓、资产、资金流水能力。
- 当前状态中的 `Scripted / Verified` 表示：
  - 脚本入口已存在
  - 已在当前测试环境完成至少一轮实际联调
- `Routed but inconsistent` 表示：
  - OpenAPI 文档已有定义
  - CLI / client 已接入
  - 但当前测试环境返回行为与文档不一致
- `Routed but server-side error` 表示：
  - 路由和参数链路已打到目标接口
  - 但当前测试环境返回服务端异常，仍需后端或接口实现侧确认
- 交易模块使用的证券代码格式为 `MARKET.CODE`，例如 `HK.00700`、`US.AAPL`。
- 后续可继续补充与 market 模块代码格式（`HK-00700` / `US-AAPL`）之间的统一展示转换。
