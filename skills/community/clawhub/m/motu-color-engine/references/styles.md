# MotuArt Color Engine — styles overview

The live catalog is authoritative — run `scripts/styles.sh` to list current ids.
This is a quick orientation to the two style tiers and the shipping looks.

## Two tiers

- **base** — a skin-tone target (the anchor the engine grades skin toward).
  Pick one as the foundation. Default: `motu_korean_id`.
- **flavour** — a look/grade layered on top (film, clean, teal, etc.).
  Optional. Combine with a base using the composite separator (default `@`):
  `<flavour>@<base>`, e.g. `kodak_gold@motu_korean_id`.

Passing only a base gives clean skin-tone correction with no stylization.

## Shipping looks (flavours)

| Look | When to use |
| --- | --- |
| Leica Classic | Neutral, true-to-life editorial; restrained contrast. |
| Kodak Gold | Warm nostalgic film; golden skin, cozy mood. |
| Clean Cool | Crisp, cool, commercial/e-commerce clarity. |
| Cine Teal | Cinematic teal shadows; moody outdoor/urban. |
| Milk Tea | Soft warm beige; lifestyle, gentle portraits. |
| JP Airy | Bright, airy, low-contrast Japanese style. |

Style ids differ from display names — always resolve the exact id via
`scripts/styles.sh` before calling `grade.sh`.

## Strength

`strength` scales the look (default `1.0`). Use `0` to disable stylization (base
correction only), and up to ~`1.5` for a stronger grade. Report `skin_dE` from the
result so the user can judge accuracy.
