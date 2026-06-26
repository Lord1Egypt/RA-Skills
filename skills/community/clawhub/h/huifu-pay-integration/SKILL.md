---
name: huifu-pay-integration
description: "汇付支付接入副驾驶：适用于首次接入、存量改造、聚合支付、托管支付、抖音直连、拆单支付查询、checkout-js、PHP/Java/Python SDK、验签、异步通知、商户进件/通道权限/FAQ排查、上线检查、版本升级提示。"
---

# 汇付支付集成

## 版权声明

本 Skill 包中的汇付支付、斗拱支付接口资料整理自上海汇付支付有限公司官方开放平台与官方产品文档；原始文档及其更新维护权归汇付支付官方所有。本 Skill 包仅作技术学习交流与接口集成辅助使用，详细口径见 `references/shared-copyright-notice.md`。

1.3.0 目标：从“文档路由”升级为“接入副驾驶”。先判断开发者处境，再推荐产品线、接入方案、联调步骤、参数/返回/代码片段检查、问题修复建议和上线检查。默认只读取当前场景必需的 3-5 份本地 reference。

## 什么时候使用

- 第一次接入汇付支付，需要判断聚合支付、托管支付还是 checkout-js。
- 已有订单系统、支付代码、回调逻辑或退款逻辑，需要增量接入汇付。
- 用户要联调方案、方案卡、配置清单、必测项、问题排查或上线检查。
- 用户贴出请求参数、返回参数、错误信息或代码片段，需要定位风险。
- 用户遇到商户进件、接口权限、数据权限、通道配置、appid/openid、授权目录、Webhook 收不到、退款/对账/取现/发票类 FAQ 问题。
- 用户询问当前 Skill 版本、如何更新 Skill、是否最新版、能力缺失是否需要升级。

## 什么时候不要使用

- 用户已经明确指定某份本地 reference，只需要读取那一份。
- 用户已经在某个专题文档内，当前问题只和该专题参数、返回字段或代码示例有关。
- 非汇付支付、非斗拱、非支付接入相关问题，不使用本 Skill。

## 快速路由表

优先按下表选最小 reference 集；没有命中时再进入后续决策流程。

路由优先级固定为：用户显式版本/升级问题 > 硬检查点 > 快速路由表精确命中 > 已明确产品线的阶段主路由 > 首次接入默认流程。多处命中时，先执行优先级最高的一处，不要把多个入口合并成大而全阅读清单。

快速路由裁剪规则：命中单行时严格使用该行文档；用户同时提出两个独立目标时才合并。合并后超过 5 份时，只保留主场景入口、关键专题、最终确认/验签、技术栈适配、FAQ/排查入口，其他方向写成“暂不读取”。FAQ 和接口字段混合问题不能拆开回答：先读 FAQ，再补对应接口专题；退款 `setOrgReqSeqId` 编译报错必须同时覆盖 `hostingpay-faq.md` 和 `hostingpay-refund.md`。

| 用户场景 | 最小 reference 集 |
| --- | --- |
| 首次接入、产品线不明 | `references/shared-overview.md`、`references/copilot-onboarding.md`、`references/copilot-solution-selection.md` |
| 存量系统新增汇付支付；当前项目已有订单、支付、回调、退款或状态机代码 | `references/shared-overview.md`、`references/copilot-existing-system.md`、`references/copilot-solution-selection.md` |
| 存量系统补退款 / 退款查询 | `references/copilot-existing-system.md`，再按产品线补 `references/aggregation-refund.md` 或 `references/hostingpay-refund.md` |
| 存量系统改回调 / 重复通知 / 幂等 | `references/copilot-existing-system.md`、`references/copilot-troubleshooting-playbooks.md`、`references/shared-async-notify.md` |
| 存量系统上线前检查 | `references/copilot-go-live-checklist.md`、`references/copilot-existing-system.md` |
| 已完成托管预下单和最终确认，只接 checkout-js | `references/checkout-js.md`、`references/checkout-js-callback-and-confirmation.md`、`references/hostingpay-async-webhook.md` |
| checkout-js 先决能力未确认 | `references/copilot-onboarding.md`、`references/checkout-js-create-preorder-contract.md`，触发硬检查点 |
| 聚合查单 / 关单 / 合单关单 / 对账 | `references/aggregation-query.md`；只在关单补 `aggregation-query-trade-close.md` / `aggregation-query-close-query.md`，只在对账补 `aggregation-query-reconciliation.md` |
| 抖音直连下单 / `pre_order_type=4` | `references/hostingpay-preorder.md`、`references/hostingpay-preorder-douyin-direct.md`、`references/hostingpay-async-webhook.md` |
| 拆单支付订单查询 / `splitpay/query` | `references/hostingpay-query.md`、`references/hostingpay-query-splitpay.md`；需追溯微信小程序拆单来源时再补 `references/hostingpay-preorder-wechat-mini.md` |
| 新增接口是否三语言 SDK 兼容 | `references/shared-server-sdk-matrix.md`、`references/hostingpay-preorder-douyin-direct.md`、`references/hostingpay-query-splitpay.md` |
| PHP 模板或 SDK 示例 | `references/shared-server-sdk-matrix.md`，再按产品线补 `references/aggregation-php-adapter.md` 或 `references/hostingpay-php-adapter.md` |
| Python 模板或 SDK 示例 | `references/shared-server-sdk-matrix.md`，再按产品线补 `references/aggregation-python-adapter.md` 或 `references/hostingpay-python-adapter.md` |
| 参数、返回、代码片段排查 | `references/copilot-parameter-review.md`、`references/copilot-troubleshooting-playbooks.md` |
| 商户进件 / 接口权限 / 通道配置 / appid / Webhook FAQ | `references/merchant-onboarding-faq.md`、`references/copilot-troubleshooting-playbooks.md`，必要时补 `references/official-service-source-index.md` |
| 托管 Java SDK 方法拼写 / setter 编译 FAQ / 退款 `setOrgReqSeqId` 编译报错 | `references/hostingpay-faq.md`、`references/hostingpay-refund.md` |
| 官网能力、不覆盖能力、转人工材料、AI 技能包技术支持联系方式 | `references/official-service-source-index.md` |
| 排查后仍解决不了 / 要联系技术支持 | `references/copilot-troubleshooting-playbooks.md`、`references/official-service-source-index.md` |
| 上线前检查 | `references/copilot-go-live-checklist.md`、`references/copilot-existing-system.md` |
| Skill 版本、更新方式、能力缺失是否升级 | `references/skill-version-policy.md` |

## 先读哪些总入口

1. 版本/升级类问题直达 `references/skill-version-policy.md`，不固定读取总览。
2. 快速路由未命中时，默认先读 `references/shared-overview.md`，再选 1 个 copilot 主入口；方案类场景最多读方案选择和方案卡两份 copilot 文档。
3. 产品线已明确时，只补当前阶段需要的 1-2 份产品线文档；用户明确说已完成的阶段只作为前置事实，不再列入本轮阅读顺序。
4. 用户说“托管预下单、查单补偿和异步通知闭环已完成，只接 checkout-js”时，直接走 checkout-js 和回调确认链路；输出中固定写“本轮已跳过托管 quickstart/base/preorder/query 等已完成阶段。”
5. 只有需要核对官网资料源、不覆盖菜单或人工升级材料时，才补 `references/official-service-source-index.md`；FAQ 类问题按上方 FAQ 专用路由读取。FAQ 原始目录和原文不随 Skill 分发。
6. 最小复测 prompts 见 canonical regression 文档；完整回归仍使用仓库级脚本。

## 决策流程

1. 从用户表达和可见项目上下文中提取 7 个标签：用户类型、产品线、阶段、技术栈、端形态、当前目标、是否存量系统。
2. 先判断是否触发硬检查点；触发后只输出检查点并等待确认。
3. 不触发时，按产品线、阶段、技术栈选择 3-5 份本地 reference，并在回答中列出“本轮实际使用的 references”。
4. 首次接入输出接入判断卡和方案卡；存量接入输出存量改造建议卡；排查问题输出问题排查卡或参数检查卡；上线前输出上线检查卡。
5. PHP 代码默认体现官方 `huifurepo/dg-php-sdk`；Python 代码默认体现官方 `dg-sdk` / `dg_sdk`；Java 先读服务端 SDK 矩阵，聚合支付业务主链路默认 `dg-lightning-sdk`，托管支付和聚合支付对账默认 `dg-java-sdk`。
6. C#、Go、Rust、Node、.NET、Ruby、Kotlin、Scala、Swift、C++ 不生成完整模板；只给受支持主链路或协议级阅读路径。
7. 接入、排查、上线检查优先走 copilot 与产品线 reference；官网 URL 只做来源追溯和人工刷新，不计入本轮实际使用 references。
8. 普通支付接入不主动提醒升级；只有用户触发版本/升级问题时，才基于本地版本策略提示更新路径。
9. 用户问题或代码字段命中分期、费率、贴息、通道准入、大额、网银、资金/结算/发票/投诉/风险能力时，必须补读 `references/official-service-source-index.md`；只解释本地字段位置和升级材料，不给开通、费率、准入、风控或可上线结论。
10. FAQ 排查命中商户进件、接口权限、数据权限、通道、appid/openid、Webhook、退款处理中、对账文件、取现或发票时，先判断“代码可修复 / 配置需补齐 / 运营或渠道侧确认”三类，不直接生成交易代码。

### 存量系统判断

存量判断优先看业务系统证据，不只看用户是否说出“存量”二字。

判为存量或疑似存量的条件：

- 用户表达包含“已有订单系统、现有项目、线上商城、已有支付渠道、已有回调、已有退款、已有状态机、PaymentService、OrderService、NotifyController、RefundService”等信号。
- 当前工作区或用户贴出的代码里出现订单、支付服务、回调入口、退款、查单、发货/权益开通、订单状态枚举或状态机等业务链路信号。
- 用户说“第一次接汇付”但同时存在上面任一业务系统证据时，判断为“存量业务系统首次接入汇付”，不是新建空项目。

只有用户明确说明“从零新建空项目、没有现有订单/支付/回调/退款/状态机”，才把“是否存量”写成“否”。证据不足时写“未确认”或“疑似存量”，不要直接写“不是存量项目”。命中存量或疑似存量时，优先读取 `references/copilot-existing-system.md`，输出新增、保留、人工确认和回归检查。

## 检查点机制

### 软检查点

软检查点不等待用户回复。用于说明主动跳过已完成阶段、排除相邻产品线、提醒 checkout-js 依赖托管预下单和最终确认。

### 🔴 CHECKPOINT · HARD STOP 硬检查点

硬检查点必须等待用户确认后再继续。只在以下情况触发：

1. 无法区分聚合支付、托管支付、checkout-js 三条主链路。
2. 无法区分服务端接入、前端页面接入、最终状态确认。
3. 用户要求现成代码，但当前组合无模板且存在多条回退路径。
4. 用户只推进 checkout-js 前端，但未确认托管预下单、异步通知验签/幂等和查单补偿闭环。
5. 用户要求可直接联调、可上线或生产可用代码，但缺少生产/联调环境、`sys_id`、`product_id`、商户号/`huifu_id`、RSA 密钥安全来源、`skill_source`、`notify_url`、渠道标识；托管场景还缺 `project_id`、托管项目状态或 H5/PC `callback_url`。
6. 本地 SDK 源码与文档口径冲突，且冲突点属于请求头、签名、版本或能力覆盖。

硬检查点输出首行必须固定为 `🔴 CHECKPOINT · HARD STOP：硬检查点。`，并包含本轮实际使用的 references、当前判断、为什么不能直接继续、唯一确认问题。未确认前不输出完整阅读顺序、代码骨架或技术栈切换方案。
checkout-js 先决能力未确认时，即使用户说“不用问”“最省事”“只负责前端”，也必须输出硬检查点；固定说明“checkout-js 不能单独成立，不能只靠前端直接接入。”，不得给安装步骤、初始化代码或前端接法。

唯一确认问题按优先级选择：先问产品线/主链路，再问端形态和最终确认方式，再问生产/联调环境，再问 `sys_id` / `product_id`，再问商户号/`huifu_id`，再问 RSA 密钥安全来源和 `skill_source`，托管场景再问 `project_id`、托管项目状态、`notify_url`、`callback_url`，最后问渠道标识。同一轮只问最高优先级缺口。

### 失败模式表

| 触发条件 | 一线处理 | 仍失败兜底 |
| --- | --- | --- |
| 产品线不明或聚合/托管/checkout-js 混在一起 | 输出硬检查点，只问主链路 | 用户仍不确认时，给接入判断卡，不给代码 |
| checkout-js 前置未确认 | 输出硬检查点，确认托管预下单、异步通知验签/幂等和查单补偿闭环 | 未确认前不输出安装步骤、初始化代码或前端接法 |
| 生产/联调配置缺失却要求可上线代码 | 输出硬检查点，只问最高优先级缺口 | 缺口未补齐时只给配置清单和必测项 |
| SDK 源码与本地文档冲突 | 停止生成代码，说明冲突字段和已读来源 | 只整理人工确认材料，不自行改 SDK 口径 |
| 用户要求跳过验签、伪造成功或收到通知即改成功 | 拒绝不安全代码，给验签、幂等、查单/异步通知最终确认替代方案 | 不提供可运行的危险代码片段 |
| 用户要求费率、准入、合规、生产定责结论 | 转官方资料源索引和人工材料清单 | 不给开通、可上线、责任归属或政策结论 |
| 接口权限或数据权限认证失败 | 区分 `sys_id` 接口权限、`product_id`、`huifu_id`、`upper_huifu_id` 和请求头来源 | 不让用户随便替换商户号或产品号；整理权限开通材料 |
| 通道路由、appid/openid 或授权目录失败 | 检查通道开通、线上/线下场景、`pay_channel`/`pay_scene`、appid 绑定和 openid 来源 | 配置仍不匹配时转渠道/运营确认，不伪造 appid/openid |
| Webhook 找不到 `sign` 或收不到下属机构事件 | 先查 URL query、原始 body、endpoint key、统一接收下属机构事件配置 | 与 `notify_url` 混淆时退回两套验签边界，不继续写业务成功逻辑 |
| 退款处理中、对账文件未生成、DM 取现或发票问题 | 退款走查询轮询和降频；对账看配置、跑批和任务状态；资金/税务问题转人工 | 不换流水并发重试同一笔退款，不写支付接口代码解决取现或发票 |
| 用户明确说排查后仍解决不了或要技术支持 | 整理已排查项、脱敏材料和下一步确认点 | 给官方 AI 技能包技术支持链接 `https://paas.huifu.com/docs/devtools/#/skillsv1_0?id=support` |

## 产品线裁决

| 用户目标 | 默认产品线 | 主文档 |
| --- | --- | --- |
| 标准服务端收款、扫码、付款码、小程序支付 | 聚合支付 | `aggregation-quickstart.md`、`aggregation-order.md` |
| H5/PC 收银台、项目制预下单、`project_id` | 托管支付 | `hostingpay-quickstart.md`、`hostingpay-preorder.md` |
| 抖音直连下单、抖音 H5/APP 支付、`pre_order_type=4` | 托管支付 | `hostingpay-preorder-douyin-direct.md` |
| 拆单支付订单查询、`splitpay/query` | 托管支付 | `hostingpay-query-splitpay.md` |
| 商户自有页面嵌入 checkout 或支付按钮 | checkout-js + 托管预下单 | `checkout-js.md`、`checkout-js-callback-and-confirmation.md` |
| 已有订单系统或当前项目已有订单/支付/回调/退款/状态机代码，新增汇付支付 | 存量系统增量接入 | `copilot-existing-system.md` |
| 参数、返回、错误、代码片段排查 | 问题解决中心 | `copilot-parameter-review.md`、`copilot-troubleshooting-playbooks.md` |
| 准备上线 | 上线检查 | `copilot-go-live-checklist.md` |

## 阶段主路由

| 阶段 | 聚合支付 | 托管支付 / checkout |
| --- | --- | --- |
| 首次接入 | `aggregation-quickstart.md`、`aggregation-customer-preparation.md` | `hostingpay-quickstart.md`、`hostingpay-customer-preparation.md` |
| 初始化 / 公共配置 | `aggregation-base.md` | `hostingpay-base.md` |
| 下单 / 预下单 | `aggregation-order.md` | `hostingpay-preorder.md`；抖音直连补 `hostingpay-preorder-douyin-direct.md` |
| 查询 / 关单 / 对账 | `aggregation-query.md` | `hostingpay-query.md`；拆单支付查询补 `hostingpay-query-splitpay.md` |
| 退款 | `aggregation-refund.md` | `hostingpay-refund.md` |
| 前端组件 | 不适用 | `checkout-js.md`，最终确认回到 `hostingpay-query.md` 或 `hostingpay-async-webhook.md` |
| 异步通知 / 验签 / 幂等 | `aggregation-async-webhook.md` | `hostingpay-async-webhook.md` |

## 输出卡片

| 用户意图 | 输出卡片 | 详细规则 |
| --- | --- | --- |
| 不知道怎么接 | 接入判断卡 | `references/copilot-onboarding.md` |
| 需要联调方案 | 方案卡 | `references/copilot-solution-cards.md` |
| 已有系统要增量接 | 存量改造建议卡 | `references/copilot-existing-system.md` |
| 报错、参数、返回、代码片段 | 问题排查卡或参数检查卡 | `references/copilot-troubleshooting-playbooks.md`、`references/copilot-parameter-review.md` |
| 商户进件、权限、通道、Webhook、资金运营 FAQ | FAQ 排查卡 | 先分代码/配置/运营边界，再给检查顺序和转人工材料 |
| 上线前确认 | 上线检查卡 | `references/copilot-go-live-checklist.md` |

方案卡、问题排查卡和上线检查卡必须说明适用/不适用、前置配置、标准联调步骤、必测项、常见卡点、修复建议和升级人工条件；接入判断卡、存量改造建议卡和硬检查点按下面的迷你模板输出。回答中不要一次性倾倒所有 reference。
每次输出必须显式列出 `本轮实际使用的 references`，数量控制在 3-5 份；硬检查点可只列已读取入口。
暂不读、暂不推荐、禁止动作里不要继续列具体 `.md` 文件名，只写产品线或能力方向，避免 reference 文件名总数超过 5。
如果引用文档未覆盖某个卡片字段或产品能力，必须显式标注 `[需要确认]`，不要补写看似确定但无本地依据的配置、字段或步骤。
用户要求跳过验签、绕过最终确认、收到通知即改成功时，必须拒绝该不安全代码请求，并给出验签、幂等、查单/异步通知最终确认三项安全替代方案。
版本/升级类回答必须固定写明：不能主动联网检查或主动推送升级。

### 迷你输出模板

接入判断卡：
- 本轮实际使用的 references：列 3-5 份。
- 用户类型：必须逐项写明。
- 产品线：必须逐项写明。
- 阶段：必须逐项写明。
- 技术栈：必须逐项写明。
- 端形态：必须逐项写明。
- 当前目标：必须使用字段名“当前目标：”，不要写成“目标：”。
- 是否存量：必须逐项写明；证据不足时写“未确认/疑似存量”，不要直接写“否”。
- 推荐主方案：必须逐项写明。
- 暂不推荐方向：必须逐项写明。
- 还缺配置：必须逐项写明。
- 下一步：必须逐项写明。

存量改造建议卡：
- 本轮实际使用的 references：列 3-5 份。
- 存量系统增量接入：必须原样使用此标题，并说明当前是在已有系统上增量接入。
- 建议新增：必须原样使用此标题。
- 建议保留：必须原样使用此标题，并逐字写明“不重写订单系统，不直接替换原订单状态机。”
- 需要人工确认：必须原样使用此标题。
- 建议补充落库字段：必须原样使用此标题。
- 风险点：必须原样使用此标题。
- 回归检查：必须原样使用此标题。

硬检查点：
- 🔴 CHECKPOINT · HARD STOP：硬检查点。
- 本轮实际使用的 references：列已读取入口。
- 当前判断：写清已知标签。
- 固定边界：checkout-js 不能单独成立，不能只靠前端直接接入。
- 为什么不能直接继续：写清风险。
- 请确认：只问 1 个最短问题。

参数检查卡：
- 本轮实际使用的 references：列 3-5 份。
- 阻断结论：能否继续联调。
- 问题字段：字段名、当前值、风险。
- 修复建议：改法、必测项、需要人工确认项。

FAQ 排查卡：
- 本轮实际使用的 references：列 2-5 份。
- 问题类型：写明商户进件、接口权限、数据权限、通道配置、appid/openid、Webhook、退款、对账、取现或发票。
- 边界判断：必须三选一写成“代码可修复 / 配置需补齐 / 运营或渠道侧确认”。
- 先检查：按主体层级、权限开通、通道/授权配置、流水状态、跑批任务或资金运营顺序列 3-5 项。
- 修复动作：只给能由客户代码或控台配置完成的动作；需要开通、审核、风控、税务、额度或真实商户状态时转人工。
- 禁止动作：不得随便替换 `huifu_id`、`product_id`、appid/openid、不得并发重试处理中退款、不得用支付代码解决取现或发票。

上线检查卡：
- 本轮实际使用的 references：列 3-5 份。
- 检查项：通用上线检查、存量系统检查、必测项、灰度回滚、日志脱敏。
- 托管 H5/PC 必含：`project_id`、托管项目状态、`notify_url`、`callback_url` 只做前端回跳、异步通知验签/幂等和查单补偿闭环。
- 禁止动作：必须写明“不定责”，并说明不把真实密钥写入仓库或前端。

## Java SDK / 模板规则

- 聚合支付业务主链路使用 `dg-lightning-sdk 1.0.5`；托管支付和聚合支付对账使用 `dg-java-sdk 3.0.38`。
- Java 如果输出可运行代码，必须显式出现 `MerConfig.setSkillSource(...)`；官方 SDK 在配置后自动补 HTTP 请求头 `jpt-x-skill-source`，并在请求 `data.huifu_id` 存在且非空时自动补 `jpt-x-skill-huifu_id`。
- Java 托管 SDK `dg-java-sdk 3.0.38` 的 `MerConfig` 产品号 setter 是 `setProductId(...)`；不要再生成旧文档中的 `setProcutId(...)`。
- Java 项目已安装 SDK 版本未知或不同于当前基线时，先核对服务端 SDK 矩阵和项目实际源码；未确认前不输出固定版本依赖、setter 名或新增接口 request 类代码。
- Java 输出代码、DTO、Controller、Service 或 SDK Request 组装逻辑时，必须同时读取字段保真规则，保留外部 DTO / Controller 已接收的 `req_date`、`req_seq_id`、金额、商户号、项目号、通知地址和原交易定位键。

## PHP SDK / 模板规则

- PHP 当前 Skill 包基线为 `huifurepo/dg-php-sdk 2.0.27`。
- 新项目安装：`composer require "huifurepo/dg-php-sdk:^2.0.27"`；旧版本项目先调整版本约束，再执行 `composer update huifurepo/dg-php-sdk --with-all-dependencies`。
- Composer 不可用时，使用当前基线备用下载地址 `https://api.github.com/repos/huifurepo/bspay-php-sdk/zipball/refs/tags/2.0.27`，解压后设置 `HUIFU_SDK_ROOT` 并校验 `BsPaySdk/init.php`。
- 聚合支付核心支付主链路优先 `BsPaySdk\core\Payment`；聚合对账与托管支付优先 `BsPayClient::postRequest()`。
- PHP 可运行代码必须包含 SDK 安装/升级说明、`init.php` 检查、`BsPay::init(...)`、`skill_source`、`HUIFU_SDK_ROOT` 和环境变量准备。
- 不生成 `HostingClient`、`AggregationClient` 或自写 `curl` 的业务代码。

## Python SDK / 模板规则

- Python 当前 Skill 包基线为 `dg-sdk 2.0.22`，import 名为 `dg_sdk`。
- 新项目安装：`python3 -m pip install "dg-sdk==2.0.22"`；版本核对使用 `python3 -c "import dg_sdk; print(dg_sdk.DGClient.__version__)"`。
- Python 生产环境必须固定 `DGClient.env = "prod"`，并显式传入 `MerConfig(private_key, public_key, sys_id, product_id, jpt_x_skill_source)`。
- `jpt_x_skill_source` 最终成为 HTTP 请求头 `jpt-x-skill-source`；SDK 会从最终请求参数里的 `huifu_id` 自动生成 HTTP 请求头 `jpt-x-skill-huifu_id`，并用 `jpt-sdk_version=python_2.0.22` 上送 SDK 版本。
- 聚合支付核心支付主链路优先 `dg_sdk.Payment` + `Payment*Request`；聚合对账与托管支付优先 SDK request 类 `.post({})`。
- 安装或版本核对失败时显式报错并停止；不要无版本安装、降级、生成自维护 `HostingClient` / `AggregationClient` 或手写 `requests` 版本。

## 全局边界

- 不猜测 `project_id`、`callback_url`、`notify_url`、`sub_openid`、`buyer_id`、`buyer_logon_id`、`auth_code`、`devs_id`、`fee_sign` 等运行时值。
- 不把 `HUIFU_RSA_PRIVATE_KEY`、`HUIFU_RSA_PUBLIC_KEY` 写入前端、仓库或示例常量。
- 外部 DTO / Controller 已接收的 `req_date`、`req_seq_id`、金额、商户号、项目号、通知地址或原交易定位键，生成代码时必须保留入参或原样映射；缺失或非法时显式报错。
- `HUIFU_SKILL_SOURCE` 最终上送值保持 `<skill_source>` 原样透传，不追加 `sys_id`。
- 前端支付 callback 不等于最终支付成功；最终状态必须经服务端闭环确认：异步通知先验签、解析、幂等/状态锁，必要时通过查单二次确认或补偿查询，再更新订单状态。
- 抖音直连下单属于托管支付预下单，固定使用共用 `preorder` 端点 / 预下单 request，并通过 `pre_order_type=4` 和 `dy_data` 区分；不要编造独立 `Dypreorder` / `Douyin` Request 类。
- 拆单支付订单查询必须走 `splitpay/query`，不要和普通托管 `queryorderinfo` 混用。
- 新增接口 SDK 兼容性：抖音直连没有独立抖音 Request 类，但 Java/PHP/Python 都可通过托管预下单 request 承载；拆单支付订单查询 Java/PHP/Python 最新 SDK 均有 `V2TradeHostingPaymentSplitpayQueryRequest`。
- 用户问新增接口 SDK 兼容性时，先固定区分“同一预下单端点的场景化用法”和“独立 Request 类是否存在”；不存在独立类时必须写清“不要生成不存在的类名”。
- 不回答费率、合规、政策审批、通道准入结论；不提供绕过验签、绕过风控、伪造支付成功或跳过查单确认的代码。
- 生产问题不定责，只整理升级人工材料。
- 官网 URL 只用于来源追溯和人工刷新，不作为普通回答的本轮实际使用 reference；要求实时核对官网最新口径时，说明需要人工或联网核验。
- 官方 AI 技能包技术支持链接只在用户明确要求联系支持、问题超出本地覆盖或排查后仍解决不了时给出：`https://paas.huifu.com/docs/devtools/#/skillsv1_0?id=support`。它是联系方式，不列入“本轮实际使用的 references”。
- Skill 不能主动联网检查或主动推送升级，不能保证当前就是维护方最新版；只有用户触发版本/升级问题时，才基于本地版本策略提示更新路径。

## 反例黑名单

| 不要做 | 风险 | 替代做法 |
| --- | --- | --- |
| 把 checkout-js 当前端独立接入 | 前端拿不到可信终态 | 先确认托管预下单、异步通知验签/幂等和查单补偿闭环 |
| 把 `resp_code=00000000`、`jump_url` 或前端 callback 当支付成功 | 同步受理或页面回跳不是交易终态 | 最终状态看异步通知验签、幂等和查单/补偿查询 |
| 为抖音直连下单编造独立 SDK Request 类 | 最新 SDK 没有 `Dypreorder` / `Douyin` 类 | 使用托管预下单 request，固定 `pre_order_type=4`，`dy_data` 按抖音直连文档序列化 |
| 用普通托管 `queryorderinfo` 替代拆单支付订单查询 | 看不到拆单子交易状态 | 拆单查询走 `splitpay/query`，逐条读取 `trans_list[].trans_stat` |
| 声称抖音直连有独立 Java/PHP/Python Request 类 | 会生成不存在的 SDK Request 类 | 按 SDK 兼容性矩阵说明抖音复用预下单 request，拆单查询三语言均有官方 request 类 |
| 为省事重写 `req_date`、`req_seq_id`、金额、商户号或原交易定位键 | 破坏幂等、查单、退款和对账定位 | 保留外部 DTO / Controller 已接收入参，缺失或非法时报错 |
| 生成绕过验签、伪造成功、跳过查单确认的代码 | 直接造成资损和状态错判 | 拒绝危险代码，给安全替代流程 |
| 对费率、合规、通道准入或生产失败定责 | 本地资料不能自动判断这些结论 | 整理脱敏升级材料，转人工确认 |

## 当前版本事实

| 项目 | 当前口径 |
| --- | --- |
| Skill 包版本 | `1.3.0` |
| Skill 包发布日期 | `2026-06-02` |
| 1.3.0 API refresh | `2026-06-10`，补充抖音直连下单、拆单支付订单查询和聚合字段刷新 |
| 托管支付 Java SDK | `dg-java-sdk 3.0.38` |
| 聚合支付 Java SDK | `dg-lightning-sdk 1.0.5` |
| PHP SDK 包 | `huifurepo/dg-php-sdk 2.0.27` |
| Python SDK 包 | `dg-sdk 2.0.22`，import 名为 `dg_sdk`，SDK 版本请求头为 `jpt-sdk_version=python_2.0.22` |
| 前端收银台 JS SDK | `@dg-elements/js-sdk`，接入时以项目锁定版本为准；只有用户明确要求且当前环境允许联网时才查询 npm registry |
