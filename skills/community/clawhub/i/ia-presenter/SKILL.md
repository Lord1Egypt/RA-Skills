---
name: ia-presenter
description: "Write, lint, package and theme iA Presenter presentations. Use when the user mentions iA Presenter, wants slides / a deck / a talk written in Markdown with speaker notes, wants to turn notes or an article into a presentation, set a theme, add images, videos, tables, charts or layouts to slides, or customize fonts/colors via a custom iA Presenter theme (template.json, presets.json, CSS). Produces .iapresenter bundles that open directly in the app. Verified against iA Presenter 2.0.2 on macOS."
license: MIT
compatibility: "Authoring works anywhere. Previewing, exporting and theme installation need macOS with iA Presenter 2.x. Helper scripts need python3."
metadata:
  author: dAAAb
  version: "1.0.3"
  verified-with: "iA Presenter 2.0.2 (build 20026), macOS"
  openclaw:
    emoji: "🎞️"
    requires:
      bins: ["python3"]
---

# iA Presenter

iA Presenter is a **text-first** presentation app (macOS / iOS). You write one Markdown
file; the app auto-lays out responsive slides and keeps your speech as speaker notes.
This skill covers two jobs:

1. **Authoring decks** – writing iA Presenter Markdown, packaging it as a `.iapresenter`
   bundle with a theme pre-selected, linting it, previewing it.
2. **Custom themes** – `template.json` + `presets.json` + CSS in the app's Themes folder.

Everything below was checked against the app's own bundled Help, `layouts.json`, the
theme files shipped inside iA Presenter 2.0.2, the metadata parser in the app binary,
and live rendering tests. Where community docs disagree with the app, the app wins.

## Decision tree

| User wants | Do |
|---|---|
| A new presentation / deck / talk | **Author** → write `text.md`, run `scripts/new_deck.py`, lint, open, review |
| Turn an article / notes / outline into slides | Same as above; speech goes flush-left, only the punchline gets a TAB |
| Fix a deck that "looks wrong" | Run `scripts/lint_deck.py`, then check [references/layouts.md](references/layouts.md) |
| Change look / fonts / colors beyond built-ins | **Theme** → copy `assets/starter-theme`, edit, `scripts/install_theme.sh` |
| Choose a built-in theme | Set `"template"` in `info.json` (see *Packaging*) |
| Export PDF / PPTX / images / HTML | The app does it: `File → Export` or Command Palette. See [references/file-format.md](references/file-format.md) |

Load references progressively: `syntax.md` and `layouts.md` for any deck; `content-blocks.md`
for images/video; `charts.md` for tables→charts; `themes.md` + `engine-css.md` for themes;
`file-format.md` for bundle/export/automation.

## Core model (memorize this)

```
	Kicker line (TAB paragraph right before a heading = small line above it)
# Title                         ← headings are ALWAYS visible
	Visible body text             ← a real TAB (\t) at line start puts a paragraph on the slide

This flush-left paragraph is speech. The audience never sees it.   ← speaker notes

---                             ← three dashes on their own line = next slide
```

- **Visible by default:** headings `#`–`######`, images/videos (content blocks), tables,
  fenced code, display math, charts, footnotes.
- **Speaker notes by default:** paragraphs, lists, blockquotes, definition lists. Prefix
  every line of them with a **TAB** to show them (`⇥- item`, `⇥> quote`).
- **Never TAB a table or a code fence** – that turns it into an indented code block.
- Use real tab characters. Spaces do not work. Editors that convert tabs to spaces will
  silently break the deck.
- `// comment` lines are author-only.

## Authoring workflow

1. **Frame it** – audience, goal, duration, tone. Default speaking rate in the app is
   110 wpm, so a 10-minute talk ≈ 1,100 words of notes across ~12–20 slides.
2. **Write the story first**, flush-left, as if it were an email. Then cut it into slides
   with `---`. One idea per slide.
3. **Promote only what the audience should see**: a heading, one TAB line, an image, a
   table. Do not paste the notes onto the slide. Create tension between what is shown and
   what is said.
4. **Shape the layout by shaping cells** (blank line = new cell; see below). Add
   `Layout: …` only when auto-layout picks wrong.
5. **Add visuals last**: `/assets/photo.jpg` content blocks, `Background: true` for covers.
6. **Pick a theme** in `info.json` that fits the room; never leave every deck on the
   default white theme.
7. **Package, lint, open, look** – `scripts/new_deck.py`, `scripts/lint_deck.py`, then
   `open -a "iA Presenter" deck.iapresenter` and inspect the thumbnails (or
   `scripts/preview_deck.sh` to screenshot). Fix and repeat.
8. **End on a landing line or an ask**, not "Thank you / Questions".

## Cells and auto-layout (how you "design")

A slide is split into **cells** by blank lines. iA Presenter picks a layout from the
number of cells, whether they contain graphics, the first heading level of each cell, and
their order. Verified behaviour:

| You write | You get |
|---|---|
| one heading (+ TAB subtitle, no blank line) | big centered / cover-style title |
| `## Heading` + blank + 2–3 cells | title on top, cells side by side (columns) |
| 2–3 cells, no title | side-by-side split |
| 4+ cells | grid (`grid-items-N`) |
| heading + blank + image | title with image |
| `#### caption` + image, or image + `#### caption` | caption above / below the image |
| image with `Background: true` + heading | text over a full-bleed background |
| a lone image | full-bleed image |

Heading levels carry meaning: `#` cover title (pair with `###` for details), `##`
centered section/slide title, `###`/`####` smaller headings, `####` + image = caption.

Force a layout with a first line `Layout: Name`. Verified working: `Cover`, `Title`,
`Section`, `Default`, `Split`, `Grid`, `Title-and-Columns`, `Caption`, `Caption-Top`,
`Image`. **Avoid `Layout: Columns`** – it renders unusably small in 2.0.2; use
`Title-and-Columns` or plain auto-layout instead. `Layout: Grid` treats the heading as a
grid cell too; use `Title-and-Columns` when you want a title row. Details:
[references/layouts.md](references/layouts.md).

## Images, video, backgrounds (content blocks)

Put the path alone on a flush-left line, then optional `key: value` lines **directly
under it** (no blank line):

```
/assets/photo.jpg
size: contain
x: right
y: top

/assets/cover.jpg
Background: true
filter: darken
opacity: 60%

/assets/clip.mp4
```

- Paths: `/assets/<file>` (files inside the bundle's `assets/` folder), `/Theme/<file>`
  (files shipped with the theme), or a remote `https://…` URL that **ends in an image
  extension** (`.jpg .jpeg .png .apng .gif .webp .tif .tiff .svg`) or is an
  `unsplash.com` link. Remote URLs work (verified); URLs without an image extension are
  treated as plain text.
- Keys (case-insensitive): `size: cover|contain`, `x: left|center|right`,
  `y: top|center|bottom`, `background: true`, `filter: lighten|darken|grayscale|sepia|blur`,
  `opacity: 10%…100%`, `title:`, `alt:`, `class: css-class`. Full list and semantics:
  [references/content-blocks.md](references/content-blocks.md).
- Formats: png/apng, jpg, gif, webp, tif, svg, pdf; video m4v/mp4/mov; YouTube via the
  Inspector's Visuals tab (or paste the YouTube URL as a content block).
- Classic `![alt](assets/photo.jpg)` also works (no leading slash, spaces as `%20`), but
  content blocks are the recommended, controllable form.

## Tables → charts

Write a flush-left Markdown table; add metadata lines **immediately after** it:

```
| Quarter | Revenue | Cost |
| :------ | ------: | ---: |
| Q1      | 10      | 6    |
| Q2      | 15      | 8    |
Chart: bar
Orientation: horizontal
bar-type: stacked
yLabel: Millions
```

`Chart: bar|line|pie|donut`; options `Orientation`, `bar-type: stacked`, `line-type`,
`Color-Type: sequential|differential`, `xLabel`, `yLabel`, `xFormat`, `colors`. Charts
use the theme's `--graph-data-N` palette. See [references/charts.md](references/charts.md).

## Packaging: the `.iapresenter` bundle

A presentation is a **folder** named `Name.iapresenter`:

```
Name.iapresenter/
├── text.md        # the deck
├── info.json      # metadata + theme choice
└── assets/        # every file referenced as /assets/…
```

`info.json` (verified – the theme is applied on open):

```json
{
  "type": "net.daringfireball.markdown",
  "creatorIdentifier": "net.ia.presenter",
  "version": 2,
  "transient": false,
  "net.ia.presenter": { "template": "tokyo", "preset": "Default" }
}
```

- `template` = the theme **Name in lowercase, spaces kept**: `"helvetica"` (default),
  `"zurich"`, `"basel"`, `"copenhagen"`, `"vancouver"`, `"tokyo"`, `"milano"`,
  `"new york"`, `"paris"`, `"san francisco"`, `"la"`, `"garamond"` (premium), or your
  custom theme's lowercased `Name`. `"sanfrancisco"` / `"newyork"` silently fall back to
  the default theme.
- `preset` = a preset `Name` from that theme's `presets.json`: most themes only have
  `"Default"`; Helvetica and Garamond have `"Light"`/`"Dark"`, Basel `"Default"`/`"Dark"`,
  Tokyo `"Default"`/`"Light"`. `scripts/install_theme.sh --list` prints them.

Build it: `python3 scripts/new_deck.py deck.md "My Talk.iapresenter" --theme "new york" --assets ./img --open`
(copies referenced images, writes `info.json`, checks paths). Plain `.md` files also
open/import in the app (`File → Import`), but a bundle is what you should hand over.

## Verify before you hand over

- `python3 scripts/lint_deck.py "My Talk.iapresenter"` → zero errors.
- Open it: `open -a "iA Presenter" "My Talk.iapresenter"`. The thumbnail strip shows the
  rendered slides; hovering a thumbnail shows its speaking time. `scripts/preview_deck.sh`
  screenshots the window for you (needs Screen Recording permission).
- Check: every slide has something visible; nothing is a wall of text; images load; the
  theme applied; notes read aloud naturally; the last slide lands.

## Custom themes (short version)

Themes live in
`~/Library/Containers/net.ia.presenter/Data/Library/Application Support/iA Presenter/Themes/<Name>/`
and consist of `template.json` (metadata, fonts' display names, `Css` file, per-layout
`Classes`, `LayoutExamples`), `presets.json` (fonts' CSS names, appearance, colors,
accents, gradients), a CSS file, optional fonts/images and a `template.png` thumbnail.

- Start from `assets/starter-theme/`, rename `Name` and `Css`, then
  `scripts/install_theme.sh path/to/MyTheme`. Quit and relaunch the app the first time;
  afterwards the app hot-reloads the theme in use on every save.
- **Color naming trap:** `DarkBodyTextColor` is *dark-colored text* (used on light
  backgrounds); `LightBodyTextColor` is light text for dark mode. Swapping them gives
  invisible text.
- Select it with `"template": "mytheme"` (lowercased `Name`) or in the Design inspector.
- Typography is driven by engine CSS variables (`--scale-factor-h1`, `--font-weight-h2`,
  `--case-h1`, …) and iA's own selector form `[class*="layout-"] > div h1`. Backgrounds
  target `.backgrounds .cover-container`; inline SVG must use `rgb()` not hex. Full
  guide: [references/themes.md](references/themes.md), class/variable catalog:
  [references/engine-css.md](references/engine-css.md).

## Gotchas (all verified in 2.0.2)

- TAB, not spaces. A TABbed table or code fence becomes a code block.
- Metadata lines must touch the block they modify (no blank line between).
- `Layout: Columns` is broken; `Layout: Grid` swallows the title.
- A heading + blank line + table becomes a split (narrow table). Keep the table right under the
  heading (same cell) for full width. CJK text works fine; system font falls back to PingFang.
- `template` values are lowercase with spaces; wrong values fall back silently.
- iA's shipped JSON has trailing commas (lenient parser). Write strict JSON anyway.
- Fonts: `template.json` gets the *display* name, `presets.json` the *CSS family*.
- Charts are limited to bar / line / pie / donut; the theme decides colors.
- Web Sharing exists only for licenses bought directly from iA (not App Store).
- The app is not AppleScript-scriptable; automation = `open -a` + UI. Exports go through
  the UI or the Command Palette added in 2.0.

## Resources

- `references/syntax.md` – complete Markdown syntax (from the in-app Help)
- `references/layouts.md` – auto-layout rules, `Layout:` names, CSS classes, verified results
- `references/content-blocks.md` – image/video paths, all metadata keys + values
- `references/charts.md` – table→chart metadata
- `references/themes.md` – theme files, fonts, backgrounds, gradients, appearance, install
- `references/engine-css.md` – rendering-engine classes and CSS variables to override
- `references/file-format.md` – bundle format, `info.json`, import/export, shortcuts, automation
- `assets/example-deck.md` – a complete deck using every pattern (real tabs inside)
- `assets/starter-theme/` – minimal, valid theme to copy
- `scripts/new_deck.py`, `scripts/lint_deck.py`, `scripts/install_theme.sh`, `scripts/preview_deck.sh`
