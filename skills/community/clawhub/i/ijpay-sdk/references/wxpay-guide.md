# 微信支付接入完整指南

## Api-v3（推荐）vs Api-v2

| 特性 | Api-v2 | Api-v3（推荐）|
|------|--------|-------------|
| 签名算法 | MD5/HMAC-SHA256 | RSA2 |
| 平台证书 | 不需要 | 必需（含证书自动刷新）|
| 证书操作 | 不需要 | 需下载安装证书 |
| 退款/企业红包 | 需上传证书 | 需下载平台证书 |
| 适用场景 | 老系统兼容 | 新接入首选 |

## Api-v3 配置参数

```yaml
wx-pay:
  app-id: wx1234567890abcdef
  mch-id: 1234567890
  serial-no: XXXXXXXXXXXXXXXXXX     # 证书序列号
  api-v3-key: xxxxxxxx               # APIv3密钥（32位）
  # Api-v2 密钥（也称 APIKEY）
  api-key: xxxxxxxx
  # 证书路径（退款时必需）
  cert-path: /opt/deepfmt/certs/apiclient_key.pem
  private-key-path: /opt/deepfmt/certs/apiclient_key.pem
  callback-url: https://your-domain.com/api/pay/wx-callback
```

## 微信支付场景

| 场景 | 说明 | 适合 |
|------|------|------|
| Native支付 | 生成二维码链接，客户扫码付 | PC网站 |
| JSAPI支付 | 微信内置浏览器调起支付 | 公众号/小程序 |
| H5支付 | 微信外浏览器，Wap网页支付 | 手机浏览器 |
| App支付 | App内调起微信 | 手机App |
| 小程序支付 | 微信小程序内支付 | 小程序 |

## 场景1：Native 支付（PC扫码付）

```java
@PostMapping("/wx-native")
public Map<String, String> wxNativePay(@RequestParam("orderId") String orderId,
                                        @RequestParam("amount") int amountFen) {
    String appId = wxConfig.getAppId();
    String mchId = wxConfig.getMchId();

    Map<String, String> params = new TreeMap<>();
    params.put("appid", appId);
    params.put("mchid", mchId);
    params.put("description", "FMT治疗费用");
    params.put("out_trade_no", orderId);
    params.put("notify_url", wxConfig.getCallbackUrl());

    Map<String, Object> amount = new TreeMap<>();
    amount.put("total", amountFen);      // 金额：分（整数）
    amount.put("currency", "CNY");
    params.put("amount", JSON.toJSONString(amount));

    // 调用微信统一下单接口
    String result = WxPayApi.push(
        null,                               // certPath（v2用）
        mchId,
        "https://api.mch.weixin.qq.com/v3/pay/transactions/native",
        null,
        WxPayEnum.DOMAIN_API.getUrl(),
        params
    );

    Map<String, Object> resp = JSON.parseObject(result);
    Map<String, String> codeUrl = new HashMap<>();
    codeUrl.put("code_url", (String) resp.get("code_url"));
    return codeUrl;
}
```

## 场景2：H5 支付（微信外浏览器）

```java
@PostMapping("/wx-h5")
public Map<String, String> wxH5Pay(@RequestParam("orderId") String orderId,
                                     @RequestParam("amount") int amountFen) {
    Map<String, String> params = new TreeMap<>();
    params.put("appid", wxAppId);
    params.put("mchid", wxMchId);
    params.put("description", "FMT治疗费用");
    params.put("out_trade_no", orderId);
    params.put("notify_url", wxCallbackUrl);

    Map<String, Object> amount = new TreeMap<>();
    amount.put("total", amountFen);
    amount.put("currency", "CNY");
    params.put("amount", JSON.toJSONString(amount));

    // 场景信息（必填）
    Map<String, Object> sceneInfo = new TreeMap<>();
    Map<String, String> h5Info = new TreeMap<>();
    h5Info.put("type", "Wap");
    sceneInfo.put("h5_info", h5Info);
    params.put("scene_info", JSON.toJSONString(sceneInfo));

    String result = WxPayApi.push(null, mchId,
        "https://api.mch.weixin.qq.com/v3/pay/transactions/h5",
        null, WxPayEnum.DOMAIN_API.getUrl(), params);

    Map<String, Object> resp = JSON.parseObject(result);
    Map<String, String> h5Url = new HashMap<>();
    h5Url.put("h5_url", ((Map)resp.get("h5")).get("h5_url"));
    return h5Url;
}
```

## 场景3：JSAPI 支付（公众号/小程序）

```java
@PostMapping("/wx-jsapi")
public Map<String, String> wxJsapiPay(@RequestParam("orderId") String orderId,
                                       @RequestParam("amount") int amountFen,
                                       @RequestParam("openid") String openid) {
    Map<String, String> params = new TreeMap<>();
    params.put("appid", wxAppId);
    params.put("mchid", wxMchId);
    params.put("description", "FMT治疗费用");
    params.put("out_trade_no", orderId);
    params.put("notify_url", wxCallbackUrl);
    params.put("payer", JSON.toJSONString(ImmutableMap.of("openid", openid)));

    Map<String, Object> amount = new TreeMap<>();
    amount.put("total", amountFen);
    amount.put("currency", "CNY");
    params.put("amount", JSON.toJSONString(amount));

    String result = WxPayApi.push(null, mchId,
        "https://api.mch.weixin.qq.com/v3/pay/transactions/jsapi",
        null, WxPayEnum.DOMAIN_API.getUrl(), params);

    // 获取预支付交易会话ID后，调起支付
    Map<String, String> jsapi = new HashMap<>();
    jsapi.put("appId", wxAppId);
    jsapi.put("timeStamp", String.valueOf(System.currentTimeMillis() / 1000));
    jsapi.put("nonceStr", WxPayUtil.generateUUID());
    jsapi.put("package", "prepay_id=" + tradeId);
    jsapi.put("signType", "RSA");
    // ... 签名后返回前端调起微信支付
    return jsapi;
}
```

## 微信支付证书安装

```bash
# 1. 登录微信商户平台（https://pay.weixin.qq.com）
# 2. API安全 → 申请证书
# 3. 下载证书，得到：apiclient_cert.p12（含私钥） + apiclient_key.pem

# 将证书放到服务器指定目录
mkdir -p /opt/deepfmt/certs
chmod 600 /opt/deepfmt/certs/apiclient_key.pem
chown deepfmt:deepfmt /opt/deepfmt/certs
```

## 微信支付回调（Api-v3）

```java
@PostMapping("/wx-callback")
public String wxPayCallback(HttpServletRequest request) {
    try {
        String body = StreamUtils.readToString(request.getInputStream());
        log.info("微信支付回调: {}", body);

        // 解析回调报文（无需主动验签，框架已处理）
        Map<String, Object> notify = JSON.parseObject(body);
        String tradeState = (String) notify.get("trade_state");

        if ("SUCCESS".equals(tradeState)) {
            String orderId = (String) notify.get("out_trade_no");
            String transactionId = (String) notify.get("transaction_id");
            int total = ((Map)notify.get("amount")).get("total");

            // 幂等处理（关键！）
            if (orderService.markPaidIfAbsent(orderId, transactionId)) {
                log.info("订单 {} 支付成功，流水号 {}", orderId, transactionId);
            }
        }

        // 返回 SUCCESS 表示已处理
        return JSON.toJSONString(ImmutableMap.of("code", "SUCCESS", "message", "成功"));
    } catch (Exception e) {
        log.error("微信回调异常", e);
        return JSON.toJSONString(ImmutableMap.of("code", "FAIL", "message", "失败"));
    }
}
```

## 常见错误码

| 错误码 | 含义 | 解决方案 |
|--------|------|---------|
| ORDERPAID | 订单已支付 | 不用重新支付，查询订单状态 |
| ORDERCLOSED | 订单已关闭 | 重新创建订单 |
| SYSTEMERROR | 系统错误 | 换单号重试 |
| BANKERROR | 银行系统异常 | 换单号重试 |
| USERPAYING | 支付中 | 等待用户输入密码确认 |
| AUTHCODEEXPIRE | 授权码过期 | 重新扫码 |
| NOTENOUGH | 余额不足 | 联系用户充值 |
