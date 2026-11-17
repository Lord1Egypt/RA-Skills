# 商户进件资料总览

本页负责进件能力导航与未明确合同的开发提醒。详细字段必须读取原子接口页、完整字段目录和字段合同。

## 什么时候读取

- 用户尚未明确企业、个人、业务开通/修改、基本资料修改、图片、费率、短信、详情或状态任务。
- 需要判断最小阅读链路。
- 需要确认支付交易问题应交接到哪个 Skill。

## 能力地图

| 目标 | 首选 reference |
| --- | --- |
| 企业商户开户 | `merchant-onboarding-enterprise.md` |
| 无执照个人商户开户 | `merchant-onboarding-individual.md` |
| 图片资料 | `merchant-onboarding-image-upload.md` |
| 支付、分账等业务能力开通 | `merchant-onboarding-business-open.md` |
| 查询商户完整配置 | `merchant-onboarding-detail-query.md` |
| 查询申请、绑卡、结算等状态 | `merchant-onboarding-application-status-query.md` |
| 修改已开通业务或费率 | `merchant-onboarding-business-open-modify.md` |
| 修改商户基础资料 | `merchant-onboarding-basic-info-modify.md` |
| 查询商户费率配置 | `merchant-onboarding-rate-query.md` |
| 开通或关闭商户状态 | `merchant-onboarding-status-change.md` |
| 发送或核验商户短信验证码 | `merchant-onboarding-sms-send.md` |
| 配置或修改微信、支付宝多场景底价 | `merchant-onboarding-multifee-config.md` |
| 查询多费率配置或按 `fee_sign` 定位 | `merchant-onboarding-multifee-query.md` |
| 开通商户现金子账户及结算配置 | `account-subaccount-open.md` |
| 修改商户子账户结算/绑卡配置 | `account-subaccount-modify.md` |
| 完整字段和嵌套路径 | `merchant-onboarding-complete-field-catalog.md` |
| 条件、互斥、冲突和 SDK 边界 | `merchant-onboarding-field-contracts.md` |
| 外部编码、XLSX、协议和第三方资料 | `merchant-onboarding-external-resources.md` |

## 补充资料

| 主题 | reference |
| --- | --- |
| 调用方请求字段保留 | `shared-request-field-preservation.md` |

## 固定边界

- `huifu_id` 已返回不等于支付能力已经可用。
- 业务开通结果必须按逐业务状态判断，不能只看同步受理。
- 本 Skill 不实现支付下单、退款、对账、checkout-js 或支付终态；这些能力交接给 `$huifu-pay-integration`。
- 图片传输使用已核验 SDK/专项适配；未知响应或通知协议按下方提醒隔离，不阻断已明确部分的开发。
- 账户管理中的子账户创建/配置属于本 Skill；余额、账务流水及汇总查询交接支付 Skill。此处按操作目的分工，查询商户资料和进件状态仍由本 Skill 处理。

## 文档疑义与开发提醒

`[需要官方确认]`、`[官方文档口径冲突]` 和空白 `—` 都表示证据边界，不是停止开发的指令。遇到字段类型、长度、条件、响应或通知协议不明确时：

1. 列出接口、方向、完整字段路径和具体疑点，给出该原子页的对应官方文档地址；可从三个官方来源索引定位来源，不用同名字段或示例替代合同。
2. 提醒开发者核对文档，不清楚时建议咨询汇付官方或汇付开发者交流沟通群。不虚构群号/链接，也不要求先取得答复或证明才能继续开发。
3. 继续已明确的官方 SDK 调用、请求模型、业务框架和测试。把有疑义的序列化、字段约束、响应映射、ACK 或重试策略隔离为明确的 TODO/待填配置；不猜测值、默认值、协议或签名规则，不把未完成模块声称为已联调完成。

已明确的非法参数、签名/验签失败、敏感信息泄露和无授权真实操作仍按原有保护处理。本轮指定的本地 SDK TLS 风险按 `shared-server-sdk-matrix.md` 提醒，不构成 Skill 开发或联调代码生成的前置条件；既不声称风险已修复，也不自动修改 SDK。

## 当前来源

当前商户字段快照为 `2026-11-09`，十三接口共2,258个字段路径。36份进件文档本轮1份变化、35份未变，仅业务开通修改的sign_start_date长度7修正为8；正式字段无增删。`upper_huifu_id:String(18) C`、门店图片条件和 `material_card_info` 独立父路径继续保留。官网URL用于来源追溯和维护刷新，不计入普通回答的本轮references。
