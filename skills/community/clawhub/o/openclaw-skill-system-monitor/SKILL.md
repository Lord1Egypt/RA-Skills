---
name: system-monitor
description: "Real-time system metrics monitoring (CPU, memory, disk, network, processes). Use when: user asks to check system status, cpu usage, memory usage, disk space, network traffic, running processes, or system performance. Supports macOS and Linux. Tools: top, htop, df, iostat, vm_stat, host, free, lsof, uptime."
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins:
        - top
        - df
        - vm_stat
        - free
        - lsof
        - uptime
---

# System Monitor Skill

Monitor real-time system metrics including CPU, memory, disk, network, and processes.

## When to Use

✅ **USE this skill when:**

- "Check system status"
- "CPU usage" / "How's the CPU doing?"
- "Memory usage" / "RAM usage"
- "Disk space" / "How much storage left?"
- "Network traffic" / "Network usage"
- "Running processes" / "Top processes"
- "System performance" / "System load"

## Setup

Some tools may need installation via Homebrew:

```bash
# Install optional enhanced tools
brew install htop      # Enhanced top (better UI)
brew install nettop    # Real-time network monitoring (macOS)
brew install iostat    # I/O statistics (Linux)
```

## Platform Detection

Detect the platform to use appropriate commands:

```bash
uname -s  # Darwin = macOS, Linux = Linux
```

## CPU Usage

### macOS

```bash
# CPU usage summary (user, system, idle)
top -l 1 -n 0 | grep "CPU usage"

# Detailed per-core usage
top -l 2 -n 0 | tail -1

# Overall CPU percentage
vm_stat | head -5
```

### Linux

```bash
# CPU usage summary
top -bn1 | head -5

# Detailed per-core
mpstat -P ALL 1 1

# Overall
uptime
```

### One-liner (cross-platform friendly)

```bash
# macOS
top -l 1 -n 0 -s 0 | awk '/CPU usage/ {print}'

# Linux  
top -bn1 | grep "Cpu(s)"
```

### JSON-friendly (scripting)

```bash
# macOS: CPU stats with specific fields
top -l 1 -n 0 -s 0 -stats pid,pcpu,pmem,comm
```

## Memory Usage

### macOS

```bash
# Memory info (page size, pages active, wired, compressed, free)
vm_stat

# Human-readable summary
top -l 1 -n 0 | grep "PhysMem"

# Full memory details
hostinfo | grep "memory"
```

### Linux

```bash
# Human-readable
free -h

# Detailed in MB
free -m

# Swap info
swapon -s
```

### Memory Calculation (macOS)

```bash
# Calculate used memory from vm_stat
vm_stat | awk '/Pages active/ {active=$3} /Pages wired/ {wired=$3} /Pages free/ {free=$3} END {print "Active: " active " Wired: " wired " Free: " free}'
```

## Disk Space

### macOS & Linux

```bash
# All filesystems, human-readable
df -h

# Specific volume (macOS)
df -h /

# Linux root
df -h /

# Show inode usage (Linux)
df -i

# Sorted by usage (macOS)
df -h | sort -k5 -h

# Only local filesystems
df -h -t local
```

## Disk Usage (directory-level)

```bash
# Current directory (macOS)
du -sh .

# Top-level directories
du -h --max-depth=1

# Linux sorted by size
du -h --max-depth=1 | sort -h
```

## Network Statistics

### macOS

```bash
# Network interfaces (use ifconfig instead)
ifconfig -a

# Active connections
lsof -i -n | head -20

# Listening ports
lsof -i -n | grep LISTEN

# Real-time network usage
nettop -P -L 1 -J bytes_in,bytes_out
```

### Linux

```bash
# Interface statistics
ip -s link

# TCP/UDP stats
ss -s

# Active connections
ss -tunap
```

## Process List

### macOS

```bash
# Top processes by CPU
top -o cpu -l 1 -n 15

# Top processes by memory
top -o mem -l 1 -n 15

# All processes
ps aux

# User processes
ps -U $(whoami)
```

### Linux

```bash
# Top processes by CPU
top -bn1 | head -12

# Top by memory
top -bo %MEM -bn1 | head -12

# Process tree
pstree

# User processes
ps -U $(whoami) --sort=-%mem
```

## System Load

### macOS

```bash
# Load average
uptime

# Detailed
hostinfo | grep "load"
```

### Linux

```bash
uptime
# or
cat /proc/loadavg
```

## Combined System Status

### Quick Health Check

```bash
# CPU, Memory, Disk in one view (macOS)
echo "=== CPU ===" && top -l 1 -n 0 | grep "CPU usage"
echo "=== Memory ===" && top -l 1 -n 0 | grep "PhysMem"
echo "=== Disk ===" && df -h / | tail -1

# Linux
echo "=== CPU ===" && top -bn1 | head -5
echo "=== Memory ===" && free -h
echo "=== Disk ===" && df -h /
echo "=== Load ===" && uptime
```

## Bundled Scripts

### system-stats.sh

A combined system stats script for quick health checks:

```bash
#!/bin/bash
# Combined system stats - run from skills/system-monitor/scripts/

PLATFORM=$(uname -s)

echo "=== System Stats ==="
echo "Time: $(date)"
echo "Platform: $PLATFORM"
echo ""

if [ "$PLATFORM" = "Darwin" ]; then
    echo "--- CPU ---"
    top -l 1 -n 0 -s 0 | grep "CPU usage"
    echo ""
    
    echo "--- Memory ---"
    top -l 1 -n 0 | grep "PhysMem"
    vm_stat | head -5
    echo ""
    
    echo "--- Disk ---"
    df -h / | tail -1
    echo ""
    
    echo "--- Load Average ---"
    uptime
else
    echo "--- CPU ---"
    top -bn1 | head -5
    echo ""
    
    echo "--- Memory ---"
    free -h
    echo ""
    
    echo "--- Disk ---"
    df -h / | tail -1
    echo ""
    
    echo "--- Load Average ---"
    uptime
fi
```

## Notes

- macOS uses `vm_stat` for memory, Linux uses `free`
- `top` output format differs between platforms
- Use `hostinfo` on macOS for system overview
- Use `lsof` or `nettop` instead of deprecated `netstat`
- For continuous monitoring, use `watch` command or run `top` in loop
