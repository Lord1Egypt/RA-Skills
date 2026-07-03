# 02 — Requirements Clarification & Problem Diagnosis

## Objectives
Transform the client's vague expressions ("our IT is broken," "we want to do AI," "the system is too slow") into structured, actionable problem statements and initial hypotheses.

## Prerequisites
- Initial client communication has been completed
- Basic understanding of the client's situation and pain points has been obtained
- Background materials may have been received from the client

## Inputs
- Initial meeting minutes
- Background documents provided by the client (if any)
- Client industry research report

---

## Operation Steps

### Step 1: Problem Classification — Determine Which Bucket in 5 Seconds

Once you receive the client's requirements, use the following classification framework for the first layer of judgment:

```
Client's Description                        → Problem Category        → Core Solution Direction
──────────────────────────────────────────────────────────────────────────────────────────
"System is too slow / crashes often / unusable"  → Technology Infrastructure  → Modernization / Cloud Migration / Architecture Refactoring
"Business waits 6 months for IT to develop"      → Delivery Efficiency        → DevOps / Platform Engineering / Agile Transformation
"Can't track what IT spends money on"            → IT Financial Management    → TBM / FinOps / TCO Modeling
"Competitors are using AI, we need it too"       → AI Strategy                → Maturity Assessment / Use Case Identification / Roadmap
"Data is everywhere across departments but unusable" → Data Strategy           → Data Mesh / Governance / Platform
"Systems were acquired through M&A, total mess"  → Integration & Architecture → M&A Integration / EA / Application Rationalization
"ERP/CRM was implemented but doesn't feel adopted" → Change & Adoption        → Change Management / Training / Process Reengineering
"Don't know which direction IT should go"        → IT Strategy Planning       → Strategy Translation / Benchmarking / Roadmap
"Company was hacked / worried about incidents"   → Security & Risk            → NIST Assessment / Maturity / Compliance
"Need to select a new system, too many vendors"  → Vendor Selection           → RFP / Scoring Model / PoC
"IT costs too high, boss is watching"            → Cost Optimization          → FinOps / Outsourcing Assessment / License Optimization
"IT team capability is too weak"                 → Organization & Talent      → Org Design / Capability Model / Recruitment
```

### Step 2: Problem Structuring — Five-Dimensional MECE Decomposition

Any IT problem can be decomposed using MECE across the following 5 dimensions:

```
Problem: [Client's original description]

Dimension 1 — Technology:
  ├── Infrastructure (servers / network / cloud / storage)
  ├── Application Systems (SoR / SoD / SoI health)
  ├── Data (quality / accessibility / governance)
  ├── Integration (interfaces / middleware / API)
  └── Security (protection / detection / response / compliance)

Dimension 2 — Process:
  ├── Requirements Management (how decisions are made on what to build)
  ├── Development & Delivery (process from requirement to go-live)
  ├── Operations Management (change / incident / problem / configuration)
  ├── Procurement & Vendor Management
  └── IT Governance & Decision-Making

Dimension 3 — Organization:
  ├── IT Team Structure (centralized / federated / product-oriented)
  ├── Personnel Capability & Talent Pipeline
  ├── Culture & Collaboration Patterns
  ├── Leadership & Decision-Making Efficiency
  └── Performance Evaluation & Incentive Mechanisms

Dimension 4 — Data:
  ├── Data Asset Inventory & Quality
  ├── Data Standardization / Master Data Management
  ├── Data Governance & Compliance
  ├── Data Analytics & AI Readiness
  └── Data Security & Privacy

Dimension 5 — Financial:
  ├── Total IT Spend as % of Revenue
  ├── Run / Grow / Transform Allocation Ratio
  ├── Per-Project / Per-Service TCO
  ├── Outsourced vs. In-House Spend
  └── IT Investment ROI Tracking
```

### Step 3: Form the Problem Statement

A good problem statement must include: **Current State + Gap + Consequence + Time Urgency**

```
Template:

"[Company Name] currently has [specific problem] in the area of [domain],
with a gap of [quantified gap] compared to [industry benchmark / business requirement].
If not resolved, this will cause [business consequence] within [timeframe],
requiring us to resolve it through [general direction] within [timeframe]."

Example:

"XX Insurance Company currently has severe technical debt in its core underwriting system —
the system is based on a 15-year-old architecture, with a single change cycle taking up to 3 months,
while leading competitors (Ping An / ZhongAn) have already achieved weekly iteration.
If modernization is not initiated, it is expected that within the next 18-24 months,
the lag in new product launch speed will result in a 5-8% loss of premium market share.
We need to complete the re-platforming and microservice-based transformation of the core system within 12 months."
```

### Step 4: Generate Initial Hypotheses

Based on the problem statement, use a hypothesis-driven approach to generate 3-5 verifiable hypotheses:

```
Hypothesis Template:
"If [hypothesis is true], we should observe [observable phenomenon]"

Example:
Problem: A retail company's online conversion rate is 30% below industry average

Hypothesis 1: Recommendation algorithm data quality is insufficient
  → Should observe product tag coverage <60%, user profile dimensions <20
Hypothesis 2: Technical architecture performance bottleneck
  → Should observe homepage load time >3s (P95), API response >500ms
Hypothesis 3: Organizational collaboration issues
  → Should observe marketing requirement to go-live averaging >4 weeks, involving 5+ department approvals
Hypothesis 4: Missing data strategy
  → Should observe CDP not built, user behavior data collection rate <50%

Next step: Prioritize verifying Hypotheses 1 and 3 (quick to verify + high impact)
```

### Step 5: Output — Problem Diagnosis Summary

Synthesize the above steps into a 1-page diagnostic summary to send to the client:

```markdown
# [Client Company] IT Problem Preliminary Diagnosis Summary

## Problem Statement
[1-2 paragraph Problem Statement]

## Five-Dimensional Problem Analysis
| Dimension | Current Score (1-5) | Key Findings | Impact Level |
|------|-------------|---------|---------|
| Technology | [Score] | [Finding] | 🔴/🟡/🟢 |
| Process | [Score] | [Finding] | 🔴/🟡/🟢 |
| Organization | [Score] | [Finding] | 🔴/🟡/🟢 |
| Data | [Score] | [Finding] | 🔴/🟡/🟢 |
| Financial | [Score] | [Finding] | 🔴/🟡/🟢 |

## Initial Hypotheses (To Be Verified)
1. [Hypothesis 1] — Estimated impact: [quantified]
2. [Hypothesis 2]
3. [Hypothesis 3]

## Recommended Next Steps
- Short-term (within 2 weeks): [Quick-win diagnostic actions]
- Medium-term (1-2 months): [Deep-dive analysis directions]
- Suggested consulting project scope: [Preliminary scope description]

## Why Us
[2-3 sentences explaining your unique advantage for this project — not showing off, but demonstrating fit]
```

---

## Outputs
1. **Problem Classification Judgment**: Which of the 12 problem categories
2. **Five-Dimensional Decomposition Analysis**: Technology / Process / Organization / Data / Financial
3. **Problem Statement Document**: Problem statement template (direction / gap / consequence / urgency) + initial hypotheses
4. **Client Communication Minutes**: Including instant insights and recommended next steps

## Quality Checklist

- [ ] Problem category correctly identified (matches one of the 12 categories above)
- [ ] Five-dimensional decomposition has no obvious omissions
- [ ] Problem statement includes: current state + gap + consequence + urgency
- [ ] Hypotheses are verifiable (not unfalsifiable assertions)
- [ ] Diagnostic summary does not exceed 2 pages
- [ ] Next-step recommendations are specific and actionable

## Common Pitfalls

| Pitfall | Correct Approach |
|------|---------|
| Taking the client at face value ("We need AI") | Follow up: "What business problem does AI need to solve?" — it may be a data / process / people problem, not necessarily AI |
| Diagnosis focuses only on technology | Always use five-dimensional analysis — 6 out of 10 IT problems have root causes in process / organization / people |
| Jumping to solutions too quickly | Hypothesis phase only proposes directional hypotheses, no commitment to specific solutions |
| Hypotheses that are unverifiable (e.g., "management doesn't value IT") | Transform into observable: e.g., "IT budget <50% of industry average AND no CIO reporting to CEO" |