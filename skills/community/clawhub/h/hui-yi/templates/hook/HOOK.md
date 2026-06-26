---
name: hui-yi-signal-hook
description: "Trigger Hui-Yi session signal accumulation on likely cold-memory / recall turns"
metadata:
  { "openclaw": { "emoji": "🧠", "events": ["message:preprocessed"] } }
---

# Hui-Yi Signal Hook

Workspace hook prototype for Hui-Yi.

Purpose:
- listen on `message:preprocessed`
- prefer explicit Hui-Yi skill-hit metadata when available
- fall back to conservative Hui-Yi / recall / historical-continuity intent detection only when explicit skill-hit metadata is absent
- run the same conservative signal detection and weak-activation writeback inline
- update `memory/cold/` note `Session signals` and `memory/cold/tags.json` without invoking external binaries

This hook is intended as the minimal stable OpenClaw-side integration prototype.

## What this hook persists (privacy)

Note files and `tags.json` under `memory/cold/`:
- per-note activation counters (`Session signals`) and `last_activated` dates
- session identity only as a truncated `sha256:` fingerprint — raw session keys,
  user ids, and chat ids are never written

`hooks/hui-yi-signal-hook/hook.log` (default mode):
- only `triggered` / `completed` / `pipeline_error` stages
- no message bodies or previews, no raw scope/thread identifiers; scope identity
  appears only as the hashed `sessionHash`
- the log self-rotates at 256 KB (keeps the most recent ~128 KB)

Debug mode (`HUI_YI_HOOK_DEBUG=1`, off by default):
- additionally logs `alive` / `skipped` stages, raw event metadata, raw scope and
  thread ids, and up-to-200-character body previews
- intended for short local troubleshooting sessions only; unset the variable and
  delete `hook.log` when done

How to disable the hook:
- set `hooks.internal.entries.hui-yi-signal-hook.enabled = false` in
  `openclaw.json`, or remove the `hooks/hui-yi-signal-hook/` directory
