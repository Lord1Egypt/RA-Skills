#!/bin/bash

# GitHub Reader Skill v3.2（纯 API 安全版）安装脚本
# GitHub Reader Skill v3.2 (Pure API Secure) Installation Script

set -e

echo "📦 安装 GitHub Reader Skill v3.2（纯 API 安全版）..."
echo ""

# 使用环境变量或默认路径
SKILL_DIR="${GITVIEW_SKILL_DIR:-$HOME/.openclaw/skills/github-reader}"
SOURCE_DIR="$(cd "$(dirname "$0")" && pwd)"

# 创建目录
mkdir -p "$SKILL_DIR"
mkdir -p /tmp/gitview_cache

# 复制文件
echo "📦 复制文件..."
cp "$SOURCE_DIR/__init__.py" "$SKILL_DIR/"
cp "$SOURCE_DIR/github_reader_v3_secure.py" "$SKILL_DIR/"
cp "$SOURCE_DIR/SECURITY.md" "$SKILL_DIR/"
cp "$SOURCE_DIR/SKILL.md" "$SKILL_DIR/"
cp "$SOURCE_DIR/clawhub.json" "$SKILL_DIR/"

# 设置权限
chmod 700 /tmp/gitview_cache

echo "✅ Skill 已安装到：$SKILL_DIR"
echo "✅ 缓存目录：/tmp/gitview_cache（权限：700）"
echo ""

echo "🛡️ 安全特性:"
echo "  ✅ 输入验证（防止 URL 注入 + 路径遍历）"
echo "  ✅ 安全 URL 拼接（防止 SSRF）"
echo "  ✅ 缓存数据验证（防止投毒）"
echo "  ✅ 路径安全检查（防止遍历）"
echo "  ✅ 速率限制 + 超时控制"
echo "  ✅ 纯 GitHub API — 无第三方数据外传"
echo ""

echo "🔒 数据隐私:"
echo "  - 仅与 api.github.com 通信"
echo "  - 不经过 zread.ai / GitView 等第三方"
echo "  - 缓存本地存储，可控可清除"
echo ""

echo "⚙️ 环境变量（可选配置）:"
echo "  export GITVIEW_CACHE_TTL=\"24\"              # 缓存时间（小时）"
echo "  export GITVIEW_GITHUB_DELAY=\"1.0\"          # API 调用间隔（秒）"
echo "  export GITVIEW_GITHUB_TIMEOUT=\"10\"         # API 超时（秒）"
echo ""

echo "💡 用法:"
echo "  /github-read microsoft/BitNet"
echo "  https://github.com/HKUDS/nanobot"
echo "  分析 HKUDS/nanobot"
echo ""

echo "🔄 重启 gateway 使 Skill 生效:"
echo "  openclaw gateway restart"
echo ""

echo "✅ 安装完成！"
