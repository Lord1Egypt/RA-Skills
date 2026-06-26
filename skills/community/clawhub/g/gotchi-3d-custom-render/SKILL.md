---
name: gotchi-3d-custom-render
description: Render custom Aavegotchi 3D images from arbitrary trait and wearable combinations. Use when the user describes a synthetic or hypothetical gotchi look in plain language, asks for an outfit preview, headshot, or full-body image, and is not asking for an existing onchain token by tokenId or inventory URL.
---

# gotchi-3d-custom-render

Use this skill when the user wants a custom 3D gotchi render from selected traits, wearable IDs, wearable names, or a named preset.

Plain-language requests should also route here, for example:

- "render an ETH gotchi with common eyes, aagent hat, shades, shirt, headset, and pistol"
- "show me a custom gotchi portrait on a cream background"
- "make a gotchi outfit preview with wizard hat and blue wand"
- "give me a headshot of a hypothetical gotchi with shades and a fedora"

Do not wait for the user to explicitly say `gotchi-3d-custom-render`.

## What this skill does

- writes a structured render request JSON
- uses the hosted Aavegotchi renderer by default for official-style output
- falls back to the local Unity batch worker when hosted assets are unavailable
- returns:
  - full-body PNG
  - headshot PNG
  - manifest JSON
- supports friendlier presets, slot aliases, themed backgrounds, and render-mode selection
- wearable flags accept either numeric IDs or quoted wearable names
- supports plain-language outfit requests after routing picks this skill

## Constraints

- requires a local Unity editor installation
- hosted mode matches the existing Aavegotchi renderer look much more closely, but may ignore custom local-only pose behavior
- Unity fallback is still useful for hypothetical combinations or local debugging
- hosted mode can run on non-Unity hosts as long as `node`, `jq`, and `npm install` have been run in the repo root so the bundled PNG background compositor is available when a non-transparent background is requested
- intended for local development first, then AAi/Telegram integration through hosted mode
- no environment variables are required for normal hosted rendering

## Routing Notes

- Prefer this skill when the user describes a look, outfit, traits, wearables, background, portrait, headshot, or hypothetical gotchi.
- Prefer `aavegotchi-3d-renderer` instead when the user gives a tokenId or inventory URL for an existing gotchi.
- If the user gives both a tokenId and custom outfit instructions, clarify whether they want the real token render or a hypothetical custom loadout.

## Entry points

- main wrapper: `scripts/render-custom-gotchi.sh`
- preset gallery helper: `scripts/render-preset-gallery.sh`
- direct Unity runner: `scripts/run-unity-render.sh`
- Unity project: `unity/GotchiCustomRenderer`

## Quick usage

From the skill root:

```bash
bash scripts/render-custom-gotchi.sh \
  --preset aagent-eth
```

Default mode is `hosted`. Use `--render-mode auto` if you specifically want hosted-first with Unity fallback, or `--render-mode unity` for local-only rendering.

Outputs land in:

- `Renders/<slug>-full.png`
- `Renders/<slug>-headshot.png`
- `Renders/<slug>-manifest.json`

## Input contract

Supported flags:

- `--preset`
- `--slug`
- `--haunt-id`
- `--collateral`
- `--eye-shape`
- `--eye-color`
- `--skin-id`
- `--background`
- `--pose`
- `--body`
- `--face`
- `--eyes`
- `--head`
- `--pet`
- `--hand-left`
- `--hand-right`
- `--left-hand`
- `--right-hand`
- `--slot`
- `--wearables`
- `--print-presets`
- `--write-only`
- `--render-mode`
- `--hosted-only`
- `--unity-only`
- `--find-wearable`

Wearable flags can take either:
- numeric IDs like `--head 59`
- quoted names like `--head 'Aagent Fedora Hat'`

## Friendly Examples

```bash
bash scripts/render-custom-gotchi.sh --find-wearable aagent
bash scripts/render-custom-gotchi.sh --preset portrait-eth
bash scripts/render-custom-gotchi.sh --preset aagent-eth
bash scripts/render-custom-gotchi.sh --preset aagent-eth --render-mode auto
bash scripts/render-custom-gotchi.sh --body 'Aagent Shirt' --face 'Aagent Headset' --eyes 'Aagent Shades' --head 'Aagent Fedora Hat' --hand-right 'Aagent Pistol'
bash scripts/render-custom-gotchi.sh --wearables 'head=56,hand-right=58' --bg gotchi-radio --pose hero
bash scripts/render-custom-gotchi.sh --slot hat=56 --slot weapon=58 --background transparent
bash scripts/render-preset-gallery.sh
bash scripts/render-preset-gallery.sh --preset aagent-eth --preset portrait-eth --gallery-name quicklook
bash scripts/render-preset-gallery.sh --preset aagent-eth --preset portrait-eth --gallery-name quicklook --skip-failures
bash scripts/render-preset-gallery.sh --preset aagent-eth --gallery-name quicklook --open
```

Natural-language request examples this skill should handle:

- "render a custom ETH gotchi with common eyes and an aagent pistol"
- "show me a gotchi with aagent hat, shades, shirt, and headset"
- "make a portrait gotchi on a studio cream background"
- "preview this outfit on an ETH gotchi with common eyes"

If you need to inspect the request shape or adjust it manually, read `references/request-schema.md`.
If you need the preset list or alias vocabulary, read `references/presets.md`.

## When to read extra files

- read `references/request-schema.md` when you need the exact JSON payload layout
- read `references/presets.md` when you need preset names, background aliases, or friendlier slot names
- read `references/wearables.tsv` when you need the built-in wearable name catalog used on non-Unity hosts
- read `unity/GotchiCustomRenderer/Assets/Editor/GotchiCustomRenderCLI.cs` only when changing the Unity render behavior
