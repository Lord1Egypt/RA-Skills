---
name: polymarket-verify
description: Verify Polymarket MR-V4 trading system deployment health. Use when asked to check trader processes, verify deployment, audit 韭菜王's changes, or after any strategy/config update. Runs a comprehensive check script and reports results.
---

# Polymarket Deployment Verification

One-command verification of the MR-V4 trading system.

## Usage

Run the check script:

```bash
bash /Users/0xbobby/.openclaw/workspace/skills/polymarket-verify/scripts/verify.sh
```

## What It Checks

1. **Process count** — exactly 3 trader processes (V4 LIVE + 2 sims)
2. **No duplicate processes** — each directory has at most 1 trader
3. **V4 flock protection** — lock file is held by running process
4. **Config validation** — dry_run, max_entries, hedge_size match expected values
5. **Trade activity** — trades.jsonl has recent writes (within 2 hours)
6. **Sim-trader isolation** — sim processes running from sim-trader/ directory, not CLI
7. **Cron health** — guardian cron (980acb62) and hourly report (4ddfd61a) have no consecutive errors
8. **Data collector** — DC process alive and writing tick data

## Output Format

```
✅ PASS: [check name] — [detail]
❌ FAIL: [check name] — [detail]
⚠️ WARN: [check name] — [detail]

Summary: X/Y checks passed
```

## When to Use

- After any strategy deployment or config change
- When Bobby asks to verify 韭菜王's work
- Automatically from guardian cron (optional)
- After process restarts or Gateway restarts
