# 前端收银台接入主链路

> 这份文档只回答一个问题：`references/checkout-js.md` 在真实项目里应该怎么串起前端页面、服务端预下单、JS SDK 与最终状态确认。最终确认必须同时列出 `hostingpay-query.md` 和 `hostingpay-async-webhook.md`，不能只列查单。

## 主链路

```text
商户页面
  -> 调用自有服务端 createPreOrder 接口
  -> 服务端调用托管支付预下单接口
  -> 服务端返回 pre_order_id / req_seq_id / req_date / huifu_id
  -> 前端把结果交给 HFPay checkout 或单支付按钮
  -> 前端收到 callback
  -> 服务端验签异步通知、做幂等和状态锁，并通过查单二次确认/补偿查询
```

## 职责边界

| 环节 | 前端负责什么 | 服务端负责什么 |
|------|-------------|---------------|
| 页面初始化 | 渲染订单、金额、支付区域 | 返回业务订单详情 |
| 创建预下单 | 调用自有 `/api/hostingpay/preorder` | 调汇付预下单、落库请求标识 |
| 发起支付 | 调用 `HFPay()`、挂载 `checkout` / 按钮组件 | 不参与页面渲染 |
| 接收前端回调 | 更新页面提示、触发后端确认 | 不能仅靠前端回调认定成功 |
| 最终状态确认 | 展示查询结果 | 异步通知验签和幂等后，结合查单二次确认/补偿查询更新订单 |

## 推荐阅读顺序

1. 先看 `references/hostingpay-customer-preparation.md` 确认 `project_id`、`callback_url`、支付方式开通状态等来源。
2. 再看 `references/hostingpay-preorder-h5-pc-request.md` 明确服务端预下单字段。
3. 再读 `references/checkout-js.md` 落 `HFPay`、`createPreOrder` 与组件挂载。
4. 支付后同时看 `references/hostingpay-query.md` 与 `references/hostingpay-async-webhook.md` 做最终确认闭环。

## 接入前必须先确认

- 你自己的服务端已经能创建真实预下单，不是前端临时拼假数据。
- `project_id` 是控台真实创建的托管项目号。
- `callback_url` 只是支付完成后的前端回跳地址，不是支付成功依据。
- 最终状态依赖服务端闭环确认，而不是前端 callback；异步通知也要结合查单二次确认或补偿查询。

## 最小页面协作模型

```js
const { error, hfPay } = await HFPay();
if (error) throw error;

const checkout = hfPay.component("checkout", {
  createPreOrder,
  callback,
});

checkout?.mount("#checkout-container");
```

```js
async function callback(result) {
  if (result?.type !== "payment_data") return;

  await fetch("/api/orders/confirm", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      req_seq_id: result.data?.reqSeqId,
      req_date: result.data?.reqDate,
    }),
  });
}
```

## 常见误解

- 误解：checkout-js 可以替代服务端预下单。
  - 不是。前端只能调用你自己的服务端接口获取预下单结果。
- 误解：前端 callback 成功就能把订单标成已支付。
  - 不是。仍要服务端查单或等异步通知。
- 误解：`callback_url` 就是异步通知地址。
  - 不是。`callback_url` 是页面跳转，`notify_url` 是服务端异步回调地址。
