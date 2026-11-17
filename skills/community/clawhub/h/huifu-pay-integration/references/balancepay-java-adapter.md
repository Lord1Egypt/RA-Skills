# 余额支付 Java SDK 适配

初始化复用 `hostingpay-java-sdk-quickstart.md` 的通用 `dg-java-sdk 3.0.41`，本页不使用Lightning客户端。请求前全局关闭 `BasePay.debug`，凭据和来源头来自服务端配置。

六个专属类及声明字段见 `balancepay-sdk-matrix.md`。完整字段、条件和String(JSON)先按 `payment-complete-field-catalog.md`、`balancepay-field-contracts.md` 验证；声明字段走setter，其他正式字段走 `setExtendInfo`，扩展不得覆盖setter字段。SDK私有必填集合不能覆盖官网C/N条件。

## 查单与短信

示例以已验证的业务输入为参数，保留原日期与流水。真实金额、分账、出款号等值由调用方提供；不生成示例生产ID。

```java
import com.huifu.bspay.sdk.opps.client.BasePayClient;
import com.huifu.bspay.sdk.opps.core.exception.BasePayException;
import com.huifu.bspay.sdk.opps.core.request.V2TradeAcctpaymentPayQueryRequest;
import java.util.HashMap;
import java.util.Map;

public final class BalanceQueryAdapter {
    public static Map<String, Object> query(String initiatorId, String originalDate,
                                           String originalRequestId)
            throws BasePayException, IllegalAccessException {
        V2TradeAcctpaymentPayQueryRequest request = new V2TradeAcctpaymentPayQueryRequest();
        request.setHuifuId(initiatorId);
        request.setOrgReqDate(originalDate);
        Map<String, Object> extra = new HashMap<>();
        extra.put("org_req_seq_id", originalRequestId);
        request.setExtendInfo(extra);
        return BasePayClient.request(request);
    }

    public static Map<String, Object> sendSms(Map<String, Object> validatedSmsData)
            throws BasePayException {
        // 五个字段已按短信原子页校验；不包含外层信封或签验开关。
        return BasePayClient.request(new HashMap<>(validatedSmsData),
                "v2.trade.sms.verifycode.send", false);
    }
}
```

查询的可替代全局流水分支只发送 `org_hf_seq_id`；不同时发送两个定位键。短信映射仅 `req_seq_id/req_date/out_huifu_id/mobile_no/trans_type`，不得添加 `huifu_id`、关闭验签或使用 `isPage=true`。

## 支付与退款

支付分别将分账对象和风控对象序列化为JSON字符串，然后设置 `acctSplitBunch/riskCheckData`；原生 `acct_infos` 数组仅存在于字符串解码后的对象中。条件字段仅在条件成立时设置，不能发送编造默认值。

官方通用 `BasePayClient.request(Map, funcCode, false)` 也可承载经过完整字段校验的常规业务映射，保持签验主链路；不能改成HttpClient/OkHttp手写传输。同步返回验签由SDK处理，业务仍校验 `trans_stat`。余额支付通知的未知包装/ACK单独留TODO，不沿用托管通知代码。
