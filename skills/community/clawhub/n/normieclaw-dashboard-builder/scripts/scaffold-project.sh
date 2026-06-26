#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# scaffold-project.sh — NormieClaw Dashboard scaffolding
#
# Creates a Next.js 14 project with all NormieClaw templates, deps, and
# directory structure. Run from the parent directory where you want the
# project created.
#
# Usage: bash scaffold-project.sh [project-name]
# Default project name: normieclaw-dashboard
###############################################################################

PROJECT_NAME="${1:-normieclaw-dashboard}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
TEMPLATE_DIR="$SKILL_DIR/templates"

# ── Preflight checks ────────────────────────────────────────────────────────
echo "🔧 NormieClaw Dashboard Scaffolder"
echo "──────────────────────────────────"

if ! command -v node &>/dev/null; then
  echo "❌ Node.js not found. Install Node.js 18+ first."
  exit 1
fi

NODE_MAJOR=$(node -v | cut -d. -f1 | tr -d 'v')
if [ "$NODE_MAJOR" -lt 18 ]; then
  echo "❌ Node.js 18+ required. Found: $(node -v)"
  exit 1
fi

if ! command -v npm &>/dev/null; then
  echo "❌ npm not found."
  exit 1
fi

if [ -d "$PROJECT_NAME" ]; then
  echo "❌ Directory '$PROJECT_NAME' already exists. Choose a different name or delete it."
  exit 1
fi

echo "✅ Node $(node -v) / npm $(npm -v)"
echo "📁 Creating project: $PROJECT_NAME"
echo ""

# ── Step 1: Create Next.js project ──────────────────────────────────────────
echo "📦 Step 1/6: Creating Next.js project..."
npx create-next-app@latest "$PROJECT_NAME" \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --src-dir=false \
  --import-alias="@/*" \
  --use-npm \
  --yes

cd "$PROJECT_NAME"

# ── Step 2: Install dependencies ────────────────────────────────────────────
echo ""
echo "📦 Step 2/6: Installing NormieClaw dependencies..."
npm install \
  @supabase/ssr@^0.5.0 \
  @supabase/supabase-js@^2.45.0 \
  recharts@^2.12.0 \
  lucide-react@^0.400.0 \
  date-fns@^3.6.0 \
  zod@^3.23.0 \
  clsx@^2.1.0 \
  tailwind-merge@^2.4.0 \
  class-variance-authority@^0.7.0 \
  @dnd-kit/core@^6.1.0 \
  @dnd-kit/sortable@^8.0.0 \
  @dnd-kit/utilities@^3.2.0

npm install -D \
  tailwindcss-animate@^1.0.0

# ── Step 3: Create directory structure ───────────────────────────────────────
echo ""
echo "📂 Step 3/6: Creating directory structure..."
mkdir -p app/{login,settings,notifications}
mkdir -p app/api/sync
mkdir -p components/{shell,shared/charts,ui,skills}
mkdir -p lib/{supabase,types,utils}
mkdir -p skills
mkdir -p supabase/migrations
mkdir -p styles
mkdir -p public

# ── Step 4: Copy templates ──────────────────────────────────────────────────
echo ""
echo "📄 Step 4/6: Copying NormieClaw templates..."

cp "$TEMPLATE_DIR/globals.css" styles/globals.css
cp "$TEMPLATE_DIR/layout.tsx" app/layout.tsx
cp "$TEMPLATE_DIR/home-overview.tsx" app/page.tsx
cp "$TEMPLATE_DIR/middleware.ts" middleware.ts

# Shell components
cp "$TEMPLATE_DIR/sidebar.tsx" components/shell/sidebar.tsx

# Shared components
cp "$TEMPLATE_DIR/stat-card.tsx" components/shared/stat-card.tsx
cp "$TEMPLATE_DIR/data-table.tsx" components/shared/data-table.tsx
cp "$TEMPLATE_DIR/chart-wrapper.tsx" components/shared/charts/chart-wrapper.tsx
cp "$TEMPLATE_DIR/page-template.tsx" components/shared/page-template.tsx

# Supabase
cp "$TEMPLATE_DIR/supabase-client.ts" lib/supabase/client.ts
cp "$TEMPLATE_DIR/supabase-server.ts" lib/supabase/server.ts

# ── Step 5: Create utility files ────────────────────────────────────────────
echo ""
echo "🛠️  Step 5/6: Creating utility files..."

cat > lib/utils/cn.ts << 'UTILEOF'
import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
UTILEOF

cat > lib/utils/format.ts << 'FMTEOF'
import { format, formatDistanceToNow, isToday, isYesterday } from 'date-fns'

export function formatCents(cents: number, currency = 'USD'): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency', currency, minimumFractionDigits: 2,
  }).format(cents / 100)
}

export function formatDate(date: string | Date, pattern = 'MMM d, yyyy'): string {
  const d = typeof date === 'string' ? new Date(date) : date
  if (isToday(d)) return 'Today'
  if (isYesterday(d)) return 'Yesterday'
  return format(d, pattern)
}

export function formatRelative(date: string | Date): string {
  return formatDistanceToNow(typeof date === 'string' ? new Date(date) : date, { addSuffix: true })
}

export function formatNumber(n: number): string {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`
  if (n >= 1_000) return `${(n / 1_000).toFixed(1)}K`
  return n.toLocaleString()
}

export function formatPercent(value: number, decimals = 1): string {
  return `${value >= 0 ? '+' : ''}${value.toFixed(decimals)}%`
}
FMTEOF

# Type definitions
cat > lib/types/skill.ts << 'TYPEEOF'
export interface NavChild {
  label: string
  route: string
  lucideIcon?: string
}

export interface SkillManifest {
  id: string
  displayName: string
  icon: string
  lucideIcon: string
  dbPrefix: string
  accentColor: string
  version: string
  category: string
  nav: {
    label: string
    defaultRoute: string
    children?: NavChild[]
  }
  homeWidgets: {
    id: string
    component: string
    span: number
    dataSource: string
  }[]
  tables: {
    name: string
    description: string
  }[]
  settings: {
    key: string
    label: string
    type: string
    defaultValue: any
    description?: string
    options?: { label: string; value: string }[]
  }[]
  sync: {
    strategy: 'direct' | 'json' | 'webhook'
    sourceDir?: string
    webhookPath?: string
  }
}
TYPEEOF

# Empty registry (user populates with skill imports)
cat > lib/registry.ts << 'REGEOF'
import type { SkillManifest } from '@/lib/types/skill'

// Import skill manifests here:
// import { manifest as expenseManifest } from '@/skills/expense-report/manifest'

const allSkills: SkillManifest[] = [
  // Add imported manifests here:
  // expenseManifest,
]

export const registry = {
  getEnabledSkills(): SkillManifest[] {
    return allSkills
  },

  getSkillById(id: string): SkillManifest | undefined {
    return allSkills.find((s) => s.id === id)
  },

  getAllHomeWidgets() {
    return allSkills.flatMap((skill) =>
      skill.homeWidgets.map((w) => ({ ...w, skillId: skill.id }))
    )
  },

  getAllRoutes(): string[] {
    return allSkills.flatMap((s) => [
      s.nav.defaultRoute,
      ...(s.nav.children?.map((c) => c.route) ?? []),
    ])
  },

  validatePrefixes(): void {
    const prefixes = allSkills.map((s) => s.dbPrefix)
    const dupes = prefixes.filter((p, i) => prefixes.indexOf(p) !== i)
    if (dupes.length > 0) {
      throw new Error(`Duplicate database prefixes detected: ${dupes.join(', ')}`)
    }
  },

  validateRoutes(): void {
    const routes = this.getAllRoutes()
    const dupes = routes.filter((r, i) => routes.indexOf(r) !== i)
    if (dupes.length > 0) {
      throw new Error(`Duplicate routes detected: ${dupes.join(', ')}`)
    }
  },
}
REGEOF

# Noise SVG
cat > public/noise.svg << 'NOISEEOF'
<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200">
  <filter id="noise">
    <feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" stitchTiles="stitch"/>
    <feColorMatrix type="saturate" values="0"/>
  </filter>
  <rect width="100%" height="100%" filter="url(#noise)" opacity="1"/>
</svg>
NOISEEOF

# .env.local template
cat > .env.local.example << 'ENVEOF'
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<your-supabase-anon-key>
SUPABASE_SERVICE_ROLE_KEY=<your-supabase-service-role-key>
WEBHOOK_SECRET=generate-with-openssl-rand-hex-32
ENVEOF

# ── Step 6: Summary ─────────────────────────────────────────────────────────
echo ""
echo "──────────────────────────────────"
echo "✅ NormieClaw Dashboard scaffolded!"
echo ""
echo "Next steps:"
echo "  1. cd $PROJECT_NAME"
echo "  2. Copy .env.local.example to .env.local and fill in your Supabase credentials"
echo "  3. Run database migrations (see run-migrations.sh)"
echo "  4. Add skill manifests to lib/registry.ts"
echo "  5. npm run dev"
echo ""
echo "📖 Full docs: Read the Dashboard Builder SKILL.md"
echo "──────────────────────────────────"
