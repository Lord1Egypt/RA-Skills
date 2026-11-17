---
name: "mochi-reminders"
description: "Audit scheduler jobs, record real delivery receipts and export calendar events. Use for Reminders and Scheduled Tasks."
metadata: {"openclaw": {"requires": {"bins": ["node"]}, "homepage": "https://mochilab.bz", "version": "1.1.1"}}
---

# Reminders and Scheduled Tasks

## Register a reminder in the native scheduler

Read references/scheduling.md and inspect the installed host scheduler schema. Resolve the requesting agent, timezone, channel, account and recipient. prepare validates the time and returns a plan; it does not create a timer. Create the job through the host's native scheduling tool, read it back, then record the matching receipt. Before retrying an uncertain create, list existing jobs to avoid duplicates. Do not edit another agent's jobs.

## Check execution and chat delivery

audit accepts the real scheduler list as jobs [{jobId,enabled,nextRunAtMs,delivery}]. It compares only this workspace's registered jobs and distinguishes missing jobs, disabled jobs, route changes and overdue next-run values. Supply native read-back data, never a model-created success record. record-delivery saves jobId and receipt {source:"native-scheduler",confirmedByScheduler:true,runId,state:"delivered"|"failed",finishedAt,evidence,delivery}; a receipt for another account is rejected. Successful registration is scheduled, while only a verified run establishes delivered. Keep failures visible.

## Export to a calendar

export-calendar uses jobId and optional durationMinutes (default 15) to create reminder.ics and a receipt note. Supported calendar copies are one-time jobs or daily/weekly/monthly fixed-time cron jobs. It retains the IANA timezone for recurring events. Calendar import is separate from the original WeChat delivery: neither exporting nor importing the copy registers an OpenClaw job. Unsupported cron shapes and interval timers produce an explicit error. list and update-receipt keep the original management workflow. Every write/export requires requestId; scheduler creation and pausing still use the actual native tool.

## Run the local helper

Prepare an input JSON file inside the active agent workspace. Use the actual workspace, not another agent's directory.

```text
node "{baseDir}/scripts/run.mjs" --workspace "CURRENT_WORKSPACE" --input "request.json"
```

Read [references/input.md](references/input.md) before preparing fields. Every mutation and export uses a stable unique requestId; an identical retry returns its saved result. Put user text in JSON, not shell code. Successful exports return actual file paths, sizes and SHA256 values under this workspace's `.mochilab/mochi-reminders/exports/` directory. Inspect the files before reporting completion. Previous exports are retained. No MochiLab key is needed by this standalone helper.

[User guide](README.md) · [Simplified Chinese guide](README.zh-CN.md)
