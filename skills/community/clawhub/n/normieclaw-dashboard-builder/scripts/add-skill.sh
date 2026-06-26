#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# add-skill.sh — Add a NormieClaw skill to an existing dashboard
#
# Reads the skill's manifest.json, creates route directories, generates
# a starter page, and registers the skill in the dashboard registry.
#
# Usage: bash add-skill.sh <skill-name> [--skills-dir /path]
# Example: bash add-skill.sh expense-report-pro
###############################################################################

if [ $# -lt 1 ]; then
  echo "Usage: bash add-skill.sh <skill-name> [--skills-dir /path/to/skills]"
  echo "Example: bash add-skill.sh expense-report-pro"
  exit 1
fi

SKILL_NAME="$1"
shift
SKILLS_DIR=""

if [[ ! "$SKILL_NAME" =~ ^[a-z0-9-]+$ ]]; then
  echo "❌ Invalid skill name: $SKILL_NAME"
  exit 1
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    --skills-dir)
      [ $# -ge 2 ] || { echo "Missing value for --skills-dir"; exit 1; }
      SKILLS_DIR="$2"
      shift 2
      ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

validate_route() {
  local route="$1"
  [[ "$route" =~ ^/[a-z0-9/_-]*$ ]] || return 1
  [[ "$route" != *".."* ]] || return 1
  [[ "$route" != *"//"* ]] || return 1
}

js_quote() {
  python3 - "$1" <<'PYEOF'
import json
import sys

print(json.dumps(sys.argv[1]))
PYEOF
}

# Find skills directory
if [ -z "$SKILLS_DIR" ]; then
  SKILLS_DIR=$(find "$PWD" "$HOME" -path "*/normieclaw/skills" -type d 2>/dev/null | head -1)
  if [ -z "$SKILLS_DIR" ]; then
    echo "❌ Cannot find normieclaw/skills under current directory or \$HOME. Use --skills-dir."
    exit 1
  fi
fi

MANIFEST="$SKILLS_DIR/$SKILL_NAME/dashboard-kit/manifest.json"
if [ ! -f "$MANIFEST" ]; then
  echo "❌ Manifest not found: $MANIFEST"
  echo "Available skills:"
  for d in "$SKILLS_DIR"/*/dashboard-kit/manifest.json; do
    [ -f "$d" ] && basename "$(dirname "$(dirname "$d")")"
  done
  exit 1
fi

# Verify we're in a Next.js project
if [ ! -f "package.json" ] || ! grep -q "next" package.json; then
  echo "❌ Not in a Next.js project root. cd into your dashboard project first."
  exit 1
fi

echo "🔌 Adding skill: $SKILL_NAME"
echo "──────────────────────────────────"

# Extract and validate manifest data
MANIFEST_META=$(python3 - "$MANIFEST" <<'PYEOF'
import json
import re
import sys

with open(sys.argv[1]) as f:
    m = json.load(f)

skill_id = m['skill_id']
display_name = m['display_name']
icon = m['icon']
prefix = m['database']['prefix']
route = m['sidebar']['route']
accent = m['accent_color']
category = m.get('category', 'other')

if not re.fullmatch(r'[a-z0-9-]+', skill_id):
    raise SystemExit(f"Invalid skill_id: {skill_id}")
if not re.fullmatch(r'[a-z][a-z0-9_]{1,15}', prefix):
    raise SystemExit(f"Invalid database prefix: {prefix}")

for value in (display_name, icon, accent, category, route):
    if '\n' in value or '\r' in value:
        raise SystemExit("Manifest fields cannot contain newlines")

print(skill_id)
print(display_name)
print(icon)
print(prefix)
print(route)
print(accent)
print(category)
PYEOF
)

MANIFEST_FIELDS=()
while IFS= read -r line; do
  MANIFEST_FIELDS+=("$line")
done <<< "$MANIFEST_META"

SKILL_ID="${MANIFEST_FIELDS[0]:-}"
DISPLAY_NAME="${MANIFEST_FIELDS[1]:-}"
LUCIDE_ICON="${MANIFEST_FIELDS[2]:-}"
PREFIX="${MANIFEST_FIELDS[3]:-}"
ROUTE="${MANIFEST_FIELDS[4]:-}"
ACCENT="${MANIFEST_FIELDS[5]:-}"
CATEGORY="${MANIFEST_FIELDS[6]:-}"

if [ -z "$SKILL_ID" ] || [ -z "$DISPLAY_NAME" ] || [ -z "$ROUTE" ]; then
  echo "❌ Failed to parse required manifest fields"
  exit 1
fi

if ! validate_route "$ROUTE"; then
  echo "❌ Invalid route in manifest: $ROUTE"
  exit 1
fi

echo "  ID: $SKILL_ID"
echo "  Display: $DISPLAY_NAME"
echo "  Route: $ROUTE"
echo "  DB Prefix: $PREFIX"
echo ""

# ── Step 1: Create skill directory ──────────────────────────────────────────
SKILL_DIR="skills/${SKILL_ID//-/_}"
mkdir -p "$SKILL_DIR"/{pages,widgets,migrations}

echo "📁 Created $SKILL_DIR/"

# ── Step 2: Generate manifest.ts ────────────────────────────────────────────
python3 - "$MANIFEST" <<'PYEOF' > "$SKILL_DIR/manifest.ts"
import json
import re
import sys


def js(value):
    return json.dumps(value)


def validate_route(route):
    return bool(re.fullmatch(r'/[a-z0-9/_-]*', route)) and '..' not in route and '//' not in route

with open(sys.argv[1]) as f:
    m = json.load(f)

sb = m['sidebar']
children = sb.get('children', [])
prefix = m['database']['prefix']

children_ts = ''
if children:
    items = []
    for c in children:
        if not validate_route(c['route']):
            raise SystemExit(f"Invalid child route: {c['route']}")
        icon_part = f", lucideIcon: {js(c['icon'])}" if c.get('icon') else ''
        items.append(f"      {{ label: {js(c['label'])}, route: {js(c['route'])}{icon_part} }}")
    children_ts = '\n' + ',\n'.join(items) + ',\n    '

widgets = m.get('widgets', [])
widgets_ts = []
for w in widgets:
    widgets_ts.append(f"    {{ id: {js(w['id'])}, component: {js(w.get('type', 'stat') + 'Widget')}, span: {'2' if w.get('size','1x1').startswith('2') else '3' if w.get('size','1x1').startswith('3') else '1'}, dataSource: {js(prefix + '_' + w['id'].replace('-','_'))} }}")

settings = m.get('settings', [])
settings_ts = []
for s in settings:
    d = s.get('default', '')
    if isinstance(d, bool):
        default_val = 'true' if d else 'false'
    elif isinstance(d, (int, float)):
        default_val = str(d)
    else:
        default_val = js(str(d))
    settings_ts.append(f"    {{ key: {js(s['key'])}, label: {js(s['label'])}, type: {js(s['type'])}, defaultValue: {default_val} }}")

sync = m.get('sync', {'mode': 'direct'})
sync_strategy = sync.get('mode', 'direct')

print(f"""import type {{ SkillManifest }} from '@/lib/types/skill'

export const manifest: SkillManifest = {{
  id: {js(m['skill_id'])},
  displayName: {js(m['display_name'])},
  icon: {js(m.get('emoji', '📊'))},
  lucideIcon: {js(m['icon'])},
  dbPrefix: {js(m['database']['prefix'])},
  accentColor: {js(m['accent_color'])},
  version: '1.0.0',
  category: {js(m.get('category', 'other'))},
  nav: {{
    label: {js(sb['label'])},
    defaultRoute: {js(sb['route'])},
    children: [{children_ts}],
  }},
  homeWidgets: [
{chr(10).join(widgets_ts)},
  ],
  tables: [],
  settings: [
{chr(10).join(settings_ts)},
  ],
  sync: {{ strategy: {js(sync_strategy)} }},
}}""")
PYEOF

echo "📝 Generated $SKILL_DIR/manifest.ts"

# ── Step 3: Create route directories and pages ──────────────────────────────
# Main route
ROUTE_DIR="app${ROUTE}"
mkdir -p "$ROUTE_DIR"

cat > "$ROUTE_DIR/page.tsx" << PAGEEOF
import { createServerClient } from '@/lib/supabase/server'

export const metadata = { title: $(js_quote "$DISPLAY_NAME | NormieClaw") }

export default async function ${SKILL_ID//-/}Page() {
  const supabase = createServerClient()
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) return null

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-[1.75rem] font-bold text-text-1">{$(js_quote "$DISPLAY_NAME")}</h1>
        <p className="text-[13px] text-text-3 mt-0.5">{$(js_quote "Manage your ${DISPLAY_NAME,,} data")}</p>
      </div>
      <div className="rounded-lg border border-border-soft bg-surface-1 p-6 noise-overlay">
        <p className="text-sm text-text-3">Content goes here. Customize this page for your skill.</p>
      </div>
    </div>
  )
}
PAGEEOF

echo "📄 Created $ROUTE_DIR/page.tsx"

# Sub-routes
python3 - "$MANIFEST" "$ROUTE" <<'SUBEOF'
import json
import sys

with open(sys.argv[1]) as f:
    children = json.load(f)['sidebar'].get('children', [])
for c in children:
    route = c['route']
    # Skip main route (already created)
    if route == sys.argv[2]:
        continue
    print(route)
SUBEOF | while read -r child_route; do
  validate_route "$child_route" || { echo "❌ Invalid child route: $child_route"; exit 1; }
  CHILD_DIR="app${child_route}"
  mkdir -p "$CHILD_DIR"
  CHILD_LABEL=$(python3 - "$MANIFEST" "$child_route" <<'PYEOF'
import json
import sys

with open(sys.argv[1]) as f:
    children = json.load(f)['sidebar'].get('children', [])

route = sys.argv[2]
matches = [c['label'] for c in children if c['route'] == route]
if not matches:
    raise SystemExit(f"Missing child label for route: {route}")
print(matches[0])
PYEOF
)
  CHILD_COMPONENT=$(python3 - "$CHILD_LABEL" <<'PYEOF'
import re
import sys

name = re.sub(r'[^A-Za-z0-9]+', '', sys.argv[1])
if not name:
    name = 'Skill'
if name[0].isdigit():
    name = f'Skill{name}'
print(name)
PYEOF
)

  cat > "$CHILD_DIR/page.tsx" << CHILDEOF
import { createServerClient } from '@/lib/supabase/server'

export const metadata = { title: $(js_quote "$CHILD_LABEL | $DISPLAY_NAME | NormieClaw") }

export default async function ${CHILD_COMPONENT}Page() {
  const supabase = createServerClient()
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) return null

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-[1.75rem] font-bold text-text-1">{$(js_quote "$CHILD_LABEL")}</h1>
      </div>
      <div className="rounded-lg border border-border-soft bg-surface-1 p-6 noise-overlay">
        <p className="text-sm text-text-3">Content goes here.</p>
      </div>
    </div>
  )
}
CHILDEOF
  echo "📄 Created $CHILD_DIR/page.tsx"
done

# ── Step 4: Update registry ─────────────────────────────────────────────────
REGISTRY_FILE="lib/registry.ts"
IMPORT_NAME="${SKILL_ID//-/}Manifest"
IMPORT_PATH="@/skills/${SKILL_ID//-/_}/manifest"

if grep -q "$IMPORT_PATH" "$REGISTRY_FILE" 2>/dev/null; then
  echo "⚠️  Skill already in registry — skipping registry update"
else
  echo ""
  echo "📌 Add to lib/registry.ts:"
  echo "  import { manifest as ${IMPORT_NAME} } from '${IMPORT_PATH}'"
  echo "  // Then add ${IMPORT_NAME} to the allSkills array"
fi

echo ""
echo "──────────────────────────────────"
echo "✅ Skill '$DISPLAY_NAME' added!"
echo ""
echo "Next steps:"
echo "  1. Add the import to lib/registry.ts (see above)"
echo "  2. Run migrations: bash run-migrations.sh"
echo "  3. Customize the pages in $SKILL_DIR/pages/"
echo "  4. npm run dev to preview"
