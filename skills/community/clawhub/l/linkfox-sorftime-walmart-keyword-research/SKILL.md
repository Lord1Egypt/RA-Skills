---
name: linkfox-sorftime-walmart-keyword-research
description: 调用 Sorftime 研究 Walmart 美国站关键词市场、名称反查词、搜索结果商品、关键词详情、商品关联词与扩展词，并管理收藏关键词目录。当用户提到 Walmart 关键词研究、搜索量或排名筛选、商品反查关键词、相关关键词、关键词详情、关键词搜索结果商品、收藏关键词、关键词分组、keyword research、keyword discovery、related keywords 或 product keywords 时使用。
---

# Walmart 关键词研究

Use one Sorftime endpoint to research Walmart US keywords or explicitly manage the saved-keyword library.

## Core Concepts

- Send exactly one `operation` per request. Never run multiple keyword operations as an automatic discovery chain.
- Use a flat JSON body. The only business nesting is the optional `pattern` object for `marketQuery`.
- `operation` values are case-sensitive. A different operation, page, or filter is another paid call.
- `favoriteAdd` and `favoriteChange` mutate external account data and require an explicit, unambiguous user request.

## Operation Routing

| Intent | operation | Required input | Sorftime Request |
|---|---|---|---:|
| Filter current hot keywords | `marketQuery` | None; filters optional | 5 |
| Find hot keywords from a name | `searchByName` | `name` | 1 |
| Find products for a hot keyword | `searchProducts` | `keyword` | 5 |
| Inspect keyword metrics | `detail` | `keyword` | 1 |
| Find a product's associated keywords | `productKeywords` | `productId` | 1 |
| Expand related keywords | `relatedKeywords` | `keyword` | 5 |
| Add a saved keyword | `favoriteAdd` | `keyword` | 1 |
| Delete or move a saved keyword | `favoriteChange` | `keyword`, `command` | 0 |
| List saved keywords or folders | `favoriteList` | `command` | 1 |

Read `references/api.md` for the complete conditional parameter matrix before calling.

## Parameter Guide

- `marketQuery`: optional `pattern.keyword`, `pattern.rankCondition`, and `pattern.searchVolumeCondition`; `pageIndex` defaults to 1 and `pageSize` to 20 (20–200).
- A one-value condition such as `[10000]` is a lower bound. `[0,10000]` follows Sorftime's documented less-than-10000 semantics.
- `searchByName`: `name` is a product or category name; `pageIndex` defaults to 1, and Sorftime returns at most 200 rows per page.
- `searchProducts`, `productKeywords`, and `relatedKeywords`: pagination defaults to page 1 and 20 rows, maximum 200.
- `favoriteList` exposes `pageIndex` (default 1); the backend maps it to Sorftime's upstream `Page` field.

## 调用方式

- **API 端点**：`POST /sorftime/walmart/keywordResearch`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/sorftime_walmart_keyword_research.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；只读研究操作对同一参数组合使用 24h 本地缓存，`favoriteAdd`、`favoriteChange`、`favoriteList` 始终绕过缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-sorftime-walmart-keyword-research-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 解决认证和积分问题

发生以下异常情况时，采用 `references/onboarding.md` 引导解决问题：

- **未配置 API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`
- **响应 401 或 402 状态码**
- **响应提示积分或余额不足**：消息含“积分余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值”或类似含义

## Keyword Library Safety

- Add to the default “未分类” folder by omitting `dict`; a provided folder may be created by Sorftime.
- Delete with `command="del"`. Omitting `dict` deletes the keyword from every folder, so explicitly confirm that scope.
- Move with `command="move=<目标目录>"`. Omitting `dict` means the source is “未分类”.
- List with `command` equal to `all`, `dict`, or `dict=<目录>`.
- If an explicitly authorized mutation truly must be repeated after external state changed, use `--no-cache`; never use it to bypass the confirmation guard.
- `favoriteAdd`, `favoriteChange`, and `favoriteList` always bypass the local cache, so mutations are never suppressed and list results reflect the latest upstream state.

## Usage Examples

```bash
python scripts/sorftime_walmart_keyword_research.py '{"operation":"marketQuery","pattern":{"keyword":"wireless","searchVolumeCondition":[10000]},"pageIndex":1,"pageSize":20}'
python scripts/sorftime_walmart_keyword_research.py '{"operation":"detail","keyword":"wireless earbuds"}'
python scripts/sorftime_walmart_keyword_research.py '{"operation":"productKeywords","productId":"5169493923","pageIndex":1,"pageSize":20}'
python scripts/sorftime_walmart_keyword_research.py '{"operation":"favoriteList","command":"dict","pageIndex":1}'
```

Run mutation operations only after explicit authorization.

## Display Rules

1. State the selected operation and show `requestConsumed` and `costToken` when returned.
2. Preserve metric meanings and observation windows; do not turn estimates into guaranteed demand or sales.
3. Report the requested page and offer another only after explaining that it creates another paid call.
4. Treat product IDs and keywords as strings.
5. For mutations, report the returned data code; HTTP 200 alone does not prove mutation success.

## Important Limitations

- This integration targets Walmart US only.
- Current-hot-keyword data, the 15-day product window, and the 30-day product-keyword window are Sorftime constraints.
- A single saved-keyword folder supports at most 2,000 keywords.
- The API saved-keyword library is separate from Sorftime Professional favorites; data is not synchronized between them.
- Read the Sorftime business response from `data.value`; its JSON shape varies by operation.
- Empty results must not trigger automatic variants, pagination, or related-keyword calls.
- This skill excludes Sorftime Walmart “其他” APIs.

## User Expression & Scenario Quick Reference

**Applicable**: Walmart keyword discovery, keyword metrics, product-to-keyword research, related terms, or an explicit saved-keyword-library action.

**Not applicable**: category-market reports, product detail/trend analysis, or any Sorftime Walmart “其他” capability.

**Boundary judgment**: Choose exactly one operation that matches the user's stated intent; never turn one keyword request into an automatic multi-step research chain.

## 积分消耗规则

按动态规则计费：消耗积分 = Sorftime内部查询次数 × 12。Sorftime内部查询次数：不同 operation 需要的查询次数可能不同，实际次数由 Sorftime 决定。

> 用户会因积分消耗而支付费用。高消耗筛选、扩展词或连续分页前必须提醒用户；任何收藏变更都须明确授权。

**Feedback:**

Auto-detect and report feedback via the Feedback API when behavior or results mismatch intent, the user expresses praise or dissatisfaction, or an improvement is apparent. Follow `references/api.md` without interrupting the user's flow.

---
*For more high-quality, professional cross-border e-commerce skills, visit [LinkFox Skills](https://skill.linkfox.com/).*
