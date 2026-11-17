## 目录

- [接口概述](#接口概述)
- [应用场景](#应用场景)
- [SDK 映射](#sdk-映射)
- [公共请求参数](#公共请求参数)
- [请求参数 data](#请求参数-data)
- [同步响应 data 嵌套参数展开](#同步响应-data-嵌套参数展开)
- [请求示例](#请求示例)
- [同步返回参数](#同步返回参数)
- [业务返回码](#业务返回码)
- [文档勘误与实现备注](#文档勘误与实现备注)

# 托管交易退款查询

> 本文依据 2026-10-10 官方文档整理，适用于 `v2/trade/hosting/payment/queryRefundInfo`。

## 接口概述

| 属性 | 值 |
|------|-----|
| 请求方式 | `POST` |
| 汇付 API 端点 | `https://api.huifu.com/v2/trade/hosting/payment/queryRefundInfo` |
| SDK Request 类 | `V2TradeHostingPaymentQueryrefundinfoRequest` |
| Content-Type | `application/json;charset=UTF-8` |

说明：

- 支持 JSON 报文。
- 请求整体需要签名，验签规则见 `references/hostingpay-java-tech-spec.md`。
- 本接口为同步查询接口，没有独立异步通知。
- 查询的是退款交易，不是原支付交易。

## 应用场景

- 通过托管支付预下单发起的退款交易，都可以通过本接口查询退款处理结果。
- 适用于同步受理后的状态确认、退款轮询、退款异步回调后的结果核对。

## SDK 映射

`V2TradeHostingPaymentQueryrefundinfoRequest` 的独立 setter 字段：

| 字段 | setter | 类型 | 必填 | 说明 |
|------|--------|------|------|------|
| reqDate | `setReqDate()` | String(8) | Y | 本次查询请求日期，`yyyyMMdd` |
| reqSeqId | `setReqSeqId()` | String(128) | Y | 本次查询请求流水号，同一 `huifu_id` 下当天唯一 |
| huifuId | `setHuifuId()` | String(32) | Y | 商户号 |
| orgReqDate | `setOrgReqDate()` | String(8) | Y | 退款请求日期，`yyyyMMdd` |
| orgHfSeqId | `setOrgHfSeqId()` | String(128) | C | 退款全局流水号；与 `orgReqSeqId` 二选一，不能同时为空 |
| orgReqSeqId | `setOrgReqSeqId()` | String(128) | C | 退款请求流水号；与 `orgHfSeqId` 二选一，不能同时为空 |

说明：

- 这里的 `orgReqSeqId` 是退款请求流水号，不是原支付交易流水号。
- 一般优先使用退款请求时保存下来的 `req_seq_id` 作为查询条件。

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
| req_date | 请求日期 | String | 8 | Y | `yyyyMMdd` |
| req_seq_id | 请求流水号 | String | 128 | Y | 同一 `huifu_id` 下当天唯一 |
| huifu_id | 商户号 | String | 32 | Y | 开户自动生成 |
| org_req_date | 退款请求日期 | String | 8 | Y | `yyyyMMdd` |
| org_hf_seq_id | 退款全局流水号 | String | 128 | C | 与 `org_req_seq_id` 二选一，不能都为空 |
| org_req_seq_id | 退款请求流水号 | String | 128 | C | 与 `org_hf_seq_id` 二选一，不能都为空 |

## 同步响应 data 嵌套参数展开

以下对象全部属于 `response.data`，不是退款查询请求字段。完整路径、类型、长度和 Y/N/C 同时以 `payment-complete-field-catalog.md` 的“托管交易退款查询”为准。

### `response.data.acct_split_bunch`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| acct_infos | 分账明细 | Array | 2048 | Y | 分账明细 |

#### `response.data.acct_split_bunch.acct_infos[]`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| div_amt | 分账金额 | String | 14 | Y | 单位元，保留两位小数，最低 `0.01` |
| huifu_id | 分账接收方 ID | String | 32 | Y | 分账接收方 ID |
| acct_id | 账户号 | String | 16 | N | 账户号 |
| part_loan_amt | 垫资金额 | String | 12 | N | 单位元，保留两位小数；若由第三方全额垫资，则不传 |

### `response.data.split_fee_info`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| total_split_fee_amt | 分账手续费总金额 | String | 14 | N | 单位元 |
| split_fee_flag | 分账手续费扣款标志 | String | 1 | N | `1`=外扣，`2`=内扣 |
| split_fee_details | 分账手续费明细 | Array | - | N | 分账手续费明细 |

#### `response.data.split_fee_info.split_fee_details[]`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| split_fee_amt | 分账手续费金额 | String | 14 | Y | 单位元 |
| split_fee_huifu_id | 分账手续费承担方商户号 | String | 32 | Y | 分账手续费承担方商户号 |
| split_fee_acct_id | 分账手续费承担方账号 | String | 16 | Y | 分账手续费承担方账号 |

### `response.data.unionpay_response`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| coupon_info | 银联优惠信息 | String(JSON Array) | - | N | 银联使用优惠活动时出现；长度未声明 |

#### `response.data.unionpay_response.coupon_info[]`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| addnInfo | 附加信息 | String | 100 | N | 内容自定义 |
| spnsrId | 出资方 | String | 20 | N | `00010000`=银联出资，也可能为付款方机构代码或商户代码 |
| type | 项目类型 | String | 4 | N | `DD01`=随机立减，`CP01`=抵金券 |
| offstAmt | 抵消交易金额 | String | 14 | N | 不能为全 `0`，单位元 |
| id | 项目编号 | String | 40 | N | 用于票券编号等 |
| desc | 项目简称 | String | 40 | N | 优惠活动简称 |

### `response.data.dy_response`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| org_out_trans_id | 抖音原交易订单号 | String | 32 | N | 抖音原交易订单号 |
| out_trans_id | 抖音退款单号 | String | 32 | N | 抖音退款单号 |
| payer_refund | 用户退款金额 | String | 12 | N | 退款给用户的金额，不包含所有优惠券金额，单位元 |

## 请求示例

```json
{
  "sys_id": "6666000123123123",
  "product_id": "MYPAY",
  "data": {
    "req_date": "20231102",
    "req_seq_id": "20231102q111302328123112121122121112",
    "huifu_id": "6666000003100616",
    "org_hf_seq_id": "",
    "org_req_seq_id": "52022070919803411999411514",
    "org_req_date": "20240229"
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
| resp_code | 业务响应码 | String | 8 | Y | `00000000` 表示查询成功 |
| resp_desc | 业务响应信息 | String | 512 | Y | 业务返回描述 |
| req_date | 请求日期 | String | 8 | Y | `yyyyMMdd` |
| req_seq_id | 请求流水号 | String | 128 | Y | 本次查询请求流水号 |
| huifu_id | 商户号 | String | 32 | Y | 商户号 |
| org_hf_seq_id | 退款全局流水号 | String | 128 | N | 退款全局流水号 |
| org_req_date | 退款请求日期 | String | 8 | N | `yyyyMMdd` |
| org_req_seq_id | 退款请求流水号 | String | 128 | N | 退款请求流水号 |
| ord_amt | 退款金额 | String | 14 | N | 单位元，保留两位小数，最低 `0.01` |
| actual_ref_amt | 实际退款金额 | String | 14 | N | 扫码退款返回 |
| trans_stat | 交易状态 | String | 1 | N | `P`=处理中，`S`=成功，`F`=失败，`I`=初始；官方行内示例写成 `TRANS_REFUND`，但该值不是状态枚举，代码和示例必须按 `P/S/F/I` 处理 |
| bank_code | 通道返回码 | String | 64 | N | 通道返回码 |
| bank_message | 通道返回描述 | String | 256 | N | 通道返回描述 |
| fee_amt | 退款返还手续费 | String | 14 | N | 单位元，保留两位小数 |
| acct_split_bunch | 分账对象 | String(JSON Object) | - | N | 分账对象，见上文 `acct_split_bunch` |
| split_fee_info | 分账手续费信息 | String(JSON Object) | - | N | 分账手续费信息，见上文 `split_fee_info` |
| org_party_order_id | 原交易用户账单上的商户订单号 | String | 64 | N | 扫码退款返回 |
| remark | 备注 | String | 84 | N | 扫码退款返回，原样返回 |
| loan_flag | 是否垫资退款 | String | 2 | N | `Y`=垫资出款，`N`=普通出款，默认 `N`；延时交易退款如已在“交易确认退款”接口设置垫资，这里不可再次设置 |
| loan_undertaker | 垫资承担者 | String | 32 | N | 垫资方的 `huifu_id` |
| loan_acct_type | 垫资账户类型 | String | 2 | N | `01`=基本户，`05`=充值户，默认充值户 |
| org_out_order_id | 原外部订单号 | String | 128 | N | 扫码退款返回 |
| unionpay_response | 银联返回的响应报文 | String(JSON Object) | 6000 | N | 扫码退款返回 |
| dy_response | 抖音返回的响应报文 | String(JSON Object) | 6000 | N | 先解码JSON对象字符串，再读取子字段 |
| trans_finish_time | 退款完成时间 | String | 14 | N | `yyyyMMddHHmmss` |

`dy_response:String(JSON Object)(6000)` 的编码已由正式说明明确，先解码字符串再读取退款子字段，旧编码疑义已关闭。

### 同步成功示例

```json
{
  "data": {
    "resp_code": "00000000",
    "resp_desc": "操作成功",
    "huifu_id": "6666000003100616",
    "org_hf_seq_id": "0056default240305162924Pa41a9ac1984fd843",
    "org_req_date": "20240229",
    "org_req_seq_id": "52022070919803411999411514",
    "ord_amt": "0.01",
    "actual_ref_amt": "",
    "trans_stat": "S",
    "bank_code": "00",
    "bank_message": "交易成功",
    "fee_amt": "0.00",
    "acct_split_bunch": "{\"acct_infos\":[{\"acct_id\":\"B00164310\",\"div_amt\":\"0.01\",\"huifu_id\":\"6666000003100616\"}]}",
    "split_fee_info": "{\"total_split_fee_amt\":0}",
    "org_party_order_id": "202403051611224y3v28C1Y0",
    "org_out_order_id": "20240305161117defaultit671658378",
    "req_date": "20231102",
    "req_seq_id": "20231102q111302328123112121122121112"
  }
}
```

## 业务返回码

| 返回码 | 返回描述 | 处理 |
|--------|----------|------|
| 00000000 | 查询成功 | 继续结合 `trans_stat` 判断退款结果 |
| 其他 | 参见官方业务返回码页面 | 结合 `resp_desc`、`bank_code`、`bank_message` 排查 |

## 文档勘误与实现备注

- 公共返回参数表声明顶层 `sign` 必返，但官方成功示例只展示了 `data`，没有展示 `sign`。
- 2026-10-10官网已将 `trans_stat` 示例修正为 S；枚举仍为P/S/F/I。I需联系汇付技术，不能改作退款成功。
- `unionpay_response` 是JSON对象字符串，解码后其 `coupon_info` 仍是JSON数组字符串；先读取coupon_info，再二次解码为数组后遍历。Object/Array旧冲突已关闭，容器长度仍未声明。
- `actual_ref_amt` 在官方成功示例里给的是空字符串，但字段表定义为金额字段；消费方不要只按数值型做强解析。
- 本页与退款申请异步的 `split_fee_acct_id` 长度均为16，旧跨页长度冲突已关闭；本页Y、退款异步N各自保留。
- 本页 `org_req_date`、`org_req_seq_id` 指向退款请求本身，不是原支付交易；这是退款查询最容易用错的地方。

## 2026-10-25 官网更新同步

本地当前来源SHA-256：`4b78ba8567f606a870076d9f637fe064b21743f8139382c7a06e9016e5449f0c`。

本轮新增合单/子单请求、查询或通知字段；同名父容器按本接口和方向建模。官网通知中的`sub_trams_amt`拼写原样保留，不更改为其他字段名；split_fee_details的Object/String/数组语义也不得跨接口外推。完整嵌套类型、长度、条件和解码路径见 `payment-complete-field-catalog.md` 对应接口。

| 新增完整合同路径 | 中文名 | 类型 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- | --- |
| `response.data.sub_orders_response[]` | 退款子单返回信息列表 | `String` | `—` | `N` | 条件与完整原文见对应完整目录 |
| `response.data.sub_orders_response[].acct_split_bunch` | 分账信息 | `String` | `4000` | `N` | 条件与完整原文见对应完整目录 |
| `response.data.sub_orders_response[].acct_split_bunch.acct_infos` | 分账明细 | `String` | `2048` | `N` | 条件与完整原文见对应完整目录 |
| `response.data.sub_orders_response[].acct_split_bunch.acct_infos.div_amt` | 分账金额 | `String` | `14` | `Y` | 条件与完整原文见对应完整目录 |
| `response.data.sub_orders_response[].acct_split_bunch.acct_infos.huifu_id` | 分账接收方ID | `String` | `32` | `Y` | 条件与完整原文见对应完整目录 |
| `response.data.sub_orders_response[].acct_split_bunch.fee_amt` | 退款返还手续费 | `String` | `14` | `Y` | 条件与完整原文见对应完整目录 |
| `response.data.sub_orders_response[].fund_freeze_stat` | 资金冻结状态 | `String` | `16` | `N` | 条件与完整原文见对应完整目录 |
| `response.data.sub_orders_response[].split_fee_info` | 分账手续费信息 | `String` | `—` | `N` | 条件与完整原文见对应完整目录 |
| `response.data.sub_orders_response[].split_fee_info.split_fee_details[]` | 分账手续费明细 | `String` | `—` | `Y` | 条件与完整原文见对应完整目录 |
| `response.data.sub_orders_response[].split_fee_info.split_fee_details[].split_fee_acct_id` | 分账手续费承担方账号 | `String` | `9` | `N` | 条件与完整原文见对应完整目录 |
| `response.data.sub_orders_response[].split_fee_info.split_fee_details[].split_fee_amt` | 分账手续费金额 | `String` | `14` | `Y` | 条件与完整原文见对应完整目录 |
| `response.data.sub_orders_response[].split_fee_info.split_fee_details[].split_fee_huifu_id` | 分账手续费承担方商户号 | `String` | `32` | `Y` | 条件与完整原文见对应完整目录 |
| `response.data.sub_orders_response[].split_fee_info.split_fee_flag` | 分账手续费扣款标志 | `Integer` | `1` | `Y` | 条件与完整原文见对应完整目录 |
| `response.data.sub_orders_response[].split_fee_info.total_split_fee_amt` | 分账手续费总金额(元) | `String` | `14` | `N` | 条件与完整原文见对应完整目录 |
| `response.data.sub_orders_response[].sub_actual_ref_amt` | 子单实际退款金额 | `String` | `14` | `N` | 条件与完整原文见对应完整目录 |
| `response.data.sub_orders_response[].sub_hf_seq_id` | 退款子单全局流水号 | `String` | `128` | `N` | 条件与完整原文见对应完整目录 |
| `response.data.sub_orders_response[].sub_huifu_id` | 退款子单商户号 | `String` | `32` | `N` | 条件与完整原文见对应完整目录 |
| `response.data.sub_orders_response[].sub_ord_amt` | 子单退款金额 | `String` | `14` | `N` | 条件与完整原文见对应完整目录 |
| `response.data.sub_orders_response[].sub_org_fee_amt` | 原子单交易手续费 | `String` | `14` | `N` | 条件与完整原文见对应完整目录 |
| `response.data.sub_orders_response[].sub_org_ord_amt` | 原子单交易订单金额 | `String` | `14` | `N` | 条件与完整原文见对应完整目录 |
| `response.data.sub_orders_response[].sub_org_req_date` | 原子单交易请求日期 | `String` | `8` | `N` | 条件与完整原文见对应完整目录 |
| `response.data.sub_orders_response[].sub_org_req_seq_id` | 原子单交易请求流水号 | `String` | `128` | `N` | 条件与完整原文见对应完整目录 |
| `response.data.sub_orders_response[].sub_ref_cut` | 子单累计退款次数 | `String` | `14` | `N` | 条件与完整原文见对应完整目录 |
| `response.data.sub_orders_response[].sub_remark` | 子单备注 | `String` | `1500` | `N` | 条件与完整原文见对应完整目录 |
| `response.data.sub_orders_response[].sub_req_date` | 退款子单请求日期 | `String` | `8` | `N` | 条件与完整原文见对应完整目录 |
| `response.data.sub_orders_response[].sub_req_seq_id` | 退款子单请求流水号 | `String` | `128` | `N` | 条件与完整原文见对应完整目录 |
| `response.data.sub_orders_response[].sub_total_ref_amt` | 原子单交易累计退款金额 | `String` | `14` | `N` | 条件与完整原文见对应完整目录 |
| `response.data.sub_orders_response[].sub_total_ref_fee_amt` | 原子单交易累计退款手续费金额 | `String` | `14` | `N` | 条件与完整原文见对应完整目录 |
| `response.data.sub_orders_response[].sub_trans_date` | 子单退款交易发生日期 | `String` | `8` | `N` | 条件与完整原文见对应完整目录 |
