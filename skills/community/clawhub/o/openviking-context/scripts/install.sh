#!/usr/bin/env bash
set -euo pipefail

BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m'

log_info()  { echo -e "${GREEN}[✓]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[!]${NC} $1"; }
log_error() { echo -e "${RED}[✗]${NC} $1"; }
log_step()  { echo -e "\n${BOLD}▸ $1${NC}"; }

WORKSPACE_DIR="${OPENVIKING_WORKSPACE:-$HOME/openviking_workspace}"
CONFIG_DIR="$HOME/.openviking"

log_step "检查 Python 版本"
if ! command -v python3 &>/dev/null; then
    log_error "未找到 python3，请先安装 Python 3.10+"
    exit 1
fi

PY_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
PY_MAJOR=$(echo "$PY_VERSION" | cut -d. -f1)
PY_MINOR=$(echo "$PY_VERSION" | cut -d. -f2)

if [ "$PY_MAJOR" -lt 3 ] || ([ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 10 ]); then
    log_error "Python 版本 $PY_VERSION 不满足要求，需要 >= 3.10"
    exit 1
fi
log_info "Python $PY_VERSION ✓"

log_step "安装 OpenViking Python 包"
pip install openviking --upgrade --force-reinstall 2>&1 | tail -5
log_info "openviking 安装完成"

log_step "创建工作目录"
mkdir -p "$WORKSPACE_DIR"
mkdir -p "$CONFIG_DIR"
log_info "工作目录: $WORKSPACE_DIR"
log_info "配置目录: $CONFIG_DIR"

log_step "是否安装 Rust CLI (ov)? [y/N]"
read -r INSTALL_CLI
if [[ "$INSTALL_CLI" =~ ^[Yy]$ ]]; then
    if command -v cargo &>/dev/null; then
        log_info "通过 cargo 安装 ov_cli..."
        cargo install --git https://github.com/volcengine/OpenViking ov_cli
    else
        log_info "通过安装脚本安装 ov..."
        curl -fsSL https://raw.githubusercontent.com/volcengine/OpenViking/main/crates/ov_cli/install.sh | bash
    fi
    log_info "Rust CLI 安装完成"
else
    log_info "跳过 Rust CLI 安装"
fi

log_step "设置环境变量"
SHELL_RC=""
if [ -f "$HOME/.zshrc" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_RC="$HOME/.bashrc"
fi

if [ -n "$SHELL_RC" ]; then
    if ! grep -q "OPENVIKING_CONFIG_FILE" "$SHELL_RC" 2>/dev/null; then
        {
            echo ""
            echo "# OpenViking"
            echo "export OPENVIKING_CONFIG_FILE=$CONFIG_DIR/ov.conf"
            echo "export OPENVIKING_CLI_CONFIG_FILE=$CONFIG_DIR/ovcli.conf"
        } >> "$SHELL_RC"
        log_info "环境变量已写入 $SHELL_RC"
    else
        log_warn "环境变量已存在于 $SHELL_RC，跳过"
    fi
fi

export OPENVIKING_CONFIG_FILE="$CONFIG_DIR/ov.conf"
export OPENVIKING_CLI_CONFIG_FILE="$CONFIG_DIR/ovcli.conf"

log_step "验证安装"
if python3 -c "import openviking; print(f'openviking {openviking.__version__}')" 2>/dev/null; then
    log_info "OpenViking 导入成功"
else
    log_warn "无法导入 openviking，可能需要重新安装"
fi

echo ""
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo -e "${GREEN}  OpenViking 安装完成！${NC}"
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo ""
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "下一步："
echo "  1. 运行配置脚本:  bash $SCRIPT_DIR/setup-config.sh"
echo "  2. 启动服务器:    openviking-server"
echo "  3. 测试连接:      python3 $SCRIPT_DIR/viking.py info"
echo ""
