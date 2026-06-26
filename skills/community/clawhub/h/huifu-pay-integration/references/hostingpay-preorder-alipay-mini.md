## 目录

- [接口概述](#接口概述)
- [应用场景](#应用场景)
- [SDK 映射](#sdk-映射)
- [公共请求参数](#公共请求参数)
- [请求参数 data](#请求参数-data)
- [嵌套参数展开](#嵌套参数展开)
- [请求示例](#请求示例)
- [同步返回参数](#同步返回参数)
- [异步返回参数](#异步返回参数)
- [业务返回码](#业务返回码)
- [文档勘误与实现备注](#文档勘误与实现备注)

# 支付宝小程序预下单

> 本文依据 2026-05-26 官方文档整理，适用于 `v2/trade/hosting/payment/preorder` 的支付宝小程序场景。

## 接口概述

| 属性 | 值 |
|------|-----|
| 请求方式 | `POST` |
| 汇付 API 端点 | `https://api.huifu.com/v2/trade/hosting/payment/preorder` |
| pre_order_type | `2` |
| SDK Request 类 | `V2TradeHostingPaymentPreorderAliRequest` |
| Content-Type | `application/json;charset=UTF-8` |

说明：

- 支持 JSON 报文。
- 请求整体需要签名，验签规则见 `references/hostingpay-java-tech-spec.md`。
- 文档中的 `String(JSON Object)` / `String(JSON Array)` 表示字段外层类型仍是 `String`，但值内容需要传 JSON 字符串。

## 应用场景

- 支付宝小程序预下单接口可以满足商户或服务商在 App 拉起支付宝支付的需求。

## 官方业务开通及配置要点

- 官方托管产品文档要求先开通托管支付权限并配置支付宝费率。
- `app_data.app_schema` 必须来自真实客户端回跳方案，不应使用示例值。
- `notify_url` 需满足官方回调地址约束：`http/https`、不重定向、URL 不带参数、自定义端口在 `8000-9005`、收到通知后返回 `200`。
- 支付完成后的前端回跳不是最终成功依据，后端仍应通过异步通知或主动查询确认状态。

## SDK 映射

`V2TradeHostingPaymentPreorderAliRequest` 的独立 setter 字段：

| 字段 | setter | 类型 | 必填 | 说明 |
|------|--------|------|------|------|
| huifuId | `setHuifuId()` | String(32) | Y | 商户号 |
| reqDate | `setReqDate()` | String(8) | Y | 请求日期，`yyyyMMdd` |
| reqSeqId | `setReqSeqId()` | String(64) | Y | 同一 `huifu_id` 下当天唯一 |
| preOrderType | `setPreOrderType()` | String(1) | Y | 固定传 `2` |
| transAmt | `setTransAmt()` | String(14) | Y | 交易金额，单位元，保留两位小数 |
| goodsDesc | `setGoodsDesc()` | String(40) | Y | 商品描述 |
| appData | `setAppData()` | String(2000) | Y | app 扩展参数集合，JSON 字符串 |

其余扩展字段通过 `setExtendInfo(Map<String, Object>)` 传入。

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
| huifu_id | 商户号 | String | 32 | Y | 开户自动生成 |
| acct_id | 收款汇付账户号 | String | 32 | N | 仅支持基本户、现金户；不填默认基本户；仅微信、支付宝、网银支持指定收款账户 |
| req_date | 请求日期 | String | 8 | Y | `yyyyMMdd` |
| req_seq_id | 请求流水号 | String | 64 | Y | 同一 `huifu_id` 下当天唯一 |
| pre_order_type | 预下单类型 | String | 1 | Y | 支付宝预下单固定为 `2` |
| trans_amt | 交易金额 | String | 14 | Y | 单位元，保留两位小数，最低 `0.01` |
| goods_desc | 商品描述 | String | 40 | Y | 商品描述 |
| delay_acct_flag | 是否延迟交易 | String | 1 | N | `Y`=延迟，`N`=不延迟，默认 `N` |
| acct_split_bunch | 分账对象 | String(JSON Object) | 2000 | N | 分账对象 |
| hosting_data | 统一收银台扩展参数集合 | String(JSON Object) | 2000 | N | 可传项目号等托管扩展 |
| app_data | app 扩展参数集合 | String(JSON Object) | 2000 | Y | app 扩展参数集合 |
| time_expire | 交易失效时间 | String | 14 | N | `yyyyMMddHHmmss`；默认 10 分钟 |
| biz_info | 业务信息 | String(JSON Object) | 2000 | N | 交易相关信息 |
| notify_url | 异步通知地址 | String | 512 | N | `http` 或 `https` 开头 |
| alipay_data | 支付宝参数集合 | String(JSON Object) | 2048 | N | 支付宝场景扩展参数 |
| terminal_device_data | 设备信息 | String(JSON Object) | 2048 | N | 设备信息 |
| fee_sign | 手续费场景标识 | String | 32 | N | 商户业务开通配置的手续费场景标识码，仅微信/支付宝交易时生效 |
| fee_split_flag | 是否交易手续费分摊 | String | 1 | N | `Y`=分摊，`N`=不分摊；不传默认 `N` |
| fee_flag | 手续费扣款标志 | String | 1 | N | `1`=外扣，`2`=内扣；默认取控台配置 |

## 嵌套参数展开

### acct_split_bunch

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| acct_infos | 分账明细 | Array | - | N | 分账明细 |
| percentage_flag | 百分比分账标志 | String | 1 | N | `Y`=使用百分比分账 |
| is_clean_split | 是否净值分账 | String | 1 | N | `Y`=使用净值分账；仅交易手续费内扣且使用百分比分账时起作用 |

#### acct_split_bunch.acct_infos[]

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| div_amt | 分账金额 | String | 14 | N | 单位元，保留两位小数，最低 `0.01` |
| huifu_id | 分账接收方 ID | String | 32 | N | 斗拱开户时生成 |
| acct_id | 收款汇付账户号 | String | 32 | N | 仅支持基本户、现金户；仅微信、支付宝、网银支持指定收款账户 |
| percentage_div | 分账百分比 | String | 6 | N | 表示百分比，如 `23.50`；仅 `percentage_flag=Y` 时起作用，全部分账百分比之和必须为 `100.00` |

### hosting_data

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| project_id | 项目号 | String | 32 | N | 商户创建的项目号 |

### app_data

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| appid | 支付宝小程序 ID | String | 32 | N | 托管支付宝小程序时上送 |
| app_schema | 小程序返回码 | String | 100 | Y | 小程序完成支付后回跳所需 AppScheme；限 100 字符，包含 `+/?%#&=` 时需 URL 编码 |
| private_info | 私有信息 | String | 255 | N | 对应异步通知和主动查询接口中的 `remark` |

### biz_info

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| payer_check_ali | 付款人验证（支付宝） | Object | - | N | 支付宝特殊交易需验证买家信息；当前只支持 AT 类交易有验证功能 |
| person_payer | 个人付款人信息 | Object | - | N | 付款人验证打开后可填写付款人信息 |

#### biz_info.payer_check_ali

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| need_check_info | 是否提供校验身份信息 | String | 1 | N | `T`=强制校验，需要填写 `person_payer`；`F`=不强制 |
| min_age | 允许的最小买家年龄 | String | 3 | N | 仅 `need_check_info=T` 时有效；整数且大于等于 `0` |
| fix_buyer | 是否强制校验付款人身份信息 | String | 8 | N | `T`=强制校验，`F`=不强制 |

#### biz_info.person_payer

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| name | 姓名 | String | 16 | N | 支付宝交易 `need_check_info=T` 时有效 |
| cert_type | 证件类型 | String | 32 | N | `IDENTITY_CARD`、`PASSPORT`、`OFFICER_CARD`、`SOLDIER_CARD`、`HOKOU` |
| cert_no | 证件号 | String | 64 | N | 支付宝交易 `need_check_info=T` 时有效；需使用汇付 RSA 公钥加密 |
| mobile | 手机号 | String | 20 | N | 文档说明当前暂不校验 |

### alipay_data

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| alipay_store_id | 支付宝的店铺编号 | String | 32 | N | 支付宝店铺编号 |
| extend_params | 业务扩展参数 | Object | 2048 | N | 业务扩展参数 |
| goods_detail | 订单包含的商品列表信息 | Array | 2048 | N | 订单商品列表 |
| merchant_order_no | 商户原始订单号 | String | 32 | N | 商户原始订单号 |
| operator_id | 商户操作员编号 | String | 28 | N | 商户操作员编号 |
| product_code | 产品码 | String | 32 | N | 商家和支付宝签约的产品码；小程序场景支付为 `JSAPI_PAY`，当面付为 `FACE_TO_FACE_PAYMENT` |
| seller_id | 卖家支付宝用户号 | String | 28 | N | 卖家支付宝用户号 |
| store_id | 商户门店编号 | String | 32 | N | 商户门店编号 |
| subject | 订单标题 | String | 256 | N | 直连模式必填 |
| store_name | 商家门店名称 | String | 512 | N | 商家门店名称 |
| ali_business_params | 商户业务信息 | String | 512 | N | JSON 字符串 |

#### alipay_data.extend_params

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| card_type | 卡类型 | String | 32 | N | 卡类型 |
| food_order_type | 支付宝点餐场景类型 | String | 20 | N | `QR_ORDER`、`PRE_ORDER`、`HOME_DELIVERY`、`DIRECT_PAYMENT`、`QR_FOOD_ORDER`、`P_QR_FOOD_ORDER`、`SELF_PICK`、`TAKE_OUT`、`OTHER` |
| hb_fq_num | 花呗分期数 | String | 5 | N | 花呗分期数 |
| hb_fq_seller_percent | 花呗卖家手续费百分比 | String | 3 | N | 花呗商贴支付默认传 `0` |
| industry_reflux_info | 行业数据回流信息 | String | 64 | N | 行业数据回流信息 |
| fq_channels | 信用卡分期资产方式 | String | 20 | N | `alipayfq_cc` 表示信用卡分期，为空默认花呗 |
| parking_id | 停车场 ID | String | 28 | N | 支付宝停车场唯一标识 |
| sys_service_provider_id | 系统商编号 | String | 64 | N | 系统商签约协议 PID |

#### alipay_data.goods_detail[]

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| goods_id | 商品编号 | String | 32 | Y | 商品编号 |
| goods_name | 商品名称 | String | 256 | Y | 商品名称 |
| price | 商品单价 | String | 16 | Y | 单位元 |
| quantity | 商品数量 | String | 10 | Y | 商品数量 |
| body | 商品描述信息 | String | 1000 | N | 商品描述 |
| categories_tree | 商品类目树 | String | 128 | N | 从根类目到叶子类目 ID 组成 |
| goods_category | 商品类目 | String | 24 | N | 商品类目 |
| show_url | 商品展示地址 | String | 400 | N | 商品展示地址 |

### terminal_device_data

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| devs_id | 汇付机具号 | String | 32 | Y | 通过汇付报备的机具必传 |

## 请求示例

```json
{
  "sys_id": "6666000108840829",
  "product_id": "YYZY",
  "data": {
    "checkout_id": "",
    "delay_acct_flag": "N",
    "req_seq_id": "20240514165442868h32ss2g3s7vnxq",
    "req_date": "20240514",
    "trans_amt": "0.10",
    "huifu_id": "6666000109133323",
    "goods_desc": "app跳支付宝消费",
    "pre_order_type": "2",
    "app_data": "{\"app_schema\":\"app跳转链接\"}",
    "notify_url": "https://callback.service.com/xx",
    "acct_split_bunch": "{\"acct_infos\":[{\"huifu_id\":\"6666000109133323\",\"div_amt\":\"0.08\"}]}"
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
| resp_code | 业务响应码 | String | 8 | Y | 接口受理返回码，用于排查；订单终态仍看通知和查单结果 |
| resp_desc | 业务响应信息 | String | 128 | Y | 业务返回描述 |
| req_date | 请求日期 | String | 8 | Y | 原样返回 |
| req_seq_id | 请求流水号 | String | 64 | Y | 原样返回 |
| huifu_id | 商户号 | String | 32 | Y | 原样返回 |
| trans_amt | 交易金额 | String | 12 | Y | 原样返回 |
| jump_url | 支付跳转链接 | String | 256 | Y | 用于 App 跳转支付宝 |

### 同步成功示例

```json
{
  "data": {
    "resp_code": "00000000",
    "resp_desc": "交易成功",
    "req_date": "20220424",
    "req_seq_id": "20220424561166000",
    "huifu_id": "6666000111546360",
    "trans_amt": "0.10",
    "jump_url": "alipays://platformapi/startapp?appId=2021003121605466&thirdPartSchema=app跳转链接&page=pages/cashier/cashier?p%3DH2022042814245600912499897%26s%3Dapp"
  }
}
```

## 异步返回参数

> 只有成功发起支付才会有异步返回；异步回调体为 `resp_data`。

### resp_data

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| resp_code | 业务返回码 | String | 8 | Y | 业务返回码 |
| resp_desc | 业务返回信息 | String | 512 | Y | 业务返回描述 |
| huifu_id | 商户号 | String | 32 | Y | 商户号 |
| req_date | 请求时间 | String | 8 | Y | 原样返回，格式 `yyyyMMdd` |
| req_seq_id | 请求流水号 | String | 64 | Y | 原样返回 |
| hf_seq_id | 全局流水号 | String | 40 | N | 汇付全局流水号 |
| out_trans_id | 用户账单上的交易订单号 | String | 64 | N | 用户账单交易订单号 |
| party_order_id | 用户账单上的商户订单号 | String | 64 | N | 用户账单商户订单号 |
| trans_type | 交易类型 | String | 20 | N | 文档列出的支付类型包括 `T_JSAPI`、`T_MINIAPP`、`A_JSAPI`、`A_NATIVE`、`U_NATIVE`、`U_JSAPI`、`T_MICROPAY`、`A_MICROPAY`、`U_MICROPAY`、`D_NATIVE`、`D_MICROPAY` |
| trans_amt | 交易金额 | String | 12 | N | 单位元，保留两位小数 |
| settlement_amt | 结算金额 | String | 16 | N | 单位元，保留两位小数 |
| fee_amount | 手续费金额 | String | 16 | N | 单位元，保留两位小数 |
| trans_stat | 交易状态 | String | 1 | N | `S`=成功，`F`=失败 |
| trans_finish_time | 汇付侧交易完成时间 | String | 6 | N | 文档原表长度列为 `6`，格式说明为 `yyyyMMddHHmmss` |
| end_time | 支付完成时间 | String | 14 | N | `yyyyMMddHHmmss` |
| acct_date | 入账时间 | String | 8 | N | `yyyyMMdd` |
| debit_flag | 借贷记标识 | String | 1 | N | `D`=借记卡，`C`=信用卡，`Z`=借贷合一卡 |
| alipay_response | 支付宝返回的响应报文 | String(JSON Object) | 6000 | N | JSON 格式 |
| is_div | 是否分账交易 | String | 1 | Y | `1`=分账交易，`0`=非分账交易 |
| acct_split_bunch | 分账对象 | String(JSON Object) | 2048 | N | 分账对象 |
| is_delay_acct | 是否延时交易 | String | 1 | Y | `1`=延迟，`0`=不延迟 |
| fee_flag | 手续费扣款标志 | Int | 1 | N | `1`=外扣，`2`=内扣 |
| trans_fee_allowance_info | 手续费补贴信息 | String(JSON Object) | 6000 | N | JSON 格式 |
| fee_formula_infos | 手续费费率信息 | String(JSON Array) | - | N | 微信、支付宝、云闪付成功时返回 |
| remark | 备注 | String | 45 | N | 原样返回 |
| bank_code | 通道返回码 | String | 32 | N | 通道返回码 |
| bank_message | 通道返回描述 | String | 200 | N | 通道返回描述 |
| devs_id | 汇付机具号 | String | 32 | Y | 通过汇付报备的机具必传 |

### alipay_response

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| voucher_detail_list | 本交易支付时使用的所有优惠券信息 | Array | - | N | 本交易支付时使用的所有优惠券信息 |
| fund_bill_list | 支付金额信息 | String(JSON) | 512 | N | 支付成功的各个渠道金额信息 |
| buyer_id | 买家的支付宝唯一用户号 | String | 28 | N | 2088 开头的纯数字 |
| buyer_logon_id | 买家支付宝账号 | String | 100 | N | 买家支付宝账号 |
| hb_fq_num | 花呗分期数 | String | 10 | N | 花呗分期数 |
| hb_fq_seller_percent | 卖家承担的手续费 | String | 3 | N | 卖家承担的手续费 |

#### alipay_response.voucher_detail_list[]

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| id | 券 ID | String | 32 | Y | 券 ID |
| name | 券名称 | String | 32 | Y | 券名称 |
| type | 券类型 | String | 32 | Y | `ALIPAY_FIX_VOUCHER`、`ALIPAY_DISCOUNT_VOUCHER`、`ALIPAY_ITEM_VOUCHER` |
| amount | 优惠券面额 | String | 8 | Y | 优惠券面额 |
| merchant_contribute | 商家出资 | String | 8 | N | 发起交易商家的出资金额 |
| other_contribute | 其他出资方出资金额 | String | 11 | N | 其他出资方金额 |

#### alipay_response.fund_bill_list

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| bank_code | 银行卡支付时的银行代码 | String | 10 | N | 银行卡支付时的银行代码 |

### acct_split_bunch

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| acct_infos | 分账明细 | Array | 2048 | Y | 分账明细 |

#### 异步返回 acct_split_bunch.acct_infos[]

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| div_amt | 分账金额 | String | 14 | Y | 单位元，保留两位小数，最低 `0.01` |
| huifu_id | 分账接收方 ID | String | 32 | Y | 分账接收方 ID |
| acct_id | 收款汇付账户号 | String | 32 | N | 收款账户号 |
| acct_date | 账务日期 | String | 8 | N | `yyyyMMdd` |

### trans_fee_allowance_info

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| receivable_fee_amt | 商户应收手续费 | String | 16 | Y | 商户应收手续费 |
| actual_fee_amt | 商户实收手续费 | String | 16 | Y | 商户实收手续费 |
| allowance_fee_amt | 补贴手续费 | String | 16 | Y | 补贴手续费 |
| allowance_type | 补贴类型 | String | 10 | N | `0`、`1`、`2`、`3`、`4` |
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

### fee_formula_infos[]

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| fee_formula | 手续费计算公式 | String | 512 | Y | 手续费计算公式 |
| fee_type | 手续费类型 | String | 32 | Y | `TRANS_FEE` 或 `ACCT_FEE` |
| huifu_id | 商户号 | String | 32 | N | 补贴支付账户补贴时，补贴账户的 `huifu_id` |
| fee_sign | 手续费场景标识 | String | 32 | N | 微信/支付宝交易手续费场景标识码 |

## 业务返回码

| 返回码 | 返回描述 | 处理 |
|--------|----------|------|
| 99010002 | 预下单请求流水重复 | 提供新的 `req_seq_id` |

## 文档勘误与实现备注

- 请求示例里出现了 `checkout_id`，但参数表没有定义该字段；当前 skill 不将其视为正式接入参数。
- 异步字段 `trans_finish_time` 的长度列写为 `6`，但格式说明为 `yyyyMMddHHmmss`；实现时按 14 位时间串处理更合理。
- `alipay_response`、`trans_fee_allowance_info` 在父表中写成 `String` 且说明为 Json 格式，同时又展开了子字段；当前文档按“JSON 字符串承载对象”的方式描述。
- `app_schema` 限长 100 字符，且含 `+/?%#&=` 时必须编码，否则容易导致无法唤起收银台。
