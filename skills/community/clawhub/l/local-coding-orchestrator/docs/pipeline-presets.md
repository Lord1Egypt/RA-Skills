# Pipeline presets

This document defines the initial pipeline presets for `local-coding-orchestrator`.

## Goal

Multi-tool orchestration should use role-based pipelines, not just side-by-side tool fan-out.

## Presets

### `implement_and_review`
- Codex: implementation lead
- Claude: architecture and risk review
- OpenCode: alternative plan or follow-up support

Use when:
- default coding delivery flow
- normal feature work
- refactors that benefit from post-implementation scrutiny

### `design_then_build`
- Claude: design and solution framing
- Codex: implementation
- Claude: post-build review

Use when:
- solution framing matters before code changes
- UI or architecture direction is still soft

### `investigate_then_fix`
- Claude: root-cause analysis
- Codex: fix implementation
- Claude: regression and edge-case review

Use when:
- bug cause is unclear
- user wants diagnosis before code edits

### `parallel_compare`
- Codex: candidate A
- Claude: candidate B
- OpenCode: candidate C

Use when:
- the user explicitly wants comparison
- benchmarking or solution diversity matters more than speed

### `pr_hardening`
- Claude: review for architecture and maintainability
- OpenCode: alternative patch or follow-up strategy
- Codex: repair pass for blocking issues

Use when:
- a candidate implementation already exists
- the goal is to harden before merge or approval

## Guidance

Prefer the narrowest pipeline that fits the task.
Do not default to `parallel_compare` unless the user really wants multiple competing outputs.

## Stage model

The v2 scaffold now benefits from treating work as stage-based rather than as a single launch.

Recommended conceptual stages:
- `probe`
- `implement`
- `review`
- `harden`

Current implementation is strongest in `probe` and `implement`, and is moving toward a more formal `review` stage.
