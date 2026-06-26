# 抖音直连下单

> 官方接口更新时间：`2026.04.17`。来源页：`https://paas.huifu.com/partners/api/doc/cpjs/api_cpjs_dypreorder.md`。
> 本接口属于托管支付预下单，和 H5/PC、支付宝小程序、微信小程序预下单共用 `v2/trade/hosting/payment/preorder`，通过 `pre_order_type=4` 区分抖音直连场景。

## 目录

- 什么时候读这里
- 接口概览
- SDK 兼容性
- 公共请求参数
- 请求参数 data
- dy_data
- 同步返回参数
- 异步返回参数
- dy_response
- 分账、手续费和网银扩展
- 实现备注

## 什么时候读这里

- 用户明确说抖音直连、抖音 H5、抖音 APP 支付或 `pre_order_type=4`
- 需要构造抖音直连下单请求、处理 `jump_url` 或抖音支付异步通知
- 需要在托管预下单中按 `pre_order_type=4` 组织抖音直连字段

## 接口概览

| 属性 | 值 |
| --- | --- |
| 请求方式 | `POST` |
| 汇付 API 端点 | `https://api.huifu.com/v2/trade/hosting/payment/preorder` |
| 场景 | 抖音直连下单 |
| `pre_order_type` | `4` |
| 报文格式 | `application/json` |
| SDK Request 类 | Java / PHP / Python 均使用托管预下单 `V2TradeHostingPaymentPreorderH5Request`；不要生成独立 `Dypreorder` / `Douyin` 类 |

## SDK 兼容性

| 语言 | 当前核对结果 | 输出规则 |
| --- | --- | --- |
| Java | 使用 `V2TradeHostingPaymentPreorderH5Request`，该 request 指向共用 `preorder` 端点且有 `setPreOrderType(...)` | 调用 `setPreOrderType("4")`，`dy_data`、`notify_url` 等无专属 setter 的字段通过 `setExtendInfo(...)` / `addExtendInfo(...)` 传入；不要生成不存在的 `Dypreorder` / `Douyin` request 类 |
| PHP | 使用 `V2TradeHostingPaymentPreorderH5Request`，该 request 指向共用 `preorder` 端点且有 `setPreOrderType(...)` | 调用 `setPreOrderType("4")`，`dy_data`、`notify_url` 等扩展字段通过 `setExtendInfo(...)` / params 传入；不要生成不存在的 `Dypreorder` / `Douyin` request 类 |
| Python | 使用 `V2TradeHostingPaymentPreorderH5Request`，该 request 调用共用 `preorder` URL | 设置 `request.pre_order_type = "4"`，`dy_data` 先序列化为 JSON 字符串后通过 `.post(extend_infos)` 传入；不要生成不存在的抖音专属 request 类 |

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
| `pre_order_type` | 预下单类型 | String | Y | 固定传 `4` |
| `req_date` | 请求日期 | String | Y | `yyyyMMdd` |
| `req_seq_id` | 请求流水号 | String | Y | 同一 `huifu_id` 下当天唯一 |
| `huifu_id` | 商户号 | String | Y | 商户开户生成 |
| `trans_amt` | 交易金额 | String | Y | 单位元，保留两位小数，最低 `0.01` |
| `goods_desc` | 商品描述 | String | Y | 最长 40 |
| `time_expire` | 交易失效时间 | String | N | `yyyyMMddHHmmss`；不传默认约 10 分钟 |
| `notify_url` | 交易异步通知地址 | String | N | `http` 或 `https` 开头；最终状态仍以服务端闭环为准 |
| `dy_data` | 抖音参数集合 | String(JSON Object) | Y | 见下方字段 |

## dy_data

| 参数 | 中文名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `sub_appid` | 子商户应用 ID | String | Y | 子商户或二级商户在抖音开放平台申请的应用 ID，需确保已与 `sub_mchid` 绑定 |
| `busi_scene` | 业务场景 | String | Y | `APP` 或 `H5` |
| `coupon_info` | 优惠标记 | String(JSON Object) | N | 与抖音支付协商后使用，可含业务场景、个性化策略或指定优惠信息 |
| `h5_info` | H5 场景信息 | Object | C | `busi_scene=H5` 时必填 |
| `scene_info` | 场景信息 | Object | Y | 支付场景描述 |

### dy_data.h5_info

| 参数 | 中文名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `type` | 场景类型 | String | Y | `Ios`、`Android`、`Wap` |
| `app_name` | 应用名称 | String | N | 应用展示名称 |
| `app_url` | 网站 URL | String | N | H5 网站地址 |
| `bundle_id` | iOS Bundle ID | String | N | iOS 场景使用 |
| `package_name` | Android PackageName | String | N | Android 场景使用 |

### dy_data.scene_info

| 参数 | 中文名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `payer_client_ip` | 用户终端 IP | String | Y | 支持 IPv4 / IPv6，必须来自真实客户端 |

## 同步返回参数

| 参数 | 中文名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `resp_code` | 业务响应码 | String | Y | `00000000` 只表示接口处理成功，不代表支付终态 |
| `resp_desc` | 业务响应信息 | String | Y | 业务返回描述 |
| `req_date` | 请求日期 | String | Y | 原样返回 |
| `req_seq_id` | 请求流水号 | String | Y | 原样返回 |
| `huifu_id` | 商户号 | String | Y | 原样返回 |
| `trans_amt` | 交易金额 | String | Y | 原样返回 |
| `jump_url` | 预支付会话标识 | String | Y | APP 场景返回预支付会话参数，有效期约 2 小时；H5 场景返回拉起抖音支付收银台的中间页 URL，有效期约 5 分钟 |

## 异步返回参数

| 参数 | 中文名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `resp_code` | 业务返回码 | String | Y | 业务返回码 |
| `resp_desc` | 业务返回信息 | String | Y | 业务返回描述 |
| `req_seq_id` | 请求流水号 | String | Y | 交易时传入，原样返回 |
| `req_date` | 请求日期 | String | Y | 交易时传入，原样返回 |
| `hf_seq_id` | 汇付全局流水号 | String | N | 支付平台流水 |
| `out_trans_id` | 用户账单交易订单号 | String | N | 用户账单展示用 |
| `party_order_id` | 用户账单商户订单号 | String | N | 用户账单展示用 |
| `huifu_id` | 商户号 | String | Y | 商户号 |
| `trans_type` | 交易类型 | String | N | `Y_APP`=抖音 APP 支付，`Y_H5`=抖音 H5 支付 |
| `trans_amt` | 交易金额 | String | N | 单位元 |
| `settlement_amt` | 结算金额 | String | N | 单位元 |
| `trans_stat` | 交易状态 | String | N | `S` 成功，`F` 失败 |
| `trans_finish_time` | 汇付侧完成时间 | String | N | `yyyyMMddHHmmss` |
| `end_time` | 支付完成时间 | String | N | `yyyyMMddHHmmss` |
| `acct_date` | 入账时间 | String | N | `yyyyMMdd` |
| `dy_response` | 抖音响应报文 | String(JSON Object) | N | 见下方字段 |
| `is_div` | 是否分账交易 | String | Y | `1`=分账，`0`=非分账 |
| `acct_split_bunch` | 分账对象 | String(JSON Object) | N | 分账结果 |
| `is_delay_acct` | 是否延时交易 | String | Y | `1`=延迟，`0`=不延迟 |
| `fee_flag` | 手续费扣款标志 | Int | N | `1`=外扣，`2`=内扣 |
| `fee_amount` | 手续费金额 | String | N | 单位元 |
| `trans_fee_allowance_info` | 手续费补贴信息 | Object | N | 手续费补贴对象 |
| `remark` | 备注 | String | N | 原样返回 |
| `bank_code` | 通道返回码 | String | N | 通道返回码 |
| `bank_message` | 通道返回描述 | String | N | 通道返回描述 |
| `bank_id` | 收款方银行代号 | String | N | 快捷、网银返回 |
| `bank_extend_param` | 银行扩展信息 | String(JSON Object) | N | 网银返回 |
| `fee_formula_infos` | 手续费费率信息 | String(JSON Array) | N | 微信、支付宝、云闪付交易成功时可能返回 |
| `order_type` | 订单类型 | String | N | `P`=支付，`R`=充值，默认 `P` |
| `devs_id` | 汇付机具号 | String | Y | 报备机具场景返回 |
| `request_ip` | 请求 IP | String | N | 支付成功后可能返回 |

## dy_response

| 参数 | 中文名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `sub_appid` | 子商户应用 ID | String | N | 抖音开放平台应用 ID |
| `openid` | 用户标识 | String | Y | 用户在商户 appid 下的唯一标识 |
| `sub_openid` | 子商户用户标识 | String | N | 用户在子商户 appid 下的唯一标识 |
| `bank_type` | 付款银行 | String | Y | 银行类型标识 |
| `promotion_detail` | 营销详情列表 | String(JSON Array) | N | 抖音营销详情 |

### dy_response.promotion_detail[]

| 参数 | 中文名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `coupon_id` | 券 ID | String | N | 券或立减优惠 ID |
| `name` | 优惠名称 | String | N | 优惠名称 |
| `scope` | 优惠范围 | String | N | `GLOBAL` 或 `SINGLE` |
| `type` | 优惠类型 | String | N | `CASH` 或 `NOCASH` |
| `amount` | 优惠券面额 | String | Y | 单位元 |
| `stock_id` | 活动 ID | String | N | 活动 ID |
| `douyinpay_contribute` | 抖音出资 | String | N | 单位元 |
| `merchant_contribute` | 商户出资 | String | N | 单位元 |
| `other_contribute` | 其他出资 | String | N | 单位元 |
| `currency` | 优惠币种 | String | N | 境内商户通常为 `CNY` |
| `goods_detail` | 单品列表 | Array | N | 单品明细 |

### dy_response.promotion_detail[].goods_detail[]

| 参数 | 中文名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `goods_id` | 商品编码 | String | Y | 商品编码 |
| `quantity` | 商品数量 | String | Y | 购买数量 |
| `unit_price` | 商品单价 | String | N | 单位元 |
| `discount_amount` | 商品优惠金额 | String | Y | 单品优惠金额 |
| `goods_remark` | 商品备注 | String | N | 原样返回 |

## 分账、手续费和网银扩展

### acct_split_bunch.acct_infos[]

| 参数 | 中文名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `acct_infos` | 分账明细 | Array | Y | 分账明细数组 |

#### acct_split_bunch.acct_infos[] 明细

| 参数 | 中文名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `div_amt` | 分账金额 | String | Y | 单位元，保留两位小数 |
| `huifu_id` | 分账接收方 ID | String | Y | 斗拱开户生成 |
| `acct_id` | 收款汇付账户号 | String | N | 不填默认基本户 |
| `acct_date` | 账务日期 | String | N | `yyyyMMdd` |

### trans_fee_allowance_info

| 参数 | 中文名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `receivable_fee_amt` | 商户应收手续费 | String | Y | 单位元 |
| `actual_fee_amt` | 商户实收手续费 | String | Y | 单位元 |
| `allowance_fee_amt` | 补贴手续费 | String | Y | 单位元 |
| `allowance_type` | 补贴类型 | String | N | `0` 不补贴或为空默认，`1` 补贴，`2` 部分补贴，`3` 全额补贴，`4` 部分补贴优惠后 |
| `no_allowance_desc` | 不补贴原因 | String | N | 补贴系统返回原因码；官方列出 `1`-`9`，用于区分活动无效、不满足规则、额度不足等不补贴原因 |
| `cur_allowance_config_infos` | 手续费补贴活动详情 | Object | N | 补贴系统返回，斗拱原样返回 |

### trans_fee_allowance_info.cur_allowance_config_infos

| 参数 | 中文名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `acct_id` | 门店 | String | N | 门店或账户标识 |
| `merchant_group` | 商户号 | String | N | 商户号 |
| `allowance_sys` | 补贴方 | String | Y | `1` 银行，`2` 服务商，`3` 汇来米 |
| `allowance_sys_id` | 补贴方 ID | String | Y | 补贴方标识 |
| `is_delay_allowance` | 补贴类型 | String | Y | `1` 实补，`2` 后补，默认实补 |
| `market_id` | 自定义活动编号 | String | Y | 活动编号 |
| `market_name` | 自定义活动名称 | String | N | 活动名称 |
| `market_desc` | 自定义活动描述 | String | N | 活动描述 |
| `start_time` | 活动开始时间 | String | Y | `yyyyMMdd` |
| `end_time` | 活动结束时间 | String | Y | `yyyyMMdd` |
| `pos_debit_limit_amt` | POS 借记卡补贴额度 | String | Y | 单位元 |
| `pos_credit_limit_amt` | POS 贷记卡补贴额度 | String | Y | 单位元 |
| `pos_limit_amt` | POS 补贴额度 | String | Y | 单位元 |
| `qr_limit_amt` | 扫码补贴额度 | String | Y | 单位元 |
| `total_limit_amt` | 活动总补贴额度 | String | Y | 单位元 |
| `status` | 活动是否有效 | String | Y | `1` 生效，`0` 失效 |
| `human_flag` | 是否人工操作 | String | Y | `N` 自动，`Y` 人工 |
| `activity_id` | 活动号 | String | Y | 活动号 |
| `activity_name` | 活动描述 | String | N | 活动描述 |
| `create_by` | 创建人 | String | Y | 创建人 |
| `create_time` | 创建时间 | String | Y | 创建时间 |
| `update_time` | 更新时间 | String | Y | 更新时间 |

### bank_extend_param

| 参数 | 中文名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `gate_type` | 网关支付类型 | String | N | `01` 个人网关，`02` 企业网关 |
| `bank_id` | 付款方银行号 | String | N | 网银返回 |
| `pyer_acct_id` | 付款方银行账户 | String | N | B2B 支付成功后可能返回密文 |
| `pyer_acct_nm` | 付款方银行账户名 | String | N | B2B 支付成功后可能返回 |

### fee_formula_infos[]

| 参数 | 中文名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `fee_formula` | 手续费计算公式 | String | Y | 手续费计算公式 |
| `fee_type` | 手续费类型 | String | Y | `TRANS_FEE` 交易手续费，`ACCT_FEE` 组合支付账户补贴手续费 |
| `huifu_id` | 商户号 | String | N | 补贴账户的 `huifu_id` |
| `fee_sign` | 手续费场景标识 | String | N | 业务开通配置时获取的场景标识 |

## 实现备注

- `dy_data`、`h5_info`、`scene_info` 建议在业务层建模为对象，调用 SDK 前再序列化为 JSON 字符串。
- `busi_scene=H5` 时必须准备真实 `h5_info` 和真实用户终端 IP，不能复用示例值。
- `dy_data.sub_appid` 必须使用已与抖音商户号绑定的应用 ID。
- `jump_url` 是短时效拉起凭证：APP 预支付参数约 2 小时有效，H5 中间页 URL 约 5 分钟有效，业务侧过期后应重新下单。
- 同步返回的 `jump_url` 或预支付参数只用于前端拉起支付，不等于支付成功。
- 最终状态必须走服务端闭环：异步通知验签、幂等和必要的托管查单或拆单查询确认。
- SDK 说明必须区分“抖音直连是托管预下单场景”与“存在独立抖音 Request 类”；三语言都使用托管预下单 request，不要说存在独立抖音 Request 类。
