# Access Control

Last reviewed: March 17, 2026.

Primary authority pointers:

- HIPAA Security Rule technical safeguards
- HIPAA Security Rule access control standard
- HHS Security Rule overview and safeguards pages

## Why this domain matters

Access control is a stage-gating domain from PRS-1 onward. A workload cannot credibly claim PHI-oriented security alignment without workload-level identity and authorization controls.

## Review questions

- Are users and services uniquely identifiable where required by the architecture?
- Is least privilege defined at the workload boundary?
- Are privileged access paths controlled?
- Are access changes, revocations, and emergency paths defined?
- Is there an access-review mechanism for live operation?

## Minimum expectations by stage

- PRS-1: authentication and authorization model materially implemented
- PRS-2: operating responsibility for access management documented
- PRS-3: go-live access model approved for scoped PHI use
- PRS-4: access review evidence exists and is current

## Strong evidence

- identity-provider configuration
- RBAC or policy configuration
- service-account controls
- access-review records
- joiner, mover, leaver procedure references

## Common blockers

- shared credentials
- excessive admin access
- undocumented service-to-service trust
- no access review evidence for live operation

## Recommended next actions

- define and document workload-level access roles
- remove shared credentials and unmanaged secrets
- retain periodic access-review artifacts
