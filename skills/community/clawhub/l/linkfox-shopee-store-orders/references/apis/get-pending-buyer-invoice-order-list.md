# get_pending_buyer_invoice_order_list

| 项 | 值 |
|----|-----|
| 脚本 | `scripts/get_pending_buyer_invoice_order_list.py` |
| Method / path | GET `api/v2/order/get_pending_buyer_invoice_order_list` |
| 官方文档 | [get_pending_buyer_invoice_order_list](https://open.shopee.com/documents/v2/v2.order.get_pending_buyer_invoice_order_list?module=94&type=1) |
| 用途 | PH/BR local sellers |

经 **`POST /shopee/developerProxy`** 转发；依赖 **`linkfox-shopee-store-auth`** 选店（通常传 `shopId` 或 `merchantId`）。

---

## 脚本 JSON 入参

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `shopId` | string | 与 `merchantId` 二选一 | 店铺 ID（推荐；Public 等无店铺接口可省略） |
| `merchantId` | string | 与 `shopId` 二选一 | 商户 ID |
| `page_size` | — | **是** | Query 必填（见 notes / 官方文档） |

- Method：**GET**
- GET：业务字段放 JSON **顶层**，runner 拼进 `queryString`（不含 `?`）
- `shopId` / `merchantId` / `skipDepCheck` 等为网关选店保留字段，不会进 Shopee query/body
- Registry notes：PH/BR local sellers

---

## 调用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/get_pending_buyer_invoice_order_list.py '{"shopId": "67890", "page_size": 20}'

# 通用入口
python scripts/order_api.py '{"api": "get_pending_buyer_invoice_order_list", "shopId": "67890", "page_size": 20}'
```

---

## 响应要点

1. 先看 **`developerProxy.httpStatus`** / `errcode`
2. 再读 **`getPendingBuyerInvoiceOrderList`**（Shopee `response` 解析结果）
3. 字段以官方文档为准

---

## 补充说明（自原 references/api.md）

[官方文档](https://open.shopee.com/documents/v2/v2.order.get_pending_buyer_invoice_order_list?module=94&type=1)

**Query（必填）**：`page_size`（1–100）

**Query（可选）**：`cursor`

**区域**：PH、BR 本地卖家

---
