# 聚合支付退款

这份文档覆盖聚合支付退款申请和退款查询。

本页用于退款流程、定位键和高风险字段解释，不是完整 DTO。请求、同步响应、异步通知及所有嵌套字段的类型、长度、Y/N/C 必须读取 `references/payment-complete-field-catalog.md` 的“交易退款”；退款查询联读目录中的“交易退款查询”。

## 目录

- 什么时候读这里
- 退款主流程
- 对应接口
- 请求头强制约束
- 退款申请 data 请求字段
- 退款申请返回参数
- 退款申请扩展返回字段
- 退款异步返回参数
- 退款查询 data 请求字段
- 关键定位字段
- 核心规则
- 退款期限
- 容易混淆的流水号
- 当前语言边界
- 回读建议

## 什么时候读这里

- 原交易已确认支付成功
- 需要调用聚合支付退款接口
- 需要轮询或查询退款结果

## 退款主流程

```text
确认原交易成功且定位键完整
  -> 发起退款
  -> 处理中时等待异步通知或主动查询
  -> 查询最终退款状态
  -> 成功后再更新业务退款状态
```

## 对应接口

| 场景 | 接口 |
| --- | --- |
| 退款申请 | `v4/trade/payment/scanpay/refund` |
| 退款查询 | `v4/trade/payment/scanpay/refundquery` |

## 请求头强制约束

- 上面 2 个接口都必须带 `jpt-x-skill-source: <skill_source>`
- 如果当前按 PHP 接入，且请求 `data` 中存在 `huifu_id`，还必须带 `jpt-x-skill-huifu_id: <data.huifu_id>`
- 当前 Skill 包对齐的官方 PHP SDK 主链路在 `MerConfig.skill_source` 已配置时，会自动带 `jpt-x-skill-source`，并在当前请求 `huifu_id` 存在且非空时自动带 `jpt-x-skill-huifu_id`
- 当前 Java SDK 基线也会在请求 `data` 中存在 `huifu_id` 且非空时自动带 `jpt-x-skill-huifu_id: <data.huifu_id>`
- 这两项属于 HTTP 请求头，不属于业务报文 `data`；具体明细以 `references/shared-request-header-policy.md` 为准

## 退款申请 data 请求字段

| 参数 | 类型 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `req_date` | String | 8 | Y | 本次退款请求日期，格式 `yyyyMMdd` |
| `req_seq_id` | String | 128 | Y | 本次退款请求流水号，同一 `huifu_id` 下当天唯一 |
| `huifu_id` | String | 32 | Y | 商户号 |
| `ord_amt` | String | 14 | Y | 申请退款金额，单位元，保留两位小数；延时交易退款金额必须小于等于待确认金额 |
| `org_req_date` | String | 8 | Y | 原交易请求日期，格式 `yyyyMMdd` |
| `org_hf_seq_id` | String | 128 | N | 官网标记 N；条件上与 `org_party_order_id`、`org_req_seq_id` 三选一 |
| `org_party_order_id` | String | 64 | N | 官网标记 N；条件上与另外两项三选一 |
| `org_req_seq_id` | String | 128 | N | 官网标记 N；条件上与另外两项三选一 |
| `remark` | String | 84 | N | 备注，原样返回 |
| `notify_url` | String | 512 | N | 退款异步通知地址 |
| `acct_split_bunch` | String(JSON Object) | 2048 | N | 分账退款对象 |
| `combinedpay_data` | String(JSON Array) | 官方未给定 | N | 补贴支付退款信息 |
| `terminal_device_data` | String(JSON Object) | 2048 | N | 设备信息 |

### 交易能力扩展字段

字段结论必须明确：请求侧不传 `tx_metadata` 包装层；不要传 `tx_metadata`；按实际扩展能力直接传它下面的字段，例如 `acct_split_bunch`、`combinedpay_data`、`terminal_device_data`。

#### `acct_split_bunch.acct_infos[]`

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `div_amt` | Y | 分账金额，单位元，保留两位小数 |
| `huifu_id` | Y | 分账接收方 ID |

#### `acct_split_bunch.confirm_acct_infos[]`

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `confirm_hf_seq_id` | Y | 交易确认单号 |
| `div_amt` | Y | 确认分账退款金额，单位元，保留两位小数 |
| `huifu_id` | Y | 分账接收方 ID |

#### `combinedpay_data[]`

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `huifu_id` | Y | 渠道与一级代理商直属商户 ID |
| `user_type` | Y | 补贴方类型：`channel`、`merchant`、`agent`、`mertomer` |
| `acct_id` | Y | 营销补贴方账户号 |
| `amount` | Y | 补贴金额，单位元，保留两位小数 |

#### `terminal_device_data`

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `device_type` | N | `1` 手机，`2` 平板，`3` 手表，`4` PC |
| `device_ip` | N | 交易设备公网 IP，当前建议按 IPv4 传 |
| `device_mac` | N | 交易设备 MAC |
| `device_imei` | N | 交易设备 IMEI |
| `device_imsi` | N | 交易设备 IMSI |
| `device_icc_id` | N | 交易设备 ICCID |
| `device_wifi_mac` | N | 交易设备 WIFI MAC |
| `device_gps` | N | 交易设备 GPS |

## 退款申请返回参数

退款申请同步返回只表示接口受理或当前处理结果，不是退款终态。`resp_code=00000000` 或 `00000100` 时仍要走退款查询和异步通知闭环。

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `resp_code` | Y | 业务响应码 |
| `resp_desc` | Y | 业务响应信息 |
| `product_id` | Y | 产品号，原样返回 |
| `req_date` | Y | 退款请求日期，原样返回 |
| `req_seq_id` | Y | 退款请求流水号，原样返回 |
| `huifu_id` | Y | 商户号 |
| `ord_amt` | N | 退款金额 |
| `actual_ref_amt` | N | 实际退款金额 |
| `hf_seq_id` | N | 退款全局流水号 |
| `org_req_date` | N | 原交易请求日期 |
| `org_req_seq_id` | N | 原交易请求流水号 |
| `org_hf_seq_id` | N | 原交易全局流水号 |
| `trans_date` | N | 退款交易发生日期，`yyyyMMdd` |
| `trans_time` | N | 退款交易发生时间，`HHmmss` |
| `trans_finish_time` | N | 退款完成时间，`yyyyMMddHHmmss` |
| `trans_stat` | N | `P` 处理中，`S` 成功，`F` 失败 |
| `bank_message` | N | 通道返回描述 |
| `fund_freeze_stat` | N | 退款发生时原交易资金冻结状态，`FREEZE` 冻结，`UNFREEZE` 解冻 |
| `pay_channel` | N | 交易通道：`A` 支付宝，`T` 微信，`U` 银联二维码，`D` 数字货币 |
| `fee_amount` | N | 退款返还手续费 |
| `trade_type` | N | 交易类型，当前为 `TRANS_REFUND` |
| `tx_metadata` | N | 扩展参数集合；只为文档展示和返回承载，退款请求仍不要上送 `tx_metadata` 包装层 |
| `acct_split_bunch` | N | 分账退款信息 |
| `combinedpay_data` | N | 补贴支付退款信息 |
| `terminal_device_data` | N | 设备信息 |

## 退款申请扩展返回字段

### `tx_metadata.acct_split_bunch`

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `acct_infos` | N | 分账明细 |
| `confirm_acct_infos` | N | 交易确认分账明细 |
| `fee_amount` / `fee_amt` | N | 退款返还手续费；官方同步/异步页字段名存在差异，解析时兼容 |

`acct_infos[]` 字段：

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `div_amt` | Y | 分账退款金额 |
| `huifu_id` | Y | 分账接收方 ID |

`confirm_acct_infos[]` 字段：

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `confirm_hf_seq_id` | Y | 交易确认单号 |
| `div_amt` | Y | 确认分账退款金额 |
| `huifu_id` | Y | 分账接收方 ID |
| `confirm_refund_status` | N | 交易确认退款状态，`P` 处理中，`S` 成功，`F` 失败；为空代表不走交易确认退款 |

### `wx_response`

| 字段路径 | 类型 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `sub_appid` | String | 32 | N | 子商户公众账号 ID |
| `sub_mch_id` | String | 32 | N | 子商户号 |
| `org_out_trans_id` | String | 32 | N | 微信订单号 |
| `out_trans_id` | String | 32 | N | 微信退款单号 |
| `cash_fee` | String | 12 | N | 现金支付金额，单位元 |
| `cash_refund_fee` | String | 12 | N | 现金退款金额，单位元 |
| `coupon_refund_fee` | String | 12 | N | 代金券退款总金额 |
| `coupon_refund_count` | Integer | 12 | N | 退款代金券使用数量 |
| `refund_coupon_info[]` | Array | 1024 | N | 退款代金券信息 |
| `promotion_detail[]` | Array | 官方未给定 | N | 优惠详情 |
| `user_received_account` | String | 64 | N | 退款入账账户 |

`wx_response.refund_coupon_info[]`：

| 字段路径 | 类型 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `coupon_type` | String | 8 | N | `CASH` 充值代金券、`NO_CASH` 非充值代金券 |
| `coupon_refund_id` | String | 20 | N | 退款代金券 ID |
| `coupon_refund_fee` | String | 11 | N | 单个退款代金券金额 |

`wx_response.promotion_detail[]`：

| 字段路径 | 类型 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `promotion_id` | String | 32 | Y | 券或立减优惠 ID |
| `scope` | String | 32 | N | `GLOBAL` 全场、`SINGLE` 单品 |
| `type` | String | 32 | N | `COUPON` 代金券、`DISCOUNT` 优惠券 |
| `refund_amount` | String | 32 | N | 代金券退款金额 |
| `amount` | String | 32 | N | 券面额 |
| `goods_detail[]` | Array | 官方未给定 | N | 单品优惠退款商品明细 |

`wx_response.promotion_detail[].goods_detail[]`：

| 字段路径 | 类型 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `goods_id` | String | 32 | Y | 商户商品编码 |
| `wxpay_goods_id` | String | 32 | N | 微信支付商品编码 |
| `goods_name` | String | 14 | N | 商品名称 |
| `refund_amt` | String | 11 | Y | 商品退款金额 |
| `refund_quantity` | Integer | 11 | Y | 商品退款数量 |
| `price` | String | 11 | Y | 商品优惠后单价 |

### `dc_response`

| 字段路径 | 类型 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `merchant_id` | String | 35 | N | 商户号 |
| `sub_merchant_id` | String | 35 | N | 子商户号 |
| `openid` | String | 64 | N | 用户标识 |
| `sub_openid` | String | 64 | N | 用户子标识 |
| `custom_bank_code` | String | 14 | N | 客户所属运营机构代码 |
| `custom_bank_name` | String | 70 | N | 客户所属运营机构名称 |
| `coupon_refund_count` | String | 3 | N | 退款代金券数量；注意此处官方类型为 String，与微信对象不同 |
| `coupon_refund_list[]` | Array | 2048 | N | 退款代金券集合 |
| `refund_recv_wallet_id` | String | 22 | N | 退款入账钱包 ID |

`dc_response.coupon_refund_list[]`：

| 字段路径 | 类型 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | String | 40 | N | 退款代金券 ID |
| `type` | String | 8 | N | 退款代金券类型 |
| `amount` | String | 14 | N | 单个退款代金券金额 |

### 其他扩展返回对象

| 对象 | 类型/长度 | 说明 |
| --- | --- | --- |
| `combinedpay_data` | Array / 官方未给定 | 补贴支付退款信息 |
| `combinedpay_data_fee_info` | Object / 官方未给定 | 含 `huifu_id`、`acct_id`、`combinedpay_fee_amt` |
| `trans_fee_ref_allowance_info` | Object / 官方未给定 | 含 `receivable_ref_fee_amt`、`actual_ref_fee_amt`、`allowance_ref_fee_amt` |
| `unionpay_response` | Object / 官方未给定 | 银联优惠退款信息 |

## 退款异步返回参数

退款异步通知字段比同步受理字段更完整，业务侧应按异步通知验签、幂等和退款查询闭环处理。

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `resp_code` | Y | 业务响应码 |
| `resp_desc` | Y | 业务响应信息 |
| `huifu_id` | Y | 商户号 |
| `req_date` | Y | 退款请求日期 |
| `req_seq_id` | Y | 退款请求流水号 |
| `hf_seq_id` | N | 退款全局流水号 |
| `org_req_date` | N | 原交易请求日期 |
| `org_req_seq_id` | N | 原交易请求流水号 |
| `org_ord_amt` | Y | 原交易订单金额 |
| `org_fee_amt` | Y | 原交易手续费 |
| `trans_date` | Y | 退款交易发生日期 |
| `trans_time` | N | 退款交易发生时间 |
| `trans_finish_time` | N | 退款完成时间 |
| `trans_type` | Y | 交易类型，`TRANS_REFUND` |
| `trans_stat` | N | `P` 处理中，`S` 成功，`F` 失败 |
| `ord_amt` | Y | 本次退款金额 |
| `actual_ref_amt` | N | 实际退款金额 |
| `total_ref_amt` | Y | 原交易累计退款金额 |
| `total_ref_fee_amt` | Y | 原交易累计退款手续费金额 |
| `ref_cut` | Y | 累计退款次数 |
| `party_order_id` | N | 微信 / 支付宝用户账单上的商户单号 |
| `bank_code` | N | 通道返回码 |
| `bank_message` | N | 通道返回描述 |
| `fund_freeze_stat` | N | 原交易资金冻结状态 |
| `pay_channel` | N | `A` 支付宝，`T` 微信，`U` 银联二维码，`D` 数字货币 |
| `is_confirm_refund_flag` | N | 是否已延迟分账，`Y` 是，`N` 否，默认 `N` |
| `is_refund_fee_flag` | N | 是否退还手续费；支付宝直连场景返回，`Y` 或空=退费，`N`=不退费 |
| `acct_split_bunch` | Y | 分账信息；含 `acct_infos`、`confirm_acct_infos` 和退款返还手续费 |
| `wx_response` | N | 微信返回响应，含退款券和营销明细时展开解析 |
| `dc_response` | N | 数字人民币响应报文 |
| `combinedpay_data` | N | 补贴支付信息 |
| `combinedpay_data_fee_info` | N | 补贴支付手续费承担方信息 |
| `unionpay_response` | N | 银联响应报文 |
| `trans_fee_ref_allowance_info` | N | 手续费补贴返还信息 |
| `remark` | N | 备注，最长 1500，原样返回 |

## 退款查询 data 请求字段

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `huifu_id` | Y | 商户号 |
| `org_req_date` | C | 退款请求日期；传退款全局流水号时可不传 |
| `org_hf_seq_id` | C | 退款全局流水号；与 `org_req_seq_id`、`mer_ord_id` 三选一 |
| `org_req_seq_id` | C | 退款请求流水号；与 `org_hf_seq_id`、`mer_ord_id` 三选一 |
| `mer_ord_id` | C | 终端订单号；与 `org_hf_seq_id`、`org_req_seq_id` 三选一 |

查询补充说明：

- 退款查询里的 `org_req_seq_id` 指的是退款请求流水号，不是原支付流水号。
- 查询返回字段和勘误说明继续看 `references/aggregation-refund-query.md`。

## 关键定位字段

- 原交易定位键：`org_hf_seq_id`、`org_party_order_id`、`org_req_seq_id` 三选一；退款申请时 `org_req_date` 仍是必带字段
- 退款查询定位键：退款交易自己的 `org_hf_seq_id`、退款 `org_req_seq_id`、`mer_ord_id` 三选一

## 核心规则

1. 退款金额不能超过原交易金额
2. `resp_code=00000000` 或 `00000100` 只表示请求已受理
3. 退款最终结果必须以退款查询和异步通知闭环为准
4. 退款结果要做幂等处理

## 退款期限

| 渠道 | 最大退款期限 |
| --- | --- |
| 微信 | `360` 天 |
| 支付宝 | `360` 天 |
| 银联二维码 | `360` 天 |

## 容易混淆的流水号

```text
原交易下单：A001
退款请求：B001，且 org_req_seq_id = A001
退款查询：查询的是 B001，不是 A001
```

## 当前语言边界

| 方面 | 聚合支付退款当前文档链路 | 托管支付退款 |
|------|---------------------|-----------|
| SDK | dg-lightning-sdk | dg-java-sdk |
| org_req_seq_id | 有独立 setter，直接调用 | **无 setter**，必须 extendInfoMap |
| remark/notify_url | **无 setter**，通过 `client.optional()` | 通过 extendInfoMap |
| 交易能力扩展字段 | 请求侧不传 `tx_metadata` 包装层；不要传 `tx_metadata`；按能力名直接传 `acct_split_bunch` / `combinedpay_data` / `terminal_device_data` | 通过 extendInfoMap / setter |
| 调用方式 | `client.refund(req)` | `BasePayClient.request(req, false)` |



- Java 提供完整路径
- 聚合支付 PHP 已支持 `Payment::refund()` 与 `Payment::refundQuery()`；示例入口见 `references/aggregation-query-php-scenarios.md`

## 回读建议

- 需要看退款查询完整返回字段：读 `references/aggregation-refund-query.md`
- 还没做最终支付确认：先读 `references/aggregation-query.md`
- 还没完成初始化：回到 `references/aggregation-base.md`
