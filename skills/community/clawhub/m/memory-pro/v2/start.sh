#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# --- 環境變數設定 ---
export PATH="$HOME/.local/bin:$PATH"
export MEMORY_PRO_DATA_DIR="${MEMORY_PRO_DATA_DIR:-${OPENCLAW_WORKSPACE}/memory/}"
export MEMORY_PRO_CORE_FILES="${MEMORY_PRO_CORE_FILES:-MEMORY.md,SOUL.md,STATUS.md,AGENTS.md,USER.md}"
export MEMORY_PRO_PORT="${MEMORY_PRO_PORT:-8001}"
export MEMORY_PRO_INDEX_PATH="${MEMORY_PRO_INDEX_PATH:-memory.index}"
export MEMORY_PRO_SENTENCES_PATH="${MEMORY_PRO_SENTENCES_PATH:-sentences.txt}"
export MEMORY_PRO_META_PATH="${MEMORY_PRO_META_PATH:-memory_meta.jsonl}"
export MEMORY_PRO_BM25_PATH="${MEMORY_PRO_BM25_PATH:-bm25_corpus.pkl}"

# --- 啟動前檢查：Port 衝突 fail-fast ---
if command -v lsof >/dev/null 2>&1; then
  if lsof -iTCP:"$MEMORY_PRO_PORT" -sTCP:LISTEN -Pn >/dev/null 2>&1; then
    echo "❌ Port $MEMORY_PRO_PORT already in use. Aborting startup to avoid conflict."
    lsof -iTCP:"$MEMORY_PRO_PORT" -sTCP:LISTEN -Pn || true
    exit 1
  fi
fi

# --- 重建索引 ---
echo "🔄 Starting Memory Pro Service..."
echo "🔨 Rebuilding Index to ensure consistency..."
python3 build_index.py

# --- 啟動服務 ---
echo "🚀 Starting Uvicorn on port $MEMORY_PRO_PORT..."
exec python3 -m uvicorn main:app --host 127.0.0.1 --port "$MEMORY_PRO_PORT" --log-level info
