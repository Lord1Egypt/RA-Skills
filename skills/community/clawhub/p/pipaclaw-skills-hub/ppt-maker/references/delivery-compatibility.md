# Delivery Compatibility

The deck is not "done" until it is usable in the user's real delivery path.

## First Rule

Ask where the deck will actually be opened and edited:

- desktop Office / WPS
- WeChat download and open
- both

Do this during intake, not after export fails.

## Delivery Profiles

### `desktop-editable`

Optimize for:
- best visual fidelity
- desktop editing
- richer layout freedom

Allowed bias:
- more complex composition
- broader font choices if brand requires them

### `wechat-editable-safe`

Optimize for:
- WeChat download and open
- mobile-side editing tolerance
- avoiding blank-looking pages in weaker viewers

Must preserve editability for:
- text
- tables
- simple charts
- key diagrams built from basic shapes

Should simplify or rasterize only:
- decorative background layers
- non-essential visual textures
- fragile ornamental compositions

### `both`

Produce two editable files:

- `full-fidelity.pptx`
- `wechat-safe-editable.pptx`

Do not force one file to satisfy both goals if that materially hurts reliability.

## WeChat-Safe Rules

- Prefer stable cross-device fonts for editable text.
- For Chinese decks, prefer conservative editable font choices over modern desktop defaults.
- Do not default Chinese decks to `Aptos` or similar modern Microsoft font families when WeChat compatibility matters.
- Avoid fragile default font chains that may render inconsistently in mobile viewers.
- Do not rely on a page being readable only because textboxes render perfectly.
- Give title and key-message areas a visible supporting layer, panel, or card so the page does not look empty if text rendering degrades.
- Keep charts simple and directly labeled.
- Keep headers, footers, page numbers, and logo placement structurally simple.
- Avoid overusing transparency, masks, layered effects, or brittle decorative geometry in text-heavy pages.
- Avoid footer copy that is so verbose or repetitive that it becomes visual noise on every page.

## Review Checklist

Before export, ask:

- Which profile is this delivery using?
- If WeChat is involved, did we create a dedicated `wechat-editable-safe` file?
- If text rendering weakens, do the important pages still look intentionally composed rather than blank?
- Are the main editable surfaces still text/table/chart instead of screenshots?

## Product Rule

PDF is not a substitute when the user needs editing.

If WeChat is part of the delivery path and the user still needs editing, the answer is a safer editable `.pptx`, not a non-editable fallback.
