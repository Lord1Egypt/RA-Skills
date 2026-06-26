---
name: kpi-tree-design-coach
description: Coach a CEO, COO, CFO, Head of Strategy, Head of Operations, or VP-level functional leader through designing or rebuilding a KPI tree (also known as North Star Metric tree, OKR tree, value driver tree, metric tree, or key results tree) for a company, business unit, or function. KPI tree design is one of the highest-leverage strategy artifacts but most companies do it badly — they have a "metric soup" of 50 dashboards instead of a hierarchical decomposition of the one metric that matters into the operational levers people actually pull. Covers the foundational concepts (input metrics vs output metrics; leading vs lagging; lead-time of the metric; metric ownership vs metric awareness; the difference between a North Star Metric and a KPI tree), the North Star Metric selection (single-metric vs constellation; the criteria — measures customer value created, predicts long-term revenue, captures the business model), the tree structure (root → 1st-level drivers → 2nd-level drivers → operational metrics; multiplicative vs additive vs composite relationships; the 3-4 levels rule), the metric-tree archetypes by business model (B2B SaaS subscription, B2B SaaS PLG, B2C subscription, B2C transactional/e-commerce, marketplace, ad-supported media, fintech, healthcare/regulated), the operational principle (each leaf metric must be ownable by a specific person and movable on a sub-90-day timeframe), the cadence and ritual design (weekly business review, monthly operating review, quarterly strategy review — what each consumes from the tree), the integration with OKRs (the tree provides denominator metrics; OKRs are quarterly initiatives that move them; KRs are not metrics in themselves), the integration with planning (the tree is the spine of the operating plan and budget), the most-common failure modes (metric soup; vanity-metrics in the tree; too many leaves; metric ownership ambiguity; trees that ignore unit economics; trees that ignore quality; LTV/CAC as North Star is wrong; activity metrics in customer-outcome tree), the tooling decisions (Looker / Tableau / Sigma / Mode / Hex / Metabase / Sigma — and dedicated metric-tree tools like Klipfolio, Mosaic, Metabase, ChartMogul, Equals), the role of CFO and FP&A in maintaining the tree, the role of executive team in interpreting the tree, the data-engineering reality (most KPI trees fail because the data pipeline doesn't exist), and the difference between KPI tree, OKR tree, MOO/MoMo, value-driver tree, and balanced scorecard. Use when leader says "we have too many metrics", "what should our North Star be", "design our KPI tree", "metric tree for our company", "input vs output metrics", "OKR tree refresh", "operating plan metrics". Triggers on phrases like "KPI tree", "metric tree", "North Star Metric", "OKR tree", "value driver tree", "key results tree", "balanced scorecard", "operating metrics", "operational KPIs", "leading indicators", "input metrics", "lagging indicators", "metric ownership", "metric soup".
---

# kpi-tree-design-coach

Coach a CEO, COO, CFO, or Head of Strategy through designing (or rebuilding) a KPI tree — the hierarchical decomposition of the company's North Star Metric into operational levers that specific people can pull on sub-quarterly timeframes. KPI tree design is one of the highest-leverage strategic artifacts, and most companies have either nothing or a "metric soup" instead. A good tree drives operating discipline, focus, planning, board confidence, and 1:1 conversations.

This skill is for leaders who own or significantly influence the company's metric system. For functional KPI design (sales-only, marketing-only), the same principles apply but at narrower scope.

## When to engage

Trigger when:
- "We have too many metrics — how do we focus?"
- "What should our North Star Metric be?"
- "Design our company's KPI tree"
- "Our OKRs aren't connected to anything"
- "Board wants a clearer view of operational metrics"
- "Refreshing our operating plan / metrics for next year"
- "Just hired as CFO and we have 80 metrics, none ownable"
- "Investor said our metric story is muddled"

Don't engage when:
- The user wants a single metric calculated (this is an instruction skill, not an analysis skill)
- The user wants OKR writing help (different skill — OKR design)
- The user wants dashboard / BI tool selection (use a different skill)

## Diagnostic intake (run first)

1. **Business model?** — B2B SaaS subscription, B2B SaaS PLG, B2C subscription, B2C transactional / e-commerce, marketplace, ad-supported media, fintech, healthcare-regulated, hardware. Each has a different tree shape.
2. **Stage?** — Pre-PMF, post-PMF / Series A, B/C scaling, growth, public, PE-owned. Stage determines depth of tree and frequency of refresh.
3. **Current metric reality?** — Single dashboard? Many dashboards? Spreadsheets? Different metrics in board pack vs ops review? Metric soup? Documented tree? Just OKRs, no tree?
4. **Existing North Star?** — If yes, is it the right one? Has it changed in 18 months? Is it owned?
5. **Decision-driver gap?** — Which decisions are being made without good metric backing? Pricing? Pipeline forecasting? Hiring plan? Budget allocation?
6. **Org context?** — Founder-led, CEO-led, professionally-managed, PE-owned, public. Different governance for the tree.
7. **Data + analytics maturity?** — Is the pipeline ready to support a tree? Or do you need to build the data foundation first?
8. **Time horizon for impact?** — Tree-redesign for next quarter? Annual plan? IPO prep?

## Foundational concepts (get these right before designing)

### Input metrics vs output metrics
- **Output metric** (lagging): result. Revenue, churn, net new ARR, GMV, MAU.
- **Input metric** (leading): controllable activity that drives output. Sales calls per AE, pipeline created per SDR, content published per week, NPS by segment.
- **Why this matters:** A tree of only outputs tells you what happened. A tree of inputs tells you what to do. **A useful tree is mostly inputs at the leaf level.**

### Leading vs lagging horizon
Every metric has a "lag time" — the time between the action and the metric showing it.
- Sales-call volume: today (real-time)
- Demos: today (1 day lag)
- Pipeline: 1-2 weeks lag
- Bookings: 30-90 days lag
- Revenue: 30-90+ days lag
- Cohort retention: 6-12 months lag
- LTV: 12-36 months lag
- A useful tree has metrics at each lag horizon. **Don't have a tree where everything has 90+ days lag** — you can't manage anything in real-time.

### Metric ownership vs awareness
- **Owned**: a specific person (or small team) can move this metric in <90 days through their daily/weekly actions
- **Aware**: leadership tracks but isn't responsible for daily action
- **Every leaf metric in the tree must be owned.** If it's not owned, either fix the org structure or remove the metric.

### North Star Metric vs KPI tree
- **North Star Metric (NSM)**: single metric that captures the customer value the company creates and predicts long-term revenue. Examples: Spotify's "time spent listening", Airbnb's "nights booked", Slack's "messages sent within paid teams", Shopify's "GMV processed", a B2B SaaS's "ARR" or "active customers" or "seats activated".
- **KPI tree**: the hierarchical decomposition of the NSM into operational levers.
- **The relationship**: NSM is the root of the tree. The tree is the operational plan to move it.

### What a KPI tree is NOT
- A list of all metrics tracked
- A balanced scorecard (related but different — balanced scorecard is across financial, customer, internal, learning perspectives; KPI tree is decomposition)
- An OKR tree (related but OKRs are initiatives, not metrics)
- A dashboard

## North Star Metric selection

### The 5 criteria for a good NSM
1. **Captures customer value created** — measures something good customers experience, not just what makes the company money
2. **Predicts long-term revenue** — if this number goes up, revenue follows in 6-24 months
3. **Stable over time** — doesn't change with every product release or strategic pivot
4. **Single metric, not composite** — a number, not "growth × retention × margin"
5. **Quantifiable from existing data** — you can compute it monthly without heroics

### Common B2B SaaS subscription NSM choices
- **ARR (Annual Recurring Revenue)** — financial, captures growth + retention. Good but financial-flavored. Most common at Series B+.
- **Active customers / seats** — captures value-delivered. Good for usage-priced or per-seat products.
- **Activated accounts** — captures depth of adoption. Good for PLG.
- **Net New ARR** — captures only growth in current quarter. Too narrow for North Star; better as a 1st-level driver.

### Common PLG NSM choices
- **Weekly active users at paid customers** — captures product engagement, predicts retention
- **Active workspaces** — for collaboration tools
- **Activations per week** — for self-serve products
- **Power-user count** — users who hit a depth threshold

### Common B2C subscription NSM choices
- **Subscriber-weeks-watched** (Netflix-style) — engagement × subscribers
- **Active subscribers** — simpler, less rich
- **Engaged subscribers** (some engagement threshold)
- **Net new subscribers** — only growth, narrower

### Common B2C transactional NSM choices
- **GMV** — captures purchase volume
- **Active buyers per period** — captures customer breadth
- **Purchase frequency × buyers × AOV** — too composite to be NSM, but it's the tree below
- **Repeat purchases** — captures stickiness

### Common marketplace NSM choices
- **GMV** — total transaction value
- **Active matches per period** — transactions completed
- **Liquidity ratio** — % of supply with demand match
- **Repeat-transaction rate** — captures stickiness

### Common media / ad-supported NSM choices
- **Time spent / engagement** — predicts ad inventory + retention
- **Daily active users** — narrower
- **Sessions per user per week** — depth metric

### When you should NOT have a single NSM
- Multi-product companies where the products have fundamentally different value props (consider sub-NSMs by business unit)
- Companies in early experimentation phase where the value prop isn't clear
- Holding companies with portfolio of businesses

In these cases, use a **constellation of 3-5 metrics**, not a single NSM. Documented as such, not pretending to be a tree.

## KPI tree structure

### The 3-4 level rule
- **Level 0 (root)**: NSM
- **Level 1**: 2-4 multiplicative drivers of NSM
- **Level 2**: 2-4 drivers of each L1 metric
- **Level 3 (leaves)**: operational metrics, owned by specific people, movable in <90 days

**A tree with 5+ levels is too deep.** People won't navigate it.
**A tree with 1-2 levels is too shallow.** It's just a North Star and dashboards, not a tree.

### Multiplicative vs additive vs composite relationships
- **Multiplicative**: NSM = A × B × C × D. Most common for transactional businesses. e.g., Revenue = Customers × ARPU × Retention × Frequency.
- **Additive**: NSM = A + B + C. Common when there are multiple revenue streams.
- **Composite (formula)**: NSM = function(inputs). Less common; used when there's a specific definition (e.g., LTV = ARPU × GM% / Churn rate).

**Always show the math.** A tree that doesn't show how the math rolls up isn't a tree.

### Example tree (B2B SaaS subscription)
```
ARR (root)
├── New ARR
│   ├── # of new customers (won)
│   │   ├── # of qualified opportunities
│   │   │   ├── # of MQLs
│   │   │   ├── MQL-to-SQL conv %
│   │   │   ├── SQL-to-Opp conv %
│   │   │   └── (paid + organic + outbound + referral inputs)
│   │   ├── Opp-to-close win rate
│   │   └── Sales cycle days
│   └── Average new ARR per customer (ACV)
│       ├── Tier mix (% Pro, % Enterprise)
│       ├── Discount rate %
│       └── Multi-year contract mix %
└── Retained ARR
    ├── Logo retention rate
    │   ├── Implementation success rate
    │   ├── 90-day activation rate
    │   ├── Time-to-first-value
    │   └── CSAT in-product
    └── Net dollar retention (NRR)
        ├── Gross retention rate
        ├── Expansion ARR
        │   ├── Seat expansion
        │   ├── Tier upgrade rate
        │   ├── Usage-based growth
        │   └── Cross-sell new product
        └── Contraction ARR
```

Each leaf metric is owned by a specific person/team:
- # of MQLs → Demand Gen Manager
- MQL-to-SQL conv → Demand Gen + Sales Dev jointly
- Opp-to-close win rate → AE Manager
- 90-day activation rate → CS Onboarding Lead
- Tier upgrade rate → CS Manager + Account Manager

## Metric-tree archetypes by business model

### B2B SaaS subscription
NSM: ARR or Active Customers
L1 drivers: New ARR + Retained ARR (multiplicative-ish since you need both)
L2: # new customers × ACV + retention × NRR
L3: pipeline metrics, conversion metrics, retention metrics

### B2B SaaS PLG
NSM: Active Workspaces or Activated Users at Paid Customers
L1: Signups → Activated → Engaged → Paid → Expanding
L2: Activation rate × Engagement rate × Conversion rate × Expansion rate
L3: time-to-first-value, weekly-active-rate, paid-conversion rate, seat-expansion rate

### B2C subscription
NSM: Net Adds or Engaged Subscribers
L1: New Subs - Cancellations + Reactivations
L2: Acquisition channels × CAC; Churn drivers; Reactivation campaign performance
L3: paid-channel ROAS, organic-search visits, content-engagement rates, exit-survey reasons, win-back-campaign ROI

### B2C transactional / e-commerce
NSM: GMV
L1: Buyers × Frequency × AOV
L2: New buyers + Repeat buyers; Purchases per buyer per period; Mix-shift drivers
L3: paid-acquisition CAC, organic SEO traffic, cart-abandonment rate, recommendation-engine CTR

### Marketplace (B2B or B2C)
NSM: GMV or Active Matches
L1: Supply × Demand × Match Rate
L2: New supply / churn; New buyers / repeat buyers; Match algorithm metrics; Trust / reviews
L3: Onboarding completion %, listing quality score, time-to-first-transaction, dispute rate

### Ad-supported media
NSM: Time Spent or Daily Active Users
L1: Reach × Frequency × Session Length
L2: Acquisition; Engagement; Retention
L3: install rate, content-engagement, push-open rate, weekly-active rate

### Fintech (lending / payments / wealth)
NSM: Active Users × ARPU (often for net interest margin) or AUM (for wealth)
L1: User growth × Activation × Engagement × Monetization
L2: Onboarding completion, KYC pass rate, first-transaction rate, recurring-transaction rate
L3: KYC verification time, deposit funding rate, transactions per active per week

### Healthcare / regulated
NSM: Outcomes-based (e.g., Patients with improved condition) or Visits or Active Members
L1: Population × Engagement × Outcomes
L2: Acquisition (in-network referrals, marketing); Engagement (visits, app-use); Outcomes (clinical metrics)
L3: in-network referral rate, app-engagement, outcomes by condition, NPS by visit

## Operational principle: ownability + sub-90-day movability

For each leaf metric, ask:
1. **Is there a specific person (or small team) who owns moving this number?** If not, fix org structure or remove the metric.
2. **Can this metric be meaningfully moved in <90 days through specific actions?** If it takes 12 months to move, it's not a leaf — it's a parent.
3. **Does the owner have a budget / authority / tools to move it?** If not, the ownership is fake.

If 3 yeses → the metric is a real leaf.
If any nos → it's not a leaf; restructure the tree.

## Cadence + ritual design

The tree drives operational cadence:

### Weekly Business Review (WBR) — frontline + functional leaders
- Cover: leaf metrics that move in <7 days
- Format: 30-60 min
- Outcome: identify "what changed" and "what we'll do this week"
- Example: pipeline-created, demos-booked, cart-abandonment-rate, bug-resolution-rate

### Monthly Operating Review (MOR) — exec team + functional VPs
- Cover: L1 + L2 metrics; deviations from plan
- Format: 90-120 min
- Outcome: cross-functional issue resolution, monthly forecasting, hiring decisions

### Quarterly Strategy Review (QSR) — exec team + board (sometimes)
- Cover: NSM + L1 metrics; operating plan vs actual; strategic implications
- Format: half-day
- Outcome: re-plan if needed, strategic decisions

### Annual Operating Plan (AOP)
- Tree is the spine of the AOP. Each metric has a target with explanation of how to hit it.
- AOP should reference the tree explicitly.

## Integration with OKRs

KPI trees and OKRs serve different purposes; both are needed:

- **KPI tree**: the metric system. Always-on. The denominator.
- **OKRs**: quarterly initiatives + key results. Episodic. The acceleration. KRs are typically *about* metrics on the tree.

Example OKR (B2B SaaS):
- Objective: Reduce churn in Enterprise segment
- KR1: Improve gross retention from 88% to 93% (this is a metric on the tree — gross retention)
- KR2: Achieve 50% adoption of new feature X among Enterprise customers (this is also a metric, possibly on the tree as a depth-of-engagement metric)

OKRs without a tree → people pursue arbitrary KRs that don't connect to North Star
Tree without OKRs → no quarterly focus / acceleration; tree becomes ambient reporting

## Integration with operating plan + budget

The tree is the spine of the operating plan:
- Each L1 metric has a target ("New ARR target = $X")
- Each L2 metric has a target ("New customers = Y, ACV = $Z, total = $X")
- Each L3 metric has a target ("# of MQLs = Q, MQL-to-SQL = R%, SQL-to-Opp = S%")
- The math rolls up; budget supports the leaves

Budget without tree → spending without metric accountability
Tree without budget → metrics without resources to move them

## The most-common failure modes

### Metric soup
**Symptom:** 50 dashboards, no hierarchy, no clear NSM.
**Fix:** Start over with NSM selection. Get exec team in a room and force prioritization to a single number (or 3-5 if multi-business).

### Vanity metrics in the tree
**Symptom:** Tree includes "press mentions per quarter", "Twitter followers", "blog subscribers".
**Fix:** Each metric must pass the "if this triples, does our business meaningfully improve" test. If unclear, it's vanity.

### Too many leaves
**Symptom:** L3 has 30 metrics; nobody can attend to all of them.
**Fix:** L3 should have 12-25 metrics total across the tree. More than that and you're back to metric soup.

### Metric ownership ambiguity
**Symptom:** "Marketing-Sourced Pipeline" is owned by "Marketing AND Sales" — i.e., nobody.
**Fix:** Single owner per metric. Joint ownership = no ownership.

### Trees that ignore unit economics
**Symptom:** Tree focused on growth metrics; CAC, LTV, gross margin, payback nowhere.
**Fix:** Either include unit-economics metrics on the main tree, or maintain a parallel "unit-economics tree" that the CFO owns.

### Trees that ignore quality
**Symptom:** Pipeline, bookings, revenue all there; NPS, CSAT, support volume, customer-effort-score nowhere.
**Fix:** Quality / experience metrics must be in the tree, especially at the leaf level.

### LTV/CAC as North Star
**Symptom:** "Our North Star is LTV/CAC > 3"
**Fix:** LTV/CAC is a *guardrail*, not a North Star. NSM should measure customer value created. LTV/CAC is a financial efficiency metric; it goes on the tree but not as the root.

### Activity metrics in customer-outcome tree
**Symptom:** "Demos done", "calls made", "emails sent" treated as leaves.
**Fix:** Activity metrics are inputs to outcome metrics. They can be in the tree but should be very-low-leaves with clear owner-accountability. Don't measure activity for its own sake.

## Tooling decisions

### What you need
- A canonical tree document (Notion, Coda, Confluence, Almanac, Slab)
- A live metric source (data warehouse + BI tool)
- A weekly metric review artifact (slide / dashboard)

### BI tool choices
- **Looker**: powerful, expensive, complex; best for Series C+ companies with data team
- **Tableau**: also powerful, slightly less complex
- **Sigma**: spreadsheet-style, popular with finance teams
- **Mode**: SQL-first, popular with analytics-heavy companies
- **Hex**: notebook-style, great for analytics + storytelling
- **Metabase**: open-source-ish, growing market
- **Sigma Computing**: another rising option

### Dedicated metric-tree / dashboarding tools
- **Klipfolio, Dasheroo, Geckoboard**: dashboards-only
- **Mosaic**: financial-planning tool, has tree-building features
- **ChartMogul, Equals, MetricBase**: subscription-business-specific
- **Lattice for OKRs** (separate from KPI tree, but linked)

### What you don't need (yet)
- A purpose-built "metric tree" tool — Notion + a BI tool is enough for 95% of companies
- 5+ BI tools — pick one, master it

## The data-engineering reality

**Most KPI trees fail because the data pipeline doesn't exist.** A tree that requires "monthly cohort retention by segment" is meaningless if your data warehouse can't produce that.

**Before designing the tree, audit:**
- What data exists in the warehouse / source systems?
- What metrics are computable today?
- What's the cost (time / engineering) to compute the metrics that aren't ready?

**Phased approach:**
- **Phase 1** (weeks 1-4): design the tree based on what's instrumentable today + key gaps
- **Phase 2** (weeks 5-12): close the highest-priority data gaps
- **Phase 3** (months 4-6): full tree operational

Don't design the perfect tree on paper that takes 12 months to instrument.

## CFO + FP&A's role

The CFO is the natural steward of the tree. FP&A maintains it.

- **CFO**: defines + reviews the tree quarterly; uses it for planning + board pack
- **FP&A**: maintains the data, computes metrics monthly, surfaces variances
- **Each functional VP**: owns their L2 / L3 leaves; brings them to MOR

If the CFO doesn't own the tree, **someone has to** — usually a Head of Strategy or Chief of Staff. Don't let it be ownerless.

## Related but distinct frameworks

### Balanced scorecard
- 4 perspectives: financial, customer, internal process, learning & growth
- Strategic but less hierarchical than KPI tree
- More common in older / industrial companies; less common in tech
- Can complement KPI tree

### MOO/MoMo (Metric of Metrics, Mother of Mothers)
- An older/internal Amazon term for the metric-tree concept
- Same idea, different name

### V2MOM (Salesforce framework)
- Vision, Values, Methods, Obstacles, Measures
- Methods/Measures connect to the tree but the framework is broader
- Strategic / cultural framework that includes metric system

### Wardley Mapping
- Strategic mapping, not metric system
- Doesn't replace KPI tree but complements it

## Output format

Always produce:
- **NSM recommendation**: 1-3 candidates with reasoning, single best choice
- **Top-of-tree structure**: L0, L1, L2 with multiplicative or additive math
- **Leaf-level metrics**: 12-25 across the tree, each with owner + cadence
- **Cadence design**: WBR / MOR / QSR / AOP integration
- **OKR integration**: how to use the tree as the denominator for KRs
- **Data-engineering gap analysis**: what needs to be instrumented in next 60 days
- **Failure-mode flags**: which 2-3 modes are highest risk for this company
- **Refresh cadence**: how often to revisit the tree (annually + on major strategy shifts)

## Anti-patterns

- Don't recommend a 50-metric tree — too many to attend to
- Don't recommend "growth × engagement × retention" as North Star — it's not a metric, it's a formula
- Don't include vanity metrics on the recommendation
- Don't allow "joint ownership" of metrics
- Don't ignore unit economics or quality metrics

## What "great" looks like

- Single page tree document, exec team can recite from memory
- Each metric has a single owner, refreshed in CRM/BI tool
- Weekly cadence reviewed; deviations explained; actions tracked
- OKRs link explicitly to leaf metrics
- Operating plan and budget reflect tree
- Board pack uses tree's L0/L1
- Major strategic decisions reference tree (e.g., "we're investing in X because it moves Y leaf metric")

A bad result looks like:
- "Tree" exists but exec team can't recite it
- Metrics in board pack don't match metrics in MOR don't match metrics in BI tool
- OKRs don't link to anything on the tree
- Vanity metrics in the tree (press mentions, blog subscribers)
- Too many metrics; team is fatigued
- Tree hasn't been refreshed in 18 months

Coach toward the first picture, away from the second.
