#!/bin/bash
# step7: 验证：核心数（借天马拉起）+ 重启天马 + 截图 + 运行日志错误检查
source "$(dirname "$0")/kpa_env.sh"
require_device

echo "== 重启天马 =="
sh "am force-stop $PEG_PKG; sleep 1; monkey -p $PEG_PKG -c android.intent.category.LAUNCHER 1" >/dev/null 2>&1
sleep 7
OUT=/tmp/kpa_verify.png
"$ADB" exec-out screencap -p > "$OUT"
echo "截图已保存: $OUT"

echo "== 天马运行日志错误 =="
sh "grep -icE 'cannot|error|missing|failed' /sdcard/pegasus-frontend/lastrun.log 2>/dev/null" | tr -d '\r' | while read c; do
  if [ "$c" = "0" ]; then echo "OK    lastrun.log 无资源缺失错误"; else echo "WARN  lastrun.log 有 $c 行错误，需检查"; sh "grep -iE 'cannot|error|missing|failed' /sdcard/pegasus-frontend/lastrun.log | head -5"; fi
done

echo "== RA 主配置 =="
sh "test -f $INT/Android/data/$RA_PKG/files/retroarch.cfg && echo OK || echo MISSING"

echo "== 核心解包验证（需掌机上人工确认）=="
echo "NOTE  shell 无法读 RA 私有目录。请掌机上启动 RetroArch 确认核心列表，"
echo "      或直接用天马启动各平台任一游戏验证（MSX 除外，见 SKILL.md 手动步骤）。"
echo "step7 done"
