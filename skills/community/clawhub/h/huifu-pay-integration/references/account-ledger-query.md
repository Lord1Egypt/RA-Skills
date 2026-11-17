# 账务流水查询

官方来源：<https://paas.huifu.com/partners/api/doc/yuer/api_acctlscx.md>。来源快照：2026-11-04；SHA-256：`46295c022efcc9464472d396cfe4c2befd74ba634a8c6f02e183fe1f99dd30c2`。

接口：`/v2/trade/acctpayment/acctlog/query`。方法：POST。

## 使用条件与边界

- huifu_id可属于渠道、代理、商户或用户；必须根据调用目标保留角色和原始字符串，不能固定解释为商户或将平台分配ID补零。

- 请求没有req_date字段；req_seq_id、huifu_id、acct_date正式Y。page_size最大100、默认10，page_num默认1；last_end_log_id与page_num不能同时为空。

- 使用last_end_log_id游标时acct_id必填，page_num无需传，首次游标0。hf_seq_id传入时优先按全局流水查询，分页和账务日期条件失效；acct_date正式Y仍保留，不因查询优先级自行改成N。

- 单日最多查询10000条，超过时联系技术支持获取账务文件；不能声称循环翻页即可无限获取。acct_type支持01/02/03/05/09，未填默认01；无acct_id时默认基本户。

- 这是账务明细，不是支付订单状态。同步容器、流水列表和入出账类型按完整目录和页面表外枚举处理，保留敏感账户与对手信息的脱敏边界。

## 完整字段与SDK

完整DTO、响应或嵌套字段任务联读 `payment-extension-complete-field-catalog.md` 中的“账务流水查询”，已覆盖40条正式字段路径；仅请求定义的接口不称为已掌握完整响应。

代码任务联读 `payment-extension-sdk-matrix.md` 与 `shared-server-sdk-matrix.md`，按本项目实际SDK版本核对。只使用官方SDK的专属或通用入口，扩展字段不得覆盖已声明字段。公共请求头使用当前实际参与的Skill来源；调用方的日期、流水、账户与角色ID原样保留。
