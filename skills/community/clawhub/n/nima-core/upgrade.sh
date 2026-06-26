#!/bin/bash
# NIMA Core Upgrade Script — Safe upgrade for existing installations
# Usage: ./upgrade.sh [--force] [--dry-run] [--skip-hooks] [--skip-db]
#
# This script is designed to NEVER break an existing setup:
#   1. Detects what you have installed
#   2. Backs up everything before touching it
#   3. Only adds new files — never overwrites customized ones
#   4. Database changes are additive only (CREATE IF NOT EXISTS)
#   5. Shows you exactly what will change before doing it

set -e

# ── Config ────────────────────────────────────────────────────────────────────
NIMA_HOME="${NIMA_HOME:-$HOME/.nima}"
# Source user config to detect existing backend choice
# Safely read NIMA_DB_BACKEND from .env (avoid sourcing arbitrary shell code)
if [ -f "$NIMA_HOME/.env" ]; then
    _env_val=$(grep -E "^NIMA_DB_BACKEND=" "$NIMA_HOME/.env" | tail -1 | cut -d= -f2-)
    [ -n "$_env_val" ] && NIMA_DB_BACKEND="$_env_val"
fi
EXTENSIONS_DIR="$HOME/.openclaw/extensions"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKUP_DIR="$NIMA_HOME/backups/upgrade_$(date +%Y%m%d_%H%M%S)"
VERSION="3.3.3"
DRY_RUN=false
FORCE=false
SKIP_HOOKS=false
SKIP_DB=false
UPDATE_ONLY=false
BRANCH="main"

for arg in "$@"; do
    case $arg in
        --force)     FORCE=true ;;
        --dry-run)   DRY_RUN=true ;;
        --skip-hooks) SKIP_HOOKS=true ;;
        --skip-db)   SKIP_DB=true ;;
        --update)    UPDATE_ONLY=true ;;
        --branch)    shift; BRANCH="$1" ;;
        --help|-h)
            echo "Usage: ./upgrade.sh [--force] [--dry-run] [--skip-hooks] [--skip-db]"
            echo ""
            echo "  --dry-run     Show what would change without making changes"
            echo "  --force       Overwrite customized files (backs up first)"
            echo "  --skip-hooks  Don't touch hook files"
            echo "  --skip-db     Don't modify database schema"
            echo "  --update      Pull latest code then run full upgrade"
            echo "  --branch BR   Branch to pull when using --update (default: main)"
            exit 0
            ;;
    esac
done

# ── Helper: write/update a key in ~/.nima/.env ────────────────────────────────
_set_env_var() {
    local key="$1" val="$2" envfile="$3"
    mkdir -p "$(dirname "$envfile")"
    touch "$envfile"
    if grep -q "^${key}=" "$envfile"; then
        sed -i.bak "s|^${key}=.*|${key}=${val}|" "$envfile" && rm -f "${envfile}.bak"
    else
        echo "${key}=${val}" >> "$envfile"
    fi
}


echo "🧠 NIMA Core Upgrade → v$VERSION"
echo "================================="
if $DRY_RUN; then echo "🔍 DRY RUN — no changes will be made"; fi
echo ""

# ── Step 1: Detect Current Installation ──────────────────────────────────────
echo "📋 Step 1: Detecting current installation..."

SQLITE_DB="$NIMA_HOME/memory/graph.sqlite"
LADYBUG_DB="$NIMA_HOME/memory/ladybug.lbug"
HAS_SQLITE=false
HAS_LADYBUG=false
HAS_HOOKS=false
INSTALLED_HOOKS=""

if [ -f "$SQLITE_DB" ]; then
    HAS_SQLITE=true
    SQLITE_SIZE=$(du -h "$SQLITE_DB" 2>/dev/null | cut -f1)
    echo "   ✅ SQLite database: $SQLITE_DB ($SQLITE_SIZE)"
fi

if [ -f "$LADYBUG_DB" ]; then
    HAS_LADYBUG=true
    LADYBUG_SIZE=$(du -h "$LADYBUG_DB" 2>/dev/null | cut -f1)
    echo "   ✅ LadybugDB: $LADYBUG_DB ($LADYBUG_SIZE)"
fi

for hook in nima-memory nima-recall-live nima-affect; do
    if [ -d "$EXTENSIONS_DIR/$hook" ]; then
        HAS_HOOKS=true
        INSTALLED_HOOKS="$INSTALLED_HOOKS $hook"
        echo "   ✅ Hook: $hook"
    fi
done

if ! $HAS_SQLITE && ! $HAS_LADYBUG && ! $HAS_HOOKS; then
    echo "   ⚠️  No existing installation detected."
    echo "   Run ./install.sh for a fresh install instead."
    exit 0
fi
echo ""

# ── Step 2: Check for Customizations ─────────────────────────────────────────
echo "📋 Step 2: Checking for customizations..."

CUSTOMIZED_FILES=""
CUSTOM_COUNT=0

for hook in nima-memory nima-recall-live nima-affect; do
    INSTALLED="$EXTENSIONS_DIR/$hook"
    SOURCE="$SCRIPT_DIR/openclaw_hooks/$hook"
    
    if [ ! -d "$INSTALLED" ] || [ ! -d "$SOURCE" ]; then
        continue
    fi
    
    # Compare each file
    for src_file in $(find "$SOURCE" -type f \( -name "*.js" -o -name "*.py" -o -name "*.json" \) | grep -v __pycache__ | grep -v node_modules); do
        rel_path="${src_file#$SOURCE/}"
        inst_file="$INSTALLED/$rel_path"
        
        if [ -f "$inst_file" ]; then
            if ! diff -q "$src_file" "$inst_file" > /dev/null 2>&1; then
                CUSTOMIZED_FILES="$CUSTOMIZED_FILES\n   ⚠️  $hook/$rel_path (modified)"
                CUSTOM_COUNT=$((CUSTOM_COUNT + 1))
            fi
        fi
    done
done

if [ $CUSTOM_COUNT -gt 0 ]; then
    echo -e "$CUSTOMIZED_FILES"
    echo ""
    echo "   Found $CUSTOM_COUNT customized file(s)."
    if ! $FORCE; then
        echo "   These will NOT be overwritten. Use --force to replace (backup created first)."
    else
        echo "   --force: These WILL be replaced (backup created first)."
    fi
else
    echo "   No customizations detected — safe to update all files."
fi
echo ""

# ── Step 3: Backup ───────────────────────────────────────────────────────────
echo "📋 Step 3: Creating backup..."

if ! $DRY_RUN; then
    mkdir -p "$BACKUP_DIR"
    
    # Backup hooks
    for hook in $INSTALLED_HOOKS; do
        if [ -d "$EXTENSIONS_DIR/$hook" ]; then
            cp -r "$EXTENSIONS_DIR/$hook" "$BACKUP_DIR/$hook"
        fi
    done
    
    # Backup database schema (not data — too large)
    if $HAS_SQLITE; then
        python3 -c "
import sqlite3
conn = sqlite3.connect('$SQLITE_DB')
schema = conn.execute(\"SELECT sql FROM sqlite_master WHERE sql IS NOT NULL\").fetchall()
with open('$BACKUP_DIR/schema.sql', 'w') as f:
    for row in schema:
        f.write(row[0] + ';\n')
conn.close()
print('   Schema backed up')
" 2>/dev/null || echo "   ⚠️  Could not backup schema"
    fi
    
    echo "   ✅ Backup: $BACKUP_DIR"
else
    echo "   [dry-run] Would backup to: $BACKUP_DIR"
fi
echo ""

# ── Step 4: Update Hook Files ────────────────────────────────────────────────
if ! $SKIP_HOOKS; then
    echo "📋 Step 4: Updating hooks..."
    
    UPDATED=0
    SKIPPED=0
    ADDED=0
    
    for hook in nima-memory nima-recall-live nima-affect; do
        SOURCE="$SCRIPT_DIR/openclaw_hooks/$hook"
        DEST="$EXTENSIONS_DIR/$hook"
        
        if [ ! -d "$SOURCE" ]; then continue; fi
        
        # Create hook dir if new
        if [ ! -d "$DEST" ]; then
            if ! $DRY_RUN; then
                mkdir -p "$DEST"
            fi
            echo "   📦 NEW: $hook (not previously installed)"
        fi
        
        for src_file in $(find "$SOURCE" -type f \( -name "*.js" -o -name "*.py" -o -name "*.json" \) | grep -v __pycache__ | grep -v node_modules); do
            rel_path="${src_file#$SOURCE/}"
            dest_file="$DEST/$rel_path"
            
            if [ -f "$dest_file" ]; then
                # File exists — check if customized
                if diff -q "$src_file" "$dest_file" > /dev/null 2>&1; then
                    continue  # Identical, skip
                fi
                
                if ! $FORCE; then
                    echo "   ⏭️  SKIP: $hook/$rel_path (customized — use --force)"
                    SKIPPED=$((SKIPPED + 1))
                    continue
                fi
                
                echo "   🔄 UPDATE: $hook/$rel_path (backed up)"
            else
                echo "   ➕ NEW: $hook/$rel_path"
                ADDED=$((ADDED + 1))
            fi
            
            if ! $DRY_RUN; then
                mkdir -p "$(dirname "$dest_file")"
                cp "$src_file" "$dest_file"
            fi
            UPDATED=$((UPDATED + 1))
        done
    done
    
    echo "   Updated: $UPDATED | Skipped: $SKIPPED | New: $ADDED"
else
    echo "📋 Step 4: Skipping hooks (--skip-hooks)"
fi
echo ""

# ── Step 5: Database Schema Upgrade ──────────────────────────────────────────
if ! $SKIP_DB; then
    echo "📋 Step 5: Upgrading database schema..."
    
    if ! $DRY_RUN; then
        if $HAS_SQLITE; then
            # Run init_db.py — it only uses CREATE TABLE IF NOT EXISTS
            NIMA_HOME="$NIMA_HOME" python3 "$SCRIPT_DIR/scripts/init_db.py" --verbose 2>&1 | sed 's/^/   /'
        fi
        # Run init_ladybug.py — independent of SQLite; only when NIMA_DB_BACKEND=ladybug
        if [ "${NIMA_DB_BACKEND:-sqlite}" = "ladybug" ]; then
            _LADYBUG_PATH="${NIMA_LADYBUG_DB:-$LADYBUG_DB}"
            if python3 -c "import real_ladybug" 2>/dev/null && [ -f "$_LADYBUG_PATH" ]; then
                echo "   🗄️  Migrating LadybugDB schema (NIMA_DB_BACKEND=ladybug)..."
                NIMA_HOME="$NIMA_HOME" python3 "$SCRIPT_DIR/scripts/init_ladybug.py" --db "$_LADYBUG_PATH" 2>&1 | sed 's/^/   /'
            else
                echo "   ⚠️  NIMA_DB_BACKEND=ladybug but real_ladybug not installed or .lbug not found — skipping"
            fi
        fi
            # Migration offer: prompt to switch to LadybugDB if currently on SQLite
            if [ "${NIMA_DB_BACKEND:-sqlite}" != "ladybug" ] && [ -t 0 ]; then
                echo ""
                echo "   💡 LadybugDB is available (not currently enabled)."
                printf "   Migrate SQLite memories to LadybugDB? [y/N]: "
                read -r _migrate_choice
                case "$_migrate_choice" in
                    [yY]|[yY][eE][sS])
                        echo "   📦 Installing real-ladybug..."
                        pip install real-ladybug --quiet || pip install real-ladybug --quiet --break-system-packages
                        echo "   🗄️  Initialising LadybugDB schema..."
                        NIMA_HOME="$NIMA_HOME" python3 "$SCRIPT_DIR/scripts/init_ladybug.py" --db "$LADYBUG_DB" 2>&1 | sed 's/^/   /'
                        echo "   🔄 Running SQLite → LadybugDB migration..."
                        NIMA_HOME="$NIMA_HOME" python3 "$SCRIPT_DIR/scripts/migrate_sqlite_to_ladybug.py" 2>&1 | sed 's/^/   /'
                        _set_env_var "NIMA_DB_BACKEND" "ladybug" "$NIMA_HOME/.env"
                        echo "   ✅ NIMA_DB_BACKEND=ladybug written to $NIMA_HOME/.env"
                        ;;
                    *)
                        echo "   ⏭️  Skipped LadybugDB migration."
                        ;;
                esac
            fi
    else
        if $HAS_SQLITE; then
            echo "   [dry-run] Would run: python3 scripts/init_db.py"
            echo "   All CREATE TABLE IF NOT EXISTS — safe on existing databases"
        fi
        if [ "${NIMA_DB_BACKEND:-sqlite}" = "ladybug" ]; then
            echo "   [dry-run] Would run: python3 scripts/init_ladybug.py (LadybugDB column migrations)"
        fi
    fi
else
    echo "📋 Step 5: Skipping database (--skip-db)"
fi
echo ""

# ── Step 6: Verify ───────────────────────────────────────────────────────────
echo "📋 Step 6: Verification..."

if ! $DRY_RUN; then
    # Check hooks exist
    ALL_OK=true
    for hook in nima-memory nima-recall-live nima-affect; do
        if [ -d "$EXTENSIONS_DIR/$hook" ]; then
            echo "   ✅ $hook"
        else
            echo "   ❌ $hook (missing)"
            ALL_OK=false
        fi
    done
    
    # Check database tables
    if $HAS_SQLITE; then
        python3 -c "
import sqlite3
conn = sqlite3.connect('$SQLITE_DB')
tables = [r[0] for r in conn.execute(\"SELECT name FROM sqlite_master WHERE type='table'\").fetchall()]
required = ['memory_nodes', 'memory_edges', 'memory_turns', 'nima_insights', 'nima_patterns', 'nima_dream_runs', 'nima_suppressed_memories', 'nima_pruner_runs', 'nima_lucid_moments']
for t in required:
    status = '✅' if t in tables else '❌'
    print(f'   {status} Table: {t}')
conn.close()
" 2>/dev/null || echo "   ⚠️  Could not verify tables"
    fi
    
    echo ""
    if $ALL_OK; then
        echo "🎉 Upgrade to v$VERSION complete!"
        echo ""
        echo "   Restart OpenClaw to activate:"
        echo "   openclaw gateway restart"
    else
        echo "⚠️  Upgrade completed with warnings. Check above."
    fi
    
    echo ""
    echo "   Backup at: $BACKUP_DIR"
    echo "   To rollback: cp -r $BACKUP_DIR/nima-* $EXTENSIONS_DIR/"
else
    echo "   [dry-run] No changes made."
    echo "   Run without --dry-run to apply."
fi
