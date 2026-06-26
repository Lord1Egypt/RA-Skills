# Integrity

Last reviewed: March 17, 2026.

Primary authority pointers:

- HIPAA Security Rule integrity standard
- HHS Security Rule guidance

## Why this domain matters

Integrity controls help establish that ePHI is not improperly altered or destroyed. In PRS, this domain affects design credibility, change control, and operational confidence.

## Review questions

- What protects sensitive records from unauthorized modification?
- Are change paths controlled and auditable?
- Are integrity checks, validation, or transaction safeguards used where needed?
- Can the team detect or reconstruct unintended changes?

## Minimum expectations by stage

- PRS-1: integrity protections are part of the design or documented as required controls
- PRS-2: data-flow and operational procedures account for integrity-sensitive paths
- PRS-3: approved go-live scope includes integrity-relevant operational controls
- PRS-4: change and incident evidence supports ongoing integrity assurance

## Strong evidence

- application validation controls
- database protections and audit trails
- deployment approvals
- immutable log or version-history patterns

## Common blockers

- uncontrolled direct database changes
- no auditable change process
- weak validation on sensitive write paths

## Recommended next actions

- document integrity-sensitive components and change paths
- require auditable approvals for sensitive modifications
- retain incident and change artifacts tied to integrity-impacting events
