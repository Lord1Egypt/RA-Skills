# 聚合支付下单

这份文档覆盖聚合支付的下单场景选择、关键字段和状态理解。

## 什么时候读这里

- 已完成聚合支付初始化
- 现在要调用 `v4/trade/payment/create`
- 需要按 `trade_type` 选择微信、支付宝或银联场景

## 下单主流程

```text
选择 trade_type
  -> 准备场景参数
  -> 调用 v4/trade/payment/create
  -> 保存 req_seq_id / req_date / hf_seq_id
  -> 前端展示二维码或拉起支付
  -> 回到 aggregation-query 做最终确认
```

## 场景与关键返回

| 场景 | trade_type | 关键返回 |
| --- | --- | --- |
| 微信公众号 / 小程序 / APP | `T_JSAPI` / `T_MINIAPP` / `T_APP` | `pay_info` |
| 微信付款码 | `T_MICROPAY` | 同步支付结果 |
| 支付宝 JS / 正扫 / 付款码 | `A_JSAPI` / `A_NATIVE` / `A_MICROPAY` | `pay_info` 或 `qr_code` |
| 银联 JS / 正扫 / 付款码 | `U_JSAPI` / `U_NATIVE` / `U_MICROPAY` | `pay_info` 或 `qr_code` |

## 关键前置条件

| 场景 | 必须来自真实链路的值 |
| --- | --- |
| 微信公众号 / 小程序 | `sub_openid` |
| 支付宝 JS | `buyer_id` 或 `buyer_logon_id` |
| 银联 JS | `user_id`、`customer_ip` |
| 各类付款码 | `auth_code` |

## 通用请求字段

| 字段 | 说明 |
| --- | --- |
| `huifu_id` | 商户号 |
| `req_seq_id` | 请求流水号 |
| `req_date` | 请求日期，建议始终传并保存 |
| `trade_type` | 交易类型 |
| `trans_amt` | 交易金额 |
| `goods_desc` | 商品描述 |
| `notify_url` | 异步通知地址 |
| `method_expand` | 场景扩展字段 |

## 请求头强制约束

- `v4/trade/payment/create` 必须带 `jpt-x-skill-source: <skill_source>`
- 如果当前按 PHP 接入，且请求 `data` 中存在 `huifu_id`，还必须带 `jpt-x-skill-huifu_id: <data.huifu_id>`
- 当前 Skill 包对齐的官方 PHP SDK 主链路在 `MerConfig.skill_source` 已配置时，会自动带 `jpt-x-skill-source`，并在当前请求 `huifu_id` 存在且非空时自动带 `jpt-x-skill-huifu_id`
- 当前 Java SDK 基线也会在请求 `data` 中存在 `huifu_id` 且非空时自动带 `jpt-x-skill-huifu_id: <data.huifu_id>`
- 这两项属于 HTTP 请求头，不属于业务报文 `data`；完整口径以 `references/shared-request-header-policy.md` 为准

## 通用返回字段

| 字段 | 说明 |
| --- | --- |
| `resp_code` | 接口受理结果 |
| `hf_seq_id` | 汇付全局流水号 |
| `trans_stat` | `P` 处理中、`S` 成功、`F` 失败 |
| `qr_code` | 正扫二维码地址 |
| `pay_info` | JS / 小程序拉起参数 |

## 必须保存的字段

- `req_seq_id`
- `req_date`
- `hf_seq_id`
- 商户侧订单号或渠道订单号

## 易错点

- 前端支付完成回调不等于最终支付成功
- `resp_code=00000000` 也不代表交易一定成功，仍需看 `trans_stat`
- `method_expand` 不要手写裸字符串，先建模再序列化

## PHP 官方 SDK 路由

- 聚合支付 PHP 下单已支持官方 `huifurepo/dg-php-sdk`
- 默认先读 `references/aggregation-php-adapter.md` 与 `references/aggregation-query-php-scenarios.md`
- 代码入口优先 `BsPaySdk\core\Payment::create()` + `TradePaymentCreateRequest`
- 头部约束仍以 `references/shared-request-header-policy.md` 为准

## 下一步

支付发起后统一读 `references/aggregation-query.md` 做最终确认。
