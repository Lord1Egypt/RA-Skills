#!/bin/bash
# create_agent.sh - 创建子Agent的workspace
# 版本: 5.0.2 (修复：修正workspace路径)

set -e

AGENT_NAME=$1
AGENT_DIR=~/.openclaw/workspace-$AGENT_NAME

if [ -z "$AGENT_NAME" ]; then
    echo "Usage: $0 <agent_name>"
    echo "Example: $0 munger"
    exit 1
fi

echo "🚀 Creating sub-agent: $AGENT_NAME"

mkdir -p "$AGENT_DIR"/{memory,skills}

touch "$AGENT_DIR"/{SOUL.md,AGENTS.md,IDENTITY.md,WORKSPACE.md}

mkdir -p "$AGENT_DIR/memory"
echo "# Memory Index" > "$AGENT_DIR/memory/index.md"

mkdir -p "$AGENT_DIR/skills"

cat > "$AGENT_DIR/WORKSPACE.md" << EOF
# WORKSPACE.md

这是 ${AGENT_NAME} 的独立工作空间。

## 目录结构
- memory/ - 记忆系统
- skills/ - 专属技能

## 权限
- ✅ 可以读写此目录下的所有文件
- ❌ 不能访问主Agent的敏感文件

## 调用方式（持久Agent）

\`\`\`bash
sessions_send sessionKey="agent:${AGENT_NAME}:main" message="任务描述" timeoutSeconds=0
\`\`\`

---

**创建时间:** $(date +%Y-%m-%d)
**版本:** v5.0.2
EOF

chmod -R 755 "$AGENT_DIR"

echo ""
echo "✅ Created workspace: $AGENT_DIR"
echo ""
echo "📝 Next steps:"
echo "  1. Edit $AGENT_DIR/SOUL.md"
echo "  2. Edit $AGENT_DIR/AGENTS.md"
echo "  3. Install skills: cd $AGENT_DIR/skills/ && clawhub install <skill>"
echo "  4. Update openclaw.json: add { id: '$AGENT_NAME', workspace: '$AGENT_DIR' } to agents.list"
echo "  5. Restart gateway: openclaw gateway restart"
echo "  6. Test: sessions_send sessionKey=\"agent:${AGENT_NAME}:main\" message='自我介绍' timeoutSeconds=60"