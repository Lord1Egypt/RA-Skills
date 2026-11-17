# 异步通知与 Webhook

> 本文面向 `references/aggregation-base.md` 依赖的聚合支付 Skill，重点把交易通知的真实报文形态、验签方式、幂等和终态判断说明清楚。


## 目录

- 两种异步机制
- `notify_url` 使用规范
- 聚合交易通知报文形态
- Spring Boot 接收、验签与查单示例
- 终态判断原则
- 签名差异
- Webhook 使用场景
- Webhook 落地步骤
- Webhook 重发规则
- 使用建议
- 参考

## 两种异步机制

| 机制 | 入口 | 用途 | 签名方式 |
|------|------|------|----------|
| `notify_url` | 下单、退款等接口请求参数 | 交易结果回调 | 汇付 RSA 公钥验签 |
| Webhook | 汇付控台端点订阅 | 平台事件通知 | 终端密钥 + MD5 原始事件体 |

## `notify_url` 使用规范

- 汇付以 HTTP `POST` 发送交易结果。
- 响应必须在 5 秒内返回。
- 正确应答格式为：HTTP `200` + `RECV_ORD_ID_` + `req_seq_id`。
- 未及时应答或应答格式不正确时，汇付会自动重试，最多 3 次。
- 自定义端口需落在 `8000-9005`。
- URL 不要带查询参数。
- 同一笔交易可能会重复通知，必须用 `hf_seq_id` 做幂等。

## 聚合交易通知报文形态

聚合支付的交易类异步通知，外层通常包含以下 4 个网关字段：

| 字段 | 说明 |
|------|------|
| `resp_code` | 网关返回码 |
| `resp_desc` | 网关返回信息 |
| `sign` | 对整个业务数据的签名 |
| `resp_data` | 业务数据 JSON 字符串 |

其中真正要驱动业务的字段在 `resp_data` 里，而不是直接平铺在最外层。

```json
{
  "resp_code": "10000",
  "resp_desc": "成功调用",
  "sign": "返回签名串",
  "resp_data": "{\"resp_code\":\"00000000\",\"resp_desc\":\"处理成功\",\"req_seq_id\":\"20240514163256046l9da4ecgqugo7h\",\"req_date\":\"20240514\",\"hf_seq_id\":\"00290TOP1A240514165442P385ac131b5d00000\",\"trans_type\":\"T_JSAPI\",\"trans_amt\":\"1.00\",\"trans_stat\":\"S\"}"
}
```

## Spring Boot 接收、验签与查单示例

```java
import com.alibaba.fastjson.JSON;
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
public class AggregateNotifyController {

    private final String huifuPublicKey;
    private final AggregateQueryService queryService;
    private final NotifyIdempotentService idempotentService;

    public AggregateNotifyController(
            @Value("${huifu.rsa-public-key}") String huifuPublicKey,
            AggregateQueryService queryService,
            NotifyIdempotentService idempotentService) {
        this.huifuPublicKey = huifuPublicKey;
        this.queryService = queryService;
        this.idempotentService = idempotentService;
    }

    @PostMapping("/payment")
    public String onNotify(HttpServletRequest request) {
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
        String transType = dataObj.getString("trans_type");

        if (idempotentService.isProcessed(hfSeqId)) {
            return "RECV_ORD_ID_" + reqSeqId;
        }

        AggregateQueryResult queryResult = queryService.query(reqDate, reqSeqId);
        if (!Objects.equals(queryResult.getTransStat(), transStat)) {
            throw new IllegalStateException("异步通知与查单状态不一致");
        }

        if ("S".equals(transStat)) {
            // 支付成功：更新订单并执行后续业务
        } else if ("F".equals(transStat)) {
            // 支付失败：记录失败原因
        } else if ("P".equals(transStat)) {
            // 处理中：继续等待通知或轮询
        } else {
            throw new IllegalStateException("未知 trans_stat=" + transStat);
        }

        // 同步返回常见字段名是 trade_type，异步回调字段名是 trans_type，不要混用
        // 例如：log.info("notify reqSeqId={}, hfSeqId={}, transType={}, transStat={}", ...);
        return "RECV_ORD_ID_" + reqSeqId;
    }
}
```

## 终态判断原则

- `trans_stat`、查单结果、幂等键可以驱动订单状态流转。
- `resp_code`、`resp_desc`、HTTP 返回码主要用于排查，不直接驱动订单终态。
- 不要写“`resp_code=00000000` 就直接支付成功”这种逻辑。

## 签名差异

| 场景 | 密钥 | 说明 |
|------|------|------|
| API 请求与 `notify_url` | 商户 RSA 私钥签名，汇付 RSA 公钥验签 | `SHA256WithRSA` |
| Webhook | Webhook 终端密钥 | `MD5(raw_body + endpoint_key)`，与 API RSA 密钥无关 |

Webhook 必须先对原始请求体验签，再 JSON 解析事件体。不要先反序列化后重新序列化，也不要用 `sign` 长度自动猜 MD5 / RSA。完整共享规则见 `shared-webhook-signing.md`。

## Webhook 使用场景

Webhook 更适合做平台级事件通知，例如：

| 事件类型编号 | 说明 |
|--------------|------|
| `trans.close` | 关单事件 |
| `refund.standard` | 退款事件 |
| `statement.day` | 日结算通知 |
| `statement.auto` | 自动结算通知 |
| `settlement.encashment` | 取现通知 |

## Webhook 落地步骤

1. 在服务端创建 HTTPS 端点。
2. 在汇付控台注册端点并选择订阅事件。
3. 使用测试事件验证联通性。
4. 处理正式事件，并监控失败重试。

## Webhook 重发规则

- 首次发送失败后会快速重试 3 次。
- 之后按小时级补发，直到成功。
- 控台支持手工重新推送。

## 使用建议

- 支付交易主状态仍优先依赖 `notify_url` 和主动查询。
- Webhook 更适合对账、结算、告警和平台事件同步。
- API 回调验签和 Webhook 验签必须分开实现，不要共用密钥。

## 参考

- 平台 Webhook 工具介绍：<https://paas.huifu.com/open/doc/devtools/#/webhook/webhook_jieshao>
