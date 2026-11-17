---
name: "mochi-work-reports"
description: "Import work records, update status with revision history, and export dated reports and evidence. Use for Daily and Weekly Work Reports."
metadata: {"openclaw": {"requires": {"bins": ["node"]}, "homepage": "https://mochilab.bz", "version": "1.1.1"}}
---

# Daily and Weekly Work Reports

## Accumulate real work evidence

Collect the reporting date range and intended reader. add requires date, title, detail, status done|in-progress|blocked and evidence references. Preserve references to permitted commits, notes, tickets or labeled user statements. minutes is optional actual recorded duration, not an estimated full workday.

## Update the same event as it progresses

update selects a record by id and can change date, title, detail, status, evidence or minutes. Prior values are retained in history. Use minutes:null to remove an incorrectly recorded duration. Correct a blocked item to done on its existing ID instead of appending another copy of the event. Ask which record to edit when an informal description matches several events.

import-csv reads date,title,detail,status,evidence and optional minutes,sourceId. Separate several evidence references with semicolons. Stable external source IDs or exact file/row keys prevent duplicate imports. Validate the full batch before saving; an invalid record leaves the ledger unchanged. Imported evidence remains attributed to its actual source rather than being described as independently verified.

## Create a dated report file

report selects inclusive from/to dates and groups current records into completed, ongoing and blocked sections. export saves work-report.md and work-records.csv with source references and recorded durations. Earlier revision history stays in the ledger; only the current state of an event is counted. Show missing durations separately and leave empty periods empty. The generated Markdown is an evidence-based report scaffold; polish wording for the intended reader without inventing impact metrics. Saving does not send the report. Use a messaging tool only for a user-requested recipient and delivery.

## Run the local helper

Prepare an input JSON file inside the active agent workspace. Use the actual workspace, not another agent's directory.

```text
node "{baseDir}/scripts/run.mjs" --workspace "CURRENT_WORKSPACE" --input "request.json"
```

Read [references/input.md](references/input.md) before preparing fields. Every mutation and export uses a stable unique requestId; an identical retry returns its saved result. Put user text in JSON, not shell code. Successful exports return actual file paths, sizes and SHA256 values under this workspace's `.mochilab/mochi-work-reports/exports/` directory. Inspect the files before reporting completion. Previous exports are retained. No MochiLab key is needed by this standalone helper.

[User guide](README.md) · [Simplified Chinese guide](README.zh-CN.md)
