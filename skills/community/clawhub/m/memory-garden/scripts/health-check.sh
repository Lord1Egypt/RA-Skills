#!/bin/bash
# Health check script for Memory Garden MCP skill
# Used by container orchestration and monitoring

set -e

PORT="${MG_PORT:-18790}"
URL="${MG_DAEMON_URL:-http://127.0.0.1:${PORT}}"

# Check daemon health endpoint
response=$(curl -s -w "\n%{http_code}" "${URL}/health" 2>/dev/null || echo "000")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | head -n -1)

if [ "$http_code" != "200" ]; then
    echo "UNHEALTHY: Daemon not responding (HTTP ${http_code})"
    exit 1
fi

# Verify it's actually Memory Garden (IR-3)
status=$(echo "$body" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
if [ "$status" != "ok" ]; then
    echo "UNHEALTHY: Daemon status is '${status}'"
    exit 1
fi

echo "HEALTHY: Daemon running at ${URL}"
exit 0
