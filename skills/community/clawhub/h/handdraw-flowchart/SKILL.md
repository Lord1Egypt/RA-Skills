---
name: handdraw-flowchart
version: 0.1.0
description: Create hand-drawn workflow diagrams from natural-language process descriptions by generating strictly validated Mermaid flowchart, sequenceDiagram, or classDiagram code, converting Mermaid to Excalidraw scene files, and exporting PNGs. Use when Codex needs sketch-style process diagrams, Mermaid-to-Excalidraw conversion, validated Mermaid diagram generation, or PNG exports from process descriptions.
metadata:
  openclaw:
    homepage: https://github.com/zengiai/handdraw-flowchart
    requires:
      bins:
        - node
        - npm
---

# Handdraw Flowchart

## Workflow

1. Convert the user's natural-language process into one supported Mermaid diagram:
   - `flowchart TD` or `flowchart LR` for business processes, decision trees, and state transitions.
   - `sequenceDiagram` for actor/system interactions over time.
   - `classDiagram` for domain objects, DTOs, entities, interfaces, and relationships.
2. Generate raw Mermaid only. Do not wrap it in Markdown fences when writing `.mmd` files.
3. Read `references/mermaid-generation-rules.md` before producing non-trivial Mermaid, especially for sequence or class diagrams.
4. Save the Mermaid source as `<name>.mmd`.
5. Run the renderer script. It performs strict Mermaid parsing before conversion:

   ```bash
   cd <skill-directory>
   npm install
   node scripts/render-mermaid-handdraw.mjs --input /path/to/<name>.mmd --out-dir /path/to/output --name <name>
   ```

The script writes:

- `<name>.mmd`: normalized Mermaid source
- `<name>.excalidraw`: editable Excalidraw scene
- `<name>.png`: rendered PNG

## Conversion Contract

- Treat `flowchart` as the primary hand-drawn path. It converts to native Excalidraw elements and gives the best editable sketch-style result.
- Treat `sequenceDiagram` as supported but still verify output visually when the diagram is complex.
- Treat `classDiagram` as supported with possible image fallback inside the Excalidraw scene. If the script reports `image-fallback`, the PNG is valid, but editability is limited.
- Reject unsupported Mermaid diagram types instead of silently producing a lower-quality result.
- Do not claim success until the renderer has completed without validation or export errors.

## Strict Validation Rules

- Run `node scripts/render-mermaid-handdraw.mjs --input <file> --validate-only` after generating Mermaid if you need a fast syntax gate.
- If validation fails, edit the Mermaid source and rerun. Do not bypass validation.
- Prefer simple Mermaid syntax over clever syntax. Avoid custom CSS, HTML labels, Markdown tables inside labels, YAML frontmatter, and experimental Mermaid shape declarations.
- Keep node IDs stable and ASCII where practical. Put user-facing Chinese text in labels, not IDs.

## Rendering Notes

- The script uses browser execution because Excalidraw export utilities require DOM/canvas APIs.
- If Playwright has no bundled browser, the script tries common local Chrome/Chromium executable paths and honors `CHROME_PATH`.
- For reproducible results, keep the versions pinned in `package.json` unless there is a specific reason to upgrade and retest the renderer.
