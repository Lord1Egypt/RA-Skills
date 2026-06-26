# 聚合支付基础

这份文档负责聚合支付的初始化、公共参数、语言边界和接入前置判断。

## 什么时候读这里

- 第一次接聚合支付
- 需要确认 `trade_type`、公共环境变量、初始化顺序
- 需要判断当前应该走 Java、PHP 还是 Python

## 推荐阅读顺序

```text
shared-overview
  -> shared-signing-v2
  -> shared-request-header-policy
  -> aggregation-base
  -> aggregation-order / aggregation-query / aggregation-refund
```

## 当前版本口径

| 项目 | 当前值 |
| --- | --- |
| Java SDK | `dg-lightning-sdk 1.0.5` |
| PHP 覆盖范围 | 下单、扫码交易查询、关单、关单查询、退款、退款查询、对账 |
| `HUIFU_SKILL_SOURCE` 最终值 | `<skill_source>` |

## 必备环境变量

| 环境变量 | 用途 |
| --- | --- |
| `HUIFU_PRODUCT_ID` | 汇付分配的产品号 |
| `HUIFU_SYS_ID` | 渠道商 / 商户 `huifu_id` |
| `HUIFU_RSA_PRIVATE_KEY` | 请求签名私钥 |
| `HUIFU_RSA_PUBLIC_KEY` | 响应验签公钥 |
| `HUIFU_SKILL_SOURCE` | 可选来源覆盖项，请求头层按 `<skill_source>` 原样透传 |

## 初始化前确认事项

1. 先读 `references/shared-signing-v2.md`
2. 先读 `references/shared-async-notify.md`
3. 如果不是 Java，必须额外核对 `references/shared-request-header-policy.md`
4. 不要猜测 `sub_openid`、`buyer_id`、`auth_code`、`devs_id`、`fee_sign` 等运行时值

## 聚合支付主流程

```text
准备产品号和密钥
  -> 初始化 SDK 或 HTTP 客户端
  -> 选择 trade_type
  -> aggregation-order 下单
  -> aggregation-query 查单 / 关单 / 对账
  -> aggregation-refund 退款
```

## trade_type 速查

| trade_type | 说明 |
| --- | --- |
| `T_JSAPI` | 微信公众号支付 |
| `T_MINIAPP` | 微信小程序支付 |
| `T_APP` | 微信 APP 支付 |
| `T_MICROPAY` | 微信付款码反扫 |
| `A_JSAPI` | 支付宝 JS 支付 |
| `A_NATIVE` | 支付宝正扫 |
| `A_MICROPAY` | 支付宝付款码反扫 |
| `U_JSAPI` | 银联 JS 支付 |
| `U_NATIVE` | 银联正扫 |
| `U_MICROPAY` | 银联付款码反扫 |

## 语言边界

- Java 是聚合支付完整基线
- PHP 已覆盖聚合支付核心主链路与对账；默认入口先读 `references/aggregation-php-adapter.md` 与 `references/aggregation-query-php-scenarios.md`
- Python 已覆盖聚合支付核心主链路与对账；默认入口先读 `references/aggregation-python-adapter.md` 与 `references/aggregation-python-scenarios.md`
- 当前 Skill 包不再内置 PHP 模板资产；PHP 默认走官方 `huifurepo/dg-php-sdk`
- C#、Go 当前只保留统一入口说明，不提供现成业务模板

## 公共字段提醒

- `req_seq_id` 必须保证当日唯一
- `req_date` 建议始终保存，后续查询、关单、退款都要回用
- `method_expand`、`acct_split_bunch`、`terminal_device_data`、`combinedpay_data`、`combinedpay_data_fee_info`、`trans_fee_allowance_info` 应先建模再序列化；`tx_metadata` 本身不作为请求字段上送

## 下一步怎么走

- 要创建订单：读 `references/aggregation-order.md`
- 要查单 / 关单 / 对账：读 `references/aggregation-query.md`
- 要退款：读 `references/aggregation-refund.md`
