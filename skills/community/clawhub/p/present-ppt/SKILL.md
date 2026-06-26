---
name: present-ppt
description: Convert structured single-slide or small deck HTML files into editable PPTX slides with native text boxes, shapes, chips, arrows, and panels. Use when the user has an HTML slide/design draft and wants a high-fidelity editable PowerPoint instead of a screenshot-based export. Also use when the HTML does not fit an existing slide family and a new preset must be added before conversion. Especially useful for Gartner/analyst-style technical slides, architecture pages, AI runtime pages, and other fixed-layout HTML presentation pages.
---

# html-slide-to-pptx

Convert structured HTML slides into editable PPTX by parsing semantic blocks and mapping them to native PowerPoint objects.

This skill is preset-driven.
- Reuse an existing preset when the HTML belongs to a supported slide family.
- Add a new preset when the HTML belongs to a new slide family.
- Do not promise arbitrary HTML/CSS fidelity.

## First steps

1. Read the incoming HTML and identify the slide family.
2. Place the output PPTX in `./output/<name>.pptx` (create the directory if it doesn't exist).
2. If you are on a new machine, a fresh agent, or dependency state is unclear, read `references/setup.md` first.
3. Run `npm run check-env` before first use on a new environment.
4. If dependencies are missing, run `npm ci` or `npm install` in the skill directory.

## Workflow

1. Identify whether the HTML belongs to a supported preset.
2. Parse the HTML into a small intermediate model instead of trying to render arbitrary CSS.
3. Generate PPTX with native text/shapes using the bundled script.
4. Run a QA/preflight review on the generated result or the extracted model.
5. Open or preview the PPTX and inspect spacing, overflow, and arrow direction issues.
6. Iterate the preset mapping when fidelity is not good enough.

## Current support

### Preset: `v9-architecture`

Use for this exact or near-exact structure:
- Header eyebrow + brand
- Title
- Core summary box
- Left driver panel
- Center layered architecture stack
- Right judgement chain panel

### Preset: `ai-runtime-page`

Use for this exact or near-exact structure:
- Header eyebrow + brand
- Title + lead box
- Input chip row
- Main runtime box with 5 modules
- Support layer cards
- Output chip row
- Base layer + takeaway

## Commands

### Verify environment

```bash
npm run check-env
```

### Convert HTML to PPTX

```bash
# Output is saved to ./output/<name>.pptx by default
node scripts/html_to_pptx.js <input.html> ./output/<name>.pptx [--preset=v9-architecture|ai-runtime-page] [--dump-model <file.json>]
```

### Run preflight QA

```bash
node scripts/preflight_qa.js <model.json> [--preset=v9-architecture|ai-runtime-page] [--report <report.json>]
```

## When no preset fits

Do not hard-convert arbitrary HTML.

If the HTML structure is meaningfully different from existing presets, add a new preset by implementing all three layers:

1. DOM extraction rules
2. Layout/render mapping rules
3. QA/preflight rules

Reuse existing presets only when the page family is genuinely close.
If the structure differs in information architecture, add a new preset instead of overloading an old one.

## Rules

- Prefer semantic mapping over screenshot embedding.
- Preserve editability first, then iterate toward fidelity.
- Treat browser rendering as reference, not as the generation engine.
- Run QA for every generated result.
- If setup or portability is the issue, read `references/setup.md`.
- If extending support, read `references/preset-decision-rules.md` first, then `references/presets.md`, `references/preset-template.md`, and `references/qa-heuristics.md`.

## References

- Read `references/setup.md` when installing or using the skill on a new machine/agent.
- Read `references/preset-decision-rules.md` when deciding whether to reuse, extend, or replace a preset.
- Read `references/presets.md` when extending to new slide families.
- Read `references/preset-template.md` when creating a brand-new preset.
- Read `references/qa-heuristics.md` when designing or tuning preflight checks.
- Read `references/roadmap.md` when planning higher-fidelity HTML measurement or hybrid background/text-layer approaches.
- Read `references/usage-principles.md` for the full 5-rule usage guide.
- Read `README.md` for a human-friendly overview, setup summary, and portability notes.
