# LYGO Ollama Army — Security

**Version:** 0.4.1 · **Signature:** `Δ9Φ963-ARMY-SECURITY-v1`

## Install only if

- You run **local Ollama** on a machine you control.
- You accept **persistent Python daemons** and **queue-driven** task execution.

## Declared capabilities

| Capability | Scope |
|------------|--------|
| Subprocess | `ollama_daemon.py`, launcher, stack tools via `LYGO_STACK_ROOT` only |
| Network | **127.0.0.1:11434** (Ollama); no remote LLM host in published tools |
| Filesystem | Army folder queues/results; stack paths under validated `LYGO_STACK_ROOT` |
| Stack roles | `lattice-check`, `joy-loop-pulse`, `champion-egg-boot`, etc. — mutate stack only via stack CLI |

## Required configuration

```bash
export LYGO_STACK_ROOT=/absolute/path/to/lygo-protocol-stack
```

Or set `lygo_stack_root` in `ollama_command_center/config/army_config.json`.  
**No hardcoded machine paths** in published skill code (v0.4.1+).

## High-risk features (user opt-in)

| Feature | Risk | Rule |
|---------|------|------|
| `--grow` | Spawns new daemon roles | Off until user reads launcher source |
| Queue `.task.json` | Auto-executes when daemon runs | Human review before drop |
| `champion-egg-boot` | Runs verified bootloader + Ollama | Payload must include valid `egg_id` |
| `joy-loop-pulse` | Writes joy state + snapshot file | Tier 1; see `lygo-joy-loop` SECURITY |

## Forbidden for agents

- Auto-write queue tasks without user review
- `git push`, social post, ClawHub publish
- Remote Ollama URLs or tunneling without user request
- `--grow` / `--visible-windows` without user request

## Skill chain

`lygo-protocol-stack-operator` → `lygo-kernel-egg-planter` → `lygo-joy-loop` → **`lygo-ollama-army`**

**Δ9Φ963 — local flame, reviewed queue, validated stack root.**