#!/bin/bash

# Smart Search 快速配置脚本
# 用于测试环境快速配置

set -e

echo "🔧 Smart Search 快速配置"
echo "================================"
echo ""

# 1. 生成主密钥
if [ ! -f .env ]; then
  echo "1. 生成主密钥..."
  export OPENCLAW_MASTER_KEY=$(openssl rand -base64 32)
  echo "OPENCLAW_MASTER_KEY=$OPENCLAW_MASTER_KEY" > .env
  echo "✅ 主密钥已生成并保存到 .env"
else
  echo "✅ .env 文件已存在"
  source .env
fi

echo ""
echo "2. 当前配置状态:"
echo "   主密钥长度：${#OPENCLAW_MASTER_KEY} 字符"
echo "   配置文件：~/.openclaw/secrets/smart-search.json.enc"
echo ""

echo "3. 配置 API Key（至少配置一个引擎才能测试）:"
echo ""
echo "   请选择要配置的引擎："
echo "   1) 百炼 MCP (中文搜索，2000 次/月)"
echo "   2) Tavily (高级搜索，1000 次/月)"
echo "   3) Serper (Google 结果，2500 次/月)"
echo "   4) Exa (学术/技术，1000 次/月)"
echo "   5) Firecrawl (网页抓取，500 页/月)"
echo "   6) 跳过（稍后手动配置）"
echo ""

read -p "请选择 [1-6]: " choice

case $choice in
  1)
    read -p "输入百炼 API Key: " key
    export BAILIAN_API_KEY="$key"
    ;;
  2)
    read -p "输入 Tavily API Key: " key
    export TAVILY_API_KEY="$key"
    ;;
  3)
    read -p "输入 Serper API Key: " key
    export SERPER_API_KEY="$key"
    ;;
  4)
    read -p "输入 Exa API Key: " key
    export EXA_API_KEY="$key"
    ;;
  5)
    read -p "输入 Firecrawl API Key: " key
    export FIRECRAWL_API_KEY="$key"
    ;;
  6)
    echo "跳过配置"
    exit 0
    ;;
esac

echo ""
echo "4. 运行配置向导..."
export OPENCLAW_MASTER_KEY
npm run setup

echo ""
echo "✅ 配置完成！"
echo ""
echo "测试搜索:"
echo "  npm run search \"test\""
echo "  npm run search \"OpenClaw 智能搜索\""
echo "  npm run search \"transformer 论文\" -- --intent=academic"
echo ""
