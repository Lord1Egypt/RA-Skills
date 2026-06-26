#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# run-migrations.sh — Generate and run Supabase migrations from manifests
#
# Reads each installed skill's manifest.json from the normieclaw skills
# directory, extracts database table definitions, generates SQL migrations,
# and pushes them to Supabase.
#
# Usage: bash run-migrations.sh [--dry-run] [--skills-dir /path/to/skills]
#
# Options:
#   --dry-run       Print SQL but don't execute
#   --skills-dir    Override the default skills directory
###############################################################################

DRY_RUN=false
SKILLS_DIR=""
MIGRATION_DIR="supabase/migrations"
TIMESTAMP=$(date +%Y%m%d%H%M%S)

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=true; shift ;;
    --skills-dir)
      [ $# -ge 2 ] || { echo "Missing value for --skills-dir"; exit 1; }
      SKILLS_DIR="$2"
      shift 2
      ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

# Find skills directory
if [ -z "$SKILLS_DIR" ]; then
  SKILLS_DIR=$(find "$PWD" "$HOME" -path "*/normieclaw/skills" -type d 2>/dev/null | head -1)
  if [ -z "$SKILLS_DIR" ]; then
    echo "❌ Cannot find normieclaw/skills directory under current directory or \$HOME. Use --skills-dir."
    exit 1
  fi
fi

echo "🗄️  NormieClaw Migration Generator"
echo "──────────────────────────────────"
echo "📁 Skills dir: $SKILLS_DIR"
echo ""

# Ensure migration dir exists
mkdir -p "$MIGRATION_DIR"

# ── Core tables migration ────────────────────────────────────────────────────
CORE_FILE="$MIGRATION_DIR/${TIMESTAMP}00_core.sql"

cat > "$CORE_FILE" << 'CORESQL'
-- NormieClaw Core Tables
-- Shared across all skills

-- Profiles (extends auth.users)
CREATE TABLE IF NOT EXISTS profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  display_name TEXT,
  avatar_url TEXT,
  timezone TEXT DEFAULT 'America/New_York',
  sidebar_order JSONB DEFAULT '[]',
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
CREATE POLICY "profiles_select" ON profiles FOR SELECT USING (auth.uid() = id);
CREATE POLICY "profiles_insert" ON profiles FOR INSERT WITH CHECK (auth.uid() = id);
CREATE POLICY "profiles_update" ON profiles FOR UPDATE USING (auth.uid() = id) WITH CHECK (auth.uid() = id);

-- Settings (per-skill user settings)
CREATE TABLE IF NOT EXISTS user_settings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  skill_id TEXT NOT NULL,
  key TEXT NOT NULL,
  value JSONB NOT NULL DEFAULT 'null',
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(user_id, skill_id, key)
);

ALTER TABLE user_settings ENABLE ROW LEVEL SECURITY;
CREATE POLICY "settings_select" ON user_settings FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "settings_insert" ON user_settings FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "settings_update" ON user_settings FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "settings_delete" ON user_settings FOR DELETE USING (auth.uid() = user_id);

-- Notifications (aggregated timeline)
CREATE TABLE IF NOT EXISTS notifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  skill_id TEXT NOT NULL,
  type TEXT NOT NULL DEFAULT 'info',
  title TEXT NOT NULL,
  body TEXT,
  metadata JSONB DEFAULT '{}',
  read BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;
CREATE POLICY "notifications_select" ON notifications FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "notifications_insert" ON notifications FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "notifications_update" ON notifications FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "notifications_delete" ON notifications FOR DELETE USING (auth.uid() = user_id);

CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id, created_at DESC);

-- Updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger to core tables
CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER update_user_settings_updated_at BEFORE UPDATE ON user_settings FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- Auto-create profile on signup
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, display_name)
  VALUES (NEW.id, COALESCE(NEW.raw_user_meta_data->>'full_name', NEW.email));
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created AFTER INSERT ON auth.users FOR EACH ROW EXECUTE FUNCTION handle_new_user();
CORESQL

echo "✅ Core migration: $CORE_FILE"

# ── Per-skill migrations ────────────────────────────────────────────────────
SKILL_COUNT=0

for manifest in "$SKILLS_DIR"/*/dashboard-kit/manifest.json; do
  [ -f "$manifest" ] || continue

  META_OUTPUT=$(python3 - "$manifest" <<'PYEOF'
import json
import re
import sys

with open(sys.argv[1]) as f:
    m = json.load(f)

skill_id = m['skill_id']
prefix = m['database']['prefix']

if not re.fullmatch(r'[a-z0-9-]+', skill_id):
    raise SystemExit(f"Invalid skill_id: {skill_id}")
if not re.fullmatch(r'[a-z][a-z0-9_]{1,15}', prefix):
    raise SystemExit(f"Invalid database prefix: {prefix}")

print(skill_id)
print(prefix)
PYEOF
  )

  META_FIELDS=()
  while IFS= read -r line; do
    META_FIELDS+=("$line")
  done <<< "$META_OUTPUT"

  SKILL_ID="${META_FIELDS[0]:-}"
  PREFIX="${META_FIELDS[1]:-}"

  if [ -z "$SKILL_ID" ] || [ -z "$PREFIX" ]; then
    echo "❌ Failed to parse manifest metadata: $manifest"
    exit 1
  fi

  SKILL_COUNT=$((SKILL_COUNT + 1))
  MIGRATION_FILE="$MIGRATION_DIR/${TIMESTAMP}$(printf '%02d' $SKILL_COUNT)_${SKILL_ID//-/_}.sql"

  # Generate SQL from manifest using Python
  python3 - "$manifest" <<'PYEOF' > "$MIGRATION_FILE"
import json, sys
import re


def ensure_ident(name, label):
    if not re.fullmatch(r'[a-z_][a-z0-9_]*', name):
        raise SystemExit(f"Invalid {label}: {name}")
    return name


def ensure_sql_type(sql_type):
    if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_\\[\\](), ]*', sql_type):
        raise SystemExit(f"Invalid SQL type: {sql_type}")
    return sql_type


def ensure_reference(ref):
    if not re.fullmatch(r'[a-z_][a-z0-9_]*(\\.[a-z_][a-z0-9_]*)?(\\([a-z_][a-z0-9_]*\\))?', ref):
        raise SystemExit(f"Invalid reference target: {ref}")
    return ref


def sql_quote(value):
    return "'" + value.replace("'", "''") + "'"

with open(sys.argv[1]) as f:
    m = json.load(f)

prefix = m['database']['prefix']
tables = m['database']['tables']
skill_id = m['skill_id']

print(f"-- {m['display_name']} tables")
print(f"-- Prefix: {prefix}")
print(f"-- Generated from manifest.json")
print()

for t in tables:
    tname = ensure_ident(t['name'], 'table name')
    cols = t.get('columns', [])
    indexes = t.get('indexes', [])

    if not cols:
        print(f"-- WARNING: {tname} has no column definitions in manifest")
        print(f"-- Create this table manually based on skill documentation")
        print()
        continue

    # Build CREATE TABLE
    col_defs = []
    has_user_id = False
    has_updated_at = False
    for c in cols:
        col_name = ensure_ident(c['name'], f"column name in {tname}")
        col_type = ensure_sql_type(c['type'])
        parts = [col_name, col_type]
        if c.get('primary_key'):
            parts.append('PRIMARY KEY DEFAULT gen_random_uuid()')
        if c.get('references'):
            ref = ensure_reference(c['references'])
            parts.append(f'REFERENCES {ref} ON DELETE CASCADE')
        if 'default' in c and not c.get('primary_key'):
            d = c['default']
            if isinstance(d, bool):
                parts.append(f"DEFAULT {'true' if d else 'false'}")
            elif isinstance(d, (int, float)):
                parts.append(f"DEFAULT {d}")
            elif isinstance(d, str):
                parts.append(f"DEFAULT {sql_quote(d)}")
        if col_name == 'user_id':
            has_user_id = True
            parts.append('NOT NULL')
        if col_name == 'updated_at':
            has_updated_at = True
        if col_name == 'created_at':
            parts = [col_name, col_type, 'DEFAULT now()']
        if col_name == 'updated_at':
            parts = [col_name, col_type, 'DEFAULT now()']
        col_defs.append('  ' + ' '.join(parts))

    print(f"CREATE TABLE IF NOT EXISTS {tname} (")
    print(',\n'.join(col_defs))
    print(');')
    print()

    # RLS
    print(f"ALTER TABLE {tname} ENABLE ROW LEVEL SECURITY;")

    if has_user_id:
        print(f"CREATE POLICY \"{tname}_select\" ON {tname} FOR SELECT USING (auth.uid() = user_id);")
        print(f"CREATE POLICY \"{tname}_insert\" ON {tname} FOR INSERT WITH CHECK (auth.uid() = user_id);")
        print(f"CREATE POLICY \"{tname}_update\" ON {tname} FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);")
        print(f"CREATE POLICY \"{tname}_delete\" ON {tname} FOR DELETE USING (auth.uid() = user_id);")
    else:
        # Child table — needs parent-chain RLS (documented in SKILL.md)
        print(f"-- NOTE: {tname} is a child table. Add parent-chain RLS policy manually.")

    print()

    # Updated_at trigger
    if has_updated_at:
        trigger_name = f"update_{tname}_updated_at"
        print(f"CREATE TRIGGER {trigger_name} BEFORE UPDATE ON {tname} FOR EACH ROW EXECUTE FUNCTION update_updated_at();")
        print()

    # Indexes
    for idx in indexes:
        idx_name = ensure_ident(idx['name'], f"index name on {tname}")
        idx_type = idx.get('type', '')
        if idx_type and not re.fullmatch(r'[A-Za-z_]+', idx_type):
            raise SystemExit(f"Invalid index type: {idx_type}")
        using = f' USING {idx_type}' if idx_type else ''
        index_cols = [ensure_ident(col, f"index column on {tname}") for col in idx['columns']]
        cols_str = ', '.join(index_cols)
        print(f"CREATE INDEX IF NOT EXISTS {idx_name} ON {tname}{using} ({cols_str});")

    print()

PYEOF

  echo "✅ Skill migration: $MIGRATION_FILE ($SKILL_ID)"
done

echo ""
echo "──────────────────────────────────"
echo "Generated $((SKILL_COUNT + 1)) migration files in $MIGRATION_DIR/"

if [ "$DRY_RUN" = true ]; then
  echo ""
  echo "🔍 DRY RUN — SQL files generated but not executed."
  echo "Review them in $MIGRATION_DIR/ then run:"
  echo "  npx supabase db push"
else
  echo ""
  echo "Next step: Run migrations with:"
  echo "  npx supabase link --project-ref YOUR_PROJECT_REF"
  echo "  npx supabase db push"
fi
