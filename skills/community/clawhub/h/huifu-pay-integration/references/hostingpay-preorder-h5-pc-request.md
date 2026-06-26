# H5、PC 预下单请求参数

> 对应接口：`POST /v2/trade/hosting/payment/preorder`，`pre_order_type=1`。本文件覆盖公共请求参数、`data` 顶层字段，以及 `acct_split_bunch`、`hosting_data`、`biz_info` 三组嵌套对象。


## 目录

- 公共请求参数
- `data` 顶层字段
- `trans_type` 支持值
- 顶层字段约束
- `acct_split_bunch`
- `hosting_data`
- `biz_info`
- 实现备注

## 公共请求参数

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `sys_id` | 系统号 | String | 32 | Y | 渠道商或商户的 `huifu_id`；渠道商主体传渠道商号，直连商户主体传商户号 |
| `product_id` | 产品号 | String | 32 | Y | 汇付分配的产品号，例如 `YYZY` |
| `sign` | 加签结果 | String | 512 | Y | 对整个报文签名 |
| `data` | 请求数据 | JSON | - | Y | 业务请求参数 |

> 强制请求头约束：
> - 必须带 `jpt-x-skill-source: <skill_source>`
> - 如果当前按 PHP 接入，由于本页请求 `data` 明确包含 `huifu_id`，还必须带 `jpt-x-skill-huifu_id: <data.huifu_id>`
> - 当前 Skill 包对齐的官方 PHP SDK 主链路在 `MerConfig.skill_source` 已配置时，会自动带 `jpt-x-skill-source`，并在当前请求 `huifu_id` 存在且非空时自动带 `jpt-x-skill-huifu_id`
> - 当前 Java SDK 基线也会在请求 `data` 明确包含 `huifu_id` 时自动带 `jpt-x-skill-huifu_id: <data.huifu_id>`
> - 这两项属于 HTTP 请求头，不要误写进 `data`；完整口径见 `references/shared-request-header-policy.md`

## `data` 顶层字段

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `req_date` | 请求日期 | String | 8 | Y | 格式 `yyyyMMdd` |
| `req_seq_id` | 请求流水号 | String | 64 | Y | 同一 `huifu_id` 下当天唯一 |
| `huifu_id` | 商户号 | String | 32 | Y | 商户开户自动生成 |
| `acct_id` | 收款汇付账户号 | String | 32 | N | 仅支持基本户、现金户；不传默认基本户；仅微信、支付宝、网银支持指定收款账户 |
| `trans_amt` | 交易金额 | String | 14 | Y | 单位元，保留 2 位小数，最低 `0.01` |
| `goods_desc` | 商品描述 | String | 40 | Y | 商品描述 |
| `pre_order_type` | 预下单类型 | String | 1 | Y | H5/PC 固定为 `1` |
| `delay_acct_flag` | 是否延迟交易 | String | 1 | N | `Y`=延迟，`N`=不延迟；默认 `N` |
| `multi_pay_way_flag` | 是否支持切换支付方式 | String | 1 | N | `Y`=支持切换，`N`=不支持；默认 `N` |
| `acct_split_bunch` | 分账对象 | String | 2000 | N | JSON 对象字符串 |
| `hosting_data` | 统一收银台扩展参数集合 | String | 2000 | Y | JSON 对象字符串 |
| `time_expire` | 交易失效时间 | String | 14 | N | 格式 `yyyyMMddHHmmss`；默认 10 分钟 |
| `biz_info` | 业务信息 | String | 2000 | N | JSON 对象字符串 |
| `notify_url` | 交易异步通知地址 | String | 512 | N | `http` 或 `https` 开头；交易成功或失败时触发 |
| `usage_type` | 使用类型 | String | 1 | N | `P`=支付，默认；`R`=充值 |
| `trans_type` | 交易类型 | String | 256 | N | 单个值直达支付页，多个值或不传进入收银台 |
| `wx_data` | 微信参数集合 | String | 2048 | N | JSON 对象字符串 |
| `alipay_data` | 支付宝参数集合 | String | 2048 | N | JSON 对象字符串 |
| `dy_data` | 抖音参数集合 | String | 2048 | N | JSON 对象字符串 |
| `unionpay_data` | 银联参数集合 | String | 2048 | N | JSON 对象字符串 |
| `terminal_device_data` | 设备信息 | String | 2048 | N | JSON 对象字符串 |
| `largeamt_data` | 大额支付参数集合 | String | 2500 | N | JSON 对象字符串 |
| `fee_sign` | 手续费场景标识 | String | 32 | N | 微信、支付宝交易时生效；不传时走商户默认费率 |
| `fee_split_flag` | 是否交易手续费分摊 | String | 1 | N | `Y`=分摊，`N`=不分摊；不传默认 `N` |
| `fee_flag` | 手续费扣款标志 | String | 1 | N | `1`=外扣，`2`=内扣；默认取控台配置 |

## `trans_type` 支持值

| 值 | 含义 | 场景 |
|----|------|------|
| `T_JSAPI` | 微信公众号支付 | PC、H5 |
| `A_JSAPI` | 支付宝 JS | PC、H5 |
| `A_NATIVE` | 支付宝正扫 | PC、H5 |
| `U_NATIVE` | 银联正扫 | PC、H5 |
| `U_JSAPI` | 银联 JS | PC、H5 |
| `ONLINE_PAY_B2B` | B2B 网银支付 | PC |
| `ONLINE_PAY_B2C` | B2C 网银支付 | PC |
| `QUICK_PAY` | 快捷支付 | PC、H5 |
| `LARGE_PAY` | 备付金下单模式 | PC、H5 |
| `Y_H5` | 抖音 H5 支付 | H5 |

## 顶层字段约束

- `multi_pay_way_flag=Y` 时，用户选定一种支付方式后仍可切换到其他支付方式。
- 若启用支付方式切换，对账可选两种主键策略：
  - 以支付成功返回的 `hf_seq_id` 作为唯一标识。
  - 仍以请求流水号作为唯一标识时，解析账单需忽略请求流水号中 `-` 及其后缀。
- `time_expire` 为空时默认 10 分钟，超时后用户仍可能支付成功，最终状态要以异步通知或主动查询为准。
- `notify_url` 正常情况下只回调一次，但仍应按幂等处理。
- `notify_url` 还需满足官方托管产品文档的 URL 规则：只允许 `http/https`、不支持重定向、URL 不带参数、自定义端口在 `8000-9005`、收到回调后返回 `200`。

## `acct_split_bunch`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `acct_infos` | 分账明细 | Array | - | N | 分账明细数组 |
| `percentage_flag` | 百分比分账标志 | String | 1 | N | `Y`=按百分比分账 |
| `is_clean_split` | 是否净值分账 | String | 1 | N | `Y`=净值分账；仅在手续费内扣且按百分比分账时生效 |

### `acct_split_bunch.acct_infos[]`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `div_amt` | 分账金额 | String | 14 | N | 单位元，保留 2 位小数；支持传 `0.00` |
| `huifu_id` | 分账接收方 ID | String | 32 | N | 斗拱开户时生成 |
| `acct_id` | 收款汇付账户号 | String | 32 | N | 仅支持基本户、现金户；不传默认基本户 |
| `percentage_div` | 分账百分比 | String | 6 | N | 仅 `percentage_flag=Y` 时生效；所有比例之和必须为 `100.00` |

## `hosting_data`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `project_title` | 项目标题 | String | 64 | Y | 用于账单页面展示 |
| `project_id` | 托管项目号 | String | 32 | Y | 商户创建的统一收银台托管项目号 |
| `private_info` | 商户私有信息 | String | 255 | N | 异步通知和主动查询接口中的 `remark` 原样返回 |
| `callback_url` | 回调地址 | String | 512 | N | 支付成功后跳转回该地址；不填则停留当前页面 |
| `request_type` | 请求类型 | String | 1 | C | `P`=PC 页面版，默认；`M`=H5 页面版；指定 `trans_type` 时必填 |

`hosting_data` 实现约束：

- `project_id` 必须来自合作伙伴控台里真实创建并留存的托管项目号。
- 指定单一 `trans_type` 时，建议显式传 `request_type`，避免默认按 PC 页面处理。
- `callback_url` 仅作前端回跳地址，不可作为支付成功依据。

## `biz_info`

| 参数 | 中文名 | 类型 | 必填 | 说明 |
|------|--------|------|------|------|
| `payer_check_ali` | 付款人验证（支付宝） | Object | N | 支付宝特殊交易需校验买家信息 |
| `payer_check_wx` | 付款人验证（微信） | Object | N | 微信实名支付场景校验买家信息 |
| `person_payer` | 个人付款人信息 | Object | N | 开启付款人验证后可传 |

### `biz_info.payer_check_ali`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `need_check_info` | 是否提供校验身份信息 | String | 1 | N | `T`=强制校验，需要填写 `person_payer`；`F`=不强制 |
| `min_age` | 允许的最小买家年龄 | String | 3 | N | 仅 `need_check_info=T` 时有效；必须是大于等于 `0` 的整数 |
| `fix_buyer` | 是否强制校验付款人身份信息 | String | 8 | N | `T`=强制校验，`F`=不强制 |

### `biz_info.payer_check_wx`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `limit_payer` | 指定支付者 | String | 5 | N | `ADULT` 表示仅成年人允许支付 |
| `real_name_flag` | 微信实名验证 | String | 1 | N | `Y/N`，默认 `N` |

### `biz_info.person_payer`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `name` | 姓名 | String | 16 | N | 支付宝 `need_check_info=T` 时有效 |
| `cert_type` | 证件类型 | String | 32 | N | `IDENTITY_CARD`、`PASSPORT`、`OFFICER_CARD`、`SOLDIER_CARD`、`HOKOU`；微信仅支持身份证 |
| `cert_no` | 证件号 | String | 64 | N | 需要密文传输，使用汇付 RSA 公钥加密 |
| `mobile` | 手机号 | String | 20 | N | 支付宝字段；官方文档说明当前暂不校验 |

## 实现备注

- `acct_split_bunch`、`hosting_data`、`biz_info` 在官方文档中都属于“字符串承载 JSON”类型，传参时不要直接把对象塞给 SDK。
- `request_type` 实际上用于区分 PC 页面版和 H5 页面版；如果已经指定了单一 `trans_type`，建议显式传值，避免汇付侧按默认 PC 逻辑处理。
- `person_payer.cert_no`、后文的 `largeamt_data.bank_card_no` 都涉及加密，接入时应复用 base skill 中的 RSA 工具链。
