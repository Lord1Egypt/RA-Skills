# Conversion Design & Landing Page Reference

## 1. Landing Page Anatomy

### Hero Section Variations

| Pattern | Best For | Key Spec |
|---------|----------|----------|
| **Split** (text left, visual right) | SaaS, B2B | 50/50 or 60/40 split; text column gets primary CTA |
| **Centered** (text stacked over image) | Brand launches, simple products | Max 600-700px text width; single focal CTA below headline |
| **Full-bleed media** (text overlay) | Lifestyle, hospitality, portfolios | 4.5:1 contrast on overlay text; darken overlay at 40-60% opacity |
| **Video background** | High-engagement storytelling | Auto-mute; < 5s to first frame; fallback static image required |

**Above-the-fold priorities (in order):** Value proposition headline, supporting subhead (1-2 sentences), primary CTA, trust signal (logo bar or stat).

Users form an opinion in **50 milliseconds**. Every extra 100KB in hero media increases bounce by ~1.8%.

### CTA Design

- **Minimum size:** 44x44px (Apple/WCAG), 48x48px (Material).
- **Color:** 3:1+ contrast ratio against background; prominence matters more than specific color.
- **Placement:** Above fold in hero; repeat after mid-page value build; repeat near final content.
- **Copy:** First-person ("Start my free trial") outperforms second-person by 10-90%.
- **Repetition:** Single consistent CTA repeated 2-3 times, not multiple competing actions.

### Social Proof Patterns

| Type | Effectiveness | Placement |
|------|--------------|-----------|
| Star ratings + reviews | 82% influence | Near pricing/CTA |
| Customer testimonials | 78% influence | After feature sections |
| Video testimonials | +34% conversion lift | Mid-page or dedicated section |
| Client logos | Trust signal | Directly below hero |
| User count / stats | Up to +43% conversion | Hero section or sub-hero |
| Security badges | Reduces abandonment | Near forms and payment |

### Pricing Page Design

**3 tiers optimal** (center-stage effect). Structure per card:
1. Tier name + "best for" one-liner
2. Price with billing toggle (default annual; show savings as % AND dollar)
3. Primary CTA button (below price, above features)
4. 8-12 core features with checkmarks/values

**Highlight recommended tier:** Distinct background, "Most Popular" badge, border emphasis, or elevation. Produces 12-15% lift in mid-tier selection.

---

## 2. Conversion Psychology

### Visual Hierarchy for Conversion

Follow the **F-pattern**: headline, key benefit, and CTA along the top-left-to-bottom path. **Z-pattern** for simpler pages: logo top-left, nav CTA top-right, content center diagonal, conversion CTA bottom-right.

### Scarcity & Urgency (Ethical Only)
- Real-time inventory counts -- only truthful data.
- Time-limited offers with visible countdown -- only genuine deadlines.
- Social proof urgency ("42 people viewing") -- must reflect real data.

### Trust Signals Hierarchy
1. Security badges (SSL, payment logos) -- near checkout/forms.
2. Money-back guarantees -- near CTA.
3. Third-party reviews (G2, Trustpilot) -- 82% influence.
4. Customer logos -- below hero.
5. Certifications (SOC 2, GDPR, HIPAA) -- footer or trust section.

### Friction Reduction
- Each additional form field reduces completion by 3-5%.
- Multi-step forms: 300% higher conversion on mobile vs single long form.
- Progress bars: +20-30% form completion when visible.
- Smart defaults: pre-fill known data; appropriate input types.
- Single-column layout mandatory on mobile.
- Inline validation on blur, not on submit.

---

## 3. Mobile Conversion Patterns

### Sticky CTAs
- Position 100-150px from bottom viewport, above gesture areas.
- 10-20% conversion improvement on long pages.
- Must not cover critical content; include dismiss option.
- Pair with micro trust note: "No credit card required."

### Thumb Zone Design
- **Primary actions:** Lower-center of screen (natural thumb reach).
- **Navigation:** Bottom bar with 3-5 destinations.
- **Avoid:** Top corners for frequent actions.
- **Tap targets:** Minimum 48px square with spacing.

### Bottom Sheets & Swipe
- Bottom sheets for secondary actions, filters, confirmations.
- Swipe-to-dismiss for non-critical modals.
- Swipe actions on list items for quick operations.

### One-Tap Actions
- Apple Pay / Google Pay for instant checkout.
- Social login to reduce signup friction.
- Quick-reply chips in notifications and chat.

---

## 4. Navigation & Information Architecture

### Navigation by App Type

| App Type | Primary Pattern | Key Feature |
|----------|----------------|-------------|
| **SaaS** | Left sidebar + top bar | Collapsible sidebar; breadcrumbs for depth |
| **E-commerce** | Mega menu + category nav | Faceted filtering; persistent cart with count |
| **Content** | Top nav + hamburger (mobile) | Search-forward; reading progress indicator |
| **Social** | Bottom tab bar (mobile) | 3-5 tabs; notification badges; create center |

### Search UX
- Autocomplete after 2-3 characters; limit to 5-7 results.
- Display recent searches on focus before typing.
- Surface top 3-5 filters inline; bottom sheet for advanced.
- No results: offer spelling corrections, related terms, category browsing.

### Infinite Scroll vs Pagination

| Criterion | Pagination | Infinite Scroll | Load More |
|-----------|-----------|----------------|-----------|
| Content type | Structured data, tables | Discovery feeds, social | Catalogs, search |
| User intent | Find specific item | Browse/explore | Mixed |
| SEO need | High (unique URLs) | Low | Medium |
| Accessibility | Best | Worst | Good |
| Mobile performance | Good | Memory risk | Good |

### Breadcrumbs
Use for hierarchies 3+ levels deep. Place below top nav, above page title. Truncate middle items on mobile with ellipsis.

---

## 5. Onboarding UX

### Progressive Onboarding Framework

**Phase 1 -- Signup:** Ask only email + password (or social login). Defer profile details until after first value moment.

**Phase 2 -- First-run experience:** Welcome screen with 1-2 sentence value prop. 3-5 step setup wizard for essential configuration. Pre-populated sample data so the product feels alive.

**Phase 3 -- Feature discovery (ongoing):** Contextual tooltips triggered by user behavior, not on first load. Checklist widget showing setup progress (drives 70%+ completion). Celebrate milestones.

### Tooltips vs Modals vs Coachmarks

| Pattern | Use When | Avoid When |
|---------|----------|------------|
| **Tooltips** | Explaining a single element | More than 1-2 on screen |
| **Modals** | Critical announcements, required input | Interrupting flow; never on first load for tours |
| **Coachmarks** | Introducing 3-5 key features in sequence | Users are mid-task; keep under 5 steps |
| **Hotspots** | Passive discovery of new features | Overuse trains users to ignore them |

### Empty States
Every empty state needs: (1) Illustration/icon, (2) Brief explanation, (3) Primary action CTA, (4) Optional link to docs/help.

---

## 6. Email & Notification Design

### Transactional Email Structure
Brand header, clear subject line, single-column body at 600px max width, primary action button (min 44px height, full-width mobile), minimal footer with unsubscribe.

### Notification Hierarchy

| Level | Channel | Timing |
|-------|---------|--------|
| **Urgent** | Push + in-app + email | Immediate |
| **Informational** | In-app + email | Batched or near-real-time |
| **Promotional** | Email only | Scheduled; respect quiet hours |

### Push Notification UX
- 40-50 character headline max.
- Deep-link to relevant screen, not app home.
- Limit to 3-5 per day.
- Implement quiet hours (default 10 PM - 8 AM local time).

---

## Quick Reference: Conversion Numbers

| Metric | Value |
|--------|-------|
| First impression time | 50ms |
| Mobile bounce if load > 3s | 53% |
| First-person CTA copy lift | 10-90% |
| Drop per extra form field | 3-5% |
| Progress bar completion boost | 20-30% |
| Multi-step form mobile lift | up to 300% |
| Video testimonial lift | +34% |
| Sticky mobile CTA lift | 10-20% |
| "Most Popular" badge lift | 12-15% |
| Per extra second load time | 7-10% drop |
