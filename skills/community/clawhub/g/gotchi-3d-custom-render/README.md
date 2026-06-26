# gotchi-3d-custom-render

Render custom or hypothetical Aavegotchi 3D images from trait mixes, wearable combinations, and named presets.

This skill supports two execution paths:

- `hosted` (default): uses Aavegotchi's hosted renderer for official-style output
- `unity`: uses the local Unity worker for fallback and local-only experimentation

## What It Produces

- full-body PNG
- headshot PNG
- manifest JSON

## Main Entry Point

From the repo root:

```bash
bash scripts/render-custom-gotchi.sh --preset aagent-eth
```

Hosted mode is the default and is the recommended path for most uses.

## Friendly Examples

Search wearables:

```bash
bash scripts/render-custom-gotchi.sh --find-wearable aagent
```

Render a named preset:

```bash
bash scripts/render-custom-gotchi.sh --preset aagent-eth
```

Render from wearable names:

```bash
bash scripts/render-custom-gotchi.sh \
  --collateral ETH \
  --eye-shape Common \
  --eye-color Common \
  --body 'Aagent Shirt' \
  --face 'Aagent Headset' \
  --eyes 'Aagent Shades' \
  --head 'Aagent Fedora Hat' \
  --hand-right 'Aagent Pistol'
```

Render a batch gallery:

```bash
bash scripts/render-preset-gallery.sh --preset aagent-eth --gallery-name quicklook --open
```

## Output Paths

Generated files are written to `Renders/` and ignored by git:

- `Renders/<slug>-full.png`
- `Renders/<slug>-headshot.png`
- `Renders/<slug>-manifest.json`

## Repo Layout

- `scripts/render-custom-gotchi.sh`: main wrapper
- `scripts/render-hosted-custom.mjs`: hosted renderer path
- `scripts/run-unity-render.sh`: Unity batch runner
- `scripts/render-preset-gallery.sh`: multi-render gallery helper
- `references/presets.md`: preset names, slot aliases, backgrounds
- `references/request-schema.md`: request JSON structure
- `references/wearables.tsv`: built-in wearable name catalog
- `unity/GotchiCustomRenderer`: Unity project used for local rendering

## Telegram / AAi

This skill is also packaged for AAi/OpenClaw usage.

Natural-language requests like these should route here:

- `Render a custom ETH gotchi with common eyes, aagent hat, shades, shirt, headset, and pistol in right hand.`
- `Show me a portrait gotchi on a cream background.`

## Requirements

Hosted mode:

- `node`
- `jq`
- `npm install` in the repo root so the bundled PNG background compositor is available when a non-transparent background is requested

Unity mode:

- Unity `2022.3.11f1`
- local Unity editor installation

## Notes

- Hosted mode ignores some local-only pose behavior.
- Unity mode is mainly for fallback, debugging, and local experimentation.
- No environment variables are required for normal hosted rendering.
- The Unity `Library/`, `Logs/`, `UserSettings/`, `Renders/`, and top-level generated outputs are intentionally ignored.
