# 托管支付预下单

这份文档覆盖 H5/PC、支付宝小程序、微信小程序和抖音直连四类托管预下单场景。

## 什么时候读这里

- 已完成托管支付初始化
- 现在要创建托管支付订单
- 需要确定 `pre_order_type` 和预下单返回字段

## 预下单主流程

```text
准备 project_id / notify_url / callback_url
  -> 选择 pre_order_type
  -> 调用 v2/trade/hosting/payment/preorder
  -> 保存 pre_order_id / req_seq_id / req_date
  -> 前端跳转或接入 checkout-js
  -> 回到 hostingpay-async-webhook + hostingpay-query 做服务端最终确认闭环
```

## pre_order_type 对照

| 场景 | pre_order_type |
| --- | --- |
| H5 / PC | `1` |
| 支付宝小程序 | `2` |
| 微信小程序 | `3` |
| 抖音直连 | `4` |

## 关键前置条件

| 场景 | 必须提前准备 |
| --- | --- |
| H5 / PC | 控台托管项目、`project_id`、支付方式配置 |
| 支付宝小程序 | 托管支付权限、费率和 `app_data` / `alipay_data` |
| 微信小程序 | 托管授权、应用 ID、`miniapp_data.seq_id` |
| 抖音直连 | 抖音开放平台应用、`dy_data.sub_appid`、`busi_scene` 和真实客户端 IP |
| 全场景 | 合规的 `notify_url` 和真实 `callback_url` |

## 通用请求字段

| 字段 | 说明 |
| --- | --- |
| `huifu_id` | 商户号 |
| `req_date` | 请求日期 |
| `req_seq_id` | 请求流水号 |
| `pre_order_type` | 场景类型 |
| `trans_amt` | 交易金额 |
| `goods_desc` | 商品描述 |
| `notify_url` | 异步通知地址 |
| `fee_split_flag` | 是否交易手续费分摊，新版托管预下单字段，`Y`=分摊、`N`=不分摊 |

## 请求头强制约束

- `v2/trade/hosting/payment/preorder` 必须带 `jpt-x-skill-source: <skill_source>`
- 如果当前按 PHP 接入，且请求 `data` 中存在 `huifu_id`，还必须带 `jpt-x-skill-huifu_id: <data.huifu_id>`
- 当前 Skill 包对齐的官方 PHP SDK 主链路在 `MerConfig.skill_source` 已配置时，会自动带 `jpt-x-skill-source`，并在当前请求 `huifu_id` 存在且非空时自动带 `jpt-x-skill-huifu_id`
- 当前 Java SDK 基线也会在请求 `data` 中存在 `huifu_id` 且非空时自动带 `jpt-x-skill-huifu_id: <data.huifu_id>`
- 这两项属于 HTTP 请求头，不属于业务报文 `data`；完整口径以 `references/shared-request-header-policy.md` 为准

## 通用返回字段

| 字段 | 说明 |
| --- | --- |
| `resp_code` | 受理结果 |
| `req_seq_id` | 请求流水号 |
| `req_date` | 请求日期 |
| `pre_order_id` | 预下单标识 |
| `jump_url` | 跳转收银台或拉起支付地址 |

## 协作边界

- 如果前端要自己渲染支付入口，下一步读 `references/checkout-js.md`
- 如果是抖音直连下单，下一步读 `references/hostingpay-preorder-douyin-direct.md`
- 页面回跳只代表前端流程结束，不代表订单最终成功
- 最终状态必须回到服务端闭环：异步通知验签/幂等 + `references/hostingpay-query.md` 查单二次确认或补偿查询

## PHP 路径

托管支付 PHP 支持预下单，默认入口先读：

- `references/hostingpay-php-adapter.md`
- `references/hostingpay-preorder-php-scenarios.md`

如果只是核对补头或签名口径，读取 `references/shared-request-header-policy.md` 与 `references/shared-signing-v2.md`

## 下一步

- 前端嵌入收银台：读 `references/checkout-js.md`
- 服务端最终确认闭环：读 `references/hostingpay-async-webhook.md` 和 `references/hostingpay-query.md`
