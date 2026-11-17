# Anti-slop bans

Borrowed from the frontend-slides quality bar — fonts and palettes that instantly read as generic AI output.

## Fonts — never default to these

| Banned | Why |
|--------|-----|
| Inter | Default “startup” face — zero personality |
| Roboto | Android/system generic |
| Arial / Helvetica as display | Lazy fallback |
| Poppins everywhere | 2023 AI slide fingerprint |
| Space Grotesk **as the only** display on every slide | Fine as part of a pairing, not alone on every deck |

Prefer distinctive pairings from the theme packages (Archivo Black, Fraunces, Orbitron, Playfair, IBM Plex Mono, etc.).

## Colors — never default to these

| Banned | Why |
|--------|-----|
| `#6366f1` / indigo-500 as sole accent | Tailwind AI purple |
| Purple-on-white gradients | Peak slop |
| `#667eea` → `#764ba2` hero gradients | Overused template |
| Rainbow accents on one slide | No hierarchy |
| Warm cream `#F4F1EA` + terracotta as a “safe” default when the brief isn’t paper/editorial | Samey AI-deck fingerprint — pick a theme with a real surface (signal, aurora, blueprint, kinetic) |
| Dark mode + purple glow for every “tech” deck | Lazy neon; prefer `developer-dark`, `aerospace-hud`, `blueprint`, or `default-tech` with discipline |

Use the theme's `--accent` and `--accent-2` roles. If custom, pick **one** dominant accent + one supporting hue.

## Site / product chrome (presentation-md brand)

When designing marketing UI or Studio chrome for this pack — not slide themes — use **signal-grid**:
cool paper `#E8EEF4`, signal red `#FF3B1F`, **Syne / DM Sans / IBM Plex Mono**. Never Inter-on-purple dashboards.

## Layout tells (see also Deadly Sins in SKILL.md)

- Accent line under every title
- Identical 3-column card grid on every slide
- Centered body paragraphs
- Lorem ipsum or `[Company Name]` placeholders

## One-shot first draft (beat frontend-slides)

The first JSON you emit must already clear this file. Do **not** ship a purple/Inter/cream “vibe draft” hoping a rewrite fixes it.

1. Lock a real theme (stunning-25 or popular shortlist) before writing slides.
2. Lock density (speaker-led vs reading-first) once.
3. Force asymmetry (`emphasis`, non-1-1 `ratio`, or `bento`) on the first body beat.
4. Call `audit_deck` — fix errors before the user sees the draft.
5. Ban stock illustration SVGs and placeholder art — real product/place imagery or typographic craft only.
6. Prefer schema layouts; at most **one** intentional `custom-html` art beat (see `custom-html-recipes.md`) — never stickers for theme atmosphere.

## Enforcement

1. Pick a theme from `theme-selection-index.json` (don't invent colors ad hoc)
2. Run `preview_themes` — user must **see** the vibe before the full deck
3. Run `audit_deck` + optional `deck-design-judge` before shipping
4. For paper/editorial themes, refuse SaaS three-up card stacks — demand magazine cadence (quote, comparison+emphasis, short literary leads)
5. Prefer shipping HTML when quiet fiber grain / mix-blend is the brand; PPTX keeps washes, frames, and mastheads only
