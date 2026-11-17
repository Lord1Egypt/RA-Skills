---
name: linkfox-shopee-store-ams
description: Shopee（虾皮）联盟营销 AMS Affiliate Marketing Solutions（与 linkfox-shopee-store-auth 同系列），经 /shopee/developerProxy 转发 Shopee Open API AMS 模块全部 36 个接口：get_open_campaign_added_product、batch_add_products_to_open_campaign、create_new_targeted_campaign、get_affiliate_performance、get_shop_performance 等。当用户提到 Shopee 联盟营销、AMS、达人带货、affiliate、Open Campaign、Targeted Campaign、佣金率、达人推广、get_open_campaign_added_product 时触发。即使未明确提及"联盟"，只要涉及已授权 Shopee 店铺的联盟推广或达人 campaign 管理，也应触发。
---

# Shopee 联盟营销 AMS

Shopee Open Platform **AMS（Affiliate Marketing Solutions）模块**（36 个 API）。**依赖 `linkfox-shopee-store-auth`** 选店；经 **`POST /shopee/developerProxy`** 传入 `shopId`（或 `merchantId`），由服务端解析 token 转发（`path` 须 `api/v2/ams/...`）。

## 调用方式

- **API 端点**：`POST /shopee/developerProxy`（不同操作通过请求体区分；完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/<脚本名>.py '<JSON 参数>' [--inline]`（可用脚本见上文脚本一览）
- **成本约束**：本工具会消耗算力；失败/空结果不得自动换关键词、翻页或连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-shopee-store-ams-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
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

AMS 模块索引：[v2.ams.get_open_campaign_added_product](https://open.shopee.com/documents/v2/v2.ams.get_open_campaign_added_product?module=127&type=1)

---

## Prerequisites（必须先读）

1. 运行 `python scripts/check_auth_dependency.py`；exit code **42** → 先安装 **`linkfox-shopee-store-auth`** 并授权店铺。
2. **不要**在本 skill 内实现授权/令牌逻辑。
3. **AMS vs Ads**：本 skill 为联盟营销/达人带货；站内 CPC 广告见 `linkfox-shopee-store-ads`（module=117）。

---

## Core Concepts

- **转发链路**：`developerProxy`（`shopId`/`merchantId` 选店，服务端注入 token）→ 紫鸟 `shopee-proxy` → Shopee API
- **Open Campaign**：开放推广，所有达人可推广 → `get_open_campaign_added_product`、`batch_add_products_to_open_campaign`
- **Targeted Campaign**：定向推广，指定达人 → `create_new_targeted_campaign`、`edit_affiliate_list_of_targeted_campaign`
- **效果**：`get_shop_performance`、`get_product_performance`、`get_affiliate_performance`
- **佣金**：`get_shop_suggested_rate`、`batch_get_products_suggested_rate`

## 可用脚本（AMS 模块 36 个 API）

| 分组 | 脚本 |
|------|------|
| Open Campaign | `get_open_campaign_added_product.py`、`batch_add_products_to_open_campaign.py`、`get_open_campaign_performance.py` 等 |
| Targeted Campaign | `create_new_targeted_campaign.py`、`get_targeted_campaign_list.py`、`terminate_targeted_campaign.py` 等 |
| 达人/Affiliate | `get_recommended_affiliate_list.py`、`query_affiliate_list.py`、`get_affiliate_performance.py` |
| 效果报表 | `get_shop_performance.py`、`get_product_performance.py`、`get_conversion_report.py` |
| 通用入口 | `ams_api.py`（JSON 含 `api` 字段） |

完整列表见 `references/api.md`。共享：`_shopee_ams_common.py`、`_ams_endpoints.py`、`_ams_api_runner.py`。

## 接口说明（按 API）

入参与响应细节放在 `references/apis/`，SKILL 只保留索引。

| API | 说明文档 |
|-----|----------|
| `add_all_products_to_open_campaign` | [references/apis/add-all-products-to-open-campaign.md](./references/apis/add-all-products-to-open-campaign.md) |
| `batch_add_products_to_open_campaign` | [references/apis/batch-add-products-to-open-campaign.md](./references/apis/batch-add-products-to-open-campaign.md) |
| `batch_edit_products_open_campaign_setting` | [references/apis/batch-edit-products-open-campaign-setting.md](./references/apis/batch-edit-products-open-campaign-setting.md) |
| `batch_get_products_suggested_rate` | [references/apis/batch-get-products-suggested-rate.md](./references/apis/batch-get-products-suggested-rate.md) |
| `batch_remove_products_open_campaign_setting` | [references/apis/batch-remove-products-open-campaign-setting.md](./references/apis/batch-remove-products-open-campaign-setting.md) |
| `create_new_targeted_campaign` | [references/apis/create-new-targeted-campaign.md](./references/apis/create-new-targeted-campaign.md) |
| `edit_affiliate_list_of_targeted_campaign` | [references/apis/edit-affiliate-list-of-targeted-campaign.md](./references/apis/edit-affiliate-list-of-targeted-campaign.md) |
| `edit_all_products_open_campaign_setting` | [references/apis/edit-all-products-open-campaign-setting.md](./references/apis/edit-all-products-open-campaign-setting.md) |
| `edit_product_list_of_targeted_campaign` | [references/apis/edit-product-list-of-targeted-campaign.md](./references/apis/edit-product-list-of-targeted-campaign.md) |
| `get_affiliate_performance` | [references/apis/get-affiliate-performance.md](./references/apis/get-affiliate-performance.md) |
| `get_auto_add_new_product_toggle_status` | [references/apis/get-auto-add-new-product-toggle-status.md](./references/apis/get-auto-add-new-product-toggle-status.md) |
| `get_campaign_key_metrics_performance` | [references/apis/get-campaign-key-metrics-performance.md](./references/apis/get-campaign-key-metrics-performance.md) |
| `get_content_performance` | [references/apis/get-content-performance.md](./references/apis/get-content-performance.md) |
| `get_conversion_report` | [references/apis/get-conversion-report.md](./references/apis/get-conversion-report.md) |
| `get_managed_affiliate_list` | [references/apis/get-managed-affiliate-list.md](./references/apis/get-managed-affiliate-list.md) |
| `get_open_campaign_added_product` | [references/apis/get-open-campaign-added-product.md](./references/apis/get-open-campaign-added-product.md) |
| `get_open_campaign_batch_task_result` | [references/apis/get-open-campaign-batch-task-result.md](./references/apis/get-open-campaign-batch-task-result.md) |
| `get_open_campaign_not_added_product` | [references/apis/get-open-campaign-not-added-product.md](./references/apis/get-open-campaign-not-added-product.md) |
| `get_open_campaign_performance` | [references/apis/get-open-campaign-performance.md](./references/apis/get-open-campaign-performance.md) |
| `get_optimization_suggestion_product` | [references/apis/get-optimization-suggestion-product.md](./references/apis/get-optimization-suggestion-product.md) |
| `get_performance_data_update_time` | [references/apis/get-performance-data-update-time.md](./references/apis/get-performance-data-update-time.md) |
| `get_product_performance` | [references/apis/get-product-performance.md](./references/apis/get-product-performance.md) |
| `get_recommended_affiliate_list` | [references/apis/get-recommended-affiliate-list.md](./references/apis/get-recommended-affiliate-list.md) |
| `get_shop_performance` | [references/apis/get-shop-performance.md](./references/apis/get-shop-performance.md) |
| `get_shop_suggested_rate` | [references/apis/get-shop-suggested-rate.md](./references/apis/get-shop-suggested-rate.md) |
| `get_targeted_campaign_addable_product_list` | [references/apis/get-targeted-campaign-addable-product-list.md](./references/apis/get-targeted-campaign-addable-product-list.md) |
| `get_targeted_campaign_list` | [references/apis/get-targeted-campaign-list.md](./references/apis/get-targeted-campaign-list.md) |
| `get_targeted_campaign_performance` | [references/apis/get-targeted-campaign-performance.md](./references/apis/get-targeted-campaign-performance.md) |
| `get_targeted_campaign_settings` | [references/apis/get-targeted-campaign-settings.md](./references/apis/get-targeted-campaign-settings.md) |
| `get_validation_list` | [references/apis/get-validation-list.md](./references/apis/get-validation-list.md) |
| `get_validation_report` | [references/apis/get-validation-report.md](./references/apis/get-validation-report.md) |
| `query_affiliate_list` | [references/apis/query-affiliate-list.md](./references/apis/query-affiliate-list.md) |
| `remove_all_products_open_campaign_setting` | [references/apis/remove-all-products-open-campaign-setting.md](./references/apis/remove-all-products-open-campaign-setting.md) |
| `terminate_targeted_campaign` | [references/apis/terminate-targeted-campaign.md](./references/apis/terminate-targeted-campaign.md) |
| `update_auto_add_new_product_setting` | [references/apis/update-auto-add-new-product-setting.md](./references/apis/update-auto-add-new-product-setting.md) |
| `update_basic_info_of_targeted_campaign` | [references/apis/update-basic-info-of-targeted-campaign.md](./references/apis/update-basic-info-of-targeted-campaign.md) |

模块总览 / Feedback 见 [references/api.md](./references/api.md)。

## Usage Scenarios

### 1. 管理 Open Campaign 商品
1. `get_open_campaign_added_product.py` 查已加入商品
2. `get_open_campaign_not_added_product.py` 查可加入商品
3. `batch_add_products_to_open_campaign.py` 批量添加

### 2. 创建定向达人 Campaign
1. `get_recommended_affiliate_list.py` 选达人
2. `create_new_targeted_campaign.py` 传完整 `body`
3. `get_targeted_campaign_performance.py` 查效果

## 调用原则

- 先看 **`developerProxy.httpStatus`**，再读 `*Response` 字段
- GET：业务参数放 JSON 顶层
- POST：复杂接口传 `body`
- 每个脚本 docstring 含 **官方文档 URL**（`module=127`）

## Not Applicable

- 店铺授权 → `linkfox-shopee-store-auth`
- 站内 CPC 广告 → `linkfox-shopee-store-ads`
- 商品 listing → `linkfox-shopee-store-product`
- 店铺视频 → `linkfox-shopee-store-video`
- 订单 → `linkfox-shopee-store-orders`

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
