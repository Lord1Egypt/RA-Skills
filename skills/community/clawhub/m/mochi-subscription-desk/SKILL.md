---
name: "mochi-subscription-desk"
description: "Track software, memberships and service renewals, calculate cancellation deadlines, forecast costs by currency and queue due notices. Use for Subscription and Renewal Desk."
metadata: {"openclaw": {"requires": {"anyBins": ["python3", "python"]}, "homepage": "https://mochilab.bz", "version": "1.0.1"}}
---

# Subscription and Renewal Desk

## Run a job

Use Python 3.10+ in the current agent workspace. Install scripts/requirements.txt into a dedicated virtual environment when it is nonempty. Credentials are private host configuration, not dependencies. Save the requested action as workspace-local JSON, then run:

```text
python3 "{baseDir}/scripts/run.py" --workspace "CURRENT_AGENT_WORKSPACE" --input "request.json"
```

Read the JSON ok/result receipt; a failed command is not a completed operation. Paths are workspace-relative except an explicitly supplied private connection profile. Agents have separate workspaces and separate state. Never use another agent's workspace just because it has a working account. Data and notifications persist under .mochilab. Do not upload those private state folders with a Skill package.

Use for planned recurring charges rather than historic expense accounting. Store the first charge date, amount, currency, cycle and cancellation lead days. Forecasts preserve the original day-of-month: a Jan 31 monthly plan uses Feb's last day and then Mar 31. Feb 29 annual plans return to Feb 29 in a leap year. Currency totals remain separate; never invent exchange rates. end is the inclusive final charge date, not an automatically executed cancellation.

poll lists approaching renewal and cancellation deadlines with persistent notice IDs. Read references/notifications.md to create an actual user-authorized host schedule and destination. A reminder does not pay or cancel a subscription. After editing a price/cycle, review the next forecast and replace any stale pending notices before sending. User-selected subscriptions and state stay in this agent workspace.

[User guide](README.md) · [Simplified Chinese guide](README.zh-CN.md)
