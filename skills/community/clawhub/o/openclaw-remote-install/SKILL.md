---
name: openclaw-remote-install
version: "1.0.0"
description: |
  One-click remote OpenClaw deployment via SSH. Auto-detects OS and selects best method (Docker/Podman/npm). Use when: (1) Installing on VPS/cloud servers, (2) Automating multi-machine deployment, (3) Configuring models/channels/gateway post-install.
---

# OpenClaw Remote Install Skill

This skill handles remote installation and configuration of OpenClaw on remote servers via SSH with intelligent method selection and async execution support.

## Log Directory

All installation logs are automatically saved to:
```
~/.openclaw/remote-install-logs/<host>_<timestamp>/
```

Each installation creates:
- `install.log` - Main installation log with timestamps
- `install_output.log` - Raw command output
- `install.pid` - Background process PID (async mode)
- `install.status` - Installation status: running/success/failed/timeout

A symlink `latest` points to the most recent log directory.

## Supported Installation Methods

| Method | Description | Best For |
|--------|-------------|----------|
| `auto` (default) | Auto-detect best method based on OS | Most cases |
| `installer` | Official install.sh script | Standard Linux/macOS |
| `cli` | install-cli.sh (local prefix) | No system Node dependency |
| `npm` | npm install -g openclaw | Node 22+ already installed |
| `pnpm` | pnpm add -g openclaw | pnpm users |
| `docker` | Docker container | Containerized deployments |
| `podman` | Podman rootless container | Rootless environments |

## Usage

### Quick Start (Auto-detect)

```bash
./scripts/install_openclaw_remote.sh <host> <user> <key_path>
```

### Async Installation (Recommended for long-running installs)

```bash
# Run installation in background with progress monitoring
./scripts/install_openclaw_remote.sh <host> <user> <key_path> --async

# Monitor in real-time
tail -f ~/.openclaw/remote-install-logs/latest/install_output.log

# Check status
cat ~/.openclaw/remote-install-logs/latest/install_status
```

### With Password

```bash
./scripts/install_openclaw_remote.sh <host> <user> <password> --password-based
```

### Force Specific Method

```bash
# Docker installation
./scripts/install_openclaw_remote.sh <host> <user> <key_path> --docker

# Podman installation
./scripts/install_openclaw_remote.sh <host> <user> <key_path> --podman

# npm method (if Node 22+ available)
./scripts/install_openclaw_remote.sh <host> <user> <key_path> --method npm
```

### Non-interactive (Automation)

```bash
./scripts/install_openclaw_remote.sh <host> <user> <key_path> \
  --non-interactive \
  --configure
```

### Custom Log Directory

```bash
./scripts/install_openclaw_remote.sh <host> <user> <key_path> \
  --log-dir /path/to/custom/logs
```

## Auto-Detection Logic

The installer automatically selects the best method:

1. **If `--docker` or `--podman` flag**: Use container method (if available)
2. **If Node 22+ installed**: Use `pnpm` or `npm` method
3. **Otherwise**: Use official `install.sh` script

## Supported Operating Systems

- **Ubuntu/Debian** (apt)
- **Fedora/RHEL/CentOS** (dnf/yum)
- **Alpine** (apk)
- **Arch Linux** (pacman)
- **macOS** (Homebrew)
- **Windows** (WSL2) - via installer script

## Post-Installation

```bash
# SSH into remote server
ssh user@host

# Check status
openclaw status

# Run diagnostics
openclaw doctor

# Configure (models, channels, etc.)
openclaw configure

# Or use Python script for non-interactive config
python3 scripts/configure_openclaw_remote.py <host> <user> \
  --auth <key> --key-based --configure \
  --auth-choice openai-api-key --api-key "your-key"
```

## Configuration Options

### Auth Providers (via Python script)

- `openai-api-key` - OpenAI API
- `anthropic-api-key` - Anthropic API
- `custom-api-key` - Custom OpenAI-compatible endpoint
- `azure-openai` - Azure OpenAI
- `google-ai` - Google AI (Gemini)
- `mistral-api-key` - Mistral AI
- `zai-api-key` - Z.AI endpoints

### Secret Modes

- `plaintext` - Store directly in config (not recommended)
- `ref` - Environment variable reference (recommended)

### Gateway Modes

```bash
--gateway-mode local    # Local gateway (default)
--gateway-mode remote   # Remote gateway
--gateway-port 18789
```

## Environment Variables

For secure non-interactive configuration:

```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export CUSTOM_API_KEY="your-key"
```

Then use `--secret-mode ref` to reference them securely.

## Troubleshooting

### SSH Issues

```bash
# Check key permissions
chmod 600 ~/.ssh/id_rsa

# Add to ssh-agent
ssh-add ~/.ssh/id_rsa
```

### Installation Issues

- Ensure curl is installed
- Check Node.js 22+ requirement (for non-Docker methods)
- Review logs: `~/.openclaw/logs/`

### Docker Issues

```bash
# Check Docker status
docker ps

# View logs
docker logs openclaw

# Restart container
docker restart openclaw
```
