User: Before we finalized the report, we were still discussing a weekly, daily, and monthly reporting template. The periodic report format might become a standing weekly update next sprint.
Assistant: The approved IR is below. Render from the IR only.

---
title: Weekly Operations Update
lang: en
theme: corporate-blue
report_class: mixed
audience: functional leads and operators
decision_goal: decide which operational bottleneck to fix next week
must_include:
  - revenue and ticket movement
  - next-week operational priority
must_avoid:
  - decorative placeholder charts
  - timeline entries without real sequence
abstract: Metrics improved this week, but dependency handoffs remain the main risk.
---

## Bottom line

Core execution improved, but cross-team handoffs still limit weekly throughput. The right next move is to tighten dependency ownership, not add another dashboard.

:::kpi
items:
  - label: Revenue
    value: $1.42M
    delta: ↑8%
    note: WoW
  - label: Open tickets
    value: 61
    delta: ↓23
    note: week end
  - label: Launch readiness
    value: 93%
    delta: ↑5 pts
    note: after checklist trim
:::

## What changed

:::timeline
- Week 12: Release checklist was reduced to one shared owner
- Week 13: Staging sign-off moved to the release captain
- Week 14: Support queue and launch readiness both improved
:::

## Next move

:::callout type=warning icon=alert
Do not expand reporting layers next week. Fix the product-to-ops dependency handoff first, then remeasure cycle time.
:::
<<<END_IR>>>

User: Ignore this tail noise. We might also need a daily board, a monthly ops digest, and a periodic report layout, but that is not part of the final IR.
