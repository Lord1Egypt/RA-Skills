---
name: native-scripts
description: Native OpenCLAW automation scripts for post-Docker setup. Heartbeat reports, watchdog monitoring, and cost tracking for OpenCLAW running natively on Ubuntu.
---

# Native Scripts for OpenCLAW

System automation scripts designed for OpenCLAW running natively without Docker containers. These scripts provide essential monitoring, reporting, and cost tracking capabilities.

## Overview

After migrating from Docker to native execution, these scripts replace the container-based automation stack with lightweight shell scripts and systemd integration.

## Included Scripts

### heartbeat.sh
Daily status report sent to Telegram at 18:00 UTC (7am NZDT).

Reports:
- Gateway process status
- Model in use
- Session count
- 24h and all-time costs
- System resources (disk, memory)
- Uptime

### watchdog.sh
Process monitor running every 5 minutes.

Checks:
- OpenCLAW gateway process health
- Logs status to ~/.openclaw/logs/watchdog.log
- Sends Telegram alert if gateway stops
- Auto-trims log file at 1000 lines

### cost-tracker.sh
Calculates usage costs from session JSONL files.

Features:
- Parses session files for token usage
- Calculates costs based on model pricing
- Supports 24h, today, or all-time periods
- JSON or text output formats

## Installation

1. Copy scripts to ~/openclaw/
2. Make executable: chmod +x ~/openclaw/*.sh
3. Install systemd timers (optional)
4. Configure Telegram bot token in ~/.openclaw/openclaw.json

## Requirements

- bash
- jq (for JSON parsing)
- bc (for calculations)
- curl (for Telegram API)
- systemd (for timers, optional)

## Configuration

Scripts read configuration from:
- ~/.openclaw/openclaw.json (Telegram token, model pricing)
- ~/.openclaw/.env (API keys)

## License

Private - For nz365guy use only
