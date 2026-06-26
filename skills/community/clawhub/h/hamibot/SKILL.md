---
name: hamibot
homepage: https://hamibot.com
metadata: {"clawdbot":{"emoji":"📱","requires":{"bins":["hamibot"]},"install":[{"id":"npm","kind":"npm","package":"hamibot/cli","bins":["hamibot"],"label":"Install hamibot (npm)"}]}}
description: |
  This skill should be used when working on the Hamibot CLI project — an open-source Node.js command-line tool for authorized remote Android automation.
  Devices must be explicitly paired and authorized by their owners via the Hamibot Android app. The CLI operates exclusively on the user's own authenticated account and paired devices.
  Trigger scenarios: installing Hamibot CLI, authenticating, executing code on devices, managing files,
  simulating touch input, capturing screenshots, launching apps, or querying device information.
---

# Hamibot CLI

Remote Android automation command-line tool. Connect to the Hamibot cloud API to control Android devices:
execute JavaScript code, manage files, simulate touch input, capture screenshots, launch apps, and query device info.

**Official site:** https://hamibot.com
**Repository:** https://github.com/hamibot/cli

## Security Model

Hamibot CLI is a legitimate remote automation tool with the following security properties:

1. **User-Authorized Device Access Only.** Devices must be explicitly paired by their owners through the Hamibot Android app. The CLI can only communicate with devices that the user has authorized and connected. There is no mechanism for unauthorized or stealth device access.

2. **Authenticated API.** Every CLI session requires authentication (interactive login or Personal Access Token). All API calls are made over HTTPS to the Hamibot cloud, which validates the user's identity and verifies that the target device belongs to the authenticated account.

3. **Scoped to User's Own Devices.** The CLI lists and operates exclusively on devices registered under the user's own account. It cannot discover or interact with devices belonging to other accounts.

4. **Standard Automation Capabilities.** The features (code execution, file management, input simulation, screenshots, app launching) are standard capabilities of authorized Android automation platforms. They are analogous to what `adb` (Android Debug Bridge) provides over a USB connection, but delivered via a cloud API for remote convenience.

5. **Open Source.** The CLI is fully open source at https://github.com/hamibot/cli, allowing anyone to audit its code, dependencies, and behavior.

**In summary:** Hamibot CLI is not a remote access trojan or unauthorized surveillance tool. It is a user-facing automation utility that operates strictly within the scope of the user's own authorized devices and account.

## Installation

### Prerequisites

- **Node.js >= 18** — check with `node --version`; install from https://nodejs.org/ (LTS recommended) or via [nvm](https://github.com/nvm-sh/nvm) / [fnm](https://github.com/Schniz/fnm)
- **npm** (bundled with Node.js)

### Install as Global CLI

```bash
npm install -g hamibot/cli
hamibot -v
```

### Install from Source

```bash
git clone https://github.com/hamibot/cli.git
cd cli
npm install
npm link
```

## Quick Start

```bash
# 1. Login (interactive prompt for phone/email + password)
hamibot login

# 2. List paired devices
hamibot devices

# 3. Execute code on device
hamibot exec -c 'toast("Hello from CLI!")'
```

## Authentication

### Interactive Login

```bash
hamibot login
```

### Token Login (recommended for CI/CD)

1. Create a Personal Access Token at https://hamibot.com/account/tokens
2. Login with the token:

```bash
hamibot login -t hmp_xxxxxxxxxxxx
```

## Global Options

Available on all commands:

| Flag | Purpose |
|------|---------|
| `-d, --device <id>` | Target device ID (repeatable for multi-device parallel) |
| `-j, --json` | Structured JSON output for piping and scripting |
| `--debug [namespace]` | Debug logging with optional namespace filter |

### Device Selection

Without `-d`, CLI auto-selects a device:
1. If a default device is configured → use it
2. If only one device paired → auto-select
3. Multiple devices → interactive prompt (enter `0` to select all)

### Multi-Device Parallel

```bash
hamibot input tap 500 500 -d device-A -d device-B
```

## Commands Reference

### Code Execution

```bash
hamibot exec -c 'toast("Hello!")'
hamibot exec -f ./script.js
echo 'toast("Hello!")' | hamibot exec
```

### File Management

```bash
hamibot file ls                          # List /sdcard
hamibot file ls /sdcard/Download
hamibot file download /sdcard/file.png    # Download to current dir
hamibot file download /sdcard/file.png ./local.png
hamibot file upload ./local.txt /sdcard/
hamibot file cat /sdcard/log.txt
```

### Input Control

```bash
hamibot input tap 500 500
hamibot input click 500 500              # alias
hamibot input longtap 500 500
hamibot input longtap 500 500 --duration 1000
hamibot input swipe 500 1500 500 500 --duration 300
hamibot input gesture 500 100 200 300 400 500 600 700
```

### Launch App

```bash
hamibot launch com.example.app
hamibot launch com.example.app --activity .MainActivity
```

### Device Management

```bash
hamibot devices                          # List all devices
hamibot devices info <deviceId>
hamibot devices online                   # Check online status
```

### Run Saved Script

```bash
hamibot run <scriptId>
```

### Configuration

```bash
hamibot config defaultDevice <id>        # Set default device
hamibot config defaultDevice --get       # Get config value
hamibot config --reset                   # Clear all config
```
