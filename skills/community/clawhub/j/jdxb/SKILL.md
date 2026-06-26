---
name: jdxb
description: Manage 节点小宝 (Node Baby Link / JDxB) remote access service on Linux. Install, start/stop/restart the systemd service, check status, view logs, get pairing codes, update, and uninstall. Triggers on mentions of 节点小宝, jdxb, node baby link, remote access proxy, or port 9118.
---

# 节点小宝 (JDxB) Management

## Quick Commands

Use the bundled script for all operations:

```bash
bash skills/jdxb/scripts/jdxb.sh <command>
```

| Command | Description |
|---------|-------------|
| `status` | Show service status, version, and pairing info |
| `start` | Start the service |
| `stop` | Stop the service |
| `restart` | Restart the service |
| `logs` | View recent journal logs |
| `pair` | Get current pairing URL and active code |
| `install` | First-time install (downloads from CDN) |
| `update` | Update to latest version |
| `uninstall` | Stop service and remove files |

## Installation

Requires root. First-time install:

```bash
sudo bash skills/jdxb/scripts/jdxb.sh install
```

Or use the official one-liner:

```bash
curl -sL https://iepose.com/install.sh | sudo bash
```

## Service Details

- **Service name**: `owjdxb.service`
- **Default port**: 9118
- **Install dir**: `~/owjdxb/`
- **Working dir**: `/home/skipper/owjdxb/`
- **Logs**: `/tmp/.owjdxb/` and `journalctl -u owjdxb.service`

## Pairing

After install/start, the script waits up to 30s for the service to generate a pairing URL. The URL contains an active code for the 节点小宝 mobile app. To get the pairing code at any time:

```bash
bash skills/jdxb/scripts/jdxb.sh pair
```

The script automatically extracts the active code from the pairing server.

## Web Dashboard

Access at `http://127.0.0.1:9118` (local only). The service redirects to the pairing page on first access.
