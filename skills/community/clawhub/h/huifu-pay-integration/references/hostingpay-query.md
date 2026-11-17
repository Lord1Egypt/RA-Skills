# 托管支付查询、关单与对账

这份文档覆盖托管订单状态查询、拆单支付订单查询、关单和对账单查询。

## 什么时候读这里

- 预下单后需要确认最终支付状态
- 微信小程序拆单支付后需要查询拆单明细
- 订单超时未支付，需要关单
- 需要按账单日期下载对账文件

## 对应接口

| 场景 | 接口 |
| --- | --- |
| 交易查询 | `v2/trade/hosting/payment/queryorderinfo` |
| 拆单支付订单查询 | `v2/trade/hosting/payment/splitpay/query` |
| 交易关单 | `v2/trade/hosting/payment/close` |
| 对账单查询 | `v2/trade/check/filequery` |

## 请求头强制约束

- 上面 4 类接口都必须带 `jpt-x-skill-source: <skill_source>`
- 如果当前按 PHP 接入，且请求 `data` 中存在 `huifu_id`，还必须带 `jpt-x-skill-huifu_id: <data.huifu_id>`
- 当前 Skill 包对齐的官方 PHP SDK 主链路在 `MerConfig.skill_source` 已配置时，会自动带 `jpt-x-skill-source`，并在当前请求 `huifu_id` 存在且非空时自动带 `jpt-x-skill-huifu_id`
- 当前 Java SDK 基线也会在请求 `data` 中存在 `huifu_id` 且非空时自动带 `jpt-x-skill-huifu_id: <data.huifu_id>`
- 这两项属于 HTTP 请求头，不属于业务报文 `data`；具体明细以 `references/shared-request-header-policy.md` 为准

## 查询 / 关单主流程

```text
确认已保存 req_date / req_seq_id / party_order_id / hf_seq_id
  -> 先查单
  -> 未支付且符合条件时再关单
  -> 对处理中订单轮询确认
  -> 按 file_date / bill_type 下载对账文件
```

## 关键查询键

- 查询支持 `party_order_id` 单独查询
- 也可使用 `huifu_id + org_req_date + org_req_seq_id`
- 拆单支付订单查询必须使用原拆单支付的 `org_req_date + org_req_seq_id`，明细字段继续看 `references/hostingpay-query-splitpay.md`
- 关单必须保留原交易的 `org_req_date` 和 `org_req_seq_id`

## 状态字段

| 字段 | 含义 |
| --- | --- |
| `trans_stat` | `P` 处理中、`S` 成功、`F` 失败、`I` 初始 |
| `order_stat` | 预下单状态 |
| `close_stat` | 关单状态 |

## 处理中轮询策略

- 轮询间隔：`5` 秒
- 最大次数：`30`
- 总窗口：`150` 秒

超时后记录异常并人工介入，不要自动关单。

## 对账规则

- 请求字段必须保持 `file_date` 和 `bill_type`
- 常见下载结果为 zip 内含 csv
- 结算资金对账单模板为 xlsx
- 当前口径仍按 1 年内账单查询理解

## 关单边界

1. 关单前建议先查单
2. 已支付成功的订单不能关单，只能走退款
3. 关单会影响后续支付，不能在状态不清晰时直接关闭

## PHP 路径

托管支付 PHP 支持查询、关单和对账，默认入口先读：

- `references/hostingpay-php-adapter.md`
- `references/hostingpay-query-php-scenarios.md`

如果只是核对补头或签名口径，读取 `references/shared-request-header-policy.md` 与 `references/shared-signing-v2.md`

## 下一步

- 原交易成功后退款：读 `references/hostingpay-refund.md`
- 前端组件协作：读 `references/checkout-js.md`
