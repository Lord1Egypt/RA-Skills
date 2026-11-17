# 账户余额信息查询

官方来源：<https://paas.huifu.com/partners/api/doc/jyjs/api_jyjs_yuexxcx.md>。来源快照：2026-11-04；SHA-256：`4684913f1338f44423f025d72a73b7012e477dd48ec82b3a9216340571f6d39e`。

接口：`/v2/trade/acctpayment/balance/query`。方法：POST。

## 使用条件与边界

- 用于查询商户各类账户余额；商户须已完成进件或业务入驻创建账户，具体开户/子账户配置实施交给进件Skill。

- req_date和huifu_id均Y；req_seq_id正式N且只用于定位查询请求，不能因SDK流水生成行为把它改成必填。acct_date为N，默认当天；账务日期与请求日期分开保留。

- 只读账务返回不能替代支付、确认或退款的订单状态查询；金额按正式类型读取，不用浮点计算或把账户总额解释为某笔交易成功。

- 同步data及账户列表的类型、长度和分层路径见完整目录；仅输出本次需要的账户信息，日志和演示结果脱敏。

## 完整字段与SDK

完整DTO、响应或嵌套字段任务联读 `payment-extension-complete-field-catalog.md` 中的“账户余额信息查询”，已覆盖26条正式字段路径；仅请求定义的接口不称为已掌握完整响应。

代码任务联读 `payment-extension-sdk-matrix.md` 与 `shared-server-sdk-matrix.md`，按本项目实际SDK版本核对。只使用官方SDK的专属或通用入口，扩展字段不得覆盖已声明字段。公共请求头使用当前实际参与的Skill来源；调用方的日期、流水、账户与角色ID原样保留。
