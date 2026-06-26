#!/usr/bin/env bash
# index-batch-ram.sh — Two-phase indexing to avoid OOM on low-RAM systems.
# Phase 1: Text files only (md, txt, tex) — 25 files per round
# Phase 2: PDF files up to 25MB — 1 file per round
set -euo pipefail

VENV_PY="$HOME/.local/share/local-rag/venv/bin/python"
SCRIPT="$HOME/.openclaw/workspace/skills/lookupmark-local-rag/scripts/index.py"

MAX_ROUNDS=50

echo "=========================================="
echo "FASE 1: Indicizzazione file testuali"
echo "=========================================="

for i in $(seq 1 $MAX_ROUNDS); do
    echo "=== Phase 1 — Round $i/$MAX_ROUNDS (max 25 files) ==="
    OUTPUT=$($VENV_PY "$SCRIPT" --text-only --max-files 25 2>&1) || true
    echo "$OUTPUT"
    
    if echo "$OUTPUT" | grep -q "Nuovi indicizzati:       0" && echo "$OUTPUT" | grep -q "Aggiornati:              0"; then
        echo "=== Phase 1 complete. All text files indexed. ==="
        break
    fi
    
    echo "--- Round $i complete, waiting 5s ---"
    sleep 5
done

echo ""
echo "=========================================="
echo "FASE 2: Indicizzazione PDF (1 per volta)"
echo "=========================================="

for i in $(seq 1 $MAX_ROUNDS); do
    echo "=== Phase 2 — Round $i/$MAX_ROUNDS (1 PDF) ==="
    OUTPUT=$($VENV_PY "$SCRIPT" --pdf-only --max-files 1 2>&1) || true
    echo "$OUTPUT"
    
    if echo "$OUTPUT" | grep -q "Nuovi indicizzati:       0" && echo "$OUTPUT" | grep -q "Aggiornati:              0"; then
        echo "=== Phase 2 complete. All PDFs indexed. ==="
        break
    fi
    
    echo "--- Round $i complete, waiting 5s ---"
    sleep 5
done

echo ""
echo "=========================================="
echo "INDICIZZAZIONE COMPLETATA"
echo "=========================================="
