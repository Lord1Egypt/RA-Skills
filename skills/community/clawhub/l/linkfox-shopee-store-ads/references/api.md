# linkfox-shopee-store-ads — 参数与字段参考

> 单接口入参/响应说明已拆到 **`apis/`**（按 API 一份）；本文件保留模块总览与 Feedback。
Shopee **Ads 模块**全部 23 个 API，经 **`POST /shopee/developerProxy`** 转发。

授权见 **`linkfox-shopee-store-auth`**。官方索引：[v2.ads.get_total_balance](https://open.shopee.com/documents/v2/v2.ads.get_total_balance?module=117&type=1)

> 未纳入：`create_auto_product_ads`、`edit_auto_product_ads`（官方标注 coming offline soon）

## 通用约定

- **Base URL**：`https://tool-gateway.linkfox.com`
- **Method**：POST（网关），上游 Method 见各接口
- **Auth**：Header `Authorization: <api_key>`（`LINKFOXAGENT_API_KEY`）
- **流程**：auth 确认目标店 **`appType=ad`** → 直接 `POST /shopee/developerProxy`（**不要**先取 accessToken）
- **path**：须 `api/v2/ads/...`（服务端自动用 AD partner/token）
- **标识**：店铺级广告 API，通常传 **`shopId`**（或 `merchantId`）
- **禁止**：在 developerProxy 传 `accessToken` 或 `appType`
- **权限**：需 LinkFox 侧 `appType=ad` 授权 + Shopee 侧开通广告能力；ERP 授权不能代替
- **官方文档 URL 规则**：`https://open.shopee.com/documents/v2/v2.ads.{api}?module=117&type=1`
- **复杂 POST**（如 `create_manual_product_ads`）：推荐传完整 `body`；日期格式常为 DD-MM-YYYY

---

## Ads 模块总览

| # | API | Method | path | 脚本 | 官方文档 |
|---|-----|--------|------|------|----------|
| 1 | check_create_gms_product_campaign_eligibility | GET | `api/v2/ads/check_create_gms_product_campaign_eligibility` | `check_create_gms_product_campaign_eligibility.py` | [apis/check-create-gms-product-campaign-eligibility.md](./apis/check-create-gms-product-campaign-eligibility.md) |
| 2 | create_gms_product_campaign | POST | `api/v2/ads/create_gms_product_campaign` | `create_gms_product_campaign.py` | [apis/create-gms-product-campaign.md](./apis/create-gms-product-campaign.md) |
| 3 | create_manual_product_ads | POST | `api/v2/ads/create_manual_product_ads` | `create_manual_product_ads.py` | [apis/create-manual-product-ads.md](./apis/create-manual-product-ads.md) |
| 4 | edit_gms_item_product_campaign | POST | `api/v2/ads/edit_gms_item_product_campaign` | `edit_gms_item_product_campaign.py` | [apis/edit-gms-item-product-campaign.md](./apis/edit-gms-item-product-campaign.md) |
| 5 | edit_gms_product_campaign | POST | `api/v2/ads/edit_gms_product_campaign` | `edit_gms_product_campaign.py` | [apis/edit-gms-product-campaign.md](./apis/edit-gms-product-campaign.md) |
| 6 | edit_manual_product_ad_keywords | POST | `api/v2/ads/edit_manual_product_ad_keywords` | `edit_manual_product_ad_keywords.py` | [apis/edit-manual-product-ad-keywords.md](./apis/edit-manual-product-ad-keywords.md) |
| 7 | edit_manual_product_ads | POST | `api/v2/ads/edit_manual_product_ads` | `edit_manual_product_ads.py` | [apis/edit-manual-product-ads.md](./apis/edit-manual-product-ads.md) |
| 8 | get_ads_facil_shop_rate | GET | `api/v2/ads/get_ads_facil_shop_rate` | `get_ads_facil_shop_rate.py` | [apis/get-ads-facil-shop-rate.md](./apis/get-ads-facil-shop-rate.md) |
| 9 | get_all_cpc_ads_daily_performance | GET | `api/v2/ads/get_all_cpc_ads_daily_performance` | `get_all_cpc_ads_daily_performance.py` | [apis/get-all-cpc-ads-daily-performance.md](./apis/get-all-cpc-ads-daily-performance.md) |
| 10 | get_all_cpc_ads_hourly_performance | GET | `api/v2/ads/get_all_cpc_ads_hourly_performance` | `get_all_cpc_ads_hourly_performance.py` | [apis/get-all-cpc-ads-hourly-performance.md](./apis/get-all-cpc-ads-hourly-performance.md) |
| 11 | get_create_product_ad_budget_suggestion | GET | `api/v2/ads/get_create_product_ad_budget_suggestion` | `get_create_product_ad_budget_suggestion.py` | [apis/get-create-product-ad-budget-suggestion.md](./apis/get-create-product-ad-budget-suggestion.md) |
| 12 | get_gms_campaign_performance | GET | `api/v2/ads/get_gms_campaign_performance` | `get_gms_campaign_performance.py` | [apis/get-gms-campaign-performance.md](./apis/get-gms-campaign-performance.md) |
| 13 | get_gms_item_performance | GET | `api/v2/ads/get_gms_item_performance` | `get_gms_item_performance.py` | [apis/get-gms-item-performance.md](./apis/get-gms-item-performance.md) |
| 14 | get_product_campaign_daily_performance | GET | `api/v2/ads/get_product_campaign_daily_performance` | `get_product_campaign_daily_performance.py` | [apis/get-product-campaign-daily-performance.md](./apis/get-product-campaign-daily-performance.md) |
| 15 | get_product_campaign_hourly_performance | GET | `api/v2/ads/get_product_campaign_hourly_performance` | `get_product_campaign_hourly_performance.py` | [apis/get-product-campaign-hourly-performance.md](./apis/get-product-campaign-hourly-performance.md) |
| 16 | get_product_level_campaign_id_list | GET | `api/v2/ads/get_product_level_campaign_id_list` | `get_product_level_campaign_id_list.py` | [apis/get-product-level-campaign-id-list.md](./apis/get-product-level-campaign-id-list.md) |
| 17 | get_product_level_campaign_setting_info | GET | `api/v2/ads/get_product_level_campaign_setting_info` | `get_product_level_campaign_setting_info.py` | [apis/get-product-level-campaign-setting-info.md](./apis/get-product-level-campaign-setting-info.md) |
| 18 | get_product_recommended_roi_target | GET | `api/v2/ads/get_product_recommended_roi_target` | `get_product_recommended_roi_target.py` | [apis/get-product-recommended-roi-target.md](./apis/get-product-recommended-roi-target.md) |
| 19 | get_recommended_item_list | GET | `api/v2/ads/get_recommended_item_list` | `get_recommended_item_list.py` | [apis/get-recommended-item-list.md](./apis/get-recommended-item-list.md) |
| 20 | get_recommended_keyword_list | GET | `api/v2/ads/get_recommended_keyword_list` | `get_recommended_keyword_list.py` | [apis/get-recommended-keyword-list.md](./apis/get-recommended-keyword-list.md) |
| 21 | get_shop_toggle_info | GET | `api/v2/ads/get_shop_toggle_info` | `get_shop_toggle_info.py` | [apis/get-shop-toggle-info.md](./apis/get-shop-toggle-info.md) |
| 22 | get_total_balance | GET | `api/v2/ads/get_total_balance` | `get_total_balance.py` | [apis/get-total-balance.md](./apis/get-total-balance.md) |
| 23 | list_gms_user_deleted_item | GET | `api/v2/ads/list_gms_user_deleted_item` | `list_gms_user_deleted_item.py` | [apis/list-gms-user-deleted-item.md](./apis/list-gms-user-deleted-item.md) |
通用入口：`ads_api.py`（JSON 含 `"api": "<上表 API 名>"`）。

---

## 常用接口说明

### 账户与推荐

| API | 要点 |
|-----|------|
| `get_total_balance` | 广告账户余额 — [apis/get-total-balance.md](./apis/get-total-balance.md) |
| `get_shop_toggle_info` | 自动充值、Campaign Surge 开关 — [apis/get-shop-toggle-info.md](./apis/get-shop-toggle-info.md) |
| `get_recommended_keyword_list` | 推荐关键词 — [apis/get-recommended-keyword-list.md](./apis/get-recommended-keyword-list.md) |
| `get_recommended_item_list` | 推荐推广商品 — [apis/get-recommended-item-list.md](./apis/get-recommended-item-list.md) |

### 效果报表

| API | 要点 |
|-----|------|
| `get_all_cpc_ads_daily_performance` / `hourly` | 全部 CPC 广告效果 |
| `get_product_campaign_daily_performance` / `hourly` | 商品广告活动效果 |
| `get_gms_campaign_performance` / `get_gms_item_performance` | GMS 广告效果 |

### 手动商品广告

| API | 要点 |
|-----|------|
| `get_product_level_campaign_id_list` | 商品级 campaign ID 列表 — [apis/get-product-level-campaign-id-list.md](./apis/get-product-level-campaign-id-list.md) |
| `get_product_level_campaign_setting_info` | campaign 设置详情 — [apis/get-product-level-campaign-setting-info.md](./apis/get-product-level-campaign-setting-info.md) |
| `create_manual_product_ads` | 创建手动选品广告 — [apis/create-manual-product-ads.md](./apis/create-manual-product-ads.md) |
| `edit_manual_product_ads` / `edit_manual_product_ad_keywords` | 编辑广告/关键词 |
| `get_create_product_ad_budget_suggestion` | 预算建议 — [apis/get-create-product-ad-budget-suggestion.md](./apis/get-create-product-ad-budget-suggestion.md) |
| `get_product_recommended_roi_target` | 推荐 ROI — [apis/get-product-recommended-roi-target.md](./apis/get-product-recommended-roi-target.md) |

### GMS 广告

| API | 要点 |
|-----|------|
| `check_create_gms_product_campaign_eligibility` | 创建资格检查 — [apis/check-create-gms-product-campaign-eligibility.md](./apis/check-create-gms-product-campaign-eligibility.md) |
| `create_gms_product_campaign` / `edit_gms_product_campaign` | 创建/编辑 GMS campaign |
| `edit_gms_item_product_campaign` | 编辑 GMS 商品 campaign — [apis/edit-gms-item-product-campaign.md](./apis/edit-gms-item-product-campaign.md) |
| `list_gms_user_deleted_item` | 用户删除商品列表 — [apis/list-gms-user-deleted-item.md](./apis/list-gms-user-deleted-item.md) |

---

## 网关错误码

| errcode | 含义 | 建议 |
|---------|------|------|
| 1002 | 参数/未登录 | 检查 shopId 与 API Key |
| 1003 | 代理/网络异常 | 稍后重试 |
| 1004 | 无 **AD** 授权记录 | 即使店铺有 ERP，也须 auth 发起 `appType=ad` |
| 1005 | Token 失效或 path 未白名单 | 重新 AD 授权；确认 `api/v2/ads/...` |

---

## curl 示例

```bash
export KEY=$LINKFOXAGENT_API_KEY
BASE=https://tool-gateway.linkfox.com

# 业务转发：只传 path + shopId（服务端注入 AD token）
curl -X POST $BASE/shopee/developerProxy -H "Authorization: $KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "path": "api/v2/ads/get_total_balance",
    "method": "GET",
    "shopId": "67890"
  }'
```

---

## Feedback API

```bash
curl -X POST https://skill-api.linkfox.com/api/v1/public/feedback \
  -H "Content-Type: application/json" \
  -d '{"skillName":"linkfox-shopee-store-ads","sentiment":"POSITIVE",
       "category":"OTHER","content":"广告余额查询正常"}'
```
