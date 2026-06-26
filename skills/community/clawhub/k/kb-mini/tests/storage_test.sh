#!/bin/bash
# storage.sh TDD 测试
# RED: 写测试 → GREEN: 最小实现 → REFACTOR: 重构

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KB_SCRIPT="$SCRIPT_DIR/../scripts/storage.sh"

# 测试数据库路径（测试用）
TEST_DB="/tmp/kb_test_$$.db"
export KNOWLEDGE_DB="$TEST_DB"

echo "Testing with KB_SCRIPT=$KB_SCRIPT"
echo "Test DB=$TEST_DB"

# 清理函数
cleanup() {
    rm -f "$TEST_DB"
    rm -f "${TEST_DB}-journal"
}

trap cleanup EXIT

# 初始化数据库
init_db() {
    rm -f "$TEST_DB" "${TEST_DB}-journal"
}

echo "=== Phase 1: storage.sh 核心功能测试 ==="

# ============================================
# TEST 1: store - 基本存储
# ============================================
echo ""
echo "TEST 1: store - 基本存储"

init_db
"$KB_SCRIPT" init

result=$("$KB_SCRIPT" store --title "Test Entry" --content "Test content" --source "manual" 2>&1)
echo "Result: $result"

if echo "$result" | grep -q '"status".*"ok"'; then
    echo "✅ TEST 1 PASSED: store 基本存储成功"
else
    echo "❌ TEST 1 FAILED: store 返回错误"
    exit 1
fi

# ============================================
# TEST 2: store - 相同 topic_key 追加
# ============================================
echo ""
echo "TEST 2: store - 相同 topic_key 追加（upsert）"

init_db
"$KB_SCRIPT" init

# 第一次存入
"$KB_SCRIPT" store --title "Test" --content "Content A" --source "manual" --topic-key "test-entry" 2>&1

# 第二次存入相同 topic_key
result=$("$KB_SCRIPT" store --title "Test" --content "Content B" --source "manual" --topic-key "test-entry" 2>&1)

if echo "$result" | grep -q '"action".*"update"'; then
    echo "✅ TEST 2 PASSED: upsert 更新成功"
else
    echo "❌ TEST 2 FAILED: upsert 未更新"
    echo "Result was: $result"
    exit 1
fi

# ============================================
# TEST 3: search - 关键词检索
# ============================================
echo ""
echo "TEST 3: search - 关键词检索"

init_db
"$KB_SCRIPT" init

"$KB_SCRIPT" store --title "OpenClaw Hooks" --content "Configure before_agent_start and after_turn hooks" --source "manual" 2>&1
"$KB_SCRIPT" store --title "SQLite FTS5" --content "Full-text search with SQLite FTS5" --source "manual" 2>&1

result=$("$KB_SCRIPT" search --query "OpenClaw" 2>&1)
echo "Search result: $result"

if echo "$result" | grep -q "OpenClaw Hooks"; then
    echo "✅ TEST 3 PASSED: 关键词检索成功"
else
    echo "❌ TEST 3 FAILED: 检索未返回预期结果"
    exit 1
fi

# ============================================
# TEST 4: retrieve - 按 topic_key 获取
# ============================================
echo ""
echo "TEST 4: retrieve - 按 topic_key 获取"

init_db
"$KB_SCRIPT" init

"$KB_SCRIPT" store --title "Test Retrieve" --content "Full content here" --source "manual" --topic-key "retrieve-test" 2>&1

result=$("$KB_SCRIPT" retrieve --topic-key "retrieve-test" 2>&1)
echo "Retrieve result: $result"

if echo "$result" | grep -q "Full content here"; then
    echo "✅ TEST 4 PASSED: retrieve 成功"
else
    echo "❌ TEST 4 FAILED: retrieve 未返回内容"
    exit 1
fi

# ============================================
# TEST 5: store - 带 tags
# ============================================
echo ""
echo "TEST 5: store - 带 tags"

init_db
"$KB_SCRIPT" init

result=$("$KB_SCRIPT" store --title "Tagged Entry" --content "Content" --source "manual" --tags "tag1,tag2" 2>&1)

if echo "$result" | grep -q '"status".*"ok"'; then
    echo "✅ TEST 5 PASSED: tags 存储成功"
else
    echo "❌ TEST 5 FAILED: tags 存储失败"
    exit 1
fi

# ============================================
# TEST 6: search - 按 source 过滤
# ============================================
echo ""
echo "TEST 6: search - 按 source 过滤"

init_db
"$KB_SCRIPT" init

"$KB_SCRIPT" store --title "GitHub Entry" --content "From github" --source "github" 2>&1
"$KB_SCRIPT" store --title "HF Entry" --content "From huggingface" --source "huggingface" 2>&1

result=$("$KB_SCRIPT" search --query "entry" --source "github" 2>&1)
echo "Source filter result: $result"

if echo "$result" | grep -q "GitHub Entry" && ! echo "$result" | grep -q "HF Entry"; then
    echo "✅ TEST 6 PASSED: source 过滤成功"
else
    echo "❌ TEST 6 FAILED: source 过滤失败"
    exit 1
fi

echo ""
echo "=== Phase 1 测试完成 ==="
echo "所有核心存储测试通过！"
