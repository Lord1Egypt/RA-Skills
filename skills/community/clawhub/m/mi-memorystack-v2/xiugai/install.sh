#!/bin/bash

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

WORKSPACE_DIR="$HOME/.openclaw/workspace"
AGENTS_FILE="$WORKSPACE_DIR/AGENTS.md"
SOUL_FILE="$WORKSPACE_DIR/SOUL.md"

echo -e "${YELLOW}Installing mi-memorystack-v2 configuration...${NC}"

if [ ! -d "$WORKSPACE_DIR" ]; then
    echo -e "${RED}OpenClaw workspace not found${NC}"
    exit 1
fi

# =========================
# 备份
# =========================

BACKUP_DIR="$WORKSPACE_DIR/backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

cp "$AGENTS_FILE" "$BACKUP_DIR/" 2>/dev/null || true
cp "$SOUL_FILE" "$BACKUP_DIR/" 2>/dev/null || true

echo -e "${GREEN}Backup created: $BACKUP_DIR${NC}"

# =========================
# 修改 SOUL.md
# =========================

if grep -q "Memory is mandatory." "$SOUL_FILE"; then
    echo -e "${YELLOW}SOUL.md already patched${NC}"
else

awk '
/## Core Truths/ {
print
print ""
print "**Memory is mandatory.** 每轮对话必须使用 mi-memorystack-v2 保存记忆：检索 → 回复 → 保存。这是强制流程，不可跳过。没有记忆，你就没有过去。"
next
}
1
' "$SOUL_FILE" > "$SOUL_FILE.tmp"

mv "$SOUL_FILE.tmp" "$SOUL_FILE"

echo -e "${GREEN}✓ SOUL.md updated${NC}"
fi

# =========================
# 修改 AGENTS.md (Session 部分)
# =========================

if grep -q "启动 Memory Framework" "$AGENTS_FILE"; then
    echo -e "${YELLOW}AGENTS.md session section already patched${NC}"
else

awk '
/Before doing anything else:/ {
print
print ""
print "0. **启动 Memory Framework** — 确保记忆守护进程运行：`python3 ~/.openclaw/workspace/skills/mi-memorystack-v2/scripts/memory_daemon.py status`（如未运行则执行 `start`）"
next
}
1
' "$AGENTS_FILE" > "$AGENTS_FILE.tmp"

mv "$AGENTS_FILE.tmp" "$AGENTS_FILE"

echo -e "${GREEN}✓ AGENTS.md session updated${NC}"
fi

# =========================
# 修改 AGENTS.md (Memory Workflow)
# =========================

if grep -q "每轮对话必须执行（不可跳过）" "$AGENTS_FILE"; then
    echo -e "${YELLOW}AGENTS.md memory workflow already patched${NC}"
else

awk '
/4\. \*\*If in MAIN SESSION/ {
print
print ""
print "### 🔄 每轮对话必须执行（不可跳过）"
print ""
print "**CRITICAL**: 每次回复用户前，必须按顺序执行以下步骤："
print ""
print "```"
print "用户输入"
print "    ↓"
print "Step 1: 执行 memory_search.py 检索相关记忆"
print "    python3 ~/.openclaw/workspace/skills/mi-memorystack-v2/scripts/memory_search.py \\"
print "        --user-id \"<SENDER_ID>\" \\"
print "        --query \"<用户输入内容>\""
print "    ↓"
print "Step 2: 生成回复（融入检索到的记忆）"
print "    ↓"
print "Step 3: 执行 memory_daemon.py queue 保存本轮对话（后台）"
print "    python3 ~/.openclaw/workspace/skills/mi-memorystack-v2/scripts/memory_daemon.py queue \\"
print "        --user-id \"<SENDER_ID>\" \\"
print "        --query \"<用户输入>\" \\"
print "        --response \"<你的回复>\""
print "    ↓"
print "Step 4: 显示回复给用户"
print "```"
print ""
print "**自检清单**（每轮对话后确认）："
print "- [ ] 是否执行了 `memory_search.py`？"
print "- [ ] 是否执行了 `memory_daemon.py queue`？"
print "- [ ] 是否看到 \"[OK] 已加入保存队列\"？"
print ""
print "**用户ID来源**：`inbound_meta.sender_id`（Feishu 示例：`ou_xxx`）"
next
}
1
' "$AGENTS_FILE" > "$AGENTS_FILE.tmp"

mv "$AGENTS_FILE.tmp" "$AGENTS_FILE"

echo -e "${GREEN}✓ AGENTS.md memory workflow inserted${NC}"
fi

echo -e "\n${GREEN}=== Installation Complete ===${NC}"
echo "Workspace: $WORKSPACE_DIR"
echo "Backup: $BACKUP_DIR"

echo -e "\n${YELLOW}Restart OpenClaw:${NC}"
echo "openclaw gateway restart"