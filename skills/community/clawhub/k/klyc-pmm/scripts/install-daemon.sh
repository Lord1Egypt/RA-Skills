#!/bin/bash
# klyc-pmm 9.3.12 — 全自动守护安装器
# ⚠️ 安装前请了解：本脚本会检查依赖、写入/etc/systemd/system、启用并启动systemd服务。
#    守护启动后会持续监听文件变更并自动通过HTTPS推送到kunlunyaochi.com。
# 用法: bash install-daemon.sh [--user-id N] [--tier dingxinfu|huhunfu|fenshenfu]
set -euo pipefail

VERSION="9.3.12"
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo -e "${GREEN}  klyc-pmm v${VERSION} 守护安装器${NC}"
echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo ""

# ─── 依赖检查 ───
for cmd in jq curl inotifywait; do
    command -v "$cmd" >/dev/null 2>&1 || {
        echo -e "${RED}❌ 缺少依赖: $cmd${NC}"
        case "$cmd" in
            jq) echo "   安装: apt install jq / yum install jq" ;;
            inotifywait) echo "   安装: apt install inotify-tools / yum install inotify-tools" ;;
        esac
        exit 1
    }
done
echo "✅ 依赖齐全 (jq curl inotifywait)"

# ─── 参数解析 ───
# （2026-09-11 修正：新增 --help/-h 识别，避免"想查帮助却误装守护"）
usage() {
    cat <<'USAGE'
用法: bash install-daemon.sh [选项]

选项:
  --user-id N       指定 AI 体 user_id（默认自动发现）
  --tier  <等级>    产品等级: dingxinfu | huhunfu | fenshenfu
  -h, --help        显示本帮助并退出（不做任何安装/系统更改）

说明:
  本脚本会写入 /etc/systemd/system/<name>.service 并启用、启动 systemd 守护。
  守护启动后持续监听文件变更并自动通过 HTTPS 推送到 kunlunyaochi.com。
USAGE
}

USER_ID=""
TIER=""
while [ $# -gt 0 ]; do
    case "$1" in
        -h|--help) usage; exit 0 ;;
        --user-id) USER_ID="$2"; shift 2 ;;
        --tier) TIER="$2"; shift 2 ;;
        --tier=*) TIER="${1#*=}"; shift ;;
        *) shift ;;
    esac
done

# ─── 发现工作区 ───
WS=""
for ws in \
    "${LIGHTCLAW_WORKSPACE:-}" \
    "${HOME:-/root}/.lightclaw/workspace" \
    "${HOME:-/root}/.openclaw/workspace" \
    "${HOME:-/root}/workspace" \
    ; do
    [ -n "$ws" ] && [ -f "$ws/MEMORY.md" ] && { WS="$ws"; break; }
done

if [ -z "$WS" ]; then
    WS=$(find "${HOME:-/root}" -maxdepth 4 -name MEMORY.md -type f 2>/dev/null | head -1 | xargs dirname 2>/dev/null)
fi

if [ -z "$WS" ] || [ ! -f "$WS/MEMORY.md" ]; then
    echo -e "${RED}❌ 未找到工作区 (需包含 MEMORY.md)${NC}"
    echo "   请手动指定: bash install-daemon.sh /path/to/workspace"
    exit 1
fi
echo "✅ 工作区: $WS"

# ─── 检测 user_id ───
if [ -z "$USER_ID" ] && [ -f "$WS/IDENTITY.md" ]; then
    USER_ID=$(grep -oP '(?:昆仑ID|瑶池ID|ID|id)[：:=]\s*\K\d+' "$WS/IDENTITY.md" 2>/dev/null | head -1)
fi
if [ -z "$USER_ID" ]; then
    echo -e "${YELLOW}⚠️ 未能自动检测 user_id，守护将以通用模式运行${NC}"
    echo "   建议在 IDENTITY.md 中添加: ID: <你的数字ID>"
fi

# ─── 检测/设置产品等级 ───
REAL_HOME="$(getent passwd "$(id -un 2>/dev/null || echo root)" 2>/dev/null | cut -d: -f6 || echo "$HOME")"
CONFIG_DIR="$REAL_HOME/.klyc-pmm"
mkdir -p "$CONFIG_DIR"

if [ -z "$TIER" ]; then
    if [ -f "$CONFIG_DIR/product_tier" ]; then
        TIER=$(cat "$CONFIG_DIR/product_tier")
    else
        TIER="dingxinfu"  # 默认容灾备份
    fi
fi

case "$TIER" in
    dingxinfu) TIER_LABEL="容灾备份" ;;
    huhunfu)   TIER_LABEL="守护记忆" ;;
    fenshenfu) TIER_LABEL="记忆分身" ;;
    *) echo -e "${RED}无效等级: $TIER${NC}"; exit 1 ;;
esac
echo "$TIER" > "$CONFIG_DIR/product_tier"
echo "✅ 产品等级: $TIER_LABEL"

# ─── 按等级生成文件列表 ───
FILES=()
[ -f "$WS/MEMORY.md" ] && FILES+=("$WS/MEMORY.md")
[ -f "$WS/SOUL.md" ] && FILES+=("$WS/SOUL.md")
[ -f "$WS/AGENTS.md" ] && FILES+=("$WS/AGENTS.md")
[ -f "$WS/USER.md" ] && FILES+=("$WS/USER.md")
[ -f "$WS/IDENTITY.md" ] && FILES+=("$WS/IDENTITY.md")
[ -f "$WS/TOOLS.md" ] && FILES+=("$WS/TOOLS.md")

if [ "$TIER" != "dingxinfu" ]; then
    [ -f "$WS/HEARTBEAT.md" ] && FILES+=("$WS/HEARTBEAT.md")
    if [ -d "$WS/memory" ]; then
        while IFS= read -r f; do FILES+=("$f"); done < <(find "$WS/memory" -maxdepth 1 \( -name "*.md" -o -name "*.json" \) -type f 2>/dev/null)
    fi
fi

if [ "$TIER" = "fenshenfu" ] && [ -d "$WS/arena" ]; then
    while IFS= read -r f; do FILES+=("$f"); done < <(find "$WS/arena" -maxdepth 1 -name "*.md" -type f 2>/dev/null)
fi

echo "✅ 纳入守护: ${#FILES[@]} 个文件"

# ─── 定位 pmm_watch.sh ───
PMM_SCRIPT=""
for p in \
    /root/bin/pmm_watch.sh \
    ./pmm_watch.sh \
    ./scripts/pmm_watch.sh \
    "$(dirname "$0")/pmm_watch.sh" \
    "$(dirname "$0")/scripts/pmm_watch.sh" \
    ; do
    [ -f "$p" ] && { PMM_SCRIPT="$p"; break; }
done

if [ -z "$PMM_SCRIPT" ]; then
    echo -e "${RED}❌ 未找到 pmm_watch.sh${NC}"
    echo "   请先安装 klyc-pmm skill 包"
    exit 1
fi
echo "✅ pmm_watch.sh: $PMM_SCRIPT"

# ─── 生成 systemd service（2026-09-11 审核修正 T07：追加 User= / 参数转义 / 沙箱加固）───
SERVICE_NAME="klyc-pmm-watch.service"
SERVICE_PATH="/etc/systemd/system/$SERVICE_NAME"

# 运行用户（默认当前用户；root 场景显式声明，避免以 root 无边界运行）
RUN_USER="${SUDO_USER:-$(id -un 2>/dev/null || echo root)}"
RUN_GROUP="$(id -gn "$RUN_USER" 2>/dev/null || echo "$RUN_USER")"

# 参数转义：每个路径用 systemd 单元语法做引号包裹，防注入/传参错误
quote_unit_arg() {
    local a="$1"
    a="${a//\\/\\\\}"        # 反斜杠转义
    a="${a//\"/\\\"}"          # 双引号转义
    printf '"%s"' "$a"
}
FILES_ARGS=""
for f in "${FILES[@]}"; do FILES_ARGS="$FILES_ARGS $(quote_unit_arg "$f")"; done

USER_ID_ARG=""
[ -n "$USER_ID" ] && USER_ID_ARG="--user-id $USER_ID"

cat > "$SERVICE_PATH" << UNIT
[Unit]
Description=klyc-pmm Watch Daemon (${TIER_LABEL})
After=network-online.target
Wants=network-online.target
StartLimitBurst=3
StartLimitIntervalSec=120

[Service]
Type=simple
User=${RUN_USER}
Group=${RUN_GROUP}
ExecStartPre=-/usr/bin/pkill -f "inotifywait.*${SERVICE_NAME}" 2>/dev/null || true
ExecStart=$(quote_unit_arg "$PMM_SCRIPT") watch $USER_ID_ARG$FILES_ARGS
Restart=always
RestartSec=30
# 安全加固（最小权限）
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=full
ProtectHome=read-only
MemoryMax=32M
MemoryHigh=24M
OOMScoreAdjust=500
LimitNOFILE=4096
KillMode=mixed
KillSignal=SIGTERM
TimeoutStopSec=10

[Install]
WantedBy=multi-user.target
UNIT

echo "✅ systemd unit 已写入: $SERVICE_PATH"

# ─── 启动（需用户明确确认） ───
read -p "是否启用 systemd 守护服务？按回车确认 " CONFIRM
systemctl daemon-reload
systemctl enable "$SERVICE_NAME" 2>/dev/null || true
systemctl restart "$SERVICE_NAME" 2>/dev/null || {
    echo -e "${YELLOW}⚠️ 无法启动 systemd 服务（可能无 root 权限）${NC}"
    echo ""
    echo "  手动启动:"
    echo "  $PMM_SCRIPT watch $USER_ID_ARG$FILES_ARGS"
    exit 0
}

sleep 2
if systemctl is-active --quiet "$SERVICE_NAME"; then
    echo ""
    echo -e "${GREEN}═══════════════════════════════════════${NC}"
    echo -e "${GREEN}  ✅ 守护已启动${NC}"
    echo -e "${GREEN}  等级: $TIER_LABEL${NC}"
    echo -e "${GREEN}  文件: ${#FILES[@]} 个${NC}"
    echo -e "${GREEN}  配额: 见 pmm_watch.sh status${NC}"
    echo -e "${GREEN}═══════════════════════════════════════${NC}"
else
    echo -e "${RED}❌ 守护启动失败，查看日志: journalctl -u $SERVICE_NAME -n 20${NC}"
    exit 1
fi
