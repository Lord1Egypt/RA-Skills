#!/bin/bash
# step6: 清理垃圾（macOS AppleDouble ._文件 / .DS_Store / 测试截图 / 应用缓存），幂等
source "$(dirname "$0")/kpa_env.sh"
require_device

cat > /tmp/kpa_step6_device.sh <<'EOS'
#!/system/bin/sh
INT="/storage/emulated/0"
n1=0
# AppleDouble 元数据垃圾（经 Mac 拷贝产生）
for root in "$INT/RetroArch" "$INT/PSP" "$INT/pegasus-frontend" "/storage/6AF3-384F"; do
  c=$(find "$root" -name '._*' -type f 2>/dev/null | wc -l)
  find "$root" -name '._*' -type f -delete 2>/dev/null
  n1=$((n1+c))
done
find "$INT/RetroArch" "$INT/PSP" -name '.DS_Store' -type f -delete 2>/dev/null
# 失效的旧 PPSSPP 路径：只报告不自动删（需人工确认后分批执行）
echo "OPTIONAL old_ppsspp_paths:"
for p in "$INT/PSP/SYSTEM" "$INT/PSP/shaders" "$INT/PSP/ISO"; do [ -d "$p" ] && echo "  $p"; done
echo "RESULT appledouble_deleted=$n1"
EOS
"$ADB" push /tmp/kpa_step6_device.sh /sdcard/kpa_step6_device.sh >/dev/null
sh "sh /sdcard/kpa_step6_device.sh"
sh "rm -f /sdcard/kpa_step6_device.sh" >/dev/null
rm -f /tmp/kpa_step6_device.sh

# 应用缓存：只盘点不自动删（通配 rm -rf 风险高，按禁令需用户确认后分批执行）
echo "OPTIONAL app_cache_size_kb:"
sh "du -sk $INT/Android/data/*/cache 2>/dev/null | tail -20"
echo "OK    缓存已盘点，未删除任何文件"

# 提示类垃圾（仅统计报告，不自动删）
echo "---- 报告：以下为可选清理项（需人工确认）----"
echo "天马测试截图（本机 /sdcard 根目录 t_*.png、u*.png 等）："
sh "ls $INT/*.png 2>/dev/null | wc -l"
echo "旧主题 pegasusG-* + Resource 资源包（当前用 prosperoOS 时可省约 552M）："
sh "du -sk $INT/pegasus-frontend/themes 2>/dev/null"
echo "step6 done"
