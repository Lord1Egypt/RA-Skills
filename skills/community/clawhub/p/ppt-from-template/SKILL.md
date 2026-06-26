---
name: ppt-from-template
description: >-
  Generate presentations by extracting visual style from a reference template and
  recreating slides from scratch using PptxGenJS. Use when: user provides a PPT/PDF
  as style reference and wants new slides in that style; user says "按这个风格做PPT",
  "模仿这个模板", "参考这个PDF做演示", "make slides like this", "use this template",
  "做个PPT", "用这个模板做课件", "帮我做演示文稿"; user uploads a .pptx file as template.
  Supports: template directory auto-discovery, user upload, multi-template selection,
  image/video placeholders, large decks (30-100+ pages via batched generation).
  Requires: pptx skill (PptxGenJS), python-pptx, pdftoppm (poppler-utils).
  NOT for: editing existing PPT (use pptx skill), creating slides without style reference
  (use pptx skill directly).
---

# PPT from Template

Generate presentations by extracting style from a reference template, then building fresh slides with PptxGenJS.

**Core principle:** Never modify existing PPT XML. Look at the style, then draw from scratch.

## Template Management

### Template Directory

Default template directory: `{workspaceDir}/template/`

On every invocation:

1. Scan `{workspaceDir}/template/` for `*.pptx` files.
2. If **one** template found → use it automatically.
3. If **multiple** templates found → list them and ask user to choose.
4. If **none** found → tell user to upload a `.pptx` file or provide a path.

### User Upload

Accept `.pptx` files uploaded by user. Before processing:

- **Size check**: reject files > 50 MB with message: "模板文件超过 50MB 限制，请压缩后重试"
- Save to `{workspaceDir}/template/` for reuse.

## Workflow

### Phase 1: Extract Style

```bash
# If .pptx, convert to PDF for visual analysis:
python3 {baseDir}/scripts/pptx_to_pdf.py template.pptx /tmp/ppt_style/template.pdf

# Extract page images:
bash {baseDir}/scripts/extract_pages.sh /tmp/ppt_style/template.pdf /tmp/ppt_style/ 150

# Precision extraction from PPTX XML:
python3 {baseDir}/scripts/extract_style.py template.pptx -o /tmp/ppt_style/style_raw.yaml
```

Read `style_raw.yaml` for exact data (hex colors, font names, font sizes in pt, positions in inches, fill types, line styles). Then read 3-5 page images for semantic understanding (element roles, layout classification).

Extract two levels:

| Level | Source | What to Capture |
|-------|--------|----------------|
| Global | style_raw.yaml | Colors (hex), typography (font/size/weight), decorations |
| Per-layout | style_raw.yaml + images | Element inventory: type, role, x/y/w/h, style properties |

Element types: `text`, `image`, `video`, `shape`, `line`, `numbered_list`, `step_list`, `tag_group`, `chart`, `table`.

For images/videos: set `placeholder: true` with `description` for user replacement.

Write results to `style.yaml`. Schema: [references/style-schema.md](references/style-schema.md).

### Phase 2: Generate PPT

Use the `pptx` skill (PptxGenJS) to create slides:

1. Read `style.yaml` for visual parameters.
2. Combine with user content (topic, page count, outline).
3. Generate PptxGenJS JavaScript applying extracted style.
4. Run JS to produce `.pptx`.
5. QA: convert to images, verify style fidelity.

### Large Deck Strategy (>15 pages)

PptxGenJS generation is fast (seconds), but **writing the JS code** for many slides can hit context/time limits. Mitigate:

| Pages | Strategy |
|-------|----------|
| ≤15 | Single generation pass |
| 16-30 | Split into 2 JS files: slides 1-15, slides 16-30. Generate sequentially, merge via `pptx-merge` or generate in one `pres` object across two code blocks |
| 31-100+ | Generate a **slide factory function** per layout type, then loop over a content array. One JS file, data-driven |

**Slide factory pattern** for large decks:

```javascript
// Define layout factories from style.yaml
function makeCover(pres, content) { /* ... */ }
function makeContent(pres, content) { /* ... */ }
function makeSection(pres, content) { /* ... */ }

// Content array — easy to extend
const slides = [
  { layout: "cover", title: "...", subtitle: "..." },
  { layout: "content", title: "...", items: [...] },
  // ... 50+ entries
];

slides.forEach(s => layoutFactories[s.layout](pres, s));
```

This keeps code size O(layouts) not O(pages).

### Output Size Control

Target output < 20 MB. PptxGenJS output is typically small (100-500 KB for text-only decks). Large files come from embedded images. If output approaches 20 MB:

1. Reduce image resolution/quality in PptxGenJS options.
2. Use placeholders instead of embedded images.
3. Split into multiple files if unavoidable.
4. Warn user: "PPT 接近 20MB 限制，已使用图片占位符，请手动替换"

### Placeholder Convention

- **Image**: Dark rectangle + dashed gray border + 🖼️ + label + suggestion
- **Video**: Dark rectangle + dashed red border + ▶️ + label + suggestion

### Key Rules

- Never modify existing PPT XML — always generate from scratch.
- `style.yaml` is reusable — once extracted, generate unlimited PPTs in the same style.
- Use `shrinkText: true` in PptxGenJS to auto-fit long text.
- Match slide dimensions exactly from `style_raw.yaml` (not hardcoded 16:9).

## File Convention

```
{workspaceDir}/
├── template/              ← .pptx templates (auto-discovered)
│   └── *.pptx             ← max 50 MB each
├── output/                ← generated PPTs
│   └── *.pptx             ← max 20 MB each
/tmp/ppt_style/            ← working directory (ephemeral)
├── template.pdf
├── page-*.jpg
├── style_raw.yaml         ← from extract_style.py
└── style.yaml             ← merged (exact + semantic)
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Template > 50 MB | Ask user to compress or remove embedded media |
| Output > 20 MB | Use placeholders, reduce image count/resolution |
| >30 pages timeout | Use slide factory pattern, data-driven generation |
| No template found | Prompt user to upload .pptx or specify path |
| Multiple templates | List options, ask user to choose |
| Fonts not available | Fall back to Arial/sans-serif; note in output |
| Complex gradients | Describe in style.yaml; use background image |
