# spec-ocas-recovery.md — Recovery Contract (Custodian Perspective)

**Full spec**: `<hermes-home>/commons/specs/spec-ocas-recovery-draft.md`

Custodian enforces this recovery contract across all OCAS skills. Key sections:

| Section | Custodian implementation |
|---|---|
| Durable Intent Queue (DIQ) | `intents.jsonl` — tracks pending actions with state machine: staged → complete/superseded/stale/cancelled |
| Execution Evidence Log (EEL) | `evidence.jsonl` — every scheduled run writes an evidence record (including no-op runs with `not_activity_reason`) |
| Schedule gap detection | Deep scan checks `evidence.jsonl` for missing runs; triggers remedial passes when gaps exceed thresholds |
| `not_activity_reason` | Written to `evidence.jsonl` on no-op runs (all_clear, quiet_hours_deferred, activity_ongoing) |
| Degraded mode | Explicit `degraded: true` flag in evidence records — never silent skip; always recorded |
| Self-repair validation | Every fix includes re-validation; `fix_effectiveness.jsonl` tracks outcomes |
| `schedule_adherence` OKR | Fraction of expected runs that produced evidence (target ≥ 0.98, window 30 runs) |
| `data_integrity` OKR | Fraction of reads that pass schema validation (target 1.00, window 30 runs) |

**Storage files (recovery-specific):**

| File | Purpose | Retention |
|---|---|---|
| `intents.jsonl` | Durable intent queue — pending actions across all OCAS skills | 30 days terminal state |
| `evidence.jsonl` | Execution evidence log — one entry per scheduled run | 30 days (no-op), 90 days (errors/gaps) |

**When modifying custodian's recovery behavior**, update both this reference and the full spec file simultaneously.