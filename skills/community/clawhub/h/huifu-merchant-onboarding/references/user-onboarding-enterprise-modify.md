# 企业用户基本信息修改

## 适用范围

修改已经存在的企业用户基础资料。官方来源：[企业用户基本信息修改](https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_qyyhjbxxxg.md)。本接口不是 `/v2/merchant/basicdata/modify` 商户基本信息修改；请求 `huifu_id` 当前已明确为直属汇付企业用户 ID。

## 接口与字段面

- Endpoint：`POST https://api.huifu.com/v2/user/basicdata/ent/modify`。
- 官网更新时间：`2026-09-04`；本地冻结：`2026-11-09`；原文 SHA-256：`bb0b2a7339463d9731243e7d91ec9bfd729180d844646bb119b68655a11a5df8`。
- 共37个字段路径：请求32、同步响应5、异步0；4个根表、1个扩展表、3个父节点、34个叶节点。完整类型、长度、Y/N/C 与说明读取 `user-onboarding-complete-field-catalog.md`。
- 请求定位字段为 `req_date:String(8) Y`、`req_seq_id:String(32) Y`、`huifu_id:String(18) Y`；响应业务字段为 `resp_code:String(8) Y`、`resp_desc:String(512) Y`、`huifu_id:String(18) N`。

`request.data.huifu_id` 的中文名和说明现已统一指向渠道与一级代理商的直属汇付客户 ID；`response.data.huifu_id` 中文名也已明确为“汇付企业用户ID”。本接口按企业用户号定位，不再保留旧版商户号角色硬停。

## 修改规则

- 可修改企业名称、简称、公司类型、法人、管理员、证照有效期、注册地址、材料和 MCC；可选字段不能用空字符串表达“删除”，因为官网没有定义清空语义。未提交字段是否保持原值也未明示，调用前应以用户详情查询确认现值并仅传确定要修改的字段。
- 修改企业名称前必须联系汇付运营加入白名单，否则官网说明会校验失败。
- 官网页内注意明确：修改法人证件时，`legal_cert_type`、`legal_cert_validity_type`、`legal_cert_begin_date`、`legal_cert_end_date` 必须同步填写。该组合要求绑定到四个完整路径，不得只更新证件号码或只补其中一个有效期字段。
- `legal_cert_validity_type=1` 表示长期有效，`0` 表示非长期有效；长期有效时 `legal_cert_end_date` 可不填。法人证件为外国人居留证时，`legal_cert_nationality:String(50) C` 必填。
- `file_list:String N` 的说明为 jsonArray，wire 使用 String(JSON Array)；子项 `file_type:String(8) Y`、`file_id:String(128) Y`，`file_name:String(128) N`。不得因目录路径带 `[]` 就改发原生数组。
- `mcc:String(7) N` 的说明仍写“用户业务入驻修改、电子回单配置开通时需填写”。该条件涉及另一个修改接口，不能把 `mcc` 在本接口无条件提升为必填。
- 本页没有异步通知字段；不得补 `async_return_url`，也不得套用用户业务入驻回调合同。

## SDK 边界

已核验源码基线 Java `3.0.41`、PHP `2.0.31`、Python `2.0.28` 均使用 `V2UserBasicdataEntModifyRequest`，精确路由为 `/v2/user/basicdata/ent/modify`。三语言生成类只显式声明 `req_date`、`req_seq_id`、`huifu_id`、`legal_cert_nationality`；其余官方可选字段通过 exact-key 扩展映射传入。

扩展映射在 Java `putAll`、PHP `array_merge`、Python `dict.update` 中后合并，会覆盖同名显式字段。因此接入层必须先拒绝扩展中的 `req_date`、`req_seq_id`、`huifu_id`、`legal_cert_nationality`，再只允许本页正式请求 `data` 中的其他键；未知键、响应键和包络键全部拒绝。`file_list` 在扩展中仍传已经序列化的一层 JSON Array 字符串。

## 同步响应与安全

外层 `response.data:Json` 的官网必填列为 `N`；成功示例返回原生对象并包含企业用户 `huifu_id`。先验签再解析；成功缺少 `data` 或 `resp_code` 按协议异常处理，异常响应 DTO 仍允许 `data` 缺失。法人证件号、手机号、邮箱、地址和文件标识按高敏资料脱敏，禁止完整日志和前端回显。
