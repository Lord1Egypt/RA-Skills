# handle_prescription_check

| 项 | 值 |
|----|-----|
| 脚本 | `scripts/handle_prescription_check.py` |
| Method / path | POST `api/v2/order/handle_prescription_check` |
| 官方文档 | [handle_prescription_check](https://open.shopee.com/documents/v2/v2.order.handle_prescription_check?module=94&type=1) |
| 用途 | operation: APPROVE | REJECT; ID/PH whitelist |

经 **`POST /shopee/developerProxy`** 转发；依赖 **`linkfox-shopee-store-auth`** 选店（通常传 `shopId` 或 `merchantId`）。

---

## 脚本 JSON 入参

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `shopId` | string | 与 `merchantId` 二选一 | 店铺 ID（推荐；Public 等无店铺接口可省略） |
| `merchantId` | string | 与 `shopId` 二选一 | 商户 ID |
| `package_number` | — | 是 | 见 notes / 官方文档 |
| `order_sn` | — | 否（POST body） | 见 notes / 官方文档 |
| `operation` | — | 是 | 见 notes / 官方文档 |
| `reject_reason` | — | 否（POST body） | 见 notes / 官方文档 |
| `is_approved` | — | 否（POST body） | 见 notes / 官方文档 |
| `reject_reason_code` | — | 否（POST body） | 见 notes / 官方文档 |
| `items` | — | 否（POST body） | 见 notes / 官方文档 |
| `pharmacist_name` | — | 否（POST body） | 见 notes / 官方文档 |
| `free_text` | — | 否（POST body） | 见 notes / 官方文档 |

- Method：**POST**
- POST：传 `body` / `requestBody`，或把 `body_fields` 列在 JSON 顶层
- `shopId` / `merchantId` / `skipDepCheck` 等为网关选店保留字段，不会进 Shopee query/body
- Registry notes：operation: APPROVE | REJECT; ID/PH whitelist

---

## 调用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/handle_prescription_check.py '{"shopId": "67890", "package_number": "<package_number>", "operation": "<operation>"}'

# 通用入口
python scripts/order_api.py '{"api": "handle_prescription_check", "shopId": "67890", "package_number": "<package_number>", "operation": "<operation>"}'
```

---

## 响应要点

1. 先看 **`developerProxy.httpStatus`** / `errcode`
2. 再读 **`handlePrescriptionCheck`**（Shopee `response` 解析结果）
3. 字段以官方文档为准

---

## 补充说明（自原 references/api.md）

[官方文档](https://open.shopee.com/documents/v2/v2.order.handle_prescription_check?module=94&type=1)

**Body（必填）**：`package_number`、`operation`（`APPROVE`|`REJECT`）

**Body（可选）**：`order_sn`、`reject_reason`、`is_approved`、`reject_reason_code`、`items`、`pharmacist_name`、`free_text`

**区域**：ID、PH 白名单卖家

---
