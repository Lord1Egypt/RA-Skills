# 个人商户进件

## 适用范围

适用于无营业执照的个人商户基础信息开户。官方来源：[个人商户进件](https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_grshjbxxrz_kyc.md)。企业/个体与个人资料不可混用。

## 已确认的请求合同

- Endpoint：`POST https://api.huifu.com/v2/merchant/basicdata/indv`；顶层包含 `sys_id`、`product_id`、`sign`、`data`。
- 官网更新时间 `2026-09-04`；本地活动快照 `2026-11-09`；原文 SHA-256：`09862a3923b114abcf7dbc9e7545798481abc37f88b6eb64911ce7d53f9f5437`。
- 请求、同步响应和审核异步的完整父子路径、类型、长度、Y/N/C 与官方说明见 `merchant-onboarding-complete-field-catalog.md` 的“个人商户进件”；本页不能替代完整字段目录。
- `data` 使用当日唯一的 `req_seq_id`、`req_date`。`upper_huifu_id:String(18) C`：`sys_id` 主体为渠道商时填写真实渠道商号，总部商户主体时选填；其余资料按负责人、证件、经营信息、联系人、结算卡、结算/取现规则分组校验。
- `scene_type=OFFLINE` 或 `ALL` 时必须提供经营详细地址。身份证、银行卡和门店图片字段只接收图片上传后的文件标识。
- `store_header_pic`、`store_indoor_pic`、`store_cashier_desk_pic` 均为 `String(64) C`，`scene_type` 含线下场景时必填。
- `head_office_flag=0` 表示下级商户；必须按对应总部 `head_type` 补材料：集团客户 F725，大型商业综合体 F726，品牌连锁客户按加盟/直营提交 F727。个人商户接口本身没有 `head_type` 请求字段，不能为满足说明而补造该键。
- `card_info`、`settle_config`、`cash_config` 是 String(JSON) 边界：先建对象、校验条件字段、统一序列化；不直接透传未经校验的字符串。
- `data.prov_id/area_id` 是经营省市，`data.card_info.prov_id/area_id` 是银行所在省市。不得按 `prov_id/area_id` 叶字段名去重；适用时两组都保留，并把银行卡省市序列化在 `card_info` 内。
- 受益人、电子账户、扩展材料等多层对象必须从完整字段目录沿父路径读到全部相关叶子；不得只写父字段或根据字段名猜结构。
- 生成字段时必须同时读取 `merchant-onboarding-field-contracts.md` 的个人值域表：`scene_type`、负责人证件日期、`occupation`、`sms_send_flag`、下级商户标识、结算/取现枚举分别校验。官网示例值不是默认值，禁止把所有开关写成 `1`。
- `legal_cert_end_date` 在个人进件官网表中是 Y；即使 `legal_cert_validity_type=1` 也不得自行按企业进件规则省略。若长期证件的结束日取值无法从调用方资料确定，标记 `[需要官方确认]`，不猜填日期。
- 涉及 MCC、地区、证件类型、图片上传、银行编码、结算批次或补充材料等带外部资料的字段时，必须同时读取 `merchant-onboarding-external-resources.md`，并按完整字段路径单列 `外部资料提示`，给出未经改写的原始地址；示例 URL 不是资料或默认值。

## 异步通知字段

- 个人进件审核异步通知地址是 `data.async_return_url:String(120) N`。
- `notify_url` 是支付交易接口字段，不是个人进件字段；个人进件的业务 DTO、`extendInfoMap` 和最终 `data` 中都禁止使用 `notify_url`。
- Java `V2MerchantBasicdataIndvRequest` 没有该扩展字段的专属 setter 时，通过 `extendInfoMap.put("async_return_url", ...)` 原名透传；禁止把 `notify_url` 作为扩展字段键。

## 公共请求头

- 在已核验源码基线中，Java 与 PHP 使用 Skill 调用时都要求 `jpt-x-skill-source: <skill_source>`；Java `3.0.41` 与 PHP `2.0.31` 的官方 SDK 主链路会在配置来源值后自动补该头。Python `2.0.28` 同样从 `MerConfig.jpt_x_skill_source` 自动补头。
- 个人基础进件请求没有 `data.huifu_id`，按官网字段合同生成，不因 SDK 内部请求头增加该业务字段。

## 状态与数据保护

- 同步响应的 `resp_code` / `resp_desc` 表示本次接口受理结果；可能条件返回 `huifu_id`、`apply_no`、`token_no`，均不代表审核通过或交易可用。
- 个人审核状态与企业审核状态不强行合并；按申请单状态查询中的实际枚举保存状态历史。
- 证件号、银行卡号、手机号、地址、`token_no` 和图片标识均按高敏感数据处理：禁止示例、日志、前端回显和未经加密的持久化。

## SDK 证据边界

已核验源码基线 Java `3.0.41`、PHP `2.0.31`、Python `2.0.28` 都有 `V2MerchantBasicdataIndvRequest` 作为可选封装。它只证明 URI、字段序列化和 SDK 默认的请求/同步响应处理路径；主体判断、材料条件和渠道准入仍以本页和官方联调为准。每次调用显式传入新的当天唯一 `req_seq_id` / `req_date`，Python 不会自动生成。

## 回调边界

官网已确认异步包络为 `resp_code:String(5) Y`、`resp_desc:String(512) Y`、`sign:String(512) Y`、`data:String(JSON Object) N`。`data` 中已知字段为：

| 路径 | 类型 / 必填 | 说明 |
| --- | --- | --- |
| `data.sub_resp_code` / `data.sub_resp_desc` | `String(8) Y` / `String(512) Y` | 业务返回码与描述。 |
| `data.req_seq_id` / `data.req_date` | `String(32) Y` / `String(8) Y` | 原请求流水与日期。 |
| `data.audit_status` | `String(1) Y`：`Y/N/F` | 审核通过、审核拒绝、失败。 |
| `data.audit_desc` / `data.product_id` | `String(512) N` / `String(32) Y` | 审核描述与产品号。 |
| `data.huifu_id` / `data.apply_no` / `data.token_no` | `String(18) N` / `String(18) N` / `String(20) N` | 条件返回的商户、申请单及取现卡定位字段。 |
| `data.notify_type` / `data.elec_acct_result` | `String(1) N` / `String(JSON Object) N` | `notify_type=Z` 时为电子账户开通结果。 |

官网未给出可核验的验签原文、成功 ACK、HTTP 超时或重试样本，这些仍为 `[需要官方确认]`。按 `shared-overview.md` 的开发提醒给出本页官方来源和官方/交流群咨询建议；可继续回调框架、补偿查询及已明确字段处理，未知协议留 TODO/配置，不猜测具体 ACK、验签原文或重试策略。
