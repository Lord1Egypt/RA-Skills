# Risk Scoring Reference

Score is 0–100 (higher = safer).

## Scoring Table

| Risk Factor | Points |
|-------------|--------|
| **Source** | |
| Official OpenClaw | +50 |
| Trusted company (GitHub verified org) | +30 |
| Active community dev (>100 stars) | +10 |
| Personal dev (<100 stars) | -10 |
| No GitHub repo | -30 |
| **Code Type** | |
| Documentation only (SKILL.md) | +20 |
| Has scripts (Python/Bash) | -10 |
| Has binaries/executables | -30 |
| **Activity** | |
| Recent commits (<1 month) | +10 |
| Moderate activity (1-3 months) | 0 |
| Aging (3-6 months) | -10 |
| Stale (>6 months) | -20 |
| **Community** | |
| >1000 stars | +20 |
| 100-1000 stars | +10 |
| <100 stars | -5 |
| No stars visible | -10 |
| **ClawHub Assessment** | |
| All checks passed | +30 |
| Some warnings | -10 |
| Security concerns noted | -30 |

Base score starts at 50. Add/subtract points from the table above, then clamp to 0–100.

## Interpretation

| Score | Level | Action |
|-------|-------|--------|
| 80–100 | Very safe | Skip sandbox, approve |
| 60–79 | Safe | Approve, optional sandbox |
| 40–59 | Moderate | Sandbox required |
| 20–39 | High risk | Sandbox required |
| 0–19 | Very high risk | Reject immediately |
