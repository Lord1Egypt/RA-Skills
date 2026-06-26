# Presets And Aliases

## Presets

- `blank-eth`
  - ETH collateral
  - mythical/high eyes
  - empty wearables
  - `arcade-purple` background
  - `idle` pose

- `aagent-eth`
  - ETH collateral
  - mythical/high eyes
  - head `56`
  - right hand `58`
  - `arcade-purple` background
  - `hero` pose

- `portrait-eth`
  - ETH collateral
  - mythical/high eyes
  - empty wearables
  - `studio-cream` background
  - `portrait` pose

## Background Aliases

- `arcade-purple` -> `#806AFB`
- `studio-cream` -> `#F4EDE1`
- `slime-lime` -> `#D8FF5E`
- `night-ink` -> `#131722`
- `soft-sky` -> `#D9F3FF`
- `gotchi-radio` -> `#1DDA8D`
- `transparent` -> `transparent`

## Pose Aliases

- `idle`
  - centered classic front-facing framing
- `portrait`
  - tighter crop tuned for headshot requests
- `hero`
  - slight three-quarter turn for more depth
- `left`
  - turns the gotchi to the left
- `right`
  - turns the gotchi to the right

## Friendlier Slot Names

- `--slot hat=56`
- `--slot weapon=58`
- `--slot left=12`
- `--slot right=58`
- `--wearables 'head=56,hand-right=58'`

Wearable flags also accept quoted names:

- `--head 'Aagent Fedora Hat'`
- `--face 'Aagent Headset'`
- `--eyes 'Aagent Shades'`
- `--body 'Aagent Shirt'`
- `--hand-right 'Aagent Pistol'`

Wearable search helper:

- `--find-wearable aagent`
- `--find-wearable shades`
- `--find-wearable pistol`

## Render Modes

- `hosted`
  - default mode
  - use the hosted Aavegotchi renderer only
  - best match for the existing `aavegotchi-3d-renderer` look
- `auto`
  - hosted renderer first
  - falls back to local Unity if hosted assets are unavailable
- `unity`
  - use the local Unity worker only
  - best when testing local-only rendering behavior

## Gallery Helper

- `bash scripts/render-preset-gallery.sh`
  - renders the default preset set:
    - `blank-eth`
    - `aagent-eth`
    - `portrait-eth`
  - writes:
    - `Renders/<gallery>-gallery.json`
    - `Renders/<gallery>-gallery.html`

- `bash scripts/render-preset-gallery.sh --preset aagent-eth --preset portrait-eth --gallery-name quicklook`
  - renders only the selected presets

- `bash scripts/render-preset-gallery.sh --preset aagent-eth --preset portrait-eth --gallery-name quicklook --skip-failures`
  - keeps going if one preset fails
  - records failures into the gallery JSON and HTML

- `bash scripts/render-preset-gallery.sh --preset aagent-eth --gallery-name quicklook --open`
  - opens the generated HTML gallery when the run finishes

- `bash scripts/render-preset-gallery.sh --gallery-name radio -- --bg gotchi-radio`
  - forwards extra args after `--` to every preset render
