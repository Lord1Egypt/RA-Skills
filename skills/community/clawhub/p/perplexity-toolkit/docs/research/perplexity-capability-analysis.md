# Perplexity AI: Web Interface vs API — Complete Capability Gap Analysis

**Prepared:** August 2026 (UTC+10)
**Purpose:** Feed research for building a Perplexity web-automation skill. This document maps what can ONLY be done through browser automation of the web interface, why the API falls short, pricing/hidden costs, and workarounds.
**Method:** Synthesized from Perplexity's official docs/help center, API pricing pages, third-party pricing trackers, dev forum posts, and Reddit practitioner threads. Where sources conflict or figures have shifted over time, that variance is flagged inline.

> **Headline finding:** The Perplexity web interface and the Perplexity API are *deliberately different products*, not two surfaces for the same engine. Perplexity's own moderators and community managers have stated there is **no intention to match API output quality to the web UI** — the UI is financially differentiated (if the API were as good, no one would pay for the UI). This is the single most important fact for anyone building Perplexity automation: **the reason you need browser automation is not that the API is missing small features — it's that the API is intentionally a lower-tier product.**

---

## Table of Contents
1. [Feature matrix: web-only vs API-available](#1-feature-matrix-web-only-vs-api-available)
2. [API pricing structure & hidden costs](#2-api-pricing-structure--hidden-costs)
3. [API rate limits by tier](#3-api-rate-limits-by-tier)
4. [Model availability differences](#4-model-availability-differences)
5. [Output quality differences (web vs API, same query)](#5-output-quality-differences-web-vs-api-same-query)
6. [Third-party Perplexity-like alternatives](#6-third-party-perplexity-like-alternatives)
7. [Known workarounds to get more from Perplexity](#7-known-workarounds-to-get-more-from-perplexity)
8. [Free vs Pro vs Max feature comparison](#8-free-vs-pro-vs-max-feature-comparison)
9. [Implications for web automation](#9-implications-for-web-automation)
10. [Sources](#10-sources)

---

## 1. Feature matrix: web-only vs API-available

Legend: ✅ available · ⚠️ partial / changed semantics · ❌ not available · 🔒 web-only (requires browser automation to replicate)

| Feature | Web (perplexity.ai) | API (api.perplexity.ai) | Notes / why it matters for automation |
|---|---|---|---|
| **Pro Search** (multi-step, deeper retrieval + reasoning) | ✅ default | ❌ **not supported** | Official forum: "The API doesn't support Pro Search today." Web answers run Pro Search; API answers resemble the "default/quick" answer style. Biggest single quality gap. |
| **Deep Research / Research** (agentic multi-query research loop) | ✅ (renamed "Research"; renamed from "Deep Research" May 2025) | ⚠️ **exposed as `sonar-deep-research`** model | The API does expose it programmatically (CoT/reasoning tokens NOT exposed in API response, unlike `sonar-reasoning-pro`). Web version (esp. on Max plan, Claude Opus backbone) is generally deeper. |
| **Advanced Deep Research / Learn Mode** | ✅ (new 2026 updates) | ❌ | Web-only UI around the research loop. |
| **Collections / Spaces** (folders of threads + custom AI instructions + shared files + collaboration) | ✅ ("Collections" now rebranded to **Spaces**) | ❌ **no API at all** | No create/query/update endpoints. Persistent knowledge workspaces with per-space file libraries are completely unreachable via API. 🔒 |
| **Focus modes** (All/Web, Academic, Math, Writing, Video, Social, Finance[Pro], YouTube, Reddit) | ✅ | ❌ **no documented `focus_mode` param** (see workarounds §7 — undocumented `search_focus` param partly replicates) | Client-side filter in web. API always searches "Web/all." Some focus modes have been temporarily removed/trimmed on web (mid-2026) while kept in mobile. 🔒 |
| **Comet browser** (agentic Chromium browser; acts on pages with your logged-in session) | ✅ (free via invite/rollout; Max early access) | ❌ | Perplexity's browser agent performs real web actions (booking, forms, multi-tab) — impossible via API. Direct ToS-driven competitor to browser automation. 🔒 |
| **Model Council** (one query answered by 3+ models side-by-side) | ✅ Max tier only | ❌ | No API equivalent. |
| **File upload (native UI)** — PDF, DOCX, XLSX, CSV, PPTX, MD, JSON, TXT, images, **audio, video** | ✅ (audio/video transcribed & searchable; multiple files; drag-and-drop folders) | ⚠️ Sonar API accepts limited doc formats (**PDF, DOC, DOCX, TXT, RTF**) as base64/URL up to 50 MB; **stateless per-request** — no persistent storage, no AV transcription, no spreadsheets | Web retains files in threads/Spaces; API discards after the request. Agent API additionally accepts **image attachments** (base64/HTTPS URL, PNG/JPEG/WEBP/GIF, ≤50 MB). 🔒 |
| **Image generation** (GPT Image 1, Nano Banana/Ge/Gemini image, Seedream 4.5; free 3/day, Pro unlimited) | ✅ | ❌ **no image generation endpoint** | No text-to-image or image editing in the API (cloudinary: "check whether Perplexity's current API offering supports this" — it does not). 🔒 |
| **Pages** (turn a thread into a shareable branded web article) | ✅ | ❌ | Publishing feature, no API. |
| **Memory** (persistent personalization across sessions) | ✅ | ❌ (API is stateless) | Web has personalized context; API requests are independent. |
| **Connectors** (400+ app integrations — Google Docs, Notion, GitHub, etc.) | ✅ | ❌ | Web can pull from your connected apps; API cannot. |
| **Perplexity Computer** (scheduled tasks, background assistant, email assistant, agentic workflows) | ✅ (Max/Enterprise Max) | ⚠️ separate **Agent API + Sandbox API** exist, but no Computer/scheduled-task surface | Browser-level autonomy (booking, browsing under your session) is web-only. |
| **Visual search / Shopping / Finance (UI tiles)** | ✅ (US shopping) | ❌ | Consumer UI surfaces; API has separate finance_search tool in Agent API (quote data), but not the UI experience. |
| **Voice input** | ✅ | ❌ | Web/mobile only. |
| **Standard cited Q&A (Fast/Quick/Best search)** | ✅ | ✅ Sonar / sonar-pro | The closest parity surface — but quality of citations differs (§5). |
| **Reasoning (chain-of-thought)** | ✅ UI modes | ⚠️ `sonar-reasoning-pro` exposes reasoning in a `refusal`/reasoning block; `sonar-deep-research` does NOT | |
| **Function calling / structured output** | n/a | ✅ | API-only advantage (Agent API / Sonar). |

### Summary — what *only* browser automation of the web can do (API impossible)
1. **Spaces/Collections** — create, populate, read, and share persistent research workspaces with files and custom instructions.
2. **Focus-mode/search-domain targeting** — Academic, Reddit, YouTube, Social, Math/Wolfram, Finance, video-scoped search.
3. **Image generation** and **image editing**.
4. **Comet-style agentic browsing** — logging into sites, filling forms, multi-tab workflows, under a real logged-in session.
5. **Model Council**, **Pages**, **Memory/personalization**, **connectors** (Google Docs etc.).
6. **Uploading arbitrary file types** (audio/video/spreadsheets) and having them persisted & searchable across the session.
7. **Pro Search-quality answers** (multi-step) without a separately-priced API tier.

---

## 2. API pricing structure & hidden costs

### 2.1 Official model (Sonar) pricing — token rates
| Model | Input ($/1M) | Output ($/1M) | Cache read ($/1M) | Best for |
|---|---|---|---|---|
| `sonar` (base) | $1.00 | $1.00 | — | high-volume factual lookups |
| `sonar-pro` (flagship) | $3.00 | $15.00 | — | complex queries, richer citations |
| `sonar-reasoning-pro` | $2.00 | $8.00 | — | multi-step reasoning |
| `sonar-deep-research` | $2.00 | $8.00 | +$2/1M citation +$3/1M reasoning | exhaustive research reports |
| Embeddings `pplx-embed-v1-0.6b` / `-4b` | $0.004 / $0.03 per 1M | — | — | context variants $0.008/$0.05 |

*(Note: an alternative "agent API model list" snippet from docs showed `perplexity/sonar` at $0.25/$2.50 — pricing changes between API generations; always re-verify against the live pricing page.)*

### 2.2 The hidden cost layer — **per-request fees** (this is what surprises everyone)
Perplexity bills **two ways at once**: token rates **PLUS** a flat per-request fee that scales with the "search context" setting (how much web content it retrieves).

**Sonar / Sonar Pro / Sonar Reasoning Pro — request fee per 1,000 requests (by search context):**
| Search context | `fast` | `pro` (Pro Search mode) |
|---|---|---|
| Low | $6 | $14 |
| Medium | $10 | $18 |
| High | $14 | $22 |

(Some versions of the pricing page quote base-Sonar request fees as $5/$8/$12 for low/med/high; the $6/$10/$14 ladder is the Pro-tier figure. **Verify current ladder** — this has been revised several times.)

**Why it hurts:**
- The request fee is **flat per call regardless of answer length** — a workload of many tiny queries is dominated by request fees, not tokens.
- `search_type: "auto"` silently routes complex queries to `pro` — request fee jumps from ~$6–14/1K to ~$14–22/1K **with no code change**. Your query mix drift changes your bill invisibly.
- Higher search context = more retrieved content = higher per-request fee.

**Sonar Deep Research — triple metering (reasoning + citations + search queries):**
- Base tokens: $2/$8 per 1M
- **Citation tokens: $2 per 1M**
- **Reasoning tokens: $3 per 1M** — and these dominate. Published example: one Deep Research call generated **339,594 reasoning tokens ≈ $1.02 in reasoning alone**, total call ≈ $1.32. A single Deep Research run can cost **$0.40 to >$1.00**.
- **Search queries: $5 per 1,000** queries fired inside the research loop (`searchQueries` meter).
- CoT tokens are *not* exposed in the API response — you pay for reasoning you never see.

**Other API surfaces:**
| API | Price | Billing unit |
|---|---|---|
| **Search API** (`POST /search`) | **$5 / 1,000 requests** | Per successful request; up to **5 queries per request = 1 billing unit**; invalid/rate-limited/unbilled; billed even for empty result sets; no token fees. |
| **Agent API `web_search`** tool | $0.005 / invocation | Per tool call (stacks with model tokens) |
| **Agent API `fetch_url`** | $0.0005 / invocation | |
| **Agent API `people_search` / `finance_search`** | $0.005 each / invocation | |
| **Sandbox** | ~$0.03 per 20-min session | + SDK search queries billed separately |

### 2.3 Hidden-cost cheat sheet (most common budget surprises)
1. **Request fees not in your mental model** → real cost ~2× your token-based estimate.
2. **Deep Research reasoning tokens** can cost dollars per call — "Running everything through Deep Research is the most common way to overspend."
3. **Output > input** — Sonar Pro output is $15/1M (5× input). Long gratuitous answers cost you.
4. **`auto` search routing** silently upgrades you to the expensive `pro` request tier.
5. **Raw Search API is cheapest for "I only need links"** — $5/1K requests, no tokens; far cheaper than Sonar for pure retrieval.
6. **Pro consumer subscription ≠ API pricing** — the $20/month Pro UI and the API are separate billing systems. Pro includes **~$5/month in API credits**, but API usage beyond that is metered at the full API rates. (Suprmind also notes Pro includes ~$40 in "Computer credits" for the Max-tier orchestrator — separate credit pool.)
7. **No monthly minimums; pay-as-you-go; prepaid credits**; request *fees* vs request *limits* use different units (see §3).

---

## 3. API rate limits by tier

Perplexity API rate limits are **usage tiers based on lifetime API credits purchased**, NOT on your consumer Pro/Max subscription (Enterprise plans get negotiated/custom limits separately).

### 3.1 Tier progression
| Tier | Total credits purchased (lifetime) | Label |
|---|---|---|
| Tier 0 | $0 | New accounts, limited access |
| Tier 1 | $50+ | Light usage |
| Tier 2 | $250+ | Regular usage |
| Tier 3 | $500+ | Heavy usage |
| Tier 4 | $1,000+ | Production |
| Tier 5 | $5,000+ | Enterprise |
*Tiers are cumulative lifetime purchases, not current balance; **no downgrade** once reached. Paid tiers unlock beta features.*

### 3.2 Sonar API rate limits (requests per minute)
| Tier | `sonar` / `sonar-pro` / `sonar-reasoning-pro` | `sonar-deep-research` | async POST | async GET status | async GET result |
|---|---|---|---|---|---|
| 0 | 50 | 5 | 5 | 3,000 | 6,000 |
| 1 | 150 | 10 | 10 | 3,000 | 6,000 |
| 2 | 500 | 20 | 20 | 3,000 | 6,000 |
| 3 | 1,000 | 40 | 40 | 3,000 | 6,000 |
| 4 | 4,000 | 60 | 60 | 3,000 | 6,000 |
| 5 | 4,000 | 100 | 100 | 3,000 | 6,000 |

`sonar-deep-research` is deliberately rate-limited far below the others (5–100 RPM) because each run fires hundreds of searches.

### 3.3 Search API rate limits
| Limit | Value |
|---|---|
| `POST /search` | **50 query-units/second**, burst capacity 50 (leaky bucket) |
| Tier dependence | **None** — same for all accounts |
| `max_results` | 1–20 (default 10) |
| Multi-query | up to 5 queries/request (consumes 5 rate-limit units but 1 billing unit) |

### 3.4 Agent API rate limits
| Tier | QPS | Requests/min |
|---|---|---|
| 0 | 1 | 50 |
| 1 | 3 | 150 |
| 2 | 8 | 500 |
| 3 | 17 | 1,000 |
| 4 | 33 | 4,000 (2,000 in older docs revision) |
| 5 | 33 | 8,000 (2,000 in older docs revision) |

### 3.5 Operational notes
- Overshoots return **HTTP 429 + `Retry-After`**; 429s are **not billed**.
- Algorithm is leaky-bucket → bursts OK, sustained traffic above average gets throttled.
- Above Tier 5: fill out a custom rate-limit-increase request form.
- A team can hold Enterprise *seats* but still need *API credits* for integration throughput — the two systems are separate.

---

## 4. Model availability differences

### 4.1 What the API exposes (access via `POST /chat/completions` / models, or Agent API)
- **Sonar family (native):** `sonar`, `sonar-pro`, `sonar-reasoning-pro`, `sonar-deep-research` (+ embeddings).
- **Agent API (2026):** third-party frontier models served at **direct provider rates with no markup**, e.g. `openai/gpt-5.6-sol`, Nemotron 3 Ultra (`perplexity/nemotron-3-ultra-550b-a55b`), Nemotron 3.5 Lightning, plus OpenAI/Anthropic/Google/xAI via the agent gateway. Function-calling + JSON structured output supported.

### 4.2 What the web exposes that the API does not (per surface)
**Web Chat (Pro plan) — search models:**
| Model | Provider | Pro | Max | Notes |
|---|---|---|---|---|
| Sonar 2 | Perplexity | ✅ | ✅ | default |
| GPT-5.6 Terra | OpenAI | ✅ | ✅ | Thinking optional |
| GPT-5.6 Sol | OpenAI | ❌ | ✅ | |
| Gemini 3.1 Pro | Google | ✅ | ✅ | Thinking always on |
| Claude Sonnet 5 | Anthropic | ✅ | ✅ | Thinking optional |
| Claude Opus 5 | Anthropic | ❌ | ✅ | |
| Kimi K3 | Moonshot AI | ✅ | ✅ | |
| GLM 5.2 | Z.ai | ✅ | ✅ | |
| Grok 4.5 | xAI | ✅ | ✅ | excluded for Enterprise |
| Nemotron 3 Ultra | NVIDIA | ✅ | ✅ | |
*(Current default set as of Jul 2026: GPT-5.6 Sol w/ Thinking, Claude Opus 5 w/ Thinking, Gemini 3.1 Pro w/ Thinking — "Model Council" default.)*

Why this matters for automation:
- **Model Council** and per-thread **model switching between 3rd-party frontier models** is a web-UI feature with no 1:1 API equivalent on the Sonar path (the Agent API gives you 3rd-party models at provider rates, but not Perplexity's curated web UI selection, Model Council ensemble comparisons, or "Best"/auto routing with the same defaults).
- Max-only models (GPT-5.6 Sol, Claude Opus 5) are **web-only** unless you call those providers' own APIs through the Agent API at full provider price.
- The web's Sonar is "Sonar 2"; the API's base `sonar` is a different, older/smaller generation — a concrete reason API answers differ.

---

## 5. Output quality differences (web vs API, same query)

**Consensus across Reddit + official forum: the web/UI is better, and it is intentionally so.**

Official forum (Perplexity API Platform forum, "Why don't I receive the same level of response using the API as I do using the official UI search?"):
> "The answers you get in the UI will likely always be better than the answers from the API — it's not only intentional, it's in Perplexity's best interest to do so financially. If their API gave the same results as their UI did, there would be no reason to use their UI as opposed to a competitor wrapping their API in a better interface." — Several Perplexity Discord moderators have additionally stated there is **no intention of matching API output quality to the UI.**

Documented causes of the gap:
1. **Pro Search is web-only** — the multi-step reasoning loop that produces the better UI answers has no API support; the API returns default-style answers.
2. **Different search subsystem / citation quality** — users repeatedly report the API "does not quote the same references" and UI citations are higher quality and more relevant, implying different retrieval configuration under the hood.
3. **Different profile/system prompts** — Perplexity uses different (richer) system prompts in the consumer app than in the API ("They use different profile prompts for perplexity vs the api"), including injected personalization/memory.
4. **Different model generation** — web runs Sonar 2 / frontier models at higher capability; API `sonar` is the lighter variant.
5. **Different content license** — one r/n8n thread notes the API lacks the same content licensing the web chat has, which they attribute to reduced accuracy in API results.
6. Real-world examples: soccer scores (web got the right score/scorer/opponent; API failed); "results wildly different to web app."

**Practical implications for automation:**
- If you automate the **web UI**, you get Pro-Search class answers + better citations + memory, for the cost of your browser session (free/Pro subscription), but at the cost of fragility, slower throughput, and rate-limit caps (§3 consumer ≠ API).
- If you automate the **API**, you get consistency/JSON/rate-limit transparency but knowingly-second-tier answer quality.
- This asymmetry is *the* core justification for browser-level Perplexity automation.

---

## 6. Third-party Perplexity-like alternatives

Not every "Perplexity-like" service produces *synthesized answers* — the category splits into (a) **raw SERP/retrieval APIs** (you do the synthesis with your own LLM) and (b) **end-to-end answer/research providers** (Perplexity-like).

### 6.1 Comparison matrix (as of Aug 2026 — verify live)
| Provider | Type | API pricing | Free tier | Strong at | Weak at |
|---|---|---|---|---|---|
| **Perplexity (Sonar)** | Synthesized answer + citations | $5/1K Search; Sonar $1–$15/1M tokens + request fees; DR fees | $0 — 50 RPM, Tier 0 | Highest-quality cited answers, Deep Research | Request fees, Deep Research costs, API quality < UI, no file persistence |
| **OpenAI web search (SearchGPT tech, Responses API `web_search` tool)** | Synthesized answer + search | **$10/1,000 calls + search-content tokens** (billed at model input rate) for most models; gpt-5/o-series preview $10/1K + tokens; non-reasoning preview **$25/1K with content tokens free** | API $5 credit/month | Deep search/snippet grounding with OpenAI models; inline citation deep-links | Cost per call high; no dedicated "Perplexity-style" research loop by default; tied to OpenAI models |
| **Tavily** | Raw search/extract API for agents | ~$5/1K + extraction; paid plans from ~$25–30/mo, top ~$100/mo + enterprise | 1,000 credits/month | Agent/RAG search+extract, per-source scoring, MCP/LangChain integration | No synthesized answer generation (that's your LLM's job) |
| **Exa (formerly Metaphor)** | Neural/semantic search API | `/search` **$7/1K** (incl. 10 results); `/contents` $1/1K pages; `/answer` $5/1K; `/monitors` $15/1K; deep search $12/1K; deep-reasoning $15/1K | **$20 free credits + ~$10/mo recurring** (~2,800 searches) | Semantic recall on exploratory queries, own index (not a Google wrapper), best MCP support, neural search | Cost adds up at scale; weaker on exact-keyword lookups; extra results/summaries are separate line items |
| **Serper** | Google SERP API (structured JSON) | Starter **$50/mo** (50K queries ≈ $1/1K); Standard $375/mo (500K ≈ $0.75/1K); Scale/Ultimate higher | **2,500 free queries**, no card | Raw Google rankings, knowledge graph, people-also-ask, speed (1–2s), LangChain wrapper | Google-only; no synthesis; paid pricing client-side rendered |
| **You.com** | Search + synthesis APIs | Web Search **$5/1K** (≤100 results incl. full page content); Contents $1/1K pages; **Answer API $5/1K** (synthesized, cited, 93.5% SimpleQA); Research API from **$12/1K** | 100 queries/day + **$100 free credit** | All-in-one: search + extraction + synthesized answered + research tiers; SOC2, ZDR | Research API priced per-tier; newer/less battle-tested than Perplexity |
| **Phind** | Consumer dev search (no public API in 2026) | n/a (consumer Pro **$15/mo**) | Free tier | Developer/technical answers, code search, paired programming | **No API for automation** — effectively web-only; consumer-focused |
| *(mention)* **Brave Search API**, **Firecrawl**, **Kagi** | Raw SERP / scrape+extract / consumer | Brave ~$3–5/1K; Firecrawl free-$599/mo; Kagi $5–14/mo | varies | SERP coverage, scraping, privacy | No synthesis (except Kagi Assistant) |

### 6.2 Which to pick for what
- **Raw retrieval pipeline you control** → Tavily (agent-friendly extraction) or Exa (semantic/neural) or Serper (cheap structured Google results), pair with your own LLM for synthesis.
- **Drop-in Perplexity replacement that is API-first** → **You.com Answer/Research API** or **OpenAI web search** (if you're already on OpenAI models). Perplexity's own API is competitive but remember the UI-quality gap (§5).
- **Deep multi-source research at API scale** → Perplexity `sonar-deep-research` or You.com Research API (Exa agent endpoint, if you want a raw-search loop, but "up to $1.00 per single run" at high effort).
- **Google SEO/rank data only** → Serper is purpose-built.
- **Consumer-quality dev search, not automation** → Phind.

---

## 7. Known workarounds to get more from Perplexity

### A. API-side workarounds (replicate web features)
1. **Focus mode via undocumented `search_focus` param.** The API schema has no `focus_mode`, but community findings report an undocumented `search_focus` parameter on the chat/completions endpoint that mirrors web focus modes: `academic`, `writing`, `math`, `video`, `social` (and others). *Caveat: undocumented, not supported, may break* — but it's the closest programmatic equivalent to web Focus modes.
2. **Prompt-injected focus.** When you need source-domain control, use a system prompt as a workaround (e.g. "Focus mode: Academic. Search only academic sources." / "You are a search assistant that returns results only from [domain]") + `temperature: 0`; strengthen with a "CRITICAL" marker if the model ignores it. Not reliable, but commonly reported to help.
3. **Replicate Deep Research for cheaper:** use `sonar-reasoning-pro` as a fallback when `sonar-deep-research` is rate-limited or too expensive on Tier 0 (its reasoning tokens stack up per run).
4. **Batch queries to save request fees:** put up to 5 related queries in one Search API request (1 billing unit, 5 rate-limit units) — cheaper than 5 single calls.
5. **Use Search API + your own LLM** instead of Sonar for link-extraction workloads → $5/1K flat vs token+request-fee metering of Sonar.
6. **Control Deep Research cost:** set `reasoning_effort` low, search context Low by default, reserve High for the queries that need it.
7. **Cache aggressively** — repeated queries re-run paid searches; caching kills the request-fee line entirely.

### B. Web-UI workarounds (the ones that justify browser automation)
8. **Pro Search quota management:** Pro Search (web) is capped (Free ~3/day; Pro reports ~300/day). Every follow-up in a Pro-Search thread burns a Pro query. Workaround: use **Pro Search only for the initial deep query**, then continue the thread with **Quick/Best (standard, unlimited)** searches — the thread context persists and standard search handles follow-ups fine. Counter resets at midnight UTC (or rolling 24h on Free — sources differ).
9. **Free-tier Deep Research spacing:** Deep Research/Research allowance on Free is tiny (has dropped from ~5/day in mid-2026 to **1/month** per the July 22, 2026 help center). Split multi-day research projects across daily credit refresh windows; do broad context day 1, deep analysis day 2. Standard searches are unlimited and fill the gap.
10. **Structure via prompt:** when out of Pro/Research budget, force structure with explicit prompting — "Summarize the three strongest arguments for and against X, with citations ranked by publication date."
11. **Dead-link recovery:** if citations 404, click the citation's preview panel (full text may already be extracted), or fall back to web.archive.org / `cache:` queries.
12. **Free image-gen limit (3/day)** and **free file uploads (3/day)** — the web caps them, but they're still more generous than the API (which has no image gen at all).
13. **Focus modes on the free tier** can gate quality: e.g. Academic focus gets peer-reviewed sources without Pro spend; use the default globe icon toggle before searching.
14. **"Focus mode confusion" is a real failure mode**: if citations vanish or answers degrade, check you're not in a mismatched focus mode — reset to All/Web.
15. **Browser automation + logged-in session** unlocks all web-only features (§1) at consumer-plan cost — including Comet-like agentic behavior, Model Council, Spaces, and image generation — which is the whole point of the parent skill. (See §9 for cost/risk.)

### C. Workarounds to avoid / stability warns
- Using **Perplexity's private web/internal API** (reversing `perplexity.ai` endpoints) works but is **explicitly unsupported, TOS-fragile, and breaks on updates**. Treat any such integration as throwaway and design fallbacks.
- VPN/network switching to refresh free-tier allocations is anecdotally reported; unreliable and TOS-questionable.
- API usage during peak hours and UI "throttling" both degrade; schedule heavy runs off-peak.

---

## 8. Free vs Pro vs Max feature comparison

**Plans (2026):** Free $0 · Pro $20/mo ($200/yr ≈ $16.67/mo) · Education Pro $10/mo (verified students) · Max $200/mo · Enterprise Pro $40/user/mo · Enterprise Max ~$325/user/mo.

> ⚠️ **Variance warning:** Perplexity has changed free-tier caps repeatedly in 2026 (Pro Searches 5/day → 3/day; Deep Research 5/day → "Research" 1/month; file/images 3/day). Figures below are the best-available latest snapshot (Jul 2026 in many rows); treat exact counts as "check the help center today."

| Feature | Free ($0) | Pro ($20/mo) | Max ($200/mo) |
|---|---|---|---|
| Basic/Quick/Best searches | ✅ unlimited | ✅ unlimited | ✅ unlimited |
| **Pro Search** | ⚠️ ~3/day (was 5/day) | ✅ effectively unlimited (reports of ~300/day soft cap) | ✅ highest limits |
| **Research (Deep Research)** | ⚠️ **1/month** (was 5/day) | ✅ hundreds/day (wide allowance) | ✅ highest, on Claude Opus backbone |
| Model selection (3rd-party frontier: GPT, Claude, Gemini…) | ❌ auto-assigned | ✅ manual per-thread (Pro palette) | ✅ full palette incl. Anthropic Opus / GPT-5.6 Sol |
| **Model Council** (multi-model answers) | ❌ | ❌ | ✅ |
| **File uploads** | ⚠️ ~3/day (≤25–40 MB) | ✅ unlimited-ish, 50 MB/file, 10 files/prompt, 90-day retention | ✅ higher caps |
| **Spaces** | ⚠️ limited | ✅ up to 50 files/Space, full collaboration | ✅ full + enterprise tooling |
| **Image generation** | ✅ 3/day (non-commercial) | ✅ unlimited (GPT Image, Nano Banana, Seedream) | ✅ unlimited + Computer tools |
| **Pages** | ⚠️ basic | ✅ full | ✅ full |
| **Memory & personalization** | ✅ basic | ✅ full (~95% recall per marketing) | ✅ highest |
| **Labs features** | ❌ | ✅ | ✅ |
| **Connectors (400+ apps)** | ❌ (Enterp. mostly) | ✅ (Pro) | ✅ |
| **Comet browser** | ✅ (free rollout) | ✅ | ✅ (+early access priority) |
| **Perplexity Computer / Scheduled tasks / Email Asst.** | ❌ | ❌ (Computer credits to sample: ~$40) | ✅ main surface |
| **API credits** | — | ~**$5/mo API credits** | 10,000 monthly credits + 35,000 bonus |
| **Priority support / early features** | ❌ | ❌/partial | ✅ |

**Enterprise delta (Pro/Max at $40/$325 per user/mo):** SSO, shared Spaces, admin controls, data-privacy guarantees, "Choose sources" (Web / Org Files / Web+Org / None) replacing Focus mode, internal knowledge search over org files, 1 GB file uploads, 30–500+ files per Space, one-year retention.

**Bottom line for an automation skill:** The **free tier is a deliberately starving tier** (a few Pro Searches/day, 1 Research/month, 3 images/files/day). **Pro at $20/mo is the practical automation substrate** — unlimited Pro Search, model switching, full Spaces, generous file/image limits — and it's what a browser-automation build should target. Max mostly adds Computer/agentic + Model Council + top models, which are nice-to-haves but not required to unlock the core web-only value.

---

## 9. Implications for web automation

1. **Why browser automation is justified:** No API surface provides Pro-Search quality, Spaces/Collections, Focus-mode-restricted search, image generation, model council, connectors, or Comet-level agentic browsing. These are web-only, so any skill that needs them must drive the web UI (or reverse its endpoints at risk).
2. **Cost math favors the UI for many workloads:** Pro UI (unlimited Pro Searches + 3 Research-capable… careful: Research is still capped on Pro but generous; file/image unlimited) can beat API pay-per-token for moderate-volume human-paced research. API wins for programmatic high-volume, JSON-shaped workloads.
3. **Design for UI-version drift:** Focus modes were already removed/restored on web once in mid-2026; free caps changed 3× in one year; the interface changes without notice. A web-automation skill must: detect "Pro Search limit reached", "Research limit", "Focus removed", dialogs, and login walls as first-class states, and re-locate controls by text/AX rather than fixed coordinates.
4. **Rate-limit caps are per-account, not per-session** — an automation that burns 300 Pro Searches/day hits a real wall (midnight UTC reset). Plan for it (batch, cache, off-peak).
5. **Against API-abuse detection:** automated web queries trigger the same rate-limit machinery as humans; keep concurrency modest (a few QPS) and human-like, and avoid the private internal API unless you accept breakage risk.
6. **Checkpoint the value:** the features that *only* the web delivers (§1 summary) are exactly the ones the parent skill should automate. Everything else is cheaper/faster via API or a third-party (§6).

---

## 10. Sources
- Perplexity API docs — Pricing: `docs.perplexity.ai/docs/getting-started/pricing`
- Perplexity API docs — Rate Limits & Usage Tiers: `docs.perplexity.ai/docs/admin/rate-limits-usage-tiers`
- Perplexity API FAQ: `docs.perplexity.ai/docs/resources/faq`
- Perplexity official forum — API vs UI quality: `community.perplexity.ai/t/why-dont-i-receive-the-same-level-of-response-using-the-api-as-i-do-using-the-official-ui-search/116`
- Perplexity Help Center — Subscription plans & rate limits: `perplexity.ai/help-center/en/articles/11187416-which-perplexity-subscription-plan-is-right-for-you.html`
- Perplexity Help Center — Image generation: `perplexity.ai/help-center/en/articles/10354781-generating-images-with-perplexity`
- Perplexity Help Center — File uploads: `perplexity.ai/help-center/en/articles/10354807-file-uploads`
- Perplexity Help Center — Models in subscription: `perplexity.ai/help-center/en/articles/10354919-what-advanced-ai-models-are-included-in-my-subscription.html`
- Perplexity API docs — Agent API models / image attachments: `docs.perplexity.ai/docs/agent-api/models`, `/docs/agent-api/image-attachments`
- Suprmind — Perplexity features & pricing: `suprmind.ai/hub/perplexity/features`, `/perplexity/pricing/`
- Developer.puter.com — Perplexity API pricing breakdown (Jun 2026)
- Amnic — Perplexity API pricing two-layer structure (Jun/Aug 2026)
- perplexityaimagazine.com — API rate limits explained (2026); File upload limit; Collections guide
- OneHuman — Free-tier caps reconfirmed (Aug 5, 2026); BuyersPrint — Free vs Pro (Apr 2026); Datastudios — Free vs Pro search; file uploads
- Reddit r/perplexity_ai — API vs web quality threads (multiple)
- WiseChecker — Focus mode API workaround (`search_focus`); Social/YouTube focus guides
- Tavily — `tavily.com`; Exa — `exa.ai/pricing` (API tab); Serper — `serper.dev` (via costbench/webscraping.cc)
- You.com — `you.com/pricing` (Web Search $5/1K, Contents $1/1K, Answer $5/1K, Research $12/1K)
- OpenAI API pricing — `developers.openai.com/api/docs/pricing` (web search $10/1K + content tokens)
- AISO Tools — Phind pricing ($15/mo Pro; no public API)
