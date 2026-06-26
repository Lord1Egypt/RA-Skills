# Workflow surface

## Read/query layer

Use the official Obsidian CLI directly for:
- `search`
- `read`
- `daily:read`
- `links`
- `outline`
- `tags`
- `tasks`
- `vault`

These are primary CLI workflows and should not trigger Git sync.

## Write/update layer

Use the bundled wrapper script for deterministic post-write sync behavior when needed. The wrapper defaults to this skill's own `scripts/backup.sh` instead of borrowing another skill's backup implementation.

Safe write surface in the wrapper:
- today's `daily:append` via official CLI when available
- simple root-level note creation via official CLI when available
- fallback direct-file write for memo, append, create, and dated daily-note writes

## Why the wrapper is narrower than the CLI

The official CLI may expose more commands than the wrapper script handles.
That is intentional.

The wrapper exists to provide a stable, publishable automation surface for the most common write-and-sync workflows, not to mirror every CLI command.
