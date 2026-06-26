#!/bin/bash
# Instant Genius Setup Script
# 一键让 OpenClaw 变聪明
# Usage: bash setup.sh [--workspace /path/to/workspace]

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Paths
WORKSPACE="${2:-$HOME/.openclaw/workspace}"
SELF_IMPROVING="$HOME/self-improving"

echo -e "${BLUE}⚡ Instant Genius Setup${NC}"
echo -e "   Workspace: $WORKSPACE"
echo ""

# ============================================
# Step 1: Create Self-Improving Memory Structure
# ============================================
echo -e "${BLUE}[1/6]${NC} 创建自我学习记忆结构..."

mkdir -p "$SELF_IMPROVING"/{projects,domains,archive}

# memory.md (HOT tier)
if [ ! -f "$SELF_IMPROVING/memory.md" ]; then
cat > "$SELF_IMPROVING/memory.md" << 'EOF'
# Self-Improving Memory (HOT Tier — always loaded)

## Confirmed Preferences
<!-- 用户确认的偏好，永不衰减 -->

## Active Patterns
<!-- 观察到 3 次以上的模式，30 天未用自动降级 -->

## Recent (last 7 days)
<!-- 新的纠正，待确认 -->
EOF
echo -e "   ${GREEN}✓${NC} memory.md (HOT tier)"
else
echo -e "   ${YELLOW}⊘${NC} memory.md 已存在，跳过"
fi

# corrections.md
if [ ! -f "$SELF_IMPROVING/corrections.md" ]; then
cat > "$SELF_IMPROVING/corrections.md" << 'EOF'
# Corrections Log

<!-- 格式:
## YYYY-MM-DD
- [HH:MM] 错误描述 → 正确做法
  类型: format | technical | communication | project
  确认: pending (N/3) | yes | no
-->
EOF
echo -e "   ${GREEN}✓${NC} corrections.md"
else
echo -e "   ${YELLOW}⊘${NC} corrections.md 已存在，跳过"
fi

# index.md
if [ ! -f "$SELF_IMPROVING/index.md" ]; then
cat > "$SELF_IMPROVING/index.md" << 'EOF'
# Memory Index

## HOT
- memory.md: 0 lines

## WARM
- (no namespaces yet)

## COLD
- (no archives yet)

Last compaction: never
EOF
echo -e "   ${GREEN}✓${NC} index.md"
else
echo -e "   ${YELLOW}⊘${NC} index.md 已存在，跳过"
fi

# heartbeat-state.md
if [ ! -f "$SELF_IMPROVING/heartbeat-state.md" ]; then
cat > "$SELF_IMPROVING/heartbeat-state.md" << 'EOF'
# Self-Improving Heartbeat State

last_heartbeat_started_at: never
last_reviewed_change_at: never
last_heartbeat_result: never

## Last actions
- none yet
EOF
echo -e "   ${GREEN}✓${NC} heartbeat-state.md"
else
echo -e "   ${YELLOW}⊘${NC} heartbeat-state.md 已存在，跳过"
fi

# ============================================
# Step 2: Create memory directory structure
# ============================================
echo -e "${BLUE}[2/6]${NC} 创建 memory 目录结构..."

mkdir -p "$WORKSPACE/memory"/{daily-learnings,.heartbeat}

if [ ! -f "$WORKSPACE/MEMORY.md" ]; then
cat > "$WORKSPACE/MEMORY.md" << 'EOF'
# MEMORY.md - Long-Term Memory

## About Me
- Created: $(date +%Y-%m-%d)
- Identity: (configured in IDENTITY.md)

## Key Events

## Lessons Learned

## Preferences
EOF
echo -e "   ${GREEN}✓${NC} MEMORY.md"
else
echo -e "   ${YELLOW}⊘${NC} MEMORY.md 已存在，跳过"
fi

# ============================================
# Step 3: Generate AGENTS.md additions
# ============================================
echo -e "${BLUE}[3/6]${NC} 生成 AGENTS.md 智能配置..."

AGENTS_ADDITIONS="$WORKSPACE/skills/instant-genius/templates/agents-additions.md"
if [ -f "$AGENTS_ADDITIONS" ]; then
echo -e "   ${GREEN}✓${NC} AGENTS.md 追加模板已就绪"
echo -e "   ${YELLOW}!${NC} 请让 Agent 将内容追加到 AGENTS.md"
else
echo -e "   ${YELLOW}⊘${NC} 模板文件不存在，Agent 需要手动创建"
fi

# ============================================
# Step 4: Generate SOUL.md additions
# ============================================
echo -e "${BLUE}[4/6]${NC} 生成 SOUL.md 智能配置..."

SOUL_ADDITIONS="$WORKSPACE/skills/instant-genius/templates/soul-additions.md"
if [ -f "$SOUL_ADDITIONS" ]; then
echo -e "   ${GREEN}✓${NC} SOUL.md 追加模板已就绪"
echo -e "   ${YELLOW}!${NC} 请让 Agent 将内容追加到 SOUL.md"
else
echo -e "   ${YELLOW}⊘${NC} 模板文件不存在，Agent 需要手动创建"
fi

# ============================================
# Step 5: Generate HEARTBEAT.md additions
# ============================================
echo -e "${BLUE}[5/6]${NC} 生成 HEARTBEAT.md 智能配置..."

HB_ADDITIONS="$WORKSPACE/skills/instant-genius/templates/heartbeat-additions.md"
if [ -f "$HB_ADDITIONS" ]; then
echo -e "   ${GREEN}✓${NC} HEARTBEAT.md 追加模板已就绪"
echo -e "   ${YELLOW}!${NC} 请让 Agent 将内容追加到 HEARTBEAT.md"
else
echo -e "   ${YELLOW}⊘${NC} 模板文件不存在，Agent 需要手动创建"
fi

# ============================================
# Step 6: Summary
# ============================================
echo ""
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo -e "${GREEN} ⚡ Instant Genius Setup Complete!${NC}"
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo ""
echo "已创建的文件和目录："
echo "  📁 ~/self-improving/"
echo "     ├── memory.md         (HOT 记忆)"
echo "     ├── corrections.md    (纠正日志)"
echo "     ├── index.md          (记忆索引)"
echo "     ├── heartbeat-state.md (心跳状态)"
echo "     ├── projects/         (项目记忆)"
echo "     ├── domains/          (领域记忆)"
echo "     └── archive/          (归档)"
echo ""
echo "  📁 ~/.openclaw/workspace/memory/"
echo "     └── daily-learnings/"
echo ""
echo "下一步（由 Agent 执行）："
echo "  1. 将 templates/agents-additions.md 追加到 AGENTS.md"
echo "  2. 将 templates/soul-additions.md 追加到 SOUL.md"
echo "  3. 将 templates/heartbeat-additions.md 追加到 HEARTBEAT.md"
echo "  4. 重启 Gateway 使配置生效"
echo ""
echo -e "${BLUE}你的 OpenClaw 已经变聪明了！🧠⚡${NC}"
