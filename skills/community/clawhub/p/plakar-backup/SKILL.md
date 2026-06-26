---
slug: plakar-backup
name: Plakar Restore Workflows
tags:
  - backup
  - filesystem
  - resilience
description: >
  Teaches the agent how to list, inspect, diff, and restore Plakar snapshots.
  Invoke when the user says "undo", "rollback", "restore", or "revert".
---

# Plakar Restore Workflows

This skill covers **restore operations only**. Triggering snapshots is handled
automatically by the openclaw-plugin-plakar plugin — you do not need to run
`plakar backup` manually.

## When to offer restore

Offer to restore from a Plakar snapshot when the user says anything like:
- "undo that", "roll back", "revert to before", "restore my files"
- "something went wrong, can we go back"
- "the last tool call broke things"

## Prerequisites

- `plakar` must be in `$PATH`
- The store path is available in plugin config as `plakar.store`
- Always pass `-no-agent` to avoid requiring a running plakar agent daemon

## CLI syntax (v1.0.6+)

All commands use the form:
```
plakar -no-agent at <store> <command> [options]
```

## List all snapshots

```bash
plakar -no-agent at <store> ls
```

Output: snapshot ID, timestamp, size, path. Present the list to the user and
ask which snapshot to restore from.

## Inspect a snapshot's contents

```bash
plakar -no-agent at <store> ls <snapshotID>
plakar -no-agent at <store> ls -recursive <snapshotID>:/path
```

Use this to confirm the snapshot contains the expected state before restoring.

## Diff two snapshots

```bash
plakar -no-agent at <store> diff <snapshotID1> <snapshotID2>
plakar -no-agent at <store> diff -highlight <snapshotID1>:/file <snapshotID2>:/file
```

Use this to show the user what changed between two points in time.

## Restore a snapshot

Restore all files to the original paths:
```bash
plakar -no-agent at <store> restore <snapshotID>
```

Restore to a specific directory:
```bash
plakar -no-agent at <store> restore -to /tmp/restore-here <snapshotID>
```

Restore a specific path within a snapshot:
```bash
plakar -no-agent at <store> restore -to /tmp/restore-here <snapshotID>:/path/to/file
```

**Always confirm with the user** before running a restore — it overwrites live files.

## Example agent interaction

> User: "The last edit broke my config file, can you undo it?"

1. Run `plakar -no-agent at <store> ls` and show the most recent snapshots
2. Ask: "Should I restore from snapshot `<id>` taken at `<timestamp>`?"
3. On confirmation: `plakar -no-agent at <store> restore -to <original-path> <id>`
4. Confirm the restore completed and invite the user to verify the file
