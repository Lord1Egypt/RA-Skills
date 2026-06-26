# UX Psychology & Cognitive Design Reference

## 1. Gestalt Principles Applied to UI

### Proximity
Elements near each other are perceived as related. Spacing is the primary grouping mechanism.

```css
.form-group     { margin-bottom: 32px; }   /* between groups */
.form-group input { margin-bottom: 8px; }  /* within a group  */
```

**Rule:** Inner spacing (within a group) should be at most half of outer spacing (between groups). A 2:1 or 3:1 ratio is safest.

### Similarity
Elements that look alike are perceived as belonging together. Use shared color, size, shape, or weight.

**Rule:** Keep a maximum of 3 distinct visual "families" of interactive elements per screen.

### Closure
The brain fills in gaps to see complete shapes. Use this for progress indicators, icon design, and loading states.

### Continuity
The eye follows smooth lines and curves. Align elements along a clear axis.

**Rule:** Use a strict column grid. Every element edge should snap to a grid line. Misaligned elements break continuity and create visual friction.

### Figure-Ground
Users must instantly distinguish foreground content from background. Contrast, elevation, and blur create separation.

```css
.modal-backdrop { background: rgba(0,0,0,0.5); backdrop-filter: blur(4px); }
.modal          { background: #fff; border-radius: 12px; box-shadow: 0 24px 48px rgba(0,0,0,0.16); }
```

**Rule:** Overlays need a minimum contrast shift of 40% luminance between foreground and background.

### Common Region
Borders or background fills create perceived groups, even without proximity.

**Rule:** Cards and sections should use either a border OR a fill, rarely both. Doubling cues wastes visual weight.

---

## 2. Cognitive Laws

### Fitts's Law -- Target Sizing & Placement

Time to reach a target = f(distance, size). Larger and closer targets are faster to hit.

| Context | Minimum Target Size |
|---------|-------------------|
| Touch (mobile) | 48 x 48 dp |
| Touch (iOS) | 44 x 44 pt |
| WCAG 2.5.5 | 44 x 44 CSS px |
| Desktop click | 32 x 32 px |
| Spacing between targets | >= 8px gap |

**Rules:**
- Primary actions go in bottom-right (desktop) or bottom-center (mobile) where the thumb rests.
- Destructive actions go far from confirm buttons to prevent accidental taps.
- Edge-anchored targets (menus flush to screen edges) have effectively infinite size on one axis.

### Hick's Law -- Reducing Choices

Decision time increases logarithmically with the number of options.

**Rules:**
- Limit primary navigation items to 5-7.
- For longer lists, chunk into categories.
- Highlight a recommended/default option to collapse the decision tree.
- Use progressive disclosure to defer secondary options.

### Miller's Law -- Chunking

Working memory holds roughly 7 +/- 2 items. Group information into digestible chunks.

**Rules:**
- Phone numbers: `(555) 123-4567` not `5551234567`.
- Credit card fields: 4 groups of 4 digits.
- Break long forms into multi-step wizards with 3-5 fields per step.
- Dashboard metrics: group into cards of 3-4 related KPIs.

### Jakob's Law -- Convention Over Invention

Users spend most of their time on other sites. Match existing mental models.

**Conventions:**
- Logo top-left, linking to home.
- Primary navigation horizontal at top or vertical at left.
- Search bar top-center or top-right.
- Shopping cart icon top-right with badge count.
- Underlined blue text = link.
- Forms: labels above inputs, submit button bottom-right.

### Doherty Threshold -- Response Time

Productivity soars when system response is under 400ms.

| Response Time | User Perception | UI Treatment |
|--------------|----------------|--------------|
| < 100ms | Instantaneous | No feedback needed |
| 100-400ms | Slight delay | Subtle state change |
| 400ms-1s | Noticeable | Show spinner |
| 1-5s | Waiting | Skeleton screen / progress bar |
| > 5s | Frustrated | Progress % and time estimate |

**Rules:**
- Optimistic UI updates for actions under 1s.
- Skeleton screens always beat loading spinners for perceived performance.
- Animate transitions at 200-300ms; under 100ms feels jumpy, over 500ms feels sluggish.

### Peak-End Rule

People judge an experience by its most intense moment (peak) and its final moment (end).

**Rules:**
- End flows with a moment of delight: confetti on signup completion, a clear success state with next steps.
- Eliminate negative peaks: never show an error without a recovery path.
- Onboarding should front-load a quick win within the first 60 seconds.

---

## 3. Visual Scanning Patterns

### F-Pattern (Text-Heavy Pages)
Users scan horizontally across the top, shorter horizontal sweep partway down, then vertically down the left edge.

**Design responses:**
- Put critical information in the first two paragraphs.
- Start headings and bullet points with information-carrying words (front-load keywords).
- Use bold for scannable anchor phrases.
- Break walls of text with subheadings every 3-5 paragraphs.

### Z-Pattern (Sparse / Marketing Pages)
Users scan top-left to top-right, diagonal to bottom-left, then across to bottom-right.

**Design responses:**
- Logo/brand mark: top-left.
- Navigation/CTA: top-right.
- Hero content/value prop: center (the diagonal).
- Primary CTA button: bottom-right.

### Layer-Cake Pattern
Users scan only headings and subheadings, skipping body text entirely. Headings must be self-sufficient.

### Serial Position Effect
Users remember the first and last items in a list best.

**Rule:** Put the most important nav items first and last. Bury less critical items in the middle.

---

## 4. Decision Architecture

### Progressive Disclosure
Show only what is needed at each step; reveal complexity on demand.

**Implementation patterns:**
- Accordion sections for secondary settings.
- "Show advanced options" toggle.
- Multi-step forms with 3-5 fields per step.
- Tooltip/popover for contextual help vs. inline text.

**Rule:** Primary display should cover 80% of user needs. The remaining 20% is disclosed progressively.

### Default Bias
Users overwhelmingly accept pre-set defaults. Use this ethically.

**Rules:**
- Pre-select the most common/safest option.
- Toggle switches should default to the privacy-respecting state.
- Pre-fill forms with smart defaults (country from IP, timezone from browser).

### Anchoring
The first piece of information presented becomes the reference point for all subsequent judgments.

**Rules:**
- Show the higher-priced plan first in pricing tables.
- Display original price before discount to establish anchor.
- Show "most popular" labels on the plan you want users to choose.

### Social Proof Placement
Place social proof adjacent to decision points, not buried in separate sections.

**Rules:**
- Testimonials directly below or beside pricing CTAs.
- User counts near signup forms.
- Trust badges next to checkout buttons.
- Star ratings visible without scrolling on product cards.

---

## 5. Emotional Design

### Color & Emotion

| Emotion | Color Family | Usage |
|---------|-------------|-------|
| Trust/Security | Blue | Finance, SaaS, healthcare |
| Urgency/Error | Red | Alerts, destructive actions, sales |
| Success/Growth | Green | Confirmations, positive metrics |
| Warning/Caution | Amber | Non-blocking alerts |
| Calm/Premium | Neutral + generous whitespace | Luxury, editorial |
| Energy/Optimism | Yellow/Orange | CTAs, highlights |

### Typography & Emotion

| Feeling | Typeface Characteristics |
|---------|------------------------|
| Trust/Authority | Serif or geometric sans |
| Modern/Clean | Geometric sans-serif |
| Friendly/Approachable | Rounded sans-serif |
| Technical/Precise | Monospace or condensed sans |

### Spacing & Calm
More whitespace = more premium/calm. Dense layouts signal "tool"; spacious layouts signal "product."

### Motion & Delight
Enter transitions should be slightly slower than exit transitions (users need time to register new content). Stagger list item animations by 30-50ms per item, cap total duration at 500ms.

---

## Quick-Reference Cheat Sheet

| Principle | Key Number | Action |
|-----------|-----------|--------|
| Fitts's Law | 44-48px min | Size touch targets appropriately |
| Hick's Law | 5-7 max | Limit choices per decision point |
| Miller's Law | 7 +/- 2 | Chunk information into groups |
| Doherty Threshold | < 400ms | Keep responses under 400ms |
| Color ratio | 60-30-10 | Dominant/secondary/accent |
| F-pattern | top 2 lines | Front-load critical content |
| Proximity ratio | 2:1 or 3:1 | Inner vs outer spacing |
| First impression | 50ms | Users judge in 50 milliseconds |
