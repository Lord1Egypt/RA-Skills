# Content Creator Pro — Dashboard Companion Kit

## Overview

The Content Creator Pro Dashboard is a visual command center for your social media content strategy. It replaces terminal-only interaction with a clean, modern web interface for planning, reviewing, and tracking content.

**Design Language:** Clean, modern, high whitespace. Pastel/muted pillar color tags. Grid-based calendar views. Card-based post previews. Mobile-responsive. Light mode default with optional dark mode.

---

## Modules

### 1. Content Calendar View

A 7-day visual grid showing planned posts across platforms.

**Features:**
- Week view (default) with day columns
- Month view toggle for long-range planning
- Each post appears as a card with: platform icon, pillar color tag, topic preview, posting time, status badge
- Click a card to expand full post content, hashtags, and CTA
- Drag-and-drop to reschedule posts between days
- Status indicators: 🟡 Draft → 🟢 Ready → ✅ Posted
- Filter by: platform, pillar, status
- "Add Post" button on each day slot

**Data Source:** `data/content-calendar/YYYY-MM-DD.json`

### 2. Drafts Library

Kanban-style board for content workflow management.

**Columns:**
- **💡 Ideas** — Raw ideas from the idea bank (`data/idea-bank.json`)
- **📝 Drafting** — Posts being refined (status: "draft")
- **✅ Ready to Post** — Approved content waiting to be published (status: "ready")
- **📤 Posted** — Published content with engagement data (status: "posted")

**Features:**
- Drag cards between columns to update status
- Click to view/edit full content
- Bulk actions: "Move all Ready to Posted"
- Search and filter across all columns

**Data Sources:** `data/idea-bank.json`, `data/content-calendar/*.json`

### 3. Platform Preview Mockups

Mobile phone frame mockups showing how content will appear natively on each platform.

**Supported Previews:**
- **X/Twitter:** Tweet card with avatar, handle, content, engagement buttons
- **LinkedIn:** Post card with profile header, content, hashtags, reaction bar
- **Instagram:** Photo frame with caption below, hashtag block, engagement icons

**Features:**
- Live preview updates as content is edited
- Character/word count with limit warnings
- "Copy to Clipboard" button per platform
- Side-by-side comparison of all platform versions

### 4. Pillar Distribution Tracker

Visual analytics showing content balance across pillars.

**Charts:**
- **Donut chart:** Current week's pillar distribution vs. targets
- **Stacked bar chart:** Pillar distribution over time (past 4 weeks)
- **Recommendation badge:** "Underweight: Thought Leadership — consider adding 1 more post this week"

**Data Sources:** `data/pillar-tracking.json`, `data/content-pillars.json`

### 5. Engagement Analytics

Performance tracking based on manually logged engagement data.

**Metrics:**
- Per-platform average engagement (likes, comments, shares)
- Best performing posts (top 5 by engagement)
- Best posting times (by engagement correlation)
- Trend lines: engagement over time
- Pillar performance comparison

**Charts:**
- Line chart: engagement trend over past 30 days
- Bar chart: average engagement by platform
- Heatmap: best performing days/times
- Comparison cards: this week vs. last week

**Data Source:** `data/engagement-log.json`

### 6. Brand Voice Profile Card

A summary view of the brand identity and voice settings.

**Displays:**
- Brand name, niche, target audience summary
- Voice parameters (formality, emoji frequency, humor style) as visual sliders
- Sample sentences
- Active platforms with toggle indicators
- Last updated date

**Data Source:** `data/brand-profile.json`

---

## Database Schema (Supabase/PostgreSQL)

For users who want to pair this dashboard with a hosted database:

```sql
-- Brand identity and voice settings
CREATE TABLE brand_profiles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL,
  brand_name TEXT NOT NULL,
  niche TEXT,
  value_proposition TEXT,
  target_audience JSONB DEFAULT '{}',
  voice JSONB DEFAULT '{}',
  platforms JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Recurring content themes with target distribution
CREATE TABLE content_pillars (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  brand_id UUID REFERENCES brand_profiles(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  description TEXT,
  target_ratio DECIMAL(3,2) DEFAULT 0.25,
  example_topics TEXT[],
  best_platforms TEXT[],
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Individual social media posts (planned, drafted, published)
CREATE TABLE posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  brand_id UUID REFERENCES brand_profiles(id) ON DELETE CASCADE,
  pillar_id UUID REFERENCES content_pillars(id) ON DELETE SET NULL,
  platform TEXT NOT NULL CHECK (platform IN ('x', 'linkedin', 'instagram', 'tiktok', 'facebook')),
  scheduled_date DATE,
  scheduled_time TIME,
  topic TEXT NOT NULL,
  content TEXT,
  hashtags TEXT[],
  cta TEXT,
  media_suggestion TEXT,
  status TEXT DEFAULT 'draft' CHECK (status IN ('idea', 'draft', 'ready', 'posted')),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Manually logged engagement metrics per post
CREATE TABLE engagement_metrics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  post_id UUID REFERENCES posts(id) ON DELETE CASCADE,
  impressions INTEGER DEFAULT 0,
  likes INTEGER DEFAULT 0,
  comments INTEGER DEFAULT 0,
  shares INTEGER DEFAULT 0,
  saves INTEGER DEFAULT 0,
  clicks INTEGER DEFAULT 0,
  performance TEXT CHECK (performance IN ('below_average', 'average', 'above_average', 'viral')),
  notes TEXT,
  logged_at TIMESTAMPTZ DEFAULT NOW()
);

-- Saved content ideas not yet assigned to calendar
CREATE TABLE idea_bank (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  brand_id UUID REFERENCES brand_profiles(id) ON DELETE CASCADE,
  idea TEXT NOT NULL,
  pillar_id UUID REFERENCES content_pillars(id) ON DELETE SET NULL,
  platform_hint TEXT,
  source TEXT DEFAULT 'user',
  used BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Brand voice adjustment history from user edits
CREATE TABLE voice_learnings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  brand_id UUID REFERENCES brand_profiles(id) ON DELETE CASCADE,
  original_snippet TEXT,
  edited_snippet TEXT,
  learning TEXT,
  applied_to TEXT[],
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Competitor analysis notes
CREATE TABLE competitor_notes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  brand_id UUID REFERENCES brand_profiles(id) ON DELETE CASCADE,
  competitor_name TEXT NOT NULL,
  platform TEXT,
  insights TEXT,
  content_gaps TEXT,
  analyzed_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for common queries
CREATE INDEX idx_posts_brand_date ON posts(brand_id, scheduled_date);
CREATE INDEX idx_posts_status ON posts(status);
CREATE INDEX idx_posts_platform ON posts(platform);
CREATE INDEX idx_engagement_post ON engagement_metrics(post_id);
CREATE INDEX idx_ideas_brand ON idea_bank(brand_id, used);
```

---

## Tech Stack Recommendation

- **Framework:** Next.js 14+ (App Router)
- **Styling:** Tailwind CSS + shadcn/ui components
- **Charts:** Recharts or Chart.js
- **Database:** Supabase (PostgreSQL) — matches NormieClaw standard stack
- **Auth:** Supabase Auth (email/magic link)
- **Drag & Drop:** @dnd-kit/core for calendar and kanban interactions
- **Phone Mockups:** CSS-only device frames (no external library)

---

## API Endpoints

```
GET    /api/calendar?week=YYYY-MM-DD     — Fetch week's posts
POST   /api/posts                         — Create new post
PATCH  /api/posts/:id                     — Update post (content, status, schedule)
DELETE /api/posts/:id                     — Delete post
GET    /api/pillars                       — List content pillars
GET    /api/engagement?range=30d          — Engagement metrics
GET    /api/ideas                         — List idea bank
POST   /api/ideas                         — Save new idea
GET    /api/brand                         — Get brand profile
PATCH  /api/brand                         — Update brand profile
```

---

## Build Notes

- Mobile-first responsive design — creators manage content from phones
- Optimistic UI updates for drag-and-drop (update locally, sync to DB)
- Export buttons on calendar view (CSV, markdown) mirror the CLI export script
- All platform preview components should be isolated/reusable
- Color-code pillars consistently across all views (calendar tags, donut chart, kanban labels)
