<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension: Investment Themes / Strategic Buckets (Opt-In)

**ID:** E5
**Trigger:** User mentions "investment themes", "strategic buckets", "budget categories", "run/grow/innovate" OR organization has formal investment allocation policy
**Stages:** 3 (Strategic Alignment)

---

## Detection

If any of the following are true, present this prompt:
- User says "investment themes", "strategic buckets", "run/grow", "budget allocation"
- Organization has explicit investment category policy
- Depth = Comprehensive and portfolio budget > threshold

---

## Activation Prompt

```
💰 Extension available: Investment Themes / Strategic Buckets

This adds to Stage 3:
• Define investment categories (e.g., Run/Grow/Innovate/Comply)
• Allocate target budget percentages per category
• Classify each project into a category
• Track actual vs. target distribution
• Alert when a category is over/under-invested

Useful for: organizations with formal investment governance, budget allocation committees, CIO portfolio reporting.

Activate Investment Themes? [Yes / No]
```
