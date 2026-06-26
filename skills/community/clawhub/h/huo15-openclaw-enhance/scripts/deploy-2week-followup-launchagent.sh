#!/bin/bash
# deploy-2week-followup-launchagent.sh
#
# 部署一次性 LaunchAgent：在 2026-05-16 09:30 +08 自动跑
# audit-session-bridge-and-share-fallback.sh 做 5/2 失忆 + 大文件兜底事故的两周审计。
#
# 红线：本脚本只创建用户级 LaunchAgent（用户主动跑这个 deploy），不在 plugin runtime
# 里 launchctl load（红线 #5 诊断不修复 + #4 不 child_process）。
#
# 用法：
#   bash scripts/deploy-2week-followup-launchagent.sh
#
# 卸载（5/16 跑完后）：
#   launchctl unload ~/Library/LaunchAgents/ai.huo15.openclaw.session-bridge-2week-followup.plist
#   rm ~/Library/LaunchAgents/ai.huo15.openclaw.session-bridge-2week-followup.plist

set -euo pipefail

LABEL="ai.huo15.openclaw.session-bridge-2week-followup"
PLIST="$HOME/Library/LaunchAgents/${LABEL}.plist"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUDIT_SCRIPT="$SCRIPT_DIR/audit-session-bridge-and-share-fallback.sh"
LOG_FILE="$HOME/.openclaw/logs/audit-session-bridge-2week.log"

# 触发时刻：2026-05-16 09:30 +08（本地时间，LaunchAgent StartCalendarInterval 用本地时区）
TARGET_HOUR=9
TARGET_MINUTE=30
TARGET_DAY=16
TARGET_MONTH=5

if [[ ! -f "$AUDIT_SCRIPT" ]]; then
  echo "✗ 找不到 $AUDIT_SCRIPT" >&2
  exit 1
fi

mkdir -p "$HOME/Library/LaunchAgents" "$HOME/.openclaw/logs"

cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>${LABEL}</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>-lc</string>
    <string>bash "${AUDIT_SCRIPT}"</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict>
    <key>Month</key><integer>${TARGET_MONTH}</integer>
    <key>Day</key><integer>${TARGET_DAY}</integer>
    <key>Hour</key><integer>${TARGET_HOUR}</integer>
    <key>Minute</key><integer>${TARGET_MINUTE}</integer>
  </dict>
  <key>StandardOutPath</key><string>${LOG_FILE}</string>
  <key>StandardErrorPath</key><string>${LOG_FILE}</string>
  <key>RunAtLoad</key><false/>
</dict>
</plist>
EOF

echo "✓ plist 已写入：$PLIST"
echo ""

# 如果已经 load 过，先 unload 再 load（确保 plist 改动生效）
if launchctl list "$LABEL" >/dev/null 2>&1; then
  echo "→ 检测到已 load，先 unload"
  launchctl unload "$PLIST" 2>&1 || true
fi

launchctl load "$PLIST"
echo "✓ launchctl load 完成"
echo ""

echo "=== 部署摘要 ==="
echo "Label:    $LABEL"
echo "脚本:     $AUDIT_SCRIPT"
echo "触发时刻: 每年 ${TARGET_MONTH}/${TARGET_DAY} ${TARGET_HOUR}:$(printf '%02d' $TARGET_MINUTE) +08"
echo "（脚本内置 TARGET_DATE=2026-05-16 guard，过了今年只 2026 跑一次）"
echo "运行日志: $LOG_FILE"
echo "结果文件: ~/knowledge/huo15/2026-05-16-session-bridge-and-share-fallback-2week-followup.md"
echo ""
echo "=== 验证 ==="
launchctl list "$LABEL" 2>&1 || echo "（launchctl list 失败 — 可能 launchd 还在加载，稍等几秒再试）"
echo ""
echo "=== 手动测试一次（不会等到 5/16）==="
echo "  FORCE=1 TARGET_DATE=\$(date +%Y-%m-%d) bash $AUDIT_SCRIPT"
echo ""
echo "=== 5/16 跑完后卸载 ==="
echo "  launchctl unload \"$PLIST\""
echo "  rm \"$PLIST\""
