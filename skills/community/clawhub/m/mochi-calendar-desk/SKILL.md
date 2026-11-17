---
name: "mochi-calendar-desk"
description: "Import ICS calendars, expand recurring events, inspect conflicts, create meeting files and transfer CalDAV resources with version checks. Use for Calendar and Agenda Desk."
metadata: {"openclaw": {"requires": {"anyBins": ["python3", "python"]}, "homepage": "https://mochilab.bz", "version": "1.0.1"}}
---

# Calendar and Agenda Desk

## Run a job

Use Python 3.10+ in the current agent workspace. Install scripts/requirements.txt into a dedicated virtual environment when it is nonempty. Credentials are private host configuration, not dependencies. Save the requested action as workspace-local JSON, then run:

```text
python3 "{baseDir}/scripts/run.py" --workspace "CURRENT_AGENT_WORKSPACE" --input "request.json"
```

Read the JSON ok/result receipt; a failed command is not a completed operation. Paths are workspace-relative except an explicitly supplied private connection profile. Agents have separate workspaces and separate state. Never use another agent's workspace just because it has a working account. Data and notifications persist under .mochilab. Do not upload those private state folders with a Skill package.

Use for real ICS event data, recurring agenda expansion and CalDAV resource transfer. import retains UID, recurrence overrides and VTIMEZONE from the original resource. agenda and conflicts need an explicit offset-aware time range. All-day events occupy their calendar days. Transparent and cancelled events do not count as busy. Floating-time files need an explicit timezone added using the user's calendar application before import; do not guess one.

create writes a single event ICS with start/end, title, optional location and description. Existing files are preserved. For remote calendars, use a private DAV profile pointing to the actual calendar collection. remote-list lists its resources; pull saves an ICS resource and its ETag. push creates a new resource with If-None-Match or replaces a specific current ETag. remote-delete also needs the current ETag. If the server returns a conflict, pull and review before retrying. Different providers may require an app password and a provider-specific CalDAV URL. This client uses HTTPS Basic/app-password authentication and leaves provider login/discovery to the supplied collection URL. It does not send meeting invitations or RSVP messages.

[User guide](README.md) · [Simplified Chinese guide](README.zh-CN.md)
