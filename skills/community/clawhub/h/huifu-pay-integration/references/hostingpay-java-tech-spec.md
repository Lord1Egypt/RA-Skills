## 目录

- [请求协议](#请求协议)
- [V2 接口请求格式](#v2-接口请求格式)
- [签名规则](#签名规则)
- [加密解密](#加密解密)
- [请求响应模型补充](#请求响应模型补充)
- [异步通知规范](#异步通知规范)
- [流水号规范](#流水号规范)
- [金额规范](#金额规范)
- [Spring Boot 兼容性](#spring-boot-兼容性)
- [异步通知 IP 白名单](#异步通知-ip-白名单)
- [HTTP 状态码](#http-状态码)

# 技术规范

## 请求协议

| 规范项 | 说明 |
|-------|------|
| 通信协议 | HTTPS |
| 请求方式 | POST |
| 数据格式 | JSON |
| 字符编码 | UTF-8 |
| 签名算法 | RSA（SHA256WithRSA） |
| API 基础地址 | `https://api.huifu.com/v2/` |

## V2 接口请求格式

### 请求报文结构

```json
{
    "sys_id": "商户/渠道商 huifu_id",
    "product_id": "汇付分配的产品号",
    "sign": "RSA 签名结果（SDK 自动生成）",
    "data": {
        "业务参数字段": "值"
    }
}
```

### 响应报文结构

```json
{
    "sign": "RSA 签名（SDK 自动验签）",
    "data": {
        "resp_code": "00000000",
        "resp_desc": "处理成功",
        "业务响应字段": "值"
    }
}
```

## 签名规则

1. 签名范围：对 `data` 字段的 JSON 字符串进行签名
2. 签名算法：RSA SHA256WithRSA
3. 私钥签名：商户使用自己的 RSA 私钥对请求 data 签名
4. 公钥验签：使用汇付 RSA 公钥验证响应 data 签名
5. **使用 SDK 时无需手动签名**，SDK 内部自动完成签名和验签

## 加密解密

部分敏感字段（如身份证号、银行卡号）需要加密传输：

- 加密算法：RSA
- 加密公钥：使用汇付提供的 RSA 公钥加密
- 应用场景：身份证号（cert_no）、银行卡号（card_no）等敏感信息

## 请求响应模型补充

| 项目 | 说明 |
|------|------|
| `Content-Type` | `application/json;charset=UTF-8` |
| 参数位置 | `sys_id`、`product_id`、`sign`、`data` 位于固定顶层 |
| URL 约束 | URL 参数中不要携带 JSON 数据 |
| 包体限制 | 请求或响应体尽量避免过大，文件场景优先走文件服务 |
| 空响应体 | 业务接口避免返回空响应体 |

字段补充说明：

- 通信层状态看 HTTP code，业务状态看 `data.resp_code`。
- 为避免混淆，如果业务字段与通用字段含义相同，建议统一字段名，例如 `resp_code`、`resp_desc`、`req_seq_id`。

## 异步通知规范

交易结果通过异步通知回调商户系统：

| 规范项 | 说明 |
|-------|------|
| 通知方式 | HTTP POST |
| 数据格式 | JSON |
| 通知时机 | 交易成功或失败时触发 |
| 通知频率 | 正常情况只触发一次 |
| 重试策略 | 通知失败后按策略重试（具体策略参见汇付文档） |

### 异步通知处理建议

1. 收到通知后返回 HTTP 200 + `RECV_ORD_ID_` + 请求流水号，否则汇付会重复推送
2. 通知可能有延迟，建议结合主动查询确认最终状态
3. 收到异步通知后调用查询接口进行**二次确认**，确保状态一致
4. 做好幂等处理，同一笔交易可能收到多次通知
5. 如需使用控台 Webhook，而不是接口 `notify_url`，请额外查看 `references/hostingpay-async-webhook.md`；Webhook 使用终端密钥 + MD5 原始事件体，不走 RSA 验签

## 流水号规范

| 字段 | 生成方式 | 唯一性要求 |
|------|---------|----------|
| req_seq_id | `SequenceTools.getReqSeqId32()` | 同一 huifu_id 下**当天唯一** |
| req_date | `DateTools.getCurrentDateYYYYMMDD()` | 当天日期，格式 yyyyMMdd |

## 金额规范

- 单位：**元**
- 格式：保留小数点后两位
- 最小值：0.01
- 示例：`"1.00"`、`"100.50"`

## 时间格式

| 场景 | 格式 | 示例 |
|------|------|------|
| 请求日期 | yyyyMMdd | 20240514 |
| 交易失效时间 | yyyyMMddHHmmss | 20240514165442 |
| 交易完成时间 | yyyyMMddHHmmss | 20240514170000 |

## Spring Boot 兼容性

| Spring Boot 版本 | 命名空间 | 说明 |
|-----------------|---------|------|
| 2.x | `javax.annotation.PostConstruct`、`javax.validation.constraints.NotBlank` | 默认 |
| 3.x (JDK 17/21) | `jakarta.annotation.PostConstruct`、`jakarta.validation.constraints.NotBlank` | 需替换 |

## 异步通知 IP 白名单

以下为汇付异步通知发送的服务器 IP，如需配置防火墙白名单：

```
47.102.109.221, 106.14.124.246, 139.224.233.243, 47.103.11.6,
139.224.222.55, 139.224.111.236, 139.224.111.237, 47.100.173.107,
101.132.173.54, 47.102.121.19, 47.103.197.28, 27.115.110.2,
116.228.159.35, 180.167.97.210, 112.64.184.162, 14.103.101.47
```

## 异步通知响应要求

- 收到通知后返回 HTTP 状态码 `200`
- 响应内容输出固定字符串：`RECV_ORD_ID_` + 交易应答中的请求流水号
- 超时时间 5 秒，超时后重试 3 次
- 自定义通知端口需使用 **8000-9005** 范围内
- URL 上请勿附带参数
- 同一异步消息可能通知多次，**必须做好幂等处理**

## 异步通知接收完整指南

### 通知报文结构

托管支付交易类异步通知，商户接收端通常拿到的是 `sign` 和 `resp_data` 两个字段；业务字段位于 `resp_data` 里，而不是直接平铺在最外层。

```json
{
    "sign": "返回签名串",
    "resp_data": "{\"resp_code\":\"00000000\",\"resp_desc\":\"交易成功\",\"huifu_id\":\"6666000109133323\",\"req_date\":\"20240514\",\"req_seq_id\":\"20240514165442868h32ss2g3s7vnxq\",\"hf_seq_id\":\"00290TOP1A240514165442P385ac131b5d00000\",\"trans_type\":\"T_MINIAPP\",\"trans_amt\":\"1.00\",\"trans_stat\":\"S\",\"trans_finish_time\":\"20240514170000\",\"is_div\":\"N\",\"is_delay_acct\":\"N\"}"
}
```

### `resp_data` 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| resp_code | String(8) | 业务返回码，用于日志和排查，不直接驱动订单终态 |
| resp_desc | String(512) | 响应描述 |
| huifu_id | String(32) | 商户号 |
| req_date | String(8) | 原始请求日期 |
| req_seq_id | String(64) | 原始请求流水号 |
| hf_seq_id | String(40) | 汇付全局流水号，**建议用作幂等键** |
| trans_type | String(20) | 交易类型（T_MINIAPP / A_JSAPI / WECHAT_NATIVE 等） |
| trans_amt | String(12) | 交易金额 |
| trans_stat | String(1) | 交易状态：S=成功、F=失败 |
| trans_finish_time | String(14) | 交易完成时间 yyyyMMddHHmmss |
| is_div | String(1) | 是否分账交易 |
| is_delay_acct | String(1) | 是否延迟入账 |

### Spring Boot 接收示例

以下示例是接收通知的流程片段。`HttpServletRequest` 的 import 按 Spring Boot 版本选择：2.x 用 `javax.servlet.*`，3.x 用 `jakarta.servlet.*`。`huifuPublicKey` 的注入方式可直接参考 `references/hostingpay-async-webhook.md` 中的完整类示例。

```java
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
// Spring Boot 2.x: import javax.servlet.http.HttpServletRequest;
// Spring Boot 3.x: import jakarta.servlet.http.HttpServletRequest;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/notify")
public class HuifuNotifyController {

    // huifuPublicKey 通过 @Value 或构造器注入，完整写法见 async-webhook.md

    @PostMapping("/payment")
    public String onPaymentNotify(HttpServletRequest request) {
        String respData = request.getParameter("resp_data");
        String sign = request.getParameter("sign");
        if (!StringUtils.hasText(respData) || !StringUtils.hasText(sign)) {
            throw new IllegalArgumentException("汇付回调缺少 resp_data 或 sign");
        }
        if (!RsaUtils.verify(respData, huifuPublicKey, sign)) {
            throw new IllegalArgumentException("汇付回调验签失败");
        }

        JSONObject dataObj = JSON.parseObject(respData);
        String reqSeqId = dataObj.getString("req_seq_id");
        String hfSeqId = dataObj.getString("hf_seq_id");
        String transStat = dataObj.getString("trans_stat");

        if (isDuplicate(hfSeqId)) {
            return "RECV_ORD_ID_" + reqSeqId;
        }

        // 建议继续调用查询接口做二次确认，再驱动业务状态机
        return "RECV_ORD_ID_" + reqSeqId;
    }
}
```

### 签名验证说明

- **验签原文**：交易类回调验签原文通常是 `resp_data` 中的内容；其他接口也可能是 `data`
- **验签公钥**：使用汇付 RSA 公钥
- **验签时机**：先验签，再 JSON 反序列化，再做幂等和业务处理
- **二次确认**：即使验签通过，仍建议调用查询接口做二次确认
- 完整示例见 `references/hostingpay-async-webhook.md`

### 幂等处理方案

| 方案 | 幂等键 | 实现方式 | 适用场景 |
|------|--------|---------|---------|
| Redis SETNX | `hf_seq_id` | `SETNX notify:{hf_seq_id}` + 48 小时过期 | 高并发场景 |
| 数据库唯一索引 | `hf_seq_id` | 通知记录表 `hf_seq_id` 列设唯一索引，INSERT 去重 | 通用场景 |
| 订单状态机 | `req_seq_id` + 状态 | 仅在订单状态为"待支付"时处理，已终态则跳过 | 强状态管理场景 |

### 通知重试策略

| 项目 | 说明 |
|------|------|
| 超时判定 | 商户 5 秒内未返回 HTTP 200 + 正确响应体 |
| 重试次数 | 最多 **3 次** |
| 响应格式 | HTTP 200 + 响应体 `RECV_ORD_ID_` + 请求流水号 |
| 端口要求 | 自定义通知端口需在 **8000-9005** 范围内 |
| URL 要求 | 不可附带查询参数（`?key=val`） |

> **关键提示**：异步通知可能延迟到达，生产环境应同时实现**主动轮询**（查询接口）+ **被动接收**（异步通知）双保险机制。

## HTTP 状态码

| HTTP Code | 说明 |
|-----------|------|
| 200 | 正常访问 |
| 404 | 服务不存在 |
| 412 | 请求体包含非法字符 |
| 500 | 后端服务器错误 |
| 502 | 后端服务调用超时或连接失败 |
| 512 | API 网关 SHUTDOWN |
| 911 | IP/商户/API 维度限流 |
| 914 | 接口总访问数限流 |
| 912 | 安全封禁 |
| 921 | 网关鉴权不通过 |
| 922 | 验签不通过 |
| 923 | 返回结果加签失败 |

## SDK 环境配置

```java
BasePay.debug = false;
BasePay.prodMode = BasePay.MODE_PROD;
// MODE_PROD = "prod";  // 生产环境
// MODE_TEST = "test";  // 线上联调环境
```

## SDK 自定义超时

```java
MerConfig merConfig = new MerConfig();
// 注意：参数类型为 String，不是 int
merConfig.setCustomSocketTimeout("30000");              // Socket 超时（毫秒）
merConfig.setCustomConnectTimeout("10000");              // 连接超时（毫秒）
merConfig.setCustomConnectionRequestTimeout("10000");    // 连接请求超时（毫秒）
```
