#!/bin/bash
# Remove M-flow Memory completely
set -euo pipefail

CONTAINER_NAME="mflow-memory"
VOLUME_NAME="mflow_memory_data"
OPENCLAW_CONFIG="$HOME/.openclaw/openclaw.json"

echo "This will stop M-flow Memory and remove the MCP registration."
read -p "Remove memory data too? [y/N]: " REMOVE_DATA

# Stop and remove container
docker stop "$CONTAINER_NAME" 2>/dev/null && echo "Container stopped." || true
docker rm "$CONTAINER_NAME" 2>/dev/null && echo "Container removed." || true

# Remove data volume if requested
if [[ "${REMOVE_DATA:-n}" =~ ^[Yy]$ ]]; then
    docker volume rm "$VOLUME_NAME" 2>/dev/null && echo "Data volume removed." || true
else
    echo "Data volume '$VOLUME_NAME' preserved. Re-run setup to reconnect."
fi

# Remove from OpenClaw config
if [ -f "$OPENCLAW_CONFIG" ]; then
    python3 -c "
import json
config_path = '$OPENCLAW_CONFIG'
with open(config_path) as f:
    config = json.load(f)
config.get('mcpServers', {}).pop('mflow-memory', None)
with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)
print('Removed mflow-memory from', config_path)
" 2>/dev/null || echo "Could not auto-update OpenClaw config."
fi

echo "Done. Restart OpenClaw to unload MCP tools."
