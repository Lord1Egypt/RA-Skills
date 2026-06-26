# PHI Readiness Stages (PRS) Specification

Framework version: `PRS Framework v1.1`

This document is the normative specification for assigning and reviewing PHI Readiness Stages (PRS).

## 1. Normative baseline

PRS is a HIPAA-informed workload framework. It is not a restatement of law.

Its mandatory baseline is the currently effective HIPAA Security Rule, interpreted through official HHS/OCR guidance and supported by NIST SP 800-66 Rev. 2 as an implementation guide. Proposed rules, including the December 27, 2024 NPRM, are tracked separately and do not change stage requirements until finalized.

PRS does not, by itself, determine full Privacy Rule, Breach Notification Rule, FTC, or state-law compliance. Those boundaries must be called out separately where relevant.

## 2. Purpose

PRS describes the lifecycle status of a workload that may eventually handle PHI. It exists to stop premature or ambiguous claims such as:

- `we are HIPAA compliant`
- `we could handle PHI if needed`
- `we run on secure cloud infrastructure so we are ready`

PRS provides a narrower and more defensible status model.

## 3. Scope

PRS applies per:

- workload
- product boundary
- environment
- deployment boundary

Every assignment must identify:

- system or workload name
- environment
- owner
- assessment date
- approver or reviewer
- evidence location
- next review date

## 4. Canonical stages

### PRS-0 Non-PHI

Definition:

The workload is explicitly restricted to non-PHI within the defined scope. This may be a prototype, demo, internal tool, or a mature workload intentionally kept out of PHI scope.

Entry criteria:

- scope is defined
- boundary is explicitly non-PHI only
- no approval exists for live PHI in scope

Exit criteria:

- owner is assigned
- expected data classes are identified
- intended environment is identified
- non-PHI-only status is documented
- if advancement is desired, intent to pursue PHI readiness is recorded

### PRS-1 Security-Aligned

Definition:

The workload is being built using security patterns appropriate for future PHI use, but it is not approved to handle PHI.

Entry criteria:

- PRS-0 exit criteria are met
- future PHI-readiness pursuit is explicit
- system boundary, owner, target environment, and data classes are defined
- baseline technical safeguards are materially implemented or enforced for the target workload:
  - identity and access control
  - encryption in transit
  - encryption at rest or documented compensating control where applicable
  - audit logging
  - secrets management
  - backup and restore approach
  - environment separation
  - secure build and deployment path
  - vulnerability management
- foundational governance prerequisites exist:
  - owner assigned
  - incident reporting path identified
  - baseline data-handling expectations documented
  - vendor inventory started
- real PHI is not approved in scope

Exit criteria:

- intended PHI use case and scope are defined
- major readiness gaps are known and tracked
- the workload is ready for full PHI-readiness review

### PRS-2 PHI-Ready

Definition:

Technical and process readiness is substantially complete, but formal approval for live PHI use is not yet complete.

Entry criteria:

- PRS-1 exit criteria are met
- risk analysis is completed for the scoped workload
- identified gaps have remediation plans, accepted residual risk, or approved tracked exceptions
- required policies and procedures applicable to the workload are approved
- system and data-flow documentation is complete
- retention and deletion approach is defined
- incident response and contingency procedures are documented
- restore testing is completed
- vendor and subprocessor review is completed for in-scope services
- operating responsibilities are assigned
- workforce training expectations are defined, and in-scope operators are scheduled or completed where required before approval

Exit criteria:

- approval package is complete for internal decision
- remaining issues are limited to approval-dependent items or accepted residual risk
- no unresolved blocker remains in a required domain

### PRS-3 PHI-Approved

Definition:

The workload has explicit internal approval for PHI use in defined scope, but it is not yet live with PHI.

Entry criteria:

- PRS-2 exit criteria are met
- internal security, compliance, legal, and business approvals are recorded as required by the organization
- approved scope is explicit:
  - workload or product boundary
  - environment
  - data classes
  - approved use case
  - customer or internal program scope where relevant
- contractual prerequisites are complete where required, including BAAs for in-scope relationships
- support ownership is assigned
- go-live checklist is signed
- monitoring, alerting, and escalation paths are enabled before cutover
- in-scope workforce training required for go-live is completed

Exit criteria:

- approved production cutover is executed
- PHI is actually received, transmitted, processed, or stored in the approved scope

### PRS-4 PHI-Operational

Definition:

The workload is live with PHI in approved scope, and ongoing operational controls are active and evidenced.

Entry criteria:

- PRS-3 exit criteria are met
- PHI is actually live in scoped operation
- live-control evidence is being retained

Maintenance criteria:

To remain at PRS-4, the workload must maintain evidence for:

- access review
- monitoring and alert response
- vulnerability and patch management
- change control
- incident handling readiness
- backup and restore confidence
- vendor reassessment
- periodic technical and non-technical evaluation
- re-evaluation after material change
- evidence retention for internal or external review

## 5. Stage assignment rules

### 5.1 Core rule

A stage cannot exceed the minimum satisfied criteria across all required domains for that stage.

### 5.2 Scope rule

Every statement must be scoped to:

- what workload
- what environment
- what data
- what usage boundary

### 5.3 Evidence rule

Missing evidence is a blocker. Evidence quality constrains the maximum defensible stage.

### 5.4 Overclaiming rule

Repo-only review may support PRS-0 or PRS-1 findings. It cannot establish PRS-3 or PRS-4. PRS-2 requires non-code process evidence; PRS-3 requires approval and contractual evidence; PRS-4 requires live operational evidence.

### 5.5 Downgrade rule

A workload must be reassessed and may be downgraded when:

- required evidence expires
- scope materially changes
- a critical control stops operating
- ownership becomes unclear
- vendor or architecture changes invalidate earlier assumptions

## 6. Public-language rule

Do not use `HIPAA compliant`, `HIPAA certified`, or `HIPAA secure` as PRS stages or public stage labels. If `HIPAA` is mentioned publicly, scope the statement to a specific workload, environment, and deployment context.

## 7. Companion documents

This specification is complemented by:

- `framework/stage-rubric.md`
- `framework/applicability-role-matrix.md`
- `framework/evidence-levels.md`
- `framework/evidence-freshness.md`
- `framework/minimum-artifact-matrix.md`
- `framework/regulatory-boundaries.md`
- `controls/`
- `mappings/`
- `references/source-registry.md`
