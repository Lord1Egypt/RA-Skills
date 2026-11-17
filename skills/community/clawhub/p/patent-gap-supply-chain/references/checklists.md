# Checklists and Confidence Rules

## Alternative-Hypothesis Checklist

For each inference, check each item and explicitly exclude alternative explanations.

### Alternative explanations for the patent gap
- [ ] Does A's patent gap stem from a cross-licensing agreement? (check announcements / news)
- [ ] Did A inherit T usage rights via an acquisition? (check M&A history)
- [ ] Does T belong to a patent pool? (e.g., Avanci, MPEG-LA, Via Licensing)
- [ ] Is there an open-source implementation of T? (check open-source projects)
- [ ] Does A hold T patents via a subsidiary / affiliate? (check related-entity patents)
- [ ] Does A deliberately protect T as a trade secret / know-how rather than patenting it? (run Trade Secret Indicators checklist)
- [ ] Is the patent gap simply because T is a purchased component that A has no reason to patent? (common in consumer electronics — weak signal)

### Alternative explanations for "B entered the supply chain"
- [ ] Is B an NPE (non-practicing entity)? If so, B licenses only and is not in the supply chain
- [ ] Does A use B's patent indirectly via a third-party module? The third party is the supplier; B is its upstream
- [ ] Is B only a patent licensor with no physical transaction with A?
- [ ] Is the A-B tie purely financial investment, not business cooperation?
- [ ] Is the A-B relationship economically immaterial? (financial cross-validation required to exclude)

## Patent Quality Scoring (NEW v0.4.0)

**Principle**: Patent count is a weak signal. Quality matters. A core patent family outweighs dozens of peripheral patents. Apply this scoring to Lead 1 (patent ownership) and to Step 2B (dominance confirmation).

### Factor 1 · Claim breadth (0-3)
- [ ] 3: Independent claims covering the core mechanism/architecture, broad scope
- [ ] 2: Claims cover a specific implementation, moderate scope
- [ ] 1: Claims cover a narrow detail/variant
- [ ] 0: Claims are process-only or trivial

### Factor 2 · Citation impact (0-3)
- [ ] 3: High forward citations (top decile in field); later patents build on it
- [ ] 2: Moderate citations; some later work references it
- [ ] 1: Few citations
- [ ] 0: Never cited

### Factor 3 · Family size (0-3)
- [ ] 3: PCT + multiple national entries (US/EU/CN/JP/KR)
- [ ] 2: PCT application, few national entries
- [ ] 1: Single jurisdiction (e.g., CN only)
- [ ] 0: Provisional/unpublished

### Factor 4 · Legal status (0-3)
- [ ] 3: Granted AND maintenance fees paid (active)
- [ ] 2: Granted but recently filed; maintenance status unknown
- [ ] 1: Under examination / pending
- [ ] 0: Lapsed, revoked, abandoned, or transferred to shell

### Quality levels
- **Core patent**: total ≥8/12 — broad claims, high citations, international family, active legal status
- **Supporting patent**: total 4-7/12
- **Peripheral patent**: total 0-3/12 — narrow, uncited, single-jurisdiction, or lapsed

### Impact on confidence
- B holds Core patents in T → Lead 1 can reach "high"; triangulation convergence on B is stronger
- B holds only Peripheral patents → Lead 1 capped at "low"; triangulation convergence is weaker (B may be a paper tiger)
- A (forward) holds peripheral T patents → gap may be understated; note in report
- If patent quality cannot be assessed (data unavailable) → treat as Supporting, flag in report

## Negative Verification Checklist (NEW v0.4.0)

**Principle**: Before concluding B is A's supplier, actively attempt to disprove it. Document the search.

### Revenue / scale mismatch
- [ ] Checked B's total revenue vs. A's plausible procurement of T
- [ ] Checked if B's revenue is implausibly large/small relative to A's needs
- [ ] Checked B's capacity expansion announcements for product alignment with A

### Product-category mismatch
- [ ] Checked B's actual product catalog for the specific component A uses
- [ ] Checked if B's patents cover a different product variant than A uses
- [ ] Checked whether a third party (C) manufactures the physical product under B's license

### Geographic / logistics infeasibility
- [ ] Checked geographic compatibility (regulatory, shipping cost, local-content requirements)
- [ ] Checked trade restrictions / tariffs affecting A-B trade

### Explicit customer-list exclusion
- [ ] Checked if B publicly discloses customers (annual report, case studies, press releases)
- [ ] If B's customer list is available: is A absent from it despite high concentration?
- [ ] Checked if A publicly discloses suppliers (annual report) and B is absent

### Contractor / competitor relationship
- [ ] Checked if A and B are direct competitors in T (A buying from competitor = forced, unlikely)
- [ ] Checked if A positions its product as a substitute for B's

### Negative verification outcome
- [ ] Negative evidence FOUND → reduce confidence 1-2 levels (or overturn if fundamental contradiction)
- [ ] Negative search performed, NO evidence found → "negative verification passed" — supports inference
- [ ] Negative search NOT possible → flag "negative verification incomplete"

## Evidence Freshness Tracking (NEW v0.4.0)

**Principle**: Supply chains change. A 2023 teardown does not prove a 2026 relationship. Every evidence item carries a timestamp.

### Freshness levels
| Level | Age | Treatment |
|-------|-----|-----------|
| **Current** | ≤12 months | Full weight |
| **Moderate** | 12-18 months | Normal weight; flag in report |
| **Stale** | >18 months | Down-weight one level; cannot alone support "high" |
| **Unknown** | date not found | Treat as stale; flag prominently |

### Freshness rules
- [ ] Every evidence item in the report has a date or estimated date
- [ ] If no date can be found, marked "date unknown" and treated as stale
- [ ] Conclusion resting primarily on stale evidence → capped at "medium"
- [ ] Corroborating leads that are all stale → overall capped at "medium"
- [ ] Report includes a "evidence freshness table" listing each lead + evidence date + freshness level

### Refreshing stale evidence
- [ ] If stale evidence is critical, attempt to re-verify: search for newer teardowns, newer supplier disclosures, updated customer lists
- [ ] Document whether the relationship appears current or historical

## Competitive Triangulation Checklist

### Peer identification
- [ ] Identified 3-10 direct competitors / industry peers of A
- [ ] Peer selection: same industry classification + similar product + similar revenue size

### Gap verification
- [ ] Peer C₁ patent portfolio checked for T → [has / partial / none]
- [ ] Peer C₂ patent portfolio checked for T → [has / partial / none]
- [ ] Peer Cₙ patent portfolio checked for T → [has / partial / none]

### Convergence check
- [ ] For peers with gaps, does T's ownership converge to the same B?
- [ ] Any peers pointing to different owners → flag fragmented supply
- [ ] **Quality-aware check (v0.4.0)**: does B's patent quality support the convergence? (Core → strong signal; Peripheral → weak signal)

### Triangulation boost
- [ ] ≥3 peers same gap → same B: **+2 confidence levels**
- [ ] 2 peers same gap → same B: **+1 confidence level**
- [ ] 1 peer same gap: note in report, no boost
- [ ] Peers diverge: no boost, flag fragmentation
- [ ] Triangulation cannot override trade secret cap or financial cross-validation cap

## Financial Cross-Validation Checklist

### Forward direction
- [ ] Checked A's top-5 supplier list in annual report
- [ ] Checked A's supplier concentration ratio (>30% = single-supplier risk)
- [ ] Matched A's procurement categories against B's product lines
- [ ] If B is listed: checked B's top-5 customer list for A-like profile
- [ ] Checked B's customer concentration (>20% from single customer)
- [ ] Checked accounts receivable / payable patterns for correlation
- [ ] Checked related-party transaction disclosures
- [ ] Checked A's procurement growth vs. B's revenue growth (correlation)

### Reverse direction
- [ ] Checked B's top-5 customer list
- [ ] Checked B's revenue by industry segment
- [ ] For each candidate A: checked A's supplier list for B
- [ ] For each candidate A: checked A's related-party disclosures
- [ ] Estimated revenue contribution of each candidate (where data allows)

### Financial corroboration scoring
- [ ] **Strong**: B named as A's supplier OR A named as B's customer in official filings
- [ ] **Medium**: Procurement category + revenue scale matches
- [ ] **None**: No financial data found → **cap overall confidence at "medium"**
- [ ] **Negative**: Financial data contradicts → **reduce confidence by 1 level**

## Counter-Intelligence Checklist

### Patent-ownership side
- [ ] Is B's patent ownership abnormally dispersed? (shell companies / affiliates holding separately)
- [ ] Is there a shell company set up specifically to hold patents? (low registered capital, no real operations)
- [ ] Are patent transfers frequent? (possibly to obscure true ownership)

### A's patent-strategy side
- [ ] Does A deliberately not file patents to hide its tech roadmap?
- [ ] Do A's patent filings mismatch its actual product technology? (decoy filings)

### Anomaly signals
- [ ] Is A's supplier-disclosure abnormally terse or deliberately vague?
- [ ] Are key technical staff employed via labor dispatch / outsourcing rather than directly?
- [ ] Are there related entities with frequent changes of name / legal representative / shareholders?

If any anomaly exists → flag "counter-intelligence risk" in the report.

## Trade Secret / Know-How Indicators

### Indicator 1 · Industry norms
- [ ] T is in a trade-secret-dominant industry: semiconductor process, chemical formulation, pharma manufacturing process, food/beverage formula, metallurgy, specialty coatings, advanced materials synthesis
- [ ] Industry is known for "black box" secrecy (e.g., TSMC process, ASML optics, DuPont formulas)

### Indicator 2 · Company NDA / confidentiality culture
- [ ] A has public record of aggressive NDA enforcement or trade secret litigation
- [ ] A's employee contracts include strict non-compete + confidentiality clauses
- [ ] A's facilities known for tight access control / "clean room" culture
- [ ] A's technical publications / conference presentations notably sparse or redacted

### Indicator 3 · Patent filing pattern (strategic selectivity)
- [ ] A files patents across many domains but conspicuously avoids filing in T
- [ ] A's patent portfolio shows carefully scoped filings (protecting what can be reverse-engineered, hiding what cannot)
- [ ] A's patent filings in T's general category exist but intentionally omit key implementation details

### Indicator 4 · R&D intensity vs. patent output
- [ ] A has significant R&D team / budget in T's domain (job postings, R&D headcount, R&D expense)
- [ ] A produces few or zero patents in T despite the R&D investment
- [ ] A's R&D-to-patent ratio in T is significantly lower than industry peers

### Indicator 5 · Technology nature (protectability)
- [ ] T is a process / method / formula / manufacturing technique (hard to reverse-engineer → good for trade secret)
- [ ] T is a software algorithm embedded in a black-box system (source code hidden → trade secret feasible)
- [ ] T would be difficult to prove infringement even if patented (→ low incentive to patent)

### Indicator 6 · Trade secret litigation history
- [ ] A has sued others for trade secret theft in T's domain
- [ ] A's peers in the industry have active trade secret litigation
- [ ] Industry news reports trade secret disputes related to T

### Scoring
- **4-6 indicators → High likelihood trade secret**: gap likely strategic; default "no dependency" unless procurement/teardown overrides
- **2-3 indicators → Possible trade secret**: record as alternative hypothesis; proceed normally
- **0-1 indicators → Trade secret unlikely**: gap likely reflects real dependency; proceed normally

### Override signal
- [ ] Lead 4 (procurement) returns high-confidence evidence of external sourcing → overrides trade secret hypothesis
- [ ] Lead 5 (teardown) physically identifies third-party component → overrides trade secret hypothesis

## Confidence Scoring Rules

### Per-lead confidence (v0.4.0)

| Lead | High | Medium | Low |
|------|------|--------|-----|
| Patent ownership + quality | B holds Core-quality T patents, valid timeline | B holds Supporting-quality patents, timeline OK | T patents found but peripheral quality / owner unclear |
| Corporate affiliation | JV / mutual investment | Executive overlap | Same address / same legal rep (weak) |
| Talent flow | Multiple B technical staff joined A | Single key person joined | Job postings only mention B background |
| Procurement | B directly named as supplier | B's category mentioned | Category-related but no clear pointer |
| Product teardown | Physically confirmed B component | Teardown report mentions but unconfirmed | No teardown report |

**Evidence freshness adjustment (all leads)**: stale (>18 months) evidence down-weights one level.

### Overall confidence (base)

- **High**: ≥2 high-confidence leads corroborating
- **Medium**: 1 high + 1 medium corroborating, or multiple medium leads partially corroborating
- **Low**: only 1 lead hit, or leads contradict each other
- **Cannot infer**: 0 leads hit

### Adjustment layers (apply in order, each CAN cap or boost):

**Layer 1 — Trade secret adjustment**:
- Trade secret "high" + no procurement/teardown → cap at "low"
- Trade secret "high" + procurement/teardown confirms external sourcing → no cap
- Trade secret "possible" → no cap, record as alternative hypothesis

**Layer 2 — Triangulation boost**:
- ≥3 peers same gap → same B: **+2 levels**
- 2 peers same gap → same B: **+1 level**
- Cannot override Layer 1 cap

**Layer 3 — Negative verification** (v0.4.0):
- Negative evidence found → **reduce 1-2 levels** (overturn if fundamental contradiction)
- Negative verification passed → no change
- Negative verification incomplete → no change, flag

**Layer 4 — Evidence freshness** (v0.4.0):
- Conclusion rests primarily on stale evidence → **cap at "medium"**
- All corroborating leads stale → **cap at "medium"**

**Layer 5 — Financial cross-validation cap**:
- Strong/medium corroboration → no cap
- No corroboration → **cap at "medium"** (exception: procurement/teardown physical evidence)
- Negative corroboration → **reduce by 1 level**

### Final confidence = min(base ± adjustments, caps applied in order)
