# IJPay 完整参考指南

## 项目信息

| 项目 | 值 |
|------|---|
| GitHub | https://github.com/javen205/IJPay |
| Gitee | https://gitee.com/javen205/IJPay |
| Stars | 6.4k |
| 最新版本 | v2.9.12.1（2025-04-10）|
| 稳定版 | v2.8.4（2022-09-18）|
| License | Apache-2.0 |

## Maven 模块坐标

```xml
<!-- 完整包（所有渠道） -->
<dependency>
    <groupId>com.github.javen205</groupId>
    <artifactId>IJPay-All</artifactId>
    <version>2.9.12.1</version>
</dependency>

<!-- 独立模块（按需引入） -->
<dependency>
    <groupId>com.github.javen205</groupId>
    <artifactId>IJPay-Core</artifactId>
    <version>2.9.12.1</version>
</dependency>
<dependency>
    <groupId>com.github.javen205</groupId>
    <artifactId>IJPay-AliPay</artifactId>
    <version>2.9.12.1</version>
</dependency>
<dependency>
    <groupId>com.github.javen205</groupId>
    <artifactId>IJPay-WxPay</artifactId>
    <version>2.9.12.1</version>
</dependency>
<dependency>
    <groupId>com.github.javen205</groupId>
    <artifactId>IJPay-QQ</artifactId>
    <version>2.9.12.1</version>
</dependency>
<dependency>
    <groupId>com.github.javen205</groupId>
    <artifactId>IJPay-JDPay</artifactId>
    <version>2.9.12.1</version>
</dependency>
<dependency>
    <groupId>com.github.javen205</groupId>
    <artifactId>IJPay-UnionPay</artifactId>
    <version>2.9.12.1</version>
</dependency>
<dependency>
    <groupId>com.github.javen205</groupId>
    <artifactId>IJPay-PayPal</artifactId>
    <version>2.9.12.1</version>
</dependency>
```

## Spring Boot 快速集成

### 1. 添加 JitPack 仓库

```xml
<repositories>
    <repository>
        <id>jitpack.io</id>
        <url>https://jitpack.io</url>
    </repository>
</repositories>
```

### 2. 依赖版本对应关系

| IJPay 版本 | JDK 要求 | Spring Boot | 微信 API 版本 |
|-----------|---------|------------|--------------|
| 2.9.x | 1.7+ | 任意 | Api-v3 |
| 2.8.x | 1.7+ | 任意 | Api-v2+v3 |
| 2.7.x | 1.7+ | 任意 | Api-v2 |

**推荐：使用最新版本 v2.9.12.1**，支持微信 Api-v3。

### 3. 核心类说明

| 类 | 包 | 用途 |
|----|----|------|
| `AliPayApiConfig` | com.ijpay.alipay | 支付宝配置构建器 |
| `AliPayApiConfigKit` | com.ijpay.alipay | 线程本地配置工具 |
| `AlipayTradePagePayRequest` | com.alipay.api | PC网站支付请求 |
| `AlipayTradeWapPayRequest` | com.alipay.api | WAP手机支付请求 |
| `AlipayTradeAppPayRequest` | com.alipay.api | App支付请求 |
| `AlipayTradeCloseRequest` | com.alipay.api | 关闭交易请求 |
| `AlipayTradeRefundRequest` | com.alipay.api | 退款请求 |
| `WxPayApi` | com.ijpay.wxpay | 微信支付工具类 |
| `WxPayApiV3Util` | com.ijpay.wxpay.v3 | 微信支付 Api-v3 工具 |

### 4. 微信支付 Api-v2 vs Api-v3 对比

| 对比项 | Api-v2 | Api-v3 |
|--------|--------|--------|
| 签名算法 | MD5/HMAC-SHA256 | RSA2 / HMAC-SHA256 |
| 证书 | 不需要 | 需要平台证书（退款/红包必需）|
| 响应格式 | XML | JSON |
| 推荐场景 | 简单扫码支付 | 新接入推荐 |
| 沙箱环境 | 支持 | 支持 |

**推荐新项目使用 Api-v3。**

### 5. 微信支付场景选择

| 场景 | 接口 | 说明 |
|------|------|------|
| PC扫码支付 | `unifiedOrder` | 生成二维码 |
| H5支付 | `micropay` | 微信外浏览器支付 |
| JSAPI支付 | `jsapi` | 公众号/小程序内支付 |
| App支付 | `app` | 手机App支付 |
| 小程序支付 | `miniProgram` | 微信小程序内支付 |

### 6. Demo 示例项目

- Spring Boot 版：https://github.com/Javen205/IJPay-Demo-SpringBoot
- JFinal 版：https://github.com/Javen205/IJPay-Demo-JFinal
- Solon 版：https://github.com/Javen205/IJPay-Demo-Solon

### 7. 常见报错

| 错误码 | 含义 | 解决 |
|--------|------|------|
| INVALID_SIGNATURE | 签名验证失败 | 检查密钥/证书是否正确 |
| APP_ID_NOT_EXIST | AppID 不存在 | 检查 application.yml 配置 |
| SIGN_FAIL | 签名失败 | 检查私钥格式（PKCS8）|
| CA cert error | 证书错误 | 检查证书链完整性 |
| MCHID_ERROR | 商户号错误 | 核对微信商户号 |
| TIMEOUT | 接口超时 | 增加超时时间或重试 |
