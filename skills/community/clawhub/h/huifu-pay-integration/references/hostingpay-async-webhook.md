# 异步通知与 Webhook

> 本文面向 `references/hostingpay-base.md` 依赖的托管支付 Skill，重点解决 3 个常见误区：回调报文到底长什么样、验签应该验哪一段、哪些字段能用于驱动订单终态。


## 目录

- 两种机制的区别
- `notify_url` 回调规则
- 交易类回调的真实报文形态
- Spring Boot 接收与验签示例
- 按场景解析扩展字段示例
- 哪些字段能写业务逻辑
- `notify_url` 应答要求
- Webhook 规则
- Webhook 签名与 API 签名的区别
- Webhook 落地步骤
- Webhook 重试策略
- 常见事件类型
- 使用建议
- 参考

## 两种机制的区别

| 机制 | 触发方式 | 适用场景 | 签名方式 | 推荐用途 |
|------|----------|----------|----------|----------|
| `notify_url` 回调 | 下单、退款等交易接口请求时显式上送 | 支付交易主链路 | 汇付 RSA 公钥验签 | 订单状态更新、退款结果通知 |
| Webhook 事件 | 在汇付控台注册端点并订阅事件 | 平台级事件广播 | 终端密钥 + MD5 原始事件体 | 对账、结算、投诉、配置类事件 |

## `notify_url` 回调规则

- 汇付通过 HTTP `POST` 推送交易结果。
- 回调编码统一为 `UTF-8`。
- 默认超时时间 5 秒；超时或未正确应答时会重试，最多 3 次。
- 自定义通知端口需使用 `8000-9005`。
- URL 不允许附带查询参数，也不支持重定向。
- 同一笔交易收到多次通知是正常现象，必须做幂等处理。

## 交易类回调的真实报文形态

托管支付的交易类异步通知，商户接收端通常直接拿到两个关键字段：

- `sign`：签名串
- `resp_data`：业务数据 JSON 字符串

也就是说，业务字段通常不在最外层直接展开，不能把 `req_seq_id`、`hf_seq_id`、`trans_stat` 当成 `@RequestBody Map` 顶层字段直接取。

```json
{
  "sign": "返回签名串",
  "resp_data": "{\"resp_code\":\"00000000\",\"resp_desc\":\"交易成功\",\"req_seq_id\":\"20240514163256046l9da4ecgqugo7h\",\"req_date\":\"20240514\",\"hf_seq_id\":\"00290TOP1A240514165442P385ac131b5d00000\",\"trans_type\":\"A_NATIVE\",\"trans_amt\":\"1.00\",\"trans_stat\":\"S\"}"
}
```

> 商户配置、进件等非交易类接口回调，业务体有时会放在 `data` 而不是 `resp_data`。是否使用 `data` 还是 `resp_data`，以该接口自己的返回文档为准；本文下面的示例只针对支付、退款这类交易通知。

## Spring Boot 接收与验签示例

下面这段示例代码覆盖了 6 个关键动作：取参、验签、解析、幂等、查单二次确认、固定应答。`HttpServletRequest` 的 import 按 Spring Boot 版本选择：2.x 用 `javax.servlet.*`，3.x 用 `jakarta.servlet.*`。

```java
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
// Spring Boot 2.x: import javax.servlet.http.HttpServletRequest;
// Spring Boot 3.x: import jakarta.servlet.http.HttpServletRequest;
import java.util.Objects;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/notify")
public class HuifuNotifyController {

    private final String huifuPublicKey;
    private final HostingPayQueryService queryService;
    private final NotifyIdempotentService idempotentService;

    public HuifuNotifyController(
            @Value("${huifu.rsa-public-key}") String huifuPublicKey,
            HostingPayQueryService queryService,
            NotifyIdempotentService idempotentService) {
        this.huifuPublicKey = huifuPublicKey;
        this.queryService = queryService;
        this.idempotentService = idempotentService;
    }

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
        String reqDate = dataObj.getString("req_date");
        String hfSeqId = dataObj.getString("hf_seq_id");
        String transStat = dataObj.getString("trans_stat");
        String respCode = dataObj.getString("resp_code");

        if (idempotentService.isProcessed(hfSeqId)) {
            return ack(reqSeqId);
        }

        HostingPayQueryResult queryResult = queryService.query(reqDate, reqSeqId);
        if (!Objects.equals(queryResult.getTransStat(), transStat)) {
            throw new IllegalStateException("异步通知与查单状态不一致");
        }

        if ("S".equals(transStat)) {
            // 支付成功：更新订单、发货、落账
        } else if ("F".equals(transStat)) {
            // 支付失败：标记失败并记录失败原因
        } else if ("P".equals(transStat)) {
            // 处理中：记录状态，等待后续通知或继续轮询
        } else {
            throw new IllegalStateException("未知 trans_stat=" + transStat);
        }

        // resp_code 用于日志和排查，不直接驱动订单终态
        // 例如：log.info("notify reqSeqId={}, hfSeqId={}, respCode={}, transStat={}", ...);
        return ack(reqSeqId);
    }

    private String ack(String reqSeqId) {
        return "RECV_ORD_ID_" + reqSeqId;
    }
}
```

## 按场景解析扩展字段示例

`resp_data` 里的扩展字段是否出现，取决于 `trans_type` 和业务配置。不要把某个场景的字段解析逻辑硬套到所有回调里。

下面以你提供的 `A_NATIVE` 场景为例，演示如何在主流程验签完成后再按需解析扩展字段：

```java
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;

String transType = dataObj.getString("trans_type");
if ("A_NATIVE".equals(transType)) {
    JSONArray feeFormulaInfos = JSON.parseArray(dataObj.getString("fee_formula_infos"));
    if (feeFormulaInfos != null && !feeFormulaInfos.isEmpty()) {
        String feeFormula = feeFormulaInfos.getJSONObject(0).getString("fee_formula");
    }

    JSONObject transFeeAllowanceInfo =
            JSON.parseObject(dataObj.getString("trans_fee_allowance_info"));
    if (transFeeAllowanceInfo != null) {
        String actualFeeAmt = transFeeAllowanceInfo.getString("actual_fee_amt");
    }

    JSONObject acctSplitBunch = JSON.parseObject(dataObj.getString("acct_split_bunch"));
    if (acctSplitBunch != null) {
        String feeAcctId = acctSplitBunch.getString("fee_acct_id");
        JSONArray acctInfos = JSON.parseArray(acctSplitBunch.getString("acct_infos"));
        if (acctInfos != null && !acctInfos.isEmpty()) {
            String acctId = acctInfos.getJSONObject(0).getString("acct_id");
        }
    }
}
```

关键点：

- 上面这些字段只在部分支付方式、分账、手续费补贴等场景出现。
- 没有这个字段就不要强行解析，更不要把某个示例字段当成所有通知都会返回。
- 同步返回字段名和异步返回字段名可能不同，解析时以异步文档为准。

## 哪些字段能写业务逻辑

- `trans_stat`、查单结果、业务幂等键可以驱动订单状态流转。
- `resp_code`、`resp_desc`、HTTP 返回码主要用于排查和日志。
- 不要写“`resp_code=00000000` 就直接把订单改成功”这种逻辑。

## `notify_url` 应答要求

- HTTP 状态码返回 `200`。
- 响应体必须输出固定字符串：`RECV_ORD_ID_` + 请求流水号。
- 建议优先使用 `req_seq_id` 作为应答拼接字段。
- 只有在验签、字段校验、核心落库逻辑都通过后才返回成功应答。
- 验签失败、缺字段、数据库异常时不要回伪成功；让汇付按重试策略重推，便于暴露真实问题。

## Webhook 规则

- Webhook 是平台级事件通知，不依赖单次交易请求中的 `notify_url`。
- 需要先在汇付控台注册端点并订阅事件。
- Webhook 推荐使用 `HTTPS` 端点。
- 端点收到消息后返回任意 `2xx` 状态码即可视为接收成功；超出 `2xx` 范围都视为失败。
- Webhook 可用于交易事件、结算事件、投诉事件、商户配置事件等。

## Webhook 签名与 API 签名的区别

| 项目 | API / `notify_url` | Webhook |
|------|--------------------|---------|
| 密钥类型 | 商户 RSA 私钥签名，汇付 RSA 公钥验签 | 终端密钥 + MD5 |
| 密钥来源 | API 接入密钥管理 | Webhook 端点配置中的终端密钥 |
| 是否可共用 | 否 | 否 |

关键点：

- Webhook 的终端密钥独立于接口使用的 RSA 密钥。
- 不要把 Webhook 终端密钥当作 API 加签私钥使用。
- 不要用汇付 RSA 公钥校验 Webhook。
- 如果配置了终端密钥，Webhook 发送时会带上 `sign`，接收端必须按 `MD5(raw_body + endpoint_key)` 校验。
- 必须先对原始请求体验签，再 JSON 解析事件体，避免 `0.00` 被重新序列化成 `0`。
- 完整共享规则见 `shared-webhook-signing.md`。

## Webhook 落地步骤

1. 在自己的服务端创建 Webhook 端点。
2. 在汇付控台注册端点 URL，并选择关注的事件。
3. 在控台发送测试事件验证联通性。
4. 上线后监控失败重发和幂等处理。

## Webhook 重试策略

- 首次发送失败后，约 1 秒重试一次，共尝试 3 次。
- 之后会每小时自动补发一次，直到成功。
- 控台支持手工重新推送。

## 常见事件类型

| 事件类型编号 | 说明 |
|--------------|------|
| `refund.standard` | 交易退款 |
| `trans.close` | 交易关单 |
| `statement.day` | 日结算通知 |
| `statement.auto` | 结算通知 |
| `settlement.encashment` | 取现结果通知 |
| `wechat.complaint` | 微信投诉 |
| `fund.bank_deposit` | 银行入账通知 |

## 使用建议

- 支付主流程仍以 `notify_url` 为准，Webhook 适合做补充通知和平台事件订阅。
- 重要交易状态不要只依赖被动通知，仍应通过查询接口兜底确认。
- Webhook 事件体通常较大，接收后建议落原始 JSON，再异步解析。
- 接口回调和 Webhook 最好分开 URL、分开验签逻辑、分开监控。

## 参考

- 平台 Webhook 工具介绍：<https://paas.huifu.com/open/doc/devtools/#/webhook/webhook_jieshao>
- 详细事件模板和字段说明以汇付官方资料为准。
