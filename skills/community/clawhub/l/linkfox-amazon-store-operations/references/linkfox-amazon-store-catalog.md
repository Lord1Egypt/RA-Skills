---
name: linkfox-amazon-store-catalog
description: 亚马逊店铺商品目录检索。支持按 ASIN、关键词查询商品目录、类目节点、商品图片及摘要等信息。
---

# 亚马逊店铺商品目录（Catalog Items）

本 skill 查询亚马逊店铺商品目录（Catalog），与 `linkfox-amazon-store-auth` 等同属 Amazon Store 系列：先 `POST /spApi/storeTokens`，再 `POST /spApi/developerProxy` 转发 GET。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- **listCatalogCategories**（v0）：按 `asin` 或 `sellerSku` 查询某商品所属的类目节点。
- **searchCatalogItems**（`2022-04-01` 默认 / `2020-12-01`）：按 `keywords` 或 `identifiers + identifiersType` 检索商品目录，可附带 `includedData`（summaries/images/attributes/salesRanks 等）。
- **getCatalogItem**（`2022-04-01` 默认 / `2020-12-01`）：按 `asin` 获取单个商品目录详情。
- 支持通过 `catalogItemsVersion` 切换 Catalog Items API 版本。

### ❌ 边界与限制

- **前置依赖**：依赖 `linkfox-amazon-store-auth`；运行 `python scripts/check_auth_dependency.py`，exit **42** 时需先安装授权 skill。
- **权限要求**：应用需具备 Catalog Items 相关角色；`searchCatalogItems` 按 `identifiers+SKU` 检索时 query 须带 `sellerId`（脚本在 `identifiersType=SKU` 时自动使用入参 `sellerId`）。
- **网关白名单**：path 白名单需包含 `catalog/v0/` 与 `catalog/2022-04-01/`（或 `2020-12-01`）。
- **数据口径**：本 skill 读的是 Amazon 商品目录（Catalog），**不是卖家订单**；订单见 `linkfox-amazon-store-orders`。
- **字段定义**：`includedData` 及返回字段以 Amazon schema 为准，详见 `references/api.md`。
- **成本约束**：本工具消耗积分；失败/空结果不得自动换关键词、翻页或连续试探；需要继续检索时先向用户说明会产生额外消耗。

## 调用方式

- **API 端点**：`POST /spApi/developerProxy`（不同操作通过请求体区分；完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/<脚本名>.py '<JSON 参数>' [--inline]`
- **默认 Catalog Items 版本**：`2022-04-01`；入参 `catalogItemsVersion` 可改为 `2020-12-01`。
- **共享模块**：`_spapi_catalog_common.py`。

**输出策略（脚本默认行为）**：
- 始终将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-amazon-store-catalog-<timestamp>.json`（`<session>` 取自环境变量 `SESSION_ID`；禁止写入 /tmp，当前目录不可写则报错）。
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout。
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）。
- 加 `--inline` 强制全量打印到 stdout（同样落盘）。

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

### 官方参考索引

| 能力 | 文档 |
|------|------|
| listCatalogCategories | [listCatalogCategories](https://developer-docs.amazon.com/sp-api/reference/listcatalogcategories) |
| searchCatalogItems | [searchCatalogItems](https://developer-docs.amazon.com/sp-api/reference/searchcatalogitems) |
| getCatalogItem | [getCatalogItem](https://developer-docs.amazon.com/sp-api/reference/getcatalogitem) |

## 使用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/list_catalog_categories.py '{"sellerId":"A1...","region":"NA","marketplaceId":"ATVPDKIKX0DER","asin":"B08N5WRWNW"}'

python scripts/search_catalog_items.py '{"sellerId":"A1...","region":"NA","marketplaceIds":["ATVPDKIKX0DER"],"keywords":["wireless mouse"]}'

python scripts/get_catalog_item.py '{"sellerId":"A1...","region":"NA","asin":"B08N5WRWNW","marketplaceIds":["ATVPDKIKX0DER"],"includedData":["summaries","images"]}'
```

## 展示规则

1. 先看 `developerProxy.errcode` / `httpStatus`，再读 `categories` / `catalogItems` / `catalogItem`。
2. **listCatalogCategories** 使用 v0 查询键 `MarketplaceId`（单数），与 search/get 的 `marketplaceIds` 不同。
3. 网关 path 白名单需包含 `catalog/v0/` 与 `catalog/2022-04-01/`（或 `2020-12-01`）。
4. 仅呈现数据，不做主观商业建议。

## 用户表达与场景速查

**适用** —— 亚马逊商品目录检索：

| 用户说 | 场景 |
|--------|------|
| "查这个 ASIN 的目录信息"、"按 ASIN 查商品" | getCatalogItem |
| "用关键词搜亚马逊商品目录" | searchCatalogItems（keywords） |
| "查这几个 ASIN/EAN 的目录" | searchCatalogItems（identifiers） |
| "这个 ASIN 属于哪些类目" | listCatalogCategories |
| "查商品图片、摘要、销售排名" | getCatalogItem + includedData |

不适用场景见上方【能力边界】。

## 解决认证和积分问题
发生以下异常情况时，采用以下措施来处理：

### 异常情况
- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示积分或余额不足**：消息含"积分余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

### 措施
- 优先采用skill内的 onboarding.md 引导解决问题。
- 如找不到 onboarding.md 文件，则加载 /linkfox-onboarding 这个skill并根据它的引导来处理。如未安装请先安装：
    - 下载 https://agent-files.linkfox.com/skills/linkfox-onboarding/release.zip，解压后安装这个skill。

---

# 亚马逊店铺商品目录 API 参考

经 **LinkFox** `storeTokens` + `developerProxy` 调用 SP-API **Catalog Items**（与 listings / pricing 系列相同）。

环境变量：`LINKFOX_AGENT_API_KEY`（或 `LINKFOXAGENT_API_KEY`）（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）；可选 `LINKFOX_TOOL_GATEWAY`（回退 `STORE_API_BASE_URL` / `SPAPI_BASE_URL`，默认 `https://tool-gateway.linkfox.com`）。

---

## 1. 脚本与路径

| 脚本 | 方法 | 路径 |
|------|--------|------|
| `list_catalog_categories.py` | GET | `catalog/v0/categories` |
| `search_catalog_items.py` | GET | `catalog/2022-04-01/items`（默认） |
| `get_catalog_item.py` | GET | `catalog/2022-04-01/items/{asin}`（默认） |

`catalogItemsVersion` 可选 **`2020-12-01`**，path 中版本段随之替换。

---

## 2. listCatalogCategories（v0）

### 入参（JSON）

| 字段 | 必填 | 说明 |
|------|------|------|
| sellerId, region | 是 | 店铺与区域 |
| marketplaceId / marketplaceIds | 是 | 仅使用**第一个**站点 ID → query **`MarketplaceId`** |
| asin / ASIN | 条件 | 与 sellerSku **二选一** |
| sellerSku / SellerSKU | 条件 | 与 asin **二选一** |

### 查询参数（大小写敏感）

- `MarketplaceId`
- `ASIN` 或 `SellerSKU`

解析字段：**`categories`**

---

## 3. searchCatalogItems

### 入参

| 字段 | 必填 | 说明 |
|------|------|------|
| marketplaceIds | 是 | 文档通常 ≤1 个 |
| keywords | 条件 | 与 identifiers **互斥**，最多 20 个 |
| identifiers | 条件 | 最多 20 个；须配 **identifiersType** |
| identifiersType | 条件 | ASIN, EAN, GTIN, ISBN, JAN, MINSAN, SKU, UPC |
| includedData | 否 | summaries, images, attributes, salesRanks 等 |
| brandNames, classificationIds | 否 | 限缩关键词搜索 |
| locale, keywordsLocale | 否 | |
| pageSize | 否 | 1～20，默认 10 |
| pageToken | 否 | 分页 |
| catalogItemsVersion | 否 | `2022-04-01`（默认）或 `2020-12-01` |
| sellerIdForCatalog | 否 | 覆盖 query 中的 sellerId（默认用 sellerId） |

当 **identifiersType=SKU** 时，Amazon 要求 query 带 **sellerId**；脚本默认使用 JSON 里的 **sellerId**。

解析字段：**`catalogItems`**

---

## 4. getCatalogItem

| 字段 | 必填 | 说明 |
|------|------|------|
| asin | 是 | path 段 |
| marketplaceIds | 是 | |
| includedData | 否 | |
| locale | 否 | |
| catalogItemsVersion | 否 | |

解析字段：**`catalogItem`**

---

## 5. includedData 示例（2022-04-01）

`summaries`, `attributes`, `classifications`, `dimensions`, `identifiers`, `images`, `productTypes`, `relationships`, `salesRanks`, `vendorDetails`（以官方为准）。

---

## 6. 错误与白名单

- **401**：HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。
- **402**：HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。
- **403**：Catalog Items 权限不足。
- **1005**（网关）：需放行 `catalog/v0/`、`catalog/2020-12-01/`、`catalog/2022-04-01/`。
- **429**：按官方 usage plan 降频。
