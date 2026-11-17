# 余额支付查询

官方来源：<https://paas.huifu.com/partners/api/doc/yuer/api_acctpaycx.md>；快照 `2026-11-04`，官网更新时间 `2026-09-21`。

接口：`POST /v2/trade/acctpayment/pay/query`。查询单笔余额支付的状态及明细；完整36个字段路径见 `payment-complete-field-catalog.md` 的“余额支付查询”，联读 `balancepay-field-contracts.md`。

## 定位原支付

- `huifu_id:String(32) Y` 是发起方商户号；不得换成分账接收方或自动使用出款方。
- `org_req_date:String(8) Y` 是原支付日期，格式 yyyyMMdd。
- `org_req_seq_id:String(128) N` 与 `org_hf_seq_id:String(128) N` 正文要求二选一；不能因为表格 N 就同时省略。官方未定义同时填写的优先级，按二选一构造，不补双键选择规则。
- 本接口未声明新的 `req_date/req_seq_id`；不要从其他查询接口复制请求定位字段。

## 响应与补偿

`resp_code=00000000` 是查询成功，业务结果取 `trans_stat`：P处理中、S成功、F失败、C完成（灵活用工特有）。C 时检查 `acct_split_bunch.acct_infos[].trans_stat`；不把一项成功或总状态 C 写成全部成功。

`acct_split_bunch:String(JSON Object) N`，其中 `acct_infos` 为 Array；子项含分账金额、入账方、分账状态、手续费、未确认金额。`unconfirm_amt/confirmed_amt` 顶层与各子项同名字段分路径建模。响应 `fee_amt` 位于分账父对象内，不提升到响应顶层。

本页未声明异步通知。查询用于处理中、通知未到或请求结果未知的补偿，保存原交易定位，重试查询不等同重新支付。

新接入支付废弃发起方 `huifu_id` 与查询仍必填该角色的衔接值必须来自已确认的账户/历史交易上下文，未知时留配置项，不猜等于 `out_huifu_id`。
