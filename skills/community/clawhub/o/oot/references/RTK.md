# RTK Integration Guide

RTK and OOT solve different parts of the same token-cost problem:

- `OOT` reduces model cost, context bloat, heartbeat waste, and session budgeting.
- `RTK` reduces shell command output before it reaches the agent context.

Used together, they compound well.

## Install RTK

### Homebrew

```bash
brew install rtk
```

### Linux/macOS Quick Install

```bash
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh
```

### Cargo

```bash
cargo install --git https://github.com/rtk-ai/rtk
```

### Verify

```bash
rtk --version
rtk gain
```

### Initialize

For a general global setup:

```bash
rtk init -g
```

For Codex-oriented workflows:

```bash
rtk init -g --codex
```

If you are on native Windows, RTK can still be used explicitly, but its shell-hook experience is more limited than on Linux/macOS or WSL.

## When to Use RTK

Use RTK when your agent frequently runs verbose shell commands such as:

- `git status`, `git diff`, `git log`
- `rg`, `grep`, `find`, `ls`, `tree`
- `cargo test`, `pytest`, `npm test`, `go test`
- `docker logs`, `kubectl logs`

RTK is most valuable for command-heavy coding sessions where tool output is the main token drain.

## Recommended Split of Responsibilities

Use `OOT` for:

- choosing cheaper models for simple tasks
- reducing startup/context injection
- optimizing heartbeat intervals
- enforcing token budgets

Use `RTK` for:

- filtering command output
- collapsing repetitive logs
- shrinking test and lint output
- reducing `git` and filesystem command verbosity

## Example Combined Workflow

1. Use `model_router.py` to decide whether the task should stay on a cheap or balanced model.
2. Use `context_optimizer.py` to avoid loading unnecessary workspace files.
3. Run verbose shell tasks through `rtk` so the returned output is compressed before it reaches the model.
4. Use `token_tracker.py` to monitor whether the session is still within budget.

## Example Commands

```bash
# OOT decides the model tier
python3 scripts/model_router.py "review this git diff and summarize the failing tests"

# RTK shrinks shell output
rtk git diff
rtk cargo test
rtk grep "TODO" .
rtk read src/main.rs

# OOT checks budget impact
python3 scripts/token_tracker.py check
```

## OpenClaw Usage Pattern

If RTK is installed on the machine, prefer RTK-wrapped shell commands for large outputs:

```bash
rtk git status
rtk git diff
rtk rg "pattern" .
rtk pytest
```

For small outputs, normal commands are fine. For large or repetitive outputs, RTK should be preferred.

## Important Limitation

OOT does not bundle RTK, install RTK, or provide a native RTK hook/plugin inside this repository.

This repository supports RTK as an external companion tool by documenting the integration pattern and recommending RTK-wrapped commands where appropriate.

## Result

Best case combination:

- `OOT` cuts context and model waste
- `RTK` cuts shell-output waste

That is the correct way to support RTK here without pretending this repo contains RTK itself.
