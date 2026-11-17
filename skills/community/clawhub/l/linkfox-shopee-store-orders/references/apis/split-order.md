# split_order

| 项 | 值 |
|----|-----|
| 脚本 | `scripts/split_order.py` |
| Method / path | POST `api/v2/order/split_order` |
| 官方文档 | [split_order](https://open.shopee.com/documents/v2/v2.order.split_order?module=94&type=1) |
| 用途 | Shopee Open API `split_order` |

经 **`POST /shopee/developerProxy`** 转发；依赖 **`linkfox-shopee-store-auth`** 选店（通常传 `shopId` 或 `merchantId`）。

---

## 脚本 JSON 入参

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `shopId` | string | 与 `merchantId` 二选一 | 店铺 ID（推荐；Public 等无店铺接口可省略） |
| `merchantId` | string | 与 `shopId` 二选一 | 商户 ID |
| `order_sn` | — | 是 | 见 notes / 官方文档 |
| `package_list` | — | 是 | 见 notes / 官方文档 |

- Method：**POST**
- POST：传 `body` / `requestBody`，或把 `body_fields` 列在 JSON 顶层
- `shopId` / `merchantId` / `skipDepCheck` 等为网关选店保留字段，不会进 Shopee query/body

---

## 调用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/split_order.py '{"shopId": "67890", "order_sn": "<order_sn>", "package_list": "<package_list>"}'

# 通用入口
python scripts/order_api.py '{"api": "split_order", "shopId": "67890", "order_sn": "<order_sn>", "package_list": "<package_list>"}'
```

---

## 响应要点

1. 先看 **`developerProxy.httpStatus`** / `errcode`
2. 再读 **`splitOrder`**（Shopee `response` 解析结果）
3. 字段以官方文档为准

---

## 补充说明（自原 references/api.md）

[官方文档](https://open.shopee.com/documents/v2/v2.order.split_order?module=94&type=1)

**Body（必填）**：`order_sn`、`package_list[]`（含 `item_list[]`：`item_id`、`model_id`；可选 `order_item_id`、`promotion_group_id`、`model_quantity`）

---
