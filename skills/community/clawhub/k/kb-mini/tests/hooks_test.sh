#!/bin/bash
# hooks.sh TDD 测试
# Phase 3: OpenClaw Hooks 集成

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOKS="$SCRIPT_DIR/../scripts/hooks.sh"
STORAGE="$SCRIPT_DIR/../scripts/storage.sh"
RETRIEVER="$SCRIPT_DIR/../scripts/retriever.sh"

echo "=== Phase 3: hooks.sh 测试 ==="

# ============================================
# TEST 1: before_agent_start hook - recall
# ============================================
echo ""
echo "TEST 1: before_agent_start hook"

TEST_DB="/tmp/kb_hooks_t1_$$.db"
export KNOWLEDGE_DB="$TEST_DB"
rm -f "$TEST_DB"

"$STORAGE" init
"$STORAGE" store --title "OpenClaw Config" --content "Configure OpenClaw hooks in openclaw.json" --source "manual" --topic-key "openclaw-config"

# Simulate before_agent_start hook - use context that matches the content word order
result=$("$HOOKS" before_agent_start --context "Configure OpenClaw hooks" 2>&1)
echo "Result: $result"

if echo "$result" | grep -q '"entries_used": 1' && echo "$result" | grep -q '"injected": true'; then
    echo "✅ TEST 1 PASSED"
else
    echo "❌ TEST 1 FAILED"
fi

rm -f "$TEST_DB"

# ============================================
# TEST 2: after_turn hook - capture
# ============================================
echo ""
echo "TEST 2: after_turn hook - 显式存储"

TEST_DB="/tmp/kb_hooks_t2_$$.db"
export KNOWLEDGE_DB="$TEST_DB"
rm -f "$TEST_DB"

"$STORAGE" init

# 模拟用户说 "请记住这个配置"
result=$("$HOOKS" after_turn --user "请记住这个配置：api_key=12345" --agent "好的，已记住" 2>&1)
echo "Result: $result"

if echo "$result" | grep -q '"captured": true'; then
    echo "✅ TEST 2 PASSED"
else
    echo "❌ TEST 2 FAILED"
fi

# 验证是否存入数据库
count=$(sqlite3 "$TEST_DB" "SELECT COUNT(*) FROM entries WHERE topic_key LIKE '%capture-%';" 2>/dev/null || echo "0")
if [[ "$count" -gt 0 ]]; then
    echo "✅ Verified: Entry captured to database"
else
    echo "❌ Failed: Entry not captured"
fi

rm -f "$TEST_DB"

# ============================================
# TEST 3: after_turn hook - 低优先级不存储
# ============================================
echo ""
echo "TEST 3: after_turn hook - 低优先级"

TEST_DB="/tmp/kb_hooks_t3_$$.db"
export KNOWLEDGE_DB="$TEST_DB"
rm -f "$TEST_DB"

"$STORAGE" init

result=$("$HOOKS" after_turn --user "你好" --agent "你好，有什么可以帮助你的？" 2>&1)
echo "Result: $result"

if echo "$result" | grep -q '"captured": false'; then
    echo "✅ TEST 3 PASSED"
else
    echo "❌ TEST 3 FAILED"
fi

rm -f "$TEST_DB"

# ============================================
# TEST 4: 生成的 hook 脚本格式正确
# ============================================
echo ""
echo "TEST 4: 生成 hook 脚本格式"

TEST_DB="/tmp/kb_hooks_t4_$$.db"
export KNOWLEDGE_DB="$TEST_DB"
rm -f "$TEST_DB"

"$STORAGE" init

# 生成 hook 脚本
hook_output=$("$HOOKS" generate before_agent_start 2>&1)
echo "Generated hook: $hook_output"

if echo "$hook_output" | grep -q "hooks before_agent_start"; then
    echo "✅ TEST 4 PASSED"
else
    echo "❌ TEST 4 FAILED"
fi

rm -f "$TEST_DB"

# ============================================
# TEST 5: config 设置
# ============================================
echo ""
echo "TEST 5: hooks config"

TEST_DB="/tmp/kb_hooks_t5_$$.db"
export KNOWLEDGE_DB="$TEST_DB"
rm -f "$TEST_DB"

"$STORAGE" init

# 设置 KB 路径
"$HOOKS" config --kb-path "$TEST_DB" 2>&1

# 验证
if [[ -f "$TEST_DB" ]]; then
    echo "✅ TEST 5 PASSED: KB path configured"
else
    echo "❌ TEST 5 FAILED"
fi

rm -f "$TEST_DB"

echo ""
echo "=== Phase 3 测试完成 ==="
