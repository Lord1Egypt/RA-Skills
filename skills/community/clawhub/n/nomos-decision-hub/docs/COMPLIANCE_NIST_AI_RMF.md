# NIST AI Risk Management Framework (AI RMF 1.0) Mapping — NOMOS Intelligent Decision Hub

> This document maps NOMOS's architecture and capabilities to the NIST AI Risk Management Framework (AI RMF 1.0) functions: Govern, Map, Measure, Manage.
> **This is a draft framework; final commercial use requires legal counsel review.**

## Overview

NOMOS is a deterministic, auditable decision hub. Its design principles — no guessing, deterministic execution, human-gated approval, hash-chained audit — are inherently aligned with AI RMF's core functions. The mapping below cross-references each AI RMF sub-function to a concrete NOMOS capability.

---

## GOVERN1 — Govern

| NIST AI RMF Ref | Function | NOMOS Mapping |
|-----------------|----------|---------------|
| G1.1 | Establish organisational AI policy | `LICENSE` defines tiered authorisation; commercial deployment requires written paid authorisation |
| G1.2 | Assign accountability and roles | `decision_owner` field in `HubAnalysisRequest`; approval recorded via `governance/approval.py` |
| G1.3 | Establish AI risk tolerances | `policy.py` configurable guardrails for the deterministic engine |
| G1.4 | Cultivate an AI risk culture | Shanghai / EU / PDPA compliance docs; provider self-assessment against the IMDA AI Verify framework: 95/100 |
| G1.5 | Establish AI system lifecycle process | Production boundaries documented in `README` (v0.4 roadmap) |
| G1.6 | Train workforce | Compliance docs and `docs/INTELLIGENT_DECISION_HUB_V0_4.md` |
| G1.7 | Implement a process for AI risks and impacts | `CognitiveRiskScanner` + `InformationPriorityBuilder` |
| G2.0 | Govern AI system: legal & regulatory | `COMPLIANCE_SHANGHAI.md`, `COMPLIANCE_EU_AI_ACT.md`, `PRIVACY_POLICY_*`, `DATA_PROCESSING_AGREEMENT_*` |
| G3.0 | Govern AI system: operational | Production refuses boot without `SP_API_KEY`; OIDC-aware identity |

---

## MAP — Map

| NIST AI RMF Ref | Function | NOMOS Mapping |
|-----------------|----------|---------------|
| M1.1 | Categorise AI system | NOMOS is a deterministic decision-support tool — not a GPAI, not generative AI |
| M1.2 | Map to context & related laws | Compliance docs cover PRC, EU (AI Act), Singapore (PDPA/IMDA) |
| M2.1 | Identify users & affected parties | `decision_owner` and stakeholder fields in request schema |
| M2.2 | Identify scope, boundary, assumptions | `assumptions` array declared explicitly; each assumption has responsibility node |
| M3.1 | Identify and prioritise risks | `CognitiveRiskScanner` detects weight concentration, ranking fragility, evidence concentration |
| M3.2 | Document risks and responses | `AlgorithmAuditEvent` records every evaluation; `HubReport` seals the full analysis |

---

## MEASURE — Measure

| NIST AI RMF Ref | Function | NOMOS Mapping |
|-----------------|----------|---------------|
| ME1.1 | Identify appropriate metrics | Deterministic scores, counterfactual leader stability, Pareto exposure, weight sensitivity |
| ME1.2 | Establish measurement processes | `RobustnessAnalyzer` computes Pareto + weight perturbations; `counterfactual.py` re-selects candidates |
| ME1.3 | Collect, compute, document metrics | Every stage emits `AlgorithmAuditEvent` with explicit operands and outputs |
| ME2.1 | Categorise and measure AI trustworthiness | NOMOS design tenets: Valid & Reliable (deterministic), Safe (no autonomous decisions), Secure (hash-chained audit), Resilient (bounded reconstruction), Accountable (human gate), Transparent (full replay), Explainable (audit trail), Privacy-Enhanced (local, minimal), Fair (no bias proxy) |
| ME2.2 | Evaluate metrics | `StructuralAuditor` runs pre-evaluation audit; issues recorded with severity |
| ME3.1 | Measure and manage data risk | `audit/integrity.py` SHA-256 fingerprint; `StructuralAuditor` flags missing data; `InformationPriorityBuilder` ranks gaps |
| ME4.1 | Monitor, measure, track performance | Production can enable PostgreSQL persistence (`SP_DATABASE_DSN`); audit ledger is append-only |

---

## MANAGE — Manage

| NIST AI RMF Ref | Function | NOMOS Mapping |
|-----------------|----------|---------------|
| M1.1 | Use mapped risks to manage | `ReconstructionSessionEngine.advance()` runs one round then stops at `AWAITING_HUMAN`; only human decision advances |
| M1.2 | Manage AI system throughout lifecycle | `DecisionRecord` parent-hash chain records every evaluation/approval; `HubReport.report_hash` provides integrity |
| M1.3 | Manage third-party / supply chain | `LICENSE` dual-entity model; commercial authorisation required before deployment |
| M1.4 | Document and monitor risks | `algorithm_audit_root_hash` provides tamper-evident verification; `report_hash` seals the analysis |
| M2.1 | Respond to AI incidents | Audit ledger supports root-cause tracing; `causal.py` performs backward root-cause BFS |
| M2.2 | Contribute to AI incident sharing | `liability_report.json` demonstrates incident-attribution capability |

---

## Trustworthy AI Characteristics (Cross-Cutting)

| Characteristic | NOMOS Evidence |
|----------------|---------------|
| Valid and Reliable | Deterministic: same input → same output; no RNG, no ML |
| Safe | No autonomous final decision; human always approves |
| Secure and Resilient | Hash-chained audit ledger; bounded iteration (`max_iterations`) |
| Accountable and Transparent | `decision_owner` + responsibility nodes; full execution replay |
| Explainable | `AlgorithmAuditEvent` exposes every operand and output |
| Privacy-Enhanced | Local default; data minimisation; no telemetry |
| Fair | No profiling; deterministic scoring; no opaque proxies |

---

## Implementation Notes

NOMOS provides the **technical controls** that satisfy most AI RMF Measure and Manage sub-functions. The **Govern** and some **Map** sub-functions require the deploying organisation to establish policy, roles, training, and legal review — supported but not replaced by NOMOS documentation.

For enterprise deployment, refer to the v0.4 roadmap in `docs/INTELLIGENT_DECISION_HUB_V0_4.md` for: PostgreSQL event store, OIDC/RBAC/ABAC, KMS/HSM signing, rate limiting, observability, backups, migrations, and domain control packs.

---

## Final Review

This mapping is a draft framework. Before commercial deployment, it must be reviewed by legal counsel and the deploying organisation's AI risk function against the latest NIST AI RMF publication and supplementary guidance.
