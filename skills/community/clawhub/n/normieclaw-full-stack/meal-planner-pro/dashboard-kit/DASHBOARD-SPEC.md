# Meal Planner Pro — Dashboard Companion Kit

## Customer-Facing Copy

**Your Kitchen's Command Center.**

The Meal Planner Pro Dashboard isn't just a viewer — it's where you plan, organize, shop, and cook. A warm, beautiful interface designed for the kitchen counter, the couch on Thursday night, or the grocery store aisle.

**What You Get:**
- **Interactive Weekly Planner** — Drag-and-drop meals, toggle who's eating, mark busy days, flag special occasions.
- **Visual Meal Calendar** — Color-coded week at a glance. Tap any meal for the full recipe, ingredients, and per-person ratings.
- **Smart Grocery Lists** — Organized by store section, with checkboxes, pantry awareness, and estimated totals. Take it shopping on your phone.
- **Household Profiles** — Manage taste preferences, allergies, and adventurousness per person. Watch the AI learn over time.
- **Favorites Library** — Every ❤️ meal builds your family's personal cookbook. Filter by person, cuisine, or time since last served.
- **Prep Day Planner** — A timed, step-by-step Sunday prep schedule generated from your actual meal plan.
- **Freezer Inventory** — Track what's frozen, when it went in, and let the AI use it before it goes bad.
- **Recipe Discovery** — Browse trending recipes, flag them for next week's plan.

🛡️ **Codex Security Verified** — Your family's dietary data stays on your infrastructure. No third-party data harvesting.

---

## Internal Build Specification

### Stack
- **Framework:** Next.js (App Router)
- **Database:** Supabase (PostgreSQL) — *Fallback: SQLite for zero-config local setups*
- **Styling:** Tailwind CSS + shadcn/ui (customized for warm kitchen aesthetic)
- **Drag & Drop:** dnd-kit or @hello-pangea/dnd (touch-friendly)
- **Charts:** Chart.js (nutrition tracking, spending trends)

---

### Design System: "Warm Kitchen"

| Token | Value | Usage |
|-------|-------|-------|
| Background | `#FFFBF5` (warm white) | Page background |
| Surface | `#FFFFFF` | Cards, panels |
| Primary | `#E87461` (warm coral) | Buttons, accents, active states |
| Secondary | `#F4A261` (honey) | Highlights, hover states |
| Success / Loved | `#6BCB77` (fresh green) | ❤️ ratings, confirmations |
| Warning / OK | `#FFD166` (warm yellow) | 👍 ratings, alerts |
| Error / Hated | `#EF476F` (soft red) | 👎 ratings, errors |
| Text Primary | `#2D2D2D` | Body text |
| Text Muted | `#8B8B8B` | Secondary text, timestamps |
| Breakfast | `#FEF3C7` (warm yellow) | Meal type color coding |
| Lunch | `#D1FAE5` (fresh green) | Meal type color coding |
| Dinner | `#FED7AA` (rich coral) | Meal type color coding |
| Snack | `#EDE9FE` (light purple) | Meal type color coding |
| Dessert | `#FECDD3` (soft pink) | Meal type color coding |

**Typography:**
- Headings: DM Serif Display (warm, editorial feel)
- Body: Inter (clean, readable at all sizes)
- Quantities/Numbers: JetBrains Mono (precise, scannable)

**Design Principles:**
- Round corners everywhere (16px cards, 12px buttons) — nothing sharp or clinical
- Soft shadows, no hard borders
- Food photography as visual anchors wherever possible
- Generous whitespace — this is a kitchen tool, not a spreadsheet
- Touch targets ≥ 44px (mobile-first, designed for greasy fingers)

### Mobile Navigation

Bottom navigation on mobile:

```
┌──────────────────────────────────┐
│         [Page Content]           │
├──────────────────────────────────┤
│  📅      🗓️      🔍     🛒    ⋯ │
│  Plan   Calendar  Find  Grocery More│
└──────────────────────────────────┘
```

"More" expands to: Family Profiles, Freezer, Prep Planner, Favorites, Settings

---

## Views

### View A: Weekly Planning Grid (The Planning Screen)

This is the INTERACTIVE planning view — where the user configures the week BEFORE the AI generates. Not read-only.

```
┌─────────────────────────────────────┐
│  Week of March 9–15        [< >]    │
│  Partner traveling: Tue–Thu  [Edit] │
├─────┬─────┬─────┬─────┬─────┬──────┤
│     │ Mon │ Tue │ Wed │ Thu │ ...  │
├─────┼─────┼─────┼─────┼─────┼──────┤
│ 🌅  │ All │ M K │ M K │ M K │      │
│ BRK │     │     │     │     │      │
├─────┼─────┼─────┼─────┼─────┼──────┤
│ 🥪  │ All │ M K │ M K │ M K │      │
│ LUN │K:🎒 │K:🏫 │K:🎒 │K:🏫 │      │
├─────┼─────┼─────┼─────┼─────┼──────┤
│ 🍽️  │ All │ M K │ M K │ M K │      │
│ DIN │     │     │     │     │      │
├─────┼─────┼─────┼─────┼─────┼──────┤
│ 🍎  │ K   │ K   │ K   │ K   │      │
│ SNK │     │     │     │     │      │
└─────┴─────┴─────┴─────┴─────┴──────┘
│  [🥗 Dietary Prefs]  [🏪 Stores]   │
│  [⚡ Quick: Mon,Wed]  [🎂 Fri=Bday]│
│                                      │
│  [✨ Generate Meal Plan]             │
└──────────────────────────────────────┘
```

**Interactions:**
- Tap member pills to toggle who's eating each meal
- Tap a day header to mark as "busy day" (quick meals only)
- Long-press a cell to copy config to another day
- Travel toggle auto-removes a member from all meals on those days (with override)
- Special day flags (🎂 birthday, 💑 date night, 🎉 hosting guests) change AI behavior
- "Same as last week" copies the WHO configuration (not the meals)
- Dietary preference panel: collapsible toggles for this week's overrides
- Store selector: pick primary + specialty stores, assign roles

### View B: Meal Calendar (The Home Screen — Post-Generation)

After the AI generates (or user finalizes), this is the daily view. Scrollable vertical list, Mon–Sun.

```
┌──────────────────────────────────────────────┐
│  📅 March 9–15                   [🖨️ Print]  │
│                                               │
│  ┌─────────────────────────────────────────┐  │
│  │   MONDAY                                │  │
│  │─────────────────────────────────────────│  │
│  │ 🌅 Overnight Oats              All 4    │  │
│  │   w/ berries & honey                    │  │
│  │   ⏱ 5 min prep (night before)           │  │
│  │                                          │  │
│  │ 🥪 Turkey & Cheese Wraps       All 4    │  │
│  │   + apple slices & pretzels             │  │
│  │   Kids: 🎒 packed                       │  │
│  │   ⏱ 10 min                              │  │
│  │                                          │  │
│  │ 🍽️ One-Pan Lemon Chicken       All 4    │  │
│  │   w/ roasted broccoli & rice            │  │
│  │   ⏱ 15 min prep, 25 min cook           │  │
│  │   💡 Make extra chicken for Wed lunch    │  │
│  │   ⭐ Family confidence: 92%             │  │
│  │   [❤️] [👍] [👎]  per person →          │  │
│  │                                          │  │
│  │ 🍎 Apple slices + PB           Kids     │  │
│  └─────────────────────────────────────────┘  │
│                                               │
│  ── Chat with your agent ──                  │
│  💬 "Swap Tuesday dinner for something        │
│      without fish — kid's been anti-fish"     │
│                                               │
│  🤖 "Done! Swapped to Chicken Taco Bowls —   │
│      rated ❤️ last month. Updated your        │
│      grocery list too. ✨"                    │
│                                               │
│  [Type a message...]                    [→]   │
└──────────────────────────────────────────────┘
```

**Interactions:**
- Tap any meal to expand detail modal (full recipe, ingredients, per-person rating buttons)
- Chat drawer at bottom for real-time refinement
- Suggested chips: "Make it easier" / "More variety" / "Budget swap" / "Kid-friendlier" / "Surprise me"
- Swipe between weeks
- Print view: clean, ink-friendly layout for sticking on the fridge

### View B.1: Meal Detail Modal (Tap Any Meal)

```
┌──────────────────────────────────┐
│  🍽️ One-Pan Lemon Chicken       │
│  ⭐ Family confidence: 92%       │
│                                  │
│  ⏱ Prep: 15 min | Cook: 25 min  │
│  👥 Serves: 4 (+ leftover for   │
│     Wed lunch)                   │
│                                  │
│  📝 Ingredients                  │
│  • 2 lbs chicken thighs         │
│  • 2 heads broccoli             │
│  • 2 lemons                     │
│  • 3 cloves garlic              │
│  • Olive oil, salt, pepper      │
│  • 1.5 cups rice                │
│                                  │
│  📖 Instructions                 │
│  1. Preheat oven to 425°F...    │
│  2. Season chicken with...      │
│  3. Arrange on sheet pan...     │
│                                  │
│  ── Rate This Meal ──           │
│  Mom:   [❤️] [👍] [👎]          │
│  Dad:   [❤️] [👍] [👎]          │
│  Kid 1: [❤️] [👍] [👎]          │
│  Kid 2: [❤️] [👍] [👎]          │
│                                  │
│  📝 Notes: _______________      │
│  "Kid ate all the chicken but    │
│   picked out the broccoli"       │
│                                  │
│  [🔄 Swap This Meal]            │
│  [📌 Save to Favorites]         │
└──────────────────────────────────┘
```

### View C: Smart Grocery List

```
┌──────────────────────────────────┐
│  🛒 Grocery List — March 9–15   │
│  Est. total: ~$145               │
│                                  │
│  [All] [🟢 Whole Foods] [🔵 KS] │
│                                  │
│  ── 🟢 Whole Foods (~$85) ──    │
│                                  │
│  🥬 Produce                     │
│  ☐ Broccoli (2 heads)           │
│  ☐ Baby spinach (1 bag, 5oz)    │
│  ☐ Avocados (4)                 │
│  ☑ Lemons (3) — ✋ Already have │
│                                  │
│  🥩 Meat & Seafood              │
│  ☐ Chicken thighs (3.5 lbs)    │
│     ↳ Mon dinner + Wed lunch    │
│  ☐ Ground turkey (1 lb)         │
│                                  │
│  🧀 Dairy                       │
│  ☐ Shredded cheddar (8oz)       │
│  ☐ Greek yogurt (32oz)          │
│                                  │
│  📦 Pantry                      │
│  ☑ Olive oil — 🏠 Staple        │
│  ☑ Salt & pepper — 🏠 Staple    │
│  ☐ Chicken broth (32oz)         │
│                                  │
│  ── ✋ Manual Adds ──           │
│  ☐ Paper towels                  │
│  ☐ Dish soap                    │
│                                  │
│  [+ Add item]                    │
│  [📤 Share List]  [🖨️ Print]    │
└──────────────────────────────────┘
```

**Features:**
- Filter by store tab (shows only that store's items)
- Quantity aggregation with source notes
- Pantry staples auto-marked (learned over time)
- "Already have it" toggle — learns across weeks
- Check-off persistence
- Organized by store section/aisle
- Estimated cost per section and total
- Manual add field for non-food items
- Share as text or print

### View D: Household Profiles

```
┌──────────────────────────────────┐
│  👨‍👩‍👧‍👦 Your Household              │
│                                  │
│  ┌──────────────────────────┐    │
│  │ 👩 Mom                   │    │
│  │ Adventurousness: ████░ 4 │    │
│  │ 🚫 Tree nuts, shellfish  │    │
│  │ ❌ Mushrooms, olives     │    │
│  │ ❤️ 23 loved meals        │    │
│  │ Protein: fish > chicken  │    │
│  │ [Edit Profile]           │    │
│  └──────────────────────────┘    │
│                                  │
│  ┌──────────────────────────┐    │
│  │ 🧒 Kid 1 (age 7)        │    │
│  │ Adventurousness: ██░░░ 2 │    │
│  │ 🚫 None                  │    │
│  │ ❌ "Slimy" textures      │    │
│  │ ❤️ 8 loved meals         │    │
│  │ Protein: chicken > beef  │    │
│  │ 📝 "Eats broccoli only   │    │
│  │     if covered in cheese" │    │
│  │ [Edit Profile]           │    │
│  └──────────────────────────┘    │
│                                  │
│  [+ Add Family Member]          │
│                                  │
│  ── 🥗 Dietary Preferences ──   │
│  [Collapsible toggles panel]     │
│  ☑ Kid-friendly                  │
│  ☑ Balanced nutrition            │
│  ☐ High protein                  │
│  ☐ Low carb                     │
│                                  │
│  ── 🏪 Preferred Stores ──      │
│  [🟢 Whole Foods] Primary       │
│  [🔵 King Soopers] Bulk/staples │
│  [🟡 Sprouts] Produce           │
│  [Edit Store Strategy]           │
└──────────────────────────────────┘
```

### View E: Favorites Library

```
┌──────────────────────────────────┐
│  ❤️ Family Favorites             │
│  32 loved meals                  │
│                                  │
│  [All] [Mom] [Dad] [Kid1] [Kid2] │
│  [Quick] [Chicken] [Mexican]     │
│                                  │
│  ┌────────────────────────────┐  │
│  │ 🍽️ Chicken Taco Bowls     │  │
│  │ ❤️ Mom, Kid1, Kid2         │  │
│  │ 👍 Dad                     │  │
│  │ Last made: 2 weeks ago     │  │
│  │ Times made: 6              │  │
│  │ [📅 Add to This Week]     │  │
│  └────────────────────────────┘  │
│                                  │
│  ┌────────────────────────────┐  │
│  │ 🍽️ Mac & Cheese (scratch) │  │
│  │ ❤️ Kid1, Kid2              │  │
│  │ 👍 Mom, Dad                │  │
│  │ Last made: 3 weeks ago     │  │
│  │ ⚡ Suggestion: "It's been  │  │
│  │    3 weeks — add it?"      │  │
│  │ [📅 Add to This Week]     │  │
│  └────────────────────────────┘  │
│                                  │
│  ── 👎 Avoid List (12 items) ── │
│  [Expandable: meals rated 👎    │
│   with reasons, so AI avoids]    │
└──────────────────────────────────┘
```

### View F: Prep Day Planner

```
┌──────────────────────────────────┐
│  📋 Sunday Prep Plan             │
│  Based on: Week of March 9–15    │
│  Total: ~2.5 hours               │
│                                  │
│  1:00 PM ─ Start rice cooker     │
│  1:05 PM ─ Marinate chicken      │
│            (Mon + Wed dinner)    │
│  1:10 PM ─ Chop all vegetables   │
│            (broccoli, peppers,   │
│             onions for the week) │
│  1:30 PM ─ Start crockpot chili  │
│            (Thu dinner)          │
│  1:35 PM ─ Assemble overnight    │
│            oats (Mon + Tue)      │
│  1:45 PM ─ Bake chicken thighs   │
│  2:15 PM ─ Portion snack bags    │
│            for kids (Mon–Fri)    │
│  2:30 PM ─ Pack Mon/Tue lunches  │
│  3:00 PM ─ Clean up              │
│  3:15 PM ─ Done! 🎉              │
│                                  │
│  [🖨️ Print]  [📤 Share]         │
│  [🔄 Regenerate]                 │
└──────────────────────────────────┘
```

### View G: Freezer Inventory

```
┌──────────────────────────────────┐
│  ❄️ Freezer Inventory            │
│  8 items tracked                 │
│                                  │
│  ⚠️ Use Soon                    │
│  ┌────────────────────────────┐  │
│  │ Frozen berries (1 bag)     │  │
│  │ Added: Jan 5 — 2 months!  │  │
│  └────────────────────────────┘  │
│                                  │
│  ── All Items ──                │
│  • Ground beef (2 lbs) — Feb 15 │
│  • Chicken broth (3 cups) — Feb │
│  • Pizza dough (2 balls) — Feb  │
│  • Banana bread (half) — Feb 18 │
│  • Frozen corn (1 bag) — Jan 20 │
│  • Pork chops (4) — Feb 25     │
│  • Cookie dough (1 roll) — Mar 1│
│                                  │
│  [+ Add Item]   [📸 Scan]       │
│                                  │
│  💡 AI is using your ground beef │
│  for Tuesday's tacos this week   │
└──────────────────────────────────┘
```

### View H: Recipe Discovery Feed

```
┌──────────────────────────────────┐
│  🔍 Discover          [Filter]   │
│                                  │
│  ── Trending This Week ──       │
│  ┌────────────────────────────┐  │
│  │ [📸 Food photo]           │  │
│  │ Sheet Pan Honey Garlic    │  │
│  │ Chicken                   │  │
│  │ ⏱ 35 min | 👨‍👩‍👧‍👦 Family   │  │
│  │ 📰 Budget Bytes           │  │
│  │ ⭐ Match: 88% for your    │  │
│  │    household              │  │
│  │ [📌 Next Week!] [❤️ Save] │  │
│  └────────────────────────────┘  │
│                                  │
│  ── Because Kid 1 ❤️ Tacos ──   │
│  [Personalized recommendations]  │
│                                  │
│  ── March: Spring Produce ──    │
│  [Seasonal suggestions]          │
│                                  │
│  ── 🔍 Search ──                │
│  "I want to bake something fun"  │
│  → AI generates ideas matching   │
│    all household preferences     │
└──────────────────────────────────┘
```

**Discovery features:**
- RSS aggregation from top food publications (Budget Bytes, Serious Eats, Half Baked Harvest, etc.)
- AI-powered match scoring based on household profiles
- "📌 Next Week!" flag queues recipe for next plan generation
- Freeform search generates ideas matching all household constraints
- Seasonal recommendations based on regional produce availability

---

## Database Schema (PostgreSQL / Supabase)

```sql
-- Household (supports singles, couples, families)
CREATE TABLE households (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  budget_preference TEXT DEFAULT 'moderate',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Family/household members
CREATE TABLE members (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  household_id UUID REFERENCES households(id),
  auth_user_id UUID UNIQUE REFERENCES auth.users(id),
  name TEXT NOT NULL,
  avatar TEXT,
  age INTEGER,
  role TEXT CHECK (role IN ('adult', 'child')),
  allergies TEXT[],
  hard_dislikes TEXT[],
  texture_issues TEXT[],
  adventurousness INTEGER DEFAULT 3 CHECK (adventurousness BETWEEN 1 AND 5),
  protein_preference TEXT,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Dietary preference toggles (household-wide)
CREATE TABLE dietary_preferences (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  household_id UUID REFERENCES households(id),
  key TEXT NOT NULL,
  label TEXT NOT NULL,
  category TEXT NOT NULL,
  is_active BOOLEAN DEFAULT FALSE,
  sort_order INTEGER,
  UNIQUE(household_id, key)
);

-- Weekly meal plans
CREATE TABLE meal_plans (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  household_id UUID REFERENCES households(id),
  week_start DATE NOT NULL,
  status TEXT DEFAULT 'draft' CHECK (status IN ('draft','generating','review','finalized')),
  travel_exclusions JSONB,
  special_days JSONB,
  preference_overrides JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  finalized_at TIMESTAMPTZ
);

-- Individual meal slots
CREATE TABLE meal_slots (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  meal_plan_id UUID REFERENCES meal_plans(id),
  day TEXT NOT NULL,
  meal_type TEXT NOT NULL CHECK (meal_type IN ('breakfast','lunch','dinner','snack','dessert')),
  recipe_id UUID REFERENCES recipes(id),
  is_leftover BOOLEAN DEFAULT FALSE,
  leftover_source_id UUID,
  ai_confidence FLOAT,
  notes TEXT,
  sort_order INTEGER
);

-- Who's eating this meal
CREATE TABLE meal_slot_members (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  meal_slot_id UUID REFERENCES meal_slots(id),
  member_id UUID REFERENCES members(id),
  lunch_type TEXT CHECK (lunch_type IN ('packed', 'school_hot_lunch')),
  UNIQUE(meal_slot_id, member_id)
);

-- Recipes (AI-generated or imported)
CREATE TABLE recipes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  description TEXT,
  instructions JSONB,
  prep_time_minutes INTEGER,
  cook_time_minutes INTEGER,
  servings INTEGER,
  cuisine TEXT,
  source_url TEXT,
  source_name TEXT,
  image_url TEXT,
  tags TEXT[],
  is_ai_generated BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Recipe ingredients
CREATE TABLE recipe_ingredients (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  recipe_id UUID REFERENCES recipes(id),
  name TEXT NOT NULL,
  quantity FLOAT,
  unit TEXT,
  category TEXT,
  preparation TEXT,
  is_optional BOOLEAN DEFAULT FALSE
);

-- Per-person meal ratings (the learning engine)
CREATE TABLE ratings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  meal_slot_id UUID REFERENCES meal_slots(id),
  member_id UUID REFERENCES members(id),
  recipe_id UUID REFERENCES recipes(id),
  score TEXT CHECK (score IN ('loved', 'ok', 'hated')),
  reason TEXT,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(meal_slot_id, member_id)
);

-- Grocery lists
CREATE TABLE grocery_lists (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  meal_plan_id UUID REFERENCES meal_plans(id),
  estimated_total FLOAT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Grocery items
CREATE TABLE grocery_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  grocery_list_id UUID REFERENCES grocery_lists(id),
  name TEXT NOT NULL,
  quantity FLOAT,
  unit TEXT,
  store TEXT,
  aisle_category TEXT,
  estimated_price FLOAT,
  source_meals TEXT[],
  is_checked BOOLEAN DEFAULT FALSE,
  is_pantry_staple BOOLEAN DEFAULT FALSE,
  is_already_have BOOLEAN DEFAULT FALSE,
  is_manual_add BOOLEAN DEFAULT FALSE,
  sort_order INTEGER
);

-- Preferred stores
CREATE TABLE stores (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  household_id UUID REFERENCES households(id),
  name TEXT NOT NULL,
  role TEXT DEFAULT 'primary',
  color TEXT,
  icon TEXT,
  sort_order INTEGER
);

-- Freezer inventory
CREATE TABLE freezer_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  household_id UUID REFERENCES households(id),
  name TEXT NOT NULL,
  quantity TEXT,
  added_date DATE DEFAULT CURRENT_DATE,
  notes TEXT,
  is_used BOOLEAN DEFAULT FALSE
);

-- Flagged recipes from discovery
CREATE TABLE flagged_recipes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  household_id UUID REFERENCES households(id),
  recipe_id UUID REFERENCES recipes(id),
  source_url TEXT,
  title TEXT,
  image_url TEXT,
  match_score FLOAT,
  flagged_at TIMESTAMPTZ DEFAULT NOW(),
  used_in_plan_id UUID,
  is_dismissed BOOLEAN DEFAULT FALSE
);

-- Chat refinement messages per plan
CREATE TABLE chat_messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  meal_plan_id UUID REFERENCES meal_plans(id),
  role TEXT CHECK (role IN ('user', 'assistant')),
  content TEXT NOT NULL,
  changes_made JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Pantry staples (learned over time)
CREATE TABLE pantry_staples (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  household_id UUID REFERENCES households(id),
  name TEXT NOT NULL,
  category TEXT,
  times_marked_have INTEGER DEFAULT 0,
  auto_exclude BOOLEAN DEFAULT FALSE,
  UNIQUE(household_id, name)
);
```

### Key Indexes
```sql
CREATE INDEX idx_ratings_member ON ratings(member_id);
CREATE INDEX idx_ratings_recipe ON ratings(recipe_id);
CREATE INDEX idx_ratings_score ON ratings(score);
CREATE INDEX idx_meal_plans_week ON meal_plans(week_start);
CREATE INDEX idx_meal_slots_recipe ON meal_slots(recipe_id);
CREATE INDEX idx_grocery_items_store ON grocery_items(store);
CREATE INDEX idx_freezer_active ON freezer_items(is_used) WHERE is_used = FALSE;
CREATE INDEX idx_flagged_unused ON flagged_recipes(used_in_plan_id) WHERE used_in_plan_id IS NULL;
CREATE INDEX idx_pantry_auto ON pantry_staples(auto_exclude) WHERE auto_exclude = TRUE;
```

---

## Data Flow

1. **Planning Phase:** User configures the week on the Planning Grid (View A). Toggles members, marks busy days, sets dietary overrides, selects stores.
2. **Generation:** Agent pulls ALL context (profiles, preferences, ratings history, freezer inventory, flagged recipes, last 3 weeks of plans) and generates a complete meal plan.
3. **Refinement:** User reviews on Calendar view (View B), chats with agent to swap/adjust. Agent updates plan + grocery list in real time.
4. **Shopping:** User takes Grocery List (View C) to the store. Checks off items. Marks "already have" — system learns pantry staples over time.
5. **Cooking & Rating:** User taps meals to see recipes (View B.1). After eating, rates per person. Ratings feed back into next week's generation.
6. **Learning Loop:** Agent analyzes ratings, updates implicit taste profiles, adjusts future plans. The longer you use it, the better it gets.

---

## ⚠️ Security Requirements

### Authentication & Authorization
- **Auth required on ALL routes.** No unauthenticated access to any dashboard view or API endpoint.
- Use Supabase Auth (email/password or OAuth providers). Every request must include a valid session token.

### Row-Level Security (RLS)
- **Enable RLS on ALL tables.** Users must only see their own household's data.
- The `members` table must include `auth_user_id` mapped to Supabase `auth.uid()` for policy enforcement.
- For every table with a `household_id` column, apply: `USING (household_id IN (SELECT household_id FROM members WHERE auth_user_id = auth.uid()))`
- For tables without `household_id` (for example `meal_slots`, `grocery_items`, `ratings`, `chat_messages`), enforce RLS through joins to parent tables that resolve to the authenticated user's household.
- Never ship with permissive fallback rules like `USING (true)`; verify no policy allows cross-household reads or writes.
- Enable `FORCE ROW LEVEL SECURITY` on all tenant-scoped tables.
- Test RLS policies explicitly — verify that User A cannot read User B's meal plans, ratings, freezer items, or grocery lists.

### Data Privacy
- **Dietary/allergy data is sensitive personal information.** Treat it with the same care as health data.
- Food photos uploaded via the fridge scanner or recipe images must be stored in **private Supabase Storage buckets** (not public).
- Never expose household profile data in client-side logs, error messages, or analytics.

### Environment & Secrets
- **ALL API keys, database URLs, and secrets must be environment variables.** Never hardcode in source code.
- Required env vars: `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY` (server-side only)
- The service role key must NEVER be exposed to the client. Use it only in server-side API routes or edge functions.

### Content Security
- Recipe URLs and external content fetched for the Discovery feed must be treated as untrusted. Sanitize all HTML before rendering.
- Never execute JavaScript from external recipe sources.
- Image URLs from external sources should be proxied through the application to prevent tracking pixels.
