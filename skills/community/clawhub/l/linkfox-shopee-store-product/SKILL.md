---
name: linkfox-shopee-store-product
description: Shopee（虾皮）店铺商品管理（与 linkfox-shopee-store-auth 同系列），经 /shopee/developerProxy 转发 Shopee Open API Product 模块全部 57 个接口：get_category、get_item_list、add_item、update_item、update_price、update_stock、boost_item、search_item 等。当用户提到 Shopee 商品、虾皮 listing、上架、下架、SKU、库存、价格、类目、属性、get_item_list、add_item、商品评论、boost 置顶 时触发。即使未明确提及"商品"，只要涉及已授权 Shopee 店铺的商品查询、创建或更新，也应触发。
---

# Shopee 店铺 Product

Shopee Open Platform **Product 模块**（57 个 API）。**依赖 `linkfox-shopee-store-auth`** 选店；经 **`POST /shopee/developerProxy`** 传入 `shopId`（或 `merchantId`），由服务端解析 token 转发（`path` 须 `api/v2/product/...`）。

## 调用方式

- **API 端点**：`POST /shopee/developerProxy`（不同操作通过请求体区分；完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/<脚本名>.py '<JSON 参数>' [--inline]`（可用脚本见上文脚本一览）
- **成本约束**：本工具会消耗算力；失败/空结果不得自动换关键词、翻页或连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/<skill-name>-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
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

Product 模块索引：[v2.product.get_category](https://open.shopee.com/documents/v2/v2.product.get_category?module=89&type=1)

---

## Prerequisites（必须先读）

1. 运行 `python scripts/check_auth_dependency.py`；exit code **42** → 先安装 **`linkfox-shopee-store-auth`** 并授权店铺。
2. **不要**在本 skill 内实现授权/令牌逻辑。

---

## Core Concepts

- **转发链路**：`developerProxy`（`shopId`/`merchantId` 选店，服务端注入 token）→ 紫鸟 `shopee-proxy` → Shopee API
- **上架流程**：`get_category` → `get_attribute_tree` → `add_item`（复杂 body 建议传 `body` 字段）
- **日常运营**：`get_item_list` / `get_item_base_info` 查商品；`update_price` / `update_stock` 改价改库存；`unlist_item` 上下架
- **SKU**：`init_tier_variation` / `get_model_list` / `add_model` 等
- **选品数据**（非店铺 listing）→ `linkfox-youying-shopee-product-search`（不依赖 auth）

## 可用脚本（Product 模块 57 个 API）

| 分组 | 脚本 |
|------|------|
| 类目/属性/品牌 | `get_category.py`、`get_attribute_tree.py`、`get_brand_list.py`、`category_recommend.py`、`get_recommend_attribute.py`、`search_attribute_value_list.py` |
| 商品 CRUD | `get_item_list.py`、`get_item_base_info.py`、`get_item_extra_info.py`、`add_item.py`、`update_item.py`、`delete_item.py`、`unlist_item.py`、`search_item.py` |
| SKU/价格/库存 | `get_model_list.py`、`init_tier_variation.py`、`update_tier_variation.py`、`add_model.py`、`update_model.py`、`delete_model.py`、`update_price.py`、`update_stock.py` |
| 推广/评论 | `boost_item.py`、`get_boosted_list.py`、`get_item_promotion.py`、`get_comment.py`、`reply_comment.py` |
| 扩展 | Kit/SSP/Direct/Mart/Outlet、尺码表、违规、车辆兼容、内容诊断等 — 见 `references/api.md` 完整列表 |
| 通用入口 | `product_api.py`（JSON 含 `api` 字段） |

共享：`_shopee_product_common.py`、`_product_endpoints.py`、`_product_api_runner.py`。

## 接口说明（按 API）

入参与响应细节放在 `references/apis/`，SKILL 只保留索引。

| API | 说明文档 |
|-----|----------|
| `add_item` | [references/apis/add-item.md](./references/apis/add-item.md) |
| `add_kit_item` | [references/apis/add-kit-item.md](./references/apis/add-kit-item.md) |
| `add_model` | [references/apis/add-model.md](./references/apis/add-model.md) |
| `boost_item` | [references/apis/boost-item.md](./references/apis/boost-item.md) |
| `category_recommend` | [references/apis/category-recommend.md](./references/apis/category-recommend.md) |
| `delete_item` | [references/apis/delete-item.md](./references/apis/delete-item.md) |
| `delete_model` | [references/apis/delete-model.md](./references/apis/delete-model.md) |
| `generate_kit_image` | [references/apis/generate-kit-image.md](./references/apis/generate-kit-image.md) |
| `get_aitem_by_pitem_id` | [references/apis/get-aitem-by-pitem-id.md](./references/apis/get-aitem-by-pitem-id.md) |
| `get_all_vehicle_list` | [references/apis/get-all-vehicle-list.md](./references/apis/get-all-vehicle-list.md) |
| `get_attribute_tree` | [references/apis/get-attribute-tree.md](./references/apis/get-attribute-tree.md) |
| `get_boosted_list` | [references/apis/get-boosted-list.md](./references/apis/get-boosted-list.md) |
| `get_brand_list` | [references/apis/get-brand-list.md](./references/apis/get-brand-list.md) |
| `get_category` | [references/apis/get-category.md](./references/apis/get-category.md) |
| `get_comment` | [references/apis/get-comment.md](./references/apis/get-comment.md) |
| `get_direct_item_list` | [references/apis/get-direct-item-list.md](./references/apis/get-direct-item-list.md) |
| `get_direct_shop_recommended_price` | [references/apis/get-direct-shop-recommended-price.md](./references/apis/get-direct-shop-recommended-price.md) |
| `get_item_base_info` | [references/apis/get-item-base-info.md](./references/apis/get-item-base-info.md) |
| `get_item_content_diagnosis_result` | [references/apis/get-item-content-diagnosis-result.md](./references/apis/get-item-content-diagnosis-result.md) |
| `get_item_extra_info` | [references/apis/get-item-extra-info.md](./references/apis/get-item-extra-info.md) |
| `get_item_limit` | [references/apis/get-item-limit.md](./references/apis/get-item-limit.md) |
| `get_item_list` | [references/apis/get-item-list.md](./references/apis/get-item-list.md) |
| `get_item_list_by_content_diagnosis` | [references/apis/get-item-list-by-content-diagnosis.md](./references/apis/get-item-list-by-content-diagnosis.md) |
| `get_item_promotion` | [references/apis/get-item-promotion.md](./references/apis/get-item-promotion.md) |
| `get_item_violation_info` | [references/apis/get-item-violation-info.md](./references/apis/get-item-violation-info.md) |
| `get_kit_item_info` | [references/apis/get-kit-item-info.md](./references/apis/get-kit-item-info.md) |
| `get_kit_item_limit` | [references/apis/get-kit-item-limit.md](./references/apis/get-kit-item-limit.md) |
| `get_main_item_list` | [references/apis/get-main-item-list.md](./references/apis/get-main-item-list.md) |
| `get_mart_item_by_outlet_item_id` | [references/apis/get-mart-item-by-outlet-item-id.md](./references/apis/get-mart-item-by-outlet-item-id.md) |
| `get_mart_item_mapping_by_id` | [references/apis/get-mart-item-mapping-by-id.md](./references/apis/get-mart-item-mapping-by-id.md) |
| `get_model_list` | [references/apis/get-model-list.md](./references/apis/get-model-list.md) |
| `get_product_certification_rule` | [references/apis/get-product-certification-rule.md](./references/apis/get-product-certification-rule.md) |
| `get_recommend_attribute` | [references/apis/get-recommend-attribute.md](./references/apis/get-recommend-attribute.md) |
| `get_size_chart_detail` | [references/apis/get-size-chart-detail.md](./references/apis/get-size-chart-detail.md) |
| `get_size_chart_list` | [references/apis/get-size-chart-list.md](./references/apis/get-size-chart-list.md) |
| `get_ssp_info` | [references/apis/get-ssp-info.md](./references/apis/get-ssp-info.md) |
| `get_ssp_list` | [references/apis/get-ssp-list.md](./references/apis/get-ssp-list.md) |
| `get_variations` | [references/apis/get-variations.md](./references/apis/get-variations.md) |
| `get_vehicle_list_by_compatibility_detail` | [references/apis/get-vehicle-list-by-compatibility-detail.md](./references/apis/get-vehicle-list-by-compatibility-detail.md) |
| `get_weight_recommendation` | [references/apis/get-weight-recommendation.md](./references/apis/get-weight-recommendation.md) |
| `init_tier_variation` | [references/apis/init-tier-variation.md](./references/apis/init-tier-variation.md) |
| `link_ssp` | [references/apis/link-ssp.md](./references/apis/link-ssp.md) |
| `publish_item_to_outlet_shop` | [references/apis/publish-item-to-outlet-shop.md](./references/apis/publish-item-to-outlet-shop.md) |
| `register_brand` | [references/apis/register-brand.md](./references/apis/register-brand.md) |
| `reply_comment` | [references/apis/reply-comment.md](./references/apis/reply-comment.md) |
| `search_attribute_value_list` | [references/apis/search-attribute-value-list.md](./references/apis/search-attribute-value-list.md) |
| `search_item` | [references/apis/search-item.md](./references/apis/search-item.md) |
| `search_unpackaged_model_list` | [references/apis/search-unpackaged-model-list.md](./references/apis/search-unpackaged-model-list.md) |
| `unlink_ssp` | [references/apis/unlink-ssp.md](./references/apis/unlink-ssp.md) |
| `unlist_item` | [references/apis/unlist-item.md](./references/apis/unlist-item.md) |
| `update_item` | [references/apis/update-item.md](./references/apis/update-item.md) |
| `update_kit_item` | [references/apis/update-kit-item.md](./references/apis/update-kit-item.md) |
| `update_model` | [references/apis/update-model.md](./references/apis/update-model.md) |
| `update_price` | [references/apis/update-price.md](./references/apis/update-price.md) |
| `update_sip_item_price` | [references/apis/update-sip-item-price.md](./references/apis/update-sip-item-price.md) |
| `update_stock` | [references/apis/update-stock.md](./references/apis/update-stock.md) |
| `update_tier_variation` | [references/apis/update-tier-variation.md](./references/apis/update-tier-variation.md) |

模块总览 / Feedback 见 [references/api.md](./references/api.md)。

## Usage Scenarios

### 1. 查类目并上架
1. `get_category.py` 获取类目树
2. `get_attribute_tree.py` 传 `category_id` 获取必填属性
3. `add_item.py` 传完整 `body`（含 category_id、item_name、price、image、attribute_list 等）

### 2. 查商品与改库存
1. `get_item_list.py`：`offset`、`page_size`、`item_status`
2. `get_item_base_info.py`：`item_id_list`
3. `update_stock.py` / `update_price.py`：POST `body`

### 3. 上下架与推广
- `unlist_item.py`：批量上下架
- `boost_item.py`：置顶（最多 5 个）

## 调用原则

- 先看 **`developerProxy.httpStatus`**，再读 `*Response` 字段
- GET：业务参数放 JSON 顶层（runner 拼 queryString）
- POST：复杂接口传 `body`；简单接口可传顶层 body 字段或 `body`
- 每个脚本 docstring 含 **官方文档 URL**（`module=89`）

## Not Applicable

- 店铺授权 → `linkfox-shopee-store-auth`
- 商户信息 → `linkfox-shopee-store-merchant`
- 订单 → `linkfox-shopee-store-orders`
- 物流发货 → `linkfox-shopee-store-logistics`
- 退货退款 → `linkfox-shopee-store-returns`
- 站内广告 → `linkfox-shopee-store-ads`
- 支付结算 → `linkfox-shopee-store-payment`
- 联盟营销 AMS → `linkfox-shopee-store-ams`
- 店铺视频 → `linkfox-shopee-store-video`
- 店铺信息 → `linkfox-shopee-store-shop`
- 跨境全球商品 → `linkfox-shopee-store-global-product`
- 折扣促销 → `linkfox-shopee-store-discount`
- 套装优惠 Bundle Deal → `linkfox-shopee-store-bundle-deal`
- 加购优惠 Add-On Deal → `linkfox-shopee-store-add-on-deal`
- 店铺优惠券 Voucher → `linkfox-shopee-store-voucher`
- 店铺秒杀 Shop Flash Sale → `linkfox-shopee-store-shop-flash-sale`
- 关注有礼 Follow Prize → `linkfox-shopee-store-follow-prize`
- 精选商品 Top Picks → `linkfox-shopee-store-top-picks`
- 店铺分类 Shop Category → `linkfox-shopee-store-shop-category`
- 账户健康 Account Health → `linkfox-shopee-store-account-health`
- 跨站选品数据 → `linkfox-youying-shopee-product-search`
- 图片/视频上传（MediaSpace `api/v2/media_space/...`）→ `linkfox-shopee-store-media-space`
- 图片/视频上传（Media `api/v2/media/...`）→ `linkfox-shopee-store-media`

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
