#!/bin/bash
# 隐藏图库里的封面/素材，不删文件、不影响天马按路径读封面。
# TF 卡卷重扫不生效，需重启一次。
set -euo pipefail
source "$(dirname "$0")/kpa_env.sh"
require_device

cat > /tmp/kpa_nomedia_dev.sh <<'EOS'
#!/system/bin/sh
for d in \
  "/storage/6AF3-384F/Roms" \
  "/storage/emulated/0/RetroArch" \
  "/storage/emulated/0/pegasus-frontend" \
  "/storage/emulated/0/Android/data/com.pocketmuseum.app"; do
  if [ -d "$d" ]; then
    [ -f "$d/.nomedia" ] || { : > "$d/.nomedia"; echo "created $d/.nomedia"; }
  else
    echo "skip (not found): $d"
  fi
done
EOS
"$ADB" push /tmp/kpa_nomedia_dev.sh /sdcard/kpa_nomedia_dev.sh >/dev/null
sh "sh /sdcard/kpa_nomedia_dev.sh"
echo "== 重扫内部存储 MediaStore =="
sh "content call --uri content://media --method scan_volume --arg external_primary" 2>/dev/null | head -5 || true
sh "rm -f /sdcard/kpa_nomedia_dev.sh" >/dev/null
rm -f /tmp/kpa_nomedia_dev.sh
echo "完成。内部存储应立刻生效；TF 卡（Roms）需重启掌机一次后确认。"
echo "若 TF 卡挂载点不是默认值，请先设 KPA_TF 并同步修改脚本内的目录列表。"
