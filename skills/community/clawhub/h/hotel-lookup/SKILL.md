---
name: hotel-lookup
display_name: "Hotel Lookup — FlyAI search-hotel · Fliggy MCP"
description: >
  Hotel discovery, shortlist comparison, and booking handoff using **FlyAI `search-hotel`** on **Fliggy MCP**
  (structured filters: destination, stay dates, POI proximity, hotel/homestay/inn types, star tiers, bed layouts, sort, nightly CNY cap).
  Use when users ask to find hotels, compare options by budget, location, stars, or bed type, plan city stays, family or business lodging,
  or move toward booking/detail pages via returned **mainPic** and **detailUrl** in JSON—see `references/search-hotel.md` for exact flags.
homepage: https://open.fly.ai/
metadata:
  version: 1.2.0
  agent:
    type: tool
    runtime: node
    context_isolation: execution
    parent_context_access: read-only
  openclaw:
    emoji: "\U0001F3E8"
    priority: 88
    requires:
      bins:
        - node
    intents:
      - hotel_search
    patterns:
      - "(?i)\\b(flyai)[\\s-]*hotel\\b"
      - "((search|find|book|compare|recommend).*(hotel|hotels|stay|stays|lodging|accommodation|resort|hostel|民宿))"
      - "((hotel|hotels|stay|lodging|accommodation).*(search|book|compare|price|deal|availability|check-?in))"
      - "(搜索|查找|推荐|比较|预订|查询).*(酒店|民宿|住宿|房型|入住|退房|星级|预算)"
      - "(酒店|民宿|住宿).*(搜索|预订|比价|价格|空房|取消)"
      - "(大床房|双床房|多床房).*(酒店|民宿|搜索|预订)"
      - "(排序|按价格|按评分|按距离).*(酒店|民宿|住宿)"
      - "(关键词|主题房|亲子|商务|周末).*(酒店|民宿|搜索)"
      - "(附近酒店|邻近景点|靠近|周边).*(酒店|民宿|搜索|预订)"
      - "(每晚|一晚|预算|不超过|以内).*(元|块|CNY|人民币).*(酒店|民宿)"
      - "(民宿|客栈).*(还是|和|或).*(酒店|住宿)"
---
# Hotel Lookup (FlyAI · Fliggy MCP)

Provide **hotel discovery, comparison, and booking handoff** using the **FlyAI CLI** command **`search-hotel`**, backed by **Fliggy MCP**. Outputs are **decision-ready** when you respect live JSON fields and the flag schema in **`references/search-hotel.md`** (single source of truth).

---

## Prerequisites

1. Install FlyAI CLI: `npm i -g @fly-ai/flyai-cli`
2. Optional richer results: `flyai config set FLYAI_API_KEY "your-key"` (keep secrets out of logs).
3. **I/O:** one JSON object per line on **stdout**; guidance/errors on **stderr** (`flyai search-hotel --help` for flag discovery).

---

## Workflow

### 1. Capture intent before running `search-hotel`

Extract and confirm (ask only the minimum if missing):

- **Destination** → maps to required `--dest-name` (country / province / city / district).
- **Stay window** → `--check-in-date` / `--check-out-date` (`YYYY-MM-DD`).
- **Budget** → `--max-price` (CNY per night cap).
- **Stars & beds** → `--hotel-stars`, `--hotel-bed-types`.
- **Lodging mix** → `--hotel-types` (`酒店` / `民宿` / `客栈`).
- **Landmark / “near X”** → `--poi-name` plus `--dest-name`.
- **Free-text narrowing** → `--key-words`.
- **Ranking preference** → `--sort` (`price_asc` / `price_desc` / `rate_desc` / `distance_asc` / `no_rank`).
- **Trip purpose** (business / family / leisure) → use to choose filters and how you explain trade-offs; **do not** send fields that `references/search-hotel.md` does not define.

### 2. Align parameters to the reference (no “tag priming” RPC)

- Open **`references/search-hotel.md`** and mirror **exact flag names**—there is **no** separate “prime tags” or tag-cache step in `search-hotel`.
- Validate **dates** (not in the past; correct format). If the city or district is ambiguous, **ask the user**—never guess `--dest-name`.

### 3. Search hotels with normalized `flyai search-hotel` flags

- Build one invocation: `flyai search-hotel …` per the reference **Examples** and parameter list.
- Prefer a **bounded** result set for first pass (e.g. sensible defaults from user intent); **shortlist to top 3–5** in the final narrative.
- Respect live JSON behavior from upstream:
  - Some fields may be **null** or missing.
  - **Price** in samples appears as display strings (e.g. `¥618`); do not invent currency rules not present in data.
  - If the service returns errors or empty `itemList`, follow **Error handling** below.

### 4. Enrich finalists from **returned JSON only** (no extra hotel-detail RPC)

- Each finalist row comes from **`data.itemList`** (see output example in `references/search-hotel.md`).
- Use **`mainPic`**, **`detailUrl`**, `name`, `address`, `price`, `score`, `star`, `review`, `interestsPoi`, etc. when present.
- **There is no `getHotelDetail` call in this skill.** Deeper room-level matrices like full rate-plan grids are **only** available if they appear inside the JSON you already received; otherwise direct the user to **`detailUrl`** for authoritative booking pages.
- If you need a second pass, run a **narrower** `search-hotel` (tighter dates, POI, or keywords)—do not fabricate APIs.

### 5. Return decision-ready output

Always give:

- **Recommended** pick (best fit to stated constraints).
- **Two alternatives** with honest trade-offs (price vs distance vs stars vs POI proximity—only from observed fields).
- **Booking handoff:** what to open next (**`detailUrl`**), what to double-check on the supplier page, and **2–4** final confirmation questions if anything is still ambiguous.

---

## Output template (concise bullets)

- **行程信息**: 目的地 / 入住离店 / 人数或房型需求 / 预算（每晚 CNY）/ 关键偏好（商务/亲子等）
- **推荐酒店（首选）**
  - 酒店名 · 价格展示（来自 JSON）
  - 位置 / 交通或 POI 相关字段（如 `interestsPoi`）
  - 图片行：`![]({mainPic})`（若存在）
  - 详情/预订：`[Click to book]({detailUrl})`（若存在）
  - 评分/星级/短评（若存在）
  - 推荐理由（只引用结果中可见事实）
- **备选 1 / 备选 2**（同结构，字段缺失则说明）
- **决策建议**: 适合人群与取舍（不编造政策）
- **下一步确认**: 仅列 2–4 个必要确认项（支付前核对官方页等）

---

## Output & presentation (Markdown)

- Show **image before** booking link when both exist.
- Use headings and **tables** when comparing multiple hotels.
- Optional brand line: e.g. “Based on **fly.ai** real-time hotel results.”

---

## Quality bar

- Prefer **concrete numbers and fields** from JSON over vague adjectives.
- **Do not invent** cancellation rules, breakfast, or prices not shown in data.
- If data is missing, stale, or mismatched to user intent, **say so** and suggest adjusting flags or confirming on **`detailUrl`**.
- Keep shortlists tight—avoid dumping huge `itemList` tables unchanged.
- Never expose API keys or local config in chat.

---

## References

| Surface | Location |
|---------|----------|
| `search-hotel` flags, examples, output shape | **`references/search-hotel.md`** (authoritative) |

## Error handling

1. **Validate** inputs against `references/search-hotel.md`; ask the user when required fields are unclear.
2. **Diagnose** stderr + JSON `status` / `message`; fix flags vs retry on transient errors only.
3. **Empty results** — relax filters **once**, then explain; no infinite retries.
4. **Transparency** — if location or dates may be wrong, state it before recommending payment.

---

## Differentiation (honest scope)

| Hook | Meaning (`search-hotel` only) |
|------|-------------------------------|
| **POI + destination** | `--poi-name` + `--dest-name` for “near landmark” stays. |
| **三态住宿** | `--hotel-types`: 酒店 / 民宿 / 客栈 in one run. |
| **CNY nightly cap** | `--max-price` for per-night budget ceilings. |
| **Agent-first JSON** | `mainPic` + `detailUrl` for fast Markdown cards—**no** extra scraper stack in this bundle. |

---