# house-skills-kit 🏠

**Agent Skills for the Chinese real-estate industry — organized by role, usable one skill at a time.**

English | [中文](README.md)

This repository packages the day-to-day knowledge of Chinese real-estate practitioners into installable AI Skills: standardized `SKILL.md` instruction sets plus dependency-free Python tooling for the calculations that practitioners actually run (mortgage, property tax, provident-fund limits, floor-area efficiency, commission, rental yield, and more).

> 🇨🇳 The content is Chinese-first by design — it encodes how business is actually done in the Chinese market (35-city policy rule library, `认房不认贷` first-home determination, `公积金` loans, `维修基金`, etc.). The skill format is plain `SKILL.md`, so it drops into Claude Code, Hermes, Codex, OpenClaw, or any agent that reads Markdown-based skills.

> **First time here? Read [docs/QUICKSTART.md](docs/QUICKSTART.md)** (Chinese) — 5-minute setup for three runtimes (Claude Code project/user level, Codex via `AGENTS.md` routing, or paste-in-a-chat), three real walk-throughs (a resale agent matching a buyer, a planner building a competitor report, a first-home buyer deciding), plus the usage discipline and the five most common mistakes.

## Why this exists

Searching GitHub, ClawHub, and the major AI app marketplaces for AI skills built for Chinese real estate turns up essentially nothing — despite the industry transacting on the order of ten trillion RMB a year. So this is an attempt at the first, and hopefully most practical, Chinese real-estate AI skill library: business knowledge from the field, turned into skills an agent can actually execute.

**The difference between this and a prompt dump:** every module here (lead grading rules, commission policy, sales scripts, handover inspection checklists, city tax brackets) comes from first-line practice and corporate-standardized workflows, not from an engineer imagining what the domain looks like. Engineers know AI; practitioners know real estate.

## What's inside

### 🧮 calc-toolkit — shared calculation toolset (all roles)

Command-line tools covering the core calculation scenarios of a property transaction. **Pure Python standard library — no installation, no dependencies, Python 3.8+.**

| # | Tool | Command | What it does |
|---|---|---|---|
| 7-1 | Mortgage payment | `mortgage.py` | Commercial / provident-fund / combined loans × equal-installment or equal-principal; rates resolved per city |
| 7-2 | Resale total cost | `tax.py` | Deed tax, VAT, income tax + agent/appraisal/guarantee fees; buyer and seller split |
| 7-3 | Early repayment | `prepay.py` | Shorten-term vs reduce-payment comparison, penalty and minimum-amount warnings |
| 7-5 | Affordability | `capacity.py` | Income and debt → max loan → max price, dual bank-style ratios, bottleneck diagnosis |
| 7-6 | New-home cost | `newhome.py` | Deed tax, maintenance fund (by city × property type), first-year property fee, registration |
| 6 | First/second-home status | `status.py` | Three independent tests (commercial loan / provident fund / deed tax), sell-one-buy-one chaining |
| 7-15 | Floor premium check | `floor.py` | Floor correction × stacked discounts — detects "raise-then-discount" |
| 7-16 | Provident-fund limit | `fund.py` | Minimum of four caps: ceiling / price ratio / repayment ability / balance × deposit-months; multi-child and green-building uplifts |
| 7-17 | Commission calculator | `commission.py` | Resale commission split, channel tiered dual-algorithm reconciliation, rebates, team splits |
| 7-18 | Efficiency ratio | `efficiency.py` | Gross ↔ net ↔ shared ↔ usable area chain; unit-price conversion both ways |
| 7-19 | Rental yield | `rent.py` | Price-to-rent, gross/net yield, payback years, five reference bands, target back-solving |

**35-city rule library** (tier-1 + strong tier-2 + provincial capitals incl. Kunming) with a **four-layer rule engine**:

```
national default → city (e.g. Kunming high-rise maintenance fund 90 CNY/㎡) → district → my-own template
```

- Every number is traceable: output carries its parameter source; rule layers cite the document/number (e.g. "2024 deed-tax announcement No.16: 140㎡ threshold")
- Policy data is separated from code: policy changes mean editing `rules/cities.yaml`, not the tools
- Any parameter can be overridden inline: `--set dti=0.55`

### 🏠 Buyer-side skill (individual home buyers)

| Skill | Content | For |
|---|---|---|
| [buyer-first-home-advisor](skills/buyer-first-home-advisor/) | Seven-question needs clarification → three-line budget (comfort / ceiling / extreme) → eligibility self-check → district five-factor screen + weighted 100-point project scorecard → new-home "five checks" + 15-point resale inspection → negotiation leverage + ten contract clauses → loan options and early repayment → handover and taxes → eight common traps → three-sentence decision summary | First-time buyers, families advising them, agents running buyer-side advisory |

### 🏗 Developer advisory line (decision layer for developers)

| Skill | What it covers |
|---|---|
| [developer-sales-advisor](skills/developer-sales-advisor/) | 12 must-have data points and a five-dimension health check (volume / price / demand / competition / team) on one page, three verdicts (take it / fix then take it / walk away), price-and-incentive architecture with a three-layer discount structure (public discount anchors the price, private discount converts, in-kind swaps protect the price list), channel mix and cost-per-lead analysis with four fraud controls, five symptom-based prescriptions for stalled absorption (each with thresholds, review window and stop-loss), 5-3-2 budget allocation, and developer-facing weekly reports with three-tier recommendations and red lines |
| [project-feasibility-advisor](skills/project-feasibility-advisor/) | Pre-acquisition feasibility for developers: three go/no-go metrics (net margin, dual-scope IRR, land-to-revenue ratio), three positioning questions with mix constraints, six cost blocks and the nine items most often omitted, three-source price anchoring with absorption-year back-solving, sensitivity table plus a decision-threshold matrix, the eight-chapter feasibility report structure with six inflation techniques to watch for, and four city-entry indicators (`feasibility.py` gives breakeven price and sensitivity) |

> The advisory line handles judgment and trade-offs only; floor execution lives in the sales-floor line below, and every calculation runs through [calc-toolkit](skills/calc-toolkit/).

### 🔑 Resale brokerage line (brokerages and second-hand stores)

| Skill | Content |
|---|---|
| [broker-listing-sop](skills/broker-listing-sop/) | Six sourcing channels and a three-filter test for half-hearted listings, seller-motivation questions, four-step price-expectation calibration (market / cost / time / cost of overpricing), three-tier price recommendation, three mandate types with seven mandatory clauses (exclusivity always comes with consideration), a 12-item on-site verification checklist plus photo standards and the listing record, four-tier maintenance with 30/60/90-day triggers, and broker-jumping signals with the four-piece evidence chain |
| [broker-client-deal-sop](skills/broker-client-deal-sop/) | Seven-question needs clarification with four commonly missed down-payment items, eligibility and loan pre-assessment (assess, never promise), three-dimension matching score (hard constraints / soft preferences / risk deductions — every recommendation states its trade-off), three-property showing structure with either-or closing questions, two-sided negotiation (buyer motives vs seller reasons to hold price) with a concession ladder, seven-step transaction flow through to the five handover items, a nine-category risk checklist, and commission scope with broker-jumping responses |
| [broker-lease-sop](skills/broker-lease-sop/) | Leasing operations end to end for agencies: six-item mandate verification with three mandate types and seven mandate clauses, three-source rent pricing with listing-to-closing spread and vacancy arithmetic, the lawful limits of tenant screening plus the 3x income rule and four fraud patterns, ten mandatory lease clauses with deposit and move-in cash structure (commission via `commission.py --scene lease`), five-item handover pack, three-tier repair response, four-step move-out, and four-step arrears handling with four high-risk scenarios |

> This line is written from the practitioner's side (two-sided negotiation, title verification, truthful-listing compliance); buyer-side decision flow lives in [buyer-first-home-advisor](skills/buyer-first-home-advisor/).

### 🏠 Owner-side skills (property holders)

| Skill | What it covers |
|---|---|
| [owner-sell-home-advisor](skills/owner-sell-home-advisor/) | Seller-side decisions end to end: whether and when to sell plus the replacement-sequencing trade-off, four-step pricing (three-source anchors, **net-proceeds back-calculation**, the real cost of overpricing, a de-escalation rhythm), viewability work, six-dimension agent comparison with seven mandate clauses to verify, five questions before accepting an offer with deposit-penalty maths, the full transaction flow with five recurring dispute types and their prevention, and special cases (inheritance, co-ownership, divorce division, mortgage, seizure, school-place occupancy, tenanted sale) |
| [owner-rental-advisor](skills/owner-rental-advisor/) | Landlord-side decisions end to end: rent / sell / hold comparison with gross and net yield plus the break-even appreciation line, rent pricing with vacancy arithmetic, property preparation and compliance red lines (no partition subletting, no change of use), the lawful limits of tenant screening with ten mandatory lease clauses, performance management (repair liability, four-step move-out inspection, four-step arrears handling, entry rights), self-managing vs agency management, and special cases (shared rentals, short stays, school places, subletting) |
| [commercial-property-advisor](skills/commercial-property-advisor/) | Commercial property (shop / office / apartment) investment: the six ways commercial differs from residential, shop location grading with five hardware must-haves and a three-visit footfall check, office three-checks and apartment four-traps, income-approach valuation (NOI / cap rate) with implied-cap reverse lookup for negotiation, ten lease clauses plus four tenant-quality questions, buy thresholds and exit variables, and seven high-risk traps (guaranteed-return schemes, partitioned-title shops, high-cap bait, anchor-tenant dependency, planning hype, commercial-to-residential packaging, transfer taxes). Comes with `commercial.py` (NOI / valuation / implied cap / holding IRR) |

### 🤝 Transaction & handover line (after the deal is signed)

| Skill | What it covers |
|---|---|
| [resale-transaction-sop](skills/resale-transaction-sop/) | Resale transaction end to end as 12 nodes with a responsibility matrix (seller / buyer / agency / bank / registry): six-point title check (ownership, mortgage, seizure and restrictions, co-owners, tenancy, resale restrictions), the three kinds of "money down" and deposit penalty maths, twelve mandatory contract clauses including the three-way branch when the loan is not approved, online filing and escrow, the five reasons loans fail, buyer/seller tax split reported separately, mortgage release and the three redemption routes, six handover steps with a retained-final-payment clause, and seven failure scenes (seizure, missing co-owner signature, sitting tenant, un-migrated household registration, area error, seller walk-away, loan rejection). Uses `tax.py` `deposit.py` `loanterm.py` `status.py` `area_error.py` |
| [handover-inspection-advisor](skills/handover-inspection-advisor/) | Handover inspection: three ground rules (inspect before signing, written record, tracked rectification), pre-visit documents and a sub-200-CNY tool list, six common-area checks first, eight in-unit systems measured (water and drainage, electrical, waterproofing with a 24-48h ponding test, window and door airtightness, hollow plaster, ceiling height and room widths, flues and ventilation, fittings), the 3% area-error line and how gifted space differs, a seven-column defect-list template with a three-level escalation ladder, and 90-day warranty claim mechanics (time, written record, attribution). Uses `area_error.py` `efficiency.py` `newhome.py` |

### 🏢 Sales-floor line (new-home sales teams)

| Skill | Content |
|---|---|
| [sales-talk-library](skills/sales-talk-library/) | 24 script blocks across location / amenities / floor plan / competitors / brand, each with standard wording, segment variants, and failure warnings |
| [sales-objection-handling](skills/sales-objection-handling/) | Four high-frequency objections ("too expensive / let me look around / fear of unfinished project / will it get cheaper") with branching responses and banned phrases |
| [sales-closing-sop](skills/sales-closing-sop/) | Price calculation → concession ladder → buying-signal reading → five-level closing → contract hand-off |
| [sales-reception-sop](skills/sales-reception-sop/) | First-visit walkthrough + seven-dimension needs questioning tree + customer-profile playback |
| [sales-lead-grading](skills/sales-lead-grading/) | ABC lead grading on four dimensions, registration discipline, graded follow-up cadence, lost-lead recovery, re-grading and ownership arbitration |
| [sales-mortgage-sop](skills/sales-mortgage-sop/) | Loan-policy consistency, pre-qualification triage, six high-frequency problem paths (bank statements / credit / down-payment gap / source of funds / income type / provident fund) |
| [sales-opening-sop](skills/sales-opening-sop/) | Pre-launch customer triage, deposit-to-subscription conversion, seven-step launch-day flow, five contingency plans |
| [presale-marketing-sop](skills/presale-marketing-sop/) | Four-stage pre-sale rhythm, warm-up / customer-acquisition / circle-marketing action library, funnel and cost-efficiency review |
| [competitive-intel-sop](skills/competitive-intel-sop/) | Competitor A/B/C grading, six-module on-site collection checklist, 100-point scoring, weekly supply/absorption/price monitoring |
| [activity-organization-sop](skills/activity-organization-sop/) | Single-event objective setting, event-type matrix, one-page brief, budget approval, execution checklist, 72-hour review |
| [marketing-materials-sop](skills/marketing-materials-sop/) | Material task classification, design brief, compliance review, four-layer show-area inspection, version management |
| [engineering-progress-broadcast-sop](skills/engineering-progress-broadcast-sop/) | Construction-data collection, milestone mapping, quality/craft messaging, delay communication, escalation |
| [pricing-incentive-release-sop](skills/pricing-incentive-release-sop/) | Price-fact verification, inventory/customer segmentation, discount ladder, approval and change control, ledger review |
| [channel-collaboration-sop](skills/channel-collaboration-sop/) | Channel onboarding tiers, policy training, registration and duplicate checks, visit hand-off, lead arbitration, commission reconciliation |
| [channel-management-advisor](skills/channel-management-advisor/) | Decision layer for channel/distribution management: visit-structure back-solving for channel mix, dependency red lines, four-step commission pricing with **dual-algorithm tier maths** (whole-amount jump vs progressive brackets, both computed by the tool), fast-commission and cash-bonus toolbox with cost-efficiency ceilings, A/B/C tiering with eight mandatory contract clauses, three-stage attribution and dispute arbitration, six-metric channel diagnostics with four health profiles, broker-jumping signals and penalty ladder, and monthly channel reviews plus annual framework negotiation |
| [property-media-creator](skills/property-media-creator/) | End-to-end content engine for real-estate creators: three-circle positioning with five persona types, four-source topic bank (client questions / search suggestions / comments / site visits) with topic cards, eight hooks for the first three seconds plus format-specific scripts (10s news flash, 15s deep dive, walkthrough, policy), camera and subtitle standards (zero typos, keywords in the upper third, banned-word list), cover design with A/B, five platform red lines with shadow-ban diagnosis, comment and DM conversion in six sentences, four-metric review with stop-loss rules, and four monetisation paths with disclosure duties |
| [customer-advocacy-referral-sop](skills/customer-advocacy-referral-sop/) | Service-feedback tiers, testimonial authorization, referral triggers, lead registration, benefit fulfillment, complaint isolation |
| [launch-integrated-campaign-sop](skills/launch-integrated-campaign-sop/) | Launch-campaign brief, nine-cell coordination, milestone back-planning, asset package, full-staff rehearsal, post-launch review |

Plus template modules `marketing-review` (monthly marketing review and business dashboard) and `media-lead-growth` (paid media, budget stop-loss, creative testing, lead attribution).

## Quick start

```bash
git clone https://github.com/danfeistar/house-skills-kit.git
cd house-skills-kit

# 1) Run a calculation — no install, stdlib only
python3 skills/calc-toolkit/mortgage.py --price 1500000 --downpay 30 --years 30 --city 昆明
python3 skills/calc-toolkit/capacity.py --income 12000,8000 --cash 400000 --debts 1500 --city 昆明
python3 skills/calc-toolkit/tax.py --price 1500000 --area 89 --city 昆明 --first 1 --held 6 --unique 1

# 2) Use a skill — each directory is a self-contained SKILL.md
cat skills/buyer-first-home-advisor/SKILL.md

# 3) Generate a white-labeled advisory skill from a brand config
python3 render.py --config examples/kunming/kunming.buy.yaml --out output/my-brand/
```

## Repository structure

```
skills/            # 18 self-contained skills, each with SKILL.md (+ README.md, playbook, optional tools)
  calc-toolkit/    #   shared calculators + 35-city rule library (rules/cities.yaml)
  buyer-*/         #   buyer-side (C-end) skills
  sales-*/         #   sales-floor skills
template/
  archetypes/      # 4 role archetypes (buyer / developer sales / brokerage agent / channel distributor)
  modules/         # 31 business modules to compose an archetype
examples/          # runnable brand configs (Kunming end-to-end example, developer example)
adapters/mock/     # mock data adapter — swap in your own listing source
render.py          # renders a branded skill from a config + template
tools/             # repo maintenance scripts (skill validator, see CONTRIBUTING)
```

## Two production lines

1. **`skills/` — directly publishable skills**: each subdirectory is an independent `SKILL.md`, publishable to ClawHub as its own skill and installable on its own.
2. **`template/` — branded generation skeleton**: 4 role archetypes × 31 business modules; one brand config yields a bespoke advisor skill (`render.py`).

## Distribution

| Platform | Link |
|---|---|
| GitHub (primary) | [github.com/danfeistar/house-skills-kit](https://github.com/danfeistar/house-skills-kit) |
| Gitee (China mirror) | [gitee.com/danfeistar/house-skills-kit](https://gitee.com/danfeistar/house-skills-kit) |
| AtomGit (China mirror) | [atomgit.com/danfeistar/house-skills-kit](https://atomgit.com/danfeistar/house-skills-kit) |
| ClawHub skill marketplace | [clawhub.ai/skills/house-skills-kit](https://clawhub.ai/skills/house-skills-kit) |

## Roadmap

| Role | Skill | Status |
|---|---|---|
| All roles | `calc-toolkit` shared calculators | ✅ released (19 tools) |
| Sales floor | `sales-*` five-skill line | ✅ released |
| Home buyers | `buyer-first-home-advisor` | ✅ released |
| Developer sales | project sales advisor | planned |
| Sales agent | agent follow-up assistant | planned |
| Resale broker | broker workflow assistant | planned |
| Channel distribution | channel management assistant | planned |
| Real-estate content creator | content creation assistant | planned |

## Contributing

Issues and pull requests are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). Please open an issue before a large PR so we can agree on scope. Response target: within a few days.

## Author

**老何 (He)** — 17 years in Chinese real estate, former marketing head for multiple developers in Yunnan, long-time Kunming market practitioner and early AI adopter. Currently building a real-estate AI platform (developer side, brokerage side, sales-agent side, home-buyer side).

**Business cooperation:** need AI tooling or AI workflows for your development company, brokerage, or sales team? Reach the author via his [GitHub profile](https://github.com/danfeistar).

## License

Apache-2.0
