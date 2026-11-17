# Custom themes

Source: in-app Help (`Custom Themes.html`), the `NewTheme/` template and the 12 built-in
themes shipped inside iA Presenter 2.0.2, plus live install tests.

## Where themes live

```
~/Library/Containers/net.ia.presenter/Data/Library/Application Support/iA Presenter/
├── Themes/         ← your custom themes (one folder each) – the only folder you may edit
├── .Themes/        ← built-in themes, regenerated on launch (read for reference, never edit)
├── .Engine/        ← rendering engine (main.css, index.js…), regenerated on launch
└── readme.txt
```

Settings → Themes → **Create Theme** creates a folder from the `NewTheme` template;
**Reveal Themes Folder** opens it. A theme dropped in manually is picked up on the next
launch. Once a theme is *in use*, the app watches its files and re-renders on every save
(hot reload). Select a theme in the Design inspector, or per bundle with
`info.json → "template": "<name lowercased>"`.

## Files

```
MyTheme/
├── template.json     # metadata, display font names, per-layout classes, picker examples
├── presets.json      # one or more presets: CSS font names, appearance, colors, gradients
├── mytheme.css       # the CSS named in template.json → "Css"
├── template.png      # thumbnail shown in the theme picker (16:9, ~600px wide)
├── fonts/*.woff2     # optional custom fonts
└── image1.jpg …      # optional images, usable as /Theme/image1.jpg in decks and url("image1.jpg") in CSS
```

### template.json (real shape used by iA's themes)

```json
{
  "Name": "Zurich",
  "Version": "1.0.2",
  "Author": "iA",
  "ShortDescription": "Minimal Swiss design",
  "LongDescription": "- One size for all headline levels\n- Default white on black\n- Default font: Helvetica",
  "Css": "zurich.css",
  "TitleFont": "Helvetica",
  "BodyFont": "Helvetica",
  "CssClasses": "fixed-size-headings",
  "Layouts": [
    { "Name": "Cover", "Classes": "invert" },
    { "Name": "Title", "Classes": "invert" }
  ],
  "LayoutExamples": [
    { "Name": "Title with Background",
      "Markdown": "/Theme/image2.webp\nBackground: true\nopacity: 30%\n\n# TITLE\n#### with background" }
  ]
}
```

- `Name` – shown in the picker; its lowercase form is the `template` id.
- `TitleFont` / `BodyFont` – **display names** shown in the Style inspector.
- `CssClasses` – classes added to the presentation root. Known values:
  `variable-size-headings` (H1 > H2 > H3…, used by most themes),
  `fixed-size-headings` (all headline levels same size – Zurich),
  `has-graph-background` (charts drawn on a white card).
- `Layouts[].Classes` – per-layout classes; `invert`, `dark`, `light` force appearance.
  Layout names: Cover, Title, Section, Default, Split, Grid, Columns, Title-and-Columns,
  Caption, Image, Caption-Top.
- `LayoutExamples` – extra entries in the layout picker (Markdown snippets).
- `Description` is accepted as an alternative to Short/LongDescription.

### presets.json

```json
{
  "Presets": [
    {
      "Name": "Default",
      "TitleFont": "system-ui",
      "BodyFont": "system-ui",
      "Appearance": "dark",
      "DarkBodyTextColor": "#000000",
      "LightBodyTextColor": "#ffffff",
      "DarkTitleTextColor": "#000000",
      "LightTitleTextColor": "#ffffff",
      "DarkBackgroundColor": "#1a1a1a",
      "LightBackgroundColor": "#ffffff",
      "DarkAccent1": "#ffc400",
      "LightAccent1": "#ffc400",
      "Accent1": "#f94144", "Accent2": "#43aa8b", "Accent3": "#f9c74f",
      "Accent4": "#90be6d", "Accent5": "#f8961e", "Accent6": "#577590",
      "LightBgGradient": ["#c7e7ff", "#f0c8ff", "#ffdada", "#ffebb2"],
      "DarkBgGradient":  ["#15354c", "#3e154c", "#4c2828", "#4c3900"]
    }
  ]
}
```

- `TitleFont` / `BodyFont` here are **CSS font-family values** (`"Inter"`,
  `"-apple-system-ui-serif, ui-serif"`, `"system-ui"`), unlike template.json.
- `Appearance`: `light` or `dark` – the default mode of this preset. Users can still
  toggle; every theme must look right in both.
- **Color names describe the color, not the mode.** `DarkBodyTextColor` = dark ink, used
  in *light* appearance on `LightBackgroundColor`; `LightBodyTextColor` = light ink, used
  in *dark* appearance on `DarkBackgroundColor`. Swapping the text pair = invisible text.
  Same for `DarkTitleTextColor` / `LightTitleTextColor` and `DarkAccent1` / `LightAccent1`.
- `"transparent"` backgrounds let the gradient show (Tokyo, Vancouver, San Francisco).
- `LightBgGradient` / `DarkBgGradient`: arrays of colors; the app cycles through them
  slide by slide ("dynamic color background"). Keep 4–11 entries. Defined here, not in CSS.
- `Accent1`…`Accent6`: highlight/accent palette, also chart fallback colors.
- Several presets appear as a dropdown; `info.json → "preset"` picks one by `Name`
  (Helvetica/Garamond: Light, Dark · Basel: Default, Dark · Tokyo: Default, Light · others: Default).

### CSS

The engine (`.Engine/main.css`) does the heavy lifting: container-query based type
scale, layouts, media, charts. Your CSS sits on top. Patterns used by iA's own themes:

```css
/* 1. fonts (files in the theme folder; relative URLs) */
@font-face { font-family: 'Albert Sans'; font-style: normal; font-weight: 400;
  src: url('fonts/albert-sans-regular.woff2') format('woff2'); }

/* 2. code colors + chart palette (light and dark) */
:root { --code-background: #eee; --code-text: #303030; --dark-code-background: #101010; /* … */ }
section.light { --graph-data-0: #d94b78; --graph-data-1: #efbc74; /* … up to 7 */ }
section.dark  { --graph-data-0: #d85c83; /* … */ }

/* 3. heading weights / sizes – use iA's selector form so specificity beats the engine */
[class*='layout-'] > div h1 { font-weight: 900; }
section > :not([class*="layout-"]) h1,
[class*="layout-"] > div h1 { font-size: 2.986em; line-height: 1; }

/* 4. alignment per layout (engine variables, see engine-css.md) */
:root { --text-horizontal-align-layout-cover: left; --text-vertical-align-layout-cover: center; }
/* or the inner div directly */
.layout-cover > div { justify-content: flex-end; align-items: flex-start; }

/* 5. backgrounds per layout (bitmap, SVG file, or inline SVG with rgb() colors – hex breaks) */
.backgrounds .cover-container { background-image: url("image1.jpg"); background-size: cover; background-position: center; }
.backgrounds .v-split-container { background-image: url('data:image/svg+xml;utf8,<svg …><path fill="rgb(255,0,0)" …/></svg>'); }
.slide-background { /* all backgrounds */ }

/* 6. header / footer / logo per layout */
.cover-container .header, .cover-container .footer { display: none; }

/* 7. responsive: mobile-first; desktop tweaks */
@media (min-width: 768px) { /* … */ }
@media (max-width: 639px) { [class*="layout-"] > div h1 { font-size: 2.074em; } }
```

Tips:
- Prefer engine variables (`--scale-factor-h1`, `--font-weight-h2`, `--letter-spacing-h1`,
  `--case-h1: uppercase`, `--line-height-p`, `--margin-h2`) over hard-coded sizes;
  the engine scales them with the viewport. Full catalog: `engine-css.md`.
- Don't hard-code text/background colors in CSS – leave them to presets so the Style
  inspector can override them.
- Appearance classes: `section.light` / `section.dark`; background luminance classes
  `has-light-background` / `has-dark-background` (Helvetica uses them to invert the
  placeholder image).
- Debug by outlining: `.cover-container { outline: 4px solid red; } .layout-cover > div { outline: 4px dashed red; }`.

## Custom fonts – three steps

1. Copy `.woff2` (or `.ttf`) files into the theme folder.
2. Declare `@font-face` at the top of the CSS with relative `url()`s (one per weight/style).
3. `template.json` → `"TitleFont": "Roboto Slab"` (display name);
   `presets.json` → `"TitleFont": "'Roboto Slab', serif"` (CSS family).
   Setting the family only in CSS works but removes the Style-inspector override.

## Built-in themes (2.0.2)

| Name (`template` id) | Family | Font | Look |
|---|---|---|---|
| Helvetica (`helvetica`) – default | Typographic | Helvetica | Swiss, black on white; presets Light/Dark |
| Garamond (`garamond`) – premium | Typographic | Garamond | Renaissance serif |
| Zurich (`zurich`) | Classics | Helvetica | minimal Swiss, one headline size |
| Paris (`paris`) | Classics | Literata (Didot mood) | alternating color backgrounds |
| New York (`new york`) | Opinionated | Inter | yellow & black |
| Basel (`basel`) | Opinionated | Noto Serif | white on black serif |
| San Francisco (`san francisco`) | Vibrant | system | colorful gradient backgrounds |
| LA (`la`) | Vibrant | – | loud, animated backgrounds |
| Copenhagen (`copenhagen`) | Pastels | Albert Sans | Nordic pastels |
| Vancouver (`vancouver`) | Pastels | Montserrat | earthy dynamic colors |
| Tokyo (`tokyo`) | Colorful | system | Metro-line gradients, presets Default/Light |
| Milano (`milano`) | Colorful | Playfair Display | elegant, dynamic colors |

Read their sources in `.Themes/<Name>/` for working examples (fonts, gradients, chart
palettes). Do not edit them – they are restored on every launch.

## Install and test

```
scripts/install_theme.sh path/to/MyTheme        # validates JSON, copies into Themes/
scripts/install_theme.sh --list                 # lists custom + built-in themes with ids
```

Then quit/relaunch iA Presenter once, open a deck, pick the theme in Design → Theme (or
set `"template": "mytheme"`). Check **both** appearances, every layout you care about
(cover, section, split, grid, caption, image background, table/chart), and a phone-sized
window if the deck will be shown on mobile. Remove debug outlines before sharing. To
share a theme, zip the folder; the receiver drops it into their `Themes/`.
