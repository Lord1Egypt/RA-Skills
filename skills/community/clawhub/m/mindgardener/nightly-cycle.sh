#!/bin/bash
# MindGardener Nightly Cycle — "Sleep cycle" for agent memory
# Runs: extract → surprise → consolidate → decay → beliefs drift
# Schedule: 03:00 daily via cron

set -euo pipefail

GARDEN="python3 -m engram.cli --config /root/clawd/projects/mindgardener/garden.yaml"
LOG="/root/clawd/memory/mindgardener-nightly.log"
DATE=$(date -d "yesterday" +%Y-%m-%d 2>/dev/null || date -v-1d +%Y-%m-%d)

cd /root/clawd

echo "=== MindGardener Nightly Cycle — $(date -Iseconds) ===" >> "$LOG"

# Step 1: Extract entities from yesterday's daily log
echo "Step 1: Extract ($DATE)" >> "$LOG"
$GARDEN extract -d "$DATE" >> "$LOG" 2>&1 || echo "  Extract: no file or error" >> "$LOG"

# Step 2: Score surprise (prediction error)
echo "Step 2: Surprise scoring ($DATE)" >> "$LOG"
$GARDEN surprise -d "$DATE" >> "$LOG" 2>&1 || echo "  Surprise: error" >> "$LOG"

# Step 3: Consolidate high-surprise items to MEMORY.md
echo "Step 3: Consolidate" >> "$LOG"
$GARDEN consolidate >> "$LOG" 2>&1 || echo "  Consolidate: error" >> "$LOG"

# Step 4: Decay — archive stale entities
echo "Step 4: Decay" >> "$LOG"
$GARDEN prune >> "$LOG" 2>&1 || echo "  Prune: error" >> "$LOG"

# Step 5: Beliefs drift detection + apply
echo "Step 5: Beliefs drift ($DATE)" >> "$LOG"
$GARDEN beliefs --drift --apply -d "$DATE" >> "$LOG" 2>&1 || echo "  Beliefs: error" >> "$LOG"

# Step 6: Stats
echo "Step 6: Stats" >> "$LOG"
$GARDEN stats >> "$LOG" 2>&1

# Step 7: Rebuild FTS5 index + generate RECALL-CONTEXT.md
echo "Step 7: Auto-recall (FTS5 index + context)" >> "$LOG"
python3 /root/clawd/tools/auto-recall.py --index >> "$LOG" 2>&1 || echo "  FTS5 index: error" >> "$LOG"
python3 /root/clawd/tools/auto-recall.py >> "$LOG" 2>&1 || echo "  Recall context: error" >> "$LOG"

echo "=== Cycle complete ===" >> "$LOG"
echo "" >> "$LOG"
