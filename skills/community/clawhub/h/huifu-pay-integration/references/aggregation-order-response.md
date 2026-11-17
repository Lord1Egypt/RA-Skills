# 聚合下单返回参数


## 目录

- 同步返回
- 异步返回
- 返回侧实现备注

## 同步返回

### 公共返回参数

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `sign` | 签名 | String | 512 | Y | 对响应整体签名 |
| `data` | 响应内容体 | Json | - | N | 业务返回参数 |

### `data`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `resp_code` | 业务响应码 | String | 8 | Y | `00000000` 或 `00000100` 都不代表最终成功，仍要看 `trans_stat` |
| `resp_desc` | 业务响应信息 | String | 256 | Y | 业务返回描述 |
| `req_date` | 请求日期 | String | 8 | Y | 原样返回 |
| `req_seq_id` | 请求流水号 | String | 128 | Y | 原样返回 |
| `hf_seq_id` | 全局流水号 | String | 128 | N | 汇付全局流水号 |
| `trade_type` | 交易类型 | String | 16 | N | 同步返回字段名为 `trade_type` |
| `trans_amt` | 交易金额 | String | 14 | N | 单位元 |
| `trans_stat` | 交易状态 | String | 1 | N | `P`=处理中，`S`=成功，`F`=失败；以此为准 |
| `huifu_id` | 商户号 | String | 32 | Y | 商户号 |
| `delay_acct_flag` | 延时标记 | String | 1 | N | `Y`=延迟，`N`=实时 |
| `remark` | 备注 | String | 255 | N | 原样返回 |
| `device_type` | 终端类型 | String | 2 | N | `01`-`11` 见官方定义 |
| `out_trans_id` | 用户账单上的交易订单号 | String | 64 | N | 用户账单交易单号 |
| `party_order_id` | 用户账单上的商户订单号 | String | 64 | N | 用户账单商户单号 |
| `pay_info` | JS 支付信息 | String | 1024 | N | JSAPI / 小程序 / APP 场景返回 |
| `qr_code` | 二维码链接 | String | 1024 | N | NATIVE 场景返回 |
| `atu_sub_mer_id` | ATU 真实商户号 | String | 32 | N | 微信、支付宝、银联真实商户号 |
| `unconfirm_amt` | 待确认金额 | String | 14 | N | 延时交易待确认金额 |
| `settlement_amt` | 结算金额 | String | 16 | N | 结算金额 |
| `debit_type` | 借贷记标识 | String | 1 | N | `1`=借记卡，`2`=贷记卡，`3`=其他 |
| `wx_user_id` | 微信用户唯一标识码 | String | 128 | N | 微信用户唯一标识 |
| `end_time` | 支付完成时间 | String | 14 | N | `yyyyMMddHHmmss` |
| `acct_id` | 账户号 | String | 9 | N | 商户账户号 |
| `acct_stat` | 账务状态 | String | 1 | N | `P`=处理中，`S`=成功，`F`=失败 |
| `bank_message` | 通道返回描述 | String | 200 | N | 通道返回描述 |
| `method_expand` | 交易扩展参数 | String(JSON Object) | - | N | 各渠道结构见渠道分册 |
| `tx_metadata` | 扩展参数集合 | String(JSON Object) | - | N | 结构见 `references/aggregation-order-tx-metadata.md`；同步返回里补贴 / 分账 / 设备等扩展对象常放这里，且返回侧 `terminal_device_data` 是定位对象，不同于请求侧设备指纹对象 |
| `payment_fee` | 手续费对象 | String(JSON Object) | - | N | 结构见 `references/aggregation-order-tx-metadata.md` |

## 异步返回

### 聚合正扫 / JS 支付异步返回

#### 网关包裹字段

| 参数 | 中文名 | 类型 | 必填 | 说明 |
|------|--------|------|------|------|
| `resp_code` | 网关返回码 | String | Y | 网关返回码 |
| `resp_desc` | 网关返回信息 | String | Y | 网关返回信息 |
| `sign` | 签名 | String | Y | 对整个回调签名 |
| `resp_data` | 返回业务数据 | String(JSON Object) | Y | 业务数据体 |

#### `resp_data`

| 参数 | 中文名 | 类型 | 必填 | 说明 |
|------|--------|------|------|------|
| `resp_code` | 业务响应码 | String | Y | 业务响应码 |
| `resp_desc` | 业务响应信息 | String | Y | 业务响应信息 |
| `huifu_id` | 商户号 | String | Y | 商户号 |
| `req_seq_id` | 请求流水号 | String | Y | 原样返回 |
| `req_date` | 请求日期 | String | Y | 原样返回 |
| `trans_type` | 交易类型 | String | N | 异步字段名为 `trans_type` |
| `hf_seq_id` | 全局流水号 | String | N | 汇付全局流水号 |
| `out_trans_id` | 用户账单上的交易订单号 | String | N | 用户账单交易单号 |
| `party_order_id` | 用户账单上的商户订单号 | String | N | 用户账单商户单号 |
| `trans_amt` | 交易金额 | String | N | 交易金额 |
| `pay_amt` | 消费者实付金额 | String | N | 消费者实付金额 |
| `settlement_amt` | 结算金额 | String | N | 结算金额 |
| `end_time` | 支付完成时间 | String | N | `yyyyMMddHHmmss` |
| `acct_date` | 入账时间 | String | N | `yyyyMMdd` |
| `trans_stat` | 交易状态 | String | N | `S`=成功，`F`=失败 |
| `fee_flag` | 手续费扣款标志 | Integer | N | `1`=外扣，`2`=内扣 |
| `fee_formula_infos` | 手续费费率信息 | Array | N | 手续费费率信息 |
| `fee_amount` | 手续费金额 | String | N | 手续费金额 |
| `trans_fee_allowance_info` | 手续费补贴信息 | Object | N | 异步回调里直接位于 `resp_data` 顶层，不再包在返回 `tx_metadata` 下 |
| `combinedpay_data` | 补贴支付信息 | String | N | 异步回调里直接位于 `resp_data` 顶层，不再包在返回 `tx_metadata` 下 |
| `combinedpay_data_fee_info` | 补贴支付手续费信息 | String | N | 异步回调里直接位于 `resp_data` 顶层，不再包在返回 `tx_metadata` 下 |
| `debit_type` | 借贷记标识 | String | N | `D`=借记卡，`C`=贷记卡，`0`=其他 |
| `is_div` | 是否分账交易 | String | Y | `1`=分账交易，`0`=非分账交易 |
| `acct_split_bunch` | 分账对象 | Object | N | 分账对象 |
| `is_delay_acct` | 是否延时交易 | String | Y | `1`=延迟，`0`=非延迟 |
| `wx_user_id` | 微信用户唯一标识码 | String | N | 微信用户唯一标识 |
| `wx_response` | 微信返回报文 | Object | N | 结构见 `references/aggregation-order-method-wechat.md` |
| `alipay_response` | 支付宝返回报文 | Object | N | 结构见 `references/aggregation-order-method-alipay.md` |
| `dc_response` | 数字货币返回报文 | Object | N | 见下方说明 |
| `unionpay_response` | 银联返回报文 | Object | N | 结构见 `references/aggregation-order-method-unionpay.md` |
| `device_type` | 终端类型 | String | N | 终端类型 |
| `mer_dev_location` | 商户终端定位 | Object | N | 结构见 `references/aggregation-order-tx-metadata.md` |
| `bank_message` | 通道返回描述 | String | N | 通道返回描述 |
| `remark` | 备注 | String | N | 原样返回 |
| `fq_channels` | 分期资产方式 | String | N | 分期资产方式 |
| `notify_type` | 通知类型 | Integer | N | `1`=通道通知，`2`=账务通知 |
| `split_fee_info` | 分账手续费信息 | Object | N | 结构见 `references/aggregation-order-tx-metadata.md` |
| `atu_sub_mer_id` | ATU 真实商户号 | String | N | ATU 真实商户号 |
| `devs_id` | 汇付终端号 | String | N | 汇付终端号 |
| `fund_freeze_stat` | 资金冻结状态 | String | N | `FREEZE` / `UNFREEZE` |

### 数字货币 `dc_response`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `merchant_id` | String | N | 商户号 |
| `term_id` | String | N | 终端号 |
| `trade_type` | String | N | 交易类型 |
| `custom_bank_code` | String | N | 客户所属运营机构代码 |
| `custom_bank_name` | String | N | 客户所属运营机构名称 |
| `openid` | String | N | 用户标识 |
| `sub_openid` | String | N | 用户子标识 |
| `coupon_amount` | String | N | 代金券金额 |
| `coupon_count` | String | N | 代金券数量 |
| `coupon_list` | Array | N | 代金券集合 |
| `creditorWalletName` | String | N | 收款钱包名称 |
| `creditorWalletId` | String | N | 收款钱包 ID |
| `creditorWalletType` | String | N | 收款钱包类型 |
| `creditorWalletLevel` | String | N | 收款钱包等级 |
| `debtorWalletName` | String | N | 付款钱包名称 |
| `debtorWalletId` | String | N | 付款钱包 ID |
| `debtorWalletType` | String | N | 付款钱包类型 |
| `debtorWalletLevel` | String | N | 付款钱包等级 |
| `debtorPartyIdentification` | String | N | 付款运营机构 |
| `businessType` | String | N | 支付类型 |

### `dc_response.coupon_list[]`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `coupon_id` | String | N | 代金券 ID |
| `coupon_type` | String | N | 代金券类型 |
| `coupon_amount` | String | N | 单个代金券支付金额 |

### 聚合正扫解冻异步返回

| 参数 | 中文名 | 类型 | 必填 | 说明 |
|------|--------|------|------|------|
| `resp_code` | 业务返回码 | String | Y | 业务返回码 |
| `resp_desc` | 业务返回描述 | String | Y | 业务返回描述 |
| `hf_seq_id` | 交易的汇付全局流水号 | String | Y | 汇付全局流水号 |
| `req_seq_id` | 交易请求流水号 | String | Y | 原样返回 |
| `req_date` | 交易请求日期 | String | Y | `yyyyMMdd` |
| `huifu_id` | 商户号 | String | Y | 商户号 |
| `notify_type` | 通知类型 | Integer | Y | `3`=资金解冻通知 |
| `fund_freeze_stat` | 资金冻结状态 | String | Y | `UNFREEZE` |
| `unfreeze_amt` | 解冻金额 | String | Y | 单位元 |
| `freeze_time` | 冻结时间 | String | Y | `yyyyMMddHHmmss` |
| `unfreeze_time` | 解冻时间 | String | Y | `yyyyMMddHHmmss` |

### 聚合反扫异步返回差异

| 差异项 | 说明 |
|--------|------|
| `trans_type` | 仅出现 `T_MICROPAY`、`A_MICROPAY`、`U_MICROPAY`、`D_MICROPAY` |
| `fund_freeze_stat` | 官方反扫异步参数表未列出该字段 |
| 渠道对象 | `wx_response`、`alipay_response`、`dc_response`、`unionpay_response` 结构不变 |
| 其他扩展对象 | `acct_split_bunch`、`split_fee_info`、`mer_dev_location` 结构不变 |

## 返回侧实现备注

- 同步字段名是 `trade_type`，异步字段名是 `trans_type`，不要混用。
- `resp_code=00000000` 仅代表受理成功，不代表交易最终成功。
- 最终业务判断统一看 `trans_stat`。
- 同步 / 查询返回时，补贴类对象常放在返回 `tx_metadata` 下；异步回调时，`combinedpay_data`、`combinedpay_data_fee_info`、`trans_fee_allowance_info` 会直接展开在 `resp_data` 顶层，不要按同一包装层硬解析。
- 同步返回 `tx_metadata.terminal_device_data` 与异步 `mer_dev_location` 都是定位对象，不要按请求侧设备指纹结构去解析。
