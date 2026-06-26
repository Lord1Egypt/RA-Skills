# Cartoon Storyboard Continuity Quality Overlay

Use this overlay whenever a visual step writes image-generation prompts in text or directly generates several continuous cartoon images.

## Core Rule

Treat each batch of cartoon images as one continuous short film, not as isolated posters. Every prompt batch must preserve:

- story order;
- camera logic;
- visual style;
- character and narrator identity;
- symbol and metaphor dictionary;
- evidence-label design;
- data-flow direction;
- title/page numbering format.

If previous storyboard images already exist, the next batch must explicitly continue from them. Reuse the same style bible unless the user asks for a style reset.

Each visual part should be decomposed into multiple images by default. Do not compress a whole section or several sections into one crowded infographic. A single image should carry one main teaching point; distinct ideas need distinct images.

## Prompt Block Required For Every Multi-Image Batch

Add a compact continuity block before the per-image prompts:

```text
Continuity / Cinematography Bible
- Aspect ratio: 16:9.
- Decomposition: multiple images for this section; one main teaching point per image; do not merge the whole section into one poster.
- Style: academic cartoon-comic infographic, same line weight, palette, typography, panel border, title/footer.
- Narrator/protagonist: same appearance, expression range, outfit, and role.
- Symbol bible: repeated variables, model blocks, data icons, metric badges, warning labels, and evidence labels.
- Camera grammar: establish -> process -> close-up -> synthesis, adapted to the paper logic.
- Transition logic: each image states what it inherits from the previous image and what it prepares for the next image.
- Consistency with prior batches: preserve earlier character, palette, visual metaphors, arrows, numbering, and paper-specific icons.
```

Then each image prompt should include:

- `Image N / section name`;
- `narrative role`: open / develop / turn / close / bridge;
- `teaching point`: the one idea assigned to this image;
- `do not merge`: which adjacent ideas are intentionally left to other images;
- `camera/framing`: wide, medium, close-up, top-down, split-screen, zoom-in, pan, cutaway, reveal, etc.;
- `content`: the exact scientific point to show;
- `continuity`: link to previous and next image;
- `evidence status`: paper-stated / reasonable inference / nearby-work inference / missing-not-reported;
- `text constraints`: short labels only, no dense paragraphs.

## Choosing Camera Language

Use camera language to improve understanding:

- wide establishing shot: why the problem matters, data ecosystem, old-method failure context;
- medium shot: interaction between data, module, and learner/narrator;
- close-up: equation, tensor shape, module IO, metric definition, confusing table cell, or key exception;
- top-down map: full pipeline, dependency graph, experiment protocol, or baseline family;
- split-screen: old vs new method, training vs inference, paper-stated vs inferred, success vs failure case;
- cutaway: hidden module internals, missing implementation detail, or limitation;
- reveal: paper's central idea after motivation has been built;
- bridge shot: end one section and prepare the next visual step.

Do not use camera movement as decoration. The framing must help the viewer answer: "what should I understand now that I could not understand before?"

## Expression Suitability

A good cartoon explanation should be technically faithful and visually teachable:

- one main idea per image;
- multiple images per section by default;
- no all-in-one dense collage for background + method + experiments + limitations;
- prerequisite first, conclusion later;
- stable left-to-right or top-to-bottom flow;
- repeated symbols for repeated concepts;
- labels short enough to read in a PDF slide;
- equations shown only when they serve the explanation;
- charts/tables simplified without changing the factual result;
- missing values shown as `not reported` / `未报告`;
- uncertainty and inference categories visually distinct;
- no unsupported performance, hardware, runtime, or baseline claims;
- consistent margins, safe area, page numbers, and title bands for later PDF assembly.

## Follow-Up Batch Rule

When generating later storyboard sections, first recover or restate:

- previous image count and section boundary;
- established narrator/protagonist;
- established color palette and typography;
- established recurring metaphors and icons;
- established data-flow direction and evidence-label style;
- the last image's ending state.

Then design the next batch as a continuation. Avoid sudden switches in art style, camera grammar, arrow direction, narrator design, or symbol meanings unless the user explicitly requests a reset.

## Compression Guardrail

If a prompt tries to include more than one major teaching point, split it. Examples that should be separated:

- problem motivation vs old-method defects;
- symbol definitions vs model data flow;
- module internals vs training objective;
- training walkthrough vs inference walkthrough;
- dataset setup vs metric definitions;
- main results vs exception cases;
- limitations vs reviewer-defense answers;
- future directions vs already-validated claims.

The final PDF becomes clear because each page has a job. Do not trade readability for fewer images.
