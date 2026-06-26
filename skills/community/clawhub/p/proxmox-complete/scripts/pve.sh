#!/bin/bash
# Proxmox VE helper script
# Merged from weird-aftertaste/proxmox with enhancements

set -euo pipefail

# Load credentials - try multiple sources
if [[ -f ~/.openclaw/credentials/proxmox.json ]]; then
    # OpenClaw JSON format
    PROXMOX_HOST="https://$(jq -r '.host' ~/.openclaw/credentials/proxmox.json)"
    PROXMOX_TOKEN_ID="$(jq -r '.token_id' ~/.openclaw/credentials/proxmox.json)"
    PROXMOX_TOKEN_SECRET="$(jq -r '.token_secret' ~/.openclaw/credentials/proxmox.json)"
elif [[ -f ~/.proxmox-credentials ]]; then
    source ~/.proxmox-credentials
fi

# Also support env vars (highest priority)
: "${PROXMOX_HOST:=${PVE_HOST:-}}"
: "${PROXMOX_TOKEN_ID:=${PVE_TOKEN_ID:-}}"
: "${PROXMOX_TOKEN_SECRET:=${PVE_TOKEN_SECRET:-}}"

# Normalize host URL
PROXMOX_HOST="${PROXMOX_HOST#https://}"
PROXMOX_HOST="https://${PROXMOX_HOST}"

: "${PROXMOX_HOST:?Set PROXMOX_HOST or create ~/.openclaw/credentials/proxmox.json}"
: "${PROXMOX_TOKEN_ID:?Set PROXMOX_TOKEN_ID}"
: "${PROXMOX_TOKEN_SECRET:?Set PROXMOX_TOKEN_SECRET}"

AUTH="Authorization: PVEAPIToken=$PROXMOX_TOKEN_ID=$PROXMOX_TOKEN_SECRET"

api() {
    local method="${1:-GET}"
    local endpoint="$2"
    shift 2
    curl -ks -X "$method" -H "$AUTH" "$PROXMOX_HOST/api2/json$endpoint" "$@"
}

get_node_for_vmid() {
    local vmid="$1"
    api GET "/cluster/resources?type=vm" | jq -r ".data[] | select(.vmid==$vmid) | .node"
}

get_type_for_vmid() {
    local vmid="$1"
    api GET "/cluster/resources?type=vm" | jq -r ".data[] | select(.vmid==$vmid) | .type"
}

cmd="${1:-help}"
shift || true

case "$cmd" in
    status|nodes)
        echo "=== Cluster Nodes ==="
        api GET /cluster/resources?type=node | jq -r '.data[] | "\(.node): \(.status)\(if .cpu then " | CPU: \((.cpu*100)|round)%" else "" end)\(if .maxmem then " | Mem: \((.mem/.maxmem*100)|round)%" else "" end)"'
        ;;
    
    resources)
        echo "=== Cluster Resources ==="
        api GET /cluster/resources | jq -r '.data[] | "\(.type)\t\(.id)\t\(.status // "-")"'
        ;;
    
    vms|list)
        node="${1:-}"
        if [[ -n "$node" ]]; then
            api GET "/nodes/$node/qemu" | jq -r '.data[] | "\(.vmid)\t\(.name)\t\(.status)"'
        else
            api GET "/cluster/resources?type=vm" | jq -r '.data[] | select(.type=="qemu") | "\(.vmid)\t\(.name)\t\(.status)\t\(.node)"'
        fi
        ;;
    
    lxc|containers)
        node="${1:-}"
        if [[ -n "$node" ]]; then
            api GET "/nodes/$node/lxc" | jq -r '.data[] | "\(.vmid)\t\(.name)\t\(.status)"'
        else
            api GET "/cluster/resources?type=vm" | jq -r '.data[] | select(.type=="lxc") | "\(.vmid)\t\(.name)\t\(.status)\t\(.node)"'
        fi
        ;;
    
    all)
        echo "=== All VMs & Containers ==="
        api GET "/cluster/resources?type=vm" | jq -r '.data[] | "\(.type)\t\(.vmid)\t\(.name)\t\(.status)\t\(.node)"'
        ;;
    
    info|status)
        vmid="${1:?Specify VMID}"
        node="${2:-}"
        if [[ -z "$node" ]]; then
            node=$(get_node_for_vmid "$vmid")
        fi
        vmtype=$(get_type_for_vmid "$vmid")
        api GET "/nodes/$node/$vmtype/$vmid/status/current" | jq '.data | {name, status, cpu, mem, maxmem, uptime}'
        ;;
    
    start)
        vmid="${1:?Specify VMID}"
        node="${2:-}"
        if [[ -z "$node" ]]; then
            node=$(get_node_for_vmid "$vmid")
        fi
        vmtype=$(get_type_for_vmid "$vmid")
        echo "Starting $vmtype $vmid on $node..."
        api POST "/nodes/$node/$vmtype/$vmid/status/start" | jq
        ;;
    
    stop)
        vmid="${1:?Specify VMID}"
        node="${2:-}"
        if [[ -z "$node" ]]; then
            node=$(get_node_for_vmid "$vmid")
        fi
        vmtype=$(get_type_for_vmid "$vmid")
        echo "Stopping $vmtype $vmid on $node..."
        api POST "/nodes/$node/$vmtype/$vmid/status/stop" | jq
        ;;
    
    shutdown)
        vmid="${1:?Specify VMID}"
        node="${2:-}"
        if [[ -z "$node" ]]; then
            node=$(get_node_for_vmid "$vmid")
        fi
        vmtype=$(get_type_for_vmid "$vmid")
        echo "Shutting down $vmtype $vmid on $node..."
        api POST "/nodes/$node/$vmtype/$vmid/status/shutdown" | jq
        ;;
    
    reboot)
        vmid="${1:?Specify VMID}"
        node="${2:-}"
        if [[ -z "$node" ]]; then
            node=$(get_node_for_vmid "$vmid")
        fi
        vmtype=$(get_type_for_vmid "$vmid")
        echo "Rebooting $vmtype $vmid on $node..."
        api POST "/nodes/$node/$vmtype/$vmid/status/reboot" | jq
        ;;
    
    snap|snapshot)
        vmid="${1:?Specify VMID}"
        snapname="${2:-snap-$(date +%Y%m%d-%H%M%S)}"
        vmstate="${3:-0}"
        node="${4:-}"
        if [[ -z "$node" ]]; then
            node=$(get_node_for_vmid "$vmid")
        fi
        vmtype=$(get_type_for_vmid "$vmid")
        echo "Creating snapshot '$snapname' for $vmtype $vmid (vmstate=$vmstate)..."
        api POST "/nodes/$node/$vmtype/$vmid/snapshot" -d "snapname=$snapname" -d "vmstate=$vmstate" | jq
        ;;
    
    snapshots)
        vmid="${1:?Specify VMID}"
        node="${2:-}"
        if [[ -z "$node" ]]; then
            node=$(get_node_for_vmid "$vmid")
        fi
        vmtype=$(get_type_for_vmid "$vmid")
        echo "Snapshots for $vmtype $vmid:"
        api GET "/nodes/$node/$vmtype/$vmid/snapshot" | jq -r '.data[] | "\(.name)\t\(.description // "-")\t\(.snaptime | strftime("%Y-%m-%d %H:%M"))"'
        ;;
    
    rollback)
        vmid="${1:?Specify VMID}"
        snapname="${2:?Specify snapshot name}"
        node="${3:-}"
        if [[ -z "$node" ]]; then
            node=$(get_node_for_vmid "$vmid")
        fi
        vmtype=$(get_type_for_vmid "$vmid")
        echo "Rolling back $vmtype $vmid to snapshot '$snapname'..."
        api POST "/nodes/$node/$vmtype/$vmid/snapshot/$snapname/rollback" | jq
        ;;
    
    delsnap|delete-snapshot)
        vmid="${1:?Specify VMID}"
        snapname="${2:?Specify snapshot name}"
        node="${3:-}"
        if [[ -z "$node" ]]; then
            node=$(get_node_for_vmid "$vmid")
        fi
        vmtype=$(get_type_for_vmid "$vmid")
        echo "Deleting snapshot '$snapname' from $vmtype $vmid..."
        api DELETE "/nodes/$node/$vmtype/$vmid/snapshot/$snapname" | jq
        ;;
    
    backups)
        node="${1:?Specify node}"
        storage="${2:-local}"
        echo "Backups on $storage:"
        api GET "/nodes/$node/storage/$storage/content?content=backup" | jq -r '.data[] | "\(.volid)\t\(.size)\t(.creation | strftime("%Y-%m-%d %H:%M"))"'
        ;;
    
    backup)
        vmid="${1:?Specify VMID}"
        storage="${2:-local}"
        node="${3:-}"
        if [[ -z "$node" ]]; then
            node=$(get_node_for_vmid "$vmid")
        fi
        echo "Starting backup of VM $vmid to $storage..."
        api POST "/nodes/$node/vzdump" -d "vmid=$vmid" -d "storage=$storage" -d "mode=snapshot" -d "compress=zstd" | jq
        ;;
    
    storage)
        node="${1:?Specify node}"
        echo "Storage on $node:"
        api GET "/nodes/$node/storage" | jq -r '.data[] | "\(.storage)\t\(.type)\t\(if .total then ((.used/.total*100)|round|tostring + "%") else "N/A" end)\t\(.active)"'
        ;;
    
    content)
        node="${1:?Specify node}"
        storage="${2:-local}"
        echo "Content of $storage:"
        api GET "/nodes/$node/storage/$storage/content" | jq -r '.data[] | "\(.volid)\t\(.content)\t(.size)"'
        ;;
    
    tasks)
        node="${1:?Specify node}"
        limit="${2:-10}"
        echo "Recent tasks on $node:"
        api GET "/nodes/$node/tasks?limit=$limit" | jq -r '.data[] | "\(.starttime | strftime("%Y-%m-%d %H:%M:%S"))\t\(.type)\t\(.status)\t\(.id)"'
        ;;
    
    log)
        node="${1:?Specify node}"
        upid="${2:?Specify UPID}"
        echo "Task log for $upid:"
        api GET "/nodes/$node/tasks/$upid/log" | jq -r '.data[].t'
        ;;
    
    health)
        node="${1:?Specify node}"
        echo "Health status for $node:"
        api GET "/nodes/$node/status" | jq '.data | {cpu: (.cpu * 100 | round), memory: ((.memory.used / .memory.total * 100) | round), uptime: .uptime, loadavg: .loadavg}'
        ;;
    
    help|*)
        cat << 'EOF'
Proxmox VE CLI Helper (Complete)

Usage: pve.sh <command> [args]

Commands:
  status               Show cluster nodes status
  resources            Show all cluster resources
  vms [node]           List VMs (all or by node)
  lxc [node]           List containers (all or by node)
  all                  List all VMs and containers
  
  info <vmid>          Get VM/container status
  start <vmid>         Start VM/container
  stop <vmid>          Force stop VM/container
  shutdown <vmid>      Graceful shutdown
  reboot <vmid>        Reboot VM/container
  
  snap <vmid> [name] [vmstate]  Create snapshot (vmstate=0|1)
  snapshots <vmid>     List snapshots
  rollback <vmid> <snap>        Rollback to snapshot
  delsnap <vmid> <snap>         Delete snapshot
  
  backups <node> [storage]      List backups
  backup <vmid> [storage]       Create backup
  storage <node>                List storage pools
  content <node> [storage]      List storage content
  
  tasks <node> [limit]          Recent tasks
  log <node> <upid>             Task log
  health <node>                 Node health stats

Configuration:
  ~/.openclaw/credentials/proxmox.json:
    {"host": "your-proxmox-ip", "token_id": "...", "token_secret": "..."}
  
  Or ~/.proxmox-credentials:
    PROXMOX_HOST=https://your-proxmox-ip:8006
    PROXMOX_TOKEN_ID=user@pam!tokenname
    PROXMOX_TOKEN_SECRET=your-token-secret
  
  Or environment variables:
    PVE_HOST, PVE_TOKEN_ID, PVE_TOKEN_SECRET

Notes:
  - VMID can be used without node (auto-detected)
  - vmstate=0 saves disk only, vmstate=1 includes RAM
  - Backups use zstd compression by default
EOF
        ;;
esac