#!/bin/bash
# Ézekiel Holistic Memory System — Startup Initializer
# Ensures memory layers are initialized on system boot / OpenClaw start

LOG="/home/ezekiel/.openclaw/logs/holistic-memory-startup.log"
mkdir -p "$(dirname "$LOG")"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] === Ézekiel Holistic Memory Startup ===" >> $LOG

# 1. Ensure directories exist
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Creating directories..." >> $LOG
mkdir -p ~/.openclaw/memory-logs
mkdir -p ~/.openclaw/nebula
mkdir -p ~/.openclaw/workspace/memory/nebula_crystallized
echo "  ✅ Directories created" >> $LOG

# 2. Ensure Qdrant is running
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Checking Qdrant..." >> $LOG
if curl -s --max-time 3 http://localhost:6333/collections > /dev/null 2>&1; then
    echo "  ✅ Qdrant responding" >> $LOG
else
    echo "  ⚠️ Qdrant not responding (may start later)" >> $LOG
fi

# 3. Ensure Syncthing is running
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Checking Syncthing..." >> $LOG
if pgrep -x syncthing > /dev/null; then
    echo "  ✅ Syncthing running" >> $LOG
else
    echo "  ⚠️ Syncthing not running" >> $LOG
fi

# 4. Check OpenClaw gateway
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Checking OpenClaw..." >> $LOG
if curl -s --max-time 3 http://localhost:18790/health > /dev/null 2>&1; then
    echo "  ✅ OpenClaw gateway responding" >> $LOG
else
    echo "  ⚠️ OpenClaw gateway not responding" >> $LOG
fi

# 5. Run quick health check
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Running health check..." >> $LOG
python3 /home/ezekiel/.openclaw/skills/holistic-memory-system/scripts/ezekiel_health_check.py >> $LOG 2>&1

# 6. Apply any pending gravity decay
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Applying gravity decay..." >> $LOG
python3 /home/ezekiel/.openclaw/skills/holistic-memory-system/scripts/ezekiel_nebula.py decay >> $LOG 2>&1

# 7. Check for brillants needing crystallization
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Checking for crystallization..." >> $LOG
python3 /home/ezekiel/.openclaw/skills/holistic-memory-system/scripts/ezekiel_crystallizer.py status >> $LOG 2>&1

echo "[$(date '+%Y-%m-%d %H:%M:%S')] === Startup Complete ===" >> $LOG
echo "Startup log: $LOG"