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

| 参数 | 类型 | 长度 | 官网必填 | 条件与说明 |
| --- | --- | --- | --- | --- |
| `req_date` | String | 8 | Y | 本次退款请求日期，格式 `yyyyMMdd` |
| `req_seq_id` | String | 128 | Y | 本次退款请求流水号，同一 `huifu_id` 下当天唯一 |
| `huifu_id` | String | 32 | Y | 商户号 |
| `ord_amt` | String | 14 | Y | 申请退款金额，单位元，保留两位小数；延时交易退款金额必须小于等于待确认金额 |
| `org_req_date` | String | 8 | Y | 原交易请求日期，格式 `yyyyMMdd` |
| `org_hf_seq_id` | String | 128 | N | 条件上与 `org_party_order_id`、`org_req_seq_id` 三选一；拆单支付时与 `org_party_order_id` 二选一 |
| `org_party_order_id` | String | 64 | N | 扫码退款条件上三选一；拆单支付时与 `org_hf_seq_id` 二选一 |
| `org_req_seq_id` | String | 128 | N | 条件上与另外两项三选一 |
| `acct_split_bunch` | String(JSON Object) | 2048 | N | 分账对象 |
| `remark` | String | 84 | N | 备注，原样返回 |
| `loan_flag` | String | 2 | N | `Y`=垫资出款，`N`=普通出款，默认 `N` |
| `loan_undertaker` | String | 32 | N | 垫资承担者 `huifu_id` |
| `loan_acct_type` | String | 2 | N | `01`=基本户，`05`=充值户，默认充值户 |
| `risk_check_data` | String(JSON Object) | 2048 | C | 线上交易退款必填 |
| `terminal_device_data` | String(JSON Object) | 2048 | C | 线上交易退款必填 |
| `notify_url` | String | 512 | N | 退款异步通知地址 |
| `bank_info_data` | String(JSON Object) | 1024 | C | 银行大额转账支付退款申请时必填 |
| `dy_data` | String(JSON Object) | 2048 | N | 抖音扩展参数集合 |

### `acct_split_bunch.acct_infos[]`

| 参数 | 类型 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `div_amt` | String | 14 | Y | 分账金额，单位元，保留两位小数 |
| `huifu_id` | String | 32 | Y | 分账接收方 ID |
| `part_loan_amt` | String | 12 | N | 垫资金额；若由第三方全额垫资则不传 |

### `risk_check_data`

| 参数 | 类型 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `ip_addr` | String | 32 | N | 与经纬度、基站地址至少三选一送一项 |
| `base_station` | String | 64 | N | 与 IP、经纬度至少三选一送一项 |
| `latitude` | String | 20 | N | 与 IP、基站地址至少三选一送一项 |
| `longitude` | String | 20 | N | 与 IP、基站地址至少三选一送一项 |

> 2026-10-10官网请求示例已改为 `risk_check_data.ip_addr`，删除示例专有字段。按正式 `ip_addr/base_station/latitude/longitude` 构造，旧风控示例冲突已关闭。

### `terminal_device_data`

| 参数 | 类型 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `device_type` | String | 2 | N | `1` 手机，`2` 平板，`3` 手表，`4` PC |
| `device_ip` | String | 64 | N | 交易设备公网 IP |
| `device_mac` | String | 64 | N | 交易设备 MAC |
| `device_gps` | String | 64 | N | 交易设备 GPS |
| `device_imei` | String | 64 | N | 交易设备 IMEI |
| `device_imsi` | String | 64 | N | 交易设备 IMSI |
| `device_icc_id` | String | 64 | N | 交易设备 ICCID |
| `device_wifi_mac` | String | 64 | N | 交易设备 WIFI MAC |

### `bank_info_data`

| 参数 | 类型 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `province` | String | 4 | C | 付款方为对公账户时必填，省份代码 |
| `area` | String | 4 | C | 付款方为对公账户时必填，地区代码 |
| `bank_code` | String | 8 | C | 付款方为对公账户时必填，银行编号 |
| `correspondent_code` | String | 30 | C | 付款方为对公账户时必填，联行号 |
| `card_acct_type` | String | 1 | N | `E`=对公，`P`=对私，默认 `P` |

### `dy_data`

| 参数 | 类型 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `refund_desc` | String | 200 | N | 抖音退款原因，会展示给用户 |

## 退款申请返回参数

同步返回只代表退款请求受理或处理结果，不等于退款终态。退款最终状态仍应通过退款查询和异步通知闭环确认。

| 参数 | 类型 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `resp_code` | String | 8 | Y | 业务响应码 |
| `resp_desc` | String | 512 | Y | 业务响应信息 |
| `product_id` | String | 32 | Y | 产品号，原样返回 |
| `huifu_id` | String | 32 | Y | 商户号 |
| `req_date` | String | 8 | Y | 退款请求日期，原样返回 |
| `req_seq_id` | String | 128 | Y | 退款请求流水号，原样返回 |
| `hf_seq_id` | String | 128 | N | 退款全局流水号，扫码退款场景可能返回 |
| `org_req_date` | String | 8 | N | 原交易请求日期 |
| `org_req_seq_id` | String | 128 | N | 原交易请求流水号 |
| `org_hf_seq_id` | String | 128 | N | 原交易全局流水号 |
| `trans_time` | String | 14 | N | 退款交易发生时间 |
| `trans_stat` | String | 1 | N | `P` 处理中，`S` 成功，`F` 失败 |
| `ord_amt` | String | 14 | Y | 退款金额 |
| `actual_ref_amt` | String | 14 | N | 实际退款金额 |
| `acct_split_bunch` | String(JSON Object) | 2048 | N | 分账信息 |
| `unionpay_response` | String(JSON Object) | 6000 | N | 银联返回报文 |
| `dy_response` | String(JSON Object) | 6000 | N | 先解码JSON对象字符串，再读取子字段 |
| `remark` | String | 84 | N | 备注，原样返回 |
| `bank_code` | String | 64 | N | 通道返回码 |
| `bank_message` | String | 256 | N | 通道返回描述 |
| `fee_amt` | String | 14 | N | 退款返还手续费 |

## 退款申请异步返回参数

退款申请可能通过异步通知返回更完整的退款结果。异步通知仍需验签、幂等和必要的退款查询确认，不能只凭同步 `resp_code=00000000` 改退款成功。

| 参数 | 类型 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `resp_code` | String | 8 | Y | 业务响应码 |
| `resp_desc` | String | 512 | Y | 业务响应信息 |
| `huifu_id` | String | 32 | Y | 商户号 |
| `mer_name` | String | 128 | Y | 商户名称，线上交易返回 |
| `req_date` | String | 8 | Y | 退款请求日期 |
| `req_seq_id` | String | 128 | Y | 退款请求流水号 |
| `hf_seq_id` | String | 128 | N | 退款全局流水号 |
| `org_req_date` | String | 8 | N | 原交易请求日期 |
| `org_req_seq_id` | String | 128 | N | 原交易请求流水号 |
| `org_ord_amt` | String | 14 | Y | 原交易订单金额 |
| `org_fee_amt` | String | 14 | Y | 原交易手续费 |
| `trans_date` | String | 8 | Y | 退款交易发生日期 |
| `trans_time` | String | 6 | N | 退款交易发生时间，`HHmmss` |
| `trans_finish_time` | String | 14 | N | 退款完成时间，`yyyyMMddHHmmss` |
| `trans_type` | String | 40 | Y | 交易类型，`TRANS_REFUND` |
| `trans_stat` | String | 1 | N | `P` 处理中，`S` 成功，`F` 失败 |
| `ord_amt` | String | 14 | Y | 本次退款金额 |
| `actual_ref_amt` | String | 14 | N | 实际退款金额 |
| `total_ref_amt` | String | 14 | Y | 原交易累计退款金额 |
| `total_ref_fee_amt` | String | 14 | Y | 原交易累计退款手续费金额 |
| `ref_cut` | String | 14 | Y | 累计退款次数 |
| `party_order_id` | String | 64 | N | 微信/支付宝/抖音用户账单上的商户订单号 |
| `bank_code` | String | 64 | N | 通道返回码 |
| `bank_message` | String | 256 | N | 通道返回描述 |
| `bank_id` | String | 32 | N | 收款方银行代号，快捷或网银返回 |
| `bank_name` | String | 128 | N | 收款方银行名称，快捷或网银返回 |
| `fee_amt` | String | 14 | N | 退款返还手续费 |
| `acct_split_bunch` | String(JSON Object) | 4000 | Y | 分账退款信息 |
| `split_fee_info` | String(JSON Object) | 2048 | N | 分账手续费信息，线上交易返回 |
| `unionpay_response` | String(JSON Object) | 6000 | N | 银联返回报文，可能含 `coupon_info` 优惠信息 |
| `dy_response` | String(JSON Object) | 6000 | N | 先解码JSON对象字符串，再读取子字段 |
| `remark` | String | 84 | N | 备注，原样返回 |

### 同步/异步扩展对象

`acct_split_bunch` 的对象长度以所在主表为准：同步 2048、异步 4000。

`dy_response` 在同步及异步业务表均已明确为 String(JSON Object)(6000)。同步侧可按目录解码；退款异步外层仍标为 `data`，外层编码/签验协议未明确，不能据子字段编码推定整份通知协议。

| 字段路径 | 类型 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `acct_infos[]` | Array | 2048 | N | 分账明细 |
| `fee_amt` | String | 14 | N | 退款返还手续费 |

`acct_split_bunch.acct_infos[]`：

| 字段路径 | 类型 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `div_amt` | String | 14 | Y | 分账金额 |
| `huifu_id` | String | 32 | Y | 分账接收方 ID |

`split_fee_info`：

| 字段路径 | 类型 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `split_fee_flag` | String | 1 | Y | `1` 外扣、`2` 内扣 |
| `total_split_fee_amt` | String | 14 | Y | 总分账手续费金额 |
| `split_fee_details[]` | Array | 2048 | Y | 分账手续费明细 |

`split_fee_info.split_fee_details[]`：

| 字段路径 | 类型 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `split_fee_amt` | String | 14 | Y | 分账手续费金额 |
| `split_fee_huifu_id` | String | 32 | Y | 分账手续费承担方商户号 |
| `split_fee_acct_id` | String | 16 | N | 分账手续费承担方账号 |

`unionpay_response.coupon_info[]`：

| 字段路径 | 类型 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `addnInfo` | String | 100 | N | 附加信息 |
| `spnsrId` | String | 20 | Y | 出资方 |
| `type` | String | 4 | Y | 项目类型，如 `DD01`、`CP01` |
| `offstAmt` | String | 14 | Y | 抵消交易金额 |
| `id` | String | 40 | N | 项目编号 |
| `desc` | String | 40 | N | 项目简称 |

`dy_response`：

| 字段路径 | 类型 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `org_out_trans_id` | String | 32 | N | 抖音原交易订单号 |
| `out_trans_id` | String | 32 | N | 抖音退款单号 |
| `payer_refund` | String | 12 | N | 退款给用户的金额，不含优惠券金额 |

## 退款查询 data 请求字段

| 参数 | 类型 | 长度 | 官网必填 | 条件与说明 |
| --- | --- | --- | --- | --- |
| `req_date` | String | 8 | Y | 本次查询请求日期，格式 `yyyyMMdd` |
| `req_seq_id` | String | 128 | Y | 本次查询请求流水号，同一 `huifu_id` 下当天唯一 |
| `huifu_id` | String | 32 | Y | 商户号 |
| `org_req_date` | String | 8 | Y | 退款请求日期，不是原支付交易日期 |
| `org_hf_seq_id` | String | 128 | C | 与 `org_req_seq_id` 二选一，不能都为空 |
| `org_req_seq_id` | String | 128 | C | 与 `org_hf_seq_id` 二选一，不能都为空 |

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

## 2026-10-25 官网更新同步

本地当前来源SHA-256：`fe45dca45e8fce7a5caa19eb54196c51715546675abbaa1081984eb768e332cb`。

本轮新增合单/子单请求、查询或通知字段；同名父容器按本接口和方向建模。官网通知中的`sub_trams_amt`拼写原样保留，不更改为其他字段名；split_fee_details的Object/String/数组语义也不得跨接口外推。完整嵌套类型、长度、条件和解码路径见 `payment-complete-field-catalog.md` 对应接口。

| 新增完整合同路径 | 中文名 | 类型 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- | --- |
| `request.data.sub_orders_request[]` | 子单退款信息列表 | `String` | `—` | `N` | 条件与完整原文见对应完整目录 |
| `request.data.sub_orders_request[].acct_split_bunch` | 分账对象 | `String` | `2048` | `N` | 条件与完整原文见对应完整目录 |
| `request.data.sub_orders_request[].acct_split_bunch.acct_infos` | 分账信息列表 | `String` | `2048` | `N` | 条件与完整原文见对应完整目录 |
| `request.data.sub_orders_request[].acct_split_bunch.acct_infos.div_amt` | 分账金额 | `String` | `14` | `Y` | 条件与完整原文见对应完整目录 |
| `request.data.sub_orders_request[].acct_split_bunch.acct_infos.huifu_id` | 分账接收方ID | `String` | `32` | `Y` | 条件与完整原文见对应完整目录 |
| `request.data.sub_orders_request[].org_sub_hf_seq_id` | 原子单交易全局流水号 | `String` | `128` | `N` | 条件与完整原文见对应完整目录 |
| `request.data.sub_orders_request[].org_sub_req_date` | 原子单交易请求日期 | `String` | `8` | `Y` | 条件与完整原文见对应完整目录 |
| `request.data.sub_orders_request[].org_sub_req_seq_id` | 原子单交易请求流水号 | `String` | `128` | `N` | 条件与完整原文见对应完整目录 |
| `request.data.sub_orders_request[].sub_huifu_id` | 子单商户号 | `String` | `32` | `Y` | 条件与完整原文见对应完整目录 |
| `request.data.sub_orders_request[].sub_ord_amt` | 子单申请退款金额 | `String` | `14` | `Y` | 条件与完整原文见对应完整目录 |
| `request.data.sub_orders_request[].sub_remark` | 子单备注 | `String` | `84` | `N` | 条件与完整原文见对应完整目录 |
| `request.data.sub_orders_request[].sub_req_date` | 子单请求日期 | `String` | `8` | `Y` | 条件与完整原文见对应完整目录 |
| `request.data.sub_orders_request[].sub_req_seq_id` | 子单请求流水号 | `String` | `128` | `Y` | 条件与完整原文见对应完整目录 |
