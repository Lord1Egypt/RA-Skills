# 用户列表查询

## 适用范围

通过法人证件号查询用户列表，可用可选的上级汇付 ID 缩小范围。官方来源：[用户列表查询](https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_yhlbcx.md)。这是用户查询接口，不得与商户详情、申请单状态或单个用户信息查询共用 DTO。

## 接口与字段面

- Endpoint：`POST https://api.huifu.com/v2/user/list/query`。
- 官网更新时间：`2026-09-04`；本地活动快照：`2026-11-09`；原文 SHA-256：`b10ab1529c58d5739cae0f38b5f385a105e3f2d6b3348400f6882328b7421d9d`。
- 共17个完整字段路径：请求8、同步响应9、无异步通知；4个根表、1个扩展表、3个父节点、14个叶节点。完整字段读取 `user-onboarding-complete-field-catalog.md`。
- 请求必填 `legal_cert_no:String(32)`、`req_date:String(8)` 和 `req_seq_id:String(32)`；`upper_huifu_id:String(18) N` 不传时不得自行填充当前用户号或商户号。

## 官方冲突与响应边界

- 当前正式参数表把 `response.data.user_list_info_list` 定义为 `String N` 并注明 `jsonArray格式`；响应模型按一层 String(JSON Array) 解码，并保留 `response.data.user_list_info_list[]` 子路径。成功示例使用原生数组，与正式类型冲突，不能静默覆盖。
- 当前正式表已把 `response.data.user_list_info_list[].huifu_id` 与 `response.data.user_list_info_list[].upper_huifu_id` 修正为 `String(18) N`，与16位成功示例兼容；校验上限为18，禁止沿用旧版长度2。
- 当前请求示例和成功响应示例均已包含正式必填的 `sign:String(512) Y`。示例中的签名值不是固定值；真实请求仍须加签，真实响应仍须验签。
- `cust_type:String(2) N` 只使用官网明示的 `1=企业用户` 和 `2=个人用户`；不得从商户主体类型枚举外推。

## SDK 边界

已核验源码基线 Java `3.0.41`、PHP `2.0.31`、Python `2.0.28` 都使用 `V2UserListQueryRequest`，精确路由 `/v2/user/list/query`。三语言生成类恰好只声明 `legal_cert_no/req_date/req_seq_id`，可选 `upper_huifu_id` 通过白名单 exact-key 扩展传入。

Java `putAll`、PHP `array_merge`、Python `dict.update` 都会让扩展值覆盖已声明字段，因此扩展必须拒绝 `legal_cert_no/req_date/req_seq_id`，仅允许官网已声明但 SDK 未生成的 `upper_huifu_id`。三语言都必须用脱敏运行探针验证路由、扩展合并和覆盖拒绝策略。

## 安全

`legal_cert_no`、用户名称和两类汇付 ID 不得写日志、前端或回答示例。本接口无通知表，不得生成 webhook、ACK 或幂等回调逻辑。
