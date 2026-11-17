# 个人用户基本信息修改

## 适用范围

维护渠道商或商户开通的个人分账用户、快捷交易用户资料。官方来源：[个人用户基本信息修改](https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_gryhjbxxxg.md)。本接口不是个人商户进件，也不是企业用户修改。

## 接口与字段面

- Endpoint：POST https://api.huifu.com/v2/user/basicdata/indv/modify。
- 官网更新时间：2026-09-04；本地活动快照：2026-11-09；原文 SHA-256：b1495f896cfc12f8e8324c8aa1f97655c0c87d41c626ea636eda54b7b3aa741c。
- 共26个字段路径：请求21、同步响应5、异步0；4个根表、1个扩展表、3个父节点、23个叶节点。完整字段读取 user-onboarding-complete-field-catalog.md。
- 定位字段是 req_seq_id:String(32) Y、req_date:String(8) Y、huifu_id:String(18) Y；流水要求同一商户号当天唯一，日期按北京时间 yyyyMMdd。

## 请求号角色冲突

接口标题、中文名和 request.data.huifu_id 说明现已统一指向渠道与一级代理商的直属汇付客户 ID；按个人用户号定位，不再保留旧版商户号角色硬停。

## 修改字段

- 证件有效期：cert_validity_type:String(1) N 正式枚举只有 1=长期有效、0=非长期有效；非长期有效时按业务完整性同时传开始、截止日期。当前请求示例已修正为 `1`。
- 联系资料：email:String(64) N、mobile_no:String(11) N；手机号说明要求11位数字。
- file_list:String N 的说明为 jsonArray，wire 发送 String(JSON Array)。子项 file_type:String(8) Y、file_id:String(64) Y、file_name:String(64) N；注意本页两个文件字段长度均为64，不能复制企业修改页的128。
- address:String(256) N 在开通中信E管家或电子回单时说明要求必填。
- mcc:String(7) N 及省市区均在“用户业务入驻修改且电子回单开通”时说明要求填写；该条件属于另一个接口的组合流程，不得在本接口无条件提升为必填。
- prov_id/area_id/district_id 都是 String(6) N，修改省市区时必须级联修改；不能复制企业修改页的6/8/12长度。
- 本页没有清空字段、部分更新保持原值或异步通知语义；空字符串不解释为删除，提交后用用户信息查询核对结果。

## SDK 边界

已核验源码基线 Java 3.0.41、PHP 2.0.31、Python 2.0.28 都使用 V2UserBasicdataIndvModifyRequest，精确路由 /v2/user/basicdata/indv/modify。三语言生成类恰好只声明 req_seq_id/req_date/huifu_id；其余14个正式请求字段通过 exact-key 扩展映射传入。

Java putAll、PHP array_merge、Python dict.update 都会后写覆盖声明字段。接入层必须拒绝扩展中的 req_seq_id/req_date/huifu_id，只允许本页正式可选键，拒绝未知键、响应键与包络键。file_list 在扩展中仍是一层 JSON Array 字符串。

## 响应与安全

外层 response.data:Json N；业务对象包含 resp_code:String(8) Y、resp_desc:String(512) Y、huifu_id:String(18) N。当前成功示例已包含 response.sign:String(512) Y，必须验签。手机号、邮箱、地址和文件标识必须脱敏，禁止完整日志或前端回显。
