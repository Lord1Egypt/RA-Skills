#!/bin/bash
# 推送详情页增强版 GameDetails.qml（字号 / 卡片 / 去截断）并清缓存。
# 原版自动留一份回滚点；观感必须实机目视确认，远程输入停不到详情页那一屏。
set -euo pipefail
source "$(dirname "$0")/kpa_env.sh"
require_device

SRC="$KPA_SKILL_DIR/assets/golden/GameDetails.improved.qml.txt"
[ -f "$SRC" ] || die "缺少 $SRC"
THEME="/sdcard/pegasus-frontend/themes/prosperoOS"
TARGET="$THEME/GameDetails.qml"
STAMP=$(date +%Y%m%d)

echo "== 1/3 确认主题目录 =="
sh "test -d '$THEME'" || die "未找到主题目录 $THEME（KPA_THEME 可覆盖）"

echo "== 2/3 留回滚点并推送 =="
sh "if [ -f '$TARGET' ] && [ ! -f '$TARGET.bak$STAMP' ]; then cp '$TARGET' '$TARGET.bak$STAMP'; echo 'backup saved'; fi"
"$ADB" push "$SRC" "$TARGET" >/dev/null

echo "== 3/3 清缓存 =="
sh "rm -f /sdcard/pegasus-frontend/dataCache.json" >/dev/null

echo "完成。重启天马，检查 logcat 无 QML/QQml 报错，实机看详情页观感。"
echo "不满意用 $TARGET.bak$STAMP 回滚；随包另附 assets/golden/GameDetails.before.qml.txt 原版。"
