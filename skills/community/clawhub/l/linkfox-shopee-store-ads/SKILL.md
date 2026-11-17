---
name: linkfox-shopee-store-ads
description: Shopee（虾皮）店铺站内广告 Ads（与 linkfox-shopee-store-auth 同系列），经 /shopee/developerProxy 转发 Shopee Open API Ads 模块 23 个接口：get_total_balance、create_manual_product_ads、get_product_campaign_daily_performance、GMS 广告等。调用前须确认目标店已有 appType=ad 授权（ERP 授权不能代替）。当用户提到 Shopee 广告、Ads、广告余额、CPC、商品推广、手动广告、campaign、广告效果、ROI、get_total_balance、广告授权 时触发。即使未明确提及"广告"，只要涉及已授权 Shopee 店铺的广告账户、推广或效果查询，也应触发。
---

# Shopee 店铺 Ads

Shopee Open Platform **Ads 模块**（23 个 API，不含即将下线的 auto product ads）。**依赖 `linkfox-shopee-store-auth`**；须目标店存在 **`appType=ad`** 授权。经 **`POST /shopee/developerProxy`** 传入 `shopId`（或 `merchantId`）+ `api/v2/ads/...` 路径，服务端自动走 AD 应用 Token（**勿**传 `accessToken` / `appType`）。

## 调用方式

- **API 端点**：`POST /shopee/developerProxy`（不同操作通过请求体区分；完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/<脚本名>.py '<JSON 参数>' [--inline]`（可用脚本见上文脚本一览）
- **成本约束**：本工具会消耗算力；失败/空结果不得自动换关键词、翻页或连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-shopee-store-ads-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 解决认证和算力问题
发生以下异常情况时，采用 references/onboarding.md 引导解决问题：

### 异常情况
- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示算力或余额不足**：消息含"算力余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

## 官方参考

Ads 模块索引：[v2.ads.get_total_balance](https://open.shopee.com/documents/v2/v2.ads.get_total_balance?module=117&type=1)

---

## Prerequisites（必须先读）

1. 运行 `python scripts/check_auth_dependency.py`；exit code **42** → 先安装 **`linkfox-shopee-store-auth`**。
2. **不要**在本 skill 内实现授权/令牌逻辑；授权一律走 auth skill。
3. 调用业务 API **之前**，用 auth 的 `authorized_stores.py` 确认目标店存在 **`appType=ad`**：
   - 仅有 `appType=erp`（或历史空值）→ **不能**当广告已授权；引导 `authorize_url.py` 且传 **`appType=ad`**
   - 两项都缺 → 若用户只要广告，只开 AD 授权即可（不必先开 ERP）
4. Ads API 还需 Shopee 侧开通广告能力；并非所有站点/店铺可用。
5. **禁止**向 `developerProxy` 传 `accessToken` 或 `appType`；path 用 `api/v2/ads/**` 即可由服务端路由到 AD。

---

## Core Concepts

- **AD 与 ERP 分离**：广告 Token 与 ERP Token 独立；店铺在列表中存在 ≠ 广告已授权
- **转发链路**：`developerProxy`（`shopId`/`merchantId` + `api/v2/ads/...`，服务端注入 **AD** token）→ 紫鸟 `shopee-proxy/ad/...` → Shopee API
- **余额**：`get_total_balance` 查广告账户余额
- **手动商品广告**：`create_manual_product_ads` → `edit_manual_product_ads` / `edit_manual_product_ad_keywords`
- **效果报表**：`get_all_cpc_ads_*_performance`、`get_product_campaign_*_performance`
- **GMS**：`create_gms_product_campaign` 等系列
- **未纳入**：`create_auto_product_ads`、`edit_auto_product_ads`（官方标注 coming offline soon）
- **联盟营销 AMS**（module=127）→ 非本 skill

## 可用脚本（Ads 模块 23 个 API）

| 分组 | 脚本 |
|------|------|
| 账户/推荐 | `get_total_balance.py`、`get_shop_toggle_info.py`、`get_recommended_keyword_list.py`、`get_recommended_item_list.py` |
| CPC 效果 | `get_all_cpc_ads_daily_performance.py`、`get_all_cpc_ads_hourly_performance.py` |
| 商品广告 | `create_manual_product_ads.py`、`edit_manual_product_ads.py`、`get_product_level_campaign_id_list.py` 等 |
| GMS | `create_gms_product_campaign.py`、`get_gms_campaign_performance.py` 等 |
| 通用入口 | `ads_api.py`（JSON 含 `api` 字段） |

完整列表见 `references/api.md`。共享：`_shopee_ads_common.py`、`_ads_endpoints.py`、`_ads_api_runner.py`。

## 接口说明（按 API）

入参与响应细节放在 `references/apis/`，SKILL 只保留索引。

| API | 说明文档 |
|-----|----------|
| `check_create_gms_product_campaign_eligibility` | [references/apis/check-create-gms-product-campaign-eligibility.md](./references/apis/check-create-gms-product-campaign-eligibility.md) |
| `create_gms_product_campaign` | [references/apis/create-gms-product-campaign.md](./references/apis/create-gms-product-campaign.md) |
| `create_manual_product_ads` | [references/apis/create-manual-product-ads.md](./references/apis/create-manual-product-ads.md) |
| `edit_gms_item_product_campaign` | [references/apis/edit-gms-item-product-campaign.md](./references/apis/edit-gms-item-product-campaign.md) |
| `edit_gms_product_campaign` | [references/apis/edit-gms-product-campaign.md](./references/apis/edit-gms-product-campaign.md) |
| `edit_manual_product_ad_keywords` | [references/apis/edit-manual-product-ad-keywords.md](./references/apis/edit-manual-product-ad-keywords.md) |
| `edit_manual_product_ads` | [references/apis/edit-manual-product-ads.md](./references/apis/edit-manual-product-ads.md) |
| `get_ads_facil_shop_rate` | [references/apis/get-ads-facil-shop-rate.md](./references/apis/get-ads-facil-shop-rate.md) |
| `get_all_cpc_ads_daily_performance` | [references/apis/get-all-cpc-ads-daily-performance.md](./references/apis/get-all-cpc-ads-daily-performance.md) |
| `get_all_cpc_ads_hourly_performance` | [references/apis/get-all-cpc-ads-hourly-performance.md](./references/apis/get-all-cpc-ads-hourly-performance.md) |
| `get_create_product_ad_budget_suggestion` | [references/apis/get-create-product-ad-budget-suggestion.md](./references/apis/get-create-product-ad-budget-suggestion.md) |
| `get_gms_campaign_performance` | [references/apis/get-gms-campaign-performance.md](./references/apis/get-gms-campaign-performance.md) |
| `get_gms_item_performance` | [references/apis/get-gms-item-performance.md](./references/apis/get-gms-item-performance.md) |
| `get_product_campaign_daily_performance` | [references/apis/get-product-campaign-daily-performance.md](./references/apis/get-product-campaign-daily-performance.md) |
| `get_product_campaign_hourly_performance` | [references/apis/get-product-campaign-hourly-performance.md](./references/apis/get-product-campaign-hourly-performance.md) |
| `get_product_level_campaign_id_list` | [references/apis/get-product-level-campaign-id-list.md](./references/apis/get-product-level-campaign-id-list.md) |
| `get_product_level_campaign_setting_info` | [references/apis/get-product-level-campaign-setting-info.md](./references/apis/get-product-level-campaign-setting-info.md) |
| `get_product_recommended_roi_target` | [references/apis/get-product-recommended-roi-target.md](./references/apis/get-product-recommended-roi-target.md) |
| `get_recommended_item_list` | [references/apis/get-recommended-item-list.md](./references/apis/get-recommended-item-list.md) |
| `get_recommended_keyword_list` | [references/apis/get-recommended-keyword-list.md](./references/apis/get-recommended-keyword-list.md) |
| `get_shop_toggle_info` | [references/apis/get-shop-toggle-info.md](./references/apis/get-shop-toggle-info.md) |
| `get_total_balance` | [references/apis/get-total-balance.md](./references/apis/get-total-balance.md) |
| `list_gms_user_deleted_item` | [references/apis/list-gms-user-deleted-item.md](./references/apis/list-gms-user-deleted-item.md) |

模块总览 / Feedback 见 [references/api.md](./references/api.md)。

## Usage Scenarios

### 0. 确认 AD 授权（每次任务开头）

1. auth：`authorized_stores.py` → 找目标 `shopId` 且 **`appType=ad`**
2. 缺失 → auth：`authorize_url.py` 传 `appType=ad`，提示用户完成**广告**授权（URL 1 小时有效）
3. 完成后再进入下列业务场景；收到 **1004** 时优先怀疑缺 AD 授权，不要用 ERP 记录硬调

### 1. 查余额与推荐
1. `get_total_balance.py`
2. `get_recommended_item_list.py` / `get_recommended_keyword_list.py`

### 2. 创建手动商品广告
1. `get_create_product_ad_budget_suggestion.py`
2. `create_manual_product_ads.py` 传完整 `body`
3. `get_product_campaign_daily_performance.py` 查效果

## 调用原则

- 先确认 **`appType=ad`**，再调脚本
- 先看 **`developerProxy.httpStatus`** / 网关 `errcode`，再读 `*Response` 字段
- GET：业务参数放 JSON 顶层
- POST：复杂接口传 `body`；create/edit 建议传唯一 `reference_id` 防重复
- 每个脚本 docstring 含 **官方文档 URL**（`module=117`）
- 不要先 `storeTokens` 取 raw token，也不要在 proxy 里塞 `accessToken`

## Not Applicable

- 店铺授权 → `linkfox-shopee-store-auth`
- 商品 listing → `linkfox-shopee-store-product`
- 联盟营销 AMS（module=127）→ `linkfox-shopee-store-ams`
- Amazon 广告 → `linkfox-amazon-ads-*` 系列

## 算力消耗规则

不消耗算力。

**Feedback:**

Auto-detect and report feedback via the Feedback API when any of the following apply:
1. The functionality or purpose described in this skill does not match actual behavior
2. The skill's results do not match the user's intent
3. The user expresses dissatisfaction or praise about this skill
4. Anything you believe could be improved

Call the feedback API as specified in `references/api.md`. Do not interrupt the user's flow.


---
*For more high-quality, professional cross-border e-commerce skills, visit [LinkFox Skills](https://skill.linkfox.com/).*
