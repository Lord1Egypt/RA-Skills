## 目录

- [接口概述](#接口概述)
- [应用场景](#应用场景)
- [SDK 映射](#sdk-映射)
- [公共请求参数](#公共请求参数)
- [请求参数 data](#请求参数-data)
- [嵌套参数展开](#嵌套参数展开)
- [请求示例](#请求示例)
- [同步返回参数](#同步返回参数)
- [业务返回码](#业务返回码)
- [文档勘误与实现备注](#文档勘误与实现备注)

# 托管交易退款查询

> 本文依据 2026-05-22 官方文档整理，适用于 `v2/trade/hosting/payment/queryRefundInfo`。

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

## 嵌套参数展开

### acct_split_bunch

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| acct_infos | 分账明细 | Array | 2048 | Y | 分账明细 |

#### acct_split_bunch.acct_infos[]

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| div_amt | 分账金额 | String | 14 | Y | 单位元，保留两位小数，最低 `0.01` |
| huifu_id | 分账接收方 ID | String | 32 | Y | 分账接收方 ID |
| acct_id | 账户号 | String | 16 | N | 账户号 |
| part_loan_amt | 垫资金额 | String | 12 | N | 单位元，保留两位小数；若由第三方全额垫资，则不传 |

### split_fee_info

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| total_split_fee_amt | 分账手续费总金额 | String | 14 | N | 单位元 |
| split_fee_flag | 分账手续费扣款标志 | String | 1 | N | `1`=外扣，`2`=内扣 |
| split_fee_details | 分账手续费明细 | Array | - | N | 分账手续费明细 |

#### split_fee_info.split_fee_details[]

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| split_fee_amt | 分账手续费金额 | String | 14 | Y | 单位元 |
| split_fee_huifu_id | 分账手续费承担方商户号 | String | 32 | Y | 分账手续费承担方商户号 |
| split_fee_acct_id | 分账手续费承担方账号 | String | 16 | Y | 分账手续费承担方账号 |

### unionpay_response

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| coupon_info | 银联优惠信息 | Object | - | N | 银联使用优惠活动时出现；官方说明同时写为 `jsonArray` 格式 |

#### unionpay_response.coupon_info[]

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| addnInfo | 附加信息 | String | 100 | N | 内容自定义 |
| spnsrId | 出资方 | String | 20 | Y | `00010000`=银联出资，也可能为付款方机构代码或商户代码 |
| type | 项目类型 | String | 4 | Y | `DD01`=随机立减，`CP01`=抵金券 |
| offstAmt | 抵消交易金额 | String | 14 | Y | 不能为全 `0`，单位元 |
| id | 项目编号 | String | 40 | N | 用于票券编号等 |
| desc | 项目简称 | String | 40 | N | 优惠活动简称 |

### dy_response

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
| dy_response | 抖音返回的响应报文 | String(JSON Object) | 6000 | N | 抖音响应报文 |
| trans_finish_time | 退款完成时间 | String | 14 | N | `yyyyMMddHHmmss` |

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
- `trans_stat` 的说明列给出了 `P/S/F/I` 四种状态，但同一行示例值写成 `TRANS_REFUND`；当前保留该官方冲突记录，字段取值仍只按 `P/S/F/I` 输出和解析，不要生成 `TRANS_REFUND` 作为 `trans_stat` 示例。
- `unionpay_response.coupon_info` 的类型列写为 `Object`，说明又写成 `jsonArray` 格式；当前按“对象中承载数组语义”理解，并展开为 `coupon_info[]`。
- `actual_ref_amt` 在官方成功示例里给的是空字符串，但字段表定义为金额字段；消费方不要只按数值型做强解析。
- `split_fee_acct_id` 在本页长度写为 `16`，而退款申请异步文档中的同名字段长度写为 `9`；当前按本页官方表保留，并显式记录跨页不一致。
- 本页 `org_req_date`、`org_req_seq_id` 指向退款请求本身，不是原支付交易；这是退款查询最容易用错的地方。
