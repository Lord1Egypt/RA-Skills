---
name: linkfox-chuhaijiang-tiktok-live
description: 使用出海匠（Chuhaijiang）研究 TikTok 公开直播市场，支持多条件直播搜索、单场直播详情和直播带货商品钻取。用户明确点名出海匠或 Chuhaijiang 且意图是直播搜索、直播详情或从直播反查商品时触发；即使用户未指定数据源，也仅在需要从直播反查带货商品时触发。通用 TikTok 带货直播榜单或详情使用 linkfox-kalodata-tiktok-livestream，从商品出发的关联直播研究使用 linkfox-chuhaijiang-tiktok-product；点名其他数据源时不触发。
---

# TikTok Live Commerce Intelligence

Use this skill to research public TikTok livestream commerce: discover live sessions with market filters, inspect one session and its performance metrics, or identify the products sold in that session.

## Core Concepts

- This is read-only public-market research. It does not start, moderate, schedule, or manage a TikTok livestream.
- Search returns `data.items[]` plus `data.total_count`. Reuse a search item's string `id` for detail or related-product calls.
- Detail returns identity and creator context in `data.items[]`; `include=core` additionally returns performance metrics in `data.core.items[]`.
- Related-product rows use `tiktok_live_detail_product_*` fields. Read `references/api.md` before interpreting them.
- Money fields are objects such as `{ "unit": "US", "value": 2015752.25 }`. Preserve both fields and do not silently relabel or convert the unit.
- A requested `country` is query context; preserve the row-level `country_code` because it is authoritative for the returned record.

## Data Fields

| Field | Meaning |
|---|---|
| `data.total_count` | Total matching live sessions or products |
| `data.items[].id` | Live room ID, or product ID on the related-products endpoint |
| `title` / `room_link` | Live title and public room URL |
| `user_id` / `user_unique_id` | Host identifiers |
| `gmv` / `gpm` / `opm` | Revenue, GMV per thousand viewers, and orders per thousand viewers |
| `total_sold_count` / `product_count` | Units sold and products promoted in the live |
| `total_user` / `max_user_count` | Total and peak audience counts |
| `data.core.items[]` | Optional normalized performance metrics from detail `include=core` |
| `tiktok_live_detail_product_*` | Related product, seller, price, sales, GMV, commission, and conversion fields |

## Endpoints

| User goal | Endpoint | Script |
|---|---|---|
| Search public livestreams | `/chuhaijiang/lives/search` | `chuhaijiang_live_search.py` |
| Inspect one livestream | `/chuhaijiang/lives/detail` | `chuhaijiang_live_detail.py` |
| Find products sold in a livestream | `/chuhaijiang/lives/related-products` | `chuhaijiang_live_related_products.py` |

Call only the endpoint needed for the user's current question. Do not automatically drill from search to detail or products because each endpoint is billed independently.

## Parameter Guide

- `country`: required lowercase marketplace code: `br,de,es,fr,gb,id,it,jp,mx,my,ph,sg,th,us,vn`.
- `page`: starts at 1. Search and related products accept `pageSize` up to 10.
- `id`: required for detail and related products. Pass 19-digit IDs as JSON strings to preserve precision.
- `include`: detail-only optional string; use `core` when normalized performance metrics are needed.
- Search supports `keyword`, `category`, `productCategory`, `isLiving`, `isCommercial`, sales/GMV/audience ranges, and `sort` in `field:asc|desc` form. The default sort is `gmv:desc`.
- Use the camelCase request fields documented in `references/api.md`; do not send the upstream snake_case aliases.

## 调用方式

- **API 端点**：`POST /chuhaijiang/lives/search`、`POST /chuhaijiang/lives/detail` 或 `POST /chuhaijiang/lives/related-products`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/chuhaijiang_live_<entry>.py '<JSON 参数>' [--inline]`，其中 `<entry>` 为 `search`、`detail` 或 `related_products`
- **成本约束**：业务入口脚本默认只缓存成功响应 24 小时，业务成功的空结果也可缓存；缓存按当前工作目录、调用身份、网关、端点和完整请求参数隔离。相同组合命中时输出 `Cache hit`，不会发起新的付费请求。HTTP 或业务失败不缓存；`--inline` 不绕过缓存；`--no-cache` 会强制真实请求并可能再次消耗算力，仅在用户明确同意额外消耗或调试时使用。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-chuhaijiang-tiktok-live-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、业务总数、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 JSON 文件按需抽取，避免整份 JSON 进入上下文。

## 解决认证和算力问题

网关返回认证或余额错误时，读取 `references/onboarding.md`，按其中的 auth/billing 分流使用 `scripts/onboarding.py`。不要把 API Key、验证码、支付链接或原始用户消息写入反馈。

## Usage Examples

```bash
python scripts/chuhaijiang_live_search.py '{"country":"us","isCommercial":true,"sort":"gmv:desc","page":1,"pageSize":3}'
python scripts/chuhaijiang_live_detail.py '{"country":"us","id":"7643101948819835678","include":"core"}'
python scripts/chuhaijiang_live_related_products.py '{"country":"us","id":"7643101948819835678","page":1,"pageSize":3}'
```

These examples were production-validated with non-empty semantic results on 2026-08-29. Public-market IDs are volatile; use a fresh search result if an example stops resolving.

## Display Rules

1. State the requested marketplace, filters, sort, page, page size, and returned total.
2. For search, show title, room ID/link, host, time range, audience, products, units sold, GMV, GPM, and OPM when returned.
3. For detail, separate identity/host fields from optional `core` metrics; label `follower_conversion_rate` as a decimal unless explicitly formatting it as a percentage.
4. For related products, show product ID/title/image, country, price range, seller, units sold, GMV, commission rate, and conversion rate when present.
5. Preserve 19-digit IDs as strings. Preserve raw epoch-millisecond timestamps and add readable dates only as derived labels.
6. Report empty arrays honestly and never invent a product relationship or a currently-live status.

## Important Limitations

1. Data reflects the provider's indexed public snapshot and can lag TikTok.
2. `isLiving` is a search filter, not proof that a returned room is still live when displayed later.
3. Related products are available only when the indexed live session has product relationships.
4. Search filters do not imply causality between audience, GMV, sales, and creator performance.
5. Do not expose internal tool identifiers, credentials, cache files, or unrelated response fields.

## User Expression & Scenario Quick Reference

**Use this skill**: “用出海匠搜美国 TikTok 带货直播”, “用 Chuhaijiang 看这场直播详情”, “这场直播卖了哪些商品”, “出海匠 TikTok live analytics”.

**Adjacent**: General TikTok livestream rankings or detail requests without a named source should use `linkfox-kalodata-tiktok-livestream`. Product-first research, including finding livestreams associated with a product, uses `linkfox-chuhaijiang-tiktok-product`. Creator-first live research uses `linkfox-chuhaijiang-tiktok-creator`.

**Not applicable**: starting or scheduling livestreams, moderation, seller-backend operations, order handling, replay downloading, transcription, or media generation/editing.

## 算力消耗规则

按端点分别计费：直播详情 9 算力/次；直播搜索和直播关联商品 18 算力/次。

> 用户会因算力消耗而支付费用。高频调用或多端点钻取前，先说明预计调用次数与算力消耗。

---

**Feedback:** Use the Feedback API in `references/api.md` only when the user explicitly asks to submit feedback or authorizes it after an issue is identified. Sanitize the content and never include credentials, signed URLs, phone numbers, or unrelated task context.

---
*For more high-quality, professional cross-border e-commerce skills, visit [LinkFox Skills](https://skill.linkfox.com/).*
