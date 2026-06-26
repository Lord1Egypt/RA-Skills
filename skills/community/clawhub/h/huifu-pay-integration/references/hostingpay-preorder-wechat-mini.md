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
- [拆单支付异步返回参数](#拆单支付异步返回参数)
- [业务返回码](#业务返回码)
- [文档勘误与实现备注](#文档勘误与实现备注)

# 微信小程序预下单
> 本文依据 2026-05-26 官方文档整理，适用于 `v2/trade/hosting/payment/preorder` 的微信小程序场景。

## 接口概述
| 属性 | 值 |
|------|-----|
| 请求方式 | `POST` |
| 汇付 API 端点 | `https://api.huifu.com/v2/trade/hosting/payment/preorder` |
| pre_order_type | `3` |
| SDK Request 类 | `V2TradeHostingPaymentPreorderWxRequest` |
| Content-Type | `application/json;charset=UTF-8` |

说明：
- 支持 JSON 报文。
- 请求整体需要签名，验签规则见 `references/hostingpay-java-tech-spec.md`。
- 文档中的 `String(JSON Object)` / `String(JSON Array)` 表示字段外层类型仍是 `String`，但值内容需要传 JSON 字符串。

## 应用场景
- 外部 App 跳转微信支付：App 需接入微信 OpenSDK，跳转微信拉起小程序时，需将返回 `miniapp_data.path` 拼成 `pages/cashier/cashier?p={pre_order_id}&s=app`。
- 外部浏览器 H5 跳转微信支付：访问返回的 `miniapp_data.scheme_code`；H5 跳转微信支付后不支持跳回原浏览器。
- 小程序跳转小程序支付：见汇付“小程序跳转小程序支付说明”。

## 官方业务开通及配置要点

- 官方产品文档要求先完成小程序托管授权、代码发布和 appid 绑定，之后才能拿到真实应用 ID `seq_id`。
- 商户需事先开通微信支付产品并配置相应费率，否则无法完成交易。
- `split_pay_flag=Y` 前提是拆单支付权限已预开通或特批通过。
- `notify_url` 需满足官方回调地址约束：`http/https`、不重定向、URL 不带参数、自定义端口在 `8000-9005`、收到通知后返回 `200`。
- 支付完成后的前端回跳不是最终成功依据，后端仍应通过异步通知或主动查询确认状态。

## SDK 映射
`V2TradeHostingPaymentPreorderWxRequest` 的独立 setter 字段：

| 字段 | setter | 类型 | 必填 | 说明 |
|------|--------|------|------|------|
| preOrderType | `setPreOrderType()` | String(1) | Y | 固定传 `3` |
| reqDate | `setReqDate()` | String(8) | Y | 请求日期，`yyyyMMdd` |
| reqSeqId | `setReqSeqId()` | String(64) | Y | 同一 `huifu_id` 下当天唯一 |
| huifuId | `setHuifuId()` | String(32) | Y | 商户号 |
| transAmt | `setTransAmt()` | String(14) | Y | 交易金额，单位元，保留两位小数 |
| goodsDesc | `setGoodsDesc()` | String(40) | Y | 商品描述 |
| miniappData | `setMiniappData()` | String(2000) | Y | 微信小程序扩展参数集合，JSON 字符串 |

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
| pre_order_type | 预下单类型 | String | 1 | Y | 微信预下单固定为 `3` |
| req_date | 请求日期 | String | 8 | Y | `yyyyMMdd` |
| req_seq_id | 请求流水号 | String | 64 | Y | 同一 `huifu_id` 下当天唯一 |
| huifu_id | 商户号 | String | 32 | Y | 开户自动生成 |
| acct_id | 收款汇付账户号 | String | 32 | N | 仅支持基本户、现金户；不填默认基本户；仅微信、支付宝、网银支持指定收款账户 |
| trans_amt | 交易金额 | String | 14 | Y | 单位元，保留两位小数，最低 `0.01` |
| goods_desc | 商品描述 | String | 40 | Y | 商品描述 |
| delay_acct_flag | 是否延迟交易 | String | 1 | N | `Y`=延迟，`N`=不延迟，默认 `N` |
| split_pay_flag | 是否拆单支付 | String | 1 | N | `Y`=拆单支付，`N`=非拆单支付，默认 `N`；需预开通拆单支付权限 |
| split_pay_data | 拆单支付参数集合 | String(JSON Object) | 2000 | N | 拆单支付参数集合 |
| acct_split_bunch | 分账对象 | String(JSON Object) | 2000 | N | 分账对象；拆单支付时不生效 |
| hosting_data | 统一收银台扩展参数集合 | String(JSON Object) | 2000 | N | 可传项目号等托管扩展 |
| miniapp_data | 微信小程序扩展参数集合 | String(JSON Object) | 2000 | Y | 微信小程序扩展参数集合 |
| time_expire | 交易失效时间 | String | 14 | N | `yyyyMMddHHmmss`；默认 10 分钟 |
| biz_info | 业务信息 | String(JSON Object) | 2000 | N | 交易相关信息 |
| notify_url | 交易异步通知地址 | String | 512 | N | `http` 或 `https` 开头 |
| wx_data | 微信参数集合 | String(JSON Object) | 2048 | N | 微信场景扩展参数 |
| terminal_device_data | 设备信息 | String(JSON Object) | 2048 | N | 设备信息 |
| fee_sign | 手续费场景标识 | String | 32 | N | 商户业务开通配置的手续费场景标识码，仅微信/支付宝交易时生效 |
| fee_split_flag | 是否交易手续费分摊 | String | 1 | N | `Y`=分摊，`N`=不分摊；不传默认 `N` |
| fee_flag | 手续费扣款标志 | String | 1 | N | `1`=外扣，`2`=内扣；默认取控台配置 |

## 嵌套参数展开
### split_pay_data
| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| fq_mer_discount_flag | 商户贴息标记 | String | 1 | N | 花呗分期商户补贴活动拆单支付时生效；`Y`=商户全额贴息，`P`=商户部分贴息，不传为默认 |
| ali_business_params | 商户业务信息 | String | 1 | N | 拆单支付时生效，JSON 字符串 |

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
| percentage_div | 分账百分比 | String | 6 | N | 表示百分比，如 `23.50`；仅 `percentage_flag=Y` 时生效，合计必须为 `100.00` |

### hosting_data
| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| project_id | 项目号 | String | 32 | N | 商户创建的项目号 |

### miniapp_data
| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| seq_id | 应用 ID | String | 64 | N | 不传默认使用斗拱收银台唤起支付；自有渠道可通过控台获取 |
| private_info | 私有信息 | String | 255 | N | 对应异步通知和主动查询接口中的 `remark` |
| need_scheme | 是否生成 `scheme_code` | String | 1 | Y | `Y` 适用于 App/短信/H5/邮件/外部网页/微信内拉起汇付小程序；`N` 适用于汇付微信插件支付 |

### biz_info
| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| payer_check_wx | 付款人验证（微信） | Object | - | N | 微信实名支付需验证买家信息；当前只支持 AT 类交易有验证功能 |
| person_payer | 个人付款人信息 | Object | - | N | 付款人验证打开后可填写付款人信息 |

#### biz_info.payer_check_wx
| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| limit_payer | 指定支付者 | String | 5 | N | `ADULT`=仅成年人可支付 |
| real_name_flag | 微信实名验证 | String | 1 | N | `Y/N`，默认 `N` |

#### biz_info.person_payer
| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| name | 姓名 | String | 16 | N | 姓名 |
| cert_type | 证件类型 | String | 32 | N | 微信仅支持 `IDENTITY_CARD` |
| cert_no | 证件号 | String | 64 | N | 需使用汇付 RSA 公钥加密 |

### wx_data
| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| sub_appid | 子商户应用 ID | String | 32 | N | 子商户在微信申请的应用 ID；部分聚合正扫发货管理场景需配合 `sub_openid` 使用 |
| sub_openid | 子商户用户标识 | String | 128 | N | 公众号和小程序场景必填；用户在子商户 `sub_appid` 下的唯一标识 |
| attach | 附加数据 | String | 127 | N | 在查询 API 和支付通知中原样返回 |
| body | 商品描述 | String | 128 | N | 格式要求：门店品牌名-城市分店名-实际商品名称 |
| detail | 商品详情 | Object | 6000 | N | 单品优惠功能字段 |
| device_info | 设备号 | String | 32 | N | H5 与小程序支付取值：苹果 APP=1，安卓 APP=2，iOS H5=3，Android H5=4 |
| goods_tag | 订单优惠标记 | String | 32 | N | 代金券或立减优惠参数 |
| identity | 实名支付 | String | 128 | N | 公安和保险类商户使用，JSON 字符串，包含类型、证件号、姓名 |
| receipt | 开发票入口开放标识 | String | 8 | N | 开发票入口开放标识 |
| scene_info | 场景信息 | Object | 2048 | N | 当前支持上报门店信息 |
| spbill_create_ip | 终端 IP | String | 64 | N | 调用微信支付 API 的机器 IP |
| promotion_flag | 单品优惠标识 | String | 1 | N | `Y`=是，`N`=否；若为 `Y`，则 `detail` 必填 |
| product_id | 新增商品 ID | String | 32 | N | 直连模式 `trade_type=T_NATIVE` 时必填 |
| limit_payer | 指定支付者 | String | 5 | N | `ADULT`=仅成年人可支付 |

#### wx_data.detail
| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| cost_price | 订单原价 | String | 12 | N | 用于防止同一小票分多次支付享受多次优惠 |
| receipt_id | 商品小票 ID | String | 32 | N | 商家小票 ID |
| goods_detail | 单品列表 | Array | 2048 | Y | 单品信息 JSON 数组 |

#### wx_data.detail.goods_detail[]
| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| goods_id | 商品编码 | String | 32 | N | 商品编码 |
| goods_name | 商品名称 | String | 256 | N | 商品名称 |
| price | 商品单价 | String | 12 | N | 如果商户有优惠，传优惠后单价 |
| quantity | 商品数量 | Int | 11 | N | 用户购买数量 |
| wxpay_goods_id | 微信侧商品编码 | String | 32 | N | 微信侧商品编码 |

#### wx_data.scene_info
| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| store_info | 门店信息 | Object | 2048 | N | 门店信息 |

#### wx_data.scene_info.store_info
| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| id | 门店 ID | String | 32 | N | 门店编号 |
| name | 门店名称 | String | 64 | N | 门店名称 |
| area_code | 门店行政区划码 | String | 6 | N | 门店所在地行政区划码 |
| address | 门店详细地址 | String | 128 | N | 门店详细地址 |

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
    "delay_acct_flag": "Y",
    "req_seq_id": "20240515094131812h3xogy21j9dls6",
    "req_date": "20240515",
    "trans_amt": "0.13",
    "miniapp_data": "{\"need_scheme\":\"Y\",\"seq_id\":\"APP_2022100912694428\",\"private_info\":\"oppsHosting://\"}",
    "huifu_id": "6666000109133323",
    "goods_desc": "app跳微信消费",
    "pre_order_type": "3",
    "notify_url": "https://callback.service.com/xx",
    "acct_split_bunch": "{\"acct_infos\":[{\"huifu_id\":\"6666000109133323\",\"div_amt\":\"0.01\"}]}"
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
| pre_order_id | 预下单订单号 | String | 64 | Y | 预下单订单号 |
| miniapp_data | 微信小程序返回集合 | String(JSON Object) | 2000 | Y | 用于 App/H5/外部网页跳转微信支付 |

#### 同步返回 miniapp_data
| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| gh_id | 小程序原始 ID | String | 64 | N | 小程序原始 ID |
| path | 小程序页面支付路径 | String | 64 | N | 如 `pages/cashier/cashier` |
| scheme_code | 小程序跳转码 | String | 64 | N | `need_scheme=N` 时返回空 |
> 示例可见但未进入官方同步返回参数表的键：`appid`、`need_scheme`、`private_info`、`seq_id`。消费返回时可以兼容读取，但生成字段表、DTO 或校验规则时不要把它们当成官方稳定返回字段。

### 同步成功示例
```json
{
  "data": {
    "resp_code": "00000000",
    "resp_desc": "交易成功",
    "req_date": "20220321",
    "req_seq_id": "20220SQSS63235883",
    "huifu_id": "6666000003100616",
    "trans_amt": "0.13",
    "pre_order_id": "H2023112713461700667284637",
    "miniapp_data": "{\"appid\":\"wxd1b54ceabdfdbd4f\",\"gh_id\":\"gh_1a8554fca417\",\"need_scheme\":\"Y\",\"path\":\"pages/cashier/cashier\",\"private_info\":\"oppsHosting://\",\"scheme_code\":\"weixin://dl/business/?t=f5x3WMhYPat\",\"seq_id\":\"APP_2022033147154783\"}"
  }
}
```

## 异步返回参数
> 交易完成后返回异步；异步回调体为 `resp_data`。

### resp_data
| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| resp_code | 业务返回码 | String | 8 | Y | 业务返回码 |
| resp_desc | 业务返回信息 | String | 512 | Y | 业务返回描述 |
| req_date | 请求时间 | String | 8 | Y | 原样返回，格式 `yyyyMMdd` |
| req_seq_id | 请求流水号 | String | 32 | Y | 文档此处写为 `32` |
| hf_seq_id | 全局流水号 | String | 40 | N | 汇付全局流水号 |
| out_trans_id | 用户账单上的交易订单号 | String | 64 | N | 用户账单交易订单号 |
| party_order_id | 用户账单上的商户订单号 | String | 64 | N | 用户账单商户订单号 |
| huifu_id | 商户号 | String | 32 | Y | 商户号 |
| trans_type | 交易类型 | String | 20 | N | 文档列出的支付类型包括 `T_JSAPI`、`T_MINIAPP`、`A_JSAPI`、`A_NATIVE`、`U_NATIVE`、`U_JSAPI`、`T_MICROPAY`、`A_MICROPAY`、`U_MICROPAY`、`D_NATIVE`、`D_MICROPAY` |
| trans_amt | 交易金额 | String | 12 | N | 单位元，保留两位小数，最低 `0.01` |
| settlement_amt | 结算金额 | String | 16 | N | 单位元，保留两位小数，最低 `0.01` |
| fee_amount | 手续费金额 | String | 16 | N | 单位元，保留两位小数，最低 `0.01` |
| acct_date | 入账时间 | String | 8 | N | `yyyyMMdd` |
| trans_stat | 交易状态 | String | 1 | N | `S`=成功，`F`=失败 |
| end_time | 支付完成时间 | String | 14 | N | `yyyyMMddHHmmss` |
| trans_finish_time | 汇付侧交易完成时间 | String | 6 | N | 文档原表长度列为 `6`，格式说明为 `yyyyMMddHHmmss` |
| debit_flag | 借贷记标识 | String | 1 | N | `D`=借记卡，`C`=信用卡，`Z`=借贷合一卡 |
| wx_user_id | 微信用户唯一标识码 | String | 128 | N | 微信用户唯一标识码 |
| wx_response | 微信返回的响应报文 | String(JSON Object) | 6000 | N | JSON Object 格式 |
| is_div | 是否分账交易 | String | 1 | Y | `1`=分账交易，`0`=非分账交易 |
| acct_split_bunch | 分账对象 | String(JSON Object) | 2048 | N | 分账对象 |
| is_delay_acct | 是否延时交易 | String | 1 | Y | `1`=延迟，`0`=不延迟 |
| fee_flag | 手续费扣款标志 | Int | 1 | N | `1`=外扣，`2`=内扣 |
| trans_fee_allowance_info | 手续费补贴信息 | String(JSON Object) | 6000 | N | JSON Object 格式 |
| fee_formula_infos | 手续费费率信息 | String(JSON Array) | - | N | 微信、支付宝、云闪付交易成功时返回 |
| remark | 备注 | String | 45 | N | 原样返回 |
| bank_code | 通道返回码 | String | 32 | N | 通道返回码 |
| bank_message | 通道返回描述 | String | 200 | N | 通道返回描述 |
| devs_id | 汇付机具号 | String | 32 | Y | 通过汇付报备的机具必传 |

### wx_response
| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| sub_appid | 子商户公众号 ID | String | 32 | N | 微信分配的子商户公众号 ID |
| openid | 用户标识 | String | 128 | Y | 用户在商户 `appid` 下的唯一标识 |
| sub_openid | 用户子标识 | String | 128 | N | 用户在子商户 `appid` 下的唯一标识 |
| bank_type | 付款银行 | String | 16 | Y | 银行类型标识 |
| cash_fee | 现金支付金额 | String | 12 | N | 订单现金支付金额 |
| coupon_fee | 代金券金额 | String | 12 | N | 代金券或立减优惠金额 |
| attach | 商家数据包 | String | 128 | N | 原样返回 |
| promotion_detail | 营销详情列表 | Array | 6000 | N | JSON 数组 |

#### wx_response.promotion_detail[]
| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| promotion_id | 券或者立减优惠 ID | String | 32 | Y | 优惠 ID |
| name | 优惠名称 | String | 64 | N | 优惠名称 |
| scope | 优惠范围 | String | 32 | N | `GLOBAL`=全场代金券，`SINGLE`=单品优惠 |
| type | 优惠类型 | String | 32 | N | `COUPON` 或 `DISCOUNT` |
| amount | 优惠券面额 | String | 5 | Y | 用户享受优惠金额 |
| activity_id | 活动 ID | String | 32 | Y | 微信商户后台配置的批次 ID |
| merchant_contribute | 商户出资 | String | 32 | N | 商户出资金额 |
| other_contribute | 其他出资 | String | 32 | N | 其他出资方金额 |
| goods_detail | 单品列表 | Object | 3000 | N | JSON Object |

#### wx_response.promotion_detail[].goods_detail
| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| goods_id | 商品编码 | String | 32 | Y | 商品编码 |
| goods_remark | 商品备注 | String | 32 | N | 原样返回 |
| discount_amount | 商品优惠金额 | String | 32 | Y | 单位元 |
| quantity | 商品数量 | String | 32 | Y | 商品数量 |
| price | 商品价格 | String | 32 | Y | 单位元 |

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
| cur_allowance_config_infos | 手续费补贴活动详情 | Array | - | N | 补贴系统返回，斗拱原样返回 |

#### trans_fee_allowance_info.cur_allowance_config_infos
| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| acct_id | 门店 | String | 64 | N | 门店标识 |
| merchant_group | 商户号 | String | 64 | N | 商户号 |
| allowance_sys | 补贴方 | String | 64 | N | `1`=银行，`2`=服务商，`3`=汇来米 |
| allowance_sys_id | 补贴方 ID | String | 64 | N | 补贴方 ID |
| is_delay_allowance | 补贴类型 | String | 2 | N | `1`=实补，`2`=后补 |
| market_id | 自定义活动编号 | String | 64 | N | 自定义活动编号 |
| market_name | 自定义活动名称 | String | 128 | N | 自定义活动名称 |
| market_desc | 自定义活动描述 | String | 64 | N | 自定义活动描述 |
| start_time | 活动开始时间 | String | 8 | N | `yyyyMMdd` |
| end_time | 活动结束时间 | String | 8 | N | `yyyyMMdd` |
| pos_debit_limit_amt | POS 借记卡补贴额度 | String | 16 | N | 单位元 |
| pos_credit_limit_amt | POS 贷记卡补贴额度 | String | 16 | N | 单位元 |
| pos_limit_amt | POS 补贴额度 | String | 16 | N | 单位元 |
| qr_limit_amt | 扫码补贴额度 | String | 16 | N | 单位元 |
| total_limit_amt | 活动总补贴额度 | String | 16 | N | 单位元 |
| status | 活动是否有效 | String | 4 | N | `1`=生效，`0`=失效 |
| human_flag | 是否人工操作 | String | 4 | N | `N`=自动，`Y`=人工 |
| activity_id | 活动号 | String | 64 | N | 活动号 |
| activity_name | 活动描述 | String | 128 | N | 活动描述 |
| create_by | 创建人 | String | 32 | N | 创建人 |
| create_time | 创建时间 | String | 32 | N | 创建时间 |
| update_time | 更新时间 | String | 32 | N | 更新时间 |

### fee_formula_infos[]
| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| fee_formula | 手续费计算公式 | String | 512 | Y | 手续费计算公式 |
| fee_type | 手续费类型 | String | 32 | Y | `TRANS_FEE` 或 `ACCT_FEE` |
| huifu_id | 商户号 | String | 32 | N | 补贴支付账户补贴时，补贴账户的 `huifu_id` |
| fee_sign | 手续费场景标识 | String | 32 | N | 微信/支付宝交易手续费场景标识码 |

## 拆单支付异步返回参数
> 拆单支付成功时返回该异步；异步回调体为 `resp_data`。

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| resp_code | 业务返回码 | String | 8 | Y | 业务返回码 |
| resp_desc | 业务返回信息 | String | 512 | Y | 业务返回描述 |
| huifu_id | 商户号 | String | 32 | Y | 商户号 |
| req_date | 请求时间 | String | 8 | Y | 原样返回，格式 `yyyyMMdd` |
| req_seq_id | 请求流水号 | String | 32 | Y | 原样返回 |
| trans_stat | 交易状态 | String | 1 | Y | `S`=成功，`F`=失败 |
| sys_id | 系统号 | String | 32 | Y | 渠道商/商户的 `huifu_id` |

## 业务返回码
| 返回码 | 返回描述 | 处理 |
|--------|----------|------|
| 90000000 | 生成微信 Scheme 失败，`access_token` 无效或不是最新 | 小程序有变更或被微信封禁，需要重新配置 |
| 99010002 | 预下单请求流水重复 | 提供新的 `req_seq_id` |

## 文档勘误与实现备注
- 请求示例里出现了 `checkout_id`，但参数表没有定义该字段；当前 skill 不将其视为正式接入参数。
- 异步字段 `trans_finish_time` 的长度列写为 `6`，但格式说明为 `yyyyMMddHHmmss`；实现时按 14 位时间串处理更合理。
- 主异步与拆单异步中的 `req_seq_id` 长度列写为 `32`，但请求参数表与同步返回都写为 `64`；当前按官方原表保留并显式记录该冲突。
- 同步返回 `miniapp_data` 的官方子表只定义了 `gh_id`、`path`、`scheme_code`；官方成功示例还出现了 `appid`、`need_scheme`、`private_info`、`seq_id`，当前只作为示例可见键记录，不能升级成官方稳定字段。
- `wx_response`、`trans_fee_allowance_info` 在父表中写成 `String` 且说明为 JsonObject/JsonArray，同时又展开了子字段；当前文档按“JSON 字符串承载对象/数组”的方式描述。
