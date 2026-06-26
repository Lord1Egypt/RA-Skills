#!/bin/bash
# Medical Record Structurer - Auto-Evolution Daemon
# 每30分钟自动检查并进化

SKILL_PATH="/home/node/.openclaw/workspace/skills/medical-record-structurer"
LOG_FILE="$SKILL_PATH/auto-evolution.log"

echo "========================================" >> $LOG_FILE
echo "🧬 Auto-Evolution Started: $(date)" >> $LOG_FILE
echo "========================================" >> $LOG_FILE

while true; do
    echo "" >> $LOG_FILE
    echo "[$(date)] Running self-evolution..." >> $LOG_FILE
    
    cd $SKILL_PATH
    python3 scripts/self_evolve.py >> $LOG_FILE 2>&1
    
    echo "[$(date)] Evolution cycle complete. Sleeping 30 minutes..." >> $LOG_FILE
    
    # 每30分钟进化一次
    sleep 1800
done
