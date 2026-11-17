# Intelligent Decision-Hub v0.4: Second-Order Causal Decision Framework

## Positioning

v0.3 upgraded a single decision from "one-shot computation" to "hub orchestration" — baseline decision + algorithm audit + counterfactuals + stress scenarios + cognitive challenge + information prioritization + governance records.

v0.4 systematically addresses **assumption-to-assumption interactions** rather than treating each failure as an independent event; pins the iterative reconstruction loop to **formally classified convergence states** (provable, not heuristic); and places LLMs behind a **three-tier permission gate** that provably prevents LLM output from becoming adjudication.

v0.4 is therefore a feature-complete **second-order causal decision framework core** — the second-order interaction layer, formal convergence, and LLM guardrails are production-grade. It is not yet a complete multi-tenant enterprise control plane.

## Relationship to v0.3

v0.4 does not replace `IntelligentDecisionHub`; it adds three new layers on top:

```text
IntelligentDecisionHub (v0.4)
├── DecisionService
│   ├── IntelligentDecisionEngine
│   ├── StructuralAuditor
│   ├── Counterfactual Analyzer
│   ├── Robustness Analyzer
│   └── Append-only DecisionRepository
├── Interaction Layer (new · second-order causality)
│   ├── InteractionDeclaration
│   ├── InvalidationClosure + 2nd-order joint effect
│   └── Four invariants: I-1 ~ I-4
├── Convergence Layer (new · formal convergence)
│   ├── ConvergenceChecker (5-state classification)
│   └── Three propositions: P-1 ~ P-3
├── LLM Compliance Layer (new · LLM guardrails)
│   ├── LLMGate (T1/T2/T3 permission tiers)
│   └── Three invariants: L-1 ~ L-3
├── ReconstructionSessionEngine (upgraded · three-layer reconstruction)
│   ├── Forward invalidation
│   ├── Backward root-cause tracing
│   └── Delta reconstruction + human gate
├── Scenario Analyzer
├── CognitiveRiskScanner
├── Information Priority Builder
├── HubReport Integrity Sealer
└── Immutable HubReport Repository Interface
```

All v0.3 APIs and decision request formats remain compatible. When `interaction_declaration` is not supplied, the engine behaves identically to v0.3.

---

## 1. Assumption Interaction Layer (Second-Order Causality)

In v0.3 and earlier, assumption-failure propagation was first-order: each assumption failed independently and affected its own dependent alternatives. In reality, simultaneous failure of multiple assumptions can produce **synergistic effects** (amplification, redundancy, cancellation, and other second-order interactions).

v0.4 introduces an explicitly declared assumption interaction layer: the caller (responsible party) declares the existence and strength of second-order effects, and the engine only validates and composes them.

### Four Invariants

- **I-1 Non-conjectural**: Every interaction strength Δ must be explicitly declared by a responsible party; the engine never estimates or learns Δ.
- **I-2 Order-conservation**: An interaction fires only when **all** member assumptions are simultaneously invalidated; partial failure does not trigger a second-order effect.
- **I-3 Effect-boundedness**: Cumulative interaction effect ≤ `amplification_ceiling × Σ|first-order effect|`; redundant (negative) interactions are not floor-clamped, allowing genuine damping.
- **I-4 Monotonicity**: Augmenting the invalidated set never un-triggers an already-fired interaction (union semantics).

### Three Interaction Types

| Type | Semantics | Effect direction |
|---|---|---|
| `synergy` | Effect amplifies when multiple assumptions fail simultaneously | Positive amplification |
| `redundancy` | Failure of one assumption can be partially compensated by another | Negative damping |
| `amplification` | Failure chain cascades along the dependency direction | Positive amplification (with upper bound) |

### Composition with First-Order Failure

```text
First-order invalidation closure (invalidation_closure)
       │
       ▼
Second-order interaction matching (interaction_declaration + member check + I-2)
       │
       ▼
Interaction-effect accumulation (I-3 upper-bound clamping + I-4 monotonicity)
       │
       ▼
Joint failure result: affected alternatives + adjusted impact score + interaction-trigger audit trail
```

`DecisionRequest` gains an optional `interaction_declaration` field (default `None`, fully backward-compatible). The session engine delegates stop-condition checks to the formal `ConvergenceChecker`.

---

## 2. Formal Convergence Engine

v0.3's reconstruction loop used a heuristic stop condition ("stop when nothing changes"). v0.4 classifies stop conditions into **five deterministic states** via three checkable propositions, and explicitly distinguishes "true convergence" from "budget exhaustion."

### Five Convergence States

| State | Meaning | True convergence? |
|---|---|---|
| `FIXED_POINT` | Candidate set identical to the previous round (P-2 proof) | ✅ Yes |
| `NO_GAIN` | No unresolved branches remain; remaining branches are all `BLOCKED` | ✅ Yes |
| `BUDGET_EXHAUSTED` | Budget ran out before a fixed point was reached | ❌ No |
| `DIVERGED` | Still changing with budget remaining | ❌ No |
| `BLOCKED` | Structural block hit; requires human intervention | ❌ No |

### Three Checkable Propositions

- **P-1 Termination**: Iteration count ≤ `max_iterations`, and new ΔVars produced per iteration do not exceed the declared set → the loop must terminate.
- **P-2 Fixed-point**: `FIXED_POINT` holds if and only if the leading candidate set and failed-assumption set are identical between consecutive rounds. Once a fixed point is reached, no subsequent round changes (monotonicity guarantee).
- **P-3 Effect-boundedness**: The absolute value of the cumulative correction effect ≤ `amplification_ceiling × Σ|initial first-order effect|`; the process does not diverge.

`is_true_convergence()` guards against the classic bug of misclassifying budget exhaustion as convergence. Any caller that reports `BUDGET_EXHAUSTED` as "convergence" violates v0.4's core contract.

---

## 3. LLM Compliance Layer

v0.4 introduces LLM augmentation for the first time, but places it behind **provably non-adjudicating** guardrails. LLMs can annotate, propose, and polish, but can never flip an assumption state, alter an alternative's rank, or produce a final verdict.

### Three Permission Tiers

| Tier | Permission | What it can do | What it cannot do |
|---|---|---|---|
| **T1 Annotation** | Lowest | Add summaries, tags, or structured restatements to existing conclusions | Cannot introduce new judgments; cannot modify state |
| **T2 Proposal** | Medium | Generate candidate ΔVar suggestions, list alternative phrasings, draft questions | Must receive explicit human approval before taking effect |
| **T3 Narrative** | Highest (still restricted) | Generate report bodies, explanatory text, natural-language polish | Structural power is stripped; cannot touch the decision graph |

### Three Invariants

- **L-1 Zone isolation**: Every LLM call must explicitly declare its tier; cross-tier calls are rejected immediately.
- **L-2 No adjudication**: Any LLM output must pass through `LLMGate.strip_structural_power()` before entering the decision graph, removing all fields that could change state, weights, or rankings.
- **L-3 Strength stripping**: Any "strength," "probability," or "confidence" fields generated by the LLM are discarded and are not allowed to influence quantitative computation.

### Provenance Tracking

Every LLM call records: the tier invoked, input hash, output hash, model name, duration, success/failure, and stripping-operation log. All LLM-generated content in the `HubReport` carries an `llm_generated` flag and a `provenance_ref`, and can be independently verified.

---

## 4. Three-Layer Causal Reconstruction (Upgraded)

v0.3's causal reconstruction was one-shot. v0.4 upgrades it into a **bounded, hash-chained, human-gated** iterative process.

Each round runs three causal operators:

1. **Forward invalidation propagation**: `invalidation_closure` propagates a declared assumption failure forward, removing alternatives that lose that assumption's support.
2. **Backward root-cause tracing**: Reverse BFS traces deviation signals back to a candidate set of root-cause assumptions.
3. **Delta reconstruction**: Applies declared correction variables (`DeltaVar`) to a copy of the request, re-runs the deterministic evaluator, and judges convergence of the leading candidate set.

### Design Invariants

- **No guessing**: Every hypothesis is a candidate; a human decides. The engine never auto-loops.
- **Deterministic**: Each round derives exclusively from declared inputs.
- **Auditable**: Each round is hash-linked to the previous one; the whole session forms a `session_root_hash`.
- **Bounded**: Capped by `max_iterations` and `max_evidence_requests`.
- **Human gate**: `advance()` performs exactly one round and then stops at `AWAITING_HUMAN`; only a human decision (`approve` / supply evidence / reject) may move to the next round.

### Three DeltaVar Path Forms

| Form | Example | Effect |
|---|---|---|
| Assumption ID | `"A2"` | Falsify an assumption; propagate along the dependency graph |
| Criterion weight | `"criteria.K1.weight"` | Rewrite the weight of a criterion |
| Alternative metric | `"alternatives.S1.metrics.cost"` | Rewrite a specific metric value of an alternative |

The engine mirrors each declared `DeltaVar` verbatim and never invents correction variables.

---

## 5. Core Request Structure (v0.4 Additions)

v0.3's `HubAnalysisRequest` gains an optional `interaction_declaration` field:

```json
{
  "decision": {
    "objective": "...",
    "decision_owner": {},
    "criteria": [],
    "constraints": [],
    "assumptions": [],
    "alternatives": [],
    "evidence": []
  },
  "scenarios": [
    {
      "id": "SC1",
      "name": "Critical assumption failure",
      "failed_assumption_ids": ["A1"]
    }
  ],
  "interaction_declaration": {
    "interactions": [
      {
        "id": "INT-1",
        "type": "synergy",
        "member_assumption_ids": ["A1", "A2"],
        "effect_delta": 0.3,
        "responsibility": "risk_team",
        "declared_at": "2026-09-01T00:00:00Z"
      }
    ],
    "amplification_ceiling": 2.0
  },
  "run_cognitive_audit": true,
  "llm_zone": "annotation"
}
```

---

## 6. Integrity and Governance (Upgraded)

v0.4 adds the following on top of v0.3's three integrity layers:

1. Event hash chain of a single algorithm execution (retained);
2. `DecisionRecord` parent-hash chain across multiple evaluations/approvals of the same decision (retained);
3. `HubReport.report_hash` aggregating the baseline decision, scenarios, cognitive findings, and information queue (retained);
4. **New**: Reconstruction-session `session_root_hash` — each reconstruction round is hash-linked to the previous, making the whole session verifiable;
5. **New**: Provenance hash chain for LLM calls — input/output/stripping operations of every LLM call are recorded and bound to the corresponding decision event.

Hashes detect content modification, but without external signatures, trusted timestamps, and independent storage, they cannot prove that an entire database was never rewritten wholesale. Production deployments must integrate KMS/HSM and an immutable event store.

---

## 7. Test Coverage

Tests grow from approximately 280 in v0.3 to **402 passing** (122 added) in v0.4:

- `test_interaction.py` — Assumption interaction layer (I-1 ~ I-4 + three interaction types)
- `test_convergence.py` — Formal convergence (5 states + P-1 ~ P-3)
- `test_llm_compliance.py` — LLM compliance layer (T1/T2/T3 + L-1 ~ L-3 + provenance)
- `test_session.py` — Reconstruction session (human gate + hash chain + three DeltaVar forms)
- `test_v04_integration.py` — End-to-end integration (baseline + interaction + reconstruction + LLM annotation)

---

## 8. Production Boundaries

v0.4 is a feature-complete **deterministic decision framework core** — the second-order causal layer, formal convergence, and LLM guardrails are production-grade. It is not yet a complete multi-tenant enterprise control plane.

**Already included (production-grade)**:
- First-order + second-order causal decision kernel
- Formal convergence proofs
- Three-tier LLM permission guardrails
- Hash-chain auditing (decision + session + LLM provenance)
- PostgreSQL persistence option (`SP_DATABASE_DSN`)
- OIDC identity awareness (`SP_OIDC_ISSUER`)
- API key gating + production-mode mandatory verification

**Still required on the production side (outside the framework core scope)**:
- Multi-tenant isolation and tenant routing
- Full RBAC/ABAC model
- KMS/HSM signing and trusted timestamps
- Asynchronous scenario task queues
- Metrics, tracing, and alerting
- Policy registry and canary releases
- Rate limiting and idempotency
- Backups and migrations
- Domain control packs (industry templates)

---

## 9. Explicit Boundaries (Strengthened)

- The Hub never auto-approves a decision;
- The cognitive scan does not diagnose individual psychology;
- Scenarios only use changes explicitly declared by the user;
- Effect strengths for second-order interactions must be declared by a responsible party; the engine never estimates or learns them;
- `BUDGET_EXHAUSTED` is not convergence; any behavior reporting it as "convergence" violates the core contract;
- LLMs never adjudicate: T2 proposals require human approval; T3 narrative is stripped of structural power; no LLM output can flip an assumption state or an alternative's rank;
- There is currently no probabilistic inference, Monte Carlo, or machine-learning prediction;
- The default in-memory repository is unsuitable for multi-instance production;
- Medical, legal, financial, and security decisions remain the responsibility of the corresponding professional responsible parties.
