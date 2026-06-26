## 目录

- [接口概述](#接口概述)
- [应用场景](#应用场景)
- [SDK 映射](#sdk-映射)
- [公共请求参数](#公共请求参数)
- [请求参数 data](#请求参数-data)
- [嵌套参数展开](#嵌套参数展开)
- [请求示例](#请求示例)
- [同步返回参数](#同步返回参数)
- [业务返回码](#业务返回码)
- [文档勘误与实现备注](#文档勘误与实现备注)

# 托管交易查询

> 本文依据 2026-05-27 官方文档整理，适用于 `v2/trade/hosting/payment/queryorderinfo`。

## 接口概述

| 属性 | 值 |
|------|-----|
| 请求方式 | `POST` |
| 汇付 API 端点 | `https://api.huifu.com/v2/trade/hosting/payment/queryorderinfo` |
| SDK Request 类 | `V2TradeHostingPaymentQueryorderinfoRequest` |
| Content-Type | `application/json;charset=UTF-8` |

说明：

- 支持 JSON 报文。
- 请求整体需要签名，验签规则见 `references/hostingpay-java-tech-spec.md`。
- 本接口为同步查询接口，没有独立异步通知。
- 文档中的 `String(JSON Object)` / `String(JSON Array)` 表示字段外层类型仍是 `String`，但值内容需要传 JSON 字符串。

## 应用场景

- 通过托管支付预下单接口发起的交易，都可以通过本接口查询支付结果。
- 适用于支付完成后的主动确认、异步回调后的二次确认、以及处理中订单的轮询查询。

## SDK 映射

`V2TradeHostingPaymentQueryorderinfoRequest` 的独立 setter 字段：

| 字段 | setter | 类型 | 必填 | 说明 |
|------|--------|------|------|------|
| reqDate | `setReqDate()` | String(8) | Y | 本次查询请求日期，`yyyyMMdd` |
| reqSeqId | `setReqSeqId()` | String(64) | Y | 本次查询请求流水号，同一 `huifu_id` 下当天唯一 |
| huifuId | `setHuifuId()` | String(32) | C | 商户号；不填时必填 `partyOrderId` |
| orgReqDate | `setOrgReqDate()` | String(8) | C | 原交易请求日期；不填时必填 `partyOrderId` |
| orgReqSeqId | `setOrgReqSeqId()` | String(64) | C | 原交易请求流水号；不填时必填 `partyOrderId` |
| partyOrderId | `setPartyOrderId()` | String(64) | C | 用户账单上的商户订单号；不填时必须提供 `huifuId + orgReqDate + orgReqSeqId` |

说明：

- 查询条件是二选一：`partyOrderId`，或者 `huifuId + orgReqDate + orgReqSeqId`。
- 该接口没有单独列出的扩展 setter，公共包装字段 `sys_id`、`product_id`、`sign` 由统一请求封装处理。

## 公共请求参数

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| sys_id | 系统号 | String | 32 | Y | 渠道商/商户的 `huifu_id`；渠道商主体传渠道商号，直连商户主体传商户号 |
| product_id | 产品号 | String | 32 | Y | 汇付分配的产品号 |
| sign | 加签结果 | String | 512 | Y | 对整个请求报文签名 |
| data | 请求数据 | JSON | - | Y | 业务请求参数 |

> 强制请求头约束：
> - 必须带 `jpt-x-skill-source: <skill_source>`
> - 如果当前按 PHP 接入，由于本页请求 `data` 明确包含 `huifu_id`，还必须带 `jpt-x-skill-huifu_id: <data.huifu_id>`
> - 当前 Skill 包对齐的官方 PHP SDK 主链路在 `MerConfig.skill_source` 已配置时，会自动带 `jpt-x-skill-source`，并在当前请求 `huifu_id` 存在且非空时自动带 `jpt-x-skill-huifu_id`
> - 当前 Java SDK 基线也会在请求 `data` 明确包含 `huifu_id` 时自动带 `jpt-x-skill-huifu_id: <data.huifu_id>`
> - 这两项属于 HTTP 请求头，不要误写进 `data`；完整口径见 `references/shared-request-header-policy.md`

## 请求参数 data

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| req_date | 请求日期 | String | 8 | Y | `yyyyMMdd` |
| req_seq_id | 请求流水号 | String | 64 | Y | 同一 `huifu_id` 下当天唯一 |
| huifu_id | 商户号 | String | 32 | C | 开户自动生成；不填时必填 `party_order_id` |
| org_req_date | 原交易请求日期 | String | 8 | C | `yyyyMMdd`；不填时必填 `party_order_id` |
| org_req_seq_id | 原交易请求流水号 | String | 64 | C | 不填时必填 `party_order_id` |
| party_order_id | 用户账单上的商户订单号 | String | 64 | C | 不填时必须提供 `huifu_id + org_req_date + org_req_seq_id` |

## 嵌套参数展开

### wx_response

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| sub_appid | 子商户公众账号 ID | String | 32 | N | 微信分配的子商户公众账号 ID |
| openid | 用户标识 | String | 128 | Y | 用户在商户 `appid` 下的唯一标识 |
| sub_openid | 子商户用户标识 | String | 128 | N | 用户在子商户 `appid` 下的唯一标识 |
| bank_type | 付款银行 | String | 16 | Y | 银行类型标识 |
| cash_fee | 现金支付金额 | Int | 100 | N | 订单现金支付金额 |
| coupon_fee | 代金券金额 | Int | 100 | N | 代金券或立减优惠金额 |
| attach | 商家数据包 | String | 128 | N | 原样返回 |
| promotion_detail | 营销详情列表 | Array | 6000 | N | 返回值为 JSON 数组 |

#### wx_response.promotion_detail[]

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| promotion_id | 券或者立减优惠 ID | String | 32 | Y | 优惠 ID |
| name | 优惠名称 | String | 64 | N | 优惠名称 |
| scope | 优惠范围 | String | 32 | N | `GLOBAL`=全场代金券，`SINGLE`=单品优惠 |
| type | 优惠类型 | String | 32 | N | `COUPON`=代金券，`DISCOUNT`=优惠券 |
| amount | 优惠券面额 | String | 5 | Y | 用户享受优惠金额 |
| activity_id | 活动 ID | String | 32 | Y | 微信商户后台配置的批次 ID |
| merchant_contribute | 商户出资 | String | 32 | N | 商户出资金额，单位元 |
| other_contribute | 其他出资 | String | 32 | N | 其他出资方出资金额，单位元 |
| goods_detail | 单品列表 | Object | 3000 | N | 使用 JSON 格式 |

#### wx_response.promotion_detail[].goods_detail

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| goods_id | 商品编码 | String | 32 | Y | 商品编码 |
| goods_remark | 商品备注 | String | 32 | N | 原样返回 |
| discount_amount | 商品优惠金额 | String | 32 | Y | 单位元 |
| quantity | 商品数量 | String | 32 | Y | 商品数量 |
| price | 商品价格 | String | 32 | Y | 单位元；商户如有优惠，应传优惠后的单价 |

### alipay_response

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| voucher_detail_list | 优惠券信息 | Array | - | N | 本交易支付时使用的所有优惠券信息 |
| fund_bill_list | 支付金额信息 | Object | 512 | N | 支付成功的各渠道金额信息，JSON 格式 |
| buyer_id | 买家的支付宝唯一用户号 | String | 28 | N | 2088 开头的纯数字 |
| buyer_logon_id | 买家支付宝账号 | String | 100 | N | 买家支付宝账号 |
| hb_fq_num | 花呗分期数 | String | 10 | N | 花呗分期数 |
| hb_fq_seller_percent | 卖家承担的手续费 | String | 3 | N | 卖家承担的手续费百分比 |

#### alipay_response.voucher_detail_list[]

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| id | 券 ID | String | 32 | Y | 优惠券 ID |
| name | 券名称 | String | 32 | Y | 优惠券名称 |
| type | 券类型 | String | 32 | Y | 当前文档列出 `ALIPAY_FIX_VOUCHER`、`ALIPAY_DISCOUNT_VOUCHER`、`ALIPAY_ITEM_VOUCHER` |
| amount | 优惠券面额 | String | 8 | Y | 单位元；通常等于商家出资加其他出资方出资 |
| merchant_contribute | 商家出资 | String | 8 | N | 发起交易商家出资金额 |
| other_contribute | 其他出资方出资金额 | String | 11 | N | 可能来自支付宝、品牌商或第三方 |

#### alipay_response.fund_bill_list

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| bank_code | 银行代码 | String | 10 | N | 银行卡支付时的银行代码 |

### unionpay_response

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| coupon_info | 银联优惠信息 | Object | - | N | 银联使用优惠活动时出现，JSON 格式 |

#### unionpay_response.coupon_info

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| addnInfo | 附加信息 | String | 100 | N | 内容自定义 |
| spnsr_id | 出资方 | String | 20 | Y | `00010000` 表示银联出资；未来可能增加其他出资方 |
| type | 项目类型 | String | 4 | Y | `DD01`=随机立减，`CP01`=抵金券 |
| offst_amt | 抵消交易金额 | String | 12 | Y | 不能为全 `0` |
| id | 项目编号 | String | 40 | N | 用于票券编号等，格式自定义 |
| desc | 项目简称 | String | 40 | N | 可用于展示、打单等 |

### dy_response

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| sub_appid | 子商户应用 ID | String | 32 | N | 抖音开放平台申请的应用 ID |
| openid | 用户标识 | String | 128 | Y | 用户在商户 `appid` 下的唯一标识 |
| sub_openid | 子商户用户标识 | String | 128 | N | 用户在子商户 `appid` 下的唯一标识 |
| bank_type | 付款银行 | String | 16 | Y | 银行类型标识 |
| promotion_detail | 营销详情列表 | String(JSON Array) | - | N | 返回值为 JSON 数组 |

#### dy_response.promotion_detail[]

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| coupon_id | 券 ID | String | 32 | N | 券或者立减优惠 ID |
| name | 优惠名称 | String | 64 | N | 优惠名称 |
| scope | 优惠范围 | String | 32 | N | `GLOBAL`=全场代金券，`SINGLE`=单品优惠 |
| type | 优惠类型 | String | 32 | N | `CASH`=充值型代金券，`NOCASH`=免充值型代金券 |
| amount | 优惠券面额 | String | 12 | Y | 单位元 |
| stock_id | 活动 ID | String | 32 | N | 活动 ID |
| douyinpay_contribute | 抖音出资 | String | 32 | N | 抖音出资金额，单位元 |
| merchant_contribute | 商户出资 | String | 32 | N | 商户出资金额，单位元 |
| other_contribute | 其他出资 | String | 32 | N | 其他出资金额，单位元 |
| currency | 优惠币种 | String | 32 | N | `CNY` 表示人民币 |
| goods_detail | 单品列表 | Array | - | N | 单品信息，使用 JSON 数组 |

#### dy_response.promotion_detail[].goods_detail[]

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| goods_id | 商品编码 | String | 32 | Y | 商品编码 |
| quantity | 商品数量 | String | 32 | Y | 商品数量 |
| unit_price | 商品单价 | String | 32 | N | 单位元 |
| discount_amount | 商品优惠金额 | String | 32 | Y | 单位元 |
| goods_remark | 商品备注 | String | 128 | N | 原样返回 |

### acct_split_bunch

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| acct_infos | 分账明细 | Array | 2048 | Y | 分账明细 |

#### acct_split_bunch.acct_infos[]

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| div_amt | 分账金额 | String | 14 | Y | 单位元，保留两位小数，最低 `0.01` |
| huifu_id | 分账接收方 ID | String | 32 | Y | 分账接收方 ID |
| acct_date | 账务日期 | String | 8 | N | `yyyyMMdd` |

### trans_fee_allowance_info

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| receivable_fee_amt | 商户应收手续费 | String | 16 | Y | 商户应收手续费 |
| actual_fee_amt | 商户实收手续费 | String | 16 | Y | 商户实收手续费 |
| allowance_fee_amt | 补贴手续费 | String | 16 | Y | 补贴手续费 |
| allowance_type | 补贴类型 | String | 10 | N | `0`=不补贴，`1`=补贴，`2`=部分补贴，`3`=全额补贴(优惠后)，`4`=部分补贴(优惠后) |
| no_allowance_desc | 不补贴原因 | String | 128 | N | 补贴系统返回的不补贴原因 |
| cur_allowance_config_infos | 手续费补贴活动详情 | Object | - | N | 补贴系统返回，斗拱原样返回 |

#### trans_fee_allowance_info.cur_allowance_config_infos

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| acct_id | 门店 | String | 64 | N | 门店标识 |
| merchant_group | 商户号 | String | 64 | N | 商户号 |
| allowance_sys | 补贴方 | String | 64 | Y | `1`=银行，`2`=服务商，`3`=汇来米 |
| allowance_sys_id | 补贴方 ID | String | 64 | Y | 补贴方 ID |
| is_delay_allowance | 补贴类型 | String | 2 | Y | `1`=实补，`2`=后补 |
| market_id | 自定义活动编号 | String | 64 | Y | 自定义活动编号 |
| market_name | 自定义活动名称 | String | 128 | N | 自定义活动名称 |
| market_desc | 自定义活动描述 | String | 64 | N | 自定义活动描述 |
| start_time | 活动开始时间 | String | 8 | Y | `yyyyMMdd` |
| end_time | 活动结束时间 | String | 8 | Y | `yyyyMMdd` |
| pos_debit_limit_amt | POS 借记卡补贴额度 | String | 16 | Y | 单位元 |
| pos_credit_limit_amt | POS 贷记卡补贴额度 | String | 16 | Y | 单位元 |
| pos_limit_amt | POS 补贴额度 | String | 16 | Y | 单位元 |
| qr_limit_amt | 扫码补贴额度 | String | 16 | Y | 单位元 |
| total_limit_amt | 活动总补贴额度 | String | 16 | Y | 单位元 |
| status | 活动是否有效 | String | 4 | Y | `1`=生效，`0`=失效 |
| human_flag | 是否人工操作 | String | 4 | Y | `N`=自动，`Y`=人工 |
| activity_id | 活动号 | String | 64 | Y | 活动号 |
| activity_name | 活动描述 | String | 128 | N | 活动描述 |
| create_by | 创建人 | String | 32 | Y | 创建人 |
| create_time | 创建时间 | String | 32 | Y | 创建时间 |
| update_time | 更新时间 | String | 32 | Y | 更新时间 |

### quick_online_response

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| debit_flag | 借贷记标识 | String | 1 | N | `D`=借记卡，`C`=信用卡，`Z`=借贷合一卡 |
| user_huifu_id | 用户号 | String | 32 | N | 汇付分配的用户号，快捷支付时才有值 |
| order_type | 订单类型 | String | 1 | N | `P`=支付，`R`=充值，默认 `P` |
| bank_id | 银行代号 | String | 8 | N | 银行代号 |

### bank_extend_param

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| gate_type | 网关支付类型 | String | 2 | N | `01`=个人网关，`02`=企业网关 |
| bank_id | 付款方银行号 | String | 32 | N | 付款方银行号 |
| pyer_acct_id | 付款方银行账户 | String | 1024 | N | B2B 支付成功后可能返回密文 |
| pyer_acct_nm | 付款方银行账户名 | String | 128 | N | 付款方银行账户名 |

### fee_formula_infos[]

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| fee_formula | 手续费计算公式 | String | 512 | Y | 手续费计算公式，如 `AMT*0.003` |
| fee_type | 手续费类型 | String | 32 | Y | `TRANS_FEE`=交易手续费，`ACCT_FEE`=组合支付账户补贴手续费 |
| huifu_id | 商户号 | String | 32 | N | 补贴支付账户补贴时，补贴账户的 `huifu_id` |
| fee_sign | 手续费场景标识 | String | 32 | N | 商户业务开通配置的手续费场景标识码 |

## 请求示例

```json
{
  "sys_id": "6666000123123123",
  "product_id": "SPIN",
  "data": {
    "huifu_id": "6666000109133323",
    "req_date": "20231020",
    "req_seq_id": "202310201652361987182513",
    "org_req_seq_id": "202310201652361987182512",
    "org_req_date": "20231020"
  },
  "sign": "<SDK_AUTOGENERATED_SIGNATURE>"
}
```

## 同步返回参数

### 公共返回参数

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| sign | 签名 | String | 512 | Y | 对响应整体签名 |
| data | 响应内容体 | JSON | - | N | 业务返回参数 |

### data

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| resp_code | 业务响应码 | String | 8 | Y | 查询接口受理返回码；仍需继续结合 `order_stat`、`trans_stat`、`close_stat` 解析订单状态 |
| resp_desc | 业务响应信息 | String | 512 | Y | 业务响应描述 |
| huifu_id | 商户号 | String | 32 | Y | 商户号 |
| req_date | 请求日期 | String | 8 | Y | 本次查询请求日期，`yyyyMMdd` |
| req_seq_id | 请求流水号 | String | 64 | Y | 本次查询请求流水号 |
| org_req_date | 原机构请求日期 | String | 8 | Y | 原交易请求日期，`yyyyMMdd` |
| org_req_seq_id | 原机构请求流水号 | String | 128 | N | 原交易请求流水号 |
| org_hf_seq_id | 斗拱返回的全局流水号 | String | 128 | N | 汇付全局流水号 |
| pre_order_id | 预下单订单号 | String | 64 | Y | 预下单订单号 |
| order_stat | 预下单状态 | String | 1 | N | `1`=支付成功，`2`=支付中，`3`=已退款，`4`=处理中，`5`=支付失败，`6`=部分退款 |
| party_order_id | 用户账单上的商户订单号 | String | 64 | N | 用户账单商户订单号 |
| trans_date | 订单日期 | String | 8 | Y | `yyyyMMdd` |
| trans_amt | 交易金额 | String | 14 | Y | 单位元，保留两位小数 |
| pay_type | 交易类型 | String | 16 | N | 返回字段名固定为 `pay_type`；不要按其他接口习惯改成 `trans_type`。官方文档列出 `T_JSAPI`、`T_MINIAPP`、`A_JSAPI`、`A_NATIVE`、`U_NATIVE`、`U_JSAPI`、`QUICK_PAY`、`ONLINE_PAY_B2B`、`ONLINE_PAY_B2C`、`UNION_PAY`、`Y_H5` |
| trans_stat | 交易状态 | String | 1 | N | `P`=处理中，`S`=成功，`F`=失败，`I`=初始；`I` 状态很罕见，需联系汇付技术处理 |
| trans_time | 交易时间 | String | 14 | N | `yyyyMMddHHmmss` |
| close_stat | 关单状态 | String | 1 | N | `P`=处理中，`S`=成功，`F`=失败 |
| fee_flag | 手续费扣款标志 | Int | 1 | N | `1`=外扣，`2`=内扣 |
| fee_amt | 手续费金额 | String | 14 | N | 单位元，保留两位小数 |
| ref_amt | 可退金额 | String | 14 | N | 单位元 |
| goods_desc | 商品描述 | String | 40 | N | 商品描述 |
| remark | 备注 | String | 255 | N | 原样返回 |
| mer_priv | 商户私有域 | String | 1500 | N | 商户私有域 |
| bank_code | 外部通道返回码 | String | 32 | N | 外部通道返回码 |
| bank_desc | 外部通道返回描述 | String | 200 | N | 外部通道返回描述 |
| wx_response | 微信返回的响应报文 | String(JSON Object) | 6000 | N | 见下文 `wx_response` |
| alipay_response | 支付宝返回的响应报文 | String(JSON Object) | 6000 | N | 见下文 `alipay_response` |
| unionpay_response | 银联返回的响应报文 | String(JSON Object) | 6000 | N | 见下文 `unionpay_response` |
| wx_user_id | 微信用户唯一标识码 | String | 128 | N | 微信用户唯一标识码 |
| dy_response | 抖音返回的响应报文 | String(JSON Object) | - | N | 见下文 `dy_response` |
| is_div | 是否分账交易 | String | 1 | Y | `Y`=分账交易，`N`=非分账交易 |
| acct_split_bunch | 分账对象 | String(JSON Object) | 2048 | N | 见下文 `acct_split_bunch` |
| is_delay_acct | 是否延时交易 | String | 1 | Y | `Y`=延迟，`N`=不延迟 |
| trans_fee_allowance_info | 手续费补贴信息 | String(JSON Object) | 6000 | N | 见下文 `trans_fee_allowance_info` |
| quick_online_response | 快捷网银响应 | String(JSON Object) | 6000 | N | 见下文 `quick_online_response` |
| bank_extend_param | 银行扩展信息 | String(JSON Object) | - | N | 网银返回，见下文 `bank_extend_param` |
| fee_formula_infos | 手续费费率信息 | String(JSON Array) | - | N | 微信、支付宝、云闪付交易成功时返回 |
| devs_id | 汇付机具号 | String | 32 | Y | 通过汇付报备的机具必传 |
| out_trans_id | 交易单号 | String | 64 | N | 用户账单上的交易订单号 |
| request_ip | 请求 IP | String | 15 | N | 付款方 IP，仅在支付成功后返回 |

### 返回字段命名约束

- 托管交易查询同步返回中的字段名固定为 `pay_type`。
- “交易类型”只是中文释义，不是建议按其他接口习惯改成 `trans_type`。
- 如果需要生成返回 VO、DTO 或 OpenAPI 描述，优先直接保留 `pay_type`。
- 除非用户已有存量响应契约必须兼容，否则不要额外设计 `trans_type -> pay_type` 的二次映射。

### 同步成功示例

```json
{
  "data": {
    "resp_code": "00000000",
    "resp_desc": "操作成功",
    "huifu_id": "6666000109133323",
    "req_date": "20231102",
    "req_seq_id": "2023110222q11130232812311212",
    "org_req_date": "20231020",
    "org_req_seq_id": "202310201652361987182512",
    "org_hf_seq_id": "0056default231020165304P660ac1360ef00000",
    "pre_order_id": "H2023102016523600627296228",
    "order_stat": "1",
    "party_order_id": "03222310206078496112933",
    "trans_amt": "0.01",
    "pay_type": "A_JSAPI",
    "trans_date": "20231020",
    "trans_time": "20231020165311",
    "trans_stat": "S",
    "fee_amt": "0.00",
    "ref_amt": "0.01",
    "goods_desc": "支付托管消费",
    "remark": "商户私有信息test",
    "product_id": "YYZY",
    "bank_code": "TRADE_SUCCESS",
    "bank_desc": "TRADE_SUCCESS"
  }
}
```

## 业务返回码

| 返回码 | 返回描述 | 处理 |
|--------|----------|------|
| 00000000 | 操作成功 | 按 `order_stat`、`trans_stat`、`close_stat` 继续解析订单状态 |
| 其他 | 官方字段说明要求参考通用业务返回码页 | 结合 `resp_desc` 排查请求参数、原交易标识和通道返回信息 |

## 文档勘误与实现备注

- 官方历史资料中的“业务返回码”说明曾指向旧测试域名；该链接已废弃，当前实现应以正式文档站点为准。
- 公共返回参数表声明顶层 `sign` 为必返字段，但官方成功示例只展示了 `data`，没有给出 `sign`；接入时仍应按“有签名响应”处理。
- 官方成功示例里出现了 `product_id`，但同步返回参数表没有定义该字段；当前不将其视为稳定返回字段。
- `wx_response.cash_fee` 与 `wx_response.coupon_fee` 的类型列写为 `Int`、长度列写为 `100`，但示例值却是金额格式字符串（如 `10.00`、`1.00`）；当前按官方原表保留，并按“金额语义字段”理解。
- 查询条件在原文中分散写在各字段说明里，容易误读成 `huifu_id` 单字段可选；实际应按 `(party_order_id) OR (huifu_id + org_req_date + org_req_seq_id)` 理解。
- `trans_fee_allowance_info.cur_allowance_config_infos` 在本页定义为 `Object`，而前面几个托管支付异步文档中同名字段常见定义为 `Array`；当前以本页官方定义为准，不做静默改写。
- `request_ip` 长度写为 `15`，明显仅覆盖 IPv4 形式；如果上游后续支持 IPv6，应以真实返回为准而不是在调用方写死长度校验。
