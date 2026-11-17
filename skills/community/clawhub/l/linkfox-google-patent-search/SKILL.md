---
name: linkfox-google-patent-search
description: 通过 Google Patents 公开专利数据库检索全球专利，支持关键词、发明人、受让人、国家、日期、专利状态等多维筛选，返回专利公开号、标题、发明人、申请/公开/授权日期、受让人、CPC 分类、PDF 链接等核心著录数据。当用户提到谷歌专利、Google Patents、专利检索、专利搜索、查专利、专利防侵权、FTO 排查、prior art search、专利侵权排查时触发此技能。即使用户未明确提及"Google Patents"，只要用户希望通过关键词或著录条件检索专利文献，也应触发此技能。
---

# Google Patents Search

This skill searches the public Google Patents database, returning matching patents with publication numbers, titles, inventors, assignees, dates, CPC classifications, and PDF links. Useful for cross-border sellers doing freedom-to-operate (FTO) checks, prior-art searches, and patent-infringement risk screening before listing a product.

## Core Concepts

Google Patents Search runs a query (`q`) against the public Google Patents corpus. The query supports Google Patents' native advanced syntax (e.g. `owner:"company"`, `inventor:"name"`, date ranges). Results are returned as a ranked list of patents (and optionally Google Scholar articles).

**This skill returns a list** of patents with bibliographic fields. To retrieve detailed bibliographic data, full text, legal status, family, or images for a specific patent found here, feed the returned `patentId`/`publicationNumber` into the corresponding `linkfox-zhihuiya-bibliography` / `linkfox-zhihuiya-legal-status` / `linkfox-zhihuiya-patent-family` skills.

## Data Fields

Each `organicResults[]` item (one matching patent):

| Field | Description |
|-------|-------------|
| publicationNumber | Publication (announcement) number |
| patentId | Patent ID |
| title | Patent (or Scholar article) title |
| snippet | Result snippet / abstract |
| inventor | Inventor(s) |
| assignee | Assignee(s) |
| filingDate | Filing date |
| publicationDate | Publication / issue date |
| grantDate | Grant date |
| priorityDate | Priority date |
| language | Patent language |
| cpc | Cooperative Patent Classification (only when clustered) |
| cpcDescription | CPC description |
| countryStatus | Per-country legal status map |
| position | Search result position |
| rank | Result rank (may differ from position when clustered) |
| patentLink | Google Patents link |
| pdf | Patent PDF link |
| thumbnail | Patent thumbnail |
| figures | Figure list (`thumbnail`, `full`) |
| scholar | Whether this is a Google Scholar result |
| scholarId / scholarLink / author / authorEtal / publicationVenue / urlHostname | Scholar-article fields (present when `scholar=true`) |
| serpapiLink | Result detail-API link |

Top-level fields:

| Field | Description |
|-------|-------------|
| organicResults | Patent search result list |
| searchParameters | Echoed query parameters |
| searchInformation | Search metadata (total results, time, etc.) |
| pagination / serpapiPagination | Pagination info |
| summary | Result summary |
| costToken | Token cost for this query |
| message | Provider info message (may appear when query succeeds but yields no results) |

## 调用方式

- **API 端点**：`POST /googlePatent/search`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/google_patent_search.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗算力；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索或翻页时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-google-patent-search-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 解决认证和算力问题
发生以下异常情况时，采用 references/onboarding.md 引导解决问题：

### 异常情况
- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示算力或权限不足**：消息含"算力余额不足/计费不足/余额不足/quota exceeded/insufficient balance/No permission/API package quota/套餐到期/需充值/请充值"，或类似含义的内容。

## Parameter Guide

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| q | Yes | - | Google Patents search query, supports native advanced syntax (e.g. `owner:"Company"`, `inventor:"Lee"`, date operators). Max 1000 chars |
| num | No | 10 | Results per page, range 10–100 |
| page | No | 1 | Page number, starting from 1 |
| country | No | - | Country codes, comma-separated (e.g. `US,CN,WO`) |
| language | No | - | Languages, comma-separated (Google Patents official language values) |
| before | No | - | Max date, format `priority|filing|publication:YYYYMMDD` |
| after | No | - | Min date, same format as `before` |
| sort | No | - | `new` (newest) or `old` (earliest); default = relevance |
| type | No | - | Result type: `PATENT` or `DESIGN` |
| status | No | - | Patent status: `GRANT` or `APPLICATION` |
| patents | No | true | Whether to include patent results |
| scholar | No | false | Whether to include Google Scholar results |
| litigation | No | - | Litigation status: `YES` or `NO` |
| inventor | No | - | Inventor(s), comma-separated |
| assignee | No | - | Assignee(s), comma-separated |
| clustered | No | - | Cluster by classification; provider currently only supports `true` |
| dups | No | - | Dedup mode; default = by patent family, `language` = by publication text |

### Query syntax

`q` accepts Google Patents' advanced query operators. Common forms:

| Operator | Meaning |
|----------|---------|
| `(wireless earbuds)` | Full-text / general keyword |
| `owner:"Company Inc"` | Assignee/owner match |
| `inventor:"J Lee"` | Inventor match |
| `before:publication:20250101` / `after:filing:20200101` | Date bounds (also passable as `before`/`after` params) |

## Usage Examples

**1. Basic keyword search**
```
在 Google Patents 检索 wireless earbuds 相关专利，返回 10 条
```
Action: `{"q": "wireless earbuds", "num": 10}`

**2. Filter by country + status**
```
检索美国授权的 wireless earbuds 专利
```
Action: `{"q": "wireless earbuds", "country": "US", "status": "GRANT"}`

**3. Date range + sort newest**
```
检索 2024 年至今公开的 wireless earbuds 专利，按最新排序
```
Action: `{"q": "wireless earbuds", "after": "publication:20240101", "sort": "new"}`

**4. Assignee search**
```
检索受让人 Apple 的专利
```
Action: `{"q": "owner:\"Apple\"", "assignee": "Apple"}`

**5. Paginate**
```
继续检索 wireless earbuds，查看第 2 页，每页 20 条
```
Action: `{"q": "wireless earbuds", "page": 2, "num": 20}`

## Display Rules

1. **Present results as a table**: show `publicationNumber`, `title`, `inventor`, `assignee`, `publicationDate`/`grantDate` per item.
2. **Show totals**: always state the total hit count from `searchInformation`/`pagination` and the current page range.
3. **Date formatting**: render `filingDate`/`publicationDate`/`grantDate`/`priorityDate` as readable dates.
4. **Links**: surface `patentLink` and `pdf` so the user can open the patent directly.
5. **Scholar results**: when `scholar=true`, visually distinguish Scholar articles from patents.
6. **Large result sets**: present a summary table first, note the total, and offer to expand specific patents.
7. **Expand via sibling skills**: to get full bibliographic/legal/family detail for a found patent, direct the user to `linkfox-zhihuiya-bibliography` / `linkfox-zhihuiya-legal-status`; do not re-query this search skill for details.
8. **No fabrication**: only display fields actually present in the response; never invent titles, dates, or assignees not returned.

## Important Limitations

- **`q` is the primary search input**: a query without `q` yields no meaningful results.
- **`num` range 10–100**; values outside the range are rejected.
- **List-only output**: this skill returns bibliographic list fields. Full text, legal status, family, and images must be fetched via dedicated `linkfox-zhihuiya-*` skills.
- **No auto-retry on empty/error**: if the query returns no hits or an error, do not automatically swap keywords or rewrite the query; confirm with the user first (each call costs credits).
- **`clustered` currently only supports `true`** per the upstream provider.
- **Date params use the `priority|filing|publication:YYYYMMDD` form**, not bare dates.

## User Expression & Scenario Quick Reference

**Applicable** — Discover patents on Google Patents:

| User Says | Scenario |
|-----------|----------|
| "检索 wireless earbuds 的专利" | Basic keyword search |
| "查谷歌专利" / "Google Patents 搜一下" | General patent search |
| "美国授权的 XX 专利" | Country + status filter |
| "2024 年至今公开的 XX 专利" | Date range filter |
| "受让人是 Apple 的专利" | Assignee search |
| "翻到第 2 页" | Pagination |

**Not applicable** — Needs beyond Google Patents list search:

- Bibliographic detail / full text / legal status of a known patent number (use `linkfox-zhihuiya-bibliography` etc.)
- Image-based patent search (use `linkfox-zhihuiya-patent-image-search`)
- Zhihuiya Analytics expression search with field-scoped boolean syntax (use `linkfox-zhihuiya-retrieval-patent-search`)

**Boundary judgment**: When the user wants to **discover** patents by keyword/inventor/assignee/country/date on the public Google Patents corpus → this skill. When they have a patent number and want its detailed metadata → the `linkfox-zhihuiya-*` skills.

## 算力消耗规则

消耗 8 算力。

> 用户会因算力消耗而支付费用。请充分评估：当需要高频调用本技能，或用户对算力消耗量预期不足时，务必提醒用户，由用户决定是否继续。

**Feedback:**

Auto-detect and report feedback via the Feedback API when any of the following apply:
1. The functionality or purpose described in this skill does not match actual behavior
2. The skill's results do not match the user's intent
3. The user expresses dissatisfaction or praise about this skill
4. Anything you believe could be improved

Call the feedback API as specified in `references/api.md`. Do not interrupt the user's flow.

---
*For more high-quality, professional cross-border e-commerce skills, visit [LinkFox Skills](https://skill.linkfox.com/).*
