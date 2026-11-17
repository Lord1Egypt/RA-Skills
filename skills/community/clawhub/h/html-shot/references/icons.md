# Icon sets

## Contents

- Presets and selection
- Source requirements
- Icon parameters
- Output transaction
- Wiring examples and limitations

## Presets and selection

```bash
node "$SKILL_DIR/icons.mjs" <source> <existing-output-directory> [options]
```

| Preset | Default outputs |
| --- | --- |
| web / docusaurus | favicon.ico, favicon.svg if SVG source, apple-touch-icon.png (180) |
| next | favicon.ico, icon.svg (or icon.png 512 for non-SVG), apple-icon.png (180) |
| electron | icon.ico, icon.icns, icon.png (1024) |
| tauri | icon.ico, icon.icns, icon.png (1024), 32x32.png, 128x128.png, 128x128@2x.png (256) |

Use `--only ico,svg,apple,pwa` for web presets, or `--only ico,icns,png` for app presets.
PWA output is opt-in: `--pwa` or `--only pwa` adds icon-192.png and icon-512.png. The Next
preset is intended for App Router's app directory: generate PWA files separately in public/.
An HTML/raster source does not synthesize a fake SVG. Web/docusaurus skip that slot with a
warning, while Next uses its 512px PNG fallback. Selecting only an unavailable SVG fails.

SVG-only passthrough skips browser/encoder imports and permits a non-square source because
no raster icon is being generated. The SVG is copied without sanitising or embedding resources.
Check that linked resources remain reachable after deployment; self-contained SVG is preferred.

## Source requirements

- For browser-rendered icons, use square SVG or responsive square HTML; master is 1024×1024.
  A fixed 320px HTML drawing does not fill a 1024px viewport. Prefer `icon.example.html` —
  see [Starter templates](templates.md) for how it is sized and why transparency needs
  three things at once.
- For raster sources, require a square image with sufficient native resolution. PNG, JPEG,
  WebP, GIF, AVIF, TIFF are decoded to sRGB PNG; use the first frame, honour orientation,
  and downsample oversized masters to at most 1024px without enlarging smaller inputs.
  BMP and ICO input are not supported. Source extension must identify its format correctly.
- Require at least 256px for ICO, 180px for apple-touch, 512px for PWA/Next PNG, and 1024px
  for ICNS/desktop PNG. The largest selected requirement wins. `--small` needs at least 32px.
- Reject undersized sources before committing output. Use `--allow-upscale` only when the
  user accepts interpolation. Files retain exact platform dimensions; no silent clamping.
- Use a separate simple 16/32px drawing for detail-heavy logos. Inspect it at actual size.
- Remote URLs are captured as web pages, not downloaded as raster images. Download remote
  raster artwork through an approved mechanism first, then pass the local file.

## Icon parameters

| Option | Behaviour |
| --- | --- |
| `--preset` | Output names/platform convention; web by default |
| `--only` | Explicit subset; invalid/empty selection fails |
| `--pwa` | Add 192/512 PNG pair; web/docusaurus only, not next/app presets |
| `--bg` | Opaque named/hex colour for apple-touch only; default #ffffff |
| `--small` | Local alternate source for 16/32 ICO entries; only with ICO output |
| `--allow-upscale` | Opt in to interpolation for insufficient raster resolution |
| `--url-prefix` | Public URL directory for snippets, e.g. /assets/icons |
| Renderer flags | scale, wait, base, style, channel, executable, timeout, max-pixels, wait-for, offline |

Renderer flags are relevant to HTML/SVG/page masters. The raster branch does not launch a
browser. `max-pixels` also guards raster-source decoding. Icon generation deliberately has
no allow-missing escape hatch: do not build a set from an incomplete browser render.

Apple-touch output is flattened and has its alpha channel removed. Choose an opaque background
matching the artwork; passing transparent or partially transparent colours is an error. Prefer
full-bleed square Apple artwork if a pre-rounded source leaves visible corners under the OS mask.
The script does not generate a special maskable/safe-zone composition from an ordinary source.
PWA manifest snippets therefore use `purpose: "any"`, not `"maskable"`.

Default ICO uses png2icons' 9-entry 16/24/32/48/64/72/96/128/256 ladder: entries below 64 are
BMP, the rest PNG (the `forWinExe` mix). With `--small`, a six-entry PNG-compressed container combines 16/32
from the simplified mark and 48/64/128/256 from the main mark. Test the default path for legacy
Windows executable support. ICNS is built in JavaScript and does not require macOS iconutil.

## Output transaction

Generate into a private temporary directory under the output directory. Complete all
conversions and collision checks first, then rename targets into place. Keep backups while
committing and attempt rollback on filesystem errors. Preserve recovery files if rollback
fails. Keep source files untouched, except identical SVG passthrough onto the same source path.

This is best-effort multi-file rollback, not a filesystem-wide atomic transaction. SIGKILL,
power loss, concurrent writers, or an unwritable filesystem can leave a temporary recovery
directory. Do not run concurrent generators into the same directory. Unselected existing
files remain untouched; the tool does not delete stale assets or old Next icon variants.

## Wiring examples and limitations

```bash
mkdir -p public app build
node "$SKILL_DIR/icons.mjs" mark.svg public --only ico
node "$SKILL_DIR/icons.mjs" mark.svg public --pwa --bg "#2783de"
node "$SKILL_DIR/icons.mjs" mark.svg app --preset next
node "$SKILL_DIR/icons.mjs" mark.svg public --only pwa
node "$SKILL_DIR/icons.mjs" mark.svg build --preset electron
node "$SKILL_DIR/icons.mjs" mark.svg public --only ico --small simple.svg
```

The script prints HTML/manifest snippets for files actually generated. It infers URL paths
from public/ or static/ segments in relative or absolute output paths. Other directory layouts
need `--url-prefix`; when absent the script explicitly states its site-root assumption. Verify
these paths against your hosting base path and framework configuration. An explicit ICO link
is printed even if the file is placed below the web root.

Presets are common filename bundles, not complete deployment configuration or platform
certification. Tauri Store/MSIX assets and special sizes may require the framework's own icon
pipeline. App Store marketing icons, Android adaptive layers and maskable PWA icons require
purpose-made assets. No obsolete browserconfig/mstile set is generated by default. Safari
pinned-tab SVG can be supplied separately if that feature is required; do not assume every
Safari version ignores mask-icon. Test Next file conventions in the project's actual version.
