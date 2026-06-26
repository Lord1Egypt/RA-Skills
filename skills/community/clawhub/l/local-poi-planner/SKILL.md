---
name: local-poi-planner
description: "Plan nearby places for dining, desserts, cafes, malls, and date spots using one local POI planning workflow. Best for queries like “附近有什么适合坐着聊天的咖啡店”, “帮我找地铁可达的甜品店”, or “规划一个适合约会的商场/餐厅”. Uses a single orchestrated flow: structured POI recall (Amap-first with OSM fallback) → anchor expansion → unified-search evidence → scoring → fallback to area-level recommendations when store-level data is weak."
metadata:
  openclaw:
    requires:
      bins: ["python3", "bash"]
    optionalBins: ["jq"]
files:
  read:
    - references/: Design notes, output template, anchor strategy
    - config/anchors.json: Optional anchor overrides for common places
    - config/geocode_overrides.json: Optional coordinate overrides for ambiguous place names
    - scripts/: Planner implementation
    - unified-search/: Unified search skill (must be installed as sibling skill) → https://clawhub.ai/ccmxigua/unified-search-suite (default routes ordinary queries to the deep search-layer: Exa + Tavily + Grok + TinyFish; legacy three-engine path only via --legacy)
  write:
    - /tmp/local-poi-planner-*.json: Intermediate planner outputs
    - /tmp/local-poi-planner-*.md: Final rendered reports
---

# Local POI Planner

Use this skill when the user wants a **specific nearby place recommendation** with constraints like:

- start point / origin
- metro access
- seating / environment quality
- mall preference
- budget / category / vibe
- avoid rules (night market, takeaway-only, no seating)

This skill is a **single top-level skill**. Internally it may call the existing `unified-search` skill script as a supporting evidence source.

## What this skill does

1. Parse the request into:
   - origin (see Location Resolution below)
   - category (see Category Resolution below)
   - preferences
   - constraints
   - avoid rules
2. Recall nearby candidates from a structured POI source (currently Amap-first with OSM fallback)
3. Expand the origin into nearby anchors (mall / road / station / area)
4. Generate multiple local search queries
5. Run `unified-search` over those queries and top POI candidates
6. Score evidence via auto-derived category hints (from CATEGORY_ALIASES)
7. **Quality gate**: assess bundle quality (poor/weak/acceptable); if evidence is weak, trigger specialty fallback
8. **Specialty fallback**: for cinema queries, supplement with Maoyan API city-level hall search (IMAX/4DX/CINITY/Dolby/LUXE/CGS)
9. Return:
   - top pick
   - backups
   - not recommended / weak-evidence notes
   - fallback area-level guidance if store-level evidence is weak

### Category Resolution

- `--category` explicitly set by caller → used directly (for known categories like `cafe`, `dessert`)
- `infer_category(query)` matches a known category via regex rules → used
- Neither → `_extract_fallback_keywords(query)` strips noise words (我/附近/的/找/...) → raw keywords passed directly to Amap as pure keyword search (no typecode, no category normalization)
- No Grok/LLM involved — the agent should NOT translate queries to categories (e.g. don't convert "修理书包" to "皮具护理"). Just pass `--query` and let the fallback pipeline handle keyword extraction. Amap supports free-text keyword search without a category/typecode.

### Location Resolution

- `--origin` explicitly set: used directly
- `--corelocation` flag: forces CoreLocationCLI (WiFi-based, ~500m accuracy) to get current coordinates
- No flag + query contains nearby hints (`附近`/`周边`/`方圆`): auto-tries CoreLocationCLI → IP geolocation fallback
- None of the above: "未指定起点"

## Quick Start

### Natural language mode
```bash
python3 scripts/planner.py \
  --query "福州大学旗山校区北门附近，地铁可达，适合坐着吃甜品，偏酸奶/gelato" \
  --format markdown
```

### Explicit mode
```bash
python3 scripts/planner.py \
  --origin "福州大学旗山校区北门" \
  --category dessert \
  --preferences "yogurt,gelato,smoothie" \
  --constraints "metro,seating,environment,mall" \
  --avoid "night_market,takeaway_only,no_seating" \
  --format markdown
```

### CoreLocation mode (auto-detect current position)
```bash
python3 scripts/planner.py \
  --query "附近有什么电影院支持4DX" \
  --corelocation \
  --format markdown
```

## Output contract

The planner returns either:
- **store-level recommendation** when evidence is sufficient, or
- **area-level fallback** when exact shop hits are weak.

Confidence levels:
- `high`: repeated store-level hits with supporting evidence
- `medium`: usable candidates but some ambiguity
- `low`: fallback area recommendation only

## Internal dependency

This skill uses the unified-search entrypoint here:
```bash
bash <unified-search>/scripts/unified-search.sh "<query>" --num 5 --topic general
```

**Important — which path actually runs (verified 2026-05-31):**
- The entrypoint is the new `unified-search.sh`, **not** `unified-search-legacy.sh`.
- For an ordinary query with no `--legacy`/`--mode` flag, the script routes to
  `run_search_layer_auto` → deep **search-layer** with `--source exa,tavily,grok,tinyfish`.
  So Grok + TinyFish are part of the real path; the legacy Tavily+Exa+Google merge is **not** used here.
- `--num 5 --topic general` are legacy-only flags. On the deep search-layer path they are
  effectively ignored (not forwarded to `search-layer`), so they do not change behavior.
- When debugging latency/hangs, profile `run-search-layer.sh` → `search.py` (deep search-layer),
  **not** `unified-search-legacy.sh`. The legacy script is a different code path.

## Lessons / Pitfalls

See `references/lessons-2026-05-31.md` for hard-won debugging notes:
- Profiling the **wrong** unified-search path (legacy vs deep) wastes hours — always confirm the actual entry script first.
- Only Grok is usable for local Chinese queries; Tavily/TinyFish pollute ~87% of results; Exa often 402s.
- Grok needs `proxies={http:None,https:None}` (Surge proxy hangs `enable_search`) and a 1800s timeout for Chinese multi-agent queries.
- Transit detail rendering rules: same-segment buslines are **alternatives** (not sequential transfers); `via_stops` carries stop names; walking has full turn-by-turn; no `max_parts` truncation.
- Accessibility scoring/thresholds and the "shops are just geographically far from metro" reality.

## Rules

- **Planner execution time**: The planner is silent during execution (3-10 minutes is normal).
  All output is buffered until completion — there is zero intermediate output even on
  stdout. **MANDATORY: when running planner.py via exec, you MUST set timeout=1800
  (30 minutes).** Do NOT use shorter timeouts (120s, 600s) — they will kill the process
  before unified-search completes. The planner runs these stages sequentially: POI search
  → web enrichment (up to 5 POIs, 30-90s each) → anchor expansion → unified-search
  queries (up to 3, 30-90s each) → decision → transit details. 5 POIs × 90s ≈ 7.5 min
  for web enrichment alone; the full pipeline can exceed 10 minutes. Do NOT kill the
  process because you see "no output yet." If the planner actually hangs, it's more
  likely in the unified-search network calls than in local Python code.

- Prefer one final recommendation workflow, not fragmented sub-skills
- If exact local store evidence is weak, **do not hallucinate shop names**
- Fallback to area / mall / anchor recommendation with explicit uncertainty
- Use concise decision output:
  - 首选
  - 备选
  - 不推荐 / 风险点
  - 下一步
- **Web search: ALL external web enrichment MUST go through `unified-search.sh`.**
  Do NOT DIY via DuckDuckGo Lite, `curl` to Baidu/Sogou/360, `requests` scraping, or ad-hoc
  HTTP calls. These are unreliable (empty results, anti-bot blocking, wrong encoding) and
  waste time. Only `unified-search.sh` (especially with Grok) works for Chinese local queries.
  The Tavily research script is a secondary option for deep-dive topics, but for POI
  enrichment always prefer unified-search.
- **For cinema/venue features that POI APIs don't expose (e.g. 4D/IMAX/Dolby screen types)**,
  the skill may supplement with structured venue APIs like Maoyan (`m.maoyan.com` city-level
  cinema list). See `references/lessons-2026-06-01.md` for Maoyan API notes.

- **Quality gate**: After unified-search completes, `_assess_bundle_quality` evaluates
  each candidate bundle (max_score ≤2 → poor, avg_score <10 → weak, else acceptable).
  If `need_fallback=True`, the pipeline automatically triggers `_specialty_fallback_run`
  (currently only cinema → Maoyan API) and inserts the fallback bundle at the front of
  the run list.

- **CATEGORY_EVIDENCE_HINTS auto-derivation**: `_get_evidence_hints(category)` first checks
  the curated `CATEGORY_EVIDENCE_HINTS` dict (dessert/cafe/tea/bakery/restaurant/电影院);
  if not found, it auto-generates hints from `CATEGORY_ALIASES` by collecting all aliases
  that map to the same canonical category. This means adding a new category only requires
  updating `CATEGORY_ALIASES` — no separate hints dict needed.

- **CoreLocation**: On macOS, the skill can auto-resolve current position via
  `CoreLocationCLI` (WiFi-based, ~500m accuracy). Requires `brew install corelocationcli`.
  Use `--corelocation` flag to force this, or rely on auto-detection when origin is
  unspecified and query contains nearby hints (`附近`/`周边`/`方圆`). CoreLocationCLI may
  trigger a macOS location permission popup on first use.
  See `scripts/macos_location.py` for the implementation.

## Suggested trigger examples

- “帮我找附近适合约会的甜品店”
- “从 XX 出发，找地铁可达、能坐着聊天的咖啡馆”
- “附近有没有适合带女朋友去的 mall 里甜品店”
- “规划一个商场内、清爽口味优先的甜品点”
