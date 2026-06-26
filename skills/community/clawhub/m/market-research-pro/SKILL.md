---
name: market-research
description: >
  Use this skill when you need to generate structured market research reports,
  competitive landscape analysis, industry trend summaries, or TAM/SAM/SOM
  sizing for a product, business, or investment decision. Activates on requests
  like "research the X market", "give me a market overview of Y", or
  "what's the market size for Z".
---

# Market Research Report Generator

A systematic workflow for producing professional market research reports with
actionable insights, grounded in structured frameworks.

## When to Use
- Evaluating a new product/business opportunity
- Preparing investor pitch market slides
- Conducting industry landscape analysis
- Sizing addressable market for a segment
- Tracking emerging trends in a sector

## Core Workflow

### Step 1 — Define Research Scope
Clarify with the user:
- **Target market**: geography, industry vertical, customer segment
- **Report depth**: executive summary vs. full report
- **Time horizon**: current state, 3-year, 5-year outlook
- **Key questions**: market size? competitors? customer pain points? trends?

### Step 2 — Market Sizing (TAM / SAM / SOM)
Use **top-down** or **bottom-up** approach:

**Top-down**:
```
TAM = Total industry revenue (cite source + year)
SAM = TAM × addressable segment %
SOM = SAM × realistic capture % (Year 1–3)
```

**Bottom-up**:
```
SOM = Target customers × Average deal size × Conversion rate
SAM = SOM / Estimated market share
TAM = SAM / Serviceable segment ratio
```

Always cite data sources (Statista, IBISWorld, Gartner, CB Insights, etc.)

### Step 3 — Industry Structure Analysis
Apply **Porter's Five Forces**:
| Force | Level (L/M/H) | Key Factors |
|---|---|---|
| Competitive rivalry | | |
| Supplier power | | |
| Buyer power | | |
| Threat of new entrants | | |
| Threat of substitutes | | |

### Step 4 — Trend Analysis (PESTEL)
Scan macro environment:
- **P**olitical: regulations, trade policy, subsidies
- **E**conomic: GDP growth, inflation, consumer spending
- **S**ocial: demographics, behavioral shifts, cultural trends
- **T**echnological: disruptive tech, R&D investment, adoption curves
- **E**nvironmental: sustainability pressure, ESG regulations
- **L**egal: IP landscape, compliance requirements, labor laws

### Step 5 — Customer Segmentation
Identify 2–4 primary customer segments:
```
Segment A: [Name]
  - Size: ~X users / companies
  - Key pain points: ...
  - Willingness to pay: $X–$Y / month
  - Acquisition channels: ...
```

### Step 6 — Competitive Landscape
Build a comparison matrix:
```
| Player | Founded | Funding | Positioning | Strengths | Weaknesses |
|--------|---------|---------|-------------|-----------|------------|
| Co A   |         |         |             |           |            |
| Co B   |         |         |             |           |            |
```
Identify market gaps and whitespace opportunities.

### Step 7 — Synthesis & Recommendations
Conclude with:
1. **Market attractiveness score** (1–10) with rationale
2. **Top 3 opportunities** ranked by impact × feasibility
3. **Top 3 risks** with mitigation strategies
4. **Recommended next steps** (validation experiments, partnerships, etc.)

## Output Format
Default to a structured markdown report with:
- Executive Summary (≤ 200 words)
- Market Sizing section
- Industry Analysis section
- Competitive Landscape section
- Opportunities & Risks
- Appendix (data sources)

## Quality Standards
- Always cite data sources with year
- Distinguish between verified data and informed estimates
- Flag assumptions explicitly: `[ASSUMPTION: ...]`
- Use ranges rather than false precision for estimates
