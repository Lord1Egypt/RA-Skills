# 托管支付查询、关单与对账快速接入


## 目录

- 这份文档解决什么问题
- 官方产品文档确认的额外前提
- 细分文档
- 快速接入
- trans_stat=P 轮询策略
- 关键约束
- 下一步

支付状态查询、拆单支付订单查询、托管交易关单和交易结算对账单查询。

> **前置依赖**：首次接入请先完成 `references/hostingpay-base.md` 的 SDK 初始化。

## 这份文档解决什么问题

| 场景 | 问题 | 解决方案 |
|------|------|---------|
| 支付后页面未跳转 | 用户不确定是否支付成功 | 调用**查询接口**确认 trans_stat |
| 收到异步通知 | 通知可能被伪造 | 调用**查询接口**做二次确认 |
| 微信小程序拆单支付后要看子交易 | 普通查单只给订单级信息 | 调用**拆单支付订单查询**读取 `trans_list[].trans_stat` |
| trans_stat=P | 交易还在处理中 | **轮询查询**：间隔 5 秒，最多 30 次 |
| 用户长时间未支付 | 订单占用库存 | 调用**关单接口**释放资源 |
| 需要财务对账 | 核对交易/结算明细 | 调用**对账单查询**下载对账文件 |

## 官方产品文档确认的额外前提

- 托管产品文档明确建议：前端页面回跳和异步通知都不能替代关键业务环节的主动查询确认。
- 对账单文档明确要求：先在控台配置对账文件生成；`sys_id`、`product_id` 可从开发者信息获取。

## 细分文档

- `references/hostingpay-query.md`
- `references/hostingpay-query-payment-status-query.md`
- `references/hostingpay-query-splitpay.md`
- `references/hostingpay-query-trade-close.md`
- `references/hostingpay-query-reconciliation.md`
- `references/hostingpay-query-php-scenarios.md`

## 快速接入

### 支付状态查询

```java
V2TradeHostingPaymentQueryorderinfoRequest request = new V2TradeHostingPaymentQueryorderinfoRequest();
request.setReqDate(DateTools.getCurrentDateYYYYMMDD());
request.setReqSeqId(SequenceTools.getReqSeqId32());
request.setHuifuId("你的商户号");
request.setOrgReqDate("原交易日期");       // 来自预下单响应的 req_date
request.setOrgReqSeqId("原交易流水号");     // 来自预下单响应的 req_seq_id

Map<String, Object> response = BasePayClient.request(request, false);
String transStat = (String) response.get("trans_stat");
// S=成功, F=失败, P=处理中（需继续轮询）
```

### 托管交易关单

```java
V2TradeHostingPaymentCloseRequest request = new V2TradeHostingPaymentCloseRequest();
request.setReqDate(DateTools.getCurrentDateYYYYMMDD());
request.setReqSeqId(SequenceTools.getReqSeqId32());
request.setHuifuId("你的商户号");
request.setOrgReqDate("原交易日期");
request.setOrgReqSeqId("原交易流水号");

Map<String, Object> response = BasePayClient.request(request, false);
```

完整参数和 JSON 示例见各 reference 文档。

### 交易结算对账单查询

```java
V2TradeCheckFilequeryRequest request = new V2TradeCheckFilequeryRequest();
request.setReqDate(DateTools.getCurrentDateYYYYMMDD());
request.setReqSeqId(SequenceTools.getReqSeqId32());
request.setHuifuId("你的商户号");
request.setFileDate("20240428");  // 字段名固定是 file_date；补生成场景填交易日期+1天

// 可选：指定文件类型
Map<String, Object> extendInfoMap = new HashMap<>();
extendInfoMap.put("bill_type", "TRADE_BILL"); // 字段名固定是 bill_type，不要改成 file_type
request.setExtendInfo(extendInfoMap);

Map<String, Object> response = BasePayClient.request(request, false);
// file_details 是已生成文件；未生成或跑批中时查看 task_details.task_stat
```

完整参数和返回说明见 `references/hostingpay-query-reconciliation.md`。

字段命名约束：

- 请求参数名固定使用 `file_date` 和 `bill_type`
- `file_date` 表示文件生成日期，不要改成 `bill_date`、`generate_date`
- “文件类型”只是中文描述，不是建议改成 `file_type`
- 除非用户已有存量接口兼容要求，否则不要额外设计 `file_type -> bill_type` 转换层

## trans_stat=P 轮询策略

当查询结果为 `trans_stat=P`（处理中）时，**不可当作失败处理**：

```
1. 前端展示"支付处理中"
2. 后端轮询查询接口：间隔 5 秒，最多 30 次（150 秒）
3. 同时监听异步通知，以先到者为准
4. 150 秒后仍为 P → 记录异常日志，人工介入，不要自动关单
```

## 关键约束

- 查询和关单都需要原交易的 `org_req_date` + `org_req_seq_id`（来自预下单响应，务必保存）
- **已支付成功的订单无法关单**，只能走退款流程
- 关单前建议先查询确认订单确实未支付，避免"关单瞬间用户完成支付"的竞态问题
- 关单成功后用户将无法再对该订单支付

## 下一步

| 查询结果 | 下一步操作 |
|---------|-----------|
| trans_stat=S | 执行业务成功逻辑（发货等） |
| trans_stat=F | 提示用户重新发起支付 |
| trans_stat=P 超时 | 人工介入排查 |
| 需要退款 | 前往 `references/hostingpay-refund.md` |
