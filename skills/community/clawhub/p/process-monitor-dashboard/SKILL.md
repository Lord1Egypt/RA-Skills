---
name: process-monitor-dashboard
description: Monitor system processes, resource usage, and performance metrics with real-time terminal dashboard.
version: 1.0.0
author: skill-factory
metadata:
  openclaw:
    requires:
      bins:
        - python3
      libs:
        - python3-psutil
---

# Process Monitor Dashboard

## What This Does

A real-time terminal dashboard for monitoring system processes and resource usage. Provides a live, updating view of CPU, memory, disk, network, and running processes—all within your terminal.

Key features:
- **Real-time CPU monitoring** - Overall usage + per‑core breakdown
- **Memory dashboard** - RAM usage, swap, detailed memory stats
- **Disk I/O & usage** - Read/write rates, free space per filesystem
- **Network activity** - Upload/download speeds, connections
- **Process list** - Top processes by CPU/memory, with sorting options
- **Refresh control** - Adjustable update interval (1–10 seconds)
- **Color‑coded alerts** - Highlight high resource usage
- **Lightweight** - Minimal overhead, runs in background

## How To Use

### Start the dashboard:
```bash
./scripts/main.py dashboard
```

### Monitor with custom interval (3 seconds):
```bash
./scripts/main.py dashboard --interval 3
```

### Get a single snapshot (no continuous updates):
```bash
./scripts/main.py snapshot
```

### List top N processes by CPU:
```bash
./scripts/main.py top --by cpu --limit 10
```

### List top N processes by memory:
```bash
./scripts/main.py top --by memory --limit 10
```

### Monitor a specific process by PID:
```bash
./scripts/main.py monitor --pid 1234
```

### Full command reference:
```bash
./scripts/main.py help
```

## Commands

- `dashboard`: Start interactive real‑time dashboard
  - `--interval`: Refresh interval in seconds (default: 2)
  - `--simple`: Simplified view (no per‑core/disk details)
  - `--log`: Also write metrics to a log file
  
- `snapshot`: Print a one‑time system snapshot
  - `--json`: Output as JSON for scripting
  
- `top`: Show top processes
  - `--by`: Sort by `cpu`, `memory`, `disk`, `name` (default: cpu)
  - `--limit`: Number of processes to show (default: 10)
  - `--user`: Filter by username
  - `--json`: Output as JSON
  
- `monitor`: Monitor a specific process
  - `--pid`: Process ID to monitor (required)
  - `--interval`: Refresh interval (default: 2)
  - `--watch`: Watch for process creation/termination
  
- `stats`: Show system‑wide statistics
  - `--cpu`: CPU details only
  - `--memory`: Memory details only
  - `--disk`: Disk details only
  - `--network`: Network details only
  - `--json`: Output as JSON
  
- `alert`: Check for resource alerts
  - `--threshold-cpu`: CPU alert threshold % (default: 90)
  - `--threshold-memory`: Memory alert threshold % (default: 85)
  - `--threshold-disk`: Disk alert threshold % (default: 90)

## Output Examples

### Dashboard view (sample):
```
─────────────────────────────────────────────────────
 System Monitor | Refresh: 2s | 2026‑03‑16 10:30:00 UTC
─────────────────────────────────────────────────────
CPU:  ███████░░░ 72%   Memory:  █████████░ 92% (8.2/12 GB)
Core 0: 65%  Core 1: 78%  Core 2: 70%  Core 3: 75%

Top Processes (by CPU):
   PID USER     CPU% MEM% COMMAND
  1234 alice    45.2 12.3 python3 /app/server.py
  5678 bob      22.1  5.8 /usr/bin/node index.js
  9101 root     10.5  0.3 systemd-journal

Disk: /  █████░░░░ 52% free   Network: ▲ 1.2 MB/s ▼ 4.5 MB/s
─────────────────────────────────────────────────────
```

### JSON snapshot (via `--json`):
```json
{
  "timestamp": "2026-03-16T10:30:00Z",
  "cpu": {
    "total_percent": 72.5,
    "per_core": [65.2, 78.1, 70.3, 75.0],
    "load_average": [1.2, 1.5, 1.8]
  },
  "memory": {
    "total_gb": 12.0,
    "used_gb": 8.2,
    "percent": 68.3,
    "swap_used_gb": 0.5
  },
  "processes": [
    {"pid": 1234, "name": "python3", "cpu_percent": 45.2, "memory_percent": 12.3}
  ]
}
```

## Installation Notes

Requires Python 3.6+ and `psutil` library. Install with:

```bash
pip install psutil
```

On most systems, `psutil` is available via package managers:

```bash
# Debian/Ubuntu
sudo apt install python3-psutil

# RHEL/CentOS
sudo yum install python3-psutil

# macOS
brew install psutil
```

## Limitations

- **Terminal size** - Dashboard optimized for terminals ≥ 80 columns
- **Refresh rate** - Very fast intervals (<1s) may cause high CPU
- **Platform support** - Best on Linux/macOS; Windows support limited
- **Process details** - Some process information may require root
- **Historical data** - No built‑in long‑term trending (single‑session only)
- **No remote monitoring** - Only monitors the local system
- **No alert actions** - Only displays warnings, doesn’t auto‑resolve issues

## Security Considerations

- Only reads system metrics (no writes or modifications)
- Doesn’t require root/sudo for basic operation
- No network listening or external connections
- All data stays local; no telemetry
- Process listing may reveal running applications (same as `ps`/`top`)

## Examples

### Basic dashboard (2‑second updates):
```bash
./scripts/main.py dashboard
```

### Lightweight dashboard (simple view, 3‑second updates):
```bash
./scripts/main.py dashboard --simple --interval 3
```

### Get a JSON snapshot for scripting:
```bash
./scripts/main.py snapshot --json > system.json
```

### Find top 5 memory‑hungry processes:
```bash
./scripts/main.py top --by memory --limit 5
```

### Monitor a specific web server:
```bash
./scripts/main.py monitor --pid $(pgrep -f "nginx") --interval 5
```

### Check for resource alerts:
```bash
./scripts/main.py alert --threshold-cpu 95 --threshold-memory 90
```