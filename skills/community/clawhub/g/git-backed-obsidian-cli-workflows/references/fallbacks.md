# Fallback policy

## Preferred path

Use the official Obsidian CLI first when it is already available and the command is supported.

In this skill, the preferred CLI path is intentionally conservative:
- `daily:append` for today's daily note
- simple `create` workflows when the target is a root-level note name

## Fallback path

For lightweight write workflows, fall back to direct markdown file writes when:
- the CLI wrapper is missing
- the CLI write command fails
- the requested target is more specific than the safe CLI wrapper supports
- the workflow intentionally uses direct write mode

## Reporting rule

Always distinguish these outcomes:
- write succeeded and sync succeeded
- write succeeded but sync failed
- CLI write failed and fallback write succeeded
- write failed completely

## Boundary

Fallback writing is for simple capture/update workflows. It should not pretend to replace the full query surface of the official CLI, and it should not invent unsupported write commands.
