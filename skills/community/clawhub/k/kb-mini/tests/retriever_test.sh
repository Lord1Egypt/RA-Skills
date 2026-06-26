#!/bin/bash
# retriever.sh TDD 测试
# Phase 2: 时间衰减 + 分层加载

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RETRIEVER="$SCRIPT_DIR/../scripts/retriever.sh"
STORAGE="$SCRIPT_DIR/../scripts/storage.sh"

echo "=== Phase 2: retriever.sh 测试 ==="

# ============================================
# TEST 1: 时间衰减
# ============================================
echo ""
echo "TEST 1: 时间衰减"

TEST_DB="/tmp/kb_retriever_t1_$$.db"
export KNOWLEDGE_DB="$TEST_DB"
rm -f "$TEST_DB"

"$STORAGE" init
"$STORAGE" store --title "Recent Entry" --content "Content from today" --source "manual" --topic-key "recent-entry"
"$STORAGE" store --title "Old Entry" --content "Content from old day" --source "manual" --topic-key "old-entry"
sqlite3 "$TEST_DB" "UPDATE entries SET created_at = datetime('now', '-30 days') WHERE topic_key = 'old-entry';"

result=$("$RETRIEVER" retrieve --query "Content" --limit 2 2>&1)
echo "Result: $result"

if echo "$result" | grep -q "recent-entry" && echo "$result" | grep -q "old-entry"; then
    echo "✅ TEST 1 PASSED"
else
    echo "❌ TEST 1 FAILED"
fi

rm -f "$TEST_DB"

# ============================================
# TEST 2: 分层加载 L0
# ============================================
echo ""
echo "TEST 2: 分层加载 L0"

TEST_DB="/tmp/kb_retriever_t2_$$.db"
export KNOWLEDGE_DB="$TEST_DB"
rm -f "$TEST_DB"

"$STORAGE" init
LONG_CONTENT="This is a very long content. " && for i in {1..50}; do LONG_CONTENT="$LONG_CONTENT Repeated content $i. "; done
"$STORAGE" store --title "Long Entry" --content "$LONG_CONTENT" --source "manual" --topic-key "long-entry"

result=$("$RETRIEVER" retrieve --query "Repeated" --level 0 2>&1)
echo "Result length: $(echo "$result" | wc -c)"

if echo "$result" | grep -q "long-entry"; then
    echo "✅ TEST 2 PASSED"
else
    echo "❌ TEST 2 FAILED"
fi

rm -f "$TEST_DB"

# ============================================
# TEST 3: 分层加载 L2
# ============================================
echo ""
echo "TEST 3: 分层加载 L2"

TEST_DB="/tmp/kb_retriever_t3_$$.db"
export KNOWLEDGE_DB="$TEST_DB"
rm -f "$TEST_DB"

"$STORAGE" init
"$STORAGE" store --title "Test L2" --content "Full content here" --source "manual" --topic-key "l2-entry"

result=$("$RETRIEVER" retrieve --query "Full content" --level 2 2>&1)
echo "Result: $result"

if echo "$result" | grep -q "Full content here"; then
    echo "✅ TEST 3 PASSED"
else
    echo "❌ TEST 3 FAILED"
fi

rm -f "$TEST_DB"

# ============================================
# TEST 4: 来源过滤
# ============================================
echo ""
echo "TEST 4: 来源过滤"

TEST_DB="/tmp/kb_retriever_t4_$$.db"
export KNOWLEDGE_DB="$TEST_DB"
rm -f "$TEST_DB"

"$STORAGE" init
"$STORAGE" store --title "GitHub Item" --content "From github source" --source "github" --topic-key "github-item"
"$STORAGE" store --title "HF Item" --content "From huggingface source" --source "huggingface" --topic-key "hf-item"

result=$("$RETRIEVER" retrieve --query "source" --limit 1 --boost-source "github" 2>&1)
echo "Result: $result"

if echo "$result" | grep -q "github-item"; then
    echo "✅ TEST 4 PASSED"
else
    echo "❌ TEST 4 FAILED"
fi

rm -f "$TEST_DB"

# ============================================
# TEST 5: recall
# ============================================
echo ""
echo "TEST 5: recall"

TEST_DB="/tmp/kb_retriever_t5_$$.db"
export KNOWLEDGE_DB="$TEST_DB"
rm -f "$TEST_DB"

"$STORAGE" init
"$STORAGE" store --title "OpenClaw Hooks" --content "Configure hooks for agent" --source "manual" --topic-key "hooks-config"
"$STORAGE" store --title "SQLite FTS5" --content "Full text search" --source "manual" --topic-key "sqlite-fts5"

# recall uses context as search query, so use a term that matches the content
result=$("$RETRIEVER" recall --context "Configure hooks for agent" --limit 2 2>&1)
echo "Result: $result"

if echo "$result" | grep -q "OpenClaw Hooks"; then
    echo "✅ TEST 5 PASSED"
else
    echo "❌ TEST 5 FAILED"
fi

rm -f "$TEST_DB"

# ============================================
# TEST 6: capture
# ============================================
echo ""
echo "TEST 6: capture"

TEST_DB="/tmp/kb_retriever_t6_$$.db"
export KNOWLEDGE_DB="$TEST_DB"
rm -f "$TEST_DB"

result=$("$RETRIEVER" capture --turn "请记住这个配置：api_key=12345" 2>&1)
echo "Result: $result"

if echo "$result" | grep -q '"captured": true'; then
    echo "✅ TEST 6 PASSED"
else
    echo "❌ TEST 6 FAILED"
fi

echo ""
echo "=== Phase 2 测试完成 ==="
