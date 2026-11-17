---
name: "mochi-cloud-files"
description: "Connect a WebDAV drive, list and compare a directory, upload or download files, check versions and produce integrity hashes. Use for WebDAV Cloud File Desk."
metadata: {"openclaw": {"requires": {"anyBins": ["python3", "python"]}, "homepage": "https://mochilab.bz", "version": "1.0.1"}}
---

# WebDAV Cloud File Desk

## Run a job

Use Python 3.10+ in the current agent workspace. Install scripts/requirements.txt into a dedicated virtual environment when it is nonempty. Credentials are private host configuration, not dependencies. Save the requested action as workspace-local JSON, then run:

```text
python3 "{baseDir}/scripts/run.py" --workspace "CURRENT_AGENT_WORKSPACE" --input "request.json"
```

Read the JSON ok/result receipt; a failed command is not a completed operation. Paths are workspace-relative except an explicitly supplied private connection profile. Agents have separate workspaces and separate state. Never use another agent's workspace just because it has a working account. Data and notifications persist under .mochilab. Do not upload those private state folders with a Skill package.

Use this as a client for a user-specified WebDAV collection (for example Nextcloud, Jianguoyun, a user-managed WebDAV service or an enabled WebDAV gateway). It does not expose or mount the OpenClaw workspace as a public service. Read references/input.md. Profile location is private and outside the installed Skill. Credentials are referenced through an environment variable.

list reports ETags and sizes at one collection depth. plan compares one local directory with that listing and the last transfer receipts: unchanged, upload-new, review, or remote-only. review means inspect versions before deciding direction; plan performs no transfers or deletions. upload creates new files conditionally, or updates the exact ETag supplied. download refuses to replace a local file without its current localSha256. delete needs a current remote ETag. A conflict means refresh the listing and review changes, not bypass version checks. Transfer one file at a time, <=50MiB. This is selective transfer, not a recursive background mirror.

[User guide](README.md) · [Simplified Chinese guide](README.zh-CN.md)
