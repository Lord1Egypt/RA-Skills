# Spec Loading Matrix

Load this file before `--plan` and `--generate` as a silent classifier.

This is not a user-visible mode system. It is a small routing table that helps the skill read fewer files, not more files.

## Minimal Archetypes

Only keep these four archetypes:

- `brief`
- `research`
- `comparison`
- `update`

## Decision Table

| Archetype | Primary emphasis | Load first | Load only if needed | First-screen structure | Component preference |
|-----------|------------------|------------|---------------------|------------------------|----------------------|
| `brief` | bottom-line judgment and decision frame | `references/review-checklist.md`, `references/anti-patterns.md` | `references/rendering-rules.md` when structured components appear | purpose → judgment → action | callout, short KPI, short list |
| `research` | thesis, mechanism, evidence, implication | `references/review-checklist.md`, `references/anti-patterns.md` | `references/diagram-decision-rules.md` only when relationships are genuinely structural | judgment → timeline/mechanism → implication | prose, callout, timeline, selective diagram |
| `comparison` | side-by-side differences and decision tradeoffs | `references/rendering-rules.md`, `references/review-checklist.md` | `references/diagram-decision-rules.md` only when decision paths branch | comparison frame → key differences → recommendation | table, badge, KPI, chart |
| `update` | what changed, what matters now, what to do next | `references/review-checklist.md`, `references/anti-patterns.md` | `references/rendering-rules.md` when real metrics exist | status → signal → next step | KPI, timeline, callout, short list |

## Silent Classify Rule

The classifier should do only two things:

1. Determine `report_class`
2. Optionally determine `archetype`

If the archetype is unclear, leave it unset and continue. The report should still render correctly without it.
