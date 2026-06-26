# PRS Agent Instructions

Use this repository when asked to assess a system, workload, repository, environment, or product for its current PHI Readiness Stage (PRS), its blocking gaps, or the next actions required to advance safely.

## Required startup sequence

1. Read `skills/phi-readiness-review/SKILL.md`.
2. Read `framework/assessment-rules.md`.
3. Read `framework/applicability-role-matrix.md`.
4. Read `framework/stage-rubric.md`.
5. Read `framework/evidence-levels.md`.
6. Read `framework/evidence-freshness.md`.
7. Read `framework/minimum-artifact-matrix.md`.
8. Read `framework/regulatory-boundaries.md`.
9. Verify live official sources from `references/source-registry.md` before making any statement about current HIPAA rules, guidance, or enforcement posture.
10. When apps, APIs, mobile devices, or wearables are in scope, read the matching scenario references under `skills/phi-readiness-review/references/`.

## Hard rules

- Treat PRS as a workload status framework, not a legal determination.
- Do not use `HIPAA compliant`, `HIPAA certified`, or `HIPAA secure` as stage labels or as shorthand for any PRS stage.
- Scope every conclusion to a specific workload, environment, data boundary, and usage boundary.
- Separate current law from proposed changes.
- Separate Security Rule stage logic from Privacy Rule, Breach Notification Rule, and state-law questions.
- Distinguish observed evidence from inference.
- Missing evidence is a blocker, not an invitation to assume a pass.
- If the only evidence is code or repo content, do not assign PRS-3 or PRS-4.
- If approval records, contracts, or live operational evidence are absent, cap the stage accordingly.
- If inherited controls are claimed, require a documented shared-responsibility path.
- If evidence is stale or invalidated by material change, reduce confidence or downgrade the stage.

## Required assessment outputs

Every assessment must include:

- scoped system description
- HIPAA applicability and role assessment
- evidence reviewed and evidence gaps
- evidence freshness assessment
- official sources verified live with access date
- current PRS stage with confidence
- stage blockers by domain
- recommended next actions ordered by priority
- regulatory boundary note for Privacy Rule, Breach Notification Rule, state law, or other adjacent review when relevant
- exact caveats against overstating regulatory status

Use `framework/output-contract.md` for the required structure.
