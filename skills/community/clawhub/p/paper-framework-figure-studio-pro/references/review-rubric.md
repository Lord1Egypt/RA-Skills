# Review Rubric

Version: 1.2.0

Check generated framework diagrams against:

- thesis clarity: can a reader understand the main point in 10 seconds?
- multi-label fit: were all applicable diagram labels considered before selecting the primary subtype?
- subtype fit: does the layout match the intended primary diagram role?
- paper fidelity: no invented modules, labels, metrics, or claims;
- hierarchy: proposed contribution is visually dominant;
- reading path: arrows and panels have a clear order;
- label quality: short, readable, and exact;
- density: enough detail for the paper slot without clutter;
- sample-image transfer: borrowed only requested attributes from each sample image;
- candidate-image bridge: text candidates were followed by P4 setup, P5 image-only candidate board, and P6 candidate review before final prompt;
- rendering route: ChatGPT web used Create image / ChatGPT Images 2.0; Codex used `$imagegen` first or an approved API fallback;
- rendering safety: no watermark, fake UI, malformed text, or decorative clutter;
- response boundary: first trigger did not generate images, text turns did not append image generation, and IMAGE_ONLY turns had no prose/state;
- state footer: every text turn listed all steps, current position, current artifacts, pending artifacts, and next prompts.

## Revision Routes

- If structure is wrong: revise layout skeleton before style.
- If text is wrong: reduce labels and specify exact text.
- If novelty is buried: increase contrast and visual weight on the proposed component.
- If too decorative: switch to formal architecture schematic or minimal line-art.
- If too sparse: add evidence cards or callouts, but only from provided paper material.
- If no candidate-board step occurred after text candidates: return to P4 and set up the board before final prompt/final generation.
