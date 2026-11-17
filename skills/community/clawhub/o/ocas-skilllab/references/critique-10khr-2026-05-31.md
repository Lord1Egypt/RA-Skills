# 10khr Grind — 2026-05-31 Session

_Session log for the May 31 2026 10khr iteration. Cumulative patterns go in `critique-10khr-learnings.md`._

## Target: ocas-custodian

**Heuristic score:** 45/50 (Band A) — lowest in library
**Manual score:** 39/50 (Band B)
**Score after:** 47/50 (Band A)

## What was fixed

1. **Known Code Fixes section (~50 lines)** — Full Python code patches for `oc_platform_sms_auto_detect_override` and `oc_telegram_edit_finalize`, plus the Escalation Runner Pattern workflow, moved to `references/known-code-fixes-and-cascade.md` (D3: 3→5, D8: 3→5)
2. **Duplicate Self-Update procedure (7 steps)** — Already had `references/self-update.md` but also had a full 7-step inline copy. Inline copy removed, reference pointer only retained. (D3: +delta)
<<<<<<< Updated upstream
3. **MCP Cascade section** — Full bash snippet with absolute path `<hermes-home>/config.yaml` moved to reference file. Fixed phantom reference `util-ustodian/references/mcpcascade-triage.md` (doesn't exist) — replaced with pointer to `util-hermes-ops/references/mcp-cascade-triage.md`. (D5: 4→5)
=======
3. **MCP Cascade section** — Full bash snippet with absolute path `~/.hermes/config.yaml` moved to reference file. Fixed phantom reference `util-ustodian/references/mcpcascade-triage.md` (doesn't exist) — replaced with pointer to `util-hermes-ops/references/mcp-cascade-triage.md`. (D5: 4→5)
>>>>>>> Stashed changes
4. **Missing `## Escalation Path` heading** — Patch tool accidentally removed this heading when extracting the Known Code Fixes section. Restored.
5. **Duplicate `## OKRs` heading** — Patch tool created a duplicate when inserting Support File Map table markings. Resolved by removing the extra copy.
6. **Support file map entries** — Added 9 entries for previously-unlisted reference files (including `known-code-fixes-and-cascade.md`, `transient-provider-errors.md`, `runtime-error-triage.md`, `divergent-branch-handling.md`, `system-maintenance.md`, `api_endpoints.md`, `script-library-organization.md`, `self-improvement.md`). Updated `using-script.md` description (removed "applying known code fixes" which moved to new reference file). (D4: 3→4, D5: +delta)
7. **Heading rename** — `## Scripts & Known Fixes` → `## Scripts` (content moved to reference).

## Score impact

| Dim | Before | After | Delta |
|-----|--------|-------|-------|
| D3 | 3 | 5 | +2 |
| D4 | 3 | 4 | +1 |
| D5 | 4 | 5 | +1 |
| D8 | 3 | 5 | +2 |
| D10 | 4 | 5 | +1 |
| **Total** | **39** | **47** | **+8** |

## Key learnings

### Lesson: Patch tool section extraction is high-risk
Extracting a large inline section via patch (replacing lines X..Y with a one-line pointer) requires extreme care about adjacent headings. The patch tool matched on heading-adjacent content and:
- Eaten the subsequent heading (`## Escalation Path`)
- Created duplicate headings (`## OKRs` appeared twice)
- Required 6 patches to accomplish what should have been 2 conceptually

**Rule:** When moving a large inline section to references, first verify the pre- and post-context of the target range includes the full section AND no adjacent headings. After applying, immediately grep for `## ` to detect duplicates or orphans.

### Lesson: Absolute paths in inline code blocks
<<<<<<< Updated upstream
The MCP Cascade section contained `open('<hermes-home>/config.yaml')` — an absolute path that fails on non-Hermes installs. When moving inline code to reference files, replace hardcoded paths with template variables (`{agent_root}/config.yaml`).
=======
The MCP Cascade section contained `open('~/.hermes/config.yaml')` — an absolute path that fails on non-Hermes installs. When moving inline code to reference files, replace hardcoded paths with template variables (`{agent_root}/config.yaml`).
>>>>>>> Stashed changes

### Lesson: Cross-skill path references are fragile
`util-ustodian/references/mcpcascade-triage.md` was a typo/cross-skill reference that doesn't exist. The correct path is `util-hermes-ops/references/mcp-cascade-triage.md`. Always verify cross-skill paths exist before embedding them.