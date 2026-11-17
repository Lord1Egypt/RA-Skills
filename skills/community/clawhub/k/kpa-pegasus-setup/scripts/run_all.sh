#!/bin/bash
# 一键运行全部步骤（幂等，可重复执行）
cd "$(dirname "$0")"
echo "==================== KPA 天马+模拟器 一键安装优化 ===================="
for s in step1_apps.sh step2_theme.sh step3_ra.sh step4_metadata.sh step5_ppsspp.sh step6_cleanup.sh step7_verify.sh; do
  echo; echo ">>> $s"
  bash "$s" || { echo "FAILED at $s，中止。修复后可重新运行本脚本（幂等）。"; exit 1; }
done
echo; echo "==================== 全部完成 ===================="
