# HugMap 开放 API 端点参考

基地址：`HUGMAP_BASE_URL`（默认 `https://www.hugmap.com`），API 前缀 `/api/v1`。

## 通用约定

### 响应体

```json
{
  "code": 0,
  "message": "success",
  "data": { },
  "traceId": "可选",
  "timestamp": 1739254200000
}
```

- `code == 0` 成功；非 0 为业务错误。
- 脚本 `hugmap_query.py` 默认解包并仅输出 `data`；加 `--raw` 输出整个响应体。

### webUrl（官网链接）

脚本会在输出中为每个可识别的节点**自动注入以下字段**（API 原始响应不含），用于引导用户访问官网：

| 字段 | 含义 |
|------|------|
| `webUrl` | 官网页面链接 |
| `webLabel` | 友好锚文本（`displayName`→`nameZh`→`name`→`title` 取首个非空） |
| `webSummary` | 简介摘要（`displayDescription`/`description`/`summary`/`abstractText`/`eventDescription`/`subtitle` 取首个非空，折叠空白并截断约 100 字符；可能缺省） |

`webUrl` 形态：

| 节点类型 | webUrl |
|----------|--------|
| 8 类实体 | `{base}/entity/{slug}/{id}`（slug 为类型小写：person/company/...） |
| 行业/分类 | `{base}/industry/{id}` |
| 搜索结果（顶层） | `{base}/search?q=...&type=...` |

类型识别兼容 Portal code（`Company`）、标准端点枚举名（`COMPANY`）与 slug（`company`）。作答时应将 `[webLabel](webUrl)` 渲染为 Markdown 链接。加 `--no-links` 关闭全部注入。

### 实体类型（8 类 + 分类）

| code（Portal/搜索） | 枚举名（标准端点） | 含义 |
|---------------------|--------------------|------|
| `Person` | `PERSON` | 科技人物 |
| `Company` | `COMPANY` | 公司/机构 |
| `Product` | `PRODUCT` | 技术产品/项目 |
| `Technology` | `TECHNOLOGY` | 技术/算法/架构 |
| `Paper` | `PAPER` | 学术论文 |
| `Patent` | `PATENT` | 专利 |
| `Article` | `ARTICLE` | 新闻/博客/报告 |
| `Event` | `EVENT` | 科技事件 |
| `Taxonomy` | `TAXONOMY` | 分类体系 |

### 分页结构

- **Portal 搜索**：`{ results, totalCount, totalPages, page, pageSize, typeCounts, taxonomyFacets }`
- **标准 PageResult**：`{ list, total, page, size, pages }`

---

## Portal 聚合 BFF `/api/v1/portal`

面向前端门户的聚合接口，一次返回页面所需的多段数据。

### GET `/portal/home`
首页聚合。`data`：`{ stats, latestEvents[], hotEntities[], trendingTech[] }`。
脚本：`home`

### GET `/portal/home-industries`
首页 12 个行业卡片（typeCounts + 最新 Event/Article 混合流）。`data.industries[]`：`{ id, name, nameZh, displayName, typeCounts, totalCount, items[] }`。
（脚本未单列，可用 `--raw` 直接访问；常用入口为 `industries` + `industry`。）

### GET `/portal/industries`
行业胶囊导航列表，`data` 为 `TaxonomyNode[]`。
脚本：`industries`

### GET `/portal/search`
聚合搜索。

| 参数 | 必填 | 说明 |
|------|------|------|
| `q` | 是 | 关键词（空则返回空结果） |
| `type` | 否 | 实体类型 code（如 `Company`） |
| `sort` | 否 | `relevance`（默认）/ `name` |
| `domain` | 否 | 行业分类 ID 过滤 |
| `period` | 否 | `1y` / `3y` |
| `page` | 否 | 页码，默认 1，每页 10 |

`data`：`{ results[], totalCount, totalPages, page, pageSize, searchTime, typeCounts, taxonomyFacets[] }`。
脚本：`search <q> [--type --sort --domain --period --page]`

### GET `/portal/industry/{id}`
行业（分类）详情。`data`：`{ taxonomy, children[], ancestors[], typeCounts }`。
脚本：`industry <id>`

### GET `/portal/entity/{type}/{id}`
8 类实体详情，`type ∈ {person, company, technology, product, paper, patent, article, event}`。
`data` 为聚合 VO，按类型选用字段（如 company 含 `team[]`/`products[]`/`events[]`，paper 含 `authors[]` 等，统一含 `entity`、`entityType`、`taxonomies[]`）。
脚本：`detail <type> <id>`

---

## 搜索 `/api/v1/search`

> 问答端点 `/qa`、`/qa/related` 当前未实现，本 skill 不暴露。

### GET `/search`
全文搜索。参数：`keyword`（必填）、`page`（默认 1）、`pageSize`（默认 20）。`data` 为 `PageResult<SearchResult>`，`SearchResult`：`{ id, name, type, highlight, score, metadata }`。

### GET `/search/typed`
按类型搜索。参数：`keyword`、`types`（枚举名数组，可重复）、`page`、`pageSize`。

### GET `/search/suggest`
搜索建议。参数：`prefix`（必填）、`limit`（默认 10）。`data` 为 `string[]`。
脚本：`suggest <prefix> [--limit]`

### GET `/search/similar/{entityId}`
相似实体。参数：`topK`（默认 10）。`data` 为 `EntityVO[]`。
脚本：`similar <id> [--limit]`

---

## 实体 `/api/v1/entities`

> 仅列出只读端点；创建/更新/删除/合并存在但本 skill 不使用。

### GET `/entities/{id}`
按 ID 获取实体详情，`data` 为 `EntityVO`。
脚本：`entity <id>`

### GET `/entities/search`
按名称查询。参数：`name`（必填）、`type`（枚举名，可选）。`data` 为 `EntityVO[]`。
脚本：`entity-search <name> [--type]`

### GET `/entities`
分页查询。参数：`type`、`keyword`、`page`、`pageSize`。`data` 为 `PageResult<EntityVO>`。

### GET `/entities/{id}/related`
关联实体。参数：`depth`（默认 1）。`data` 为 `EntityVO[]`。

---

## 关系 `/api/v1/relations`

> 仅列出只读端点。

### GET `/relations/entity/{entityId}`
实体的关系列表。参数：`type`（关系类型枚举名，可选）。`data` 为 `RelationDTO[]`。
脚本：`relations <id> [--type]`

### GET `/relations/path`
两实体间路径。参数：`sourceId`、`targetId`（均必填）、`maxDepth`（默认 3）。`data` 为 `GraphPathDTO[]`，每条含 `{ nodes[], relations[], length, score }`。
脚本：`path <src> <dst> [--max-depth]`

### GET `/relations/connected`
是否连通。参数：`entityId1`、`entityId2`。`data` 为 `boolean`。

### GET `/relations/{id}`
关系详情，`data` 为 `RelationDTO`。

---

## 图谱 `/api/v1/graph`

### GET `/graph/subgraph/{entityId}`
以实体为中心的子图。参数：`depth`（默认 2）。`data` 为 `GraphSubsetVO`：`{ nodes[], edges[], nodeCount, edgeCount, truncated, centerId }`。
脚本：`graph <id> [--depth]`

### POST `/graph/subgraph`
多实体子图。Body：实体 ID 数组；参数 `depth`（默认 1）。`data` 为 `GraphSubsetVO`。

### GET `/graph/statistics`
全局统计。`data` 为 `GraphStatistics`：`{ totalNodes, totalRelations, nodeCountByType, relationCountByType }`。
脚本：`stats`

### GET `/graph/neighbors/{entityId}`
邻居节点 ID 列表。参数：`direction`（`in`/`out`/`both`，默认 both）、`limit`（默认 50）。`data` 为 `string[]`。
脚本：`neighbors <id> [--direction --limit]`

---

## 分类体系 `/api/v1/taxonomies`

### GET `/taxonomies/tree`
分类树。参数：`type`（必填，`INDUSTRY`/`RESEARCH_DOMAIN`/`PRODUCT_CATEGORY`）、`maxDepth`（可选）。`data` 为 `TaxonomyNode[]`（含 `children` 嵌套）。
脚本：`taxonomy-tree <type> [--max-depth]`

### GET `/taxonomies/{taxonomyId}/entities`
按分类浏览实体（递归覆盖子分类），**结果按展示日期倒序**（eventDate / publishedDate / applicationDate / publishedYear / updatedAt），因此可直接用于取"某行业最新内容"，如 `--type Article` 取最新资讯、`--type Event` 取最新事件。参数：`entityType`（可选，code 或枚举名均可）、`page`（默认 1）、`pageSize`（默认 20）。`data` 为 `PageResult<EntityVO>`（`EntityVO.type` 为大写枚举名）。
脚本：`taxonomy-entities <id> [--type --page --limit]`

### GET `/taxonomies/{taxonomyId}/children`
子分类列表，`data` 为 `TaxonomyNode[]`。

### GET `/taxonomies/{taxonomyId}/type-counts`
按分类统计各实体类型数量，`data` 为 `{ <typeCode>: count }`。

---

## curl 直连示例

```bash
BASE="${HUGMAP_BASE_URL:-https://www.hugmap.com}"

# 全局统计
curl -s "$BASE/api/v1/graph/statistics"

# 聚合搜索（公司类型）
curl -s "$BASE/api/v1/portal/search?q=OpenAI&type=Company"

# 公司详情
curl -s "$BASE/api/v1/portal/entity/company/company_openai"

# 两实体路径
curl -s "$BASE/api/v1/relations/path?sourceId=person_yann_lecun&targetId=product_chatgpt&maxDepth=3"
```
