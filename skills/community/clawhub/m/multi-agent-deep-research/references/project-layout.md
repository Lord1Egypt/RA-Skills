# Project Layout

Use one canonical project root, usually named after the topic:

```text
topic_research/
├── README.md
├── workflow/
│   ├── STATE.md
│   ├── TASK_BOARD.md
│   └── DECISIONS.md
├── sources/
│   ├── source_registry.md
│   └── notes/
├── claims/
│   └── claim_tracker.md
├── checks/
│   └── fact_check_log.md
├── handoffs/
│   └── CURRENT.md
├── matrices/
│   └── comparison_matrix.md
└── deliverables/
    └── report.md
```

## Minimal rules

- `README.md`: describe goal, scope, and the canonical directory rule.
- `workflow/STATE.md`: current phase, recent progress, next actions, open questions.
- `workflow/TASK_BOARD.md`: task ownership, dependencies, and output files.
- `workflow/DECISIONS.md`: scope or method decisions that future agents must not silently undo.
- `sources/source_registry.md`: one row per source.
- `sources/notes/`: topic or dimension notes with compact summaries and URLs.
- `claims/claim_tracker.md`: one row per material claim.
- `checks/fact_check_log.md`: review status, caveats, and downgrade notes.
- `handoffs/CURRENT.md`: the next agent's starting point.
- `matrices/comparison_matrix.md`: optional but strongly recommended for comparative research.
- `deliverables/report.md`: the evolving final report.

## When to add more structure

- Add `docs/` if the project needs a dedicated method memo or execution blueprint.
- Add `agents/` if the PM needs reusable task packets.
- Add `references/` only if the topic has stable internal standards or domain docs worth reusing.

## Canonical-directory rule

- Choose one root and say so explicitly.
- If subagents or parallel drafts create duplicate folders, consolidate quickly.
- Keep "reference-only" parallel artifacts clearly marked so they do not compete with the main ledger.
