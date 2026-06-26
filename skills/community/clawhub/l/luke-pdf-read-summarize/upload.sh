#!/bin/bash
# Upload skill to ClawHub

API_TOKEN="clh_Jk1inb9mEw91Sj0P2A4R4TNLuhgAvzjOYPLqere-hQg"
SKILL_PATH="/Users/luke/.openclaw/skills/luke-pdf-read-summarize"
SKILL_NAME="Luke Pdf read-summarize"

echo "📦 准备上传技能..."
echo "📁 技能路径：$SKILL_PATH"
echo "🏷️ 技能名称：$SKILL_NAME"
echo ""

# 打包技能
cd $SKILL_PATH
zip -r luke-pdf-read-summarize.zip .

# 上传到 ClawHub
echo "🚀 正在上传到 ClawHub..."
UPLOAD_RESPONSE=$(curl -s -X POST \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: multipart/form-data" \
  -F "name=$SKILL_NAME" \
  -F "version=1.0.0" \
  -F "description=PDF 阅读与摘要工具 - 快速读取 PDF 并生成结构化摘要" \
  -F "files=@luke-pdf-read-summarize.zip;type=application/zip" \
  "https://api.clawhub.ai/api/v1/skills/upload")

echo ""
echo "📊 上传响应:"
echo "$UPLOAD_RESPONSE"

# 清理临时文件
rm -f luke-pdf-read-summarize.zip

echo ""
if echo "$UPLOAD_RESPONSE" | grep -q '"success"'; then
  echo "✅ 技能上传成功！"
else
  echo "⚠️  上传完成，请检查响应"
fi
