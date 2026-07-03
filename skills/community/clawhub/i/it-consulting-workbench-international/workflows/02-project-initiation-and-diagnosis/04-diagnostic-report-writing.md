# 04 — Diagnostic Report Writing

## Objectives
Synthesize the five-dimension diagnostic results and stakeholder interview findings into a logically rigorous, insightful, action-driving diagnostic report. The diagnostic report is the foundation for subsequent strategy design and the first "real deliverable" by which the client judges your professional caliber.

## Prerequisites
- Five-dimension diagnosis completed (Technology / Process / Organization / Data / Finance)
- Stakeholder interviews completed
- Core findings internally discussed and consensus reached
- Industry benchmark data prepared

## Inputs
- IT current-state diagnostic records (output of 03-IT-Current-State-Diagnosis.md)
- Stakeholder interview synthesis cards
- Industry benchmark data

---

## Operation Steps

### Step 1: Finding → Insight → Recommendation — Three-level distillation

Before you start writing, first distill raw findings into insights:

```
Raw Finding (What): The core ERP system is based on a 15-year-old technology architecture;
                    a single change cycle exceeds 3 months
      ↓  So What?
Insight (Why it matters): This means business units' new product requirements cannot be
                          responded to in a timely manner; they have already begun
                          bypassing IT to procure SaaS solutions on their own
      ↓  Now What?
Recommendation (What to do): Launch an ERP modernization initiative, prioritizing the
                            integration layer and API-enablement so that business units
                            can at least self-serve data access

Every finding must pass the "So What?" test. If you write a sentence and the reader asks
"So what?" and you don't have a ready answer — delete it or rewrite it.
```

### Step 2: Standard report structure

```
Cover Page
  ├── Project Name / Client Company / Date / Classification Level

Chapter 1: Executive Summary — ≤2 pages
Chapter 2: Diagnostic Methodology Overview (1 page)
Chapter 3: Overall Findings (1–2 pages)
Chapter 4: Detailed Findings by Dimension (main section, 8–12 pages)
  ├── Technology Dimension
  ├── Process Dimension
  ├── Organization Dimension
  ├── Data Dimension
  └── Finance Dimension
Chapter 5: IT Maturity Composite Score (1–2 pages)
Chapter 6: Root Cause Analysis (1–2 pages)
Chapter 7: Quick Win Identification (1–2 pages)
Chapter 8: Recommendations & Next Steps (1–2 pages)
Appendix: Detailed Data / Interview List / Scoring Methodology
```

### Step 3: Chapter-by-chapter writing guide

**Chapter 1: Executive Summary — The soul of the diagnostic report**

Standard structure:
```
Paragraph 1: Diagnostic scope and methodology (1–2 sentences)
  "This diagnostic covered [Company]'s IT across five core dimensions — Technology
   Architecture, Process Efficiency, Organizational Capability, Data Readiness, and
   Financial Management — conducted through [methods: X interviews / Y systems reviewed /
   Z data analyzed / W standards benchmarked]."

Paragraph 2: Core findings (3–5 items, ordered by importance)
  "Core Findings:
   1. [Most important finding, e.g.: IT technical debt has reached a tipping point —
      8 of 15 core systems are running on EOL versions]
   2. [...]
   3. [...]"

Paragraph 3: Overall maturity score
  "IT Composite Maturity Score: 2.4/5 (Industry Average 3.1, Industry Leader 4.2)
   By Dimension: Technology 2.0 / Process 2.5 / Organization 2.8 / Data 2.0 / Finance 3.0"

Paragraph 4: Summary of key recommendations
  "We recommend prioritizing three actions:
   1. [Quick Win 1] — Estimated [time], Investment [magnitude], Benefit [magnitude]
   2. [Quick Win 2]
   3. [Strategic recommendation]"

Paragraph 5: Urgency statement
  "Without action, within [timeframe] the most severe consequence is [X]. The good news
   is that [core strength/opportunity] provides a solid starting point for transformation."
```

**Chapter 4: Findings by dimension (standard template for each dimension)**

```
4.X [Dimension Name] Dimension

4.X.1 Current State Overview
  [2–3 sentences describing the overall situation of this dimension]

4.X.2 Core Findings
  Finding X.1: [Title: Finding + Impact]
    ├── Current State: [Specific description, with data]
    ├── Impact: [Specific business impact, quantified]
    ├── Root Cause: [Preliminary judgment of cause]
    ├── Evidence: [Evidence sources supporting this finding: interview quotes / data analysis / observation]
    └── Benchmark: [Gap vs. industry average / industry leader]

  Finding X.2: [Same structure as above]
  ...

4.X.3 Strengths in This Dimension
  [Don't only list problems! At least 1 thing done well per dimension]
  "Although the overall score is low, [specific area done well] deserves recognition and retention."

4.X.4 Key Risks in This Dimension
  [If not improved, what is the biggest risk within 1–2 years]
```

**Handling difficult wording in the report:**

```
Don't write...                            Rewrite as...
────────────────────────────────────────────────────────────────────────
"The IT team's capability is clearly      "The IT team has a capability gap in
insufficient"                             [specific skill area], primarily manifested
                                          in [specific symptoms]. The team has
                                          [specific strengths], and with targeted
                                          upskilling can achieve [expected outcome]."

"Management doesn't value IT"             "IT's strategic positioning within the
                                          organization needs elevation — the CIO
                                          reports to the CFO (not the CEO), and
                                          IT budget as a percentage of revenue is
                                          40% below industry average. This leads to
                                          [specific consequences]."

"The system architecture is a mess"       "The technology architecture has undergone
                                          [X] years of organic growth and [M] M&A
                                          events, currently featuring [N] parallel
                                          tech stacks and [Y]% point-to-point
                                          integration. This is a normal outcome of
                                          rapid growth, but has now reached an
                                          inflection point requiring systematic
                                          optimization."

"Outsourcing management is completely     "There are currently [X] IT vendors with
out of control"                           inconsistent contract management approaches;
                                          [Y]% of contracts lack SLAs and exit clauses.
                                          We recommend prioritizing the top [Z] vendors
                                          for establishing standard governance mechanisms."
```

### Step 4: Root cause analysis — Use 5-Whys to find the real cause

Do a 5-Why analysis for each core problem:

```
Example:

Problem: New features take an average of 4 months from requirement to go-live

Why 1: Why?
→ Because development resources are insufficient, constantly switching between projects

Why 2: Why are resources insufficient?
→ Because the IT team spends 60% of its time maintaining legacy systems

Why 3: Why is maintenance time so high?
→ Because the 15-year-old ERP system has no documentation; any change requires
  reverse engineering + extensive regression testing

Why 4: Why is there no documentation?
→ Because for the past 10 years no one was required to write documentation;
  "delivery speed" was always prioritized over "maintainability"

Why 5: Why was speed prioritized over maintainability?
→ Because IT's performance metrics only measure "on-time project go-live rate,"
  not "long-term system health"

Root Cause: The IT performance system incentivizes short-term delivery behavior,
leading to systematic accumulation of long-term technical debt.
(If you stop at Why 2 — "insufficient resources" — the solution would be "hire more
people" — which treats the symptom, not the cause.)
```

### Step 5: Quick win identification

**Quick Win Three Elements: High Impact + Low Effort + High Visibility**

```
Quick Win Scoring Matrix:

Opportunity              Business Impact   Implementation   Time    Visibility  Priority
                         (1–5)             Difficulty (1–5↓) (weeks) (H/M/L)
──────────────────────────────────────────────────────────────────────────────────
Clean up zombie cloud    4                 1                 2       M           ★★★ #1
resources
Establish IT service     3                 2                 4       H           ★★★ #2
catalog
Automate 3 high-frequency 4                2                 3       H           ★★★ #3
reports
ERP core upgrade         5                 5                 52      M           ★ (Strategic, not quick win)
Org structure redesign   4                 5                 26      H           ★ (Strategic, not quick win)
```

### Step 6: Presenting maturity scores

```
IT Maturity Radar Chart (text description):

              Technology
              /\
             /  \
            /    \
           /  2.0 \
          /        \
   Finance / 3.0    2.5 \ Process
          │            │
          │   2.4      │
          │  (Overall) │
          │            │
    Data  \ 2.0    2.8 /  Organization
          \        /
           \      /
            \    /
             \  /
              \/

Industry Comparison:
  Client Score:   2.0  2.5  2.8  2.0  3.0 = 2.4/5.0
  Industry Avg:   3.2  3.0  3.5  2.8  3.5 = 3.2/5.0
  Industry Leader: 4.5  4.2  4.5  4.0  4.5 = 4.3/5.0

Largest Gaps: Technology (2.0 vs 4.5) and Data (2.0 vs 4.0) — these two dimensions
should be prioritized for investment.
```

---

## Outputs
1. **Diagnostic Report**: Complete 8-chapter diagnostic report + appendix
2. **Maturity Assessment**: Five-dimension radar chart + industry benchmarking
3. **Root Cause Analysis**: 5-Why drilled down to systemic root causes
4. **Quick Win List**: Impact/Effort matrix ranked
5. **Core Recommendations**: "If you can only do three things" prioritization

## Quality Check

- [ ] Executive summary can be read standalone; all key information fits within 2 pages
- [ ] Every finding passes the "So What?" test
- [ ] Each dimension has at least 1–2 data-supported findings
- [ ] Root cause analysis drilled down to at least Why 3+
- [ ] No hollow judgments like "insufficient capability" or "management doesn't value IT" — all transformed into specific, observable phenomena
- [ ] Report identifies both problems and strengths
- [ ] Quick wins have clear Impact/Effort assessments
- [ ] Maturity scores have benchmark data, not "gut-feel scores"
- [ ] After reading the full report, the reader knows "what are the three most urgent things"

## Common Pitfalls

| Pitfall | Correct Approach |
|------|---------|
| Report = a list of problems, no prioritization | Must have a "if you can only do three things" ranking. The client wants direction, not an encyclopedia |
| Using "industry best practice" to pressure the client | "Company X did Y" — this is not a good argument. Point out "your situation suits model Z, because..." — that is |
| Every finding points to the same set of root causes | If every problem's root cause is "management doesn't value IT," you haven't dug deep enough |
| Over-diagnosis (analysis paralysis) | Diagnosis is for action. One directionally correct recommendation you can act on immediately > 10 perfect analyses still being verified |
| Afraid to write the real difficulties | Honesty > flattery. If the problem is serious, using constructive language to tell the truth earns more respect than whitewashing |