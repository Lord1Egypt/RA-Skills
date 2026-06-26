# Minimum Artifact Matrix

Use this matrix to standardize what evidence must exist before a stage is defensible. These are minimum PRS artifacts, not a complete compliance inventory.

## PRS-0

Minimum artifacts:

- scoped workload description
- environment and deployment boundary
- owner assignment
- explicit non-PHI statement or data-boundary statement
- identified expected data classes

Acceptable alternatives:

- architecture note plus issue tracker record
- design document plus explicit scope statement

## PRS-1

Minimum artifacts:

- architecture or system-boundary diagram
- access-control design or configuration evidence
- encryption and secrets-management evidence
- audit-logging evidence
- environment-separation evidence
- build and deployment control evidence
- vulnerability-management path
- backup and restore approach
- incident-reporting path
- vendor inventory
- tracked known gaps

Acceptable alternatives:

- IaC, configuration, or managed-platform evidence may replace prose documents if the control is clear

## PRS-2

Minimum artifacts:

- scoped risk analysis
- remediation tracker or approved exception record
- approved applicable procedures or policy applicability record
- system and data-flow documentation
- retention and deletion approach
- incident-response procedure
- contingency procedure
- restore-test evidence
- vendor and subprocessor review record
- operating ownership matrix
- workforce readiness plan or completed prerequisite training record

Acceptable alternatives:

- one review package may satisfy multiple rows if it is explicit and current

## PRS-3

Minimum artifacts:

- recorded internal approval decision
- approved scope statement
- environment-specific go-live checklist
- signed or completed required contract artifacts, including BAAs where required
- monitoring and escalation enablement evidence
- support ownership record
- completed go-live training evidence where required

Acceptable alternatives:

- approval workflow records are acceptable if durable and auditable

## PRS-4

Minimum artifacts:

- evidence that PHI is live in approved scope
- recent access-review evidence
- recent monitoring or alert-handling evidence
- recent vulnerability and patch evidence
- recent change-control evidence
- current incident-readiness evidence
- current backup and restore confidence evidence
- current vendor reassessment record
- periodic technical and non-technical evaluation record
- evidence-retention index or equivalent record location map

Acceptable alternatives:

- operational dashboards may support but should not replace durable records

## Consistency rule

If the minimum artifact set for a candidate stage is not materially present, do not assign that stage even if technical implementation appears strong.
