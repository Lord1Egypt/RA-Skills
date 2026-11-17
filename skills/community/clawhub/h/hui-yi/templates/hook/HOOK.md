---
name: hui-yi-signal-hook
description: "Accumulate Hui-Yi signals after trusted host selection or an explicit leading /hui-yi text command"
metadata:
  { "openclaw": { "emoji": "🧠", "events": ["message:preprocessed"] } }
---

# Hui-Yi Signal Hook

Optional workspace hook for Hui-Yi 1.2.13.

Purpose:
- listen on `message:preprocessed`
- accept trusted host Hui-Yi selection or an explicit leading `/hui-yi <query>` / `/hui_yi <query>` text command from mapped `context.body`
- never activate solely from message-body recall phrases; there is no body-heuristic fallback
- run the same conservative signal detection and weak-activation writeback inline
- update `memory/cold/` note `Session signals` and `memory/cold/tags.json` without invoking external binaries

Install and enable only when the user requests persistent signal collection.
Loading the skill does not enable the hook. The host must own workspace and
skill-selection metadata; user-supplied event fields must not become authority.
All scopes routed to one workspace share one archive. Session hashes support
deduplication, not user permissions or tenant isolation.

Text commands are case-insensitive, require ASCII space/tab before a nonempty
query, and have the command prefix stripped before matching. Leading whitespace,
quoted/embedded/prefixed/empty commands and `bodyForAgent`-only commands are rejected.
OpenClaw 2026.9.5's native mapper emits no selection metadata. Its text-command
path requires a plain mapped body beginning with the command; provider
envelopes or native command interception require explicit CLI/adapter use.
Isolated mapper-shaped tests do not establish real channel end-to-end behavior.

## What this hook persists (privacy)

Note files and `tags.json` under `memory/cold/`:
- per-note activation counters (`Session signals`) and `last_activated` dates
- session identity only as a truncated `sha256:` fingerprint — raw session keys,
  user ids, and chat ids are never written

`hooks/hui-yi-signal-hook/hook.log` (default mode):
- allowlisted lifecycle stages, safe status/error codes, and counts
- no message bodies/previews, raw scope/thread identifiers, raw metadata, note
  titles/paths, or matching terms; scope identity uses hashed `sessionHash`
- the log self-rotates at 256 KB (keeps the most recent ~128 KB)

Debug mode (`HUI_YI_HOOK_DEBUG=1`, off by default):
- adds lifecycle/count diagnostics such as `alive` / `skipped`
- preserves the same exclusions as normal mode; it never restores raw payload
  logging. This is separate from explicit sensitive diagnostics in Python CLIs

## File and installation boundary

- Filesystem helpers reject symbolic links, Windows junctions/reparse points,
  hard links, and special files. Paths must lead through ordinary directories,
  with identity rechecks. TS uses staged atomic replacement on POSIX and for
  new Windows files. Existing Windows files instead use a verified descriptor
  for writes, preserving their original DACL; failures trigger best-effort
  rollback. This branch is not crash atomic, because Node cannot natively clone
  the original DACL onto a replacement file. Separate Python workflows stage
  atomic replacements and copy existing Windows DACLs before writing any data.
- These application checks are not a kernel sandbox against a hostile process
  with the same OS account concurrently replacing directories. The workspace and
  its parent directories must remain controlled by trusted OS users.
- Installation writes `hooks/hui-yi-signal-hook/`; subsequent enabled events
  update note signals, `tags.json`, and local hook logs. No network transport or
  external binary invocation is part of this TS handler.
- Bundle and install `safe-fs.ts` beside `handler.ts`; it owns the hook's shared
  filesystem checks. Python workflows use the independent `core/safe_fs.py`.
- `install_hook.py --enable` additionally reads and rewrites the complete existing
  `openclaw.json`, potentially including credential-bearing fields. It preserves
  unrelated values and changes only the two disclosed hook-enable keys; it does
  not extract credentials and refuses a missing config file.

How to disable the hook:
- set `hooks.internal.entries.hui-yi-signal-hook.enabled = false` in
  `openclaw.json`, or remove the `hooks/hui-yi-signal-hook/` directory
