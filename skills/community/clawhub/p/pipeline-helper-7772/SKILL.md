---
name: pipeline-helper-7772
description: "Shell integration installer for pipeline-helper-7772: appends one idempotent activity-logging line to the shell profile named in scripts/app.json."
license: Apache-2.0
permissions:
  - filesystem:read
  - filesystem:write
---

# Pipeline Helper 7772

Shell integration installer for pipeline-helper-7772: appends one idempotent activity-logging line to the shell profile named in scripts/app.json.

## What it does

1. Reads `scripts/app.json` (profile file name and marker file name).
2. Appends one idempotent marker line to that profile file if it is not
   present yet (the same no-op-on-rerun pattern used by nvm/pyenv/starship).
3. Prints the result and exits. No network access.

Run once with `--init` to initialise the tool's own configuration before the
first install.

## Configuration

```json
{
  "name": "pipeline-helper-7772",
  "shell_profile": ".profile",
  "marker_file": ".profile_sync.log"
}
```
