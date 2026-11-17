# Decision Foundation v0.2: From Prototype to Deterministic Core

## Verdict

The previous branch is already a runnable deterministic MCDA prototype, but it cannot yet be called a "decision foundation." The safest one-step approach is not to cram in every algorithm at once, but to lock down the core contract that is hard to overturn: no fabricated inputs, versioned rules, traceable causality, reproducible results, accountable approvals, and no silent record overwrites.

v0.2 codifies this core contract. Future capabilities can be added around it without rewriting `DecisionRequest`, `DecisionResult`, or the governance boundary.

## Full Branch Audit

What the original implementation already has: strict input models, hard constraints, linear weighted scoring, assumption and evidence references, structural auditing, human approval, FastAPI, in-memory repository, and basic tests.

Key gaps in the original implementation:

1. Soft constraints were only checked but did not affect results.
2. Assumption failure only looked at direct references, with no transitive propagation.
3. Evidence had only status, not quality, timeliness, or content fingerprint.
4. A single weighted total score easily masked Pareto dominance and weight fragility.
5. Approval only compared display names; no credential verification.
6. Production environments allowed access when no API key was set.
7. The in-memory repository overwrote history; no revision chain or integrity proof.
8. Rules, engine version, and input summary were not frozen with the result.
9. OpenAPI spec, Dockerfile, package metadata, and README filenames had drifted.
10. Test coverage was insufficient; governance, security, and robustness tests were missing.

## v0.2 Invariants

These constraints are the long-term boundary of the foundation:

- The engine must never guess missing weights, evidence, metrics, responsible parties, thresholds, or authorization relationships.
- Hard constraints determine eligibility; soft constraints must carry an explicit penalty value and must not silently alter scores.
- Every policy that affects behavior must carry a `policy_id` and `version`, embedded into the result.
- The quality of critical evidence is assessed by a named responsibility node; the engine never fabricates credibility on behalf of the user.
- Assumption dependency failures must propagate along the dependency graph and explicitly flag affected alternatives.
- Algorithm output can only be called "leading candidate under current parameters"; the final state must pass independent human approval.
- The approver name and `authorization_ref` must both match the decision owner anchored in the input.
- Every evaluation or approval is a new revision and never overwrites old records; each record points to the previous record's hash.
- Identical inputs, `evaluation_as_of`, policy, and engine version must produce identical evaluation content (revision metadata excepted).

## Implemented Architecture

```text
DecisionRequest
  │
  ├─ Pydantic strict validation: IDs, references, ranges, weights, soft penalty
  │
  ├─ StructuralAuditor
  │    ├─ Responsibility attribution
  │    ├─ Evidence status / timeliness / quality
  │    ├─ Critical-assumption evidence
  │    └─ Assumption dependency cycle detection
  │
  ├─ Deterministic Evaluator
  │    ├─ hard constraint eligibility
  │    ├─ soft constraint penalty
  │    └─ normalized weighted / constraint-only scoring
  │
  ├─ Causal invalidation closure
  │    └─ ¬A -> transitive failed assumptions -> affected alternatives
  │
  ├─ Robustness Analyzer
  │    ├─ Pareto frontier
  │    └─ Single-factor weight ±δ sensitivity
  │
  ├─ Human Governance Gate
  │    └─ owner + authorization_ref
  │
  └─ Append-only Repository
       └─ revision + parent_record_hash + record_hash
```

## v0.2 Result Contract

Every `DecisionResult` now contains:

- Eligible, information-incomplete, and ineligible alternatives;
- Base scores, soft-constraint penalties, and final scores;
- Blocking and non-blocking audit findings;
- Transitive failure branches and candidate exposure ratios;
- Pareto frontier, sensitivity cases, fragile metrics, and stable leaders;
- Responsibility mapping and unresolved variables;
- A human-readable rule trace;
- A complete policy snapshot, engine version, frozen evaluation timestamp, and input SHA-256 fingerprint.

Every `DecisionRecord` additionally contains `revision`, `parent_record_hash`, and `record_hash`, forming an append-only history chain.

The repository recomputes the record digest on both write and read and verifies the entire parent-hash chain; mismatches cause the record to be rejected.

## File Mapping

| Domain | File | Responsibility |
|---|---|---|
| Input / output contract | `models/schemas.py` | Strict models and cross-reference validation |
| Behavior policies | `decision/policy.py` | Versioned, snapshotable deterministic rules |
| Alternative evaluation | `decision/evaluator.py` | Constraints, normalization, explicit penalties |
| Causal propagation | `decision/causal.py` | Transitive closure of assumption failure |
| Robustness | `decision/robustness.py` | Pareto and weight sensitivity |
| Integrity | `decision/integrity.py` | Input fingerprint and record hashing |
| Structural audit | `audit/auditor.py` | Evidence, responsibility, and dependency gaps |
| Governance | `governance/approval.py` | Human approve/reject and authorization matching |
| Versioned storage | `repository.py` | Append-only history interface and dev implementation |
| Use-case orchestration | `service.py` | Evaluate, approve, revise, and history |
| External interface | `api/` | API, security boundaries, and status codes |

## Iteration Roadmap

### v0.3: Production Control Plane

Goal: "deployable, isolated, recoverable" — without changing the v0.2 decision contract.

- PostgreSQL event repository, optimistic locking, migrations, and backup/recovery drills;
- Tenant isolation, OIDC identity, service identities, and RBAC/ABAC authorization;
- Policy registry, policy signing, canary release, and rollback;
- Idempotency keys, request size limits, rate limiting, and task queues;
- Metrics, structured logs, tracing, alerts, audit export, and retention policies;
- KMS/HSM signatures on record hashes instead of only a local SHA-256 chain.

Completion criteria: no revisions lost under multi-instance concurrency; cross-tenant access blocked by automated tests; policies replayable; backups restorable.

### v0.4: Advanced Decision Intelligence

Goal: enhance analysis without letting language models take over decisions.

- Interval and probability distributions for metrics;
- Fixed-seed Monte Carlo and declared scenario stress tests;
- Multi-strategy comparison: weighted sum, TOPSIS, ELECTRE/ranking, outputting consistency gaps;
- Value of Information (VoI) analysis pointing to the most worthwhile evidence to gather;
- True counterfactual recomputation: remove alternatives that lose invalidated-assumption support and recompute candidates and robustness;
- Compositional constraints and alternative-portfolio optimization;
- Versioned normalization, missing-value, and outlier policies.

Completion criteria: all stochastic analyses reproducible; different algorithms are not blended into one "mystery total score"; counterfactual results explainable rule-by-rule.

### v0.5: Evidence and Organizational Knowledge Layer

- Evidence connectors, content hashing, signature verification, and data lineage;
- Temporal evidence and automatic expiry reviews;
- Responsibility delegation chains, authorization validity periods, and duty-conflict checks;
- Optional graph database for large-scale assumption/evidence/responsibility network queries;
- Industry control packs: procurement, investment/financing, product, incident response, and other independent policy templates.

Completion criteria: every fact can be traced to a source, responsible party, validity period, and the decision revisions that used it.

### v1.0: Enterprise Decision Platform

- Constrain LLMs to the "collect, structure, challenge, explain" layer; the deterministic engine runs independently;
- Dual-track human-machine audit: raw input, model suggestions, user confirmation, and final structure are stored separately;
- Offline benchmark sets, historical replay, drift detection, red-teaming, and domain accuracy thresholds;
- Approval workflows, countersign, veto, conflict-of-interest, and escalation mechanisms;
- SDK, webhooks, batch evaluation, and embeddable frontend components.

Completion criteria: provably answering "who, under what authority, based on which version of facts and policies, formed this result, and why."

## Migration

When upgrading v0.1 requests to v0.2:

1. All constraints with `kind=soft` must supply `penalty`; hard constraints must not carry this field.
2. Critical evidence should be supplemented with `valid_until`, `quality`, and optional `content_hash`.
3. A timezone-aware `evaluation_as_of` should be provided explicitly; if omitted the engine freezes the first-evaluation timestamp.
4. Decision owners must supply `authorization_ref` or approval is denied.
5. Consumers must accept the new fields on `DecisionResult`: `robustness`, `trace`, `policy`, `engine_version`, and `input_fingerprint`.
6. The same `decision_id` is no longer overwritten; clients can view all revisions via `/history`.

## Security and Responsibility Boundaries

The v0.2 Bearer API key is suitable only for development and controlled pilot deployments; it cannot prove the identity of a real person. Production approval must integrate with the organization's identity provider and verify the authorization chain. The hash chain can expose tampered records, but without external signatures and trusted timestamps it cannot by itself prove that the storage system was never rewritten wholesale.

This engine exists to increase decision transparency; it does not replace the professional responsible parties in legal, medical, financial, or security domains.
