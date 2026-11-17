# linkfox-shopee-store-shop-flash-sale — 参数与字段参考

> 单接口入参/响应说明已拆到 **`apis/`**（按 API 一份）；本文件保留模块总览与 Feedback。
Shopee **Shop Flash Sale 模块**全部 11 个 API，经 **`POST /shopee/developerProxy`** 转发。

授权见 **`linkfox-shopee-store-auth`**。官方索引：[v2.shop_flash_sale.get_time_slot_id](https://open.shopee.com/documents/v2/v2.shop_flash_sale.get_time_slot_id?module=123&type=1)

## 通用约定

- **path**：须 `api/v2/shop_flash_sale/...`
- **标识**：通常传 **`shopId`**
- **官方文档 URL 规则**：`https://open.shopee.com/documents/v2/v2.shop_flash_sale.{api}?module=123&type=1`

---

## Shop Flash Sale 模块总览

| # | API | Method | path | 脚本 | 官方文档 |
|---|-----|--------|------|------|----------|
| 1 | add_shop_flash_sale_items | POST | `api/v2/shop_flash_sale/add_shop_flash_sale_items` | `add_shop_flash_sale_items.py` | [apis/add-shop-flash-sale-items.md](./apis/add-shop-flash-sale-items.md) |
| 2 | create_shop_flash_sale | POST | `api/v2/shop_flash_sale/create_shop_flash_sale` | `create_shop_flash_sale.py` | [apis/create-shop-flash-sale.md](./apis/create-shop-flash-sale.md) |
| 3 | delete_shop_flash_sale | POST | `api/v2/shop_flash_sale/delete_shop_flash_sale` | `delete_shop_flash_sale.py` | [apis/delete-shop-flash-sale.md](./apis/delete-shop-flash-sale.md) |
| 4 | delete_shop_flash_sale_items | POST | `api/v2/shop_flash_sale/delete_shop_flash_sale_items` | `delete_shop_flash_sale_items.py` | [apis/delete-shop-flash-sale-items.md](./apis/delete-shop-flash-sale-items.md) |
| 5 | get_item_criteria | GET | `api/v2/shop_flash_sale/get_item_criteria` | `get_item_criteria.py` | [apis/get-item-criteria.md](./apis/get-item-criteria.md) |
| 6 | get_shop_flash_sale | GET | `api/v2/shop_flash_sale/get_shop_flash_sale` | `get_shop_flash_sale.py` | [apis/get-shop-flash-sale.md](./apis/get-shop-flash-sale.md) |
| 7 | get_shop_flash_sale_items | GET | `api/v2/shop_flash_sale/get_shop_flash_sale_items` | `get_shop_flash_sale_items.py` | [apis/get-shop-flash-sale-items.md](./apis/get-shop-flash-sale-items.md) |
| 8 | get_shop_flash_sale_list | GET | `api/v2/shop_flash_sale/get_shop_flash_sale_list` | `get_shop_flash_sale_list.py` | [apis/get-shop-flash-sale-list.md](./apis/get-shop-flash-sale-list.md) |
| 9 | get_time_slot_id | GET | `api/v2/shop_flash_sale/get_time_slot_id` | `get_time_slot_id.py` | [apis/get-time-slot-id.md](./apis/get-time-slot-id.md) |
| 10 | update_shop_flash_sale | POST | `api/v2/shop_flash_sale/update_shop_flash_sale` | `update_shop_flash_sale.py` | [apis/update-shop-flash-sale.md](./apis/update-shop-flash-sale.md) |
| 11 | update_shop_flash_sale_items | POST | `api/v2/shop_flash_sale/update_shop_flash_sale_items` | `update_shop_flash_sale_items.py` | [apis/update-shop-flash-sale-items.md](./apis/update-shop-flash-sale-items.md) |
通用入口：`shop_flash_sale_api.py`（JSON 含 `"api": "<上表 API 名>"`）。

---

## 常用接口说明

| API | 要点 |
|-----|------|
| `get_time_slot_id` | 获取可用秒杀时段 ID — [apis/get-time-slot-id.md](./apis/get-time-slot-id.md) |
| `create_shop_flash_sale` | 创建店铺秒杀活动；POST `body` — [apis/create-shop-flash-sale.md](./apis/create-shop-flash-sale.md) |
| `get_item_criteria` | 查询商品参与条件 — [apis/get-item-criteria.md](./apis/get-item-criteria.md) |
| `add_shop_flash_sale_items` | 添加秒杀商品 — [apis/add-shop-flash-sale-items.md](./apis/add-shop-flash-sale-items.md) |
| `get_shop_flash_sale_list` | 活动列表 — [apis/get-shop-flash-sale-list.md](./apis/get-shop-flash-sale-list.md) |
| `get_shop_flash_sale` | 活动详情 — [apis/get-shop-flash-sale.md](./apis/get-shop-flash-sale.md) |
| `get_shop_flash_sale_items` | 活动内商品 — [apis/get-shop-flash-sale-items.md](./apis/get-shop-flash-sale-items.md) |
| `update_shop_flash_sale` / `update_shop_flash_sale_items` | 更新活动或商品 |
| `delete_shop_flash_sale` / `delete_shop_flash_sale_items` | 删除活动或商品 |

---

## curl 示例

```bash
curl -X POST ${LINKFOX_TOOL_GATEWAY}/shopee/developerProxy \
  -H "Authorization: ${LINKFOX_AGENT_API_KEY:-$LINKFOXAGENT_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "path": "api/v2/shop_flash_sale/get_time_slot_id",
    "method": "GET",
    "accessToken": "xxx",
    "shopId": "67890"
  }'
```

---

## Feedback API

```bash
curl -X POST https://skill-api.linkfox.com/api/v1/public/feedback \
  -H "Content-Type: application/json" \
  -d '{"skillName":"linkfox-shopee-store-shop-flash-sale","sentiment":"POSITIVE",
       "category":"OTHER","content":"店铺秒杀查询正常"}'
```
