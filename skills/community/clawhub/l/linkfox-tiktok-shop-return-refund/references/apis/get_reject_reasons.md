# Get Reject Reasons

> 官方文档：https://partner.tiktokshop.com/docv2/page/get-reject-reasons-202309

## LinkFox 转发映射（本 skill）

| 项 | 值 |
|----|----|
| 具名 api | `get_reject_reasons` |
| 脚本 | `scripts/get_reject_reasons.py` |
| 网关 | `POST /tiktokShop/developerProxy` |
| appType | **`erp`（固定）** |
| 上游 path | `return_refund/202309/reject_reasons` |
| method | `GET` |
| shop_cipher | 是 |
| 令牌 | 网关按 `openId` + `appType=erp` 从库取 token（401/过期自动刷新并重试一次） |

### developerProxy 示例

```json
{
  "appType": "erp",
  "openId": "7010...",
  "path": "return_refund/202309/reject_reasons",
  "method": "GET",
  "queryString": "shop_cipher=GCP_...&return_or_cancel_id=4035633471902223141"
}
```

### 脚本示例

```bash
python scripts/return_refund_api.py '{"api":"get_reject_reasons","openId":"...","return_or_cancel_id":"4035..."}'
```

---

## 官方接口原文（整理）

# Path: /return_refund/202309/reject_reasons
# Method: [GET]
# Function Description
Retrieve the list of valid reject reasons for a return or cancellation request. Call this before rejecting a return/cancellation so the seller can pick an allowed reason.

# Common Parameters
| Properties | Location | Type | Require | Sample | Properties description |
| --- | --- | --- | --- | --- | --- |
| shop_cipher | query | string | Y | GCP_... | Shop cipher from Get Authorized Shops |
| content-type | header | string | Y | application/json | Allowed type: application/json |

# Request Query Parameters
| Properties | Type | Require | Sample | Properties description |
| --- | --- | --- | --- | --- |
| return_or_cancel_id | string | Y | 4035633471902223141 | Unique ID of the return or cancellation request |
| locale | string | N | en-US | Locale for localized reason text |

> `app_key` / `sign` / `timestamp` 由紫鸟注入，调用方不要传。

# Request Sample
```Plain Text
https://open-api.tiktokglobalshop.com/return_refund/202309/reject_reasons?shop_cipher=ROW_...&return_or_cancel_id=4035633471902223141&app_key=...&timestamp=...&sign=...
```

# Response Parameters
| Properties | Type | Sample | Properties description |
| --- | --- | --- | --- |
| code | int | 0 | Status code |
| message | string | Success | Message |
| request_id | string | ... | Request id |
| data | object |  | Payload |
| ^reject_reasons | []object |  | Available reject reasons |
| ^^name / reason_code | string | PRODUCT_DAMAGED | Reason key/code |
| ^^text / reason_description | string | Product is damaged | Localized description |

# Response Sample
```json
{
  "code": 0,
  "data": {
    "reject_reasons": [
      {
        "name": "PRODUCT_DAMAGED",
        "text": "Product is damaged"
      },
      {
        "name": "INSUFFICIENT_EVIDENCE",
        "text": "Evidence provided is insufficient"
      }
    ]
  },
  "message": "Success",
  "request_id": "202407021210000112233445566AABB"
}
```

## Agent 注意事项

1. 必须先有 `return_or_cancel_id`（来自售后列表/详情；后续可扩 search returns）。
2. 展示时列出 `name`/`text`（或 `reason_code`/`reason_description`，以线上响应为准）。
3. 真正拒绝退货/取消走 Reject Return / Reject Cancellation（可后续纳入本 skill）。
