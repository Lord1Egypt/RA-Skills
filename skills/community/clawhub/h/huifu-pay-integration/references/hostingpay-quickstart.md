# 托管支付基础快速接入


## 目录

- 这份文档解决什么问题
- 文件阅读地图
- 5 分钟快速接入
- 联调环境
- 参考资料索引

所有托管支付场景文档的前置依赖，包含 SDK 安装初始化、技术规范、公共参数和错误码。

## 这份文档解决什么问题

在调用任何汇付支付接口之前，开发者需要完成：

1. 获取商户凭据（product_id、sys_id、RSA 密钥对）
2. 安装 dg-java-sdk 并在 Spring Boot 中初始化
3. 理解签名规则、异步通知机制、流水号规范等通用约定

这份文档将以上内容集中提供，避免在每个专题文档中重复说明。

## 文件阅读地图

| 文件 | 相比官方文档额外补了什么 | 什么时候看 |
|-----|----------------------|-----------|
| `references/hostingpay-base.md` | 补了进入条件、主流程树、运行时边界和下一步路由 | 第一次进入托管支付路径时先看 |
| `references/hostingpay-customer-preparation.md` | 补了参数来源矩阵、控台项目创建、费率开通、授权绑定、订单沉淀要求 | 还没开始写代码，先确认客户材料是否齐 |
| `references/hostingpay-payload-construction.md` | 补了条件必填校验、对象字段建模、JSON 序列化边界 | 需要把复杂对象传进 SDK 时看 |
| `references/hostingpay-java-sdk-quickstart.md` | 补了 Maven 依赖、Spring Boot 配置类、`setProductId()` 这类 SDK 细节 | 要落初始化代码时看 |
| `references/hostingpay-java-tech-spec.md` | 补了签名、异步通知、重试、HTTP 状态码、连接超时等技术约束 | 遇到技术边界或联调问题时看 |
| `references/hostingpay-async-webhook.md` | 补了 `notify_url` / Webhook 区分、报文形态、验签、幂等、应答要求 | 需要接异步通知时看 |
| `references/hostingpay-common-params.md` | 补了 `sys_id`、`huifu_id`、`trans_stat` 等公共语义，不只给字段名 | 不确定公共字段该怎么理解时看 |
| `references/hostingpay-error-codes.md` | 把网关返回码、网关业务返回码、托管支付常见业务码集中到一处 | 返回码排查时看，不用它驱动订单终态 |

## 5 分钟快速接入

### 第 1 步：获取商户配置

从汇付开放平台获取以下 4 项凭据：

| 配置项 | 环境变量 | 说明 |
|-------|---------|------|
| 产品号 | `HUIFU_PRODUCT_ID` | 汇付分配，如 `YYZY` |
| 系统号 | `HUIFU_SYS_ID` | 商户/渠道商的 huifu_id |
| RSA 私钥 | `HUIFU_RSA_PRIVATE_KEY` | 用于请求签名 |
| RSA 公钥 | `HUIFU_RSA_PUBLIC_KEY` | 用于响应验签 |

### 第 2 步：添加 Maven 依赖

```xml
<dependency>
    <groupId>com.huifu.bspay.sdk</groupId>
    <artifactId>dg-java-sdk</artifactId>
    <version>3.0.38</version>
</dependency>
```

### 第 3 步：配置环境变量

`application.yml`（通过环境变量注入，**严禁硬编码**）：

```yaml
huifu:
  product-id: ${HUIFU_PRODUCT_ID}
  sys-id: ${HUIFU_SYS_ID}
  rsa-private-key: ${HUIFU_RSA_PRIVATE_KEY}
  rsa-public-key: ${HUIFU_RSA_PUBLIC_KEY}
```

### 第 4 步：初始化 SDK

详见 `references/hostingpay-java-sdk-quickstart.md` 中的 Spring Boot 配置类完整代码。

关键注意点：
- **Spring Boot 3.x** 用户需将 `javax.*` 替换为 `jakarta.*`
- SDK 产品号方法名为 `setProductId()`，与 `dg-java-sdk 3.0.38` 源码保持一致

### 第 5 步：开始调用业务接口

初始化完成后，根据业务场景选择对应文档：

| 业务需求 | 下一步 |
|---------|-------|
| 发起支付 | `references/hostingpay-preorder.md` |
| 查询订单 / 关单 | `references/hostingpay-query.md` |
| 退款 | `references/hostingpay-refund.md` |

### 第 5 步之前建议先做的两件事

1. 阅读 `references/hostingpay-customer-preparation.md`，把“客户要先提供什么、哪些参数来自控台配置 / 前端授权 / 终端采集 / 上游订单沉淀”梳理清楚。
2. 阅读 `references/hostingpay-payload-construction.md`，按统一规则实现必填 / 条件必填校验，并把对象字段在 SDK 边界再序列化成 JSON 字符串。
3. 官方托管产品文档还要求先完成项目创建、支付方式启用、授权绑定和对账文件配置；这些前置动作未完成时，不要让模型仅靠接口参数拼装继续开发。

## 联调环境

SDK 支持切换到联调（沙箱）环境进行测试，不会产生真实扣款：

```java
BasePay.prodMode = BasePay.MODE_TEST;  // 联调环境
```

- 联调商户号需联系汇付销售经理申请
- 本地 webhook 测试可使用 ngrok / frp 等内网穿透工具

联调环境和主流程说明统一看 `references/hostingpay-base.md`。

## 参考资料索引

| 文档 | 你需要它当… |
|-----|------------|
| `references/hostingpay-java-sdk-quickstart.md` | 第一次安装 SDK、写初始化代码 |
| `references/hostingpay-customer-preparation.md` | 开发前要向客户索取哪些参数、哪些值不能让模型猜 |
| `references/hostingpay-payload-construction.md` | 需要把嵌套对象优雅地转成 SDK 所需 JSON 字符串 |
| `references/hostingpay-java-tech-spec.md` | 需要了解请求模型、签名规则、IP 白名单 |
| `references/hostingpay-async-webhook.md` | 需要落地 `notify_url` 回调或控台 Webhook |
| `references/hostingpay-common-params.md` | 不确定 sys_id 和 huifu_id 填什么、交易状态 P/S/F 怎么处理 |
| `references/hostingpay-error-codes.md` | 接口返回了错误码，需要排查原因，但不拿返回码直接判定订单终态 |
