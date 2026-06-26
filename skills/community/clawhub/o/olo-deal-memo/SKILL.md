---
name: olo-deal-memo
version: 1.0.0
description: Investment memorandum generation for M&A — structured deal write-ups from the acquirer's perspective with data-backed analysis
author: ololand.ai
author_url: https://ololand.ai
license: MIT
triggers:
  - investment memo
  - deal memo
  - investment memorandum
  - deal write-up
  - ic memo
  - investment committee
  - deal recommendation
tags:
  - finance
  - documents
  - m-and-a
  - due-diligence
  - investment-banking
---

# Investment Memorandum Generation

Generate structured investment memos from the acquiring company's perspective.

## Perspective

- Written **for** the acquiring company (use "we" for acquirer)
- Written **about** the target company (use company name or "the target")
- Align with acquirer's investment thesis and acquisition strategy
- Present balanced view: opportunity AND risk

## Memo Structure

### 1. Executive Summary (1 page)
- Transaction overview: target name, sector, deal size, structure
- Strategic rationale in 3-4 bullet points
- Key financial metrics (revenue, EBITDA, growth, valuation)
- Recommendation: Proceed / Proceed with Conditions / Pass

### 2. Company Overview
- Business description and history
- Products/services and revenue mix
- Customer base (count, concentration, retention)
- Management team assessment
- Organizational structure and headcount

### 3. Market & Competitive Position
- Industry overview and growth outlook (reference market intelligence)
- Competitive landscape and target's positioning
- Sustainable competitive advantages (moats)
- Key risks to market position

### 4. Financial Analysis
- Historical financials (3-5 years): revenue, EBITDA, margins, FCF
- Revenue quality: recurring %, customer concentration, cohort analysis
- Working capital dynamics and cash conversion
- CapEx requirements and capital intensity
- Key financial trends and inflection points

### 5. Valuation
- DCF analysis (base/bull/bear cases)
- Comparable company analysis (public comps)
- Precedent transaction analysis
- Implied valuation range and recommended offer price
- Sensitivity analysis on key assumptions

### 6. Strategic Rationale & Synergies
- Revenue synergies (cross-sell, market expansion, pricing)
- Cost synergies (overlap elimination, procurement, shared services)
- Timeline to achieve synergies (Year 1 / Year 2 / Year 3)
- Integration complexity and risk assessment
- Synergy value vs. premium paid analysis

### 7. Risk Assessment
- Deal-specific risks (top 5, ranked by impact × likelihood)
- Mitigation strategies for each risk
- Deal-breaker thresholds
- Sensitivity of returns to key risk scenarios

### 8. Transaction Structure & Returns
- Proposed structure (asset vs. stock, cash vs. equity mix)
- Sources and uses of funds
- Pro forma leverage and coverage ratios
- Expected returns: IRR, MOIC, payback period
- Key assumptions driving returns

### 9. Recommendation & Next Steps
- Clear recommendation with confidence level
- Conditions or diligence items to resolve
- Proposed timeline for next phase
- Required approvals and process steps

## Data Aggregation Strategy

1. Pull existing DD data from platform (fast, <1s)
2. Fill gaps with RAG queries over uploaded documents (medium, ~3s)
3. Augment with market context via web research (slower, ~5s)
4. Synthesize into narrative sections with AI (~5-10s)

## Quality Standards

- Every claim backed by data point with source
- Financial figures must reconcile across sections
- Clearly separate facts from assumptions from opinions
- Use conditional language for projections ("we estimate", "management projects")
- Flag data gaps explicitly rather than filling with generic text
- Total generation target: 15-20 seconds

## Output Formats

- **Markdown**: Primary format for platform display and editing
- **PDF**: Professional layout for IC distribution
- **PPTX**: Presentation format for deal committee meetings
- **Excel**: Supporting financial model and sensitivity tables
