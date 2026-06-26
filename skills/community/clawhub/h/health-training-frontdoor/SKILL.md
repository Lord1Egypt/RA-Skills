---
name: health-training-frontdoor
description: Narrow first-class front door for live Fitbit/training retrieval via stable JSON actions.
---

# Health/Training Front Door

Use this when OpenClaw needs **live Fitbit/health/training data** in a stable, low-ambiguity way.

This is a thin, typed front door over the canonical Fitbit connector tooling.

## Why this exists

`fitbit_tools.py` is the canonical operational backend, but it still requires low-level CLI composition.
This front door provides a narrow action contract so agents can call one stable interface instead of assembling raw shell commands every time.

## Contract

Run:

- `node skills/health-training-frontdoor/scripts/request.js '{...json...}'`

Input JSON:

```json
{
  "action": "latest_recovery"
}
```

Supported actions:

- `auth_status`
- `latest_recovery`
- `quality_flags`
- `training_status`
- `training_window`
- `unified_latest`

Optional fields:

- `days` (integer)
- `ensureFresh` (boolean)
- `source` (for `unified_latest`, default `best`)

## Default behavior by action

- `latest_recovery`: fetches latest days of `hrv_rmssd,resting_hr,sleep_minutes,sleep_score,data_quality`; defaults `days=3`, `ensureFresh=true`
- `quality_flags`: defaults `days=7`
- `training_status`: defaults `days=14`, `ensureFresh=true`
- `training_window`: defaults `days=14`, `ensureFresh=true`
- `unified_latest`: defaults `days=14`, `source=best`

## Notes

- Output is compact JSON.
- This surface is read-only.
- Interpretation/coaching remains outside this skill.

## Training Programming Reference

All programming decisions must be grounded in **Practical Programming for Strength Training** (Rippetoe & Baker, 3rd Ed.).

**Always load before giving any programming advice:**
1. `reference/practical-programming/INDEX.md` — who Joao is, relevant chapters, reading guide
2. `memory/training-continuity.md` — current lifts, recent sessions, health signals

For any programming question, read the relevant sections of `reference/practical-programming/book.md` directly. The book is the authority.

## Backend mapping

This front door maps directly to:
- `fitbit-connector/scripts/fitbit_tools.py`

Do not use this to bypass auth or write-capable operations.
