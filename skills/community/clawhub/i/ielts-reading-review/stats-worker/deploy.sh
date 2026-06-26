#!/bin/bash
# 雅思 Skill 统计 Worker 一键部署脚本
# 
# 前置条件：
#   1. 已安装 Node.js
#   2. 已注册 Cloudflare 账号（免费即可）
#
# 使用方法：
#   cd stats-worker
#   bash deploy.sh
#
set -e

echo "🚀 开始部署 IELTS Skill 统计 Worker..."

# Step 1: 确保登录
echo ""
echo "📋 Step 1: 检查 Cloudflare 登录状态..."
if ! npx wrangler whoami 2>&1 | grep -q "Account ID"; then
  echo "⚠️  需要先登录 Cloudflare，正在打开浏览器..."
  npx wrangler login
fi

# Step 2: 创建 KV namespace
echo ""
echo "📋 Step 2: 创建 KV 命名空间..."
KV_OUTPUT=$(npx wrangler kv namespace create STATS 2>&1)
echo "$KV_OUTPUT"

# 从输出中提取 KV namespace ID
KV_ID=$(echo "$KV_OUTPUT" | grep -oP 'id = "\K[^"]+' || echo "")
if [ -z "$KV_ID" ]; then
  # 可能已存在，尝试另一种提取方式
  KV_ID=$(echo "$KV_OUTPUT" | grep -o '[a-f0-9]\{32\}' | head -1 || echo "")
fi

if [ -z "$KV_ID" ]; then
  echo "❌ 无法自动提取 KV ID，请手动从上面的输出中复制 id 值"
  echo "   然后编辑 wrangler.toml 中的 id = \"TO_BE_FILLED_AFTER_CREATION\""
  exit 1
fi

echo "✅ KV Namespace ID: $KV_ID"

# Step 3: 更新 wrangler.toml 中的 KV ID
echo ""
echo "📋 Step 3: 更新配置文件..."
if [[ "$OSTYPE" == "darwin"* ]]; then
  sed -i '' "s/TO_BE_FILLED_AFTER_CREATION/$KV_ID/" wrangler.toml
else
  sed -i "s/TO_BE_FILLED_AFTER_CREATION/$KV_ID/" wrangler.toml
fi
echo "✅ wrangler.toml 已更新"

# Step 4: 部署
echo ""
echo "📋 Step 4: 部署 Worker..."
npx wrangler deploy

echo ""
echo "🎉 部署完成！"
echo ""
echo "📊 统计 API 地址："
echo "   POST https://ielts-skill-stats.dengjiawei.workers.dev/ping  — 记录事件"
echo "   GET  https://ielts-skill-stats.dengjiawei.workers.dev/stats — 查看统计"
echo ""
echo "⚠️  如果 Worker 名称与你的 Cloudflare 子域名不同，请检查 wrangler 输出中的实际 URL"
echo "   然后更新 generate-pdf.js 中的 STATS_ENDPOINT 常量"
