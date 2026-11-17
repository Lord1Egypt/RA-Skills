#!/bin/bash
# sync_from_device.sh（自用，不上架）：从一台已配置好的 KPA 拉取完整黄金数据
# 重建本 skill 的重资产（APK / RA config+overlays / BIOS system），供下次离线装机使用
# 用法：bash scripts/sync_from_device.sh
source "$(dirname "$0")/kpa_env.sh"
require_device

GOLD="$KPA_SKILL_DIR/assets/golden"
mkdir -p "$GOLD" "$KPA_SKILL_DIR/assets/apks"

echo "== 1/4 拉取三个 APK =="
for p in "$RA_PKG" "$PEG_PKG" "$PPS_PKG"; do
  apk="$(sh "pm path $p" | sed 's/package://' | head -1 | tr -d '\r')"
  [ -n "$apk" ] || { echo "WARN 未安装 $p，跳过"; continue; }
  case "$p" in
    *retroarch*) n=retroarch.apk;; *pegasus*) n=pegasus.apk;; *) n=ppsspp.apk;;
  esac
  [ -s "$KPA_SKILL_DIR/assets/apks/$n" ] && { echo "SKIP $n 已存在"; continue; }
  "$ADB" pull "$apk" "$KPA_SKILL_DIR/assets/apks/$n" | tail -1
done

echo "== 2/4 打包 RA config + overlays =="
[ -s "$GOLD/kpa_config.tar" ] || {
  sh "cd /sdcard/RetroArch && tar cf /sdcard/kpa_config.tar config overlays"
  "$ADB" pull /sdcard/kpa_config.tar "$GOLD/kpa_config.tar" | tail -1
  sh "rm /sdcard/kpa_config.tar"
}

echo "== 3/4 打包 RA system BIOS（约 400MB）=="
[ -s "$GOLD/kpa_system.tar" ] || {
  sh "cd /sdcard/RetroArch && tar cf /sdcard/kpa_system.tar system"
  "$ADB" pull /sdcard/kpa_system.tar "$GOLD/kpa_system.tar" | tail -1
  sh "rm /sdcard/kpa_system.tar"
}

echo "== 4/4 拉取天马配置 =="
for f in settings.txt game_dirs.txt; do
  "$ADB" pull "/sdcard/pegasus-frontend/$f" "$GOLD/$f" >/dev/null 2>&1 && echo "OK $f"
done
"$ADB" pull "$INT/Android/data/$RA_PKG/files/retroarch.cfg" "$GOLD/retroarch.cfg.txt" >/dev/null 2>&1 && echo "OK retroarch.cfg"
"$ADB" pull "/sdcard/Android/data/$PPS_PKG/files/PSP/SYSTEM/ppsspp.ini" "$GOLD/ppsspp.ini.txt" >/dev/null 2>&1 && echo "OK ppsspp.ini"

du -sh "$KPA_SKILL_DIR/assets/apks" "$GOLD"
echo "同步完成。注意：BIOS 为版权固件，重建的重资产目录仅供个人离线装机，请勿公开发布。"
