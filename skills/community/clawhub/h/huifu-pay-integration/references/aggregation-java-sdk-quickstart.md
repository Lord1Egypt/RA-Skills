## 目录

- [SDK 信息](#sdk-信息)
- [步骤 1：添加 Maven 依赖](#步骤-1添加-maven-依赖)
- [步骤 2：SDK 初始化](#步骤-2sdk-初始化spring-boot-配置类)
- [步骤 3：验证核心类导入](#步骤-3验证核心类导入)
- [Factory 调用模式](#factory-调用模式)
- [与 dg-java-sdk 的关键差异](#与-dg-java-sdk-的关键差异)

# SDK 安装与初始化

## SDK 信息

| 属性 | 值 |
|-----|-----|
| SDK 名称 | dg-lightning-sdk |
| 当前版本 | 1.0.5 |
| GroupId | com.huifu.dg.lightning.sdk |
| ArtifactId | dg-lightning-sdk |

> **说明**：如果项目中同时需要托管支付（dg-java-sdk）和聚合支付（dg-lightning-sdk），两个 SDK 可以共存，各自独立初始化。

## 步骤 1：添加 Maven 依赖

在 `pom.xml` 中添加：

```xml
<dependency>
    <groupId>com.huifu.dg.lightning.sdk</groupId>
    <artifactId>dg-lightning-sdk</artifactId>
    <version>1.0.5</version>
</dependency>
```

如果同时需要托管支付，也添加：

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

> **[Spring Boot 3.x 用户必读]** 如果你使用 Spring Boot 3.x（JDK 17/21），`javax.*` 命名空间已迁移至 `jakarta.*`，初始化代码中的 import 需替换。

| Spring Boot 版本 | PostConstruct |
|-----------------|---------------|
| 2.x | `javax.annotation.PostConstruct` |
| 3.x (JDK 17/21) | `jakarta.annotation.PostConstruct` |

> **[产品号方法名]** Lightning SDK 和当前 `dg-java-sdk 3.0.38` 的 `MerConfig` 产品号方法名都使用 `setProductId(...)`。

```java
package com.yourcompany.huifu.config;

import com.huifu.dg.lightning.biz.config.MerConfig;
import com.huifu.dg.lightning.utils.BasePay;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;

import javax.annotation.PostConstruct;

@Configuration
@Slf4j
public class HuifuLightningConfig {

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

    @Value("${huifu.mode:prod}")
    private String mode;

    @PostConstruct
    public void initSdk() throws Exception {
        // 设置环境模式
        if ("test".equals(mode)) {
            BasePay.prodMode = BasePay.MODE_TEST;
            log.info("汇付聚合支付SDK: 联调环境");
        } else {
            BasePay.prodMode = BasePay.MODE_PROD;
            log.info("汇付聚合支付SDK: 生产环境");
        }

        // 初始化商户配置
        MerConfig merConfig = new MerConfig();
        merConfig.setProductId(productId);   // 注意：Lightning SDK 拼写正常
        merConfig.setSysId(sysId);
        merConfig.setRsaPrivateKey(rsaPrivateKey);
        merConfig.setRsaPublicKey(rsaPublicKey);
        merConfig.setSkillSource(skillSource);

        BasePay.initWithMerConfig(merConfig);  // 注意：throws Exception
        log.info("汇付聚合支付SDK初始化完成");
    }
}
```

### 多商户配置（可选）

如果需要支持多个商户，使用 `initWithMerConfigs`：

```java
Map<String, MerConfig> configs = new HashMap<>();

MerConfig config1 = new MerConfig();
config1.setProductId("MYPAY");
config1.setSysId("6666000123120001");
config1.setRsaPrivateKey("...");
config1.setRsaPublicKey("...");
config1.setSkillSource("hfps/1.3.0");
configs.put("merchant1", config1);

MerConfig config2 = new MerConfig();
config2.setSysId("6666000123120002");
config2.setSkillSource("hfps/1.3.0");
// ... 配置第二个商户
configs.put("merchant2", config2);

BasePay.initWithMerConfigs(configs);
```

### 自定义超时时间（可选）

```java
MerConfig merConfig = new MerConfig();
// ... 基本配置
merConfig.setCustomConnectTimeout("30000");              // 连接超时 30s（默认 20s），注意是 String 类型
merConfig.setCustomSocketTimeout("30000");               // 读取超时 30s（默认 20s）
merConfig.setCustomConnectionRequestTimeout("40000");    // 请求超时 40s（默认 30s）
merConfig.setSkillSource("hfps/1.3.0");
```

## 步骤 3：验证核心类导入

确认以下类可正常导入：

| 类 | 包路径 | 用途 |
|---|-------|------|
| BasePay | `com.huifu.dg.lightning.utils.BasePay` | SDK 入口，初始化配置、环境模式 |
| MerConfig | `com.huifu.dg.lightning.biz.config.MerConfig` | 商户配置对象 |
| Factory | `com.huifu.dg.lightning.factory.Factory` | 工厂类，获取业务客户端 |
| CommonPayClient | `com.huifu.dg.lightning.biz.client.CommonPayClient` | 聚合支付客户端 |
| BasePayException | `com.huifu.dg.lightning.biz.exception.BasePayException` | SDK 异常类 |
| DateTools | `com.huifu.dg.lightning.utils.DateTools` | 日期工具（`getCurrentDateYYYYMMDD()`） |
| SequenceTools | `com.huifu.dg.lightning.utils.SequenceTools` | 流水号工具（`getReqSeqId32()`） |

`MerConfig.setSkillSource(...)` 按 `<skill_source>` 原样透传；聚合支付要求的 `sys_id` 仍通过独立请求头 `sys_id` / `jpt-sys_id` 传递，`jpt-x-skill-source` 只承载来源值本身。

## Factory 调用模式

Lightning SDK 使用 Factory 模式创建业务客户端，与 dg-java-sdk 的 `BasePayClient.request()` 不同：

```java
import com.huifu.dg.lightning.factory.Factory;
import com.huifu.dg.lightning.biz.client.CommonPayClient;
import com.huifu.dg.lightning.models.payment.*;

// 1. 获取聚合支付客户端
CommonPayClient client = Factory.Payment.Common();

// 2. 下单
TradePaymentCreateRequest createReq = new TradePaymentCreateRequest();
// ... 设置参数
Map<String, Object> createResp = client.create(createReq);

// 3. 查询
TradePaymentScanpayQueryRequest queryReq = new TradePaymentScanpayQueryRequest();
// ... 设置参数
Map<String, Object> queryResp = client.query(queryReq);

// 4. 关单
TradePaymentScanpayCloseRequest closeReq = new TradePaymentScanpayCloseRequest();
Map<String, Object> closeResp = client.close(closeReq);

// 5. 关单查询
TradePaymentScanpayClosequeryRequest closeQueryReq = new TradePaymentScanpayClosequeryRequest();
Map<String, Object> closeQueryResp = client.closeQuery(closeQueryReq);

// 6. 退款
TradePaymentScanpayRefundRequest refundReq = new TradePaymentScanpayRefundRequest();
Map<String, Object> refundResp = client.refund(refundReq);

// 7. 退款查询
TradePaymentScanpayRefundQueryRequest refundQueryReq = new TradePaymentScanpayRefundQueryRequest();
Map<String, Object> refundQueryResp = client.refundQuery(refundQueryReq);
```

### 添加可选业务参数

CommonPayClient 支持通过 `optional()` 方法添加额外参数：

```java
CommonPayClient client = Factory.Payment.Common();
client.optional("notify_url", "https://your-domain.com/notify");
client.optional("remark", "备注信息");
Map<String, Object> response = client.create(request);
```

### 延迟交易客户端

```java
import com.huifu.dg.lightning.biz.client.DelayTransClient;

DelayTransClient delayClient = Factory.Solution.DelayTrans();
// delayClient.confirm()      - 延迟交易确认
// delayClient.confirmQuery() - 确认查询
// delayClient.refund()       - 延迟交易退款
// delayClient.refundQuery()  - 退款查询
// delayClient.splitQuery()   - 分账查询
```

## SDK Request 类速查表

| 场景 | Request 类 | 包路径 |
|------|-----------|-------|
| 聚合支付下单 | `TradePaymentCreateRequest` | `com.huifu.dg.lightning.models.payment` |
| 聚合交易查询 | `TradePaymentScanpayQueryRequest` | 同上 |
| 聚合交易关单 | `TradePaymentScanpayCloseRequest` | 同上 |
| 聚合交易关单查询 | `TradePaymentScanpayClosequeryRequest` | 同上 |
| 交易退款 | `TradePaymentScanpayRefundRequest` | 同上 |
| 交易退款查询 | `TradePaymentScanpayRefundQueryRequest` | 同上 |

## 与 dg-java-sdk 的关键差异

| 对比项 | dg-lightning-sdk | dg-java-sdk |
|-------|-----------------|------------|
| 初始化 import | `com.huifu.dg.lightning.*` | `com.huifu.bspay.sdk.opps.*` |
| MerConfig 包路径 | `com.huifu.dg.lightning.biz.config.MerConfig` | `com.huifu.bspay.sdk.opps.core.config.MerConfig` |
| BasePay 包路径 | `com.huifu.dg.lightning.utils.BasePay` | `com.huifu.bspay.sdk.opps.core.BasePay` |
| 设置产品号 | `setProductId()` | `setProductId()` |
| 调用方式 | `Factory.Payment.Common().create(req)` | `BasePayClient.request(req, false)` |
| 扩展参数 | `client.optional(key, value)` | `request.setExtendInfo(map)` |
| HTTP 客户端 | Apache HttpClient 4.5.2 | OkHttp |
