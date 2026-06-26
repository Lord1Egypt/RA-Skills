# Health Buddy Pro — Dashboard Starter Kit Specification

**Design Vibe:** Premium modern dark theme. Deep blacks/grays (`#0a0a0a`, `#1a1a1a`, `#2a2a2a`), electric teal (`#14b8a6`) for positive progress and primary accents, vibrant orange (`#f97316`) for alerts/warnings/active states. Clean typography, generous whitespace, smooth animations.

---

## Dashboard Sections

### 1. Daily Nutrition Overview (Hero Section)

**Component:** Nested donut chart — calories consumed vs. remaining as the outer ring, with inner rings for Protein (teal), Carbs (blue `#3b82f6`), and Fat (orange).

**Data source:** `data/nutrition-log.json` (today's entries) + `config/health-config.json` (targets)

**Features:**
- Center of donut shows: calories consumed / target + remaining
- Rings animate on load (fill from 0 to current)
- Hover/tap on a ring shows the exact gram count
- Color shifts: teal when on track, orange when approaching limit, red (`#ef4444`) when over target
- Responsive — collapses to stacked bars on mobile

### 2. Visual Meal Log (Timeline)

**Component:** Vertical timeline showing each meal logged today, with the actual food photos displayed inline.

**Data source:** `data/nutrition-log.json` (today's entries, `photo_logged` field)

**Features:**
- Each entry shows: timestamp, meal type icon (☀️🌤️🌙🍎), food description, photo thumbnail (if available), macro breakdown
- Clicking a meal expands to show full details and the larger photo
- "Add meal" button at the bottom for quick logging
- Empty state: friendly prompt to snap their first photo

### 3. Weekly/Monthly Trends

**Component:** Dual-axis chart — smooth line chart for weight trend overlaid with bar chart for daily calorie adherence.

**Data source:** `data/nutrition-log.json` (aggregated by day) + `data/custom-metrics.json` (weight entries)

**Features:**
- Toggle between weekly and monthly views
- Calorie bars: teal when within ±10% of target, orange when over, gray when no data
- Weight line: smooth interpolation between logged data points
- Hover shows exact values for any day
- Average line (dashed) for quick reference

### 4. Macro Breakdown Chart

**Component:** Stacked bar chart showing daily protein/carbs/fat breakdown for the past 7 days.

**Data source:** `data/nutrition-log.json` (aggregated by day)

**Features:**
- Color-coded: Protein (teal `#14b8a6`), Carbs (blue `#3b82f6`), Fat (orange `#f97316`)
- Target lines (dashed horizontal) for each macro
- Percentage labels on each segment
- Click a day to see meal-by-meal breakdown

### 5. Hydration Tracker

**Component:** Horizontal progress bar with water drop animation.

**Data source:** `data/hydration-log.json` (today's entries)

**Features:**
- Shows current oz / target oz with percentage
- Fills with a water-wave animation effect
- Each glass logged appears as a small water drop icon on the bar
- Historical view: 7-day heat map showing hydration consistency
- Color: light blue (`#38bdf8`) to deep blue (`#1d4ed8`) gradient

### 6. Streak Tracker

**Component:** Prominent streak counter with calendar heat map.

**Data source:** `data/nutrition-log.json` (check for entries on consecutive days)

**Features:**
- Large number display: "🔥 18-day streak"
- GitHub-style contribution heat map for the past 90 days
- Each day colored by logging completeness: dark (no logs), light teal (partial), bright teal (fully tracked)
- Milestones highlighted: 7-day, 30-day, 60-day, 90-day badges
- Streak-break warning if today has no entries yet

### 7. Goal Progress Cards

**Component:** Grid of progress cards for each active goal.

**Data source:** `config/health-config.json` (goals) + computed from log data

**Features:**
- Each card shows: goal name, current value, target, progress bar, trend arrow (↑↓→)
- Supports custom goals from `custom_goals` array
- Cards for: calorie target, protein target, weight goal, hydration goal, supplement adherence
- Click to expand and see historical trend for that specific goal

### 8. Supplement Adherence

**Component:** Simple checklist with monthly adherence percentage.

**Data source:** `data/supplement-log.json`

**Features:**
- Today's checklist: each supplement with ✅ or ⬜
- Monthly adherence rate as a percentage ring
- Streak count for consecutive days with all supplements taken

### 9. Activity Feed

**Component:** Clean chronological feed of imported workouts and activities.

**Data source:** `data/activity-log.json`

**Features:**
- Each entry shows: activity type icon, name, duration, calories burned, source
- Weekly summary: total active minutes, total calories burned
- Integration badges showing where data came from (Apple Watch, Fitbit, manual)

---

## Database Schema (Supabase/Postgres)

For users who want persistent cloud-backed storage via the Nollio Dashboard:

```sql
-- Users table (links to auth)
CREATE TABLE health_users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id),
  user_name TEXT,
  calorie_target INTEGER DEFAULT 2000,
  protein_target_g INTEGER DEFAULT 150,
  carbs_target_g INTEGER DEFAULT 200,
  fat_target_g INTEGER DEFAULT 67,
  hydration_target_oz INTEGER DEFAULT 64,
  primary_goal TEXT DEFAULT 'maintain',
  activity_level TEXT DEFAULT 'active',
  units TEXT DEFAULT 'imperial',
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- Nutrition log
CREATE TABLE nutrition_entries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES health_users(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  meal_type TEXT NOT NULL CHECK (meal_type IN ('breakfast', 'lunch', 'dinner', 'snack')),
  description TEXT NOT NULL,
  photo_url TEXT,
  calories INTEGER NOT NULL,
  protein_g NUMERIC(6,1) NOT NULL,
  carbs_g NUMERIC(6,1) NOT NULL,
  fat_g NUMERIC(6,1) NOT NULL,
  fiber_g NUMERIC(6,1),
  logged_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX idx_nutrition_user_date ON nutrition_entries(user_id, date);

-- Hydration log
CREATE TABLE hydration_entries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES health_users(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  amount_oz NUMERIC(6,1) NOT NULL,
  logged_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX idx_hydration_user_date ON hydration_entries(user_id, date);

-- Supplement log
CREATE TABLE supplement_entries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES health_users(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  supplement_name TEXT NOT NULL,
  taken BOOLEAN DEFAULT true,
  logged_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX idx_supplement_user_date ON supplement_entries(user_id, date);

-- Activity log
CREATE TABLE activity_entries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES health_users(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  activity TEXT NOT NULL,
  duration_minutes INTEGER,
  calories_burned INTEGER,
  source TEXT DEFAULT 'manual',
  notes TEXT,
  logged_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX idx_activity_user_date ON activity_entries(user_id, date);

-- Custom metrics
CREATE TABLE custom_metrics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES health_users(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  metric_name TEXT NOT NULL,
  value NUMERIC(10,2) NOT NULL,
  note TEXT,
  logged_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX idx_metrics_user_date ON custom_metrics(user_id, date, metric_name);

-- Daily summaries (cached)
CREATE TABLE daily_summaries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES health_users(id) ON DELETE CASCADE,
  date DATE NOT NULL UNIQUE,
  total_calories INTEGER,
  total_protein_g NUMERIC(6,1),
  total_carbs_g NUMERIC(6,1),
  total_fat_g NUMERIC(6,1),
  total_water_oz NUMERIC(6,1),
  supplements_complete BOOLEAN,
  meals_logged INTEGER,
  generated_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX idx_summary_user_date ON daily_summaries(user_id, date);

-- RLS policies (enable row-level security)
ALTER TABLE health_users ENABLE ROW LEVEL SECURITY;
ALTER TABLE nutrition_entries ENABLE ROW LEVEL SECURITY;
ALTER TABLE hydration_entries ENABLE ROW LEVEL SECURITY;
ALTER TABLE supplement_entries ENABLE ROW LEVEL SECURITY;
ALTER TABLE activity_entries ENABLE ROW LEVEL SECURITY;
ALTER TABLE custom_metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE daily_summaries ENABLE ROW LEVEL SECURITY;
```

---

## Tech Stack

- **Framework:** Next.js 14+ (App Router)
- **Styling:** Tailwind CSS + custom dark theme
- **Charts:** Recharts or Chart.js (lightweight, responsive)
- **Database:** Supabase (Postgres) with Row Level Security
- **Auth:** Supabase Auth
- **Hosting:** Vercel

---

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `bg-primary` | `#0a0a0a` | Page background |
| `bg-card` | `#1a1a1a` | Card backgrounds |
| `bg-hover` | `#2a2a2a` | Hover states, borders |
| `accent-teal` | `#14b8a6` | Primary accent, on-track states |
| `accent-blue` | `#3b82f6` | Carbs, hydration, secondary |
| `accent-orange` | `#f97316` | Fat, warnings, active states |
| `accent-red` | `#ef4444` | Over-target, errors |
| `text-primary` | `#f5f5f5` | Primary text |
| `text-secondary` | `#a3a3a3` | Secondary/muted text |

---

## Cross-Sells (Dashboard Context)

- **Meal Planner Pro Dashboard:** Add meal planning visualization alongside nutrition tracking
- **Trainer Buddy Pro Dashboard:** Unified fitness + nutrition view
- **Dashboard Builder:** Full customization of layout, widgets, and themes
