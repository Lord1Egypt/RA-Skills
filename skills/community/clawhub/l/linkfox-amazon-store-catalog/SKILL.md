---
name: linkfox-amazon-store-catalog
description: 亚马逊商品目录（Catalog Items）查询。用于按 ASIN 获取目录详情，按关键词、标识符或分类条件搜索商品，以及查询商品类目节点、标题摘要、图片和其他 includedData。用户提到亚马逊商品目录、Catalog Items、ASIN 查商品、关键词搜亚马逊商品、类目节点、商品图片或摘要、searchCatalogItems、getCatalogItem、listCatalogCategories 时触发。即使未明确说“Catalog”，只要希望查询亚马逊全站目录中的商品基础资料而不是卖家自己的 Listing，也应触发此技能；卖家 SKU 的刊登增删改查使用 linkfox-amazon-store-listings。
---

# Amazon 店铺 Catalog Items

本 skill 与 **`linkfox-amazon-store-auth`** 等同属 **Amazon Store** 系列：依赖 **`linkfox-amazon-store-auth`** 选店（`sellerId`+`region`）；直接 **`POST /spApi/developerProxy`** 传入 `sellerId`+`region`，由服务端解析 token（勿传 `amzAccessToken`，除非兼容旧调用）。转发 **GET**。

## 调用方式

- **API 端点**：`POST /spApi/developerProxy`（不同操作通过请求体区分；完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/<脚本名>.py '<JSON 参数>' [--inline]`（可用脚本见上文脚本一览）
- **成本约束**：本工具会消耗算力；失败/空结果不得自动换关键词、翻页或连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-amazon-store-catalog-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
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

## 官方参考索引

| 能力 | 文档 |
|------|------|
| listCatalogCategories | [listCatalogCategories](https://developer-docs.amazon.com/sp-api/reference/listcatalogcategories) |
| searchCatalogItems | [searchCatalogItems](https://developer-docs.amazon.com/sp-api/reference/searchcatalogitems) |
| getCatalogItem | [getCatalogItem](https://developer-docs.amazon.com/sp-api/reference/getcatalogitem) |

---

## Prerequisites

1. 依赖 **`linkfox-amazon-store-auth`**；`python scripts/check_auth_dependency.py`，exit **42** 时需先安装授权 skill。
2. 应用需具备 **Catalog Items** 相关角色；`searchCatalogItems` 按 **identifiers+SKU** 检索时 query 须带 **`sellerId`**（脚本在 `identifiersType=SKU` 时自动使用入参 `sellerId`）。

---

## Current Capabilities

| 能力 | path | 脚本 |
|------|------|------|
| listCatalogCategories | `catalog/v0/categories` | `list_catalog_categories.py` |
| searchCatalogItems | `catalog/{2022-04-01\|2020-12-01}/items` | `search_catalog_items.py` |
| getCatalogItem | `catalog/{version}/items/{asin}` | `get_catalog_item.py` |

默认 Catalog Items 版本：**`2022-04-01`**；入参 **`catalogItemsVersion`** 可改为 **`2020-12-01`**。

共享模块：**`_spapi_catalog_common.py`**。

---

## Quick Parameters

- **listCatalogCategories**：`marketplaceId` + **`asin`** 或 **`sellerSku`**（二选一）。
- **searchCatalogItems**：`marketplaceIds` + **`keywords`** 或 **`identifiers` + `identifiersType`**（互斥）；可选 `includedData`、`brandNames`、`classificationIds`、`pageSize`、`pageToken`。
- **getCatalogItem**：`asin`、`marketplaceIds`；可选 `includedData`、`locale`。

---

## Scripts

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/list_catalog_categories.py '{"sellerId":"A1...","region":"NA","marketplaceId":"ATVPDKIKX0DER","asin":"B08N5WRWNW"}'

python scripts/search_catalog_items.py '{"sellerId":"A1...","region":"NA","marketplaceIds":["ATVPDKIKX0DER"],"keywords":["wireless mouse"]}'

python scripts/get_catalog_item.py '{"sellerId":"A1...","region":"NA","asin":"B08N5WRWNW","marketplaceIds":["ATVPDKIKX0DER"],"includedData":["summaries","images"]}'
```

---

## Display Rules

1. 先看 **`developerProxy.errcode` / `httpStatus`**，再读 **`categories`** / **`catalogItems`** / **`catalogItem`**。
2. **listCatalogCategories** 使用 v0 查询键 **`MarketplaceId`**（单数），与 search/get 的 **`marketplaceIds`** 不同。
3. 网关 path 白名单需包含 **`catalog/v0/`** 与 **`catalog/2022-04-01/`**（或 `2020-12-01`）。

---

## Important Limitations

- 本 skill 读的是 **Amazon 商品目录（Catalog）**，不是卖家订单；订单见 **`linkfox-amazon-store-orders`**。
- `includedData`、返回字段以 Amazon schema 为准，详见 **`references/api.md`**。

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

**Feedback：** `skillName`：`linkfox-amazon-store-catalog`。

---
*更多跨境 skill：[LinkFox Skills](https://skill.linkfox.com/)*

