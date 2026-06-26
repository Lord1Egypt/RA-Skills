# Visual Style And Board Protocol

## Core Rule

If the skill presents multiple subtypes, schemes, layouts, styles, metaphors, density levels, or prompt alternatives, it must move through:

1. `TEXT_ONLY`: present text options and recommend visual comparison.
2. `TEXT_ONLY`: set up a visual candidate board.
3. `IMAGE_ONLY`: generate/display 4-6 candidate images or schematic candidates, normally 6.
4. `TEXT_ONLY`: record the image batch and ask the user to select, revise, combine, or request another board.

## Candidate Board Setup

The P4 setup turn must state:

- board type: subtype, scheme, layout, style, metaphor, density, prompt, or final candidate;
- candidate count: 4, 5, or 6, default 6;
- varied axis: exactly what differs across candidates;
- fixed elements: paper thesis, target slot, required case evidence, exact labels, color semantics, and sample-image transfer rules;
- rendering route: ChatGPT web Create image / ChatGPT Images 2.0; Codex `$imagegen` first; approved API fallback only if unavailable;
- comparison criteria: what the user should choose by looking at the images.

The setup turn is `TEXT_ONLY` and stops before generation.

## Image-Only Board Generation

The P5 generation turn must be `IMAGE_ONLY`:

- no prose;
- no state footer;
- no captions or analysis;
- 4-6 candidates, normally 6;
- native image generation only.

Allowed route: ChatGPT web Create image through ChatGPT Images 2.0, or Codex `$imagegen` first. If `$imagegen` is unavailable, use ChatGPT Images 2.0 API or another approved image-generation API.

Forbidden: SVG, Mermaid, TikZ, Graphviz, HTML/CSS, canvas, matplotlib, filesystem code drawing, or code-rendered/exported images.

## Style Families For Inspiration Figures

- Clean editorial flat
- Formal scientific schematic
- Storyboard panels
- Split-screen contrast
- Mechanism snapshot
- Mini evidence infographic
- Design-space map
- Premium scientific illustration
- Dashboard/interface metaphor
- Minimal line-art schematic
- Isometric / soft 3D only when spatial or system context matters

## Candidate Review Turn

The next text turn after P5 must:

1. record the image batch as a produced output;
2. summarize candidate IDs or positions;
3. recommend the strongest candidate and why;
4. identify risks/edits;
5. ask the user to select, revise, combine, or request another board;
6. update state fields;
7. end with standard next prompts.

## Required State Fields

```yaml
visual_candidate_board_status: not_started | setup_ready | confirmed | generated | reviewed | skipped_by_user
visual_board_type: subtype | scheme | layout | style | metaphor | density | prompt | final_candidate
visual_board_candidate_count: 6
visual_board_axis_varied: ""
visual_board_fixed_elements: []
candidate_image_batch_id: ""
visual_candidate_history: []
selected_visual_candidate: null
visual_candidate_board_skipped_by_user: false
```
