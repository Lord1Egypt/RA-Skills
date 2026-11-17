# Webhook 签名规则

这份文档只处理汇付控台 Webhook 的签名边界。

如果你接的是接口参数里的 `notify_url`，先看 `shared-async-notify.md` 和 `shared-signing-v2.md`；不要把两套机制混成一个入口。

## 两种入口

| 入口 | 触发方式 | 业务数据 | 验签方式 | 成功应答 |
| --- | --- | --- | --- | --- |
| `notify_url` | 下单、退款等接口参数 | `resp_data` 或少数接口的 `data` | 汇付 RSA 公钥验签 | HTTP `200` + `RECV_ORD_ID_` + 请求流水号 |
| 控台 Webhook | 汇付控台端点订阅 | 原始 JSON 事件体 | 终端密钥 + MD5 | 任意 `2xx` |

## Webhook 验签规则

Webhook 不使用 API RSA 公私钥。

验签步骤：

1. 从请求中取官方发送的 `sign`。FAQ 口径里 `sign` 常在 URL query 参数中，不一定在 header；实现时按当前 Web 框架同时确认 query/header 读取位置。
2. 读取原始请求体字符串 `raw_body`。
3. 读取当前 Webhook 端点配置的 32 位终端密钥 `endpoint_key`。
4. 计算 `MD5(raw_body + endpoint_key)`。官方和本地沙箱按大写十六进制字符串发送 `sign`。
5. 将计算结果与 `sign` 做大小写不敏感比较，避免历史 SDK/helper 输出小写导致误判。
6. 验签通过后，再 JSON 解析事件体并执行业务处理。

必须先用原始请求体验签，再做 JSON 解析。不要先反序列化再重新序列化；金额里的 `0.00` 可能被改成 `0`，导致验签失败。

## PHP SDK 口径

官方 PHP SDK 的 `BsPayTools::verify_webhook_sign($sign, $data, $key)` 使用：

```text
md5(json_encode($data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . $key)
```

如果应用已经拿到了原始请求体，优先用原始请求体直接计算 `MD5(raw_body + endpoint_key)`；如果只能复用 SDK helper，必须保证 `$data` 的序列化结果与汇付原始事件体完全一致。

## Java 参考形态

开发指南里的 Java Demo 本质是：

```java
String expected = md5Hex(rawBody + endpointKey);
if (!expected.equalsIgnoreCase(sign)) {
    throw new IllegalArgumentException("Webhook 验签失败");
}
```

这只是 Webhook 事件验签。`notify_url` 的 `resp_data + sign` 仍走 RSA 验签。

本地沙箱 `hf-payment-local-sandbox 1.0.1` 的 Webhook 签名与官方口径对齐：`sign` 放在 URL query 参数中，值为大写 `MD5(raw_body + endpoint_key)`。业务接收端仍建议使用 `equalsIgnoreCase` 或等价逻辑比较。

## 禁止混用

- 不要拿 Webhook 终端密钥做 API 请求签名。
- 不要拿 API RSA 私钥或汇付 RSA 公钥校验 Webhook。
- 不要把 `notify_url` 的 `RECV_ORD_ID_` 应答套到 Webhook。
- 不要用 `sign` 长度或字符形态自动猜 MD5 / RSA。
- 不要把 Webhook 事件当作支付主链路的唯一终态依据；重要交易仍建议查询二次确认。

## 参考来源

- 官方 Webhook 工具介绍：`https://paas.huifu.com/open/doc/devtools/#/webhook/webhook_jieshao`
- 官方 PHP SDK：`BsPaySdk\core\BsPayTools::verify_webhook_sign`
- 开发指南 Demo：`docs/开发指南/webhook加解签DEMO/MD5Utils.java`
