#!/bin/bash
# step1: 安装 RetroArch / Pegasus / PPSSPP（上架版）
# APK 不随包分发：已安装则跳过；未安装则从官方渠道下载（直连失败自动走镜像）
source "$(dirname "$0")/kpa_env.sh"
require_device

DL_DIR="${KPA_DL_DIR:-/tmp/kpa_downloads}"
mkdir -p "$DL_DIR"

dl() {  # dl 输出文件 URL...
  local out="$1"; shift
  [ -s "$out" ] && { echo "      使用已下载的 $(basename "$out")"; return 0; }
  local u
  for u in "$@"; do
    echo "      下载 $u"
    if curl -fL --connect-timeout 15 --retry 2 -o "$out" "$u" && [ -s "$out" ]; then return 0; fi
    rm -f "$out"
  done
  return 1
}

gh_latest_url() {  # gh_latest_url owner/repo 关键字...：从最新 release 找匹配的 APK 链接
  local repo="$1"; shift
  curl -fsL --connect-timeout 15 "https://api.github.com/repos/$repo/releases/latest" \
    | grep -o '"browser_download_url": *"[^"]*"' | cut -d'"' -f4 \
    | while read -r u; do
        local ok=1 kw
        for kw in "$@"; do echo "$u" | grep -qi "$kw" || ok=0; done
        [ "$ok" = 1 ] && echo "$u"
      done | head -1
}

RA_JUST_INSTALLED=0
install_apk() {  # install_apk 包名 名称 apk文件 描述
  local pkg="$1" name="$2" apk="$3" desc="$4"
  if pkg_installed "$pkg"; then
    echo "SKIP  $name 已安装 ($(sh "dumpsys package $pkg | grep versionName | head -1" | tr -d ' \r'))"
    return 0
  fi
  echo "INSTALL $name（$desc）..."
  [ -n "$apk" ] && [ -s "$apk" ] || die "$name APK 下载失败：请手动下载 APK 后运行 adb install，或联网后重试本脚本"
  "$ADB" install -r "$apk" || die "$name 安装失败"
  echo "OK    $name 安装完成"
  [ "$pkg" = "$RA_PKG" ] && RA_JUST_INSTALLED=1
}

# RetroArch：libretro buildbot 稳定版 APK 内置约 80 个核心（装完免手动下核心）
if pkg_installed "$RA_PKG"; then
  echo "SKIP  RetroArch 已安装"
else
  echo "INSTALL RetroArch ..."
  RA_APK="$DL_DIR/retroarch.apk"
  dl "$RA_APK" \
    "https://buildbot.libretro.com/stable/1.22.2/android/RetroArch_aarch64.apk" \
    "https://gh-proxy.com/https://buildbot.libretro.com/stable/1.22.2/android/RetroArch_aarch64.apk" \
    || RA_APK=""
  install_apk "$RA_PKG" "RetroArch" "$RA_APK" "内置核心包 300MB+，下载较慢请耐心"
fi

# Pegasus 前端：GitHub 最新 release
if pkg_installed "$PEG_PKG"; then
  echo "SKIP  Pegasus 已安装"
else
  echo "INSTALL Pegasus ..."
  PEG_APK="$DL_DIR/pegasus.apk"
  u="$(gh_latest_url pegasus-frontend/pegasus android)"
  [ -n "$u" ] && dl "$PEG_APK" "$u" "https://gh-proxy.com/$u" || PEG_APK=""
  install_apk "$PEG_PKG" "Pegasus" "$PEG_APK" "前端"
fi

# PPSSPP：GitHub 最新 release
if pkg_installed "$PPS_PKG"; then
  echo "SKIP  PPSSPP 已安装"
else
  echo "INSTALL PPSSPP ..."
  PPS_APK="$DL_DIR/ppsspp.apk"
  u="$(gh_latest_url hrydgard/ppsspp android)"
  [ -n "$u" ] && dl "$PPS_APK" "$u" "https://gh-proxy.com/$u" || PPS_APK=""
  install_apk "$PPS_PKG" "PPSSPP" "$PPS_APK" "PSP 模拟器"
fi

if [ "$RA_JUST_INSTALLED" = "1" ]; then
  echo "NOTE  RA 刚安装，拉起它做首次核心解包（1-2 分钟）。"
  sh "monkey -p $RA_PKG -c android.intent.category.LAUNCHER 1" >/dev/null 2>&1
  sleep 5
  sh "input keyevent KEYCODE_HOME" >/dev/null
fi
echo "step1 done"
