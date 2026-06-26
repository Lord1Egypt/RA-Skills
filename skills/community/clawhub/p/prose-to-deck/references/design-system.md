# Design System — Design Principles

This file is about how to think, not what to copy.
No templates, no ready-made palettes, no component code.
The reasoning here should lead you to original decisions — not to reproductions of decisions someone else made.

---

## Color

### How color works in a presentation

A presentation is a sequence of screens. Color does two jobs simultaneously: it creates
**identity** (this feels like one coherent thing) and **rhythm** (each slide feels distinct
within that thing). These two goals are in tension. Resolve the tension deliberately.

**Background temperature sets the room.**
The background is the largest surface — it determines the emotional temperature before
anything else is read. Cool dark backgrounds (near-black with a blue or green cast) feel
precise, forward-looking, technical. Warm dark backgrounds (near-black with brown or red
cast) feel intimate, serious, weighty. Light backgrounds feel open, readable, authoritative.
Pure white and pure black feel stark — powerful when intentional, empty when not.

**Accent color is a promise.**
Whatever color you use as your primary accent, you're making a promise: this color means
something. Use it consistently for the most important element on each slide. If you use it
for everything, it means nothing.

**Harmony vs. tension.**
Analogous colors (neighbors on the color wheel) create harmony — calm, cohesive, easy to
sustain across many slides. Complementary colors (opposites) create tension — energetic,
dramatic, harder to sustain. Most presentations benefit from a dominant analogous palette
with one complementary accent used sparingly for moments of emphasis.

**Saturation is volume.**
High saturation commands attention and creates energy, but fatigues quickly. Low saturation
recedes and supports. A presentation that's all high saturation has no dynamic range. One
that's all low saturation has no pulse. Vary saturation to create shape — the way a musician
varies volume.

**The contrast floor is non-negotiable.**
Text on background: minimum 4.5:1 contrast ratio. Secondary text: minimum 3:1.
This is not aesthetic preference — it's the difference between readable and unreadable.

**What to avoid:**

- Purple gradient on white. It's the default AI aesthetic — it signals no decision was made.
- More than 3–4 accent colors. Beyond that, you have noise, not richness.
- Accent colors too close in value to the background. They disappear.
- Pure `#000000` or `#ffffff`. Slightly off-black and off-white feel more intentional.

### CSS variable architecture

Define all colors as CSS custom properties on `:root`. Never hardcode hex values in
component styles — always reference variables. This makes the entire presentation
re-themeable by changing one block of code.

The minimum set of roles you need: background, one or two surface elevations (for cards
and containers), one or more accent colors, primary text, secondary/muted text, and a
border color (almost always very low opacity).

Name variables by **role**, not value. `--accent-1` not `--mint-green`.
The value will change; the role won't.

---

## Typography

### Type is not decoration — it's the content

In a text-heavy presentation, typography _is_ the design. Typeface choice, scale
relationships, weight contrast, line-height — these determine whether content lands
or slides past.

**The three-role system.**
Every presentation needs three distinct typographic voices:

_Display_ — the voice that commands. Headlines, slide titles, the thing you read first.
Needs strong personality at large sizes and enough weight range to create hierarchy.
This is where you make a statement about the presentation's character.

_Body_ — the voice that explains. Paragraphs, supporting text, anything read at length.
Needs to be comfortable at 14–18px. Personality matters less than readability here.

_Mono_ — the voice that annotates. Labels, metadata, data, code, small technical details.
Its job is to feel distinct from body text — to signal "this is a different kind of
information." Not every presentation needs a mono voice.

**Contrast is hierarchy.**
The most important typographic tool is size contrast. A 72px headline next to 14px body
creates immediate, unambiguous hierarchy. A 32px headline next to 24px body creates
confusion. Adjacent typographic levels should differ by at least 1.5×.

**Weight contrast amplifies size contrast.**
Heavy headline (700–900) paired with light body (300–400) creates tension that makes both
feel more intentional. Same weight throughout feels flat.

**Line-height is breathing room.**
Body text: 1.6–1.8. Tighter than 1.5 and paragraphs feel compressed.
Headlines: 1.0–1.2. Large type at 1.6 line-height looks like it's falling apart.

**Letter-spacing by size.**
Large display type (48px+) often benefits from slightly negative letter-spacing (−0.5 to
−2px) — it looks intentional, not just scaled up. Small labels benefit from positive
letter-spacing (1–2px) — it improves legibility and adds precision.

**Responsive type.**
This is a viewport presentation. Use `clamp(min, preferred, max)` for all font sizes.
The preferred value should be in `vw` so type scales with the viewport. To derive the vw
value: divide your target pixel size by the viewport width you're designing for, multiply
by 100. Set a floor and ceiling that prevent the type from becoming unreadable at extremes.

**Font loading.**
Load from Google Fonts via `<link>` in `<head>`. Load all roles you'll use. Specify only
the weights you'll actually use. Always include `display=swap`.

**What to avoid:**

- More than 2 typefaces (Display + Body is often enough)
- A display font used for body text
- Identical or near-identical weights for headline and body
- Line-height below 1.5 for body text
- CJK content without a font that has CJK coverage

---

## Layout and Space

**Space is not emptiness — it's structure.**
A slide with one large headline and generous padding is not empty — it's giving the idea
room to land. A slide packed with bullets is not thorough — it's refusing to decide what
matters.

**The single-job principle.**
Every slide does exactly one thing. If you can't name the job in five words, the slide is
doing too much.

**Visual weight and reading order.**
Readers scan before they read. Their eye goes to the largest, highest-contrast element
first. Design the reading order deliberately. Size, contrast, position, and color all
influence it — use them intentionally.

**Alignment creates relationship.**
Elements that share a left edge, baseline, or center axis feel related. Elements that
don't align feel accidental. You don't need a visible grid — but you need consistent
alignment axes.

**Padding is a design decision.**
The space between content and the slide edge is part of the composition. Generous padding
makes content feel considered. Tight padding makes it feel dense and urgent. Neither is
wrong; both are choices.

**Vertical rhythm.**
Spacing between elements should reflect their relationship. Tightly related elements get
less space. Loosely related elements get more. Consistent spacing ratios create rhythm.

**Multi-column layouts.**
Columns work when content is genuinely parallel. Don't use them to fill horizontal space.
Always plan for mobile: columns must collapse to a single column at small viewports.

---

## Motion and Interaction

**Animation serves comprehension, not decoration.**
Every animation should answer: does this help the reader understand the content, or does
it just look interesting? If the answer is the latter, remove it.

**Reveal on scroll** is the most useful animation in a scroll-snap presentation. Content
fades/slides in as the slide enters the viewport — a sense of arrival, a moment to orient.
Use it for content elements, not for structural chrome or backgrounds.

**Stagger** — when multiple elements reveal together, staggering their entrance (100–200ms
apart) creates sequence and prevents overwhelm. Don't stagger more than 4–5 elements.

**Duration and easing.**
Reveals: 500–800ms, ease-out. Hover interactions: 200–300ms, ease.
Longer than 1s feels slow. Shorter than 150ms feels abrupt.

**What to avoid:**

- Animations that replay every time the user scrolls back to a slide
- Entrance animations on every element — reserve them for what matters most
- Animations that delay content visibility
- Parallax effects that make text hard to read

---

## Slide Structure

**The scroll-snap model.**
The `<html>` element is the scroll container with `scroll-snap-type: y mandatory`.
Each slide is a full-viewport `<section>` with `scroll-snap-align: start`.
The slide is a positioning context (`position: relative`). Background effects sit inside
it as `position: absolute; pointer-events: none`. Content sits above them.

**Navigation and position awareness.**
Two functional needs exist in any multi-slide presentation: how does the reader move
between slides, and where are they in the sequence? These are design problems, not just
implementation problems. The solution should fit the visual direction and be unobtrusive —
navigation chrome should never compete with content for attention.

Possible approaches: fixed dots on an edge, a slide counter in a corner, a progress bar,
keyboard-only navigation. Choose based on the presentation's length and character.

**Atmosphere.**
Background effects — blobs, grids, noise textures — create depth and texture. They work
best when barely visible: present enough to feel intentional, absent enough not to compete.
They must never reduce text contrast below the 4.5:1 floor. When in doubt, use none.

---

## What "consistent" means

A presentation is consistent when it feels like one person made all of it:

- The same CSS variables used everywhere — no one-off hex values
- The same typographic scale throughout
- The same spacing rhythm — padding and gaps follow the same ratios
- The same animation behavior — all reveals use the same duration and easing
- The same accent logic — `--accent-1` means the same thing on every slide

Consistency is not sameness. Slides should look different from each other. But they
should feel like they belong to the same family.
