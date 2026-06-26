#!/bin/bash
# Daily Memory Cleanup Script (Simplified)
# 📅 Created: 2026-03-12
# 📅 Updated: 2026-03-19 - Fixed hardcoded paths for cross-platform compatibility

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 跨平台路径配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(dirname "$SCRIPT_DIR")"
MEM_DIR="${WORKSPACE_ROOT}/memory"
TODAY=$(date +%Y-%m-%d)

# macOS/Linux 兼容的日期计算
if [[ "$OSTYPE" == "darwin"* ]]; then
    YESTERDAY=$(date -v-1d +%Y-%m-%d)
else
    YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)
fi

echo -e "${BLUE}=== Daily Memory Cleanup ===${NC}"
echo -e "${BLUE}Date: $(date +%Y-%m-%d)${NC}"
echo ""

TASKS_COMPLETED=0
TASKS_FAILED=0

run_task() {
    local task_name="$1"
    local task_command="$2"

    echo -e "${YELLOW}▶ $task_name${NC}"

    if eval "$task_command" > /tmp/cleanup-task.log 2>&1; then
        echo -e "${GREEN}✅ $task_name completed${NC}"
        ((TASKS_COMPLETED++))
        return 0
    else
        echo -e "${RED}❌ $task_name failed${NC}"
        ((TASKS_FAILED++))
        return 1
    fi
}

echo -e "${BLUE}--- Step 1: Verify TL;DR exists ---${NC}"
run_task "Check today's TL;DR" \
    "test -f ${MEM_DIR}/${TODAY}.md && grep -q 'TL;DR 摘要' ${MEM_DIR}/${TODAY}.md && echo '✓ TL;DR exists' || echo '✗ TL;DR missing'"

echo -e "${BLUE}--- Step 2: Check for key sections ---${NC}"
run_task "Verify TL;DR has bullet points" \
    "test -f ${MEM_DIR}/${TODAY}.md && grep -A 10 'TL;DR 摘要' ${MEM_DIR}/${TODAY}.md | grep -q '^\s*•\|^\s*-\|^\s*\*' && echo '✓ Bullet points found' || echo '✗ No bullet points'"

run_task "Check for progress tracking" \
    "test -f ${MEM_DIR}/${TODAY}.md && grep -q 'Progress Tracking' ${MEM_DIR}/${TODAY}.md && echo '✓ Progress tracking present' || echo '✗ Progress tracking missing'"

echo -e "${BLUE}--- Step 3: Check previous day ---${NC}"
if [ -f "${MEM_DIR}/${YESTERDAY}.md" ]; then
    run_task "Verify yesterday's TL;DR" \
        "grep -q 'TL;DR 摘要' ${MEM_DIR}/${YESTERDAY}.md && echo '✓ Yesterday TL;DR exists' || echo '✗ Yesterday TL;DR missing'"
else
    echo -e "${YELLOW}⚠ Yesterday's file not found${NC}"
    ((TASKS_FAILED++))
fi

echo -e "${BLUE}--- Step 4: Check LONG-TERM memory ---${NC}"
run_task "Check MEMORY.md exists" \
    "test -f ${MEM_DIR}/MEMORY.md && echo '✓ MEMORY.md exists' || echo '✗ MEMORY.md missing'"

run_task "Check MEMORY.md has content" \
    "test -f ${MEM_DIR}/MEMORY.md && grep -q '# ' ${MEM_DIR}/MEMORY.md && echo '✓ MEMORY.md has content' || echo '✗ MEMORY.md empty'"

echo -e "${BLUE}--- Step 5: Cleanup statistics ---${NC}"
if [ -f "${MEM_DIR}/${TODAY}.md" ]; then
    LINE_COUNT=$(wc -l < ${MEM_DIR}/${TODAY}.md)
    WORD_COUNT=$(wc -w < ${MEM_DIR}/${TODAY}.md)
    TOKEN_COUNT=$(wc -c < ${MEM_DIR}/${TODAY}.md)

    echo -e "   Lines: $LINE_COUNT"
    echo -e "   Words: $WORD_COUNT"
    echo -e "   Bytes: $TOKEN_COUNT"

    if [ $TOKEN_COUNT -lt 10240 ]; then
        echo -e "${GREEN}✓ File size is reasonable (< 10KB)${NC}"
    else
        echo -e "${YELLOW}⚠ File size is large (> 10KB)${NC}"
    fi
fi

echo ""
echo -e "${BLUE}=== Summary ===${NC}"
echo -e "Completed: ${GREEN}$TASKS_COMPLETED${NC}"
echo -e "Failed: ${RED}$TASKS_FAILED${NC}"
echo -e "Total: $((TASKS_COMPLETED + TASKS_FAILED))"
echo ""
echo -e "${BLUE}✅ Complete!${NC}"
