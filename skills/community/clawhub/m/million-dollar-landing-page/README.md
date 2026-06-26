# Million Dollar Landing

> Transform a generic landing page into a high-converting product that makes visitors feel like they've landed on a million-dollar company.

## What's included

| File | Purpose |
|---|---|
| `resources/design-tokens.css` | Glass surfaces, dot-grid, gradient-border, marquee, animations — all brand-color aware via CSS variables |
| `resources/tailwind-config-additions.js` | Animation keyframes + brand color tokens |
| `resources/cursor-glow.tsx` | Mouse-tracking brand-color radial gradient overlay |
| `resources/scroll-progress.tsx` | Right-edge scroll depth indicator bar |
| `resources/scroll-reveal.tsx` | Framer Motion fade-in-up on scroll |
| `resources/marquee.tsx` | Infinite horizontal scroll strip — platforms, logos, features, social proof |
| `resources/terminal-steps.tsx` | Animated dark terminal for the Agitate section |

## Three Pillars

### 1. Copy (PAS Formula + Fewer Words)
- Problem → Agitate → Solve structure for every section
- Audience framing: your customer didn't take on their role to deal with the problem you solve
- Mandatory "fewer words" pass: cut 30–40%, keep 100% of the message
- Guarantee before final CTA; comparison table with your product column

### 2. Visual (Dark Glass Design System)
- Deep dark background with layered radial gradient depth
- Glass surfaces with `backdrop-filter: blur + saturate`
- Brand accent color (fully customisable via `--brand-rgb` CSS variable) for all CTAs and active states
- Sora (display) + DM Sans (body) + JetBrains Mono fonts
- Staggered `animation-delay` fade-up on hero entry
- `CursorGlow` + `ScrollProgress` on root layout
- `ScrollReveal` wrapping every major section
- `Marquee` after hero, `TerminalSteps` in Agitate section

### 3. Mobile (Responsive Hardening)
- `min-w-0` on all grid/flex children prevents overflow
- `overflow-x-auto` wrapper on all wide tables
- iOS Safari: all inputs `font-size ≥ 16px` or auto-zoom fires
- `html, body { overflow-x: hidden; max-width: 100vw }`
- Mobile-first type scale: `text-4xl md:text-6xl lg:text-7xl`
- Dashboard: fixed sidebar on desktop, off-canvas drawer on mobile

## Quick start

```bash
# 1. Install via Claude Code skills
npx skills add Flacko2048/million-dollar-landing

# 2. Install dependency
npm install framer-motion

# 3. Add fonts in layout.tsx
#    Sora + DM Sans + JetBrains Mono via next/font/google

# 4. Merge design-tokens.css into globals.css
#    Set --brand-rgb and --brand-complement-rgb to your brand colors

# 5. Merge tailwind-config-additions.js into tailwind.config.js
#    Update the `brand` color object to your palette

# 6. Copy components into src/components/landing/
```

Then ask Claude (with this skill loaded):

> "Transform my landing page using the million-dollar-landing methodology"

## Requirements

- Next.js 14+ (App Router)
- Tailwind CSS
- framer-motion

## License

MIT — built by [Flacko](https://github.com/Flacko2048)
