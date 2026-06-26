# OpenClaw Cost Tracker

[![ClawHub](https://img.shields.io/badge/ClawHub-openclaw--cost--tracker-blue)](https://clawhub.ai/pfrederiksen/openclaw-cost-tracker)
[![Version](https://img.shields.io/badge/version-1.1.1-green)]()

An [OpenClaw](https://openclaw.ai) skill for analyzing token usage and API costs from local session data. The preferred workflow now uses `openclaw-cost-diff` for current analysis and window-over-window comparisons, with the older `cost_tracker.py` kept as a fallback.

## Features

- 💰 **Cost diffs across time windows** via `openclaw-cost-diff`
- 🧭 **Breakdowns by model, agent, and channel**
- 📊 **Window-over-window regression detection**
- 📄 **JSON output** for integrations and dashboards
- 🧰 **Legacy fallback** with `cost_tracker.py` for the older single-window summary format

## Installation

```bash
clawhub install openclaw-cost-tracker
```

## Usage

```bash
# Preferred local wrapper
/root/.openclaw/workspace/tools/ocost --last 7d --prev 7d --top 5

# Direct diff tool invocation
/root/.openclaw/venvs/openclaw-cost-diff/bin/openclaw-cost-diff --data /root/.openclaw/agents --last 7d --prev 7d

# JSON output
/root/.openclaw/venvs/openclaw-cost-diff/bin/openclaw-cost-diff --data /root/.openclaw/agents --last 7d --prev 7d --json

# Legacy fallback
python3 scripts/cost_tracker.py --days 7
```

## Security

**Minimal and transparent.** The bundled fallback script is plain Python source, and the preferred diff workflow uses a separately installed CLI. Keep both repo and skill text-only and auditable.

**No hidden payloads.** This skill README and SKILL.md are plain text only.

**Run as non-root when possible.** The analysis only needs read access to local session data.

You can still audit the fallback script source at [scripts/cost_tracker.py](scripts/cost_tracker.py).

## Requirements

- OpenClaw installed with session data in `~/.openclaw/agents/`
- Python 3.8+

## License

MIT

## Links

- [ClawHub](https://clawhub.ai/pfrederiksen/openclaw-cost-tracker)
- [OpenClaw](https://openclaw.ai)
- [Full source](scripts/cost_tracker.py)
