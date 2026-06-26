# Post-Creation Materialization Checklist (Mandatory)

After creating team agents, do not stop at registration/binding. Materialize role files.

## 1) Required files per role workspace
- `SOUL.md` (role mission, responsibilities, boundaries, quality bar)
- `AGENTS.md` (team directory, delegation protocol, return-path rule, escalation)
- `IDENTITY.md` (localized role display name + one-line value proposition)
- `USER.md` (can be minimal placeholder)

## 2) Minimum content checks
For each role, verify:
- responsibilities section exists
- deliverables section exists
- boundaries section exists
- collaboration protocol reference exists
- upstream/downstream or escalation mapping exists

## 3) Team-level checks
- `team-leader` exists and is single intake role
- risk override policy documented (HIGH/EXTREME requires explicit confirmation)
- team shared directory exists: `/workspace-<team>/shared/`
- no-raw-bulk-output rule is documented for all roles
- team-leader boundary documented (orchestrate only, no specialist implementation)

## 4) Completion gate
Creation is NOT complete until all role files pass checks.
If any role fails, return status `partially_ready` with missing items list.

Additional gate before declaring ready:
- team-leader boundary clause exists in SOUL/AGENTS
- shared path policy exists in all role docs
- report template includes stage deliverables + shared paths
