# 聚合下单交易能力扩展边界：请求顶层与返回 `tx_metadata`

> 这份文件只做一件事：把“请求怎么传”和“返回怎么收”分开。请求侧 `tx_metadata` 本身不作为请求字段上送；`acct_split_bunch`、`terminal_device_data`、`combinedpay_data`、`combinedpay_data_fee_info`、`trans_fee_allowance_info` 都按 `data` 顶层字段处理。同步 / 查询返回里，部分扩展对象仍可能放在返回 `tx_metadata` 下；异步回调里，这些对象又可能直接展开在 `resp_data` 顶层。


## 目录

- 请求侧边界速记
- 请求顶层扩展字段
- 返回侧路径差异速记
- 同步 / 查询返回中的扩展对象
- 结构边界说明

## 请求侧边界速记

| 路径 | 对象 | 传参方式 | 说明 |
|------|------|----------|------|
| `data.acct_split_bunch` | 分账对象 | `setAcctSplitBunch()` | 请求顶层字段 |
| `data.terminal_device_data` | 设备信息 | `setTerminalDeviceData()` | 请求顶层字段 |
| `data.combinedpay_data` | 补贴支付信息 | `request.addExtendInfo(...)` / `client.optional(...)` | 请求顶层扩展字段 |
| `data.combinedpay_data_fee_info` | 补贴支付手续费承担方信息 | `request.addExtendInfo(...)` / `client.optional(...)` | 请求顶层扩展字段 |
| `data.trans_fee_allowance_info` | 手续费补贴信息 | `request.addExtendInfo(...)` / `client.optional(...)` | 请求顶层扩展字段 |

关键约束：

- 请求时不要传 `tx_metadata` 包装层。
- 请求时不要把 `acct_split_bunch`、`terminal_device_data` 塞进 `tx_metadata`。
- 请求时也不要把 `combinedpay_data`、`combinedpay_data_fee_info`、`trans_fee_allowance_info` 再包进 `tx_metadata`。
- 这些交易能力扩展字段现在按开发确认的真实请求口径，直接作为 `data` 顶层字段或顶层扩展字段上送。

## 请求顶层扩展字段

### `acct_split_bunch`（请求顶层）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `acct_infos` | Array | N | 分账明细 |
| `percentage_flag` | String | N | `Y`=使用百分比分账 |
| `is_clean_split` | String | N | `Y`=净值分账；仅在手续费内扣且使用百分比分账时生效 |

### `acct_infos[]`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `div_amt` | String | N | 分账金额，普通固定金额分账时使用 |
| `huifu_id` | String | Y | 分账接收方 ID |
| `acct_id` | String | N | 指定账户号，仅支持基本户、现金户 |
| `percentage_div` | String | N | 分账百分比；仅在 `percentage_flag=Y` 时使用 |

实现备注：

- 固定金额分账时，核心字段是 `div_amt + huifu_id`。
- 百分比分账时，`acct_infos` 中全部 `percentage_div` 之和必须为 `100.00`。
- `is_clean_split` 只有在“手续费内扣 + 百分比分账”场景下才有意义。

### `terminal_device_data`（请求顶层）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `device_ip` | String | N | 交易设备 IP；反扫交易必填，当前以 IPv4 传入为主 |
| `device_mac` | String | N | 交易设备 MAC |
| `device_imei` | String | N | 交易设备 IMEI |
| `device_imsi` | String | N | 交易设备 IMSI |
| `device_icc_id` | String | N | 交易设备 ICCID |
| `device_wifi_mac` | String | N | 交易设备 WiFi MAC |
| `device_gps` | String | N | 交易设备 GPS |
| `app_version` | String | N | 商户终端应用版本号 |
| `encrypt_rand_num` | String | N | 加密随机因子，仅在被扫支付类交易出现 |
| `icc_id` | String | N | SIM 卡卡号 |
| `location` | String | N | 商户终端实时经纬度信息；银联 AT 交易时与 `mer_device_ip` 二选一必填 |
| `mer_device_ip` | String | N | 商户交易设备 IP；银联 AT 交易时与 `location` 二选一必填 |
| `mer_device_type` | String | N | 商户设备类型 |
| `mobile_country_cd` | String | N | 移动国家代码 |
| `mobile_net_num` | String | N | 移动网络号码 |
| `network_license` | String | N | 商户终端入网认证编号 |
| `secret_text` | String | N | 密文数据 |
| `serial_num` | String | N | 商户终端序列号 |
| `devs_id` | String | N | 汇付机具号；通过汇付报备的机具交易必传 |

关键约束：

- `encrypt_rand_num` 在 19 位付款码场景取后 6 位；EMV 二维码场景取 `tag57` 卡号 / token 后 6 位。
- `location` 格式为 `纬度/经度`，例如 `+37.12/-121.213`。
- `devs_id` 取自汇付终端报备或终端查询接口返回的 `device_id`。

### `combinedpay_data[]`（请求顶层）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `huifu_id` | String | N | 补贴方汇付商户号 |
| `user_type` | String | N | `channel`、`merchant`、`agent`、`mertomer` |
| `acct_id` | String | N | 营销补贴方账户号 |
| `amount` | String | N | 补贴金额 |

### `combinedpay_data_fee_info`（请求顶层）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `huifu_id` | String | N | 补贴支付手续费承担方汇付编号 |
| `acct_id` | String | N | 补贴支付手续费承担方账户号 |

### `trans_fee_allowance_info`（请求顶层）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `allowance_fee_amt` | String | N | 补贴手续费金额 |

## 返回侧路径差异速记

| 场景 | 路径 | 说明 |
|------|------|------|
| 同步返回 | `data.tx_metadata.*` 或顶层返回扩展字段 | 同步返回的扩展对象存在包装差异，落地时应按实际报文解析 |
| 查询返回 | `data.tx_metadata.*` | 查询接口通常沿用 `tx_metadata` 包装 |
| 异步回调 | `resp_data.combinedpay_data` / `resp_data.combinedpay_data_fee_info` / `resp_data.trans_fee_allowance_info` | 这 3 个补贴类对象在异步里通常直接展开在 `resp_data` 顶层 |
| 异步回调 | `resp_data.acct_split_bunch` / `resp_data.mer_dev_location` | 异步里分账和定位对象也直接在 `resp_data` 顶层 |
| 独立返回对象 | `data.payment_fee` | `payment_fee` 是独立返回对象，不属于请求参数 |

## 同步 / 查询返回中的扩展对象

### `combinedpay_data[]`

- 查询返回路径通常为 `tx_metadata.combinedpay_data`。
- 异步回调路径通常为 `resp_data.combinedpay_data`。

| 参数 | 类型 | 说明 |
|------|------|------|
| `huifu_id` | String | 补贴方汇付商户号 |
| `user_type` | String | 同步返回通常沿用请求枚举；异步表里官方示例收紧为 `channel`、`agent` |
| `acct_id` | String | 补贴方账户号 |
| `amount` | String | 补贴金额 |

### `combinedpay_data_fee_info`

- 查询返回路径通常为 `tx_metadata.combinedpay_data_fee_info`。
- 异步回调路径通常为 `resp_data.combinedpay_data_fee_info`。

| 参数 | 类型 | 说明 |
|------|------|------|
| `huifu_id` | String | 补贴支付手续费承担方汇付编号 |
| `acct_id` | String | 补贴支付手续费承担方账户号 |
| `combinedpay_fee_amt` | String | 补贴支付手续费金额；该字段出现在返回侧 |

### `trans_fee_allowance_info`

- 查询返回路径通常为 `tx_metadata.trans_fee_allowance_info`。
- 异步回调路径通常为 `resp_data.trans_fee_allowance_info`。

同步 / 异步返回共有字段：

| 参数 | 类型 | 说明 |
|------|------|------|
| `receivable_fee_amt` | String | 商户应收手续费 |
| `actual_fee_amt` | String | 商户实收手续费 |
| `allowance_fee_amt` | String | 补贴手续费 |

异步回调可能额外出现：

| 参数 | 类型 | 说明 |
|------|------|------|
| `allowance_type` | String | 补贴类型 |
| `no_allowance_desc` | String | 不补贴原因 |
| `cur_allowance_config_infos` | Object | 手续费补贴活动详情 |

### `cur_allowance_config_infos`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `acct_id` | String | N | 门店 |
| `merchant_group` | String | N | 商户号 |
| `allowance_sys` | String | Y | 补贴方 |
| `allowance_sys_id` | String | Y | 补贴方 ID |
| `is_delay_allowance` | String | Y | `1`=实补，`2`=后补 |
| `market_id` | String | Y | 自定义活动编号 |
| `market_name` | String | N | 自定义活动名称 |
| `market_desc` | String | N | 自定义活动描述 |
| `start_time` | String | Y | 活动开始时间 |
| `end_time` | String | Y | 活动结束时间 |
| `pos_debit_limit_amt` | String | Y | POS 借记卡补贴额度 |
| `pos_credit_limit_amt` | String | Y | POS 贷记卡补贴额度 |
| `pos_limit_amt` | String | Y | POS 补贴额度 |
| `qr_limit_amt` | String | Y | 扫码补贴额度 |
| `total_limit_amt` | String | Y | 活动总补贴额度 |
| `status` | String | Y | 活动状态 |
| `human_flag` | String | Y | 是否人工操作 |
| `activity_id` | String | Y | 活动号 |
| `activity_name` | String | N | 活动描述 |
| `create_by` | String | Y | 创建人 |
| `create_time` | String | Y | 创建时间 |
| `update_time` | String | Y | 更新时间 |

### `terminal_device_data`（同步 / 查询返回 `tx_metadata.terminal_device_data`）

| 参数 | 类型 | 说明 |
|------|------|------|
| `terminal_ip` | String | 交易设备公网 IP |
| `terminal_location` | String | 终端实时经纬度信息 |

### `mer_dev_location`（异步回调 `resp_data.mer_dev_location`）

| 参数 | 类型 | 说明 |
|------|------|------|
| `terminal_ip` | String | 交易设备公网 IP |
| `terminal_location` | String | 终端实时经纬度信息 |

### `payment_fee`

| 参数 | 类型 | 说明 |
|------|------|------|
| `fee_huifu_id` | String | 手续费承担方汇付号 |
| `fee_flag` | Integer | `1`=外扣，`2`=内扣 |
| `fee_formula_infos` | Array | 手续费公式列表 |
| `fee_amount` | String | 手续费金额 |

### `fee_formula_infos[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| `fee_formula` | String | 手续费计算公式 |
| `fee_type` | String | `TRANS_FEE` 或 `ACCT_FEE` |
| `huifu_id` | String | 补贴账户的 `huifu_id` |

### `split_fee_info`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `total_split_fee_amt` | String | N | 分账手续费总金额 |
| `split_fee_flag` | Integer | Y | `1`=外扣，`2`=内扣 |
| `split_fee_details` | Array | Y | 分账手续费明细 |

### `split_fee_details[]`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `split_fee_amt` | String | Y | 分账手续费金额 |
| `split_fee_huifu_id` | String | Y | 分账手续费承担方商户号 |
| `split_fee_acct_id` | String | N | 分账手续费承担方账号 |

## 结构边界说明

- 请求侧 `acct_split_bunch`、`terminal_device_data`、`combinedpay_data`、`combinedpay_data_fee_info`、`trans_fee_allowance_info` 都按 `data` 顶层字段处理。
- `tx_metadata` 不再承担请求字段的包装职责；请求时不要传这个包装层。
- 查询返回里，补贴类对象仍常放在返回 `tx_metadata` 下；异步回调里，同名扩展对象可能直接展开在 `resp_data` 顶层。
- 同步 / 查询返回 `tx_metadata.terminal_device_data` 和异步 `mer_dev_location` 都是定位对象，只含 `terminal_ip` / `terminal_location`，不要按请求侧设备指纹结构去解析。
- `payment_fee` 是汇付返回的独立手续费对象，不属于请求参数本体。
