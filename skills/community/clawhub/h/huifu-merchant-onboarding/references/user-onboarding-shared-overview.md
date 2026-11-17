# 汇付用户开户与入驻总览

## 能力边界

本 Skill 面向服务商或商户为旗下企业/个人建立分账、结算用户并配置结算能力。它不创建支付商户，不代替 `/v2/merchant/*` 商户进件，也不处理支付交易。

| 生命周期 | 接口 | 结果定位 |
| --- | --- | --- |
| 企业用户开户 | `POST /v2/user/basicdata/ent` | 返回用户 `huifu_id`，可能返回管理员初始密码 |
| 个人用户开户 | `POST /v2/user/basicdata/indv` | 返回用户 `huifu_id`，可能返回管理员初始密码 |
| 用户业务入驻 | `POST /v2/user/busi/open` | 配置结算、结算卡、取现、e账户、电子回单及LV3资金能力；可能返回申请单 |
| 非同名对公卡审核查询 | `POST /v2/user/apply/query` | 通过用户号和申请单查询 `Y/P/N/F` |
| 用户信息查询 | `POST /v2/user/basicdata/query` | 查询用户资料、卡、结算/取现、e账户、电子回单和账户等级/资金配置 |
| 企业用户基本信息修改 | `POST /v2/user/basicdata/ent/modify` | 修改既有企业用户名称、法人、管理员、地址、材料等基础资料 |
| 个人用户基本信息修改 | `POST /v2/user/basicdata/indv/modify` | 修改既有个人用户证件有效期、联系方式、地址、材料和地区资料 |
| 用户业务入驻修改 | `POST /v2/user/busi/modify` | 修改既有用户的结算、结算卡、取现、e账户和电子回单配置；可能再次产生审核通知 |
| 用户列表查询 | `POST /v2/user/list/query` | 按法人证件号查询用户列表，可选限定上级汇付 ID |

## 路由判定

先问目标实体：

- 需要支付收单、门店、支付渠道或商户状态的是 `merchantHuifuId`，切换到本 Skill 的 `/v2/merchant/*` 商户路由。
- 需要多方分账、结算用户或用户结算卡的是 `userHuifuId`，使用本 Skill。
- 仅出现字符串键 `huifu_id` 不能判定实体；上下文仍不清楚时硬停，只问实体类型。

用户开户返回的 `huifu_id` 不能写入图片上传接口的 `data.huifu_id`。图片上传该字段只支持直属商户号；用户材料应取得 `file_id` 后在本 Skill 请求中使用，但上传过程不得伪造用户号头或业务字段。

## 状态模型

业务入驻至少有三层状态：

1. 审核状态 `audit_status=Y/P/N`。
2. 配置结果 `resp_business[].code=S/F`。
3. e账户银行状态 `bank_status=S/F`。

申请状态查询另有 `apply_status=Y/P/N/F`，其中 `F` 是系统处理失败。不同层次和接口的同字母不能合并为一个通用状态。

用户等级account_level=LV1/LV2/LV3，LV3仅企业。业务入驻及修改的balance_pay_config/account_recharge_config/delay_pay_config为String(JSON Object)；详情同名三组和account_info为原生Object，当前异步account_info已改为String(JSON Object)。等级验证trans_status是独立状态，不能替代审核或支付终态。具体材料、签约条件和费用冲突读取 `user-onboarding-field-contracts.md`；本轮九接口共644路径。

## 已知文档冲突

- 九页公共返回表的外层 `response.data` 必填列均为 `N`（业务入驻修改仍为 String，其余为 Json）。列表查询的 `user_list_info_list` 当前为 String/jsonArray格式，成功示例却是原生数组；生产 DTO 保留两种形态并优先按正式表解码。异常响应 DTO 仍允许外层 `data` 缺失。

- 官网曾将 `C` 同时说明为“条件必填”和“条件选填”；接入方已裁决为条件必填，按字段说明和主体/卡类型矩阵触发，不做无条件全局必填。
- 企业与个人开户的 `file_list` 已修正为 String/jsonArray格式，按 String(JSON Array) 发送。
- 企业与个人开户当前成功示例均包含正式必填的 `sign`；仍须验签。
- 业务入驻公共返回 `data` 已修正为 Json，与成功示例的原生对象一致。
- 业务入驻及修改的 `async.data.huifu_id` 中文名和说明均已统一为汇付客户号。
- 业务入驻新增与修改请求的 `elec_card_list`、`elec_receipt_config` 与 `sign_user_info` 当前都已修正为 String 类型；分别按 String(JSON Array/Object) 逐层编码。用户详情的同名结构也按当前 String 类型逐层解码。
- 业务入驻 D1 请求示例已补齐 `constant_amt`，`fixed_ratio` 与取现 `fee_rate` 也已使用两位小数；e账户卡 `card_type` 当前示例已修正为正式枚举值 `0`。示例值仍不得作为默认值。
- 接入方确认个人用户只允许 `card_type=1` 对私法人卡，禁止 `0/2/4`；企业用户按业务条件使用 `0/1/2/4`。
- 用户详情 `ent_base_info.file_list` 与 `indv_base_info.file_list` 当前为 String/jsonArray格式；解码各自父字符串后再解一层数组字符串。
- 用户详情 `out_settle_acct_type` 当前示例已修正为正式枚举值 `01`。
- 用户详情 D1 工作日 `weekday_fix_amt`、`weekday_fee_rate` 的说明已统一为 D1 时生效。
- 用户详情 `resp_code` 已修正为 `String(8)`。
- 用户详情的个人省/区与取现卡市/省示例互相颠倒；不得把示例编码当默认值。
- 企业与个人用户基本信息修改的请求 `huifu_id` 说明均已统一为直属汇付客户 ID；分别按企业用户号、个人用户号定位，不得传商户号。
- 个人用户基本信息修改的 `cert_validity_type` 当前示例已修正为正式枚举值 `1`。
- 用户业务入驻修改请求示例是合法 JSON，且只声明一次 `file_list`；仍不得把示例提升为 fixture、默认值或正式字段合同。
- 用户业务入驻修改的 `elec_receipt_config`、`elec_card_list` 与 `sign_user_info` 已修正为 String(JSON)；同步 `resp_business` 为 Object/jsonArray，异步 `audit_info.resp_business` 为 String/jsonArray。`delay_flag` 与 `async_return_url` 示例也已修正。
- 用户列表查询的 `user_list_info_list` 当前正式类型为 String/jsonArray格式，子项 `huifu_id/upper_huifu_id` 长度均为18；请求与成功响应示例均包含正式必填的 `sign`，但列表值的原生数组示例与正式 String 类型仍冲突。

官网正式参数表当前有4处空说明；account_info父对象已新增JSON与通知类型说明。已没有长度为空的标量叶字段。机械目录继续对空说明及结构父节点的空长度保留`—`。原先没有可执行触发条件的两个C字段已由接入方裁决：所有接受的卡类型要求card_name，e账户卡mp在card_type=1时要求、card_type=0时不要求。完整清单读取 `user-onboarding-field-contracts.md`。

参数表外当前有9个字段注记绑定：保留既有7项实名认证/法人证件同步填写注记，并新增企业与个人开户request.sys_id的上下级关系说明。完整目录分别绑定请求信封与data字段，不能只按叶名匹配。

原始合同、示例冲突和接入方裁决必须分层保留。未被裁决的冲突继续标记 `[需要官方确认]`；不得把接入决策伪装成官网字段表原文。
