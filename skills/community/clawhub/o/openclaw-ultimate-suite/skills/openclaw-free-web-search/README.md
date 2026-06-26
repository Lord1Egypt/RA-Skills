# OpenClaw Free Web Search v4.1

> **Zero-cost · Zero-API-key · Privacy-first · Model-agnostic**
> The only free OpenClaw web search skill that tells you **how much to trust the answer** — and works with **any LLM** you configure as your commander.

[中文文档](./README_zh.md) · [Report Issue](https://github.com/wd041216-bit/openclaw-free-web-search/issues)

---

## What makes this different

Most free OpenClaw search skills give you a list of URLs. This skill gives you a **verdict**.

Every answer produced by this skill comes with a confidence score backed by multi-source cross-validation. Before your agent asserts a fact, it checks that fact against 3–10 independent sources, weights them by domain authority, and tells you whether the claim is `VERIFIED`, `LIKELY_TRUE`, `UNCERTAIN`, or `LIKELY_FALSE`. No other free skill in the community does this.

v4.1 adds **automatic proxy detection** and **local Chrome detection** — so the skill works out of the box on machines running Clash, V2Ray, or any other local proxy, without any manual configuration.

---

## Model compatibility — any commander, any LLM

This skill is fully model-agnostic. It uses standard Python scripts invoked via shell commands. Any LLM that can run a shell command can use it — whether running locally via Ollama or vLLM, or accessed via API.

| Commander model | Compatible |
|---|---|
| Claude 3.5 / 3.7 (Anthropic) | ✅ |
| GPT-4 / GPT-4o (OpenAI) | ✅ |
| Gemini 1.5 / 2.0 (Google) | ✅ |
| Mistral / Mixtral | ✅ |
| Llama 3 / 3.1 (Meta) | ✅ |
| DeepSeek V3 / R1 | ✅ |
| Qwen 3 / Qwen3-Coder (Alibaba) | ✅ |
| Any model with shell tool access | ✅ |

---

## What's new in v4.1

| Change | Details |
|---|---|
| **Model-agnostic** | Explicit compatibility declaration in SKILL.md and AGENTS.md; no model-specific assumptions anywhere |
| **Proxy auto-detection** | Both `search_local_web.py` and `browse_page.py` auto-detect local proxies on ports 7890, 7897, 1080 before falling back to direct connection |
| **Local Chrome detection** | `browse_page.py` detects `/Applications/Google Chrome.app` and passes `real_chrome=True` to StealthyFetcher/DynamicFetcher for better anti-bot evasion |
| **TLS relaxation for local proxies** | When a local MITM proxy (Clash, mitmproxy) is detected, TLS verification is automatically relaxed to prevent certificate errors |
| **AGENTS.md Step 3** | Standard workflow now includes `verify_claim.py` as an explicit third step |

---

## Three-tool architecture

```
OpenClaw Agent (any model)
    │
    ├── 1. search_local_web.py   ← Find relevant URLs
    │       ├── Intent-aware query expansion (Agent Reach)
    │       ├── Parallel multi-engine: Bing + DDG + Google + Startpage + Qwant
    │       ├── Quality scoring: authority (35%) + freshness (20%) + cross-engine (20%)
    │       │                    + snippet density (15%) + title quality (10%)
    │       ├── Paywall / 404 / login-wall filter
    │       ├── Proxy auto-detection (env vars + ports 7890/7897/1080)
    │       └── SearXNG (local) → public fallback (searx.be)
    │
    ├── 2. browse_page.py        ← Read a page deeply
    │       ├── Tier 1: Scrapling Fetcher (TLS fingerprint spoofing, ~1–3s)
    │       ├── Tier 2: StealthyFetcher (Cloudflare Turnstile bypass, ~5–15s)
    │       ├── Tier 3: DynamicFetcher (full Playwright JS rendering, ~10–30s)
    │       ├── Tier 4: stdlib urllib (no-Scrapling graceful fallback)
    │       ├── Proxy auto-detection + local Chrome detection (macOS)
    │       ├── Adaptive CSS content extraction
    │       ├── Paywall detection + publication date extraction
    │       └── Confidence: HIGH / MEDIUM / LOW
    │
    └── 3. verify_claim.py       ← How much should I trust this?
            ├── Expands claim into 3 search query variants
            ├── Fetches 3–10 independent sources in parallel
            ├── Classifies each source: AGREE / CONTRADICT / NEUTRAL
            ├── Authority-weighted confidence (Wikipedia/Reuters = 3×; Reddit = 1×)
            ├── Cross-agreement bonus (agreeing sources reinforce each other)
            ├── --urls direct mode: verify against known URLs, no SearXNG needed
            └── Verdict: VERIFIED / LIKELY_TRUE / UNCERTAIN / LIKELY_FALSE / UNVERIFIABLE
```

---

## Recommended workflow

```
User question
    │
    ▼
search_local_web.py  →  top 5 URLs + quality scores + [cross-validated] tags
    │
    ▼
browse_page.py       →  full page content, Confidence: HIGH / MEDIUM / LOW
    │                   retry with --mode stealth for Cloudflare-protected sites
    ▼
verify_claim.py      →  multi-source verdict before asserting key facts
    │                   VERIFIED / LIKELY_TRUE → answer confidently with citation
    │                   UNCERTAIN / LIKELY_FALSE → tell the user explicitly
    ▼
Answer with source URL + publication date + confidence level
```

---

## Requirements

- macOS (Apple Silicon or Intel)
- Python 3.8+
- OpenClaw desktop app

**Optional but strongly recommended (enables anti-bot bypass):**

```bash
pip install scrapling[all]
python -m playwright install chromium
```

The install script handles all of this automatically.

---

## Quick start

```bash
# 1. Clone
git clone https://github.com/wd041216-bit/openclaw-free-web-search.git
cd openclaw-free-web-search

# 2. One-click install (SearXNG + Scrapling + Playwright)
./install_local_search.sh

# 3. Start SearXNG
./start_local_search.sh

# 4. Sync skill into OpenClaw workspace
./sync_openclaw_workspace.sh

# 5. Restart OpenClaw — all three tools are now active
```

---

## Usage

### 1. Web search

```bash
python3 ~/.openclaw/workspace/skills/local-web-search/scripts/search_local_web.py \
  --query "Claude 4 release date" --intent news --limit 5

# Search + auto-browse top result
python3 ... --query "DeepSeek V3 architecture" --intent research --browse

# Downrank results older than 30 days
python3 ... --query "AI model rankings" --max-age-days 30
```

### 2. Browse a page

```bash
# Auto mode (Scrapling cascade: fast → stealth → dynamic)
python3 ~/.openclaw/workspace/skills/local-web-search/scripts/browse_page.py \
  --url "https://example.com/article" --max-words 600

# Force stealth (Cloudflare-protected sites)
python3 ... --url "https://..." --mode stealth

# Full JS rendering (SPAs, React apps)
python3 ... --url "https://..." --mode dynamic
```

### 3. Verify a claim

```bash
# Auto mode: SearXNG finds sources automatically
python3 ~/.openclaw/workspace/skills/local-web-search/scripts/verify_claim.py \
  --claim "DeepSeek V3 was released in 2025 with 671B parameters" \
  --sources 5

# Direct URL mode: no SearXNG needed
python3 ... \
  --claim "DeepSeek V3 was released in 2025 with 671B parameters" \
  --urls https://deepseek.com/blog/... \
         https://en.wikipedia.org/wiki/DeepSeek

# Machine-readable JSON output
python3 ... --claim "..." --json
```

**Example output:**

```
VERDICT    : 🟢 LIKELY_TRUE
CONFIDENCE : 72%
SOURCES    : 4 checked  (3 agree / 0 contradict / 1 neutral)
MODE       : FULL (Scrapling + StealthyFetcher)

[1] ✅ deepseek.com  [HIGH]  score=0.87
    Excerpt: "DeepSeek-V3, a strong Mixture-of-Experts (MoE) language model with 671B total parameters..."

[2] ✅ en.wikipedia.org  [HIGH]  score=0.85

[3] ✅ arxiv.org  [HIGH]  score=0.81

[4] ➖ techcrunch.com  [HIGH]  score=0.44
```

---

## Verdict reference

| Verdict | Confidence | Meaning |
|---|---|---|
| ✅ VERIFIED | ≥ 75% | Multiple high-authority sources agree |
| 🟢 LIKELY_TRUE | 55–74% | Majority of sources support the claim |
| 🟡 UNCERTAIN | 35–54% | Mixed or insufficient evidence |
| 🔴 LIKELY_FALSE | 15–34% | Multiple sources contradict the claim |
| ⬜ UNVERIFIABLE | < 15% | Cannot find relevant sources |

---

## Intent options (search_local_web.py)

| Intent | Best for | Engines used |
|---|---|---|
| `general` | Default | bing, ddg, google |
| `factual` | Facts, docs, definitions | bing, google, ddg |
| `news` | Breaking news, recent events | bing, ddg, google |
| `research` | Papers, GitHub, technical | google, startpage, bing |
| `tutorial` | How-to, code examples | google, bing, ddg |
| `comparison` | A vs B, reviews | google, bing, startpage |
| `privacy` | Sensitive queries | ddg, startpage, qwant |

---

## Fetcher modes (browse_page.py)

| Mode | Engine | Use case | Speed |
|---|---|---|---|
| `auto` | Tier 1 → 2 → 3 | Default, tries fastest first | variable |
| `fast` | Scrapling `Fetcher` | Normal sites, TLS spoof | ~1–3s |
| `stealth` | `StealthyFetcher` | Cloudflare, anti-bot | ~5–15s |
| `dynamic` | `DynamicFetcher` | Heavy JS / SPA | ~10–30s |

---

## Management

```bash
./start_local_search.sh    # Start SearXNG
./stop_local_search.sh     # Stop SearXNG
./doctor.sh                # Health check (SearXNG + Scrapling + Playwright)
```

---

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `LOCAL_SEARCH_URL` | `http://127.0.0.1:18080` | Local SearXNG base URL |
| `LOCAL_SEARCH_FALLBACK_URL` | `https://searx.be` | Public fallback when local is down |
| `LOCAL_SEARCH_PROXY` | _(auto-detected)_ | Override proxy (e.g. `http://127.0.0.1:7890`) |

Proxy detection priority: `LOCAL_SEARCH_PROXY` > `HTTPS_PROXY` > `ALL_PROXY` > auto-probe ports 7890/7897/1080.

---

## Comparison with other free skills

| Skill | Search | Anti-bot Browse | Cross-Validation | Proxy Support | Model-Agnostic |
|---|---|---|---|---|---|
| **This skill (v4.1)** | ✅ Multi-engine | ✅ 3-tier Scrapling | ✅ Multi-source verdict | ✅ Auto-detect | ✅ Any LLM |
| `hugoreno/scrapling-browse` | ❌ | ✅ Scrapling | ❌ | ❌ | ✅ |
| `keef-agent/openclaw-scrapling` | ❌ | ✅ Scrapling | ❌ | ❌ | ✅ |
| Generic SearXNG skills | ✅ Single-engine | ❌ `web_fetch` only | ❌ | ❌ | ✅ |

---

## License

MIT © 2025
