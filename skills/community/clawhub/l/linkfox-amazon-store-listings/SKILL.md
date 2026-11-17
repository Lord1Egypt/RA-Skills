---
name: linkfox-amazon-store-listings
description: 亚马逊卖家 Listing 刊登与商品类型定义管理。用于按 SKU 查询或搜索 Listing，创建、全量更新、局部修改和删除刊登，检查 ASIN 刊登限制，并查询 product type 及其 JSON Schema 属性要求。用户提到亚马逊 Listing、刊登商品、修改商品信息、删除 Listing、卖家 SKU、ASIN 能否销售、刊登限制、product type、商品类型定义、JSON Schema、Listings Items、Listings Restrictions 时触发。即使未明确提及 API，只要希望管理卖家自己的商品刊登或确认上架所需字段与资格，也应触发此技能；查询亚马逊全站商品目录使用 linkfox-amazon-store-catalog，批量提交使用 linkfox-amazon-store-feeds。
---

# Amazon 店铺 Listings 与相关 API

本 skill 与 **`linkfox-amazon-store-auth`**、**`linkfox-amazon-store-report`** 同属 **Amazon Store** 系列：依赖 **`linkfox-amazon-store-auth`** 选店（`sellerId`+`region`）；直接 **`POST /spApi/developerProxy`** 传入 `sellerId`+`region`，由服务端解析 token（勿传 `amzAccessToken`，除非兼容旧调用）。转发上游 **GET**、**PATCH**、**PUT** 或 **DELETE**。

| 操作 | 官方参考 |
|------|----------|
| 单条刊登 | [getListingsItem](https://developer-docs.amazon.com/sp-api/reference/getlistingsitem) |
| 检索列表 | [searchListingsItems](https://developer-docs.amazon.com/sp-api/reference/searchlistingsitems) |
| 部分更新刊登 | [patchListingsItem](https://developer-docs.amazon.com/sp-api/reference/patchlistingsitem) |
| 创建 / 全量更新刊登 | [putListingsItem](https://developer-docs.amazon.com/sp-api/reference/putlistingsitem) |
| 删除刊登 | [deleteListingsItem](https://developer-docs.amazon.com/sp-api/reference/deletelistingsitem) |
| 刊登限制（ASIN） | [getListingsRestrictions](https://developer-docs.amazon.com/sp-api/reference/getlistingsrestrictions) |
| 搜索 product type | [searchDefinitionsProductTypes](https://developer-docs.amazon.com/sp-api/reference/searchdefinitionsproducttypes) |
| 获取 product type 定义 | [getDefinitionsProductType](https://developer-docs.amazon.com/sp-api/reference/getdefinitionsproducttype) |

---

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

---

## Prerequisites（必须先读）

本 skill **依赖** **`linkfox-amazon-store-auth`**。流程与 `linkfox-amazon-store-report` 相同：

1. 运行 `python scripts/check_auth_dependency.py`；若 exit code **42** 且 stderr 含 `DEPENDENCY_MISSING:`，请先安装 **`linkfox-amazon-store-auth`**。
2. **不要**在本 skill 内绕过依赖实现授权或令牌逻辑。

---

## Current Capabilities

| 能力 | Path 要点 | 脚本 |
|------|-----------|------|
| **获取单条 Listing** | `listings/2021-08-01/items/{sellerId}/{sku}` + Query | `scripts/get_listings_item.py` |
| **搜索刊登列表** | `listings/2021-08-01/items/{sellerId}` + Query（**无**路径尾段 SKU） | `scripts/search_listings_items.py` |
| **部分更新 Listing（PATCH）** | 同 **get** 路径 + Query + JSON body | `scripts/patch_listings_item.py` |
| **创建 / 全量更新 Listing（PUT）** | 同 **get** 路径 + Query + body；**marketplaceIds 仅 1 个** | `scripts/put_listings_item.py` |
| **删除 Listing（DELETE）** | 同 **get** 路径 + Query（**marketplaceIds 仅 1 个**） | `scripts/delete_listings_item.py` |
| **刊登限制** | `listings/2021-08-01/restrictions` + Query（asin、sellerId、marketplaceIds 等） | `scripts/get_listings_restrictions.py` |
| **搜索 Product Type** | `definitions/2020-09-01/productTypes` + Query | `scripts/search_definitions_product_types.py` |
| **获取 Product Type 定义** | `definitions/2020-09-01/productTypes/{productType}` + Query；**marketplaceIds 仅 1 个** | `scripts/get_definitions_product_type.py` |

**searchListingsItems** 下 `identifiers` / `variationParentSku` / `packageHierarchySku` **三者互斥**（仅该接口；见 **`references/api.md`**）。**searchDefinitionsProductTypes** 下 **`keywords`** 与 **`itemName`** **互斥**。

---

## Quick Parameters

### getListingsItem（单条）

| 字段 | 必填 | 说明 |
|------|------|------|
| sellerId | 是 | 已授权 Seller ID |
| region | 是 | `NA` / `EU` / `FE` |
| sku | 是 | **卖家 SKU**（非 ASIN） |
| marketplaceIds | 是 | 建议仅 **一个** marketplace id |
| includedData / issueLocale | 否 | 见 `references/api.md` |

### searchListingsItems（列表）

| 字段 | 必填 | 说明 |
|------|------|------|
| sellerId | 是 | 已授权 Seller ID |
| region | 是 | `NA` / `EU` / `FE` |
| marketplaceIds | 是 | 建议仅 **一个** marketplace id |
| identifiers + identifiersType | 否 | 最多 **20** 个；与 `variationParentSku`、`packageHierarchySku` **不能同用** |
| variationParentSku / packageHierarchySku | 否 | 与 identifiers **互斥** |
| 时间窗 / 状态 / 排序 / 分页 | 否 | `createdAfter`、`lastUpdatedBefore`、`withStatus`、`sortBy`、`pageSize`（≤20）、`pageToken` 等，见 **`references/api.md`** |

### patchListingsItem（部分更新）

| 字段 | 必填 | 说明 |
|------|------|------|
| sellerId | 是 | 已授权 Seller ID |
| region | 是 | `NA` / `EU` / `FE` |
| sku | 是 | **卖家 SKU** |
| marketplaceIds | 是 | 数组或逗号字符串；脚本拼入 Query |
| productType | 是 | Amazon product type |
| patches | 是 | **至少 1 条** JSON Patch（`op`、`path` 等） |
| includedData / mode / issueLocale | 否 | 见 **`references/api.md`** |

### putListingsItem（创建 / 全量更新）

| 字段 | 必填 | 说明 |
|------|------|------|
| sellerId | 是 | 已授权 Seller ID |
| region | 是 | `NA` / `EU` / `FE` |
| sku | 是 | **卖家 SKU** |
| marketplaceIds | 是 | **恰好一个** marketplace id |
| productType | 是 | Amazon product type |
| requirements | 是 | `LISTING` \| `LISTING_PRODUCT_ONLY` \| `LISTING_OFFER_ONLY` |
| attributes | 是 | 须符合该 product type schema |
| includedData / mode / issueLocale | 否 | 见 **`references/api.md`** |

### deleteListingsItem（删除）

| 字段 | 必填 | 说明 |
|------|------|------|
| sellerId | 是 | 已授权 Seller ID |
| region | 是 | `NA` / `EU` / `FE` |
| sku | 是 | **卖家 SKU** |
| marketplaceIds | 是 | **恰好一个** marketplace id |
| issueLocale | 否 | 见 **`references/api.md`** |

### getListingsRestrictions

| 字段 | 必填 | 说明 |
|------|------|------|
| sellerId | 是 | 用于 `storeTokens` 与 Query |
| region | 是 | `NA` / `EU` / `FE` |
| asin | 是 | 目录 ASIN |
| marketplaceIds | 是 | 数组或逗号字符串 |
| conditionType / reasonLocale | 否 | 见 **`references/api.md`** |

### searchDefinitionsProductTypes

| 字段 | 必填 | 说明 |
|------|------|------|
| sellerId | 是 | 用于 `storeTokens` |
| region | 是 | `NA` / `EU` / `FE` |
| marketplaceIds | 是 | 数组或逗号字符串 |
| keywords **或** itemName | 否 | **二者不可同时传**（非空时互斥） |
| locale / searchLocale | 否 | 见 **`references/api.md`** |

### getDefinitionsProductType

| 字段 | 必填 | 说明 |
|------|------|------|
| sellerId | 是 | 用于 `storeTokens` |
| region | 是 | `NA` / `EU` / `FE` |
| productType | 是 | 如 `LUGGAGE`（写入 path） |
| marketplaceIds | 是 | **恰好一个** id |
| querySellerId | 否 | 若需上游 Query **`sellerId`**（卖家专属 schema），传入；常与 `sellerId` 相同 |
| productTypeVersion / requirements / requirementsEnforced / locale | 否 | 见 **`references/api.md`** |

---

## Scripts

- **`scripts/get_listings_item.py`** — 单条 listing。
- **`scripts/search_listings_items.py`** — 搜索列表。
- **`scripts/patch_listings_item.py`** — PATCH 部分更新。
- **`scripts/put_listings_item.py`** — PUT 创建或全量更新。
- **`scripts/delete_listings_item.py`** — DELETE 删除刊登。
- **`scripts/get_listings_restrictions.py`** — GET 刊登限制。
- **`scripts/search_definitions_product_types.py`** — GET 搜索 product type。
- **`scripts/get_definitions_product_type.py`** — GET product type JSON Schema。
- **`scripts/check_auth_dependency.py`** — 依赖检测。

示例：

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/get_listings_item.py '{"sellerId":"A1...","region":"NA","sku":"MY-SKU","marketplaceIds":["ATVPDKIKX0DER"]}'

python scripts/search_listings_items.py '{"sellerId":"A1...","region":"NA","marketplaceIds":["ATVPDKIKX0DER"],"identifiers":["B0XXXXXXXX"],"identifiersType":"ASIN"}'

python scripts/patch_listings_item.py '{"sellerId":"A1...","region":"NA","sku":"MY-SKU","marketplaceIds":["ATVPDKIKX0DER"],"productType":"LUGGAGE","patches":[{"op":"replace","path":"/attributes/item_name","value":[{"value":"New Title","marketplace_id":"ATVPDKIKX0DER"}]}]}'

python scripts/put_listings_item.py '{"sellerId":"A1...","region":"NA","sku":"MY-SKU","marketplaceIds":["ATVPDKIKX0DER"],"productType":"LUGGAGE","requirements":"LISTING","attributes":{"item_name":[{"value":"Title","marketplace_id":"ATVPDKIKX0DER"}]}}'

python scripts/delete_listings_item.py '{"sellerId":"A1...","region":"NA","sku":"MY-SKU","marketplaceIds":["ATVPDKIKX0DER"]}'

python scripts/get_listings_restrictions.py '{"sellerId":"A1...","region":"NA","asin":"B0XXXXXXXX","marketplaceIds":["ATVPDKIKX0DER"]}'

python scripts/search_definitions_product_types.py '{"sellerId":"A1...","region":"NA","marketplaceIds":["ATVPDKIKX0DER"],"keywords":["luggage"]}'

python scripts/get_definitions_product_type.py '{"sellerId":"A1...","region":"NA","productType":"LUGGAGE","marketplaceIds":["ATVPDKIKX0DER"],"querySellerId":"A1..."}'
```

---

## Display Rules

1. **items** 类接口：路径含 **卖家 SKU** 时强调非 ASIN；**searchListingsItems** 路径仅到 `sellerId`。
2. 展示网关结果时说明 **`errcode` / `httpStatus`**；成功后再解析 `body`（`listing` / `searchResult` / `patchResult` / `putResult` / `deleteResult` / **`restrictionsResult`** / **`productTypesSearchResult`** / **`productTypeDefinitionResult`**）。
3. **searchListingsItems** 多页：从 `searchResult` 取下一页 token（字段名以 Amazon 响应为准），传入 `pageToken`。
4. **restrictions** / **definitions** 路径与 **items** 不同；**1005** 时需为 **`listings/2021-08-01/restrictions`** 与 **`definitions/2020-09-01/productTypes`** 等前缀分别配置白名单（以运维为准）。
5. **patch** / **put** / **delete** 为写操作；**delete** 须谨慎；**put** 为全量 **`attributes`**；**patch** 仅顶层属性可 patch（以官方为准）。

---

## Important Limitations

- **marketplaceIds**：**get** / **searchListingsItems** 脚本对多 id 常仅取第一个；**put** / **delete** / **getDefinitionsProductType** 多于 1 个即报错；**patch**、**restrictions**、**searchDefinitionsProductTypes** 行为见 **`references/api.md`**。
- **searchListingsItems**：`pageSize` **≤ 20**；`identifiers` **≤ 20**。
- **patch**：`patches` 至少 1 条；JSON Patch 的 **`delete`** 与 **deleteListingsItem** 接口不同；Vendor 对部分 patch 可能 **400**。
- **put**：**LISTING_OFFER_ONLY** 对 Vendor **400**。
- **白名单**：`listings/.../items`、`listings/.../restrictions`、`definitions/2020-09-01/productTypes` 均须按需放行。

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

**Feedback：** 见 `references/api.md` 中 Feedback API，`skillName`：`linkfox-amazon-store-listings`。

---
*更多跨境 skill：[LinkFox Skills](https://skill.linkfox.com/)*
