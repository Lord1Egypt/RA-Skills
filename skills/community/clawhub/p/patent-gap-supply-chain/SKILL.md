---
name: patent-gap-supply-chain
description: 'Competitive intelligence workflow that infers supply-chain
  relationships from patent gaps — with trade secret assessment, competitive
  triangulation, negative verification, patent quality scoring, evidence
  freshness tracking, reverse workflow (supplier→client), and financial
  cross-validation. 通过"专利缺口"反推产业链关系的竞争情报工作流，集商业秘密评估、竞对三角验证、
  负向验证、专利质量评分、证据时效追踪、反向工作流（供应商→客户）、财务数据交叉验证于一体。
  Use when researching tech/hardware/manufacturing/pharma stocks, analyzing
  industry supply chains, identifying suppliers or customers, investigating
  patent gaps, or inferring supply-chain relationships from patent ownership.
  Supports both forward (patent gap → supplier) and reverse (technology owner →
  downstream clients) analysis directions. 触发场景：科技股研究、行业分析、产业链推断、
  供应商识别、客户挖掘、专利缺口分析、专利归属查询、技术依赖分析、上下游推断 / Triggers:
  patent gap analysis, supply chain inference, supplier identification,
  customer identification, technology dependency, competitive intelligence,
  tech stock research, industry analysis, trade secret assessment, negative
  verification, patent quality, financial cross-validation, reverse
  supply-chain analysis. The skill starts from a patent gap (or known technology
  owner), evaluates trade secret likelihood, activates five verification leads
  with competitive triangulation, runs negative verification to rule out false
  positives, scores patent quality, tracks evidence freshness, then
  cross-validates against financial disclosures, outputting a
  confidence-scored supply-chain inference report.'
version: 0.4.0
agent_created: true
disable: true
---

# Patent Gap Supply Chain Inference

## Overview

This skill implements a competitive intelligence workflow: "patent gap → supply chain inference." Core insight: when target company A's product uses technology T, but A holds no patents related to T, there may be a technology-licensing or supply-chain dependency. By searching T's patent ownership to identify company B, then activating multiple verification leads, one can infer whether B has entered A's supply chain.

**Critical caveat**: A patent gap can also mean A protects T as a **trade secret / know-how** rather than through patents. Patents require public disclosure; many companies (especially in semiconductor processes, chemical formulations, pharma manufacturing) deliberately choose trade secrets. This skill explicitly evaluates this distinction before concluding supply-chain dependency.

**v0.4.0 new capabilities**:
- **Patent quality scoring**: Not all patents are equal. A core patent (broad claims, high citations, PCT family) carries far more weight than a peripheral patent (narrow claims, single jurisdiction). Lead 1 now scores patent quality, not just quantity.
- **Negative verification**: Actively search for evidence that B is NOT A's supplier (revenue mismatch, capacity mismatch, geography, explicit customer lists excluding A). Only when negative evidence fails does the positive chain stand. This is the strongest defense against false positives.
- **Evidence freshness tracking**: Every lead carries an evidence timestamp. Evidence older than 18 months is flagged and down-weighted; conclusions resting on stale evidence cannot reach "high" confidence.
- **Quality × triangulation interplay**: Patent quality scoring feeds into triangulation — peers converging on the same HIGH-QUALITY patent holder is much stronger than convergence on a peripheral patent holder.

The skill downgrades "patents" from the sole evidence chain to an entry lead, enforcing multi-lead parallel verification, competitive triangulation, negative verification, financial cross-validation, alternative-hypothesis checks, and counter-intelligence checks to prevent overconfident wrong conclusions.

## When to Use

Trigger when any of the following applies:

**Forward direction** (patent gap → find supplier):
- Researching tech, hardware, manufacturing, pharma, or materials companies where supply chain matters
- Discovering or suspecting a company uses a technology but lacks related patents
- Explicitly asked to do patent ownership analysis, technology dependency analysis, or supply-chain inference

**Reverse direction** (technology owner → find clients):
- A company B holds dominant/monopoly patents in a technology T and you want to identify B's downstream customers
- Investment thesis: "B is the sole/dominant supplier of T; companies using T must be B's customers"
- Asked to identify companies that depend on a specific technology or component

Trigger keywords (bilingual): 科技股研究, 行业分析, 产业链, 供应链, 供应商识别, 客户挖掘, 上下游推断, 专利缺口, 专利归属, 技术依赖, 专利质量, 负向验证, patent gap, supply chain, supplier identification, customer identification, technology dependency, competitive intelligence, patent quality, negative verification, reverse supply chain.

## Step 0: Applicability Pre-check (mandatory)

Before running the workflow, judge whether the target type is applicable. See `references/industry-guide.md` for industry-specific dynamics:

| Target type | Applicability | Handling |
|-------------|---------------|----------|
| Hardware / manufacturing / pharma / materials | Strong | Proceed. Reference `industry-guide.md` for vertical-specific signals |
| Software / internet | Weak | Warn that patent protection is weak and tech is hidden; suggest code / open-source intelligence; may proceed at reduced confidence |
| Business-model innovation | Not applicable | Stop; suggest financial reports / prospectus / business-model analysis instead |

When not applicable, clearly inform the user and suggest alternatives. Do not force execution.

## Direction Selection

Before proceeding, determine the analysis direction:

| Direction | Starting point | Goal | Trigger phrase examples |
|-----------|---------------|------|------------------------|
| **Forward** | Company A uses T but lacks T's patents | Find who supplies T to A | "Identify XX's suppliers", "Who provides XX's technology?" |
| **Reverse** | Company B holds dominant T patents | Find who depends on B's T | "Who are B's customers?", "What downstream companies need this patent?" |

Both directions share the same verification leads, but the entry point and initial search differ. See `references/workflow.md` for detailed reverse-workflow operations.

## Workflow Overview

The full workflow has 11 steps. Detailed operations in `references/workflow.md`:

1. **Trigger lead identification**: Confirm target company, product, technology; determine forward or reverse direction
2. **Patent gap confirmation** (forward) / **Patent dominance confirmation** (reverse): Search patent portfolio, determine gap validity or market dominance
3. **Trade secret assessment**: Evaluate whether gap reflects deliberate trade secret / know-how protection
4. **Multi-lead parallel verification**: Activate 5 leads — patent ownership, corporate affiliation, talent flow, procurement, product teardown. **Patent quality scoring** applied to Lead 1.
5. **Competitive triangulation**: Check A's peers/competitors for the same patent gap. If ≥2 peers also lack T's patents and all point to B, boost confidence.
6. **Negative verification** (NEW v0.4.0): Actively search for evidence that B is NOT A's supplier. Only when negative evidence fails does the positive chain stand.
7. **Multi-lead fusion + confidence scoring**: ≥2 high-confidence leads corroborating required; triangulation provides confidence multiplier; **evidence freshness adjustment** applied (NEW v0.4.0).
8. **Financial cross-validation**: Cross-validate inferred relationship against A's supplier disclosures / B's customer concentration / accounts receivable. Inference without financial corroboration is capped.
9. **Alternative-hypothesis check**: Explicitly exclude alternative explanations; see `references/checklists.md`
10. **Counter-intelligence check**: Check for shell companies / dispersed patents; see `references/checklists.md`
11. **Output report**: Relationship determination + evidence chain + patent quality + evidence freshness + negative verification + triangulation + financial corroboration + confidence + follow-up

## Input/Output Contract

**Input**:
- Target company (A for forward, B for reverse) — name / ticker
- Technology T or product P of interest (optional; may be identified during analysis)
- Analysis direction: forward or reverse (default: forward if user mentions "supplier", reverse if user mentions "customer" or "downstream")
- Known background info (optional)

**Output**: Supply-chain inference report, including:
- **Direction**: forward or reverse analysis
- **Relationship determination**: whether a supply-chain relationship exists + role (direct supplier / technology licensor / customer / indirect affiliation / NPE license-only)
- **Trade secret assessment**: likelihood + indicator breakdown
- **Evidence chain**: per-lead hit status + per-lead confidence + **patent quality score** (for Lead 1) + **evidence timestamp/freshness** (all leads, v0.4.0)
- **Triangulation result**: which peers confirmed the same gap + triangulation boost applied
- **Negative verification result** (v0.4.0): negative evidence searched + found/not found + impact on confidence
- **Financial corroboration**: supplier disclosure hits, customer concentration data, AR patterns, corroboration status
- **Overall confidence**: high / medium / low + rationale (including all adjustments: trade secret, triangulation, negative verification, evidence freshness, financial cap)
- **Alternative-hypothesis list**: excluded + unexcluded
- **Counter-intelligence risk flag**: shell companies / dispersed patents
- **Follow-up verification suggestions**: next evidence to gather

## Tool Integration

Available tools per lead (by availability priority):

| Lead | Tools | Purpose |
|------|-------|---------|
| Patent search + quality | tushare (patent API), PatSnap patsnap-search connector | Search A/B/peers patents, T's patent ownership, patent quality scoring (claims, citations, family) |
| Corporate affiliation | Tianyancha tyc-mcp, Qichacha qcc-company, Qixinbao qixinbao-mcp | A-B investment / JV / executive overlap |
| Listed-co data | tushare, westock-mcp, westock-tool | Financial report supplier disclosure, prospectus |
| Talent flow | WebSearch, job-site search | B→A technical hires |
| Procurement | WebSearch, gov-procurement portals, tender announcements | A's tender / supplier announcements |
| Product teardown | WebSearch, professional teardown reports | A's product BOM / teardown for B components |
| Trade secret assessment | WebSearch, legal databases, company reports | NDAs, non-competes, trade secret litigation, R&D disclosures |
| Competitive triangulation | tushare, WebSearch, industry reports | A's peer patent portfolios, cross-company gap confirmation |
| Negative verification (v0.4.0) | WebSearch, tushare, annual reports, B's customer disclosures | Revenue mismatch, capacity mismatch, geography, explicit customer lists |
| Financial cross-validation | westock-mcp, tushare, annual report filings | Supplier concentration, customer concentration, AR aging, related-party transactions |
| Evidence freshness (v0.4.0) | All sources | Timestamp every evidence item; flag >18 months old |
| Industry guidance | `references/industry-guide.md` | Vertical-specific patent/trade-secret dynamics and verification strategies |

When a tool is unavailable, fall back to WebSearch for public info and reduce that lead's confidence accordingly.

## Key Principles

- **Patents are an entry lead, not final evidence**: A patent gap triggers verification but does not directly conclude
- **Trade secrets must be ruled out before concluding dependency**: A patent gap may reflect deliberate trade secret / know-how protection
- **Procurement/teardown leads override trade secret hypothesis**: Physical evidence trumps trade secret likelihood
- **Patent quality matters more than patent count** (v0.4.0): A core patent family with broad claims outweighs dozens of peripheral patents. Score quality, not just presence.
- **Negative verification is mandatory** (v0.4.0): You must actively attempt to disprove the inference. An inference that survives active disproof attempts is far more credible than one that was never tested.
- **Evidence freshness is tracked** (v0.4.0): Every lead carries an evidence timestamp. Stale evidence (>18 months) cannot support "high" confidence alone.
- **Competitive triangulation strengthens inference**: Cross-company corroboration is one of the strongest signals
- **Financial cross-validation is required for high-confidence conclusions**: No inference reaches "high" without financial corroboration
- **Multi-lead corroboration**: ≥2 high-confidence leads corroborating required to conclude
- **Explicit confidence scoring**: Every lead and inference gets a confidence score (high / medium / low)
- **Alternative hypotheses are mandatory**: Every inference must explicitly exclude alternative explanations
- **Counter-intelligence check is mandatory**: Watch for shell companies / dispersed patents hiding the real supply chain

## Resources

### references/
- `references/workflow.md`: Detailed 11-step operations + reverse workflow section
- `references/checklists.md`: All checklists — alternative hypotheses, trade secret indicators, patent quality scoring, negative verification, evidence freshness, triangulation, financial cross-validation, counter-intelligence, confidence scoring rules
- `references/industry-guide.md`: Vertical-specific guidance for semiconductor, pharma, new energy, consumer electronics, and materials

### examples/
- `examples/sample-output.md`: Fictional case showing the full 11-step report format
- `examples/real-case.md`: A real Chinese A-share case study with actual company names and data
