# linkfox-shopee-store-discount — 参数与字段参考

> 单接口入参/响应说明已拆到 **`apis/`**（按 API 一份）；本文件保留模块总览与 Feedback。
Shopee **Discount 模块**全部 12 个 API，经 **`POST /shopee/developerProxy`** 转发。

授权见 **`linkfox-shopee-store-auth`**。官方索引：[v2.discount.add_discount](https://open.shopee.com/documents/v2/v2.discount.add_discount?module=99&type=1)

## 通用约定

- **path**：须 `api/v2/discount/...`
- **标识**：通常传 **`shopId`**
- **官方文档 URL 规则**：`https://open.shopee.com/documents/v2/v2.discount.{api}?module=99&type=1`

---

## Discount 模块总览

| # | API | Method | path | 脚本 | 官方文档 |
|---|-----|--------|------|------|----------|
| 1 | add_discount | POST | `api/v2/discount/add_discount` | `add_discount.py` | [apis/add-discount.md](./apis/add-discount.md) |
| 2 | add_discount_item | POST | `api/v2/discount/add_discount_item` | `add_discount_item.py` | [apis/add-discount-item.md](./apis/add-discount-item.md) |
| 3 | delete_discount | POST | `api/v2/discount/delete_discount` | `delete_discount.py` | [apis/delete-discount.md](./apis/delete-discount.md) |
| 4 | delete_discount_item | POST | `api/v2/discount/delete_discount_item` | `delete_discount_item.py` | [apis/delete-discount-item.md](./apis/delete-discount-item.md) |
| 5 | delete_sip_discount | POST | `api/v2/discount/delete_sip_discount` | `delete_sip_discount.py` | [apis/delete-sip-discount.md](./apis/delete-sip-discount.md) |
| 6 | end_discount | POST | `api/v2/discount/end_discount` | `end_discount.py` | [apis/end-discount.md](./apis/end-discount.md) |
| 7 | get_discount | GET | `api/v2/discount/get_discount` | `get_discount.py` | [apis/get-discount.md](./apis/get-discount.md) |
| 8 | get_discount_list | GET | `api/v2/discount/get_discount_list` | `get_discount_list.py` | [apis/get-discount-list.md](./apis/get-discount-list.md) |
| 9 | get_sip_discounts | GET | `api/v2/discount/get_sip_discounts` | `get_sip_discounts.py` | [apis/get-sip-discounts.md](./apis/get-sip-discounts.md) |
| 10 | set_sip_discount | POST | `api/v2/discount/set_sip_discount` | `set_sip_discount.py` | [apis/set-sip-discount.md](./apis/set-sip-discount.md) |
| 11 | update_discount | POST | `api/v2/discount/update_discount` | `update_discount.py` | [apis/update-discount.md](./apis/update-discount.md) |
| 12 | update_discount_item | POST | `api/v2/discount/update_discount_item` | `update_discount_item.py` | [apis/update-discount-item.md](./apis/update-discount-item.md) |
通用入口：`discount_api.py`（JSON 含 `"api": "<上表 API 名>"`）。

---

## 常用接口说明

| API | 要点 |
|-----|------|
| `add_discount` | 创建折扣活动；POST `body` — [apis/add-discount.md](./apis/add-discount.md) |
| `add_discount_item` | 向活动添加商品/SKU — [apis/add-discount-item.md](./apis/add-discount-item.md) |
| `get_discount_list` | 折扣活动列表 — [apis/get-discount-list.md](./apis/get-discount-list.md) |
| `get_discount` | 单个活动详情 — [apis/get-discount.md](./apis/get-discount.md) |
| `update_discount` / `update_discount_item` | 更新活动/商品折扣 |
| `end_discount` | 提前结束活动 — [apis/end-discount.md](./apis/end-discount.md) |
| `delete_discount` / `delete_discount_item` | 删除活动/商品 |
| `get_sip_discounts` / `set_sip_discount` / `delete_sip_discount` | SIP 跨境折扣 |

---

## curl 示例

```bash
curl -X POST https://tool-gateway.linkfox.com/shopee/developerProxy \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "path": "api/v2/discount/get_discount_list",
    "method": "GET",
    "accessToken": "xxx",
    "shopId": "67890",
    "queryString": "discount_status=ongoing&page_no=1&page_size=20"
  }'
```

---

## Feedback API

```bash
curl -X POST https://skill-api.linkfox.com/api/v1/public/feedback \
  -H "Content-Type: application/json" \
  -d '{"skillName":"linkfox-shopee-store-discount","sentiment":"POSITIVE",
       "category":"OTHER","content":"折扣活动查询正常"}'
```
