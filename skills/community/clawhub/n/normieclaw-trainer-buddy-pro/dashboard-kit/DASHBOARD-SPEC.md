# Trainer Buddy Pro — Dashboard Companion Kit

**Build Spec for the Visual Dashboard Upsell**

*"Take your training out of the chat window. See your PRs climb."*

---

## Overview

A dark-mode, athletic-aesthetic web dashboard that visualizes workout history, progressive overload trends, PR tracking, and exercise analytics. Built on the same data files that Trainer Buddy Pro generates in chat.

---

## Design System

### Colors
- **Background:** Jet Black `#0A0A0A`
- **Surface/Card:** Dark Gray `#1A1A1A`
- **Border/Divider:** `#2A2A2A`
- **Primary Accent:** Electric Blue `#00F0FF`
- **Secondary Accent:** Neon Green `#39FF14`
- **PR Highlight:** Gold `#FFD700`
- **Text Primary:** White `#FFFFFF`
- **Text Secondary:** Gray `#9CA3AF`
- **Danger/Injury:** Red `#FF4444`

### Typography
- **Font Family:** Inter (primary), system-ui fallback
- **Headings:** Inter 700 (Bold)
- **Body:** Inter 400 (Regular)
- **Monospace (numbers/data):** JetBrains Mono or SF Mono

### General Rules
- All cards have `border-radius: 12px` and subtle `border: 1px solid #2A2A2A`
- Hover states: slight elevation (`box-shadow`) and border brightening
- Charts use Electric Blue as primary line color, Neon Green for targets/goals
- PRs always highlighted in Gold `#FFD700` with a subtle glow effect

---

## Component Breakdown

### 1. Overview Dashboard (`/`)

**OverviewCard (top row — 4 cards)**
| Card | Data Source | Display |
|------|------------|---------|
| Workouts This Week | `workout-log.json` — count entries this week | Large number + "of [target]" |
| Total Volume (lbs) | Sum of (weight × reps) across all sets this week | Large number + % change vs last week |
| Active Streak | Consecutive weeks with ≥1 workout | "🔥 X weeks" |
| Next PR Target | Highest-priority exercise approaching a PR | Exercise name + target weight/reps |

**Weekly Volume Chart**
- Bar chart: daily volume (weight × reps) for the current week
- X-axis: Mon-Sun, Y-axis: total volume in lbs
- Color: Electric Blue bars, with today's bar in Neon Green

**Recent Workouts (below cards)**
- List of last 5 workouts with: date, split day, duration, exercise count, total volume
- Click to expand full session details

---

### 2. Workout Log Viewer (`/workouts`)

**WorkoutLogViewer**
- Expandable list of all past sessions, newest first
- Each row shows: Date, Split Day, Duration, # Exercises, Total Volume
- Expanded view shows every exercise with sets/reps/weight/RPE
- Filter by: date range, split day, exercise name
- Search: find any exercise across all sessions

---

### 3. Progress Charts (`/progress`)

**ProgressChart — Per-Exercise Trend**
- Line chart showing weight progression over time for a selected exercise
- X-axis: dates, Y-axis: weight (lbs/kg)
- Data points: best set from each session (highest weight × reps)
- Secondary line: Estimated 1RM over time (Epley formula)
- Dropdown to select exercise
- Color: Electric Blue for weight, Neon Green for est. 1RM

**Volume Trend Chart**
- Line chart: weekly total volume over time
- Shows overall training load trends
- Useful for spotting deload needs

**Body Metrics Chart** (if body weight data is logged)
- Line chart: body weight over time
- Optional: body fat % overlay

---

### 4. Exercise Library (`/exercises`)

**ExerciseLibrary**
- Filterable list of all exercises the user has ever performed
- Each exercise card shows:
  - Exercise name
  - Muscle group
  - Times performed (total sessions)
  - Personal best: weight PR, rep PR, estimated 1RM
  - Last performed date
  - Trend indicator: ↑ improving, → plateau, ↓ declining
- Filter by: muscle group, equipment type, compound/isolation
- Sort by: name, frequency, PR, last performed

---

### 5. PR Board (`/prs`)

**PRBoard**
- Grid of personal records, organized by exercise
- Each PR card shows:
  - Exercise name
  - Weight PR (heaviest weight × reps achieved)
  - Rep PR (most reps at any weight)
  - Estimated 1RM
  - Date achieved
  - Gold glow effect on cards with PRs set in last 7 days
- Filter by: muscle group, date range
- Celebration animation on new PRs (subtle confetti or pulse effect)

---

## Database Schema (Supabase/PostgreSQL)

For users who want a persistent database instead of JSON files:

```sql
-- Users table
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  name TEXT,
  age INTEGER,
  gender TEXT,
  weight_lbs NUMERIC(5,1),
  height_in NUMERIC(4,1),
  experience_level TEXT DEFAULT 'beginner',
  primary_goal TEXT DEFAULT 'build_muscle',
  preferred_split TEXT DEFAULT 'full_body',
  training_days_per_week INTEGER DEFAULT 3,
  session_duration_minutes INTEGER DEFAULT 60,
  units TEXT DEFAULT 'imperial'
);

-- Injuries tracking
CREATE TABLE injuries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  area TEXT NOT NULL,
  severity TEXT DEFAULT 'mild',
  movements_to_avoid TEXT[],
  date_reported DATE DEFAULT CURRENT_DATE,
  date_resolved DATE,
  notes TEXT
);

-- Exercises reference
CREATE TABLE exercises (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL UNIQUE,
  muscle_group TEXT NOT NULL,
  movement_type TEXT, -- compound, accessory, isolation
  equipment_required TEXT[],
  description TEXT
);

-- Workouts (sessions)
CREATE TABLE workouts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  date DATE NOT NULL DEFAULT CURRENT_DATE,
  split_day TEXT NOT NULL,
  duration_minutes INTEGER,
  overall_notes TEXT,
  bodyweight_lbs NUMERIC(5,1),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Individual sets within a workout
CREATE TABLE workout_sets (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workout_id UUID REFERENCES workouts(id) ON DELETE CASCADE,
  exercise_id UUID REFERENCES exercises(id),
  exercise_name TEXT NOT NULL, -- denormalized for convenience
  set_number INTEGER NOT NULL,
  weight_lbs NUMERIC(6,1),
  reps INTEGER NOT NULL,
  rpe NUMERIC(3,1),
  notes TEXT
);

-- Body metrics over time
CREATE TABLE body_metrics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  date DATE NOT NULL DEFAULT CURRENT_DATE,
  weight_lbs NUMERIC(5,1),
  body_fat_pct NUMERIC(4,1),
  notes TEXT
);

-- Personal records (auto-calculated, materialized for fast reads)
CREATE TABLE personal_records (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  exercise_name TEXT NOT NULL,
  weight_pr_lbs NUMERIC(6,1),
  weight_pr_reps INTEGER,
  weight_pr_date DATE,
  rep_pr_weight NUMERIC(6,1),
  rep_pr_reps INTEGER,
  rep_pr_date DATE,
  estimated_1rm NUMERIC(6,1),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, exercise_name)
);

-- Indexes for performance
CREATE INDEX idx_workouts_user_date ON workouts(user_id, date DESC);
CREATE INDEX idx_workout_sets_workout ON workout_sets(workout_id);
CREATE INDEX idx_workout_sets_exercise ON workout_sets(exercise_name);
CREATE INDEX idx_body_metrics_user_date ON body_metrics(user_id, date DESC);
CREATE INDEX idx_personal_records_user ON personal_records(user_id);
```

---

## Tech Stack (Recommended)

- **Framework:** Next.js 14+ (App Router)
- **Styling:** Tailwind CSS + custom dark theme
- **Charts:** Recharts or Chart.js
- **Database:** Supabase (PostgreSQL) — or read directly from JSON files for local-only setups
- **Auth:** Supabase Auth (optional — single-user mode doesn't need it)
- **Deployment:** Vercel

---

## Data Flow

1. User trains and logs workouts via Trainer Buddy Pro in chat → data saved to `data/workout-log.json`
2. Dashboard reads from `data/workout-log.json` (local mode) OR syncs to Supabase (cloud mode)
3. PRs auto-calculated on each new workout entry
4. Charts update in real-time when new data is available

---

## Pages

| Route | Component | Data Source |
|-------|-----------|-------------|
| `/` | Overview Dashboard | workout-log, pr-history |
| `/workouts` | Workout Log Viewer | workout-log |
| `/workouts/[id]` | Single Workout Detail | workout-log (by index/id) |
| `/progress` | Progress Charts | workout-log, body-metrics |
| `/exercises` | Exercise Library | workout-log (aggregated) |
| `/prs` | PR Board | pr-history |
| `/profile` | User Profile Editor | user-profile |

---

*This spec is for the Dashboard Builder upsell (free.99). The core Trainer Buddy Pro skill ($9.99) works perfectly without it — the dashboard is for users who want to visualize their gains.*
