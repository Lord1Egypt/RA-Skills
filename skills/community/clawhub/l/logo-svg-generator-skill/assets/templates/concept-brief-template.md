# Concept Brief Template

Fill this out (or infer sensibly from the user's natural-language request) before Step 3 of the workflow. The completed brief becomes the design contract and is passed to the visual reviewer alongside the SVG.

```yaml
product_name: "NovaSync"
slug: "novasync"                       # auto: lowercase, strip non-alnum, dot->dot, +->plus, &->and
tagline: "Cross-device file sync tool"
purpose: |
  Keep folders in sync across desktop, mobile, and cloud with zero-config,
  aimed at power users and developers.
audience: ["developer", "power_user"]
mood_keywords: ["clean", "geometric", "trustworthy", "modern", "technical"]
avoid_keywords: ["playful", "childish", "handdrawn", "gradient"]
preferred_color: "#4F46E5"             # brand hex
mono_required: true                    # emit monochrome master + branded variant
metaphor_hints: |
  Letter "N" combined with sync-arrows loop, or two orbiting nodes.
composition: "symbol_only"             # symbol_only | monogram | pictogram
shape_family: "geometric"              # geometric | letterform | abstract | pictogram
sizes: [16, 24, 32, 64, 128, 256, 512]
output_formats: ["svg", "png", "ico"]
constraints:
  touches_two_sides: true
  centered: true
  single_path: true
  no_stroke: true
  ink_coverage_pct: [25, 65]
notes: |
  Free-form notes from the user go here.
```

## How to auto-derive fields from a plain-language brief

Given: *"I want a logo for NovaSync, a cross-device file sync tool for developers. Clean and modern, indigo color."*

Derived:
- `product_name`: "NovaSync"
- `slug`: "novasync"
- `purpose`: "cross-device file sync tool"
- `audience`: ["developer"]
- `mood_keywords`: ["clean", "modern"]
- `preferred_color`: "#4F46E5" (indigo default)
- `metaphor_hints`: (inferred) sync arrows / orbits / letter N
- `composition`: "symbol_only"
