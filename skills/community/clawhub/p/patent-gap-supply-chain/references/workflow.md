# Detailed Workflow

## Step 1: Trigger lead identification + direction selection

**Goal**: Define the analysis target, determine analysis direction, and identify a potential patent gap.

**Operations**:
1. Confirm target company (full name, ticker)
2. Determine analysis direction based on user intent:
   - **Forward**: user asks "who supplies X?" / "identify suppliers" / "what company provides the tech?" → target is A (the patent-gap company)
   - **Reverse**: user asks "who are B's customers?" / "which downstream companies depend on this?" / "what companies need this technology?" → target is B (the patent owner)
3. Identify the key technology T and/or product P:
   - If not specified by user, extract from product docs, annual report, prospectus, research reports
4. Preliminarily judge patent status:
   - Forward: does A likely lack T's patents?
   - Reverse: does B likely hold dominant/leading T patents?

**Output**: Direction (forward/reverse) + target company + T + P + preliminary judgment

## Step 2A: Patent gap confirmation (forward direction)

**Goal**: Confirm with data whether A truly lacks T-related patents, and rule out legitimate-use scenarios.

**Operations**:
1. Search A's patents using patent search tools (tushare patent API / PatSnap)
   - Dimensions: A's company name + technology T keywords + IPC class
   - Scope: CN patents + US patents + PCT (per A's market coverage)
   - Note: A may hold patents via subsidiaries / affiliates — search A's related entities
2. Determine gap:
   - A (incl. affiliates) has zero T-related patents → gap confirmed
   - A has T-related patents but count significantly below industry average → partial gap
   - A has sufficient T-related patents → no gap, terminate
3. Rule out legitimate-use scenarios (if gap confirmed):
   - Cross-licensing, acquisition inheritance, patent pool, open-source

**Output**: Gap determination + excluded legitimate-use scenarios

## Step 2B: Patent dominance confirmation (reverse direction)

**Goal**: Confirm that B indeed holds a dominant position in T's patent landscape.

**Operations**:
1. Search T's patent landscape comprehensively
2. Rank patent holders by quantity and citation count
3. Determine B's dominance:
   - B holds >30% of T's patents OR top-3 cited in T → dominant position confirmed
   - B holds 10-30% → moderate position
   - B holds <10% → weak position, may not be the key technology gatekeeper
4. Identify B's patent family: core patents + timing + jurisdiction coverage

**Output**: Dominance level (dominant / moderate / weak) + B's core patent list

## Step 3: Trade secret / know-how assessment

**Goal**: Determine whether the patent gap reflects true external dependency or deliberate trade secret / know-how protection.

**Core distinction**:
- **Trade secret**: A has the technology internally, but protects it through secrecy
- **True gap → dependency**: A genuinely lacks the technology and must source it externally

**Trade secret assessment — 6 indicators**:

| # | Indicator | Strong trade secret signal | Strong dependency signal |
|---|-----------|---------------------------|--------------------------|
| 1 | Industry norms | Semiconductor process, chemical formula, pharma manufacturing, metallurgy | Consumer electronics, commoditized components |
| 2 | NDA / confidentiality culture | Aggressive NDAs, non-compete lawsuits, "black box" secrecy | Open publications, transparent R&D |
| 3 | Patent filing pattern | Files patents in some domains, conspicuously avoids T | Files patents evenly or rarely |
| 4 | R&D intensity vs. patent output | High R&D spend + low T patents | Little to no R&D in T's domain |
| 5 | Technology nature | Process/method/formula (hard to reverse-engineer) | Physical component (identifiable in teardown) |
| 6 | Trade secret litigation | Company/industry trade secret theft lawsuits | Patent litigation is the norm |

**Scoring**: 4-6 = high likelihood, 2-3 = possible, 0-1 = unlikely.

**Override rule**: Procurement or teardown evidence can override trade secret finding.

**Note for reverse workflow**: In reverse direction, spend LESS effort on trade secret assessment for each downstream A — the key question is whether B's patents are essential, not whether A could develop internally. Assessment still runs but reduced weight.

**Output**: Trade secret likelihood + indicator breakdown

## Step 4: Multi-lead parallel verification

**Goal**: Activate 5 leads in parallel, each with an independent confidence score. **Every lead must record its evidence timestamp** (evidence freshness, v0.4.0). Detailed scoring rules in `checklists.md`.

### Lead 1 · Patent ownership + quality (confidence: medium, adjusted by quality)
- Forward: Search T's patent holders, identify primary owner B
- Reverse: For each candidate A, search whether A's products use T and whether A holds T patents
- Check patent status, timeline, NPE risk
- **Patent quality scoring (v0.4.0)**: Do not count patents — score them. See `checklists.md` for the 4-factor quality score:
  - Claim breadth (independent claims, scope)
  - Citation impact (forward citations, whether later patents build on it)
  - Family size (PCT/multi-jurisdiction vs single-country)
  - Legal status (granted & maintained vs lapsed/revoked/pending)
  - Quality levels: Core (≥8/12), Supporting (4-7/12), Peripheral (0-3/12)
- Quality-adjust Lead 1 confidence: Core patents → confidence can reach high; Peripheral patents only → cap at low

### Lead 2 · Corporate affiliation (confidence: high)
- Search A-B affiliation via Tianyancha / Qichacha / Qixinbao
- Check: mutual investment, JV, executive overlap, historical changes

### Lead 3 · Talent flow (confidence: medium)
- Search B→A technical-hire / job-change records
- Use WebSearch + job sites
- Multiple technical staff → high likelihood

### Lead 4 · Procurement (confidence: high)
- Forward: Search A's tender announcements, supplier disclosures for B
- Reverse: Search B's listed customers, annual report client disclosures
- Directly named → high; category only → medium

### Lead 5 · Product teardown (confidence: very high)
- Physical evidence of B components in A's products
- Teardown reports / BOM analysis / product certifications

**Evidence freshness (v0.4.0, applies to ALL leads)**:
- Record the date of each evidence item
- Freshness levels:
  - **Current** (≤12 months): full weight
  - **Moderate** (12-18 months): normal weight, flag in report
  - **Stale** (>18 months): down-weight one level; cannot alone support "high" confidence
  - **Unknown date**: treat as stale, flag prominently
- A conclusion resting primarily on stale evidence is capped at "medium"

**Output**: Per-lead hit status + per-lead confidence + patent quality score (Lead 1) + evidence timestamps

## Step 5: Competitive triangulation

**Goal**: Check whether A's industry peers show the same patent gap pattern, providing cross-company corroboration.

**Why this matters**: A single company's patent gap could be random or internal. But if 3-5 industry peers ALL lack T's patents and ALL point to the same technology owner B, the pattern is unlikely to be coincidental.

**Operations**:
1. Identify A's direct competitors / industry peers (C₁, C₂...Cₙ): 3-10 peers, same industry classification, similar product/revenue profile
2. For each peer Cᵢ, check patent gap for T
3. For peers with gaps, check where T likely comes from (same B or different owners)
4. **Quality-aware triangulation (v0.4.0)**: If multiple peers converge on B AND B's patents score as Core quality → strongest possible signal. If B's patents are only Peripheral, convergence is weaker (B may be a paper tiger holding low-value patents).

| Pattern | Interpretation | Triangulation boost |
|---------|---------------|---------------------|
| ≥3 peers same gap → same B, B=Core quality | Industry-wide dependency on genuine tech leader | **+2 levels** |
| ≥3 peers same gap → same B (any quality) | Industry-wide dependency | **+2 levels** |
| ≥2 peers same gap → same B | Significant corroboration | **+1 level** |
| 1 peer same gap → B | Mild corroboration | No boost |
| Peers point to different owners | Fragmented supply → B weaker | No boost, flag |
| Peers have T patents | A is the outlier → investigate | No boost |

**Output**: Peer gap matrix + triangulation boost + quality-aware interpretation

## Step 6: Negative verification (NEW v0.4.0)

**Goal**: Actively attempt to DISPROVE the supply-chain inference. An inference that survives active disproof is far more credible than one that was never tested.

**Core principle**: Positive evidence (patents, affiliations, teardowns) can be coincidental or over-interpreted. Negative verification searches for the "why not" — evidence that B is NOT A's supplier despite the positive signals.

**Operations** — search each of the following for counter-evidence:

1. **Revenue/scale mismatch**:
   - Does B's reported revenue exceed what A could plausibly buy? (if B's revenue is 100x A's procurement budget for T, B may not be A's supplier — or A is trivial for B)
   - Does B's capacity announcement target products A doesn't make?

2. **Product-category mismatch**:
   - Does B's product line actually include what A needs? (B holds T patents but may not manufacture the specific product variant A uses)
   - Check B's product catalog / website for the specific component A needs

3. **Geographic/logistics infeasibility**:
   - Are A and B in incompatible geographies for the component type? (some components are regional by nature — e.g., regulatory, shipping cost)
   - Check trade routes, tariffs, local-content requirements

4. **Explicit customer-list exclusion**:
   - If B publicly lists customers (annual report top-5, website case studies, press releases), does it explicitly EXCLUDE A?
   - If B's top-5 customer list is disclosed and A is not among them AND B's concentration is high → strong negative evidence

5. **Contractor/competitor relationship**:
   - Is A actually a competitor of B in T? (A wouldn't buy from its direct competitor unless forced)
   - Is A's product positioned as a substitute for B's?

6. **Patent-licensing-only alternative**:
   - Does A license B's patents but buy the physical product from a THIRD party (C)? If so, B is a licensor, not a supplier — the supply chain passes through C.

**Negative verification outcome**:

| Outcome | Impact on confidence |
|---------|---------------------|
| Negative evidence FOUND (any of the above confirmed) | **Reduce confidence by 1-2 levels**, flag the specific contradiction. If the contradiction is fundamental (e.g., A is B's direct competitor), the inference may be overturned. |
| Negative search performed, no evidence found | **Confidence confirmed** — record "negative verification passed" in report; supports high confidence |
| Negative search could not be performed (data unavailable) | Note in report; confidence unchanged but flagged as "negative verification incomplete" |

**Critical rule**: The report MUST document that negative verification was attempted. A report without negative verification is incomplete.

**Output**: Negative evidence found/not found + specifics + impact on confidence

## Step 7: Multi-lead fusion + confidence scoring

**Goal**: Cross-validate and produce an overall determination.

**Fusion rules**:
- ≥2 high-confidence leads corroborating → overall "high", can conclude
- 1 high + 1 medium corroborating → overall "medium"
- Only 1 lead hit, no corroboration → overall "low", hypothesis only
- 0 leads hit → terminate, cannot infer

**Trade secret override rules**:
- Trade secret "high" + no procurement/teardown → cap at "low"
- Trade secret "high" + procurement/teardown confirms → no cap

**Triangulation boost** (applied after base scoring):
- +2 levels if ≥3 peers confirm same gap → same B
- +1 level if ≥2 peers confirm same gap → same B
- Triangulation cannot override trade secret cap

**Negative verification adjustment (v0.4.0)**:
- Negative evidence found → reduce by 1-2 levels (or overturn if fundamental contradiction)
- Negative verification passed → no change (recorded as supporting)
- Negative verification incomplete → no change, flag in report

**Evidence freshness adjustment (v0.4.0)**:
- If the conclusion rests primarily on stale (>18 months) evidence → cap at "medium"
- Each lead using stale evidence is down-weighted one level before fusion
- If the only corroborating leads are stale → overall capped at "medium"

**Role determination**:
- Leads 4/5 hit (procurement / teardown) → B is A's direct supplier (forward) / A is B's customer (reverse)
- Only leads 1/2 hit → technology licensor or indirect affiliation
- Lead 1 hit but B is NPE → B licenses only, not in supply chain

**Output**: Overall confidence + all adjustments applied + B's/A's role

## Step 8: Financial cross-validation

**Goal**: Cross-validate the inferred supply-chain relationship against hard financial data.

**Operations** (select applicable checks based on direction):

### Forward direction (A → find supplier B):
1. A's supplier concentration (top-5 supplier list, concentration ratio)
2. A's procurement category matching (does A's procurement align with B's products?)
3. B's customer concentration (if listed: top-5 customers, concentration)
4. Accounts receivable / payable patterns, related-party disclosures

### Reverse direction (B → find customers A):
1. B's customer concentration, revenue by industry segment
2. For each candidate A: top-5 supplier list, related-party disclosures

### Financial corroboration scoring:

| Finding | Corroboration | Confidence effect |
|---------|---------------|-------------------|
| B named as A's supplier / A as B's customer | **Strong** | No cap, confirms |
| Procurement category + revenue size matches | **Medium** | Supports |
| Related-party disclosures confirm | **Strong** | Confirms |
| No financial evidence | **None** | Cap at "medium" |
| Financial data contradicts | **Negative** | Reduce 1 level, flag |

**Output**: Financial corroboration level + specific evidence + confidence cap applied

## Step 9: Alternative-hypothesis check

See `checklists.md`. Explicitly exclude alternative explanations for each inference.

## Step 10: Counter-intelligence check

See `checklists.md`. Check for shell companies / dispersed patents / decoy filings.

## Step 11: Output report

Organize per the I/O contract in SKILL.md. Must include:
- Analysis direction (forward / reverse)
- Relationship determination (incl. role)
- Trade secret assessment result
- Evidence chain (5-lead hit table + confidence + **patent quality scores** + **evidence timestamps**)
- Triangulation result (peer gap matrix + boost applied)
- **Negative verification result** (searched + found/not found + impact)
- Financial corroboration (evidence + level)
- Overall confidence + rationale (all adjustments transparent: trade secret, triangulation, negative verification, evidence freshness, financial)
- Alternative-hypothesis list
- Counter-intelligence risk flag
- Follow-up verification suggestions

---

# Appendix: Reverse Workflow (Supplier → Clients)

## When to use

Trigger when the user provides a technology-owning company B and wants to identify downstream customers. Common scenarios:

- "台积电的先进封装客户有哪些？"
- "Qualcomm's 5G modem customers besides Apple?"
- "哪些车企用了宁德时代的麒麟电池？"
- "What companies depend on ASML's EUV lithography?"

## Process

### R1: Confirm B's patent dominance
- Run Step 2B to validate B's position in T
- **Apply patent quality scoring** to B's core patents — dominance + Core quality = genuine gatekeeper; dominance + Peripheral quality = weak gatekeeper
- If B is not dominant → warn and proceed at reduced confidence

### R2: Identify technology T and its necessity
- What exactly does B's patented technology enable?
- Is T a must-have (essential standard) or a nice-to-have (one of many options)?
- Essential standard → downstream dependency is automatic; non-essential → need product-level evidence

### R3: Candidate screening
- Identify all companies whose products plausibly need T
- Build candidate list: A₁, A₂...Aₙ

### R4: For each high-priority candidate, run abbreviated forward workflow
- Step 2A: Confirm Aᵢ lacks T patents
- Step 3: Quick trade secret check (reduced weight)
- Step 4: Run 5 leads for Aᵢ→B (with evidence timestamps)
- Step 6: Negative verification per candidate
- Step 8: Financial cross-validation (check B's customer list for Aᵢ)

### R5: Aggregate report
- List all confirmed customers with per-customer confidence
- Map B's customer concentration risk
- Flag any unnatural customer concentration (>30% from single customer)
