#!/bin/bash
#
# OpenClaw 完整更新脚本
# 同时更新 CLI + Menu Bar App
#

set -e

LOG_DIR="${HOME}/.openclaw/logs"
LOG_FILE="${LOG_DIR}/autoupdate.log"

mkdir -p "$LOG_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

log "=== OpenClaw 完整更新开始 ==="

# 1. 检查CLI当前版本
CURRENT_CLI=$(openclaw --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || echo "unknown")
log "当前CLI版本: ${CURRENT_CLI}"

# 2. 检查GitHub最新版本
LATEST_GITHUB=$(curl -sL "https://api.github.com/repos/openclaw/openclaw/releases/latest" | grep -oE '"tag_name":\s*"v[0-9]+\.[0-9]+\.[0-9]+"' | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
log "GitHub最新版本: ${LATEST_GITHUB}"

# 3. 检查Menu Bar App当前版本
CURRENT_APP=$(plutil -p /Applications/OpenClaw.app/Contents/Info.plist 2>/dev/null | grep CFBundleShortVersionString | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' || echo "unknown")
log "当前App版本: ${CURRENT_APP}"

# 判断是否需要更新
NEED_UPDATE=false
if [ "$CURRENT_CLI" != "$LATEST_GITHUB" ] || [ "$CURRENT_APP" != "$LATEST_GITHUB" ]; then
    NEED_UPDATE=true
fi

if [ "$NEED_UPDATE" = false ]; then
    log "已是最新版本 (CLI: ${CURRENT_CLI}, App: ${CURRENT_APP})"
    exit 0
fi

log "检测到新版本，开始更新..."

# 4. 更新 Menu Bar App (需要sudo)
log "下载最新dmg..."
DMG_URL="https://github.com/openclaw/openclaw/releases/download/v${LATEST_GITHUB}/OpenClaw-${LATEST_GITHUB}.dmg"
DMG_PATH="/tmp/OpenClaw-${LATEST_GITHUB}.dmg"

curl -L -o "$DMG_PATH" "$DMG_URL" 2>&1 | tee -a "$LOG_FILE"

log "安装App..."
# 卸载旧版
rm -rf /Applications/OpenClaw.app 2>/dev/null || true
# 挂载dmg并安装
hdiutil attach "$DMG_PATH" -nobrowse 2>&1 | tee -a "$LOG_FILE"
cp -R "/Volumes/OpenClaw/OpenClaw.app" /Applications/ 2>&1 | tee -a "$LOG_FILE"
hdiutil detach "/Volumes/OpenClaw" 2>&1 | tee -a "$LOG_FILE"
rm -f "$DMG_PATH"

log "App更新完成"

# 5. 更新CLI (优先用npm)
log "更新CLI..."
npm install -g openclaw@latest 2>&1 | tee -a "$LOG_FILE"

# 6. 重启服务
log "重启Gateway..."
openclaw gateway restart 2>&1 | tee -a "$LOG_FILE" || true
sleep 3

# 7. 验证
NEW_CLI=$(openclaw --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || echo "unknown")
NEW_APP=$(plutil -p /Applications/OpenClaw.app/Contents/Info.plist 2>/dev/null | grep CFBundleShortVersionString | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' || echo "unknown")

log "=== 更新完成 ==="
log "CLI: ${CURRENT_CLI} → ${NEW_CLI}"
log "App: ${CURRENT_APP} → ${NEW_APP}"

if [ "$NEW_CLI" = "$LATEST_GITHUB" ] && [ "$NEW_APP" = "$LATEST_GITHUB" ]; then
    log "✅ 全部更新成功！"
else
    log "⚠️ 请检查更新结果"
fi
