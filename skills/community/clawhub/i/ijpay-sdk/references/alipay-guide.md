# 支付宝支付接入完整指南

## 支付场景与适用场景

| 场景 | 接口方法 | 适用 |
|------|---------|------|
| PC网站支付 | `AlipayTradePagePayRequest` | 电脑端网站，扫码付 |
| WAP手机支付 | `AlipayTradeWapPayRequest` | 手机浏览器 H5 |
| App支付 | `AlipayTradeAppPayRequest` | 手机App内 |
| JS支付 | `AlipayTradeCreateRequest` | 支付宝内嵌网页 |
| 小程序支付 | `AlipayTradeAppPayRequest` | 支付宝小程序 |
| 扫码付 | `AlipayTradePrecreateRequest` | 生成付款二维码 |

## 配置参数说明

### 普通公钥方式（简单，推荐个人开发者）

```yaml
ali-pay:
  app-id: "2021001xxxxxx"
  server-url: "https://openapi-sandbox.dl.alipaydev.com/gateway.do"  # 沙箱
  # 生产: https://openapi.alipay.com/gateway.do
  private-key: "MIIEvQIBADANB...(PKCS8格式RSA2私钥)"
  alipay-public-key: "MIIBIjANBgk...(支付宝公钥)"
  sign-type: "RSA2"
```

### 证书方式（安全，推荐企业）

```java
AliPayApiConfig config = AliPayApiConfig.builder()
    .setAppId(appId)
    .setAppCertPath("/path/to/app_cert_public_key.cert")     // 应用公钥证书
    .setAliPayCertPath("/path/to/alipay_cert_public_key.cert") // 支付宝公钥证书
    .setAliPayRootCertPath("/path/to/alipay_root_cert.cert")   // 支付宝根证书
    .setCharset("UTF-8")
    .setPrivateKey(privateKey)
    .setServiceUrl(alipayServerUrl)
    .setSignType("RSA2")
    .buildByCert();  // 注意：用 buildByCert() 而非 build()
```

## 6大支付场景代码

### 场景1：PC 网站支付（扫码付）

```java
@PostMapping("/page-pay")
public String pagePay(@RequestParam("orderId") String orderId,
                      @RequestParam("amount") BigDecimal amount) {
    AliPayApiConfig config = buildAliPayConfig();
    AliPayApiConfigKit.setThreadLocalAliPayApiConfig(config);

    AlipayTradePagePayRequest request = new AlipayTradePagePayRequest();
    request.setBizContent(JSON.toJSONString(ImmutableMap.of(
        "out_trade_no", orderId,
        "product_code", "FAST_INSTANT_TRADE_PAY",
        "total_amount", amount.toString(),
        "subject", "FMT治疗费用-#" + orderId
    )));
    request.setReturnUrl("https://your-domain.com/pay/success");
    request.setNotifyUrl("https://your-domain.com/api/pay/ali-callback");

    AlipayTradePagePayResponse resp = config.getAlipayClient().execute(request);
    return resp.isSuccess() ? resp.getBody() : JSON.toJSONString(resp);
}
```

### 场景2：WAP 手机网站支付

```java
@PostMapping("/wap-pay")
public String wapPay(@RequestParam("orderId") String orderId,
                     @RequestParam("amount") BigDecimal amount) {
    AliPayApiConfig config = buildAliPayConfig();
    AliPayApiConfigKit.setThreadLocalAliPayApiConfig(config);

    AlipayTradeWapPayRequest request = new AlipayTradeWapPayRequest();
    request.setBizContent(JSON.toJSONString(ImmutableMap.of(
        "out_trade_no", orderId,
        "total_amount", amount.toString(),
        "subject", "FMT治疗费用",
        "quit_url", "https://your-domain.com"
    )));
    request.setReturnUrl("https://your-domain.com/pay/success");
    request.setNotifyUrl("https://your-domain.com/api/pay/ali-callback");

    AlipayTradeWapPayResponse resp = new AlipayTradeWapPayRequest()
        .getAlipayTradeWapPayResponse(request, config.getAlipayClient());
    return resp.isSuccess() ? resp.getBody() : "fail";
}
```

### 场景3：App 支付（手机App）

```java
@PostMapping("/app-pay")
public Map<String, String> appPay(@RequestParam("orderId") String orderId,
                                  @RequestParam("amount") BigDecimal amount) {
    AliPayApiConfig config = buildAliPayConfig();
    AliPayApiConfigKit.setThreadLocalAliPayApiConfig(config);

    AlipayTradeAppPayRequest request = new AlipayTradeAppPayRequest();
    request.setBizContent(JSON.toJSONString(ImmutableMap.of(
        "out_trade_no", orderId,
        "total_amount", amount.toString(),
        "subject", "FMT治疗费用"
    )));
    request.setNotifyUrl("https://your-domain.com/api/pay/ali-callback");

    AlipayTradeAppPayResponse resp = config.getAlipayClient().execute(request);
    Map<String, String> result = new HashMap<>();
    result.put("orderInfo", resp.getOrderString()); // 直接调起支付宝SDK
    return result;
}
```

### 场景4：统一收单交易退款

```java
@PostMapping("/refund")
public String refund(@RequestParam("orderId") String orderId,
                    @RequestParam("amount") BigDecimal amount) {
    AliPayApiConfig config = buildAliPayConfig();
    AliPayApiConfigKit.setThreadLocalAliPayApiConfig(config);

    AlipayTradeRefundRequest request = new AlipayTradeRefundRequest();
    request.setBizContent(JSON.toJSONString(ImmutableMap.of(
        "trade_no", "原交易流水号",  // 如有
        "out_trade_no", orderId,
        "refund_amount", amount.toString(),
        "refund_reason", "患者申请退款"
    )));

    AlipayTradeRefundResponse resp = config.getAlipayClient().execute(request);
    return resp.isSuccess() ? "refund_success" : "refund_fail";
}
```

### 场景5：关闭交易

```java
@PostMapping("/close")
public String closeOrder(@RequestParam("orderId") String orderId) {
    AliPayApiConfig config = buildAliPayConfig();
    AliPayApiConfigKit.setThreadLocalAliPayApiConfig(config);

    AlipayTradeCloseRequest request = new AlipayTradeCloseRequest();
    request.setBizContent(JSON.toJSONString(ImmutableMap.of("out_trade_no", orderId)));
    AlipayTradeCloseResponse resp = config.getAlipayClient().execute(request);
    return resp.isSuccess() ? "closed" : "close_fail";
}
```

### 场景6：查询订单

```java
@PostMapping("/query")
public Map<String, Object> queryOrder(@RequestParam("orderId") String orderId) {
    AliPayApiConfig config = buildAliPayConfig();
    AliPayApiConfigKit.setThreadLocalAliPayApiConfig(config);

    AlipayTradeQueryRequest request = new AlipayTradeQueryRequest();
    request.setBizContent(JSON.toJSONString(ImmutableMap.of("out_trade_no", orderId)));
    AlipayTradeQueryResponse resp = config.getAlipayClient().execute(request);

    Map<String, Object> result = new HashMap<>();
    result.put("success", resp.isSuccess());
    result.put("status", resp.getTradeStatus());
    result.put("amount", resp.getTotalAmount());
    return result;
}
```

## 沙箱测试（免手续费）

1. 登录蚂蚁金服开放平台 → 开发工具 → 沙箱
2. 获取沙箱 AppID + 密钥替换生产配置
3. 网关替换为：`https://openapi-sandbox.dl.alipaydev.com/gateway.do`
4. 使用支付宝沙箱版App扫码付款

## 敏感字段处理

| 字段 | 安全要求 |
|------|---------|
| `private-key` | 必须从环境变量读取，禁止硬编码 |
| `alipay-public-key` | 存入数据库需加密存储 |
| `app-cert` | 证书文件部署在服务器 /data/certs/ 目录 |
| 回调通知 | 接收参数后必须调用 `AlipaySignature.checksum()` 验签 | 
