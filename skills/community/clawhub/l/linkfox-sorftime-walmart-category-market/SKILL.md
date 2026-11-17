---
name: linkfox-sorftime-walmart-category-market
description: 调用 Sorftime 研究 Walmart 美国站类目：获取完整类目树、按自然语言类目名称匹配相关 NodeId，或使用下划线分隔的 NodePath 查询类目市场数据及 Best Seller Top 80。用户提到 Walmart 类目树、类目名称搜索、类目匹配、类目节点、NodeId、NodePath、类目市场分析、类目调研、类目规模、类目热销商品、Best Seller，或需要先定位类目再研究市场时使用。
---

# Walmart 类目市场研究

Use Sorftime data to retrieve the Walmart US category hierarchy, match a natural-language category name, or inspect one category's market report and Best Seller Top 80.

## Core Concepts

- Send exactly one `operation` per request. Do not automatically chain operations; each call consumes Sorftime Requests.
- `tree` returns the complete category hierarchy and needs no other business parameter.
- `searchByName` accepts a natural-language category name and returns up to three related category matches.
- `marketReport` requires a known `nodePath`. Never guess the path from a category name.
- All fields are flat at the top level of the JSON body. `operation` values are case-sensitive.

## Operation Routing

| Intent | operation | Other parameters | Sorftime Request |
|---|---|---|---:|
| Download the category tree | `tree` | None | 5 |
| Match a natural-language category name | `searchByName` | `name` | 1 |
| Query a category market report | `marketReport` | `nodePath` | 5 |

Complete parameter and response details are in `references/api.md`.

## 调用方式

- **API 端点**：`POST /sorftime/walmart/categoryMarket`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/sorftime_walmart_category_market.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-sorftime-walmart-category-market-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 解决认证和积分问题

发生以下异常情况时，采用 `references/onboarding.md` 引导解决问题：

- **未配置 API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`
- **响应 401 或 402 状态码**
- **响应提示积分或余额不足**：消息含“积分余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值”或类似含义

## Usage Examples

```bash
python scripts/sorftime_walmart_category_market.py '{"operation":"tree"}'
python scripts/sorftime_walmart_category_market.py '{"operation":"searchByName","name":"patio furniture"}'
python scripts/sorftime_walmart_category_market.py '{"operation":"marketReport","nodePath":"4044_623679_1032619_5842891_9823303"}'
```

Prefer `searchByName` when the user supplies a natural-language category name. Use `tree` only when full hierarchy traversal is required. A tree response can be approximately 10 MB; normally inspect its saved JSON selectively rather than using `--inline`.

## Display Rules

1. State the selected operation and show `requestConsumed` and `costToken` when returned.
2. For `tree`, show matched category names, their ID hierarchy, and the derived `nodePath`; never dump the full tree into conversation.
3. For `searchByName`, show at most the returned three `NodeId` and `CategoryName` pairs; label them as related matches rather than exact classification.
4. For `marketReport`, summarize only returned metrics and present Best Seller products compactly.
5. Label Best Seller data as a maximum Top 80 scope, not the entire category catalog.
6. Preserve upstream field meanings and never invent missing category relationships or metrics.

## Important Limitations

- All three operations target Walmart US (`domain=21` is applied by the backend).
- Sorftime may omit categories unsuitable for third-party sellers; absence does not prove Walmart has no such category.
- `marketReport` accepts a numeric underscore-delimited `nodePath`, not a free-text category name.
- `searchByName` returns no more than three related categories and does not guarantee an exact match.
- `tree` and `marketReport` consume 5 upstream requests each; `searchByName` consumes 1. Do not retry or run another operation without user authorization.
- This skill does not cover product or keyword data.

## User Expression & Scenario Quick Reference

**Applicable**: Walmart category tree, natural-language category matching, category NodeId/path, category market, and category Best Seller requests.

**Not applicable**: product detail/trend/sales, keyword metrics, or saved-keyword management.

**Boundary judgment**: If the primary object is a Walmart product ID, use product analysis. Use `searchByName` for a category name, `tree` for hierarchy traversal, and `marketReport` for a known category path.

## 积分消耗规则

按动态规则计费：消耗积分 = Sorftime内部查询次数 × 12。Sorftime内部查询次数：不同 operation 需要的查询次数可能不同，实际次数由 Sorftime 决定。

> 用户会因积分消耗而支付费用。必须提醒用户并让用户决定是否继续执行另一个 operation。

**Feedback:**

Auto-detect and report feedback via the Feedback API when the skill behavior or result mismatches intent, the user expresses praise or dissatisfaction, or an improvement is apparent. Call it as specified in `references/api.md` without interrupting the user's flow.

---
*For more high-quality, professional cross-border e-commerce skills, visit [LinkFox Skills](https://skill.linkfox.com/).*
