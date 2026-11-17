# Version Manifest

Skill: `nomos-decision-hub` · skill version **2.1.0**

Engine: NOMOS **0.7.0** (`src/second_perspective/version.py`)

Source: `https://github.com/nohn3043-arch/NOMOS`

This file replaces the v0.3 branch manifest. It records which capabilities the
bundled engine actually claims — nothing here is aspirational.

## Retained from v0.2 (Decision Foundation)

- strict structured decision inputs
- deterministic hard and soft constraints
- normalized weighted and constraint-only evaluation
- evidence quality, expiry, and responsibility anchors
- transitive causal assumption invalidation
- Pareto frontier and weight sensitivity
- human authorization gate
- append-only hash-chained decision revisions
- production fail-closed API-key behavior

## v0.3 — Hub application core

- hash-chained fine-grained algorithm audit events
- explicit constraint operands, scoring normalization, penalty and aggregation records
- counterfactual leader reselection after assumption failure
- metric / evidence-status / assumption-failure scenario stress tests
- deterministic structural cognitive-risk scanner
- ranked information and review priorities
- versioned `HubPolicy`, sealed `HubReport`
- `IntelligentDecisionHub` orchestration API and CLI
- `POST /v1/hub/analyze`

## v0.4 — Second-order causality

- assumption interaction layer (`interaction/`), invariants I-1…I-4
- three interaction types: `conjunctive` / `disjunctive` / `degenerate`
- formal convergence engine (`convergence/`), five states
  `FIXED_POINT` / `NO_GAIN` / `BUDGET_EXHAUSTED` / `DIVERGED` / `BLOCKED`,
  propositions P-1…P-3, `is_true_convergence` guard
- LLM compliance layer (`llm_compliance/`), tiers T1/T2/T3, invariants L-1…L-3
- optional `interaction_declaration` on `DecisionRequest` (default `None`)

## v0.5 — Enterprise control plane (env-gated, off by default)

- persistent event store (`persistence/event_store.py`), in-memory + PostgreSQL
- tenant isolation via `contextvars` and `X-Tenant-Id`
- OIDC + opt-in scope enforcement (`SP_AUTHZ_ENFORCE`)
- KMS detached HMAC-SHA256 signing (`SP_KMS_SECRET` / `SP_KMS_KEY_FILE`)
- opt-in token-bucket rate limiting (`SP_RATE_LIMIT`)
- per-route observability and `GET /v1/metrics`
- idempotent migrations (`scripts/migrate.py`) and JSON backups (`scripts/backup.py`)
- pluggable `DomainControlPack` registry; ships `FinanceRiskControlPack`

## v0.6 — Ten-operator cognitive audit kernel

- kernel upgraded 5 → 10 operators: `ORI` / `NS` / `IAP` / `LCH` / `TPG` / `BFC` /
  `CCS` / `GRF` / `META` / `STATE`
- topology substrate with four parallel checks (consistency, constraint, closure,
  time order)
- `META` meta-causal ledger: measure-only, always T2, structurally unable to block
- conditional adapter registration for `ORI` and `GRF`
- proposal-only autonomous evolution layer (`auto_applied ≡ 0`)
- report top-level views `topology` / `bfc` / `meta_ledger`
- artifact version `GCAE-1.0.0 → GCAE-1.1.0`; tests 507 → 520

## v0.7 — Meta-causal ledger terminology (breaking)

- `meta_ledger.bases` keys are `trace_gap` / `parallel_convergence` /
  `narrative_occlusion` / `bounded_audit` / `causal_succession`
- reason-code prefixes `TRACE_` / `CONVERGENCE_` / `NARRATIVE_` / `AUDIT_` /
  `SUCCESSION_`
- old keys and prefixes retired, **no aliases kept**
- normative text paraphrased with section numbers instead of verbatim quotation
- tests 520 passing

## Explicitly not claimed

- durable multi-tenant Hub/event database beyond the shipped event store
- RBAC/ABAC beyond opt-in OIDC scope enforcement
- KMS/HSM and trusted timestamps beyond the shipped HMAC signer
- uncertainty distributions or seeded Monte Carlo analysis
- portfolio optimisation
- external evidence connectors and provenance verification
- domain validation packs and historical benchmark datasets
- any guarantee of decision quality: output is a leading candidate under declared
  inputs, and final authority stays outside the algorithm

Full details: `CHANGELOG.md`, `docs/INTELLIGENT_DECISION_HUB_V0_4.md`,
`docs/VERIFICATION_GUIDE.md`.
