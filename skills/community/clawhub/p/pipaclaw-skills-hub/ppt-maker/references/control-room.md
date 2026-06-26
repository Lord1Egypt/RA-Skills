# PPT Control Room

The PPT system should feel like a small team with visible ownership, not a single black box.

Use this status shape whenever the work is more than a quick answer:

- `Current Owner`
- `Current Gate`
- `Current Artifact`
- `Blocker`
- `Next Action`

## Roles

- `Producer`
Front desk. Clarifies `decision`, `audience`, `scene`, and `materials`.

- `Story Strategist`
Chooses the narrative pattern, opening tension, core argument, and closing ask.

- `Research Analyst`
Audits evidence, extracts usable facts, logs proof gaps, and maps source materials to pages.

- `Slide Architect`
Turns the story into a page sequence with one job per slide.

- `Design Director`
Chooses the visual system, density, media policy, and template fit for the scene.

- `Deck Designer`
Writes slide-by-slide copy, asset placement, and speaker-note-ready specs.

- `Review Editor`
Rejects weak drafts and issues revision orders.

- `Export Operator`
Builds the final `.pptx`, preview assets, and local output bundle.

## Handoff Artifacts

- `Producer -> Story Strategist`
`DeckProject`, `IntakeAssessment`

- `Story Strategist -> Research Analyst`
`NarrativeArc`, `Open Questions`

- `Research Analyst -> Slide Architect`
`EvidenceAudit`, `asset-map.json`, `assumption-log.json`

- `Slide Architect -> Design Director`
`DeckOutline`, `page-jobs.json`

- `Design Director -> Deck Designer`
`VisualDirection`, `MediaPlan`

- `Deck Designer -> Review Editor`
`DeckPack`

- `Review Editor -> Export Operator`
`DeckReadiness`, `quality-report.json`

## Default Rule

Do not skip an upstream gate:
- if `decision / audience / scene / materials` are unclear, return to `Producer`
- if proof is weak for a proof-heavy deck, block with `Research Analyst`
- if the outline does not have one job per slide, return to `Slide Architect`
- if the visual direction is chosen only because it "looks good", return to `Design Director`
- if the deck draft still has missing content, distorted assets, or unclear asks, block in `Review Editor`
