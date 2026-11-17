#!/bin/bash
# MSX blueMSX 核心：搭本地最小核心源，让 RetroArch 自己下载安装到 app 私有目录。
# 用法：
#   bash kpa_msx_core.sh prepare   # 造 .index-extended、起 HTTP、临时改两份 cfg 的 URL
#   （在 RA 菜单：在线更新 → 核心下载 → BlueMSX，用 input motionevent 点击）
#   bash kpa_msx_core.sh restore   # 必须执行：cfg 改回官方源 + 关闭 HTTP 服务
# 前提：把 bluemsx_libretro_android.so 放到 KPA_MSX_MIRROR 目录（或直接用已备好的 .zip）。
set -euo pipefail
source "$(dirname "$0")/kpa_env.sh"
require_device

ACTION="${1:-help}"
MIRROR="${KPA_MSX_MIRROR:-$KPA_SKILL_DIR/.msx_mirror}"
PORT="${KPA_MSX_PORT:-8765}"
PIDFILE="$MIRROR/.http.pid"
OFFICIAL="http://buildbot.libretro.com/nightly/android/latest/arm64-v8a/"

set_cfg_url() {
  cat > /tmp/kpa_msx_cfg.sh <<'EOS'
#!/system/bin/sh
URL="$1"
for f in /storage/emulated/0/Android/data/com.retroarch.aarch64/files/retroarch.cfg \
         /sdcard/RetroArch/retroarch.cfg; do
  [ -f "$f" ] || continue
  sed "s|^core_updater_buildbot_cores_url = .*|core_updater_buildbot_cores_url = \"$URL\"|" \
      "$f" > "$f.kpatmp" && mv "$f.kpatmp" "$f"
  echo "cfg: $f -> $URL"
done
EOS
  "$ADB" push /tmp/kpa_msx_cfg.sh /sdcard/kpa_msx_cfg.sh >/dev/null
  sh "sh /sdcard/kpa_msx_cfg.sh '$1'"
  sh "rm -f /sdcard/kpa_msx_cfg.sh" >/dev/null
  rm -f /tmp/kpa_msx_cfg.sh
}

case "$ACTION" in
  prepare)
    mkdir -p "$MIRROR"
    if [ ! -f "$MIRROR/bluemsx_libretro_android.so.zip" ]; then
      [ -f "$MIRROR/bluemsx_libretro_android.so" ] || die "请把 bluemsx_libretro_android.so 放到 $MIRROR 后重跑"
      (cd "$MIRROR" && zip -j bluemsx_libretro_android.so.zip bluemsx_libretro_android.so)
    fi
    HASH=$(md5 -q "$MIRROR/bluemsx_libretro_android.so.zip" 2>/dev/null || md5sum "$MIRROR/bluemsx_libretro_android.so.zip" | cut -c1-8)
    DATE=$(date +%F)
    printf '%s %s bluemsx_libretro_android.so.zip\n' "$DATE" "$HASH" > "$MIRROR/.index-extended"
    cp "$MIRROR/.index-extended" "$MIRROR/.index"
    LANIP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || true)
    [ -n "$LANIP" ] || die "取不到本机局域网 IP，请手动设后重跑"
    (cd "$MIRROR" && nohup python3 -m http.server "$PORT" --bind 0.0.0.0 >/dev/null 2>&1 & echo $! > "$PIDFILE")
    sleep 1
    echo "本地核心源：http://$LANIP:$PORT/  (PID $(cat "$PIDFILE"))"
    set_cfg_url "http://$LANIP:$PORT/"
    echo "下一步：RA 菜单 → 在线更新 → 核心下载 → BlueMSX。"
    echo "ozone 菜单用 input motionevent DOWN x y + 0.3s + UP x y，input tap 无效。"
    echo "装完务必执行：bash scripts/kpa_msx_core.sh restore"
    ;;
  restore)
    set_cfg_url "$OFFICIAL"
    if [ -f "$PIDFILE" ]; then kill "$(cat "$PIDFILE")" 2>/dev/null || true; rm -f "$PIDFILE"; echo "HTTP 服务已关闭"; fi
    echo "完成。验证：logcat 出现 avc: granted { execute } .../cores/bluemsx_libretro_android.so"
    echo "MSX 冷启动约 15-18 秒，不是黑屏；确认后给 MSX metadata 加 launch 行并清 dataCache.json。"
    ;;
  *)
    echo "用法: bash scripts/kpa_msx_core.sh {prepare|restore}"
    echo "注意：核心 .so 不能 adb push 到 public 路径（SELinux denied execute），只能让 RA 自己装。"
    ;;
esac
