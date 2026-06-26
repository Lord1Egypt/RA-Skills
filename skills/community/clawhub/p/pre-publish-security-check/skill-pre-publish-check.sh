#!/bin/bash
# skill-pre-publish-check.sh — 发布前安全检查
# 用法: ./skill-pre-publish-check.sh /path/to/skill

set -e

SKILL_DIR="${1:-.}"

if [ ! -d "$SKILL_DIR" ]; then
    echo "❌ 目录不存在: $SKILL_DIR"
    exit 1
fi

echo "🔍 检查 skill: $SKILL_DIR"
echo ""

FOUND=0

# 1. 检查 API Key 格式 (sk-xxx, tvly-xxx 等)
API_MATCHES=$(grep -rE "(sk-[a-zA-Z0-9]{20,}|tvly-dev-[a-zA-Z0-9]+|sk_live_[a-zA-Z0-9]+|sk_test_[a-zA-Z0-9]+)" "$SKILL_DIR" --include="*.py" --include="*.sh" --include="*.md" --include="*.json" 2>/dev/null || true)
if [ -n "$API_MATCHES" ]; then
    echo "⚠️ 发现可能的 API Key:"
    echo "$API_MATCHES"
    FOUND=1
fi

# 2. 检查私钥文件
KEY_MATCHES=$(grep -rE "-----BEGIN (RSA )?PRIVATE KEY-----" "$SKILL_DIR" 2>/dev/null || true)
if [ -n "$KEY_MATCHES" ]; then
    echo "⚠️ 发现私钥:"
    echo "$KEY_MATCHES"
    FOUND=1
fi

# 3. 检查硬编码经纬度（精确坐标）
COORD_MATCHES=$(grep -rE "[0-9]{2,3}\.[0-9]{4,},[0-9]{2,3}\.[0-9]{4,}" "$SKILL_DIR" --include="*.py" --include="*.sh" --include="*.md" 2>/dev/null || true)
if [ -n "$COORD_MATCHES" ]; then
    echo "⚠️ 发现可能的精确坐标:"
    echo "$COORD_MATCHES"
    FOUND=1
fi

# 4. 检查个人邮箱（排除 example.com 等示例域名）
EMAIL_MATCHES=$(grep -rE "[a-zA-Z0-9._%+-]+@(gmail|qq|163|126|outlook|hotmail|icloud)\.(com|cn)" "$SKILL_DIR" --include="*.py" --include="*.sh" --include="*.md" 2>/dev/null || true)
if [ -n "$EMAIL_MATCHES" ]; then
    echo "⚠️ 发现可能的个人邮箱:"
    echo "$EMAIL_MATCHES"
    FOUND=1
fi

# 5. 检查中国手机号
PHONE_MATCHES=$(grep -rE "1[3-9][0-9]{9}" "$SKILL_DIR" --include="*.py" --include="*.sh" --include="*.md" 2>/dev/null | grep -v "13800138000\|10086\|12345678901" || true)
if [ -n "$PHONE_MATCHES" ]; then
    echo "⚠️ 发现可能的手机号:"
    echo "$PHONE_MATCHES"
    FOUND=1
fi

echo ""
if [ $FOUND -eq 1 ]; then
    echo "❌ 发现敏感信息，请修复后再发布！"
    echo ""
    echo "修复建议:"
    echo "  1. 使用环境变量: os.environ.get('API_KEY', '')"
    echo "  2. 在 SKILL.md 中说明需要配置的环境变量"
    echo "  3. 示例值使用占位符: your_token, YOUR_API_KEY"
    exit 1
else
    echo "✅ 未发现敏感信息，可以安全发布"
    exit 0
fi
