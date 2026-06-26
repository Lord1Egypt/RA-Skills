# Cliche Exhaustion Loop

## Goal

Use the Cliche Exhaustion Loop as a supervisor-side protocol layer that pressure-tests novelty before canonizing a direction.

This is not a new workflow stage.
It overlays `Discovery`, `Story Planning`, `Opening`, and `Proofreading` with mode-specific anti-cliche checks.

Parent ownership remains unchanged:
- the parent remains the sole owner of `.novel-state.json`
- the parent remains the sole owner of staging branch selection
- the parent remains the sole owner of canonical backfill
- the parent remains the sole owner of stale-branch cleanup

## Mode split

- `Discovery` uses `quick` mode
- `Story Planning` uses `deep` mode
- `Opening` validates retained novelty axes rather than reopening broad ideation
- `Proofreading` only does lightweight parent-side backslide detection and reporting in this slice

## `quick` mode for Discovery

Use `quick` mode to expose obvious, first-order cliché gravity before topic approval.

Minimum checks:
- enumerate the intuitive market-default version of the direction
- note why that version is attractive
- note why that version is likely to collapse into sameness
- retain the novelty axes worth carrying into planning

`quick` mode is fast by design.
It does not try to exhaust every branch.

## `deep` mode for Story Planning

Use `deep` mode after a discovery direction is retained and before planning approval.

Minimum checks:
- enumerate cliché samples for the retained direction, not just abstract warnings
- identify which novelty axes must survive outline expansion
- state the failure mode if the outline falls back to the default genre rail
- record what the retained direction is explicitly not doing

Hard rule:
- planning approval must not occur until the retained direction has gone through deep anti-cliche review and the branch conclusion states which novelty axes survived
- when the supervisor activates the deep anti-cliche pass, it must be recorded through the staging branch conclusion (`05_定稿结论.md`) before planning approval
- do not treat an unpersisted discussion-only deep pass as sufficient planning-gate evidence

## Staging branch artifact layout

When explicit brainstorming mode creates a Cliche Exhaustion staging branch, use this layout under `staging/<stage>/<branch-id>/`:
- `00_脑暴任务卡.md`
- `01_直觉俗套清单.md`
- `02_反驳与否认.md`
- `03_变异候选.md`
- `04_保留候选.md`
- `05_定稿结论.md`

Rules:
- these are supervisor-side branch artifacts, not canonical project files
- only `05_定稿结论.md` may authorize canonical backfill
- if no branch reaches `05_定稿结论.md`, do not backfill exploratory material into canonical files
- after one branch is accepted and backfilled, delete stale sibling branches

## Opening hook

Opening review must validate delivery of the retained novelty axes.

It should check:
- whether the first-3 / first-10 / first-20 chapter design still reflects the retained novelty axes
- whether the opening has collapsed back to the intuitive cliché version
- whether the retained freshness survives scene-level execution pressure

Do not use the opening review to restart wide ideation.

## Proofreading hook

Proofreading only does lightweight parent-side backslide detection in this slice.

It may report:
- where a batch slides back toward the previously enumerated cliché samples
- which retained novelty axes weakened
- whether drift is cosmetic, moderate, or blocking

Rules:
- lightweight backslide detection is parent-side only in this slice
- accepted proofreading may trigger a parent-side style-risk refresh
- the child proofreading bundle/result contract does not change because of this slice

It does not reopen Discovery or Story Planning by itself.
