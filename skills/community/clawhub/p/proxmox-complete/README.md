# Proxmox Complete Skill

Comprehensive Proxmox VE management for OpenClaw.

## What It Does

- **Power Control**: Start, stop, reboot, shutdown VMs and containers
- **Snapshots**: Create, list, delete, rollback (with optional RAM state)
- **Backups**: List and create backups
- **Storage**: View storage pools and content
- **Tasks**: Track async operations and logs
- **Cluster Overview**: Nodes, resources, health stats

## Setup

### Option 1: OpenClaw Credentials (Recommended)

Create `~/.openclaw/credentials/proxmox.json`:

```json
{
  "host": "your-proxmox-ip",
  "token_id": "clawd@pve!tokenname",
  "token_secret": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "verify_ssl": false
}
```

### Option 2: Environment Variables

```bash
export PVE_HOST="your-proxmox-ip"
export PVE_TOKEN_ID="clawd@pve!tokenname"
export PVE_TOKEN_SECRET="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
export PVE_VERIFY_SSL="false"
```

### Create API Token

1. Login to Proxmox web UI
2. Datacenter → Permissions → API Tokens → Add
3. Select user, enter token ID
4. Copy the secret (shown only once!)

## Usage

### Quick Commands (Bash)

```bash
# Cluster status
bash scripts/pve.sh status

# List all VMs
bash scripts/pve.sh vms

# List all containers
bash scripts/pve.sh lxc

# Start VM by ID (auto-detects node)
bash scripts/pve.sh start 115

# Create snapshot with RAM
bash scripts/pve.sh snap 115 pre-update 1

# Rollback to snapshot
bash scripts/pve.sh rollback 115 pre-update

# List backups
bash scripts/pve.sh backups pve local

# Node health
bash scripts/pve.sh health pve
```

### Python API

```bash
# All nodes
python3 scripts/proxmox.py nodes

# VM status
python3 scripts/proxmox.py status pve qemu 115

# Create snapshot
python3 scripts/proxmox.py snapshot pve qemu 115 pre-update 0

# Rollback
python3 scripts/proxmox.py rollback pve qemu 115 pre-update
```

## Approval Requirements

Actions requiring user approval:
- Power: `start`, `stop`, `shutdown`, `reboot`
- Snapshots: `snapshot`, `delete_snapshot`, `rollback`
- Backups: `backup`

Read-only (no approval):
- `nodes`, `vms`, `status`, `list_snapshots`
- `backups` (list), `storage`, `tasks`, `health`

## Requirements

- `curl`, `jq` (for bash script)
- Python 3 + `proxmoxer` (for Python API)

Install proxmoxer:
```bash
pip install proxmoxer
```

## Credit

Merged from:
- `robnew/proxmox-skill` — Python tools with approval framework
- `weird-aftertaste/proxmox` — Comprehensive bash helper

## License

MIT