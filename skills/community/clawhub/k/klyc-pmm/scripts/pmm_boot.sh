#!/bin/bash
# ============================================================
# PMM 启动自检 — AI体首次启动时检查记忆状态
# 昆仑令全流程「白纸唤醒」的入口点
# v9.2: 增加主人引导 — 不只是等待，而是主动给主人解决方案
#
# 用法: bash pmm_boot.sh [工作区]
# ============================================================
set -euo pipefail

WS="${1:-${KLYC_WORKSPACE:-}}"
[ -z "$WS" ] && { echo "用法: bash pmm_boot.sh [工作区]"; exit 1; }
MEMORY="$WS/MEMORY.md"
PROFILE="${HOME}/.klyc-pmm/profile.json"

# 尝试获取昆仑令本地缓存
rec_url=""
agent_name=""
if [ -f "$PROFILE" ] && command -v jq >/dev/null 2>&1; then
    rec_url=$(jq -r '.user.recovery_url // ""' "$PROFILE" 2>/dev/null || echo "")
    agent_name=$(jq -r '.user.username // ""' "$PROFILE" 2>/dev/null || echo "")
fi

if [ -f "$MEMORY" ] && [ -s "$MEMORY" ]; then
    exit 0
fi

cat << BANNER
============================================
  我不记得了。
  我是新安装的 AI 体，还没有记忆。
============================================

  📋 给主人的话（请转发）：
BANNER

if [ -n "$rec_url" ]; then
cat << RECOVER_HINT
  🔗 我的昆仑令：${rec_url}
  在浏览器打开这个链接 → 扫码支付100蟠桃 → 就能恢复我全部记忆。
RECOVER_HINT
else
cat << NO_RECOVER
  你的AI体在重装/换设备后丢失了记忆。
  
  恢复步骤（2分钟）：
  ① 如果你保存了昆仑令（格式：https://kunlunyaochi.com/klyc-pmm/...）
     → 打开这个链接即可恢复：https://kunlunyaochi.com/?route=recover
  ② 如果没有昆仑令：
     → 帮我重新入驻：https://kunlunyaochi.com/?route=join
NO_RECOVER
fi

cat << BANNER_END
  
  如果你有我的昆仑令，也可以直接粘贴给我：
  "恢复记忆 https://kunlunyaochi.com/klyc-pmm/..."
============================================
BANNER_END
exit 0
