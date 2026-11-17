# linkfox-shopee-store-global-product — 参数与字段参考

> 单接口入参/响应说明已拆到 **`apis/`**（按 API 一份）；本文件保留模块总览与 Feedback。
Shopee **GlobalProduct 模块**全部 34 个 API，经 **`POST /shopee/developerProxy`** 转发。

授权见 **`linkfox-shopee-store-auth`**。官方索引：[v2.global_product.get_category](https://open.shopee.com/documents/v2/v2.global_product.get_category?module=90&type=1)

## 通用约定

- **Base URL**：`https://tool-gateway.linkfox.com`
- **Method**：POST（网关），上游 Method 见各接口
- **Auth**：Header `Authorization: <api_key>`（`LINKFOXAGENT_API_KEY`）（如未配置 按 SKILL.md 的 **## 解决认证和算力问题** 处理）
- **流程**：`POST /shopee/storeTokens` → `POST /shopee/developerProxy`
- **path**：须 `api/v2/global_product/...`
- **标识**：跨境 GlobalProduct 接口通常用 **`merchantId`**（商户级）；部分发布/映射接口需 **`shopId`**
- **官方文档 URL 规则**：`https://open.shopee.com/documents/v2/v2.global_product.{api}?module=90&type=1`
- **复杂 POST**（如 `add_global_item`、`create_publish_task`）：推荐传完整 `body` 对象

---

## GlobalProduct 模块总览

| # | API | Method | path | 脚本 | 官方文档 |
|---|-----|--------|------|------|----------|
| 1 | add_global_item | POST | `api/v2/global_product/add_global_item` | `add_global_item.py` | [apis/add-global-item.md](./apis/add-global-item.md) |
| 2 | add_global_model | POST | `api/v2/global_product/add_global_model` | `add_global_model.py` | [apis/add-global-model.md](./apis/add-global-model.md) |
| 3 | category_recommend | POST | `api/v2/global_product/category_recommend` | `category_recommend.py` | [apis/category-recommend.md](./apis/category-recommend.md) |
| 4 | create_publish_task | POST | `api/v2/global_product/create_publish_task` | `create_publish_task.py` | [apis/create-publish-task.md](./apis/create-publish-task.md) |
| 5 | delete_global_item | POST | `api/v2/global_product/delete_global_item` | `delete_global_item.py` | [apis/delete-global-item.md](./apis/delete-global-item.md) |
| 6 | delete_global_model | POST | `api/v2/global_product/delete_global_model` | `delete_global_model.py` | [apis/delete-global-model.md](./apis/delete-global-model.md) |
| 7 | get_attribute_tree | GET | `api/v2/global_product/get_attribute_tree` | `get_attribute_tree.py` | [apis/get-attribute-tree.md](./apis/get-attribute-tree.md) |
| 8 | get_brand_list | GET | `api/v2/global_product/get_brand_list` | `get_brand_list.py` | [apis/get-brand-list.md](./apis/get-brand-list.md) |
| 9 | get_category | GET | `api/v2/global_product/get_category` | `get_category.py` | [apis/get-category.md](./apis/get-category.md) |
| 10 | get_global_item_id | GET | `api/v2/global_product/get_global_item_id` | `get_global_item_id.py` | [apis/get-global-item-id.md](./apis/get-global-item-id.md) |
| 11 | get_global_item_info | GET | `api/v2/global_product/get_global_item_info` | `get_global_item_info.py` | [apis/get-global-item-info.md](./apis/get-global-item-info.md) |
| 12 | get_global_item_limit | GET | `api/v2/global_product/get_global_item_limit` | `get_global_item_limit.py` | [apis/get-global-item-limit.md](./apis/get-global-item-limit.md) |
| 13 | get_global_item_list | GET | `api/v2/global_product/get_global_item_list` | `get_global_item_list.py` | [apis/get-global-item-list.md](./apis/get-global-item-list.md) |
| 14 | get_global_model_list | GET | `api/v2/global_product/get_global_model_list` | `get_global_model_list.py` | [apis/get-global-model-list.md](./apis/get-global-model-list.md) |
| 15 | get_local_adjustment_rate | GET | `api/v2/global_product/get_local_adjustment_rate` | `get_local_adjustment_rate.py` | [apis/get-local-adjustment-rate.md](./apis/get-local-adjustment-rate.md) |
| 16 | get_publish_task_result | GET | `api/v2/global_product/get_publish_task_result` | `get_publish_task_result.py` | [apis/get-publish-task-result.md](./apis/get-publish-task-result.md) |
| 17 | get_publishable_shop | GET | `api/v2/global_product/get_publishable_shop` | `get_publishable_shop.py` | [apis/get-publishable-shop.md](./apis/get-publishable-shop.md) |
| 18 | get_published_list | GET | `api/v2/global_product/get_published_list` | `get_published_list.py` | [apis/get-published-list.md](./apis/get-published-list.md) |
| 19 | get_recommend_attribute | POST | `api/v2/global_product/get_recommend_attribute` | `get_recommend_attribute.py` | [apis/get-recommend-attribute.md](./apis/get-recommend-attribute.md) |
| 20 | get_shop_publishable_status | GET | `api/v2/global_product/get_shop_publishable_status` | `get_shop_publishable_status.py` | [apis/get-shop-publishable-status.md](./apis/get-shop-publishable-status.md) |
| 21 | get_size_chart_detail | GET | `api/v2/global_product/get_size_chart_detail` | `get_size_chart_detail.py` | [apis/get-size-chart-detail.md](./apis/get-size-chart-detail.md) |
| 22 | get_size_chart_list | GET | `api/v2/global_product/get_size_chart_list` | `get_size_chart_list.py` | [apis/get-size-chart-list.md](./apis/get-size-chart-list.md) |
| 23 | get_variations | GET | `api/v2/global_product/get_variations` | `get_variations.py` | [apis/get-variations.md](./apis/get-variations.md) |
| 24 | init_tier_variation | POST | `api/v2/global_product/init_tier_variation` | `init_tier_variation.py` | [apis/init-tier-variation.md](./apis/init-tier-variation.md) |
| 25 | search_global_attribute_value_list | POST | `api/v2/global_product/search_global_attribute_value_list` | `search_global_attribute_value_list.py` | [apis/search-global-attribute-value-list.md](./apis/search-global-attribute-value-list.md) |
| 26 | set_sync_field | POST | `api/v2/global_product/set_sync_field` | `set_sync_field.py` | [apis/set-sync-field.md](./apis/set-sync-field.md) |
| 27 | support_size_chart | POST | `api/v2/global_product/support_size_chart` | `support_size_chart.py` | [apis/support-size-chart.md](./apis/support-size-chart.md) |
| 28 | update_global_item | POST | `api/v2/global_product/update_global_item` | `update_global_item.py` | [apis/update-global-item.md](./apis/update-global-item.md) |
| 29 | update_global_model | POST | `api/v2/global_product/update_global_model` | `update_global_model.py` | [apis/update-global-model.md](./apis/update-global-model.md) |
| 30 | update_local_adjustment_rate | POST | `api/v2/global_product/update_local_adjustment_rate` | `update_local_adjustment_rate.py` | [apis/update-local-adjustment-rate.md](./apis/update-local-adjustment-rate.md) |
| 31 | update_price | POST | `api/v2/global_product/update_price` | `update_price.py` | [apis/update-price.md](./apis/update-price.md) |
| 32 | update_size_chart | POST | `api/v2/global_product/update_size_chart` | `update_size_chart.py` | [apis/update-size-chart.md](./apis/update-size-chart.md) |
| 33 | update_stock | POST | `api/v2/global_product/update_stock` | `update_stock.py` | [apis/update-stock.md](./apis/update-stock.md) |
| 34 | update_tier_variation | POST | `api/v2/global_product/update_tier_variation` | `update_tier_variation.py` | [apis/update-tier-variation.md](./apis/update-tier-variation.md) |
通用入口：`global_product_api.py`（JSON 含 `"api": "<上表 API 名>"`）。

---

## 常用接口说明

### 类目与属性

| API | 要点 |
|-----|------|
| `get_category` | 全球商品类目树；可选 `language` — [apis/get-category.md](./apis/get-category.md) |
| `get_attribute_tree` | 必填 `category_id` — [apis/get-attribute-tree.md](./apis/get-attribute-tree.md) |
| `get_brand_list` | 必填 `offset`、`page_size`、`category_id` — [apis/get-brand-list.md](./apis/get-brand-list.md) |
| `category_recommend` | POST：推荐类目 — [apis/category-recommend.md](./apis/category-recommend.md) |
| `get_recommend_attribute` | POST：推荐属性 — [apis/get-recommend-attribute.md](./apis/get-recommend-attribute.md) |

### 全球商品 CRUD

| API | 要点 |
|-----|------|
| `get_global_item_list` | 必填 `offset`、`page_size` — [apis/get-global-item-list.md](./apis/get-global-item-list.md) |
| `get_global_item_info` | 必填 `global_item_id_list`（最多 50） — [apis/get-global-item-info.md](./apis/get-global-item-info.md) |
| `add_global_item` / `update_global_item` | POST `body`：完整全球商品结构 |
| `delete_global_item` | 必填 `global_item_id` — [apis/delete-global-item.md](./apis/delete-global-item.md) |

### SKU / 价格 / 库存

| API | 要点 |
|-----|------|
| `get_global_model_list` | 必填 `global_item_id` — [apis/get-global-model-list.md](./apis/get-global-model-list.md) |
| `init_tier_variation` / `update_tier_variation` | 全球 SKU 规格 |
| `add_global_model` / `update_global_model` / `delete_global_model` | 全球 SKU 管理 |
| `update_price` / `update_stock` | POST body 含 global_item_id 与 price/stock 列表 |

### 发布到站点

| API | 要点 |
|-----|------|
| `create_publish_task` | 将全球商品发布到各站点店铺 — [apis/create-publish-task.md](./apis/create-publish-task.md) |
| `get_publishable_shop` | 可发布的目标店铺 — [apis/get-publishable-shop.md](./apis/get-publishable-shop.md) |
| `get_publish_task_result` | 发布任务结果 — [apis/get-publish-task-result.md](./apis/get-publish-task-result.md) |
| `get_published_list` | 已发布列表 — [apis/get-published-list.md](./apis/get-published-list.md) |
| `set_sync_field` | 设置同步字段 — [apis/set-sync-field.md](./apis/set-sync-field.md) |
| `get_global_item_id` | shop item_id 映射到 global_item_id — [apis/get-global-item-id.md](./apis/get-global-item-id.md) |
| `get_shop_publishable_status` | 店铺发布资格 — [apis/get-shop-publishable-status.md](./apis/get-shop-publishable-status.md) |

### 其他

尺码表（`support_size_chart`、`update_size_chart`、`get_size_chart_*`）、本地调价（`get_local_adjustment_rate`、`update_local_adjustment_rate`）、`search_global_attribute_value_list` 等 — 见上表及官方文档。

---

## 网关错误码

| errcode | 含义 | 建议 |
|---------|------|------|
| 1002 | 参数/未登录 | 检查 merchantId/shopId 与 API Key |
| 1003 | 代理/网络异常 | 重试 |
| 1004 | 无授权记录 | auth skill |
| 1005 | path 未白名单 | 确认 `api/v2/global_product/...` |

---

## curl 示例

```bash
export KEY=$LINKFOX_AGENT_API_KEY
BASE=${LINKFOX_TOOL_GATEWAY}

# 全球类目
curl -X POST $BASE/shopee/developerProxy -H "Authorization: $KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "path": "api/v2/global_product/get_category",
    "method": "GET",
    "accessToken": "xxx",
    "merchantId": "12345",
    "queryString": "language=zh-hans"
  }'

# 全球商品列表
curl -X POST $BASE/shopee/developerProxy -H "Authorization: $KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "path": "api/v2/global_product/get_global_item_list",
    "method": "GET",
    "accessToken": "xxx",
    "merchantId": "12345",
    "queryString": "offset=0&page_size=20"
  }'
```

---

## Feedback API

```bash
curl -X POST https://skill-api.linkfox.com/api/v1/public/feedback \
  -H "Content-Type: application/json" \
  -d '{"skillName":"linkfox-shopee-store-global-product","sentiment":"POSITIVE",
       "category":"OTHER","content":"全球商品查询正常"}'
```
