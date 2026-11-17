---
name: "mochi-important-dates"
description: "Track Gregorian and lunar birthdays, anniversaries and sourced annual holidays, with advance alerts, time zones, leap-day policies and calendar export. Use for Important Dates and Holidays."
metadata: {"openclaw": {"requires": {"anyBins": ["python3", "python"]}, "homepage": "https://mochilab.bz", "version": "1.0.1"}}
---

# Important Dates and Holidays

## Run a job

Use Python 3.10+ in the current agent workspace. Install scripts/requirements.txt into a dedicated virtual environment when it is nonempty. Credentials are private host configuration, not dependencies. Save the requested action as workspace-local JSON, then run:

```text
python3 "{baseDir}/scripts/run.py" --workspace "CURRENT_AGENT_WORKSPACE" --input "request.json"
```

Read the JSON ok/result receipt; a failed command is not a completed operation. Paths are workspace-relative except an explicitly supplied private connection profile. Agents have separate workspaces and separate state. Never use another agent's workspace just because it has a working account. Data and notifications persist under .mochilab. Do not upload those private state folders with a Skill package.

Use for birthdays, wedding anniversaries, family milestones and imported statutory holidays. Store events with put; list/upcoming review them. Use event timezone and time for reminders, rather than inferring a timezone from a name. A birth year is optional; do not report an age when none was supplied. For a lunar birthday, ask whether a leap-month birth is celebrated only in matching leap years or also in its regular month. Feb 29 supports Feb 28, March 1 or leap-years-only. A DST gap advances to the next valid local minute; an ambiguous time uses its first occurrence.

Holiday imports are annual JSON with country/region and official source URL. Preserve workday, holiday and observance labels. Do not infer statutory days off or Chinese adjusted working weekends from ordinary festival dates. Fetch the relevant year's official notice when the user asks to import a holiday calendar; keep that URL in the file. Lunar conversion and date exports run locally.

Use poll for due reminders and upcoming for a planning view. Birthday ages are based only on explicit Gregorian birth years. export-ics expands actual dated occurrences over a selected <=730-day horizon, including lunar dates. Import that file into a calendar to view it; it is not a live calendar subscription. For automated delivery, read references/notifications.md. poll catches up over the last 48 hours by default, <=7 days; keep the host schedule more frequent than that. Repeated polls deduplicate by event revision, occurrence and advance offset. Editing/removing an event retires its old pending notices. Retain the same user timezone and advance settings on edits.

[User guide](README.md) · [Simplified Chinese guide](README.zh-CN.md)
