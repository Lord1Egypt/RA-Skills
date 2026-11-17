# 商户费率信息查询

## 适用范围

用于查询指定商户的微信、支付宝、银行卡或银联二维码费率配置。官方来源：[商户费率信息查询](https://paas.huifu.com/partners/api/doc/shgl/shjj/api_merchant_conf_search_cx.md)，官网更新时间 `2026-09-21`，本地活动快照 `2026-11-09`，原文 SHA-256 为 `20a3be9f505c542a716bbdad65da146f9089be05b206850c089c6df4e9ac050e`。

这是进件配置查询，不是支付订单、对账或实际手续费结算结果查询。

## 已确认的接口合同

- Endpoint：`POST https://api.huifu.com/v2/merchant/fee-rate/query`。
- 请求顶层为 `sys_id:String(32) Y`、`product_id:String(32) Y`、`sign:String(512) Y`、`data:Json Y`；响应顶层为 `sign:String(512) Y`、`data:Json N`。
- 完整目录共35个节点：请求8、同步响应27、无异步通知。完整路径、类型、长度、Y/N/C 和官方说明见 `merchant-onboarding-complete-field-catalog.md` 的“商户费率信息查询”。
- 请求 `data` 为 `req_seq_id:String(32) Y`、`req_date:String(8) Y`、`huifu_id:String(18) Y`、`fee_rate_type:Array<string>(117) N`。
- `fee_rate_type` 支持 `ALI_FEE_RATE`、`WX_FEE_RATE`、`BANK_CARD_FEE_RATE`、`UNION_FEE_RATE`；不传返回全部费率。

## 类型与方向

`fee_rate_type` 最新正式类型为 `Array<string>`，请求示例也已改为原生 JSON 数组。按数组传入官方 SDK，禁止 JSON 字符串化或二次序列化；长度列 `117` 原样保留，不推断为数组元素数量。旧版 String(JSON Array) 与单引号示例冲突已关闭。

`request.data.huifu_id:String(18) Y` 与 `response.data.huifu_id:String(18) Y` 的官方长度列均为18；请求和响应仍按各自方向建模。长度列不证明标识必须恰好18位：本次真实查询已接受汇付分配的16位商户号。原样传入真实分配值，不补零、不截断，不生成`len(huifu_id) == 18`固定长度校验。旧版请求32、响应18的长度差异已关闭，不再作为官方冲突提示。

响应的 `wx_fee_rate_list`、`ali_fee_rate_list`、`bank_card_fee_rate_list`、`union_fee_rate_list` 均按官方 jsonArray 说明解析。费率值保持字符串，不能自动换算、四舍五入或当成实际订单计费结果。

## 公共请求头

- `jpt-x-skill-source: <skill_source>` 必须按 `shared-request-header-policy.md` 生成；仅进件默认 `hfms/1.2.0`，双 Skill 默认 `hfps/1.6.0;hfms/1.2.0`。

## SDK 证据边界

在用户提供且已锁定源码树摘要的 Java `3.0.41`、PHP `2.0.31`、Python `2.0.28` 中未找到 `/v2/merchant/fee-rate/query` 的专属 Request 类或路由常量。因此：

- 不得声称三语言 SDK 已有专属类支持本接口；
- 不得用名称相近的费率或支付查询类替代；
- 可经官方 SDK 通用调用入口生成可运行代码（如 Java `BasePayClient.request(Map, funcCode, ...)` 传本接口 funcCode，内部把 `.` 替换为 `/` 拼接 URL），仍走 SDK 签名、验签、请求头与 TLS 主链路，不限于图片接口；因无类型化封装兜底，`fee_rate_type` 等字段必须逐项按本文合同构造。

字段解释和 DTO 审查仍可基于锁定官方文档完成。

## 实际网关联调与 Python 兼容边界

2026-10-10一次授权商户联调中，响应的三个费率列表实际为原生JSON数组，`union_fee_rate_list[].fee_rate_up/down` 实际为JSON数字，与上述官方String合同存在 `[需要官方确认]` 的类型差异；不能据此修改所有账号的官方DTO或在验签前归一化数据。

Python2.0.28的 `DGTools.request_post` 会先解析响应 `data` 再重序列化验签。本次四项数字的末尾0因此丢失，签名原文由1381变为1377字节，导致 `RuntimeError('Invalid signature')`。原始data使用官方辅助方法的离线验证通过，但这不授权绕过SDK消费业务结果；本版本对此响应存在实际兼容缺口。Python请求骨架可以继续生成，实际遇到验签失败必须拒绝该响应，不跳过验签、不改变数字/类型后重试猜协议。

同一配置下，Java3.0.41官方 `BasePayClient.request(params, "v2.merchant.fee-rate.query", false)` 保留BigDecimal数值，真实调用验签通过并返回业务成功；初始化前全局 `BasePay.debug=false`，保持默认TLS。需要联调可采用此已验证Java官方SDK路径；项目限定Python时，明确该接口的局部兼容缺口，等待兼容版本或确认方案，继续其他已明确接口。PHP未在本次真实网关验证，不推断其兼容性。

上述结果只证明本次测试响应；费率配置查询不证明实际扣费或支付闭环。
