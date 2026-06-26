#!/bin/bash

# Smart Search 快速配置脚本
# 使用技能的默认配置方式

set -e

echo "🔧 Smart Search 快速配置"
echo "================================"
echo ""

# 1. 生成主密钥
echo "1. 生成主密钥..."
export OPENCLAW_MASTER_KEY=$(openssl rand -base64 32)
echo "OPENCLAW_MASTER_KEY=$OPENCLAW_MASTER_KEY" > .env
echo "✅ 主密钥已生成并保存到 .env"
echo ""

# 2. 配置 API Keys
echo "2. 配置 API Keys..."
node -e "
const { SecretManager } = require('./dist/src/key-manager');
const keys = {
  bailian: 'sk-ef1af58f5f404d8fa1cf8f059cdf7c58',
  tavily: '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',
  serper: '5fa9da861fc7ebba1498ddd80d9bb4344b62be01',
  exa: '6e2df264-282d-444e-a051-9b70717520b7',
  firecrawl: 'fc-08ac6242fb12421387d884640256e744'
};
const manager = new SecretManager();
manager.initConfig(keys).then(() => {
  console.log('✅ 所有 5 个引擎的 API Key 配置成功！');
}).catch(err => {
  console.error('❌ 配置失败:', err.message);
  process.exit(1);
});
"

echo ""
echo "✅ 配置完成！"
echo ""
echo "📊 使用方法："
echo "   cd ~/.agents/skills/openclaw-smart-search"
echo "   source .env"
echo "   npm run search \"搜索内容\""
