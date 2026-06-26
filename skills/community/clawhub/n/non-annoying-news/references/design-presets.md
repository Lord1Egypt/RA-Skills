# Design Presets and Personalization

Use this reference when the user asks about naming, look, layout, density, or personal taste.

## Design principle

The newspaper should feel edited, not generated. Personalization should be easy, but it must not degrade clarity, source trust, or layout density.

## User-facing choices

Offer these simple knobs during setup:

- **Title:** e.g. “The Non-Annoying News”, “Weekly Signal”, “The Saved Links Review”.
- **Subtitle:** one-line promise, e.g. “A compact newspaper from the sources you meant to read.”
- **Language:** issue language and source-language handling.
- **Preset:** classic newspaper, modern review, weekend magazine, research brief, compact wire.
- **Density:** airy, standard, compact.
- **Color accent:** muted brown, slate, burgundy, forest, blue-grey, or user hex value.
- **Sections:** fixed sections or issue-specific sections.
- **Images:** none, source-only, one front image, or restrained inside images.

## Presets

### classic-newspaper

Best for general personal newspapers and saved-link digests.

- Serif body and headlines, sans-serif metadata.
- Strong masthead, narrow rails, discreet source notes.
- Compact but readable.
- Works well for 2–4 pages and mixed topics.

### modern-review

Best for technology/business analysis.

- Cleaner sans-serif headings with serif body.
- More whitespace than classic, fewer but stronger boxes.
- Good for explainers, product/market analysis, and executive reading.

### weekend-magazine

Best for culture, science, travel, film, long reads, and reflective issues.

- Larger lead image or illustration when source-appropriate.
- More generous decks and pull quotes.
- Fewer stories, more narrative flow.

### research-brief

Best for technical, scientific, policy, or investment research.

- Evidence boxes, source-grade labels, and explicit uncertainty notes.
- More restrained typography and fewer decorative elements.
- Prioritizes clarity over warmth.

### compact-wire

Best for frequent daily updates.

- Dense layout, shorter briefs, minimal imagery.
- Strong section labels and quick source notes.
- Avoids becoming a bullet list by keeping mini-articles substantive.

## Layout choices

- **Masthead:** keep one line when possible. If the title is long, use a shorter display title and full title in subtitle.
- **Side rails:** use 4–7 meaningful briefs per front page rail depending on density. Never leave a rail visually abandoned.
- **Inside pages:** use two-column article grids, with one wide analysis piece when needed.
- **Images:** use only source-relevant images or clearly marked illustrations. Do not use generic filler images.
- **Color:** one accent color is enough. Avoid dashboard badges and neon labels.

## Copy/design fit

When layout is weak, do not add decorative junk. Choose one of:

1. expand a real story with mechanism/evidence;
2. split a dense story into a main article plus a concrete side note;
3. add a directly relevant counterpoint, consequence, or source-boundary brief;
4. change page structure or density.

## CSS implementation

`assets/newspaper-template/base.css` exposes theme variables and classes:

- `theme-classic`, `theme-modern`, `theme-weekend`, `theme-research`, `theme-wire`;
- `density-airy`, `density-standard`, `density-compact`.

The agent may copy the template and change classes or variables per local config. Keep the public template generic.
