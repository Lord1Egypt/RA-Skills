# ROI & Business Case Development

## Objectives

Build a complete return-on-investment analysis, create a persuasive business case, and ensure IT investment decisions have a solid financial foundation.

---

## Prerequisites
- Technical solution is defined, TCO has been estimated
- Business benefits are quantifiable (at least estimable within a range)
- Understand the client's financial criteria (e.g. minimum IRR requirement / maximum payback period)

## Inputs
- TCO analysis (from workflow 05-01)
- Business benefit estimates (from business units / industry benchmarks)
- Client financial policies (discount rate / evaluation criteria)
- Risk assessment (from relevant workflows)

---

## Operation Steps

### Step 1: Benefit Identification and Quantification

#### 1.1 Benefit Classification Framework

IT investment benefits fall into four categories, ordered by quantifiability from high to low:

```
A. Cost Savings (Hard Savings) — Directly reflected on the P&L
├── Headcount reduction/transfer: Automation replaces manual work, 10 people → 4 people
├── Infrastructure reduction: Shut down data center after cloud migration
├── Software license reduction: Retire old systems, stop renewals
├── Vendor contract optimization: Renegotiate to lower rates
└── Operational efficiency: Process time reduction = staff time freed up

B. Revenue Growth — Quantifiable but with assumptions
├── New digital revenue: New channels / new products
├── Conversion rate improvement: AI recommendations → purchase conversion +15%
├── Customer retention improvement: Better CX → renewal rate +5%
├── Pricing optimization: Dynamic pricing → average order value +3%
└── Speed to market: New product go-live from 6 months → 2 months

C. Risk Avoidance — "How much we lose if we don't do this"
├── Compliance penalty avoidance: e.g. GDPR/data protection law fines (up to 4% of annual revenue)
├── Security incident avoidance: Average data breach cost $4.88M
├── Business continuity: Cost per minute of system downtime
├── Technical debt accumulation: 5-year remediation cost vs. cost to fix now
└── Talent attrition: Difficulty recruiting/retaining staff due to legacy technology

D. Intangible Benefits — Cannot be quantified but influence decisions
├── Brand / Reputation
├── Employee satisfaction / Retention
├── Customer experience / NPS
├── Industry competitiveness / Market position
├── Agility / Responsiveness to market changes
└── Data asset accumulation (AI fuel)
```

#### 1.2 Benefit Quantification Method

Four steps to quantify each benefit:

| Step | Action | Example |
|------|--------|---------|
| **Step 1: Define** | What exactly is the benefit? | "Customer service automation reduces manual agent headcount" |
| **Step 2: Baseline** | What is the current number? | Current: 100 agents, avg annual cost $50K/person = $5M/year |
| **Step 3: Estimate** | What is the number after the change? | AI handles 70% of standard queries; need 30 people for complex issues + 10 for AI training/optimization = 40 people |
| **Step 4: Verify** | Is this number credible? | Industry case: A bank's customer service automation went from 100→35 people; our estimate is within a reasonable range |

**Benefit Quantification Template:**
| Benefit Item | Type | Baseline | Target | Annual Benefit | Year-by-Year Realization Path | Confidence (H/M/L) |
|-------------|------|----------|--------|---------------|------------------------------|---------------------|
| Manual CS reduction | Cost | $5M/yr | $2M/yr | $3M/yr | Y1:20%, Y2:70%, Y3:100% | M |
| Cross-sell uplift | Revenue | $10M/yr | $12M/yr | $2M/yr | Y1:10%, Y2:60%, Y3:100% | L |
| Penalty risk avoidance | Risk | $10M (prob. 20%) | $2M (prob. 5%) | $1.6M/yr (expected value) | Y1:100% | M |

---

### Step 2: Cash Flow Model

#### 2.1 5-Year Incremental Cash Flow

```
(Unit: $M)

                         Year0    Year1    Year2    Year3    Year4    Year5
────────────────────────────────────────────────────────────────────────────
Cash Outflows:
  Initial investment (one-time) [  ]     [  ]     [  ]     [  ]     [  ]     [  ]
  Annual operating costs       [  ]     [  ]     [  ]     [  ]     [  ]     [  ]
  Total Outflows               [  ]     [  ]     [  ]     [  ]     [  ]     [  ]

Cash Inflows (Benefits):
  Cost savings                 [  ]     [  ]     [  ]     [  ]     [  ]     [  ]
  Revenue growth               [  ]     [  ]     [  ]     [  ]     [  ]     [  ]
  Risk avoidance               [  ]     [  ]     [  ]     [  ]     [  ]     [  ]
  Total Inflows                [  ]     [  ]     [  ]     [  ]     [  ]     [  ]

Net Cash Flow                  [  ]     [  ]     [  ]     [  ]     [  ]     [  ]
Cumulative Cash Flow           [  ]     [  ]     [  ]     [  ]     [  ]     [  ]
```

#### 2.2 "Do Nothing" Comparison

```
                         Year0    Year1    Year2    Year3    Year4    Year5
────────────────────────────────────────────────────────────────────────────
Option A: Invest (Net CF)   [  ]     [  ]     [  ]     [  ]     [  ]     [  ]
Option B: Do Nothing        [  ]     [  ]     [  ]     [  ]     [  ]     [  ]

Incremental (A - B)         [  ]     [  ]     [  ]     [  ]     [  ]     [  ]
```

---

### Step 3: Financial Metric Calculation

#### 3.1 Core Metrics

| Metric | Formula | Meaning | Typical Threshold |
|--------|---------|---------|-------------------|
| **NPV** (Net Present Value) | Σ(Net CF_t / (1+r)^t) | Value of the project today | >0 (the larger the better) |
| **IRR** (Internal Rate of Return) | Discount rate where NPV=0 | Annualized return of the project | >WACC, typically >15-20% |
| **Payback** (Payback Period) | Point when cumulative CF turns positive | How long to recoup investment | <3 years (<5 years for large projects) |
| **ROI** (Return on Investment) | (Total Benefit - Total Cost) / Total Cost | Total return multiple on investment | >100% (3yr), >200% (5yr) |
| **BCR** (Benefit-Cost Ratio) | Total Benefit / Total Cost | How much benefit per dollar invested | >1.5 |

#### 3.2 Calculation Example

```
Assumptions: discount rate r=8%, initial investment $5M (Year0)

Year0: -5.00
Year1: -2.00 (investment > benefit)
Year2: +1.00 (benefits start to materialize)
Year3: +3.00
Year4: +4.00
Year5: +5.00

NPV = -5 + (-2)/(1.08) + 1/(1.08)² + 3/(1.08)³ + 4/(1.08)⁴ + 5/(1.08)⁵
    = -5 + (-1.85) + 0.86 + 2.38 + 2.94 + 3.40
    = $2.73M  ✅ (NPV>0, project creates value)

IRR ≈ 22% (calculate using Excel IRR function)
Payback ≈ 3.5 years (cumulative CF approaches positive near end of Year3)

ROI = (Total Benefit - Total Cost) / Total Cost = (15-7)/7 ≈ 114%
BCR = 15/7 ≈ 2.14

Conclusion: Project meets investment criteria (NPV>0, IRR>15%, Payback<5 years)
```

---

### Step 4: Business Case Document

#### 4.1 Five Case Model

Originating from UK government best practice, applicable to large IT investments:

**Case 1: Strategic Case** — "Why do it?"
- Alignment with business strategy
- The cost of doing nothing over 5 years
- External trends / competitive pressures

**Case 2: Economic Case** — "Is it worth doing?"
- Scenario comparison (Do Nothing vs Option A vs Option B)
- NPV / IRR / Payback
- Sensitivity analysis

**Case 3: Commercial Case** — "Can it be done?"
- Vendor market analysis
- Procurement strategy
- Key contract terms

**Case 4: Financial Case** — "Can we afford it?"
- Funding source
- Impact on budget / cash flow
- 5-year total cost as a percentage of IT budget

**Case 5: Management Case** — "Do we have the capability to do it?"
- Project management capability
- Change management plan
- Key risks and mitigations
- Governance and decision-making structure

#### 4.2 One-Page Business Case (for rapid decision-making)

```
Business Case: [Project Name]

Investment Request:
┌─────────────────────────────────────────────────┐
│ Total Investment: $[X]M (one-time $[A]M + 5yr ops $[B]M) │
│ 5-Year Net Benefit: $[Y]M                        │
│ NPV: $[Z]M | IRR: [X]% | Payback: [X] years     │
└─────────────────────────────────────────────────┘

Why It Must Be Done Now (Top 3):
1. [Most urgent reason, quantified]
2. [Second most urgent reason]
3. [Strategic alignment]

Cost of Doing Nothing:
[Quantified 5-year cumulative loss of "doing nothing"]

Key Benefits (Top 5):
1. [Benefit] — $[X]M/year — [Confidence: H/M/L]
2. ...

Key Risks (Top 3 + Mitigations):
1. [Risk] → [Mitigation measure]
2. ...

Decision Request:
Approve $[X]M investment + authorize Phase 1 launch

Alternatives:
A. [Recommended]: Invest $[X]M, 5-year net benefit $[Y]M ✅
B. [Minimal]: Invest $[X/2]M, 5-year net benefit $[Y/3]M
C. Do Nothing: Invest $0, 5-year cumulative loss $[LOSS]M
```

---

### Step 5: Stakeholder Alignment

#### 5.1 Top 10 Questions CFOs Ask

Prepare answers to these:

1. "Why $X? Can't it be less?" → Prepare the scope-vs-cost relationship
2. "Where did your assumed benefit growth rate (X%) come from? Isn't that too optimistic?" → Have industry benchmarks / internal pilot data
3. "In the cash flow forecast, why do costs increase year over year?" → User growth / inflation / vendor price increases
4. "What about a cheaper alternative?" → Already evaluated; the gap lies in...
5. "When will we see the first dollar of return?" → Year X, specific benefit item is...
6. "What if the exchange rate changes?" → Sensitivity analysis shows...
7. "What if benefits only reach 50% of estimates?" → NPV still >0 / NPV would turn negative, but we can...
8. "Capitalize or expense?" → Confirmed with finance team; the treatment is...
9. "What is the exit cost of this project?" → If stopped in Year1, loss $X; Year2, loss $Y
10. "How do I know the money is being well spent?" → We have set up XXX KPIs and monthly reporting

---

## Outputs
1. **Benefit Quantification Model** (source + assumptions + calculation for each benefit)
2. **5-Year Cash Flow Model** (including Do Nothing comparison)
3. **Financial Metric Calculations** (NPV + IRR + Payback + ROI + BCR)
4. **Sensitivity Analysis** (key variables: benefit / cost / time / discount rate)
5. **Business Case Document** (use templates/Business Case Template.md)

---

## Quality Checklist
- [ ] Every benefit has a clear calculation logic, not just "should be able to save X%"
- [ ] Benefits are categorized into Hard Savings / Revenue / Risk Avoidance / Intangible
- [ ] NPV uses a reasonable discount rate (8-12%) with justification
- [ ] "Do Nothing" comparison is included
- [ ] Sensitivity analysis covers at least 3 key variables
- [ ] All 10 CFO questions can be answered
- [ ] Independently reviewed by finance personnel (not IT calculating and believing its own numbers)

---

## Common Pitfalls

| Pitfall | Why It's Wrong | Correct Approach |
|---------|---------------|------------------|
| Beautiful ROI calculation but assumptions don't hold up | "Customer conversion rate improves 30%" — where did that come from? | Every benefit assumption has 3 anchors: pilot data / industry case study / conservative floor |
| Optimism Bias | Humans naturally overestimate benefits and underestimate costs; UK government research found average 50% overrun | Apply an "optimism correction factor" to all forecasts (cost ×1.2, benefit ×0.8) |
| Only looking at financial returns | Some IT investments (security/compliance/infrastructure) may have negative financial returns but are mandatory | For "must-do" projects, the business case focuses on "the cost of not doing it" |
| Quantifying intangible benefits too precisely | "Customer experience improvement = $3.7M" ← this number is meaningless | Honestly label confidence levels: hard-to-quantify benefits go in "Intangible" — don't force a number |
| Comparing with "Do Nothing" but secretly changing the baseline | To make the numbers look good, inflating the Do Nothing cost | Do Nothing baseline must be based on current actual operational costs, unembellished |