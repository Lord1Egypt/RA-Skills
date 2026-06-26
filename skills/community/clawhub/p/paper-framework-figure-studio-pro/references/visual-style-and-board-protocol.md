# Visual Style and Candidate-Board Protocol

Version: 1.2.0

The visual candidate board is mandatory after multi-option text decisions. It is a selection aid, not the final figure.

## Board Setup

In P4, state:

- board type: subtype / scheme / layout / style / metaphor / density / prompt;
- candidate count: 4, 5, or 6, default 6;
- varied axis: exactly what differs;
- fixed elements: paper thesis, target slot, required modules, labels, color semantics, sample-image transfer rules;
- rendering route: ChatGPT web Create image / ChatGPT Images 2.0; Codex `$imagegen` first; fallback ChatGPT Images 2.0 API or approved image API;
- comparison criteria: what the user should choose by looking at the images.

Then stop. P4 is text-only.

## Board Generation

P5 is `IMAGE_ONLY`:

- generate/display 4-6 candidate images or schematic candidates, normally 6;
- no prose or state footer;
- no caption or critique.

## Board Review

P6 is text-only and must:

1. record `candidate_image_batch_id`;
2. compare candidates;
3. recommend one direction;
4. identify risks and fixes;
5. ask the user to select, revise, combine, or request another board.

## Style Families

Use 4-6 style choices when style is live, normally 6:

- clean editorial flat;
- formal architecture schematic;
- mechanism snapshot;
- premium scientific illustration;
- isometric / soft 3D;
- storyboard panels;
- tile/card/mosaic board;
- blueprint / technical drawing;
- minimal line-art schematic;
- dashboard metaphor.

If style choices are visibly different, proceed through P4/P5/P6 rather than locking style from prose alone.
