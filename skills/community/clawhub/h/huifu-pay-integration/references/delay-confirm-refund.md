# 交易确认退款

官方来源：<https://paas.huifu.com/partners/api/doc/smzf/api_jyqrtk.md>。来源快照：2026-11-04；SHA-256：`e740c12c8884f7f5ec242f0e1a053530f37ce2cd24418924b3f9f9a819c7f9ad`。

接口：`/v2/trade/payment/delaytrans/confirmrefund`。方法：POST。

## 使用条件与边界

- 用于交易确认成功后，将已确认订单金额退回原商户账户，属于确认分配资金的退回；该接口结果不能直接标记为付款人已收到退款。向付款人退款仍需按原支付产品的退款合同另行处理，不自动串联真实退款操作。

- org_req_date、org_req_seq_id均为交易确认请求的日期和流水，两个字段均Y，不能使用普通支付退款的定位规则。同步响应中的org_req_date说明却称支付交易业务请求时间，保留方向语义差异与[需要官方确认]。

- 请求没有ord_amt字段；退款分配在acct_split_bunch的acct_infos数组中按接收方、div_amt表达，不能复制普通退款顶层金额。该父字段正式N，是否省略须按业务目标和官方说明核对。

- div_amt和part_loan_amt单位元、两位小数、最低0.01。loan_flag为空默认N；loan_undertaker为空时各自承担，第三方垫资方必须参与原分账；loan_acct_type为01基本户或05充值户，默认充值户。

- 同步trans_stat为P/S/F；官网成功示例缺公共响应签名，不能因此关闭SDK验签。来源无独立退款通知表，不复制支付通知协议。

## 完整字段与SDK

完整DTO、响应或嵌套字段任务联读 `payment-extension-complete-field-catalog.md` 中的“交易确认退款”，已覆盖45条正式字段路径；仅请求定义的接口不称为已掌握完整响应。

代码任务联读 `payment-extension-sdk-matrix.md` 与 `shared-server-sdk-matrix.md`，按本项目实际SDK版本核对。只使用官方SDK的专属或通用入口，扩展字段不得覆盖已声明字段。公共请求头使用当前实际参与的Skill来源；调用方的日期、流水、账户与角色ID原样保留。
