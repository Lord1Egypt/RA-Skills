# max-throughput

An [Agent Skills](https://agentskills.io) compatible skill that makes coding
agents (Cursor, Codex, Claude Code, ...) stop running your expensive machine
single-threaded.

**The problem it solves:** agents happily execute `python train.py` on an
8-GPU box and `pytest` on a 128-core workstation, one thing after another.
The default objective becomes *minimum wall-clock completion time*: probe the
hardware, build a work DAG, and dispatch everything concurrently - agent-level
parallelism, multi-GPU DDP, per-GPU experiment packing, `pytest -n auto`,
`make -j$(nproc)` - then verify utilization and escalate parallelism if
resources sit idle.

## Install

With the [skills CLI](https://skills.sh) (works for Cursor, Codex, Claude Code
and more):

```bash
# pick your agent with -a, repeat to install for several at once
npx skills add Promethe-us/max-throughput -g -a cursor
npx skills add Promethe-us/max-throughput -g -a codex
```

Manual install: copy this folder into your agent's skill directory, e.g.

```
~/.cursor/skills/max-throughput/
~/.codex/skills/max-throughput/     (or reference via AGENTS.md)
~/.claude/skills/max-throughput/
```

## What the agent will do differently

| Before | After |
|---|---|
| `python train.py` on 8 GPUs | `torchrun --standalone --nproc_per_node=8 train.py` |
| experiments queued one by one | experiments packed one per GPU via `CUDA_VISIBLE_DEVICES` |
| `pytest` | `pytest -n auto` |
| `make` | `make -j$(nproc)` |
| serial preprocessing loop | sharded inputs via multiprocessing / GNU parallel |
| guesses a knob when slow | profiles first (`quick_triage.py`, py-spy, torch.profiler), then tunes the measured bottleneck: batch size, num_workers, prefetch, pre-encode, AMP/compile |
| never checks anything | runs `scripts/inspect_resources.py`, then `nvidia-smi` / `top` to confirm the machine is actually saturated |

## Structure

```
max-throughput/
├── SKILL.md                        # the skill itself (name + description + instructions)
├── scripts/
│   ├── inspect_resources.py        # cross-platform probe: CPU/RAM/GPU/disk + recommended plan
│   ├── inspect_resources.sh        # Linux/macOS shell alternative
│   └── quick_triage.py             # samples a running job, classifies the bottleneck, suggests knobs
└── references/
    ├── profiling.md                # profiling ladder: triage -> dataloader bench -> py-spy -> torch.profiler -> nsys
    ├── tuning-playbook.md          # batch size, DataLoader workers, pre-encode decisions, AMP/compile
    ├── pytorch.md                  # DDP / FSDP / DataLoader tuning / under-utilization triage
    ├── cpu-parallelism.md          # builds, pytest-xdist, preprocessing, downloads
    └── experiment-packing.md       # scheduling J independent jobs onto G GPUs
```

The resource probe is dependency-free (Python standard library, optional
`psutil`); run it yourself:

```bash
python scripts/inspect_resources.py
```

## Making it truly "every time"

A skill is pulled in when the model deems it relevant. To make throughput the
permanent default, also add one line to your global agent instructions:

- **Cursor**: Settings -> Rules -> User Rules
- **Codex**: `~/.codex/AGENTS.md`
- **Claude Code**: `~/.claude/CLAUDE.md`

```text
PERFORMANCE DEFAULT:
Optimize primarily for minimum wall-clock completion time. Before
long-running compute, inspect available CPU/GPU resources and parallelize
independent work aggressively. Do not default to single-process or
single-GPU execution when safe parallelism is available. Verify actual
utilization after launch and correct avoidable under-utilization.
```

## License

MIT
