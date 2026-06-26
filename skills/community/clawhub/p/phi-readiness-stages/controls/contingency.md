# Contingency

Last reviewed: March 17, 2026.

Primary authority pointers:

- HIPAA Security Rule contingency plan standard
- HHS risk analysis and contingency guidance

## Why this domain matters

Contingency planning becomes stage-gating before approval. A backup strategy without restore confidence is not enough for PRS-2 or higher.

## Review questions

- Is there a defined backup approach for the scoped workload?
- Has restore capability been tested?
- Are disaster recovery and emergency-mode expectations documented?
- Are dependencies and recovery owners known?

## Minimum expectations by stage

- PRS-1: backup and restore approach is defined
- PRS-2: contingency procedures are documented and restore testing is completed
- PRS-3: go-live approval includes contingency ownership
- PRS-4: restore confidence is maintained through current evidence

## Strong evidence

- backup design
- restore test report
- recovery procedure
- emergency-mode operating procedure

## Common blockers

- backup exists but restore has never been tested
- recovery objectives are implicit only
- recovery ownership is unclear

## Recommended next actions

- run and retain restore tests
- assign recovery ownership explicitly
- connect contingency procedures to actual dependencies
