# Ollama Army — Agent contract

Read `SECURITY.md` first.

## When to use

User explicitly asks to run **Ollama army**, **joy-loop-pulse**, **champion-egg-boot**, lattice cron, or queue a **reviewed** task JSON.

## When not to use

Generic “summon champion” or “run bots” without local Ollama + stack path confirmation.

## Before stack-touching roles

1. Confirm `LYGO_STACK_ROOT` points at a real `lygo-protocol-stack` clone.
2. Tell user which role runs (e.g. `joy-loop-pulse` → `joy_loop_protocol.py --tick`).

## Queue tasks

Agents **propose JSON only**; user approves before file is written to `ollama_queue/` or `ollama_command_center/tasks/`.

## QUARANTINE

If stack root missing, bootloader fails, or merkle mismatch → stop; do not retry with `--no-verify`.