# 企业商户进件

## 适用范围

适用于有营业执照或企业/个体主体的基础信息开户。官方来源：[企业商户进件](https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_qyshjbxxrz_kyc.md)。主体类型不明时必须触发硬检查点，只问“本次进件主体是企业/个体还是无执照个人？”。

## 已确认的请求合同

- Endpoint：`POST https://api.huifu.com/v2/merchant/basicdata/ent`；顶层包含 `sys_id`、`product_id`、`sign`、`data`。
- 官网更新时间 `2026-09-18`；本地活动快照 `2026-11-09`；原文 SHA-256：`6606629100f94813a7a4238c8f1ffc970ec3b905d1af9487bb92baee6138822e`。
- 请求、同步响应和审核异步的完整父子路径、类型、长度、Y/N/C 与官方说明见 `merchant-onboarding-complete-field-catalog.md` 的“企业商户进件”；本页只保留生成策略和高风险约束，不能替代完整字段目录。
- `data` 的请求定位键为 `req_seq_id`（当日唯一）和 `req_date`（`yyyyMMdd`）。`upper_huifu_id:String(18) C`：`sys_id` 主体为渠道商时填写真实渠道商号，总部商户主体时选填；不得为满足字段而虚构。
- 最小资料按主体、营业执照、注册地址/经营地址、法人、联系人、结算卡和门店资料分组校验。图片字段只接收图片上传接口返回的标识。
- `scene_type=OFFLINE` 或 `ALL` 时，经营详细地址是条件必填；证照非长期时必须提供结束日期。
- `store_header_pic`、`store_indoor_pic`、`store_cashier_desk_pic` 均为 `String(64) C`，仅当 `scene_type` 含线下场景时必填；不得继续按旧版无条件 `Y` 处理。
- `head_office_flag=1` 时 `head_type:String(1) C` 按说明条件必填：`0=集团客户`、`1=大型商业综合体`、`2=品牌连锁客户`。总部按类型提交 F718-F724；下级商户按对应总部客群及加盟/直营性质提交 F725-F727。按 `C` 和说明执行条件必填，材料也不能只传父标识而遗漏。
- `card_info` 是 SDK 边界的 JSON 字符串：业务层先校验对公/对私卡条件，再统一序列化；不得手拼或使用示例卡号。
- `data.prov_id/area_id` 表示经营省市，`data.card_info.prov_id/area_id` 表示结算银行卡省市，`data.material_card_info.prov_id/area_id` 表示补充对公同名账户省市。三组叶字段同名但父路径不同，适用时必须分别生成；不能按叶字段名合并或把任一子对象字段提升到 `data` 顶层。
- `data.material_card_info:String(JSON Object) Y` 是补充对公同名账户信息；当前官网类型列已由旧版 `Object` 修正为 `String`，说明列仍为“jsonObject字符串”。非个体工商户的企业商户在 `card_info` 选择对私结算（含法人、非法人）时需要补充，并通过图片上传接口提交 F08 对公账户证明。正式标记Y与条件说明不完全一致，必须标注 `[官方文档口径冲突]`；未满足适用条件时不擅自增加材料。叶字段长度为card_name128、card_no32、prov_id/area_id6，branch_code正式8但例子12位，该长度约束用 TODO/配置隔离并提示核对本页官方来源，不影响其余字段与 SDK 开发。先校验全部适用叶字段，再整体 JSON 序列化。当前官网已经删除旧的 `material_card_info.card_type`；不得继续生成该键或套用“默认0”。
- 生成字段时必须同时读取 `merchant-onboarding-field-contracts.md` 的企业值域表：`ent_type`、`busi_type`、`scene_type`、证照/证件有效期、`sms_send_flag`、总部/下级商户标识、结算/取现枚举均按各自字符串值域处理。官网示例值不是默认值，禁止把所有开关写成 `1`。
- String(JSON) 对象只能在 `merchant-onboarding-complete-field-catalog.md` 中沿父路径加载到全部相关叶子且调用方提供真实选择后生成；`card_info` 与 `material_card_info` 当前均为 String(JSON Object)。业务对象校验通过后整体序列化一次，不得发送普通嵌套 Object，也不得二次序列化。受益人、电子账户、股东和扩展材料对象不得只写父字段，也不得猜值。
- 涉及 MCC、地区、证件类型、图片上传、银行编码、结算批次或补充材料等带外部资料的字段时，必须同时读取 `merchant-onboarding-external-resources.md`，并按完整字段路径单列 `外部资料提示`，给出未经改写的原始地址；示例 URL 不是资料或默认值。

## 异步通知字段

- 企业进件审核异步通知地址是 `data.async_return_url:String(120) N`。
- `notify_url` 是支付交易接口字段，不是企业进件字段；企业进件的业务 DTO、`extendInfoMap` 和最终 `data` 中都禁止使用 `notify_url`。
- Java `V2MerchantBasicdataEntRequest` 没有该扩展字段的专属 setter 时，必须通过 `extendInfoMap` 原名透传，禁止改名：

```java
Map<String, Object> extendInfoMap = new HashMap<>();
if (request.asyncReturnUrl() != null && !request.asyncReturnUrl().isBlank()) {
    extendInfoMap.put("async_return_url", request.asyncReturnUrl());
}
sdkRequest.setExtendInfo(extendInfoMap);
```

## 公共请求头

- 在已核验源码基线中，Java 与 PHP 使用 Skill 调用时都要求 `jpt-x-skill-source: <skill_source>`；Java `3.0.41` 与 PHP `2.0.31` 的官方 SDK 主链路会在配置来源值后自动补该头。Python `2.0.28` 同样从 `MerConfig.jpt_x_skill_source` 自动补头。
- 企业基础进件请求没有 `data.huifu_id`，按官网字段合同生成，不因 SDK 内部请求头增加该业务字段。

## 同步受理与状态

- 同步返回可能含 `huifu_id`、`apply_no`、`token_no`；它们只用于后续状态定位，不等于审核通过、渠道实名完成或支付业务可用。
- 将 `req_seq_id`、`req_date`、`apply_no`、主体资料版本和状态历史落库；`token_no` 必须字段级加密、访问审计，禁止前端、日志和示例输出。
- 审核补偿优先使用申请单状态查询；网络不确定时先查状态，不换流水盲目重复提交。

## SDK 证据边界

已核验源码基线 Java `3.0.41`、PHP `2.0.31`、Python `2.0.28` 都有 `V2MerchantBasicdataEntRequest` 作为可选封装，但三个锁定版本均没有 `material_card_info` 或新 `head_type` 的专属字段/setter。使用各语言 Request 的 exact-key 扩展字段能力时，键必须保持 `material_card_info`、`head_type`；前者值必须是已校验业务对象整体序列化得到的 JSON 字符串，后者保持枚举字符串。不能改名、传合同外子键或声称 SDK 已原生覆盖。三语言真实请求均使用对应官方 SDK；PHP 仍受独立 DEBUG 硬停约束。该 Request 只证明 URI、已有字段序列化和 SDK 默认的请求/同步响应处理路径；不替代本页资料、权限和条件必填校验，也不证明实际审核结果或回调协议。每次调用显式传入新的当天唯一 `req_seq_id` / `req_date`，Python 不会自动生成。

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

官网只说明 `sign` 对报文整体签名，未给出可核验的验签原文、成功 ACK、HTTP 超时或重试样本。这些仍为 `[需要官方确认]`；按 `shared-overview.md` 的开发提醒引用本页官方来源并建议咨询官方/交流群，继续回调框架与已明确的审核状态处理，未知协议留 TODO/配置。不得套用支付 `notify_url` 或 `RECV_ORD_ID_` 规则。
