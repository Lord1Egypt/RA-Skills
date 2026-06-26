# 前端收银台 JS SDK

这份文档只负责商户前端页面里的 checkout 组件和单支付按钮接入。

## 什么时候读这里

- 服务端已经能完成托管预下单
- 现在要在 H5 / PC 页面嵌入收银台或单支付按钮
- 需要确定 `createPreOrder` 契约、组件模式和回调边界

## 当前版本口径

| 项目 | 当前值 |
| --- | --- |
| npm 包 | `@dg-elements/js-sdk` |
| 版本策略 | 以项目锁定版本为准；升级前查询 npm registry |
| 初始化对象 | `HFPay` |

## 前后端协作链路

```text
hostingpay-preorder
  -> checkout-js
  -> shared-async-notify
  -> hostingpay-query
```

也就是说，前端 SDK 只能拉起支付流程，不能单独完成支付闭环。

## 前端负责什么

1. 调用自有服务端 `createPreOrder`
2. 初始化 `HFPay`
3. 渲染 `checkout` 或单支付按钮
4. 接收前端 `callback`

## 前端不负责什么

- 不持有商户私钥
- 不直接请求汇付签名网关
- 不判定最终支付成功

## 安装方式

```bash
npm install @dg-elements/js-sdk
```

## `createPreOrder` 返回契约

前端回调自有服务端预下单接口后，至少要返回：

```json
{
  "pre_order_id": "P202604080001",
  "req_seq_id": "202604081530001234",
  "huifu_id": "6666000109133323",
  "req_date": "20260408"
}
```

## 常见组件模式

| 模式 | 适合场景 |
| --- | --- |
| `checkout` | 一个区域里展示多种支付方式 |
| `alipay` | 只展示支付宝按钮 |
| `wechatpay` | 只展示微信按钮 |
| `unionpay` | 只展示云闪付按钮 |

## 环境展示规则

- 支付宝内：只展示支付宝
- 微信内：只展示微信
- 云闪付内：只展示云闪付
- 系统浏览器：默认展示支付宝和微信

## 关键边界

- 前端 `callback` 只代表前端流程结束，不代表最终支付成功
- 最终订单状态必须由服务端闭环确认：异步通知需验签、幂等和状态锁，必要时通过托管查单二次确认或补偿查询
- `project_id`、`callback_url` 等值必须来自真实项目配置，不要让模型猜

## 下一步

- 服务端预下单能力：读 `references/hostingpay-preorder.md`
- 支付完成后的最终确认闭环：读 `references/hostingpay-async-webhook.md` 和 `references/hostingpay-query.md`
