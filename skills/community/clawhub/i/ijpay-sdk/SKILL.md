---
name: pay
description: 支付接入技能 — 基于 IJPay SDK 封装微信支付、支付宝、QQ支付、银联、京东、PayPal 等主流支付渠道。触发场景包括：用户说"接入支付"、"配置支付"、"微信支付"、"支付宝"、"订单支付"、"支付回调"、"支付对账"、"IJPay"等关键词，或需要为项目添加在线支付功能时激活。
---

# Pay Skill — 小龙虾支付接入技能

让小龙虾具备接入主流支付渠道的能力。基于 **IJPay**（Javen205 开源，6.4k⭐，Apache-2.0）封装。

---

## 支持的支付渠道

| 渠道 | 模块 | 签名方式 |
|------|------|---------|
| 支付宝 | `IJPay-AliPay` | RSA2 普通公钥 / 证书模式 |
| 微信支付 | `IJPay-WxPay` | Api-v2 / Api-v3 |
| QQ 钱包 | `IJPay-QQ` | API |
| 银联 | `IJPay-UnionPay` | 银联标准 |
| 京东支付 | `IJPay-JDPay` | API |
| PayPal | `IJPay-PayPal` | OAuth2 |

---

## 快速集成流程（Spring Boot）

### 1. 引入 Maven 依赖

```xml
<!-- 按需引入以下依赖（选一个或多个） -->
<!-- 完整包（含所有渠道） -->
<dependency>
    <groupId>com.github.javen205</groupId>
    <artifactId>IJPay-All</artifactId>
    <version>2.9.12.1</version>
</dependency>

<!-- 或按渠道引入（推荐，按需选择） -->
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
```

> ⚠️ 如果 Maven 无法拉取，检查是否配置了 JitPack 仓库：
> ```xml
> <pluginRepositories>
>   <pluginRepository>
>     <id>jitpack.io</id>
>     <url>https://jitpack.io</url>
>   </pluginRepository>
> </pluginRepositories>
> ```

### 2. 配置参数（application-prod.yml）

```yaml
# 支付宝配置
ali-pay:
  app-id: 2021xxxxx                                  # 支付宝应用AppID
  server-url: https://openapi.alipay.com/gateway.do   # 支付宝网关
  private-key: MIIBIjANBgkq...                        # 应用私钥（RSA2）
  alipay-public-key: MIIBIjANBgkq...                 # 支付宝公钥
  sign-type: RSA2                                     # 签名方式
  callback-url: https://your-domain.com/api/pay/ali-callback  # 回调地址

# 微信支付配置
wx-pay:
  app-id: wx1234567890abcdef                         # 微信应用AppID
  mch-id: 1234567890                                 # 商户号
  api-key: xxxxxxxx                                  # APIv2 密钥（32位）
  cert-path: /path/to/apiclient_cert.p12             # 证书路径（退款/红包用）
  callback-url: https://your-domain.com/api/pay/wx-callback  # 回调地址
```

> 🔐 **私钥等敏感配置禁止硬编码**，必须通过环境变量或配置中心注入。

### 3. 支付接口示例

#### 支付宝 PC 网站支付

```java
@RestController
@RequestMapping("/api/pay")
public class PayController {

    @Value("${ali-pay.app-id}")
    private String appId;
    @Value("${ali-pay.private-key}")
    private String privateKey;

    @PostMapping("/create-ali")
    public String createAliPayOrder(@RequestParam("orderId") String orderId,
                                     @RequestParam("amount") BigDecimal amount) {
        AliPayApiConfig config = AliPayApiConfig.builder()
            .setAppId(appId)
            .setPrivateKey(privateKey)
            .setCharset("UTF-8")
            .setServiceUrl("https://openapi.alipay.com/gateway.do")
            .setSignType("RSA2")
            .build();

        AliPayApiConfigKit.setThreadLocalAliPayApiConfig(config);

        AlipayTradePagePayRequest request = new AlipayTradePagePayRequest();
        request.setBizContent(JSON.toJSONString(ImmutableMap.of(
            "out_trade_no", orderId,
            "product_code", "FAST_INSTANT_TRADE_PAY",
            "total_amount", amount.toString(),
            "subject", "FMT治疗费用"
        )));
        request.setReturnUrl("https://your-domain.com/pay/success");

        AlipayTradePagePayResponse response = config.getAlipayClient().execute(request);
        return response.isSuccess() ? response.getBody() : "支付创建失败";
    }

    @PostMapping("/ali-callback")
    public String aliPayCallback(HttpServletRequest request) {
        Map<String, String> params = getParams(request);
        if (TradeStatus.SUCCESS.name().equals(params.get("trade_status"))) {
            String orderId = params.get("out_trade_no");
            // ✅ 支付成功：更新订单状态
            orderService.updatePaid(orderId);
        }
        return "success";
    }
}
```

#### 微信 H5 支付

```java
@PostMapping("/create-wx")
public Map<String, String> createWxPayOrder(@RequestParam("orderId") String orderId,
                                             @RequestParam("amount") int amountFen) {
    Map<String, String> params = new HashMap<>();
    params.put("appid", wxAppId);
    params.put("mchid", wxMchId);
    params.put("description", "FMT治疗费用");
    params.put("out_trade_no", orderId);
    params.put("amount", JSON.toJSONString(ImmutableMap.of("total", amountFen, "currency", "CNY")));
    params.put("notify_url", wxCallbackUrl);

    WxPayApiV3Util v3Util = new WxPayApiV3Util();
    String result = v3Util.push(wechatCertPath, wechatMchId, params);
    Map<String, Object> resp = JSON.parseObject(result);
    return Collections.singletonMap("h5_url", ((Map)resp.get("h5")).get("h5_url"));
}
```

### 4. 支付回调处理

```java
@PostMapping("/ali-callback")
public String aliCallback(HttpServletRequest request) {
    if (!AliPayApiConfigKit.validateResponse(request)) {
        return "fail";
    }
    if (!AlipaySignature.checksum(request.getParameterMap(), ...)) {
        return "fail";
    }
    String status = request.getParameter("trade_status");
    if (TradeStatus.TRADE_SUCCESS.name().equals(status)) {
        String orderId = request.getParameter("out_trade_no");
        orderService.markPaid(orderId, request.getParameter("trade_no"));
    }
    return "success";
}

@PostMapping("/wx-callback")
public String wxCallback(HttpServletRequest request) {
    String body = StreamUtils.readToString(request.getInputStream());
    if (WxPayApiKit.verifyNotify(body, signKey)) {
        Map<String, Object> data = JSON.parseObject(body);
        if ("SUCCESS".equals(data.get("trade_state"))) {
            orderService.markPaid((String)data.get("out_trade_no"), (String)data.get("transaction_id"));
        }
    }
    return "success";
}
```

---

## 参考文档

| 文档 | 说明 | 何时读取 |
|------|------|---------|
| [ijpay-guide.md](references/ijpay-guide.md) | IJPay 完整指南（项目结构/版本/Maven坐标）| 首次集成时 |
| [alipay-guide.md](references/alipay-guide.md) | 支付宝完整接入（6个支付场景/字段详解/沙箱）| 选择支付宝时 |
| [wxpay-guide.md](references/wxpay-guide.md) | 微信支付完整接入（Api-v2/v3差异/场景/证书）| 选择微信时 |
| [callback-handler.md](references/callback-handler.md) | 支付回调高级处理（幂等/并发/补偿）| 实现回调时 |

---

## 常用场景决策

```
需要接入支付？
    │
    ├── 支付宝 ✅ → 优先推荐（个人/企业均可，费率低）
    │              参考：references/alipay-guide.md
    │
    ├── 微信支付 ✅ → 必须有商户号，支持H5/小程序/App
    │               参考：references/wxpay-guide.md
    │
    ├── 银联/京东/PayPal → 参考 references/ijpay-guide.md
    │
    └── 小程序内支付 → 微信支付服务商模式，参考 wxpay-guide.md
```

---

## 快速检查清单

- [ ] Maven 依赖已添加（IJPay-AliPay / IJPay-WxPay）
- [ ] 沙箱环境测试通过（先用沙箱，不花钱）
- [ ] 生产环境 AppID + 商户号 + 密钥配置完成
- [ ] 支付回调 URL 已填写（必须是公网可访问 HTTPS）
- [ ] 回调接口已加幂等处理（防止重复通知）
- [ ] 微信退款/企业付款需上传证书到服务器
- [ ] 支付宝签名验签通过
- [ ] 日志记录完整（支付请求/回调/异常）
