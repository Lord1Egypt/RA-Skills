# system-monitor

Real-time system metrics monitoring skill for OpenClaw/Codex.

## Description

Monitor CPU, memory, disk, network, and processes using native CLI tools. Cross-platform (macOS & Linux).

## Features

- CPU usage monitoring
- Memory stats (vm_stat for macOS, free for Linux)
- Disk space and usage
- Network statistics
- Process list
- System load average

## Installation

### Via ClawHub
```bash
clawhub install ppopenbot/openclaw-skill-system-monitor
```

### Manual
```bash
git clone https://github.com/ppopenbot/openclaw-skill-system-monitor.git
# Copy to your skills directory
```

## Usage

Trigger phrases:
- "Check system status"
- "CPU usage"
- "Memory usage"  
- "Disk space"
- "Network traffic"
- "Top processes"

## Requirements

- `top` - CPU/process monitoring
- `vm_stat` - macOS memory stats
- `free` - Linux memory stats
- `df` - Disk space
- `lsof` - Network connections (macOS)
- `ip`, `ss` - Network stats (Linux)

## Platform

- macOS (Darwin)
- Linux

## License

MIT
