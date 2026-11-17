# 前端回调与最终状态确认

> 这份文档只收口一个高风险问题：前端 callback 只能代表支付过程事件，不能直接当作最终支付成功。
> 最终回答最短结论必须包含：前端 `callback` 不等于最终支付成功；最终确认要同时看 `hostingpay-query.md` 和 `hostingpay-async-webhook.md`，不能只列查单。

## 典型回调结构

```json
{
  "type": "payment_data",
  "data": {
    "transStat": "1",
    "huifuId": "6666000109133323",
    "reqSeqId": "1753150933645",
    "reqDate": "20250722",
    "respDesc": "操作成功"
  }
}
```

## 前端该怎么处理

| 场景 | 前端动作 | 是否能直接改订单终态 |
|------|----------|----------------------|
| SDK 初始化失败 | 提示用户并阻断支付入口 | 否 |
| 支付方式不支持 / 拉起失败 | 提示错误，可允许重试 | 否 |
| 收到 `payment_data` | 记录 `reqSeqId` / `reqDate`，通知后端确认 | 否 |
| 用户关闭页面 / 主动取消 | 只更新页面提示 | 否 |

## 推荐确认链路

```text
前端收到 callback
  -> 把 reqSeqId / reqDate 发给自有服务端
  -> 服务端调用 cashier-query
  -> 或者等待 notify_url / Webhook 异步通知
  -> 服务端确认成功后再更新业务订单
```

## 推荐前端代码形态

```js
async function callback(result) {
  if (result?.type !== "payment_data") return;

  const payload = {
    req_seq_id: result.data?.reqSeqId,
    req_date: result.data?.reqDate,
  };

  await fetch("/api/orders/confirm", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}
```

## 服务端确认入口

- 订单查询： `references/hostingpay-query.md`
- 异步通知： `references/hostingpay-async-webhook.md`

## 不要这样做

- 不要在前端看到“操作成功”就直接把业务订单改成已支付。
- 不要把 `callback_url` 页面跳转当成支付成功通知。
- 不要只信前端，不落库 `reqSeqId` / `reqDate`。
- 不要前端直接请求汇付查询接口。

## 推荐落库字段

前端至少要把下面两项交给后端：
- `reqSeqId`
- `reqDate`

如果你自己的页面上下文里已经有业务订单号，也一起带给后端，方便做幂等绑定。
