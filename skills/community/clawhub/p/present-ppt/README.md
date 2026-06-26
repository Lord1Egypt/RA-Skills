# present-ppt

> **present-ppt** is forked & enhanced from [html-slide-to-pptx](https://github.com/mucsbr/ppt-agent-workflow-san/tree/main/html-slide-to-pptx).
>
> This is one of the skills in [mk-present](https://github.com/textboy/mk-present).

Convert structured HTML slides into editable PowerPoint (.pptx) slides with native text boxes, shapes, chips, arrows, and panels.

This is a preset-driven converter, not a generic browser renderer.

- If the HTML matches an existing preset, convert it directly.
- If the HTML belongs to a new slide family, add a new preset first, then convert.

## What this skill is good at

- Analyst-style fixed-layout slides
- Architecture pages
- AI runtime / process pages
- Small decks or single-slide HTML designs where editability matters more than arbitrary CSS fidelity

## What this skill is not

- A universal HTML/CSS-to-PPT engine
- A screenshot exporter
- A responsive web page converter

## Current preset support

### `v9-architecture`

Use for a structure close to:
- Header eyebrow + brand
- Title
- Core summary box
- Left driver panel
- Center layered architecture stack
- Right judgement chain panel

### `ai-runtime-page`

Use for a structure close to:
- Header eyebrow + brand
- Title + lead box
- Input chip row
- Main runtime box with 5 modules
- Support layer cards
- Output chip row
- Base layer + takeaway

## Environment requirements

- Node.js installed
- npm available
- Local dependencies installed from `package.json`

Recommended:
- Node.js 18+

This skill does **not** require Python, Chrome, Playwright, or LibreOffice for its core conversion flow.

## Install on a new machine or another agent

```bash
cd <skill-dir>
npm ci
npm run check-env
```

If `npm ci` is unavailable or fails because the lockfile is missing/outdated:

```bash
npm install
npm run check-env
```

Detailed setup notes: see `references/setup.md`.

## Quick start

### 1) Verify environment

```bash
npm run check-env
```

### 2) Convert HTML to PPTX

```bash
node scripts/html_to_pptx.js input.html output.pptx --preset=v9-architecture --dump-model model.json
```

or:

```bash
node scripts/html_to_pptx.js input.html output.pptx --preset=ai-runtime-page --dump-model model.json
```

### 3) Run QA / preflight

```bash
node scripts/preflight_qa.js model.json --preset=v9-architecture --report qa.json
```

## Standard workflow

1. Identify the slide family.
2. Read `references/preset-decision-rules.md` and decide whether to reuse, extend, or replace a preset.
3. If no preset fits, add a new preset instead of hard-converting arbitrary HTML.
4. Convert HTML into PPTX and optionally dump the intermediate model.
5. Run QA/preflight checks.
6. Open the PPTX and visually inspect spacing, overflow, and arrow direction.
7. Iterate the preset mapping if needed.

## How to extend to a new slide family

When the incoming HTML does not fit an existing preset, add support in three layers:

1. **DOM extraction rules**
   - Extract semantic content from HTML into a small model.
2. **Layout/render mapping**
   - Map the model into native PowerPoint objects.
3. **QA rules**
   - Add preset-specific overflow and spacing checks.

Useful files:
- `references/preset-decision-rules.md`
- `references/presets.md`
- `references/preset-template.md`
- `references/qa-heuristics.md`
- `references/roadmap.md`
- `references/usage-principles.md`

## Main files

- `SKILL.md` — agent-facing instructions and trigger description
- `scripts/html_to_pptx.js` — main conversion entry point
- `scripts/preflight_qa.js` — preflight QA runner
- `scripts/check_env.js` — environment self-check
- `scripts/html_to_pptx_v9.js` — v9 preset renderer
- `scripts/ai_runtime_preset.js` — AI runtime preset extractor/renderer

## Troubleshooting

### `Cannot find module 'cheerio'` or `Cannot find module 'pptxgenjs'`

Run:

```bash
npm ci
```

or:

```bash
npm install
```

### Conversion works on one machine but not another

- Reinstall dependencies on the target machine.
- Do not assume copied `node_modules/` is portable across environments.
- Run `npm run check-env` again.

### HTML is structurally different from existing presets

Do not force it through an old preset. Add a new preset.

## Portability note

Another agent can usually understand and use this skill **if**:
- the skill folder is installed in a visible skill directory,
- `SKILL.md` is present,
- dependencies are installed,
- and the agent follows the preset-driven workflow.

For best portability, distribute the whole skill folder including:
- `SKILL.md`
- `package.json`
- `package-lock.json`
- `scripts/`
- `references/`

`node_modules/` may help for local reuse, but should not be relied on as the only installation method.
