---
name: proxmox-complete
description: Manage Proxmox VE clusters via REST API. List nodes, VMs, containers; control power states; manage snapshots, backups, storage, and tasks. Use when user asks about Proxmox, VMs, LXC, snapshots, backups, or cluster status.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🖥️"
    requires:
      bins: ["curl", "jq", "python3"]
      python_packages: ["proxmoxer"]
---

# Proxmox Complete Skill

Comprehensive Proxmox VE management combining:
- **Power control**: Start, stop, reboot, shutdown VMs/containers
- **Snapshots**: Create, list, delete, rollback (with optional RAM state)
- **Backups**: List and create backups
- **Storage**: View storage pools and content
- **Tasks**: Track async operations and logs
- **Cluster overview**: Nodes, resources, health

## Configuration

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

### Option 3: Credentials File

```bash
cat > ~/.proxmox-credentials << 'EOF'
PROXMOX_HOST=https://your-proxmox-ip:8006
PROXMOX_TOKEN_ID=clawd@pve!tokenname
PROXMOX_TOKEN_SECRET=your-token-secret
EOF
chmod 600 ~/.proxmox-credentials
```

### Create API Token

1. Login to Proxmox web UI
2. Datacenter → Permissions → API Tokens → Add
3. Select user, enter token ID, uncheck "Privilege Separation" if needed
4. Copy the secret (shown only once!)

## Tools

### Cluster & Nodes

```bash
# Cluster overview
python3 scripts/proxmox.py nodes

# Node health (CPU, RAM, uptime)
python3 scripts/proxmox.py node_health pve

# Bash alternative
bash scripts/pve.sh status
```

### List Resources

```bash
# All VMs cluster-wide
python3 scripts/proxmox.py vms

# All VMs on specific node
bash scripts/pve.sh vms pve

# LXC containers on node
bash scripts/pve.sh lxc pve

# Cluster resources (all types)
bash scripts/pve.sh resources
```

### VM/Container Status

```bash
# Python (detailed)
python3 scripts/proxmox.py status pve qemu 115

# Bash (quick)
bash scripts/pve.sh info pve 115
```

### Power Control (Requires Approval)

```bash
# Start VM
python3 scripts/proxmox.py start pve qemu 115

# Stop VM (hard)
python3 scripts/proxmox.py stop pve qemu 115

# Shutdown VM (graceful)
python3 scripts/proxmox.py shutdown pve qemu 115

# Reboot VM
python3 scripts/proxmox.py reboot pve qemu 115

# Bash alternatives
bash scripts/pve.sh start 115 pve
bash scripts/pve.sh stop 115 pve
bash scripts/pve.sh shutdown 115 pve
```

### Snapshots

```bash
# List snapshots
python3 scripts/proxmox.py list_snapshots pve qemu 115

# Create snapshot (vmstate=0: no RAM, vmstate=1: include RAM)
python3 scripts/proxmox.py snapshot pve qemu 115 pre-update 0

# Delete snapshot (requires approval)
python3 scripts/proxmox.py delete_snapshot pve qemu 115 pre-update

# Rollback to snapshot (bash)
bash scripts/pve.sh rollback pve 115 pre-update
```

### Backups

```bash
# List backups
bash scripts/pve.sh backups pve local

# Start backup
bash scripts/pve.sh backup pve 115 local
```

### Storage

```bash
# List storage pools
bash scripts/pve.sh storage pve

# Storage content
bash scripts/pve.sh content pve local
```

### Tasks & Logs

```bash
# Recent tasks
bash scripts/pve.sh tasks pve

# Task log
bash scripts/pve.sh log pve UPID:pve:00001234:...
```

## Approval Requirements

These actions require user approval:
- Power control: `start`, `stop`, `shutdown`, `reboot`
- Snapshots: `snapshot`, `delete_snapshot`
- Backups: `backup`
- Rollback: `rollback`

Read-only operations (no approval needed):
- `nodes`, `vms`, `status`, `list_snapshots`
- `backups` (list only), `storage`, `tasks`, `log`

## Response Format

All commands return JSON for easy parsing:

```json
{
  "ok": true,
  "data": { ... }
}
```

Error responses:

```json
{
  "ok": false,
  "error": "Missing env var: PVE_HOST"
}
```

## Notes

- Replace `pve` with your actual node name
- Replace `115` with actual VMID
- `qemu` = VM, `lxc` = container
- API tokens don't need CSRF tokens
- Self-signed certs: set `verify_ssl: false` or use `-k` flag

## Credit

Merged from:
- `robnew/proxmox-skill` — Python tool-based approach with approvals
- `weird-aftertaste/proxmox` — Bash helper with comprehensive API coverage

## License

MIT