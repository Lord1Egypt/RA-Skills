# 拆单支付订单查询

> 官方接口更新时间：`2025.12.30`。来源页：`https://paas.huifu.com/partners/api/doc/cpjs/api_cpjs_hostingcdzf.md`。
> 本接口只用于拆单支付订单查询，不等同于普通托管交易查询 `v2/trade/hosting/payment/queryorderinfo`。

## 目录

- 什么时候读这里
- 接口概览
- SDK 兼容性
- 公共请求参数
- 请求参数 data
- 同步返回参数
- trans_list
- wx_response
- alipay_response
- 实现备注

## 什么时候读这里

- 用户明确说拆单支付、拆单订单查询、`splitpay/query` 或微信小程序拆单支付查询
- 已通过托管微信小程序预下单的 `split_pay_flag=Y` 发起拆单支付，需要查询拆单明细
- 普通托管查单只能给订单级状态，不足以返回拆单支付列表

## 接口概览

| 属性 | 值 |
| --- | --- |
| 请求方式 | `POST` |
| 汇付 API 端点 | `https://api.huifu.com/v2/trade/hosting/payment/splitpay/query` |
| 场景 | 拆单支付订单查询 |
| SDK Request 类 | Java / PHP / Python：`V2TradeHostingPaymentSplitpayQueryRequest` |
| 报文格式 | `application/json` |

## SDK 兼容性

| 语言 | 当前核对结果 | 输出规则 |
| --- | --- | --- |
| Java | 官方源码存在 `V2TradeHostingPaymentSplitpayQueryRequest` | 可生成官方 request 类代码，字段为 `req_date`、`req_seq_id`、`huifu_id`、`org_req_date`、`org_req_seq_id` |
| PHP | 官方源码存在 `V2TradeHostingPaymentSplitpayQueryRequest` | 可生成官方 request 类代码或 `BsPayClient::postRequest()` 代码 |
| Python | 官方源码存在 `V2TradeHostingPaymentSplitpayQueryRequest` 和 `V2_TRADE_HOSTING_PAYMENT_SPLITPAY_QUERY` URL 常量 | 可生成官方 request 类代码；属性名为 `req_date`、`req_seq_id`、`huifu_id`、`org_req_date`、`org_req_seq_id` |

## 公共请求参数

| 参数 | 中文名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `sys_id` | 系统号 | String | Y | 渠道商或直连商户的 `huifu_id` |
| `product_id` | 产品号 | String | Y | 汇付分配的产品号 |
| `sign` | 加签结果 | String | Y | 对整个报文签名 |
| `data` | 请求数据 | JSON | Y | 业务请求参数 |

> 请求头强制约束同托管支付：必须带 `jpt-x-skill-source`；当 `data.huifu_id` 存在且非空时，按语言 SDK 能力补 `jpt-x-skill-huifu_id`。详见 `references/shared-request-header-policy.md`。

## 请求参数 data

| 参数 | 中文名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `req_date` | 请求日期 | String | Y | 本次查询请求日期，`yyyyMMdd` |
| `req_seq_id` | 请求流水号 | String | Y | 本次查询请求流水号，同一 `huifu_id` 下当天唯一 |
| `huifu_id` | 商户号 | String | Y | 商户开户生成 |
| `org_req_date` | 原交易请求日期 | String | Y | 原拆单支付交易请求日期 |
| `org_req_seq_id` | 原交易请求流水号 | String | Y | 原拆单支付交易请求流水号 |

## 同步返回参数

| 参数 | 中文名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `resp_code` | 业务响应码 | String | Y | 查询受理返回码 |
| `resp_desc` | 业务响应信息 | String | Y | 业务返回描述 |
| `huifu_id` | 商户号 | String | Y | 商户号 |
| `req_date` | 请求日期 | String | Y | 本次查询请求日期 |
| `req_seq_id` | 请求流水号 | String | Y | 本次查询请求流水号 |
| `org_req_date` | 原交易请求日期 | String | Y | 原交易请求日期 |
| `org_req_seq_id` | 原交易请求流水号 | String | N | 原交易请求流水号 |
| `pre_order_id` | 预下单订单号 | String | Y | 托管预下单订单号 |
| `order_stat` | 预下单状态 | String | N | `1` 支付成功，`2` 支付中，`3` 已退款，`4` 处理中，`5` 支付失败，`6` 部分退款 |
| `trans_list` | 拆单支付列表 | String(JSON Array) | N | 拆单明细列表 |

## trans_list

| 参数 | 中文名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `pay_type` | 交易类型 | String | N | 如 `T_MINIAPP`、`A_NATIVE`、`A_JSAPI` |
| `org_hf_seq_id` | 原机构请求流水号 | String | N | 拆单子交易平台流水 |
| `trans_amt` | 交易金额 | String | N | 单位元 |
| `party_order_id` | 用户账单商户订单号 | String | N | 用户账单展示用 |
| `fee_amt` | 手续费金额 | String | N | 单位元 |
| `ref_amt` | 可退金额 | String | N | 单位元 |
| `trans_stat` | 交易状态 | String | N | `P` 处理中，`S` 成功，`F` 失败，`I` 初始 |
| `trans_time` | 交易时间 | String | N | `yyyyMMddHHmmss` |
| `bank_code` | 外部通道返回码 | String | N | 通道返回码 |
| `bank_desc` | 外部通道返回描述 | String | N | 通道返回描述 |
| `wx_response` | 微信响应报文 | String(JSON Object) | N | 微信拆单明细扩展 |
| `alipay_response` | 支付宝响应报文 | String(JSON Object) | N | 支付宝拆单明细扩展 |

## wx_response

| 参数 | 中文名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `wx_user_id` | 微信用户唯一标识码 | String | N | 微信用户唯一标识 |
| `sub_appid` | 子商户公众账号 ID | String | N | 微信子商户公众账号 ID |
| `openid` | 用户标识 | String | Y | 用户在商户 appid 下的唯一标识 |
| `sub_openid` | 子商户用户标识 | String | N | 用户在子商户 appid 下的唯一标识 |
| `bank_type` | 付款银行 | String | Y | 银行类型标识 |
| `cash_fee` | 现金支付金额 | Int | N | 订单现金支付金额 |
| `coupon_fee` | 代金券金额 | Int | N | 代金券或立减优惠金额 |
| `attach` | 商家数据包 | String | N | 原样返回 |
| `promotion_detail` | 营销详情列表 | Array | N | 微信营销详情 |

### wx_response.promotion_detail[]

| 参数 | 中文名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `promotion_id` | 优惠 ID | String | Y | 券或立减优惠 ID |
| `name` | 优惠名称 | String | N | 优惠名称 |
| `scope` | 优惠范围 | String | N | `GLOBAL` 或 `SINGLE` |
| `type` | 优惠类型 | String | N | `COUPON` 或 `DISCOUNT` |
| `amount` | 优惠券面额 | String | Y | 单位元 |
| `activity_id` | 活动 ID | String | Y | 微信批次 ID |
| `merchant_contribute` | 商户出资 | String | N | 单位元 |
| `other_contribute` | 其他出资 | String | N | 单位元 |
| `goods_detail` | 单品列表 | Object | N | 单品优惠信息 |

### wx_response.promotion_detail[].goods_detail

| 参数 | 中文名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `goods_id` | 商品编码 | String | Y | 商品编码 |
| `goods_remark` | 商品备注 | String | N | 原样返回 |
| `discount_amount` | 商品优惠金额 | String | Y | 单品优惠金额 |
| `quantity` | 商品数量 | String | Y | 购买数量 |
| `price` | 商品价格 | String | Y | 优惠后的单价 |

## alipay_response

| 参数 | 中文名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `voucher_detail_list` | 优惠券信息 | Array | N | 支付宝优惠券信息 |
| `fund_bill_list` | 支付金额信息 | Object | N | 支付成功的各渠道金额信息 |
| `buyer_id` | 买家支付宝用户号 | String | N | 2088 开头用户号 |
| `buyer_logon_id` | 买家支付宝账号 | String | N | 买家账号 |
| `hb_fq_num` | 花呗分期数 | String | N | 花呗分期数 |
| `hb_fq_seller_percent` | 卖家承担手续费 | String | N | 手续费百分比 |

### alipay_response.voucher_detail_list[]

| 参数 | 中文名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | 券 ID | String | Y | 优惠券 ID |
| `name` | 券名称 | String | Y | 优惠券名称 |
| `type` | 券类型 | String | Y | 如 `ALIPAY_FIX_VOUCHER`、`ALIPAY_DISCOUNT_VOUCHER`、`ALIPAY_ITEM_VOUCHER` |
| `amount` | 优惠券面额 | String | Y | 单位元 |
| `merchant_contribute` | 商家出资 | String | N | 单位元 |
| `other_contribute` | 其他出资 | String | N | 单位元 |

## 实现备注

- 查询定位键是原拆单支付的 `org_req_date + org_req_seq_id`，不要用退款请求流水或普通托管查单的 `party_order_id` 替代。
- `order_stat` 是订单级状态；拆单子交易状态要逐条读取 `trans_list[].trans_stat`。
- `trans_stat=I` 属于异常初始态，官方口径提示需联系汇付技术人员处理。
- 拆单支付查询没有独立异步通知；最终状态仍要结合支付异步通知、幂等和主动查询闭环。
- SDK 说明必须按最新源码说明 Java/PHP/Python 均已有 `V2TradeHostingPaymentSplitpayQueryRequest`；不要再提示 Python 需要裸端点或通用方法兜底。
