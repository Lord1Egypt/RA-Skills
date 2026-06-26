# Party Planner Pro — Dashboard Companion Kit Spec

**A local, browser-based visual interface for Party Planner Pro data.**

Vibrant design with fuchsia (`#e879f9`) and emerald (`#10b981`) accents on a dark background. Feels like a sleek event command center.

---

## Tech Stack

- **Framework:** Next.js 14+ (App Router)
- **Styling:** Tailwind CSS + shadcn/ui component primitives
- **Charts:** Recharts
- **Data Source:** Local JSON files from `data/` directory via server-side loaders/route handlers
- **Hosting:** Next.js dashboard shell (`npm run dev`)

---

## Pages & Components

### 1. Events Dashboard (Home)

**Top Cards Row:**
- 🎉 Active Events (count, with next event date)
- 👥 Total Guests Confirmed (across all active events)
- 💰 Total Budget / Spent (across all active events)
- ✅ Tasks Remaining (across all active events)

**Upcoming Events (Card Grid):**
- One card per active event with:
  - Event name, type icon, date, guest count
  - Progress indicators: RSVP %, Budget %, Tasks %
  - Color accent from event's theme color
  - Click to drill into event detail

**Quick Actions:**
- "Plan a New Event" button
- "View All Tasks" button
- "Budget Overview" button

### 2. Event Detail Page

**Header:**
- Event name, type badge, date and time, venue
- Theme color bar with color swatches
- Status badge (Planning / Ready / Day-Of / Complete)
- Edit event details button

**Tab Navigation:**
- Overview | Guests | Budget | Menu | Tasks | Vendors | Day-Of

**Overview Tab:**
- Summary cards: Guest count, Budget status, Tasks remaining, Days until event
- Countdown timer (days, hours, minutes)
- Recent activity feed (last 5 changes: new RSVP, expense added, task completed, etc.)

### 3. Guest Management Page

**Guest List Table:**
- Columns: Name, Group, RSVP Status, Dietary, +1, Table, Contact
- RSVP status as color-coded badges (green=confirmed, red=declined, yellow=maybe, gray=pending)
- Sortable and filterable by group, RSVP status, dietary needs
- Inline editing for RSVP status and table assignment
- Bulk actions: send reminder, change group, export

**RSVP Summary (Top Bar):**
- Donut chart: Confirmed / Declined / Maybe / No Response
- Total headcount (including +1s)
- Dietary restriction breakdown (bar chart)

**Guest Add Form:**
- Name, email/phone, group (dropdown), dietary (multi-select), +1 toggle, notes

### 4. Budget Page

**Summary Cards:**
- 💰 Total Budget (green)
- 💸 Total Spent (orange/fuchsia)
- 💵 Remaining (emerald)
- 📊 Cost Per Head

**Budget vs. Actual (Horizontal Bar Chart):**
- One bar per category
- Green (under 80%), yellow (80-100%), red (over 100%)
- Hover for exact numbers

**Expense Log (Scrollable Table):**
- Date, description, vendor, category, amount, paid status
- Add new expense inline
- Category filter

**Category Breakdown (Donut Chart):**
- Interactive — click slice to filter expense log

### 5. Menu Page

**Course-by-Course View:**
- Expandable sections per course (Appetizers, Main, Sides, Dessert, Drinks)
- Each item shows: name, dietary tags (colored pills), quantity, estimated cost, assigned-to

**Dietary Matrix:**
- Grid: menu items × dietary needs
- Green checkmarks where an item satisfies a need
- Red flags where a dietary need has <2 options

**Drink Calculator Widget:**
- Input: guest count, event hours, alcohol preference
- Output: beer, wine, liquor, non-alcoholic, and ice quantities

**Potluck Tracker (if applicable):**
- Who's bringing what
- Gap indicators (missing categories highlighted)

### 6. Tasks & Timeline Page

**Timeline View:**
- Visual Gantt-style view of milestones
- Milestone groups: 8 wk, 6 wk, 4 wk, 2 wk, 1 wk, day-before, day-of
- Color-coded by status: done (green), overdue (red), upcoming (blue)

**Task List (Kanban or List Toggle):**
- Kanban columns: To Do | In Progress | Done
- Each card: task name, due date, assignee, priority badge
- Drag to change status
- Filter by assignee, priority, milestone

**Progress Bar:**
- X of Y tasks complete — overall percentage with visual bar

### 7. Vendor Directory Page

**Vendor Cards (Grid Layout):**
- Business name, service type icon, contact info
- Booking status badge (Researching → Quoted → Booked → Paid)
- Quote amount and payment progress
- Click to expand: full details, contract notes, cancellation policy

**Quote Comparison View:**
- Side-by-side for vendors of same service type
- Highlight cheapest, note what's included

**Payment Timeline:**
- Upcoming vendor payments sorted by due date
- Overdue payments flagged in red

### 8. Day-Of Coordination Page

**Hour-by-Hour Timeline:**
- Visual timeline from setup to teardown
- Color blocks for setup, event, cleanup phases
- Current time indicator (on event day)

**Helper Assignment Matrix:**
- Grid: helpers × time slots
- Shows what each person is doing when
- Print-friendly view for day-of distribution

**Emergency Contacts:**
- Quick-access cards with phone numbers (tap to call on mobile)

**Checklist:**
- Expandable setup checklist by zone (entrance, food area, activity area, etc.)
- One-tap check-off on mobile

---

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `primary` | `#e879f9` | Accents, active states, CTAs |
| `secondary` | `#10b981` | Success, confirmed, on-track |
| `warning` | `#f59e0b` | Approaching limits, pending |
| `danger` | `#ef4444` | Over budget, overdue, declined |
| `surface` | `#1e293b` | Cards, panels |
| `background` | `#0f172a` | Page background |
| `text-primary` | `#f8fafc` | Headlines, primary text |
| `text-secondary` | `#94a3b8` | Labels, descriptions |

---

## Mobile Responsiveness

- All pages responsive down to 375px width
- Task checklist and day-of timeline optimized for phone use on event day
- Guest list supports swipe actions on mobile (confirm/decline RSVP)
- Bottom navigation bar on mobile replaces sidebar

---

## Data Flow

1. Agent creates/updates JSON files in `data/events/`
2. Next.js server utilities normalize JSON into typed view models consumed by dashboard pages/components
3. Server components fetch initial event state; client components handle filters, charts, and tab interactions
4. Optional write actions post to Next.js route handlers that validate payloads before persisting JSON changes
5. Export actions trigger report scripts and return generated file links for download
