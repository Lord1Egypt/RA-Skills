# 余额支付退款查询

官方来源：<https://paas.huifu.com/partners/api/doc/yuer/api_acctpaytkcx.md>；快照 `2026-11-04`，官网更新时间 `2026-04-27`。

接口：`POST /v2/trade/acctpayment/refund/query`；完整31个字段路径见 `payment-complete-field-catalog.md` 的“余额支付退款查询”，联读 `balancepay-field-contracts.md`。

## 请求

只有三个正式业务字段，均 Y：`org_req_seq_id:String(128)` 为原退款请求流水，`org_req_date:String(8)` 为原退款请求日期，`huifu_id:String(32)` 为发起方。不能填原支付日期/流水，也不能用响应中的 `org_hf_seq_id` 作为未声明的请求替代键。

## 响应

- 查询返回码与退款业务状态分别判断；`trans_stat=P/S/F`，未声明 C。
- `org_hf_seq_id:String(40) N` 表示原退款全局流水，与支付查询同名键角色不同。
- `acct_split_bunch:String(JSON Object) N`，内部 `acct_infos:Array Y`，逐项保留 `div_amt/huifu_id/acct_id/fee_amt`。父节点 N 时不能把子节点 Y 提升成外层永远存在。
- 顶层 `unconfirm_amt/confirmed_amt` 与金额、手续费使用独立路径；本页未声明异步通知。

SDK 三语言专属类只声明这三个请求字段。扩展映射应为空，拒绝查询原支付的替代键或未知业务字段。
