---
name: prompt-diet
description: "Analyze and optimize OpenClaw system prompt token usage by compressing workspace files (AGENTS.md, SOUL.md, USER.md, TOOLS.md, IDENTITY.md, HEARTBEAT.md, MEMORY.md). Performance-first approach: only safe compressions that preserve agent behavior quality. Use when: (1) system prompt feels bloated or costs are high, (2) user wants to audit token usage of workspace files, (3) MEMORY.md has grown large with stale entries, (4) periodic prompt hygiene check. NOT for: modifying OpenClaw core system instructions, safety rules, or tool definitions."
---

# Prompt Diet

## Overview

Audit → recommend → apply cycle for workspace file token optimization. Run `scripts/token_count.py` to measure, identify compression opportunities by safety tier, then apply only approved changes with backup.

## Target Files

Files analyzed by this skill (all relative to the workspace root):

| File | Purpose | Typical Size |
|---|---|---|
| `AGENTS.md` | Agent capability declarations | Medium |
| `SOUL.md` | Persona and behavioral directives | Small–Medium |
| `USER.md` | User profile and preferences | Small–Medium |
| `TOOLS.md` | Tool configurations | Medium–Large |
| `IDENTITY.md` | Agent identity/role | Small |
| `HEARTBEAT.md` | Periodic check logic | Small–Medium |
| `MEMORY.md` | Memory index | Grows over time |
| Custom context files | Any user-added workspace .md files | Variable |

## Safety Classification

### 🟢 Safe — Auto-recommendable
Changes that cannot affect agent behavior:
- Trailing whitespace and excess blank lines (more than 1 between sections)
- Empty sections with no content (e.g., `## Section\n\n## Next`)
- Redundant markdown decoration (e.g., `---` separators between every item)
- Exact duplicate sentences or bullet points within the same file
- Unfilled template placeholders (`[TODO: ...]`, `[OPTIONAL]`, unused scaffolding)
- Trailing comments that describe what was deleted

### 🟡 Review — Needs user approval
Changes that reduce information density:
- Semantic rewrites for brevity (same meaning, fewer words)
- Example reduction (3 examples → 1 representative example)
- Long narrative descriptions → key-point bullet lists
- Archiving stale MEMORY.md entries to daily log files
- Merging near-duplicate memory entries

### 🔴 Skip — Never touch
Changes that could break agent behavior:
- Behavioral directives (what the agent should/shouldn't do)
- Safety rules and ethical constraints
- Persona core traits and tone instructions
- Critical workflow instructions (e.g., commit protocols, tool usage rules)
- All entries in memory files that the user explicitly saved
- Tool authentication configs and secrets references

## Workflow: Audit

1. Identify workspace root (default: `/home/aif/.openclaw/workspace/` or current working directory's `.openclaw/workspace/`).
2. Run token count script:
   ```bash
   python3 skills/prompt-diet/scripts/token_count.py /home/aif/.openclaw/workspace/ --detail
   ```
3. Review output: per-file token count, % of total, per-section breakdown.
4. Note files where token count is unexpectedly high or has grown since last audit.
5. Report summary to user before proceeding.

## Workflow: Recommend

For each file with compression opportunities, produce a recommendation table:

```
File: MEMORY.md  (847 tokens, 34% of total)
┌─────────────────────────────────────────────────┬────────┬──────────┐
│ Opportunity                                      │ Tier   │ Savings  │
├─────────────────────────────────────────────────┼────────┼──────────┤
│ 3 entries reference completed 2026-03 project   │ 🟡     │ ~120 tok │
│ 2 near-duplicate feedback entries               │ 🟡     │ ~60 tok  │
│ 4 blank lines between entries                   │ 🟢     │ ~4 tok   │
└─────────────────────────────────────────────────┴────────┴──────────┘
```

Ask the user: "Apply 🟢 safe changes automatically? Show me which 🟡 review items to approve?"

Do not apply any changes without explicit user confirmation.

## Workflow: Apply

Only after user approval:

1. **Create backup** before any edits:
   - Option A: rename original to `<filename>.pre-diet` (e.g., `MEMORY.md.pre-diet`)
   - Option B: copy all targets to `prompt-diet-backup/` directory with timestamp
   - Default to Option A for single-file edits, Option B for multi-file runs

2. **Apply changes** using Edit tool, one file at a time.

3. **Show diff summary**: lines removed, tokens saved per file.

4. **Report before/after**:
   ```
   Before: 2,481 tokens across 7 files
   After:  1,934 tokens across 7 files
   Saved:  547 tokens (22%)
   ```

5. Offer to clean up backup files after user confirms the result looks good.

## MEMORY.md Special Handling

MEMORY.md grows continuously and is the highest-yield target. Check for:

- **Stale project entries**: reference projects that are completed or no longer active (check if referenced files still exist).
- **Completed task items**: memory entries about in-progress work that has since shipped.
- **Duplicate information**: entries in MEMORY.md that are already captured in `memory/` daily log files (cross-reference).
- **Outdated environment info**: OS versions, tool versions, paths that have changed.
- **Over-indexed topics**: 5+ entries on the same topic → consider merging into one authoritative entry.

For each candidate removal, show the full entry text and ask: "Archive to daily log, merge, or keep?"

Never silently remove MEMORY.md entries — always show the user what will be deleted.

## Cron / Periodic Usage

This skill does NOT auto-register a cron job. To set up periodic audits yourself:

**Weekly audit cron (example):**
```bash
# Add via: /schedule  OR  CronCreate tool
# Schedule: 0 9 * * 1  (every Monday 9am)
# Command: /prompt-diet audit-only
```

**HEARTBEAT.md addition template** (copy-paste into your HEARTBEAT.md):
```markdown
## Prompt Diet Check (Weekly)
- Run token audit on workspace files
- Flag if any file has grown >20% since last check
- Remind user if MEMORY.md exceeds 200 lines
```

**Manual one-off audit:**
```bash
python3 /home/aif/.openclaw/workspace/skills/prompt-diet/scripts/token_count.py \
  /home/aif/.openclaw/workspace/ --format json | python3 -m json.tool
```

## Limitations

This skill **does not** touch:
- OpenClaw core system prompt (injected by the harness, not a workspace file)
- Tool definitions and schemas
- Runtime metadata injected at conversation start (git status, date, etc.)
- Files outside the workspace directory
- Binary files, images, or non-text assets

Token counts are **estimates** (tiktoken cl100k_base encoding approximates Claude tokenization; actual Claude token counts may differ by ±5–10%).

## Resources

### scripts/
- `token_count.py` — Standalone token counter. Works with or without `tiktoken` installed.

### references/
- `compression-rules.md` — Detailed per-file compression rules and examples.
