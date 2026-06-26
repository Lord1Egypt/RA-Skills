# 前端收银台补充资料

本文件汇总 `references/checkout-js.md` 的补充参考文档，重点补 checkout-js 最容易接错的几层边界，而不是重复主入口文档的整篇内容。

## 阅读地图

| 文件 | 解决什么问题 |
|------|-------------|
| `references/checkout-js-integration-flow.md` | 前端页面、服务端预下单、JS SDK、查单确认如何串成主链路 |
| `references/checkout-js-create-preorder-contract.md` | `createPreOrder` 的入参、返回字段、`pre_order_type` 决策与常见错误 |
| `references/checkout-js-component-modes.md` | `checkout` 与单支付按钮模式怎么选 |
| `references/checkout-js-callback-and-confirmation.md` | 前端 callback 为什么不能直接当成支付成功 |
| `references/checkout-js-framework-integration-notes.md` | React / Vue / 原生 JS 集成时的最小边界提示 |

## 推荐阅读顺序

1. 先看 `references/checkout-js-integration-flow.md`
2. 再看 `references/checkout-js-create-preorder-contract.md`
3. 根据页面形态看 `references/checkout-js-component-modes.md`
4. 支付结果处理看 `references/checkout-js-callback-and-confirmation.md`
5. 最后按技术栈看 `references/checkout-js-framework-integration-notes.md`

## 与其他 Skill 的关系

- 服务端预下单： `references/hostingpay-preorder.md`
- 服务端查单： `references/hostingpay-query.md`
- 托管支付公共规则： `references/hostingpay-base.md`
- 共享前端矩阵： `references/shared-frontend-sdk-matrix.md`
