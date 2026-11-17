# get_order_list

| 项 | 值 |
|----|-----|
| 脚本 | `scripts/get_order_list.py` |
| Method / path | GET `api/v2/order/get_order_list` |
| 官方文档 | [get_order_list](https://open.shopee.com/documents/v2/v2.order.get_order_list?module=94&type=1) |
| 用途 | time_from/time_to max 15 days; order_status optional filter |

经 **`POST /shopee/developerProxy`** 转发；依赖 **`linkfox-shopee-store-auth`** 选店（通常传 `shopId` 或 `merchantId`）。

---

## 脚本 JSON 入参

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `shopId` | string | 与 `merchantId` 二选一 | 店铺 ID（推荐；Public 等无店铺接口可省略） |
| `merchantId` | string | 与 `shopId` 二选一 | 商户 ID |
| `time_range_field` | — | **是** | Query 必填（见 notes / 官方文档） |
| `page_size` | — | **是** | Query 必填（见 notes / 官方文档） |
| `time_to` | — | **是** | Query 必填（见 notes / 官方文档） |
| `time_from` | — | **是** | Query 必填（见 notes / 官方文档） |

- Method：**GET**
- GET：业务字段放 JSON **顶层**，runner 拼进 `queryString`（不含 `?`）
- `shopId` / `merchantId` / `skipDepCheck` 等为网关选店保留字段，不会进 Shopee query/body
- Registry notes：time_from/time_to max 15 days; order_status optional filter

---

## 调用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/get_order_list.py '{"shopId": "67890", "time_range_field": "<time_range_field>", "time_from": "<time_from>", "time_to": "<time_to>", "page_size": 20}'

# 通用入口
python scripts/order_api.py '{"api": "get_order_list", "shopId": "67890", "time_range_field": "<time_range_field>", "time_from": "<time_from>", "time_to": "<time_to>", "page_size": 20}'
```

---

## 响应要点

1. 先看 **`developerProxy.httpStatus`** / `errcode`
2. 再读 **`getOrderList`**（Shopee `response` 解析结果）
3. 字段以官方文档为准

---

## 补充说明（自原 references/api.md）

[官方文档](https://open.shopee.com/documents/v2/v2.order.get_order_list?module=94&type=1)

**Query（必填）**：`time_range_field`（`create_time`|`update_time`）、`time_from`、`time_to`（Unix 秒，跨度 ≤15 天）、`page_size`（1–100）

**Query（可选）**：`cursor`、`order_status`（`UNPAID`/`READY_TO_SHIP`/`PROCESSED`/`SHIPPED`/`COMPLETED`/`IN_CANCEL`/`CANCELLED`/`INVOICE_PENDING`）、`response_optional_fields`、`request_order_status_pending`、`logistics_channel_id`（仅 BR）

**Response**：`more`、`next_cursor`、`order_list[]`（含 `order_sn`）

---
