# Haqi Operator — Schedule (24/7 cadence)

There is no server cron in this phase. "24/7" is achieved by the operator agent
(e.g. an always-on OpenClaw task) running ticks on this cadence. Keep it gentle.

## Minimum viable cadence
| Lane          | Interval        | Notes |
|---------------|-----------------|-------|
| Companionship | every 3–6 h     | Only act on real `careTodos`; skip if pet is healthy. |
| Content       | every 12–24 h   | One artifact per run; verify before saving. |
| Marketing     | every 12–24 h   | One card/post; save to `agent/marketing/`, no auto-publish. |
| Analytics     | once per day    | Write the daily KPI summary; pick next priority. |

## Tick algorithm
1. Run **Pre-flight** (see PLAYBOOK.md).
2. Choose the lane whose interval has elapsed and whose value is highest:
   prefer Companionship if `careTodos` is non-empty, else the most overdue lane.
3. Do exactly ONE lane action, then **Post-tick**.
4. Wait ~1–3 h, repeat.

## Safety throttles
- Max ~1 marketing artifact/day and ~1 content artifact/day unless the owner raises it.
- Never send `buy` or publish to third parties without explicit owner approval.
- If three consecutive ticks error, stop and surface the problem to the owner.
