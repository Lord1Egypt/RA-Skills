#!/bin/bash
#===============================================================================
# huo15-memory-evolution: 验证脚本
#
# 用法: ./verify.sh
#
# 功能: 验证迁移后记忆系统是否正确隔离
#===============================================================================

set -e

# 动态路由：优先使用 PWD 检测 > OC_AGENT_ID > 默认
if [ -d "${PWD}/memory" ] && [[ "$PWD" == *".openclaw/workspace"* ]]; then
    WORKSPACE_DIR="$PWD"
elif [ -n "${OC_AGENT_ID:-}" ]; then
    WORKSPACE_DIR="$HOME/.openclaw/workspace-${OC_AGENT_ID}"
else
    WORKSPACE_DIR="$HOME/.openclaw/workspace"
fi

MEMORY_DIR="$WORKSPACE_DIR/memory"
OPENCLAW_DIR="$HOME/.openclaw"

echo "🔍 huo15-memory-evolution 验证"
echo "================================"
echo ""

PASS=0
FAIL=0

check() {
    local name="$1"
    local result="$2"
    if [ "$result" == "PASS" ]; then
        echo "   ✅ $name"
        PASS=$((PASS + 1))
    else
        echo "   ❌ $name"
        FAIL=$((FAIL + 1))
    fi
}

#===========================================
# 1. 检查主 workspace MEMORY.md
#===========================================
echo "1️⃣ 检查主 Workspace..."

if [ -f "$WORKSPACE_DIR/MEMORY.md" ]; then
    LINES=$(wc -l < "$WORKSPACE_DIR/MEMORY.md")
    if [ "$LINES" -le 200 ]; then
        check "MEMORY.md ≤ 200 行 (当前: ${LINES}行)" "PASS"
    else
        check "MEMORY.md ≤ 200 行 (当前: ${LINES}行)" "FAIL"
    fi
else
    check "MEMORY.md 存在" "FAIL"
fi

#===========================================
# 2. 检查新目录结构
#===========================================
echo ""
echo "2️⃣ 检查新目录结构..."

for type in user feedback project reference archive; do
    if [ -d "$MEMORY_DIR/$type" ]; then
        check "memory/$type/ 目录存在" "PASS"
    else
        check "memory/$type/ 目录存在" "FAIL"
    fi
done

#===========================================
# 3. 检查 index.json
#===========================================
echo ""
echo "3️⃣ 检查 index.json..."

if [ -f "$MEMORY_DIR/index.json" ]; then
    check "index.json 存在" "PASS"
    if grep -q '"version"' "$MEMORY_DIR/index.json" 2>/dev/null; then
        check "index.json 格式正确" "PASS"
    else
        check "index.json 格式正确" "FAIL"
    fi
else
    check "index.json 存在" "FAIL"
fi

#===========================================
# 4. 检查动态 Agent 隔离
#===========================================
echo ""
echo "4️⃣ 检查动态 Agent 记忆隔离..."

SENSITIVE_PATTERNS=(
    "工商银行"
    "建设银行"
    "3803021019200476891"
    "37150198541000001436"
)

WORKSPACES=$(find "$OPENCLAW_DIR" -maxdepth 1 -type d -name "workspace-wecom-*" 2>/dev/null | sort)
AGENT_COUNT=0

for ws in $WORKSPACES; do
    AGENT_COUNT=$((AGENT_COUNT + 1))
    ws_name=$(basename "$ws")
    
    # 检查目录结构
    if [ -d "$ws/memory" ]; then
        HAS_MEMORY=1
        for type in user feedback project reference; do
            if [ ! -d "$ws/memory/$type" ]; then
                HAS_MEMORY=0
                break
            fi
        done
        
        if [ "$HAS_MEMORY" == "1" ]; then
            check "$ws_name: 独立 memory/ 结构完整" "PASS"
        else
            check "$ws_name: 独立 memory/ 结构完整" "FAIL"
        fi
    else
        check "$ws_name: memory/ 目录存在" "FAIL"
    fi
    
    # 检查敏感信息（排除 skills 目录）
    SENSITIVE_FOUND=0
    for pattern in "${SENSITIVE_PATTERNS[@]}"; do
        if grep -r -l "$pattern" "$ws/" 2>/dev/null | grep -v ".git" | grep -v "skills/" > /dev/null; then
            SENSITIVE_FOUND=1
            break
        fi
    done
    
    if [ "$SENSITIVE_FOUND" == "0" ]; then
        check "$ws_name: 无 ZhaoBo 敏感信息" "PASS"
    else
        check "$ws_name: 无 ZhaoBo 敏感信息" "FAIL"
    fi
done

#===========================================
# 5. 汇总
#===========================================
echo ""
echo "================================"
echo "📊 验证结果汇总"
echo "================================"
echo "   ✅ 通过: $PASS"
echo "   ❌ 失败: $FAIL"
echo "   处理动态 Agent 数: $AGENT_COUNT"
echo ""

if [ "$FAIL" == "0" ]; then
    echo "✅ 所有验证通过! 记忆系统已正确改造。"
    exit 0
else
    echo "⚠️  有 $FAIL 项验证失败，请检查。"
    exit 1
fi
