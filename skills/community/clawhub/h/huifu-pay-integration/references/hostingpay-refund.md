# 托管支付退款

这份文档覆盖托管支付退款申请和退款查询。

> 字段结论回答必须同时读取并列出 `hostingpay-refund-query.md`；退款申请字段和退款查询字段要一起说明，不能只停留在 `hostingpay-refund.md` 或 `hostingpay-refund-quickstart.md`。

## 目录

- 什么时候读这里
- 对应接口
- 请求头强制约束
- 退款主流程
- 退款申请 data 请求字段
- 退款申请返回参数
- 退款申请异步返回参数
- 退款查询 data 请求字段
- 关键定位字段
- 核心规则
- device_type 参考
- Java 特殊点
- 退款期限
- PHP 路径
- 下一步

## 什么时候读这里

- 原交易已确认支付成功
- 需要发起托管支付退款
- 需要查询退款最终状态

## 对应接口

| 场景 | 接口 |
| --- | --- |
| 退款申请 | `v2/trade/hosting/payment/htRefund` |
| 退款查询 | `v2/trade/hosting/payment/queryRefundInfo` |

## 请求头强制约束

- 上面 2 个接口都必须带 `jpt-x-skill-source: <skill_source>`
- 如果当前按 PHP 接入，且请求 `data` 中存在 `huifu_id`，还必须带 `jpt-x-skill-huifu_id: <data.huifu_id>`
- 当前 Skill 包对齐的官方 PHP SDK 主链路在 `MerConfig.skill_source` 已配置时，会自动带 `jpt-x-skill-source`，并在当前请求 `huifu_id` 存在且非空时自动带 `jpt-x-skill-huifu_id`
- 当前 Java SDK 基线也会在请求 `data` 中存在 `huifu_id` 且非空时自动带 `jpt-x-skill-huifu_id: <data.huifu_id>`
- 这两项属于 HTTP 请求头，不属于业务报文 `data`；具体明细以 `references/shared-request-header-policy.md` 为准

## 退款主流程

```text
确认原交易成功且定位键完整
  -> 发起退款
  -> 处理中时等待异步通知或主动查询
  -> 查询最终退款状态
  -> 成功后更新业务退款结果
```

## 退款申请 data 请求字段

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `req_date` | Y | 本次退款请求日期，格式 `yyyyMMdd` |
| `req_seq_id` | Y | 本次退款请求流水号，同一 `huifu_id` 下当天唯一 |
| `huifu_id` | Y | 商户号 |
| `ord_amt` | Y | 申请退款金额，单位元，保留两位小数；延时交易退款金额必须小于等于待确认金额 |
| `org_req_date` | Y | 原交易请求日期，格式 `yyyyMMdd` |
| `org_hf_seq_id` | C | 原交易全局流水号；与 `org_party_order_id`、`org_req_seq_id` 三选一 |
| `org_party_order_id` | C | 原交易微信/支付宝用户账单上的商户单号；扫码退款场景三选一，拆单支付场景与 `org_hf_seq_id` 二选一 |
| `org_req_seq_id` | C | 原交易请求流水号；与其他两项按官方规则择一上送 |
| `acct_split_bunch` | N | 分账对象，JSON Object 字符串 |
| `remark` | N | 备注，原样返回 |
| `loan_flag` | N | 是否垫资退款，`Y`=垫资出款，`N`=普通出款，默认 `N` |
| `loan_undertaker` | N | 垫资承担者 `huifu_id` |
| `loan_acct_type` | N | 垫资账户类型，`01`=基本户，`05`=充值户，默认充值户 |
| `risk_check_data` | C | 安全信息，线上交易退款必填，JSON Object 字符串 |
| `terminal_device_data` | C | 设备信息，线上交易退款必填，JSON Object 字符串 |
| `notify_url` | N | 退款异步通知地址 |
| `bank_info_data` | C | 大额转账支付账户信息，银行大额转账支付退款申请时必填 |
| `dy_data` | N | 抖音扩展参数集合，JSON Object 字符串 |

### `acct_split_bunch.acct_infos[]`

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `div_amt` | Y | 分账金额，单位元，保留两位小数 |
| `huifu_id` | Y | 分账接收方 ID |
| `part_loan_amt` | N | 垫资金额；若由第三方全额垫资则不传 |

### `risk_check_data`

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `ip_addr` | N | IP 地址；与经纬度、基站地址至少三选一送一项 |
| `base_station` | N | 基站地址；与 IP、经纬度至少三选一送一项 |
| `latitude` | N | 纬度；与 IP、基站地址至少三选一送一项 |
| `longitude` | N | 经度；与 IP、基站地址至少三选一送一项 |

### `terminal_device_data`

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `device_type` | N | `1` 手机，`2` 平板，`3` 手表，`4` PC |
| `device_ip` | N | 交易设备公网 IP |
| `device_mac` | N | 交易设备 MAC |
| `device_gps` | N | 交易设备 GPS |
| `device_imei` | N | 交易设备 IMEI |
| `device_imsi` | N | 交易设备 IMSI |
| `device_icc_id` | N | 交易设备 ICCID |
| `device_wifi_mac` | N | 交易设备 WIFI MAC |

### `bank_info_data`

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `province` | C | 付款方为对公账户时必填，省份代码 |
| `area` | C | 付款方为对公账户时必填，地区代码 |
| `bank_code` | C | 付款方为对公账户时必填，银行编号 |
| `correspondent_code` | C | 付款方为对公账户时必填，联行号 |
| `card_acct_type` | N | 付款方账户类型，`E`=对公，`P`=对私，默认 `P` |

### `dy_data`

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `refund_desc` | N | 抖音退款原因，会展示给用户 |

## 退款申请返回参数

同步返回只代表退款请求受理或处理结果，不等于退款终态。退款最终状态仍应通过退款查询和异步通知闭环确认。

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `resp_code` | Y | 业务响应码 |
| `resp_desc` | Y | 业务响应信息 |
| `product_id` | Y | 产品号，原样返回 |
| `huifu_id` | Y | 商户号 |
| `req_date` | Y | 退款请求日期，原样返回 |
| `req_seq_id` | Y | 退款请求流水号，原样返回 |
| `hf_seq_id` | N | 退款全局流水号，扫码退款场景可能返回 |
| `org_req_date` | N | 原交易请求日期 |
| `org_req_seq_id` | N | 原交易请求流水号 |
| `org_hf_seq_id` | N | 原交易全局流水号 |
| `trans_time` | N | 退款交易发生时间 |
| `trans_stat` | N | `P` 处理中，`S` 成功，`F` 失败 |
| `ord_amt` | Y | 退款金额 |
| `actual_ref_amt` | N | 实际退款金额 |
| `acct_split_bunch` | N | 分账信息 |
| `unionpay_response` | N | 银联返回报文 |
| `dy_response` | N | 抖音返回报文 |
| `remark` | N | 备注，原样返回 |
| `bank_code` | N | 通道返回码 |
| `bank_message` | N | 通道返回描述 |
| `fee_amt` | N | 退款返还手续费 |

## 退款申请异步返回参数

退款申请可能通过异步通知返回更完整的退款结果。异步通知仍需验签、幂等和必要的退款查询确认，不能只凭同步 `resp_code=00000000` 改退款成功。

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `resp_code` | Y | 业务响应码 |
| `resp_desc` | Y | 业务响应信息 |
| `product_id` | Y | 产品号 |
| `huifu_id` | Y | 商户号 |
| `mer_name` | N | 商户名称 |
| `req_date` | Y | 退款请求日期 |
| `req_seq_id` | Y | 退款请求流水号 |
| `hf_seq_id` | N | 退款全局流水号 |
| `org_req_date` | N | 原交易请求日期 |
| `org_req_seq_id` | N | 原交易请求流水号 |
| `org_hf_seq_id` | N | 原交易全局流水号 |
| `org_ord_amt` | N | 原交易订单金额 |
| `org_fee_amt` | N | 原交易手续费 |
| `trans_date` | N | 退款交易发生日期 |
| `trans_time` | N | 退款交易发生时间 |
| `trans_finish_time` | N | 退款完成时间 |
| `trans_type` | N | 交易类型，`TRANS_REFUND` |
| `trans_stat` | N | `P` 处理中，`S` 成功，`F` 失败，`I` 初始 |
| `ord_amt` | Y | 本次退款金额 |
| `actual_ref_amt` | N | 实际退款金额 |
| `total_ref_amt` | N | 原交易累计退款金额 |
| `total_ref_fee_amt` | N | 原交易累计退款手续费金额 |
| `ref_cut` | N | 累计退款次数 |
| `party_order_id` | N | 微信/支付宝/抖音用户账单上的商户订单号 |
| `bank_code` | N | 通道返回码 |
| `bank_message` | N | 通道返回描述 |
| `bank_id` | N | 收款方银行代号，快捷或网银返回 |
| `bank_name` | N | 收款方银行名称，快捷或网银返回 |
| `fee_amt` | N | 退款返还手续费 |
| `acct_split_bunch` | N | 分账退款信息 |
| `split_fee_info` | N | 分账手续费信息 |
| `unionpay_response` | N | 银联返回报文，可能含 `coupon_info` 优惠信息 |
| `dy_response` | N | 抖音返回报文，含抖音原交易订单号、退款单号、用户退款金额等 |
| `remark` | N | 备注，原样返回 |

### 异步扩展对象摘要

| 对象 | 关键字段 |
| --- | --- |
| `acct_split_bunch.acct_infos[]` | `div_amt`、`huifu_id`、`acct_id`、`part_loan_amt` |
| `split_fee_info` | `total_split_fee_amt`、`split_fee_flag`、`split_fee_details[]` |
| `split_fee_details[]` | `split_fee_amt`、`split_fee_huifu_id`、`split_fee_acct_id` |
| `unionpay_response.coupon_info[]` | `type`、`spnsrId`、`offstAmt`、`id`、`desc`、`addnInfo` |
| `dy_response` | `org_out_trans_id`、`out_trans_id`、`payer_refund` |

## 退款查询 data 请求字段

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `req_date` | Y | 本次查询请求日期，格式 `yyyyMMdd` |
| `req_seq_id` | Y | 本次查询请求流水号，同一 `huifu_id` 下当天唯一 |
| `huifu_id` | Y | 商户号 |
| `org_req_date` | Y | 退款请求日期，不是原支付交易日期 |
| `org_hf_seq_id` | C | 退款全局流水号；与 `org_req_seq_id` 二选一 |
| `org_req_seq_id` | C | 退款请求流水号；与 `org_hf_seq_id` 二选一 |

查询补充说明：

- 退款查询里的 `org_req_seq_id` 指退款请求本身的 `req_seq_id`。
- 完整返回字段、分账手续费返回结构和银联 / 抖音返回对象继续看 `references/hostingpay-refund-query.md`。

## 关键定位字段

- 原交易定位键：`org_req_seq_id`、`org_party_order_id`、`org_hf_seq_id`
- 退款查询定位键：退款交易自己的 `org_req_seq_id` 或 `org_hf_seq_id`

## 核心规则

1. 退款金额不能超过原交易金额
2. `resp_code=00000000` 只表示退款请求已受理
3. 退款最终状态必须看退款查询和异步通知闭环
4. 退款逻辑必须幂等

## device_type 参考

| 原交易场景 | 建议 device_type |
| --- | --- |
| H5 手机网页、支付宝小程序、微信小程序 | `"1"` |
| PC 网页支付 | `"4"` |

## Java 特殊点

在 Java 路径里，`org_req_seq_id` 没有独立 setter，必须通过扩展参数传入。这个坑只影响 Java 写法，不影响协议字段本身。

## 退款期限

| 场景 | 最大退款期限 |
| --- | --- |
| 微信 / 支付宝 / H5 / PC | `360` 天 |

## PHP 路径

托管支付 PHP 支持退款，默认入口先读：

- `references/hostingpay-php-adapter.md`
- `references/hostingpay-refund-php-scenarios.md`

如果只是核对补头或签名口径，读取 `references/shared-request-header-policy.md` 与 `references/shared-signing-v2.md`

## 下一步

- 需要看退款查询完整返回字段：读 `references/hostingpay-refund-query.md`
- 还没确认原交易成功：先读 `references/hostingpay-query.md`
- 前端回调配合问题：再读 `references/checkout-js.md`
