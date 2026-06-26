# 汇付聚合支付 — 下单快速导览

基于 dg-lightning-sdk 的聚合支付下单导览，覆盖微信/支付宝/银联全场景。

## 定位

聚合支付下单入口，支持 10 种支付类型（正扫/反扫/JS支付/小程序/APP）。

## 核心内容

- **聚合支付下单**：`v4/trade/payment/create`
- **10 种 trade_type**：T_JSAPI、T_MINIAPP、T_APP、T_MICROPAY、A_JSAPI、A_NATIVE、A_MICROPAY、U_JSAPI、U_NATIVE、U_MICROPAY
- **method_expand 各场景详解**：不同 trade_type 的扩展结构与条件必填关系，且 JSON 内容直接是当前场景对象本身
- **前端处理与回调**：二维码生成、JS 调起、付款码扫码、异步通知 / webhook
- **完整型 reference**：按请求、渠道、扩展、响应、错误拆成多个分册，避免单文件过大

## 参考文件

| 文件 | 内容 |
|-----|------|
| `references/aggregation-order.md` | 场景总览与阅读入口 |
| `references/aggregation-customer-preparation.md` | 客户前置准备清单、场景参数来源 |
| `references/aggregation-payload-construction.md` | `method_expand` / 顶层交易能力扩展字段参数校验与序列化规范 |
| `references/aggregation-order-request.md` | 公共请求参数与顶层字段 |
| `references/aggregation-order-method-wechat.md` | 微信请求与回调字段 |
| `references/aggregation-order-method-alipay.md` | 支付宝请求与回调字段 |
| `references/aggregation-order-method-unionpay.md` | 银联请求与回调字段 |
| `references/aggregation-order-tx-metadata.md` | 请求顶层交易能力扩展字段与返回 `tx_metadata` 的边界说明 |
| `references/aggregation-order-response.md` | 同步返回、异步回调、解冻通知 |
| `references/aggregation-order-errors.md` | 返回码与文档勘误 |

## 开发前检查

- 先确认客户是否已经准备好 `trade_type` 对应的运行时值，例如 `sub_openid`、`buyer_id`、`user_id`、`auth_code`、`customer_ip`、`devs_id`。
- 先确认官方开发指引要求的业务开通、应用配置、授权绑定动作已经完成；这些不是补参数可以替代的。
- `method_expand`、`acct_split_bunch`、`terminal_device_data`、`combinedpay_data`、`combinedpay_data_fee_info`、`trans_fee_allowance_info` 在业务层应保持对象结构，做完校验后再统一转成 JSON 字符串；`tx_metadata` 本身不作为请求字段上送。
- 条件必填字段建议在客户自己的 API 层先拦截，不要把缺参请求直接打进 SDK。
- 微信 / 支付宝 / 银联官方开发指引都要求：前端收到支付完成回调后，后端仍需调用查询订单 API 确认最终状态。
