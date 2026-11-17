# search_package_list

| 项 | 值 |
|----|-----|
| 脚本 | `scripts/search_package_list.py` |
| Method / path | POST `api/v2/order/search_package_list` |
| 官方文档 | [search_package_list](https://open.shopee.com/documents/v2/v2.order.search_package_list?module=94&type=1) |
| 用途 | Pass body object or top-level filter/pagination/sort |

经 **`POST /shopee/developerProxy`** 转发；依赖 **`linkfox-shopee-store-auth`** 选店（通常传 `shopId` 或 `merchantId`）。

---

## 脚本 JSON 入参

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `shopId` | string | 与 `merchantId` 二选一 | 店铺 ID（推荐；Public 等无店铺接口可省略） |
| `merchantId` | string | 与 `shopId` 二选一 | 商户 ID |
| `filter` | object | 否（可嵌在 body） | 嵌套对象；或整体传 `body` / `requestBody` |
| `pagination` | object | 否（可嵌在 body） | 嵌套对象；或整体传 `body` / `requestBody` |
| `sort` | object | 否（可嵌在 body） | 嵌套对象；或整体传 `body` / `requestBody` |

- Method：**POST**
- POST：传 `body` / `requestBody`，或把 `body_fields` 列在 JSON 顶层
- `shopId` / `merchantId` / `skipDepCheck` 等为网关选店保留字段，不会进 Shopee query/body
- Registry notes：Pass body object or top-level filter/pagination/sort

---

## 调用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/search_package_list.py '{"shopId": "67890"}'

# 通用入口
python scripts/order_api.py '{"api": "search_package_list", "shopId": "67890"}'
```

---

## 响应要点

1. 先看 **`developerProxy.httpStatus`** / `errcode`
2. 再读 **`searchPackageList`**（Shopee `response` 解析结果）
3. 字段以官方文档为准

---

## 补充说明（自原 references/api.md）

[官方文档](https://open.shopee.com/documents/v2/v2.order.search_package_list?module=94&type=1)

**Body（必填）**：`pagination.page_size`（1–100）

**Body（可选）**：
- `filter`：`package_status`、`product_location_ids`、`logistics_channel_ids`、`fulfillment_type`、`invoice_pending`、`sorting_group`（TW）、`order_type`、`is_pre_order`、`shipping_priority`
- `pagination.cursor`
- `sort`：`sort_type`（1=ShipByDate/2=CreateDate/3=ConfirmedDate）、`ascending`

**示例**：
```json
{
  "shopId": "67890",
  "filter": {"package_status": 2, "fulfillment_type": 2},
  "pagination": {"page_size": 20, "cursor": ""},
  "sort": {"sort_type": 1, "ascending": false}
}
```

---
