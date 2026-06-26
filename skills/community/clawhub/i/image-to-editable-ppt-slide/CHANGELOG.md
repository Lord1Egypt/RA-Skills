# Changelog

## 1.0.0

Initial public release of **Image to Editable PPT Slide**.

### Highlights

- Recreates reference images as **matching editable PowerPoint slides** instead of embedding the source as a flat screenshot
- Supports **single-slide** reconstructions and **multi-slide decks**
- Includes a reusable `python-pptx` builder for generating decks from JSON specs
- Includes a starter spec generator to speed up new slide reconstruction jobs
- Encourages a fidelity-first workflow with **inspection, rebuild, refinement, and delivery**

### Included files

- `SKILL.md` — main skill instructions and triggering guidance
- `EXAMPLES.md` — usage examples, spec examples, and command examples
- `PUBLISH.md` — ClawHub publication notes
- `scripts/pptx_rebuilder.py` — reusable JSON-to-PPTX deck builder
- `scripts/generate_spec_template.py` — starter JSON template generator

### Intended use

Use this skill when a user wants a flowchart, infographic, dashboard, process diagram, or designed slide rebuilt as a **visually matching, editable PPT/PPTX**.
