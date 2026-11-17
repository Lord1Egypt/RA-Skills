#!/bin/bash
# step2: 安装优化版 prosperoOS 主题（放大封面 + 潜水员戴夫背景 + 平台 Logo）并切换
# SkillHub / ClawHub 文本版不含二进制主题包：缺文件时只提示、不中断整条流程。
source "$(dirname "$0")/kpa_env.sh"
require_device

THEMES_DIR="/sdcard/pegasus-frontend/themes"
THEME="prosperoOS"
ZIP="$KPA_SKILL_DIR/assets/golden/prosperoOS-kpa.zip"
HEAVY_URL="https://github.com/lisong2003-lgtm/kpa-pegasus-setup/tree/main/assets-heavy"

if sh "test -f $THEMES_DIR/$THEME/assets/images/davebg.jpg"; then
  echo "SKIP  $THEME 主题已安装（含戴夫背景）"
elif [ ! -f "$ZIP" ]; then
  echo "SKIP  主题包未随文本版分发（SkillHub/ClawHub 只允许文本类文件）。"
  echo "      从 $HEAVY_URL 下载 prosperoOS-kpa.zip 放到 assets/golden/ 后重跑本步骤，"
  echo "      或从 GitHub 克隆完整版仓库。其余步骤不受影响。"
else
  TMP="/sdcard/kpa_theme_tmp"
  sh "mkdir -p $TMP"
  "$ADB" push "$ZIP" "$TMP/theme.zip" || die "主题包推送失败"
  sh "cd $THEMES_DIR && unzip -qo $TMP/theme.zip && rm -rf $TMP" || die "主题解压失败"
  echo "OK    $THEME 主题已安装（覆盖模式，不保留旧副本）"
fi

# 切换主题
sh "sed -i 's|^general\.theme *=.*|general.theme = $THEME|' /sdcard/pegasus-frontend/settings.txt"
if ! sh "grep -q '^general\.theme' /sdcard/pegasus-frontend/settings.txt"; then
  sh "echo 'general.theme = $THEME' >> /sdcard/pegasus-frontend/settings.txt"
fi
echo "OK    天马主题已切换为 $THEME"

# 系统壁纸（AYA 桌面只认内置壁纸；把图片放进 Pictures 供手动/半自动设置）
WP="$KPA_SKILL_DIR/assets/golden/dave_wallpaper_system.png"
if [ -f "$WP" ]; then
  if sh "test -f /sdcard/Pictures/dave_sunset.png"; then
    echo "SKIP  系统壁纸图片已存在"
  else
    "$ADB" push "$WP" /sdcard/Pictures/dave_sunset.png >/dev/null
    sh "am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///sdcard/Pictures/dave_sunset.png" >/dev/null 2>&1
    echo "OK    系统壁纸图片已放入 /sdcard/Pictures/dave_sunset.png（桌面壁纸需在掌机设置内手动选）"
  fi
else
  echo "SKIP  系统壁纸图未随文本版分发，可选从 $HEAVY_URL 获取"
fi
echo "step2 done"
