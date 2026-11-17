# Architecture Decision Record

> 2026-07-02 | initial | docs/wiki/architecture/ARCHITECTURE.md

## Background

After reviewing AI-Novel-Writing-Assistant's AGENTS.md, we adopted several architectural rules that were missing from the original one-novel-skill codebase.

## Decisions

### 1. Quality Debt over Pipeline Blocking

**Problem**: A single chapter's quality issue could block a 50-chapter batch.

**Decision**: Adopt the Auto-Director Quality Gate pattern:
- Local quality issues (< 3 minor errors) → record as QualityDebt, continue batch
- Only unrecoverable failures (break OPEN, data integrity failure) → stop
- QualityDebt persisted to `追踪/quality_debt.json`

**Related modules**: `scheduler.QualityDebt`, `scheduler.Scheduler.run_batch()`

### 2. AI-First Routing (planned)

**Problem**: Detection routing uses hard-coded regex and keywords instead of AI judgment.

**Decision**: Migrate to AI-first routing where:
- AI determines the problem type first
- Deterministic code only for input validation and post-processing
- (See FUTURE_BACKLOG.md for timeline)

### 3. Module Size Limit

**Problem**: Some engine files exceed 600 lines (generator.py ~780, run_all_detectors.py ~600).

**Decision**: Source files should stay ≤ 700 lines. When exceeded, split into functional modules.

**Current violations**: generator.py, run_all_detectors.py

## Related

- [`quality_gate.py` workflow](../workflows/QUALITY_GATE.md)
- [`FUTURE_BACKLOG.md`](../../FUTURE_BACKLOG.md)
