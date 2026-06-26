---
name: predict-intelligence
description: >-
  Predict intelligence skill for AI agents. Generates professional PDF reports
  with probability-ranked predictions, D3 visualizations, and Polymarket
  consensus signals. Covers geopolitics, finance, tech, elections, and any
  predicting question. Use when user asks about event predictions, probability
  predicts, "when will X happen", "will X happen", or outcome analysis.
keywords:
  - predict
  - prediction
  - intelligence report
  - PDF generation
  - Polymarket
  - prediction market
  - D3 visualization
  - geopolitics
  - financial predicting
  - market consensus
---

# Predict Intelligence Skill

You generate a professional PDF intelligence brief. The user should
grasp the key finding in **30 seconds**. You own **information efficiency**.

## Agent Requirements

| Capability | What you need |
|---|---|
| **Web search** | Search the internet for news, analysis, data |
| **URL fetch** | Open a URL and read its content |
| **File read/write** | Read template, write HTML report |
| **Shell execute** | Run Python 3.9+ scripts |

## First-Time Setup

```bash
pip install playwright
playwright install chromium
```

No other Python packages needed (Jinja2, requests, etc. are NOT required).

---

## How It Works

```
Read template → Do research → Write HTML → Convert to PDF
```

1. Read `SKILL_DIR/templates/report_template.html` — your structural reference.
2. Research and analyze the topic (Steps 1–8 below).
3. Generate a NEW `.html` file following the template's exact structure.
4. Convert to PDF:
   ```bash
   python SKILL_DIR/scripts/to_pdf.py report.html predict_report.pdf
   ```

**The template IS the spec.** It contains:
- All CSS (copy verbatim — never modify)
- All D3 visualization code (copy verbatim — only change data variables)
- Example content showing exact formatting for every section
- Extensive comments explaining what each section does and how to fill it

---

## Step 0 — Domain Detection

| Signal | Domain |
|---|---|
| Countries, leaders, military, diplomacy, sanctions | **Geopolitical** |
| Stocks, crypto, Fed, rates, commodities | **Financial** |
| Tech releases, AI models, products | **Technology** |
| M&A, acquisitions, IPO, corporate | **Corporate** |
| Other | **Custom** |

Classification bar is always: `ANYGEN PREDICT INTELLIGENCE ASSESSMENT`
with `#YY-MM-DD` on the right (2-digit year, e.g. `#26-03-12`).

The report structure and design are IDENTICAL across all domains.
Only research sources and visualization choices change.
See **Domain Adaptation** at the bottom.

## Step 1 — Parse Query

Extract:
- **event**: what is being predicted
- **actors**: who is involved
- **regions / sectors**: geographic or industry scope
- **timeframe**: any dates or deadlines
- **question type**: `temporal` ("when"), `binary` ("will"), or `multi_outcome` ("what")

## Step 2 — Research

Search the web at least 8 times, covering:

1. Breaking news (last 48 hours)
2. Diplomatic / military / industry developments
3. Decision-makers' public statements
4. Historical precedent
5. Expert / think-tank / analyst reports
6. Regional or sector-specific media
7. Economic / financial context
8. Low-probability high-impact wildcards

**CRITICAL**: For every fact, **save the exact article URL**.

**For geopolitical / diplomacy / military / sanctions topics, ALSO collect:**
- 3–5 key locations (cities, capitals, bases, meeting venues) with lat/lon
- ISO alpha-2 country codes of all parties involved
- Any diplomatic channels, proxy lines, or trade routes between locations
This data is required for the V2 Regional Map in Step 7. Collect it now.

```
fact: "Oman hosted senior US-Iran talks on March 5"
url:  "https://reuters.com/world/middle-east/oman-hosts-rare-us-iran-talks-2026-03-06/"
```

Homepage URLs are forbidden. Every URL must point to a specific article.

## Step 3 — Formulate Predictions

Create outcomes sorted by probability descending. All must sum to ~100%.

The verdict has five parts:
- **verdict_number**: top probability as text (e.g. "34%") — displayed at 52px, the BIGGEST element
- **verdict_outcome**: 3–6 word label
- **verdict_detail**: 1 sentence — "Most likely path: ..."
- **verdict_bg** (Context): 2–3 sentences of BACKGROUND BRIEFING — what led to
  the current situation, key prior events, the "前情提要" (previously on...)
- **verdict_context**: 2–3 sentences of assessment reasoning with key evidence

Calibration:

| Confidence | Range |
|---|---|
| Near-certain | 90–99% |
| Very likely | 75–89% |
| Likely | 60–74% |
| Toss-up | 40–59% |
| Unlikely | 25–39% |
| Very unlikely | 10–24% |
| Remote | 1–9% |

## Step 4 — Key Drivers (5 items, causal logic required)

Each driver MUST have:
- **Title**: 3–5 words
- **Direction**: `positive` (↑ increases likelihood) or `negative` (↓ decreases)
- **Causal logic**: 1 sentence: fact → mechanism → directional impact
- **Source URL**: exact article URL

❌ Bad: "Sanctions pressure — Iran inflation at 45%"
✅ Good: "Sanctions pressure ↑ — 45% inflation pushes Tehran toward concessions for relief"

The bad one states facts. The good one explains the causal chain.

## Step 5 — Watch List (5 items, forward-looking only)

Each item is a FUTURE event or trigger that could shift the predict.
No past events. No source URLs (these haven't happened yet).

Each item MUST have:
- **Date or window**: specific date or range (e.g. "Apr 3", "Late March")
- **Trigger**: 3–6 words describing what might happen
- **Conditional impact**: 1 sentence — "If [X] → [how probability shifts]"

✅ Good: "Apr 3 — UNSC sanctions vote — If passed → ceasefire probability ↑10-15%"
✅ Good: "Late Mar — FOMC meeting — Dovish tone → ↑ rate cut odds; hawkish → ↓"
❌ Bad: "Mar 5 — Secret Muscat meeting happened" (PAST event — belongs in Key Drivers)

**The distinction:**
- **Key Drivers** = WHY the current probability is what it is (past + present evidence, with source URLs)
- **Watch List** = WHAT could change the probability next (future triggers, no sources needed)

## Step 6 — Polymarket Data

Run:
```bash
python SKILL_DIR/scripts/fetch_polymarket.py --query "<keywords>" --limit 10
```

From results:
1. Add your probability estimate for each option
2. Calculate delta = your_estimate − market_probability
3. Select **3 markets with highest absolute delta**
4. Sort by delta descending (most undervalued first)

If no script available, search "polymarket [topic]" on the web.
If no markets exist, skip the Polymarket section entirely.

## Step 7 — Visualization (REQUIRED)

### ⚠ MANDATORY MAP RULE — READ THIS FIRST

**If the topic involves countries, regions, borders, military, diplomacy,
or sanctions → you MUST include V2 (Regional Map). Non-negotiable.**

Do NOT skip V2 because:
- "I only want one chart" → V2 IS that one chart. Add a second if needed.
- "It needs extra dependencies" → TopoJSON is already in the template `<head>`.
  Just keep the `<script>` tag. Do NOT remove it.
- "I don't have good marker data" → You researched 8+ sources in Step 2.
  You have city names, country names, and actor locations. Use them.
  Minimum: 3 markers from your research + highlight the relevant countries.

**Only these domains are exempt from V2:** financial, technology, corporate,
budget/aid (unless they have a geographic dimension).

### Choosing visualizations

Pick 1 or 2 types total. Minimum 1, maximum 2.

| Domain | Required | Optional 2nd |
|---|---|---|
| War / conflict | **V2 (map)** | V3 (entity) |
| Sanctions / trade | **V2 (map)** | V5 (comparison) or V8 (sankey) |
| Military balance | **V2 (map)** | V5 (comparison bars) |
| Diplomacy | **V2 (map)** | V9 (gantt phases) |
| Election | **V7 (choropleth)** | V1 (polling trend) |
| Economic / monetary | V1 (trend) | V10 (key rate) or V5 (comparison) |
| Budget / aid flow | V8 (sankey) | V5 (comparison) |
| Multi-phase process | V9 (gantt) | V4 (timeline) |

### V2 data — how to fill it

From your Step 2 research, extract:
- `markers[]`: 3–5 locations mentioned in your sources (capitals, cities,
  military bases, meeting venues). Use real lat/lon coordinates.
- `connections[]`: diplomatic channels, proxy influence lines, trade routes.
- `hlCodes[]`: ISO alpha-2 codes of countries involved (e.g. `["IR","IQ","OM"]`).

This data comes from your research. You already have it. Do not skip.

### Available types

9 pre-built types (there is NO V6). **DO NOT write custom D3/SVG.**

| Type | ID | When to use |
|---|---|---|
| **Regional Map** | V2 | Geographic theater with markers |
| **Metric Trend** | V1 | Data over time — polls, rates, escalation |
| **Entity Graph** | V3 | Actor networks — alliances, proxies |
| **Event Timeline** | V4 | Complex event sequences (sparingly) |
| **Comparison Bars** | V5 | Ranked values — spending, strength, polls |
| **Choropleth** | V7 | Election maps / regional statistics |
| **Sankey** | V8 | Flow diagrams — funding, resources, influence |
| **Gantt** | V9 | Phase / timeline bars for overlapping activities |
| **Big Number** | V10 | 1–3 key metrics as large display (see rules below) |

**V10 Big Number — VERY RARE, strict rules:**
- Use ONLY when a specific number is truly critical to the analytical argument
- The number must NOT already appear in the Verdict
- Maximum 3 number cards
- Must include delta/change indicator (↑ or ↓ with amount)
- ✅ "US unemployment 4.1% (↑0.3pp)" when discussing Fed rate decisions
- ✅ "$12B reserves (↓40% YoY)" when discussing Iran sanctions threshold
- ❌ Generic statistics, redundant percentages, or decorative numbers

### Placement and rules

**Section order:** Visualization comes AFTER Predict → Key Drivers →
Watch List, and BEFORE Polymarket.

For each type you use:
1. Keep its `<section>` in the HTML body (after Watch List section)
2. Keep its matching `<script>` block at the bottom
3. Only change the **data variables** at the top of the script (`AGENT:` markers)
4. **Delete ALL unused types** — both HTML `<section>` AND `<script>`
5. `<h2>` title MUST describe what the chart shows

**Label limits** (auto-truncated, keep short anyway):

| Type | Limits |
|---|---|
| V2 | marker labels ≤20 |
| V1 | y-label ≤20, series ≤20, max 12 x-points, max 3 lines |
| V3 | node ≤16, edge ≤14, max 8 nodes |
| V4 | labels ≤45, max 8 items |
| V5 | bar labels ≤18, max 8 bars |
| V7 | category labels ≤20 |
| V8 | node names ≤18, max 12 nodes, max 15 links |
| V9 | task labels ≤22, max 8 tasks |
| V10 | max 3 cards |

## Step 8 — Fact Check

**This report may inform six-figure financial decisions.**

- [ ] Every source URL is a real article page you actually visited
- [ ] Every Polymarket URL is a real event page on polymarket.com
- [ ] All stated facts match their sources
- [ ] Probabilities sum to ~100%
- [ ] Remove any claim without a verified source URL

## Step 9 — Generate HTML

Open `SKILL_DIR/templates/report_template.html` and read it.
Then generate a **new** HTML file following the same structure:

1. **Copy the entire `<style>` block verbatim** — never modify CSS.
2. **Copy D3 `<script>` blocks for the 1–2 viz types you chose.**
   Only replace the data variables at the top of each script
   (clearly marked with `AGENT: Replace` comments).
3. **CDN dependencies:**
   - D3: always include (needed for V1–V9)
   - TopoJSON: only for V2 (map), V7 (choropleth)
   - d3-sankey: only for V8 (sankey)
   - V10 (Big Number) needs NO scripts — pure HTML/CSS
4. **Fill in the HTML content sections** following the template's structure.
   **Section order:** [A] → [B] → [E] → [F] → [G] → Visualization → [H] → [I]
5. **Delete ALL unused viz types** — both `<section>` and matching `<script>`.
   - No Polymarket → delete section [H]

Save as `report.html` in the working directory.

## Step 10 — Convert to PDF

```bash
python SKILL_DIR/scripts/to_pdf.py report.html predict_report.pdf
```

## Step 11 — Deliver

Tell the user the PDF is ready. State the verdict in one sentence:
"Report generated. **34% chance of ceasefire before April 15** — most
likely via Omani-mediated direct talks."

---

## Template Quick Reference

The template contains example content for a "US-Iran Ceasefire" report.
Here's the section-by-section mapping:

| Order | Section | What to fill |
|---|---|---|
| 1 | Classification bar `[A]` | `ANYGEN PREDICT INTELLIGENCE ASSESSMENT` + `#YY-MM-DD` |
| 2 | Header + verdict `[B]` | Title, date, verdict number/outcome/detail/context-bg/context |
| 3 | Predict `[E]` | Outcome divs with probability bars |
| 4 | Key Drivers `[F]` | 5 driver items with ↑/↓, causal logic, source URL |
| 5 | Watch List `[G]` | 5 future triggers with date/window, trigger title, conditional impact |
| 6 | **Visualization** | **REQUIRED** — pick 1–2 of 9 types (V1–V5, V7–V10). See domain rules for mandatory types. |
| 7 | Polymarket `[H]` | Optional: 3 market blocks with option tables |
| 8 | Footer `[I]` | Source list + disclaimer |

---

## Domain Adaptation

### Research Sources by Domain

| Domain | Primary sources |
|---|---|
| Geopolitical | Reuters, AP, Al Jazeera, CSIS, IISS, Brookings, ICG |
| Financial | Bloomberg, FT, WSJ, Fed minutes, bank research, on-chain analytics |
| Technology | TechCrunch, The Verge, Ars Technica, company blogs, SEC filings |
| Corporate | SEC filings, press releases, industry analysts, FT, Bloomberg |

### Visualization by Domain (pick 1–2, min 1 max 2)

**⚠ V2 (Regional Map) is MANDATORY for Geopolitical, Diplomacy, Military,
and Sanctions topics. Do not substitute Gantt, Timeline, or any other type
in place of V2. V2 must always be included; add a second chart if needed.**

| Domain | Required viz | Optional 2nd | Rule |
|---|---|---|---|
| Geopolitical | **V2 (map)** | V3 (entity) | **V2 MANDATORY — never omit** |
| Diplomacy | **V2 (map)** | V9 (gantt — phases) | **V2 MANDATORY — never omit** |
| Military | **V2 (map)** | V5 (comparison) | **V2 MANDATORY — never omit** |
| Sanctions | **V2 (map)** | V5 or V8 (sankey) | **V2 MANDATORY — never omit** |
| Financial | V1 (trend) | V10 (key metric) or V5 | |
| Technology | V1 (trend) | V3 (entity — ecosystem) | |
| Corporate | V3 (entity — M&A) | V8 (sankey — deal flow) | |
| Election | **V7 (choropleth)** | V1 (polling trend) | **V7 MANDATORY** |
| Budget / aid | V8 (sankey — flow) | V5 (comparison) | |

### What NEVER Changes

1. White monochrome CIA-brief aesthetic with ANYGEN classification bars
2. 52px verdict number — the biggest element on the page
3. Verdict block: number → outcome → detail → context background → assessment
4. Probability-ranked outcomes with bars
5. Key drivers with ↑/↓ direction and causal logic
6. Watch list with forward-looking triggers and conditional impacts
7. Polymarket delta comparison with UNDERVALUED highlight (when markets exist)
8. Every URL must be a real article, never a homepage
9. 30-second scannability — no filler, no academic prose

## Writing Rules

| Element | Rule |
|---|---|
| Verdict number | 52px. THE biggest element. |
| Verdict outcome | 3–6 words |
| Verdict context | 2–3 sentences of reasoning |
| Driver title | 3–5 words |
| Driver detail | 1 sentence: fact → mechanism → direction |
| Watch trigger | 3–6 words |
| Watch impact | 1 sentence: "If [X] → [shift]" |
| URLs | Real article URLs. Never homepages. |
| Polymarket | 3 markets, delta-sorted, highlight undervalued |
| General | If a word doesn't add information, cut it |
