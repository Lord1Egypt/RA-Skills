# Starter templates

Two starter files ship with this skill. Copy one into your own working directory, edit
the copy, and render that. Both use system fonts only, so they render with no font
directory to set up.

| File | Use it for | Default size |
| --- | --- | --- |
| `template.example.html` | An OG/social card | 1200×630 |
| `icon.example.html` | A transparent app icon, favicon master or badge | square, 1024 master |

```bash
cp "$SKILL_DIR/template.example.html" og.html     # a card
cp "$SKILL_DIR/icon.example.html" icon.html        # a transparent mark
```

`$SKILL_DIR` is this skill's own directory — wherever your agent installed it.

## The card template

`template.example.html` is a 1200×630 card. `body` gets an explicit `width`/`height` in
pixels, so the output size flows from the CSS.

```bash
node "$SKILL_DIR/render.mjs" og.html og.png
```

To use a custom font, set the body's `font-family` to that font's family name and add a
`@font-face` rule:

```css
@font-face { font-family:"MyFont"; src:url("/fonts/xxx.woff2") format("woff2"); }
```

Put the font file in the project's `public/fonts/` — the site-absolute `/fonts/...` path
resolves there — or next to the HTML file and reference it relatively.

The `lang` attribute is optional. Set it to the content's language when you know it; any
BCP-47 tag is accepted (`zh-CN`, `zh-TW`, `ja`, `ko`, `en`). Leave it off and the renderer
uses the host default. It is not just markup: when the font stack does not pin a CJK
family, it decides which one the browser falls back to, and 骨 / 直 / 今 are drawn
differently for zh-CN, zh-TW, ja and ko. Leaving it off makes the output depend on the
locale of whatever machine renders the card.

## The icon template

`icon.example.html` is a transparent square mark. Every size in it is in `vmin`, not
pixels: an icon has no one size. `icons.mjs` renders the master at 1024, you may want
512 or 180 elsewhere, and a body pinned to `width:320px` would draw a 320 px mark in the
corner of whatever larger frame it is given — the shape would not fill the icon. `100vmin`
makes `body` a square that fills the frame it is handed, and vmin-based type and radii
scale with it. Sizes are given as a share of the icon: `41.25vmin` means "41.25% of the
icon's side".

It feeds both entry points:

```bash
node "$SKILL_DIR/render.mjs" icon.html icon.png --width 1024 --height 1024 --transparent
node "$SKILL_DIR/icons.mjs"  icon.html public --preset web --bg "#1b3fd8"
```

Without `--width`/`--height` you get a square at the viewport's shorter side (630). Pass
the size you want; 1024 is the usual master.

### Transparency takes three things

Missing any one of these fails silently — the image comes out opaque:

1. **CSS** — `html` *and* `body` must be `background: transparent`. Any opaque colour on
   either (even `#fff` or a page-grey) fills the area outside the border-radius with that
   colour.
2. **The shape goes on a child, never on `body`.** A background set on `body` is
   propagated to the root canvas, and the canvas is not clipped by `body`'s
   `border-radius` — put the radius and fill on `body` and the corners come back opaque
   no matter what else you do. That is why the mark in the template is an `.icon` div and
   `body` is only a transparent box.
3. **The flag** — `--transparent`. It only removes the *browser's* default white; it
   cannot override a background the page paints itself.

Do not rely on a viewer's background: it can hide an unwanted opaque fill. Check the
actual alpha pixels with the bundled inspector, which reports the format, the dimensions
and whether any pixel is really transparent:

```bash
node "$SKILL_DIR/inspect.mjs" icon.png
```

`"opaque":false` means the file really has transparent pixels; `"hasAlpha":true` on its
own only says the channel exists.

One thing transparency does **not** survive: apple-touch-icon. iOS composites alpha onto
black, so that one file must be flattened — `icons.mjs` does it for you, onto `--bg`.

The shape in the template is a generic rounded mark, not a guaranteed match for any OS
icon mask. For Apple delivery, prefer purpose-made full-bleed square artwork.
