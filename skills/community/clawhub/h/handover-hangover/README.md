# Handover Hangover

**Seamless model handoff for [OpenClaw](https://openclaw.ai) agents.**

When your agent's primary model hits a rate limit and the gateway silently switches to a fallback, the new model inherits the conversation but not the context. It sees prior assistant messages as *its own*, hallucinates continuity, and may re-run irreversible commands. Handover Hangover fixes this.

## The problem

OpenClaw agents run on a fallback chain — when the primary model is unavailable, the gateway transparently routes to the next one. The conversation history survives, but:

1. **Hallucinated continuity** — treats the previous model's reasoning as its own
2. **Lost task details** — what was being edited, checked, what step comes next
3. **Lost cognitive mode** — was the agent researching, debugging, synthesizing?
4. **Scope collapse** — the task silently narrows ("analyze the past week" → "analyze this session")
5. **Tool state blindness** — risks re-running irreversible commands (duplicate messages, double commits)

## How it works

Handover Hangover is a **three-channel** OpenClaw skill (`always: true`) that uses layered defense to ensure handoff continuity even when one channel fails:

- **Channel 1: System prompt** (`SKILL.md`) — tells the model *what* to write and *when*
- **Channel 2: Filesystem** (`memory/handoff-note.md`, `memory/current-task.md`) — stores the handoff data
- **Channel 3: Bash watchdog** (`scripts/handoff.sh`) — ensures the data *exists*, even if the model didn't follow instructions. Idempotent — safe for boot, heartbeat, hooks, and cron. Requires explicit integration (see [Integration](#integration))

### Four responsibilities

**Write-side:** on every state-changing moment, the agent writes a structured handoff note to disk — extending OpenClaw's existing `memoryFlush` pattern.

**Detection:** the agent self-checks on every turn whether a model switch may have occurred, using three heuristic indicators. Biased toward false positives — better to re-read state than to assume continuity.

**Read-side:** when a handoff is detected, the incoming model reads the baton, performs an epistemic reset, verifies tool state, and continues work without asking "where were we?"

**Watchdog:** an idempotent bash script that checks whether a handoff note exists and generates a mechanical fallback if not. Safe for any execution frequency — repeated runs without a new note are no-ops. Wire it through the managed hook pack, boot sequence, heartbeat, or manual scheduler. See [Integration](#integration).

## Installation

Copy to your OpenClaw skills directory:

```bash
clawhub install handover-hangover
```

If your installer does not preserve executable bits, restore them:

```bash
chmod +x ~/.openclaw/workspace/skills/handover-hangover/scripts/*.sh
```

The prompt layer activates automatically (`always: true`). The watchdog script requires integration — run the installer below for the current OpenClaw hook system, or use the fallback snippets for older versions.

## Integration

OpenClaw skills are prompt-injected — `SKILL.md` gives the model the handoff protocol. Shell scripts do **not** run automatically just because a skill has `always: true`, so Handover Hangover ships multiple integration layers. They are intentionally redundant and version-tolerant.

### Recommended: managed hook installer

Run once after installing or updating the skill:

```bash
bash ~/.openclaw/workspace/skills/handover-hangover/scripts/install-integration.sh
```

What it does:

1. Copies a managed hook pack to `~/.openclaw/hooks/handover-hangover/`.
2. Copies `handoff.sh` next to the hook handler so it survives skill path/layout differences.
3. Enables the hook with `openclaw hooks enable handover-hangover` when the hooks CLI is available.
4. Prints fallback snippets for older OpenClaw versions.

Restart the Gateway after enabling hooks so the handler is loaded.

### Why the hook is `message:received`, not only `afterTurn`

OpenClaw hook APIs changed over time. Some versions expose command/startup hooks, some expose plugin-level `agent_end`, and older notes often mention ad-hoc `afterTurn` directories. To avoid binding the skill to one OpenClaw release, the shipped managed hook runs at **next-turn boundaries**:

- `message:received` — before the next model acts, so a switched-in model sees `.handoff-pending` before doing work.
- `command:new` / `command:reset` — explicit session boundaries.
- `gateway:startup` — process restarts and upgrades.

This gives the important guarantee: the incoming model checks the baton before it continues. It is provider/model agnostic and works across fallback chains, manual model changes, and Gateway restarts.

### Status check

```bash
bash ~/.openclaw/workspace/skills/handover-hangover/scripts/status.sh
```

This reports whether the watchdog is executable, whether the managed hook is installed, and whether OpenClaw has the hook enabled.

### Fallback: boot sequence

If hook discovery is unavailable, add this to `AGENTS.md`, after the existing boot steps:

```bash
# Handover Hangover — archive/generate baton for incoming model
WORKSPACE=~/.openclaw/workspace bash ~/.openclaw/workspace/skills/handover-hangover/scripts/handoff.sh
```

### Fallback: heartbeat / scheduler

Add to `HEARTBEAT.md`, cron, or any periodic scheduler:

```bash
# Handover Hangover — periodic baton validation
WORKSPACE=~/.openclaw/workspace bash ~/.openclaw/workspace/skills/handover-hangover/scripts/handoff.sh
```

The watchdog is idempotent. Running it at startup, before turns, on heartbeat, or manually is safe.

### What each layer covers

| Layer | Trigger | Covers |
|-------|---------|--------|
| `SKILL.md` (`always: true`) | Prompt context | Detection + write-side + read-side protocol |
| Managed hook pack | `message:received`, `/new`, `/reset`, startup | Next-turn baton archival/generation before the model acts |
| Boot sequence | Session start | Baseline baton check at session boundary |
| Heartbeat/scheduler | Periodic | Coarse repair if hooks are unavailable |
| Manual `handoff.sh` | Operator/model action | Emergency recovery and diagnostics |

## Requirements

- [OpenClaw](https://openclaw.ai) with a multi-model fallback chain configured
- At least one fallback model in `agents.defaults.model.fallbacks`
- The `context-anchor` skill installed (for read-side file scanning)
- Bash (for the watchdog script — available on all standard OpenClaw environments)

## What Handover Hangover is NOT

- **Not a memory framework** — it's a handoff protocol between interpreters of the same state
- **Not a replacement for compaction flush** — compaction handles "same model, shorter memory"; Handover Hangover handles "different model, same history"
- **Not semantic search** — vector/embedding memory is a separate layer
- **Not cross-session continuity** — that's `continuity`, `MEMORY.md`, and daily logs

## Design principles

- **Three-channel reliability.** System prompt (policy) + filesystem (state) + bash watchdog (enforcement). Each channel compensates for the others' failure modes. The prompt tells the model what to do; the filesystem stores the result; the watchdog ensures the result exists — from per-turn hooks to session boundaries (see [Integration](#integration)). Pattern borrowed from `context-anchor`.
- **Extend, don't invent.** Uses existing OpenClaw files and conventions (`memory/current-task.md`, `memory/YYYY-MM-DD.md`, `memoryFlush` pattern). The only new files are `memory/handoff-note.md` and `scripts/handoff.sh`.
- **Bias toward false positives.** Better to re-read state unnecessarily than to assume continuity that doesn't exist.
- **Low overhead when not switching.** Every turn performs a cheap baton check (one file read + author comparison). Same-model continuations early-exit without a full reboot; full read-side runs only on actual model change or fallback recovery. Write-side and watchdog run regardless but double as useful compaction insurance.

## Status

**v1.2.1** — hardens managed hook execution: direct shebang launch, executable-bit self-repair, and lower ClawHub scanner friction around shell execution.

## License

[MIT-0](LICENSE) &copy; 2026 Handover Hangover contributors
