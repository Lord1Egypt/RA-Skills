# 聚合扫码交易查询

## 目录

- [接口概览](#接口概览)
- [SDK 映射](#sdk-映射)
- [公共参数](#公共参数)
- [请求参数](#请求参数)
- [同步返回参数](#同步返回参数)
- [扩展返回参数](#扩展返回参数)
- [请求示例](#请求示例)
- [返回示例](#返回示例)
- [业务返回码](#业务返回码)
- [实现备注与文档勘误](#实现备注与文档勘误)

## 接口概览

| 项 | 值 |
| --- | --- |
| 接口名称 | 扫码交易查询 |
| 汇付端点 | `POST /v4/trade/payment/scanpay/query` |
| 官方最近更新时间 | `2026-05-28` |
| 支持格式 | `JSON` |
| 适用场景 | 异步通知未收到、反扫返回处理中、支付结果二次确认 |
| 支持交易类型 | `T_JSAPI`、`T_MINIAPP`、`T_APP`、`A_JSAPI`、`A_NATIVE`、`U_JSAPI`、`U_NATIVE`、`T_MICROPAY`、`A_MICROPAY`、`U_MICROPAY` |
| 签名说明 | [接入指引-开发指南](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |

服务商/商户系统因网络原因未收到交易状态时，可主动调用本接口查询订单状态。官方描述同时覆盖微信、支付宝、银联二维码的正扫、JS、小程序、APP、反扫场景。

## SDK 映射

| 项 | 值 |
| --- | --- |
| SDK Request 类 | `TradePaymentScanpayQueryRequest` |
| 包路径 | `com.huifu.dg.lightning.models.payment` |
| SDK Client 方法 | `Factory.Payment.Common().query(request)` |

`TradePaymentScanpayQueryRequest` 常用字段映射：

| 字段 | setter | 必填 | 说明 |
| --- | --- | --- | --- |
| `huifu_id` | `setHuifuId()` | Y | 汇付商户号 |
| `req_date` | `setReqDate()` | C | 请求日期，`yyyyMMdd` |
| `out_ord_id` | `setOutOrdId()` | C | 汇付服务订单号，三选一 |
| `hf_seq_id` | `setHfSeqId()` | C | 汇付全局流水号，三选一 |
| `req_seq_id` | `setReqSeqId()` | C | 创建服务订单请求流水号，三选一 |

## 公共参数

### 公共请求参数

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `sys_id` | String | 32 | Y | 渠道商/代理商/商户的 `huifu_id` |
| `product_id` | String | 32 | Y | 汇付分配的产品号，例如 `MCS` |
| `sign` | String | 512 | Y | 请求签名 |
| `data` | JSON | - | Y | 业务请求参数 |

> 强制请求头约束：
> - 必须带 `jpt-x-skill-source: <skill_source>`
> - 如果当前按 PHP 接入，由于本页请求 `data` 明确包含 `huifu_id`，还必须带 `jpt-x-skill-huifu_id: <data.huifu_id>`
> - 当前 Skill 包对齐的官方 PHP SDK 主链路在 `MerConfig.skill_source` 已配置时，会自动带 `jpt-x-skill-source`，并在当前请求 `huifu_id` 存在且非空时自动带 `jpt-x-skill-huifu_id`
> - 当前 Java SDK 基线也会在请求 `data` 明确包含 `huifu_id` 时自动带 `jpt-x-skill-huifu_id: <data.huifu_id>`
> - 这两项属于 HTTP 请求头，不要写进 `data`；完整口径见 `references/shared-request-header-policy.md`

### 公共返回参数

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `sign` | String | 512 | Y | 响应签名 |
| `data` | JSON | - | N | 业务返回体 |

## 请求参数

### `data`

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `huifu_id` | String | 32 | Y | 汇付商户号 |
| `req_date` | String | 8 | C | 请求日期，格式 `yyyyMMdd`，以北京时间为准 |
| `out_ord_id` | String | 32 | C | 汇付服务订单号，`out_ord_id`、`hf_seq_id`、`req_seq_id` 三选一 |
| `hf_seq_id` | String | 128 | C | 创建服务订单返回的汇付全局流水号，三选一 |
| `req_seq_id` | String | 128 | C | 服务订单创建请求流水号，三选一 |

### 查询键规则

- `out_ord_id`、`hf_seq_id`、`req_seq_id` 不能同时为空。
- `req_date` 在官方文档中标记为条件必填；实务上建议在使用 `req_seq_id` 查询时一并传入。
- 交易最终结果以响应中的 `trans_stat` 为准，不以 `resp_code=00000000` 直接判定支付成功。

## 同步返回参数

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `resp_code` | String | 8 | Y | 业务响应码，见[业务返回码](#业务返回码) |
| `resp_desc` | String | 512 | Y | 业务响应信息 |
| `huifu_id` | String | 32 | Y | 商户号 |
| `req_date` | String | 8 | Y | 请求日期，格式 `yyyyMMdd` |
| `hf_seq_id` | String | 128 | N | 汇付全局流水号 |
| `req_seq_id` | String | 128 | N | 请求流水号，同一商户号当天唯一 |
| `out_trans_id` | String | 64 | N | 用户账单上的交易订单号 |
| `party_order_id` | String | 64 | N | 用户账单上的商户订单号 |
| `trans_amt` | String | 14 | Y | 交易金额，单位元，保留两位小数 |
| `settlement_amt` | String | 14 | N | 结算金额，单位元 |
| `unconfirm_amt` | String | 14 | N | 待确认总金额，单位元 |
| `trade_type` | String | 16 | N | 交易类型，见接口概览 |
| `trans_stat` | String | 1 | N | `P` 处理中，`S` 成功，`F` 失败，`I` 初始 |
| `end_time` | String | 14 | N | 支付完成时间，14 位时间串 |
| `delay_acct_flag` | String | 1 | Y | `Y` 延时交易，`N` 非延时交易 |
| `acct_id` | String | 9 | N | 商户账户号 |
| `acct_date` | String | 8 | N | 账务日期，格式 `yyyyMMdd` |
| `acct_stat` | String | 1 | N | `I` 初始，`P` 处理中，`S` 成功，`F` 失败 |
| `debit_type` | String | 1 | N | `D` 借记卡，`C` 信用卡，`Z` 借贷合一卡，`O` 其他 |
| `wx_user_id` | String | 128 | N | 微信用户唯一标识码 |
| `div_flag` | String | 1 | Y | `Y` 分账交易，`N` 非分账交易 |
| `remark` | String | 255 | N | 原样返回 |
| `device_type` | String | 2 | N | 终端类型，`01` 智能POS，`02` 扫码POS，`03` 云音箱，`04` 台牌，`05` 云打印，`06` 扫脸设备，`07` 收银机，`08` 收银助手，`09` 传统POS，`10` 一体音箱，`11` 虚拟终端 |
| `bank_message` | String | 200 | N | 外部通道返回描述 |
| `atu_sub_mer_id` | String | 32 | N | ATU 真实商户号 |
| `freeze_time` | String | 14 | Y | 冻结时间，14 位时间串 |
| `unfreeze_amt` | String | 14 | Y | 解冻金额，单位元 |
| `unfreeze_time` | String | 14 | Y | 解冻时间，14 位时间串 |
| `fund_freeze_stat` | String | 16 | N | `FREEZE` 冻结，`UNFREEZE` 解冻 |
| `method_expand` | String | - | N | 交易类型扩展参数，JSON 字符串 |
| `tx_metadata` | String | - | N | 扩展参数集合，JSON 字符串 |
| `payment_fee` | String | - | N | 手续费对象，JSON 字符串 |
| `combinedpay_fee_amt` | String | 14 | N | 官方成功示例出现的顶层兼容字段，表示补贴支付手续费金额；优先按 `tx_metadata.combinedpay_data_fee_info` / `payment_fee` 解析结构化信息 |

## 扩展返回参数

### `method_expand`

`method_expand` 为一个 JSON Object 字符串。官方参数表按 `trade_type` 显式列出 `T_JSAPI`、`T_MINIAPP`、`T_APP`、`T_MICROPAY`、`A_JSAPI`、`A_NATIVE`、`A_MICROPAY`、`U_JSAPI`、`U_NATIVE`、`U_MICROPAY` 等包装行；这些行是文档场景分组，不是线上返回的 key。对 `method_expand` 只解码一次，渠道字段直接位于解码后对象的根层。例如支付宝场景读取 `$.buyer_logon_id`，不得读取 `$.A_JSAPI.buyer_logon_id`，也不得对 `A_JSAPI` 再做第二次 JSON 解码。

解析和路由必须遵守以下边界：

- 线上字段名是 `response.data.trade_type`；若业务 DTO 使用 `pay_type` 等别名，必须保留原始 `trade_type` 并显式映射。真实报文只有 `pay_type` 时按合同漂移处理，不得直接据此路由。
- 对 `method_expand` 做且只做一次严格 JSON Object 解码；中间件已预解码成 Object 时可直接进入同一字段读取逻辑，但必须记录原始类型。出现 `A_JSAPI` 等场景包装 key 时按合同漂移处理，不得把官网展示分组固化为 DTO 层级。
- 非法 JSON、解码后不是 Object、超过本地大小或嵌套深度限制时必须显式报解析错误，不得回退为空对象。保留原始值和规范化视图，禁止用重新序列化结果覆盖原始审计证据。
- 路由只对接口概览中的正式枚举做精确匹配。支付宝付款码交易的正式值是 `A_MICROPAY`；当前官网成功示例已经使用该正确值。参数说明仍把支付宝付款码重复写成 `A_NATIVE`，该行按已确认勘误解释为 `A_MICROPAY`。真实线上响应若出现其他拼写，保留原值并按合同漂移告警，不得静默改写后掩盖证据。
- `buyer_logon_id` 属于账号信息，不得写入普通日志；其他未知键只在受控扩展 map 中原样保留，不能驱动结算、退款或渠道特有核心逻辑。

#### 微信类交易

适用 `T_JSAPI`、`T_MINIAPP`、`T_APP`、`T_MICROPAY`。

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `sub_openid` | String | 16 | N | 用户在子商户 appid 下的唯一标识 |
| `openid` | String | 128 | N | 用户在商户 appid 下的唯一标识 |
| `cash_fee` | String | 14 | N | 现金支付金额，单位元 |
| `attach` | String | 128 | N | 商家数据包，原样返回 |
| `coupon_fee` | String | 14 | N | 代金券或立减优惠金额，单位元 |
| `promotion_detail` | Array | 6000 | N | 营销详情列表 |
| `bank_type` | String | 16 | N | 付款银行，参见微信银行类型说明 |
| `sub_appid` | String | 32 | N | 商户公众号或小程序 APPID |
| `device_info` | String | 32 | N | 交易终端设备信息 |

`promotion_detail` 字段：

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `activity_id` | String | 32 | Y | 微信商户后台配置的批次 ID |
| `amount` | String | 5 | Y | 用户享受优惠金额 |
| `promotion_id` | String | 32 | Y | 券或立减优惠 ID |
| `goods_detail` | Array | 3000 | N | 单品信息 |
| `merchant_contribute` | String | 32 | N | 商户出资金额 |
| `name` | String | 64 | N | 优惠名称 |
| `other_contribute` | String | 32 | N | 其他出资方金额 |
| `scope` | String | 32 | N | `GLOBAL` 全场券，`SINGLE` 单品优惠 |
| `type` | String | 32 | N | `COUPON` 代金券，`DISCOUNT` 优惠券 |

`goods_detail` 字段：

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `discount_amount` | String | 32 | Y | 商品优惠金额，单位元 |
| `goods_id` | String | 32 | Y | 商品编码 |
| `price` | String | 32 | Y | 商品价格，单位元 |
| `quantity` | String | 32 | Y | 商品数量 |
| `goods_remark` | String | 32 | N | 商品备注 |

#### 支付宝类交易

适用 `A_JSAPI`、`A_NATIVE`、`A_MICROPAY`。

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `buyer_id` | String | 28 | N | 买家支付宝用户号 |
| `buyer_logon_id` | String | 100 | N | 买家支付宝账号 |
| `fund_bill_list` | Array | 2048 | N | 交易支付使用的资金渠道 |
| `hb_fq_num` | String | 10 | N | 花呗分期数 |
| `voucher_detail_list` | Array | 2048 | N | 本交易使用的所有优惠券信息 |

##### 成功样例专属兼容键（参数表未定义）

锁定官网成功样例的 `response.data.method_expand` 还出现 `buyer_pay_amount`、`buyer_user_id`、`invoice_amount`、`point_amount`、`send_pay_date`，但响应参数表没有定义这五个键的类型、长度、必填性或稳定性。它们只能按“样例可见、表未定义”的兼容扩展保留：解析器可以忽略未知键或在扩展 map 中原样保存，固定 DTO、校验器和业务判断不得依赖这些键；需要正式使用时标记 `[需要官方确认]`。

`fund_bill_list` 字段：

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `bank_code` | String | 10 | N | 银行卡支付时的银行代码 |
| `amount` | String | 32 | N | 该支付工具使用金额，单位元 |
| `fund_channel` | String | 32 | N | 交易使用的资金渠道 |
| `fund_type` | String | 32 | N | `BANKCARD` 渠道下返回，`DEBIT_CARD`、`CREDIT_CARD`、`MIXED_CARD` |
| `real_amount` | String | 11 | N | 渠道实际付款金额，单位元 |

`voucher_detail_list` 字段：

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `amount` | String | 32 | Y | 优惠券面额，单位元 |
| `id` | String | 32 | Y | 券 ID |
| `name` | String | 32 | Y | 券名称 |
| `type` | String | 32 | Y | `COUPON` 代金券，`DISCOUNT` 优惠券 |
| `merchant_contribute` | String | 32 | N | 商家出资金额，单位元 |
| `other_contribute` | String | 14 | N | 其他出资方金额，单位元 |

#### 银联类交易

适用 `U_JSAPI`、`U_NATIVE`、`U_MICROPAY`。

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `coupon_info` | Array | - | N | 银联优惠信息 |
| `acc_no` | String | 40 | N | 付款方卡号/账号/Token |

`coupon_info` 字段：

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `type` | String | 4 | Y | `DD01` 随机立减，`CP01` 无需领取抵金券，`CP02` 事前领取抵金券 |
| `spnsrId` | String | 20 | Y | 出资方，`00010000` 表示银联出资 |
| `offstAmt` | String | 14 | Y | 抵消交易金额，不能为全 0 |
| `id` | String | 40 | N | 项目编号 |
| `desc` | String | 40 | N | 项目简称 |
| `addnInfo` | String | 100 | N | 附加信息 |

### `tx_metadata`

`tx_metadata` 为扩展参数集合，通常在分账、补贴、手续费补贴、设备信息场景下返回。

| 参数 | 定义 | 说明 |
| --- | --- | --- |
| `acct_split_bunch` | Object | 分账对象 |
| `combinedpay_data` | Array | 补贴支付信息 |
| `combinedpay_data_fee_info` | Object | 补贴支付手续费信息 |
| `trans_fee_allowance_info` | Object | 手续费补贴信息 |
| `terminal_device_data` | Object | 设备信息 |

`acct_split_bunch` 字段：

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `acct_infos` | Array | 4000 | Y | 分账明细 |
| `is_clean_split` | String | 1 | N | `Y` 使用净值分账，仅在 `percentage_flag=Y` 时生效 |

`acct_infos` 字段：

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `div_amt` | String | 14 | Y | 分账金额，单位元 |
| `huifu_id` | String | 32 | Y | 分账接收方 ID |
| `acct_id` | String | 9 | N | 分账接收方子账户 |

`combinedpay_data` 字段：

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `huifu_id` | String | 32 | Y | 补贴方汇付商户号 |
| `user_type` | String | 32 | Y | `channel` 渠道，`agent` 代理 |
| `acct_id` | String | 32 | Y | 营销补贴方账户号 |
| `amount` | String | 14 | Y | 补贴金额，单位元 |

`combinedpay_data_fee_info` 字段：

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `huifu_id` | String | 32 | Y | 补贴支付手续费承担方汇付编号 |
| `acct_id` | String | 32 | Y | 补贴支付手续费承担方账户号 |
| `combinedpay_fee_amt` | String | 14 | Y | 补贴支付手续费金额，单位元 |

`trans_fee_allowance_info` 字段：

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `actual_fee_amt` | String | 14 | Y | 商户实收手续费 |
| `allowance_fee_amt` | String | 14 | Y | 补贴手续费 |
| `allowance_type` | String | 1 | Y | `0` 不补贴，`1` 补贴，`2` 部分补贴，`3` 全额补贴(优惠后)，`4` 部分补贴(优惠后) |
| `cur_allowance_config_infos` | Object | - | N | 手续费补贴活动详情 |
| `no_allowance_desc` | String | 128 | Y | 不补贴原因编码说明 |
| `receivable_fee_amt` | String | 14 | Y | 商户应收手续费 |

`cur_allowance_config_infos` 字段：

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `merchant_group` | String | 64 | N | 商户号 |
| `acct_id` | String | 64 | N | 门店 |
| `activity_id` | String | 64 | Y | 活动号 |
| `activity_name` | String | 128 | N | 活动描述 |
| `status` | String | 4 | Y | `1` 生效，`0` 失效 |
| `total_limit_amt` | String | 16 | Y | 活动总补贴额度 |
| `start_time` | String | 8 | Y | 开始日期，`yyyyMMdd` |
| `end_time` | String | 8 | Y | 结束日期，`yyyyMMdd` |
| `human_flag` | String | 4 | Y | `N` 自动，`Y` 人工 |
| `allowance_sys` | String | 64 | Y | `1` 银行，`2` 服务商，`3` 汇来米 |
| `allowance_sys_id` | String | 64 | Y | 补贴方 ID |
| `is_delay_allowance` | String | 2 | Y | `1` 实补，`2` 后补 |
| `is_share` | String | 4 | N | 是否共享额度 |
| `market_id` | String | 64 | Y | 自定义活动编号 |
| `market_name` | String | 128 | N | 自定义活动名称 |
| `market_desc` | String | 64 | N | 自定义活动描述 |
| `pos_credit_limit_amt` | String | 16 | Y | POS 贷记卡补贴额度 |
| `pos_debit_limit_amt` | String | 16 | Y | POS 借记卡补贴额度 |
| `pos_limit_amt` | String | 16 | Y | POS 补贴额度 |
| `qr_limit_amt` | String | 16 | Y | 扫码补贴额度 |
| `create_by` | String | 32 | Y | 创建人 |
| `create_time` | String | 32 | Y | 创建时间 |
| `update_time` | String | 32 | Y | 更新时间 |

`terminal_device_data` 字段：

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `terminal_ip` | String | 64 | N | 交易设备公网 IP |
| `terminal_location` | String | 32 | N | 终端实时经纬度，格式 `纬度/经度` |

### `payment_fee`

`payment_fee` 为手续费对象。

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `fee_huifu_id` | String | 32 | N | 手续费商户号 |
| `fee_formula_infos` | Array | - | N | 手续费费率信息，交易成功时返回 |
| `fee_flag` | String | 1 | N | `1` 外扣，`2` 内扣 |
| `fee_amount` | String | 14 | N | 手续费金额，单位元 |

`fee_formula_infos` 字段：

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `fee_formula` | String | 512 | N | 手续费计算公式 |
| `fee_type` | String | 32 | N | `TRANS_FEE` 交易手续费，`ACCT_FEE` 组合支付账户补贴手续费 |
| `huifu_id` | String | 32 | N | 组合支付账户补贴时的补贴账户 `huifu_id` |

## 请求示例

```json
{
  "sys_id": "6666000003100616",
  "product_id": "MYPAY",
  "data": {
    "hf_seq_id": "0029000topA250804164235P330c0a8200900000",
    "huifu_id": "6666000003100616"
  },
  "sign": "<SDK_AUTOGENERATED_SIGNATURE>"
}
```

## 返回示例

```json
{
  "data": {
    "atu_sub_mer_id": "2088641544658593",
    "bank_message": "处理成功",
    "delay_acct_flag": "N",
    "div_flag": "N",
    "end_time": "20250804164236",
    "hf_seq_id": "0029000topA250804164235P330c0a8200900000",
    "huifu_id": "6666000003100616",
    "method_expand": "{\"buyer_logon_id\":\"131******66\",\"buyer_pay_amount\":\"0.00\",\"buyer_user_id\":\"2088052888888888283\",\"invoice_amount\":\"0.00\",\"point_amount\":\"0.00\",\"send_pay_date\":\"2025-08-04 16:42:36\"}",
    "out_trans_id": "2025080422001478281403316633",
    "party_order_id": "2508046015554200132",
    "payment_fee": "{\"fee_amount\":\"0.01\",\"fee_formula_infos\":[{\"fee_formula\":\"AMT*0.38\",\"fee_type\":\"TRANS_FEE\"}]}",
    "remark": "聚合反扫消费",
    "req_date": "20250804",
    "req_seq_id": "202508040442356120",
    "resp_code": "00000000",
    "resp_desc": "查询成功",
    "settlement_amt": "0.03",
    "trade_type": "A_MICROPAY",
    "trans_amt": "0.03",
    "trans_stat": "S",
    "freeze_time": "20091225091010",
    "unfreeze_amt": "1.23",
    "unfreeze_time": "20091225091010"
  }
}
```

## 业务返回码

| 返回码 | 返回描述 |
| --- | --- |
| `10000000` | 请求内容体不能为空 / 参数不能为空 / 长度不合法 / 枚举不存在 / 格式不正确 |
| `21000000` | 原机构请求流水号、交易返回全局流水号、用户账单商户订单号、用户账单交易订单号、外部订单号、终端订单号不能同时为空 |
| `22000000` | 产品号不存在 |
| `22000000` | 产品状态异常 |
| `23000001` | 交易不存在 |
| `91111119` | 通道异常，请稍后重试 |
| `98888888` | 系统错误 |

## 实现备注与文档勘误

1. 官方成功示例已把 `trade_type` 修正为 `A_MICROPAY`；参数说明仍把支付宝付款码重复写成 `A_NATIVE`。生成请求、DTO 枚举、校验器和业务路由必须使用 `A_MICROPAY`。若线上响应出现其他拼写，保留原始值并按合同漂移告警。
2. 官方“应用场景”段出现 `U_JSAP` 拼写，结合参数表与上下文应按 `U_JSAPI` 处理。
3. 官方时间格式在 `end_time`、`freeze_time`、`unfreeze_time` 等位置混用了 `yyyyMMddHHMMSS`；实现中建议统一按 14 位时间串 `yyyyMMddHHmmss` 解析。
4. `method_expand`、`tx_metadata`、`payment_fee` 均为 JSON 字符串，不是外层响应里的嵌套对象；落库或读取子字段前应先反序列化。其中 `method_expand` 解码后为单层平铺对象，文档里的渠道包装行不参与解码。
5. 查询成功只代表“查询动作成功”，交易成败仍要看 `trans_stat`。当 `trans_stat=P` 时应按业务轮询；当 `trans_stat=I` 时建议联系汇付支持排查。
6. `freeze_time`、`unfreeze_amt`、`unfreeze_time` 在最新官方参数表中必填列为 `Y`；即使官方返回示例未展示，生成字段清单和 DTO 时也不要降级成 `N`。
