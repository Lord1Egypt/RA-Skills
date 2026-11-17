#!/bin/bash
# KPA 公共环境：定位 adb、检查设备、TF 卡路径
# 由各 step 脚本 source 调用

KPA_SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export KPA_SKILL_DIR

find_adb() {
  if [ -n "${KPA_ADB:-}" ] && [ -x "${KPA_ADB:-}" ]; then return; fi
  for c in "$(which adb)" "$HOME/WorkBuddy"/*/tools/platform-tools/adb "$HOME/.workbuddy/tools/platform-tools/adb" "/opt/homebrew/bin/adb"; do
    if [ -n "$c" ] && [ -x "$c" ]; then export KPA_ADB="$c"; return; fi
  done
  echo "ERROR: 未找到 adb。请将 platform-tools 解压到 ~/WorkBuddy/ 下的 tools/platform-tools，或设置 KPA_ADB 环境变量。" >&2
  exit 1
}
find_adb

ADB="$KPA_ADB"
TF="/storage/6AF3-384F"   # TF 卡挂载点（KONKR Pocket ADVANCE 实测）。若不同，用 KPA_TF 覆盖
TF="${KPA_TF:-$TF}"
INT="/storage/emulated/0"
RA_PKG="com.retroarch.aarch64"
PEG_PKG="org.pegasus_frontend.android"
PPS_PKG="org.ppsspp.ppsspp"

sh() { "$ADB" shell "$@"; }
# 推送目录/文件：push_all 本地路径 设备路径
die() { echo "ERROR: $*" >&2; exit 1; }
require_device() {
  [ "$("$ADB" get-state 2>/dev/null)" = "device" ] || die "未检测到 KPA 设备（adb devices 无 device）。请先 USB 连接或 adb connect。"
}
pkg_installed() { sh "pm path $1 2>/dev/null" | grep -q "package:"; }
# 备份设备文件：bak 设备路径 后缀（存在才备份，后缀默认 .bakKPA3）
bak() { local f="$1" sfx="${2:-.bakKPA3}"; sh "if [ -f '$f' ] && [ ! -f '$f$sfx' ]; then cp '$f' '$f$sfx'; fi" >/dev/null 2>&1; }
