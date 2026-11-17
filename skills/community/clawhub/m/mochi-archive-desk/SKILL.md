---
name: "mochi-archive-desk"
description: "Inspect ZIP/TAR contents, extract into new folders, create ZIPs from selected files and report per-file integrity hashes. Use for Archive and Integrity Toolbox."
metadata: {"openclaw": {"requires": {"anyBins": ["python3", "python"]}, "homepage": "https://mochilab.bz", "version": "1.0.1"}}
---

# Archive and Integrity Toolbox

## Run a job

Use Python 3.10+ in the current agent workspace. Install scripts/requirements.txt into a dedicated virtual environment when it is nonempty. Credentials are private host configuration, not dependencies. Save the requested action as workspace-local JSON, then run:

```text
python3 "{baseDir}/scripts/run.py" --workspace "CURRENT_AGENT_WORKSPACE" --input "request.json"
```

Read the JSON ok/result receipt; a failed command is not a completed operation. Paths are workspace-relative except an explicitly supplied private connection profile. Agents have separate workspaces and separate state. Never use another agent's workspace just because it has a working account. Data and notifications persist under .mochilab. Do not upload those private state folders with a Skill package.

Use for actual archive inspection, selective file packaging and integrity receipts. inspect inventories paths and expanded sizes without extracting. extract validates portable paths, duplicates, links and total expansion, decompresses all data successfully, then writes into a new directory. The result lists each file's SHA256. create uses the exact explicit input list and verifies the resulting ZIP CRCs. Source files are preserved.

ZIP and ordinary TAR/TAR.GZ/TAR.BZ2/TAR.XZ archives are supported by Python's standard library. Encrypted ZIP, links, devices, duplicate/case-colliding names and Windows reserved names are rejected. Extract to a new directory and review the returned manifest before opening untrusted files. This is a file tool, not an instruction to execute extracted content. It does not install packages or restore a live service.

[User guide](README.md) · [Simplified Chinese guide](README.zh-CN.md)
