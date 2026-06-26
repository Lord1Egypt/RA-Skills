#!/bin/bash
# M-flow Memory — One-click setup for OpenClaw
set -euo pipefail

CONTAINER_NAME="mflow-memory"
IMAGE="flowelement/m_flow-mcp:latest@sha256:ba9955bb9c9e57b40bf5619f37474357bfe00268e81514783a956de2b301bb82"
VOLUME_NAME="mflow_memory_data"
DEFAULT_PORT=8001
OPENCLAW_CONFIG="$HOME/.openclaw/openclaw.json"

echo "================================================"
echo "  M-flow Memory — Setup for OpenClaw"
echo "================================================"
echo ""

# Check Docker
if ! command -v docker &>/dev/null; then
    echo "ERROR: Docker is required."
    echo "Install: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! docker info &>/dev/null 2>&1; then
    echo "ERROR: Docker daemon is not running."
    echo "Start Docker Desktop and try again."
    exit 1
fi

# Check if already running
if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "M-flow Memory is already running."
    echo "Use 'docker restart $CONTAINER_NAME' to restart."
    echo "Use 'bash scripts/teardown.sh' to remove."
    exit 0
fi

# Remove stopped container if exists
docker rm "$CONTAINER_NAME" 2>/dev/null || true

# Get API key (env var or interactive)
API_KEY="${LLM_API_KEY:-}"
if [ -z "$API_KEY" ]; then
    echo "M-flow needs an LLM API key for knowledge extraction."
    echo "Get one from: https://platform.openai.com/api-keys"
    echo "(Or set LLM_API_KEY environment variable before running)"
    echo ""
    read -p "LLM API Key: " API_KEY
fi

if [ -z "$API_KEY" ]; then
    echo "ERROR: API key is required."
    exit 1
fi

# Find available port
PORT=$DEFAULT_PORT
while lsof -ti:$PORT &>/dev/null 2>&1; do
    PORT=$((PORT + 1))
    if [ $PORT -gt 8010 ]; then
        echo "ERROR: No available port found (tried $DEFAULT_PORT-8010)."
        exit 1
    fi
done

if [ $PORT -ne $DEFAULT_PORT ]; then
    echo "Port $DEFAULT_PORT is busy, using $PORT instead."
fi

# Pull latest image
echo ""
echo "Pulling M-flow MCP image..."
docker pull "$IMAGE"

# Start container
echo ""
echo "Starting M-flow Memory..."
docker run -d \
    --name "$CONTAINER_NAME" \
    --restart unless-stopped \
    -p "$PORT:8000" \
    -e "LLM_API_KEY=$API_KEY" \
    -e "TRANSPORT_MODE=sse" \
    -v "$VOLUME_NAME:/srv/mcp/m_flow/.mflow" \
    "$IMAGE"

# Wait for healthy
echo "Waiting for server to be ready..."
for i in $(seq 1 30); do
    if curl -sf "http://localhost:$PORT/health" &>/dev/null; then
        echo "M-flow Memory is ready."
        break
    fi
    sleep 2
done

if ! curl -sf "http://localhost:$PORT/health" &>/dev/null; then
    echo "WARNING: Server did not become healthy in 60s."
    echo "Check logs: docker logs $CONTAINER_NAME"
fi

# Register MCP with OpenClaw
echo ""
echo "Registering MCP server with OpenClaw..."

mkdir -p "$(dirname "$OPENCLAW_CONFIG")"

if [ -f "$OPENCLAW_CONFIG" ]; then
    # Add to existing config
    python3 -c "
import json, sys

config_path = '$OPENCLAW_CONFIG'
with open(config_path) as f:
    config = json.load(f)

mcp = config.setdefault('mcpServers', {})
mcp['mflow-memory'] = {
    'url': 'http://localhost:$PORT/sse',
    'transport': 'sse'
}

with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)

print('Updated', config_path)
" 2>/dev/null || echo "Could not auto-update config. See manual instructions below."
else
    # Create new config
    cat > "$OPENCLAW_CONFIG" << EOF
{
  "mcpServers": {
    "mflow-memory": {
      "url": "http://localhost:$PORT/sse",
      "transport": "sse"
    }
  }
}
EOF
    echo "Created $OPENCLAW_CONFIG"
fi

echo ""
echo "================================================"
echo "  Setup complete!"
echo "================================================"
echo ""
echo "  M-flow Memory: http://localhost:$PORT"
echo "  Data volume:   $VOLUME_NAME"
echo "  Container:     $CONTAINER_NAME"
echo ""
echo "  Your agent now has long-term memory."
echo "  Restart OpenClaw to load the MCP tools."
echo "================================================"
