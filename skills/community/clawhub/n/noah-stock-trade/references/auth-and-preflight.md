# Auth and Preflight

## Current Access Assumption
当前交易侧 / trade 模块按以下新接入前提理解：
- Base URL：与当前环境一致的 securities-open-api 域名
- Request Header：`Authorization: Bearer <token>`

当前阶段：
- trade 与 market 共用同一个 Bearer token
- token 不内置；安装后用户需自行配置
- 不再使用 `groupNo` 作为主要鉴权方式

## Recommended Local Config Names
建议本地统一使用：
- `NOAH_TRADE_API_BASE_URL`
- `NOAH_MARKET_APIKEY`

示例：

```bash
NOAH_TRADE_API_BASE_URL=https://stock-open-api.noahgroup.com
NOAH_MARKET_APIKEY=your_bearer_token
```

## Preflight Checklist
1. 确认交易侧 Base URL 已配置。
2. 确认统一 Bearer token 已配置，并放入 `Authorization` 请求头。
3. 确认当前调用的是订单 / 成交 / 费用 / 可买可卖相关接口。
4. 确认证券代码格式使用交易侧约定：`MARKET.CODE`，例如 `HK.00700`、`US.AAPL`。
5. 对写操作保持禁用认知：当前一期不承诺下单、改单、撤单。

## Notes
- 当前 trade 与 market 复用同一套 token 配置。
- 当前 OpenAPI 中写操作仍为 TEMP DISABLED。
- 若后续 trade 再拆回独立鉴权，再单独补充新的鉴权规则。
