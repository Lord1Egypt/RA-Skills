# Kimi Usage Monitor

A lightweight skill for monitoring Kimi K2.5 API usage and making autonomous resource decisions.

## Features

- 📊 Real-time usage monitoring from Kimi console
- 🟢🟡🔴 Capacity-aware decision making
- ✈️ Pre-flight checks for intensive operations
- 🤖 Subagent spawn guards
- 📈 JSON output for automation
- 💻 Cross-platform (Linux, macOS, Windows/WSL)

## Requirements

- Python 3.8+
- OpenClaw with browser control enabled
- Chrome with OpenClaw extension attached
- Active Kimi account session

## Platform Support

| Platform | Command | Status |
|----------|---------|--------|
| Linux | `./check_usage.sh` | ✅ |
| macOS | `./check_usage.sh` | ✅ |
| Windows (WSL) | `./check_usage.sh` | ✅ |
| Windows (Native) | `check_usage.bat` | ✅ |
| Windows (PowerShell) | `.\check_usage.ps1` | ✅ |

See [PLATFORM_SUPPORT.md](PLATFORM_SUPPORT.md) for detailed compatibility information.

## Quick Start

```bash
# Check current usage (Linux/macOS/WSL)
./check_usage.sh

# Check current usage (Windows CMD)
check_usage.bat

# Check current usage (Windows PowerShell)
.\check_usage.ps1

# Get JSON output for scripts
python3 scripts/fetch_usage.py --json

# Check before intensive work
python3 scripts/preflight_check.py intensive

# Check before spawning subagent
python3 scripts/subagent_guard.py
```

## Decision Thresholds

| Remaining | Status | Recommended Action |
|-----------|--------|-------------------|
| >50% | 🟢 | Full operations, subagents OK |
| 25-50% | 🟡 | Batch tasks, sparse subagents |
| <25% | 🔴 | Essential only, no subagents |

## Pre-Flight Operation Types

| Type | Min Capacity | Use Case |
|------|--------------|----------|
| `light` | 10% | Single queries, simple tasks |
| `standard` | 25% | Normal research, one subagent |
| `intensive` | 50% | Deep research, multi-subagent |

## Automation Example

```python
import subprocess

# Check before spawning
result = subprocess.run(
    ["python3", "scripts/subagent_guard.py"],
    capture_output=True,
    text=True
)

data = json.loads(result.stdout)
if data["can_spawn"]:
    # Safe to spawn subagent
    spawn_subagent("Complex research task...")
else:
    # Defer to later
    queue_task("Research task", priority="high")
```

## Files

- `SKILL.md` - Full documentation
- `check_usage.sh` - Quick usage check
- `scripts/fetch_usage.py` - Main scraper
- `scripts/usage_logger.py` - Logging + decisions
- `scripts/preflight_check.py` - Operation validation
- `scripts/subagent_guard.py` - Subagent quota check

## License

MIT
