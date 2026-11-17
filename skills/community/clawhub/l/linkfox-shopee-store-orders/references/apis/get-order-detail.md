# get_order_detail

| 项 | 值 |
|----|-----|
| 脚本 | `scripts/get_order_detail.py` |
| Method / path | GET `api/v2/order/get_order_detail` |
| 官方文档 | [get_order_detail](https://open.shopee.com/documents/v2/v2.order.get_order_detail?module=94&type=1) |
| 用途 | order_sn_list: string or array, max 50, comma-joined |

经 **`POST /shopee/developerProxy`** 转发；依赖 **`linkfox-shopee-store-auth`** 选店（通常传 `shopId` 或 `merchantId`）。

---

## 脚本 JSON 入参

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `shopId` | string | 与 `merchantId` 二选一 | 店铺 ID（推荐；Public 等无店铺接口可省略） |
| `merchantId` | string | 与 `shopId` 二选一 | 商户 ID |
| `order_sn_list` | — | **是** | Query 必填（见 notes / 官方文档） |

- Method：**GET**
- GET：业务字段放 JSON **顶层**，runner 拼进 `queryString`（不含 `?`）
- `shopId` / `merchantId` / `skipDepCheck` 等为网关选店保留字段，不会进 Shopee query/body
- Registry notes：order_sn_list: string or array, max 50, comma-joined

---

## 调用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/get_order_detail.py '{"shopId": "67890", "order_sn_list": "<order_sn_list>"}'

# 通用入口
python scripts/order_api.py '{"api": "get_order_detail", "shopId": "67890", "order_sn_list": "<order_sn_list>"}'
```

---

## 响应要点

1. 先看 **`developerProxy.httpStatus`** / `errcode`
2. 再读 **`getOrderDetail`**（Shopee `response` 解析结果）
3. 字段以官方文档为准

---

## 补充说明（自原 references/api.md）

[官方文档](https://open.shopee.com/documents/v2/v2.order.get_order_detail?module=94&type=1)

**Query（必填）**：`order_sn_list`（逗号分隔或数组，1–50 个）

**Query（可选）**：`response_optional_fields`、`request_order_status_pending`

**Response**：`order_list[]`（`order_sn`、`order_status`、`total_amount`、`item_list`、`recipient_address` 等）

---
