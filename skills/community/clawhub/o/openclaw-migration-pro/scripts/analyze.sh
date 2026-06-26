#!/bin/bash
# OpenClaw 迁移工具 - 分析环境

set -e

# 配置
OPENCLAW_DIR="${HOME}/.openclaw"
WORKSPACE_DIR="${HOME}/openclaw/workspace"
OUTPUT_DIR="${1:-${HOME}/openclaw-migrate}"

# 颜色
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🔍 分析 OpenClaw 环境...${NC}"
echo ""

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 初始化 MANIFEST
cat > "$OUTPUT_DIR/MANIFEST.json" << 'EOF'
{
  "skills": {
    "pack": [],
    "reinstall": []
  },
  "memory": {
    "files": 0,
    "size": "0MB"
  },
  "config": {},
  "associations": []
}
EOF

echo "📊 分析完成"
echo ""
echo "MANIFEST 已生成：$OUTPUT_DIR/MANIFEST.json"
echo ""
echo "下一步：运行 pack 命令打包"
echo "  openclaw-migrate pack --output ~/openclaw-pack/"
