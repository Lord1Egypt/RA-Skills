# 交易确认查询

官方来源：<https://paas.huifu.com/partners/api/doc/smzf/api_jyqrcx.md>。来源快照：2026-11-04；SHA-256：`da52b2f0ad6afe88d1487ee5235e6dc31e4411f4e1f3aec1b2de4c3387415526`。

接口：`/v3/trade/payment/delaytrans/confirmquery`。方法：POST。

## 使用条件与边界

- 官网当前路由为V3，使用V3TradePaymentDelaytransConfirmqueryRequest；SDK同时存在V2类，不能只按中文标题选择。

- 三个请求字段org_req_date、org_req_seq_id、huifu_id均Y；org_req_date和org_req_seq_id定位交易确认请求，而非直接用支付下单流水替换。

- 查询返回的trans_stat为P/S/F；待确认与已确认金额分别建模，保留可选字段。响应acct_split_bunch为String(JSON Array)，每个数组元素内acct_infos为Array；不能沿用确认接口的String(JSON Object)。

- 查询是补偿和状态核对入口；记录原确认流水，不能通过换流水重发确认来代替查询。

## 完整字段与SDK

完整DTO、响应或嵌套字段任务联读 `payment-extension-complete-field-catalog.md` 中的“交易确认查询”，已覆盖26条正式字段路径；仅请求定义的接口不称为已掌握完整响应。

代码任务联读 `payment-extension-sdk-matrix.md` 与 `shared-server-sdk-matrix.md`，按本项目实际SDK版本核对。只使用官方SDK的专属或通用入口，扩展字段不得覆盖已声明字段。公共请求头使用当前实际参与的Skill来源；调用方的日期、流水、账户与角色ID原样保留。
