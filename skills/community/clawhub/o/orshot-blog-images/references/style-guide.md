# In-article image style guide

The look of every image inside the post. The blueprints already follow it; use this when you change a layout or build a page from scratch.

## Shape and size

- Canvas 1200x960 for every in-article image. Blogs cap image height around 560px and shrink to fit, so 1200x960 is the tallest that still fills the column. A taller canvas only gets smaller.
- Outer padding 56px. The headline sits at the top, content starts at y 228, a footer line sits at y 912.
- Give everything room: cards at least 90px tall, 24px gaps, text boxes sized for the longest line. Nothing overlaps.
- Fill the page. A card with 400px of empty space under its content gets shorter, not left tall.

## The recipe

- **Background:** canvas `#F7F6F2`. Optional dotted-grid texture full bleed (`https://storage.orshot.com/cloud/w-11/brand_assets/1770156105075-133751010-10262400.jpg`, objectFit cover, zIndex 0) under a scrim rectangle `rgba(250,250,248,0.8)` (zIndex 1). Drop both for a plain background.
- **Headline inside the image, two lines:** line 1 Fraunces 700 50px `#141414` at (56,46); line 2 Fraunces 700 italic 50px in the accent at (56,100). Line 2 is the takeaway. Under line 2, an underline swoosh SVG in the accent, sized to the text, at (58,162). A small four-point sparkle SVG at the top right (1118,36), 30px.
- **Optional chip above the headline** ("CHECKED OCT 2026"): accent-tint rectangle radius 8 with Spline Sans Mono 15px 600 in the accent.
- **Cards:** white, radius 16, `dropShadowY: 8px`, `dropShadowBlur: 18px`, `dropShadowColor: rgba(20,20,20,0.10)`. The option the reader should notice is white; the other one is dimmed grey `#EEEDE8` with a white pill inside.
- **Pills:** a shape behind the text. Mono 15px 600 on the accent tint, grey `#EFEEEA` with `#4A4A48`, or red tint `#FCEBE8` with `#B42318` for a warning. Value pills radius 999, Inter 700 19px: grey for the other option, solid accent with white text for the highlighted one.
- **Numbered cards:** 30px black circle with a white Inter 700 15px number, Fraunces 600 22px two-line title, then a 24px logo and an Inter 500 17px name.
- **Browser frame** for a website: white card, `#141414` 40px header with three dots and the domain in mono, the screenshot with objectFit contain and the frame sized to its ratio.
- **Code card:** `#141414` radius 16, Spline Sans Mono 16px `#D6D6D2`, the key line on an accent highlight at 40% in white. Indent with non-breaking spaces.
- **Type:** Fraunces for headlines and card titles, Inter for body (16 to 19px), Spline Sans Mono for chips, numbers and the footer (14 to 16px). Footer: mono 16px `#6B6A66` with the source and the month.
- **Colors:** ink `#141414`, body `#4A4A48`, muted `#6B6A66`, bar grey `#CFCDC6`, one accent and its tint. Nothing else.
- **60 words or fewer** per image.

## Every image shows something real

At least one of:

- the real output: the actual PDF, image, screenshot or video frame, cropped to what matters
- data drawn as data: bars with values on them, a takeaway note, a source line
- logos of the tools named, as small marks (`https://cdn.simpleicons.org/<name>/<hex>` or the favicon URL in SKILL.md)
- icons in tinted tiles: Lucide line icons (`https://cdn.jsdelivr.net/npm/lucide-static@0.460.0/icons/<name>.svg`)
- request and result: code on the left, the output it made on the right, joined by an arrow

Never: text-only images, grey placeholder lines pretending to be a document, a credit line or watermark.

## Checklist before saving each image

- 1200x960, two-line serif headline with the swoosh
- nothing overlaps, nothing wraps at the right edge, no half-empty cards
- at least one real visual
- one accent color plus greys
- no text under 14px
- rendered at scale 2 and looked at
- alt text names what the image shows
