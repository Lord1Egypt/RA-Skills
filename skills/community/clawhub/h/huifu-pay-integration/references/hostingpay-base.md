# 托管支付基础

这份文档负责托管支付的初始化、公共配置、请求头约束和语言边界。

## 什么时候读这里

- 第一次接托管支付
- 需要初始化 `dg-java-sdk` 或官方 PHP SDK
- 需要确认请求头、公共参数和项目参数准备方式

## 当前版本口径

| 项目 | 当前值 |
| --- | --- |
| Java SDK 常量版本 | `dg-java-sdk 3.0.38` |
| PHP 路径 | 托管支付核心场景已覆盖 |
| `HUIFU_SKILL_SOURCE` 最终值 | `<skill_source>` |

## 必备环境变量

| 环境变量 | 用途 |
| --- | --- |
| `HUIFU_PRODUCT_ID` | 汇付产品号 |
| `HUIFU_SYS_ID` | 当前商户 / 渠道 `huifu_id` |
| `HUIFU_RSA_PRIVATE_KEY` | 请求签名私钥 |
| `HUIFU_RSA_PUBLIC_KEY` | 响应验签公钥 |
| `HUIFU_SKILL_SOURCE` | 可选来源前缀覆盖项 |

## 初始化前必须确认

1. 先读 `references/shared-signing-v2.md`
2. 先读 `references/shared-async-notify.md`
3. 先读 `references/shared-request-header-policy.md`
4. 确认 `project_id`、`notify_url`、`callback_url` 等值来自真实业务配置

## 托管支付主流程

```text
准备产品号、sys_id 和密钥
  -> 初始化 SDK 或 HTTP 客户端
  -> hostingpay-preorder 预下单
  -> hostingpay-query 查单 / 关单 / 对账
  -> hostingpay-refund 退款
  -> 如需商户自有页面，再接 checkout-js
```

## 语言边界

- Java 是托管支付完整基线
- PHP 已覆盖基础、预下单、查询 / 关单 / 对账、退款
- PHP 默认落地走官方 `huifurepo/dg-php-sdk`，入口先读 `references/hostingpay-php-adapter.md`
- 当前 Skill 包不再内置 PHP 模板资产；不要回到历史自维护 PHP client 方案

## 公共边界

- 私钥只能留在服务端
- 如果不是使用官方 Java SDK，必须手动对齐请求头
- `skill_source` 可以覆盖，但请求头层只透传 `<skill_source>`，不再在该字段内拼接 `sys_id`

## 下一步怎么走

- 预下单：读 `references/hostingpay-preorder.md`
- 查询 / 关单 / 对账：读 `references/hostingpay-query.md`
- 退款：读 `references/hostingpay-refund.md`
- 商户前端页面组件：读 `references/checkout-js.md`
