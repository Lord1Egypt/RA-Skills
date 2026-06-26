# 联调方案卡

本文件定义 1.3.0 的方案卡。每张卡只保留开发者联调必需信息。

## 目录

- [统一模板](#统一模板)
- [卡详写规则](#卡详写规则)
- [完整展开样例](#完整展开样例)
- [编号说明](#编号说明)
- [P0 方案卡](#p0-方案卡)
- [P1 方案卡](#p1-方案卡)
- [使用规则](#使用规则)

## 统一模板

每张方案卡输出时必须覆盖：

| 项 | 内容 |
| --- | --- |
| 适用场景 | 什么问题可以用这张卡 |
| 不适用场景 | 哪些场景不能套用 |
| 前置配置 | 商户、权限、密钥、回调、项目、渠道等 |
| 标准联调步骤 | 从配置、请求、支付/跳转、回调、查单到退款/对账 |
| 必测项 | 正常、异常、重复、退款、回调、状态确认等 |
| 常见卡点 | 高频 FAQ 和字段误用 |
| 修复建议 | 可执行检查和修改方向 |
| 升级人工 | 何时联系商务、运营、技术支持 |

## 卡详写规则

本文件中的 S01-S18 条目是方案卡入口和路由索引，不是把每张卡的 8 项内容完整复制在一处。实际输出某张方案卡时，必须按统一模板逐项展开，并到该条目列出的关键本地文档中读取依据。

如果某个关键本地文档没有明确覆盖模板中的某一项，可以基于已读取的本地文档做保守推断，但必须标注 `[需要确认]`；不能为了填满模板而编造前置配置、接口字段、必测项或升级条件。

## 完整展开样例

下面两张只作为写法样例。实际回答仍要按用户场景选择 1 张卡，并回到该卡列出的本地 reference 取依据。

### S03 聚合支付微信小程序

- 适用场景：用户要做微信小程序、公众号、JSAPI 类交易，服务端负责聚合支付下单和最终状态确认。
- 不适用场景：用户要 H5/PC 收银台、托管项目制页面、只接 checkout-js 前端组件，或希望仅以前端 callback 判定成功。
- 前置配置：确认 `huifu_id`、微信渠道配置、`trade_type` / 微信 openid 或对应渠道标识、`notify_url`、RSA 密钥和服务端下单权限。
- 标准联调步骤：先读 `aggregation-order-method-wechat.md` 确认微信参数，再按 `aggregation-payload-construction.md` 构造下单请求，支付完成后走异步通知验签/幂等和查单补偿闭环。
- 必测项：正常支付、重复通知幂等、支付中查单、失败/关闭、退款前后状态、通知验签失败处理。
- 常见卡点：微信用户标识缺失、渠道参数放错层级、只信前端结果、`notify_url` 不可公网访问、`huifu_id` 与来源头不一致。
- 修复建议：先保留原始请求/返回和验签结果，按本地字段文档逐项核对；缺渠道配置时标注 `[需要确认]`，不要编造 openid 或商户配置。
- 升级人工：涉及微信渠道准入、费率、风控拦截、生产事故定责或官方配置不确定时转人工。

### S08 托管支付 H5/PC 收银台

- 适用场景：用户要 H5/PC 跳转收银台、项目制托管支付、需要 `project_id` 和收银台页面。
- 不适用场景：标准扫码/付款码聚合支付、只要 checkout-js 前端组件、尚未完成托管项目配置。
- 前置配置：确认 `project_id`、托管项目状态、`huifu_id`、`notify_url`、`callback_url`、RSA 密钥、服务端预下单和最终查单能力。
- 标准联调步骤：按 `hostingpay-preorder-h5-pc.md` 完成预下单，按 `hostingpay-preorder-h5-pc-request.md` 核对请求字段，用户跳转收银台后通过异步通知验签/幂等和 `hostingpay-query.md` 查单二次确认或补偿查询形成最终状态闭环。
- 必测项：预下单成功、跳转地址可用、前端 callback 不直接改成功、异步通知验签和幂等、查单补偿、关单/退款链路。
- 常见卡点：缺 `project_id`、项目未启用、`callback_url` 和 `notify_url` 混用、只看浏览器回跳、未落库 `pre_order_id`。
- 修复建议：先补齐项目和回调配置，再做异步通知验签/幂等和查单补偿确认最终状态；存量商城只新增汇付适配层，不改原订单状态机主干。
- 升级人工：托管项目开通、项目状态异常、准入/费率/合规、生产责任归因不在本地 Skill 内判断。

## 编号说明

1.3.0 MVP 为了匹配交付优先级，将原方案中的 S11/S12/S13/S14 上移为当前 S09/S10/S11/S12；原 S09/S10 降为当前 P1 的 S13/S14；原 S15-S18 保持编号和内容含义不变。对照排期或旧评审材料时，以本段映射为准。

## P0 方案卡

| 编号 | 方案卡 | 适用 | 关键本地文档 |
| --- | --- | --- | --- |
| S01 | 聚合支付 Java 首次接入 | Java 服务端标准收款 | `aggregation-quickstart.md`、`aggregation-java-sdk-quickstart.md`、`aggregation-order.md`、`aggregation-query.md` |
| S02 | 聚合支付 PHP 首次接入 | PHP 服务端标准收款 | `aggregation-quickstart.md`、`aggregation-php-adapter.md`、`aggregation-order.md`、`aggregation-query-php-scenarios.md` |
| S03 | 聚合支付微信小程序 | 微信小程序、公众号、JSAPI 类交易 | `aggregation-order-method-wechat.md`、`aggregation-payload-construction.md`、`aggregation-async-webhook.md` |
| S04 | 聚合支付支付宝正扫/付款码 | 支付宝正扫、反扫、买家标识 | `aggregation-order-method-alipay.md`、`aggregation-order-response.md`、`aggregation-query.md` |
| S05 | 聚合支付查单/关单 | 下单后状态确认、关单、关单查询 | `aggregation-query.md`、`aggregation-query-payment-query.md`、`aggregation-query-trade-close.md` |
| S06 | 聚合支付退款/退款查询 | 原交易退款、部分退款、退款状态确认 | `aggregation-refund.md`、`aggregation-refund-query.md`、`aggregation-async-webhook.md` |
| S07 | 聚合支付随交易分账参数 | 下单携带分账、补贴、终端信息 | `aggregation-order-tx-metadata.md`、`aggregation-payload-construction.md` |
| S08 | 托管支付 H5/PC 收银台 | H5/PC 跳转收银台、project_id | `hostingpay-preorder-h5-pc.md`、`hostingpay-preorder-h5-pc-request.md`、`hostingpay-query.md` |
| S09 | 异步通知/验签/幂等 | 接收 notify_url 或控台 Webhook | `shared-async-notify.md`、`shared-webhook-signing.md`、`aggregation-async-webhook.md`、`hostingpay-async-webhook.md` |
| S10 | 上线前联调验收 | 联调完成准备上线 | `copilot-go-live-checklist.md`、`shared-release-checklist.md` |
| S11 | 存量订单系统新增汇付支付 | 已有订单系统新增汇付渠道 | `copilot-existing-system.md`、`aggregation-query.md`、`shared-async-notify.md` |
| S12 | 存量系统新增退款/退款查询 | 已有支付后补退款能力 | `copilot-existing-system.md`、`aggregation-refund.md`、`hostingpay-refund.md` |

## P1 方案卡

| 编号 | 方案卡 | 适用 | 关键本地文档 |
| --- | --- | --- | --- |
| S13 | 托管支付小程序预下单 | 托管微信/支付宝小程序 | `hostingpay-preorder-wechat-mini.md`、`hostingpay-preorder-alipay-mini.md`、`hostingpay-query.md` |
| S14 | checkout-js 嵌入支付组件 | 自有页面嵌入 checkout 或按钮 | `checkout-js.md`、`checkout-js-create-preorder-contract.md`、`checkout-js-callback-and-confirmation.md` |
| S15 | 存量系统异步通知改造 | 已有回调但幂等/验签/回包不稳 | `copilot-existing-system.md`、`shared-async-notify.md` |
| S16 | 存量系统支付状态映射 | 已有订单状态机，需要映射汇付状态 | `copilot-existing-system.md`、`aggregation-query-payment-query.md`、`hostingpay-query-payment-status-query.md` |
| S17 | 存量商城接入托管 H5/PC | 已有商城新增托管收银台 | `copilot-existing-system.md`、`hostingpay-preorder-h5-pc.md` |
| S18 | 存量系统接入分账参数 | 已有订单新增分账 | `copilot-existing-system.md`、`aggregation-order-tx-metadata.md`、`hostingpay-customer-preparation.md`、`hostingpay-payload-construction.md`、`hostingpay-preorder-h5-pc-request.md` |

## 使用规则

- 用户问题明确落到某张方案卡时，只输出该卡，不一次性列出 18 张。
- 首次接入优先 S01/S02/S03/S04/S08/S13/S14。
- 存量系统优先 S11/S12/S15/S16/S17/S18。
- 排查问题优先跳到 `copilot-troubleshooting-playbooks.md`，不要把方案卡当 FAQ。
- 若方案卡涉及 checkout-js，必须确认托管预下单、异步通知验签/幂等和查单补偿组成的服务端最终确认闭环。
- 抖音直连下单直接路由到 `hostingpay-preorder-douyin-direct.md`，不要套 H5/PC 收银台方案卡。
- 拆单支付订单查询直接路由到 `hostingpay-query-splitpay.md`，不要套普通托管交易查询字段表。
