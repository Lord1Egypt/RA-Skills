---
name: paper-highlight
description: "Automatically highlight academic papers by 5 semantic categories — goal, motivation, method, results, contributions — to help you quickly skim a paper. Configurable density levels, opacity, and optional note layers."
metadata: '{"openclaw":{"emoji":"🖍️","requires":{"bins":["python3","uv"]},"install":[{"id":"brew","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv (brew)"}]}}'
---

# Paper Highlight

Use this skill as a paper-reading workflow: understand first, then mark reusable information with stable semantics. Tune density with the highlight level, but keep each color meaning consistent.

## Setup

This skill needs a one-time setup after installation. Prefer `uv` so the dependency stays isolated and reproducible:

```bash
cd /Users/yo/.codex/skills/paper-highlight
uv venv .venv
source .venv/bin/activate
uv pip install pymupdf
```

If the environment already exists, refresh it with:

```bash
cd /Users/yo/.codex/skills/paper-highlight
source .venv/bin/activate
uv pip install --upgrade pymupdf
```

## Workflow

1. Read [`references/highlight-rules.md`](references/highlight-rules.md) before annotating.
2. Do a preflight inspection before any model-heavy reading. Surface the PDF page count, extracted text volume, rough word count, and a rough token estimate to the user.
3. Explicitly warn that full-paper pre-reading can consume a large number of tokens, especially on long PDFs or dense two-column papers. Do not continue until the user clearly agrees.
4. Inspect the PDF structure once the user agrees. Prefer abstract, introduction, method overview, main results, and conclusion before touching fine details.
5. Build a mental highlight plan across the core reading chain: goal -> motivation -> method -> results. Add contribution, setup, or limitation colors only when they are independently reusable.
6. Run the bundled PyMuPDF script to annotate the PDF with semantic colors. Use `light` opacity by default; it now uses soft pastel colors at `0.5` opacity so the marks stay visible without fully covering the text. Switch to `dark` only when the source PDF is faint or image-heavy.
7. Add the optional explanation layer when needed: a paper-level `TLDR` paragraph and concise section `flow` summaries. Do not quote the original paper text inside notes; rewrite it as clear, compact summaries.
8. Review the output and remove noisy marks if the page looks busy. Prefer under-highlighting over over-highlighting.

## Preflight Gate

Before executing the full highlighting workflow, report at least:

- page count
- extracted character count
- extracted word count
- rough token estimate

Use those numbers to tell the user that the paper may be expensive to process. If the user does not explicitly confirm, stop after the inspection step.

## Selection Rules

- Highlight only sentences that remain useful when revisiting the paper later for writing, reviewing, rebuttal, or method comparison.
- Favor self-contained sentences that summarize a paragraph, state a claim, define a setup, or express a takeaway.
- Skip transitions, generic field background, implementation trivia, decorative prose, and sentences that only feel important in the moment.
- Keep one semantic meaning per color. Do not reuse a color for a neighboring but different category.
- Stay useful even at higher density. Use the level presets to control how aggressive the pass should be, then trim obvious noise if a page becomes crowded.

## Highlight Levels

Use `--highlight-level` to control annotation density:

- `low`: fixed baseline
- `medium`: target about `1.25x` the `low` count
- `high`: target about `1.5x` the `low` count
- `extreme`: target up to `2x` the `low` count

Manual flags such as `--max-per-page`, `--max-total`, and `--min-score` still override the level preset when needed.

## Note Modes

Use `--note-mode` to control the explanation layer:

- `default`: add a title `TLDR` paragraph and concise section `flow` summaries
- `none`: disable all note annotations

## Color Policy

Use the required 5-color core by default:

- Yellow: research goal or problem definition
- Orange: motivation, gap, challenge, or prior limitation
- Blue: main method or core mechanism
- Pink: contributions or novelty claims
- Green: main results or conclusions

Enable optional colors only when they clearly add value:

- Purple: definitions, assumptions, notation, or evaluation setup
- Gray: limitations, caveats, failure cases, or future work

## Commands

Set up the local environment:

```bash
cd /Users/yo/.codex/skills/paper-highlight
uv venv .venv
source .venv/bin/activate
uv pip install pymupdf
```

Run the highlighter:

```bash
cd /Users/yo/.codex/skills/paper-highlight
source .venv/bin/activate
python3 scripts/highlight_paper.py input.pdf
python3 scripts/highlight_paper.py input.pdf --highlight-level medium
python3 scripts/highlight_paper.py input.pdf --highlight-level high --include-optional
python3 scripts/highlight_paper.py input.pdf --note-mode flow
python3 scripts/highlight_paper.py input.pdf --note-mode hightlight
python3 scripts/highlight_paper.py input.pdf --note-mode full
python3 scripts/highlight_paper.py input.pdf --highlight-level exteme --opacity dark
python3 scripts/highlight_paper.py input.pdf --disable-optional definitions
```

Ask the script for its exact CLI when needed:

```bash
cd /Users/yo/.codex/skills/paper-highlight
source .venv/bin/activate
python3 scripts/highlight_paper.py --help
```

## Resources

- [`references/highlight-rules.md`](references/highlight-rules.md): color legend, density targets, and sentence-level filters
- `scripts/highlight_paper.py`: bundled PyMuPDF annotator for the final PDF pass
