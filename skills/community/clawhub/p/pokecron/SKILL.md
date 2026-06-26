---
name: pokecron
description: "Power-user scheduler that creates persisted OS-native timers (systemd/launchd/Task Scheduler) which later run user-configured argv command hooks (`--pre-cmd`, `--post-cmd`, `--on-pong-command`, `--if-unconfirmed-command`) and agent prompts under your user account, without a daemon. Also ships an opt-in `--apply` migration helper that rewrites the OpenClaw config (with a timestamped backup) to disable native heartbeat polling, and an opt-in vector-tone mode that POSTs intent text to `OLLAMA_URL` (loopback-only unless `POKE_ALLOW_REMOTE_OLLAMA=1`). Reply-aware with escalation and quiet hours. Use for time-based requests — \"remind me\", \"wake me\", \"every morning\", \"keep poking until I reply\". *Linux only for now; mac coming VERY soon. Windows eventually.*"
version: 1.0.3
metadata:
  openclaw:
    requires:
      bins: [node]
    capabilities:
      filesystem: "Reads and writes reminder state, history, and hook logs under the skill's .runtime/ directory. Path sets and --task prompts may reference user-specified file paths."
      process: "Creates OS scheduler entries (systemd/launchd/Task Scheduler) and runs user-configured command hooks (--pre-cmd/--post-cmd/--on-pong-command/--if-unconfirmed-command) via execFileSync at fire time."
      environment: "Hooks receive a minimal env (PATH, HOME, USER, LOGNAME, SHELL, LANG, LC_ALL, TZ) plus POKE_* vars. Additional parent vars only via opt-in --hook-env."
      network: "None by default. Optional vector-tone matching (--vector-tones) sends tone/intent text to OLLAMA_URL (loopback-only unless POKE_ALLOW_REMOTE_OLLAMA=1)."
      migration: "Optional one-shot helper (scripts/heartbeat-to-poke.sh --apply) rewrites the OpenClaw config to disable native heartbeat polling; only runs with --apply and writes a timestamped backup first."
---

# Poke

## When to Use

Use `poke` for reminders, alarms, recurring nudges, deferred agent work,
reply-driven escalation, and reminder side effects such as scripts that
start before delivery or stop when the user replies.

## Core Workflow

1. Classify the poke style from the user's request.
2. Read the matching `sub-skills/*.md` file before building the command.
3. Check for an existing matching reminder before creating a duplicate.
4. Use `--dry-run` for unfamiliar flag combinations.
5. Forward plausible user replies with `poke --reply`; read
   `sub-skills/replies.md` first when handling replies.

## Sub-skill Routing

| If making or handling... | Read first |
|---|---|
| Basic one-shot, exact-time, recurring reminders, or deferred tasks | `sub-skills/scheduling.md` |
| "Keep poking until I reply", escalation, rotating tones, heartbeat-style checks, unconfirmed followups, task intervals | `sub-skills/escalation.md` |
| Pre/post actions, side-effect scripts, wake lights, or stop-on-reply hooks | `sub-skills/stages.md` |
| User replies such as done, cancel, snooze, later, or ambiguous inbound messages | `sub-skills/replies.md` |
| Quiet hours, active hours, DND, urgent delivery, or "do not wake me" behavior | `sub-skills/quiet-hours.md` |
| Multiple channels, dependency chains, or per-channel visibility | `sub-skills/multi-channel.md` |
| Listing, showing, cancelling, history, stats, presets, tones, path sets, or state layout | `sub-skills/management.md` |
| Inferred promises like "I'll check on that tomorrow" without a precise fire time | `sub-skills/commitments.md` |
| Migrating OpenClaw heartbeat polling into scheduled poke tasks | `sub-skills/migration.md` |

## Notes

- `--remind` is for static reminder text.
- `--task` is for deferred agent work and needs `--agent`.
- `--channel` and `--target` identify where delivery and replies happen.
- Poke has no ears; inbound user messages must be forwarded explicitly.
- Command hooks (`--pre-cmd`, `--post-cmd`, `--on-pong-command`, `--if-unconfirmed-command`) execute real local programs under your user account at scheduled time — only configure hooks with scripts you wrote or explicitly trust.
