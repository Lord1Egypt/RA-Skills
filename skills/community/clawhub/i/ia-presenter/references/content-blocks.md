# Content blocks: images, video, backgrounds

Source: in-app Help (`Images & Videos.html`), online support (visuals/images, videos),
the metadata regex compiled into the iA Presenter 2.0.2 binary, engine CSS classes, and
live tests.

## Syntax

A content block is a **bare path or URL alone on a flush-left line**, optionally followed
by `key: value` lines that must sit **directly under it** (a blank line ends the block):

```
/assets/hero.jpg
Background: true
filter: darken
opacity: 50%

# Title over the image
```

Accepted sources:

| Form | Example | Notes |
|---|---|---|
| Bundle asset | `/assets/photo.jpg` | file lives in `Deck.iapresenter/assets/`. Spaces are fine (`/assets/My Photo.jpg`). |
| Theme asset | `/Theme/image2.webp` | file shipped in the selected theme's folder |
| Remote image | `https://example.com/pic.png` | **must end in** `.jpg .jpeg .png .apng .gif .webp .tif .tiff .svg` (query string allowed) – otherwise it is plain text. Verified working. |
| Unsplash | any `unsplash.com` URL | attribution/caption are added automatically when inserted via the Inspector |
| Video | `/assets/clip.mp4` | `.mp4`, `.m4v`, `.mov` |
| YouTube | paste the watch URL | via Inspector → Visuals → Add YouTube Video (or as a content block) |
| Classic Markdown | `![alt](assets/photo.jpg)` | no leading slash, spaces as `%20`; fewer controls |
| HTML | `<img src="assets/photo.jpg">` | same rules as classic Markdown |

Image formats: png/apng, jpg/jpeg, gif, webp, tif/tiff, svg, pdf.

## Metadata keys

The parser accepts exactly these keys (case-insensitive: `Size`, `size`, `SIZE`
all work):

| Key | Values | Effect |
|---|---|---|
| `size` | `cover` (default) \| `contain` | cover fills the container and may crop; contain letterboxes (`size-cover` / `size-contain`) |
| `x` | `left` \| `center` \| `right` | horizontal position inside the container (only matters when aspect ratios differ) |
| `y` | `top` \| `center` \| `bottom` | vertical position |
| `background` | `true` | image becomes the slide background, text renders on top |
| `filter` | `lighten` \| `darken` \| `grayscale` \| `sepia` \| `blur` | CSS filter (`image-filter-*`, `background-filter-*`) |
| `opacity` | `10%` … `100%` in steps of 10 | `image-opacity-N` / `background-opacity-N` classes |
| `title` | text | title/caption shown with the image (`title: "Placeholder"`) |
| `alt` | text | accessibility text |
| `class` | css class name(s) | extra class on the figure, for custom-theme CSS |
| `caption` | text | caption (used by tables; images use `title`) |

Chart-only keys (`chart`, `orientation`, `bar-type`, `line-type`, `color-type`,
`xlabel`, `ylabel`, `xformat`, `colors`) are documented in `charts.md`. `header` /
`footer` are accepted by the same parser too (undocumented; probably per-slide header/footer
text – verify before relying on it).

Position classes produced: `position-left-top`, `position-center-center`, … ;
size classes: `size-cover`, `size-contain`.

## Patterns

Cover with darkened photo:

```
/assets/cover.jpg
Background: true
filter: darken
opacity: 60%

⇥Kicker
# Talk title
### Speaker · Date
```

Image right, text left (auto split): put the text cell first, then the image cell:

```
## Heading
⇥One sentence the audience should read.

/assets/diagram.png
size: contain
x: right
```

Two images side by side: two content blocks separated by a blank line. Four or more →
grid. Caption: `#### Caption text` in its own cell before (top) or after (bottom) the
image, or use `Layout: Caption` / `Layout: Caption-Top`.

Video: `/assets/demo.mp4` – autoplay and controls are global settings
(Settings → Presentation → Content). Filters/opacity apply to local video but not YouTube.

## Where files live

- Drag & drop into the editor or the Visuals tab copies the file into the bundle's
  `assets/` folder. When generating a deck yourself, copy the files there
  (`scripts/new_deck.py --assets DIR` does this and verifies every `/assets/` reference).
- The Visuals tab can rename (keep the extension!), preview, and **Remove Unused Assets**.
- Theme images referenced from CSS use relative paths (`url("image1.jpg")`), from
  Markdown use `/Theme/image1.jpg`.
