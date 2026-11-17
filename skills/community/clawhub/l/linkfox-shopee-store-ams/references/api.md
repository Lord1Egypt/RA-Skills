# linkfox-shopee-store-ams — 参数与字段参考

> 单接口入参/响应说明已拆到 **`apis/`**（按 API 一份）；本文件保留模块总览与 Feedback。
Shopee **AMS（Affiliate Marketing Solutions）模块**全部 36 个 API，经 **`POST /shopee/developerProxy`** 转发。

授权见 **`linkfox-shopee-store-auth`**。官方索引：[v2.ams.get_open_campaign_added_product](https://open.shopee.com/documents/v2/v2.ams.get_open_campaign_added_product?module=127&type=1)

## 通用约定

- **Base URL**：`https://tool-gateway.linkfox.com`
- **Method**：POST（网关），上游 Method 见各接口
- **Auth**：Header `Authorization: <api_key>`（`LINKFOXAGENT_API_KEY`）
- **流程**：`POST /shopee/storeTokens` → `POST /shopee/developerProxy`
- **path**：须 `api/v2/ams/...`
- **标识**：店铺级 API，通常传 **`shopId`**
- **与 Ads 区别**：AMS 为联盟营销/达人带货；Ads（module=117）为站内 CPC 广告
- **官方文档 URL 规则**：`https://open.shopee.com/documents/v2/v2.ams.{api}?module=127&type=1`

---

## AMS 模块总览

| # | API | Method | path | 脚本 | 官方文档 |
|---|-----|--------|------|------|----------|
| 1 | add_all_products_to_open_campaign | POST | `api/v2/ams/add_all_products_to_open_campaign` | `add_all_products_to_open_campaign.py` | [apis/add-all-products-to-open-campaign.md](./apis/add-all-products-to-open-campaign.md) |
| 2 | batch_add_products_to_open_campaign | POST | `api/v2/ams/batch_add_products_to_open_campaign` | `batch_add_products_to_open_campaign.py` | [apis/batch-add-products-to-open-campaign.md](./apis/batch-add-products-to-open-campaign.md) |
| 3 | batch_edit_products_open_campaign_setting | POST | `api/v2/ams/batch_edit_products_open_campaign_setting` | `batch_edit_products_open_campaign_setting.py` | [apis/batch-edit-products-open-campaign-setting.md](./apis/batch-edit-products-open-campaign-setting.md) |
| 4 | batch_get_products_suggested_rate | POST | `api/v2/ams/batch_get_products_suggested_rate` | `batch_get_products_suggested_rate.py` | [apis/batch-get-products-suggested-rate.md](./apis/batch-get-products-suggested-rate.md) |
| 5 | batch_remove_products_open_campaign_setting | POST | `api/v2/ams/batch_remove_products_open_campaign_setting` | `batch_remove_products_open_campaign_setting.py` | [apis/batch-remove-products-open-campaign-setting.md](./apis/batch-remove-products-open-campaign-setting.md) |
| 6 | create_new_targeted_campaign | POST | `api/v2/ams/create_new_targeted_campaign` | `create_new_targeted_campaign.py` | [apis/create-new-targeted-campaign.md](./apis/create-new-targeted-campaign.md) |
| 7 | edit_affiliate_list_of_targeted_campaign | POST | `api/v2/ams/edit_affiliate_list_of_targeted_campaign` | `edit_affiliate_list_of_targeted_campaign.py` | [apis/edit-affiliate-list-of-targeted-campaign.md](./apis/edit-affiliate-list-of-targeted-campaign.md) |
| 8 | edit_all_products_open_campaign_setting | POST | `api/v2/ams/edit_all_products_open_campaign_setting` | `edit_all_products_open_campaign_setting.py` | [apis/edit-all-products-open-campaign-setting.md](./apis/edit-all-products-open-campaign-setting.md) |
| 9 | edit_product_list_of_targeted_campaign | POST | `api/v2/ams/edit_product_list_of_targeted_campaign` | `edit_product_list_of_targeted_campaign.py` | [apis/edit-product-list-of-targeted-campaign.md](./apis/edit-product-list-of-targeted-campaign.md) |
| 10 | get_affiliate_performance | GET | `api/v2/ams/get_affiliate_performance` | `get_affiliate_performance.py` | [apis/get-affiliate-performance.md](./apis/get-affiliate-performance.md) |
| 11 | get_auto_add_new_product_toggle_status | GET | `api/v2/ams/get_auto_add_new_product_toggle_status` | `get_auto_add_new_product_toggle_status.py` | [apis/get-auto-add-new-product-toggle-status.md](./apis/get-auto-add-new-product-toggle-status.md) |
| 12 | get_campaign_key_metrics_performance | GET | `api/v2/ams/get_campaign_key_metrics_performance` | `get_campaign_key_metrics_performance.py` | [apis/get-campaign-key-metrics-performance.md](./apis/get-campaign-key-metrics-performance.md) |
| 13 | get_content_performance | GET | `api/v2/ams/get_content_performance` | `get_content_performance.py` | [apis/get-content-performance.md](./apis/get-content-performance.md) |
| 14 | get_conversion_report | GET | `api/v2/ams/get_conversion_report` | `get_conversion_report.py` | [apis/get-conversion-report.md](./apis/get-conversion-report.md) |
| 15 | get_managed_affiliate_list | GET | `api/v2/ams/get_managed_affiliate_list` | `get_managed_affiliate_list.py` | [apis/get-managed-affiliate-list.md](./apis/get-managed-affiliate-list.md) |
| 16 | get_open_campaign_added_product | GET | `api/v2/ams/get_open_campaign_added_product` | `get_open_campaign_added_product.py` | [apis/get-open-campaign-added-product.md](./apis/get-open-campaign-added-product.md) |
| 17 | get_open_campaign_batch_task_result | GET | `api/v2/ams/get_open_campaign_batch_task_result` | `get_open_campaign_batch_task_result.py` | [apis/get-open-campaign-batch-task-result.md](./apis/get-open-campaign-batch-task-result.md) |
| 18 | get_open_campaign_not_added_product | GET | `api/v2/ams/get_open_campaign_not_added_product` | `get_open_campaign_not_added_product.py` | [apis/get-open-campaign-not-added-product.md](./apis/get-open-campaign-not-added-product.md) |
| 19 | get_open_campaign_performance | GET | `api/v2/ams/get_open_campaign_performance` | `get_open_campaign_performance.py` | [apis/get-open-campaign-performance.md](./apis/get-open-campaign-performance.md) |
| 20 | get_optimization_suggestion_product | GET | `api/v2/ams/get_optimization_suggestion_product` | `get_optimization_suggestion_product.py` | [apis/get-optimization-suggestion-product.md](./apis/get-optimization-suggestion-product.md) |
| 21 | get_performance_data_update_time | GET | `api/v2/ams/get_performance_data_update_time` | `get_performance_data_update_time.py` | [apis/get-performance-data-update-time.md](./apis/get-performance-data-update-time.md) |
| 22 | get_product_performance | GET | `api/v2/ams/get_product_performance` | `get_product_performance.py` | [apis/get-product-performance.md](./apis/get-product-performance.md) |
| 23 | get_recommended_affiliate_list | GET | `api/v2/ams/get_recommended_affiliate_list` | `get_recommended_affiliate_list.py` | [apis/get-recommended-affiliate-list.md](./apis/get-recommended-affiliate-list.md) |
| 24 | get_shop_performance | GET | `api/v2/ams/get_shop_performance` | `get_shop_performance.py` | [apis/get-shop-performance.md](./apis/get-shop-performance.md) |
| 25 | get_shop_suggested_rate | GET | `api/v2/ams/get_shop_suggested_rate` | `get_shop_suggested_rate.py` | [apis/get-shop-suggested-rate.md](./apis/get-shop-suggested-rate.md) |
| 26 | get_targeted_campaign_addable_product_list | GET | `api/v2/ams/get_targeted_campaign_addable_product_list` | `get_targeted_campaign_addable_product_list.py` | [apis/get-targeted-campaign-addable-product-list.md](./apis/get-targeted-campaign-addable-product-list.md) |
| 27 | get_targeted_campaign_list | GET | `api/v2/ams/get_targeted_campaign_list` | `get_targeted_campaign_list.py` | [apis/get-targeted-campaign-list.md](./apis/get-targeted-campaign-list.md) |
| 28 | get_targeted_campaign_performance | GET | `api/v2/ams/get_targeted_campaign_performance` | `get_targeted_campaign_performance.py` | [apis/get-targeted-campaign-performance.md](./apis/get-targeted-campaign-performance.md) |
| 29 | get_targeted_campaign_settings | GET | `api/v2/ams/get_targeted_campaign_settings` | `get_targeted_campaign_settings.py` | [apis/get-targeted-campaign-settings.md](./apis/get-targeted-campaign-settings.md) |
| 30 | get_validation_list | GET | `api/v2/ams/get_validation_list` | `get_validation_list.py` | [apis/get-validation-list.md](./apis/get-validation-list.md) |
| 31 | get_validation_report | GET | `api/v2/ams/get_validation_report` | `get_validation_report.py` | [apis/get-validation-report.md](./apis/get-validation-report.md) |
| 32 | query_affiliate_list | GET | `api/v2/ams/query_affiliate_list` | `query_affiliate_list.py` | [apis/query-affiliate-list.md](./apis/query-affiliate-list.md) |
| 33 | remove_all_products_open_campaign_setting | POST | `api/v2/ams/remove_all_products_open_campaign_setting` | `remove_all_products_open_campaign_setting.py` | [apis/remove-all-products-open-campaign-setting.md](./apis/remove-all-products-open-campaign-setting.md) |
| 34 | terminate_targeted_campaign | POST | `api/v2/ams/terminate_targeted_campaign` | `terminate_targeted_campaign.py` | [apis/terminate-targeted-campaign.md](./apis/terminate-targeted-campaign.md) |
| 35 | update_auto_add_new_product_setting | POST | `api/v2/ams/update_auto_add_new_product_setting` | `update_auto_add_new_product_setting.py` | [apis/update-auto-add-new-product-setting.md](./apis/update-auto-add-new-product-setting.md) |
| 36 | update_basic_info_of_targeted_campaign | POST | `api/v2/ams/update_basic_info_of_targeted_campaign` | `update_basic_info_of_targeted_campaign.py` | [apis/update-basic-info-of-targeted-campaign.md](./apis/update-basic-info-of-targeted-campaign.md) |
通用入口：`ams_api.py`（JSON 含 `"api": "<上表 API 名>"`）。

---

## 常用接口说明

### Open Campaign（开放推广）

| API | 要点 |
|-----|------|
| `get_open_campaign_added_product` | 已加入 Open Campaign 的商品 — [apis/get-open-campaign-added-product.md](./apis/get-open-campaign-added-product.md) |
| `get_open_campaign_not_added_product` | 未加入的商品 — [apis/get-open-campaign-not-added-product.md](./apis/get-open-campaign-not-added-product.md) |
| `batch_add_products_to_open_campaign` | 批量添加商品 — [apis/batch-add-products-to-open-campaign.md](./apis/batch-add-products-to-open-campaign.md) |
| `batch_edit_products_open_campaign_setting` | 批量编辑佣金等设置 — [apis/batch-edit-products-open-campaign-setting.md](./apis/batch-edit-products-open-campaign-setting.md) |
| `get_open_campaign_performance` | Open Campaign 效果数据 — [apis/get-open-campaign-performance.md](./apis/get-open-campaign-performance.md) |

### Targeted Campaign（定向推广）

| API | 要点 |
|-----|------|
| `create_new_targeted_campaign` | 创建定向达人 campaign — [apis/create-new-targeted-campaign.md](./apis/create-new-targeted-campaign.md) |
| `get_targeted_campaign_list` | campaign 列表 — [apis/get-targeted-campaign-list.md](./apis/get-targeted-campaign-list.md) |
| `edit_product_list_of_targeted_campaign` | 编辑 campaign 商品 — [apis/edit-product-list-of-targeted-campaign.md](./apis/edit-product-list-of-targeted-campaign.md) |
| `edit_affiliate_list_of_targeted_campaign` | 编辑 campaign 达人 — [apis/edit-affiliate-list-of-targeted-campaign.md](./apis/edit-affiliate-list-of-targeted-campaign.md) |
| `get_targeted_campaign_performance` | 定向 campaign 效果 — [apis/get-targeted-campaign-performance.md](./apis/get-targeted-campaign-performance.md) |

### 达人/Affiliate

| API | 要点 |
|-----|------|
| `get_recommended_affiliate_list` | 推荐达人 — [apis/get-recommended-affiliate-list.md](./apis/get-recommended-affiliate-list.md) |
| `get_managed_affiliate_list` | 已管理达人 — [apis/get-managed-affiliate-list.md](./apis/get-managed-affiliate-list.md) |
| `query_affiliate_list` | 查询达人列表 — [apis/query-affiliate-list.md](./apis/query-affiliate-list.md) |
| `get_affiliate_performance` | 达人效果 — [apis/get-affiliate-performance.md](./apis/get-affiliate-performance.md) |

### 效果报表

| API | 要点 |
|-----|------|
| `get_shop_performance` | 店铺 AMS 效果 — [apis/get-shop-performance.md](./apis/get-shop-performance.md) |
| `get_product_performance` | 商品效果 — [apis/get-product-performance.md](./apis/get-product-performance.md) |
| `get_conversion_report` | 转化报告 — [apis/get-conversion-report.md](./apis/get-conversion-report.md) |
| `get_campaign_key_metrics_performance` | 关键指标 — [apis/get-campaign-key-metrics-performance.md](./apis/get-campaign-key-metrics-performance.md) |

---

## 网关错误码

| errcode | 含义 | 建议 |
|---------|------|------|
| 1002 | 参数/未登录 | 检查 shopId 与 API Key |
| 1003 | 代理/网络异常 | 重试 |
| 1004 | 无授权记录 | auth skill |
| 1005 | path 未白名单 | 确认 `api/v2/ams/...` |

---

## curl 示例

```bash
export KEY=$LINKFOXAGENT_API_KEY
BASE=https://tool-gateway.linkfox.com

curl -X POST $BASE/shopee/developerProxy -H "Authorization: $KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "path": "api/v2/ams/get_open_campaign_added_product",
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
  -d '{"skillName":"linkfox-shopee-store-ams","sentiment":"POSITIVE",
       "category":"OTHER","content":"AMS推广商品查询正常"}'
```
