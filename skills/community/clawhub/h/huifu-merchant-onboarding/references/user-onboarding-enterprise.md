# 企业用户开户

## 适用范围

服务商或商户为旗下企业用户开户，使其可使用多方分账与结算。官方来源：[企业用户基本信息开户](https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_qyyhjbxxzc.md)。本接口不是企业商户进件；如果目标主体需要收单或支付渠道能力，切换到本 Skill 的 `/v2/merchant/*` 商户路由。

## 接口与字段面

- Endpoint：`POST https://api.huifu.com/v2/user/basicdata/ent`。
- 快照更新时间：官网 `2026-10-21`，本地冻结 `2026-11-09`；原文 SHA-256：`9ae70289683601611a7e9e675c382778e8447b48786ded16a345460ab630c476`。
- 共43个字段路径：请求36、同步响应7、异步0。完整路径、类型、长度、必填性和说明读取 `user-onboarding-complete-field-catalog.md`。
- 请求业务 `data` 不包含 `huifu_id`、`upper_huifu_id` 或异步地址；不得为请求头或 SDK 填充虚构字段。

## 请求分组

| 分组 | 核心字段与约束 |
| --- | --- |
| 流水 | `req_seq_id:String(32) Y`、`req_date:String(8) Y`，日期格式 `yyyyMMdd` |
| 企业证照 | 企业名称、18位营业执照编号、有效期类型及起止日；非长期有效时结束日必填 |
| 注册地址 | `reg_prov_id:String(6)`、`reg_area_id:String(8)`、`reg_district_id:String(12)` 和详细地址均必填 |
| 法人 | 姓名、证件类型/号码、有效期；系统执行姓名与证件实名认证；外国人居留证触发国籍 |
| 管理员 | 姓名和手机号必填；邮箱可选；短信通知或升级LV3时 `login_name` 必填 |
| 材料 | `file_list:String(JSON Array)`；子项 `file_type/file_id` 必填，`file_name` 可选，校验后整体序列化一层 |
| 业务补充 | `ent_type` 当前Y必填，扩展方和操作员仍按自身N/C条件处理；`mcc` 必填列为 N，但用户业务入驻修改且电子回单配置开通时说明要求填写 |

`sms_send_flag` 正式值域为 `Y/N`，默认不发送；当前官网请求示例已使用 `"Y"`。长期有效的示例仍带结束日期，也不改变条件合同。

## 同步响应

外层 `response.data:Json` 的官网必填列为 `N`，接入方确认成功响应一定包含该对象；成功缺失按协议异常，异常响应 DTO 仍允许缺失。对象中包含 `resp_code:String(8) Y`、`resp_desc:String(512) Y`，并可能返回用户 `huifu_id:String(18)`、管理员账号和初始 `login_password`。当前成功示例已包含外层 `sign`，同步响应始终验签。

将返回的 `huifu_id` 保存为 `userHuifuId`，不可提升为 `merchantHuifuId`，也不可传给图片上传的 `data.huifu_id`。`login_password` 只能通过一次性受控通道交付，禁止日志、前端回显和示例输出。

## SDK 边界

三语言锁定版本均有 `V2UserBasicdataEntRequest`。生成类把若干官方 C/N 字段按必填或空字符串处理时，官方合同优先；不得为通过 SDK 校验写入假值。三语言真实请求均使用对应官方 SDK；PHP 可运行代码仍受 `user-onboarding-shared-server-sdk-matrix.md` 的独立 DEBUG 硬停约束。

## 2026-10-25 官网更新同步

本地当前来源SHA-256：`9ae70289683601611a7e9e675c382778e8447b48786ded16a345460ab630c476`。

新增公共请求字段sys_id的上下级关系说明：sys_id为总部商户时在开户阶段绑定关系，否则在业务入驻阶段按upper_huifu_id绑定。该注记属于request.sys_id，不向开户data添加upper_huifu_id，也不混淆sys_id与用户ID。
