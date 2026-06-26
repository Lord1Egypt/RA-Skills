---
name: macvital
description: |
  Check macOS hardware health: CPU usage, RAM pressure, disk space, temperatures, and top processes. Returns a quick status summary or full breakdown.

  USE WHEN: User or agent wants to know if the Mac is under load, running hot, low on disk, or RAM-constrained. Also use before spawning heavy tasks to check if the machine has headroom, or when diagnosing performance issues.

  DON'T USE WHEN: User asks about network speed, battery health (use a battery-specific tool), or remote machine health.
---

# macvital

macOS hardware health monitor. Checks CPU, RAM, disk, temperature, and top resource hogs.

## Requirements

- Python 3 (pre-installed on macOS)
- Script: `scripts/macvital.py`
- Temperature data requires `sudo` (Apple Silicon only)

## Commands

```bash
# Quick one-line status (good/warn/critical with icons)
python3 scripts/macvital.py status
python3 scripts/macvital.py status --json   # machine-readable

# Full breakdown
python3 scripts/macvital.py detail

# Top CPU and RAM processes
python3 scripts/macvital.py top
python3 scripts/macvital.py top --n 10

# Temperature only (more accurate with sudo)
python3 scripts/macvital.py temp
sudo python3 scripts/macvital.py temp

# Exit code check (for scripting: 0=ok, 1=warn, 2=critical)
python3 scripts/macvital.py check

# Continuous monitoring
python3 scripts/macvital.py watch
python3 scripts/macvital.py watch --interval 10
```

## Thresholds

| Metric | Warn | Critical |
|--------|------|----------|
| CPU    | 70%  | 90%      |
| RAM    | 75%  | 90%      |
| Disk   | 80%  | 90%      |
| Temp   | 80°C | 95°C     |

## Typical Use (agent workflow)

```bash
# Before a heavy task
python3 scripts/macvital.py check
# exit 0 = safe to proceed, exit 1/2 = consider waiting

# Quick heartbeat line
python3 scripts/macvital.py status

# Diagnosing slowness
python3 scripts/macvital.py detail
python3 scripts/macvital.py top
```
