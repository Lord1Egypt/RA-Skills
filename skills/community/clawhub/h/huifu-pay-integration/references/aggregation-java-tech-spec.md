# 技术规范


## 目录

- 请求协议与报文模型
- 签名规则
- 异步通知
- HTTP 连接池配置
- 重试策略
- API 版本

## 请求协议与报文模型

| 项目 | 说明 |
|------|------|
| 通信协议 | HTTPS |
| 请求方式 | POST |
| 数据格式 | JSON |
| 字符编码 | UTF-8 |
| 建议头 | `Content-Type: application/json;charset=UTF-8` |

请求模型：

```json
{
  "sys_id": "调用方 huifu_id",
  "product_id": "产品号",
  "sign": "请求签名",
  "data": {
    "业务字段": "值"
  }
}
```

响应模型：

```json
{
  "sign": "返回签名",
  "data": {
    "resp_code": "00000000",
    "resp_desc": "处理成功"
  }
}
```

## 签名规则

### 请求签名

1. 将请求 `data` 对象序列化为 JSON
2. 对 JSON 中所有对象的 key 按 ASCII 值排序（数组不排序）
3. 使用商户 RSA 私钥对排序后的 JSON 字符串进行 SHA256WithRSA 签名
4. 将签名结果 Base64 编码后填入 `sign` 字段

> SDK 自动完成以上步骤，开发者无需手动处理。

### 响应验签

SDK 自动使用汇付 RSA 公钥验证响应签名，验签失败时抛出 `BasePayException`。

### RSA 密钥格式

- 私钥格式：PKCS#8（Base64 编码）
- 公钥格式：X.509（Base64 编码）

## 异步通知

### 通知机制

聚合支付支持两种异步通知方式：

1. **notify_url 回调**：下单时传入 `notify_url`，交易完成后汇付 POST 通知到该地址
2. **Webhook 事件**：通过汇付控台配置 Webhook 接收端，支持以下事件：
   - `trans.close` — 关单事件

### notify_url 接收规范

- **请求方式**：POST
- **报文形态**：交易类回调通常提交 `sign` 和 `resp_data` 字段，业务字段位于 `resp_data`
- **响应要求**：HTTP 200，body 返回 `RECV_ORD_ID_` + req_seq_id（5 秒内）
- **重试策略**：超时未响应最多重试 3 次
- **幂等键**：以 `hf_seq_id` 为幂等键，防止重复处理

以下示例为流程片段。`HttpServletRequest` 在 Spring Boot 2.x 使用 `javax.servlet.*`，在 3.x 使用 `jakarta.servlet.*`；`huifuPublicKey` 的注入方式可直接参考 `references/aggregation-async-webhook.md` 中的完整类示例。

```java
@PostMapping("/notify")
public String handleNotify(HttpServletRequest request) {
    String respData = request.getParameter("resp_data");
    String sign = request.getParameter("sign");
    if (!RsaUtils.verify(respData, huifuPublicKey, sign)) {
        throw new IllegalArgumentException("汇付回调验签失败");
    }

    JSONObject notification = JSON.parseObject(respData);
    String reqSeqId = notification.getString("req_seq_id");
    String hfSeqId = notification.getString("hf_seq_id");
    String transStat = notification.getString("trans_stat");

    if (isProcessed(hfSeqId)) {
        return "RECV_ORD_ID_" + reqSeqId;
    }

    // 先查单确认，再按 trans_stat 驱动订单状态
    if ("S".equals(transStat)) {
        // 交易成功
    } else if ("F".equals(transStat)) {
        // 交易失败
    }

    return "RECV_ORD_ID_" + reqSeqId;
}
```

### Webhook 使用

Webhook 是汇付提供的事件通知机制，与 notify_url 独立，可在汇付控台灵活配置接收端。

配置方式参见汇付文档：[Webhook 使用说明](https://paas.huifu.com/open/doc/devtools/#/webhook/webhook_jieshao)

Webhook 与 API 的签名密钥不是一套：

- API 请求和 `notify_url` 回调使用 RSA 密钥体系。
- Webhook 使用控台配置的终端密钥，对原始事件体计算 MD5。
- Webhook 不使用汇付 RSA 公钥验签，也不要靠 `sign` 长度自动猜算法。
- 详细说明见 `references/aggregation-async-webhook.md`。

## HTTP 连接池配置

SDK 内置 Apache HttpClient 连接池，默认配置：

| 参数 | 默认值 |
|------|-------|
| 最大连接数 | 500 |
| 每路由最大连接数 | 40 |
| 每主机最大连接数 | 100 |
| Socket 超时 | 20 秒 |
| 连接超时 | 20 秒 |
| 连接请求超时 | 30 秒 |

可通过 MerConfig 自定义超时：

```java
merConfig.setCustomConnectTimeout(30000);
merConfig.setCustomSocketTimeout(30000);
merConfig.setCustomConnectionRequestTimeout(40000);
```

## 重试策略

SDK 内置重试机制：
- 最多重试 3 次
- 可重试场景：`NoHttpResponseException`、非实体请求
- 不重试场景：SSL 错误、Socket 超时、SSL 握手失败

## API 版本

聚合支付接口涉及不同的 API 版本：

| 接口 | API 路径 | 版本 |
|------|---------|------|
| 聚合支付下单 | /v4/trade/payment/create | v4 |
| 聚合交易查询 | /v4/trade/payment/scanpay/query | v4 |
| 交易退款 | /v4/trade/payment/scanpay/refund | v4 |
| 交易退款查询 | /v4/trade/payment/scanpay/refundquery | v4 |
| 聚合交易关单 | /v2/trade/payment/scanpay/close | v2 |
| 聚合交易关单查询 | /v2/trade/payment/scanpay/closequery | v2 |
| 对账单查询 | /v2/trade/check/filequery | v2 |

> SDK 自动处理 API 路径路由，开发者无需关心版本差异。
