# 托管支付退款快速接入


## 目录

- 这份文档解决什么问题
- 细分文档
- 退款流程
- 快速接入
- 关键陷阱
- 额外环境变量
- 常见问题

对已支付成功的订单发起退款，并查询退款处理结果。

> **前置依赖**：首次接入请先完成 `references/hostingpay-base.md` 的 SDK 初始化。

## 这份文档解决什么问题

用户完成支付（trans_stat=S）后，因业务原因需要全额或部分退款。退款为异步处理，需要通过退款查询和异步通知闭环确认最终结果。

## 细分文档

- `references/hostingpay-refund.md`
- `references/hostingpay-refund-query.md`
- `references/hostingpay-refund-php-scenarios.md`

## 退款流程

```
① 确认原交易 trans_stat=S（通过 references/hostingpay-query.md 查询）
       ↓
② 调用退款接口（当前文档链路）
       ↓
③ 同步返回 resp_code=00000000 → 仅表示退款请求已受理，非最终结果
       ↓
④ 等待异步通知 或 轮询退款查询接口
       ↓
⑤ trans_stat=S → 退款成功，执行业务退款逻辑
```

## 快速接入

### 退款申请

```java
V2TradeHostingPaymentHtrefundRequest request = new V2TradeHostingPaymentHtrefundRequest();
request.setReqDate(DateTools.getCurrentDateYYYYMMDD());
request.setReqSeqId(SequenceTools.getReqSeqId32());
request.setHuifuId("你的商户号");
request.setOrdAmt("1.00");                                // 退款金额
request.setOrgReqDate("20240514");                         // 原交易日期
request.setTerminalDeviceData("{\"device_type\":\"4\"}");  // 设备信息，必填
request.setRiskCheckData("");
request.setBankInfoData("");

// ⚠️ org_req_seq_id 无专属 setter，必须通过 extendInfoMap 传入！
Map<String, Object> extendInfoMap = new HashMap<>();
extendInfoMap.put("org_req_seq_id", "原交易流水号");
extendInfoMap.put("notify_url", "https://your-domain.com/refund-notify");
request.setExtendInfo(extendInfoMap);

Map<String, Object> response = BasePayClient.request(request, false);
```

### 退款结果查询

```java
V2TradeHostingPaymentQueryrefundinfoRequest request = new V2TradeHostingPaymentQueryrefundinfoRequest();
request.setReqDate(DateTools.getCurrentDateYYYYMMDD());
request.setReqSeqId(SequenceTools.getReqSeqId32());
request.setHuifuId("你的商户号");
request.setOrgReqDate("退款请求日期");     // 退款接口的 req_date（非原支付日期）
request.setOrgReqSeqId("退款请求流水号");   // 退款接口的 req_seq_id

Map<String, Object> response = BasePayClient.request(request, false);
String transStat = (String) response.get("trans_stat");
// S=退款成功, F=退款失败, P=处理中
```

完整参数和 JSON 示例见各 reference 文档。

## 关键陷阱

### 1. org_req_seq_id 无 setter

退款最重要的字段 `org_req_seq_id`（原交易流水号）**没有独立 setter**，必须通过 `extendInfoMap` 传入：

```java
// ✗ 错误 — 编译报错，不存在此方法
request.setOrgReqSeqId("xxx");

// ✓ 正确
extendInfoMap.put("org_req_seq_id", "xxx");
request.setExtendInfo(extendInfoMap);
```

### 2. device_type 选择

退款时 `device_type` 需与原交易场景匹配：

| 原交易场景 | device_type |
|-----------|------------|
| H5 手机网页 | `"1"` |
| PC 网页 | `"4"` |
| 支付宝/微信小程序 | `"1"` |

不确定时用 `"4"` 通常可以通过校验。

### 3. resp_code=00000000 不等于退款成功

同步返回成功**仅表示退款请求已受理**，退款是异步处理的。最终结果以退款查询和异步通知闭环为准。

### 4. 退款查询结果字段

Java 代码读取退款查询结果时固定使用 `trans_stat`，不要生成或读取其它退款状态别名。

## 额外环境变量

| 变量 | 说明 |
|------|------|
| `HUIFU_REFUND_NOTIFY_URL` | 退款结果异步通知地址 |

## 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 编译报错 `cannot find symbol: setOrgReqSeqId` | org_req_seq_id 无专属 setter | 通过 extendInfoMap 传入 |
| 退款金额校验失败 | 超过原交易金额 | 检查 ord_amt 不超过原交易 trans_amt |
| 重复退款被拒绝 | 相同 org_req_seq_id 已退过 | 做幂等校验，或使用不同的退款流水号 |
| 退款一直 P 状态 | 退款异步处理中 | 等待异步通知或轮询退款查询接口 |
