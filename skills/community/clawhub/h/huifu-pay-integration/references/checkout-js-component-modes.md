# `checkout` 组件与单支付按钮模式

> 这份文档只讲组件选择：什么时候用 `checkout`，什么时候用 `alipay` / `wechatpay` / `unionpay` 单按钮，以及它们对 `createPreOrder` 的共同要求。

## 组件模式总览

| 模式 | 组件名 | 适合场景 |
|------|--------|----------|
| 完整收银台 | `checkout` | 一个区域展示多种支付方式，让用户自己选 |
| 支付宝单按钮 | `alipay` | 页面只需要支付宝入口 |
| 微信单按钮 | `wechatpay` | 页面只需要微信入口 |
| 云闪付单按钮 | `unionpay` | 页面只需要云闪付入口 |

## 共同参数

所有模式都依赖同一组核心参数：

```js
const element = hfPay.component("checkout", {
  createPreOrder,
  callback,
});
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `createPreOrder` | Function | 前端调用自有服务端创建预下单 |
| `callback` | Function | 接收支付过程事件，驱动页面提示 |

## `checkout` 模式

适合：
- 商户想在一个容器里统一承载支付方式选择
- 页面希望保留“选择支付方式 -> 发起支付”的完整收银台体验

示例：

```js
const checkout = hfPay.component("checkout", {
  createPreOrder,
  callback,
});

checkout?.mount("#checkout-container");
```

## 单支付按钮模式

适合：
- 商户自己决定页面布局
- 某个区域只展示一个支付入口
- 需要把不同支付按钮插到不同位置

示例：

```js
const wechatButton = hfPay.component("wechatpay", {
  createPreOrder,
  callback,
});

wechatButton?.mount("#wechat-button");
```

## 环境展示规则

根据当前公开资料：
- 支付宝内只展示支付宝
- 微信内只展示微信
- 云闪付内只展示云闪付
- 系统浏览器默认展示支付宝与微信

参考：
- `references/shared-frontend-sdk-matrix.md`

## 选择建议

| 你的诉求 | 推荐模式 |
|----------|----------|
| 想最快接好一个完整支付区域 | `checkout` |
| 想自己控制布局，只嵌一个按钮 | 单按钮 |
| 同页不同区域放不同支付入口 | 单按钮 |
| 需要同时展示多种支付方式并允许用户切换 | `checkout` |

## 注意事项

- 不管是 `checkout` 还是单按钮，最终都还是走同一条主链路：`createPreOrder -> HFPay -> callback -> 服务端确认`。
- 组件模式影响的是页面呈现，不改变服务端必须预下单、必须查单的基本事实。
- 不要为了“兼容所有场景”在一个页面同时无约束地挂多个支付方式组件，先根据业务流和环境做收敛。
