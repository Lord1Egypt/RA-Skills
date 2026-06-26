---
name: env-health-check
description: Inspect environment variables, critical directories, and write permissions, then produce a health report. Use when validating deployment readiness, local runtime setup, workspace health, or missing env/config prerequisites.
---

# Env Health Check

Inspect runtime prerequisites and emit a compact health report.

## Workflow

1. Pass required env var names with `--env` flags.
2. Pass critical directories with `--dir` flags.
3. Run `index.js` and review OK/WARN/FAIL output.
4. Treat missing write access as a blocker unless the path is intentionally read-only.
