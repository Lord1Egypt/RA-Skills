# get_shop_notification

| 项 | 值 |
|----|-----|
| 脚本 | `scripts/get_shop_notification.py` |
| Method / path | GET `api/v2/shop/get_shop_notification` |
| 官方文档 | [get_shop_notification](https://open.shopee.com/documents/v2/v2.shop.get_shop_notification?module=92&type=1) |
| 用途 | Optional cursor, page_size (default 10, max 50) |

经 **`POST /shopee/developerProxy`** 转发；依赖 **`linkfox-shopee-store-auth`** 选店（通常传 `shopId` 或 `merchantId`）。

---

## 脚本 JSON 入参

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `shopId` | string | 与 `merchantId` 二选一 | 店铺 ID（推荐；Public 等无店铺接口可省略） |
| `merchantId` | string | 与 `shopId` 二选一 | 商户 ID |

- Method：**GET**
- GET：业务字段放 JSON **顶层**，runner 拼进 `queryString`（不含 `?`）
- `shopId` / `merchantId` / `skipDepCheck` 等为网关选店保留字段，不会进 Shopee query/body
- Registry notes：Optional cursor, page_size (default 10, max 50)

---

## 调用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/get_shop_notification.py '{"shopId": "67890"}'

# 通用入口
python scripts/shop_api.py '{"api": "get_shop_notification", "shopId": "67890"}'
```

---

## 响应要点

1. 先看 **`developerProxy.httpStatus`** / `errcode`
2. 再读 **`getShopNotification`**（Shopee `response` 解析结果）
3. 字段以官方文档为准

---

## 补充说明（自原 references/api.md）

[官方文档](https://open.shopee.com/documents/v2/v2.shop.get_shop_notification?module=92&type=1)

**Query（可选）**：`cursor`（上一页 notification_id）、`page_size`（默认 10，最大 50）

**Response 要点**：`cursor`、`data.title`、`data.content`、`data.create_time`、`data.url`

---
