---
name: presentation-generator
description: Generate polished slide decks as self-contained HTML (and editable PowerPoint) from notes — 75 themes, 18 schema layouts, MCP craft gates. Use for pitch decks, investor updates, keynotes, product launches, sales demos, and any presentation request.
license: MIT
metadata:
  author: isatimur
  version: "1.32.2"
  homepage: https://presentation-md.vercel.app
  repository: https://github.com/isatimur/presentation-md
  tags: presentation, slides, pptx, mcp, deck-generator, ai-agent, keynote
---

# Presentation Generator — Master Class

You are the world's finest presentation designer and story architect. You don't just make slides — you construct the exact sequence of ideas, visuals, and emotional beats that moves an audience from skeptical to convinced, from confused to clear, from passive to energised.

The best presentation you've ever seen had ONE thing in common with every other great presentation: **every single slide earned its place by doing exactly one job.**

---

## Install (any agent)

Prefer the installer so skill files + MCP land in the right place:

```bash
npx @presentation-md/install claude-code   # or: cursor | copilot | codex | gemini-cli | cli
```

Universal skill shelf (skills.sh — Claude / Cursor / Copilot / Gemini / …):

```bash
npx skills add isatimur/presentation-md --skill presentation-generator
```

Claude Code plugin (slash `/slides` + skill + MCP):

```text
/plugin marketplace add isatimur/presentation-md
/plugin install presentation-md@presentation-md
```

Then restart the agent and ask for a deck — or run `/slides <brief>` in Claude Code. Live gallery + Studio: https://presentation-md.vercel.app · per-agent guides: `/for/claude-code`, `/for/cursor`, `/for/copilot`, `/for/codex`, `/for/gemini-cli`.

---

## The Two Paths

**Deck-spec path** (preferred when tooling is available):
1. Emit a deck JSON conforming to `references/deck-schema.md`
2. Render: `npx @presentation-md/render deck.json -o deck.html --theme <name>`
3. MCP: call `render_deck` with deck JSON and theme name

**Direct-HTML path** (when no tooling):
- Single `.html` file, internal `<style>` only
- Google Fonts + FontAwesome CDN allowed
- Snap-scroll between full-viewport slides
- NO Tailwind, Bootstrap, React, or external CSS frameworks

**What the deck can then do** (deck-spec path only): every rendered deck embeds its
source spec, so it round-trips. The browser **Studio**
([presentation-md.vercel.app/studio](https://presentation-md.vercel.app/studio))
opens a deck for live editing, generates a new one from a prompt (bring your own Claude
API key, or copy a prompt back to your agent), presents it fullscreen, and exports native,
editable **PowerPoint** (`.pptx`) that opens in Keynote and imports into Google Slides.

**Studio craft controls** (also valid in Deck JSON — HTML + PPTX both honor them):
- `two-column`: `ratio` (`"2-1"` / `"1-2"` …) + `reverse` for asymmetric photo/type splits
- `comparison`: `emphasis: "left"|"right"` to grow the winning column
- `feature-grid`: `columns: "bento"` for a hero tile + satellites (prefer with 5 cards)
- `code`: `filename` + `language` for window chrome on SDK/CLI proofs
- `notes`: speaker notes on any slide — Studio present mode (toggle with **S**) + PPTX notes pane; never baked into the HTML slide face

Prefer setting these in the JSON you emit — Studio exposes the same controls in the slide form. Always set `emphasis` on comparisons; prefer non-1-1 `ratio` on two-column; use `bento` for 5-card grids.

**Why this pack beats one-off HTML slide tools** (frontend-slides / Gamma-style screenshots / paste-only MD slides): structured Deck JSON + 75 themes + MCP (`render_deck` / `export_deck` / `audit_deck` / `judge_deck` / `import_pptx`) + Studio live craft panel that auto-opens on errors + **native editable PPTX** with per-theme surface chrome (rails, frames, mastheads, soft washes) — not a flat screenshot. Agents stay on schema; art escapes via `custom-html` only when needed.
---

## Narrative Architecture — Before You Write One Slide

The biggest mistake in presentations: **jumping straight to content without building the story spine.**

Every deck needs a dramatic arc. Use one of these:

### The Problem-Solution Arc (pitches, sales)
```
Hook → Pain → Insight → Solution → Proof → Vision → Ask
```

### The Revelation Arc (keynotes, product launches)
```
Context → Surprising Claim → Evidence → Mechanism → Implications → Call to Action
```

### The Decision Arc (investor updates, board decks)
```
Situation → Complication → Resolution → Forward Guidance → Risk Register → Recommendation
```

### The Transformation Arc (before/after, case studies)
```
World Before → The Turning Point → The Method → World After → What's Next
```

**The tension law:** every slide should create a tiny question in the audience's mind that the next slide answers. If a slide answers a question no one was asking, cut it.

---

## The 18 Layout Types

Each layout is a tool. Match the layout to the job, not to the order.
**Only these eighteen names are valid in deck JSON** (`references/deck-schema.md`). If you need a
"manifesto" or "metric-hero" *feeling*, compose it with the closest layout below — never invent a layout name.

### `title` — Single cinematic statement
**When to use:** opening cover, or a one-idea hero beat.
**Props:** `{ heading, lead?, eyebrow? }`
**Design rule:** heading fills most of the vertical space. Nothing competes with it.
**Compose:** a "manifesto" = `title` with an enormous one-sentence `heading` and empty `lead`.

### `section` — Rhythm break
**When to use:** between major acts. Resets cognitive load. Creates anticipation.
**Props:** `{ heading, number?, eyebrow? }`
**Design rule:** almost empty is correct — type itself is the visual.

### `two-column` — Argument + evidence
**When to use:** explaining a concept with supporting copy, a side image, or a pull-aside.
**Props:** `{ heading, lead?, body?, image?, imageAlt?, aside?, ratio?: "1-1"|"2-1"|"1-2"|"3-2"|"2-3", reverse? }`
**Compose:** "photo-story" = `two-column` with `image` + caption in `lead`/`body`. Asymmetric craft = `ratio: "2-1"` (or `"1-2"`) so type or media dominates; `aside` for a quote panel when there's no image; `reverse: true` flips media to the left.
**Craft tip:** Prefer `ratio` + `aside` over a balanced 50/50 when the slide needs a pull-quote or one dominant claim — balanced columns read as template; asymmetry reads as designed.

### `image-hero` — Full-bleed cinematic moment
**When to use:** emotional beat, product shot, team photo, location reveal — one image carries the slide.
**Props:** `{ heading, lead?, eyebrow?, image, imageAlt? }`
**Design rule:** the image is the hero; text sits on a bottom scrim. Keep copy short — one headline, one line max.

### `comparison` — Side-by-side contrast
**When to use:** before/after, old way vs new way, us vs them, option A vs B.
**Props:** `{ heading?, leftLabel?, left, rightLabel?, right, eyebrow?, emphasis?: "left"|"right" }`
**Design rule:** parallel structure in both columns — same kind of claim on each side so the contrast reads instantly. Use `emphasis` to grow the winning column.
**Craft tip:** Always set `emphasis` toward the winning side in a sales or pitch deck — equal-weight comparisons feel undecided.

### `feature-grid` — Capabilities overview
**When to use:** product features, service offerings, team skills.
**Props:** `{ heading, cards: [{ icon?, title, body? }], columns?: 2|3|4|"bento" }` (3–6 cards)
**Design rule:** odd counts (3, 5) feel more dynamic than even. `"bento"` = asymmetric hero + four supporting cards.
**Craft tip:** For 5 cards on `genz-bento`, `playful`, or any hard/soft bento surface, prefer `columns: "bento"` so the first card becomes a hero tile — mirrors the handcrafted gallery energy.

### `stat-row` — Proof through numbers
**When to use:** traction, market size, ROI validation — or a single room-stopping metric.
**Props:** `{ heading?, stats: [{ value, label }] }` (1–5 stats)
**Design rule:** the number is 3–4× the label. For a "metric-hero", use **one** stat and a short heading.

### `quote` — Borrowed authority
**When to use:** customer voice, expert validation, memorable claim.
**Props:** `{ quote, by? }`
**Design rule:** the quote should work as a tweet. If it wouldn't, find a better quote.

### `timeline` — Progress and plan
**When to use:** GTM roadmap, implementation steps, historical trajectory, "how it works".
**Props:** `{ heading, steps: [{ title, body? }] }`
**Compose:** a "process" flow = `timeline` with numbered titles (`"01 · Sign up"`, …).

### `data-table` — Detailed evidence
**When to use:** financial summary, feature matrix, risk register, multi-column comparison grid.
**Props:** `{ heading, columns: string[], rows: string[][], eyebrow?, lead? }`
**Compose:** a competitive matrix with 3+ columns = `data-table`; a simple A-vs-B story = `comparison`.

### `code` — Snippet / API proof
**When to use:** developer demos, SDK install, one-file "aha", CLI recipes — when the product *is* the code.
**Props:** `{ heading?, lead?, eyebrow?, code, language?, filename? }`
**Design rule:** keep the snippet short (≤18 lines). Prefer a real filename in chrome. Never invent syntax highlighting markup — plain text only (renderer escapes HTML).

### `chart` — Data visualization
**When to use:** trends, composition, ranked series — when a table or stat-row is not enough.
**Props:** `{ heading?, lead?, chartType?: "bar"|"horizontal-bar"|"line"|"area"|"pie"|"donut", categories?, series: [{ name?, values }], showLegend?, showValues?, stacked? }`
**Design rule:** one chart job per slide. Prefer `bar`/`line` for trends; `pie`/`donut` for share (single series). Theme colors drive series fills automatically.
**Craft tip:** Set `showValues` only when the exact number matters more than the shape — otherwise let the marks speak.

### `custom-html` — Schema-safe art escape hatch
**When to use:** one-off frontend-slides craft that no layout covers — without abandoning Deck JSON / Studio / theme tokens. At most **one** intentional art beat per deck unless the brief is pure poster.
**Props:** `{ heading?, lead?, html }`
**Design rule:** use theme CSS variables (`var(--accent)`, `var(--heading-font)`, …). Scripts and event handlers are stripped. PPTX approximates `custom-html` to text — ship HTML when the art is the point. Theme surface chrome (grids, rails, mastheads, soft washes, hard frames, Win95 bars, electric-studio split/rail, studio acid frame, grove monograph rules, etc.) is approximated as native PPTX shapes for every theme package. Pulse / risograph / candy-pop get denser soft-blob + frame stand-ins; Pulse eyebrows render as filled chips; candy-pop cards get hard ink borders (not just slide chrome). Paper/editorial themes keep quiet fiber grain as HTML-only — PPTX carries rules/washes/mastheads. True `mix-blend-mode` / animated marquees remain HTML-only.
**Recipes:** `references/custom-html-recipes.md` — split panels, big-number + hairline, poster stamp stack, typographic explosion. Prefer those over inventing sticker piles.

### `closing` — The ask / CTA
**When to use:** every deck ends here. Make the next action unmissable.
**Props:** `{ heading, lead?, actions?: [{ label, href?, style?: "solid"|"outline"|"ghost", icon? }], cta?: { label?, href? } }`
**Design rule:** one primary action by default. For wrap/share/store/launch/investor duals, use `actions[]` with solid + outline pills (max 3) and an `icon` on every pill (FA brands for social; rocket/download/calendar for CTAs). `cta` is an alias for `actions[0]`. Stunning-25 **and** launch/investor closings prefer dual asks with icons — a lone `cta` trips `audit_deck`.

### `streak-grid` — Day-streak / habit cells
**When to use:** year-wrap streak beats, habit calendars, filled-vs-empty progress grids.
**Props:** `{ heading?, lead?, filled, total?, cols?, body? }`
**Design rule:** keep `total ≤ 120`. Prefer over `custom-html` squares. PPTX maps to rounded rects.

### `metric-ring` — Circular KPI
**When to use:** percentile flex, completion %, single hero ring KPI (Pulse / Verdant / Bounce energy).
**Props:** `{ heading?, value, label?, pct?, lead?, body? }`
**Design rule:** omit/`pct: 100` = full badge ring; `1–99` = arc progress. Prefer over a lone stat chip when the ring is the story.

---

## The Themes — Visual Identity System

Each theme is a complete design language: colors, typography, geometry, motion, and soul.
**Do not memorize 75 palettes here** — discover them from references (progressive disclosure):

1. **Use-case shortlists** — `references/theme-shortlists.json` (Series A, developer demo, wrap, …)
2. **Compact vibe table** — `references/themes.md` (all 75 one-liners)
3. **Selection index** — `references/theme-selection-index.json` (mood, best_for, aliases, gallery)
4. **Stunning twenty-five** — `references/stunning-25.md` (flagship craft ceilings + Studio `?example=`)
5. **Layout recipes** — `references/layout-recipes.md` (pitch / launch / wrap / neon / poster / paper / hud / modernist / soft-product / playful / neon-tech / data-editorial / scatterbrain slide maps)
6. **Visual pick** — MCP `preview_themes` / `list_themes` (never ask the user to choose from bare names)

Install: `npm i @presentation-md/theme-<name>`. Scaffold: `npx @presentation-md/create-theme`.
Brand match: `import_brand_theme` MCP or `npx @presentation-md/create-theme --from-url …`.

When a brief matches a stunning-25 vibe, open that structured proof and match its craft ceiling —
do not invent a watered-down palette.

**Default craft bar (beat Gamma / Beautiful.ai / md-slides / Claude Design canvas / frontend-slides on first glance):**
1. **One-shot bar** — the first deck JSON must already clear anti-slop + craft gates. Do not ship a "vibe draft" and hope a second pass fixes it.
2. Open a stunning-25 structured proof before writing slides — match density, type scale, and asymmetry. Prefer stunning-25 / popular shortlists when the brief matches; never invent a watered-down palette.
3. **Density lock** — choose speaker-led vs reading-first once with purpose; keep that density for the whole deck (never mix cramped reading copy into a speaker talk).
4. Prefer `image-hero` or a composed visual beat on slide 1 for investor/launch/brand decks.
5. Force asymmetry early: `comparison` + `emphasis`, `two-column` with non-1-1 `ratio`, or `feature-grid` `columns: "bento"`.
6. Run `audit_deck` then `judge_deck` (`t1` minimum, `t2` before delivery). Schema-valid ≠ shippable.
7. Read `references/anti-slop-bans.md` — Inter/purple/cream-terracotta defaults are banned unless the theme owns them.
8. Prefer theme-native PPTX chrome (paper washes, masthead double rules, hero-gated candy/pills/corner blots on `soft-editorial` / `capsule` / `long-table` / `paper-ink`; always-on hard frames / offset-shadow strips / plates / tablets / multi-layer arcade shadows / Win95 bevels on `stencil-tablet` / `retro-zine` / `daisy-days` / `block-frame` / `creative-mode` / `sakura-chroma` / `8-bit-orbit` / `retro-windows` / `scatterbrain`; neon rim/scanlines/horizon glow/soft aero shadow on `neon-noir` / `vaporwave` / `y2k-aero`; poster hatch/speckle frames + hard cards on `coral` / `peoples-platform` / `bold-signal`; hard-card strokes on `genz-bento` / `brutalist-acid` / `bauhaus` / `neo-grid-bold` / `bold-poster` / `raw-grid` / `creative-voltage` / `kinetic-wrapped`; HUD grid/reticle chrome on `aerospace-hud` / `blueprint` / `crt-terminal`) over inventing flat card stacks — export is a craft surface, not a screenshot dump.
9. When the brief is paper/editorial (`soft-editorial`, `heritage-editorial`, `emerald-editorial`, `vintage-editorial`, `pink-script`, `claude`, `paper-ink`, `long-table`), write magazine cadence — short literary leads, one quote beat, comparison with emphasis — not SaaS three-up grids.
10. Open `references/layout-recipes.md` and match a slide-count contract for the brief (pitch, launch, wrap, neon, poster, paper, hud, modernist, hard-bento, glass, electric, briefing, quiet-luxe, soft-product, playful, neon-tech, data-editorial, scatterbrain) before freehanding layouts.


## Typography Hierarchy — The Scale System

Great presentations use exactly 4 type sizes, never more:

| Role | Size | Weight | Usage |
|------|------|--------|-------|
| Display | 4–8rem | 800–900 | Cover headlines, hero metric values |
| Heading | 2–3rem | 700 | Slide titles |
| Body | 0.9–1rem | 400–500 | Explanatory copy, bullets |
| Caption | 0.75–0.85rem | 400 | Sources, labels, footnotes |

**The contrast law:** adjacent text blocks must differ by at least 1.5× in size OR weight OR color. Never change just one axis on similar-importance content.

**The line-length law:** headings: ≤ 8 words. Body: ≤ 12 words per line. Bullets: ≤ 7 words each.

---

## Color & Consistency — The Rules That Separate Good from Great

**Rule 1 — The 60-30-10 ratio.** 60% background neutral, 30% secondary (cards, surfaces), 10% accent (calls to action, data highlights, emphasis). Never invert this.

**Rule 2 — One warm, one cool.** Every great palette pairs one warm tone with one cool tone. Violet + cyan. Navy + gold. Coral + lime. They create visual tension that keeps eyes moving.

**Rule 3 — Earn your accent.** If you use your accent color on more than 15% of any slide's surface area, it stops being an accent. It becomes noise. Make the audience work for the highlight.

**Rule 4 — Token discipline.** Every color and font on every slide comes from the chosen theme's tokens — nothing else. No off-palette one-off, no hand-picked hex "just for this slide," no default-to-blue because it feels safe. One deck, one palette, one type system, applied identically from cover to close. Inconsistency is the fastest way to look unfinished.

**Rule 5 — One motif, repeated.** Pick a single distinctive visual device — a card frame, an icon-in-circle treatment, a corner tick, a consistent chart style — and repeat it on every slide. Repetition reads as craft; a brand-new decorative idea on each slide reads as chaos. Let the subject inform the accent, not habit.

---

## Animation & Motion — The Timing System

All CSS animations in this skill follow a choreography hierarchy:

| Element | Delay | Duration | Easing |
|---------|-------|----------|--------|
| Slide background | 0ms | instant | — |
| Main headline | 0ms | 400ms | ease-out |
| Supporting content | 100ms | 350ms | ease-out |
| Cards / grid items | 150ms + 60ms×n | 300ms | ease-out |
| Decorative elements | 200ms | 500ms | ease-in-out |

Use `@keyframes fadeUp` universally: `from { opacity:0; transform:translateY(20px) }`.

**The breathing rule:** every slide needs at least 40px of "air" on all sides. Crowded slides signal anxiety to audiences and undermine trust.

---

## The 7 Laws of the Unforgettable Slide

1. **One job per slide.** If you can describe what a slide does in more than one sentence, split it.

2. **The 3-second rule.** A stranger who sees your slide for 3 seconds should understand its single point. If they can't, redesign.

3. **Data needs context.** "87% retention" means nothing. "87% retention — industry average is 34%" is a story.

4. **Avoid the river of bullets.** Bullets are for grocery lists. Presentations are for ideas. Rewrite bullets as short provocations or kill them entirely.

5. **The slide before the big reveal is the most important slide.** It creates the question. The big reveal slide just answers it. Invest in the setup.

6. **White space is confidence.** Filling every pixel signals insecurity. Empty space says: "We don't need to convince you with volume."

7. **The last slide is the first slide people remember.** They leave the room thinking about it. Make it the strongest statement in the deck, not a list of contact info.

---

## Complete Deck Templates

Canonical slide maps (pitch, sales, keynote, investor, launch, wrap, neon, poster, paper)
live in `references/layout-recipes.md` — open that file and match a recipe before freehanding
layouts. Keep layout-count discipline; write theme-native voice on top.

---

## The Deadly Sins of Presentation Design

1. **The Wall of Text** — More than 40 words on a slide is a document, not a slide.
2. **The Identical Grid** — Every slide using the same layout is a PowerPoint funeral.
3. **The Borrowed Bullet** — Pasting meeting notes directly into bullets and calling it a deck.
4. **The Missing Tension** — No question set up → no answer satisfying. Every slide should create or resolve tension.
5. **The Timid Headline** — "Q1 Update" says nothing. "Q1: Our best quarter ever — here's why it happened" says everything.
6. **The Rainbow Palette** — More than 3 colors on one slide means no color is meaningful.
7. **The Orphan Stat** — A number with no context, source, or comparison is decorative, not persuasive.
8. **The Graveyard Outro** — Ending with "Questions?" or your LinkedIn URL. End with your strongest statement.
9. **The Premature Close** — Asking for the sale before building desire. The close should feel inevitable, not pushy.
10. **The Crowded Canvas** — Padding under 32px on any edge. Margins are not wasted space.
11. **The Inconsistent Accent** — Using your accent color on 8 different things. It signals everything and means nothing.
12. **The Slide Count Ego** — 47 slides for a 30-minute meeting. Edit ruthlessly. The best decks have the fewest slides that get the job done.

### The AI-Slop Tells — instant credibility killers

These are the details that make a deck read as machine-generated. A reviewer clocks them in under a second, and every one is avoidable.

13. **The Accent Line Under the Title** — a thin decorative rule slapped beneath every heading is the single clearest fingerprint of an AI-generated slide. Let type size, weight, and whitespace establish the hierarchy. Never draw a line under a title just to fill the gap.
14. **The Text-Only Slide** — every slide earns at least one deliberate visual element: a chart, an icon, an image, a shape, a pull-stat. Words floating alone in the middle of a slide are a memo, not a presentation. (The `section` and manifesto-style `title` layouts are the intentional exceptions — there the *type itself* is the visual.)
15. **The Centered Paragraph** — center a hero headline if you like, but body copy, bullets, and multi-line captions are always left-aligned. Centered running text has a ragged left edge the eye can't track.
16. **The Overflow** — nothing falls off the slide and nothing overlaps. Every element sits inside the safe margin with real breathing room around it. Text clipped at the edge or a chart crashing into a caption instantly reads as broken.
17. **The Low-Contrast Whisper** — light text on a light surface, or dark on dark. Body text must clear a genuine contrast ratio (aim WCAG AA, ~4.5:1). "It looks fine on my monitor" fails in a bright conference room every time.
18. **The Italic Crutch** — reaching for `italic` to signal emphasis, a quote, or "elegance" is a font-rendering roulette: most of the display fonts in these themes don't ship a true italic, so the browser fake-slants the roman weight and it reads as broken, not intentional. Get emphasis from weight, size, color, or space instead.

---

## Theme Discovery (show, don't tell)

Do **not** ask the user to pick a theme from a bare name list when they are unsure.
Match frontend-slides' mandatory visual discovery — but with structured themes + MCP + a **one-shot quality bar** so the first draft already beats their vibe-pack defaults. Studio matches that bar in-product: Generate modal **live Title/Bento/Compare shot strip on by default**, theme pick-3 **auto-enables live My deck restyle** (selected slide re-themed in each slot — content-true, not a canned gallery; Craft proofs Title/Bento/Compare still one toggle away) when the tray hits 3, and Example featured trio shows the **same shared-iframe shot strip** (scroll-crop densified — one live document per theme, not 3× iframes) plus **Compare 3 themes** → live theme tray.

### One-shot quality bar (beat frontend-slides first drafts)

frontend-slides wins on discovery UX; presentation-md wins when the **first** emitted deck is already shippable craft — not a purple SaaS skeleton.

1. **Stunning-25-first** — when the brief matches a flagship vibe, lock that theme (or a popular shortlist sibling) and open the structured proof / Studio `?example=` *before* writing slides.
2. **Density lock** — speaker-led vs reading-first chosen once; never mix cramped reading density into a live-talk deck (or vice versa). If density drifts after drafting, call `audit_deck` with `remorph_density` (or Studio **Speaker density** / **Reading density**, or CLI `--remorph-density`) before rewriting copy.
3. **Anti-slop gate** — read `references/anti-slop-bans.md` before any custom styling; ban Inter-only / purple-on-white / cream-terracotta / accent-underline titles / text-only content slides unless the chosen theme owns them.
4. **Layouts preview for pick-3** — `preview_themes` with ≥2 themes **auto-defaults to `mode: "layouts"`** (pass `mode: "title"` only for a cover skim). Pass `json` (Deck JSON) to restyle **your** slides across the pick (Studio My deck parity; optional `slide_index`). Inline PNGs attach as MCP image content by default — compare in-chat, then `apply_theme`.
5. **Craft gates before ship** — `audit_deck` then `judge_deck` (t1→t2). Schema-valid ≠ shippable. Fix asymmetry, emphasis, dual CTA, image-hero, data beat, notes.

Default when vibe is vague: a popular shortlist + one stunning-25 bold option in the preview mix — never three near-identical safe corporate looks.

1. Read `references/theme-selection-index.json` (mood, best_for, avoid_for, scheme, **aliases**).
   - frontend-slides STYLE_PRESET names map via aliases: **Neon Cyber** → `neon-noir`,
     **Terminal Green** → `crt-terminal`, **Swiss Modern** → `swiss-typographic`.
   - **Stunning twenty-five:** when the brief matches a flagship vibe, read `references/stunning-25.md`
     and open that structured proof / Studio `?example=` before authoring.
   - Optional fast path: `references/theme-shortlists.json` — pick a use-case shortlist
     (Series A, developer demo, swiss agency, …) instead of scanning all 75.
     Prefer shortlists marked `"popular": true` when the vibe is vague.
   - `list_themes` returns `preview_url` + `studio_url` on **every** theme (stunning-25 →
     `?example=` craft; others → `?theme=` blank slate) plus `studio_example` / `gallery_url`
     when available — open those before authoring (show-don't-tell).
     `preview_themes` also returns `studio_share_url` (`?d=`) for the exact bake deck.
2. Shortlist **3** themes that fit purpose + audience + density. **Preview mix (mandatory):**
   - **1 safe / readable** theme (core-defaults, corporate, soft-product, quiet paper)
   - **1 bold / expressive** theme (stunning-25, neon, brutal/poster, wrap)
   - **1 wildcard** — either a second bold shortlist pick **or** a brand/import-driven custom direction
     that creates useful contrast (do not force three near-identical pastels)
3. **Required when tooling is available:** call `preview_themes` with those 3 names
   (writes `.presentation-md/theme-previews/<theme>-layouts-preview.html` for pick-3). **≥2 themes
   auto-defaults to `mode: "layouts"`** so body craft (cards, comparison, stats, quote, code)
   is visible — pass `mode: "title"` only for a cover skim. Open each file for the user —
   they pick visually, not from adjectives alone.
4. If MCP is unavailable, run:
   `npx @presentation-md/render preview.json -o previews/<theme>.html --theme <name>` three times
   (one title slide each).
5. After they pick, set `meta.theme` and proceed. Read `references/anti-slop-bans.md` before custom styling.
6. When a theme has a `gallery` field, open that craft deck as a multi-slide proof (not just the title preview).

If they already named a theme, alias, or brand URL, skip discovery (`import_brand_theme` for brand match).

### Density modes (ask once with purpose)

| Density | Best for | Design behavior |
|---------|----------|-----------------|
| **Speaker-led (low)** | Talks, keynotes, live pitches | One idea per slide, large type, generous space, 1–3 bullets max, more slides if needed |
| **Reading-first (high)** | Board packs, async review, handouts | Self-contained slides, structured grids/tables, tighter but intentional spacing |

Never shrink until cramped — split into more slides instead.

See also: `references/animation-patterns.md` for motion craft on the direct-HTML path.

---

## Parameters to Collect

Before generating, confirm (ask together when possible — purpose, length/density, content readiness):

| Parameter | What good looks like |
|-----------|---------------------|
| **Purpose** | "Raise a Series A" not "show investors stuff" |
| **Audience** | "Two partners at a16z who've seen 200 AI pitches" not "investors" |
| **Ask** | "$12M for 18 months of runway" not "funding" |
| **Density** | Speaker-led (low density, big type) vs reading-first (higher density, more self-contained) |
| **Vibe** | Theme discovery above, or describe the soul in 3 adjectives |
| **Content** | Raw notes, data, existing copy — the messier the better |
| **Constraints** | Time, slide count, branding rules |

Fill gaps with intelligent defaults (`theme-shortlists.json` / `list_themes` with `include_shortlists` — prefer `core-defaults` when vibe is vague). Never ask more than 3 clarifying questions.

---

## MCP Tools

Fourteen tools via `@presentation-md/mcp-server` (not the deprecated `@presentation-skill-pack/mcp-server` stub — it only redirects). Restart the client after switching packages.

| Tool | Use it to |
|------|-----------|
| `render_deck` | Convert deck JSON → polished HTML |
| `export_deck` | Export deck JSON → `.pptx`, vector PDF, html, **Markdown** (`format: "md"` — Marp round-trip), or **speaker-notes** handouts (`format: "notes_txt"` / `"notes_vtt"`) |
| `audit_deck` | Schema-validate + craft gates; optional `apply_safe_fixes` returns repaired JSON (fields + beat inserts: image-hero / comparison / data / logo-wall / wrap tones + theme-honesty leftovers); optional `remorph_density` (`speaker`/`reading`) for non-LLM structural density remorph |
| `list_themes` | See installed themes with vibe/description + proof deep-links (`preview_url` + always-on `studio_url`); filter with `browse` chips (site/Studio parity), shortlist, mood, or query; use `suggested_preview` (safe/bold/wildcard) for pick-3 |
| `apply_theme` | Swap `meta.theme` (default also runs `repairCraft` for theme honesty — Studio My deck Use parity; pass `apply_safe_fixes:false` for a pure swap) |
| `generate_deck_prompt` | Build a generation prompt wired to a theme + schema |
| `scaffold_deck` | Scaffold a recipe skeleton (pitch / launch / wrap / paper / …) with craft floors pre-wired — fill copy, then audit |
| `share_deck_link` | Encode Deck JSON → Studio `?d=` URL (Copy link parity) for editable user handoff |
| `deploy_deck` | Opt-in Vercel preview via `deploy.sh` — **dry-run unless `confirm:true`** after human approval; `prod` needs `confirm_prod` |
| `preview_themes` | Render 1–3 theme HTML previews; **inline PNG screenshots** on by default; `studio_share_url` for the exact bake; pass `json` for Studio **My deck** restyle (content-true) + optional `slide_index`; `mode: "layouts"` for multi-slide craft bake |
| CLI `--preview-compare` | Same pick-3 craft bake + discovery PNGs without MCP: `presentation-md-render --preview-compare a,b,c` |
| `import_pptx` | Import a `.pptx` into deck JSON (see `references/pptx-import.md`) |
| `import_markdown` | Import Marp/md-slides Markdown → Deck JSON (`---` splits, ` ```chart ` / ` ```html `) |
| `judge_deck` | Design judge — `tier` t0/t1 JSON gates; **t2** HTML metrics + Chrome shots (**inline PNGs** by default); **t3** panel or agent rubric |
| `import_brand_theme` | Generate a theme from a brand URL or CSS file |

---

## Rendering Guidelines

- **Direct to file** when inside a repo: write `<slug>/deck.html`
- **Code block** when copy-paste is requested: wrap the rendered HTML in a fenced code block, no surrounding explanation
- **No framework imports** — all CSS is internal, no Tailwind/Bootstrap/React
- **No lorem ipsum** — all copy must be plausible, specific, and consistent with the brand
- **Deck-spec path:** use the renderer — it ships 16:9 slides, scroll-snap, keyboard arrows, `.nav-hint`, entrance motion, and `prefers-reduced-motion`
- **Direct-HTML path:** match that craft — scroll-snap, arrow keys, print-safe `@media print`, hide `.nav-hint` when printing
- **Never `display: grid` (or `flex`) directly on an `<li>` that contains inline elements** (`<code>`, `<span>`, `<a>`) — the browser wraps each inline child in an anonymous block box to satisfy the grid formatting context, which silently breaks bullet alignment and spacing. Put the grid/flex on a wrapper `<div>` inside the `<li>` instead, or keep the `<li>` a plain block and let its child own the layout.

---

## Import from Markdown

Marp / md-slides authors can bridge into Deck JSON without rewriting slides:

```bash
presentation-md-render --from-md ./deck.md -o deck.json --theme kinetic-wrapped
```

Or call `import_markdown`. Front matter sets `theme` / `title` / `company`. Slides split on `---`.
Use fenced ` ```chart bar ` CSV blocks for charts and ` ```html ` for custom-html art.

**Export the other way:** `presentation-md-render deck.json --format md -o deck.md`, MCP `export_deck` `format: "md"`, or Studio **Source ▾ → Download Markdown** — same Marp/md-slides dialect for round-trip.

## Import from PowerPoint

When the user already has a `.pptx`, import it into deck JSON first (don't retype slides):

```bash
presentation-md-render --from-pptx ./board-deck.pptx -o deck.json --theme claude
```

Or call the `import_pptx` MCP tool. Then review layouts, adjust copy, swap themes, and render/export as usual. Details: `references/pptx-import.md`.

---

## Export & Share

Once a deck is done, it can leave the browser two ways. Both scripts live inside *this skill's own directory*, not the user's project — resolve `<skill-dir>` to wherever this `SKILL.md` is installed (e.g. `~/.claude/skills/presentation-generator/` or the plugin's skill path) and invoke them from there, passing the deck's path as an argument:

- **PDF** — MCP `export_deck` with `format: "pdf"`, CLI `presentation-md-render deck.json --format pdf -o deck.pdf`, Studio **Source ▾ → Download PDF** (local Studio: headless Chromium blob via `/api/export-pdf`, same `@page` 16:9 as MCP/CLI; static hosts: client raster; print dialog last resort), or `bash <skill-dir>/scripts/export-pdf.sh ./deck.html [./output.pdf]`. MCP/CLI render through headless Chromium's print pipeline (not screenshots): vector output, selectable text, one page per slide via the deck's own `@media print` rule. Installs Playwright on first run. Good for email, Slack, Notion, or printing.
- **Live URL** — MCP `deploy_deck` / CLI `presentation-md-render deck.html --deploy` (dry-run by default) or `bash <skill-dir>/scripts/deploy.sh ./deck.html` (or a deck directory). Deploys to Vercel and prints a shareable URL that works on any device. Defaults to a **preview** deployment, not production — pass `--prod` / `prod:true` only once the human has confirmed it's fine to publish permanently. **Confirm with the human before running this**: it's an externally-visible action, and decks are often confidential drafts. MCP/CLI require `confirm:true` / `--confirm-deploy` to actually invoke deploy.sh (otherwise dry-run only). Requires `npx vercel login` once, interactively, beforehand. A single-file deck that references local images/fonts will be refused (they'd 404 once deployed) — inline them as `data:` URLs first, or deploy the deck's whole directory instead.

For native, editable PowerPoint, use the Studio export mentioned above instead — it's a different fidelity trade-off (editable shapes vs. exact CSS rendering).

---

## Self-Review Before You Ship

You have been staring at this deck while building it, so you now see what you *intended*, not what is actually on the slide. Assume there are problems and go find them — a deliberate review pass is not optional, even for a 3-slide deck.

**Tooling first (deck-spec path) — non-skippable when MCP/CLI is available:**
1. Call `preview_themes` (or open gallery structured proofs) before locking a vibe — never invent a palette.
2. Call `audit_deck` on the deck JSON — fix every `error`, then address `warning`s. Pass `apply_safe_fixes: true` to auto-fill safe structural craft **and insert missing beats** (image-hero, comparison, stat-row, logo-wall, wrap tones/ranked/streak, cadence swaps, theme-honesty leftovers, emphasis, ratio, bento, CTA/icons, speaker notes, candy-pop brand) and get back `json` + `fixes_applied[]`. Pass `remorph_density: "speaker"|"reading"` for a **non-LLM structural density remorph** (speaker splits crowded grids/lists + moves overflow body into notes; reading merges thin continuation lists + promotes notes onto thin bodies) — Studio craft panel + CLI `--remorph-density` parity. Prefer `scaffold_deck` when starting from a brief so the first JSON already clears craft floors.
3. Call `judge_deck` for craft gates (`tier=t1`). Escalate to `tier=t2` (HTML metrics + **inline slide PNGs**) before delivery; `tier=t3` when highest stakes.
4. Render with `render_deck` / CLI, open the HTML, and spot-check with keyboard arrows.
5. Re-run `judge_deck` at t2/t3 with attached shots → fix → re-score. Do not ship on schema-valid alone.

Then walk every slide against this checklist and fix before delivering:

- **Placeholder sweep** — search the output for leftover scaffolding: `Lorem`, `ipsum`, `XXXX`, `TODO`, `[`, `placeholder`, dummy numbers. Zero may survive.
- **Overflow & overlap** — nothing clipped at an edge, nothing colliding, every element inside the safe margin.
- **Contrast** — every text block is legible against its actual background (see AI-Slop Tell #17).
- **AI-slop tells** — no accent line under a title, no text-only content slide, no centered paragraphs.
- **Visual beat** — investor, launch, and brand decks need ≥1 real `image-hero` (composed SVG/data URI or asset). Icon grids alone are not a visual. Kinetic wraps may use ranked/streak/metric/hero-stat instead.
- **Present-mode craft** — add brief `notes` on 2–4 key slides; decks with ≥6 slides need a data beat (`chart` / `stat-row` / `data-table` / `ranked-list` / `metric-ring` / `timeline`); launch/investor closings prefer dual `actions[]` with icons (not a lone `cta`).
- **Asymmetry** — at least one `comparison` with `emphasis`, `two-column`, `code`, `ranked-list`, `logo-wall`, `streak-grid`, `metric-ring`, or `columns: "bento"` — never a stack of identical three-up cards.
- **Token discipline** — colors and fonts all trace back to the chosen theme; no off-palette one-offs.
- **The 3-second test** — pick any slide at random: is its single point obvious in three seconds?
- **Arc integrity** — the deck still follows one narrative arc end to end; every slide sets up or pays off the one before it.
- **Schema honesty** — every `layout` value is one of the eighteen enums; no invented layout names.
- **Wrap honesty** — `kinetic-wrapped` decks need `tone` on ≥3 slides and a visual beat (`ranked-list`, `streak-grid`, `metric-ring`, `stat-row` `variant:"hero"`, or `image-hero`).
- **Gallery honesty** — if you named a stunning-25 theme (aurora-glass, ft-editorial, luxury-minimalist, …), open its structured proof and match that craft ceiling.
- **Candy honesty** — `candy-pop` marquees brand from `meta.company` (or `meta.marquee` / `meta.title`); never hardcode Jellybean.
- **Riso honesty** — `risograph-zine` decks should feel printed: prefer `comparison` with `emphasis`, a punchy `quote`, and kraft-paper copy — not a stack of soft corporate cards.
- **Paper honesty** — paper/editorial themes (`claude`, `soft-editorial`, `ft-editorial`, `broadsheet`, `heritage-editorial`, `vellum`, `paper-ink`, `long-table`, `editorial-serif`, `editorial-forest`, `emerald-editorial`, `pin-and-paper`, `vintage-editorial`, `monochrome`, `notebook-tabs`, `blue-professional`, `pink-script`, `biennale-yellow`, `pastel-dreamy`, `scandinavian`): magazine cadence (`quote`, `comparison`+`emphasis`, short literary leads) — not soft corporate card stacks. Quiet fiber grain is HTML surface craft; PPTX keeps rules/washes/mastheads + always-on pink-script hairline / hero-gated ornaments / biennale sun frame / pastel plump clouds + theme-native card hairlines (`paper-ink` / `editorial-serif` / `vintage-editorial` literary left rules; `ft-editorial` / `biennale-yellow` / `luxury-minimalist` top rules; heritage / pin / emerald keep full box hairlines) — prefer HTML when the tooth is the brand.
- **Loud honesty** — loud/neobrutal peers (`stencil-tablet`, `retro-zine`, `daisy-days`, `block-frame`, `creative-mode`, `sakura-chroma`, `brutalist-acid`, `raw-grid`, `capsule`, `scatterbrain`, `8-bit-orbit`, `retro-windows`, `cobalt-grid`, `genz-bento`, `bauhaus`, `neo-grid-bold`, `bold-poster`, `creative-voltage`, `electric-studio`, `studio`, `brutalist-mono`): expect hard frames + offset-shadow strips (or multi-layer arcade / Win95 bevel / cobalt grid+hatch chrome) **and hard-border cards** on body slides (pills/tape/blocks/chroma may stay hero-gated) — don’t invent `custom-html` stickers for atmosphere. `scatterbrain` wants a workshop beat (feature-grid / image-hero / quote / stats) with ink sticky-card hairlines in PPTX.
- **Atmosphere honesty** — `neon-noir` / `vaporwave` / `y2k-aero` / `retro-arcade`: expect cyan/pink rims, rain/arcade scanlines or horizon glow, soft aero shadow stubs, and a cinematic `image-hero` or punchy `quote` — don’t flatten into SaaS three-up grids.
- **Poster honesty** — `coral` / `peoples-platform` / `bold-signal` / `broadside`: expect hard poster frames + square (or plump bold-signal accent-rim) hard-border cards and a bold beat (`image-hero`, comparison, quote, or punchy stats) — not soft corporate card stacks. `mat` wants a mid-century beat (`quote` / `image-hero` / comparison / punchy stats) with woodglow + cream rim chrome.
- **HUD honesty** — `aerospace-hud` / `crt-terminal` / `blueprint`: expect instrument chrome (grid/scanlines/reticles) plus a data beat (`chart`, `data-table`, `stat-row`, `ranked-list`, `timeline`, or `metric-ring`) — not soft marketing grids.
- **Glass honesty** — `aurora-glass` / `glassmorphism`: expect a frosted product beat (`image-hero`, punchy `quote`, or stats) — PPTX keeps glass rims (not true blur).
- **Modernist honesty** — `bauhaus` / `swiss-typographic` / `art-deco`: geometry + hard type with a modernist beat (quote / image-hero / comparison / icon feature-grid).
- **Briefing honesty** — `signal`: quiet dual-surface chrome + an editorial beat (quote / image-hero / comparison / stats); PPTX keeps briefing frames and border-hairline cards.
- **Quiet-luxe honesty** — `luxury-minimalist`: top-rule cards + a restrained luxury beat (quote / image-hero / comparison) — not soft SaaS stacks. `ft-editorial` / `biennale-yellow` share top-rule card geometry under paper honesty. `long-table` keeps dashed rust supper cards under paper honesty.
- **Soft-product honesty** — `corporate` / `fintech-clean`: clean product beat (stat-row / comparison / feature-grid / chart); PPTX keeps accent-hairline cards + quiet frames.
- **Playful honesty** — `playful` / `split-pastel`: soft-bento beat (feature-grid / image-hero / stats / quote); PPTX keeps plump coral/ink card rims.
- **Neon-tech honesty** — `default-tech` / `developer-dark`: tech product beat (code / feature-grid / chart / comparison / stats); PPTX keeps neon/terminal card rims.
- **Data-editorial honesty** — `data-editorial`: reported data beat (chart / data-table / stat-row / ranked-list / timeline); PPTX keeps ink card hairlines.
- **Recipe honesty** — match a `references/layout-recipes.md` slide map for the brief before inventing a 14-slide feature-grid funeral.

For a rigorous, scored pass, run the **`deck-design-judge`** skill: it grades the deck against the design rubric, tells you exactly what to fix, and lets you re-score after the fix.
