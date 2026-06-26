# Python 场景示例

本文件覆盖托管支付 Python 的 H5 / PC 预下单、小程序预下单、查询、关单、退款、退款查询、对账。

## 目录

- 公共前提
- H5 / PC 预下单
- 微信小程序预下单
- 支付宝小程序预下单
- 托管交易查询
- 托管交易关单
- 托管交易退款
- 托管退款查询
- 对账单查询
- 生产写法约束

## 公共前提

- 已按 `references/hostingpay-python-adapter.md` 安装并验证 `dg-sdk==2.0.22`
- 已调用 `init_huifu_sdk()`
- 每个 request 对象的 `huifu_id` 必须等于本次真实请求商户号，SDK 会据此生成 `jpt-x-skill-huifu_id`
- 原交易字段必须来自业务订单表或上游响应
- 外部 DTO / Controller 已接收 `req_date`、`req_seq_id`、`huifu_id`、金额、项目号、回调地址等字段时，必须保留入参，缺失或非法时显式报错；不要用下面 demo 的 `datetime.now()` 或 `new_req_seq_id()` 覆盖上游值

下面示例复用工具函数：

```python
import json
import os
from datetime import datetime
from uuid import uuid4

import dg_sdk


def new_req_seq_id(prefix: str) -> str:
    return f"{prefix}{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid4().hex[:8]}"


def compact_json(payload: dict) -> str:
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
```

## H5 / PC 预下单

### SDK 类

`V2TradeHostingPaymentPreorderH5Request().post({})`

### 最小示例

```python
def create_h5_preorder() -> dict:
    huifu_id = os.environ["HUIFU_MERCHANT_ID"]
    init_huifu_sdk()

    request = dg_sdk.V2TradeHostingPaymentPreorderH5Request()
    request.req_date = datetime.now().strftime("%Y%m%d")
    request.req_seq_id = new_req_seq_id("HP")
    request.huifu_id = huifu_id
    request.trans_amt = "88.00"
    request.goods_desc = "会员充值"
    request.pre_order_type = "1"
    request.hosting_data = compact_json(
        {
            "project_id": os.environ["HUIFU_PROJECT_ID"],
            "project_title": os.environ["HUIFU_PROJECT_TITLE"],
            "callback_url": os.environ["HUIFU_CALLBACK_URL"],
        }
    )

    return request.post({"notify_url": os.environ["HUIFU_NOTIFY_URL"]})
```

### 注意事项

- `pre_order_type=1` 对应 H5 / PC。
- `callback_url` 只是前端回跳地址，不等于支付成功。
- `jump_url`、`req_seq_id`、`req_date` 必须落库。

## 微信小程序预下单

### SDK 类

`V2TradeHostingPaymentPreorderWxRequest().post({})`

### 最小示例

```python
def create_wx_preorder(seq_id: str) -> dict:
    huifu_id = os.environ["HUIFU_MERCHANT_ID"]
    init_huifu_sdk()

    request = dg_sdk.V2TradeHostingPaymentPreorderWxRequest()
    request.req_date = datetime.now().strftime("%Y%m%d")
    request.req_seq_id = new_req_seq_id("WX")
    request.huifu_id = huifu_id
    request.trans_amt = "12.50"
    request.goods_desc = "微信小程序订单"
    request.pre_order_type = "3"
    request.miniapp_data = compact_json(
        {
            "seq_id": seq_id,
            "private_info": "oppsHosting://",
            "need_scheme": "Y",
        }
    )

    return request.post({"notify_url": os.environ["HUIFU_NOTIFY_URL"]})
```

### 注意事项

- `seq_id` 必须来自真实小程序链路。
- `sub_openid`、分账和实名限制字段只能在业务已具备真实值时补。

## 支付宝小程序预下单

### SDK 类

`V2TradeHostingPaymentPreorderAliRequest().post({})`

### 最小示例

```python
def create_alipay_preorder() -> dict:
    huifu_id = os.environ["HUIFU_MERCHANT_ID"]
    init_huifu_sdk()

    request = dg_sdk.V2TradeHostingPaymentPreorderAliRequest()
    request.req_date = datetime.now().strftime("%Y%m%d")
    request.req_seq_id = new_req_seq_id("AP")
    request.huifu_id = huifu_id
    request.trans_amt = "18.80"
    request.goods_desc = "支付宝小程序订单"
    request.pre_order_type = "2"
    request.app_data = compact_json(
        {
            "app_schema": os.environ["HUIFU_ALIPAY_APP_SCHEMA"],
        }
    )

    return request.post({"notify_url": os.environ["HUIFU_NOTIFY_URL"]})
```

### 注意事项

- `app_schema` 必须来自支付宝小程序真实配置。
- `buyer_id` 不能猜，只能来自支付宝用户授权结果。

## 托管交易查询

### SDK 类

`V2TradeHostingPaymentQueryorderinfoRequest().post({})`

### 最小示例

```python
def query_hosting_payment(org_req_date: str, org_req_seq_id: str) -> dict:
    huifu_id = os.environ["HUIFU_MERCHANT_ID"]
    init_huifu_sdk()

    request = dg_sdk.V2TradeHostingPaymentQueryorderinfoRequest()
    request.req_date = datetime.now().strftime("%Y%m%d")
    request.req_seq_id = new_req_seq_id("HQ")
    request.huifu_id = huifu_id
    request.org_req_date = org_req_date
    request.org_req_seq_id = org_req_seq_id

    return request.post({})
```

### 注意事项

- 查询支持 `huifu_id + org_req_date + org_req_seq_id` 或 `party_order_id` 两种定位方式。
- 不要把两组字段都填满后声称“通用”。按用户现有落库字段选择一种。

## 托管交易关单

### SDK 类

`V2TradeHostingPaymentCloseRequest().post({})`

### 最小示例

```python
def close_hosting_payment(org_req_date: str, org_req_seq_id: str) -> dict:
    huifu_id = os.environ["HUIFU_MERCHANT_ID"]
    init_huifu_sdk()

    request = dg_sdk.V2TradeHostingPaymentCloseRequest()
    request.req_date = datetime.now().strftime("%Y%m%d")
    request.req_seq_id = new_req_seq_id("HC")
    request.huifu_id = huifu_id
    request.org_req_date = org_req_date
    request.org_req_seq_id = org_req_seq_id

    return request.post({})
```

### 注意事项

- 关单只处理适合关闭的未支付交易。
- 原请求日期和原请求流水必须来自预下单落库。

## 托管交易退款

### SDK 类

`V2TradeHostingPaymentHtrefundRequest().post({})`

### 最小示例

```python
def refund_hosting_payment(org_req_date: str, org_req_seq_id: str, amount: str) -> dict:
    huifu_id = os.environ["HUIFU_MERCHANT_ID"]
    init_huifu_sdk()

    request = dg_sdk.V2TradeHostingPaymentHtrefundRequest()
    request.req_date = datetime.now().strftime("%Y%m%d")
    request.req_seq_id = new_req_seq_id("HR")
    request.huifu_id = huifu_id
    request.ord_amt = amount
    request.org_req_date = org_req_date
    request.org_req_seq_id = org_req_seq_id
    request.risk_check_data = os.environ["HUIFU_RISK_CHECK_DATA_JSON"]
    request.terminal_device_data = os.environ["HUIFU_TERMINAL_DEVICE_DATA_JSON"]

    return request.post({"notify_url": os.environ["HUIFU_NOTIFY_URL"]})
```

### 注意事项

- `risk_check_data`、`terminal_device_data` 是否必填取决于线上退款场景，不能用空对象上线；示例要求它们由业务风控 / 设备模块提前生成 JSON 字符串。
- 原交易字段和退款金额必须来自业务订单与退款单；托管退款必须在 `org_hf_seq_id`、`org_party_order_id`、`org_req_seq_id` 三个原交易定位键中至少提供一个，示例选择 `org_req_seq_id`。

## 托管退款查询

### SDK 类

`V2TradeHostingPaymentQueryrefundinfoRequest().post({})`

### 最小示例

```python
def query_hosting_refund(org_req_date: str, org_req_seq_id: str) -> dict:
    huifu_id = os.environ["HUIFU_MERCHANT_ID"]
    init_huifu_sdk()

    request = dg_sdk.V2TradeHostingPaymentQueryrefundinfoRequest()
    request.req_date = datetime.now().strftime("%Y%m%d")
    request.req_seq_id = new_req_seq_id("RQ")
    request.huifu_id = huifu_id
    request.org_req_date = org_req_date
    request.org_req_seq_id = org_req_seq_id

    return request.post({})
```

### 注意事项

- 查询退款应按退款单落库字段定位。
- 异步通知延迟时，用退款查询补偿确认。

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
    request.req_seq_id = new_req_seq_id("HF")
    request.huifu_id = huifu_id
    request.file_date = file_date

    return request.post({})
```

### 注意事项

- `file_date` 是文件生成日期。
- 对账不走托管预下单 request，也不走 `dg_sdk.Payment`。

## 生产写法约束

1. 所有 Python 示例必须体现官方 `dg-sdk` / `dg_sdk`。
2. 所有 JSON Object 字段必须传 JSON 字符串，不要传 Python dict。
3. 每个 request 对象必须设置本次真实 `huifu_id`，不要按旧版写 `jpt_x_skill_huifu_id` 初始化参数。
4. 前端 callback 不等于最终支付成功，最终状态仍回到服务端查单补偿和异步通知闭环。
5. 不要把 `jpt-x-skill-source` 或 `jpt-x-skill-huifu_id` 放进业务 `data`。
6. 示例中的 `new_req_seq_id()` 只适用于服务端自主管理请求流水号的场景；生成真实 Controller / Service 代码时，若外部 DTO / Controller 已接收字段，必须保留入参，缺失或非法时显式报错。
