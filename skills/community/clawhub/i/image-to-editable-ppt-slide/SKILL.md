---
name: image-to-editable-ppt-slide
description: Rebuild one or more reference images as visually matching editable PowerPoint slides using native shapes, text, fills, and layout instead of a flat screenshot. Use when the user wants an image, flowchart, infographic, dashboard, process diagram, or designed slide converted into an editable PPT/PPTX deck that stays editable and closely matches the source.
homepage: https://github.com/benjaminlee/image-to-editable-ppt-slide
metadata:
  clawdbot:
    emoji: "🖼️"
    requires:
      env: []
      files: ["scripts/*"]
---

# Image to Editable PPT Slide

Convert a reference image into a visually matching **editable** PowerPoint slide or deck.

## Use this skill when

- the user wants an image turned into an editable PPT/PPTX slide
- the source is a flowchart, infographic, dashboard, process diagram, or designed slide
- fidelity matters and the result should closely match the source
- the user wants multiple source images recreated as a multi-slide deck

## Core rules

- Rebuild the slide with editable text boxes, shapes, lines, fills, and layout
- Do **not** default to placing the whole image as a flat background unless the user explicitly asks for that
- Save both the generated `.pptx` and the script/spec used to create it
- Do at least one refinement pass when visual fidelity matters
- Commit updates in the workspace after edits

## Workflow

1. **Inspect the image(s)**
   - Identify aspect ratio, title, sections, cards, arrows, connectors, icons, labels, and palette
   - Note alignment, spacing, font weight, repeated motifs, and line thickness

2. **Choose structure**
   - Single image → one editable slide
   - Multiple images/pages → multi-slide deck, usually one source image per slide unless the user asks otherwise

3. **Build with editable primitives**
   - Use `python-pptx`
   - Prefer rectangles, rounded rectangles, chevrons, circles, arrows, lines, and text boxes
   - Approximate unknown fonts with standard installed fonts

4. **Use helpers**
   - `scripts/pptx_rebuilder.py` builds a deck from a JSON spec
   - `scripts/generate_spec_template.py` generates a starter JSON template for one or more slides

5. **Refine**
   - Tighten spacing, font sizes, colors, line widths, corner radii, and proportions
   - If needed, do a second pass before presenting the result

6. **Deliver**
   - Tell the user where the `.pptx`, generator script, and/or JSON spec were saved
   - Mention any approximations if the match is not exact

## File pattern

For one-off jobs, create:

- `make_<name>.py`
- `<Name>_editable.pptx`
- optional: `<name>_spec.json`

For repeated use, adapt the reusable scripts in `scripts/`.

## Multi-slide deck guidance

- Keep slide size consistent across the deck
- Usually map one reference image to one slide
- Reuse colors, text styles, and spacing where slides belong to the same presentation
- If slides differ a lot, treat each slide as its own reconstruction while keeping the deck coherent

## External Endpoints

This skill itself does not call any external APIs or web services.

| Endpoint | Purpose | Data sent |
|---|---|---|
| None | N/A | Nothing leaves the machine by default |

## Security & Privacy

- By default, this skill works locally with `python-pptx` and local files only
- It reads local image/reference material and writes local `.pptx`, `.json`, and helper script files
- It does **not** require credentials or network access for its built-in helpers
- If a future adaptation adds external APIs, document every endpoint and every environment variable before publishing

## Model Invocation Note

OpenClaw may invoke this skill autonomously when the request matches its description. That is normal skill behavior. If the user wants to avoid autonomous invocation, they can ask for a manual or one-off approach instead.

## Trust Statement

By using this skill, you are trusting the local helper scripts in this package to read local spec/input files and write local PowerPoint output files. This packaged version does not send data to third-party services. Only install it if you trust the skill contents and your execution environment.

## ClawHub-ready note

This skill folder is structured so it can be published with `clawhub publish` once authenticated. If publishing is requested, verify `clawhub whoami` first.

## Quality bar

Good:
- text and shapes are individually editable
- visual hierarchy matches the source at normal viewing size
- spacing, colors, and proportions are close enough to feel effectively identical

Bad:
- whole image pasted as one picture
- major layout drift or incorrect proportions
- unnecessary conversion of text into non-editable elements
