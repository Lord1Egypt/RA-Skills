# INSTRUCTION FILE DISCOVERY

Progressive disclosure of project-specific instructions from the filesystem.

## DISCOVERY WALK

At session start, walk from CWD to filesystem root, collecting instruction files:

Walk order: CWD → parent → parent's parent → ... → /

File patterns to discover (in priority order):
  1. CLAW.md or AGENTS.md (per-directory, project-specific instructions)
  2. CLAW.local.md (per-directory, local overrides, gitignored)
  3. .claw/CLAW.md (per-directory, structured instructions directory)
  4. .claw/instructions.md (per-directory, supplementary instructions)

## DEDUPLICATION

Files with identical content (same SHA-256 hash) are loaded only once.
This prevents the same instructions from being injected multiple times when
files are symlinked or copied across directory levels.

## BUDGET

| Limit | Value |
|-------|-------|
| Per file | 4,000 characters |
| Total budget | 12,000 characters |
| Priority | Most specific (CWD) first, root last |

If the total exceeds 12,000 characters:
  1. Keep all files from CWD (highest priority)
  2. Keep files from immediate parent
  3. Truncate lower-priority files to fit remaining budget
  4. Log which files were truncated

## PROGRESSIVE DISCLOSURE

The agent does NOT read all discovered files upfront.
- AGENTS.md (or CLAW.md at CWD) is read at session start (base context)
- Other discovered files are listed in a "discovered but not yet read" index
- Agent reads deeper files ON DEMAND when the task requires that context
- This prevents front-loading too much context for simple tasks

## INTEGRATION WITH SESSION START

The discovery walk runs as part of Phase 0 Session Init (Step 0b).
Results are stored in agent context as a file index for on-demand reading.
