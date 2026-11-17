---
name: linkfox-sorftime-walmart-product-analysis
description: 调用 Sorftime 按自然语言名称搜索 Walmart 美国站商品，或查询商品详情、商品趋势与按日销量。用户提到 Walmart 商品名称搜索、按名称找产品、相关产品、ProductId、商品详情、价格、评分、类目排名、商品趋势、历史变化、销量趋势、变体销量、按日销量、昨日销量、竞品发现或竞品跟踪时使用。
---

# Walmart 产品分析

Use Sorftime to find Walmart US products by a natural-language name or inspect one product's detail, historical trend, or daily sales-volume series.

## Core Concepts

- Send exactly one `operation` per request. Never call all four operations as a default workflow.
- Use `searchByName` to discover related products, `detail` for the current product summary, `trend` for historical product changes, and `salesVolume` for dated sales rows.
- Every request uses a flat JSON body. `searchByName` requires `name`; the other operations require string `productId`. `operation` values are case-sensitive.
- A follow-up operation or a different date range is another paid call. Reuse the 24-hour cache for identical JSON.

## Operation Routing

| Intent | operation | Parameters | Sorftime Request |
|---|---|---|---:|
| Find related products by name | `searchByName` | `name`, optional `pageIndex` | 2 |
| Current product details | `detail` | `productId` | 1 |
| Historical product trend | `trend` | `productId` | 2 |
| Daily/variant sales rows | `salesVolume` | `productId`, optional dates/page | 1 |

Read `references/api.md` before calling for exact date and pagination rules.

## Parameter Guide

- Always treat `productId` as a string, even when it contains digits only.
- `searchByName` accepts a natural-language product name and returns up to 100 related products per page; `pageIndex` defaults to 1.
- `salesVolume` accepts optional `queryDate` and `queryEndDate` in `yyyy-MM-dd`. With neither, it returns the recent 30-day range; with only `queryDate`, the end defaults to the current day.
- `pageIndex` applies to `searchByName` and `salesVolume`, starts at 1, and defaults to 1.
- The current available historical range is controlled by Sorftime; do not promise a fixed earliest date.

## 调用方式

- **API 端点**：`POST /sorftime/walmart/productAnalysis`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/sorftime_walmart_product_analysis.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-sorftime-walmart-product-analysis-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
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
python scripts/sorftime_walmart_product_analysis.py '{"operation":"searchByName","name":"wireless earbuds","pageIndex":1}'
python scripts/sorftime_walmart_product_analysis.py '{"operation":"detail","productId":"5169493923"}'
python scripts/sorftime_walmart_product_analysis.py '{"operation":"trend","productId":"5169493923"}'
python scripts/sorftime_walmart_product_analysis.py '{"operation":"salesVolume","productId":"5169493923","queryDate":"2026-07-01","queryEndDate":"2026-07-31","pageIndex":1}'
```

## Display Rules

1. State the operation and supplied product name or product ID, and show returned `requestConsumed` and `costToken`.
2. For `searchByName`, label results as related products rather than exact matches and report the requested page.
3. For `detail`, present only fields returned by the ProductSummeryObject; do not infer missing attributes.
4. For `trend`, identify time fields and units from the response before summarizing changes.
5. For `salesVolume`, interpret rows as `[date, sales, type]`; `type=2` marks yesterday's sales record.
6. Label estimates or observed values accurately; do not present them as guaranteed Walmart transactions.

## Important Limitations

- This integration targets Walmart US only.
- The API accepts one product name or one product ID and one operation per call.
- Sorftime controls historical coverage and data availability.
- Pagination or a second operation creates another paid call and requires user authorization.
- `searchByName` is natural-language related-product discovery, not a multi-filter product database or category-market query.

## User Expression & Scenario Quick Reference

**Applicable**: finding Walmart products from a natural-language product name, or queries centered on a known ProductId and its details, trend, or sales history.

**Not applicable**: category market research, keyword metrics/reverse lookup, or multi-condition product filtering.

**Boundary judgment**: Use `searchByName` only when the user needs related products from a name; use `detail` for a current snapshot, `trend` for historical attributes, and `salesVolume` only for dated sales rows.

## 积分消耗规则

按动态规则计费：消耗积分 = Sorftime内部查询次数 × 12。Sorftime内部查询次数：不同 operation 需要的查询次数可能不同，实际次数由 Sorftime 决定。

> 用户会因积分消耗而支付费用。不要未经确认补调另一 operation 或下一页。

**Feedback:**

Auto-detect and report feedback via the Feedback API when behavior or results mismatch intent, the user expresses praise or dissatisfaction, or an improvement is apparent. Follow `references/api.md` without interrupting the user's flow.

---
*For more high-quality, professional cross-border e-commerce skills, visit [LinkFox Skills](https://skill.linkfox.com/).*
