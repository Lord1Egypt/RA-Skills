#!/bin/bash
# 部署 ANDROID 移植游戏集合：.app 占位真实文件 + per-game launch，解决「天马不显示」。
# 幂等；改完自动清 dataCache.json（第 5 条禁令）。
set -euo pipefail
source "$(dirname "$0")/kpa_env.sh"
require_device

META="$KPA_SKILL_DIR/assets/meta_latest/ANDROID.txt"
[ -f "$META" ] || die "缺少 $META"
DST="$TF/Roms/ANDROID"

echo "== 1/3 创建目录并推送 metadata =="
sh "mkdir -p '$DST/Imgs'" >/dev/null
"$ADB" push "$META" "$DST/metadata.pegasus.txt" >/dev/null

echo "== 2/3 创建 .app 占位文件（Pegasus 的 file: 必须指向真实文件）=="
grep '^file: ' "$META" | sed 's/^file: //' | tr -d '\r' | while read -r f; do
  [ -n "$f" ] || continue
  sh "if [ ! -f '$DST/$f' ]; then : > '$DST/$f'; echo 'created $f'; fi"
done

echo "== 3/3 清除天马元数据缓存 =="
sh "rm -f /sdcard/pegasus-frontend/dataCache.json" >/dev/null
echo "完成。重启天马后确认 ANDROID 集合出现 7 张卡片；封面需自行放到 $DST/Imgs/。"
echo "注意：不要用 am force-stop com.ayaneo.home 刷新桌面（会杀掉系统按键服务）。"
