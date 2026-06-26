# Relationship Buddy — Dashboard Companion Kit

**Upsell Pitch:** *"Works great in chat alone. Add the Dashboard Kit for a beautiful visual overview of your relationships."*

---

## Design Philosophy

Warm, intimate, and modern. This is NOT Salesforce. It's a beautifully designed digital scrapbook for the people you love. Dark theme base with NormieClaw's signature Teal (#14b8a6) and Orange (#f97316) accents.

- **Typography:** Clean sans-serif (Inter or similar), generous whitespace
- **Cards:** Rounded corners, soft shadows, subtle hover animations
- **Color coding:** 🟢 Teal for thriving, 🟡 Orange for needs attention, 🔴 Warm red for at risk
- **Feel:** Like opening a beautiful notebook about the people who matter most

---

## Pages & Components

### 1. Dashboard Home (`/relationships`)

**People Cards Grid:**
- Visual cards for each contact, sorted by urgency (who needs attention first)
- Each card shows:
  - Name and relationship label
  - Category badge (inner circle, close friend, etc.)
  - Next upcoming date (birthday, anniversary) with countdown
  - Last interaction: "3 days ago — lunch downtown"
  - Health indicator ring (🟢🟡🔴) — subtle glowing/fading effect
  - Quick action buttons: "Log Interaction" | "Gift Ideas" | "View Profile"
- Optional avatar/photo placeholder (user can upload)
- Search and filter bar: by category, tag, health status

**Upcoming Dates Sidebar (or top strip):**
- Next 30 days of birthdays, anniversaries, custom dates
- Grouped by week
- Click to jump to that contact's profile
- Badge count of dates needing action (gift not bought, card not sent)

### 2. Contact Profile Page (`/relationships/:id`)

**Header:**
- Name, relationship, category
- Health score with visual ring
- Last interaction date + summary
- "Days since contact" counter

**Tabs:**

**Overview Tab:**
- Key dates list with countdown timers
- Preferences grid (foods, drinks, hobbies, sizes, dislikes)
- Family tree (simple list with names and relations)
- Tags

**Interaction Timeline Tab:**
- Chronological feed of all logged interactions
- Each entry: date, type icon (📞📱🤝📧🎁), summary, mood indicator
- Filter by type, date range
- "Log New" button

**Gift History Tab:**
- All gifts given/received with dates, occasions, reactions
- "Loved it" / "Meh" / "Missed" badges
- Gift idea bookmarks (saved suggestions not yet purchased)
- "Generate Ideas" button

**Life Events Tab:**
- Timeline of major life events
- Follow-up status indicators (completed ✅ / pending ⏳ / overdue 🔴)
- Add new event button

**Notes Tab:**
- Free-form notes area
- Searchable
- Timestamped entries

### 3. Relationship Health Overview (`/relationships/health`)

**Visual health map:**
- Concentric rings layout:
  - Center: User
  - Ring 1: Inner circle contacts
  - Ring 2: Close friends
  - Ring 3: Extended family
  - Ring 4+: Friends, acquaintances, professional
- Each contact is a dot/avatar on their ring
- Color: teal (thriving) → orange (needs attention) → red (at risk)
- Glow intensity fades as health drops
- Click any dot to jump to profile

**Health Trends Chart:**
- Line chart showing overall relationship health score over time (30/60/90 day view)
- Per-category breakdown available

**Action Queue:**
- Sorted list of "reach out" suggestions, most urgent first
- One-click "Log Interaction" to mark as done
- Snooze option (push reminder 1 week)

### 4. Calendar View (`/relationships/calendar`)

**Monthly calendar:**
- All key dates plotted
- Color-coded by type (birthday 🎂, anniversary 💍, custom ⭐)
- Click date to see contacts + suggested actions
- Today highlighted with pending reminders

---

## Database Schema (Supabase / Postgres)

```sql
-- Contacts table
CREATE TABLE rb_contacts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id),
  name TEXT NOT NULL,
  nickname TEXT,
  relationship TEXT,
  category TEXT DEFAULT 'friends',
  preferences JSONB DEFAULT '{}',
  family JSONB DEFAULT '[]',
  notes TEXT,
  tags TEXT[] DEFAULT '{}',
  status TEXT DEFAULT 'active', -- active, memorial, archived
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- Key dates (birthdays, anniversaries, custom)
CREATE TABLE rb_key_dates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  contact_id UUID NOT NULL REFERENCES rb_contacts(id) ON DELETE CASCADE,
  label TEXT NOT NULL,
  date DATE NOT NULL,
  remind_days_before INTEGER DEFAULT 7,
  recurring BOOLEAN DEFAULT true
);

-- Interactions log
CREATE TABLE rb_interactions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  contact_id UUID NOT NULL REFERENCES rb_contacts(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES auth.users(id),
  interaction_date DATE NOT NULL,
  type TEXT NOT NULL, -- call, text, in_person, video_call, etc.
  summary TEXT,
  mood TEXT, -- great, good, neutral, tough
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Follow-ups
CREATE TABLE rb_follow_ups (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  contact_id UUID NOT NULL REFERENCES rb_contacts(id) ON DELETE CASCADE,
  interaction_id UUID REFERENCES rb_interactions(id),
  action TEXT NOT NULL,
  due_date DATE,
  status TEXT DEFAULT 'pending', -- pending, completed, snoozed
  completed_at TIMESTAMPTZ
);

-- Life events
CREATE TABLE rb_life_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  contact_id UUID NOT NULL REFERENCES rb_contacts(id) ON DELETE CASCADE,
  event_date DATE NOT NULL,
  description TEXT NOT NULL,
  follow_up BOOLEAN DEFAULT false,
  follow_up_status TEXT DEFAULT 'pending'
);

-- Gift history
CREATE TABLE rb_gifts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  contact_id UUID NOT NULL REFERENCES rb_contacts(id) ON DELETE CASCADE,
  gift_date DATE NOT NULL,
  occasion TEXT,
  description TEXT NOT NULL,
  price DECIMAL(10,2),
  reaction TEXT, -- loved_it, liked_it, neutral, missed
  notes TEXT
);

-- Reminders
CREATE TABLE rb_reminders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  contact_id UUID NOT NULL REFERENCES rb_contacts(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES auth.users(id),
  type TEXT NOT NULL, -- birthday, anniversary, check_in, follow_up, custom
  trigger_date DATE NOT NULL,
  message TEXT,
  status TEXT DEFAULT 'pending', -- pending, sent, completed, snoozed
  gift_suggestions JSONB DEFAULT '[]'
);

-- Relationship health scores (cached, recalculated periodically)
CREATE TABLE rb_health_scores (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  contact_id UUID NOT NULL REFERENCES rb_contacts(id) ON DELETE CASCADE,
  score DECIMAL(3,2) NOT NULL, -- 0.00 to 1.00
  level TEXT NOT NULL, -- thriving, needs_attention, at_risk
  calculated_at TIMESTAMPTZ DEFAULT now()
);

-- Indexes
CREATE INDEX idx_rb_contacts_user ON rb_contacts(user_id);
CREATE INDEX idx_rb_contacts_category ON rb_contacts(user_id, category);
CREATE INDEX idx_rb_interactions_contact ON rb_interactions(contact_id, interaction_date DESC);
CREATE INDEX idx_rb_key_dates_date ON rb_key_dates(date);
CREATE INDEX idx_rb_reminders_trigger ON rb_reminders(user_id, trigger_date, status);
CREATE INDEX idx_rb_health_scores_contact ON rb_health_scores(contact_id, calculated_at DESC);

-- Row Level Security
ALTER TABLE rb_contacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE rb_key_dates ENABLE ROW LEVEL SECURITY;
ALTER TABLE rb_interactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE rb_follow_ups ENABLE ROW LEVEL SECURITY;
ALTER TABLE rb_life_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE rb_gifts ENABLE ROW LEVEL SECURITY;
ALTER TABLE rb_reminders ENABLE ROW LEVEL SECURITY;
ALTER TABLE rb_health_scores ENABLE ROW LEVEL SECURITY;

-- RLS Policies (user can only access their own data)
CREATE POLICY "Users see own contacts" ON rb_contacts
  FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users see own interactions" ON rb_interactions
  FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users see own reminders" ON rb_reminders
  FOR ALL USING (auth.uid() = user_id);

-- Key dates, life events, gifts, follow-ups, health scores
-- access controlled through contact ownership (JOIN to rb_contacts)
CREATE POLICY "Users see own key_dates" ON rb_key_dates
  FOR ALL USING (contact_id IN (SELECT id FROM rb_contacts WHERE user_id = auth.uid()));

CREATE POLICY "Users see own life_events" ON rb_life_events
  FOR ALL USING (contact_id IN (SELECT id FROM rb_contacts WHERE user_id = auth.uid()));

CREATE POLICY "Users see own gifts" ON rb_gifts
  FOR ALL USING (contact_id IN (SELECT id FROM rb_contacts WHERE user_id = auth.uid()));

CREATE POLICY "Users see own follow_ups" ON rb_follow_ups
  FOR ALL USING (contact_id IN (SELECT id FROM rb_contacts WHERE user_id = auth.uid()));

CREATE POLICY "Users see own health_scores" ON rb_health_scores
  FOR ALL USING (contact_id IN (SELECT id FROM rb_contacts WHERE user_id = auth.uid()));
```

---

## API Endpoints (Next.js App Router)

```
GET    /api/relationships              — List contacts (filterable)
GET    /api/relationships/:id          — Contact detail
POST   /api/relationships              — Create contact
PATCH  /api/relationships/:id          — Update contact
DELETE /api/relationships/:id          — Soft delete (archive)

GET    /api/relationships/:id/interactions  — Interaction history
POST   /api/relationships/:id/interactions  — Log interaction

GET    /api/relationships/:id/gifts    — Gift history
POST   /api/relationships/:id/gifts    — Log gift

GET    /api/relationships/health       — All health scores
GET    /api/relationships/calendar     — Upcoming dates (next N days)
GET    /api/relationships/reminders    — Active reminders

POST   /api/relationships/import       — Bulk import from CSV/JSON
```

---

## Tech Stack

- **Frontend:** Next.js 14+ (App Router), React, Tailwind CSS
- **Database:** Supabase (Postgres) with Row Level Security
- **Charts:** Recharts or Chart.js for health trends
- **Calendar:** Custom component or react-big-calendar
- **Animations:** Framer Motion for card transitions and health ring effects

---

*This spec is for the Dashboard Companion Kit add-on. The core Relationship Buddy skill works entirely in chat without any dashboard.*
