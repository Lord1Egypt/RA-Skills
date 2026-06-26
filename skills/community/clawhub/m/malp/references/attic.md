# M*A*L*P Attic

## Table of contents

- [Intent](#intent)
- [Default posture](#default-posture)
- [Suggested shapes](#suggested-shapes)
- [Project-local naming](#project-local-naming)
- [Guidance](#guidance)

Use `~/.malp-home/attic/` as cold storage for malp material that should not load into normal working context.

## Intent

The attic is for old probes, not active operations.

The defining property is not just retirement. It is context temperature:
- active malps may be discovered and opened during normal malp work
- attic material must stay out of normal context unless the user explicitly asks for attic, archived, or retired malps

Use it when:
- a malp is retired from active use
- the user wants to keep historical notes without leaving the malp in the main active list
- a parent malp has become transitional and should step aside while deeper active malps remain in service
- the user wants to preserve context before deleting or heavily pruning a malp

Do not treat the attic as an active workspace. If the user starts working there again, recommend promoting the relevant material back into an active `.malp`.

## Default posture

- `~/.malp-home/MAP.txt` is for active malps only
- `~/.malp-home/attic/MAP.txt` is for attic references only
- `~/.malp-home/attic/` is for retired, dormant, or otherwise cold malp material
- attic material should not appear in the normal "what malps do we have?" answer unless the user asks for archived or attic malps too
- attic material should not be read, summarized, or pulled into context during ordinary malp work unless the user explicitly asks for it

## Suggested shapes

Prefer one of these patterns depending on what the user wants:

### 1. Archived pointer entry

Keep the original project-local malp in place, remove it from the active `MAP.txt`, and add its path to `~/.malp-home/attic/MAP.txt`.

Optionally create a small metadata note alongside it that records:
- original path
- attic date
- short reason
- whether the original project-local malp still exists in place

Use this when the goal is mainly to keep the malp out of normal context without moving project-local files.

### 2. Archived snapshot directory

Create a dated directory under `~/.malp-home/attic/` and copy in the retired malp files (`SUMMARY.txt`, `NOTES.txt`, optional `FOB.txt`) plus a tiny metadata note with the original path.

Record that snapshot path in `~/.malp-home/attic/MAP.txt`.

Use this when the user wants the attic to hold the actual retired context.

Suggested naming:
- `~/.malp-home/attic/2026-04-09-project-name/`
- keep names readable; do not over-engineer them

### 3. Transitional-parent retirement

When a broad parent malp has served its purpose and child malps are now the meaningful active units:
- remove the parent from `MAP.txt`
- preserve a short attic note or snapshot explaining the transition
- leave the still-active child malps in the active map

## Project-local naming

Default recommendation: keep the project-local directory named `.malp/` even when its path is listed in the attic.

Why:
- avoids churn inside the project
- keeps tooling and references simple
- makes promotion back to active status trivial

Only consider renaming the project-local directory itself when the user explicitly wants visible cold-storage semantics inside the repo. If that happens, treat it as a migration decision rather than a default.

## Guidance

- Do not move a malp into the attic without the user's approval.
- Suggest the attic when the goal is to avoid loading context, not just to tidy the map.
- Keep attic metadata brief and factual.
- If a user asks for a retired malp later, attic material can be used to restore or recreate an active malp.
- Default bias: prefer `attic/MAP.txt` plus optional metadata over renaming the in-project `.malp/`.
