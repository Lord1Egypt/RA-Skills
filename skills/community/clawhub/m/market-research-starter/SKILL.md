---
name: Market Research Starter
description: "Free market research toolkit — competitor audit, positioning matrix, evidence grading, and customer interview scripts. Upgrade to Pro for automated scraping + summaries."
author: CertainLogic
license: MIT
homepage: https://certainlogic.ai/brain
version: 1.0.0
---

# Market Research — Starter Kit

> **Validate your market position with 4 proven frameworks. No tools required — just honest analysis.**

---

## Quick Start

1. **Pick a framework** below (Competitor Audit, Evidence Grading, Interviews, or Positioning)
2. **Follow the steps** — fill in the blanks for your product
3. **Optional:** Store findings in Company Brain (`clawhub install company-brain-os`)

**Time to first insight:** ~20 minutes

---

---

## 1. Competitor Audit Framework

**Best for:** Understanding where you stand before building anything

### Step 1: List 5 competitors
- Direct (same product, same market)
- Indirect (solves same problem differently)
- Aspirational (where you want to be in 2 years)

### Step 2: Rate each on 4 axes

| Axis | Score 1-5 | Evidence Required |
|------|-----------|-------------------|
| **Price** | Lower = 1, Higher = 5 | Screenshot of pricing page |
| **Features** | Fewer = 1, More = 5 | Feature comparison list |
| **Speed** | Slower = 1, Faster = 5 | Measured or estimated |
| **Trust** | Unknown = 1, Proven = 5 | Reviews, case studies, age |

### Step 3: Plot your position
Draw a 2×2 matrix:
- X-axis: Price (low → high)
- Y-axis: Speed/feature density (low → high)
- Mark where you are today
- Mark where competitors are
- Mark where you want to be in 6 months

**Rule:** If you can't provide evidence for a score, it doesn't count.

---

## 2. Evidence Grading System

**Best for:** Separating opinions from facts in research

### Grades

| Grade | Description | Example |
|-------|-------------|---------|
| **A** | Primary data you collected | Customer interview recording |
| **B** | Secondary data with source | Industry report with link |
| **C** | Anecdotal but specific | "3 customers said..." |
| **D** | Generic hearsay | "Everyone knows..." |
| **F** | Unverifiable | "I heard that..." |

### Usage
- Every claim in your strategy doc gets a grade
- No D or F evidence in investor/lender materials
- C evidence gets upgraded to B before external use

---

## 3. Customer Interview Script

**Best for:** Finding real pain points (not what you assume)

### Opener
```
Hi [NAME], thanks for taking 15 minutes.
We're researching [TOPIC] — not selling anything.
I'd love to understand your current process.
```

### Core Questions
1. **"Walk me through how you currently handle [PROBLEM]"**
   - Listen for friction, workarounds, manual steps
2. **"What happens if you don't solve this?"**
   - Listen for cost of inaction (better than asking about value)
3. **"Have you tried anything else?"**
   - Listen for churn reasons from competitors
4. **"If you had a magic wand..."**
   - Listen for dream state (not constrained by reality)
5. **"Who else should I talk to?"**
   - Source next interviews

### Rules
- Never pitch during interviews
- Never lead the witness ("Don't you think...")
- Record with permission, grade evidence later

---

## 4. Positioning Matrix Template

**Best for:** Finding the gap nobody owns

### Template

```
For [TARGET AUDIENCE]
who [PAIN POINT]
our product is a [CATEGORY]
that [KEY BENEFIT]
unlike [COMPETITOR]
we [DIFFERENTIATOR]
```

### Example (CertainLogic)
```
For technical founders
who need to prevent AI hallucinations in production
our product is a deterministic knowledge engine
that answers questions with verified facts, not guesses
unlike general LLM wrappers
we prove every answer with traceable sources
```

### Gap Analysis
After filling in competitors' positioning:
- Is there a quadrant nobody owns?
- Is "faster" already claimed? Claim "more certain"
- Is "cheaper" already claimed? Claim "zero waste"

---

## Integration with Company Brain

This starter kit works better with a brain:

```bash
clawhub install certainlogicai/company-brain-os
```

Brain-enhanced market research:
- **Faster audits:** Brain stores competitor data you collect
- **Evidence library:** Interview notes get graded and stored
- **Positioning validation:** Brain cross-checks claims against stored facts

---

## Upgrade Path

| Feature | Starter (Free) | Pro (Coming Soon) |
|---------|----------------|---------------|
| Templates | 4 frameworks | 12+ frameworks |
| Analysis | Manual grading | Auto-grading via brain |
| Data | Your own research | Web scraping + summarization |
| Reports | Markdown export | PDF + presentation export |
| Collaboration | Solo | Team shared brain |

**Pro version:** Not yet available. Get notified at [certainlogic.ai/brain](https://certainlogic.ai/brain)

---

*Built by CertainLogic — we dogfood this on ourselves.*
