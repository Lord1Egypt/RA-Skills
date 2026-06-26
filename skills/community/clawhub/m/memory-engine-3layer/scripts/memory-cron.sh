#!/bin/bash
# memory-cron.sh — System-level memory maintenance (runs independently of AI)
# Install: (crontab -l; echo "0 * * * * /path/to/memory-cron.sh") | crontab -
# Recommended: every 1h (was 6h pre-v4.0). Watcher handles real-time reset detection.

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG="$WORKSPACE/.memory/cron.log"

# Resolve timezone: OPENCLAW_TZ > openclaw.json > TZ > /etc/timezone > /etc/localtime > UTC
if [ -z "$TZ" ]; then
  OPENCLAW_CFG="$WORKSPACE/../openclaw.json"
  if [ -f "$OPENCLAW_CFG" ]; then
    DETECTED_TZ=$(node -e "try{const c=require('$OPENCLAW_CFG');console.log(c?.agents?.defaults?.userTimezone||'')}catch{}" 2>/dev/null)
    [ -n "$DETECTED_TZ" ] && export TZ="$DETECTED_TZ"
  fi
fi
export TZ="${TZ:-$(cat /etc/timezone 2>/dev/null || readlink /etc/localtime 2>/dev/null | sed 's|.*/zoneinfo/||' || echo UTC)}"

mkdir -p "$(dirname "$LOG")"

# Rotate log if > 100KB
[ -f "$LOG" ] && [ "$(wc -c < "$LOG" 2>/dev/null || echo 0)" -gt 102400 ] && mv "$LOG" "$LOG.old"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] cron started" >> "$LOG"

# 1. Rebuild index (incremental, skips unchanged files)
RESULT=$(node "$SCRIPT_DIR/memory-index.js" --workspace "$WORKSPACE" 2>&1)
echo "[$(date '+%Y-%m-%d %H:%M:%S')] index: $RESULT" >> "$LOG"

# 2. Health check
HEALTH=$(node "$SCRIPT_DIR/memory-write.js" --workspace "$WORKSPACE" --status 2>&1)
echo "[$(date '+%Y-%m-%d %H:%M:%S')] health: $HEALTH" >> "$LOG"

# 3. Auto-create daily log if missing
HAS_TODAY=$(echo "$HEALTH" | grep -o '"hasTodayLog": *[a-z]*' | grep -o '[a-z]*$')
if [ "$HAS_TODAY" = "false" ]; then
    node "$SCRIPT_DIR/memory-write.js" --workspace "$WORKSPACE" --today "[auto] No activity logged today" --tag system
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] auto-created daily log" >> "$LOG"
fi

# 4. Auto-extract from reset sessions (scan unprocessed sessions)
if [ -f "$SCRIPT_DIR/memory-auto-extract.js" ]; then
    EXTRACT=$(node "$SCRIPT_DIR/memory-auto-extract.js" --workspace "$WORKSPACE" --scan 2>&1)
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] auto-extract(reset): $EXTRACT" >> "$LOG"
    # P1: Also extract incrementally from active sessions
    ACTIVE_EXTRACT=$(node "$SCRIPT_DIR/memory-auto-extract.js" --workspace "$WORKSPACE" --active 2>&1)
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] auto-extract(active): $ACTIVE_EXTRACT" >> "$LOG"
fi

# 5a. MEMORY.md integrity check — detect accidental wipe + auto-restore from snapshot/git
MEMORY_FILE="$WORKSPACE/MEMORY.md"
SNAPSHOT_DIR="$WORKSPACE/memory/snapshots"
if [ -f "$MEMORY_FILE" ]; then
    CORE_SIZE=$(wc -c < "$MEMORY_FILE" 2>/dev/null || echo 0)
    # If MEMORY.md is suspiciously small (<100 chars) but snapshots exist, it was likely wiped
    if [ "$CORE_SIZE" -lt 100 ] && [ -d "$SNAPSHOT_DIR" ]; then
        LATEST_SNAP=$(ls -t "$SNAPSHOT_DIR"/MEMORY-*.md 2>/dev/null | head -1)
        if [ -n "$LATEST_SNAP" ]; then
            SNAP_SIZE=$(wc -c < "$LATEST_SNAP" 2>/dev/null || echo 0)
            if [ "$SNAP_SIZE" -gt "$CORE_SIZE" ]; then
                cp "$LATEST_SNAP" "$MEMORY_FILE"
                echo "[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️ MEMORY.md was ${CORE_SIZE}B, restored from snapshot (${SNAP_SIZE}B): $LATEST_SNAP" >> "$LOG"
                node "$SCRIPT_DIR/memory-write.js" --workspace "$WORKSPACE" --today "[auto-restore] MEMORY.md restored from snapshot — was wiped to ${CORE_SIZE}B" --tag warning
            fi
        fi
    fi
    # Also take periodic snapshot (every 6h = when minute < 2 and hour divisible by 6)
    HOUR=$(date '+%H')
    if [ "$((HOUR % 6))" = "0" ]; then
        node "$SCRIPT_DIR/memory-write.js" --workspace "$WORKSPACE" --snapshot 2>&1 | while read line; do echo "[$(date '+%Y-%m-%d %H:%M:%S')] snapshot: $line" >> "$LOG"; done
    fi
elif [ -d "$SNAPSHOT_DIR" ]; then
    # MEMORY.md completely missing, restore from latest snapshot
    LATEST_SNAP=$(ls -t "$SNAPSHOT_DIR"/MEMORY-*.md 2>/dev/null | head -1)
    if [ -n "$LATEST_SNAP" ]; then
        cp "$LATEST_SNAP" "$MEMORY_FILE"
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️ MEMORY.md was MISSING, restored from snapshot: $LATEST_SNAP" >> "$LOG"
    fi
fi

# 5b. Gap alerting — if >2 consecutive days with no log, write warning
GAP_COUNT=$(echo "$HEALTH" | grep -o '"gapCount": *[0-9]*' | grep -o '[0-9]*$')
if [ -n "$GAP_COUNT" ] && [ "$GAP_COUNT" -gt 2 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️ Memory gap alert: $GAP_COUNT days missing in last 14 days" >> "$LOG"
fi

# 5c. Auto-compact files older than 60 days (monthly, on the 1st)
if [ "$(date '+%d')" = "01" ]; then
    COMPACT=$(node "$SCRIPT_DIR/memory-compact.js" --workspace "$WORKSPACE" --older-than 60 2>&1)
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] compact: $COMPACT" >> "$LOG"
fi

# 6. Session size warning (write to daily log if > 4MB)
SESS_DIR="$HOME/.openclaw/agents/main/sessions"
if [ -d "$SESS_DIR" ]; then
    ACTIVE=$(find "$SESS_DIR" -name "*.jsonl" ! -name "*.reset.*" ! -name "*.deleted.*" ! -name "*.lock" -printf '%s %p\n' 2>/dev/null | sort -rn | head -1)
    if [ -n "$ACTIVE" ]; then
        SIZE_BYTES=$(echo "$ACTIVE" | awk '{print $1}')
        SIZE_MB=$(echo "$SIZE_BYTES" | awk '{printf "%.1f", $1/1048576}')
        if [ "$(echo "$SIZE_MB > 8" | bc -l 2>/dev/null || echo 0)" = "1" ]; then
            node "$SCRIPT_DIR/memory-write.js" --workspace "$WORKSPACE" --today "[warning] 会话已达 ${SIZE_MB}MB，即将触发 reset！请主动做摘要压缩" --tag warning
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] WARNING: session ${SIZE_MB}MB" >> "$LOG"
        elif [ "$(echo "$SIZE_MB > 4" | bc -l 2>/dev/null || echo 0)" = "1" ]; then
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] session size: ${SIZE_MB}MB" >> "$LOG"
        fi
    fi
fi

# 5. Verify index is in sync (catches memory-flush writes that didn't trigger reindex)
SYNC_CHECK=$(node -e "
const fs=require('fs'),p=require('path'),c=require('crypto');
const ws='$WORKSPACE',mdir=p.join(ws,'memory'),db_path=p.join(ws,'.memory','index.sqlite');
if(!fs.existsSync(db_path)){console.log('no_index');process.exit(0);}
const GM=require('child_process').execSync('npm root -g',{encoding:'utf8'}).trim();
const D=require(p.join(GM,'better-sqlite3'));
const db=new D(db_path,{readonly:true});
const dbFiles=db.prepare('SELECT path,hash FROM files').all();
const dbMap=new Map(dbFiles.map(f=>[f.path,f.hash]));
let stale=0;
const hash=c=>require('crypto').createHash('sha256').update(c).digest('hex').slice(0,16);
if(fs.existsSync(p.join(ws,'MEMORY.md'))){const h=hash(fs.readFileSync(p.join(ws,'MEMORY.md'),'utf8'));if(dbMap.get('MEMORY.md')!==h)stale++;}
if(fs.existsSync(mdir))fs.readdirSync(mdir).filter(f=>f.endsWith('.md')).forEach(f=>{const h=hash(fs.readFileSync(p.join(mdir,f),'utf8'));if(dbMap.get('memory/'+f)!==h)stale++;});
console.log(stale?'stale:'+stale:'ok');
db.close();
" 2>&1)
if echo "$SYNC_CHECK" | grep -q "stale"; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] index stale ($SYNC_CHECK), forcing reindex" >> "$LOG"
    node "$SCRIPT_DIR/memory-index.js" --workspace "$WORKSPACE" --force >> "$LOG" 2>&1
fi

# 7. Ensure watcher is running (P0: session reset hook)
WATCHER_PID_FILE="$WORKSPACE/.memory/watcher.pid"
WATCHER_ALIVE=false
if [ -f "$WATCHER_PID_FILE" ]; then
  WATCHER_PID=$(cat "$WATCHER_PID_FILE")
  if kill -0 "$WATCHER_PID" 2>/dev/null; then
    WATCHER_ALIVE=true
  fi
fi
if ! $WATCHER_ALIVE; then
  nohup bash "$SCRIPT_DIR/memory-watcher.sh" >> "$WORKSPACE/.memory/watcher.log" 2>&1 &
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] watcher restarted (PID: $!)" >> "$LOG"
else
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] watcher alive (PID: $WATCHER_PID)" >> "$LOG"
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] cron completed" >> "$LOG"

# 8. Auto-backup to GitHub (if git remote configured)
BACKUP_SCRIPT="$DIR/memory-backup.sh"
if [ -f "$BACKUP_SCRIPT" ] && [ -d "$WORKSPACE/.git" ]; then
  log "starting backup"
  bash "$BACKUP_SCRIPT" >> "$LOG" 2>&1 || log "backup failed"
fi
