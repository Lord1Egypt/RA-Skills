# Configuration model

A preset composes five reusable profiles: theme, style, layers, composition, and unification. Project-specific choices belong in the manifest or preset overrides, never by editing a reusable profile.

## Complete workflow default

`presets/travel-food-journal.json` supplies every workflow and visual default that can be chosen generically. It becomes executable only after factual captions, source-specific page decisions, a configured font, and actual rendered plates with validated renderer receipts are supplied. The skill does not silently select or impersonate an image-generation backend. It defaults to:

- EXIF ascending order;
- mandatory production-plan Markdown;
- first EXIF page as the only pre-approval sample;
- plan decisions communicated either by sending the Markdown artifact or by a faithful summary, always discussed with the sample;
- explicit user approval before pages 2..N;
- the generated sample never serving as a style reference;
- no renderer backend selected by default and a validated receipt required for every rendered output;
- separate explicit consent before private references may be sent to an external image service;
- active-style plate normalization and validation;
- full-size and 360×640 phone review of every page;
- separate page-level compliance and set-level cohesion gates;
- typed page-local revision operations;
- hash-locked staging and verified ZIP packaging;
- watermark disabled until a project explicitly supplies and enables its own text;
- deterministic final outputs stripped of EXIF, GPS, and XMP metadata.

It also supplies the existing 9:16 food-journal visual profiles, captions, route, watermark, and export choices. These workflow defaults remove optional setup decisions, but **never authorize invention**: EXIF gaps, locations, caption facts, page subject priorities, identifying anchors, material/depth cues, structural lines, and forbidden inventions still require source evidence or user input.

Override reusable visual behavior with `overrides.<concern>`. Override workflow defaults in a copied project preset under `workflow_defaults`; do not put project-specific line or subject rules in the universal default.

## Style selection

`profiles.style` selects exactly one style profile. The bundled opt-in profiles `blue-lavender-watercolor` and `highway-485-lithograph` are independent initial references and are never blended implicitly. Each declares both reproducible `technique_roles` and `subject_exclusions`; only the former may influence rendering. The reusable preset continues to select `watercolor-journal` unless a copied project preset explicitly names another style.

## Rich per-page production brief

Every manifest item must contain:

```json
{
  "production_brief": {
    "subject_priority": "what must read first",
    "thumbnail_read": "what must remain legible at phone size",
    "preserve_anchors": ["identity-critical anchor"],
    "abstract_or_omit": ["detail to summarize or remove"],
    "material_depth_cues": ["glass transparency", "bird's-eye compression"],
    "structural_lines": [
      {"element": "major road direction", "operation": "retain_but_simplify"}
    ],
    "forbidden_inventions": ["transport lines not visible in the source"]
  }
}
```

`structural_lines[].operation` is `retain` or `retain_but_simplify`. These fields describe the source photograph, not the style-reference subject.

## Frozen sample style contract

The active style provides `sample_style_contract_defaults`; the manifest may override them for the project after discussion. All fields are mandatory:

- `mark_edge_quality`
- `negative_space_rules`
- `fill_tonal_rules`
- `background_cleanliness`
- `frame_border_policy`
- `abstraction_level`
- `generated_page_is_style_reference: false`

The contract flows into every page prompt and is hash-locked by the approval gate. The first generated page is approval evidence only.

## Plate normalization policy

Each style owns `plate_normalization` so cleanup does not damage incompatible media. Supported modes:

- `paper-key-soft`: remove a corner-sampled paper/background color with a feathered alpha transition while preserving darker or saturated marks.
- `alpha-required`: do not color-key; require a real alpha channel and validate it.
- `disabled`: no normalization; use only for an intentionally opaque style.

Thresholds are profile defaults and may be overridden per project through `overrides.style.plate_normalization`.

## Independence rule

- Theme owns subject extraction and prohibited inventions.
- Style owns mark/material behavior, reference technique roles, the sample style contract, and plate cleanup policy.
- Layers owns separation and deterministic/model-rendered responsibilities.
- Composition owns canvas, whitespace, placement, captions, and cross-slide rhythm.
- Unification owns shared paper and set-level normalization/QA thresholds.
