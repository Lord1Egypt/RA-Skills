---
name: linkfox-shopee-store-global-product
description: Shopee（虾皮）跨境全球商品 GlobalProduct（与 linkfox-shopee-store-auth 同系列），经 /shopee/developerProxy 转发 Shopee Open API GlobalProduct 模块全部 34 个接口：get_category、get_global_item_list、add_global_item、create_publish_task、update_price、update_stock 等。当用户提到 Shopee 全球商品、跨境商品、GlobalProduct、全球 SKU、发布到站点、merchantId、global_item_id、get_global_item_list、add_global_item 时触发。即使未明确提及"全球商品"，只要涉及已授权 Shopee 商户的全球商品管理或跨境发布，也应触发。
---

# Shopee 全球商品 GlobalProduct

Shopee Open Platform **GlobalProduct 模块**（34 个 API）。**依赖 `linkfox-shopee-store-auth`** 选店；经 **`POST /shopee/developerProxy`** 传入 `shopId`（或 `merchantId`），由服务端解析 token 转发（`path` 须 `api/v2/global_product/...`）。

## 调用方式

- **API 端点**：`POST /shopee/developerProxy`（不同操作通过请求体区分；完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/global_product_api.py '<JSON 参数>' [--inline]`（可用脚本见上文脚本一览）
- **成本约束**：本工具会消耗算力；失败/空结果不得自动换关键词、翻页或连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-shopee-store-global-product-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
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

GlobalProduct 模块索引：[v2.global_product.get_category](https://open.shopee.com/documents/v2/v2.global_product.get_category?module=90&type=1)

---

## Prerequisites（必须先读）

1. 运行 `python scripts/check_auth_dependency.py`；exit code **42** → 先安装 **`linkfox-shopee-store-auth`** 并授权。
2. **不要**在本 skill 内实现授权/令牌逻辑。
3. GlobalProduct 为**商户级** API，通常传 **`merchantId`**；发布/映射类接口可能同时需要 `shopId`。

---

## Core Concepts

- **转发链路**：`developerProxy`（`shopId`/`merchantId` 选店，服务端注入 token）→ 紫鸟 `shopee-proxy` → Shopee API
- **Product vs GlobalProduct**：`linkfox-shopee-store-product` 管单店 listing；本 skill 管**跨境全球商品**及发布到各站点
- **典型流程**：`get_category` → `get_attribute_tree` → `add_global_item` → `create_publish_task` → `get_publish_task_result`
- **SKU**：`init_tier_variation` / `get_global_model_list` / `add_global_model` 等
- **本地店商品**（非全球）→ `linkfox-shopee-store-product`

## 可用脚本（GlobalProduct 模块 34 个 API）

| 分组 | 脚本 |
|------|------|
| 类目/属性 | `get_category.py`、`get_attribute_tree.py`、`get_brand_list.py`、`category_recommend.py`、`get_recommend_attribute.py`、`search_global_attribute_value_list.py` |
| 全球商品 CRUD | `get_global_item_list.py`、`get_global_item_info.py`、`add_global_item.py`、`update_global_item.py`、`delete_global_item.py`、`get_global_item_limit.py` |
| 全球 SKU | `get_global_model_list.py`、`init_tier_variation.py`、`update_tier_variation.py`、`add_global_model.py`、`update_global_model.py`、`delete_global_model.py` |
| 价格/库存/同步 | `update_price.py`、`update_stock.py`、`set_sync_field.py`、`get_local_adjustment_rate.py`、`update_local_adjustment_rate.py` |
| 发布到站点 | `create_publish_task.py`、`get_publishable_shop.py`、`get_publish_task_result.py`、`get_published_list.py`、`get_shop_publishable_status.py`、`get_global_item_id.py` |
| 尺码表/规格 | `support_size_chart.py`、`update_size_chart.py`、`get_size_chart_list.py`、`get_size_chart_detail.py`、`get_variations.py` |
| 通用入口 | `global_product_api.py`（JSON 含 `api` 字段） |

共享：`_shopee_global_product_common.py`、`_global_product_endpoints.py`、`_global_product_api_runner.py`。

## 接口说明（按 API）

入参与响应细节放在 `references/apis/`，SKILL 只保留索引。

| API | 说明文档 |
|-----|----------|
| `add_global_item` | [references/apis/add-global-item.md](./references/apis/add-global-item.md) |
| `add_global_model` | [references/apis/add-global-model.md](./references/apis/add-global-model.md) |
| `category_recommend` | [references/apis/category-recommend.md](./references/apis/category-recommend.md) |
| `create_publish_task` | [references/apis/create-publish-task.md](./references/apis/create-publish-task.md) |
| `delete_global_item` | [references/apis/delete-global-item.md](./references/apis/delete-global-item.md) |
| `delete_global_model` | [references/apis/delete-global-model.md](./references/apis/delete-global-model.md) |
| `get_attribute_tree` | [references/apis/get-attribute-tree.md](./references/apis/get-attribute-tree.md) |
| `get_brand_list` | [references/apis/get-brand-list.md](./references/apis/get-brand-list.md) |
| `get_category` | [references/apis/get-category.md](./references/apis/get-category.md) |
| `get_global_item_id` | [references/apis/get-global-item-id.md](./references/apis/get-global-item-id.md) |
| `get_global_item_info` | [references/apis/get-global-item-info.md](./references/apis/get-global-item-info.md) |
| `get_global_item_limit` | [references/apis/get-global-item-limit.md](./references/apis/get-global-item-limit.md) |
| `get_global_item_list` | [references/apis/get-global-item-list.md](./references/apis/get-global-item-list.md) |
| `get_global_model_list` | [references/apis/get-global-model-list.md](./references/apis/get-global-model-list.md) |
| `get_local_adjustment_rate` | [references/apis/get-local-adjustment-rate.md](./references/apis/get-local-adjustment-rate.md) |
| `get_publish_task_result` | [references/apis/get-publish-task-result.md](./references/apis/get-publish-task-result.md) |
| `get_publishable_shop` | [references/apis/get-publishable-shop.md](./references/apis/get-publishable-shop.md) |
| `get_published_list` | [references/apis/get-published-list.md](./references/apis/get-published-list.md) |
| `get_recommend_attribute` | [references/apis/get-recommend-attribute.md](./references/apis/get-recommend-attribute.md) |
| `get_shop_publishable_status` | [references/apis/get-shop-publishable-status.md](./references/apis/get-shop-publishable-status.md) |
| `get_size_chart_detail` | [references/apis/get-size-chart-detail.md](./references/apis/get-size-chart-detail.md) |
| `get_size_chart_list` | [references/apis/get-size-chart-list.md](./references/apis/get-size-chart-list.md) |
| `get_variations` | [references/apis/get-variations.md](./references/apis/get-variations.md) |
| `init_tier_variation` | [references/apis/init-tier-variation.md](./references/apis/init-tier-variation.md) |
| `search_global_attribute_value_list` | [references/apis/search-global-attribute-value-list.md](./references/apis/search-global-attribute-value-list.md) |
| `set_sync_field` | [references/apis/set-sync-field.md](./references/apis/set-sync-field.md) |
| `support_size_chart` | [references/apis/support-size-chart.md](./references/apis/support-size-chart.md) |
| `update_global_item` | [references/apis/update-global-item.md](./references/apis/update-global-item.md) |
| `update_global_model` | [references/apis/update-global-model.md](./references/apis/update-global-model.md) |
| `update_local_adjustment_rate` | [references/apis/update-local-adjustment-rate.md](./references/apis/update-local-adjustment-rate.md) |
| `update_price` | [references/apis/update-price.md](./references/apis/update-price.md) |
| `update_size_chart` | [references/apis/update-size-chart.md](./references/apis/update-size-chart.md) |
| `update_stock` | [references/apis/update-stock.md](./references/apis/update-stock.md) |
| `update_tier_variation` | [references/apis/update-tier-variation.md](./references/apis/update-tier-variation.md) |

模块总览 / Feedback 见 [references/api.md](./references/api.md)。

## Usage Scenarios

### 1. 创建全球商品并发布
1. `get_category.py` + `get_attribute_tree.py`（`merchantId`）
2. `add_global_item.py` 传完整 `body`
3. `create_publish_task.py` 发布到目标站点
4. `get_publish_task_result.py` 查发布结果

### 2. 查全球商品与改库存
1. `get_global_item_list.py`：`offset`、`page_size`
2. `get_global_item_info.py`：`global_item_id_list`
3. `update_stock.py` / `update_price.py`：POST `body`

## 调用原则

- 先看 **`developerProxy.httpStatus`**，再读 `*Response` 字段
- GET：业务参数放 JSON 顶层（runner 拼 queryString）
- POST：复杂接口传 `body`；简单接口可传顶层 body 字段
- 每个脚本 docstring 含 **官方文档 URL**（`module=90`）

## Not Applicable

- 店铺授权 → `linkfox-shopee-store-auth`
- 商户信息 → `linkfox-shopee-store-merchant`
- 单店 listing → `linkfox-shopee-store-product`
- 订单 → `linkfox-shopee-store-orders`
- 店铺信息 → `linkfox-shopee-store-shop`
- 图片/视频上传 → MediaSpace 模块

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
