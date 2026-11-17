# `createPreOrder` 契约与返回格式

> 这份文档聚焦前端最容易接错的一层：`createPreOrder` 到底应该接收什么、返回什么、哪些字段是前端必须从服务端拿到的。

## 目录

- 方法定位
- 方法签名建议
- 入参语义
- 必须返回的字段
- 推荐请求体结构
- `pre_order_type` 决策规则
- 与服务端的边界
- 常见错误

## 方法定位

`createPreOrder` 由商户前端实现，再传给 JS SDK。

JS SDK 只负责：
- 在需要发起支付时调用它
- 消费它返回的预下单结果

JS SDK 不负责：
- 直接请求汇付网关
- 帮你生成 `pre_order_id`
- 帮你决定服务端该走哪一种托管预下单报文

## 方法签名建议

```js
async function createPreOrder(selectedType) {
  const response = await fetch("/api/hostingpay/preorder", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ selected_type: selectedType }),
  });
  if (!response.ok) throw new Error("create preorder failed");

  return await response.json();
}
```

## 入参语义

| 入参 | 类型 | 说明 |
|------|------|------|
| `selectedType` | String | 用户当前选择的支付方式；常见值为 `checkout`、`alipay`、`wechatpay`、`unionpay` |

## 必须返回的字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `pre_order_id` | String | 服务端真实预下单结果 |
| `req_seq_id` | String | 预下单请求流水号 |
| `huifu_id` | String | 商户号 |
| `req_date` | String | 预下单请求日期 |

最小返回示例：

```json
{
  "pre_order_id": "P202604080001",
  "req_seq_id": "202604081530001234",
  "huifu_id": "6666000109133323",
  "req_date": "20260408"
}
```

## 推荐请求体结构

前端发给自有服务端的 body，建议至少包含：

```json
{
  "trans_amt": "88.00",
  "goods_desc": "会员充值",
  "pre_order_type": "1",
  "hosting_data": {
    "project_id": "PROJECTID2023092518673961",
    "project_title": "演示项目",
    "callback_url": "https://merchant.example.com/pay/result"
  }
}
```

## `pre_order_type` 决策规则

| 条件 | 推荐值 | 说明 |
|------|--------|------|
| 支付 App 内环境 | `1` | 一般走 H5 / PC 预下单链路 |
| 系统浏览器且用户选支付宝 | `2` | 走支付宝托管小程序 |
| 系统浏览器且用户选微信 | `3` | 走微信托管小程序 |

> 最终口径以服务端托管预下单文档为准：前端只做选择，服务端必须同步切换对应报文结构。

## 与服务端的边界

前端提交给自有服务端时，可以传对象；
但服务端在调用托管支付 SDK / HTTP 接口时，仍要按服务端文档把 `hosting_data`、`biz_info` 等对象序列化成官方要求的 JSON 字符串。

参考：
- `references/hostingpay-preorder-h5-pc-request.md`
- `references/hostingpay-payload-construction.md`

## 常见错误

- 返回字段名写成 `preOrderId`、`reqSeqId` 之类驼峰，导致 SDK 取值失败。
- 直接把汇付完整网关响应原样返回给前端，但没有整理出 SDK 需要的 4 个字段。
- 前端本地拼一个假的 `pre_order_id`。
- `selectedType` 切换了，但传给服务端的 `pre_order_type` 没变。
- 把 `callback_url`、`notify_url` 混为一谈。
