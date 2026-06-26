---
name: openclaw-doctor
description: "Comprehensive OpenClaw health diagnostics and auto-repair. Checks gateway, services, memory, cron, channels, disk, logs, and security. Auto-fixes common issues. Works on macOS and Linux. Use when: system feels slow, cron jobs fail, gateway won't start, channels disconnect, or for routine health checks."
version: 1.0.0
author: 管家 (AI Butler)
---

# OpenClaw Doctor

A comprehensive health diagnostic and auto-repair skill for OpenClaw installations. Goes far beyond `openclaw doctor` with deep checks and automatic fixes.

## When to Use

- System feels slow or unresponsive
- Cron jobs failing or not running
- Gateway won't start or keeps crashing
- Channels (Telegram/WhatsApp) disconnected
- Routine health checks (add to heartbeat)
- After system restart or power outage
- Before and after upgrades

## Quick Start

Ask your agent: "Run a full health check" or "Diagnose my OpenClaw setup"

The agent will execute `scripts/diagnose.sh` and interpret results.

## What It Checks

### 1. Gateway Health
- Process running and responsive
- Port reachable and latency
- LaunchAgent/systemd service status
- KeepAlive and auto-restart configured
- Auth token strength

### 2. System Resources
- CPU load vs core count
- Memory usage and swap pressure
- Disk space (warn at 80%, critical at 90%)
- Log file sizes (detect bloat)

### 3. Service Resilience
- Auto-boot on power restore (macOS)
- Auto-restart after crash
- Sleep settings (servers should never sleep)
- Node.js path validity (survives upgrades?)

### 4. Cron & Automation
- All cron jobs status
- Failed job detection
- Stale jobs (not run in 2x their interval)
- Session count and context usage

### 5. Channel Health
- Each channel connectivity
- Last message timestamps
- Auth token validity

### 6. Security
- Config file permissions (should be 600)
- Gateway token strength
- Exposed ports check
- Workspace file permissions

### 7. Memory & Storage
- Memory file count and total size
- Stale daily logs (>30 days)
- Backup status and recency
- Vector index health

## Auto-Fix Capabilities

The script can automatically fix:
- Restart crashed gateway
- Fix file permissions
- Rotate oversized logs
- Clear stale session data
- Restart disconnected channels

## Usage

```bash
# Full diagnostic (read-only)
bash scripts/diagnose.sh

# Diagnostic with auto-fix
bash scripts/diagnose.sh --fix

# Quick check (essential items only)
bash scripts/diagnose.sh --quick
```

## Integration with Heartbeat

Add to your HEARTBEAT.md for periodic checks:
```
## System Health (every heartbeat)
Run: bash scripts/diagnose.sh --quick
Alert if any FAIL items found
```

## Platform Support
- macOS (primary, fully tested)
- Linux (systemd-based, tested)
- Windows WSL (basic support)
