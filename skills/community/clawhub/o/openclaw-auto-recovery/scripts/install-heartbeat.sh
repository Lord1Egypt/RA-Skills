#!/bin/bash
# 安装 infra-heartbeat systemd 服务
# 用法: install-heartbeat.sh [--config <配置文件>]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
HEARTBEAT_SCRIPT="${SKILL_DIR}/scripts/heartbeat-daemon.sh"

SYSTEMD_DIR="${HOME}/.config/systemd/user"
SERVICE_FILE="${SYSTEMD_DIR}/heartbeat-daemon.service"
CONFIG_DIR="${HOME}/.config/infra-heartbeat"
CONFIG_FILE="${CONFIG_DIR}/config.env"

# 默认配置值（可被配置文件覆盖）
DEFAULT_FEISHU_APP_ID="${FEISHU_APP_ID:-cli_xxxxxxxxxxxxxxxxxxxxxxxxxxxx}"
DEFAULT_FEISHU_APP_SECRET="${FEISHU_APP_SECRET:-}"
DEFAULT_GATEWAY_TOKEN="${GATEWAY_TOKEN:-}"
DEFAULT_GATEWAY_PORT="${GATEWAY_PORT:-18789}"
DEFAULT_TARGET_OPEN_ID="${TARGET_OPEN_ID:-}"
DEFAULT_OPENCLAW_JSON="${OPENCLAW_JSON:-${HOME}/.openclaw/openclaw.json}"
DEFAULT_CHECK_INTERVAL="${CHECK_INTERVAL:-180}"
DEFAULT_MAX_RESTART_FAILS="${MAX_RESTART_FAILS:-3}"
DEFAULT_DISK_THRESHOLD="${DISK_THRESHOLD:-80}"
DEFAULT_MEM_THRESHOLD="${MEM_THRESHOLD:-85}"
DEFAULT_CPU_THRESHOLD="${CPU_THRESHOLD:-60}"

show_help() {
    echo "install-heartbeat.sh — 安装 infra-heartbeat systemd 服务"
    echo ""
    echo "用法: install-heartbeat.sh [--config <配置文件>]"
    echo ""
    echo "参数:"
    echo "  --config <文件>   覆盖默认配置的配置文件路径"
    echo "  --dry-run         仅显示将要执行的操作，不实际安装"
    echo "  --help            显示帮助"
}

DRY_RUN=false
CONFIG_OVERRIDE=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run) DRY_RUN=true; shift ;;
        --config) CONFIG_OVERRIDE="$2"; shift 2 ;;
        --help|-h) show_help; exit 0 ;;
        *) echo "未知参数: $1"; show_help; exit 1 ;;
    esac
done

# 检查 heartbeat-daemon.sh 是否存在
if [[ ! -f "$HEARTBEAT_SCRIPT" ]]; then
    echo "ERROR: 找不到 heartbeat-daemon.sh: $HEARTBEAT_SCRIPT" >&2
    exit 1
fi

# 检测 ws_module 路径
detect_ws_module() {
    local ws_path
    ws_path=$(find "${HOME}/.npm-global/lib/node_modules/openclaw" -path "*/node_modules/ws" -maxdepth 6 2>/dev/null | head -1)
    if [[ -z "$ws_path" ]]; then
        echo "ERROR: 无法找到 openclaw ws module" >&2
        return 1
    fi
    echo "$ws_path"
}

WS_MODULE_PATH=$(detect_ws_module)
echo "检测到 WS module: $WS_MODULE_PATH"

# 加载已有配置（如果有）
if [[ -n "$CONFIG_OVERRIDE" && -f "$CONFIG_OVERRIDE" ]]; then
    echo "使用配置: $CONFIG_OVERRIDE"
    set -a
    source "$CONFIG_OVERRIDE"
    set +a
elif [[ -f "$CONFIG_FILE" ]]; then
    echo "使用现有配置: $CONFIG_FILE"
    set -a
    source "$CONFIG_FILE"
    set +a
fi

# 提示缺失的必要配置
missing=()
[[ -z "${FEISHU_APP_ID:-}" ]] && missing+=("FEISHU_APP_ID")
[[ -z "${FEISHU_APP_SECRET:-}" ]] && missing+=("FEISHU_APP_SECRET")
[[ -z "${GATEWAY_TOKEN:-}" ]] && missing+=("GATEWAY_TOKEN")
[[ -z "${TARGET_OPEN_ID:-}" ]] && missing+=("TARGET_OPEN_ID")

if [[ ${#missing[@]} -gt 0 ]]; then
    echo "ERROR: 以下必填配置缺失: ${missing[*]}" >&2
    echo "请创建配置文件: $CONFIG_FILE"
    echo ""
    generate_config_sample
    exit 1
fi

generate_config_sample() {
    cat <<EOF
# infra-heartbeat 配置文件模板
# 路径: $CONFIG_FILE

# === 必填 ===
FEISHU_APP_ID="${DEFAULT_FEISHU_APP_ID}"
FEISHU_APP_SECRET="${DEFAULT_FEISHU_APP_SECRET}"
GATEWAY_TOKEN="${DEFAULT_GATEWAY_TOKEN}"
TARGET_OPEN_ID="${DEFAULT_TARGET_OPEN_ID}"

# === 可选（带默认值）===
GATEWAY_PORT="${DEFAULT_GATEWAY_PORT}"
OPENCLAW_JSON="${DEFAULT_OPENCLAW_JSON}"
CHECK_INTERVAL="${DEFAULT_CHECK_INTERVAL}"
MAX_RESTART_FAILS="${DEFAULT_MAX_RESTART_FAILS}"
DISK_THRESHOLD="${DEFAULT_DISK_THRESHOLD}"
MEM_THRESHOLD="${DEFAULT_MEM_THRESHOLD}"
CPU_THRESHOLD="${DEFAULT_CPU_THRESHOLD}"

# === 自动检测（通常不需要改）===
WS_MODULE="$WS_MODULE_PATH"
EOF
}

echo ""
echo "=== 安装计划 ==="
echo "Systemd service: $SERVICE_FILE"
echo "Config file: $CONFIG_FILE"
echo "HEARTBEAT script: $HEARTBEAT_SCRIPT"
echo ""

if [[ "$DRY_RUN" == true ]]; then
    echo "[dry-run] 以下文件将被创建:"
    echo "  $SERVICE_FILE"
    echo "  $CONFIG_FILE"
    echo ""
    generate_config_sample
    exit 0
fi

# 读取交互式配置（如果必填缺失）
read_config_interactive() {
    local var_name=$1
    local prompt=$2
    local default=$3
    local value=""

    # 如果已经有值则跳过
    [[ -n "${!var_name:-}" ]] && return 0

    echo -n "$prompt"
    if [[ -n "$default" ]]; then
        echo -n " [$default]"
    fi
    echo -n ": "
    read -r value
    value="${value:-$default}"
    declare "$var_name=$value"
}

echo ""
echo "=== 交互式配置 ==="
echo "（直接回车使用默认值，已在配置文件中的值会被使用）"
echo ""

if [[ -z "${FEISHU_APP_ID:-}" ]]; then
    read_config_interactive FEISHU_APP_ID "飞书 App ID" "$DEFAULT_FEISHU_APP_ID"
fi
if [[ -z "${FEISHU_APP_SECRET:-}" ]]; then
    read_config_interactive FEISHU_APP_SECRET "飞书 App Secret" ""
fi
if [[ -z "${GATEWAY_TOKEN:-}" ]]; then
    read_config_interactive GATEWAY_TOKEN "Gateway Token" ""
fi
if [[ -z "${TARGET_OPEN_ID:-}" ]]; then
    read_config_interactive TARGET_OPEN_ID "飞书通知目标 Open ID" "$DEFAULT_TARGET_OPEN_ID"
fi

# 写入配置文件
mkdir -p "$CONFIG_DIR"
generate_config_sample | sed "s|^WS_MODULE=.*|WS_MODULE=\"${WS_MODULE_PATH}\"|" > "$CONFIG_FILE"
chmod 600 "$CONFIG_FILE"
echo "✅ 配置文件已写入: $CONFIG_FILE"

# 写入 systemd service
mkdir -p "$SYSTEMD_DIR"
cat > "$SERVICE_FILE" <<EOF
[Unit]
Description=Infra Heartbeat Daemon
After=network.target openclaw-gateway.service

[Service]
Type=simple
ExecStart=${HEARTBEAT_SCRIPT} --config ${CONFIG_FILE}
Restart=always
RestartSec=10
StandardOutput=null
StandardError=null

[Install]
WantedBy=default.target
EOF
echo "✅ Systemd service 已写入: $SERVICE_FILE"

# 重载 systemd 并启用
systemctl --user daemon-reload
systemctl --user enable heartbeat-daemon.service
systemctl --user start heartbeat-daemon.service

echo ""
echo "=== 安装完成 ==="
systemctl --user status heartbeat-daemon.service --no-pager

echo ""
echo "日志: tail -f ~/.openclaw/workspace-infra/heartbeat.log"
echo ""
echo "常用命令:"
echo "  systemctl --user status heartbeat-daemon  # 查看状态"
echo "  systemctl --user restart heartbeat-daemon # 重启"
echo "  journalctl --user -u heartbeat-daemon -f  # 查看日志"
