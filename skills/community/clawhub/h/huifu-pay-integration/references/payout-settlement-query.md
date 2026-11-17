# 结算记录查询

官方来源：<https://paas.huifu.com/partners/api/doc/jyjs/qx/api_jsjlfycx.md>。来源快照：2026-11-04；SHA-256：`d04126694730c33755a50bd8600314c387f807d6ddec44bcbb0854c6411fd4c2`。

接口：`/v2/merchant/basicdata/settlement/query`。方法：POST。

## 归属与查询条件

虽路由和SDK类含merchant，本接口查询资金结算记录，归支付Skill。只有需要更改商户结算/绑卡配置时联用进件Skill；不能仅凭URL前缀加载进件。请求huifu_id正式String(18) Y，限定渠道与一级代理商的直属商户ID，不能任填用户号、代理自身或下级非直属商户。

`req_seq_id`、`req_date`、`huifu_id`、`begin_date`、`end_date`、`page_size` 正式Y；page_size范围1..50，page_num默认1，settle_cycle可D1/T1。正文“查询100天内”与结束日期说明“开始和结束日期需小于等于7天”分别保留，可能是历史回看与单次窗口的区别；[需要官方确认]，不能据此生成单次100天窗口。

## 编码与状态

`response.data.trans_log_result_list[]` 正式String(JSON Array)，示例为原生数组。保留String的wire父字段及解码后数组路径，不静默把正式类型改Array；批量出金查询的正式Array是另一合同。分页计数正式String、示例数字，不默认改类型。

请求过滤 `trans_stat` 支持I/S/F/P，P为处理中(锁定)；响应条目只声明I/F/S，为空则未返回状态，不从请求过滤枚举补造响应P。不把结算成功等同某笔支付成功。

## 结算完成Webhook

本接口官方页明确：结算完成后发送控台Webhook事件 `statement.day`，可配置多个接收端。事件来源见[结算通知事件](https://paas.huifu.com/open/doc/devtools/#/webhook/mb_jiesuan)及[Webhook使用说明](https://paas.huifu.com/open/doc/devtools/#/webhook/webhook_jieshao?id=%e5%a6%82%e4%bd%95%e4%bd%bf%e7%94%a8webhook)。这是结算事件线索，不是本查询接口额外返回的字段，也不等同取现/代发的notify_url回调。

本次冻结的查询页没有展开该事件的字段表；事件payload、签名和ACK需核对对应事件文档后实现，当前36条查询字段不包含完整Webhook合同，不从支付或取现通知拼接字段。

## 完整字段与SDK

单字段类型/必填、完整DTO或同步响应字段均按接口与方向读取 `payment-extension-complete-field-catalog.md` 中的“结算记录查询”，覆盖36条正式字段路径。代码任务联读 `payment-extension-sdk-matrix.md` 与 `shared-server-sdk-matrix.md`；专属类 `V2MerchantBasicdataSettlementQueryRequest`，Python模块 `v2_merchant_basicdata_settlement_query`。扩展字段先拒绝覆盖SDK已声明字段，再经官方SDK发送；SDK合并本身不提供此保护。日期、流水、金额、账户和角色ID保持调用方值，来源头按实际参与的Skill确定。
