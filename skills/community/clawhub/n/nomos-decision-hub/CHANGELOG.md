# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.7.0] - 2026-10-10

### Changed — BREAKING

**Meta-causal ledger terminology**
- `meta_ledger.bases` keys are now full ASCII: `trace_gap`, `parallel_convergence`,
  `narrative_occlusion`, `bounded_audit`, `causal_succession`.
- Reason-code prefixes converge to `TRACE_`, `CONVERGENCE_`, `NARRATIVE_`, `AUDIT_`,
  `SUCCESSION_`.
- Old keys and old prefixes are retired. **No aliases are kept** — carrying two
  vocabularies side by side is the cost that never goes away.
- Normative text is no longer quoted verbatim: quotations are paraphrased with section
  numbers, because mechanical substitution had rewritten quoted text into this
  project's vocabulary.
- Engine, adapter, version comments and test descriptions renamed in step; the old
  vocabulary is zero across the repository (excluding `language Standard/` and `logs/`).

### Tests
- 520 passing, 0 failures.

---

## [0.6.0] - 2026-10-10

### Added

**Ten-operator cognitive audit kernel** (`audit/cognitive/`)
- The cognitive audit kernel moves from five operators to ten: ⊙ORI / ⊞TPG / BFC /
  ⇄GRF / META, together with the topology base (four-process verification, including
  axiom 5 of intra-chain ordering).
- **META meta-causal ledger** — measurability only; structurally unable to block
  (always T2).
- **Report top-level views** — `topology`, `bfc` and `meta_ledger` are exposed, with
  `_config` injected so the A6/A10 thresholds are configurable.
- **Autonomous evolution layer (⊛∞)** — `evolve` proposes only and never applies
  (`auto_applied` is always 0); `approve` records but does not modify code.

**Contract extension**
- `DecisionRequest` gains optional first-class fields `origin` (`DecisionOrigin`) and
  `rollout` (`DecisionRollout`).

### Changed
- Adapter registration is conditional: `ORI` is registered only when an origin is
  declared, and `GRF` only when a gray-level ladder is declared — so no
  permanently-true blocker can be introduced.
- Artifact version string `GCAE-1.0.0 → GCAE-1.1.0`.

### Tests
- 507 → 520 (6 for conditional registration, 7 for the autonomous evolution layer).

---

## [0.5.0] - 2026-10-07

### Added — Enterprise Control Plane (closes the v0.4 production gaps)

**Persistent Event Store** (`persistence/event_store.py`)
- Append-only, hash-linked `DomainEvent` log emitted by `DecisionService` on every `evaluate` / `approve` transition.
- `InMemoryEventStore` (development) and `PostgresEventStore` (durable, per-tenant) implementations; `last_hash()` supports verifiable chains.

**Tenant Isolation** (`tenant.py`)
- A `contextvars`-based active-tenant context resolved from the `X-Tenant-Id` header (or OIDC `tid` claim when authorization is enforced).
- Per-tenant partitioning on the event store; tenant columns prepared on legacy tables via `scripts/migrate.py`.

**OIDC + Authorization Enforcement** (`api/authz.py`)
- Opt-in scope enforcement (`SP_AUTHZ_ENFORCE=true`) layered on top of existing authentication; `require_scope()` dependency guards write endpoints. Off by default — existing API-key deployments are unchanged.

**KMS Signing** (`security/kms.py`)
- Detached HMAC-SHA256 signatures over sealed artifact hashes (`LocalKmsSigner`, key from `SP_KMS_SECRET` / `SP_KMS_KEY_FILE`). Transparent no-op until configured; signatures surfaced via `X-Nomos-Kms-Signature` response headers.

**Rate Limiting** (`api/ratelimit.py`)
- Opt-in token-bucket middleware (`SP_RATE_LIMIT` rps) keyed per client. Disabled by default.

**Observability** (`observability/metrics.py`)
- In-process per-route request/error counters and latency averages; `ObservabilityMiddleware` stamps `X-Process-Time-Ms`; snapshot served at `GET /v1/metrics`.

**Backups / Migrations** (`scripts/migrate.py`, `scripts/backup.py`)
- Idempotent DDL migration runner (tenant columns + event store) and a JSON exporter for point-in-time backup.

**Domain Control Packs** (`domain/`)
- Pluggable `DomainControlPack` protocol + registry; ships `FinanceRiskControlPack` (flags multi-alternative decisions lacking an explicit risk owner). Packs observe only and never alter the engine verdict; `fail_on_domain_violation` is opt-in.

### Backward Compatibility
- All v0.4 APIs and behaviours are unchanged when the new env-gated features are unset.
- v0.3 archive documentation removed; baseline compatibility reference is now v0.4.
- `version.py` corrected to `0.5.0` (was stale at `0.3.0`).

---

## [0.4.0] - 2026-09-22

### Added

**Assumption Interaction Layer** (`src/second_perspective/interaction/`)
- New `interaction/` module with four formal invariants (I-1 through I-4):
  - I-1 Non-conjectural: every interaction strength Δ is explicitly declared by a responsible party; the engine never estimates or learns Δ.
  - I-2 Order-conservation: interactions only apply when **all** member assumptions are simultaneously invalidated.
  - I-3 Effect-boundedness: cumulative interaction effect ≤ `amplification_ceiling × Σ|first_order|`; redundant (negative) interactions have no floor clamp.
  - I-4 Monotonicity (union semantics): adding a failure never un-triggers an already-triggered interaction (`augment()`).
- Three interaction types: `conjunctive` (amplification, Δ > 0), `disjunctive` (redundancy, Δ < 0), `degenerate` (Δ = 0, retained as proof of inspection).
- `InteractionEngine` with `triggered()`, `joint_effect()`, `augment()` methods.
- Declaration validator (`validate_all()`) enforcing all four invariants at construction time.

**Formal Convergence** (`src/second_perspective/convergence/`)
- New `convergence/` module replacing heuristic stop checks with a formally-classified five-state model:
  - `FIXED_POINT` — candidate set stable (true convergence, P-2).
  - `NO_GAIN` — no unresolved branches (true convergence).
  - `BUDGET_EXHAUSTED` — budget ran out (**not** convergence; requires human).
  - `DIVERGED` — still changing with budget remaining.
  - `BLOCKED` — structural blocking condition hit (requires human).
- `is_true_convergence` guard against the classic "budget exhaustion misclassified as convergence" bug.
- Three checkable propositions (P-1 Termination, P-2 Fixed-point, P-3 Effect-boundedness).
- Pure, stateless `ConvergenceChecker` class with deterministic output.

**LLM Compliance Layer** (`src/second_perspective/llm_compliance/`)
- New `llm_compliance/` module formalizing a three-tier permission model:
  - T1 (Annotation): LLM may label/propose descriptions — no structural change.
  - T2 (Proposal): LLM may propose alternatives/weights/deltas — all subject to human approval.
  - T3 (Narrative): LLM may generate explanatory text — never used as decision input.
- Three invariants (L-1 through L-3): zone isolation, no adjudication, strength stripping.
- `LLMGate` enforcing that LLM output can never directly flip status, adjudicate, or alter weights.
- Provenance tracking (model id, timestamp, prompt fingerprint) on every LLM call.

**Core integration points** (non-breaking additions)
- `models/enums.py`: added `InteractionEffectType` enum.
- `models/schemas.py`: added `InteractionDecl`, `InteractionDeclaration`, and an optional `interaction_declaration` field on `DecisionRequest`; added `triggered_interaction_ids` and `interaction_contribution` optional fields on `FailureBranch`.
- `decision/causal.py`: added `invalidation_closure_with_interaction()` returning first-order closure plus an optional `InteractionPropagationResult`; original `invalidation_closure()` is unchanged.
- `hub/session.py`: `_stop_condition()` now delegates to the formal `ConvergenceChecker` internally while preserving the existing `(SessionStatus, ConvergenceKind | None)` return contract for full backward compatibility.

### Tests
- 122 new tests across `test_interaction.py` (28), `test_convergence.py` (38), `test_llm_compliance.py` (39), and `test_v04_integration.py` (17).
- Full regression: **402 passed, 0 failures** (previously 280).

### Backward Compatibility
- All existing APIs and default behaviours are unchanged.
- When `interaction_declaration` is not supplied (the default), the engine behaves identically to v0.4.
- No existing functions or classes were removed or renamed.
- `Cognitive Audit Engine` (GCAE) was not modified.

---

## [0.3.0] - 2026-09-19 (previous release)

- Deterministic alternative evaluation with constraint + weighted scoring.
- Forward invalidation propagation (`invalidation_closure`).
- Counterfactual analysis (what-if on assumption failure).
- Three-layer reconstruction sessions (forward/backward/delta).
- Scenario stress testing.
- Cognitive audit engine (GCAE).
- FastAPI service layer and CLI entry points.
- PostgreSQL-backed repository.
