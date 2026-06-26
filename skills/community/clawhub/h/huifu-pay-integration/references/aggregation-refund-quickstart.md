# 汇付聚合支付 — 退款快速导览

基于 dg-lightning-sdk 的聚合支付退款导览。

## 定位

支付成功后的退款处理和退款状态查询。

## 核心内容

- **交易退款**：`v4/trade/payment/scanpay/refund` — 发起退款
- **退款查询**：`v4/trade/payment/scanpay/refundquery` — 查询退款结果

## 与托管支付退款的区别

| 方面 | 聚合支付退款当前文档链路 | 托管支付退款 |
|------|---------------------|-----------|
| SDK | dg-lightning-sdk | dg-java-sdk |
| org_req_seq_id | 有独立 setter，直接调用 | **无 setter**，必须 extendInfoMap |
| remark/notify_url | **无 setter**，通过 `client.optional()` | 通过 extendInfoMap |
| 交易能力扩展字段 | 请求侧不传 `tx_metadata` 包装层；不要传 `tx_metadata`；按能力名直接传 `acct_split_bunch` / `combinedpay_data` / `terminal_device_data` | 通过 extendInfoMap / setter |
| 调用方式 | `client.refund(req)` | `BasePayClient.request(req, false)` |

## 参考文件

| 文件 | 内容 |
|-----|------|
| `references/aggregation-refund.md` | 退款接口总览与阅读入口 |
| `references/aggregation-refund.md` | 退款申请字段、同步返回摘要与扩展字段 |
| `references/aggregation-refund-query.md` | 退款查询（含退款标识语义与扩展字段） |
