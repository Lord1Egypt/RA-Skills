# Boundary and Data Classification

Last reviewed: March 17, 2026.

## Why this domain matters

Every PRS assessment starts with scope. If the workload boundary or data classes are unclear, every later conclusion becomes weaker or wrong.

## Review questions

- What exact workload, environment, and deployment boundary is being assessed?
- What data classes are in scope now?
- Is PHI or ePHI explicitly out of scope, planned later, approved, or live?
- Does the deployment model change the answer?
- Are different environments or customer-hosted variants being incorrectly collapsed into one stage?

## Minimum expectations by stage

- PRS-0: boundary is explicit and non-PHI status is documented
- PRS-1: future PHI-oriented scope is defined even though PHI is not approved
- PRS-2: intended PHI use case and data flows are documented
- PRS-3: approved PHI scope is explicit by workload, environment, and data class
- PRS-4: live PHI scope matches the approved scope and is still current

## Strong evidence

- scoped workload description
- environment and deployment-boundary statement
- data classification or data inventory
- architecture and data-flow documentation
- explicit scope approvals

## Common blockers

- ambiguous workload boundary
- no explicit data classification
- one PRS stage used across materially different deployment models
- PHI assumptions inferred from product category instead of evidence

## Recommended next actions

- document the exact workload and deployment boundary under review
- classify current and intended data types explicitly
- split assessments where environments or deployment models differ materially
