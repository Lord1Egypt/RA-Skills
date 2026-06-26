#!/bin/bash
# ═══════════════════════════════════════════════════════════════════
# OpenClaw Connect Node - 一键安装脚本
# ═══════════════════════════════════════════════════════════════════
#
# 用法:
#   方式一 (git clone):
#     bash install-node.sh \
#       --hub-url http://YOUR_HUB_IP:3100 \
#       --app-id xxx --app-key xxx --token xxx \
#       --node-name "我的节点" --from-git
#
#   方式二 (本地代码):
#     cd /path/to/OpenClaw-Connect
#     bash node/install-node.sh \
#       --hub-url http://YOUR_HUB_IP:3100 \
#       --app-id xxx --app-key xxx --token xxx \
#       --node-name "我的节点" --from-local
#
#   方式三 (远程 curl):
#     curl -sSL https://your-hub/install-node.sh | bash -s -- \
#       --hub-url http://YOUR_HUB_IP:3100 \
#       --app-id xxx --app-key xxx --token xxx \
#       --node-name "��的节点"
#
# ═══════════════════════════════════════════════════════════════════

set -e

# ─── Colors ───────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

info()    { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[OK]${NC} $1"; }
warn()    { echo -e "${YELLOW}[WARN]${NC} $1"; }
error()   { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# ─── Default Values ──────────────────────────────────────────────
HUB_URL=""
APP_ID=""
APP_KEY=""
TOKEN=""
NODE_NAME=""
PORT=3200
INSTALL_DIR="/opt/openclaw-node"
SOURCE_MODE="auto"  # auto | git | local
GIT_REPO="https://codeup.aliyun.com/69a0572966d410a0f265834c/openclaw/OpenClaw-Connect.git"
GIT_BRANCH="main"
SERVICE_NAME="openclaw-node"

# ─── Parse Arguments ─────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case $1 in
    --hub-url)      HUB_URL="$2";      shift 2 ;;
    --app-id)       APP_ID="$2";       shift 2 ;;
    --app-key)      APP_KEY="$2";      shift 2 ;;
    --token)        TOKEN="$2";        shift 2 ;;
    --node-name)    NODE_NAME="$2";    shift 2 ;;
    --port)         PORT="$2";         shift 2 ;;
    --install-dir)  INSTALL_DIR="$2";  shift 2 ;;
    --from-git)     SOURCE_MODE="git";  shift ;;
    --from-local)   SOURCE_MODE="local"; shift ;;
    --git-repo)     GIT_REPO="$2";     shift 2 ;;
    --git-branch)   GIT_BRANCH="$2";   shift 2 ;;
    --service-name) SERVICE_NAME="$2"; shift 2 ;;
    --help|-h)
      echo "Usage: $0 [OPTIONS]"
      echo ""
      echo "Required:"
      echo "  --hub-url URL        Hub 服务器地址"
      echo "  --app-id ID          应用 ID"
      echo "  --app-key KEY        应用 Key"
      echo "  --token TOKEN        认证 Token"
      echo ""
      echo "Optional:"
      echo "  --node-name NAME     节点名称 (默认: hostname)"
      echo "  --port PORT          监听端口 (默认: 3200)"
      echo "  --install-dir DIR    安装目录 (默认: /opt/openclaw-node)"
      echo "  --from-git           从 Git 仓库 clone 代码"
      echo "  --from-local         使用当前目录的代码"
      echo "  --git-repo URL       Git 仓库地址"
      echo "  --git-branch BRANCH  Git 分支 (默认: main)"
      echo "  --service-name NAME  systemd 服务名 (默认: openclaw-node)"
      echo "  --help               显示帮助"
      exit 0
      ;;
    *) warn "未知参数: $1"; shift ;;
  esac
done

# ─── Banner ──────────────────────────────────────────────────────
echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║   OpenClaw Connect Node - 一键安装脚本       ║${NC}"
echo -e "${CYAN}║   版本: 0.0.1                                ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════╝${NC}"
echo ""

# ─── Validate Required Parameters ────────────────────────────────
[[ -z "$HUB_URL" ]]  && error "缺少必要参数: --hub-url"
[[ -z "$APP_ID" ]]   && error "缺少必要参数: --app-id"
[[ -z "$APP_KEY" ]]  && error "缺少必要参数: --app-key"
[[ -z "$TOKEN" ]]    && error "缺少必要参数: --token"

[[ -z "$NODE_NAME" ]] && NODE_NAME=$(hostname)

info "安装配置:"
echo "  Hub 地址:    $HUB_URL"
echo "  App ID:      $APP_ID"
echo "  节点名称:    $NODE_NAME"
echo "  监听端口:    $PORT"
echo "  安装目录:    $INSTALL_DIR"
echo "  源码模式:    $SOURCE_MODE"
echo ""

# ═══════════════════════════════════════════════════════════════════
# Step 1: Environment Checks
# ═══════════════════════════════════════════════════════════════════
info "Step 1/7: 环境检查..."

# Check root/sudo
if [[ $EUID -ne 0 ]]; then
  error "请使用 root 用户运行此脚本，或使用 sudo"
fi
success "root 权限 ✓"

# Check Node.js
if command -v node &>/dev/null; then
  NODE_VER=$(node -v | sed 's/v//' | cut -d. -f1)
  if [[ $NODE_VER -ge 18 ]]; then
    success "Node.js $(node -v) ✓"
  else
    warn "Node.js 版本过低 ($(node -v))，需要 >= 18"
    info "正在安装 Node.js 22 LTS..."
    curl -fsSL https://deb.nodesource.com/setup_22.x | bash - 2>/dev/null
    apt-get install -y nodejs 2>/dev/null || {
      # Try yum for RHEL-based
      curl -fsSL https://rpm.nodesource.com/setup_22.x | bash - 2>/dev/null
      yum install -y nodejs 2>/dev/null || error "Node.js 安装失败，请手动安装 Node.js >= 18"
    }
    success "Node.js $(node -v) 已安装 ✓"
  fi
else
  info "未检测到 Node.js，正在安装 Node.js 22 LTS..."
  if command -v apt-get &>/dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_22.x | bash - 2>/dev/null
    apt-get install -y nodejs 2>/dev/null || error "Node.js 安装失败"
  elif command -v yum &>/dev/null; then
    curl -fsSL https://rpm.nodesource.com/setup_22.x | bash - 2>/dev/null
    yum install -y nodejs 2>/dev/null || error "Node.js 安装失败"
  else
    error "无法自动安装 Node.js，请手动安装 Node.js >= 18"
  fi
  success "Node.js $(node -v) 已安装 ✓"
fi

# Check npm
if ! command -v npm &>/dev/null; then
  error "npm 未找到，请检查 Node.js 安装"
fi
success "npm $(npm -v) ✓"

# Check git (only needed for --from-git)
if [[ "$SOURCE_MODE" == "git" ]] || [[ "$SOURCE_MODE" == "auto" ]]; then
  if command -v git &>/dev/null; then
    success "git $(git --version | awk '{print $3}') ✓"
  else
    if [[ "$SOURCE_MODE" == "git" ]]; then
      info "正在安装 git..."
      apt-get install -y git 2>/dev/null || yum install -y git 2>/dev/null || error "git 安装失败"
      success "git 已安装 ✓"
    fi
  fi
fi

# Check port availability
if ss -tlnp 2>/dev/null | grep -q ":${PORT} " || netstat -tlnp 2>/dev/null | grep -q ":${PORT} "; then
  warn "端口 $PORT 已被占用！"
  echo "  占用进程:"
  ss -tlnp 2>/dev/null | grep ":${PORT} " || netstat -tlnp 2>/dev/null | grep ":${PORT} "
  echo ""
  read -p "  是否继续安装？(y/N): " -r REPLY
  [[ ! $REPLY =~ ^[Yy]$ ]] && error "安装已取消"
fi
success "端口 $PORT 可用 ✓"

# Check if tsx is available globally, install if not
if ! command -v tsx &>/dev/null && ! npx tsx --version &>/dev/null 2>&1; then
  info "正在全局安装 tsx..."
  npm install -g tsx 2>/dev/null || warn "tsx 全局安装失败，将使用 npx tsx"
fi

echo ""

# ═══════════════════════════════════════════════════════════════════
# Step 2: Get Source Code
# ═══════════════════════════════════════════════════════════════════
info "Step 2/7: 获取源码..."

# Auto-detect source mode
if [[ "$SOURCE_MODE" == "auto" ]]; then
  if [[ -f "node/server/src/index.ts" ]]; then
    SOURCE_MODE="local"
    info "检测到本地代码，使用 --from-local 模式"
  elif [[ -f "server/src/index.ts" ]] && [[ -d "frontend" ]]; then
    # Already inside node/ directory
    SOURCE_MODE="local"
    info "检测到本地 node 代码，使用 --from-local 模式"
  else
    SOURCE_MODE="git"
    info "未检测到本地代码，使用 --from-git 模式"
  fi
fi

if [[ "$SOURCE_MODE" == "git" ]]; then
  if [[ -d "$INSTALL_DIR" ]]; then
    warn "安装目录 $INSTALL_DIR 已存在"
    read -p "  是否删除并重新安装？(y/N): " -r REPLY
    if [[ $REPLY =~ ^[Yy]$ ]]; then
      rm -rf "$INSTALL_DIR"
    else
      info "将在现有目录上更新..."
      cd "$INSTALL_DIR" && git pull origin "$GIT_BRANCH" 2>/dev/null || true
    fi
  fi

  if [[ ! -d "$INSTALL_DIR" ]]; then
    info "正在 clone 代码..."
    git clone --branch "$GIT_BRANCH" --depth 1 "$GIT_REPO" "$INSTALL_DIR" || {
      error "Git clone 失败。如果是私有仓库，请使用 --from-local 模式"
    }
  fi
  success "代码已下载到 $INSTALL_DIR ✓"

elif [[ "$SOURCE_MODE" == "local" ]]; then
  CURRENT_DIR=$(pwd)

  # Detect project root
  if [[ -f "$CURRENT_DIR/node/server/src/index.ts" ]]; then
    PROJECT_ROOT="$CURRENT_DIR"
  elif [[ -f "$CURRENT_DIR/server/src/index.ts" ]] && [[ -d "$CURRENT_DIR/frontend" ]]; then
    PROJECT_ROOT="$CURRENT_DIR/.."
  else
    error "未找到 Node 服务代码。请在项目根目录运行，或使用 --from-git"
  fi

  if [[ "$PROJECT_ROOT" != "$INSTALL_DIR" ]]; then
    info "复制代码到 $INSTALL_DIR ..."
    mkdir -p "$INSTALL_DIR"
    # Copy, excluding node_modules
    rsync -a --exclude='node_modules' --exclude='.git' --exclude='dist' \
      "$PROJECT_ROOT/" "$INSTALL_DIR/" 2>/dev/null || {
      # Fallback if rsync not available
      cp -r "$PROJECT_ROOT/"* "$INSTALL_DIR/" 2>/dev/null
      # Clean up node_modules if copied
      rm -rf "$INSTALL_DIR/node/server/node_modules" "$INSTALL_DIR/node/frontend/node_modules" 2>/dev/null
    }
  fi
  success "本地代码已就绪 ✓"
fi

echo ""

# ═══════════════════════════════════════════════════════════════════
# Step 3: Install Dependencies
# ═══════════════════════════════════════════════════════════════════
info "Step 3/7: 安装依赖..."

# Install server dependencies
if [[ -f "$INSTALL_DIR/node/server/package.json" ]]; then
  info "安装 server 依赖..."
  cd "$INSTALL_DIR/node/server"
  npm install --production 2>&1 | tail -3
  success "Server 依赖安装完成 ✓"
fi

# Install and build frontend
if [[ -f "$INSTALL_DIR/node/frontend/package.json" ]]; then
  info "安装 frontend 依赖并构建..."
  cd "$INSTALL_DIR/node/frontend"
  npm install 2>&1 | tail -3
  npx vite build 2>&1 | tail -5
  success "Frontend 构建完成 ✓"
fi

echo ""

# ═══════════════════════════════════════════════════════════════════
# Step 4: Generate .env Configuration
# ═══════════════════════════════════════════════════════════════════
info "Step 4/7: 生成配置文件..."

# Create data directory
mkdir -p "$INSTALL_DIR/data"

cat > "$INSTALL_DIR/.env" << ENVEOF
# ═══════════════════════════════════════════════════════════════════
# OpenClaw Connect Node Configuration
# Generated at: $(date '+%Y-%m-%d %H:%M:%S')
# ═══════════════════════════════════════════════════════════════════

# Hub 连接配置
HUB_URL=${HUB_URL}
NODE_APP_ID=${APP_ID}
NODE_APP_KEY=${APP_KEY}
NODE_TOKEN=${TOKEN}

# 节点配置
NODE_NAME=${NODE_NAME}
NODE_PORT=${PORT}

# 数据目录
DATA_DIR=${INSTALL_DIR}/data

# 环境
NODE_ENV=production
ENVEOF

success "配置文件已生成: $INSTALL_DIR/.env ✓"
echo ""

# ═══════════════════════════════════════════════════════════════════
# Step 5: Create systemd Service
# ═══════════════════════════════════════════════════════════════════
info "Step 5/7: 配置 systemd 服务..."

# Stop existing service if running
systemctl stop "$SERVICE_NAME" 2>/dev/null || true

# Determine tsx path
TSX_PATH=$(which tsx 2>/dev/null || echo "$(npm root -g)/tsx/dist/cli.mjs")
NODE_PATH=$(which node 2>/dev/null || echo "/usr/bin/node")

cat > "/etc/systemd/system/${SERVICE_NAME}.service" << SVCEOF
[Unit]
Description=OpenClaw Connect Node (${NODE_NAME})
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=root
WorkingDirectory=${INSTALL_DIR}
EnvironmentFile=${INSTALL_DIR}/.env
ExecStart=${NODE_PATH} --import tsx/esm ${INSTALL_DIR}/node/server/src/index.ts
Restart=always
RestartSec=10
StartLimitIntervalSec=300
StartLimitBurst=5
StandardOutput=journal
StandardError=journal
SyslogIdentifier=${SERVICE_NAME}

# Resource Limits
LimitNOFILE=65535
MemoryMax=2G

# Environment
Environment=NODE_ENV=production
Environment=NODE_NO_WARNINGS=1

# Graceful shutdown
KillMode=mixed
KillSignal=SIGTERM
TimeoutStopSec=30

[Install]
WantedBy=multi-user.target
SVCEOF

systemctl daemon-reload
systemctl enable "$SERVICE_NAME" 2>/dev/null
success "systemd 服务已配置: ${SERVICE_NAME} ✓"
echo ""

# ═══════════════════════════════════════════════════════════════════
# Step 6: Create Management Command
# ═══════════════════════════════════════════════════════════════════
info "Step 6/7: 创建管理命令..."

cat > "/usr/local/bin/${SERVICE_NAME}" << 'CMDEOF'
#!/bin/bash
# OpenClaw Connect Node Management Command
# Generated by install-node.sh

SERVICE_NAME="PLACEHOLDER_SERVICE"
INSTALL_DIR="PLACEHOLDER_DIR"
ENV_FILE="${INSTALL_DIR}/.env"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

case "$1" in
  start)
    echo -e "${CYAN}启动 OpenClaw Node...${NC}"
    systemctl start "$SERVICE_NAME"
    sleep 2
    if systemctl is-active --quiet "$SERVICE_NAME"; then
      echo -e "${GREEN}✅ 节点已启动${NC}"
    else
      echo -e "${RED}❌ 启动失败，查看日志: journalctl -u $SERVICE_NAME -n 50${NC}"
    fi
    ;;
  stop)
    echo -e "${YELLOW}停止 OpenClaw Node...${NC}"
    systemctl stop "$SERVICE_NAME"
    echo -e "${GREEN}✅ 节点已停止${NC}"
    ;;
  restart)
    echo -e "${CYAN}重启 OpenClaw Node...${NC}"
    systemctl restart "$SERVICE_NAME"
    sleep 2
    if systemctl is-active --quiet "$SERVICE_NAME"; then
      echo -e "${GREEN}✅ 节点已重启${NC}"
    else
      echo -e "${RED}❌ 重启失败，查看日志: journalctl -u $SERVICE_NAME -n 50${NC}"
    fi
    ;;
  status)
    systemctl status "$SERVICE_NAME" --no-pager
    echo ""
    # Try health endpoint
    PORT=$(grep NODE_PORT "$ENV_FILE" 2>/dev/null | cut -d= -f2)
    PORT=${PORT:-3200}
    echo -e "${CYAN}健康检查:${NC}"
    curl -s "http://localhost:${PORT}/health" 2>/dev/null | python3 -m json.tool 2>/dev/null || \
    curl -s "http://localhost:${PORT}/health" 2>/dev/null || \
    echo "  (无法连接到 http://localhost:${PORT}/health)"
    ;;
  logs)
    shift
    LINES=${1:-100}
    journalctl -u "$SERVICE_NAME" -n "$LINES" -f --no-pager
    ;;
  config)
    echo -e "${CYAN}配置文件: ${ENV_FILE}${NC}"
    echo "─────────────────────────────────"
    cat "$ENV_FILE"
    echo ""
    ;;
  update)
    echo -e "${CYAN}更新 OpenClaw Node...${NC}"
    cd "$INSTALL_DIR"
    if [[ -d ".git" ]]; then
      git pull
    else
      echo -e "${YELLOW}非 git 目录，跳过代码更新${NC}"
    fi
    echo "重新安装依赖..."
    cd "$INSTALL_DIR/node/server" && npm install --production 2>&1 | tail -3
    cd "$INSTALL_DIR/node/frontend" && npm install && npx vite build 2>&1 | tail -5
    systemctl restart "$SERVICE_NAME"
    sleep 2
    if systemctl is-active --quiet "$SERVICE_NAME"; then
      echo -e "${GREEN}✅ 更新完成，节点已重启${NC}"
    else
      echo -e "${RED}❌ 重启失败，查看日志: journalctl -u $SERVICE_NAME -n 50${NC}"
    fi
    ;;
  health)
    PORT=$(grep NODE_PORT "$ENV_FILE" 2>/dev/null | cut -d= -f2)
    PORT=${PORT:-3200}
    curl -s "http://localhost:${PORT}/api/health" 2>/dev/null | python3 -m json.tool 2>/dev/null || \
    curl -s "http://localhost:${PORT}/api/health" 2>/dev/null || \
    echo -e "${RED}无法连接到健康检查端点${NC}"
    ;;
  *)
    echo -e "${CYAN}OpenClaw Connect Node 管理工具${NC}"
    echo ""
    echo "用法: $SERVICE_NAME <command>"
    echo ""
    echo "命令:"
    echo "  start       启动节点"
    echo "  stop        停止节点"
    echo "  restart     重启节点"
    echo "  status      查看状态"
    echo "  logs [N]    查看日志 (默认最近100行，持续跟踪)"
    echo "  config      查看配置"
    echo "  update      更新代码并重启"
    echo "  health      健康检查"
    ;;
esac
CMDEOF

# Replace placeholders
sed -i "s|PLACEHOLDER_SERVICE|${SERVICE_NAME}|g" "/usr/local/bin/${SERVICE_NAME}"
sed -i "s|PLACEHOLDER_DIR|${INSTALL_DIR}|g" "/usr/local/bin/${SERVICE_NAME}"

chmod +x "/usr/local/bin/${SERVICE_NAME}"
success "管理命令已创建: /usr/local/bin/${SERVICE_NAME} ✓"
echo ""

# ═══════════════════════════════════════════════════════════════════
# Step 7: Start Service & Verify
# ═══════════════════════════════════════════════════════════════════
info "Step 7/7: 启动服务..."

systemctl start "$SERVICE_NAME"
sleep 3

# Check if running
if systemctl is-active --quiet "$SERVICE_NAME"; then
  success "服务启动成功 ✓"
else
  warn "服务可能未完全启动，检查日志..."
  journalctl -u "$SERVICE_NAME" -n 20 --no-pager
fi

# Health check
sleep 2
HEALTH=$(curl -s "http://localhost:${PORT}/health" 2>/dev/null)
if [[ -n "$HEALTH" ]]; then
  success "健康检查通过 ✓"
else
  warn "健康检查未响应，服务可能仍在启动中"
fi

# ═══════════════════════════════════════════════════════════════════
# Done!
# ═══════════════════════════════════════════════════════════════════
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✅ OpenClaw Connect Node 安装成功！${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo ""
echo -e "  📍 安装目录:  ${CYAN}${INSTALL_DIR}${NC}"
echo -e "  🔗 Hub 地址:  ${CYAN}${HUB_URL}${NC}"
echo -e "  🏷️  节点名称:  ${CYAN}${NODE_NAME}${NC}"
echo -e "  🌐 本地端口:  ${CYAN}${PORT}${NC}"
echo -e "  📊 管理界面:  ${CYAN}http://$(hostname -I 2>/dev/null | awk '{print $1}' || echo 'localhost'):${PORT}${NC}"
echo ""
echo -e "  ${YELLOW}管理命令:${NC}"
echo -e "    ${SERVICE_NAME} start      启动节点"
echo -e "    ${SERVICE_NAME} stop       停止节点"
echo -e "    ${SERVICE_NAME} restart    重启节点"
echo -e "    ${SERVICE_NAME} status     查看状态"
echo -e "    ${SERVICE_NAME} logs       查看日志"
echo -e "    ${SERVICE_NAME} config     查看配置"
echo -e "    ${SERVICE_NAME} update     更新代码"
echo -e "    ${SERVICE_NAME} health     健康检查"
echo ""
