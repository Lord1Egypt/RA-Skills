# Example 01 — NovaSync

A minimal, developer-oriented file-sync brand mark. Good stress-test for:

- **Letterform + motion** (the `N` combined with orbit arrows).
- **Small-size legibility** — the orbit ring must not dissolve at 16 px.
- **0.5-unit gap trick** — the arrows and the letter share the single path but read as separate layers.

## Concept brief (auto-derived)

```yaml
product_name: "NovaSync"
slug: "novasync"
purpose: "cross-device file sync tool for developers"
audience: ["developer", "power_user"]
mood_keywords: ["clean", "geometric", "trustworthy", "modern"]
avoid_keywords: ["playful", "childish", "handdrawn", "gradient"]
preferred_color: "#4F46E5"
metaphor_hints: "letter N + orbit arrows"
composition: "symbol_only"
shape_family: "letterform"
```

## Expected deliverables

```
output/novasync/
├─ master-24.svg
├─ mono/logo-16.svg … logo-512.svg
├─ color/logo-16.svg … logo-512.svg   (fill=#4F46E5)
├─ png/logo-16.png  … logo-512.png
├─ favicon/favicon.ico + apple-touch-icon-180.png
├─ brand.json
└─ _review.png
```

## Success criteria

- `readable_at_16px == true`
- Vision-LLM `score ≥ 8.5`
- No `high`-severity issue at the final iteration
- Passes `python scripts/validate_svg.py output/novasync/master-24.svg`
