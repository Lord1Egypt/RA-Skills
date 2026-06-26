# Evidence Freshness Policy

HIPAA often requires periodic review but does not prescribe one universal recency window for every artifact. This document defines PRS default freshness expectations so assessments are consistent when no stricter internal cadence is provided.

These are PRS policy defaults, not statements of legal deadlines unless the underlying law explicitly sets a deadline.

## Freshness states

- current: within the PRS default window or the organization's stricter approved cadence
- aging: outside the preferred window but still informative
- stale: too old to support the assigned stage without strong compensating evidence
- invalidated: materially superseded by architecture, scope, vendor, or ownership change

## Default freshness windows

| Artifact or evidence type | PRS default window | Notes |
| --- | --- | --- |
| Risk analysis | 12 months and after material change | required refresh trigger for PRS-4 confidence |
| Risk remediation tracker | current open-state view | a stale point-in-time export is weak evidence |
| Data-flow documentation | 12 months and after material change | invalidate earlier if architecture changed |
| Restore test evidence | 12 months for PRS-2 or PRS-3; 6-12 months for PRS-4 based on criticality | use stricter internal policy if it exists |
| Access review evidence | 90 days for privileged or production PHI access unless a justified approved cadence exists | older evidence lowers PRS-4 confidence |
| Monitoring and alert-response evidence | 90 days | should show real operation, not just configured tooling |
| Vulnerability-management evidence | current cycle plus status of critical findings | unresolved severe findings may block stage confidence |
| Patch-management evidence | current cycle and recent execution proof | use approved internal cadence if stricter |
| Vendor review and shared-responsibility analysis | 12 months and after material vendor or scope change | includes subprocessor changes |
| Workforce training or readiness evidence | 12 months or role/onboarding change | go-live training must be current at PRS-3 |
| Incident-response exercise or readiness artifact | 12 months and after major organizational or architecture change | actual incidents may also serve as evidence |
| Go-live approval package | tied to the actual cutover window | stale approval should not carry indefinitely |
| Periodic technical and non-technical evaluation | 12 months and after material change | core PRS-4 maintenance evidence |

## Material change triggers

Treat evidence as invalidated or in need of refresh when:

- production architecture changed materially
- a major vendor or subprocessor changed
- PHI scope expanded
- authentication or logging architecture changed
- operational ownership changed
- a significant incident exposed control weakness

## Freshness rule for stage assignment

- Aging evidence can support historical context.
- Stale or invalidated evidence cannot, by itself, support the current assigned stage.
- If a stage depends on stale evidence, reduce confidence or downgrade the stage until fresh evidence exists.
