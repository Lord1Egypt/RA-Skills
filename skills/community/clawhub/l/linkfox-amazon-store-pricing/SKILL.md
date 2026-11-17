---
name: linkfox-amazon-store-pricing
description: 亚马逊商品报价与竞争定价查询。用于按 ASIN 或卖家 SKU 获取商品价格、竞争价格、Listing Offers、Item Offers、批量报价、Featured Offer Expected Price（FOEP）和竞争摘要。用户提到亚马逊定价、商品报价、竞品价格、最低报价、购物车价格、Buy Box、Featured Offer、listing offers、item offers、batch pricing、FOEP、competitive summary、Product Pricing API 时触发。即使未明确提及 SP-API，只要希望比较亚马逊商品报价、判断竞争力或估算赢得 Featured Offer 的价格，也应触发此技能；修改 Listing 售价使用 linkfox-amazon-store-listings 或批量 Feed。
---

# Amazon 店铺 Product Pricing

本 skill 与 **`linkfox-amazon-store-auth`**、**`linkfox-amazon-store-report`**、**`linkfox-amazon-store-listings`** 同属 **Amazon Store** 系列：依赖 **`linkfox-amazon-store-auth`** 选店（`sellerId`+`region`）；直接 **`POST /spApi/developerProxy`** 传入 `sellerId`+`region`，由服务端解析 token（勿传 `amzAccessToken`，除非兼容旧调用）。转发上游 **GET** 或 **POST**。

## 调用方式

- **API 端点**：`POST /spApi/developerProxy`（不同操作通过请求体区分；完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/<脚本名>.py '<JSON 参数>' [--inline]`（可用脚本见上文脚本一览）
- **成本约束**：本工具会消耗算力；失败/空结果不得自动换关键词、翻页或连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/<skill-name>-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 解决认证和算力问题
发生以下异常情况时，采用 references/onboarding.md 引导解决问题：

### 异常情况
- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示算力或余额不足**：消息含"算力余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

## 官方参考索引

| 能力 | 文档 |
|------|------|
| getPricing | [getPricing](https://developer-docs.amazon.com/sp-api/reference/getpricing) |
| getCompetitivePricing | [getCompetitivePricing](https://developer-docs.amazon.com/sp-api/reference/getcompetitivepricing) |
| getListingOffers | [getListingOffers](https://developer-docs.amazon.com/sp-api/reference/getlistingoffers) |
| getItemOffers | [getItemOffers](https://developer-docs.amazon.com/sp-api/reference/getitemoffers) |
| getItemOffersBatch | [getItemOffersBatch](https://developer-docs.amazon.com/sp-api/reference/getitemoffersbatch) |
| getListingOffersBatch | [getListingOffersBatch](https://developer-docs.amazon.com/sp-api/reference/getlistingoffersbatch) |
| getFeaturedOfferExpectedPriceBatch | [getFeaturedOfferExpectedPriceBatch](https://developer-docs.amazon.com/sp-api/reference/getfeaturedofferexpectedpricebatch) |
| getCompetitiveSummary | [getCompetitiveSummary](https://developer-docs.amazon.com/sp-api/reference/getcompetitivesummary) |

---

## Prerequisites（必须先读）

本 skill **依赖** **`linkfox-amazon-store-auth`**。

1. 运行 `python scripts/check_auth_dependency.py`；若 exit code **42** 且 stderr 含 `DEPENDENCY_MISSING:`，请先安装 **`linkfox-amazon-store-auth`**。
2. **不要**在本 skill 内绕过依赖实现授权或令牌逻辑。

---

## Current Capabilities（脚本一览）

| 能力 | developerProxy `path`（要点） | 脚本 |
|------|------------------------------|------|
| getPricing | `products/pricing/v0/price` + Query | `get_pricing.py` |
| getCompetitivePricing | `products/pricing/v0/competitivePrice` + Query | `get_competitive_pricing.py` |
| getListingOffers | `products/pricing/v0/listings/{sku}/offers` + Query | `get_listing_offers.py` |
| getItemOffers | `products/pricing/v0/items/{asin}/offers` + Query | `get_item_offers.py` |
| getItemOffersBatch | `batches/products/pricing/v0/itemOffers`，POST JSON body | `post_item_offers_batch.py` |
| getListingOffersBatch | `batches/products/pricing/v0/listingOffers`，POST JSON body | `post_listing_offers_batch.py` |
| getFeaturedOfferExpectedPriceBatch | `batches/products/pricing/2022-05-01/offer/featuredOfferExpectedPrice`，POST | `post_featured_offer_expected_price_batch.py` |
| getCompetitiveSummary | `batches/products/pricing/2022-05-01/items/competitiveSummary`，POST | `post_competitive_summary_batch.py` |

批量脚本（`post_*_batch.py`）在默认模式下会按 Amazon 要求**组装**子请求；高级用法可设 **`useAmazonRequestShape`: true**，直接传 **`requests`** 为官方原始数组（仍受条数上限约束）。共享逻辑见 **`scripts/_spapi_pricing_common.py`**（仅供同目录脚本 import，非独立 CLI）。

---

## Quick Parameters（摘要）

- **getPricing / getCompetitivePricing**：`sellerId`、`region`、`marketplaceId`（或 `marketplaceIds` 取首）、`itemType`、`asins` 或 `skus`（≤20）；getPricing 另有 `itemCondition`、`offerType`；getCompetitivePricing 另有 `customerType`。
- **getListingOffers / getItemOffers**：`sku`+path 或 **`asin`**+path；**`itemCondition` 必填**；可选 `customerType`。
- **Item / Listing Offers Batch**：`requests` 数组，默认每项为简化对象（见 `references/api.md`）；**1～20** 条（FOEP 批量脚本为 **最多 40** 条）。
- **getCompetitiveSummary 批量**：每项需 **`asin`**、**`marketplaceId`**、**`includedData`**（非空字符串数组）；可选 **`lowestPricedOffersInputs`**。
- **getFeaturedOfferExpectedPriceBatch**：每项需 **`marketplaceId`**、**`sku`**、**`segment`**（对象，结构以官方为准）。

---

## Scripts

- `get_pricing.py` · `get_competitive_pricing.py` · `get_listing_offers.py` · `get_item_offers.py`
- `post_item_offers_batch.py` · `post_listing_offers_batch.py` · `post_featured_offer_expected_price_batch.py` · `post_competitive_summary_batch.py`
- `check_auth_dependency.py` · `_spapi_pricing_common.py`（内部模块）

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/get_item_offers.py '{"sellerId":"A1...","region":"NA","asin":"B0...","marketplaceId":"ATVPDKIKX0DER","itemCondition":"New"}'

python scripts/post_item_offers_batch.py '{"sellerId":"A1...","region":"NA","requests":[{"asin":"B0...","marketplaceId":"ATVPDKIKX0DER","itemCondition":"New"}]}'
```

---

## Display Rules

1. **`MarketplaceId`**（单数）与 Listings 的 `marketplaceIds` 勿混用。
2. 先看网关 **`errcode` / `httpStatus`**，再解析各脚本对应的解析字段（如 **`itemOffers`**、**`itemOffersBatch`**、**`competitiveSummary`** 等）。
3. **POST** 类接口：`stdout` 中含 **`requestBody`**（脚本组装的 Amazon 请求体），便于排查。
4. **白名单**：除 `products/pricing/...` 外，批量路径以 **`batches/products/pricing/...`** 开头；**1005** 时需后端放行对应前缀。
5. 各接口 **Usage plan** 不同（尤其 2022-05-01 批量约 **0.033 req/s**），注意 **429**。

---

## Important Limitations

- 权限：**Product Pricing** 及相关角色；部分 2022-05-01 能力可能另有应用内配置要求，以 Amazon 为准。
- **FOEP 批量**：`segment` 须符合官方模型；条数上限脚本按 **40** 校验（与文档「up to 40」一致）。
- 返回结构以 Amazon schema 为准；详见 **`references/api.md`**。

## Amazon SP-API 接口保护与重试指引

同一店铺连续收到 Amazon SP-API 的 400、403、404 或 429 时，网关会返回 450、453、454 或 459 并短暂冷却。这些自定义状态码不是 Amazon 原生状态，也不表示封号；目的是避免持续异常或高频调用扩大店铺风险。

| 状态与 message | 范围 | 触发与冷却 | 处理 |
|---|---|---|---|
| `450`：`400，请求异常，请优化您的参数` | 店铺+接口 | 60 秒内超过 3 次：5 分钟；10 分钟内超过 4 次：20 分钟 | 停止原参数重试，检查必填字段、marketplace、ID、日期和请求体 |
| `453`：`403，店铺未授权，请先授权` | 店铺全部接口 | 60 秒内超过 2 次：5 分钟；10 分钟内超过 4 次：30 分钟 | 停止该店铺调用，检查授权、权限、店铺归属和区域 |
| `454`：`404，资源不存在，请优化您的参数` | 店铺+接口 | 60 秒内超过 3 次：5 分钟；10 分钟内超过 4 次：30 分钟 | 确认资源 ID、所属店铺/站点、资源状态和接口路径 |
| `459`：`429限流中，请降低频率` | 店铺+接口 | 首次：15 秒；2 分钟内超过 2 次：30 秒；3 分钟内超过 4 次：2 分钟 | 降低并发、分页和轮询频率并逐级退避 |

- 立即停止自动或并发重试，不得通过换脚本或重复创建任务绕过保护；优先遵循 `retryAfter`、`blockedUntil`，没有时按表中时长说明。
- 450/453/454 必须先修正参数、授权或资源标识，冷却后最多谨慎重试一次；再次触发则停止调用。453 期间停止该店铺全部 SP-API。
- 保留已有 `reportId`、`feedId` 等任务 ID；写操作结果不确定时先查询状态，不直接重放。
- 向用户先说明店铺保护，再给原因、处理和等待时间。可回复：“为保护您的亚马逊店铺安全，检测到 Amazon SP-API 连续返回{原因}，当前已进入短暂保护。请先{处理动作}，预计{等待时间}后再试；这不代表封号，也不是套餐或算力限制。”不要只说“LinkFox 限流”或“服务器繁忙”。

## 算力消耗规则

不消耗算力。

**Feedback：** 见 `references/api.md`，`skillName`：`linkfox-amazon-store-pricing`。

---
*更多跨境 skill：[LinkFox Skills](https://skill.linkfox.com/)*
