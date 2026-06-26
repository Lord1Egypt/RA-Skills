# One Person Company OS

[English](./README.md) | [简体中文](./README.zh-CN.md)

**A visual operating cockpit for AI-native solo founders.**

One Person Company OS helps one founder turn an AI product idea into a company that can be inspected, advanced, and handed off between sessions. It keeps the business loop visible:

`promise -> buyer -> product capability -> delivery -> cash -> learning -> asset`

The first workspace is built around the questions a solo founder actually needs to answer today:

- What promise can I sell?
- Who is the first buyer?
- What is the current bottleneck?
- Which arena needs the next push: sales, product, delivery, cash, or assets?
- What is the shortest action I can take today?
- Which files were actually saved inside my approved workspace?

## What You Get

- a local operating cockpit you can open after download
- editable markdown work surfaces for the founder and role agents
- numbered DOCX deliverables for formal handoff
- deterministic SVG visuals for the business loop and revenue pipeline
- role briefs, reminders, flow notes, and starter deliverables aligned to the same operating loop
- optional AI-image prompts for covers, launch posts, and promotion

## Workspace Model

Generated workspaces use three output layers:

- **HTML reading layer** for first-pass review and navigation
- **Markdown work layer** for ongoing editing and agent collaboration
- **DOCX deliverable layer** for formal outputs under `artifacts/` or `产物/`

Chinese founders get:

- `阅读版/00-经营驾驶舱.html`
- `视觉素材/business-loop.svg`
- `视觉素材/revenue-pipeline.svg`
- `视觉素材/ai-image-prompts.md`

English founders get:

- `reading/00-operating-cockpit.html`
- `visual-kit/business-loop.svg`
- `visual-kit/revenue-pipeline.svg`
- `visual-kit/ai-image-prompts.md`

The hidden machine state stays at `.opcos/state/current-state.json`.

## Safety Boundary

- script mode expects an existing local `Python 3.7+`
- `scripts/ensure_python_runtime.py` prints compatibility and manual install guidance only
- the marketplace build does not auto-install system packages
- generated files stay inside the founder-approved workspace directory
- normal use does not require API keys or unrelated credentials
- AI images are optional creative assets, not a required runtime dependency

## Local Commands

```bash
python3 scripts/preflight_check.py --mode create-company
python3 scripts/ensure_python_runtime.py
python3 scripts/init_business.py "North Star Lab" --path ./workspace --product-name "North Star Assistant" --target-user "independent builders" --core-problem "they need one visible loop for product, revenue, delivery, and cash" --product-pitch "a visual operating cockpit for one-person AI companies" --language en-US --confirmed
python3 scripts/validate_release.py
```

## One-Line Install

```bash
clawhub install one-person-company-os
```

## One-Line Start

```text
I am building a one-person AI company. Use one-person-company-os v1.0. First help me confirm the sellable promise, first buyer, and core problem. Then create the approved local workspace, open with the operating cockpit, show the current bottleneck visually, and save only approved files inside that workspace.
```

## Validation

```bash
python3 scripts/validate_release.py
```

It validates the state model, localized workspaces, operating cockpit, visual assets, DOCX-only artifact directories, role/template language, and public release materials.
