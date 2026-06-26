#!/bin/bash
# NIMA Doctor — Diagnose installation issues
# Usage: ./scripts/doctor.sh
#
# Run this if NIMA isn't working. It checks everything and tells you
# exactly what's wrong and how to fix it.

echo "🩺 NIMA Doctor — Checking your installation..."
echo "================================================"
echo ""

NIMA_HOME="${NIMA_HOME:-$HOME/.nima}"
# Source user config to pick up NIMA_DB_BACKEND and other settings
[ -f "$NIMA_HOME/.env" ] && . "$NIMA_HOME/.env"
EXTENSIONS_DIR="${EXTENSIONS_DIR:-$HOME/.openclaw/extensions}"
CRON_FILE="${CRON_FILE:-$HOME/.openclaw/cron/jobs.json}"
ISSUES=0
WARNINGS=0

# ── Python ───────────────────────────────────────────────────────────────────
echo "🐍 Python"
if command -v python3 &> /dev/null; then
    PY_VERSION=$(python3 --version 2>&1)
    echo "   ✅ $PY_VERSION"
else
    echo "   ❌ Python 3 not found"
    echo "      FIX: Install Python 3.9+ (brew install python3 / apt install python3)"
    ISSUES=$((ISSUES + 1))
fi

python3 -c "import numpy" 2>/dev/null && echo "   ✅ numpy" || { echo "   ❌ numpy missing"; echo "      FIX: pip install numpy"; ISSUES=$((ISSUES + 1)); }
python3 -c "import real_ladybug; print(f'   ✅ real_ladybug {real_ladybug.version}')" 2>/dev/null || echo "   ℹ️  real_ladybug not installed (optional — needed for LadybugDB)"
echo ""

# ── Node.js ──────────────────────────────────────────────────────────────────
echo "📦 Node.js"
if command -v node &> /dev/null; then
    echo "   ✅ Node $(node -v)"
else
    echo "   ❌ Node.js not found"
    echo "      FIX: Install Node.js 18+ (brew install node / nvm install 22)"
    ISSUES=$((ISSUES + 1))
fi
echo ""

# ── Data Directory ───────────────────────────────────────────────────────────
echo "📂 Data Directory ($NIMA_HOME)"
for dir in "" /memory /affect /logs /precog_prep; do
    if [ -d "$NIMA_HOME$dir" ]; then
        echo "   ✅ $NIMA_HOME$dir exists"
    else
        if [ -z "$dir" ]; then
            echo "   ❌ $NIMA_HOME missing"
            echo "      FIX: mkdir -p $NIMA_HOME/memory $NIMA_HOME/affect $NIMA_HOME/logs"
            ISSUES=$((ISSUES + 1))
        else
            echo "   ⚠️  $NIMA_HOME$dir missing (will be created on first run)"
        fi
    fi
done
echo ""

# ── Databases ────────────────────────────────────────────────────────────────
echo "🗄️  Databases"

SQLITE_DB="$NIMA_HOME/memory/graph.sqlite"
if [ -f "$SQLITE_DB" ]; then
    SIZE=$(du -h "$SQLITE_DB" | cut -f1)
    echo "   ✅ SQLite: $SQLITE_DB ($SIZE)"

    TABLES=$(python3 -c "
import sqlite3
conn = sqlite3.connect('$SQLITE_DB')
tables = [r[0] for r in conn.execute(\"SELECT name FROM sqlite_master WHERE type='table'\").fetchall()]
print(' '.join(tables))
conn.close()
" 2>/dev/null)

    for t in memory_nodes memory_edges memory_turns memory_fts; do
        if echo "$TABLES" | grep -q "$t"; then
            echo "   ✅ Table: $t"
        else
            echo "   ❌ Table: $t MISSING"
            echo "      FIX: python3 scripts/init_db.py --verbose"
            ISSUES=$((ISSUES + 1))
        fi
    done

    MISSING_DREAM=0
    for t in nima_insights nima_patterns nima_dream_runs nima_suppressed_memories nima_pruner_runs nima_lucid_moments; do
        echo "$TABLES" | grep -q "$t" || MISSING_DREAM=$((MISSING_DREAM + 1))
    done
    if [ "$MISSING_DREAM" -gt 0 ]; then
        echo "   ⚠️  $MISSING_DREAM dream tables missing"
        echo "      FIX: python3 scripts/init_db.py --verbose"
        WARNINGS=$((WARNINGS + 1))
    else
        echo "   ✅ All 6 dream tables present"
    fi

    python3 -c "
import sqlite3
conn = sqlite3.connect('$SQLITE_DB')
try:
    nodes = conn.execute('SELECT count(*) FROM memory_nodes').fetchone()[0]
    embedded = conn.execute('SELECT count(*) FROM memory_nodes WHERE embedding IS NOT NULL').fetchone()[0]
    print(f'   📊 {nodes} memories, {embedded} with embeddings ({100*embedded//max(nodes,1)}%)')
except:
    pass
conn.close()
" 2>/dev/null

    # Check themes column (v3.3.3+)
    python3 -c "
import sqlite3
conn = sqlite3.connect('$SQLITE_DB')
cols = [c[1] for c in conn.execute('PRAGMA table_info(memory_nodes)').fetchall()]
if 'themes' in cols:
    print('   ✅ Schema: themes column present (v3.3.3+)')
else:
    print('   ❌ Schema: themes column MISSING')
    print('      FIX: python3 scripts/init_db.py --verbose')
conn.close()
" 2>/dev/null
else
    echo "   ⚠️  SQLite not found — run init_db.py to create it"
    echo "      FIX: python3 scripts/init_db.py --verbose"
    WARNINGS=$((WARNINGS + 1))
fi

LADYBUG_DB="${NIMA_LADYBUG_DB:-$NIMA_HOME/memory/ladybug.lbug}"
if [ "${NIMA_DB_BACKEND:-sqlite}" = "ladybug" ]; then
    if [ -f "$LADYBUG_DB" ]; then
        SIZE=$(du -h "$LADYBUG_DB" | cut -f1)
        echo "   ✅ LadybugDB: $LADYBUG_DB ($SIZE)"
        python3 -c "
import sys
import real_ladybug as lb
db = lb.Database('$LADYBUG_DB')
conn = lb.Connection(db)
try:
    conn.execute('LOAD VECTOR')
    print('   ✅ LOAD VECTOR: works (mutations safe)')
except Exception as e:
    print(f'   ⚠️  LOAD VECTOR failed: {e}')
nodes = list(conn.execute('MATCH (n:MemoryNode) RETURN count(n)'))[0][0]
print(f'   📊 {nodes} LadybugDB nodes')
# Schema drift check — verify critical columns exist
missing = []
for col in ['is_ghost', 'strength', 'decay_rate', 'dismissal_count', 'recall_count']:
    try:
        conn.execute(f'MATCH (n:MemoryNode) RETURN n.{col} LIMIT 0')
    except Exception:
        missing.append(col)
if missing:
    print(f'   ⚠️  LadybugDB schema drift — missing columns: {missing}')
    print('      FIX: python3 scripts/init_ladybug.py')
    sys.exit(2)
else:
    print('   ✅ LadybugDB schema: all required columns present')
" 2>/dev/null || echo "   ⚠️  Could not connect to LadybugDB"
if [ $? -eq 2 ]; then
    ISSUES=$((ISSUES + 1))
fi
    else
        echo "   ⚠️  NIMA_DB_BACKEND=ladybug but $LADYBUG_DB not found — run: python3 scripts/init_ladybug.py"
        ISSUES=$((ISSUES + 1))
    fi
elif [ -f "$LADYBUG_DB" ]; then
    echo "   ℹ️  LadybugDB file exists but NIMA_DB_BACKEND=sqlite — set NIMA_DB_BACKEND=ladybug to enable"
else
    echo "   ℹ️  LadybugDB not configured (set NIMA_DB_BACKEND=ladybug to enable)"
fi
echo ""

# ── Precog Database ──────────────────────────────────────────────────────────
echo "🔮 Precognitions"
PRECOG_DB="$NIMA_HOME/memory/precognitions.sqlite"
if [ -f "$PRECOG_DB" ]; then
    python3 -c "
import sqlite3, time
conn = sqlite3.connect('$PRECOG_DB')
try:
    total = conn.execute('SELECT count(*) FROM precognitions').fetchone()[0]
    active = conn.execute(\"SELECT count(*) FROM precognitions WHERE status IN ('active','pending')\").fetchone()[0]
    print(f'   ✅ precognitions.sqlite: {total} total, {active} active/pending')
except Exception as e:
    print(f'   ⚠️  Could not query precognitions: {e}')
conn.close()
" 2>/dev/null
else
    echo "   ⚠️  precognitions.sqlite not found (created after first mining run)"
fi

# Check precog prep cache
PREP_CACHE="$NIMA_HOME/precog_prep/latest.json"
if [ -f "$PREP_CACHE" ]; then
    python3 -c "
import json, time
with open('$PREP_CACHE') as f:
    p = json.load(f)
age_min = (int(time.time()) - p.get('timestamp', 0)) / 60
tier = p.get('winning_tier', '?')
model = p.get('recommended_model', '?').split('/')[-1]
cats = ','.join(p.get('categories', []))
if age_min > 240:
    print(f'   ⚠️  Prep cache stale ({age_min:.0f}m old, TTL=240m) — tier: {tier} → {model}')
else:
    print(f'   ✅ Prep cache fresh ({age_min:.0f}m old) — {cats} | {tier}→{model}')
" 2>/dev/null
else
    echo "   ⚠️  No precog prep cache found (cron hasn't run yet)"
fi
echo ""

# ── Hooks ────────────────────────────────────────────────────────────────────
echo "🔌 Hooks ($EXTENSIONS_DIR)"

for hook in nima-memory nima-recall-live nima-affect; do
    HOOK_DIR="$EXTENSIONS_DIR/$hook"
    if [ -d "$HOOK_DIR" ]; then
        case $hook in
            nima-memory)      REQUIRED="index.js openclaw.plugin.json" ;;
            nima-recall-live) REQUIRED="index.js openclaw.plugin.json" ;;
            nima-affect)      REQUIRED="index.js openclaw.plugin.json" ;;
        esac
        ALL_PRESENT=true
        for f in $REQUIRED; do
            [ -f "$HOOK_DIR/$f" ] || ALL_PRESENT=false
        done
        $ALL_PRESENT && echo "   ✅ $hook" || { echo "   ⚠️  $hook — some files missing"; echo "      FIX: cp -r openclaw_hooks/$hook $EXTENSIONS_DIR/"; WARNINGS=$((WARNINGS + 1)); }
    else
        echo "   ❌ $hook — not installed"
        echo "      FIX: cp -r openclaw_hooks/$hook $EXTENSIONS_DIR/"
        ISSUES=$((ISSUES + 1))
    fi
done
echo ""

# ── OpenClaw Config ──────────────────────────────────────────────────────────
echo "⚙️  OpenClaw Config"
CONFIG="$HOME/.openclaw/openclaw.json"
if [ -f "$CONFIG" ]; then
    python3 -c "
import json
with open('$CONFIG') as f:
    cfg = json.load(f)
plugins = cfg.get('plugins', {}).get('entries', {})
for h in ['nima-memory', 'nima-recall-live', 'nima-affect']:
    if h in plugins:
        enabled = plugins[h].get('enabled', True)
        print(f'   {\"✅\" if enabled else \"⚠️  disabled\"} {h} in config')
    else:
        print(f'   ❌ {h} NOT in config')
        print(f'      FIX: Add to plugins.entries in openclaw.json')
" 2>/dev/null
else
    echo "   ❌ Config not found at $CONFIG"
    ISSUES=$((ISSUES + 1))
fi
echo ""

# ── Cron Jobs ────────────────────────────────────────────────────────────────
echo "⏰ Cron Jobs"

if [ -f "$CRON_FILE" ]; then
    CRON_ISSUES=$(python3 << PYEOF
import json, time, sys

cron_file = "$CRON_FILE"

# All cron jobs NIMA needs to run fully.
# Grouped by category — CRITICAL jobs cause ❌ if missing; RECOMMENDED cause ⚠️.
required = {
    # ── Memory lifecycle (CRITICAL) ──────────────────────────────────────────
    "nima-memory-pruner": {
        "desc": "prunes low-value memories to keep DB lean",
        "schedule": "0 2 * * *",
        "example": "daily at 2AM",
        "critical": True,
        "docs": "INSTALL.md → 'Cron Jobs' section",
    },
    "nima-dream-consolidation": {
        "desc": "dream-consolidates memories into insights/patterns",
        "schedule": "0 2 * * *",
        "example": "daily at 2AM",
        "critical": True,
        "docs": "INSTALL.md → 'Cron Jobs' section",
        "alt_names": ["NIMA Dream Consolidation", "nima-dream", "lilu_dream_consolidation", "dream_consolidation"],
    },
    "nima-embedding-index": {
        "desc": "rebuilds FAISS/embedding index for fast semantic search",
        "schedule": "0 3 * * *",
        "example": "daily at 3AM",
        "critical": True,
        "docs": "INSTALL.md → 'Cron Jobs' section",
    },

    # ── Precognition (CRITICAL) ──────────────────────────────────────────────
    "nima-precognition-miner": {
        "desc": "mines memory patterns → generates precognitions",
        "schedule": "0 6 * * *",
        "example": "daily at 6AM",
        "critical": True,
        "docs": "INSTALL.md → 'Precognitive Actions' section",
    },
    "nima-precognitive-actions": {
        "desc": "pre-warms context cache for session injection",
        "schedule": "0 */4 * * *",
        "example": "every 4 hours",
        "critical": True,
        "docs": "INSTALL.md → 'Precognitive Actions' section",
    },

    # ── Quality / scoring (RECOMMENDED) ─────────────────────────────────────
    "nima-delta-scorer": {
        "desc": "scores memory deltas for importance/novelty",
        "schedule": "30 3 * * *",
        "example": "daily at 3:30AM",
        "critical": False,
        "docs": "INSTALL.md → 'Cron Jobs' section",
    },
    "nima-deduplication": {
        "desc": "deduplicates and ghost-marks near-duplicate memories",
        "schedule": "0 4 * * 0",
        "example": "weekly on Sunday 4AM",
        "critical": False,
        "docs": "INSTALL.md → 'Cron Jobs' section",
    },

    # ── Lucid moments (RECOMMENDED) ─────────────────────────────────────────
    "lucid-memory-moments": {
        "desc": "spontaneous memory surfacing during active hours",
        "schedule": "0 10,14,18,20 * * *",
        "example": "4x/day at 10AM/2PM/6PM/8PM",
        "critical": False,
        "docs": "INSTALL.md → 'Cron Jobs' section",
    },
}

try:
    with open(cron_file) as f:
        data = json.load(f)
    jobs = data.get("jobs", [])
except Exception as e:
    print(f"   ⚠️  Could not read {cron_file}: {e}")
    print("CRON_ISSUE_COUNT=5")
    sys.exit(0)

# Build lookup by name (and alt_names)
job_lookup = {}
for j in jobs:
    name = j.get("name", "")
    job_lookup[name] = j
    # Also index by normalized lowercase
    job_lookup[name.lower()] = j

issues = 0

for name, cfg in required.items():
    # Try exact name, alt_names, and lowercase variants
    candidates = [name] + cfg.get("alt_names", [])
    job = None
    for c in candidates:
        job = job_lookup.get(c) or job_lookup.get(c.lower())
        if job:
            break

    critical = cfg["critical"]
    icon_missing = "❌" if critical else "⚠️ "

    if job:
        state = job.get("state", {})
        last_run_ms = state.get("lastRunAtMs", 0)
        last_status = state.get("lastRunStatus", "unknown")
        enabled = job.get("enabled", True)
        schedule = job.get("schedule", {})
        expr = schedule.get("expr", "?")

        if not enabled:
            print(f"   ⚠️  {name} — DISABLED (schedule: {expr})")
            print(f"      FIX: Set enabled=true in {cron_file}")
            if critical:
                issues += 1
            continue

        if last_run_ms:
            age_h = (time.time() - last_run_ms / 1000) / 3600
            status_icon = "✅" if last_status in ("ok", "success") else "⚠️ "
            print(f"   {status_icon} {name} — last run {age_h:.1f}h ago ({last_status}), schedule: {expr}")
        else:
            print(f"   ✅ {name} — configured (never run yet), schedule: {expr}")
    else:
        tag = "CRITICAL" if critical else "recommended"
        print(f"   {icon_missing} {name} — NOT CONFIGURED ({tag})")
        print(f"      Purpose: {cfg['desc']}")
        print(f"      Suggested schedule: {cfg['example']} ({cfg['schedule']})")
        print(f"      FIX: See {cfg['docs']}")
        if critical:
            issues += 1

if issues == 0:
    print("   ✅ All critical cron jobs are configured")
print(f"CRON_ISSUE_COUNT={issues}")
PYEOF
)
    echo "$CRON_ISSUES" | grep -v 'CRON_ISSUE_COUNT='
    CRON_COUNT=$(echo "$CRON_ISSUES" | grep -o 'CRON_ISSUE_COUNT=[0-9]*' | cut -d= -f2)
    if [ -n "$CRON_COUNT" ] && [ "$CRON_COUNT" -gt 0 ] 2>/dev/null; then
        ISSUES=$((ISSUES + CRON_COUNT))
    fi

else
    echo "   ⚠️  Cron file not found at $CRON_FILE"
    echo "      (OpenClaw gateway may not have been started yet)"
    echo "   Required jobs (5 critical + 3 recommended):"
    echo "   ❌ nima-memory-pruner, nima-dream-consolidation, nima-embedding-index"
    echo "   ❌ nima-precognition-miner, nima-precognitive-actions"
    echo "   ⚠️  nima-delta-scorer, nima-deduplication, lucid-memory-moments"
    WARNINGS=$((WARNINGS + 1))
fi
echo ""

# ── Embedding Provider ───────────────────────────────────────────────────────
echo "🔤 Embeddings"
EMBEDDER="${NIMA_EMBEDDER:-local}"
echo "   Provider: $EMBEDDER"
case $EMBEDDER in
    voyage)
        [ -n "$VOYAGE_API_KEY" ] && echo "   ✅ VOYAGE_API_KEY is set" || { echo "   ❌ VOYAGE_API_KEY not set"; echo "      FIX: export VOYAGE_API_KEY=your-voyage-api-key"; ISSUES=$((ISSUES + 1)); }
        ;;
    openai)
        [ -n "$OPENAI_API_KEY" ] && echo "   ✅ OPENAI_API_KEY is set" || { echo "   ❌ OPENAI_API_KEY not set"; ISSUES=$((ISSUES + 1)); }
        ;;
    local)
        echo "   ✅ Using local embeddings (no API key needed)"
        ;;
    ollama)
        echo "   ✅ Using Ollama (${NIMA_OLLAMA_MODEL:-nomic-embed-text})"
        ;;
esac
echo ""

# ── Summary ──────────────────────────────────────────────────────────────────
echo "════════════════════════════════════════════════"
if [ "$ISSUES" -eq 0 ] && [ "$WARNINGS" -eq 0 ]; then
    echo "✅ All checks passed! NIMA is healthy."
elif [ "$ISSUES" -eq 0 ]; then
    echo "⚠️  $WARNINGS warning(s) found. Review above for details."
else
    echo "❌ $ISSUES issue(s), $WARNINGS warning(s) found. See FIX instructions above."
fi
echo ""
echo "Need help? https://github.com/lilubot/nima-core/issues"
