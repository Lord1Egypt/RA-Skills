# Tier Rules

## Promote: WARM → HOT

A WARM memory should be promoted to HOT (added to `MEMORY.md`) when:

- Referenced or opened 3+ times within the past 7 days
- Contains information needed by multiple cron jobs or skills
- Contains context that was missing during a session and caused re-fetching

**How to promote:**
1. Extract a concise summary (1-5 lines) of the key facts
2. Add to the appropriate section in `MEMORY.md`
3. Note the promotion in the report with reason

## Demote: HOT → WARM

A HOT memory (section in `MEMORY.md`) should be demoted to WARM when:

- Not referenced in any session or cron job for 30+ days
- Relates to a completed or abandoned project
- Information is stale or no longer actionable

**How to demote:**
1. Verify the info exists in a WARM file (if not, create one first)
2. Remove the section from `MEMORY.md`
3. Note the demotion in the report — user must be informed

## Demote: WARM → COLD

A WARM file should be demoted to COLD (moved to `memory/archive/`) when:

- Not read or modified for 90+ days
- All actionable items in it are completed
- Content is purely historical with no ongoing reference value

**How to demote:**
1. Move the file to `memory/archive/`
2. Update any references to the old path
3. Note the demotion in the report

## Exceptions (never auto-demote)

Do not auto-demote files that:
- Are actively referenced by a cron job prompt (check via `cron list`)
- Belong to a project with status other than "done" or "archived"
- Are explicitly listed in `local-overrides.md` as protected

## Tracking Reference Counts

During each audit, check:
- Recent session transcripts (via `memory_search`) for file references
- Cron job prompts (via `cron list`) for file paths
- Root auto-loaded files for cross-references
- Last-modified timestamps on all WARM files

Count references in the past 7 days for promotion decisions. Use last-modified date for demotion decisions.
