---
name: list-running-starred-services
description: Use this skill when you need to call bytedcli tce list-starred-service and print the raw original output directly.
---

# List Running Starred Services

Use this skill when the user wants the original output of `bytedcli tce list-starred-service`.

## Workflow

1. Run `bytedcli tce list-starred-service`.
2. Print the command output directly.

## Notes

- Do not add pagination flags unless the user explicitly asks for them.
- Do not post-process the output.
- If `bytedcli` is unavailable or the network is blocked, report that clearly and include the failing command.
