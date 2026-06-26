# TOOLS.md — Local Notes

## Tool

`python3` — read `.sdr.json` files with inline `python3 -c` using `json`, `os`, `glob`.

## Rules

- Read-only. Never write files.
- No scripts on disk. Inline `python3 -c` only.
- **SILENT EXECUTION.** Never show commands or output to the user. Ever. On any channel.
  Run internally, reply with clean text only.