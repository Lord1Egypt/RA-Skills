# 商户状态变更

## 适用范围

用于渠道商发起直属商户状态开通或关闭申请。官方来源：[商户状态变更](https://paas.huifu.com/partners/api/doc/shgl/api_shgl_shztbg.md)，锁定来源 SHA-256 为 `d2fe6ab4404abd79b3ac5f5eecffaaec9d61d245ac1a60ebccddee889535a07f`。

关闭状态会影响商户资金、交易和控台登录，属于高风险管理操作；必须由调用方明确确认目标商户、目标状态和原因。

## 已确认的接口合同

- Endpoint：`POST https://api.huifu.com/v2/merchant/busi/modify/busistatus`。
- 请求顶层为 `sys_id:String(32) Y`、`product_id:String(32) Y`、`sign:String(512) Y`、`data:Json Y`；同步响应顶层为 `sign:String(512) Y`、`data:Json N`。
- 完整目录共14个节点：请求9、同步响应5、无异步通知。完整路径、类型、长度、Y/N/C 和官方说明见 `merchant-onboarding-complete-field-catalog.md` 的“商户状态变更”。
- 请求 `data` 精确包含 `req_date:string(8) Y`、`req_seq_id:string(32) Y`、`huifu_id:String(18) Y`、`status:String(1) Y`、`upd_status_reason:String(512) Y`。
- `status` 仅允许字符串 `1=开通`、`0=关闭`；官方说明支持关闭后再次打开。
- 同步响应 `data` 包含 `resp_code:String(8) Y`、`resp_desc:String(512) Y`、`apply_no:String(128) N`。

## 被官方注释删除的字段

官方原文把 `file_list` 及其 `file_type/file_id/file_name` 子表放在一段多行 HTML 注释内，并写明该字段不要。因此这四个路径不属于当前接口合同：

- 禁止生成 `request.data.file_list`；
- 禁止生成其任何子字段；
- 不得因源码中还能看到注释文本就把它恢复为可选字段。

## 状态与审核边界

- 同步返回申请单号不表示状态已经生效。
- 官网页面要求通过申请单状态查询获取审核状态；后续使用 `merchant-onboarding-application-status-query.md`。
- 不得把本接口状态 `0/1` 与业务开通的 `Y/N`、详情查询配置的 `0/1/空` 或支付订单状态混用。
- 关闭商户是高风险动作；生成可运行请求前必须再次确认目标 `huifu_id`、`status`、真实原因、权限和影响范围。

## 公共请求头

- `jpt-x-skill-source: <skill_source>` 必须按 `shared-request-header-policy.md` 生成；仅进件默认 `hfms/1.2.0`，双 Skill 默认 `hfps/1.6.0;hfms/1.2.0`。

## SDK 证据

用户提供且已锁定源码树摘要的 Java `3.0.41`、PHP `2.0.31`、Python `2.0.28` 均存在对应封装：

- Java / PHP：`V2MerchantBusiModifyBusistatusRequest`
- Python：`V2MerchantBusiModifyBusistatusRequest`，模块 `v2_merchant_busi_modify_busistatus_request.py`

SDK 类存在不证明调用方有变更权限，也不改变审核语义。Java 代码仍必须在任何 SDK 请求前全局设置 `BasePay.debug = false;`。
