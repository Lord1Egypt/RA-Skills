# 聚合下单渠道分册：微信

> 本页表格用于解释微信场景和易错父子关系，不是完整 DTO。所有字段类型、长度、Y/N/C 以 `payment-complete-field-catalog.md` 的“聚合支付下单”完整路径为准。


## 目录

- 适用交易类型
- `method_expand` 对象边界
- 官方接入前准备
- 微信公众号 / 小程序 / APP 请求字段
- 微信反扫 `T_MICROPAY` 请求字段
- 同步返回微信扩展
- 异步 `wx_response`
- 微信实现备注

## 适用交易类型

| `trade_type` | 场景 |
|--------------|------|
| `T_JSAPI` | 微信公众号支付 |
| `T_MINIAPP` | 微信小程序支付 |
| `T_APP` | 微信 APP 支付 |
| `T_MICROPAY` | 微信付款码反扫 |

## `method_expand` 对象边界

- `trade_type` 负责选择微信场景。
- `method_expand` 的 JSON 内容直接就是微信对象本身。
- 不要再写成带 `T_JSAPI`、`T_MINIAPP` 等场景 key 的包装结构。

## 官方接入前准备

- 微信公众号场景：先准备公众号、确认账户和微信业务已开通、配置支付授权目录；进件实施交给 `$huifu-merchant-onboarding`。
- 微信小程序场景：先准备小程序、确认账户和微信业务已开通、完成微信配置；进件实施交给 `$huifu-merchant-onboarding`。
- 官方开发指引明确要求：`sub_openid` 必须来自当前 `appid` / `sub_appid` 对应的真实授权或登录流程，不能跨应用复用。
- 用户前端页面收到支付完成回调后，后端仍需调用查询订单 API 确认最终状态。

## 微信公众号 / 小程序 / APP 请求字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `sub_appid` | String | N | 子商户应用 ID；走聚合正扫发货管理时需要传 |
| `sub_openid` | String | N | 子商户用户标识；公众号和小程序场景必填 |
| `attach` | String | N | 附加数据，原样返回 |
| `body` | String | N | 商品描述 |
| `detail` | Object | N | 商品详情 |
| `goods_tag` | String | N | 订单优惠标记 |

### `detail`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `cost_price` | String | N | 订单原价 |
| `receipt_id` | String | N | 商品小票 ID |
| `goods_detail` | Array | Y | 单品列表 |

### `detail.goods_detail[]`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `goods_id` | String | N | 商品编码 |
| `goods_name` | String | N | 商品名称 |
| `price` | String | N | 商品单价 |
| `quantity` | Integer | N | 商品数量 |
| `wxpay_goods_id` | String | N | 微信侧商品编码 |

## 微信反扫 `T_MICROPAY` 请求字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `auth_code` | String | Y | 用户付款码 |
| `sub_appid` | String | N | 子商户公众账号 ID |
| `device_info` | String | N | 设备号 |
| `goods_tag` | String | N | 订单优惠标记 |
| `attach` | String | N | 附加数据 |
| `detail` | Object | N | 商品详情，结构同上 |
| `scene_info` | Object | N | 场景信息 |
| `promotion_flag` | String | N | 单品优惠标识；为 `Y` 时 `detail` 必填 |
| `spbill_create_ip` | String | C | 直联模式必填 |
| `receipt` | String | N | 电子发票入口开放标识 |

### `T_MICROPAY` 的 `method_expand.scene_info.store_info`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | String | N | 门店 ID |
| `name` | String | N | 门店名称 |
| `area_code` | String | N | 行政区划码 |
| `address` | String | N | 门店详细地址 |

## 同步返回微信扩展

同步返回的 `method_expand` 中，微信侧常见字段如下：

| 字段 | 说明 |
|------|------|
| `sub_appid` | 子商户公众账号 ID |
| `openid` | 用户在商户 appid 下的唯一标识 |
| `sub_openid` | 用户在子商户 appid 下的唯一标识 |
| `bank_type` | 付款银行 |
| `cash_fee` | 现金支付金额 |
| `coupon_fee` | 代金券金额 |
| `attach` | 商家数据包 |
| `promotion_detail[]` | 营销详情列表 |
| `sub_mch_id` | 子商户号，直连模式返回 |
| `device_info` | 设备号，直连模式返回 |
| `is_subscribe` | 是否关注公众账号，直连模式返回 |
| `sub_is_subscribe` | 是否关注子公众账号，直连模式返回 |
| `fee_type` | 现金支付货币类型，直连模式返回 |
| `coupon_count` | 代金券使用数量，直连模式返回 |

## 异步 `wx_response`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `sub_appid` | String | N | 子商户公众账号 ID |
| `openid` | String | Y | 用户标识 |
| `sub_openid` | String | N | 子商户用户标识 |
| `bank_type` | String | Y | 付款银行 |
| `cash_fee` | String | N | 现金支付金额 |
| `coupon_fee` | String | N | 代金券金额 |
| `attach` | String | N | 商家数据包 |
| `promotion_detail` | Array | N | 营销详情列表 |
| `sub_mch_id` | String | N | 子商户号，直连模式返回 |
| `device_info` | String | N | 设备号，直连模式返回 |
| `is_subscribe` | String | N | 是否关注公众账号，直连模式返回 |
| `sub_is_subscribe` | String | N | 是否关注子公众账号，直连模式返回 |
| `fee_type` | String | N | 现金支付货币类型，直连模式返回 |
| `coupon_count` | String | N | 代金券使用数量，直连模式返回 |

### `promotion_detail[]`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `promotion_id` | String | Y | 券 ID |
| `name` | String | N | 优惠名称 |
| `scope` | String | N | `GLOBAL` 或 `SINGLE` |
| `type` | String | N | `COUPON` 或 `DISCOUNT` |
| `amount` | String | Y | 优惠券面额 |
| `activity_id` | String | Y | 活动 ID |
| `merchant_contribute` | String | N | 商户出资 |
| `other_contribute` | String | N | 其他出资 |
| `goods_detail` | Array | N | 单品列表 |
| `wxpay_contribute` | String | N | 微信出资 |
| `original_other_contribute` | String | N | 微信交易其他出资方出资金额 |

### `wx_response.promotion_detail[].goods_detail[]`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `goods_id` | String | Y | 商品编码 |
| `goods_remark` | String | N | 商品备注 |
| `discount_amount` | String | Y | 商品优惠金额 |
| `quantity` | String | Y | 商品数量 |
| `price` | String | Y | 商品价格 |

## 微信实现备注

- 公众号和小程序场景下，`sub_openid` 本质是支付所需关键参数。
- `sub_openid` 与 `sub_appid` 必须匹配；微信官方 QA 明确说明错配会直接导致下单失败。
- 走聚合正扫发货管理的商户，使用公众号 / 小程序支付时需要传 `sub_appid + sub_openid`。
- `promotion_flag=Y` 时，必须同时上传 `detail`。
- `spbill_create_ip` 是直联模式要求，不属于普通间联场景通用必填。
- `T_MICROPAY.auth_code` 必须来自扫码设备实时采集，且官方开发指引给出了 18 位数字规则。

## 2026-11-04接入指引复核

公众号、小程序和付款码开发指引的密钥配置入口已改为 `https://paas.huifu.com/docs/start/#/api_kfzn`。公众号示例的多重HTML转义恢复为JavaScript的 `=>`、`&&` 和 `<`，照搬时使用解码后的代码。小程序产品介绍仅标点/空格变化，未据此改变支付能力或请求字段。对应官方来源见本页所列指南和 `official-payment-page-lock.md`。
