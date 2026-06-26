#!/bin/bash
# status.sh — 检查 SearXNG 运行状态

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCKER_DIR="${DOCKER_DIR:-$HOME/docker/searxng}"

# 加载环境变量
if [ -f "$HOME/.zshrc" ]; then
    export $(grep "SEARXNG_BASE_URL" "$HOME/.zshrc" 2>/dev/null | grep -v '^#' | xargs) 2>/dev/null || true
fi

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo ""
echo "🔍 SearXNG 状态检查"
echo "═══════════════════════════════════════════════════"

# 1. 容器状态
echo ""
echo "📦 Docker 容器:"
if docker ps -a 2>/dev/null | grep -q "searxng$"; then
    echo -e "   ${GREEN}✅ searxng 容器运行中${NC}"
    docker ps --filter name=searxng --format "   状态: ${GREEN}{{./Status}}${NC} | 镜像: {{./Image}}" 2>/dev/null
else
    echo -e "   ${RED}❌ searxng 容器未运行${NC}"
fi

# 2. 端口检测
echo ""
echo "🌐 端口检测:"
PORT=$(docker port searxng 2>/dev/null | grep '8080/tcp' | grep -oE '[0-9]+$' | head -1 || echo "")
PORT="${PORT:-8888}"

if nc -z localhost $PORT 2>/dev/null; then
    echo -e "   ${GREEN}✅ 端口 $PORT 可访问${NC}"
else
    echo -e "   ${RED}❌ 端口 $PORT 无法访问${NC}"
fi

# 3. 健康检查
echo ""
echo "🔍 健康检查:"
if curl -sf --connect-timeout 3 --max-time 5 "http://localhost:$PORT/healthz" > /dev/null 2>&1; then
    echo -e "   ${GREEN}✅ SearXNG 健康检查通过${NC}"
else
    echo -e "   ${RED}❌ SearXNG 健康检查失败${NC}"
fi

# 4. JSON API 测试
echo ""
echo "🔧 JSON API 测试:"
JSON_RESULT=$(curl -sf --connect-timeout 5 --max-time 10 "http://localhost:$PORT/search?q=hello&format=json" 2>/dev/null | head -c 100 || echo "")
if echo "$JSON_RESULT" | grep -q '"results"'; then
    echo -e "   ${GREEN}✅ JSON API 正常${NC}"
else
    echo -e "   ${YELLOW}⚠️  JSON API 异常 (主页正常)${NC}"
fi

# 5. 环境变量
echo ""
echo "📝 OpenClaw 配置:"
if [ -n "$SEARXNG_BASE_URL" ]; then
    echo "   SEARXNG_BASE_URL=$SEARXNG_BASE_URL"
    echo -e "   ${YELLOW}⚠️  如未生效请运行: source ~/.zshrc${NC}"
else
    echo -e "   ${RED}⚠️  SEARXNG_BASE_URL 未设置${NC}"
fi

# 6. 数据目录
echo ""
echo "📂 配置目录:"
if [ -d "$DOCKER_DIR" ]; then
    echo "   ✅ $DOCKER_DIR"
else
    echo "   ⚠️  目录不存在"
fi

echo ""
echo "═══════════════════════════════════════════════════"
echo "🔧 常用命令:"
echo "   查看日志: docker logs searxng"
echo "   重启服务: cd $DOCKER_DIR && docker compose restart"
echo "   停止服务: cd $DOCKER_DIR && docker compose down"
echo "   卸载:     bash ~/.openclaw/workspace/skills/huo15-searxng/scripts/uninstall.sh"
echo ""
