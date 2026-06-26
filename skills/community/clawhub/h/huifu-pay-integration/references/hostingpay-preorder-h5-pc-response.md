# H5、PC 预下单顶层返回参数

> 本文件覆盖 H5/PC 预下单的同步返回公共参数、同步 `data` 字段，以及异步 `resp_data` 顶层字段。渠道专属响应对象见 `references/hostingpay-preorder-h5-pc-response-channel.md`。

## 同步返回公共参数

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `sign` | 签名 | String | 512 | Y | 对整体响应报文签名 |
| `data` | 响应内容体 | JSON | - | N | 业务返回参数 |

## 同步返回 `data`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `resp_code` | 业务响应码 | String | 8 | Y | 见错误码文档；用于排查，不直接代表订单终态 |
| `resp_desc` | 业务响应信息 | String | 128 | Y | 业务返回描述 |
| `req_date` | 请求日期 | String | 8 | Y | 预下单时传入，原样返回 |
| `req_seq_id` | 请求流水号 | String | 64 | Y | 预下单时传入，原样返回 |
| `huifu_id` | 商户号 | String | 32 | Y | 预下单时传入，原样返回 |
| `pre_order_type` | 预下单类型 | String | 1 | Y | H5/PC 固定为 `1` |
| `pre_order_id` | 预下单 ID | String | 64 | Y | 汇付生成的预下单 ID |
| `goods_desc` | 商品描述 | String | 40 | Y | 商品描述 |
| `jump_url` | 支付跳转链接 | String | 256 | Y | 直接跳转该链接即可拉起支付 |
| `usage_type` | 订单类型 | String | 1 | N | `P`=支付，`R`=充值，默认 `P` |
| `trans_type` | 交易类型 | String | 256 | N | 多值时表示收银台可用支付类型 |
| `hosting_data` | 统一收银台扩展参数集合 | String | 2000 | Y | JSON 对象字符串 |
| `current_time` | 系统响应时间 | String | 14 | Y | 格式 `yyyyMMddHHmmss` |
| `time_expire` | 交易失效时间 | String | 14 | Y | 格式 `yyyyMMddHHmmss` |

## 同步返回 `data.hosting_data`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `project_title` | 项目标题 | String | 64 | Y | 账单页展示标题 |
| `project_id` | 托管项目号 | String | 32 | Y | 商户创建的统一收银台托管项目号 |
| `private_info` | 商户私有信息 | String | 255 | N | 异步通知和主动查询中的 `remark` 原样返回 |
| `callback_url` | 回调地址 | String | 512 | N | 支付成功后跳转回该地址 |
| `request_type` | 请求类型 | String | 1 | C | `P`=PC 页面版，`M`=H5 页面版 |

## 异步返回说明

- 只有“成功发起支付”才会收到异步通知。
- 异步通知体核心业务节点为 `resp_data`。
- 接收后仍应按 `hf_seq_id` 做幂等，并结合查询接口做二次确认。

## 异步返回 `resp_data`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `resp_code` | 业务返回码 | String | 8 | Y | 见错误码文档 |
| `resp_desc` | 业务返回信息 | String | 512 | Y | 业务返回描述 |
| `req_seq_id` | 请求流水号 | String | 64 | Y | 交易时传入，原样返回 |
| `req_date` | 请求时间 | String | 8 | Y | 交易时传入，格式 `yyyyMMdd` |
| `hf_seq_id` | 汇付全局流水号 | String | 40 | N | 汇付全局流水号 |
| `out_trans_id` | 用户账单交易订单号 | String | 64 | N | 用户账单上的交易订单号 |
| `party_order_id` | 用户账单商户订单号 | String | 64 | N | 用户账单上的商户订单号 |
| `huifu_id` | 商户号 | String | 32 | Y | 商户号 |
| `trans_type` | 交易类型 | String | 20 | N | 实际成交的支付渠道类型 |
| `trans_amt` | 交易金额 | String | 12 | N | 单位元 |
| `settlement_amt` | 结算金额 | String | 16 | N | 单位元 |
| `trans_stat` | 交易状态 | String | 1 | N | `S`=成功，`F`=失败 |
| `trans_finish_time` | 汇付侧交易完成时间 | String | 6 | N | 官方长度列写 `6`，但格式说明为 `yyyyMMddHHmmss` |
| `end_time` | 支付完成时间 | String | 14 | N | 格式 `yyyyMMddHHmmss` |
| `acct_date` | 入账时间 | String | 8 | N | 格式 `yyyyMMdd` |
| `debit_flag` | 借贷记标识 | String | 1 | N | `D`=借记卡，`C`=信用卡，`Z`=借贷合一卡 |
| `user_huifu_id` | 用户号 | String | 32 | N | 快捷支付时才有值 |
| `wx_user_id` | 微信用户唯一标识码 | String | 128 | N | 微信用户唯一标识码 |
| `wx_response` | 微信返回报文 | Object | 6000 | N | 详见渠道响应文档 |
| `alipay_response` | 支付宝返回报文 | Object | 6000 | N | 详见渠道响应文档 |
| `unionpay_response` | 银联返回报文 | Object | 6000 | N | 详见渠道响应文档 |
| `dy_response` | 抖音返回报文 | String | - | N | JSON 对象字符串；详见渠道响应文档 |
| `is_div` | 是否分账交易 | String | 1 | Y | `1`=分账，`0`=非分账 |
| `acct_split_bunch` | 分账对象 | String | 2048 | N | JSON 对象字符串 |
| `is_delay_acct` | 是否延时交易 | String | 1 | Y | `1`=延迟，`0`=不延迟 |
| `fee_flag` | 手续费扣款标志 | Int | 1 | N | `1`=外扣，`2`=内扣 |
| `fee_amount` | 手续费金额 | String | 16 | N | 单位元 |
| `trans_fee_allowance_info` | 手续费补贴信息 | Object | 6000 | N | 详见渠道响应文档 |
| `remark` | 备注 | String | 45 | N | 原样返回 |
| `bank_code` | 通道返回码 | String | 32 | N | 通道返回码 |
| `bank_message` | 通道返回描述 | String | 200 | N | 通道返回描述 |
| `bank_id` | 收款方银行代号 | String | 8 | N | 快捷、网银交易返回 |
| `bank_extend_param` | 银行扩展信息 | String | - | N | JSON 对象字符串 |
| `fee_formula_infos` | 手续费费率信息 | String | - | N | JSON 数组字符串 |
| `order_type` | 订单类型 | String | 1 | N | `P`=支付，`R`=充值 |
| `devs_id` | 汇付机具号 | String | 32 | Y | 通过汇付报备的机具必传 |
| `request_ip` | 请求 IP | String | 15 | N | 付款方 IP；支付成功后返回 |

## 实现备注

- `jump_url` 是同步返回里最关键的前端拉起字段；拿到之后仍然不能视为支付成功。
- `trans_finish_time` 的官方长度定义与格式定义冲突，应用侧最好统一按 14 位时间戳兼容解析。
- 渠道扩展对象很多，回调落库时建议把顶层字段和渠道对象分表或按 JSON 列分开存储。
