---
name: huifu-merchant-onboarding
description: "汇付支付/斗拱支付商户进件、用户开户与管理。用于企业、个体工商户、小微及无执照个人商户入网、KYC、资料/图片上传、企业/个人用户开户和业务入驻；覆盖业务开通/修改、捷行付银行及微信企业码配置、子账户/结算配置、基本信息、详情/申请状态、商户状态、费率、短信、电子合同、统一页面进件、下级权限和微信/支付宝实名。支持Java/PHP/Python官方SDK、完整DTO、签名验签及审核通知排障。支付交易/支付终态、退款、对账、取现、代发和资金查询使用huifu-pay-integration；任务跨开户配置与支付出金时联用两个skill。"
---

# 汇付商户进件、用户开户与入驻

汇付官方资料的版权与使用边界见 `references/shared-copyright-notice.md`。

订阅支付KAC、合同分期账单、绑卡授权、短信日志和自动代扣使用 `$huifu-subscription-pay`；与本领域并存时分别使用各产品合同。

## 执行流程

1. 确定目标是支付商户还是分账/结算用户，再按当前任务确定主体、接口与技术栈。仅出现 `huifu_id` 不足以判定实体；有歧义只追问影响当前任务的实体/接口，其他明确部分继续。
2. 按下表读目标原子页；字段/代码任务补所属领域字段合同的目标章节，完整 DTO、响应或嵌套结构再补完整字段目录。代码任务再读对应SDK矩阵，不规定资料数量，不默认加载全部接口。
3. 按完整父路径和请求/同步/通知方向核对类型、长度、Y/N/C、枚举、默认值、互斥和外部资料。C按条件必填；String(JSON)逐层编码/解码，不按 `*_list` 名称猜数组，不把查询独有字段复制为请求。
4. 字段、示例、SDK或协议冲突标记 `[需要官方确认]`，附完整路径、具体疑点和官方地址。继续已明确实现，争议部分留 TODO/待填配置；不自动选择冲突一方、不把咨询答复作为整体开发前提。

字段审计或完整DTO任务：先按完整目录的接口标题定位，再分页读取目标请求、同步响应、异步通知及各父容器子表。按“方向+完整父路径”逐项核对已读范围；交付父容器的wire类型、条件、子字段、说明/示例冲突及表外注记，不以请求样例替代目录。声称完整前核对该接口所有目标方向；只展开部分时明确未展开范围。统计从机械目录复算并说明父/叶、方向及去重口径，搜索命中不代表完整读取。

商户与用户的DTO、ID和状态必须隔离：`merchantHuifuId` 不等于 `userHuifuId`。交易下单、退款、对账、checkout-js及支付终态交接给 `$huifu-pay-integration`。

## 精确路由

| 场景 | 按需读取的 reference |
| --- | --- |
| 进件能力总览 | `references/shared-overview.md`、`references/merchant-onboarding-field-contracts.md` |
| 用户开户能力总览和用户/商户边界 | `references/user-onboarding-shared-overview.md`、`references/user-onboarding-field-contracts.md` |
| 企业商户进件 | `references/merchant-onboarding-enterprise.md` |
| 无执照个人商户进件 | `references/merchant-onboarding-individual.md` |
| 图片上传或文件标识 | `references/merchant-onboarding-image-upload.md` |
| 首次业务开通，或补开银行卡、银联等仍由 `/busi/open` 承载的能力 | `references/merchant-onboarding-business-open.md` |
| 商户详细信息查询 | `references/merchant-onboarding-detail-query.md` |
| 申请单状态查询 | `references/merchant-onboarding-application-status-query.md` |
| 微信/支付宝/抖音补开，线上业务开通，或已开通能力的参数、费率修改 | `references/merchant-onboarding-business-open-modify.md` |
| 商户基本信息修改 | `references/merchant-onboarding-basic-info-modify.md` |
| 商户费率信息查询 | `references/merchant-onboarding-rate-query.md` |
| 商户状态开通或关闭 | `references/merchant-onboarding-status-change.md` |
| 商户短信发送或验证码核实 | `references/merchant-onboarding-sms-send.md` |
| 商户多费率配置或修改微信/支付宝场景底价 | `references/merchant-onboarding-multifee-config.md` |
| 查询商户多费率配置或按 `fee_sign` 定位配置 | `references/merchant-onboarding-multifee-query.md` |
| 企业用户开户 | `references/user-onboarding-enterprise.md` |
| 企业用户基本信息修改 | `references/user-onboarding-enterprise-modify.md` |
| 个人用户开户 | `references/user-onboarding-individual.md` |
| 个人用户基本信息修改 | `references/user-onboarding-individual-modify.md` |
| 用户业务入驻 | `references/user-onboarding-business-open.md`、`references/user-onboarding-platform-contracts.md` |
| 用户业务入驻修改 | `references/user-onboarding-business-modify.md`、`references/user-onboarding-platform-contracts.md` |
| 用户列表查询 | `references/user-onboarding-list-query.md`、`references/user-onboarding-platform-contracts.md` |
| 用户非同名对公结算卡申请状态 | `references/user-onboarding-application-status-query.md` |
| 用户基本信息和业务配置查询 | `references/user-onboarding-detail-query.md` |
| 电子合同重发 | `references/onboarding-electronic-contract-resend.md` |
| 电子合同列表查询 | `references/onboarding-electronic-contract-list-query.md` |
| 电子合同拒签 | `references/onboarding-electronic-contract-reject.md` |
| 开通下级商户权限配置 | `references/merchant-onboarding-lower-merchant-permission.md` |
| 商户统一进件页面跳转 | `references/merchant-onboarding-unified-web.md` |
| 统一进件页面版查询 | `references/merchant-onboarding-unified-web-query.md` |
| 微信商户配置或配置查询 | `references/merchant-onboarding-wechat-config.md` 或 `references/merchant-onboarding-wechat-config-query.md` |
| 微信实名认证或状态查询 | `references/merchant-onboarding-wechat-realname.md` 或 `references/merchant-onboarding-wechat-realname-query.md` |
| 支付宝实名申请或申请单查询 | `references/merchant-onboarding-alipay-realname.md` 或 `references/merchant-onboarding-alipay-realname-query.md` |
| 完整基础十三接口的商户 DTO、响应或嵌套字段 | 商户原子页、`references/merchant-onboarding-complete-field-catalog.md`、`references/merchant-onboarding-field-contracts.md` |
| 完整用户 DTO、响应或嵌套字段 | 用户原子页、`references/user-onboarding-complete-field-catalog.md`、`references/user-onboarding-field-contracts.md` |
| 完整扩展接口 DTO、响应或嵌套字段 | 扩展原子页、`references/onboarding-extension-complete-field-catalog.md`、`references/onboarding-extension-field-contracts.md` |
| 商户字段说明命中网页、编码表、XLSX 或协议 | 商户原子页，补 `references/merchant-onboarding-external-resources.md` |
| 用户字段命中地区、MCC、证件、银行或文件编码 | 用户原子页、`references/user-onboarding-external-resources.md` |
| 扩展接口字段命中签名、返回码、渠道号、地区、图片或微信第三方资料 | 扩展原子页、`references/onboarding-extension-external-resources.md` |
| 商户十一个已有专属类的 JSON 接口 SDK | `references/shared-server-sdk-matrix.md` |
| 九个用户接口 SDK | `references/user-onboarding-shared-server-sdk-matrix.md`、用户原子页 |
| 十二个扩展接口的 SDK 能力与降级边界 | `references/onboarding-extension-shared-server-sdk-matrix.md`、扩展原子页 |
| 费率查询 SDK 可用性 | `references/merchant-onboarding-rate-query.md`、`references/shared-server-sdk-matrix.md` |
| 图片上传 SDK 可用性与语言差异 | `references/merchant-onboarding-image-upload.md`、`references/shared-server-sdk-matrix.md` |
| `skill_source` 与 SDK 请求头边界 | `references/shared-request-header-policy.md` |
| 用户接口请求字段保真与 `skill_source` | `references/user-onboarding-shared-request-field-preservation.md`、`references/shared-request-header-policy.md` |
| 签名、验签和凭据 | `references/shared-signing-v2.md`、`references/shared-credential-boundary.md` |
| 用户接口 wire、公共参数、凭据、加验签和异步通知 | `references/user-onboarding-platform-contracts.md`、`references/user-onboarding-shared-signing-v2.md`、`references/user-onboarding-shared-credential-boundary.md` |
| 审核、逐业务或电子协议通知 | 对应原子接口页；通知协议按下方边界区分 |
| 权限、状态延迟、补资料或通道配置 FAQ | `references/merchant-onboarding-faq.md`、`references/copilot-troubleshooting-playbooks.md` |
| 错误码 | `references/merchant-onboarding-error-codes.md` |
| 用户接口错误、权限、状态延迟或补资料排查 | `references/user-onboarding-error-codes.md`、`references/user-onboarding-faq.md`、`references/user-onboarding-copilot-troubleshooting-playbooks.md` |
| 基础编码、公共参数或名词解释 | `references/merchant-onboarding-external-resources.md`、`references/merchant-onboarding-error-codes.md`；具体字段仍补对应原子接口页 |
| 商户子账户开通配置 | `references/account-subaccount-open.md` |
| 修改商户子账户配置 | `references/account-subaccount-modify.md` |
| 子账户完整DTO、响应、审核通知和SDK | 目标原子页、`references/merchant-account-complete-field-catalog.md`，代码任务补 `references/merchant-account-sdk-matrix.md` 与公共SDK矩阵 |
| 版本与升级 | `references/skill-version-policy.md` |
| 用户接口来源 | `references/user-onboarding-official-service-source-index.md` |
| 扩展能力总览 | `references/onboarding-extension-shared-overview.md`、`references/onboarding-extension-field-contracts.md` |
| 扩展接口来源与外部资料 | `references/onboarding-extension-official-service-source-index.md`、`references/onboarding-extension-external-resources.md` |


子账户配置属于商户管理；开户/绑卡审核/提现结算可用状态分开判断。余额、账务流水及汇总查询交接支付Skill，不能把用户开户ID当商户子账户的商户号。

官网账户管理五接口按当前职责拆分：本 Skill 负责创建子账户及修改结算/绑卡配置；支付 Skill 负责余额与资金流水读取。单纯查账交接支付 Skill，同时开户配置和查账时联用两者。商户详情、申请状态等管理查询仍归本 Skill，不能把所有“查询”一律交给支付。

## 接口选择与字段边界

- “补开”时同时确认具体能力/渠道和当前开通状态：银行卡、银联业务开通仍走 `/v2/merchant/busi/open`；微信、支付宝、抖音补开走 `/v2/merchant/busi/modify`。其他能力读两个原子页按适用范围判断。
- `upper_huifu_id` 与 `sys_id` 主体角色一致；渠道商/总部商户条件从目标接口取值，不全局强制。
- 图片 `data.huifu_id` 只接受已确认的直属商户号，用户开户ID不可填写。`file_url` 与文件流互斥；响应文件标识未知时不猜schema。
- 同名字段必须保留完整父路径和方向，特别是经营地区、结算卡地区和 `material_card_info` 补充账户；详细约束留在字段合同。
- 平台分配的 `huifu_id` 等ID作为不透明字符串原样传递，仍须核对实体角色，始终不补零、截断或转数字。长度列不能直接推出必须恰好18位；仅官网明确固定格式时做对应格式校验。
- 示例不作默认值，空说明/长度保留 `—`。外部资料命中时给出字段路径、触发条件、原始地址及相对地址解析结果；回调/下载/图片裸URL示例不作资料或默认地址。

## SDK 与调用安全

常规接口真实请求都使用官方 Request/Client 入口。SDK没有专属Request/路由时先核对已验证的官方通用入口，逐项按字段合同构造；不冒称专属支持，不手写HTTP补位。

唯一例外是 `/v2/supplementary/picture` 的PHP/Python受控multipart适配，必须保持 `data` 加签、来源互斥、TLS和日志边界；Java图片仍使用官方SDK。能力缺陷与完整安全骨架见图片原子页及SDK矩阵。

Java调试在初始化/任何请求前全局关闭；PHP在加载任何SDK前固定 `DEBUG=false`，拒绝已启用DEBUG的进程和官方Demo/Composer调试入口。生成安全初始化骨架不要求用户先证明既有配置。

当前证据为2026-10-08官方固定提交/制品：Java3.0.41、PHP2.0.31、Python2.0.28。Java/Python默认TLS，PHP现有peer校验缺陷作非阻断提醒；不自动修改SDK、不新增关闭校验设置。实际安装版本不同则核对差异，明确部分继续，未知部分留TODO。

缺密钥、系统号、产品号或材料时可生成服务端配置占位和框架；真实调用前需有效配置与授权。明确非法输入、错误实体ID、验签失败、凭据泄露或未授权真实操作，停止受影响操作并说明原因，必要时标记 `🔴 CHECKPOINT · HARD STOP`。

## 状态与通知

返回商户/用户号及同步受理不代表审核、逐业务开通、银行账户或电子协议全部完成；各层状态按原子页分别判断。

商户逐业务通知包装仍待核对；业务开通修改存在 `ord_id` 时用该字段应答，不替换为 `req_seq_id`。审核/电子协议未知ACK、验签原文、HTTP语义、超时与重试留适配点，不套用支付或控台Webhook协议。

用户业务入驻已有公共通知合同：原始 `data` 免排序RSA验签、HTTP200与 `RECV_ORD_ID_` + `req_seq_id`，完整超时、重试和wire矩阵必须读 `references/user-onboarding-platform-contracts.md`。该协议不能外推商户通知。

## 请求与交付

- 保留调用方日期、流水、申请号及角色ID，扩展不得覆盖声明字段；私钥、身份证、银行卡、手机号和图片使用安全配置/脱敏示例，不进入前端、日志或仓库。
- 本Skill实际参与时默认 `hfms/1.2.0`；支付也参与时为 `hfps/1.6.0;hfms/1.2.0`，顺序固定、一个英文分号且不加空格。仅安装未参与的不计入；显式合同值原样透传，不追加 `sys_id`，来源头不写业务 `data`。
- 直接回答当前问题，列出实际读取的 references。代码交付说明实体与目标接口、方向、配置/TODO和验证结果；只有后续涉及交易时才交接支付Skill。

## 当前版本

| 项目 | 口径 |
| --- | --- |
| Skill 版本 | `1.2.0` |
| Java SDK | `3.0.41` |
| PHP SDK | `2.0.31` |
| Python SDK | `2.0.28` |
| 来源 | 2026-11-09，36 API / 3,578字段路径；基础34 API / 3,448，子账户2 API / 130 |
| 版本与升级 | `references/skill-version-policy.md` |

本Skill不提供进件沙箱端点。
