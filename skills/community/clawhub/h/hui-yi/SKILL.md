---
name: hui-yi
description: >
  Trigger for cold-memory recall and archive work under memory/cold/. Use only for
  explicit requests about older low-frequency context, historical continuity,
  resurfacing, cooling, rebuild, and repetition-driven reinforcement — not for any
  casual mention of words like "archive" or "remember". Do not use for fresh daily
  notes, stable high-frequency facts, tooling/setup notes, or unvalidated new
  learnings. Also covers an optional opt-in hook (installed via
  scripts/install_hook.py, enabled in openclaw.json only with --enable) that
  accumulates Session signals from recall-related turns into memory/cold/ notes
  and tags.json.
---

# Hui Yi

Hui Yi manages the cold reinforcement layer under `memory/cold/`.

Core rule:

**Repeatedly reactivated information deserves reinforcement first. Ebbinghaus sets the pace, not the sole trigger.**

## Use Hui Yi when

- older low-frequency context would materially improve the current answer
- the user asks what was done before, asks to recall/archive something, or wants historical continuity
- a reusable lesson, decision, troubleshooting result, or stable background note should be preserved in `memory/cold/`
- durable content from daily notes should be cooled into cold memory
- cold-memory notes, metadata, or retrieval quality need maintenance

## Do not use Hui Yi when

- the content is today's transient note → `memory/YYYY-MM-DD.md`
- the content is a stable high-frequency fact → `MEMORY.md`
- the content is tooling, machine path, or environment setup → `TOOLS.md`
- the content is a fresh mistake or still-unvalidated lesson → `.learnings/`
- the content contains secrets, tokens, or passwords

## Boundary

OpenClaw primary memory handles:
- current chat continuity
- recent daily notes
- stable high-frequency facts
- tooling and environment notes
- fresh learnings

Hui Yi handles:
- low-frequency, high-value knowledge under `memory/cold/`
- historical context that keeps resurfacing across real conversations
- durable experience, decisions, and troubleshooting notes that should not pollute primary memory

## Files and scripts

Cold-memory area:
- `memory/cold/index.md`
- `memory/cold/tags.json`
- `memory/cold/retrieval-log.md`
- `memory/cold/_template.md`
- `memory/cold/schedule.json`
- `memory/heartbeat-state.json`

CLI entry scripts:
- `scripts/create.py`
- `scripts/validate.py`
- `scripts/search.py`
- `scripts/rebuild.py`
- `scripts/decay.py`
- `scripts/cool.py`
- `scripts/review.py`
- `scripts/scheduler.py`
- `scripts/install_hook.py`
- `scripts/smoke_test.py`
- `scripts/scrub_metadata.py`

Core modules:
- `core/signal_detect.py`
- `core/signal_pipeline.py`
- `core/openclaw_signal_hook.py`
- `core/openclaw_runtime_probe.py`

## Disclosure

- Scripts create and modify persistent local files, but only under `memory/cold/`
  and `memory/heartbeat-state.json`. No network access, no credential access.
- The hook is optional and twice opt-in: `scripts/install_hook.py` copies files
  into `hooks/hui-yi-signal-hook/`, and only `--enable` flips the two
  `hooks.internal.*` keys in `openclaw.json` (after printing a disclosure; it
  refuses to create a missing config file).
- The enabled hook persists session signals as activation counters plus truncated
  sha256 session fingerprints — never raw session keys. Its `hook.log` by default
  contains no message bodies and no raw user/chat ids (set `HUI_YI_HOOK_DEBUG=1`
  for verbose diagnostics) and rotates at 256 KB.
- The cooling playbook's routing table (MEMORY.md, TOOLS.md, .learnings/,
  AGENTS.md, SOUL.md) is agent guidance; Hui-Yi scripts never write those files.

## Sanity check

```bash
python3 scripts/smoke_test.py
```
