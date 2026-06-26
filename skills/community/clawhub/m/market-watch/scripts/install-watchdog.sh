#!/bin/bash
# install-watchdog.sh — 安装/卸载 market-watch 守卫（launchd）
#
# 每5分钟检查一次：有活跃警报 + daemon没跑 → 拉起来
# 用法:
#   install-watchdog.sh install [--agent laok]
#   install-watchdog.sh uninstall [--agent laok]

set -euo pipefail

ACTION="${1:-install}"
shift || true
AGENT="laok"
while [[ $# -gt 0 ]]; do
    case "$1" in
        --agent) AGENT="$2"; shift 2 ;;
        *) shift ;;
    esac
done

# N-03: AGENT 格式校验（与 daemon.sh 一致）
if [[ ! "$AGENT" =~ ^[a-zA-Z0-9_-]+$ ]]; then
    echo "Error: invalid --agent value: '$AGENT' (only alphanumeric, dash, underscore allowed)" >&2
    exit 1
fi

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DAEMON_SH="$SKILL_DIR/scripts/daemon.sh"
LABEL="com.openclaw.market-watch.${AGENT}"
PLIST="$HOME/Library/LaunchAgents/${LABEL}.plist"

case "$ACTION" in
    install)
        mkdir -p "$HOME/Library/LaunchAgents"
        cat > "$PLIST" << PLIST_EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${LABEL}</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>${DAEMON_SH}</string>
        <string>ensure</string>
        <string>--agent</string>
        <string>${AGENT}</string>
    </array>
    <key>StartInterval</key>
    <integer>300</integer>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/market-watch-${AGENT}-watchdog.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/market-watch-${AGENT}-watchdog.log</string>
</dict>
</plist>
PLIST_EOF
        launchctl unload "$PLIST" 2>/dev/null || true
        launchctl load "$PLIST"
        echo "[market-watch] 守卫已安装: $LABEL"
        echo "  每5分钟检查，有活跃警报自动拉起daemon"
        echo "  plist: $PLIST"
        ;;

    uninstall)
        if [[ -f "$PLIST" ]]; then
            launchctl unload "$PLIST" 2>/dev/null || true
            rm -f "$PLIST"
            echo "[market-watch] 守卫已卸载: $LABEL"
        else
            echo "[market-watch] 守卫未安装"
        fi
        ;;

    *)
        echo "用法: install-watchdog.sh {install|uninstall} [--agent AGENT]"
        exit 1
        ;;
esac
