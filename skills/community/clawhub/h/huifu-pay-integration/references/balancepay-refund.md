# 余额支付退款

官方来源：<https://paas.huifu.com/partners/api/doc/yuer/api_acctpaytk.md>；快照 `2026-11-04`，官网更新时间 `2025-02-25`。

接口：`POST /v2/trade/acctpayment/refund`。适用于已开通退款权限的余额支付交易；完整44个字段路径见 `payment-complete-field-catalog.md` 的“余额支付退款”，联读 `balancepay-field-contracts.md`。

## 请求与限制

- 新退款 `req_seq_id:String(128)`、`req_date:String(8)`，发起方 `huifu_id:String(32)`、原支付 `org_req_date:String(8)`、退款 `ord_amt:String(14)` 必填。保留调用方已分配的退款幂等流水，不能用支付流水替换。
- `org_req_seq_id` 和 `org_hf_seq_id` 各 String(128)、C，二选一定位原支付。正文误写 `orgReqSeqId`，wire 仍只用正式蛇形字段名。
- `acct_split_bunch` 可选，发送一层 String(JSON Object)；其中 `acct_infos:Array Y`，子项 `div_amt:String(14) Y`、`huifu_id:String(32) Y`。支持多个入账方退款，每个退款金额不能超过原入账金额；分账退款总额与退款订单金额按本页业务返回码说明核对。
- `risk_check_data` 为可选 String(JSON Object)，内部 `transfer_type:String(2) Y` 仅声明01至05；不能从余额支付复制06灵活用工枚举。
- 原支付未成功、权限未开通或超出可退余额时不能退款；不把查询未知视作退款许可。

## 响应与查询

`trans_stat=P/S/F`；处理中转到 `balancepay-refund-query.md`。同步 `acct_split_bunch` 为 String(JSON Object)，其中金额、账户、手续费均按父路径保留；退款返回的 `hf_seq_id:String(40)` 与支付流水长度128不共用 DTO 限制。

本页未声明异步通知，不编造退款 notify_url 或 ACK。

## 待确认项

正式请求支持 `org_hf_seq_id` 二选一，但业务返回码23000004描述“暂不支持通过全局流水号退款”。保留冲突；仅有全局流水时提醒核对官方，已拥有原请求流水的明确分支可继续。重复交易返回码20000000的建议不能自动转成重新生成退款流水并重放资金操作，先查原退款。
