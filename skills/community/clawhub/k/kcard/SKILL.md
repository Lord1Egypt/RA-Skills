---
name: kcard
description: Knowledge Card generator. Extracts key knowledge from user-provided material (text, files, URLs), determines optimal card type (concept/memo/process/comparison), applies cognitive science principles (chunking, dual coding, elaboration), outputs structured Markdown, and renders it into a beautiful image. Use when user says "知识卡片", "kcard", "make a card", "knowledge card", or wants to turn notes/articles into memorable visual cards.
---

# Knowledge Card Generator

## Workflow

### 1. Parse Input Material

Accept any of: pasted text, file path, URL, or image.

- If URL → fetch and extract main content by `web_fetch` tool
- If file → read it

Extract 3–7 core knowledge points. Prioritize: definitions > mechanisms > examples > details.

### 2. Determine Card Type

Pick the **best-fit** type based on content nature:

| Type | Trigger Pattern | Structure |
|------|----------------|-----------|
| **Concept** | Defines a term, theory, model | Term → Definition → Analogy → Key Points |
| **Memo** | Steps, commands, configs, references | Title → Ordered Steps → Tips / Gotchas |
| **Process** | Sequential workflow or lifecycle | Title → Phases → Steps per Phase → Output |
| **Comparison** | Compares 2+ items | Dimension → Item A vs Item B → Verdict |

If unsure, default to **Concept card**.

### 3. Apply Cognitive Science Principles

Follow these when structuring the card:

- **Chunking**: Group related info into 3–5 chunks max per section
- **Dual Coding**: Pair text with a visual metaphor or emoji anchors
- **Elaboration**: Add a "Why It Matters" or analogy section
- **Spaced Repetition Cue**: End with a self-test question (❓)
- **Progressive Disclosure**: Layer from simple to detailed

### 4. Generate Markdown

Use the template from `references/card-templates.md`. Output a single Markdown file.

Naming convention: `kcard_<topic>_<type>.md` (e.g., `kcard_react-hooks_concept.md`)

Save to user's specified path or default: `~/.openclaw/workspace/kcards/`

### 5. Render to Image

Run the rendering script to convert the Markdown into a PNG:

```bash
python <skill-dir>/scripts/render_card.py <path-to-markdown> [--output <output.png>] [--theme <warm|cool|girly|tech>] [--width 800]
```

Default theme: `warm`. Default output: same path with `.png` extension.

The script:
1. Parses Markdown to styled HTML
2. Renders HTML to image via headless browser or html2image
3. Returns the output path

Present the final image to the user.

## Output Format

Always output:
1. The Markdown source file (for editing/reuse)
2. The rendered PNG image
3. A brief one-line summary of what the card covers

## Notes

- Keep cards concise: one concept per card, maximum 195 words
- Use Chinese or English based on input language
- Emoji anchors are encouraged but keep them minimal (1–3 per section)
- For batch requests, process cards sequentially and summarize all outputs
