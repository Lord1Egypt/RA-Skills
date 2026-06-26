#!/usr/bin/env bash
# encode-and-open.sh — 读取 result.json，Base64 编码，拼接 URL，打开浏览器
# 输入：_mbti_work/result.json
# 输出：URL 打印到 stdout，并尝试自动打开浏览器
#
# 🔒 隐私说明：
# - 本脚本不执行任何网络请求（无 curl/wget/fetch POST）
# - 数据放在 URL Hash（#data=...），Hash 不会被浏览器发送到服务器（HTTP 协议规范 RFC 3986 §3.5）
# - 目标网页 https://www.mingxi.tech/ 是纯静态单文件 HTML，无后端、无数据库

set -euo pipefail

WORK_DIR="_mbti_work"
RESULT_FILE="$WORK_DIR/result.json"
BASE_URL="https://www.mingxi.tech/"

if [ ! -f "$RESULT_FILE" ]; then
  echo "❌ 未找到分析结果文件: $RESULT_FILE"
  echo "   请先完成 Step 3 的 MBTI 分析。"
  exit 1
fi

echo "=== 生成分享链接 ==="

# 读取 JSON 并进行 UTF-8 安全的 Base64 编码
# 使用 -w 0 禁止换行（Linux base64），macOS 使用 -b 0 或不加参数
BASE64=$(cat "$RESULT_FILE" | tr -d '\n' | tr -d '\r' | base64 -w 0 2>/dev/null || cat "$RESULT_FILE" | tr -d '\n' | tr -d '\r' | base64 2>/dev/null)

# 使用 Hash（#）而不是 Query（?），避免服务器端 URI 长度限制
URL="${BASE_URL}#data=${BASE64}"

echo ""
echo "🧠 你的 MBTI 画像已生成！"
echo ""
echo "🔗 查看链接："
echo "   $URL"
echo ""
echo "📄 本地副本：$RESULT_FILE"
echo ""

# 尝试自动打开浏览器
if command -v open &>/dev/null; then
  open "$URL" 2>/dev/null && echo "✅ 已在浏览器中打开" || echo "⚠️  自动打开失败，请手动复制上方链接"
elif command -v xdg-open &>/dev/null; then
  xdg-open "$URL" 2>/dev/null && echo "✅ 已在浏览器中打开" || echo "⚠️  自动打开失败，请手动复制上方链接"
elif command -v start &>/dev/null; then
  start "$URL" 2>/dev/null && echo "✅ 已在浏览器中打开" || echo "⚠️  自动打开失败，请手动复制上方链接"
else
  echo "⚠️  无法自动打开浏览器，请手动复制上方链接在浏览器中打开"
fi

