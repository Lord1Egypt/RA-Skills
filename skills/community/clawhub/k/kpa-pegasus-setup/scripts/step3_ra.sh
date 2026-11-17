#!/bin/bash
# step3: 恢复 RetroArch 黄金配置（上架版）
# 部署主配置 retroarch.cfg + 竖屏 per-rom cfg 生成；遮罩/BIOS 不随包分发，见提示
source "$(dirname "$0")/kpa_env.sh"
require_device

GOLD="$KPA_SKILL_DIR/assets/golden"
DATA="$KPA_SKILL_DIR/assets/data"

# 3.1 主配置 retroarch.cfg（metadata launch 行 CONFIGFILE 指向这里）
RA_FILES="$INT/Android/data/$RA_PKG/files"
if sh "test -f $RA_FILES/retroarch.cfg && grep -q 'savestate_auto_load = \"false\"' $RA_FILES/retroarch.cfg"; then
  echo "SKIP  RA 主配置已存在"
else
  "$ADB" push "$GOLD/retroarch.cfg.txt" "$RA_FILES/retroarch.cfg" || die "RA 主配置推送失败"
  echo "OK    RA 主配置（960x640 满屏/菜单按键/性能）已部署"
fi

# 3.2 RA config/overlays 目录：确保存在（遮罩 PNG 不随包分发，可在 RA 设置里自选关闭）
sh "mkdir -p /sdcard/RetroArch/config /sdcard/RetroArch/overlays /sdcard/RetroArch/system" >/dev/null 2>&1
echo "OK    RA config/overlays/system 目录已就绪"

# 3.3 BIOS 检查（不随包分发，版权固件需用户自备）
if sh "test -f /sdcard/RetroArch/system/scph1001.bin"; then
  echo "SKIP  BIOS 已存在（检测到 scph1001.bin）"
else
  echo "WARN  RA system 目录未检测到 BIOS。以下平台需要 BIOS 才能运行（放置到 /sdcard/RetroArch/system/）："
  sed 's/^/        /' "$DATA/bios_list.txt" 2>/dev/null || echo "        （清单文件缺失）"
  echo "      PS/DC/土星/PCE-CD/MSX 等 BIOS 请自行获取；其余卡带/街机平台无 BIOS 也能跑。"
fi
echo "step3 done"
