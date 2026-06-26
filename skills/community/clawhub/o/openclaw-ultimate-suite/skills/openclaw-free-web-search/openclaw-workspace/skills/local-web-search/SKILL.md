---
name: local-web-search
description: >
  Free, private, real-time web search for any OpenClaw commander model — zero API keys required.
  Powered by self-hosted SearXNG + Scrapling anti-bot engine. Multi-engine
  parallel search (Bing/DuckDuckGo/Google/Startpage/Qwant), intent-aware
  Agent Reach query expansion, three-tier Browse/Viewing (Fetcher →
  StealthyFetcher → DynamicFetcher for Cloudflare/JS sites), cross-engine
  anti-hallucination validation, multi-source factual claim cross-verification
  with confidence scoring, automatic proxy detection, and automatic public fallback.
homepage: https://github.com/wd041216-bit/openclaw-free-web-search
metadata:
  clawdbot:
    emoji: "🔍"
    requires:
      env: []
    files: ["scripts/*"]
---

# Local Free Web Search v4.1

> **Model-agnostic.** Works with Claude, GPT-4, Gemini, Mistral, Llama, DeepSeek, and any other model configured as your OpenClaw commander.

Use this skill when the agent needs current or real-time web information.
Powered by **Scrapling** (anti-bot) + **SearXNG** (self-hosted search).
Zero API keys. Zero cost. Runs entirely locally.

---

## Compatibility

This skill is designed for **any LLM that can run shell commands via OpenClaw's tool interface**. It does not rely on any model-specific API, function-calling format, or proprietary feature. The three tools are standard Python scripts invoked via `python3` — any model that can execute a shell command can use this skill.

| Commander model | Compatible |
|---|---|
| Claude (Anthropic) | ✅ |
| GPT-4 / GPT-4o (OpenAI) | ✅ |
| Gemini 1.5 / 2.0 (Google) | ✅ |
| Mistral / Mixtral | ✅ |
| Llama 3 / 3.1 (Meta) | ✅ |
| DeepSeek | ✅ |
| Qwen | ✅ |
| Any model with shell tool access | ✅ |

---

## External Endpoints

| Endpoint | Data Sent | Purpose |
|---|---|---|
| `http://127.0.0.1:18080` (local) | Search query string only | Local SearXNG instance |
| `https://searx.be` (fallback only) | Search query string only | Public fallback when local SearXNG is down |
| Any URL passed to `browse_page.py` | HTTP GET request only | Fetch page content for reading |
| URLs found in search results (via `verify_claim.py`) | HTTP GET request only | Multi-source cross-validation |

No personal data, no credentials, no conversation history is ever sent to any endpoint.

---

## Security & Privacy

- All search queries go to your **local SearXNG** instance by default — no third-party tracking
- Public fallback (`searx.be`) is only used when local service is unavailable, and only receives the raw query string
- `browse_page.py` makes standard HTTP GET requests to URLs you explicitly pass — no data is posted
- Scrapling runs entirely locally — no cloud API calls, no telemetry
- No API keys required or stored
- No conversation history or personal data leaves your machine

**Trust Statement:** This skill sends search queries to your local SearXNG instance (default) or `searx.be` (fallback). Page content is fetched via standard HTTP GET. No personal data is transmitted. Only install if you trust the public SearXNG instance at `searx.be` as a fallback.

---

## Proxy Support

Both `search_local_web.py` and `browse_page.py` support proxies automatically:

- If `LOCAL_SEARCH_PROXY`, `HTTPS_PROXY`, or `ALL_PROXY` environment variable is set, it will be used
- If no proxy env var is set, the skill **auto-detects** common local proxies on `127.0.0.1:7890`, `7897`, and `1080`
- For `stealth` and `dynamic` modes, the skill prefers an installed local Chrome browser when available (checks `/Applications/Google Chrome.app`), so it can work even before Playwright finishes downloading its own Chromium bundle

---

## Tool 1 — Web Search

```bash
python3 ~/.openclaw/workspace/skills/local-web-search/scripts/search_local_web.py \
  --query "YOUR QUERY" \
  --intent general \
  --limit 5
```

**Intent options** (controls engine selection + query expansion):

| Intent | Best for |
|---|---|
| `general` | Default, mixed queries |
| `factual` | Facts, definitions, official docs |
| `news` | Latest events, breaking news |
| `research` | Papers, GitHub, technical depth |
| `tutorial` | How-to guides, code examples |
| `comparison` | A vs B, pros/cons |
| `privacy` | Sensitive queries (ddg/startpage/qwant only) |

**Additional flags:**

| Flag | Description |
|---|---|
| `--engines bing,duckduckgo,...` | Override engine selection |
| `--freshness hour\|day\|week\|month\|year` | Filter by recency |
| `--max-age-days N` | Downrank results older than N days |
| `--browse` | Auto-fetch top result with browse_page.py |
| `--no-expand` | Disable Agent Reach query expansion |
| `--json` | Machine-readable JSON output |

---

## Tool 2 — Browse/Viewing (read full page)

```bash
python3 ~/.openclaw/workspace/skills/local-web-search/scripts/browse_page.py \
  --url "https://example.com/article" \
  --max-words 600
```

**Fetcher modes** (use `--mode` flag):

| Mode | Fetcher | Use case |
|---|---|---|
| `auto` | Tier 1 → 2 → 3 | Default — tries fast first |
| `fast` | `Fetcher` | Normal sites |
| `stealth` | `StealthyFetcher` | Cloudflare / anti-bot sites |
| `dynamic` | `DynamicFetcher` | Heavy JS / SPA sites |

Returns: title, published date, word count, confidence (HIGH/MEDIUM/LOW),
full extracted text, and anti-hallucination advisory.

---

## Tool 3 — Factual Claim Cross-Verification

```bash
python3 ~/.openclaw/workspace/skills/local-web-search/scripts/verify_claim.py \
  --claim "Claude 3.7 was released on February 24, 2025" \
  --sources 5
```

**What it does:**
1. Expands the claim into 3 search query variants
2. Searches across multiple engines and collects up to N unique sources
3. Fetches each source page via Scrapling cascade
4. Classifies each source as AGREE / CONTRADICT / NEUTRAL
5. Weights by domain authority (Wikipedia/Reuters/official sites = HIGH)
6. Outputs a structured verdict with confidence score

**Verdict levels:**

| Verdict | Confidence | Meaning |
|---|---|---|
| `VERIFIED` ✅ | ≥75% | Majority of high-authority sources agree |
| `LIKELY_TRUE` 🟢 | 55–74% | Most sources agree, some low-authority |
| `UNCERTAIN` 🟡 | 35–54% | Sources disagree or insufficient data |
| `LIKELY_FALSE` 🔴 | 15–34% | Majority of sources contradict |
| `UNVERIFIABLE` ⬜ | <15% | No relevant sources found |

**Flags:**

| Flag | Description |
|---|---|
| `--sources N` | Number of sources to check (default: 5, max recommended: 10) |
| `--urls URL1 URL2 ...` | Skip search, verify against known URLs directly |
| `--searxng-url URL` | Override SearXNG URL |
| `--json` | Machine-readable JSON output |

---

## Recommended Workflow

**Standard (search + read):**
1. Run `search_local_web.py` — review results by Score and `[cross-validated]` tag
2. Run `browse_page.py` on the top URL — check Confidence level
3. If Confidence is LOW (paywall/blocked) — retry with `--mode stealth` or try next URL
4. Answer only after reading HIGH-confidence page content
5. **Never state facts from snippets alone**

**Fact-checking (verify a specific claim):**
1. Run `verify_claim.py --claim "..."` — get multi-source verdict
2. Check `confidence` score and `sources_agreeing` / `sources_contradicting` counts
3. Read the `evidence[].excerpt` for each source to understand context
4. Only assert the claim if verdict is `VERIFIED` or `LIKELY_TRUE`
5. If `UNCERTAIN` or `LIKELY_FALSE`, tell the user the claim could not be verified

---

## Rules

- Always use `--intent` to match the query type for best results.
- When local SearXNG is unavailable, both scripts automatically fall back to `searx.be`.
- If the fallback also fails, tell the user to start local SearXNG:

```bash
cd "$(cat ~/.openclaw/workspace/skills/local-web-search/.project_root)" && ./start_local_search.sh
```

- Do NOT invent search results if all sources fail.
- `search_local_web.py` and `browse_page.py` are complementary: **search first, browse second**.
- Prefer `[cross-validated]` results (appeared in multiple engines) for factual claims.
- For sites behind Cloudflare or requiring JS, use `browse_page.py --mode stealth`.
- For specific factual claims (dates, numbers, names, events), use `verify_claim.py` to get a multi-source confidence score before asserting.
- **Never assert a claim with `UNCERTAIN`, `LIKELY_FALSE`, or `UNVERIFIABLE` verdict** — tell the user the evidence is insufficient instead.
- **This skill works identically regardless of which LLM model is acting as the OpenClaw commander.** No model-specific behavior is assumed.
