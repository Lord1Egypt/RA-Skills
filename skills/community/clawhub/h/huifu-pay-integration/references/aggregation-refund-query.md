# 聚合扫码交易退款查询

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
| 接口名称 | 扫码交易退款查询 |
| 汇付端点 | `POST /v4/trade/payment/scanpay/refundquery` |
| 官方最近更新时间 | `2026-05-28` |
| 支持格式 | `JSON` |
| 支持交易 | `T_JSAPI`、`T_MINIAPP`、`T_APP`、`A_JSAPI`、`A_NATIVE`、`U_NATIVE`、`U_JSAPI`、`T_MICROPAY`、`A_MICROPAY`、`U_MICROPAY` |
| 签名说明 | [接入指引-开发指南](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |

商家调用退款接口后未收到状态返回时，可调用本接口查询退款结果。

## SDK 映射

| 项 | 值 |
| --- | --- |
| SDK Request 类 | `TradePaymentScanpayRefundQueryRequest` |
| 包路径 | `com.huifu.dg.lightning.models.payment` |
| SDK Client 方法 | `Factory.Payment.Common().refundQuery(request)` |

`TradePaymentScanpayRefundQueryRequest` 常用字段映射：

| 字段 | setter | 必填 | 说明 |
| --- | --- | --- | --- |
| `huifu_id` | `setHuifuId()` | Y | 商户号 |
| `org_req_date` | `setOrgReqDate()` | C | 退款请求日期，传退款全局流水号时非必填 |
| `org_hf_seq_id` | `setOrgHfSeqId()` | C | 退款全局流水号，三选一 |
| `org_req_seq_id` | `setOrgReqSeqId()` | C | 退款请求流水号，三选一 |
| `mer_ord_id` | `setMerOrdId()` | C | 终端订单号，三选一 |

## 公共参数

### 公共请求参数

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `sys_id` | String | 32 | Y | 渠道商、代理商或商户的 `huifu_id` |
| `product_id` | String | 32 | Y | 汇付分配的产品号，例如 `YYZY` |
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
| `huifu_id` | String | 32 | Y | 商户号 |
| `org_req_date` | String | 8 | C | 退款请求日期，格式 `yyyyMMdd`；传入 `org_hf_seq_id` 时非必填 |
| `org_hf_seq_id` | String | 128 | C | 退款全局流水号，和 `org_req_seq_id`、`mer_ord_id` 三选一 |
| `org_req_seq_id` | String | 128 | C | 退款请求流水号，和 `org_hf_seq_id`、`mer_ord_id` 三选一 |
| `mer_ord_id` | String | 50 | C | 终端订单号，和 `org_hf_seq_id`、`org_req_seq_id` 三选一 |

### 查询规则

- `org_hf_seq_id`、`org_req_seq_id`、`mer_ord_id` 不能同时为空。
- 使用 `org_hf_seq_id` 查询时，`org_req_date` 可不传；其他场景建议必传。
- 这里的 `org_req_seq_id` 指的是退款请求流水号，不是原支付流水号。
- `trans_stat` 才是退款最终状态；`resp_code=00000000` 仅表示查询动作成功。

## 同步返回参数

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `resp_code` | String | 8 | Y | 业务响应码，见[业务返回码](#业务返回码) |
| `resp_desc` | String | 512 | Y | 业务响应信息 |
| `huifu_id` | String | 32 | Y | 商户号 |
| `org_hf_seq_id` | String | 128 | N | 退款全局流水号 |
| `org_req_date` | String | 8 | N | 退款请求日期 |
| `org_req_seq_id` | String | 128 | N | 退款请求流水号 |
| `ord_amt` | String | 14 | Y | 退款金额，单位元 |
| `actual_ref_amt` | String | 14 | N | 实际退款金额，单位元 |
| `trans_date` | String | 8 | N | 交易发生日期 |
| `trans_time` | String | 6 | N | 交易发生时间，`HHMMSS` |
| `trade_type` | String | 20 | N | 交易类型，示例值 `TRANS_REFUND` |
| `trans_stat` | String | 1 | N | `P` 处理中，`S` 成功，`F` 失败，`I` 初始 |
| `bank_code` | String | 64 | N | 通道返回码 |
| `bank_message` | String | 256 | N | 通道返回描述 |
| `fee_amount` | String | 14 | N | 手续费金额，单位元 |
| `trans_finish_time` | String | 14 | N | 退款完成时间，`yyyyMMddHHmmss` |
| `pay_channel` | String | 1 | N | `A` 支付宝，`T` 微信，`U` 银联二维码，`D` 数字货币 |
| `remark` | String | 84 | N | 退款时上送的备注，原样返回 |
| `tx_metadata` | String | - | N | 扩展参数集合，JSON 字符串 |

## 扩展返回参数

### `tx_metadata`

| 参数 | 定义 | 说明 |
| --- | --- | --- |
| `acct_split_bunch` | Object | 分账对象 |
| `split_fee_info` | Object | 分账手续费信息 |

`acct_split_bunch` 字段：

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `acct_infos` | Array | 2048 | N | 分账信息列表 |
| `is_clean_split` | String | 1 | N | `Y` 使用净值分账，仅在 `percentage_flag=Y` 时起作用 |

`acct_infos` 字段：

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `div_amt` | String | 14 | Y | 分账金额，单位元 |
| `huifu_id` | String | 16 | Y | 分账商户号 |

`split_fee_info` 字段：

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `total_split_fee_amt` | String | 14 | N | 分账手续费总金额，单位元 |
| `split_fee_flag` | Integer | 1 | Y | `1` 外扣，`2` 内扣 |
| `split_fee_details` | Array | - | Y | 分账手续费明细 |

`split_fee_details` 字段：

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `split_fee_amt` | String | 14 | Y | 分账手续费金额 |
| `split_fee_huifu_id` | String | 32 | Y | 分账手续费承担方商户号 |
| `split_fee_acct_id` | String | 32 | N | 分账手续费承担方账号 |

## 请求示例

```json
{
  "sys_id": "6666000003100616",
  "product_id": "MYPAY",
  "data": {
    "org_hf_seq_id": "0031000topA250804164514P944c0a842bf00000",
    "huifu_id": "6666000003100616"
  },
  "sign": "<SDK_AUTOGENERATED_SIGNATURE>"
}
```

## 返回示例

```json
{
  "data": {
    "acct_split_bunch": "{}",
    "actual_ref_amt": "0.03",
    "bank_message": "正常结束",
    "combinedpay_fee_amt": "0.00",
    "fee_amount": "0.01",
    "huifu_id": "6666000003100616",
    "ord_amt": "0.03",
    "org_hf_seq_id": "0031000topA250804164514P944c0a842bf00000",
    "org_req_date": "20250804",
    "org_req_seq_id": "202508040442356120tt",
    "pay_channel": "A",
    "remark": "test0001",
    "resp_code": "00000000",
    "resp_desc": "查询成功",
    "trade_type": "TRANS_REFUND",
    "trans_date": "20250804",
    "trans_finish_time": "20250804164515",
    "trans_stat": "S",
    "trans_time": "164514"
  }
}
```

## 业务返回码

| 返回码 | 返回描述 |
| --- | --- |
| `00000000` | 查询成功 |
| `10000000` | 入参数据不符合接口要求 |
| `20000001` | 并发冲突，请稍后重试 |
| `21000000` | 原退款全局流水号、原退款请求流水号、外部订单号不能同时为空 |
| `22000000` | 产品号不存在 |
| `22000000` | 产品号状态异常 |
| `23000001` | 原交易不存在 |
| `99999999` | 系统异常，请稍后重试 |

## 实现备注与文档勘误

1. 官方“应用场景”里把银联二维码 JS 写成了 `U_JSAP`，按上下文应理解为 `U_JSAPI`。
2. 官方示例返回里出现了 `combinedpay_fee_amt` 顶层字段，但返回参数表没有该字段；实现时不要把它当成稳定协议字段，优先按参数表中的 `tx_metadata` 和 `split_fee_info` 解析。
3. `org_req_seq_id` 在这个接口里是退款请求流水号，不是原支付流水号；这是最容易接错的字段语义。
4. `trans_stat=I` 属于罕见初始态，若查询到该状态，按官方建议联系汇付技术支持处理。
