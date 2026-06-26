#!/usr/bin/env bash
# setup.sh — Initialize glm-search-pro skill
# Reads API key ONLY from ZHIPU_API_KEY environment variable.
# Writes mcporter config with restrictive permissions (600/700).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
MCP_DIR="${HOME}/.openclaw/config/mcporter"
MCP_CONFIG="${MCP_DIR}/mcporter.json"

echo "=== glm-search-pro setup ==="

# 1. Check curl (required)
if ! command -v curl &>/dev/null; then
  echo "Error: curl is required but not found." >&2
  exit 1
fi

# 2. Check mcporter (optional, for MCP mode)
HAS_MCPORTER=false
if command -v mcporter &>/dev/null || command -v npx &>/dev/null; then
  HAS_MCPORTER=true
  echo "mcporter detected (optional, for MCP mode)."
else
  echo "mcporter not found. cURL mode will be used (mcporter is optional)."
fi

# 3. Get API key — ONLY from environment variable
if [ -z "${ZHIPU_API_KEY:-}" ]; then
  echo ""
  echo "Error: ZHIPU_API_KEY environment variable is not set." >&2
  echo "Get your API key at https://open.bigmodel.cn then:" >&2
  echo "  export ZHIPU_API_KEY=\"your-api-key\"" >&2
  echo "  bash scripts/setup.sh" >&2
  exit 1
fi

API_KEY="$ZHIPU_API_KEY"
echo "API key found in ZHIPU_API_KEY env var."

# 4. Write mcporter config with restrictive permissions
mkdir -p "$MCP_DIR"
chmod 700 "$MCP_DIR"

python3 << PYEOF
import json, os, stat

config_path = "$MCP_CONFIG"
api_key = "$API_KEY"

if os.path.exists(config_path):
    with open(config_path) as f:
        config = json.load(f)
else:
    config = {}

if "mcpServers" not in config:
    config["mcpServers"] = {}

config["mcpServers"]["glm-search"] = {
    "type": "sse",
    "url": f"https://open.bigmodel.cn/api/mcp-broker/proxy/web-search/mcp?Authorization={api_key}"
}

with open(config_path, "w") as f:
    json.dump(config, f, indent=2)

# Set restrictive permissions (owner read/write only)
os.chmod(config_path, 0o600)

print(f"Config written to {config_path} (permissions: 600)")
PYEOF

# 5. Verify connection
echo ""
if [ "$HAS_MCPORTER" = true ]; then
  echo "Verifying MCP connection..."
  RESULT=$(npx -y mcporter --config "$MCP_CONFIG" list glm-search 2>&1) || true
  if echo "$RESULT" | grep -q "webSearchPro"; then
    echo "✅ MCP connection successful. Available: webSearchPro, webSearchSogou, webSearchQuark, webSearchStd"
  else
    echo "⚠️  MCP verification inconclusive. Check with: npx -y mcporter --config $MCP_CONFIG list glm-search"
  fi
fi

echo "Verifying cURL connection..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"search_query":"test","search_engine":"search_pro","count":1}' \
  "https://open.bigmodel.cn/api/paas/v4/web_search")

if [ "$HTTP_CODE" = "200" ]; then
  echo "✅ cURL connection successful."
else
  echo "⚠️  cURL returned HTTP $HTTP_CODE. Check your API key."
fi

echo ""
echo "Setup complete."
echo "  MCP mode:  bash ${SKILL_DIR}/scripts/glm-search.sh --mcp \"query\""
echo "  cURL mode: bash ${SKILL_DIR}/scripts/glm-search.sh --curl \"query\""
echo "  Auto:      bash ${SKILL_DIR}/scripts/glm-search.sh \"query\""
