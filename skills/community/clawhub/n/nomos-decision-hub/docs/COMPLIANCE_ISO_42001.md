# ISO/IEC 42001:2023 (AI Management System) Alignment — NOMOS Intelligent Decision Hub

> This document maps NOMOS's architecture and the NOMOS compliance document set to the ISO/IEC 42001:2023 standard for Artificial Intelligence Management Systems (AIMS).
> **This is a draft framework; formal certification requires accredited third-party audit.**

## 1. Scope and Applicability

NOMOS is a deterministic decision-support and algorithmic-audit engine. It can serve as a **technical control component** within an organisation's AI Management System (AIMS). NOMOS itself does not constitute a complete AIMS; the deploying organisation must implement the management-system layer (policy, roles, objectives, internal audit, management review).

## 2. Clause-by-Clause Mapping

### Clause 4 — Context of the Organisation

| ISO/IEC 42001 | NOMOS Alignment |
|---------------|-----------------|
| 4.1 Understanding the organisation | Compliance docs cover PRC, EU, Singapore jurisdictions |
| 4.2 Needs of interested parties | `LICENSE` dual-entity; commercial users require paid authorisation |
| 4.3 AIMS scope | NOMOS scope: decision evaluation, causal audit, governance — documented in `docs/INTELLIGENT_DECISION_HUB_V0_4.md` |
| 4.4 AIMS processes | Deterministic engine + human approval gate + audit ledger |

### Clause 5 — Leadership

| ISO/IEC 42001 | NOMOS Alignment |
|---------------|-----------------|
| 5.1 Leadership commitment | `decision_owner` field assigns accountable party per request |
| 5.2 AI policy | `policy.py` configurable guardrails; compliance doc set |
| 5.3 Roles & responsibilities | `governance/approval.py` records human approver; responsibility nodes on assumptions |

### Clause 6 — Planning

| ISO/IEC 42001 | NOMOS Alignment |
|---------------|-----------------|
| 6.1 Risk & opportunity actions | `CognitiveRiskScanner` + `ReconstructionSessionEngine` (bounded, human-gated) |
| 6.2 AI objectives | Deterministic, auditable, human-gated design invariants |
| 6.3 Changes to AIMS | v0.4 roadmap documents planned control-plane upgrades |

### Clause 7 — Support

| ISO/IEC 42001 | NOMOS Alignment |
|---------------|-----------------|
| 7.2 Competence | Compliance docs + `docs/INTELLIGENT_DECISION_HUB_V0_4.md` |
| 7.3 Awareness | Deployment docs; production refuses keyless boot |
| 7.4 Communication | `HubReport` transparent outputs; `InformationPriorityBuilder` |
| 7.5 Documented information | Hash-chained audit ledger; `HubReport.report_hash` |

### Clause 8 — Operation

| ISO/IEC 42001 | NOMOS Alignment |
|---------------|-----------------|
| 8.1 Operational planning | Deterministic execution; declared inputs only |
| 8.2 AI risk treatment | `policy.py` guardrails; `StructuralAuditor` pre-evaluation audit |
| 8.3 AI system impact assessment | `liability_report.json` demonstrates impact-attribution (HUMAN_APPROVAL_REQUIRED) |
| 8.4 AI system lifecycle | Production boundaries + v0.4 roadmap |
| 8.5 Data management | `StructuralAuditor` completeness check; `InformationPriorityBuilder` gap ranking |
| 8.6 Third-party relationships | `LICENSE` commercial authorisation; `DATA_PROCESSING_AGREEMENT_*` |

### Clause 9 — Performance Evaluation

| ISO/IEC 42001 | NOMOS Alignment |
|---------------|-----------------|
| 9.1 Monitoring & measurement | `RobustnessAnalyzer` (Pareto, weight sensitivity); `algorithm_audit_verified` flag |
| 9.2 Internal audit | Audit ledger provides tamper-evident evidence |
| 9.3 Management review | `HubReport` sealed snapshot for review |

### Clause 10 — Improvement

| ISO/IEC 42001 | NOMOS Alignment |
|---------------|-----------------|
| 10.1 Nonconformity & corrective | `StructuralAuditor` issues recorded with severity and recommendations |
| 10.2 Continual improvement | Iterative reconstruction `session_root_hash`; v0.4 roadmap |

## 3. Annex A / Annex B Controls

ISO/IEC 42001 Annex A lists AI-specific controls; Annex B maps ISO/IEC 27001 controls. Relevant NOMOS-aligned controls include:

| Control Area | NOMOS Capability |
|--------------|------------------|
| A.1 AI policy & governance | Compliance doc set; `LICENSE` tiered authorisation |
| A.2 Internal organisation | `decision_owner`; `governance/approval.py` |
| A.3 Resource for AI | OIDC identity; PostgreSQL persistence (configurable) |
| A.4 AI risk management process | `CognitiveRiskScanner`; `RobustnessAnalyzer` |
| A.5 Impact assessment | `liability_report.json`; `HubReport` |
| A.6 AI system lifecycle | Deterministic engine + human gate + v0.4 roadmap |
| A.7 Data management | `StructuralAuditor`; `InformationPriorityBuilder` |
| A.8 Third-party | `LICENSE`; DPA docs |
| A.9 Transparency & explainability | `AlgorithmAuditEvent`; full replay |
| A.10 Controllability | `HUMAN_APPROVAL_REQUIRED` gate; `AWAITING_HUMAN` session state |

## 4. Certification Path

| Step | Actor | Output |
|------|-------|--------|
| 1. AIMS scoping | Deploying org | Define AIMS scope and objectives |
| 2. Gap assessment | Deploying org + auditor | Compare org AIMS to ISO/IEC 42001 |
| 3. NOMOS integration | Deploying org | Deploy NOMOS as technical control layer |
| 4. Internal audit | Deploying org | Use NOMOS audit ledger as evidence |
| 5. Management review | Deploying org | Review `HubReport` snapshots |
| 6. Certification audit | Accredited body | ISO/IEC 42001 certificate |

## 5. Limitations

NOMOS provides technical controls but **not** the full management-system layer required for ISO/IEC 42001 certification. The deploying organisation is responsible for:
- AI policy and leadership commitment (Clauses 5);
- Competence and training programmes (7.2);
- Internal audit and management review cadence (9.2, 9.3);
- Nonconformity handling and continual improvement governance (10).

## 6. Final Review

This alignment document is a draft framework. Formal ISO/IEC 42001 certification requires engagement with an accredited certification body and a full AIMS implementation by the deploying organisation.
