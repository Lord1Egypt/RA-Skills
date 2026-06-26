# Dashboard Spec: Travel Planner Pro

This document specifies the companion dashboard for Travel Planner Pro. While the skill works flawlessly in chat, the dashboard provides an interactive visual interface for managing trips, tracking budgets, and preparing for departure.

---

## Core Purpose

"Your agent plans the trip. Your dashboard is mission control — track your budget, check off your packing list, and access your daily itinerary in one gorgeous interface."

---

## Design System

### Theme
- **Vibe:** Adventurous and polished. Think passport blues, topographic map textures, warm accent lighting.
- **Typography:** Clean sans-serif (Inter or DM Sans). Bold headers, readable body text.
- **Photography:** Large hero images of destinations as section headers (sourced from Unsplash/Pexels API or user-uploaded).

### Colors
| Role | Color | Hex |
|------|-------|-----|
| Primary (nav, CTAs) | Deep Passport Blue | `#1e3a5f` |
| Secondary (accents) | Warm Amber | `#f59e0b` |
| Success (on track) | Emerald | `#10b981` |
| Warning (over budget) | Coral | `#ef4444` |
| Background | Off-White | `#fafaf9` |
| Card Background | White | `#ffffff` |
| Text Primary | Charcoal | `#1c1917` |
| Text Secondary | Slate | `#64748b` |
| Dark Mode BG | Deep Navy | `#0f172a` |

### Layout
- Responsive: mobile-first, works on phone during travel.
- Sidebar navigation on desktop, bottom tab bar on mobile.
- Cards-based layout with generous whitespace.

---

## Views & Features

### 1. Trip Overview (Home)

The landing page for each trip.

- **Hero Section:** Large destination photo, trip title, date range, countdown clock ("12 days until Tokyo! ✈️").
- **Weather Widget:** 5-day forecast pulled from Open-Meteo for the destination. Shows temp highs/lows and precipitation icons.
- **Quick Stats Row:**
  - Total budget: $3,000
  - Estimated spend: $2,800
  - Days: 5
  - Travelers: 2
- **Upcoming Activity Card:** Shows the next activity on the itinerary (time, location, notes).
- **Quick Actions:** "View Itinerary" / "Packing List" / "Budget" / "Share Trip"

### 2. Itinerary Tab

Interactive timeline view of the full trip.

- **Day Selector:** Horizontal scrollable day pills (Day 1, Day 2, ... ) with weather icons.
- **Activity Cards:** Collapsible cards for each time block (Morning / Afternoon / Evening).
  - Each card shows: time, activity title, location, cost estimate, transit notes.
  - Rain-friendly badge (☂️) on indoor activities.
  - Restaurant cards include: cuisine, price range, dietary notes, and a "directions" link.
- **Map Integration:** Optional embedded map showing the day's locations as pins with a suggested walking route.
- **Edit Mode:** Tap an activity to swap or remove it (sends update to the agent data file).

### 3. Budget Tracker Tab

Visual budget management.

- **Burn-Down Chart:** Line chart showing budget spent over time vs. the total budget ceiling. X-axis: trip days. Y-axis: cumulative spend.
- **Category Breakdown:** Horizontal stacked bar or donut chart showing spend by category (flights, accommodation, food, activities, transit, buffer).
- **Category Cards:** For each budget category:
  - Estimated amount
  - Booked/actual amount
  - Status indicator (green = under budget, amber = nearing limit, red = over)
  - Percentage of total budget
- **Buffer Indicator:** Visual display of remaining buffer funds. Turns amber below 50%, red below 20%.
- **Add Expense:** Quick-add button to log actual expenses during the trip (syncs with Expense Report Pro if installed).

### 4. Packing & Prep Tab

Checkbox-driven preparation tracker.

- **Packing List:** Organized by category (Documents, Clothing, Electronics, Toiletries, Health, Day Bag, Digital Prep). Each item has:
  - Checkbox (persisted — check on phone, see on desktop)
  - Item name
  - Notes (conditional — e.g., "Japan uses Type A")
- **Progress Bar:** Shows "14/23 items packed" with percentage.
- **Document Checklist:** Separate section for visa, passport, insurance, confirmations.
  - Status indicators: ✅ Ready / ⚠️ Action Needed / ❌ Missing
  - Due dates for time-sensitive items (visa application deadline, etc.)
- **Pre-Trip Reminders:** Timeline of upcoming tasks based on departure date (from trip-reminder.sh logic):
  - 30 days: Visa & docs
  - 21 days: Insurance
  - 7 days: Packing review, bank notification
  - 3 days: Weather check, offline maps
  - 1 day: Flight check-in, final checklist

### 5. Local Intel Tab

Destination reference guide.

- **Sections:** Tipping customs, transit tips, cultural notes, safety, money & payments, connectivity, useful phrases, food highlights.
- **Formatted as scannable cards** — travelers will reference this on their phone while abroad.
- **Emergency Info Card:** Pinned at top — embassy number, emergency services (110 police, 119 fire/ambulance in Japan), hotel address in local language.

### 6. Trip Archive

History of completed trips.

- **Trip Cards:** Destination photo, dates, rating (❤️/👍/👎), total actual spend.
- **Click to expand:** Full itinerary, budget actuals vs. estimates, post-trip notes.
- **Stats:** Total trips taken, total countries visited, favorite destination, average trip spend.

---

## Database Schema (Supabase / PostgreSQL)

```sql
-- User travel profile
CREATE TABLE travel_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users NOT NULL,
    pace_preference VARCHAR(20) DEFAULT 'balanced',
    budget_style VARCHAR(20) DEFAULT 'value',
    hotel_style VARCHAR(50),
    dietary_needs TEXT,
    home_airport VARCHAR(10),
    passport_valid_through DATE,
    travel_pet_peeves TEXT[],
    learned_preferences JSONB DEFAULT '{}',
    past_destinations TEXT[] DEFAULT '{}',
    bucket_list TEXT[] DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Trips
CREATE TABLE trips (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    profile_id UUID REFERENCES travel_profiles(id) NOT NULL,
    trip_id VARCHAR(100) UNIQUE NOT NULL,
    destination VARCHAR(255) NOT NULL,
    cities TEXT[] DEFAULT '{}',
    multi_city BOOLEAN DEFAULT false,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    budget_total NUMERIC(10,2),
    budget_currency VARCHAR(3) DEFAULT 'USD',
    status VARCHAR(20) DEFAULT 'planning',
    accommodation JSONB,
    flights JSONB,
    local_intel JSONB,
    trip_rating VARCHAR(20),
    post_trip_notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Trip days (itinerary)
CREATE TABLE trip_days (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trip_id UUID REFERENCES trips(id) ON DELETE CASCADE NOT NULL,
    day_number INTEGER NOT NULL,
    date DATE NOT NULL,
    title VARCHAR(255),
    weather JSONB,
    daily_cost_estimate NUMERIC(10,2),
    UNIQUE(trip_id, day_number)
);

-- Activities per day
CREATE TABLE activities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    day_id UUID REFERENCES trip_days(id) ON DELETE CASCADE NOT NULL,
    time_slot VARCHAR(20) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    location VARCHAR(255),
    transit_notes TEXT,
    cost_estimate NUMERIC(10,2) DEFAULT 0,
    rain_friendly BOOLEAN DEFAULT false,
    restaurant JSONB,
    sort_order INTEGER DEFAULT 0
);

-- Budget tracking
CREATE TABLE trip_budgets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trip_id UUID REFERENCES trips(id) ON DELETE CASCADE NOT NULL,
    category VARCHAR(50) NOT NULL,
    estimated NUMERIC(10,2) DEFAULT 0,
    booked NUMERIC(10,2) DEFAULT 0,
    actual NUMERIC(10,2) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'estimated',
    UNIQUE(trip_id, category)
);

-- Packing list items
CREATE TABLE packing_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trip_id UUID REFERENCES trips(id) ON DELETE CASCADE NOT NULL,
    category VARCHAR(50) NOT NULL,
    item VARCHAR(255) NOT NULL,
    packed BOOLEAN DEFAULT false,
    notes TEXT,
    sort_order INTEGER DEFAULT 0
);

-- Travel companions
CREATE TABLE companions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    profile_id UUID REFERENCES travel_profiles(id) ON DELETE CASCADE NOT NULL,
    name VARCHAR(100) NOT NULL,
    relationship VARCHAR(50),
    dietary_needs TEXT,
    pace_preference VARCHAR(20),
    notes TEXT
);

-- Loyalty programs
CREATE TABLE loyalty_programs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    profile_id UUID REFERENCES travel_profiles(id) ON DELETE CASCADE NOT NULL,
    program VARCHAR(100) NOT NULL,
    tier VARCHAR(50),
    member_number VARCHAR(50)
);
```

### Row Level Security

```sql
ALTER TABLE travel_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE trips ENABLE ROW LEVEL SECURITY;
ALTER TABLE trip_days ENABLE ROW LEVEL SECURITY;
ALTER TABLE activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE trip_budgets ENABLE ROW LEVEL SECURITY;
ALTER TABLE packing_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE companions ENABLE ROW LEVEL SECURITY;
ALTER TABLE loyalty_programs ENABLE ROW LEVEL SECURITY;

-- All tables follow the same pattern: users access only their own data
CREATE POLICY "Users access own travel_profiles" ON travel_profiles
    FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users access own trips" ON trips
    FOR ALL USING (
        profile_id IN (SELECT id FROM travel_profiles WHERE user_id = auth.uid())
    );

CREATE POLICY "Users access own trip_days" ON trip_days
    FOR ALL USING (
        trip_id IN (SELECT id FROM trips WHERE profile_id IN (SELECT id FROM travel_profiles WHERE user_id = auth.uid()))
    );

-- Repeat pattern for activities, trip_budgets, packing_items, companions, loyalty_programs
CREATE POLICY "Users access own activities" ON activities
    FOR ALL USING (
        day_id IN (SELECT id FROM trip_days WHERE trip_id IN (SELECT id FROM trips WHERE profile_id IN (SELECT id FROM travel_profiles WHERE user_id = auth.uid())))
    );

CREATE POLICY "Users access own trip_budgets" ON trip_budgets
    FOR ALL USING (
        trip_id IN (SELECT id FROM trips WHERE profile_id IN (SELECT id FROM travel_profiles WHERE user_id = auth.uid()))
    );

CREATE POLICY "Users access own packing_items" ON packing_items
    FOR ALL USING (
        trip_id IN (SELECT id FROM trips WHERE profile_id IN (SELECT id FROM travel_profiles WHERE user_id = auth.uid()))
    );

CREATE POLICY "Users access own companions" ON companions
    FOR ALL USING (
        profile_id IN (SELECT id FROM travel_profiles WHERE user_id = auth.uid())
    );

CREATE POLICY "Users access own loyalty_programs" ON loyalty_programs
    FOR ALL USING (
        profile_id IN (SELECT id FROM travel_profiles WHERE user_id = auth.uid())
    );
```

### Indexes

```sql
CREATE INDEX idx_trips_profile ON trips(profile_id);
CREATE INDEX idx_trips_status ON trips(status);
CREATE INDEX idx_trips_dates ON trips(start_date, end_date);
CREATE INDEX idx_trip_days_trip ON trip_days(trip_id);
CREATE INDEX idx_activities_day ON activities(day_id);
CREATE INDEX idx_packing_trip ON packing_items(trip_id);
CREATE INDEX idx_budgets_trip ON trip_budgets(trip_id);
```

---

## Data Sync

The dashboard reads from the same data the chat agent writes:

- **Chat → Dashboard:** Agent writes trip JSON files. Dashboard import script reads these and upserts into Supabase.
- **Dashboard → Chat:** User checks packing items or logs expenses in the dashboard. Agent reads updated state on next interaction.
- **Sync script:** A lightweight Node.js script that watches `travel/trips/` for changes and syncs to Supabase. Runs as a background process or on-demand.

---

## Mobile Optimization

This dashboard WILL be used on phones during travel. Design accordingly:

- Large tap targets (44px minimum)
- Offline-capable where possible (cache itinerary and packing list in localStorage)
- Quick-access packing checklist (no more than 2 taps from home)
- Dark mode for nighttime use
- Compact cards that don't require horizontal scrolling
