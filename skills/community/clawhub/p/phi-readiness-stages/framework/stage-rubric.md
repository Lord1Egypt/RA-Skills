# Stage Rubric

Use this rubric to assign the highest defensible PRS stage. A stage is available only if every required domain for that stage is sufficiently satisfied and evidenced.

Read this rubric with `framework/minimum-artifact-matrix.md` and `framework/evidence-freshness.md`.

## Required domains by stage

| Domain | PRS-0 | PRS-1 | PRS-2 | PRS-3 | PRS-4 |
| --- | --- | --- | --- | --- | --- |
| Scoped boundary and data classification | required | required | required | required | required |
| Security architecture and access control | not required | required | required | required | required |
| Audit logging and monitoring foundations | not required | required | required | required | required |
| Encryption and secrets handling | not required | required | required | required | required |
| Backup, restore, and contingency planning | not required | required in approach form | required with testing | required | required with ongoing evidence |
| Vulnerability and change control | not required | required foundationally | required | required | required with ongoing evidence |
| Risk analysis and remediation tracking | not required | not required | required | required | required with refresh cycle |
| Policies, procedures, and operating roles | not required | foundationally required | required | required | required with maintenance |
| Workforce readiness | not required | baseline expectations documented | required for approval path | required for go-live | required with recurrence where applicable |
| Vendor and subprocessor review | not required | inventory started | required | required including contracts where applicable | required with reassessment |
| Approval and contractual prerequisites | not required | not required | not required | required | required |
| Live operational evidence | not required | not required | not required | not required | required |
| Periodic evaluation and reassessment | not required | not required | review plan expected | approval plan expected | required |
| Physical safeguards or inherited physical controls | not required | baseline applicability noted | required where applicable | required where applicable | required with operating evidence where applicable |

## Stage minimums

### PRS-0

Minimum condition:

- the workload is clearly out of PHI scope and restricted to non-PHI data within the defined boundary

Blockers to advancement:

- no assigned owner
- no identified boundary
- unclear data classes

### PRS-1

Minimum condition:

- the workload is intentionally being built toward future PHI suitability
- core technical safeguards are materially implemented
- foundational governance prerequisites exist
- no real PHI is approved

Typical evidence:

- architecture and environment documentation
- infrastructure as code or configuration showing access, encryption, logging, and segmentation patterns
- CI/CD and secrets management configuration
- issue tracker or risk backlog showing known gaps

### PRS-2

Minimum condition:

- major technical safeguards are in place
- non-technical readiness is materially complete
- risk analysis exists
- operating roles, procedures, and vendor review are complete enough for approval review
- the workload is still not approved or live with PHI

Typical evidence:

- risk analysis artifact
- remediation plan and tracked exceptions
- approved policies and procedures
- data-flow diagram
- restore-test record
- vendor review records

### PRS-3

Minimum condition:

- the workload passed internal approval for PHI use in defined scope
- required contracts are complete where applicable
- go-live readiness is signed off
- monitoring and escalation paths are active before cutover
- PHI is not yet live

Typical evidence:

- approval memo or workflow record
- signed BAA or equivalent contractual artifact where required
- go-live checklist
- ownership roster

### PRS-4

Minimum condition:

- PHI is live in approved scope
- operational controls are active and evidenced on an ongoing basis
- periodic technical and non-technical evaluation is active
- evidence is current enough to defend the assigned stage

Typical evidence:

- production monitoring and alert evidence
- access review records
- vulnerability and patch records
- incident-response exercises or readiness artifacts
- backup and restore evidence
- reassessment records after material change
