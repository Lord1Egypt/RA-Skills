---
name: lemma-desks-design
description: >
  UI architecture and design guidance for Lemma desks. Read this before writing
  any component code. Covers nav model selection, screen archetypes, theme
  tokens, and layout rules.
---

# Lemma Desks — Design Reference

Use this as a supplemental reference after applying the architecture contract in `GUIDE.md`.
`GUIDE.md` is the source of truth for mandatory design gates and implementation order.

---

## Step 1 — Identify the operating loop

Answer these before picking any layout:

1. **Who is the primary user?** (AE, ops analyst, support agent, finance reviewer…)
2. **What do they do repeatedly?** (process a queue, review and approve, fill intake forms, monitor status…)
3. **What do they scan?** (status, owner, priority, age, amount…)
4. **What requires focused attention?** (detail view, editing a record, reading a transcript…)
5. **What actions need drafting, approval, or escalation?**

If you cannot answer these, ask before designing.

---

## Step 2 — Pick a nav model

| Situation | Nav model |
|---|---|
| 3+ materially different job areas | Sidebar nav with icon + label |
| 2–4 closely related views | Top tabs |
| One dominant queue-style workflow | No nav — list-detail fills the screen |
| Single-task tool or kiosk | No nav — one pane |

Do not default to sidebar just because it looks like a real app. A support desk
with one queue does not need a sidebar. An ops tool with intake, review, and
reporting does.

---

## Step 3 — Pick a screen archetype

### Queue / inbox
For: processing a list of items one at a time (support tickets, expense approvals, leads).

Layout: left pane is a filterable, sortable list with compact rows. Right pane
is the selected item detail with actions. Both panes visible simultaneously on
wide screens. On narrow screens, detail overlays the list.

Key details: row shows status badge, owner, age or amount, and one primary
label. Detail pane shows full context and surfaces the primary action (approve,
reject, assign, escalate) prominently at the top, not buried at the bottom.

### Review / approval table
For: batch review of records, bulk actions, status monitoring.

Layout: full-width dense table. Column headers are sortable. Row actions are
inline (icon buttons or a context menu). Bulk action toolbar appears above the
table when rows are selected. Filters live in a compact strip above the table.

Key details: use tight row height (`h-10` or `h-11`). Status and priority get
color-coded badges. Action icons are muted until hovered. Destructive actions
are not in the inline row — they live in the bulk toolbar or a confirmation
dialog.

### Chat / support assistant
For: conversational interfaces, agent output streams, support transcripts.

Layout: message thread fills the main area. Composer is pinned at the bottom.
Sidebar or top area holds session history, active context (ticket, account), and
status. No table rows.

Key details: use larger line height and comfortable padding (`p-4`, `leading-6`).
Differentiate user and assistant messages visually through alignment or
background, not just color. Keep the composer minimal — one textarea, one send
button, optional attachments.

### Intake / form
For: structured data entry, multi-step onboarding, request submission.

Layout: step indicator at top or left. One section or step visible at a time.
Progress is explicit. Back/next navigation is consistent. Summary or review step
before final submit.

Key details: group related fields. Do not show all fields at once if the form
has more than 6–8 inputs. Required fields are marked. Validation is inline, not
only on submit.

### Monitoring / overview
For: status dashboards, pipeline health, incident tracking.

Layout: summary strip at top (3–5 key numbers). Below that, the most actionable
view — usually a list or table of items needing attention, not more KPI cards.
Drill-down goes into a detail panel or a sub-route.

Key details: KPI cards are for scanning, not the main content. If the user's job
is to process items, the item list is the main content and the KPIs are
secondary. Do not build a wall of equal-weight cards when the real task is in a
list below.

---

## Step 4 — Choose a theme from awesome-design-md

Use the [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md/tree/main/design-md)
repo as the source of truth for theme tokens. Each file in that repo is a
design-md for one real product. Read the file for your chosen theme and extract
from it — do not invent tokens.

### Pick a theme by use case

| Use case | Themes to consider |
|---|---|
| Support, chat, conversational | `claude`, `intercom`, `x.ai` |
| Structured operator tools, queue-driven | `linear.app`, `raycast`, `notion`, `superhuman` |
| Data-heavy SaaS, admin surfaces | `stripe`, `mongodb`, `sentry`, `vercel` |
| Polished consumer-product feel | `airbnb`, `apple`, `spotify`, `webflow` |

Pick one. Do not mix themes across screens.

### How to use a design-md file

1. Fetch the file for your chosen theme, e.g.:
   `https://raw.githubusercontent.com/VoltAgent/awesome-design-md/main/design-md/linear.app.md`
2. Read it fully before writing any component.
3. Extract these four things — everything else follows from them:

**Colors** — background, surface, border, text, accent, and semantic colors (error, success, warning).
Map each to a CSS variable in `:root`. Do not use any color in a component that
is not in this map.

**Typography** — base size, heading sizes, font family (or closest web-safe/Google
Fonts match), line height, letter spacing on labels. Write these as CSS variables
or Tailwind config extensions before touching a component.

**Spacing rhythm** — the step scale the theme uses (e.g. `4 / 8 / 12 / 16 / 24 / 32`).
Apply this rhythm consistently as padding, gap, and margin across every screen.
Do not introduce ad-hoc spacing values.

**Radius and border treatment** — border radius per element type (card, input, badge,
button), border width, border color. These three values alone account for most
of whether a UI feels "on-theme" or generic.

### After reading the design-md file

Before writing the first component, fill in this template from what you read:

```css
/* Theme: linear.app (example — replace with your chosen theme's actual values) */
:root {
  --bg:           #0f0f0f;
  --bg-subtle:    #1a1a1a;
  --bg-muted:     #222222;
  --border:       rgba(255,255,255,0.08);
  --border-muted: rgba(255,255,255,0.04);
  --text:         #e8e8e8;
  --text-muted:   #8a8a8a;
  --text-faint:   #555555;
  --accent:       #5b6af7;
  --accent-hover: #4a58e0;
  --error:        #e5484d;
  --success:      #46a758;
  --warning:      #e5a50a;
  --radius-sm:    4px;
  --radius:       6px;
  --radius-lg:    10px;
}
```

Replace every value with what the design-md file specifies for your theme. If
the file does not specify a value, infer it conservatively from the theme's
overall tone — do not default to the example above.

Never hardcode colors inside components. Every color reference must go through
a CSS variable so the theme stays consistent across the entire desk without
auditing individual files.

---

## Status and priority badges

Badges are the primary way to communicate state at a glance. Make them
consistent across every screen.

```tsx
const statusStyles: Record<string, string> = {
  OPEN:       "bg-blue-50   text-blue-700   border-blue-200",
  IN_PROGRESS:"bg-amber-50  text-amber-700  border-amber-200",
  DONE:       "bg-green-50  text-green-700  border-green-200",
  BLOCKED:    "bg-red-50    text-red-700    border-red-200",
  CANCELLED:  "bg-gray-100  text-gray-500   border-gray-200",
};

function StatusBadge({ status }: { status: string }) {
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium border ${statusStyles[status] ?? "bg-gray-100 text-gray-500 border-gray-200"}`}>
      {status}
    </span>
  );
}
```

Define the full set for your domain before building list rows. Do not invent
per-screen badge colors.

---

## Typography scale

Use only these sizes. Do not introduce new ones per screen.

| Role | Size | Weight | Color |
|---|---|---|---|
| Page heading | `text-xl` (20px) | `font-semibold` | `--text` |
| Section heading | `text-sm` (14px) | `font-medium` | `--text` |
| Body / row label | `text-sm` (14px) | `font-normal` | `--text` |
| Metadata / timestamp | `text-xs` (12px) | `font-normal` | `--text-muted` |
| Badge | `text-xs` (12px) | `font-medium` | per badge style |

Do not use `text-base` (16px) for row content in dense operator desks — it
makes tables feel bloated.

---

## Layout rules

- App shell has one `<main>` with `flex h-screen overflow-hidden`.
- Sidebar is `w-56` or `w-60`, fixed, does not scroll with content.
- Content area is `flex-1 overflow-y-auto`.
- List pane in list-detail is `w-80` or `w-96`, does not flex-grow.
- Detail pane is `flex-1`.
- Use `gap-0` with explicit borders between panes, not `gap-px` hacks.
- Sticky detail pane action area: `border-t p-4 flex justify-end gap-2`.

---

## Empty states

Every list and table needs an empty state. It should:

1. Use a simple icon or illustration — not a generic spinner.
2. State what is empty in plain language ("No open tasks").
3. Offer the first useful action as a button if applicable.

Do not render an empty `<tbody>` or a blank pane. Empty states teach the user
what to do next.

---

## What to avoid

- Equal visual weight on everything — use hierarchy through size, weight, and color.
- Saturated section backgrounds for visual separation — use borders and spacing.
- Modals for information that belongs in a detail pane.
- More than one primary action button visible at a time.
- Decorative hero copy at the top of an operator screen.
- Building a KPI dashboard when the task is processing a queue.
- Mixing unrelated workflows on one page without tabs or separate routes.
