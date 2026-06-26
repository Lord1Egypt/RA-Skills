# Internal Worker Playbooks

`ppt-maker` is the only user-facing skill. The workers below are internal operating roles.

## Stages

- `intake`
Brief clarification and material packaging.

- `story`
Narrative pattern, opening tension, and closing ask.

- `evidence`
Fact extraction, proof-gap detection, and asset mapping.

- `outline`
One-job-per-slide sequencing.

- `design`
Visual system, density, and media policy.

- `draft`
Slide-by-slide content, asset placement, and speaker notes.

- `review`
Acceptance review and revision orders.

- `export`
Local artifact generation.

## Workers

### Producer

Use in `intake`.

Owns:
- `DeckProject`
- `IntakeAssessment`

Gate:
- `decision`, `audience`, `scene`, and `materials` must be clear enough to continue

### Story Strategist

Use in `story`.

Owns:
- `NarrativeArc`
- `Open Questions`

Gate:
- if the target decision is unclear, send the work back to `Producer`

### Research Analyst

Use in `evidence`.

Owns:
- `EvidenceAudit`
- `asset-map.json`
- `assumption-log.json`

Gate:
- proof-heavy decks cannot be marked ready if key evidence is still missing

### Slide Architect

Use in `outline`.

Owns:
- `DeckOutline`
- `page-jobs.json`

Gate:
- each slide must have exactly one job
- each page job should specify at least: `conclusion`, `support`, `visual role`, and `page recipe`
- do not mark outline ready if important pages still have no planned evidence or visual support

### Design Director

Use in `design`.

Owns:
- `VisualDirection`
- `MediaPlan`
- `LayoutPolicy`
- `TypographyPolicy`

Gate:
- style must fit the audience and scene, not just "look good"
- layout and typography decisions should be resolved internally unless they change meaning or violate explicit brand constraints
- polished decks should not be approved with a zero-media plan or a single repeated page grammar

### Deck Designer

Use in `draft`.

Owns:
- `DeckPack`

Gate:
- no page should carry placeholder content or unplanned assets
- `Draft` should be good enough to survive internal review before any user-facing reveal
- do not expose a shallow rough draft just to show progress

### Review Editor

Use in `review`.

Owns:
- `DeckReadiness`
- `quality-report.json`

Gate:
- missing content, distorted assets, weak proof, or language mismatch mean not ready
- zero-media text-heavy decks, repetitive page rhythm, noisy footer chrome, or async-incomprehensible demo pages mean not ready

### Export Operator

Use in `export`.

Owns:
- `.pptx`
- preview bundle
- delivery compatibility profile
- `wechat-safe-editable.pptx` when needed

Gate:
- export only after review passes
- if WeChat is in the delivery path, do not export a single desktop-only file and call the job done

## Reporting Format

When reporting progress, prefer this shape:

```text
Stage: evidence
Current Owner: Research Analyst
Current Gate: proof audit
Current Artifact: asset-map.json
Active Workers: Research Analyst, Story Strategist
Blocker: benchmark table still lacks source metrics
Next Action: finish evidence audit, then hand page jobs to Slide Architect
```
