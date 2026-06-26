#!/bin/bash
# 网盘搜索 Docker 一键部署脚本
# 用法: bash deploy.sh [--port 8888] [--web] [--auth user:pass] [--channels ch1,ch2] [--plugins p1,p2]

set -e

# 默认值
PORT=8888
WEB_MODE=false
AUTH_ENABLED=false
AUTH_USERS=""
CHANNELS=""
PLUGINS=""
CONTAINER_NAME="netdisk-search"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info()  { echo -e "${GREEN}[INFO]${NC} $1"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --port)      PORT="$2"; shift 2 ;;
        --web)       WEB_MODE=true; shift ;;
        --auth)      AUTH_ENABLED=true; AUTH_USERS="$2"; shift 2 ;;
        --channels)  CHANNELS="$2"; shift 2 ;;
        --plugins)   PLUGINS="$2"; shift 2 ;;
        --name)      CONTAINER_NAME="$2"; shift 2 ;;
        -h|--help)
            echo "网盘搜索 Docker 部署脚本"
            echo ""
            echo "用法: bash deploy.sh [选项]"
            echo ""
            echo "选项:"
            echo "  --port PORT        服务端口 (默认: 8888)"
            echo "  --web              部署含前端版本 (默认: 仅API)"
            echo "  --auth USER:PASS   启用认证 (格式: user:pass)"
            echo "  --channels CH1,CH2 TG频道列表 (逗号分隔)"
            echo "  --plugins P1,P2    启用插件列表 (逗号分隔)"
            echo "  --name NAME        容器名称 (默认: netdisk-search)"
            echo "  -h, --help         显示帮助"
            exit 0
            ;;
        *) error "未知参数: $1"; exit 1 ;;
    esac
done

# 检查 Docker
if ! command -v docker &> /dev/null; then
    error "未安装 Docker，请先安装: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! docker info &> /dev/null; then
    error "Docker 未启动，请先启动 Docker"
    exit 1
fi

# 停止旧容器
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    warn "发现旧容器 ${CONTAINER_NAME}，正在停止..."
    docker stop "$CONTAINER_NAME" 2>/dev/null || true
    docker rm "$CONTAINER_NAME" 2>/dev/null || true
fi

# 构建 Docker 运行命令
DOCKER_ARGS="-d --name ${CONTAINER_NAME}"

if [ "$WEB_MODE" = true ]; then
    IMAGE="ghcr.io/fish2018/pansou-web:latest"
    DOCKER_ARGS="$DOCKER_ARGS -p ${PORT}:80"
    CONTAINER_NAME="${CONTAINER_NAME}-web"
    info "部署模式: 前后端集成版"
else
    IMAGE="ghcr.io/fish2018/pansou:latest"
    DOCKER_ARGS="$DOCKER_ARGS -p ${PORT}:8888"
    info "部署模式: 纯 API 版"
fi

# 环境变量
if [ -n "$CHANNELS" ]; then
    DOCKER_ARGS="$DOCKER_ARGS -e CHANNELS=${CHANNELS}"
fi

if [ -n "$PLUGINS" ]; then
    DOCKER_ARGS="$DOCKER_ARGS -e ENABLED_PLUGINS=${PLUGINS}"
fi

if [ "$AUTH_ENABLED" = true ]; then
    DOCKER_ARGS="$DOCKER_ARGS -e AUTH_ENABLED=true -e AUTH_USERS=${AUTH_USERS}"
    info "认证已启用: ${AUTH_USERS%%:*}"
fi

# 拉取镜像
info "拉取镜像: ${IMAGE}"
docker pull "$IMAGE"

# 启动容器
info "启动容器: ${CONTAINER_NAME} (端口: ${PORT})"
eval docker run $DOCKER_ARGS "$IMAGE"

# 健康检查
info "等待服务启动..."
MAX_RETRIES=30
RETRY_INTERVAL=2
for i in $(seq 1 $MAX_RETRIES); do
    if curl -sf "http://localhost:${PORT}/api/health" > /dev/null 2>&1; then
        info "✅ 服务启动成功！"
        break
    fi
    if [ $i -eq $MAX_RETRIES ]; then
        error "服务启动超时，请检查日志: docker logs ${CONTAINER_NAME}"
        exit 1
    fi
    sleep $RETRY_INTERVAL
done

# 输出使用说明
echo ""
echo "=========================================="
echo "  搜索服务部署完成！"
echo "=========================================="
echo ""
echo "API 地址: http://localhost:${PORT}"
echo ""

if [ "$WEB_MODE" = true ]; then
    echo "Web 界面: http://localhost:${PORT}"
    echo ""
fi

echo "常用命令:"
echo "  查看日志: docker logs -f ${CONTAINER_NAME}"
echo "  停止服务: docker stop ${CONTAINER_NAME}"
echo "  重启服务: docker restart ${CONTAINER_NAME}"
echo "  删除容器: docker rm -f ${CONTAINER_NAME}"
echo ""

echo "快速测试:"
echo "  curl -X POST http://localhost:${PORT}/api/search \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"kw\": \"测试\"}'"
echo ""

if [ "$AUTH_ENABLED" = true ]; then
    USER="${AUTH_USERS%%:*}"
    PASS="${AUTH_USERS#*:}"
    echo "认证信息:"
    echo "  用户名: ${USER}"
    echo "  密码: ${PASS}"
    echo ""
    echo "获取 Token:"
    echo "  curl -X POST http://localhost:${PORT}/api/auth/login \\"
    echo "    -H 'Content-Type: application/json' \\"
    echo "    -d '{\"username\":\"${USER}\",\"password\":\"${PASS}\"}'"
    echo ""
fi

info "部署完成 🎉"
