# Budget Buddy Pro — Dashboard Companion Kit Spec

**A local, browser-based visual interface for Budget Buddy Pro data.**

Premium dark theme with teal (`#14b8a6`) and orange (`#f97316`) accents. Feels like a personal Bloomberg terminal for your money.

---

## Tech Stack

- **Framework:** React 18 + Vite
- **Styling:** Tailwind CSS (dark theme default)
- **Charts:** Chart.js or Recharts
- **Data Source:** Local JSON files from `data/` directory (no API server needed)
- **Hosting:** Local only — `npm run dev` on localhost

---

## Pages & Components

### 1. Budget Overview (Dashboard Home)

**Top Cards Row:**
- 💵 Monthly Income (green, `#22c55e`)
- 💸 Monthly Expenses (orange, `#f97316`)
- 💰 Net Savings (teal, `#14b8a6`)
- 📊 Budget Health Score (calculated: green >20% savings rate, yellow 10-20%, red <10%)

**Spending by Category (Donut Chart):**
- Interactive donut chart showing expense distribution by category
- Click a slice to drill into that category's transactions
- Color-coded by category group (needs=blue, wants=orange, savings=teal)

**Budget vs. Actual (Horizontal Bar Chart):**
- One bar per budget category
- Shows spent vs. limit with color coding (green/yellow/red)
- Hover shows exact amounts and percentage

**Recent Transactions (Scrollable List):**
- Last 20 transactions with date, vendor, category, amount
- Category pills color-coded
- Click to edit category or add notes

### 2. Transactions Page

**Full Transaction Table:**
- Columns: Date, Vendor, Category, Amount, Tags, Notes
- Sortable by any column (default: date descending)
- Filterable by: category, date range, amount range, search text
- Inline category editing (click to reassign)
- Bulk actions: re-categorize selected, tag selected, export selected

**Search Bar:**
- Full-text search across vendor names, notes, and tags
- Instant filtering as you type

**Import Zone:**
- Drag-and-drop area for CSV/PDF files
- Triggers `scripts/parse-statement.py` in background
- Shows parsing progress and result summary

### 3. Budget Management Page

**Active Budget Display:**
- Framework badge (50/30/20, zero-based, etc.)
- Monthly income and allocation breakdown
- Category list with editable limits
- Drag to reorder priority

**Budget Progress (Current Month):**
- Category-by-category progress bars
- Days remaining in month indicator
- Spending pace indicator (on track / ahead / behind)
- Alert threshold markers on progress bars

**Budget History:**
- Month-over-month budget adherence chart
- Shows which categories are consistently over/under

### 4. Trends & Insights Page

**Month-over-Month Spending (Line Chart):**
- Total spending trend line (last 6-12 months)
- Toggle individual category trend lines
- Highlight anomalies (spikes > 1.5x average)

**Category Breakdown Over Time (Stacked Area Chart):**
- Shows how spending distribution shifts month to month
- Identify growing categories

**Top Vendors (Bar Chart):**
- Top 10 vendors by total spend (trailing 3 months)
- Identify where the money really goes

**Subscription Tracker:**
- List of detected recurring charges
- Monthly total
- "Cancel reminder" toggle per subscription
- Month-to-month subscription cost trend

### 5. Savings Goals Page

**Goal Cards:**
- One card per active savings goal
- Circular progress indicator
- Target amount, current amount, monthly contribution
- Projected completion date
- On-track / behind / ahead indicator

**Goal Progress Over Time (Line Chart):**
- Track savings accumulation per goal
- Show projected vs. actual trajectory

**Goal Management:**
- Add/edit/archive goals
- Adjust monthly contributions
- Link goals to budget categories

### 6. Net Worth Page

**Net Worth Summary Card:**
- Current total with month-over-month change
- Breakdown: Total Assets vs. Total Liabilities

**Net Worth Over Time (Line Chart):**
- Monthly net worth snapshots
- Separate lines for assets, liabilities, and net worth

**Asset & Liability Breakdown (Stacked Bar):**
- Visual breakdown of asset types and liability types
- Edit values inline

### 7. Bills & Recurring Page

**Upcoming Bills Calendar:**
- Calendar view showing due dates
- Color by status: paid (green), upcoming (yellow), overdue (red)

**Recurring Summary:**
- Total monthly recurring expenses
- List with: name, amount, frequency, next due date, category
- Toggle active/inactive

---

## Database Schema (JSON Files)

The dashboard reads directly from Budget Buddy Pro's `data/` directory:

```
data/
├── budget.json              # Active budget (income, categories, limits, thresholds)
├── transactions/
│   └── YYYY-MM.json         # Monthly transaction files
├── recurring.json           # Recurring income & expenses
├── rules.json               # Custom categorization rules
├── categories.json          # Category definitions
├── savings-goals.json       # Savings goal tracking
├── net-worth.json           # Net worth snapshots (array of monthly records)
└── statements/              # Raw uploaded files (not displayed)
```

### Key Schema References

**budget.json** — See SKILL.md § Budget Creation
**transactions/YYYY-MM.json** — See SKILL.md § Statement Ingestion
**recurring.json** — See SKILL.md § Income & Expense Tracking
**rules.json** — See SKILL.md § Category Management
**savings-goals.json** — See SKILL.md § Savings Goals
**net-worth.json** — See SKILL.md § Net Worth Tracking

---

## Design Tokens

```css
/* Colors */
--bg-primary: #0f172a;       /* Slate 900 */
--bg-card: #1e293b;          /* Slate 800 */
--bg-hover: #334155;         /* Slate 700 */
--text-primary: #e2e8f0;     /* Slate 200 */
--text-secondary: #94a3b8;   /* Slate 400 */
--text-muted: #475569;       /* Slate 600 */
--accent-teal: #14b8a6;      /* Teal 500 */
--accent-orange: #f97316;    /* Orange 500 */
--success: #22c55e;          /* Green 500 */
--warning: #eab308;          /* Yellow 500 */
--danger: #ef4444;           /* Red 500 */

/* Category Group Colors */
--group-needs: #3b82f6;      /* Blue 500 */
--group-wants: #f97316;      /* Orange 500 */
--group-savings: #14b8a6;    /* Teal 500 */
--group-income: #22c55e;     /* Green 500 */

/* Typography */
--font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-mono: 'SF Mono', 'Fira Code', monospace;

/* Spacing */
--radius-sm: 6px;
--radius-md: 12px;
--radius-lg: 16px;
```

---

## Responsive Breakpoints

- **Desktop (1200px+):** Full layout, sidebar navigation
- **Tablet (768-1199px):** Collapsed sidebar, stacked cards
- **Mobile (< 768px):** Bottom navigation, single-column layout

---

## Data Refresh

- Dashboard watches `data/` directory for file changes (via polling or fs.watch)
- Auto-refreshes affected components when JSON files update
- No manual reload needed after agent processes a statement or updates a budget
