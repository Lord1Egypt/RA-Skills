# H5、PC 预下单渠道扩展返回参数

> 本文件覆盖 H5/PC 预下单异步通知中的渠道专属扩展对象，以及分账、手续费补贴、网银扩展等嵌套结果。


## 目录

- `wx_response`
- `alipay_response`
- `unionpay_response`
- `dy_response`
- `acct_split_bunch`
- `trans_fee_allowance_info`
- `bank_extend_param`
- `fee_formula_infos[]`
- 实现备注

## `wx_response`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `sub_appid` | 子商户公众账号 ID | String | 32 | N | 微信分配的子商户公众账号 ID |
| `openid` | 用户标识 | String | 128 | Y | 用户在商户 `appid` 下的唯一标识 |
| `sub_openid` | 子商户用户标识 | String | 128 | N | 用户在子商户 `appid` 下的唯一标识 |
| `bank_type` | 付款银行 | String | 16 | Y | 微信银行类型标识 |
| `cash_fee` | 现金支付金额 | Int | 100 | N | 官方类型列为 `Int`，但金额语义明显按金额字符串理解 |
| `coupon_fee` | 代金券金额 | Int | 100 | N | 代金券或立减优惠金额 |
| `attach` | 商家数据包 | String | 128 | N | 原样返回 |
| `promotion_detail` | 营销详情列表 | Array | 6000 | N | JSON 数组 |

### `wx_response.promotion_detail[]`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `promotion_id` | 优惠 ID | String | 32 | Y | 券或立减优惠 ID |
| `name` | 优惠名称 | String | 64 | N | 优惠名称 |
| `scope` | 优惠范围 | String | 32 | N | `GLOBAL`=全场代金券，`SINGLE`=单品优惠 |
| `type` | 优惠类型 | String | 32 | N | `COUPON`=代金券，`DISCOUNT`=优惠券 |
| `amount` | 优惠券面额 | String | 5 | Y | 用户享受优惠金额 |
| `activity_id` | 活动 ID | String | 32 | Y | 微信商户后台批次 ID |
| `merchant_contribute` | 商户出资 | String | 32 | N | 商户出资金额 |
| `other_contribute` | 其他出资 | String | 32 | N | 其他出资方金额 |
| `goods_detail` | 单品列表 | Object | 3000 | N | JSON 对象 |

### `wx_response.promotion_detail[].goods_detail`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `goods_id` | 商品编码 | String | 32 | Y | 商品编码 |
| `goods_remark` | 商品备注 | String | 32 | N | 按配置原样返回 |
| `discount_amount` | 商品优惠金额 | String | 32 | Y | 单位元 |
| `quantity` | 商品数量 | String | 32 | Y | 用户购买数量 |
| `price` | 商品价格 | String | 32 | Y | 单位元 |

## `alipay_response`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `voucher_detail_list` | 优惠券信息 | Array | - | N | 支付时使用的所有优惠券信息 |
| `fund_bill_list` | 支付金额信息 | String | 512 | N | JSON 格式的资金明细信息 |
| `buyer_id` | 买家支付宝唯一用户号 | String | 28 | N | `2088` 开头纯数字 |
| `buyer_logon_id` | 买家支付宝账号 | String | 100 | N | 买家支付宝账号 |
| `hb_fq_num` | 花呗分期数 | String | 10 | N | 花呗分期数 |
| `hb_fq_seller_percent` | 卖家承担手续费 | String | 3 | N | 卖家承担比例 |

### `alipay_response.voucher_detail_list[]`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `id` | 券 ID | String | 32 | Y | 券 ID |
| `name` | 券名称 | String | 32 | Y | 券名称 |
| `type` | 券类型 | String | 32 | Y | `ALIPAY_FIX_VOUCHER`、`ALIPAY_DISCOUNT_VOUCHER`、`ALIPAY_ITEM_VOUCHER` |
| `amount` | 优惠券面额 | String | 8 | Y | 单位元 |
| `merchant_contribute` | 商家出资 | String | 8 | N | 商家出资金额 |
| `other_contribute` | 其他出资方出资金额 | String | 11 | N | 其他出资金额 |

### `alipay_response.fund_bill_list`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `bank_code` | 银行代码 | String | 10 | N | 银行卡支付时的银行代码 |

## `unionpay_response`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `coupon_info` | 银联优惠信息 | Object | - | N | 银联使用优惠活动时返回 |

### `unionpay_response.coupon_info`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `addnInfo` | 附加信息 | String | 100 | N | 内容自定义 |
| `spnsr_id` | 出资方 | String | 20 | Y | `00010000`=银联出资 |
| `type` | 项目类型 | String | 4 | Y | `DD01`=随机立减，`CP01`=抵金券 |
| `offst_amt` | 抵消交易金额 | String | 12 | Y | 不能全 0 |
| `id` | 项目编号 | String | 40 | N | 自定义格式 |
| `desc` | 项目简称 | String | 40 | N | 优惠活动简称 |

## `dy_response`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `sub_appid` | 子商户应用 ID | String | 32 | N | 抖音开放平台申请的应用 ID |
| `openid` | 用户标识 | String | 128 | Y | 用户在商户 `appid` 下的唯一标识 |
| `sub_openid` | 子商户用户标识 | String | 128 | N | 用户在子商户 `appid` 下的唯一标识 |
| `bank_type` | 付款银行 | String | 16 | Y | 银行类型 |
| `promotion_detail` | 营销详情列表 | String | - | N | JSON 数组字符串 |

### `dy_response.promotion_detail[]`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `coupon_id` | 券 ID | String | 32 | N | 券或立减优惠 ID |
| `name` | 优惠名称 | String | 64 | N | 优惠名称 |
| `scope` | 优惠范围 | String | 32 | N | `GLOBAL`=全场代金券，`SINGLE`=单品优惠 |
| `type` | 优惠类型 | String | 32 | N | `CASH` 或 `NOCASH` |
| `amount` | 优惠券面额 | String | 12 | Y | 单位元 |
| `stock_id` | 活动 ID | String | 32 | N | 活动 ID |
| `douyinpay_contribute` | 抖音出资 | String | 32 | N | 抖音出资金额 |
| `merchant_contribute` | 商户出资 | String | 32 | N | 商户出资金额 |
| `other_contribute` | 其他出资 | String | 32 | N | 其他出资金额 |
| `currency` | 优惠币种 | String | 32 | N | 境内商户仅支持 `CNY` |
| `goods_detail` | 单品列表 | Array | - | N | JSON 数组 |

### `dy_response.promotion_detail[].goods_detail[]`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `goods_id` | 商品编码 | String | 32 | Y | 商品编码 |
| `quantity` | 商品数量 | String | 32 | Y | 用户购买数量 |
| `unit_price` | 商品单价 | String | 32 | N | 单位元 |
| `discount_amount` | 商品优惠金额 | String | 32 | Y | 单位元 |
| `goods_remark` | 商品备注 | String | 128 | N | 商品备注 |

## `acct_split_bunch`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `acct_infos` | 分账明细 | Array | 2048 | Y | 分账明细 |

### `acct_split_bunch.acct_infos[]`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `div_amt` | 分账金额 | String | 14 | Y | 单位元，保留 2 位小数，最低 `0.01` |
| `huifu_id` | 分账接收方 ID | String | 32 | Y | 分账接收方 ID |
| `acct_id` | 收款汇付账户号 | String | 32 | N | 收款账户号 |
| `acct_date` | 账务日期 | String | 8 | N | 格式 `yyyyMMdd` |

## `trans_fee_allowance_info`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `receivable_fee_amt` | 商户应收手续费 | String | 16 | Y | 应收手续费 |
| `actual_fee_amt` | 商户实收手续费 | String | 16 | Y | 实收手续费 |
| `allowance_fee_amt` | 补贴手续费 | String | 16 | Y | 补贴手续费 |
| `allowance_type` | 补贴类型 | String | 10 | N | `0`、`1`、`2`、`3`、`4` |
| `no_allowance_desc` | 不补贴原因 | String | 128 | N | 不补贴原因描述 |
| `cur_allowance_config_infos` | 手续费补贴活动详情 | Object | - | N | 补贴系统原样返回 |

### `trans_fee_allowance_info.cur_allowance_config_infos`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `acct_id` | 门店 | String | 64 | N | 门店标识 |
| `merchant_group` | 商户号 | String | 64 | N | 商户号 |
| `allowance_sys` | 补贴方 | String | 64 | Y | `1`=银行，`2`=服务商，`3`=汇来米 |
| `allowance_sys_id` | 补贴方 ID | String | 64 | Y | 补贴方 ID |
| `is_delay_allowance` | 补贴类型 | String | 2 | Y | `1`=实补，`2`=后补 |
| `market_id` | 自定义活动编号 | String | 64 | Y | 自定义活动编号 |
| `market_name` | 自定义活动名称 | String | 128 | N | 自定义活动名称 |
| `market_desc` | 自定义活动描述 | String | 64 | N | 自定义活动描述 |
| `start_time` | 活动开始时间 | String | 8 | Y | 格式 `yyyyMMdd` |
| `end_time` | 活动结束时间 | String | 8 | Y | 格式 `yyyyMMdd` |
| `pos_debit_limit_amt` | POS 借记卡补贴额度 | String | 16 | Y | 单位元 |
| `pos_credit_limit_amt` | POS 贷记卡补贴额度 | String | 16 | Y | 单位元 |
| `pos_limit_amt` | POS 补贴额度 | String | 16 | Y | 单位元 |
| `qr_limit_amt` | 扫码补贴额度 | String | 16 | Y | 单位元 |
| `total_limit_amt` | 活动总补贴额度 | String | 16 | Y | 单位元 |
| `status` | 活动是否有效 | String | 4 | Y | `1`=生效，`0`=失效 |
| `human_flag` | 是否人工操作 | String | 4 | Y | `N`=自动，`Y`=人工 |
| `activity_id` | 活动号 | String | 64 | Y | 活动号 |
| `activity_name` | 活动描述 | String | 128 | N | 活动描述 |
| `create_by` | 创建人 | String | 32 | Y | 创建人 |
| `create_time` | 创建时间 | String | 32 | Y | 创建时间 |
| `update_time` | 更新时间 | String | 32 | Y | 更新时间 |

## `bank_extend_param`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `gate_type` | 网关支付类型 | String | 2 | N | `01`=个人网关，`02`=企业网关 |
| `bank_id` | 付款方银行号 | String | 32 | N | 付款方银行号 |
| `pyer_acct_id` | 付款方银行账户 | String | 1024 | N | B2B 支付成功后可能返回密文 |
| `pyer_acct_nm` | 付款方银行账户名 | String | 128 | N | 付款方银行账户名 |

## `fee_formula_infos[]`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `fee_formula` | 手续费计算公式 | String | 512 | Y | 例如 `AMT*0.003` |
| `fee_type` | 手续费类型 | String | 32 | Y | `TRANS_FEE` 或 `ACCT_FEE` |
| `huifu_id` | 商户号 | String | 32 | N | 补贴支付账户补贴时的 `huifu_id` |
| `fee_sign` | 手续费场景标识 | String | 32 | N | 微信、支付宝交易的手续费场景码 |

## 实现备注

- `dy_response` 在官方表中既被写成字符串，又展开了子字段；这里按“字符串承载 JSON 数组/对象”的方式理解。
- `wx_response.cash_fee`、`coupon_fee` 的类型列不可信，建议业务侧统一按金额字段兼容解析。
- 如果要落库保存渠道扩展返回，推荐保留原始 JSON，同时抽取少量检索字段，如 `openid`、`buyer_id`、`bank_type`。
