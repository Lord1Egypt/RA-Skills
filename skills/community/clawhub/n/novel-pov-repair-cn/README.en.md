# Narrative POV Diagnosis & Repair

Provide one fiction scene and its viewpoint character to receive pinpointed POV breaches, a reason for each breach, and minimal replacement passages that preserve the plot. This skill fixes concrete viewpoint jumps; it is not a general prose-polishing or AI-style-removal tool.

![Promo](assets/promo-1600x900.png)

## Install

```bash
npx skills add xxjrq/novel-pov-repair-cn
```

## Usage

```text
Use $novel-pov-repair-cn to check the supplied chapter, scene, or short passage. Viewpoint: Lin Lan, third-person limited. Identify breaches and make minimal repairs while preserving existing actions, dialogue, and character knowledge.
Text: paste the material to check.
```

## Input and output

Input one chapter, scene, or short passage plus the viewpoint character (ideally also person and limited-POV scope). Process one batch at a time; split tables above 100 rows.

The result identifies each passage, explains why its information exceeds the viewpoint boundary, and offers a plot-preserving rewrite. If the text or viewpoint character is missing, the skill lists what is needed instead of inventing context.

See copyable reference deliveries: [success](fixtures/success.md) and [missing-input](fixtures/failure.md).

Full execution outputs: [success](fixtures/forward-success.md) and [insufficient input](fixtures/forward-failure.md). Partial-input examples: [missing viewpoint only](fixtures/failure-missing-viewpoint.md) and [missing text only](fixtures/failure-missing-text.md). Repairs preserve existing actions, dialogue, and character knowledge; private thoughts never become new spoken dialogue.

## Self-test

```bash
node scripts/self-test.mjs
```

The test is self-contained: it validates local structure, metadata, icon dimensions, and fixture content without a network connection or sibling skills.

## Source and license

The public [story-skills scene-craft skill](https://github.com/danjdewhurst/story-skills/blob/main/skills/scene-craft/SKILL.md) informed the product category only. This repository's instructions, workflow, and examples are original and copy no external text or code. Licensed under [MIT-0](LICENSE).
