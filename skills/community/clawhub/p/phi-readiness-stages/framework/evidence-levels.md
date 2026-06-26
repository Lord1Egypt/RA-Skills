# Evidence Levels

PRS stage assignment is constrained by evidence quality. This document defines the minimum evidence expectations and maximum defensible stage by evidence type.

Read this document together with `framework/evidence-freshness.md` and `framework/minimum-artifact-matrix.md`.

## Evidence categories

| Level | Evidence type | Examples | Maximum defensible stage by itself |
| --- | --- | --- | --- |
| E0 | No usable evidence | vague claims, assumptions, hand-waving | none |
| E1 | Repo or design evidence | code, IaC, configs, architecture docs, issue tracker references | PRS-1 |
| E2 | Process and governance evidence | risk analysis, approved procedures, data-flow docs, restore tests, vendor review records | PRS-2 |
| E3 | Approval and contractual evidence | approval records, signed go-live checklist, signed BAA where required, assigned support ownership | PRS-3 |
| E4 | Live operational evidence | monitoring evidence, alert handling, access reviews, vulnerability and patch records, change logs, reassessment records | PRS-4 |

## Evidence sufficiency rules

- Evidence must be specific to the scoped workload or to a clearly inherited control that is in scope.
- Inherited controls are acceptable only when the inheritance path is explicit and the workload still has documented responsibilities.
- Screenshots, dashboards, and config snippets are supportive but weaker than durable system records.
- Draft policies are weaker than approved policies.
- Future intent does not satisfy a current-stage requirement.

## Stage caps

### PRS-0

Can be assigned when the workload is explicitly out of PHI scope and nothing contradicts that boundary.

### PRS-1

Can be assigned from repo, architecture, and implementation evidence if:

- the workload is intentionally building toward future PHI use
- core technical safeguards are materially implemented
- no approval for PHI exists

### PRS-2

Requires E2 evidence in addition to E1. At minimum:

- risk analysis
- remediation tracking
- approved procedures or policy applicability
- restore test evidence
- vendor review evidence
- assigned operating responsibilities

### PRS-3

Requires E3 evidence in addition to E1 and E2. At minimum:

- recorded internal approval
- explicit approved scope
- go-live readiness sign-off
- required contracts complete where applicable

### PRS-4

Requires E4 evidence in addition to earlier evidence. At minimum:

- proof PHI is live in approved scope
- ongoing control execution evidence
- current periodic evaluation evidence
- reassessment after material change where applicable

## Confidence guidance

Confidence should be reduced when:

- evidence is indirect
- evidence is stale
- only one side of an inherited control is documented
- organizational role under HIPAA is uncertain
- scope is ambiguous
- live verification of official sources was not performed

Recommended confidence bands:

- high: required evidence is direct, current, and complete for the assigned stage
- medium: assigned stage is supported, but some evidence is indirect or slightly stale
- low: stage is provisional because scope, evidence, or role is materially incomplete
