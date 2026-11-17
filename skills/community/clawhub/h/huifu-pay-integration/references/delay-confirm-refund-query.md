# 交易确认退款查询

官方来源：<https://paas.huifu.com/navigator/ossApi/api_jyqrtkcq.json>。来源快照：2026-11-04；SHA-256：`65fa17cd59e7d18637ddb920e3e74a337d91e49821c4f96ad184538e9f9aae46`。

接口：`/v2/trade/payment/delaytrans/confirmrefundquery`。官方JSON未列HTTP方法；官方SDK使用POST。

## 使用条件与边界

- 这是JSON来源：正式data仅4字段。huifu_id、org_req_date为Y；org_req_seq_id和org_hf_seq_id为C且二选一。org_req_date指交易确认退款日期，流水亦定位确认退款，不是原支付或原确认日期。

- requestBody的isRequired=C与工具元数据required=true并存，业务执行按条件二选一。requestDemo同时填写两个定位键只是演示，不能提升为默认值或“必须都填”。

- 来源sign=true、uri明确；HTTP方法未在JSON声明。三语言官方Request使用POST，这是SDK事实。公共信封遵循共享SDK合同，不从requestDemo推导正式长度和必填。

- 该JSON未定义同步响应、响应状态和异步通知。只能交付已知请求及SDK调用，响应解析留[需要官方确认]适配点，不能从普通退款查询、确认退款响应或Lightning DTO复制字段并声称官网完整。

## 完整字段与SDK

完整DTO、响应或嵌套字段任务联读 `payment-extension-complete-field-catalog.md` 中的“交易确认退款查询”，已覆盖4条正式字段路径；仅请求定义的接口不称为已掌握完整响应。

代码任务联读 `payment-extension-sdk-matrix.md` 与 `shared-server-sdk-matrix.md`，按本项目实际SDK版本核对。只使用官方SDK的专属或通用入口，扩展字段不得覆盖已声明字段。公共请求头使用当前实际参与的Skill来源；调用方的日期、流水、账户与角色ID原样保留。
