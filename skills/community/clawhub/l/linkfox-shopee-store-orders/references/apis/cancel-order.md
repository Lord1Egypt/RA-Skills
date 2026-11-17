# cancel_order

| 项 | 值 |
|----|-----|
| 脚本 | `scripts/cancel_order.py` |
| Method / path | POST `api/v2/order/cancel_order` |
| 官方文档 | [cancel_order](https://open.shopee.com/documents/v2/v2.order.cancel_order?module=94&type=1) |
| 用途 | cancel_reason: OUT_OF_STOCK/CUSTOMER_REQUEST/UNDELIVERABLE_AREA/COD_NOT_SUPPORTED |

经 **`POST /shopee/developerProxy`** 转发；依赖 **`linkfox-shopee-store-auth`** 选店（通常传 `shopId` 或 `merchantId`）。

---

## 脚本 JSON 入参

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `shopId` | string | 与 `merchantId` 二选一 | 店铺 ID（推荐；Public 等无店铺接口可省略） |
| `merchantId` | string | 与 `shopId` 二选一 | 商户 ID |
| `order_sn` | — | 是 | 见 notes / 官方文档 |
| `cancel_reason` | — | 是 | 见 notes / 官方文档 |
| `item_list` | — | 否（POST body） | 见 notes / 官方文档 |
| `partial_cancel_item_list` | — | 否（POST body） | 见 notes / 官方文档 |

- Method：**POST**
- POST：传 `body` / `requestBody`，或把 `body_fields` 列在 JSON 顶层
- `shopId` / `merchantId` / `skipDepCheck` 等为网关选店保留字段，不会进 Shopee query/body
- Registry notes：cancel_reason: OUT_OF_STOCK/CUSTOMER_REQUEST/UNDELIVERABLE_AREA/COD_NOT_SUPPORTED

---

## 调用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/cancel_order.py '{"shopId": "67890", "order_sn": "<order_sn>", "cancel_reason": "<cancel_reason>"}'

# 通用入口
python scripts/order_api.py '{"api": "cancel_order", "shopId": "67890", "order_sn": "<order_sn>", "cancel_reason": "<cancel_reason>"}'
```

---

## 响应要点

1. 先看 **`developerProxy.httpStatus`** / `errcode`
2. 再读 **`cancelOrder`**（Shopee `response` 解析结果）
3. 字段以官方文档为准

---

## 补充说明（自原 references/api.md）

[官方文档](https://open.shopee.com/documents/v2/v2.order.cancel_order?module=94&type=1)

**Body（必填）**：`order_sn`、`cancel_reason`

**Body（可选）**：`item_list`、`partial_cancel_item_list`（`item_id`、`model_id`、`model_quantity` 等）

**cancel_reason**：`OUT_OF_STOCK`、`CUSTOMER_REQUEST`、`UNDELIVERABLE_AREA`（TW/MY）、`COD_NOT_SUPPORTED`

---
