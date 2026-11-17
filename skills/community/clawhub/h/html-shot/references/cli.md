# Rendering reference

## Contents

- Capture modes and pixels
- Parameters
- Local assets
- Formats and alpha
- Readiness and failures
- Examples

## Capture modes and pixels

```bash
node "$SKILL_DIR/render.mjs" <local.html|local.svg|file-url|http-url> <output> [options]
```

Create the parent output directory first. Body capture is the default. With no explicit
size, measure the body's rendered box at an initial viewport of 1200×630, growing only
as needed. If viewport-dependent sizing cannot converge, capture the initial viewport
and print a warning. Body overflow is not included. A body with no fixed width fills its
viewport; this is not content-aware auto-cropping.

- Default mode: `--width/--height` set viewport and capture dimensions on the given axes.
- `--selector CSS`: capture one visible element; width/height set its layout viewport only.
  A selector matching several elements is an error; make the selector unique.
- `--full`: capture the full scrollable document; width/height set viewport, not output size.
- If both selector and full are supplied, selector wins with a note.
- Final pixels = CSS capture size × dpr, rounded to whole pixels. Element/full capture uses
  the actual intermediate bitmap's size, so fractional CSS boxes may round by one pixel.
- Render density = max(scale,dpr). Supersampling can alter fine filter/grain appearance;
  use `--scale 1` to compare with a 1× screenshot. Never promise identical pixels across OSes.

## Parameters

| Option | Accepted value / default |
| --- | --- |
| `--width`, `--height` | Positive whole CSS pixels; automatic otherwise |
| `--dpr` | 0.05–10; default 1 |
| `--scale` | 0.1–10; default 2 |
| `--format` | png, jpeg (jpg alias), webp; overrides extension |
| `--quality` | Integer 1–100; default 90; JPEG/WebP only |
| `--palette` | Indexed PNG, up to 256 colours; no dithering |
| `--colors` | 2, 4, 16, 256; implies palette; stable 1/2/4/8-bit presets |
| `--transparent` | Omit browser background; does not remove page-painted backgrounds |
| `--scheme` | light or dark; emulate prefers-color-scheme |
| `--style` | Additional CSS injected after load, before measurement |
| `--base` | Extra local asset root; nearest project public/ by default |
| `--wait` | Nonnegative whole milliseconds; default 150 |
| `--wait-for` | Wait for a unique visible CSS readiness marker |
| `--timeout` | 1–3600000ms; default 60000; browser launch/capture deadline |
| `--max-pixels` | Positive safe integer; default 64000000; max raster area |
| `--channel` | chrome/msedge, including -beta/-dev variants |
| `--executable` | Existing browser binary; alternative to channel/download |
| `--offline` | Local input only; refuse every request (incl. WebSocket, iframe, worker, popup) not sent to the render's own server |
| `--allow-missing` | Opt in to exit 0 despite subresource/runtime warnings |
| `--help`, `--version` | Standalone CLI commands; no dependencies/browser needed |

The pixel budget applies to intermediate render dimensions as well as output, with an
additional 32767-pixel per-axis cap. A 1200×630 card at scale 2 costs 2400×1260 pixels.
The budget is a guardrail, not an operating-system memory limit or an untrusted-code sandbox.

PNG permits varying palette lengths. The CLI deliberately exposes four presets;
sharp's `colours` sets the palette length (2/4/16/256), which produces the 1/2/4/8-bit
PNG outputs — the actual number of distinct colours can be lower. Do not describe 64 as
an illegal PNG palette length or promise quantisation is lossless.

## Local assets

A throwaway loopback HTTP server serves the input directory first, then the explicit
`--base` or the nearest project `public/`. Relative paths and site-absolute paths therefore
resolve natively; MIME types and UTF-8 headers are supplied for common web resources.
All ancillary files must reside inside those roots. Parent-directory assets outside them
are intentionally unavailable: copy assets into a dedicated render folder or pass a suitable
base directory. Symlink escapes and hidden path segments are refused; `.well-known` is allowed.

Use a narrow asset-only base. Do not choose a home directory or a project containing secrets.
The page can read any non-hidden file within the served roots. The server answers only the
per-run hostname `<random-token>.localhost`, which limits other local clients; it does not
protect those files from the page being rendered. Its responses send
`Referrer-Policy: same-origin`, so that hostname is not passed to other origins.

A `file://` source is treated as a local file and served through the same mechanism. SVG is
wrapped in HTML, uses intrinsic dimensions/viewBox, and preserves aspect ratio when only one
output axis is specified. Width/height without a usable viewBox are used to repair it. Relative
SVG resources still require files under the permitted roots. The helper is not a complete XML
validator and does not resolve DTD entities; export self-contained SVG without custom entities.

## Formats and alpha

Infer PNG/JPEG/WebP from output extension, or select explicitly with `--format`. Be deliberate
if extension and encoded format differ. PNG/WebP can retain alpha; JPEG is flattened on white.
Try palette only for flat artwork and inspect small type/gradients after conversion. For photos,
start with WebP quality 82 or JPEG quality 90 instead of reduced-colour PNG.

Use `inspect.mjs`: it reports dimensions, format, alpha-channel presence, and pixel opacity.
A rounded badge should have non-opaque pixels; an apple-touch icon must be fully opaque.

## Readiness and failures

Wait for page load, then network-idle for at most 10s, fonts, an optional visible marker, and
extra wait. The capture deadline also bounds waiting for fonts. Service workers are blocked.
Finish finite animations and cancel infinite animations before measurement and capture; this
is a static capture policy, not timeline/frame capture. JS timers, canvas, videos, random data,
and remote content are not guaranteed deterministic. Lazy below-fold images are not force-loaded;
provide a readiness marker after the source has made required content available.

Main-document HTTP errors are fatal. HTTP subresource errors, failed requests, broken decoded
images and uncaught page JS errors print notes; an image may still be written for inspection
but exits nonzero unless `--allow-missing` was explicitly selected. The browser's own missing
`/favicon.ico` tab-icon request is ignored. Network-idle warnings do not alone make the run fail.

The renderer deliberately uses no Playwright request interception: with interception on,
Playwright aborts every URL ending in `/favicon.ico`, so an `<img src="favicon.ico">` would
vanish. Such images render normally, and a missing or undecodable one is reported like any
other image. Playwright emits no network events for those URLs, so the broken-image check is
what catches them; a missing `favicon.ico` used only as a CSS background is not detected.

A temporary image is encoded beside the target and renamed only on successful encoding.
Expected failures close Chromium and the local server. Do not expect guaranteed cleanup after
SIGKILL, a machine crash, or an OS/filesystem failure. Existing targets are replaced.

## Examples

```bash
node "$SKILL_DIR/render.mjs" card.html og.png --width 1200 --height 630
node "$SKILL_DIR/render.mjs" card.html og@2x.png --dpr 2 --offline
node "$SKILL_DIR/render.mjs" chart.html chart.png --selector "#chart" --wait-for "[data-ready]"
node "$SKILL_DIR/render.mjs" logo.svg logo.png --width 1024 --transparent
node "$SKILL_DIR/render.mjs" sheet.html mark.png --selector "#mark" --transparent \
  --style "html,body,.cell{background:transparent!important}"
node "$SKILL_DIR/render.mjs" https://example.com page.webp --full --quality 82
```
