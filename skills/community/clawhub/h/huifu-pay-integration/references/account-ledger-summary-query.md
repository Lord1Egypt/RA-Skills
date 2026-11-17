# 账务流水汇总结果查询

官方来源：<https://paas.huifu.com/partners/api/doc/zhy/api_acct_log_summary.md>。来源快照：2026-11-04；SHA-256：`d70d62be96cb1c20ba9be2355a57c8890468e8eab20e8adf2a81933e684e771a`。

接口：`/v2/trade/acctpayment/acctlog/summary`。方法：POST。

## 使用条件与边界

- 用于历史账务流水汇总，正文写明异步virgo返回结果。正式请求req_seq_id、req_date、huifu_id、acct_id、开始/截止时间、notify_url均Y；页面示例漏req_date，不能照抄。

- 查询窗口目前限七天，时间格式yyyy-MM-dd HH:mm:ss。文档示例边界是否含端点不能直接推广成通用时区或查询日规则，按业务实际范围保守校验并记录待确认项。

- [需要官方确认]：正文称异步结果，但字段表置于“同步返回参数”；来源没有独立异步信封、验签原文、ACK、超时或重试表。目录保留原正式章节，不把同步受理视为汇总完成，也不凭notify_url拼装通用支付Webhook。

- summary_list正式String/jsonArray而示例为原生数组，且示例含中文逗号和尾逗号，不是可直接执行的JSON。保留正式字段与示例冲突；total_summary_amt长度8与子项summary_amt长度14分别保留。

- 当前锁定三语言SDK未找到专属Request/路由常量，使用经过核验的官方通用入口，按正式字段构造映射；不虚构V2TradeAcctpaymentAcctlogSummaryRequest，不改写HTTP或关闭签验。

## 完整字段与SDK

完整DTO、响应或嵌套字段任务联读 `payment-extension-complete-field-catalog.md` 中的“账务流水汇总结果查询”，已覆盖25条正式字段路径；仅请求定义的接口不称为已掌握完整响应。

代码任务联读 `payment-extension-sdk-matrix.md` 与 `shared-server-sdk-matrix.md`，按本项目实际SDK版本核对。只使用官方SDK的专属或通用入口，扩展字段不得覆盖已声明字段。公共请求头使用当前实际参与的Skill来源；调用方的日期、流水、账户与角色ID原样保留。
