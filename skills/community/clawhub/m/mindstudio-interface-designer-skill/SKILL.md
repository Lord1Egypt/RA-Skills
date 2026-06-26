---
name: mindstudio-interface-designer-skill
description: Master frontend skill for MindStudio Interface Designer. Use this skill for every UI/UX request including creating, designing, building, improving, reviewing, or refactoring any interface, component, or web app inside MindStudio. Supports onboarding flows, dashboards, landing pages, forms, wizards, data visualizations, admin panels, e-commerce, SaaS apps, and portfolios. Always interviews the user first, commits to a bold aesthetic direction, then builds production-grade code.
---

# MindStudio Interface Designer — Master Frontend Skill

This skill governs every UI/UX task performed via Claude Code through the MindStudio local tunnel. It combines collaborative design discovery, bold aesthetic execution, comprehensive UX intelligence, React performance best practices, and a rigorous pre-delivery quality checklist — all tuned specifically for the MindStudio Interface Designer environment.

The Interface Designer outputs React components that are compiled and deployed directly into MindStudio User Input blocks. Every interface you build here is a live, interactive part of an AI agent workflow. Design accordingly: the interface must be functional, polished, accessible, and feel native to the product it serves.

---

## Phase 1: Discovery — Always Interview First

**Never jump straight to code.** Before any design or implementation work, run a focused discovery conversation. Ask one question at a time. Prefer multiple-choice when possible. The goal is to understand purpose, user, constraints, and aesthetic direction before a single line of code is written.

### Discovery Questions (ask sequentially, stop when you have enough)

**Question 1 — Purpose**
What is this interface collecting or communicating? Pick the closest:
- A) A form or data collection step inside an AI workflow
- B) An onboarding or multi-step wizard
- C) A dashboard or data display
- D) A creative tool or interactive experience
- E) Something else (describe it)

**Question 2 — User**
Who will use this interface?
- A) Internal team / operations
- B) End customers / consumers
- C) Business clients / B2B
- D) The builder themselves (testing/prototyping)

**Question 3 — Tone & Feel**
What feeling should this interface communicate? Pick one or two:
- A) Professional and trustworthy
- B) Warm and approachable
- C) Bold and energetic
- D) Minimal and focused
- E) Luxurious and refined
- F) Playful and fun
- G) Technical and precise

**Question 4 — Visual Constraints**
Do you have brand colors, fonts, or an existing design system to match?
- A) Yes — share them (hex codes, font names, logo)
- B) Loosely — here's a reference site or screenshot
- C) No — give me your best creative direction

**Question 5 — Technical Constraints**
Any technical requirements?
- A) Must work in MindStudio's React environment (default — always assume this)
- B) Specific npm packages required
- C) Must match an existing component library (shadcn, MUI, etc.)
- D) No constraints beyond MindStudio compatibility

**Question 6 — MindStudio Variable Mapping (REQUIRED)**
This is critical. In MindStudio, every input the user fills out gets passed as a variable into the rest of the agent workflow. For each input field in the interface, we need to know its variable name so the component can wire them up correctly.

Ask the user:

> "Let's map your inputs to MindStudio variables. For each field in this interface, what should the variable be named? For example: `topic`, `tone`, `keywords`, `content_type`. List each field and its variable name."

If the user isn't sure, suggest names based on the interface purpose and ask them to confirm or adjust. For example, for a LinkedIn post generator:

| Field | Suggested Variable |
|-------|--------------------|
| Raw idea / topic | `topic` |
| Tone of voice | `tone` |
| Post length | `post_length` |
| Keywords | `keywords` |
| Content format | `content_type` |

Once confirmed, use these exact variable names throughout the component. Do not invent variable names. Do not use generic names like `input1` or `field_value`.

### Variable Wiring Pattern

Every confirmed variable must be captured in component state using its exact MindStudio variable name and surfaced for the workflow. Use this pattern:

```tsx
// State keys match MindStudio variable names exactly
const [formData, setFormData] = useState({
  topic: '',
  tone: '',
  keywords: '',
  content_type: [],
})

// On submit — pass all variables to the MindStudio workflow
const handleSubmit = () => {
  // Each key in formData corresponds to a named MindStudio variable
  // that downstream blocks in the workflow can reference
  onSubmit(formData)
}
```

Always display a variable reference summary in a code comment at the top of the component so it's clear to the MindStudio builder which variables the interface produces:

```tsx
/**
 * MindStudio Variables Output:
 * - topic         (string)  — the user's research topic or idea
 * - tone          (string)  — selected tone of voice
 * - keywords      (string)  — comma-separated keywords
 * - content_type  (array)   — selected content formats
 */
```

### After Discovery

Once you understand what you're building, present the design plan in sections of 200-300 words. Check in after each section before proceeding. Cover:
1. Aesthetic direction and rationale
2. Component structure and layout
3. Data flow and state management
4. Interaction patterns and animations
5. Accessibility and edge cases

Ask: "Does this direction feel right? Any adjustments before I build?"

Propose 2-3 approaches when trade-offs exist. Lead with your recommendation and explain why. Apply YAGNI ruthlessly — remove features that aren't needed for this specific interface.

---

## Phase 2: Aesthetic Direction — Commit Boldly

Once discovery is complete, lock in a clear aesthetic direction and execute it with precision. Generic interfaces are forgettable. The best MindStudio interfaces feel purpose-built.

### Choosing a Direction

Commit to one of these aesthetic archetypes (or a deliberate blend of two):

| Archetype | Character | Best For |
|-----------|-----------|----------|
| **Refined Minimal** | Surgical whitespace, one accent color, perfect type | SaaS, B2B, professional tools |
| **Luxury Editorial** | Serif display, high contrast, generous margins | Portfolios, premium services, creative agencies |
| **Dark Technical** | Deep backgrounds, monospace accents, neon highlights | Developer tools, AI products, fintech |
| **Warm & Approachable** | Rounded corners, soft palette, friendly type | Consumer apps, health, education |
| **Bold Brutalist** | Raw grid, oversized type, stark contrast | Fashion, art, provocative brands |
| **Glassmorphic** | Frosted panels, layered depth, soft blurs | Modern SaaS, dashboards, overlays |
| **Bento Grid** | Card-based density, varied sizes, organized chaos | Dashboards, feature showcases |
| **Retro-Futuristic** | Scan lines, phosphor glow, monospace | AI tools, tech demos, niche products |
| **Claymorphic** | Inflated shapes, pastel 3D, playful shadows | Consumer apps, games, children's tools |
| **Organic/Natural** | Earth tones, texture, flowing curves | Wellness, food, sustainability |

**CRITICAL RULE**: Choose a direction and commit fully. Halfhearted execution of any style is worse than bold execution of any other. The key is intentionality.

### What Makes an Interface Unforgettable

Before coding, answer: What is the ONE thing a user will remember about this interface? It could be a font choice, an animation on entry, an unexpected color, a micro-interaction on submit. Identify it. Then build everything else to support it.

---

## Phase 3: Design System — Build Before You Code

Establish these design tokens before writing components. Store them as CSS variables or a Tailwind config extension.

### Typography

Pair a distinctive display font with a refined body font. Never default to Inter, Roboto, Arial, or system-ui as a primary choice.

**Example pairings by archetype:**

| Archetype | Display | Body |
|-----------|---------|------|
| Luxury Editorial | Playfair Display, Cormorant Garamond | Lora, EB Garamond |
| Bold Brutalist | Anton, Bebas Neue | IBM Plex Mono, Space Mono |
| Dark Technical | Syne, Oxanium | JetBrains Mono, Fira Code |
| Warm Approachable | Nunito, Quicksand | Source Sans Pro, DM Sans |
| Refined Minimal | Fraunces, Libre Baskerville | Figtree, Plus Jakarta Sans |
| Glassmorphic | Outfit, Syne | Manrope, DM Sans |

Rules:
- `line-height` for body: 1.5-1.75
- `line-length` for readable text: 65-75 characters (ch units)
- Minimum 16px body text on mobile
- Scale: xs/sm/base/lg/xl/2xl/3xl/4xl — never use arbitrary sizes

### Color System

Commit to a palette with clear roles. Every color must have a purpose.

```css
:root {
  /* Brand */
  --color-primary: /* your dominant brand color */;
  --color-primary-hover: /* 10% darker */;
  --color-accent: /* high-contrast complement */;

  /* Surface */
  --color-bg: /* page background */;
  --color-surface: /* card/panel background */;
  --color-surface-elevated: /* modal/popover */;
  --color-border: /* subtle border */;
  --color-border-strong: /* emphasis border */;

  /* Text */
  --color-text-primary: /* high contrast body */;
  --color-text-secondary: /* muted labels */;
  --color-text-disabled: /* placeholder/inactive */;

  /* Semantic */
  --color-success: ;
  --color-warning: ;
  --color-error: ;
  --color-info: ;
}
```

**Contrast requirements (WCAG AA minimum):**
- Normal text (under 18px): 4.5:1 minimum
- Large text (18px+ or 14px bold): 3:1 minimum
- Interactive elements against background: 3:1 minimum
- Never use gray-400 or lighter for body text in light mode

**Palette archetypes by product type:**

| Product | Primary Palette Direction |
|---------|--------------------------|
| SaaS / B2B | Cool slate, indigo, neutral with blue accent |
| E-commerce | High contrast black/white, product-driven accent |
| Healthcare | Calm blue-green, white, soft sage |
| Fintech | Deep navy, gold accent, crisp white |
| Beauty / Wellness | Rose, champagne, dusty sage, warm cream |
| Creative Agency | Monochrome base, electric accent |
| Education | Warm amber, forest green, cream |
| Gaming / Entertainment | Dark base, neon accent, high saturation |

### Spacing Scale

Use an 8-point grid. Common values: 4, 8, 12, 16, 24, 32, 48, 64, 96, 128px. Never use arbitrary spacing.

### Z-Index Scale

Define this explicitly to avoid stacking chaos:

```css
:root {
  --z-base: 0;
  --z-raised: 10;
  --z-dropdown: 20;
  --z-sticky: 30;
  --z-overlay: 40;
  --z-modal: 50;
  --z-toast: 60;
  --z-tooltip: 70;
}
```

---

## Phase 4: Component Architecture (MindStudio React Environment)

MindStudio's Interface Designer runs a full React environment with hot reloading, npm package support, and live preview. Build as you would in a professional React project.

### MindStudio-Specific Rules

- **Single root component**: Export one default component that MindStudio compiles
- **No SSR assumptions**: This is a client-side React environment — avoid Next.js-specific APIs
- **State is local**: Use `useState`, `useReducer`, and `useContext` — no Redux or external state stores unless explicitly needed
- **Responsive default**: Assume the interface will render at various widths — always test at 375px, 768px, 1024px, 1440px
- **No `<form>` HTML tags**: Use `onClick`/`onChange` handlers instead of native form submission

### The MindStudio Bridge — CRITICAL

MindStudio automatically provides a `./bridge` file in every Interface Designer project. This is the **only correct way** to submit data and advance the workflow to the next block. Never use `window.MindStudio.submit` or any other submission method — they will silently fail.

The bridge exposes:

| Export | Type | Purpose |
|--------|------|---------|
| `submit(values)` | function | Sends form data to the workflow and advances to the next block |
| `uploadFile(file)` | function | Uploads a file and returns a CDN URL |
| `requestFile(options?)` | function | Prompts the user to pick a file or media from their library |
| `useIsRunning()` | hook | Returns `true` while the workflow is processing after submission |
| `useTemplateVariables()` | hook | Returns current values of variables already set in the workflow |

**Always import from the bridge at the top of every component:**

```tsx
import { submit, useIsRunning } from './bridge'
```

**Never use:**
```tsx
// WRONG — will not advance the workflow
window.MindStudio.submit(data)
// WRONG — manual status state does not reflect actual workflow state
const [status, setStatus] = useState('idle')
setTimeout(() => setStatus('loading'), 0)
```

### Component Structure Pattern

```tsx
// Recommended file structure for a MindStudio interface component

// 1. Imports — always include bridge
import { useState, useCallback } from 'react'
import { submit, useIsRunning } from './bridge'

/**
 * MindStudio Variables Output:
 * - variable_one  (string) — description
 * - variable_two  (string) — description
 */

// 2. Types / interfaces
interface FormData {
  variable_one: string
  variable_two: string
}

// 3. Sub-components (keep small, focused)
const StepIndicator = ({ current, total }) => { ... }
const InputField = ({ label, ...props }) => { ... }

// 4. Main component
export default function Interface() {
  // Bridge hook — reflects actual workflow processing state
  const isRunning = useIsRunning()

  // State — keys must match confirmed MindStudio variable names
  const [data, setData] = useState<FormData>({
    variable_one: '',
    variable_two: '',
  })

  // Submit handler — always use submit() from bridge
  const handleSubmit = useCallback(() => {
    submit(data) // advances workflow to next block
  }, [data])

  // Render
  return (
    <div className="...">
      {/* interface content */}
      <button
        onClick={handleSubmit}
        disabled={isRunning}
      >
        {isRunning ? 'Processing...' : 'Submit'}
      </button>
    </div>
  )
}
```

### State Management Patterns

**Multi-step forms:**
```tsx
const [step, setStep] = useState(0)
const steps = ['Info', 'Preferences', 'Review']
// Always validate before advancing steps
const canAdvance = () => validateStep(step, data)
// Only call submit() from bridge on the final step
```

**Submit button loading state — use bridge hook, not manual state:**
```tsx
const isRunning = useIsRunning() // from './bridge'

// Correct — reflects actual workflow state
<button disabled={isRunning} onClick={handleSubmit}>
  {isRunning ? 'Processing...' : 'Submit'}
</button>

// WRONG — manual setTimeout does not reflect workflow state
const [loading, setLoading] = useState(false)
setLoading(true)
setTimeout(() => setLoading(false), 2000)
```

**Form validation:**
```tsx
const [errors, setErrors] = useState<Record<string, string>>({})
// Validate on blur, not on every keystroke
// Show errors inline, near the field, not in a banner at the top
// Clear errors when the user corrects the field
// Only call submit() after validation passes
```

---

## Phase 5: Visual Craft — The Details That Matter

### Motion & Animation

Animations should feel purposeful, not decorative. Every animation earns its place.

**Entry animations (page/component load):**
```css
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

.animate-in {
  animation: fadeUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

/* Staggered reveals */
.card:nth-child(1) { animation-delay: 0ms; }
.card:nth-child(2) { animation-delay: 60ms; }
.card:nth-child(3) { animation-delay: 120ms; }
```

**Interaction timing:**
- Hover state transitions: 150-200ms ease-out
- Focus transitions: 100ms
- Page/step transitions: 300-400ms cubic-bezier
- Loading spinners: instant appear, 200ms fade-out on resolve
- Toasts/notifications: 250ms slide-in, 200ms fade-out

**Performance rules for animation:**
- Only animate `transform` and `opacity` — never `width`, `height`, `top`, `left`, `margin`
- Use `will-change: transform` sparingly, only on elements that definitely animate
- Always include `prefers-reduced-motion` override:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Backgrounds & Depth

Never default to a flat solid color background. Create atmosphere:

```css
/* Gradient mesh */
background: radial-gradient(at 20% 20%, hsl(220 80% 60% / 0.3) 0px, transparent 60%),
            radial-gradient(at 80% 80%, hsl(280 70% 50% / 0.2) 0px, transparent 60%),
            hsl(220 20% 8%);

/* Noise overlay */
background-image: url("data:image/svg+xml,..."); /* SVG noise */
background-blend-mode: overlay;
opacity: 0.04;

/* Grain effect with pseudo-element */
.surface::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url('/noise.png');
  opacity: 0.03;
  pointer-events: none;
}
```

### Glassmorphism (when appropriate)
```css
.glass-card {
  background: rgba(255, 255, 255, 0.08);  /* dark mode */
  /* OR */
  background: rgba(255, 255, 255, 0.80);  /* light mode — never go below 0.6 */
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
}
```

### Shadows

Use layered shadows for realism:
```css
/* Soft elevation */
box-shadow: 0 1px 2px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.08);

/* Medium card */
box-shadow: 0 2px 4px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.10);

/* Floating / modal */
box-shadow: 0 4px 8px rgba(0,0,0,0.06), 0 16px 48px rgba(0,0,0,0.14);

/* Colored accent shadow */
box-shadow: 0 8px 24px rgba(99, 102, 241, 0.25); /* use primary color */
```

---

## Phase 6: Interaction Design — Pixel-Perfect UX

### Clickable Elements

Every interactive element must communicate its interactivity:

```css
/* All clickable elements */
cursor: pointer;
transition: all 150ms ease-out;

/* Hover: always provide visual feedback */
&:hover {
  /* At minimum: one of these — color change, shadow, border, scale */
  background-color: var(--color-primary-hover);
}

/* Active/pressed */
&:active {
  transform: scale(0.98); /* subtle, not jarring */
}

/* Focus (keyboard navigation) */
&:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}
```

**Touch target sizes:**
- Minimum 44x44px for all interactive elements on mobile
- Add padding rather than enlarging the visual element if needed

### Form Inputs

```tsx
// Every input needs: label, placeholder, error state, disabled state
<div className="field">
  <label htmlFor={id} className="field-label">{label}</label>
  <input
    id={id}
    aria-describedby={error ? `${id}-error` : undefined}
    aria-invalid={!!error}
    className={`field-input ${error ? 'field-input--error' : ''}`}
    {...props}
  />
  {error && (
    <p id={`${id}-error`} role="alert" className="field-error">{error}</p>
  )}
</div>
```

### Loading States

Never leave the user staring at a blank or frozen interface:

```tsx
// Button loading state
<button disabled={isLoading} onClick={handleSubmit}>
  {isLoading ? (
    <span className="flex items-center gap-2">
      <Spinner size={16} /> Processing...
    </span>
  ) : 'Submit'}
</button>

// Content loading — skeleton screens preferred over spinners for layout areas
<div className="skeleton" style={{ width: '100%', height: 48, borderRadius: 8 }} />
```

### Hover States — Common Rules

| Situation | Do | Don't |
|-----------|-----|-------|
| Card hover | Color shift or shadow elevation | Scale transform that shifts layout |
| Button hover | Darken background 10%, slight shadow | No visual change |
| Link hover | Color + underline | Only underline (too subtle) |
| Icon button | Background fill on hover | Nothing |
| Destructive action | Red tint on hover | Same as normal hover |

### Icons

- Always use SVG icon sets (Lucide, Heroicons, Phosphor, Radix Icons)
- Never use emoji as UI icons
- Keep icons consistent from one library per project
- Standard size: 16px (inline text), 20px (buttons), 24px (standalone)
- Always pair icons with accessible labels: `aria-label` for icon-only buttons

---

## Phase 7: Accessibility — Non-Negotiable

Every interface delivered must pass these checks.

### ARIA & Semantic HTML

```tsx
// Form controls — always associated labels
<label htmlFor="email">Email address</label>
<input id="email" type="email" />

// Icon-only buttons — always labeled
<button aria-label="Close dialog">
  <XIcon size={20} aria-hidden="true" />
</button>

// Status messages — announced to screen readers
<div role="status" aria-live="polite">{statusMessage}</div>
<div role="alert" aria-live="assertive">{errorMessage}</div>

// Images — always alt text
<img src="..." alt="Descriptive text about the image" />
// Decorative images
<img src="..." alt="" aria-hidden="true" />
```

### Keyboard Navigation

- Tab order must match visual reading order
- All interactive elements reachable by keyboard
- Modals/drawers trap focus while open, return focus on close
- Escape key closes overlays
- Enter/Space activate buttons

### Color & Contrast Checklist

- Normal text on background: minimum 4.5:1
- Large text (18px+ regular, 14px+ bold): minimum 3:1
- Interactive element boundaries: minimum 3:1
- Use a tool like Stark or WebAIM Contrast Checker to verify
- Color is NEVER the only indicator of state (always pair with icon, label, or pattern)

---

## Phase 8: React Performance — Build Fast Interfaces

### Eliminating Waterfalls (CRITICAL)

Never chain async operations sequentially when they can run in parallel:

```tsx
// WRONG — sequential, creates waterfall
const user = await fetchUser()
const posts = await fetchPosts(user.id)
const comments = await fetchComments()

// RIGHT — parallel where possible
const [user, comments] = await Promise.all([fetchUser(), fetchComments()])
const posts = await fetchPosts(user.id) // depends on user, fetched after
```

### Bundle Size (CRITICAL)

```tsx
// WRONG — barrel import loads entire library
import { Check, X, ChevronDown } from 'lucide-react'

// RIGHT — direct import (significant size reduction)
import Check from 'lucide-react/dist/esm/icons/check'
import X from 'lucide-react/dist/esm/icons/x'

// Dynamic import for heavy components
const Chart = dynamic(() => import('./Chart'), { ssr: false })
const HeavyEditor = React.lazy(() => import('./HeavyEditor'))
```

### Re-render Optimization

```tsx
// Memoize expensive components
const ExpensiveList = React.memo(({ items }) => {
  return items.map(item => <ListItem key={item.id} item={item} />)
})

// Stable callbacks
const handleClick = useCallback((id: string) => {
  setSelected(id)
}, []) // empty deps — no external references

// Lazy state initialization for expensive initial values
const [state, setState] = useState(() => computeExpensiveDefault())

// Transitions for non-urgent updates (React 18+)
const [isPending, startTransition] = useTransition()
startTransition(() => setSearchQuery(value))
```

### Rendering Performance

```tsx
// Explicit conditional rendering — no implicit falsy renders
// WRONG — renders "0" when count is 0
{count && <Badge count={count} />}

// RIGHT
{count > 0 && <Badge count={count} />}

// Hoist static JSX outside components
const STATIC_HEADER = <h1 className="page-title">Dashboard</h1>

function Page() {
  return <div>{STATIC_HEADER}<Content /></div>
}
```

### Common Pitfalls

| Don't | Do |
|-------|-----|
| Barrel imports | Import from source files directly |
| Sequential awaits for independent data | `Promise.all()` |
| `items.sort()` mutating array | `items.toSorted()` |
| Create RegExp inside render | Hoist to module level |
| Heavy objects created in render | Hoist or memoize |
| Load analytics in critical path | Lazy-load with `dynamic()` |
| Re-render whole tree for local state | Extract to focused child component |

---

## Phase 9: Light/Dark Mode — Both Must Work

If the interface supports theming, both modes must be production-ready.

```css
/* Light mode defaults */
:root {
  --color-bg: #ffffff;
  --color-surface: #f8fafc;
  --color-text-primary: #0f172a;
  --color-text-secondary: #475569;  /* slate-600 minimum */
  --color-border: #e2e8f0;          /* gray-200 */
}

/* Dark mode */
[data-theme="dark"], .dark {
  --color-bg: #0a0a0f;
  --color-surface: #13131a;
  --color-text-primary: #f1f5f9;
  --color-text-secondary: #94a3b8;
  --color-border: rgba(255,255,255,0.08);
}
```

**Critical light mode rules:**
- Glass cards: `bg-white/80` or higher — never `bg-white/10` (invisible)
- Body text: `#0f172a` (slate-900) minimum — never gray-400 or lighter
- Muted text: `#475569` (slate-600) minimum
- Borders must be visible: `border-gray-200` not `border-white/10`

**Critical dark mode rules:**
- Surface backgrounds need enough contrast from page background
- Text on dark: ensure sufficient luminance difference
- Colored elements may need adjusted saturation for dark contexts

---

## Phase 10: Layout Patterns for MindStudio Interfaces

### Responsive Breakpoints

```css
/* Mobile first */
/* Default: 375px — single column, full width */
/* sm: 640px — slightly wider inputs, 2-col options */
/* md: 768px — side-by-side layouts possible */
/* lg: 1024px — full multi-column layouts */
/* xl: 1280px — maximum content width, generous margins */
```

Always verify:
- No horizontal scroll on mobile
- No content hidden behind fixed/sticky elements
- Tap targets at least 44x44px

### Common MindStudio Interface Layouts

**Single-step form:**
```
┌─────────────────────────────────┐
│  Header / Title                 │
│  Subtitle / Context             │
├─────────────────────────────────┤
│  Input Field 1                  │
│  Input Field 2                  │
│  Input Field 3                  │
├─────────────────────────────────┤
│                    [Submit CTA] │
└─────────────────────────────────┘
```

**Multi-step wizard:**
```
┌─────────────────────────────────┐
│  ●──○──○──○  Step 1 of 4       │
├─────────────────────────────────┤
│  Step Title                     │
│  Step Description               │
│                                 │
│  [Step-specific content]        │
├─────────────────────────────────┤
│  [Back]              [Next →]   │
└─────────────────────────────────┘
```

**Dashboard / data display:**
```
┌──────────┬──────────┬──────────┐
│  Metric  │  Metric  │  Metric  │
├──────────┴──────────┴──────────┤
│                                │
│  Chart / Main Content          │
│                                │
├───────────────┬────────────────┤
│  Table        │  Sidebar Info  │
└───────────────┴────────────────┘
```

### Navbar Rules

If the interface has a fixed navbar:
- Add `top-4 left-4 right-4` for floating effect (not `top-0 left-0 right-0`)
- Add padding-top to content equal to navbar height + gap
- Use same `max-w-6xl` or `max-w-7xl` as page content

---

## Phase 11: Industry-Specific Design Guidance

Use these as starting points, then differentiate within the direction.

### SaaS / B2B Tools
- Clean, data-forward, trust-building
- Neutral base (slate, gray) with a blue or indigo accent
- Dense information hierarchy, not decorative
- Typography: utilitarian but distinctive (Syne, Figtree, DM Sans)

### E-commerce / Retail
- Product-first — the UI should recede, product should shine
- Strong CTAs, clear value hierarchy
- Fast-loading, mobile-optimized above all
- Trust signals: ratings, reviews, guarantees near purchase actions

### Healthcare / Wellness
- Calm, reassuring, clinical clarity
- Blue-green, soft sage, white — never alarming colors
- Extra accessibility rigor: larger text defaults, clearer labels
- No unnecessary animation — focus over delight

### Fintech / Finance
- Precise, authoritative, secure-feeling
- Deep navy, charcoal, gold accent — never playful
- Data accuracy visual cues: monospace numbers, clear decimal alignment
- Typography: sharp serifs or clean geometric sans

### Beauty / Luxury
- Atmosphere over function
- Generous whitespace, refined typography (Cormorant, Playfair)
- Muted, sophisticated palette — champagne, rose, deep forest
- Subtle animations, hover reveals, image-forward

### Creative / Agency
- The interface IS the portfolio
- Bold choices: oversized type, unexpected layouts, strong color
- Can break conventions — asymmetry, overlapping elements, diagonal flow
- Signature moment: the one thing they'll remember

---

## Phase 12: Pre-Delivery Checklist

Run every item before delivering code. No exceptions.

### Visual Quality
- [ ] No emoji used as UI icons — all icons are SVG (Lucide/Heroicons/Phosphor)
- [ ] All icons from one consistent library
- [ ] No generic fonts (Inter, Roboto, Arial) used as the primary display font
- [ ] Aesthetic direction is clearly committed — not a generic mix of styles
- [ ] Color palette has clear hierarchy: dominant, accent, semantic
- [ ] Light mode text contrast passes 4.5:1 (body), 3:1 (large text)
- [ ] Backgrounds have depth — not flat solid colors

### Interaction
- [ ] All clickable/interactive elements have `cursor: pointer`
- [ ] All hover states provide visible feedback (color, shadow, or border)
- [ ] All transitions use `transform`/`opacity` (not layout properties)
- [ ] Transition durations: 150-200ms for micro-interactions, 300ms for major transitions
- [ ] Loading states exist for all async operations
- [ ] Error states are visible, inline, and actionable
- [ ] Disabled states are visually distinct

### Layout & Responsive
- [ ] No horizontal scroll at 375px viewport
- [ ] No content hidden behind fixed navbars
- [ ] Consistent max-width container used throughout
- [ ] 8-point spacing grid respected
- [ ] Floating navbars have edge spacing (`top-4 left-4 right-4`)
- [ ] Touch targets minimum 44x44px on mobile

### Accessibility
- [ ] All images have descriptive `alt` text (or `alt=""` for decorative)
- [ ] All form inputs have associated `<label>` elements
- [ ] Icon-only buttons have `aria-label`
- [ ] Focus states are visible (`focus-visible` outline)
- [ ] Tab order matches visual reading order
- [ ] Color is not the only indicator of state
- [ ] `prefers-reduced-motion` media query respected
- [ ] Error messages use `role="alert"` or `aria-live="assertive"`

### Light/Dark Mode (if applicable)
- [ ] Light mode glass/transparent elements visible (opacity ≥ 0.6)
- [ ] Light mode muted text ≥ slate-600 (`#475569`)
- [ ] Dark mode borders visible (not `border-white/10` on dark bg)
- [ ] Both modes tested visually before delivery

### React Performance
- [ ] No barrel imports from large libraries
- [ ] Independent data fetches use `Promise.all()`
- [ ] Expensive components wrapped in `React.memo` where appropriate
- [ ] Stable callbacks use `useCallback` with correct dependencies
- [ ] No implicit falsy renders (`count && <X />` replaced with `count > 0 && <X />`)
- [ ] No RegExp or heavy objects created inside render functions
- [ ] Dynamic imports used for non-critical heavy components

### MindStudio Compatibility
- [ ] No `<form>` HTML tags — using `onClick`/`onChange` handlers
- [ ] No SSR-only APIs (no Next.js-specific routing/image APIs unless confirmed)
- [ ] Single default export from the root component
- [ ] All state is local (no external state management unless explicitly requested)
- [ ] Component compiles without errors in MindStudio's React environment
- [ ] `submit` and `useIsRunning` imported from `./bridge` — never `window.MindStudio.submit`
- [ ] Submit button uses `useIsRunning()` from bridge for loading state — no manual `setTimeout` or status state
- [ ] `submit(data)` is called with all variable values on final submission
- [ ] Every input field is wired to its confirmed MindStudio variable name — no invented or generic names (`input1`, `field_value`, etc.)
- [ ] State keys match the exact variable names confirmed during discovery
- [ ] Variable reference comment block at the top of the component lists all output variables with their types and descriptions

---

## Quick Reference Card

### Font Pairings (Never Use Inter/Roboto/Arial as Primary)

| Mood | Display | Body |
|------|---------|------|
| Luxury | Cormorant Garamond | Lora |
| Editorial | Playfair Display | Source Serif 4 |
| Technical | Syne | JetBrains Mono |
| Approachable | Nunito | DM Sans |
| Minimal | Fraunces | Figtree |
| Bold | Bebas Neue | IBM Plex Sans |
| Modern | Outfit | Manrope |
| Organic | Vollkorn | Nunito Sans |

### Animation Timing Cheat Sheet

| Interaction | Duration | Easing |
|-------------|----------|--------|
| Hover state | 150ms | ease-out |
| Button active | 100ms | ease |
| Tooltip appear | 150ms | ease-out |
| Modal open | 300ms | cubic-bezier(0.16, 1, 0.3, 1) |
| Page transition | 400ms | cubic-bezier(0.16, 1, 0.3, 1) |
| Stagger delay | 60ms per item | — |
| Reduced motion | 0.01ms | — |

### Shadow Scale

| Level | Value |
|-------|-------|
| Subtle | `0 1px 2px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.08)` |
| Card | `0 2px 4px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.10)` |
| Modal | `0 4px 8px rgba(0,0,0,0.06), 0 16px 48px rgba(0,0,0,0.14)` |
| Colored | `0 8px 24px rgba(PRIMARY_RGB, 0.25)` |

### Responsive Breakpoints (Mobile First)

| Breakpoint | Width | Layout |
|------------|-------|--------|
| default | 375px | Single column |
| sm | 640px | 2-col options |
| md | 768px | Side-by-side |
| lg | 1024px | Full multi-col |
| xl | 1280px | Max-width constrained |

---

## Design Principles — The Foundation

These principles govern every decision made with this skill:

1. **Discovery before design.** Never assume. Ask first, build second.
2. **Commit fully.** A half-executed aesthetic is worse than any aesthetic. Pick a direction and own it.
3. **The interface serves the workflow.** This is inside a MindStudio AI agent. Function is as important as form.
4. **Unforgettable over safe.** Generic is forgettable. Make one bold choice and everything else will follow.
5. **Accessibility is baseline.** No interface ships without passing contrast, label, and keyboard checks.
6. **Performance is a feature.** Fast interfaces feel better. Eliminate waterfalls, control bundle size.
7. **Details compound.** The difference between good and great is 20 small decisions made correctly.
8. **One question at a time.** Never overwhelm users during discovery. Slow down to go faster.
9. **YAGNI ruthlessly.** Every feature that doesn't serve the stated need is a liability.
10. **Measure twice, build once.** Present the design plan before coding. Validate before implementing.
