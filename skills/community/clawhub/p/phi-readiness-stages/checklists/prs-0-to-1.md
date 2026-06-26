# Checklist: PRS-0 to PRS-1

Goal: confirm that a non-PHI workload is intentionally being built toward future PHI suitability without overstating readiness.

## Required checks

- workload boundary is defined
- owner is assigned
- target environment is identified
- expected data classes are identified
- future PHI-readiness intent is explicit
- identity and access controls are materially implemented
- encryption in transit is materially implemented
- at-rest encryption approach is in place or clearly inherited
- audit logging exists
- secrets management exists
- environment separation exists
- build and deployment path is controlled
- vulnerability management path exists
- backup and restore approach exists
- incident reporting path is identified
- vendor inventory has started
- PHI is still not approved in scope

## Common blockers

- strong infrastructure claims without workload-level controls
- missing owner or missing boundary
- no logging, secrets, or deployment controls
- no documented intent to pursue PHI handling

## Minimum evidence

- architecture or system diagram
- repo or configuration evidence for safeguards
- issue tracker or notes showing known gaps
- scoped statement that PHI is not yet approved
