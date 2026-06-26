# 聚合支付查询、关单与对账

这份文档覆盖聚合支付的查单、关单、关单查询和对账单查询。

## 什么时候读这里

- 下单后需要确认最终支付状态
- 订单超时未支付，需要关单
- 需要下载或解析对账文件

## 查询 / 关单主流程

```text
确认已保存原交易 req_date / req_seq_id / hf_seq_id
  -> 先查单
  -> 未支付且满足条件时再关单
  -> 关单后继续查关单结果
  -> 按 file_date / bill_type 下载对账文件
```

## 对应接口

| 场景 | 接口 |
| --- | --- |
| 交易查询 | `v4/trade/payment/scanpay/query` 或对应查询接口 |
| 交易关单 | `v2/trade/payment/scanpay/close` |
| 关单查询 | `v2/trade/payment/scanpay/closequery` |
| 对账单查询 | `v2/trade/check/filequery` |

## 请求头强制约束

- 上面 4 类接口都必须带 `jpt-x-skill-source: <skill_source>`
- 如果当前按 PHP 接入，且请求 `data` 中存在 `huifu_id`，还必须带 `jpt-x-skill-huifu_id: <data.huifu_id>`
- 当前 Skill 包对齐的官方 PHP SDK 主链路在 `MerConfig.skill_source` 已配置时，会自动带 `jpt-x-skill-source`，并在当前请求 `huifu_id` 存在且非空时自动带 `jpt-x-skill-huifu_id`
- 当前 Java SDK 基线也会在请求 `data` 中存在 `huifu_id` 且非空时自动带 `jpt-x-skill-huifu_id: <data.huifu_id>`
- 这两项属于 HTTP 请求头，不属于业务报文 `data`；具体明细以 `references/shared-request-header-policy.md` 为准

## 查询键要求

- 查询通常使用 `out_ord_id`、`hf_seq_id`、`req_seq_id` 三选一
- 按 `req_seq_id` 查询时建议同时保留并传入 `req_date`
- 关单和关单查询都要求保留原交易标识
- 合单交易关单和关单查询必须补 `merge_flag=Y`，并使用主单信息定位；非合单或空值使用子单信息

## 关单约束

1. 仅支持微信和支付宝交易，银联二维码交易不支持关单
2. 不允许关闭一分钟以内的订单
3. 原交易已成功或失败时不能关单，应该直接结束或走退款流程

## 处理中轮询策略

当查询返回 `trans_stat=P` 时：

- 轮询间隔：`5` 秒
- 最大轮询次数：`30` 次
- 总窗口：`150` 秒

超时后记录异常并人工介入，不要自动改判成功或失败。

## 对账单规则

- 请求字段固定为 `file_date` 和 `bill_type`
- 不要自行改写成 `bill_date`、`generate_date` 或 `file_type`
- 合并账单使用 `bill_type=MERGE_BILL`
- 文件名字段生产解析要兼容 `file_name` 和历史示例里的 `file_Name`
- 对账文件通常是 zip 内含 csv
- `SETTLE_FUND_BILL` 模板是 `.xlsx`
- 接口口径为 1 年内账单查询

## PHP 官方 SDK 路由

聚合支付 PHP 当前已覆盖：

- 下单：`Payment::create()`
- 扫码交易查询：`Payment::query()`
- 关单：`Payment::close()`
- 关单查询：`Payment::closeQuery()`
- 退款：`Payment::refund()`
- 退款查询：`Payment::refundQuery()`
- 对账：`BsPayClient::postRequest()` + `V2TradeCheckFilequeryRequest`

默认入口先读 `references/aggregation-php-adapter.md` 与 `references/aggregation-query-php-scenarios.md`。
核对补头或签名时，读取 `references/shared-request-header-policy.md` 与 `references/shared-signing-v2.md`；不要回到历史自维护 PHP client 方案。

## 下一步

- 要退款：读 `references/aggregation-refund.md`
- 还没完成初始化：回到 `references/aggregation-base.md`
