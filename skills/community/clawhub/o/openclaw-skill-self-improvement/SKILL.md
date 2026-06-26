---
name: openclaw-skill-self-improvement
description: |
  Health, eval, and regression system for continuously improving OpenClaw skills.
  Use when creating, auditing, or maintaining AgentSkills to ensure quality,
  detect duplicates, prevent routing regressions, and keep the skill registry clean.
  Triggers on: "audit skills", "skill health check", "routing eval",
  "duplicate skill", "dark skill", "skill regression", "improve skill system".
version: "1.0.0"
---

# OpenClaw Skill Self Improvement

A health, eval, and regression system for continuously improving OpenClaw skills.

## Goal
Turn skill quality from an occasional cleanup task into a repeatable health loop.

## What it does

### 1. Skill Health Check
Scans all workspace and system skills to detect:
- **Duplicate skills**: skills with highly similar names/descriptions
- **Dark skills**: skills with no recent usage signals
- **Stale skills**: skills unused for extended periods

### 2. Routing Eval
Runs evaluation cases against a keyword-weighted router to verify:
- Correct skills trigger for given inputs
- Wrong skills don't accidentally trigger
- Pass rate tracking over time

### 3. Daily Heartbeat
Automated daily run that:
- Executes health check + eval
- Compares against previous run
- Generates human-readable summary
- Surfaces changes and recommended actions

## Usage

### Run health check
```bash
node scripts/skill-health-check.mjs /path/to/workspace
```

### Run routing eval
```bash
node scripts/routing-eval-runner.mjs /path/to/workspace
```

### Run daily heartbeat
```bash
node scripts/daily-health-heartbeat.mjs /path/to/workspace
```

## Output files
- `.learnings/skill-health-report.json`
- `.learnings/routing-eval-report.json`
- `.learnings/daily-skill-health-summary.txt`
- `.learnings/skill-health-history.json`

## Current status
- Total skills scanned: 122 (workspace + system)
- Duplicate pairs: 1 (false positive)
- Dark skills: 0
- Eval pass rate: 100% (8/8)

## Files
- `scripts/skill-health-check.mjs` — duplicate and dark skill detection
- `scripts/routing-eval-runner.mjs` — routing evaluation runner
- `scripts/daily-health-heartbeat.mjs` — daily automation
- `references/routing-evals.json` — evaluation case definitions

## License
MIT
