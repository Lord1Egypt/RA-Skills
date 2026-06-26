# Example: Single Skill Dashboard (Expense Report Pro)

This walkthrough builds a dashboard with just Expense Report Pro — the simplest possible setup.

## What You'll Get

- A dark-mode dashboard at `localhost:3000`
- Sidebar with: Dashboard Home, Expenses (with sub-pages: All Expenses, Reports, Budgets), Settings
- Home page with a "Spent This Month" widget
- Full expense tracking with Supabase database and RLS

## Steps

### 1. Scaffold the Project

```bash
cd ~/projects
bash /path/to/dashboard-builder/scripts/scaffold-project.sh my-expenses-dashboard
cd my-expenses-dashboard
```

### 2. Set Up Supabase

1. Create a new Supabase project (free tier is fine)
2. Create `.env.local`:
```
NEXT_PUBLIC_SUPABASE_URL=https://abc123.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<your-supabase-anon-key>
SUPABASE_SERVICE_ROLE_KEY=<your-supabase-service-role-key>
WEBHOOK_SECRET=your-random-secret
```

### 3. Add Expense Report Pro

```bash
bash /path/to/dashboard-builder/scripts/add-skill.sh expense-report-pro
```

This creates:
- `skills/expense_report/manifest.ts`
- `app/expenses/page.tsx`
- `app/expenses/reports/page.tsx`
- `app/expenses/budgets/page.tsx`

### 4. Update the Registry

Edit `lib/registry.ts`:
```typescript
import { manifest as expenseReportManifest } from '@/skills/expense_report/manifest'

const allSkills: SkillManifest[] = [
  expenseReportManifest,
]
```

### 5. Run Migrations

```bash
bash /path/to/dashboard-builder/scripts/run-migrations.sh
npx supabase link --project-ref YOUR_REF
npx supabase db push
```

### 6. Launch

```bash
npm run dev
```

Open `http://localhost:3000`. Sign up, log in, and you'll see your dashboard with the Expenses page in the sidebar.

### 7. Customize the Expense Page

The generated `app/expenses/page.tsx` is a starter. Enhance it by:
- Importing `StatCard` and `DataTable` from `@/components/shared/`
- Querying `exp_expenses` from Supabase
- Adding the monthly spend calculation
- Wiring up the "Add Expense" button

See `SKILL.md` → "How to Read a Manifest and Generate a Skill Page" for the full pattern.

## Result

A clean, functional expense tracking dashboard. One skill, one focus, zero bloat.
