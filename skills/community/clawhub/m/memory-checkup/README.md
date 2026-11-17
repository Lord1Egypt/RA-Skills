# Memory Checkup

**Audit and repair an AI agent's memory corpus for consistency.**

[English](./README.md) | [中文](./README_CN.md)

---

Agents that keep long-term memory (OpenClaw, Claude Code with memory files, or any agent with a `MEMORY.md` + `memory/` structure) accumulate drift: a metric changes on Monday, three files still say the old value on Friday; a daily flush job silently dies; a path referenced in memory no longer exists. Nobody notices until the agent confidently states a stale fact.

Memory Checkup scans the whole corpus and surfaces that drift before it reaches the user.

## What it detects

| Check | Meaning |
|---|---|
| **Stale numbers** | Same metric (downloads / GitHub stars / user counts) appearing with an old value in some files while newer files carry a newer value |
| **Dangling references** | File paths mentioned in memory that no longer exist on disk |
| **Stale entries** | Gaps in date-named daily logs near the newest entry (a flush job may have died) |
| **Orphan files** | Non-dated memory files never referenced from anywhere else |

## Quick start

```bash
git clone https://github.com/Thomaszhou22/memory-checkup.git
python3 memory-checkup/scripts/memory_checkup.py --memory-dir /path/to/agent/workspace
```

Add `--json` for machine-readable output, e.g. to pipe into a cron or a gateway hook.

The script is **read-only**. Fixing is deliberately left to the agent and the user: for every stale number, confirm the current value against live evidence first, then update or annotate the old mentions as superseded.

## Using as an OpenClaw / Claude Code skill

Copy or symlink this folder into your skills directory. The `SKILL.md` frontmatter triggers on requests like "check my memory", "memory audit", "体检记忆", and on risky recall situations (metrics recorded over many days).

Agent workflow defined by the skill:

1. Locate the corpus (workspace with `MEMORY.md` / `memory/`)
2. Run the audit script
3. Verify each finding with the user or live evidence — newest is not always correct
4. Fix file by file, re-run until clean
5. Report in the user's language

## Design notes

- **Read-only by default.** An audit tool that edits memory unsupervised would be the thing it audits.
- **Newest-wins with verification.** The script ranks values by the newest supporting file (ties broken toward the larger value), but treats every "stale" flag as a question, not a verdict.
- **Scope discipline.** Scans only the workspace root Markdown files and `memory/`; never recurses into projects or `node_modules/`.
- **Context filtering.** Number patterns are disambiguated by line context (e.g. stars must mention GitHub) to cut false positives.
- Extend `DEFAULT_PATTERNS` in the script to track any metric you care about (MAU, API latency, revenue...).

## Real-world validation

Developed and validated against a live agent workspace with 130 memory files: it found a superseded download count still lingering in five files, template placeholder paths recorded as real references, and a dead daily-flush gap — all confirmed real.

## File structure

```
├── SKILL.md                    # Skill instructions for the agent
├── scripts/
│   └── memory_checkup.py       # The read-only audit script
└── README.md
```

## Limitations

- Number detection is heuristic (regex + context); it flags candidates, not truths
- Currently ships English + Chinese number patterns
- Metric ranking assumes date-named daily logs; custom corpus layouts may need tuning

## License

MIT
