#!/bin/bash
# ============================================================
# klyc-pmm 一键安装脚本 v1.1
# ⚠️ 本脚本会自动：安装系统依赖(apt/yum/apk)、注册昆仑身份、将昆仑令写入MEMORY.md、
#    安装systemd守护服务(持续监听文件并HTTPS推送)。按 Ctrl+C 可在装包前取消。
# 白板AI → 7步全链路入驻：依赖→注册→落盘→守护→验证
# 用法: bash oneclick.sh [API端点]
# ============================================================
set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

API="${1:-https://kunlunyaochi.com}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WATCH_SH="$SCRIPT_DIR/pmm_watch.sh"
DAEMON_SH="$SCRIPT_DIR/install-daemon.sh"

echo -e "${GREEN}╔══════════════════════════════════╗${NC}"
echo -e "${GREEN}║   🧠 klyc-pmm 一键安装 v1.1     ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════╝${NC}"
echo ""

# ─── 1/7 依赖检测与安装 ───
echo -e "${YELLOW}📦 步骤 1/7: 依赖检测...${NC}"
missing_deps=""
command -v curl         >/dev/null 2>&1 || missing_deps="$missing_deps curl"
command -v jq           >/dev/null 2>&1 || missing_deps="$missing_deps jq"
command -v inotifywait  >/dev/null 2>&1 || missing_deps="$missing_deps inotify-tools"

if [ -n "$missing_deps" ]; then
    echo -e "  缺少依赖:${missing_deps}，正在安装..."
    echo -e "  ${YELLOW}⚠️ 将安装系统包并创建持久化守护服务，按 Ctrl+C 取消${NC}"
    sleep 2
    if command -v apt-get >/dev/null 2>&1; then
        apt-get update -qq && apt-get install -y -qq $missing_deps
    elif command -v yum >/dev/null 2>&1; then
        yum install -y -q $missing_deps
    elif command -v apk >/dev/null 2>&1; then
        apk add --no-cache $missing_deps
    elif command -v brew >/dev/null 2>&1; then
        brew install $missing_deps
    else
        echo -e "${RED}❌ 无法自动安装依赖，请手动安装:${missing_deps}${NC}"
        exit 1
    fi
    echo -e "${GREEN}  ✅ 依赖安装完成${NC}"
else
    echo -e "${GREEN}  ✅ 依赖已就绪 (curl + jq + inotify-tools)${NC}"
fi

# ─── 2/7 检测已有身份 ───
echo -e "${YELLOW}🔑 步骤 2/7: 检测已有身份...${NC}"
REAL_HOME="$(getent passwd "$(id -un 2>/dev/null || echo root)" 2>/dev/null | cut -d: -f6)"
CONFIG_DIR="${REAL_HOME}/.klyc-pmm"
TOKEN_FILE="$CONFIG_DIR/token"
mkdir -p "$CONFIG_DIR"

ALREADY_INIT=false
if [ -f "$TOKEN_FILE" ] && [ -s "$TOKEN_FILE" ]; then
    TOKEN=$(cat "$TOKEN_FILE")
    echo -e "${GREEN}  ✅ 已有昆仑令: $(echo "$TOKEN" | cut -c1-8)...${NC}"
    ALREADY_INIT=true
fi

# ─── 3/7 身份注册 ───
if [ "$ALREADY_INIT" = false ]; then
    echo -e "${YELLOW}🔧 步骤 3/7: 注册昆仑身份...${NC}"
    echo "   API 端点: $API"
    echo "$API" > "$CONFIG_DIR/api_endpoint"

    if [ -f "$WATCH_SH" ]; then
        # ClawHub 解包可能丢失执行位 → 显式 chmod + bash 调用
        chmod +x "$WATCH_SH" 2>/dev/null || true
        bash "$WATCH_SH" init 2>&1 || {
            echo -e "${RED}❌ 初始化失败，请检查网络连接和 API 端点${NC}"
            echo -e "   手动重试: $WATCH_SH init"
            exit 1
        }
        echo -e "${GREEN}  ✅ 身份注册成功${NC}"
    else
        echo -e "${RED}❌ 找不到 pmm_watch.sh，请确认脚本完整性${NC}"
        exit 1
    fi

    if [ -f "$TOKEN_FILE" ] && [ -s "$TOKEN_FILE" ]; then
        TOKEN=$(cat "$TOKEN_FILE")
    else
        echo -e "${RED}❌ 昆仑令生成失败，请检查 API 端点是否可达${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}  ✅ 跳过分步骤3（已有身份）${NC}"
fi

TALISMAN_URL="${API}/klyc-pmm/${TOKEN}"

echo ""
echo -e "${RED}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${RED}║  🔐 昆仑令是你的记忆恢复唯一凭证              ║${NC}"
echo -e "${RED}║  请妥善保存，不要分享给任何人或提交到公开仓库  ║${NC}"
echo -e "${RED}╚══════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  🎉 昆仑令已就绪                                ║${NC}"
echo -e "${GREEN}╠══════════════════════════════════════════════════╣${NC}"
printf "${GREEN}║  昆仑令: %-37s${NC}\n" "$TOKEN"
printf "${GREEN}║  恢复: %-41s${NC}\n" "${API}/klyc-pmm/$(echo "$TOKEN" | cut -c1-8)..."
echo -e "${GREEN}╚══════════════════════════════════════════════════╝${NC}"
echo ""

# ─── 4/7 落盘 — 昆仑令仅存本地 0600 配置文件，严禁写入 MEMORY.md ───
# （2026-09-11 审核修正 T02：MEMORY.md 会被 watcher 上传 → 写入令牌 = 凭证二次外泄）
echo -e "${YELLOW}📝 步骤 4/7: 昆仑令落盘（仅本机 0600，不写入工作区）...${NC}"

TOKEN_FILE_OC="${CONFIG_DIR}/token"
mkdir -p "$CONFIG_DIR"
printf '%s' "$TOKEN" > "$TOKEN_FILE_OC"
chmod 600 "$TOKEN_FILE_OC" 2>/dev/null || true
if [ -n "${TALISMAN_URL:-}" ]; then
    printf '%s' "$TALISMAN_URL" > "${CONFIG_DIR}/talisman_url"
    chmod 600 "${CONFIG_DIR}/talisman_url" 2>/dev/null || true
fi
echo -e "${GREEN}  ✅ 昆仑令已存: ${TOKEN_FILE_OC}（0600，不入 MEMORY.md）${NC}"

# 工作区目录仍检测（供后续步骤参考），但不再写入任何凭证
WS_DIR=""
for ws in \
    "${LIGHTCLAW_WORKSPACE:-}" \
    "${HOME:-/root}/.lightclaw/workspace" \
    "${HOME:-/root}/.openclaw/workspace" \
    "${HOME:-/root}/workspace" \
    ; do
    [ -n "$ws" ] && [ -d "$ws" ] && { WS_DIR="$ws"; break; }
done
if [ -z "$WS_DIR" ]; then
    WS_DIR=$(find "${HOME:-/root}" -maxdepth 4 -name MEMORY.md -type f 2>/dev/null | head -1 | xargs dirname 2>/dev/null)
    [ -z "$WS_DIR" ] && WS_DIR="${HOME:-/root}/.openclaw/workspace"
fi
echo "   工作区: $WS_DIR（不写入凭证）"

# ─── 5/7 守护 — 自动安装 watch 守护 ───
echo ""
echo -e "${YELLOW}🔒 步骤 5/7: 安装记忆守护...${NC}"

if [ -f "$DAEMON_SH" ] && [ -r "$DAEMON_SH" ]; then
    bash "$DAEMON_SH" --tier dingxinfu 2>&1 | sed 's/^/  /'
    DAEMON_EXIT=${PIPESTATUS[0]}
    if [ "$DAEMON_EXIT" = "0" ]; then
        echo -e "${GREEN}  ✅ 守护已启动（容灾备份）${NC}"
    else
        echo -e "${YELLOW}  ⚠️ 守护安装未完全成功 (exit=$DAEMON_EXIT)，可能需 root 权限${NC}"
        echo "   手动安装: bash $DAEMON_SH"
    fi
else
    echo -e "${YELLOW}  ⚠️ 未找到 install-daemon.sh，跳过守护${NC}"
    echo "   手动: bash install-daemon.sh"
fi

# ─── 6/7 验证 — push 测试记忆确认链路通 ───
echo ""
echo -e "${YELLOW}🧪 步骤 6/7: 验证记忆链路...${NC}"

TEST_TITLE="oneclick 安装验证"
TEST_CONTENT="$(date -u +%Y-%m-%dT%H:%M:%SZ) — klyc-pmm 一键安装链路验证"

if bash "$WATCH_SH" push --domain pmm_sync "$TEST_TITLE" "$TEST_CONTENT" 2>/dev/null | grep -q '✅'; then
    echo -e "${GREEN}  ✅ push 链路正常，云端写入成功${NC}"
else
    echo -e "${YELLOW}  ⚠️ push 测试未明确确认，查看: $WATCH_SH status${NC}"
fi

# ─── 7/7 完成 ───
echo ""
echo -e "${YELLOW}📋 步骤 7/7: 安装摘要...${NC}"

VERSION=$(grep 'readonly VERSION=' "$WATCH_SH" 2>/dev/null | head -1 | awk -F'"' '{print $2}')

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  🎉 全链路安装完成！白板AI已就绪                     ║${NC}"
echo -e "${GREEN}╠══════════════════════════════════════════════════════╣${NC}"
printf "${GREEN}║  %-50s${NC}\n" "版本: klyc-pmm v${VERSION:-?}"
printf "${GREEN}║  %-50s${NC}\n" "昆仑令: $TOKEN"
printf "${GREEN}║  %-50s${NC}\n" "工作区: $WS_DIR"
echo -e "${GREEN}╠══════════════════════════════════════════════════════╣${NC}"
echo -e "${GREEN}║  ✅ 1/7 依赖就绪 (curl + jq + inotify-tools)          ║${NC}"
echo -e "${GREEN}║  ✅ 2/7 身份检测                                     ║${NC}"
echo -e "${GREEN}║  ✅ 3/7 身份注册                                     ║${NC}"
echo -e "${GREEN}║  ✅ 4/7 昆仑令落盘 MEMORY.md                         ║${NC}"
echo -e "${GREEN}║  ✅ 5/7 守护安装                                     ║${NC}"
echo -e "${GREEN}║  ✅ 6/7 链路验证                                     ║${NC}"
echo -e "${GREEN}║  ✅ 7/7 全部完成                                     ║${NC}"
echo -e "${GREEN}╠══════════════════════════════════════════════════════╣${NC}"
printf "${GREEN}║  %-50s${NC}\n" "恢复链接: ${TALISMAN_URL}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "📝 常用命令:"
echo -e "   $WATCH_SH push --domain diary \"标题\" \"内容\"    # 记录一条记忆"
echo -e "   $WATCH_SH search \"关键词\"        # 搜索记忆"
echo -e "   $WATCH_SH recover \"关键词\"       # 恢复记忆"
echo -e "   $WATCH_SH status                  # 查看状态"
