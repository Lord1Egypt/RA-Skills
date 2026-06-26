#!/bin/bash
# install.sh — SearXNG 一键部署脚本 v1.1.0
# 功能：Docker Compose 部署 + 端口冲突检测 + OpenClaw 配置
# 修复：grep -oP (GNU) → grep -E + cut (跨平台) | sed 分隔符 | 幂等性

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(dirname "$SCRIPT_DIR")"
TEMPLATES_DIR="$SKILL_ROOT/templates"
DOCKER_DIR="$HOME/docker/searxng"

# 默认配置
DEFAULT_PORT=8888
MAX_PORT=8910
MAX_WAIT=60

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# ============================================================
# 0. 入口检测：是否已安装
# ============================================================
check_already_installed() {
    # 检查容器是否在运行
    if docker ps -a 2>/dev/null | grep -q "searxng$"; then
        log_warn "SearXNG 容器已在运行"
        local current_port=$(docker port searxng 2>/dev/null | grep '8080/tcp' | grep -oE ':[0-9]+$' | tr -d ':' | head -1 || echo "")
        if [ -n "$current_port" ]; then
            log_info "检测到端口: $current_port"
            PORT=$current_port
            configure_openclaw
            print_status
            exit 0
        fi
    fi
    
    # 检查配置文件是否存在
    if [ -f "$DOCKER_DIR/docker-compose.yml" ]; then
        log_warn "检测到已有配置，执行升级..."
        UPGRADE=true
    else
        UPGRADE=false
    fi
}

# ============================================================
# 1. 检查 Docker 和 docker compose
# ============================================================
check_docker() {
    log_info "检查 Docker 环境..."
    
    if ! command -v docker &> /dev/null; then
        log_error "Docker 未安装，请先安装 Docker Desktop"
        log_info "提示: brew install --cask docker"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        log_error "Docker 未运行，请启动 Docker Desktop"
        exit 1
    fi
    
    if ! command -v docker compose &> /dev/null; then
        log_error "docker compose v2 未安装"
        log_info "提示: Docker Desktop 已内置 docker compose，无需单独安装"
        exit 1
    fi
    
    # 跨平台获取版本号 (兼容 macOS grep)
    DOCKER_VERSION=$(docker compose version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+' | head -1)
    log_info "Docker Compose v${DOCKER_VERSION} ✓"
}

# ============================================================
# 2. 端口可用性检测
# ============================================================
find_available_port() {
    log_info "检测可用端口..."
    
    PORT=$DEFAULT_PORT
    while [ $PORT -le $MAX_PORT ]; do
        # 跨平台端口检测：nc -z 在 macOS 和 Linux 都支持
        if nc -z localhost $PORT 2>/dev/null; then
            log_warn "端口 $PORT 已被占用，尝试 $((PORT+1))..."
            PORT=$((PORT+1))
        else
            log_info "✅ 找到可用端口: $PORT"
            return 0
        fi
    done
    
    log_error "未找到可用端口 (8888-$MAX_PORT)"
    exit 1
}

# ============================================================
# 3. 创建目录并渲染 docker-compose.yml
# ============================================================
setup_docker() {
    log_info "创建 Docker 目录..."
    mkdir -p "$DOCKER_DIR/searxng" "$DOCKER_DIR/searxng-data"
    
    # 渲染 docker-compose.yml
    log_info "生成 docker-compose.yml..."
    cat > "$DOCKER_DIR/docker-compose.yml" << EOF
services:
  searxng:
    image: searxng/searxng:latest
    container_name: searxng
    restart: unless-stopped
    ports:
      - "${PORT}:8080"
    volumes:
      - ./searxng:/etc/searxng:rw
      - ./searxng-data:/var/lib/searxng:rw
    environment:
      - SEARXNG_BASE_URL=http://localhost:${PORT}/
      - HTTP_PROXY=""
      - HTTPS_PROXY=""
      - NO_PROXY=*
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    healthcheck:
      test: ["CMD", "wget", "-q", "--spider", "http://localhost:8080/healthz"]
      interval: 10s
      timeout: 5s
      retries: 3
EOF
    
    # 渲染 settings.yml (启用 JSON API)
    log_info "生成 settings.yml..."
    SECRET_KEY=$(cat /dev/urandom | tr -dc 'a-z0-9' | fold -w 32 | head -n 1)
    cat > "$DOCKER_DIR/searxng/settings.yml" << EOFSETTINGS
search:
  default_lang: zh-CN
  formats:
    - html
    - json

server:
  secret_key: "${SECRET_KEY}"
  bind_address: "0.0.0.0"
  port: 8080

outgoing:
  useragent_suffix: ""
  pool_connections: 100
  pool_maxsize: 20

engines:
  - name: google
    engine: google
    shortcut: g
  - name: bing
    engine: bing
    shortcut: b
  - name: duckduckgo
    engine: duckduckgo
    shortcut: ddg
  - name: baidu
    engine: baidu
    shortcut: bd
EOFSETTINGS

    # 创建空的 limiter.toml (解决 botdetection 403 问题)
    log_info "生成 limiter.toml..."
    touch "$DOCKER_DIR/searxng/limiter.toml"
}

# ============================================================
# 4. 启动 SearXNG
# ============================================================
start_searxng() {
    log_info "启动 SearXNG 容器..."
    
    cd "$DOCKER_DIR"
    
    # 停止旧容器（如果存在）
    if docker ps -a 2>/dev/null | grep -q "searxng$"; then
        log_info "停止旧容器..."
        docker compose down --remove-orphans 2>/dev/null || true
    fi
    
    docker compose up -d --pull always
    
    log_info "等待服务就绪..."
}

# ============================================================
# 5. 健康检查
# ============================================================
wait_for_searxng() {
    local elapsed=0
    local interval=3
    
    while [ $elapsed -lt $MAX_WAIT ]; do
        # 使用 curl 的 --fail 配合 -o /dev/null 检测 HTTP 状态码
        if curl -sf --connect-timeout 3 --max-time 5 "http://localhost:$PORT/healthz" > /dev/null 2>&1; then
            log_info "✅ SearXNG 服务已就绪"
            return 0
        fi
        
        sleep $interval
        elapsed=$((elapsed + interval))
        echo -n "."
    done
    
    echo ""
    log_error "SearXNG 启动超时 (${MAX_WAIT}s)"
    log_info "查看日志: docker -f searxng logs"
    log_info "调试: curl -v http://localhost:$PORT/healthz"
    exit 1
}

# ============================================================
# 6. 验证服务
# ============================================================
verify_searxng() {
    log_info "验证 SearXNG..."
    
    # 测试主页
    if curl -sf --connect-timeout 3 --max-time 5 "http://localhost:$PORT" > /dev/null 2>&1; then
        log_info "✅ 主页访问成功"
    else
        log_error "主页访问失败"
        return 1
    fi
    
    # 测试 JSON API
    local json_response=$(curl -sf --connect-timeout 5 --max-time 10 "http://localhost:$PORT/search?q=test&format=json" 2>/dev/null)
    if echo "$json_response" | grep -q '"results"'; then
        log_info "✅ JSON API 正常"
    else
        log_warn "JSON API 响应异常 (主页正常，搜索引擎可能需要配置)"
    fi
}

# ============================================================
# 7. 配置 OpenClaw 环境变量
# ============================================================
configure_openclaw() {
    log_info "配置 OpenClaw..."
    
    local searxng_url="http://localhost:$PORT"
    local env_line="export SEARXNG_BASE_URL=\"$searxng_url\""
    
    # 检查是否已配置（跨平台 sed）
    if grep -q "SEARXNG_BASE_URL" "$HOME/.zshrc" 2>/dev/null; then
        log_warn "SEARXNG_BASE_URL 已存在，更新..."
        # 使用 @ 作为分隔符，避免 URL 中的 / 导致问题
        sed -i '' "s|export SEARXNG_BASE_URL=.*|${env_line}|" "$HOME/.zshrc"
    else
        echo "" >> "$HOME/.zshrc"
        echo "# SearXNG (huo15-searxng)" >> "$HOME/.zshrc"
        echo "$env_line" >> "$HOME/.zshrc"
        log_info "已添加到 ~/.zshrc"
    fi
    
    # 立即生效（仅当前 shell）
    export SEARXNG_BASE_URL="$searxng_url"
    
    log_info "✅ SEARXNG_BASE_URL=$searxng_url"
}

# ============================================================
# 8. 输出状态
# ============================================================
print_status() {
    echo ""
    echo "═══════════════════════════════════════════════════"
    echo -e "  ${GREEN}🔍 SearXNG 状态${NC}"
    echo "═══════════════════════════════════════════════════"
    echo ""
    echo "  🔍 访问地址: http://localhost:$PORT"
    echo "  📡 API 端点: http://localhost:$PORT/search"
    echo "  🔧 配置目录: $DOCKER_DIR"
    echo "  📝 SEARXNG_BASE_URL=$SEARXNG_BASE_URL"
    echo ""
    echo "  常用命令:"
    echo "    查看日志: docker logs searxng"
    echo "    重启服务: cd $DOCKER_DIR && docker compose restart"
    echo "    停止服务: cd $DOCKER_DIR && docker compose down"
    echo "    卸载:     bash ~/.openclaw/workspace/skills/huo15-searxng/scripts/uninstall.sh"
    echo ""
    echo "  ⚠️  如需立即生效，请运行: source ~/.zshrc"
    echo ""
    echo "═══════════════════════════════════════════════════"
}

# ============================================================
# 9. 输出完成信息
# ============================================================
print_complete() {
    echo ""
    echo "═══════════════════════════════════════════════════"
    echo -e "  ${GREEN}🎉 SearXNG 部署完成!${NC}"
    echo "═══════════════════════════════════════════════════"
    echo ""
    echo "  🔍 访问地址: http://localhost:$PORT"
    echo "  📡 API 端点: http://localhost:$PORT/search"
    echo "  🔧 配置目录: $DOCKER_DIR"
    echo ""
    echo "  📝 OpenClaw 已配置:"
    echo "     SEARXNG_BASE_URL=$SEARXNG_BASE_URL"
    echo ""
    echo "  ⚠️  重要: 请运行以下命令使环境变量立即生效:"
    echo "     source ~/.zshrc"
    echo ""
    echo "  常用命令:"
    echo "    查看日志: docker logs searxng"
    echo "    重启服务: cd $DOCKER_DIR && docker compose restart"
    echo "    停止服务: cd $DOCKER_DIR && docker compose down"
    echo "    卸载:     bash ~/.openclaw/workspace/skills/huo15-searxng/scripts/uninstall.sh"
    echo ""
    echo "═══════════════════════════════════════════════════"
}

# ============================================================
# 主流程
# ============================================================
main() {
    echo ""
    echo "🔍 huo15-searxng — SearXNG 一键部署 v1.1.0"
    echo "═══════════════════════════════════════════════════"
    echo ""
    
    check_already_installed
    check_docker
    find_available_port
    setup_docker
    start_searxng
    wait_for_searxng
    verify_searxng
    configure_openclaw
    print_complete
}

main "$@"
