# Design Rationale — Pinterest Trends Dashboard

**Created:** 2026-03-10  
**Author:** Max (Design Subagent)

---

## Design Philosophy

**"Data-rich, decision-simple."** Affiliate marketers need to scan opportunities fast and act. Every pixel earns its place by either informing a decision or enabling an action.

---

## Layout Decisions

### 1. Dashboard (Main View)
- **Three-column layout** (sidebar + main + detail panel): Matches the PRD spec and follows the "master-detail" pattern familiar from tools like Ahrefs, SEMrush, and analytics dashboards.
- **Left sidebar as niche navigator:** Persistent, scannable list. Users can jump between niches without losing context. Badge-style competition indicators give at-a-glance filtering.
- **Center area as card grid (not a table):** Cards are more scannable than rows for non-technical users. Each card is a self-contained decision unit with ranking, revenue, payout, and opportunity score.
- **KPI strip at top:** Four summary cards (Total Niches, Avg Payout, Top Opportunity, Hidden Gems) orient the user immediately. This is standard SaaS dashboard pattern.

### 2. Trend Detail View
- **Full-width takeover with back navigation:** When drilling into a niche, the user needs focus. Side panels would be too cramped for sub-niche data + trends + products.
- **Two-column split:** Left for sub-niche breakdown (what to promote), right for Pinterest search trends (where the demand is). Maps directly to the affiliate's mental model: "What product?" → "Where's the traffic?"
- **Inline product cards:** Show top ClickBank products with payout prominently displayed. The payout is the #1 decision driver.

### 3. Filter Panel
- **Slide-over from left:** Doesn't navigate away from dashboard context. Users can adjust filters and see results update behind the panel.
- **Range sliders for quantitative filters:** More intuitive than number inputs for competition score, payout ranges, search volume.
- **Preset buttons:** "Hidden Gems," "High Volume," "Top Earners" — one-tap filter combos for common affiliate strategies.

### 4. Export Modal
- **Centered modal with format selection:** Simple, focused task. CSV for spreadsheet users, PDF for sharing, PNG for social proof.
- **Preview of what's being exported:** Reduces "did I export the right thing?" anxiety.

### 5. Mobile View
- **Single-column stack:** Sidebar becomes a collapsible hamburger menu. Cards stack vertically. Detail view is full-screen.
- **Bottom action bar:** Thumb-friendly zone for primary actions (filter, export, search).

---

## Color System

| Token | Hex | Usage |
|-------|-----|-------|
| `primary` | `#E60023` | Pinterest red — brand alignment, CTAs |
| `primary-dark` | `#AD081B` | Hover states, active indicators |
| `accent` | `#0076D3` | Links, secondary actions, info states |
| `success` | `#10B981` | Hot opportunities, growth indicators, low competition |
| `warning` | `#F59E0B` | Moderate signals, caution states |
| `danger` | `#EF4444` | High competition, declining trends |
| `bg-primary` | `#FAFAFA` | Page background |
| `bg-card` | `#FFFFFF` | Card surfaces |
| `bg-sidebar` | `#1A1A2E` | Dark sidebar for contrast and focus |
| `text-primary` | `#111827` | Headings, primary text |
| `text-secondary` | `#6B7280` | Descriptions, metadata |
| `border` | `#E5E7EB` | Card borders, dividers |

**Why Pinterest Red?** The entire product is about Pinterest affiliate marketing. Using Pinterest's brand color as the primary creates instant mental association. It also provides strong contrast against the dark sidebar and white cards.

**Why dark sidebar?** Separates navigation from content. Creates visual hierarchy. The dark sidebar is a SaaS convention (Notion, Linear, Vercel) that signals "this is a professional tool."

---

## Typography

- **Font:** Inter (system fallback: -apple-system, sans-serif) — the SaaS standard. Clean, readable at all sizes, excellent number rendering.
- **Scale:** 
  - Hero/KPI numbers: 2rem bold
  - Section headers: 1.25rem semibold  
  - Body: 0.875rem regular
  - Labels/metadata: 0.75rem medium, uppercase tracking

---

## Interaction Patterns

1. **Hover → reveal details:** Cards show expanded info on hover (desktop). Reduces initial visual noise.
2. **Click sidebar → filter center:** Selecting a niche in sidebar highlights it and scrolls the center to that card.
3. **Click card → drill down:** Opens trend detail view with transition.
4. **Keyboard navigable:** Arrow keys in sidebar, Enter to select, Esc to close modals.

---

## Accessibility Considerations

- Color is never the only indicator (icons + labels accompany green/yellow/red)
- Contrast ratios meet WCAG AA (4.5:1 for text, 3:1 for large text)
- Focus rings on all interactive elements
- Semantic HTML (nav, main, aside, section)
- ARIA labels on icon-only buttons

---

## Responsive Strategy

| Breakpoint | Layout |
|------------|--------|
| ≥1280px | Full three-column (sidebar + main + detail) |
| 1024-1279px | Two-column (collapsible sidebar + main) |
| 768-1023px | Single column, sidebar as overlay |
| <768px | Full mobile, bottom nav bar |

---

## Why These Screens?

1. **Dashboard** — The home base. 80% of time spent here.
2. **Trend Detail** — The deep-dive. Where decisions get made.
3. **Filter Panel** — Power user feature. Differentiates from static lists.
4. **Export Modal** — Conversion/retention feature. Makes data portable.
5. **Mobile Preview** — Proves portfolio-readiness on any device.

These five screens cover the complete user journey: Browse → Filter → Analyze → Decide → Export.
