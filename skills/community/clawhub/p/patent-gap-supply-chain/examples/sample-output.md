# Sample Output

A worked example showing the full v0.4.0 report format for a **fictional** case with triangulation, negative verification, patent quality scoring, and evidence freshness tracking. All companies, patents, and data below are illustrative only.

---

## Input

- **Direction**: Forward
- **Target A**: NexRouter Inc. (fictional ticker: NXR)
- **Product P**: NexRouter 5G Pro router
- **Technology T**: 5G mmWave antenna technology
- **Background**: NexRouter's 5G Pro uses mmWave antennas, but NexRouter's filings show no mmWave-antenna patents.

## Step 0: Applicability

Hardware / networking equipment → **Strong applicability**. Proceed.

## Step 1: Trigger + Direction

- Direction: Forward
- A = NexRouter Inc.
- P = NexRouter 5G Pro
- T = 5G mmWave antenna technology
- Preliminary: NexRouter's main R&D is in router firmware / SoC, not RF antenna design. Gap likely.

## Step 2: Patent gap confirmation

Searched NexRouter + subsidiaries in patent DB (CN + US + PCT) for "mmWave antenna" / IPC H01Q:
- NexRouter patents: 12 total, all in firmware / routing protocols / SoC. **Zero** mmWave-antenna patents.
- Gap status: **Confirmed**.

Excluded legitimate-use scenarios:
- Cross-licensing: no public record found.
- Acquisition: no mmWave-antenna company acquired.
- Patent pool: mmWave antenna not part of Avanci / MPEG-LA pools.
- Open-source: no open-source mmWave-antenna implementation applicable.

## Step 3: Trade secret assessment

| Indicator | Assessment | Signal |
|-----------|------------|--------|
| 1. Industry norms | mmWave antenna is RF hardware, not a process/formula; easy to reverse-engineer | Dependency |
| 2. NDA culture | NexRouter is a standard networking company; no notable NDA litigation | Neutral |
| 3. Patent filing pattern | NexRouter files actively in firmware/SoC but zero in RF — no strategic selectivity | Neutral |
| 4. R&D vs. patent output | NexRouter lists 0 RF engineers and 0 RF R&D budget in filings | Dependency |
| 5. Technology nature | mmWave antenna is a physical hardware component, identifiable in teardown | Dependency |
| 6. Trade secret litigation | No trade secret litigation in mmWave antenna industry | Dependency |

**Trade secret likelihood**: 0/6 → **Trade secret unlikely**. Proceed.

## Step 4: Multi-lead parallel verification

### Lead 1 · Patent ownership + quality

WaveAnt Technologies holds 47 mmWave-antenna patents. **Patent quality scoring**:

| Quality factor | Score | Basis |
|----------------|-------|-------|
| Claim breadth | 3/3 | Independent claims cover the phased-array steering mechanism itself |
| Citation impact | 3/3 | 41% of later mmWave-antenna patents cite WaveAnt's core family |
| Family size | 3/3 | PCT + US/CN/EU national entries |
| Legal status | 2/3 | Granted, maintenance current on core family |
| **Total** | **11/12** | **Core quality** |

Lead 1 confidence: **High** (Core quality + valid timeline, core filings 2019-2021, before 5G Pro launch 2024). Evidence date: 2024-08 (current).

### Leads 2-5

| Lead | Hit | Detail | Confidence | Evidence date | Freshness |
|------|-----|--------|------------|---------------|-----------|
| 2. Corporate affiliation | Yes | Co-founded JV "NexWave RF" (2023), 60/40 split | High | 2023-06 | Stale (>18mo) |
| 3. Talent flow | Yes | 3 WaveAnt engineers → NexRouter (2023-24) | Medium | 2024-03 | Moderate |
| 4. Procurement | Yes | 2023 annual report: "mmWave antenna module" top-5 procurement, supplier unnamed | Medium | 2024-04 | Moderate |
| 5. Product teardown | Yes | TechInsights teardown identifies "WaveAnt WN-5G39" module | Very high | 2025-11 | **Current** |

**Freshness note**: Lead 2 (JV) evidence is from 2023 — flagged as stale, down-weighted to Medium. Leads 4/5 are the freshest and strongest.

## Step 5: Competitive triangulation

A's peers in networking equipment:

| Peer | Has mmWave patents? | Points to same B? | B's quality for peer? |
|------|--------------------|-------------------|----------------------|
| C₁ RouteMax | Zero | Yes — teardown shows WN-5G37 | Core (WaveAnt) |
| C₂ NetFusion | Zero | Yes — procurement category matches | Core |
| C₃ SpeedLinx | Zero | Yes — JV with WaveAnt (2022) | Core |
| C₄ TeleCore | **Has own** | No — internal development | — |

**Triangulation result**: 3/4 peers all lack T patents, all point to WaveAnt, and WaveAnt's patents score **Core** quality across the board. **Triangulation boost: +2 levels** (quality-confirmed convergence).

## Step 6: Negative verification

Actively searched for evidence that WaveAnt is NOT NexRouter's supplier:

| Negative check | Result |
|----------------|--------|
| Revenue mismatch | **No** — WaveAnt revenue (~¥900M) is consistent with supplying 5+ networking companies; NexRouter's estimated antenna spend (~¥380M) is a plausible share |
| Product-category mismatch | **No** — WaveAnt's catalog includes the exact module type (5G mmWave array) found in teardown |
| Geographic infeasibility | **No** — both based in Guangdong, logistics normal |
| Customer-list exclusion | **Partially checked** — WaveAnt is pre-IPO, no public customer list; could not fully verify |
| Contractor/competitor | **No** — WaveAnt makes antenna modules; NexRouter makes routers; not competitors |
| Third-party licensing | **No** — teardown shows WaveAnt-branded module, not a third-party rebrand |

**Negative verification outcome**: Search performed, no fundamental negative evidence found. One gap: customer list unavailable (WaveAnt pre-IPO). **Negative verification passed** (with noted data gap).

## Step 7: Fusion + confidence

- Leads: 5/5 hit. Lead 5 (teardown, current evidence) = very high. Lead 1 (Core quality) = high. Leads 2-4 = medium (with freshness adjustments).
- Base confidence: **High** (≥2 high leads corroborating).
- Triangulation boost: +2 → remains High (already at ceiling).
- Negative verification: passed → no reduction.
- Evidence freshness: strongest evidence (teardown 2025-11) is current → no freshness cap.
- **Pre-financial confidence: High**.

Role determination: Leads 4/5 hit → WaveAnt is a **direct supplier**.

## Step 8: Financial cross-validation

| Check | Result | Corroboration |
|-------|--------|---------------|
| NexRouter top-5 suppliers | Supplier #3 "antenna module supplier" = 12.4% of procurement, ¥380M — matches WaveAnt revenue profile | **Medium** |
| WaveAnt customer concentration (pre-IPO filings) | Customer #1 = 22% of revenue, profile matches NexRouter | **Medium** |
| AR/AP patterns | WaveAnt AR 60% from one customer, 90-day terms — matches NexRouter AP | **Medium** |

**Financial corroboration**: **Medium** (category + revenue scale match, no explicit naming due to pre-IPO opacity). **No cap applied** (medium corroboration + strong physical evidence).

## Step 9: Alternative-hypothesis check

| Hypothesis | Excluded? | Basis |
|-----------|-----------|-------|
| Gap due to cross-licensing | Yes | No public record |
| WaveAnt is NPE | Yes | Manufactures physical modules (teardown) |
| Third-party module embedding WaveAnt patent | Yes | Teardown shows direct WaveAnt module |
| Pure financial investment tie | Yes | JV operational + direct supply |
| Trade secret protection | Yes | 0/6 indicators, no RF R&D |
| Relationship economically immaterial | Yes | 12.4% of procurement |
| B's patents are peripheral (paper tiger) | Yes | Core quality 11/12 |

Unexcluded: none material.

## Step 10: Counter-intelligence check

| Check | Result |
|-------|--------|
| Patent ownership dispersed? | No — 47 patents under WaveAnt directly |
| Shell companies? | No — real operating company |
| Deliberate non-filing? | Unlikely — files aggressively in core areas |
| Frequent transfers? | No |
| Supplier disclosure vague? | **Flag** — annual report doesn't name supplier |

Counter-intelligence risk: **Low**. One minor flag.

## Step 11: Output report

### Supply-Chain Inference Report — NexRouter Inc.

**Direction**: Forward (patent gap → supplier)

**Trade secret assessment**: Unlikely (0/6 indicators).

**Patent quality**: WaveAnt's core family scores **11/12 (Core)** — broad claims, high citations, international family, active status.

**Evidence freshness**: Teardown (2025-11) current; JV evidence (2023) flagged stale and down-weighted.

**Triangulation**: 3/4 peers share the gap, all converge on WaveAnt, Core-quality confirmation. +2 boost.

**Negative verification**: Performed, passed (with pre-IPO customer-list data gap noted).

**Relationship determination**: WaveAnt Technologies is a **direct supplier** of mmWave antenna modules to NexRouter.

**Evidence chain**:

| # | Lead | Hit | Confidence | Quality/Freshness |
|---|------|-----|------------|-------------------|
| 1 | Patent ownership | WaveAnt 47 patents, Core 11/12 | High | Quality-adjusted |
| 2 | Corporate affiliation | JV "NexWave RF" (2023) | Medium | Stale evidence, down-weighted |
| 3 | Talent flow | 3 engineers → NexRouter | Medium | Moderate freshness |
| 4 | Procurement | Top-5 category, unnamed | Medium | Moderate freshness |
| 5 | Product teardown | "WaveAnt WN-5G39" module | Very high | **Current** (2025-11) |

**Confidence stack**:
- Base fusion: 5/5 leads, 2 high + very high corroborating → **High**
- Triangulation: +2 (quality-confirmed) → High (ceiling)
- Negative verification: passed → no change
- Evidence freshness: no cap (strongest evidence current)
- Financial: Medium corroboration → no cap
- **Final confidence: High**

**Alternative hypotheses**: All material alternatives excluded.

**Counter-intelligence risk**: Low.

**Follow-up verification**:
- Re-verify JV "NexWave RF" activity (stale evidence, 2023)
- Await WaveAnt IPO filings for explicit customer naming
- Monitor WaveAnt patent filings post-2024 for co-development indicators
- Watch RouteMax/NetFusion teardown results (triangulation peers)
