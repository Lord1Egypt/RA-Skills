# Artifact Format — 03-visual-direction.md

Output of Phase 3. The HITL-2 review target.

This is a minimum record of the visual decisions made — not a form to fill out completely.
If your direction has nuances, a visual motif, or reasoning that doesn't fit the structure below,
add it. The goal is that someone reading this file could reproduce the visual intent without
seeing the final HTML.

````markdown
# Visual Direction — <slug>

## Direction

**Name:** <a descriptive name you invented, not a category label>
**Chosen because:** <what in the content led to this direction — one or two sentences>

## Seed match

<seed name if the content clearly matches one (e.g. "dark-warm"), or "none — content-led">
If a seed was matched but no `style` parameter was passed, note that here too.

## Visual idea

<Optional but encouraged: is there a structural motif, recurring element, or typographic
treatment that runs through the presentation and makes it distinctive? Describe it here.>

## Palette

**Background:** <dark/light, character>
**Accents:** <how many, what they do>

```css
:root {
  --bg: ...;
  --surface: ...;
  --surface2: ...;
  --accent-1: ...;
  /* add more as needed */
  --text: ...;
  --text-muted: ...;
  --border: ...;
}
```
````

## Typography

**Display:** <font name> — <why this font for this content>
**Body:** <font name> — <why>
**Mono:** <font name> — <why, or "none" if not used>

## Atmosphere

<effects chosen and where they apply, or "none — [reason]">

## Accent assignment per slide

| Slide # | Dominant accent | Notes |
| ------- | --------------- | ----- |
| 1       | accent-1        |       |
| ...     | ...             |       |

## Anything else worth recording

<Layout motifs, animation approach, special treatments for specific slides, etc.>
