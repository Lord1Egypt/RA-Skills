#!/bin/bash
# lifecycle.sh TDD 测试
# Phase 4: 生命周期管理 + DAG 摘要

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIFECYCLE="$SCRIPT_DIR/../scripts/lifecycle.sh"
STORAGE="$SCRIPT_DIR/../scripts/storage.sh"

echo "=== Phase 4: lifecycle.sh 测试 ==="

# ============================================
# TEST 1: 标记 stale 状态
# ============================================
echo ""
echo "TEST 1: 标记 stale 状态"

TEST_DB="/tmp/kb_lifecycle_t1_$$.db"
export KNOWLEDGE_DB="$TEST_DB"
rm -f "$TEST_DB"

"$STORAGE" init
"$STORAGE" store --title "Old Entry" --content "Old content" --source "manual" --topic-key "old-entry"

# 修改为 91 天前（确保严格小于 90 天阈值）
sqlite3 "$TEST_DB" "UPDATE entries SET updated_at = datetime('now', '-91 days') WHERE topic_key = 'old-entry';"

# 运行 lifecycle mark-stale
result=$("$LIFECYCLE" mark-stale 2>&1)
echo "Result: $result"

# 检查状态
status=$(sqlite3 "$TEST_DB" "SELECT status FROM entries WHERE topic_key = 'old-entry';")
if [[ "$status" == "stale" ]]; then
    echo "✅ TEST 1 PASSED"
else
    echo "❌ TEST 1 FAILED: status=$status"
fi

rm -f "$TEST_DB"

# ============================================
# TEST 2: 归档过期记录
# ============================================
echo ""
echo "TEST 2: 归档过期记录"

TEST_DB="/tmp/kb_lifecycle_t2_$$.db"
export KNOWLEDGE_DB="$TEST_DB"
rm -f "$TEST_DB"

"$STORAGE" init
"$STORAGE" store --title "Archived Entry" --content "To be archived" --source "manual" --topic-key "archived-entry"

# 设置为 stale + 365 天前
sqlite3 "$TEST_DB" "UPDATE entries SET updated_at = datetime('now', '-400 days'), status = 'stale' WHERE topic_key = 'archived-entry';"

# 运行 archive
result=$("$LIFECYCLE" archive 2>&1)
echo "Result: $result"

# 检查状态
status=$(sqlite3 "$TEST_DB" "SELECT status FROM entries WHERE topic_key = 'archived-entry';")
if [[ "$status" == "archived" ]]; then
    echo "✅ TEST 2 PASSED"
else
    echo "❌ TEST 2 FAILED: status=$status"
fi

rm -f "$TEST_DB"

# ============================================
# TEST 3: 清理已归档记录
# ============================================
echo ""
echo "TEST 3: 清理已归档记录"

TEST_DB="/tmp/kb_lifecycle_t3_$$.db"
export KNOWLEDGE_DB="$TEST_DB"
rm -f "$TEST_DB"

"$STORAGE" init
"$STORAGE" store --title "To Delete" --content "To be deleted" --source "manual" --topic-key "delete-entry"

# 设置为 archived，archived_at 设置为 400 天前
sqlite3 "$TEST_DB" "
    UPDATE entries 
    SET status = 'archived', 
        archived_at = datetime('now', '-400 days'),
        updated_at = datetime('now', '-400 days')
    WHERE topic_key = 'delete-entry';
"

# 验证设置
echo "Before cleanup:"
sqlite3 "$TEST_DB" "SELECT status, archived_at FROM entries WHERE topic_key = 'delete-entry';"

# 运行 cleanup（默认 30 天阈值）
result=$("$LIFECYCLE" cleanup 2>&1)
echo "Result: $result"

# 检查是否删除
count=$(sqlite3 "$TEST_DB" "SELECT COUNT(*) FROM entries WHERE topic_key = 'delete-entry';" 2>/dev/null || echo "0")
if [[ "$count" == "0" ]]; then
    echo "✅ TEST 3 PASSED"
else
    echo "❌ TEST 3 FAILED: count=$count"
fi

rm -f "$TEST_DB"

# ============================================
# TEST 4: 生成摘要 (DAG d2 层)
# ============================================
echo ""
echo "TEST 4: 生成摘要"

TEST_DB="/tmp/kb_lifecycle_t4_$$.db"
export KNOWLEDGE_DB="$TEST_DB"
rm -f "$TEST_DB"

"$STORAGE" init
"$STORAGE" store --title "Long Content Entry" --content "This is a very long content that should be summarized. " && for i in {1..20}; do echo -n "Repeated information $i. "; done && echo "" > /dev/null

"$STORAGE" store --title "Long Content Entry" --content " More content to make it longer. Additional details. More text." --source "manual" --topic-key "long-content-entry"

# 运行 summarize
result=$("$LIFECYCLE" summarize --topic-key "long-content-entry" 2>&1)
echo "Result: $result"

if echo "$result" | grep -q "summary" || echo "$result" | grep -q "Summary"; then
    echo "✅ TEST 4 PASSED"
else
    echo "❌ TEST 4 FAILED"
fi

rm -f "$TEST_DB"

# ============================================
# TEST 5: 状态统计
# ============================================
echo ""
echo "TEST 5: 状态统计"

TEST_DB="/tmp/kb_lifecycle_t5_$$.db"
export KNOWLEDGE_DB="$TEST_DB"
rm -f "$TEST_DB"

"$STORAGE" init
"$STORAGE" store --title "Active 1" --content "Active" --source "manual" --topic-key "active-1"
"$STORAGE" store --title "Active 2" --content "Active" --source "manual" --topic-key "active-2"

# 标记一个 stale
sqlite3 "$TEST_DB" "UPDATE entries SET status = 'stale' WHERE topic_key = 'active-1';"

# 运行 stats
result=$("$LIFECYCLE" stats 2>&1)
echo "Result: $result"

if echo "$result" | grep -q "active" && echo "$result" | grep -q "stale"; then
    echo "✅ TEST 5 PASSED"
else
    echo "❌ TEST 5 FAILED"
fi

rm -f "$TEST_DB"

echo ""
echo "=== Phase 4 测试完成 ==="
