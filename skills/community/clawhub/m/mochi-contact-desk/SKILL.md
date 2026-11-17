---
name: "mochi-contact-desk"
description: "Import CSV/vCard contacts, review email and phone duplicates, merge records, track follow-ups and export an address book. Use for Contacts and Follow-up Desk."
metadata: {"openclaw": {"requires": {"anyBins": ["python3", "python"]}, "homepage": "https://mochilab.bz", "version": "1.0.1"}}
---

# Contacts and Follow-up Desk

## Run a job

Use Python 3.10+ in the current agent workspace. Install scripts/requirements.txt into a dedicated virtual environment when it is nonempty. Credentials are private host configuration, not dependencies. Save the requested action as workspace-local JSON, then run:

```text
python3 "{baseDir}/scripts/run.py" --workspace "CURRENT_AGENT_WORKSPACE" --input "request.json"
```

Read the JSON ok/result receipt; a failed command is not a completed operation. Paths are workspace-relative except an explicitly supplied private connection profile. Agents have separate workspaces and separate state. Never use another agent's workspace just because it has a working account. Data and notifications persist under .mochilab. Do not upload those private state folders with a Skill package.

Use for a private local contact book and follow-up records. import previews CSV or vCard first; apply:true writes the previewed contacts. CSV columns include name, emails, phones, tags, organization; list fields use semicolons. Phone normalization removes punctuation but does not invent a country code. Exact shared normalized email/phone keys identify duplicate candidates; identical names alone are not enough.

merge retains the selected target ID, unions list fields and moves existing follow-ups to the target. Conflicting names, organizations or notes are returned as needsChoice until choose resolves them. User-selected field values determine the final merge. followup records a dated note and optional nextDate; due returns the most recently dated follow-up per contact whose next date has arrived. export supports CSV and vCard. CSV spreadsheet formulas are escaped. This local book is not automatically connected to the phone or a remote CRM.

[User guide](README.md) · [Simplified Chinese guide](README.zh-CN.md)
