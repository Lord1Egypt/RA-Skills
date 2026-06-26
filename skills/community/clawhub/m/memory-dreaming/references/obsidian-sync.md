# Obsidian Sync — How It Works

## Overview

When `obsidian.enabled: true` in config, Phase 4 of the dream cycle syncs consolidated knowledge to an Obsidian vault. The vault becomes the human-browsable, phone-accessible source of truth for structured knowledge.

## What Gets Synced

| Source | Target Folder | When |
|---|---|---|
| People mentioned in memory | `People/` | New person discovered or info updated |
| Projects/repos in memory | `Projects/` | New project or status change |
| Plans (task_plan.md files) | `Plans/` | New plan or phase status change |
| Tools/services configured | `Tools/` | New tool or config change |
| Key decisions | `Decisions/` | New decision from consolidation |

## Formatting Rules

All Obsidian notes follow these rules (configurable via `obsidian.formatting`):

1. **Tags on first line** — `#person #shapes #engineering` before the title
2. **Wikilinks** — `[[Related Note]]` to connect concepts
3. **Full depth** — never summarize or dilute; write the complete information
4. **YAML frontmatter** — optional, with aliases when a topic has multiple names

Example:
```markdown
#person #shapes #engineering #rnd

# Gal Peer

## Role & Organization
- **Title:** Full Stack Engineer
- **Team:** R&D
- **Reports To:** [[David Virtser]]

## Links
- **GitHub:** [GalPeer33](https://github.com/GalPeer33)

## Related
- [[Shapes Atlas]] — contributor
- [[Shapes Ecosystem]]
```

## Plan Tracking

The dreaming skill scans the workspace for `task_plan.md` files. For each:

1. Extract plan name from the parent directory name
2. Check if `Plans/<name>.md` exists in the vault
3. If not, create it with: status, phases table, key decisions, links to related notes
4. If exists, update: phase statuses, any new decisions
5. Update `Projects/Active Plans.md` dashboard with current plan list

This ensures **every plan created anywhere in the workspace automatically appears in Obsidian**.

## Sync Behavior

- **Create:** New vault notes are created from scratch with full formatting
- **Update:** Existing notes are updated — new sections appended, status fields changed. Content is never removed from vault notes during sync (only dreaming's consolidation phase removes contradictions from MEMORY.md)
- **Never delete:** Vault notes are never deleted by the dreaming skill
- **Idempotent:** Running sync twice with no new information changes nothing

## Conflict Handling

If a vault note was edited manually (by the human via Obsidian):
- The dreaming skill **appends** new information but does not overwrite manual edits
- Manual sections are preserved
- If there's a genuine conflict (e.g., status field differs), the dreaming log notes it for human review
