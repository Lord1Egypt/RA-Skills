# 汇付聚合支付 — 基础快速导览

基于汇付 dg-lightning-sdk 的聚合支付接入基础导览，包含 SDK 初始化、Factory 调用模式、支付类型说明和公共参数。

## 定位

所有聚合支付文档链路的公共前置依赖，接入聚合支付前必读。

## 核心内容

- **SDK 初始化**：dg-lightning-sdk 1.0.5 安装与 Spring Boot 集成
- **Factory 调用模式**：`Factory.Payment.Common()` 获取客户端
- **支付类型**：微信/支付宝/银联 共 10 种 trade_type
- **公共参数**：sys_id、product_id、req_seq_id 等
- **错误码**：完整错误码速查表
- **技术规范**：签名规则、异步通知、Webhook

## 与托管支付的区别

| 方面 | 聚合支付当前文档链路 | 托管支付 |
|------|-------------------|---------|
| SDK | dg-lightning-sdk 1.0.5 | dg-java-sdk 3.0.38 |
| 接入难度 | 低，Factory 模式 | 中，需手动构建 Request |
| 支付渠道 | 微信/支付宝/银联直接聚合 | 统一收银台（H5/小程序） |
| 适用场景 | 标准支付，快速上线 | 收银台托管，复杂业务 |

## 文件阅读地图

| 文件 | 相比官方文档额外补了什么 | 什么时候看 |
|-----|----------------------|-----------|
| `references/aggregation-base.md` | 补了触发词、选型建议、接入流程、环境变量和联调说明 | 第一次进入聚合支付路径时先看 |
| `references/aggregation-customer-preparation.md` | 补了 trade_type 对应的真实参数来源、渠道开通要求、授权链路 | 还没编码，先确认客户是否真的具备下单条件 |
| `references/aggregation-payload-construction.md` | 补了 `method_expand`、`acct_split_bunch`、`terminal_device_data` 和补贴类扩展字段的对象建模和序列化规范 | 要拼复杂请求对象时看 |
| `references/aggregation-java-sdk-quickstart.md` | 补了 Factory 初始化方式和 SDK 集成细节 | 要写初始化和首个调用示例时看 |
| `references/aggregation-common-params.md` | 补了 `sys_id` / `huifu_id` 区分、交易状态、金额与时间格式 | 不确定公共字段怎么解释时看 |
| `references/aggregation-error-codes.md` | 汇总常见错误码并强调它们主要用于排查 | 看到返回码异常时看，不拿它直接驱动业务终态 |
| `references/aggregation-java-tech-spec.md` | 补了签名、通知机制、连接池、重试策略等实现细节 | 联调、超时、通知接收时看 |
| `references/aggregation-async-webhook.md` | 补了 `notify_url` / Webhook 的边界、应答方式、验签和幂等 | 需要接交易回调时看 |
| `references/aggregation-faq.md` | 把渠道常见坑位集中整理 | 碰到场景性疑问时看 |

## 开发前先补两件事

1. 先看 `references/aggregation-customer-preparation.md`，梳理哪些参数是客户控台配置、前端授权、终端采集或上游订单沉淀出来的。
2. 再看 `references/aggregation-payload-construction.md`，把 `method_expand`、`acct_split_bunch`、`terminal_device_data`、`combinedpay_data`、`combinedpay_data_fee_info`、`trans_fee_allowance_info` 按对象完整建模，做完校验后再序列化；不要传 `tx_metadata` 包装层。
3. 官方产品介绍和开发指引还要求先完成业务开通 / 变更、应用配置和授权绑定；这些动作没完成时，不要只靠补参数强行下单。
