# Usage Principles (5 Rules)

1. **First identify the page family, then decide whether to convert directly.** This is not a universal HTML converter; first check whether it belongs to a supported page family (currently primarily `v9-architecture` and `ai-runtime-page`).

2. **For new structures without a preset, add the preset first, then run generation.** If the HTML's information architecture, module distribution, card/chip/judgement-chain structure differs from existing presets, do not force conversion. First add DOM extraction rules, layout mapping rules, and QA rules.

3. **Prioritize "editable + stable", do not pursue 100% pixel-perfect reproduction like a screenshot.** This skill's goal is to turn presentation-style HTML into editable PPTs, not to replicate browser-level rendering.

4. **Generation is not the end — QA must be run.** Every output should go through at least one preflight check, focusing on text overflow, title/subtitle collision, chip/card clipping, stacking pressure, and insufficient spacing.

5. **Reuse when possible, extend when necessary.** When encountering a new page, first use `references/preset-decision-rules.md` to determine whether it can be handled as a variant of an existing preset. Only create a new preset when the page family is genuinely different, to avoid turning the skill into a collection of one-off special cases.
