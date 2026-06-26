#!/bin/bash
# 节点小宝 (JDxB) Management Script for OpenClaw
# Usage: bash jdxb.sh <status|start|stop|restart|logs|pair|install|update|uninstall>

set -e

APP_NAME="owjdxb"
VERSION="4.0.10-579"
BASE_URL="http://cdn.ionewu.com/upgrade/d"
PORT=9118
INSTALL_DIR="$HOME/owjdxb"
SERVICE_FILE="/etc/systemd/system/${APP_NAME}.service"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

info()  { echo -e "${CYAN}$1${NC}"; }
ok()    { echo -e "${GREEN}$1${NC}"; }
warn()  { echo -e "${YELLOW}$1${NC}"; }
err()   { echo -e "${RED}$1${NC}"; exit 1; }

ensure_root() {
    [[ $EUID -ne 0 ]] && err "需要 root 权限，请用 sudo 运行"
}

status_cmd() {
    echo "============================================="
    info "📋 节点小宝 (JDxB) 服务状态"
    echo "============================================="
    
    if [[ ! -f "$SERVICE_FILE" ]]; then
        warn "未安装 (找不到 $SERVICE_FILE)"
        return 1
    fi

    systemctl status "${APP_NAME}.service" --no-pager 2>/dev/null || true
    
    # Version info
    local ver_file="$INSTALL_DIR/ownbsv/.version"
    if [[ -f "$ver_file" ]]; then
        echo ""
        ok "版本: $(cat "$ver_file")"
    fi
    
    # Check port
    if ss -tuln 2>/dev/null | grep -q ":${PORT} "; then
        ok "端口: ${PORT} 正在监听 ✓"
    else
        warn "端口: ${PORT} 未监听"
    fi
}

start_cmd() {
    ensure_root
    systemctl start "${APP_NAME}.service"
    ok "✅ 服务已启动"
}

stop_cmd() {
    ensure_root
    systemctl stop "${APP_NAME}.service"
    ok "✅ 服务已停止"
}

restart_cmd() {
    ensure_root
    systemctl restart "${APP_NAME}.service"
    ok "✅ 服务已重启"
}

logs_cmd() {
    journalctl -u "${APP_NAME}.service" -n 50 --no-pager
}

get_pair_url() {
    local max_retries=30
    local retry_delay=3
    local pairing_url=""
    
    info "🔍 获取配对信息..."
    
    for ((i=1; i<=max_retries; i++)); do
        local response
        response=$(curl -v -s -o /dev/null "http://127.0.0.1:${PORT}" 2>&1)
        local location_line
        location_line=$(echo "$response" | grep -i "Location:" | head -n 1)
        
        if [[ -n "$location_line" ]]; then
            pairing_url=$(echo "$location_line" | sed -n 's/^[^:]*:[[:space:]]*//p')
            break
        fi
        
        if [[ $i -lt $max_retries ]]; then
            echo -n "."
            sleep "$retry_delay"
        fi
    done
    echo ""
    
    if [[ -z "$pairing_url" ]]; then
        warn "⚠️  无法获取配对 URL，请检查服务是否运行"
        return 1
    fi
    
    ok "🔗 配对 URL: ${pairing_url}"
    
    # Extract params and get active code
    local pid t s
    if [[ "$pairing_url" =~ pid=([^&]*) ]]; then pid="${BASH_REMATCH[1]}"; fi
    if [[ "$pairing_url" =~ t=([0-9]+) ]]; then t="${BASH_REMATCH[1]}"; fi
    if [[ "$pairing_url" =~ s=([0-9]+) ]]; then s="${BASH_REMATCH[1]}"; fi
    
    if [[ -n "$pid" && -n "$t" && -n "$s" ]]; then
        local activecode_url="https://dpis.ionewu.com/dp/box/activecode?pid=${PID:-$pid}&appid=WanWu&product=2581&t=${t}&s=${s}"
        local code_response
        code_response=$(curl -s "$activecode_url")
        
        if [[ "$code_response" =~ \"activecode\"[[:space:]]*:[[:space:]]*\"([^\"]+)\" ]]; then
            ok "🔑 激活码: ${BASH_REMATCH[1]}"
        elif [[ "$code_response" =~ \"uid\"[[:space:]]*:[[:space:]]*\"([^\"]+)\" ]]; then
            ok "🆔 UID: ${BASH_REMATCH[1]}"
        else
            warn "⚠️  无法解析激活码，请手动访问配对 URL"
        fi
    fi
}

pair_cmd() {
    get_pair_url
}

install_cmd() {
    ensure_root
    
    [[ "$(uname -s)" == "Linux" ]] || err "仅支持 Linux"
    
    local arch=$(uname -m)
    local filename
    case "$arch" in
        x86_64)  filename="${APP_NAME}_linux_x64_${VERSION}.tgz" ;;
        aarch64) filename="${APP_NAME}_linux_arm64_${VERSION}.tgz" ;;
        armv7l|armv6l|armv5tel) filename="${APP_NAME}_linux_arm32_${VERSION}.tgz" ;;
        *) err "不支持的架构: $arch (支持 x86_64, ARM64, ARM32)" ;;
    esac
    
    local url="${BASE_URL}/${filename}"
    local workdir
    workdir=$(dirname "$INSTALL_DIR")
    
    info "📥 下载 ${filename}..."
    cd "$workdir"
    
    if [[ ! -f "${filename}" ]]; then
        curl -fSL --progress-bar -O "${url}" || err "下载失败"
        ok "✅ 下载完成"
    else
        ok "文件已存在，跳过下载"
    fi
    
    if [[ -d "${APP_NAME}" ]]; then
        warn "清理旧目录..."
        rm -rf "${APP_NAME}"
    fi
    
    info "📦 解压..."
    tar -xzf "${filename}" || err "解压失败"
    
    local exec_script="${workdir}/${APP_NAME}/start.sh"
    [[ -f "$exec_script" ]] || err "找不到 start.sh"
    chmod +x "$exec_script"
    
    info "⚙️  创建 systemd 服务..."
    cat > "$SERVICE_FILE" << EOF
[Unit]
Description=Owjdxb Service
After=network.target
Wants=network.target

[Service]
Type=oneshot
User=root
Group=root
WorkingDirectory=${workdir}/${APP_NAME}
ExecStart=${exec_script}
RemainAfterExit=yes
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
    
    systemctl daemon-reload
    systemctl enable "${APP_NAME}.service"
    
    info "🚀 启动服务..."
    systemctl restart "${APP_NAME}.service"
    
    sleep 3
    ok "✅ 安装完成！"
    echo ""
    info "管理命令:"
    echo "  sudo systemctl stop ${APP_NAME}.service"
    echo "  sudo systemctl start ${APP_NAME}.service"
    echo "  sudo systemctl status ${APP_NAME}.service"
    echo "  sudo systemctl restart ${APP_NAME}.service"
    echo ""
    
    get_pair_url
}

update_cmd() {
    install_cmd
}

uninstall_cmd() {
    ensure_root
    
    if [[ -f "${INSTALL_DIR}/bin/owjdxb" ]]; then
        chmod +x "${INSTALL_DIR}/bin/owjdxb"
        "${INSTALL_DIR}/bin/owjdxb" --kill=yes
        sleep 2
    fi
    
    systemctl stop "${APP_NAME}.service" 2>/dev/null || true
    systemctl disable "${APP_NAME}.service" 2>/dev/null || true
    rm -f "$SERVICE_FILE"
    systemctl daemon-reload
    
    if [[ -d "${INSTALL_DIR}" ]]; then
        rm -rf "${INSTALL_DIR}"
    fi
    
    ok "✅ 已卸载节点小宝"
}

case "${1:-status}" in
    status)     status_cmd ;;
    start)      start_cmd ;;
    stop)       stop_cmd ;;
    restart)    restart_cmd ;;
    logs)       logs_cmd ;;
    pair)       pair_cmd ;;
    install)    install_cmd ;;
    update)     update_cmd ;;
    uninstall)  uninstall_cmd ;;
    *)
        echo "用法: $0 <status|start|stop|restart|logs|pair|install|update|uninstall>"
        exit 1
        ;;
esac
