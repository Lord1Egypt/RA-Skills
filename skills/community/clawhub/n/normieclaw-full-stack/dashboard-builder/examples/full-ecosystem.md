# Example: Full Ecosystem (All 21 Skills)

The ultimate NormieClaw dashboard — every skill in one app.

## Sidebar Layout

With all 21 skills installed, the sidebar groups by category:

```
📊 Dashboard Home
🔔 Notifications
─────────────────
FINANCE
  💰 Expenses        (3 sub-pages)
  💵 Budget          (7 sub-pages)
  📈 Stocks          (5 sub-pages)
  🧾 Invoices        (3 sub-pages)
─────────────────
PRODUCTIVITY
  🧠 Memory          (4 sub-pages)
  📝 Notes           (3 sub-pages)
  📄 Documents       (2 sub-pages)
  🔒 Security        (3 sub-pages)
  ☀️ Briefing        (3 sub-pages)
─────────────────
WORK
  📱 Content         (5 sub-pages)
  📧 Email           (5 sub-pages)
  💼 Job Hunt        (4 sub-pages)
─────────────────
HEALTH & WELLNESS
  🏥 Health          (6 sub-pages)
  🏋️ Training       (5 sub-pages)
─────────────────
LEARNING
  📚 Knowledge       (2 sub-pages)
  🎓 Tutor           (6 sub-pages)
─────────────────
LIFESTYLE
  🍽️ Meal Planner   (5 sub-pages)
  ✈️ Travel          (5 sub-pages)
  👥 Relationships   (3 sub-pages)
  🌱 Plants          (3 sub-pages)
  🔧 Home            (5 sub-pages)
─────────────────
⚙️ Settings
```

## Database Prefixes

All 21 skills coexist in one Supabase database without conflicts:

| Prefix | Skill | Tables |
|--------|-------|--------|
| `exp`  | Expense Report Pro | 1 |
| `mp`   | Meal Planner Pro | 16 |
| `mem`  | Supercharged Memory | 2 |
| `sw`   | Stock Watcher Pro | 7 |
| `tp`   | Travel Planner Pro | 8 |
| `sec`  | Security Team | 2 |
| `cc`   | Content Creator Pro | 7 |
| `dbr`  | Daily Briefing | 5 |
| `kv`   | Knowledge Vault | 2 |
| `tb`   | Trainer Buddy Pro | 7 |
| `ea`   | Email Assistant | 4 |
| `hm`   | HireMe Pro | 5 |
| `hb`   | Health Buddy Pro | 7 |
| `nt`   | NoteTaker Pro | 3 |
| `rb`   | Relationship Buddy | 8 |
| `tu`   | Tutor Buddy Pro | 7 |
| `bb`   | Budget Buddy Pro | 5 |
| `pd`   | Plant Doctor | 4 |
| `ds`   | DocuScan | 1 |
| `hf`   | Home Fix-It | 5 |
| `ig`   | InvoiceGen | 4 |

**Total: ~103 tables** — all RLS-protected, all user-scoped.

## Setup Steps

### 1. Scaffold & Install
```bash
bash scaffold-project.sh normieclaw-full
cd normieclaw-full
```

### 2. Add All 21 Skills
```bash
for skill in expense-report-pro meal-planner-pro supercharged-memory stock-watcher-pro \
  travel-planner-pro security-team content-creator-pro daily-briefing knowledge-vault \
  trainer-buddy-pro email-assistant hireme-pro health-buddy-pro notetaker-pro \
  relationship-buddy tutor-buddy-pro budget-buddy-pro plant-doctor docuscan \
  home-fix-it invoicegen; do
  bash add-skill.sh "$skill"
done
```

### 3. Update Registry

Import all 21 manifests into `lib/registry.ts`. The `add-skill.sh` script prints the exact import line for each.

### 4. Run Migrations

```bash
bash run-migrations.sh
npx supabase db push
```

This generates 22 migration files (1 core + 21 skills) and creates ~103 tables.

### 5. Deploy

```bash
git init && git add -A && git commit -m "Full NormieClaw ecosystem"
# Push to GitHub → Vercel auto-deploys
```

## Performance Notes

- **Server Components** — All pages and widgets are server-rendered. No client-side data waterfall.
- **Independent queries** — Each widget fetches its own data. One slow skill doesn't block others.
- **Lazy routes** — Next.js App Router code-splits by route. Loading `/expenses` doesn't load training code.
- **DB indexes** — Every manifest specifies indexes. The migration script creates them.
- **Tested at scale** — 21 sidebar items, 103 tables, 25+ widgets. Works.

## Home Overview

With all 21 skills, the home page shows a dense widget grid:
- 4-column layout on desktop
- ~25 widgets total
- Greeting, quick actions strip, widget grid, recent activity, upcoming events
- Each widget is a self-contained server component

This is the full NormieClaw experience. Your personal OS.
