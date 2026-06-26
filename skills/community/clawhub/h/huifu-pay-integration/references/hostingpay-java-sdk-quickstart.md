## 目录

- [SDK 信息](#sdk-信息)
- [步骤 1：添加 Maven 依赖](#步骤-1添加-maven-依赖)
- [步骤 2：SDK 初始化](#步骤-2sdk-初始化spring-boot-配置类)
- [步骤 3：验证核心类导入](#步骤-3验证核心类导入)
- [SDK 调用模式](#sdk-调用模式)
- [SDK Request 类速查表](#sdk-request-类速查表)
- [专属字段 vs 扩展字段](#专属字段-vs-扩展字段)

# SDK 安装与初始化

## SDK 信息

| 属性 | 值 |
|-----|-----|
| SDK 名称 | dg-java-sdk |
| 当前版本 | 3.0.38 |
| GroupId | com.huifu.bspay.sdk |
| ArtifactId | dg-java-sdk |

## 步骤 1：添加 Maven 依赖

在 `pom.xml` 中添加：

```xml
<dependency>
    <groupId>com.huifu.bspay.sdk</groupId>
    <artifactId>dg-java-sdk</artifactId>
    <version>3.0.38</version>
</dependency>
```

执行安装：

```bash
mvn clean install
```

## 步骤 2：SDK 初始化（Spring Boot 配置类）

> **[Spring Boot 3.x 用户必读]** 如果你使用 Spring Boot 3.x（JDK 17/21），`javax.*` 命名空间已迁移至 `jakarta.*`，初始化代码中的 import 需替换，否则 `@PostConstruct` 将**编译失败**。

| Spring Boot 版本 | PostConstruct | Validation |
|-----------------|---------------|------------|
| 2.x | `javax.annotation.PostConstruct` | `javax.validation.constraints.NotBlank` |
| 3.x (JDK 17/21) | `jakarta.annotation.PostConstruct` | `jakarta.validation.constraints.NotBlank` |

> **[SDK 方法名口径]** `dg-java-sdk 3.0.38` 的 `MerConfig` 产品号方法名为 `setProductId(...)`。不要再生成旧文档中的 `setProcutId(...)`。

```java
package com.yourcompany.huifu.config;

import com.huifu.bspay.sdk.opps.core.BasePay;
import com.huifu.bspay.sdk.opps.core.config.MerConfig;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;

import javax.annotation.PostConstruct;

@Configuration
@Slf4j
public class HuifuConfig {

    @Value("${huifu.product-id}")
    private String productId;

    @Value("${huifu.sys-id}")
    private String sysId;

    @Value("${huifu.rsa-private-key}")
    private String rsaPrivateKey;

    @Value("${huifu.rsa-public-key}")
    private String rsaPublicKey;

    @Value("${huifu.skill-source:hfps/1.3.0}")
    private String skillSource;

    @PostConstruct
    public void initSdk() throws Exception {
        MerConfig merConfig = new MerConfig();
        merConfig.setProductId(productId);
        merConfig.setSysId(sysId);
        merConfig.setRsaPrivateKey(rsaPrivateKey);
        merConfig.setRsaPublicKey(rsaPublicKey);
        merConfig.setSkillSource(skillSource);
        BasePay.initWithMerConfig(merConfig);
        log.info("汇付SDK初始化完成");
    }
}
```

**关键说明**：

1. `setProductId()` 是 `dg-java-sdk 3.0.38` 源码中的产品号 setter
2. SDK 初始化在 `@PostConstruct` 中执行，应用启动时仅执行**一次**
3. 所有配置通过 `@Value` 从 `application.yml` 读取，配置文件通过环境变量注入
4. `skillSource` 默认可直接使用 `hfps/1.3.0`；如需覆盖，可通过配置项 `huifu.skill-source` 传入，初始化时按 `<skill_source>` 原样透传

## 步骤 3：验证核心类导入

确认以下类可正常导入：

| 类 | 包路径 | 用途 |
|---|-------|------|
| BasePay | `com.huifu.bspay.sdk.opps.core.BasePay` | SDK 入口，初始化商户配置 |
| MerConfig | `com.huifu.bspay.sdk.opps.core.config.MerConfig` | 商户配置对象 |
| BasePayClient | `com.huifu.bspay.sdk.opps.client.BasePayClient` | 发起 API 请求 |
| BasePayException | `com.huifu.bspay.sdk.opps.core.exception.BasePayException` | SDK 异常类 |
| DateTools | `com.huifu.bspay.sdk.opps.core.utils.DateTools` | 日期工具 |
| SequenceTools | `com.huifu.bspay.sdk.opps.core.utils.SequenceTools` | 流水号工具 |

## SDK 调用模式

所有汇付 API 调用遵循统一模式：

```java
// 1. 创建 Request 对象
XxxRequest request = new XxxRequest();
request.setReqDate(DateTools.getCurrentDateYYYYMMDD());
request.setReqSeqId(SequenceTools.getReqSeqId32());
request.setHuifuId("商户号");
// ... 设置业务参数

// 2. 设置扩展参数（没有专属 setter 的字段通过 extendInfoMap 传入）
Map<String, Object> extendInfoMap = new HashMap<>();
extendInfoMap.put("notify_url", "https://your-domain.com/notify/payment");
request.setExtendInfo(extendInfoMap);

// 3. 发起请求
Map<String, Object> response = BasePayClient.request(request, false);

// 4. 处理响应
String respCode = (String) response.get("resp_code");
if ("00000000".equals(respCode)) {
    // 成功处理
}
```

## SDK Request 类速查表

| 场景 | Request 类 | 包路径 |
|------|-----------|-------|
| H5/PC 预下单 | `V2TradeHostingPaymentPreorderH5Request` | `com.huifu.bspay.sdk.opps.core.request` |
| 支付宝小程序预下单 | `V2TradeHostingPaymentPreorderAliRequest` | 同上 |
| 微信小程序预下单 | `V2TradeHostingPaymentPreorderWxRequest` | 同上 |
| 抖音直连下单 | 使用 `V2TradeHostingPaymentPreorderH5Request`，设置 `pre_order_type=4` | 同上 |
| 托管交易查询 | `V2TradeHostingPaymentQueryorderinfoRequest` | 同上 |
| 托管交易退款 | `V2TradeHostingPaymentHtrefundRequest` | 同上 |
| 退款结果查询 | `V2TradeHostingPaymentQueryrefundinfoRequest` | 同上 |
| 托管交易关单 | `V2TradeHostingPaymentCloseRequest` | 同上 |
| 拆单支付订单查询 | `V2TradeHostingPaymentSplitpayQueryRequest` | 同上 |

## 专属字段 vs 扩展字段

SDK Request 类有两类字段：

1. **专属字段**：有独立的 setter 方法（如 `setHuifuId()`、`setTransAmt()`），直接调用 setter 设置
2. **扩展字段**：没有独立 setter 的字段，通过 `setExtendInfo(Map)` 或 `addExtendInfo(key, value)` 传入

**判断规则**：查看 Request 类是否有对应 setter，有则用 setter，无则用 extendInfoMap。

抖音直连下单属于托管预下单场景，不能编造 `Dypreorder` / `Douyin` 类名；必须使用 `V2TradeHostingPaymentPreorderH5Request`，固定 `pre_order_type=4`，并把 `dy_data` 等字段通过字段或 `extendInfoMap` 透传。
