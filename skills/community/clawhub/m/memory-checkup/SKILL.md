---
name: memory-checkup
version: 1.1.1
description: Audit and repair an AI agent's memory corpus for consistency. Use when memory contains stale numbers or superseded facts, when different memory files contradict each other (e.g. old download/star counts), when a metric changed and documents must be synced, when daily memory flushes have gaps or stopped, when memory references files that no longer exist, when the user says "check my memory", "memory audit", "memory checkup", or when answering from memory feels risky because facts may have drifted.
---

# Memory Checkup

Audit an agent's memory corpus (MEMORY.md, USER.md, and files under memory/) and surface consistency problems before they reach the user: stale superseded numbers, contradictions, dangling file references, abandoned daily entries, and orphan files.


## Onboarding (First Use)

When the user first triggers this skill and `memory/memory_checkup_state.json` doesn't exist, run a one-time setup:

1. **Introduce capability** (one sentence): _"I can audit your agent's memory corpus — stale numbers, contradictory facts, dangling references — all in one run."_

2. **Quick configuration:**

1. **Report language**(Default: Follow user input language)
   - Chinese / English / Follow user input
2. **Memory corpus path**(Default: auto-detect current workspace)

3. **Write initial state file** `memory/memory_checkup_state.json`(JSON format, with `onboarded: true` and timestamp)

4. **Confirm completion**: _"Setup done! Just use it from now on. Say 'reset settings' anytime to reconfigure."

**Onboarding runs exactly once.** Subsequent activations read the state file directly. When the user says "reset settings", delete the state file and re-run setup.

---

## When to run

1. The user asks to check/audit/clean memory ("checkup", "check my memory").
2. Before answering questions that depend on facts recorded over many days (awards, counts, project statuses).
3. After a metric changes and the user asks to sync all documents (e.g. download counts in application essays).
4. Periodically, alongside daily memory flushes.

## Procedure

### Step 1: Locate the corpus

The corpus root is the agent workspace: it must contain `MEMORY.md` and/or a `memory/` directory. Ask or infer from context; in OpenClaw this is the workspace directory.

### Step 2: Run the audit script

```bash
python3 scripts/memory_checkup.py --memory-dir <workspace-root> [--json]
```

The script scans and reports:

| Check | Meaning |
|---|---|
| Stale numbers | Same metric (downloads/stars/users) with an old value in some files and a newer value in newer files |
| Dangling references | File paths mentioned in memory that no longer exist |
| Stale entries | Daily-flush files whose date has a gap to the newest entry |
| Orphans | memory/ files never referenced from anywhere else |

### Step 3: Verify before editing

For every stale-number finding, confirm the current value with the user or with live evidence (run the real check: hit the API, count the files). Never assume the newest mention is correct just because it is newest.

### Step 4: Fix

- Update stale mentions, or annotate them as superseded if history should be preserved ("old value 4,600+ deprecated").
- Remove or repair dangling references.
- Do NOT delete orphan daily files; list them to the user and let them decide.
- After edits, re-run the audit to confirm zero issues.

### Step 5: Report

Summarize in the user's language: how many files scanned, issues by type, what was fixed, what needs a user decision.

## Notes

- The script is read-only. All fixes are made by the agent, file by file, after verification.
- Number extraction currently covers downloads/stars/users patterns (English and Chinese); extend `DEFAULT_PATTERNS` for other metrics.
- JSON output is machine-readable for piping into other tools.
