#!/usr/bin/env bash
# precheck.sh — Step 0: slug 冲突预检
# Usage: ./precheck.sh <slug>
set -euo pipefail

SLUG="${1:-}"
if [[ -z "$SLUG" ]]; then
  echo "Usage: $0 <slug>" >&2
  exit 1
fi

echo "🔍 Checking slug '$SLUG' on clawhub.com ..."

if ! command -v clawhub >/dev/null 2>&1; then
  cat <<EOF >&2
⚠️  clawhub CLI 未安装。请先安装：
   npm install -g clawhub
然后重跑：$0 $SLUG
EOF
  exit 2
fi

# clawhub inspect 退出码：
#   0     = 已找到（slug 已被注册）
#   非 0  = 未找到 / 或网络异常 / 或权限不足
# 只调用一次，同时捕获 stderr（区分网络错误和真正未注册）和退出码
if INSPECT_ERR="$(clawhub inspect "$SLUG" 2>&1 1>/dev/null)"; then
  INSPECT_RC=0
else
  INSPECT_RC=$?
fi

if [[ $INSPECT_RC -eq 0 ]]; then
  echo ""
  echo "⚠️  SLUG '$SLUG' 已被 clawhub 注册！"
  echo ""
  echo "请由用户拍板："
  echo "  1. 同 owner 同名 → 升版本号直接 publish（不走开源新流程）"
  echo "  2. 别人 owner 同名 → 必须换 slug（加品牌前缀 claw-/openclaw- 等）"
  echo "  3. 概念高度雷同 → 读对方 SKILL.md 决定差异化定位"
  echo ""
  echo "⛔ clawhub 不支持 slug rename，一旦 publish 就锁死。"
  exit 3
else
  # 区分"真未找到"和"网络/鉴权失败"
  if echo "$INSPECT_ERR" | grep -qiE 'network|timeout|connect|dns|enotfound|econnrefused|getaddrinfo'; then
    echo "⚠️  网络异常，无法确认 slug '$SLUG' 是否已注册："
    echo "     $INSPECT_ERR" | head -5
    echo ""
    echo "   建议稍后重跑：$0 $SLUG"
    exit 4
  fi
  echo "✅ SLUG '$SLUG' 在 clawhub 上未被注册，可安全使用。"
fi

# 同步建议查 GitHub（手动）
echo ""
echo "📌 同步建议："
echo "   - GitHub repo 名是否冲突：浏览器查 https://github.com/<your-handle>?tab=repositories"
echo "   - 概念关键词搜索：https://github.com/search?q=$SLUG&type=repositories"
