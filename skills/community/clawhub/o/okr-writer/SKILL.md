---
name: okr-writer
description: A professional OKR writing assistant. Generates clear and concise OKRs based on work objectives, including Objectives, Key Results, action plans, and timelines, ensuring OKRs are closely aligned with goals and actionable. 
---

# OKR Writing

Write clear, concise, and actionable OKRs (Objectives and Key Results) based on work objectives.

## Use Cases

Use when the user needs "write OKR", "create OKR", "OKR planning", "objectives and key results", "quarterly goals", or "annual OKR".

## OKR Structure

### Objectives
- Qualitative description, concise and powerful, 1-2 sentences
- Indicate direction and desired outcomes
- Challenging and motivating, yet achievable

### Key Results
- Each Objective corresponds to 2-5 KRs
- Quantitative, measurable, time-bound
- Use numbers (percentages, absolute values, completion status)

### Action Plans and Timelines
- Break down each KR into specific action steps
- Mark key milestones and time nodes
- Specify responsible persons (if known)

## Writing Principles

### Core Requirements
- OKRs must be closely aligned with work objectives; each KR directly serves its corresponding Objective
- Avoid writing daily tasks as KRs — KRs should measure outcomes, not activities
- Objectives should be challenging (typically 70% completion is considered success); avoid setting 100% achievable targets
- Use clear and concise language; avoid vague expressions (e.g., use "increase to" or "increase by X%" instead of "improve")
- Horizontal alignment: multiple Objectives should not conflict; they should synergistically advance the overall goal

### Output Format

```markdown
## OKR Overview

**Period:** [Quarterly/Annual]
**Date:** YYYY-MM-DD

---

### Objective 1: [Objective Description]

**Key Results:**
- KR1: [Measurable key result]
- KR2: [Measurable key result]
- KR3: [Measurable key result]

**Action Plan:**
| Action Step | Timeline | Responsible |
|----------|----------|--------|
| [Specific action] | [Date] | [Name/Team] |

---

### Objective 2: [Objective Description]
...
```

### Output Specifications

- Output only the OKR body, without descriptive commentary
- If the user does not specify a period, default to quarterly
- If supplementary notes are needed (e.g., alignment relationships, metric definitions), append them as comments below the corresponding KR
