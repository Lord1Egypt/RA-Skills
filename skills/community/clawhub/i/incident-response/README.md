# Incident Response

Structured 7-phase incident response workflow for OpenClaw system failures.

Built from real production investigations — binding loss events, gateway crashes, config regressions, and root cause traces through backup timelines, git diffs, and session JSONL logs.

---

## What it does

When something breaks, this skill walks you through seven phases in strict order:

| Phase | Name | Purpose |
|-------|------|---------|
| 0 | Triage | Check current state — is it actually still broken? |
| 1 | Evidence | Gather hard evidence from 4 sources (backups, git, session logs, diffs) |
| 2 | 5 Whys | Root cause analysis — every "why" must cite specific evidence |
| 3 | Restore | Merge from known-good backup, verify, restart |
| 4 | Prevent | Add guards proportional to severity (config guard, SOUL.md rule, chmod) |
| 5 | Monitor | Schedule a cron check (7–30 days depending on severity) |
| 6 | Document | Write to `~/.openclaw/learnings/rules.md` and MEMORY.md |

**Rule: Never skip a phase. Never assume — follow the evidence.**

---

## Install

```bash
clawhub install incident-response
```

---

## Trigger phrases

```
investigate binding loss
investigate gateway crash
why did X stop working
gateway down
gateway crashed
bindings lost
agent not responding
root cause
who changed X
audit X
something disappeared
```

---

## What's included

| File | Purpose |
|------|---------|
| `SKILL.md` | Full 7-phase workflow with runnable commands |
| `references/checklists.md` | Quick diagnosis checklists for 6 common failure types |
| `references/prevention-patterns.md` | 6 prevention patterns with code templates |
| `references/cron-template.md` | Post-incident monitoring cron template |

---

## Failure types covered

- **Gateway crash** — invalid config key, launchctl exit code, doctor/fix flow
- **Binding loss** — backup timeline, count guard, restore from good state
- **Config key disappeared** — grep backups, git log, patch restore
- **Agent routing wrong** — binding check, restart flow
- **Vector search not finding content** — index check, sqlite reset
- **Orphaned tool calls** — session file reset

---

## Requirements

- `exec` tool with SSH access to the affected host
- OpenClaw config backups at `~/.openclaw/config-backups/` (generated automatically)
- `git` initialized in `~/.openclaw/` (for audit trail)

---

## License

MIT
