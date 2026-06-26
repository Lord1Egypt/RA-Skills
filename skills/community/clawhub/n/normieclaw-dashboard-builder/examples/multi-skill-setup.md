# Example: Multi-Skill Dashboard (5 Skills)

Building a dashboard with Expense Report Pro, Budget Buddy Pro, Daily Briefing, NoteTaker Pro, and Trainer Buddy Pro.

## Why These 5?

This combo covers the core pillars of a personal OS:
- **Money** — Expense Report Pro + Budget Buddy Pro
- **Information** — Daily Briefing + NoteTaker Pro
- **Health** — Trainer Buddy Pro

## Steps

### 1. Scaffold

```bash
cd ~/projects
bash /path/to/dashboard-builder/scripts/scaffold-project.sh my-life-dashboard
cd my-life-dashboard
```

### 2. Supabase Setup

Create project, get credentials, write `.env.local`.

### 3. Add All 5 Skills

```bash
SCRIPTS=/path/to/dashboard-builder/scripts

bash "$SCRIPTS/add-skill.sh" expense-report-pro
bash "$SCRIPTS/add-skill.sh" budget-buddy-pro
bash "$SCRIPTS/add-skill.sh" daily-briefing
bash "$SCRIPTS/add-skill.sh" notetaker-pro
bash "$SCRIPTS/add-skill.sh" trainer-buddy-pro
```

### 4. Update Registry

```typescript
// lib/registry.ts
import { manifest as expenseManifest } from '@/skills/expense_report/manifest'
import { manifest as budgetManifest } from '@/skills/budget_buddy/manifest'
import { manifest as briefingManifest } from '@/skills/daily_briefing/manifest'
import { manifest as notetakerManifest } from '@/skills/notetaker/manifest'
import { manifest as trainerManifest } from '@/skills/trainer_buddy/manifest'

const allSkills: SkillManifest[] = [
  expenseManifest,
  budgetManifest,
  briefingManifest,
  notetakerManifest,
  trainerManifest,
]
```

### 5. Run Migrations

```bash
bash "$SCRIPTS/run-migrations.sh"
npx supabase link --project-ref YOUR_REF
npx supabase db push
```

### 6. Verify Sidebar

Your sidebar should show:

```
📊 Dashboard Home
🔔 Notifications
─────────────────
FINANCE
  💰 Expenses
  💵 Budget
─────────────────
PRODUCTIVITY
  ☀️ Briefing
  📝 Notes
─────────────────
HEALTH & WELLNESS
  🏋️ Training
─────────────────
⚙️ Settings
```

### 7. Home Overview

The home page shows 5 widgets:
- **Spent This Month** (Expense Report Pro)
- **Monthly Budget** (Budget Buddy Pro)
- **Today's Briefing** (Daily Briefing)
- **Recent Notes** (NoteTaker Pro)
- **Workout Streak** (Trainer Buddy Pro)

### 8. Deploy

```bash
git init && git add -A && git commit -m "Initial dashboard with 5 skills"
# Push to GitHub, connect to Vercel, set env vars, deploy
```

## Growing Later

Want to add Health Buddy Pro later?

```bash
bash "$SCRIPTS/add-skill.sh" health-buddy-pro
# Update registry, run new migration, redeploy
```

The plugin architecture makes it trivial.
