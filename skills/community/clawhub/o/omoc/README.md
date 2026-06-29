# OMOC - Oh My OpenClaw

OpenClaw-native workflow suite inspired by Oh My Codex.

OMOC gives OpenClaw users familiar trigger phrases and a small runtime for
durable planning, persistent execution, non-overlapping hot loops, team fan-out,
memory compaction, and review gates:

- `/plan` for scoped planning and acceptance criteria
- `/ralplan` for Planner -> Architect -> Critic consensus planning
- `/ralph` for bounded persistence until verified completion
- `/neverstop` for lease-protected hot-loop recurrence
- `/team` for useful parallel lanes with integrated verification
- `/review` for code-review, plan-review, or completion-audit routing
- memory helpers for compact resumability across long work

## Why This Exists

Long-running agent work fails in two boring ways: it stops too early, or it runs
twice at the same time. OMOC is built around the middle path:

- every run is bounded and inspectable
- unfinished work reschedules quickly
- live leases prevent overlap
- blocked work backs off
- completion requires evidence
- worker context is summarized instead of stuffed with raw logs

It ports the useful semantics of OMX-style workflows into OpenClaw's native
model: isolated agent turns, cron/reschedule, state files, subagents/sessions,
and explicit review gates.

## Runtime

The helper script stores state under `.omoc/`:

```bash
python scripts/omoc.py compose init --objective "Ship X" --modes goal,ralplan,team,ralph
python scripts/omoc.py memory add --kind decision --text "..."
python scripts/omoc.py memory compact --max-events 50
python scripts/omoc.py goal init --brief "G001 implement\nG002 verify"
python scripts/omoc.py team init --name ship-x --task "Complete G001" --goal-id G001 --workers worker-1,verifier
python scripts/omoc.py team add-task --team ship-x --subject "Implement" --description "..." --role worker
python scripts/omoc.py team loop --team ship-x --goal-id G001
python scripts/omoc.py team gate --team ship-x --goal-id G001
python scripts/omoc.py ralph init --loop-id ship-x --objective "Drive ship-x to goal completion"
```

## Core Model

`/ralph /neverstop` should feel continuous without being one infinite process.

```text
read state
  -> if live lease exists: exit
  -> acquire lease
  -> run one bounded cycle
  -> verify/update state
  -> if unfinished: schedule next run soon
  -> release lease
stop
```

If the loop is waiting on external state, it backs off. If the lease is stale, a
later run may recover it only after recording evidence.

## Safety Defaults

- No external messages, deploys, spending, or public actions without explicit
  confirmation.
- No overlapping Ralph cycles for the same loop.
- No hidden `while true` loops.
- No completion claims without fresh evidence.
- Planning modes do not silently become implementation modes.

## Install

Install from ClawHub as `omoc` once published:

```bash
clawhub install omoc
```

## Local Development

This skill lives as `openclaw-ralph-suite` in the OpenClaw workspace, but is
published as `omoc` for a shorter public name.
