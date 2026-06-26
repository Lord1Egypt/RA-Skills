#!/bin/bash

API_TOKEN="clh_kZ-UWsDcsn7OiMG67RJxp3O1fdx43c41WgHMe01KWeY"
API_BASE="https://clawhub.ai/api/v1"
SKILL_SLUG="papermc-ai-ops"

echo "发布技能: $SKILL_SLUG"

# 创建临时目录用于构建multipart
TEMP_DIR=$(mktemp -d)
echo "临时目录: $TEMP_DIR"

# 创建payload JSON
cat > "$TEMP_DIR/payload.json" << PAYLOAD_EOF
{
  "slug": "$SKILL_SLUG",
  "version": "2.0.0",
  "displayName": "PaperMC AI Operations",
  "summary": "Manage Paper Minecraft servers through safe, controlled interfaces.",
  "tags": ["minecraft", "papermc", "server-management", "automation"],
  "changelog": "Release v2.0.0: Enhanced with Plugin Upgrade Framework"
}
PAYLOAD_EOF

echo "Payload创建完成"

# 尝试使用curl上传
echo "尝试上传..."
curl -X POST \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: multipart/form-data" \
  -F "payload=<$TEMP_DIR/payload.json;type=application/json" \
  -F "files[]=@SKILL.md;type=text/markdown" \
  -F "files[]=@plugin_upgrade_framework.py;type=text/x-python" \
  -F "files[]=@upgrade_examples.py;type=text/x-python" \
  -F "files[]=@viaversion_upgrade_report.json;type=application/json" \
  -F "files[]=@docs/Turret_Plugin_User_Manual.md;type=text/markdown" \
  "$API_BASE/skills" \
  --verbose

echo ""
echo "清理临时目录..."
rm -rf "$TEMP_DIR"
