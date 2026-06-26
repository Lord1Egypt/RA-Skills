# 卖家发起取消申请 — `temu.order.cancel.appeal.apply`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/us_seller_cancel_order_cancel_appeal_apply.py` |
| **Partner 文档** | https://partner-us.temu.com/documentation（`menu_code` / `sub_menu_code` 以 Partner 后台该接口页为准） |
| **网关** | `POST /temu/proxy`，`type`=`temu.order.cancel.appeal.apply`，业务载荷放在 Body 的 `params` |

**Description:** Support merchants to initiate cancellation requests through the interface（支持商家通过接口发起取消申请）。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 `request`。建议使用 **`tokenPurpose=order-shipping`**。  
> `reason.proofUrlList` 中的图片须先经 **`temu.order.query.signature`** 转为 URL 后再传入（该接口待接入时可先用 `temu_us_proxy.py` 试调）。

---

## Request 结构（官方业务参数）

```text
params
└── request (OBJECT, 选填)
    ├── cancelType (INTEGER, 是)
    ├── applyOrder (OBJECT, 是)
    │   └── parentOrderSn (STRING, 是)
    └── reason (OBJECT, 是)
        ├── description (STRING, 是)
        └── proofUrlList[] (STRING[], 是)
```

### `request`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| cancelType | INTEGER | **是** | The types of application for cancellation（取消申请类型），见下表 |
| applyOrder | OBJECT | **是** | Details of the application to cancel the order（取消订单申请详情） |
| reason | OBJECT | **是** | Explanation of Application Reasons（申请原因说明） |

#### `cancelType`

| 值 | 说明 |
|----|------|
| `2` | Suspected batch refund（疑似批量退款） |
| `3` | Incorrect address（地址错误） |

### `applyOrder`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| parentOrderSn | STRING | **是** | Parent order sn（父订单号） |

### `reason`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| description | STRING | **是** | Explanation of the reason for cancellation initiated（发起取消的原因说明） |
| proofUrlList | STRING[] | **是** | Related screenshots serve as supplementary evidence to illustrate the rationality of the application（相关截图作为补充证据，说明申请的合理性）；图片须先通过 **`temu.order.query.signature`** 转为 URL 后传入 |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "cancelType": 3,
    "applyOrder": {
      "parentOrderSn": "PO-123456789"
    },
    "reason": {
      "description": "Customer provided incorrect shipping address",
      "proofUrlList": [
        "https://signed-url-from-temu.order.query.signature/..."
      ]
    }
  }
}
```

---

## Response（Temu `body` 解析后）

```text
response
├── success
├── errorCode
├── errorMsg
└── result
    └── applySn
```

### `response` 顶层字段

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result | OBJECT | result |

### `result`

| 参数 | 类型 | 说明 |
|------|------|------|
| applySn | STRING | apply sn（取消申请单号） |

---

## 示例

```bash
python scripts/us_seller_cancel_order_cancel_appeal_apply.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "cancelType": 3,
    "applyOrder": {
      "parentOrderSn": "PO-123456789"
    },
    "reason": {
      "description": "Incorrect address confirmed with buyer",
      "proofUrlList": ["https://signed-url/..."]
    }
  }
}'
```

典型流程：`temu.order.cancel.appeal.apply` 提交申请取得 `applySn` → [temu-order-cancel-appeal-result-get.md](./temu-order-cancel-appeal-result-get.md) 查询 `status`。
