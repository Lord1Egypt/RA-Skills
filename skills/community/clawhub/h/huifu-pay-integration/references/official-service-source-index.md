# 官方服务资料源索引

本文件是 1.3.0 接入副驾驶的本地官方资料源索引。Skill 正常回答只依赖本地 reference；官网 URL 仅用于来源追溯、人工刷新和显式核验，不作为运行时检索入口。

只沉淀脱敏摘要、判断规则、路由和必要摘录；不复制官网大图、完整 FAQ 库、真实商户信息、订单号、用户标识或密钥。

## 目录

- [资料源登记](#资料源登记)
- [运行时规则](#运行时规则)
- [本地覆盖矩阵](#本地覆盖矩阵)
- [不覆盖和转人工菜单](#不覆盖和转人工菜单)
- [技术支持联系方式](#技术支持联系方式)
- [高频 FAQ 分类映射](#高频-faq-分类映射)
- [字段规范](#字段规范)
- [禁止沉淀](#禁止沉淀)

## 资料源登记

| 官方来源类型 | 来源 URL | 采集日期 | 采集范围 | 刷新负责人 | 本地用途 |
| --- | --- | --- | --- | --- | --- |
| 业务指引 | https://paas.huifu.com/open/service/guide/#/ | 2026-05-15 | 产品功能、商户材料、控台配置、业务开通、权限边界 | 李稼祥 | 配置清单、开通前置、人工升级材料 |
| 联调攻略 | https://paas.huifu.com/open/service/develop/#/ | 2026-05-15 | 支付产品联调步骤、托管支付、分账、异步回调、常见接入顺序 | 李稼祥 | 方案卡、联调步骤、必测项、常见卡点 |
| FAQ | https://paas.huifu.com/open/service/faq/#/ | 2026-05-15 | 高频错误、权限/配置/状态/流水/回调/签名问题 | 李稼祥 | 问题分类、排查顺序、修复建议、升级人工条件 |
| API 文档 | https://paas.huifu.com/partners/lightning/api/、https://paas.huifu.com/partners/api/doc/ | 2026-06-10 | 聚合支付下单、查单、关单、退款、对账、托管预下单、抖音直连下单、拆单支付订单查询页面 | 李稼祥 | 字段差异刷新、接口新增/修改确认 |
| AI 技能包技术支持 | https://paas.huifu.com/docs/devtools/#/skillsv1_0?id=support | 2026-06-12 | 官方 AI 技能包技术支持联系方式 | 李稼祥 | 用户明确要求技术支持或本地排查仍解决不了时给出联系方式 |

## 运行时规则

1. 普通回答不得要求访问官网，也不要把官网 URL 列入“本轮实际使用的 references”。
2. 用户问 FAQ、官网能力、不覆盖能力或人工升级材料时，先读本文件，再读对应本地 playbook 或产品线 reference。
3. 用户明确要求“核对官网最新口径”“看官网现在怎么写”时，说明本地 Skill 不内置实时官网抓取；如当前环境允许联网或人工核验，再以官网为核验来源。
4. 回答依据仍控制为 3-5 份本地 `references/*.md`；官网 URL 只作为来源追溯和刷新依据，不参与普通回答路径。
5. 如果本地覆盖状态为“部分覆盖”“不覆盖”或“转人工”，不得为了填满方案卡而生成完整模板或生产判断结论。
6. AI 技能包技术支持链接只在用户明确要求联系支持、问题超出本地覆盖或排查后仍解决不了时给出；它是联系方式，不列入“本轮实际使用的 references”。

## 本地覆盖矩阵

| 能力/问题表达 | 官方来源类型 | 本地权威 reference | 覆盖状态 | 本地处理口径 | 禁止输出 | 刷新依据与采集日期 |
| --- | --- | --- | --- | --- | --- | --- |
| 首次接入、不知道选聚合还是托管 | 业务指引、联调攻略 | `references/copilot-onboarding.md`、`references/copilot-solution-selection.md`、`references/shared-overview.md` | 已覆盖 | 识别用户类型、产品线、阶段、技术栈、端形态和当前目标；输出接入判断卡 | 不直接跳到字段表；不要求访问官网 | 业务指引/联调攻略，2026-05-15 |
| 聚合支付微信、支付宝、银联常规接入 | 联调攻略、API 文档 | `references/aggregation-order.md`、`references/aggregation-order-method-wechat.md`、`references/aggregation-order-method-alipay.md`、`references/aggregation-order-method-unionpay.md` | 已覆盖 | 按渠道给前置配置、接口顺序、必测项和常见卡点；反扫设备信息、有效期和贴息字段按最新 API 口径处理 | 不复制官网截图；不生成未覆盖渠道完整模板 | 联调攻略/API 文档，2026-06-10 |
| 聚合支付查单、关单、对账 | 联调攻略、FAQ、API 文档 | `references/aggregation-query.md`、`references/aggregation-query-reconciliation.md`、`references/copilot-troubleshooting-playbooks.md` | 已覆盖 | 区分原交易定位键、合单关单 `merge_flag`、平台流水、对账文件查询和状态确认 | 不把同步受理当终态；不手写 Java HTTP 替代官方 SDK | 联调攻略/FAQ/API 文档，2026-06-10 |
| 聚合支付退款、退款查询 | 联调攻略、FAQ、API 文档 | `references/aggregation-refund.md`、`references/aggregation-refund-query.md`、`references/copilot-parameter-review.md` | 已覆盖 | 说明退款申请、退款查询、分账/补贴/终端/确认分账/手续费返还字段和流水关系 | 不混用原支付流水和退款流水；不把 `tx_metadata` 当请求包装层上送 | 联调攻略/FAQ/API 文档，2026-06-10 |
| 托管支付 H5/PC、小程序预下单 | 业务指引、联调攻略、API 文档 | `references/hostingpay-preorder.md`、`references/hostingpay-preorder-h5-pc.md`、`references/hostingpay-preorder-alipay-mini.md`、`references/hostingpay-preorder-wechat-mini.md`、`references/hostingpay-customer-preparation.md` | 已覆盖 | 沉淀 `project_id`、项目状态、预下单、跳转/拉起、异步通知验签/幂等 + 查单补偿的服务端闭环；`hosting_data` 按统一收银台扩展参数集合处理 | 不用聚合正扫冒充 H5/PC 收银台；不猜 `project_id` | 业务指引/联调攻略/API 文档，2026-06-10 |
| 托管支付抖音直连下单 | API 文档、联调攻略 | `references/hostingpay-preorder-douyin-direct.md`、`references/hostingpay-preorder.md`、`references/hostingpay-async-webhook.md` | 已覆盖 | 固定识别托管预下单 `pre_order_type=4`、`dy_data`、`busi_scene`、`jump_url` 和抖音异步返回；最终状态仍走服务端闭环 | 可以复用托管预下单 request，但不能按 H5/PC `pre_order_type=1` 场景处理；不把 `jump_url` 当终态 | API 文档，2026-06-10 |
| 托管拆单支付订单查询 | API 文档、FAQ | `references/hostingpay-query-splitpay.md`、`references/hostingpay-query.md`、`references/hostingpay-preorder-wechat-mini.md` | 已覆盖 | 使用原拆单支付 `org_req_date + org_req_seq_id` 查询，并逐条读取 `trans_list[].trans_stat` | 不用普通托管查单替代拆单明细查询；不把订单级 `order_stat` 当所有子交易终态 | API 文档，2026-06-10 |
| checkout-js 自有页面嵌入 | 联调攻略 | `references/checkout-js.md`、`references/checkout-js-create-preorder-contract.md`、`references/checkout-js-callback-and-confirmation.md` | 已覆盖 | 明确 checkout-js 依赖托管预下单，前端 callback 只做流程回调 | 不在未确认服务端预下单、异步通知和查单补偿闭环时给安装和接法 | 联调攻略，2026-05-15 |
| 异步通知、验签、幂等、固定回包 | 联调攻略、FAQ | `references/shared-async-notify.md`、`references/shared-signing-v2.md`、`references/shared-webhook-signing.md`、`references/copilot-troubleshooting-playbooks.md` | 已覆盖 | 先验签、再解析、再事件级幂等和状态锁；最终状态通过查单二次确认或补偿查询闭环 | 不提供跳过验签、收到通知即改成功、伪造支付成功代码 | 联调攻略/FAQ，2026-05-15 |
| 商户进件、接口/数据权限、通道配置、appid/openid、Webhook 高频 FAQ | FAQ、业务指引 | `references/merchant-onboarding-faq.md`、`references/copilot-troubleshooting-playbooks.md`、`references/official-service-source-index.md` | 已覆盖 | 只使用脱敏摘要；按进件结果、接口权限、数据权限、通道路由、appid/openid、授权目录和 Webhook 配置给排查顺序 | 不复制原始 FAQ 目录、截图/base64 或真实数据；不承诺通道准入/审核结果 | FAQ，2026-06-10 |
| 分账参数、分账退款、分账查询 | 业务指引、联调攻略、FAQ | `references/aggregation-order-tx-metadata.md`、`references/hostingpay-payload-construction.md`、`references/copilot-solution-cards.md` | 部分覆盖 | 覆盖聚合和托管常用分账参数、接收方、金额/比例、退款关系；复杂权限和手续费承担转人工确认 | 不自动判断分账权限、费率或资金合规结论 | 业务指引/联调攻略/FAQ，2026-05-15 |
| 存量系统新增汇付、改回调、补退款 | 业务指引、FAQ | `references/copilot-existing-system.md`、`references/copilot-go-live-checklist.md`、`references/copilot-troubleshooting-playbooks.md` | 已覆盖 | 建议新增适配层、保留原订单逻辑、补落库字段、做状态映射和回归检查 | 不重写订单系统；不直接替换原状态机 | 业务指引/FAQ，2026-05-15 |
| 上线检查、灰度、回滚、生产失败材料 | 业务指引、FAQ | `references/copilot-go-live-checklist.md`、`references/copilot-existing-system.md`、`references/official-service-source-index.md` | 已覆盖 | 输出通用上线检查、存量系统检查、必测项、日志脱敏、升级人工材料 | 不对生产问题定责；不把真实密钥写入仓库或前端 | 业务指引/FAQ，2026-05-15 |

## 不覆盖和转人工菜单

| 能力/问题表达 | 官方来源类型 | 本地权威 reference | 覆盖状态 | 本地处理口径 | 禁止输出 | 刷新依据与采集日期 |
| --- | --- | --- | --- | --- | --- | --- |
| 花呗分期、分期支付 | 联调攻略、业务指引 | `references/official-service-source-index.md`、`references/aggregation-order-method-alipay.md` | 转人工 | 识别为支付宝相关扩展能力；整理支付产品、买家侧能力、商户开通状态、测试环境、报错和流水，转商务/运营/汇付支持确认 | 不生成完整方案卡、可联调代码、费率/风控/开通结论 | 联调攻略/业务指引，2026-05-15 |
| 大额支付、大额转账、银行大额 | 业务指引、联调攻略 | `references/official-service-source-index.md`、`references/hostingpay-preorder-h5-pc-channel.md`、`references/hostingpay-refund.md` | 部分覆盖 | 只给资料准备、字段位置和人工升级材料；退款字段可按本地托管退款文档解释 | 不判断限额、准入、资质、失败责任或开通结果 | 业务指引/联调攻略，2026-05-15 |
| 网银、银联 App、银联网页授权 | 业务指引、联调攻略 | `references/official-service-source-index.md`、`references/aggregation-order-method-unionpay.md` | 部分覆盖 | 可识别为银联扩展能力，说明本地仅覆盖部分字段和接入线索；完整模板转人工 | 不扩展完整联调模板；不承诺可直接上线 | 业务指引/联调攻略，2026-05-15 |
| 全渠道资金、取现、结算、发票、投诉、风险类能力 | 业务指引、FAQ | `references/official-service-source-index.md` | 不覆盖 | 仅整理问题类型、商户/流水/时间/影响范围等升级材料 | 不生成支付接入代码；不输出资金、结算、风险处置结论 | 业务指引/FAQ，2026-05-15 |
| 费率、合规、政策审批、通道准入 | 业务指引 | `references/official-service-source-index.md` | 转人工 | 明确 Skill 不给结论；整理用户已知事实后转商务、运营、合规或汇付支持 | 不回答费率政策、合规判断、审批结果或通道准入结论 | 业务指引，2026-05-15 |
| 要求实时核对官网最新政策 | 业务指引、联调攻略、FAQ | `references/official-service-source-index.md` | 转人工 | 说明本地 Skill 不内置实时官网抓取；如需最新口径，应人工或在允许联网时核验官网 | 不假装已实时访问官网；不把旧本地口径说成最新官网结论 | 三类官网来源，2026-05-15 |
| AI 技能包使用问题、排查后仍解决不了、要求联系技术支持 | AI 技能包技术支持 | `references/official-service-source-index.md`、`references/copilot-troubleshooting-playbooks.md` | 转人工 | 先整理已排查项、脱敏请求/响应、环境、SDK 版本、流水、时间和影响范围，再给官方 AI 技能包技术支持链接 | 不把联系方式当作接口文档依据；不承诺技术支持处理结果或时效 | AI 技能包技术支持，2026-06-12 |

## 技术支持联系方式

当用户明确要求联系技术支持、当前问题超出本地覆盖范围，或已按本地 Playbook 排查仍无法解决时，可给出官方 AI 技能包技术支持入口：

`https://paas.huifu.com/docs/devtools/#/skillsv1_0?id=support`

给出该链接前，优先整理可脱敏提交的材料：问题描述、环境、接口路径、SDK 版本、脱敏请求/响应、流水、时间、日志、影响范围和已执行动作。不要把真实密钥、真实用户标识或完整生产数据写入回答。

## 高频 FAQ 分类映射

| 用户问题/报错 | 分类 | 本地权威 reference | 本地处理口径 |
| --- | --- | --- | --- |
| URL 未注册、redirect_uri 域名不一致 | 配置/渠道权限 | `references/copilot-troubleshooting-playbooks.md`、`references/hostingpay-customer-preparation.md` | 检查渠道侧域名、appid、回跳地址、`notify_url`/`callback_url` 和控台配置；必要时转运营/商务 |
| 商户进件是否成功、返回 `huifu_id` 但业务开通失败 | 商户进件/实名 | `references/merchant-onboarding-faq.md`、`references/copilot-troubleshooting-playbooks.md` | 有 `huifu_id` 只能说明账户已创建，不等于支付产品可交易；继续检查银行卡、结算、取现、渠道开通和 `token_no` |
| 接口权限认证失败、`20003`、数据权限认证失败 | 接口/数据权限 | `references/merchant-onboarding-faq.md`、`references/copilot-troubleshooting-playbooks.md` | 接口权限看 `sys_id` 和接口路径；数据权限看 `product_id`、`sys_id`、`huifu_id`、`upper_huifu_id` 和层级 |
| 该路由下未配置可用通道、入驻信息配置有误 | 通道/路由 | `references/merchant-onboarding-faq.md`、`references/copilot-troubleshooting-playbooks.md` | 检查通道开通、线上/线下业务、`pay_channel`、`pay_scene`、`fee_type`；不指定通道时不要传空 `channel_no` |
| `sub_mch_id` 与 `sub_appid` 不匹配、`sub_openid` 不匹配 | appid/openid | `references/merchant-onboarding-faq.md`、`references/aggregation-customer-preparation.md`、`references/hostingpay-customer-preparation.md` | 检查 appid 绑定、首尾空格、openid 是否来自同一 appid 授权流程 |
| orderExpireTime 或 time_expire 格式不正确 | 参数格式 | `references/copilot-parameter-review.md`、`references/aggregation-order.md` | 检查时间格式、是否未来时间、是否与接口字段名匹配 |
| 数据权限认证失败 | 权限/归属 | `references/copilot-troubleshooting-playbooks.md`、`references/shared-request-header-policy.md` | 检查 `product_id`、`sys_id`、`huifu_id`、`upper_huifu_id`、来源头和归属关系 |
| 重复交易、流水重复 | 流水幂等 | `references/copilot-parameter-review.md`、`references/copilot-troubleshooting-playbooks.md` | 检查 `req_seq_id` 是否重复使用；业务侧必须落库并保证幂等 |
| 交易成功收到 2 条异步消息 | 异步通知 | `references/shared-async-notify.md`、`references/copilot-troubleshooting-playbooks.md` | 用 `notify_type` 区分交易异步和账务异步，业务必须以平台流水或业务流水做幂等 |
| Webhook 找不到 `sign`、收不到下属机构交易消息 | Webhook 配置 | `references/shared-webhook-signing.md`、`references/merchant-onboarding-faq.md`、`references/copilot-troubleshooting-playbooks.md` | `sign` 常在 URL query；服务商接子商户事件时检查统一接收下属机构事件配置 |
| 支付验证签名失败、前端支付签名验证失败 | 签名/前端拉起 | `references/shared-signing-v2.md`、`references/checkout-js-callback-and-confirmation.md` | 区分 API RSA 验签、前端拉起签名、控台 Webhook MD5，不混用签名材料 |
| 托管项目信息不存在、非进行中项目不允许交易 | 托管配置 | `references/hostingpay-customer-preparation.md`、`references/hostingpay-preorder.md` | 检查 `project_id`、项目状态、托管权限和支付方式启用状态 |
| 退款单不存在、原 PA 流水号不能为空 | 退款流水 | `references/aggregation-refund-query.md`、`references/hostingpay-refund-query.md` | 区分原支付流水、退款请求流水、平台流水；退款查询使用退款交易自身定位键 |
| 退款一直处理中、请求频率过高 | 退款状态/频率 | `references/merchant-onboarding-faq.md`、`references/copilot-troubleshooting-playbooks.md` | 轮询退款查询并等待终态，不换流水并发重试；同商户/同订单请求需要降频 |
| 分账金额总和必须等于交易金额、比例格式错误 | 分账 | `references/aggregation-order-tx-metadata.md`、`references/hostingpay-payload-construction.md` | 检查分账权限、金额/比例、接收方、手续费承担关系；复杂权限转人工 |
| 对账文件未生成、DM 取现额度不足、手续费发票未收到 | 对账/资金/税务运营 | `references/merchant-onboarding-faq.md`、`references/official-service-source-index.md` | 对账先查配置和跑批状态；取现、发票、税务和额度问题只整理材料转人工 |
| 生产失败是否汇付问题 | 升级人工 | `references/copilot-go-live-checklist.md`、`references/official-service-source-index.md` | 不定责，只整理环境、接口、SDK 版本、脱敏请求/响应、流水、时间、日志、影响范围和已做动作 |

## 字段规范

本文件新增或维护索引项时必须包含：

- `能力/问题表达`
- `官方来源类型`
- `本地权威 reference`
- `覆盖状态：已覆盖 / 部分覆盖 / 不覆盖 / 转人工`
- `本地处理口径`
- `禁止输出`
- `刷新依据与采集日期`

## 禁止沉淀

- 不保存真实商户号、真实订单号、真实密钥、真实用户标识、真实回调地址。
- 不复制官网大图、完整 FAQ 库或非必要长篇原文。
- 不将费率、合规、政策审批、通道准入写成自动判断结论。
- 不把未 release 产品能力写入方案卡或可联调代码。
- 不把官网 URL 当作普通回答的本轮实际使用 reference。
