# 个人用户开户

## 适用范围

服务商或商户为旗下自然人建立分账/结算用户。官方来源：[个人用户基本信息开户](https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_gryhjbxxzc.md)。它不是无执照个人商户进件；实体不明时先触发硬停。

## 接口与字段面

- Endpoint：`POST https://api.huifu.com/v2/user/basicdata/indv`。
- 快照更新时间：官网 `2026-10-21`，本地冻结 `2026-11-09`；原文 SHA-256：`41f9a75dab6ff2d157ff9f02793afa1ada3baec8f0d67664bed8c1ad08e53bf2`。
- 共34个字段路径：请求27、同步响应7、异步0。完整字段读取 `user-onboarding-complete-field-catalog.md`。
- 请求业务 `data` 没有 `huifu_id`、`upper_huifu_id` 或异步地址。

## 请求合同

- 必填主字段为流水、日期、姓名、证件类型/号码、证件有效期类型/开始日和手机号。
- `cert_end_date:String(8)` 的必填列为 `N`，说明明确“长期可不填，非长期必填”；保留该官网冲突并执行条件校验。
- 外国人居留证触发 `cert_nationality`；不得把示例国籍当默认值。
- `sms_send_flag` 只使用 `Y/N`，默认不发送；当前官网请求示例已使用 `"Y"`。
- `address` 在开通中信E管家或电子回单时必填。`mcc/prov_id/area_id/district_id` 的必填列为 `N`，但当用户业务入驻修改且电子回单配置开通时说明要求填写；省市区需要级联修改。
- `file_list:String N` 的说明为 jsonArray；wire 发送一层 String(JSON Array)，不得因请求示例使用原生数组而覆盖正式类型。官网另在表外注明：证件类型为身份证时，会对姓名和身份证号做实名认证。
- 当前示例已删除旧版参数表外 `operator_id`；正式 DTO 仍只允许参数表字段。

## 同步响应

响应结构与企业用户开户相同：外层 `response.data:Json` 的官网必填列为 `N`，接入方确认成功响应一定包含该对象；成功缺失按协议异常，异常响应 DTO 仍允许缺失。对象中包含业务码、描述，并可能返回 `huifu_id`、`login_name` 和初始 `login_password`。将 `huifu_id` 建模为 `userHuifuId`；初始密码按一次性高敏凭据处理。

公共响应表将 `sign:String(512)` 标为 `Y`，当前成功示例已包含 `sign`；同步响应必须验签。

官网未声明异步通知。不得生成回调、轮询推断或复用企业/商户开户通知。

## SDK 边界

三语言锁定版本均有 `V2UserBasicdataIndvRequest`。生成类对 `cert_nationality/address` 等字段的 required/空串建模不覆盖官方 Y/N/C；三语言联调和生产实现均使用对应官方 SDK，PHP 另受 DEBUG 硬停约束。

## 2026-10-25 官网更新同步

本地当前来源SHA-256：`41f9a75dab6ff2d157ff9f02793afa1ada3baec8f0d67664bed8c1ad08e53bf2`。

新增公共请求字段sys_id的上下级关系说明：sys_id为总部商户时在开户阶段绑定关系，否则在业务入驻阶段按upper_huifu_id绑定。该注记属于request.sys_id，不向开户data添加upper_huifu_id，也不混淆sys_id与用户ID。
