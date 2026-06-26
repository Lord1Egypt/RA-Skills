#!/bin/bash
# deploy.sh — Upload agent workspaces to VPS and restart OpenClaw container.
# Usage: bash deploy.sh --vps root@your-vps-ip --key ~/.ssh/your_key --data /docker/openclaw/data

set -e

VPS=""
KEY="~/.ssh/id_rsa"
VPS_DATA="/docker/openclaw-pkpz/data/.openclaw"
LOCAL_DIR="$(cd "$(dirname "$0")" && pwd)"

while [[ $# -gt 0 ]]; do
    case $1 in
        --vps)  VPS="$2"; shift 2 ;;
        --key)  KEY="$2"; shift 2 ;;
        --data) VPS_DATA="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

if [ -z "$VPS" ]; then echo "Error: --vps required"; exit 1; fi

SSH="ssh -i $KEY $VPS"
SCP="scp -i $KEY"

echo "=== OpenClaw Multi-Agent Deployment ==="
echo "VPS: $VPS | Data: $VPS_DATA"

echo ""
echo "--- Creating workspace directories ---"
$SSH "mkdir -p $VPS_DATA/workspace-{pat,scout,publisher,builder}/{memory,drafts,skills,.claude}"

echo ""
echo "--- Uploading workspace files ---"
for agent in pat scout publisher builder; do
    if [ -d "$LOCAL_DIR/workspace-$agent" ]; then
        echo "  $agent..."
        for f in SOUL.md IDENTITY.md USER.md AGENTS.md MEMORY.md .claudeignore; do
            [ -f "$LOCAL_DIR/workspace-$agent/$f" ] && \
                $SCP "$LOCAL_DIR/workspace-$agent/$f" "$VPS:$VPS_DATA/workspace-$agent/$f"
        done
        [ -f "$LOCAL_DIR/workspace-$agent/.claude/settings.json" ] && \
            $SCP "$LOCAL_DIR/workspace-$agent/.claude/settings.json" \
                 "$VPS:$VPS_DATA/workspace-$agent/.claude/settings.json"
    fi
done

echo ""
echo "--- Uploading utility scripts ---"
for script in agent_setup.py routing_config.py memory_sync.py; do
    [ -f "$LOCAL_DIR/$script" ] && $SCP "$LOCAL_DIR/$script" "$VPS:$VPS_DATA/$script"
done

echo ""
echo "--- Restarting container ---"
CONTAINER=$($SSH "docker ps --filter name=openclaw --format '{{.Names}}' | head -1")
$SSH "docker restart $CONTAINER"
echo "Restarted: $CONTAINER"

echo ""
echo "=== Done ==="
