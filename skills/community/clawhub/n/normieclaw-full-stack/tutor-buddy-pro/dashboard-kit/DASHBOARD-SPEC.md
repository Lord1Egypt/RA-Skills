# Tutor Buddy Pro — Dashboard Companion Kit

**Product:** Parent Dashboard add-on for Tutor Buddy Pro
**Price:** $14.99 (order bump)
**Stack:** React (Next.js), TailwindCSS, Supabase (Postgres), Chart.js

---

## Overview

A visual dashboard that gives parents (or self-motivated students) real-time insights into learning progress. Track which topics are being mastered, where struggles persist, view quiz score trends, and monitor study habits — all in beautiful, easy-to-read charts.

---

## Database Schema

### `users`
| Column | Type | Notes |
|--------|------|-------|
| `id` | uuid (PK) | Auto-generated |
| `name` | varchar(100) | First name only (privacy) |
| `role` | enum('student', 'parent') | Determines dashboard view |
| `grade_level` | varchar(20) | e.g., "10th", "College Freshman" |
| `learning_style` | varchar(20) | visual, auditory, reading_writing, kinesthetic |
| `created_at` | timestamptz | |
| `updated_at` | timestamptz | |

### `sessions`
| Column | Type | Notes |
|--------|------|-------|
| `id` | uuid (PK) | |
| `user_id` | uuid (FK → users) | |
| `subject` | varchar(50) | math, science, history, english, etc. |
| `topic` | varchar(100) | e.g., "quadratic_equations" |
| `duration_minutes` | integer | |
| `session_type` | enum('tutoring', 'quiz', 'study_plan', 'review') | |
| `date` | date | |
| `created_at` | timestamptz | |

### `queries`
| Column | Type | Notes |
|--------|------|-------|
| `id` | uuid (PK) | |
| `session_id` | uuid (FK → sessions) | |
| `raw_text` | text | The problem text (OCR'd or typed) |
| `image_url` | text | NULL if typed, path if photo-submitted |
| `topic_tags` | text[] | Array of topic tags |
| `understanding_score` | integer (1-5) | 1=lost, 5=mastered. Agent-assessed. |
| `hint_levels_used` | integer | How many hint levels before correct answer |
| `created_at` | timestamptz | |

### `quiz_results`
| Column | Type | Notes |
|--------|------|-------|
| `id` | uuid (PK) | |
| `user_id` | uuid (FK → users) | |
| `subject` | varchar(50) | |
| `topic` | varchar(100) | |
| `questions_total` | integer | |
| `questions_correct` | integer | |
| `score_pct` | integer | |
| `difficulty_level` | varchar(20) | beginner, intermediate, advanced |
| `weak_areas` | text[] | Topics within the quiz that need work |
| `strong_areas` | text[] | Topics the student nailed |
| `time_minutes` | integer | |
| `date` | date | |
| `created_at` | timestamptz | |

### `mastery_tracking`
| Column | Type | Notes |
|--------|------|-------|
| `id` | uuid (PK) | |
| `user_id` | uuid (FK → users) | |
| `subject` | varchar(50) | |
| `topic_name` | varchar(100) | |
| `proficiency_pct` | integer (0-100) | |
| `proficiency_level` | enum('beginner', 'developing', 'proficient', 'advanced') | |
| `total_sessions` | integer | Sessions on this topic |
| `total_minutes` | integer | Time spent on this topic |
| `last_studied` | date | |
| `trend` | enum('improving', 'stable', 'declining') | Calculated from recent scores |
| `updated_at` | timestamptz | |

### `study_plans`
| Column | Type | Notes |
|--------|------|-------|
| `id` | uuid (PK) | |
| `user_id` | uuid (FK → users) | |
| `plan_name` | varchar(200) | e.g., "Algebra II Midterm Prep" |
| `exam_date` | date | |
| `subject` | varchar(50) | |
| `status` | enum('active', 'completed', 'abandoned') | |
| `daily_minutes` | integer | |
| `plan_data` | jsonb | Full plan structure |
| `created_at` | timestamptz | |
| `updated_at` | timestamptz | |

### `achievements`
| Column | Type | Notes |
|--------|------|-------|
| `id` | uuid (PK) | |
| `user_id` | uuid (FK → users) | |
| `achievement_id` | varchar(50) | References config achievements |
| `unlocked_at` | timestamptz | |

---

## Dashboard Components

### 1. `StudyHeatmap`
A GitHub-style contribution calendar showing days studied.
- **Data source:** `sessions` table, grouped by date
- **Visual:** Green squares for study days, gray for missed days. Darker green = more time.
- **Interaction:** Hover to see: "March 8 — 45 min (Algebra II: Quadratics)"

### 2. `TopicRadar`
A radar chart (Chart.js) showing proficiency across topics.
- **Data source:** `mastery_tracking` table
- **Visual:** Radar/spider chart with topic names around the perimeter, proficiency % as the data points.
- **Example:** Algebra 72%, Geometry 45%, Trigonometry 88%, Statistics 30%
- **Interaction:** Click a topic to drill down into quiz history for that topic.

### 3. `QuizScoreTrend`
A line chart showing quiz scores over time.
- **Data source:** `quiz_results` table, ordered by date
- **Visual:** Line chart with date on X-axis, score % on Y-axis. Color-coded by subject.
- **Trend line:** Moving average overlay to show improvement trajectory.

### 4. `RecentSessions`
A list view of recent tutoring sessions.
- **Data source:** `sessions` + `queries` tables
- **Visual:** Card list showing: date, subject, topic, duration, session type, understanding score.
- **Interaction:** Click to expand and see the specific problems worked on.

### 5. `StreakTracker`
Current study streak with motivational messaging.
- **Data source:** `sessions` table, consecutive date count
- **Visual:** Flame emoji + day count + motivational text. "🔥 12 day streak — keep it going!"
- **Milestones:** 7 days, 14 days, 30 days, 60 days, 100 days

### 6. `SubjectBreakdown`
Pie/donut chart showing time distribution across subjects.
- **Data source:** `sessions` table, summed by subject
- **Visual:** Donut chart with subject colors. Center shows total hours.

### 7. `WeeklyReport`
Auto-generated weekly summary card.
- **Data source:** Aggregated from all tables for the past 7 days
- **Content:**
  - Total study time
  - Topics covered
  - Quiz scores (average + best)
  - Improvement areas identified
  - Recommended focus for next week

### 8. `AchievementWall`
Display of unlocked achievements.
- **Data source:** `achievements` table
- **Visual:** Grid of achievement badges (emoji + name + date unlocked). Locked achievements shown grayed out.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dashboard/overview` | Aggregate stats (sessions, streak, avg score) |
| GET | `/api/dashboard/mastery` | All topic mastery data for radar chart |
| GET | `/api/dashboard/quizzes?limit=20` | Recent quiz results |
| GET | `/api/dashboard/sessions?days=30` | Session history |
| GET | `/api/dashboard/heatmap?months=6` | Study heatmap data |
| GET | `/api/dashboard/achievements` | Unlocked + available achievements |
| GET | `/api/dashboard/weekly-report` | This week's summary |
| POST | `/api/sync` | Ingest data from local JSON files |

---

## Data Sync Strategy

The skill runs locally and stores data in JSON files. The dashboard lives on the web. Bridge them:

1. **Manual sync:** User runs `scripts/generate-progress-report.sh` which can optionally POST to `/api/sync`.
2. **Periodic sync:** If the user has the Dashboard Builder skill, it can auto-sync on a schedule.
3. **Export format:** The sync endpoint accepts the same JSON schemas used in the local data files.

---

## Cross-Sells (In-Dashboard)

- **📚 Knowledge Vault** — "Save study notes alongside your progress" (sidebar link)
- **🧠 Supercharged Memory** — "Make your tutor remember everything across sessions" (settings page)
- **📊 Dashboard Builder** — "Build this dashboard for your own deployment" (footer CTA)
