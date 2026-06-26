#!/bin/bash
# env.sh — 加载 SearXNG 环境变量

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(dirname "$SCRIPT_DIR")"

# 加载 SEARXNG_BASE_URL
if [ -f "$HOME/.zshrc" ]; then
    export $(grep "SEARXNG_BASE_URL" "$HOME/.zshrc" | xargs) 2>/dev/null || true
fi

# 默认值
SEARXNG_BASE_URL="${SEARXNG_BASE_URL:-http://localhost:8888}"

echo "🔍 SearXNG 环境"
echo "   SEARXNG_BASE_URL: $SEARXNG_BASE_URL"
echo "   DOCKER_DIR: $HOME/docker/searxng"
