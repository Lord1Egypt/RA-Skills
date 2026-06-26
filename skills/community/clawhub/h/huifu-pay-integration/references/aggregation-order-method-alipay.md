# 聚合下单渠道分册：支付宝


## 目录

- 适用交易类型
- `method_expand` 对象边界
- 官方接入前准备
- `A_JSAPI` / `A_NATIVE` 请求字段
- `A_MICROPAY` 请求字段
- 支付宝共用子结构
- 同步返回支付宝扩展
- 异步 `alipay_response`
- 支付宝实现备注

## 适用交易类型

| `trade_type` | 场景 |
|--------------|------|
| `A_JSAPI` | 支付宝 JS 支付 |
| `A_NATIVE` | 支付宝正扫 |
| `A_MICROPAY` | 支付宝付款码反扫 |

## `method_expand` 对象边界

- `trade_type` 负责选择支付宝场景。
- `method_expand` 的 JSON 内容直接就是支付宝对象本身。
- 不要再写成带 `A_JSAPI`、`A_MICROPAY` 等场景 key 的包装结构。

## 官方接入前准备

- 官方开发指引要求先完成商户进件并开通支付宝业务。
- `A_JSAPI` 场景下，`buyer_id` 对应支付宝 `user_id`，必须通过支付宝官方获取链路获得。
- 用户前端页面收到支付完成回调后，后端仍需调用查询订单 API 确认最终状态。

## `A_JSAPI` / `A_NATIVE` 请求字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `alipay_store_id` | String | N | 支付宝店铺编号 |
| `buyer_id` | String | N | 买家支付宝唯一用户号；`A_JSAPI` 与 `buyer_logon_id` 二选一 |
| `buyer_logon_id` | String | N | 买家支付宝账号；`A_JSAPI` 与 `buyer_id` 二选一 |
| `goods_detail` | Array | N | 订单商品列表 |
| `extend_params` | Object | N | 业务扩展参数 |
| `ali_promo_params` | String | N | 优惠明细参数 |
| `seller_id` | String | N | 卖家支付宝用户号 |
| `merchant_order_no` | String | N | 商户原始订单号 |
| `operator_id` | String | N | 商户操作员编号 |
| `product_code` | String | N | 销售产品码 |
| `ext_user_info` | Object | N | 外部指定买家 |
| `subject` | String | N | 直连模式必填 |
| `store_name` | String | N | 商家门店名称 |
| `op_app_id` | String | N | 小程序应用 appid |
| `ali_business_params` | String | N | 商户业务信息 |
| `body` | String | N | 订单描述 |

## `A_MICROPAY` 请求字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `auth_code` | String | Y | 用户付款码 |
| `alipay_store_id` | String | N | 支付宝店铺编号 |
| `goods_detail` | Array | N | 订单商品列表 |
| `extend_params` | Object | N | 业务扩展参数 |
| `ali_business_params` | String | N | 商户业务信息 |
| `operator_id` | String | N | 商户操作员编号 |
| `store_id` | String | N | 商户门店编号 |
| `ext_user_info` | Object | N | 外部指定买家 |
| `body` | String | N | 订单描述 |
| `ali_promo_params` | String | N | 优惠明细参数 |

## 支付宝共用子结构

### `goods_detail[]`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `goods_id` | String | Y | 商品编号 |
| `goods_name` | String | Y | 商品名称 |
| `price` | String | Y | 商品单价 |
| `quantity` | String | Y | 商品数量 |
| `body` | String | N | 商品描述信息 |
| `categories_tree` | String | N | 商品类目树 |
| `show_url` | String | N | 商品展示地址 |
| `goods_category` | String | N | 商品类目 |

### `A_JSAPI` / `A_NATIVE` 的 `extend_params`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `card_type` | String | N | 卡类型 |
| `food_order_type` | String | N | 支付宝点餐场景类型 |
| `hb_fq_num` | String | N | 花呗分期数 |
| `hb_fq_seller_percent` | String | N | 花呗卖家手续费百分比 |
| `fq_channels` | String | N | 信用卡分期资产方式 |
| `parking_id` | String | N | 停车场 ID |
| `sys_service_provider_id` | String | N | 系统商编号 |

### `A_MICROPAY` 的 `extend_params`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `card_type` | String | N | 卡类型 |
| `food_order_type` | String | N | 支付宝点餐场景类型 |
| `hb_fq_num` | String | N | 花呗分期数 |
| `hb_fq_seller_percent` | String | N | 花呗卖家承担的手续费百分比 |
| `industry_reflux_info` | String | N | 行业数据回流信息 |
| `parking_id` | String | N | 停车场 ID |
| `sys_service_provider_id` | String | N | 系统商编号 |

### `ext_user_info`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | String | N | 姓名 |
| `mobile` | String | N | 手机号 |
| `cert_type` | String | N | 证件类型 |
| `cert_no` | String | N | 证件号，需按汇付加密说明加密 |
| `min_age` | String | N | 允许的最小买家年龄 |
| `fix_buyer` | String | N | 是否强制校验付款人身份信息 |
| `need_check_info` | String | N | 是否强制校验身份信息 |

## 同步返回支付宝扩展

同步返回的 `method_expand` 中，支付宝侧常见字段如下：

| 字段 | 说明 |
|------|------|
| `voucher_detail_list[]` | 优惠券信息 |
| `fund_bill_list[]` | 资金渠道 |
| `buyer_id` | 买家支付宝唯一用户号 |
| `buyer_logon_id` | 买家支付宝账号 |
| `hb_fq_num` | 花呗分期数 |
| `hb_fq_seller_percent` | 卖家承担手续费百分比 |

## 异步 `alipay_response`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `voucher_detail_list` | Array | N | 优惠券信息 |
| `fund_bill_list` | Array | N | 资金渠道 |
| `buyer_id` | String | N | 买家的支付宝唯一用户号 |
| `buyer_logon_id` | String | N | 买家支付宝账号 |
| `hb_fq_num` | String | N | 花呗分期数 |
| `hb_fq_seller_percent` | String | N | 卖家承担的手续费百分比 |
| `notify_time` | String | N | 通知时间 |
| `app_id` | String | N | 支付宝应用 `app_id` |
| `out_biz_no` | String | N | 商户业务号 |
| `invoice_amount` | String | N | 开票金额 |
| `buyer_pay_amount` | String | N | 付款金额 |
| `subject` | String | N | 订单标题 |
| `body` | String | N | 商品描述 |
| `gmt_create` | String | N | 交易创建时间 |

### `voucher_detail_list[]`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | String | Y | 券 ID |
| `name` | String | Y | 券名称 |
| `type` | String | Y | 券类型 |
| `amount` | String | Y | 优惠券面额 |
| `merchant_contribute` | String | N | 商家出资 |
| `other_contribute` | String | N | 其他出资方出资金额 |

### `fund_bill_list[]`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `bank_code` | String | N | 银行代码 |
| `amount` | String | N | 渠道使用金额 |
| `fund_channel` | String | N | 交易使用的资金渠道 |
| `fund_type` | String | N | 资金类型 |
| `real_amount` | String | N | 渠道实际付款金额 |

## 支付宝实现备注

- `A_JSAPI` 场景下，`buyer_id` 与 `buyer_logon_id` 二选一必填。
- `buyer_id` 不是示例值字段，必须来自真实用户授权结果。
- `subject` 在直连模式中属于关键字段，不要遗漏。
- `fq_channels` 是 `A_JSAPI / A_NATIVE.extend_params` 的字段，不属于 `A_MICROPAY.extend_params`。
- `industry_reflux_info` 是 `A_MICROPAY.extend_params` 的官方字段，不要错塞到 `A_JSAPI / A_NATIVE`。
- 官方参数表中曾把 `body` 与重复的 `ali_promo_params` 拼到同一行；实现时应把它们视为两个独立字段。
- `A_MICROPAY.auth_code` 必须来自扫码设备实时采集。
