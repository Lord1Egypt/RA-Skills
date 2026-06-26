# Logbox Template & Guide

The LOGBOX is the project's decision provenance trail. It tracks milestones, phase
transitions (including backtracks), and key decisions throughout the research lifecycle.

## Format

Create `LOGBOX.md` at the project root with this structure:

```markdown
# Research Logbox: [Project Title]

| # | Phase | Summary | Date |
|---|-------|---------|------|
```

### Multi-exploration format

When the project has multiple research directions, add an **Exploration Registry** table
at the top to track all explorations and their relationships:

```markdown
# Research Logbox: [Project Title]

## Explorations
| ID | Name | Status | Parent | Current Phase | Started |
|----|------|--------|--------|---------------|---------|

## Decision Log
| # | Phase | Summary | Date |
|---|-------|---------|------|
```

**Status values**: `active` / `paused` / `completed` / `archived`

Prefix each Decision Log entry with `[NNN]` to tie it to a specific exploration.
The Explorations table is only needed when multiple directions exist — for single-direction
projects, use the simple format above.

## Entry Types

### Phase Entry (work within a phase)

```
| 3 | Lit Review | Searched 4 databases (arXiv, Scholar, Scopus, DBLP), screened 47 papers, 12 included. Key gap: no evaluation of X under Y conditions. | 2026-03-01 |
```

### Forward Transition

```
| 4 | Lit Review → Experiment Design | Evidence map complete. Novelty gap validated: no prior work tests X on Z data. Moving to protocol design. | 2026-03-02 |
```

### Backward Transition (BACKTRACK)

```
| 5 | Analysis → Experiment Design | BACKTRACK: discovered train/test overlap in dataset preprocessing. Must fix splits and re-run. | 2026-03-05 |
```

### Negative Result

```
| 6 | Analysis | Negative finding: method X does not improve over baseline B on metric M (Δ = -0.3 ± 0.5). Logging as valid result. | 2026-03-06 |
```

### Decision Point

```
| 7 | Experiment Design | DECISION: chose metric M1 over M2 because M1 better reflects deployment objective. M2 kept as secondary (exploratory). | 2026-03-03 |
```

### Error / Recovery

```
| 8 | Analysis | ERROR: GPU OOM during evaluation on large test set. Switched to batch evaluation. Results unaffected. | 2026-03-07 |
```

## Rules

1. **Always log** phase entries AND transitions (including backtracks)
2. **Keep summaries to 1-2 sentences** — concise but informative
3. **Include trigger reason** for any backward transition
4. **Number sequentially** — never renumber, even after backtracks
5. **Log negative results** as valid milestones, not failures
6. **Log decisions** when choosing between alternatives
7. **Timestamp every entry** with the date it was logged

## Example: Complete Logbox

```markdown
# Research Logbox: Scaling Laws for Few-Shot Learning

| # | Phase | Summary | Date |
|---|-------|---------|------|
| 1 | Brainstorm | Generated 15 candidate directions around few-shot learning efficiency. Top 3 scored ≥ 3.8/5. | 2026-02-15 |
| 2 | Brainstorm | Fast falsification: idea #2 (meta-learning baseline) already beaten by recent work. Eliminated. | 2026-02-16 |
| 3 | Brainstorm → Lit Review | Selected idea #1: scaling laws for few-shot performance. Moving to evidence mapping. | 2026-02-17 |
| 4 | Lit Review | Searched arXiv, Scholar, DBLP. 52 papers screened, 18 included. Found 3 closely related but none on our exact formulation. | 2026-02-20 |
| 5 | Lit Review → Experiment Design | Novelty gap confirmed. Identified 4 strong baselines. Moving to protocol. | 2026-02-22 |
| 6 | Experiment Design | DECISION: primary metric = few-shot accuracy at k=5. Secondary: k=1, k=10 (exploratory). | 2026-02-23 |
| 7 | Experiment Design | Protocol locked. 5 seeds per condition, 3 datasets, 4 baselines + ours. | 2026-02-25 |
| 8 | Experiment Design → Analysis | Implementation complete. First runs submitted. | 2026-02-27 |
| 9 | Analysis | Sanity checks passed. Baseline reproduces published numbers (within 0.5%). | 2026-02-28 |
| 10 | Analysis → Experiment Design | BACKTRACK: discovered temporal leakage in dataset C. Must fix splits. | 2026-03-01 |
| 11 | Experiment Design | Fixed splits for dataset C. Re-running all conditions on corrected data. | 2026-03-02 |
| 12 | Experiment Design → Analysis | Re-runs complete. Resuming analysis with corrected data. | 2026-03-03 |
| 13 | Analysis | Primary result: our method improves by 2.1 ± 0.4 pts over best baseline on 2/3 datasets. Dataset C shows no improvement. | 2026-03-05 |
| 14 | Analysis | Ablation: component A accounts for 1.8 pts; component B adds 0.3 pts (marginal). | 2026-03-06 |
| 15 | Analysis → Writing | Claim supported on 2/3 datasets. Moving to write-up with honest limitation on dataset C. | 2026-03-07 |
| 16 | Writing | Methods and results sections drafted. Reproducibility checklist: 87%. | 2026-03-10 |
| 17 | Writing → Analysis | BACKTRACK: realized missing behavioral test for edge case. Running additional analysis. | 2026-03-11 |
| 18 | Analysis → Writing | Behavioral tests complete. Two failure modes documented. Resuming writing. | 2026-03-12 |
| 19 | Writing | Draft complete. Artifacts packaged. Pre-submission checklist passed. | 2026-03-15 |
```

Notice the natural back-and-forth between phases — this is expected and healthy.
The logbox makes the non-linear process transparent and auditable.

## Example: Multi-Exploration Logbox

When a project pivots to a new direction, the logbox tracks both explorations:

```markdown
# Research Logbox: Efficient In-Context Learning

## Explorations
| ID | Name | Status | Parent | Current Phase | Started |
|----|------|--------|--------|---------------|---------|
| 001 | prompt-compression | archived | — | lit-review | 2026-02-15 |
| 002 | retrieval-icl | active | 001 | analysis | 2026-02-22 |

## Decision Log
| # | Phase | Summary | Date |
|---|-------|---------|------|
| 1 | Brainstorm | [001] Generated 12 candidates. Top pick: prompt compression for long contexts. | 2026-02-15 |
| 2 | Brainstorm → Lit Review | [001] Moving to evidence mapping. | 2026-02-16 |
| 3 | Lit Review | [001] Novelty gap closed: [paper X] covers our exact formulation. Archiving. | 2026-02-21 |
| 4 | Brainstorm | [002] Pivoted from 001. New direction: retrieval-augmented ICL. Reused evidence map → shared/literature/. | 2026-02-22 |
| 5 | Brainstorm → Lit Review | [002] Supplementing lit review with retrieval-specific papers. | 2026-02-23 |
| 6 | Lit Review → Experiment Design | [002] Novelty gap confirmed. 3 baselines identified. | 2026-02-25 |
| 7 | Experiment Design → Analysis | [002] Protocol locked. Running experiments. | 2026-02-28 |
```

The `[NNN]` prefix makes it easy to filter the log for a specific exploration.
