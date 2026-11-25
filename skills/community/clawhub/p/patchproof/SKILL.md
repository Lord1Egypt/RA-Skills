---
name: patchproof
description: Find the 9-slice (nine-patch) borders of game UI panel images and prove each detection by re-rendering. Use when asked to work out 9-slice borders for a UI kit, set Unity spriteBorder values, Godot StyleBoxTexture patch margins, or Android .9.png markers for panel PNGs — for example "find the 9-slice borders for these panels", "set up nine-patch for my UI kit", or "which of these panels can be sliced cleanly". Not for making textures tile seamlessly (that is seamproof) or recovering the grid of damaged pixel art (that is snapgrid). Scans a whole folder at once and writes Unity .meta, Godot .tres and Android .9.png files for every proven panel.
license: MIT
compatibility: Requires Python 3.10+; pip installs Pillow and numpy. Runs fully locally on CPU; network is needed only to install.
---

# patchproof

## What this tool does

patchproof finds the 9-slice borders (left, right, top, bottom) of game UI panel PNGs — a single file or a whole folder of panels in one run. Every detection is proved by resynthesis: the panel is re-rendered 9-sliced at several sizes, odd sizes included, and its corners must come out pixel-identical, with a distortion score under the threshold. A panel that cannot be proved is reported UNCERTAIN with a reason, never given made-up border numbers. For every proven panel it also writes the engine files: a Unity `.meta` sidecar with `spriteBorder`, a Godot `.tres` StyleBoxTexture, and an Android `.9.png`.

## Install

```bash
pip install git+https://github.com/RakTikoo/patchproof
```

This provides the `patchproof` command.

## Run

Scan a folder of panels (a single PNG file also works), writing exports and a report to the output folder:

```bash
patchproof scan examples --out out
```

A folder is scanned non-recursively for PNG files. `--threshold 6.0` is the default strictness: how clean a slice must be to earn PROVEN. Lower it for a stricter pass on borderline kits.

## Reading the results

The table lists each file with its verdict, the four borders (L, R, T, B) and its distortion score, and ends with a count line such as `6 proven, 1 uncertain -- report: out/report.json`. Read verdicts per panel:

- `PROVEN` — the borders were verified by re-rendering; the panel PNG, its `.meta`, `.tres` and `.9.png` exports are in the output folder.
- `UNCERTAIN` — no borders are reported (dashes in the table, `null` in the report) and no exports are written. The stated reason says why, for example a distortion score above the threshold on a photo-like centre. Treat UNCERTAIN as "a human should set this one by hand", not as a failure of the run.

`report.json` carries the same facts per panel: `borders`, `padding` (transparent content margins, reported separately from the borders), `verdict`, `score`, `sizes_checked`, `corners_identical`, and `reason` where one applies. Exit code `0` means the scan completed — it does not mean every panel was proven, so read the per-panel verdicts. Exit code `2` means the run stopped with a clean one-line error (not a PNG file, a folder with no PNGs, or a path that does not exist).

## Limits

- Centres must be flat, smoothly gradient, or stationary grain (parchment-style texture can be proven under a statistical criterion; its grain rescales when stretched, as with any stretch). Repeating patterns (checker, brick, diamond fills) and directional grain such as wood still abstain as UNCERTAIN — stretching would change the pattern's period. Centres that should be tiled rather than stretched are not modelled.
- One panel per image: sprite sheets or atlases holding several panels in one PNG are not segmented.
- Detection on ornate panels is a judgement call: the score measures how clean the slice is, not taste. Borderline kits should use a stricter `--threshold` and a human look at the UNCERTAIN pile.
- Exports are written from the detection and round-trip tested, but they are not validated inside Unity or Godot; the first real engine import is still worth a look.
- Panels are processed in memory as full images; a folder of 8K textures will be slow. PNG only.
