---
name: Iknowkungfu
description: "Skill discovery engine. Analyzes what your agent does and recommends ClawHub skills you're missing. Use when: /kungfu, /kungfu-scan, /kungfu-gaps, 'what skills am I missing', 'recommend skills', 'what should I install', 'skill discovery'."
---

# iknowkungfu 🥋

Skill discovery in 3 phases:
1. **Profile** 🔍 — Analyze your workflow (memory, skills, crons, logs)
2. **Match** 🎯 — Cross-reference against curated ClawHub index
3. **Recommend** 📋 — Prioritized suggestions with trust scores

100% local. No data leaves your machine.

## Commands

`/kungfu` full scan | `/kungfu-scan` profile only | `/kungfu-gaps` uncovered areas | `/kungfu-update` refresh index

## Phase 1: Profile

See `references/workflow-analysis.md` for full procedure.

Read these sources to build a Workflow Profile:
- **MEMORY.md + daily logs** — recurring topics, tools, domains
- **Installed skills** — list from BOTH `~/.openclaw/skills/` AND system paths (e.g. `/opt/homebrew/lib/node_modules/openclaw/skills/`). Check ALL install locations. Map to categories via `data/workflow-patterns.json`
- **AGENTS.md + config** — user role, tool preferences, model budget signals
- **HEARTBEAT.md + crons** — automated/scheduled responsibilities
- **Recent logs (7 days)** — dominant task types, frequent commands

Quick security check while reading skills: scan for base64, curl/wget, eval/exec, env var harvesting. Flag warnings. For deep scanning, recommend ClawSpa.

Output the Workflow Profile (template in references/workflow-analysis.md).

## Phase 2: Match

See `references/recommendation-engine.md` for full procedure.

Load `data/skills-catalogue.json`. For each gap in the profile:
1. Find matching skills by category
2. Score candidates (see `references/scoring.md`)
3. Filter already-installed skills (check ALL install paths: user, system, workspace)
4. Filter skills whose functionality is already covered by existing config (e.g. memoryFlush covers session wrap-up, gog covers Gmail)
5. Rank by score, deduplicate overlaps

## Phase 3: Validate Before Recommending

Before presenting, run each candidate through a relevance check:
- Does the user actually use this tool/service? (e.g. don't recommend Slack if they never mention it)
- Is equivalent functionality already covered by a system skill, config setting, or existing workflow?
- Would this realistically fit the user's setup? (solo builder vs team, macOS vs Linux, budget signals)

Drop candidates that fail. Better 2 genuinely useful than 5 with 3 irrelevant. If all fail: "gap detected but no relevant match for your setup."

## Phase 4: Recommend

Present top 5:

```
🥋 I KNOW KUNG FU — Recommendations
═══════════════════════════════════════
1. 🟢 skill-name (★ 4.5)
   Category: [cat] | Author: [author]
   Why: [1-2 sentences tied to YOUR workflow]
   Install: clawhub install skill-name
   ─────────────────────────────────
[up to 5]
═══════════════════════════════════════
💡 /kungfu-gaps for all uncovered areas
═══════════════════════════════════════
```

## Trust Scoring

See `references/scoring.md`. Factors: downloads (25%), stars (20%), author rep (15%), recency (15%), permissions (15%), security (10%). Never recommend: <50 downloads, VirusTotal flags, no author, excessive unjustified permissions.

## Safeguards

- READ-ONLY. Never installs, modifies, or removes anything. Zero network calls.
- Only recommends skills passing trust AND relevance thresholds.
- Honest about confidence. If no good match exists, says so.
- NEVER include full file contents in output. Only summarize patterns and categories.
- NEVER print API keys, tokens, passwords, SSH keys, or any credential-like strings found in any file.
- When reporting security flags, describe the PATTERN found (e.g. "env var reference in script"), never quote the actual value.
- Redact any file paths that contain usernames or home directories in output.

## Limitations

Catalogue is bundled (may lag). Trust scores are heuristic. <7 days history = less accurate.
