# Python 场景示例

本文件覆盖聚合支付 Python 的下单、扫码交易查询、关单、关单查询、退款、退款查询、对账。

## 目录

- 公共前提
- 聚合支付下单
- 扫码交易查询
- 扫码交易关单
- 扫码交易关单查询
- 扫码交易退款
- 扫码交易退款查询
- 对账单查询
- 生产写法约束

## 公共前提

- 已按 `references/aggregation-python-adapter.md` 安装并验证 `dg-sdk==2.0.22`
- 已调用 `init_huifu_sdk()`
- 每个 request 对象的 `huifu_id` 必须等于本次真实请求商户号，SDK 会据此生成 `jpt-x-skill-huifu_id`
- 原交易字段必须来自业务订单表或上游响应
- 外部 DTO / Controller 已接收 `req_date`、`req_seq_id`、`huifu_id`、金额、通知地址等字段时，必须保留入参，缺失或非法时显式报错；不要用下面 demo 的 `datetime.now()` 或 `new_req_seq_id()` 覆盖上游值

下面示例复用工具函数：

```python
import json
import os
from datetime import datetime
from uuid import uuid4

import dg_sdk


def new_req_seq_id(prefix: str) -> str:
    return f"{prefix}{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid4().hex[:8]}"
```

## 聚合支付下单

### SDK 类

`PaymentCreateRequest` + `dg_sdk.Payment.create()`

### 最小示例

```python
def create_payment() -> dict:
    huifu_id = os.environ["HUIFU_MERCHANT_ID"]
    init_huifu_sdk()

    request = dg_sdk.PaymentCreateRequest()
    request.req_seq_id = new_req_seq_id("AP")
    request.huifu_id = huifu_id
    request.trade_type = "A_JSAPI"
    request.trans_amt = "0.10"
    request.goods_desc = "测试订单"
    request.notify_url = os.environ["HUIFU_NOTIFY_URL"]
    request.method_expand = json.dumps(
        {
            "buyer_id": os.environ["HUIFU_ALIPAY_BUYER_ID"],
        },
        ensure_ascii=False,
        separators=(",", ":"),
    )

    return dg_sdk.Payment.create(request)
```

### 注意事项

- 该骨架只演示 `A_JSAPI` 的 SDK 边界写法。
- `T_JSAPI`、`T_MINIAPP`、`T_APP`、`T_MICROPAY`、`A_JSAPI`、`A_NATIVE`、`A_MICROPAY`、`U_JSAPI`、`U_NATIVE`、`U_MICROPAY` 这些值不是 `method_expand` 的 key；`method_expand` 的 JSON 内容直接是当前场景对象本身。
- `tx_metadata` 本身不作为请求字段上送；交易能力扩展按能力名直接传 `acct_split_bunch`、`terminal_device_data`、`combinedpay_data`、`combinedpay_data_fee_info`、`trans_fee_allowance_info`。
- 其他 `trade_type` 的 `method_expand` 必须按 `aggregation-payload-construction.md` 与对应渠道 reference 建模后再序列化，不要复用空对象。
- `req_seq_id` 必须落库，后续查单、关单、退款会复用。

## 扫码交易查询

### SDK 类

`PaymentQueryRequest` + `dg_sdk.Payment.query()`

### 最小示例

```python
def query_payment(hf_seq_id: str) -> dict:
    huifu_id = os.environ["HUIFU_MERCHANT_ID"]
    init_huifu_sdk()

    request = dg_sdk.PaymentQueryRequest()
    request.huifu_id = huifu_id
    request.hf_seq_id = hf_seq_id
    request.req_date = datetime.now().strftime("%Y%m%d")

    return dg_sdk.Payment.query(request)
```

### 注意事项

- `hf_seq_id`、`out_ord_id`、`req_seq_id` 三选一，示例按 `hf_seq_id` 查询。
- 前端回调后仍需要服务端闭环确认：异步通知验签/幂等，并通过查单二次确认或补偿查询兜底。

## 扫码交易关单

### SDK 类

`PaymentCloseRequest` + `dg_sdk.Payment.close()`

### 最小示例

```python
def close_payment(org_req_date: str, org_req_seq_id: str) -> dict:
    huifu_id = os.environ["HUIFU_MERCHANT_ID"]
    init_huifu_sdk()

    request = dg_sdk.PaymentCloseRequest()
    request.req_date = datetime.now().strftime("%Y%m%d")
    request.req_seq_id = new_req_seq_id("AC")
    request.huifu_id = huifu_id
    request.org_req_date = org_req_date
    request.org_req_seq_id = org_req_seq_id

    return dg_sdk.Payment.close(request)
```

### 注意事项

- 关单适用于未支付订单释放，不适合已成功订单。
- `org_req_date` 和 `org_req_seq_id` 必须来自原下单落库。

## 扫码交易关单查询

### SDK 类

`PaymentCloseQueryRequest` + `dg_sdk.Payment.close_query()`

### 最小示例

```python
def query_close(org_req_date: str, org_req_seq_id: str) -> dict:
    huifu_id = os.environ["HUIFU_MERCHANT_ID"]
    init_huifu_sdk()

    request = dg_sdk.PaymentCloseQueryRequest()
    request.req_date = datetime.now().strftime("%Y%m%d")
    request.req_seq_id = new_req_seq_id("AQ")
    request.huifu_id = huifu_id
    request.org_req_date = org_req_date
    request.org_req_seq_id = org_req_seq_id

    return dg_sdk.Payment.close_query(request)
```

### 注意事项

- 关单请求返回处理中时，用关单查询确认最终状态。
- 不要把本次查询流水当作原交易流水。

## 扫码交易退款

### SDK 类

`PaymentRefundRequest` + `dg_sdk.Payment.refund()`

### 最小示例

```python
def refund_payment(org_req_date: str, org_req_seq_id: str, amount: str) -> dict:
    huifu_id = os.environ["HUIFU_MERCHANT_ID"]
    init_huifu_sdk()

    request = dg_sdk.PaymentRefundRequest()
    request.req_date = datetime.now().strftime("%Y%m%d")
    request.req_seq_id = new_req_seq_id("AR")
    request.huifu_id = huifu_id
    request.ord_amt = amount
    request.org_req_date = org_req_date
    request.org_req_seq_id = org_req_seq_id
    request.notify_url = os.environ["HUIFU_NOTIFY_URL"]

    return dg_sdk.Payment.refund(request)
```

### 注意事项

- `org_hf_seq_id` / `org_party_order_id` / `org_req_seq_id` 三选一，示例按 `org_req_seq_id` 定位。
- 字段必须来自原交易落库。
- 退款最终状态仍以退款查询和异步通知闭环为准。

## 扫码交易退款查询

### SDK 类

`PaymentRefundQueryRequest` + `dg_sdk.Payment.refund_query()`

### 最小示例

```python
def query_refund(org_req_date: str, org_req_seq_id: str) -> dict:
    huifu_id = os.environ["HUIFU_MERCHANT_ID"]
    init_huifu_sdk()

    request = dg_sdk.PaymentRefundQueryRequest()
    request.huifu_id = huifu_id
    request.org_req_date = org_req_date
    request.org_req_seq_id = org_req_seq_id

    return dg_sdk.Payment.refund_query(request)
```

### 注意事项

- 示例按退款请求流水定位。
- 如果异步通知延迟，可用退款查询补偿确认。

## 对账单查询

### SDK 类

`V2TradeCheckFilequeryRequest().post({})`

### 最小示例

```python
def query_check_file(file_date: str) -> dict:
    huifu_id = os.environ["HUIFU_MERCHANT_ID"]
    init_huifu_sdk()

    request = dg_sdk.V2TradeCheckFilequeryRequest()
    request.req_date = datetime.now().strftime("%Y%m%d")
    request.req_seq_id = new_req_seq_id("AF")
    request.huifu_id = huifu_id
    request.file_date = file_date

    return request.post({})
```

### 注意事项

- `file_date` 是文件生成日期，不一定等于交易日期。
- 对账使用 request 类 `.post({})`，不要走 `dg_sdk.Payment`。

## 生产写法约束

1. Python 示例必须体现官方 `dg-sdk` / `dg_sdk`。
2. 每个 request 对象必须设置本次真实 `huifu_id`，不要按旧版写 `jpt_x_skill_huifu_id` 初始化参数。
3. JSON Object 字段统一在 SDK 边界使用 `json.dumps(..., ensure_ascii=False, separators=(",", ":"))` 转成字符串。
4. 原交易定位键必须来自持久化数据，不要临时猜测。
5. 不要把 `jpt-x-skill-source` 或 `jpt-x-skill-huifu_id` 放进业务 `data`。
6. 示例中的 `new_req_seq_id()` 只适用于服务端自主管理请求流水号的场景；生成真实 Controller / Service 代码时，若外部 DTO / Controller 已接收字段，必须保留入参，缺失或非法时显式报错。
