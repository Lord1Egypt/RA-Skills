# 商户基本信息修改

## 适用范围

用于已进件商户修改主体、证照、联系人、结算、协议、受益人、股东或其他基础资料。官方来源：[商户基本信息修改](https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shjbxxxg_kyc.md)，官网更新时间 `2026-09-20`，本地活动快照 `2026-11-09`，原文 SHA-256 为 `f2146bc553eb4b1dc8c88d4487eb1b5c721468d6a8eec5be7d0ce9f086db4d6c`。

该接口不是企业/个人首次进件。修改资料可能重新进入审核，不能把同步响应成功解释为资料审核完成或已经具备支付能力。

## 已确认的接口合同

- Endpoint：`POST https://api.huifu.com/v2/merchant/basicdata/modify`。
- 请求顶层为 `sys_id:String(32) Y`、`product_id:String(32) Y`、`sign:String(512) Y`、`data:Json Y`；同步响应顶层为 `sign:String(512) Y`、`data:Json N`。
- 完整目录共199个节点：请求 164、同步响应 7、异步通知 28。12 组嵌套表、完整路径、类型、长度、Y/N/C 和官方说明见 `merchant-onboarding-complete-field-catalog.md` 的“商户基本信息修改”。
- 请求定位字段包括 `data.req_seq_id:String(32) Y`、`data.req_date:String(8) Y`、`data.upper_huifu_id:String(18) C`、`data.huifu_id:String(18) Y`。`upper_huifu_id` 在 `sys_id` 主体为渠道商时填写，总部商户主体时选填。
- 官方原文明确存在相互依赖和不可同时修改的资料。生成请求前必须读取完整字段说明，不能只凭字段名或首次进件 DTO 猜测修改规则。

## 高风险修改边界

- 结算卡、证照、法人、受益人、股东、联系人和图片资料均为敏感信息，不得写入日志、示例或前端常量。
- `data.async_return_url:String(128) N` 是审核结果地址；电子协议通知使用独立的 `async.agreement.*` 方向。
- 审核通知 `async.audit.data.audit_status`、电子账户结果和电子协议 `con_stat` 是不同状态；不得压成一个“修改成功”布尔值。
- 电子协议通知父字段只定义为 `String`；本接口完整状态路径是 `async.agreement.agreement_info_list.con_stat`，不是申请状态查询的 `response.data.agreement_info_list[].con_stat`。
- 同步响应中的 `apply_no` 用于后续申请状态查询；同步返回 `huifu_id` 不代表审核或业务开通完成。
- 修改结算卡涉及短信验证时，短信获取或核验使用独立的 `merchant-onboarding-sms-send.md`，不能虚构验证码或在本接口里猜填。

## 字段生成规则

1. 从完整字段目录按“请求方向 + 完整路径”选择本次确需修改的字段。
2. 对每个父对象读取所有相关叶子及 Y/N/C 条件；String(JSON) 对象先校验叶子再序列化。
3. `data.prov_id/area_id` 是经营省市，`data.card_info.prov_id/area_id` 是银行所在省市；不得按叶字段名合并或遗漏。修改其中一组时只更新对应父路径；本接口 `card_info.area_id` 为 `String(8) Y`，不能套用企业/个人进件的 `String(6) Y`。
4. 图片字段只接受调用方提供并经图片上传获得的真实材料标识；不得复用官网示例或其他商户材料。
5. 官网页面的例值、商户号、证件号、手机号、银行卡号和文件标识都不是默认值。
6. `data.activated_products` 只允许 `01=一体化收款产品`、`02=账户与资金产品`、`03=业财数通产品`；多值沿用官网格式，不传为空。
7. 命中外部编码、文件类型、协议或材料说明时读取 `merchant-onboarding-external-resources.md`，未读取外部正文时要求人工核验。

## 公共请求头

- `jpt-x-skill-source: <skill_source>` 必须按 `shared-request-header-policy.md` 生成；仅进件默认 `hfms/1.2.0`，双 Skill 默认 `hfps/1.6.0;hfms/1.2.0`。

## SDK 证据

用户提供且已锁定源码树摘要的 Java `3.0.41`、PHP `2.0.31`、Python `2.0.28` 均存在对应封装：

- Java / PHP：`V2MerchantBasicdataModifyRequest`
- Python：`V2MerchantBasicdataModifyRequest`，模块 `v2_merchant_basicdata_modify_request.py`

SDK 只提供路由与传输证据，不替代资料修改条件和审核判断。Java 代码仍必须在任何 SDK 请求前全局设置 `BasePay.debug = false;`。

## 通知边界

审核与电子协议通知的 ACK、验签原文、HTTP 编码、超时和重试均为 `[需要官方确认]`。不得套用支付通知或业务开通逐业务通知的 `RECV_ORD_ID_` 规则。
