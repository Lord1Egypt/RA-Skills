---
name: guizang-html-to-pptx
description: Convert a guizang-ppt-skill magazine HTML deck into a real editable PowerPoint PPTX. Use this skill whenever the user asks to export, convert, or rebuild a guizang/magazine-web-ppt HTML deck, index.html, web PPT, slides, or presentation as .pptx, especially when they say "editable PPTX", "not screenshots", "不要截图", or need PowerPoint-native text, shapes, and images. If the user explicitly selects or mentions this skill with little or no extra instruction, default to exporting the current guizang HTML PPT as a real editable PPTX, not screenshots, with fonts matching the HTML. This is an export-only companion skill for guizang-ppt-skill, originally from https://github.com/op7418/guizang-ppt-skill; it should not replace the original HTML deck generation skill.
---

# Guizang HTML To PPTX

## Source And Scope

This skill is an **export-only companion** for the original guizang PPT skill:

- Original guizang PPT skill: https://github.com/op7418/guizang-ppt-skill
- This skill's job: take an existing guizang HTML deck and rebuild it as a real editable PPTX

Do not treat this skill as a replacement for `guizang-ppt-skill`. It does not create the magazine-style HTML deck from scratch; it starts after the HTML deck already exists.

## What This Skill Does

Turn a `guizang-ppt-skill` HTML deck into a **real editable PPTX**.

The key idea: use the HTML deck as the visual and content reference, then rebuild the deck with PowerPoint-native objects:

- Text boxes for titles, body, captions, footers, and metadata
- Shapes for backgrounds, rules, callouts, stat cards, and layout structure
- Image objects for files from `ppt/images/` or `media/`
- Matching fonts and colors from the HTML theme

Do **not** solve this by putting one screenshot per slide into PowerPoint. That produces a PPTX file, but not an editable deck.

## Default Invocation

If the user explicitly selects this skill or writes only something like:

```text
[$guizang-html-to-pptx]
```

and does not provide more details, treat the request as:

```text
把当前 guizang HTML PPT 导出为真正可编辑 PPTX，不要截图，字体和 HTML 保持一致。
```

Use the current working directory as the project root. Look first for `ppt/index.html`, then for `index.html`. If neither exists, search for a likely guizang HTML deck and proceed with the best match; ask only if multiple plausible decks exist and choosing one would be risky.

## When To Use

Use this skill when the user has a guizang/magazine-style HTML deck and asks for:

- "导出为 PPTX"
- "不要截图，我要真的 PPTX"
- "editable PPTX"
- "PowerPoint 可编辑版本"
- "把当前 HTML 格式 PPT 转成 pptx"
- "HTML 和 PPTX 字体保持一致"

If the user explicitly asks for screenshot slides, follow that request. Otherwise, default to editable rebuild.

## Inputs And Expected Output

Typical input:

```text
project/
└── ppt/
    ├── index.html
    └── images/
```

Expected output:

```text
project/
└── ppt/
    ├── deck-name.pptx
    ├── export_editable_pptx.py or export_editable_pptx.js
    └── pptx-qa/
        ├── deck-name.pdf
        ├── slide-01.png
        └── contact-sheet.png
```

## Tool Choice

Prefer the repo's existing tooling if present. If there is already an `export_editable_pptx.py` or similar export script, inspect and improve it instead of starting over.

If creating the exporter from scratch:

- Use `pptxgenjs` when the project already has Node dependencies for it.
- Use `python-pptx` when Python is the simpler available path.
- Use Pillow/PIL for image dimensions and contain/cover calculations.
- Use LibreOffice `soffice` plus `pdftoppm` for visual QA when available.

Do not use browser screenshots as slide backgrounds unless the user explicitly accepts a non-editable screenshot deck.

## Workflow

### 1. Locate And Inspect The HTML Deck

Find the deck root and confirm the page count.

Useful commands:

```bash
rg -n '<section class="slide|class="slide' ppt/index.html
rg -n 'font-family|--serif|--sans|--mono|--ink|--paper' ppt/index.html
rg -n 'images/|media/' ppt/index.html
```

Read the actual slide sections, not just the CSS. Capture:

- Slide count and order
- Each slide's theme: `dark`, `light`, `hero dark`, `hero light`
- Titles, body copy, callouts, stats, captions, footers
- Image filenames and intended placement
- Theme colors and font variables

Keep the HTML deck as the source of truth. Do not freely rewrite the narrative while exporting.

### 2. Preserve Guizang Typography

Match the HTML font stack in the PPTX. The default guizang typography is:

| HTML role | PPTX role | Font |
|---|---|---|
| `--serif-zh` | Chinese titles, lead copy, callouts | `Noto Serif SC` |
| `--sans-zh` | Chinese body, step titles, notes | `Noto Sans SC` |
| `--serif-en` | English display text, large numbers, step numbers | `Playfair Display` |
| `--mono` | metadata, page labels, code, captions | `IBM Plex Mono` |

For `python-pptx`, setting `run.font.name` alone may only affect Latin text. Also set DrawingML Latin, East Asian, and complex script typefaces.

```python
from pptx.oxml.ns import qn
from pptx.oxml.xmlchemy import OxmlElement

def set_run_font(run, font_name):
    if isinstance(font_name, tuple):
        latin_font, east_asian_font = font_name
    else:
        latin_font = east_asian_font = font_name

    run.font.name = latin_font
    rpr = run._r.get_or_add_rPr()
    for tag, typeface in (
        ("a:latin", latin_font),
        ("a:ea", east_asian_font),
        ("a:cs", latin_font),
    ):
        node = rpr.find(qn(tag))
        if node is None:
            node = OxmlElement(tag)
            rpr.append(node)
        node.set("typeface", typeface)
```

Use tuple fonts for mixed roles:

```python
SERIF = "Noto Serif SC"
SANS = "Noto Sans SC"
SERIF_EN = ("Playfair Display", SERIF)
MONO = ("IBM Plex Mono", SANS)
```

### 3. Rebuild Slides As Native Objects

Use a 16:9 wide layout, commonly `13.333 x 7.5` inches.

For every slide:

- Add a PowerPoint background rectangle using the HTML theme color.
- Add top chrome and footer as editable text.
- Add headings and body copy as editable text boxes.
- Add rules, dividers, callout blocks, and stat cards as PowerPoint shapes.
- Insert source images as separate image objects, not baked into a full-slide screenshot.
- Keep images visually related to the slide content.

Preserve the slide count unless the user asks for a different count.

### 4. Fit Images Deliberately

Use `contain` for screenshots, product UI, charts, and anything that must remain legible. Use `cover` only for decorative or full-bleed imagery.

For screenshots:

- Keep the whole UI visible whenever possible.
- Add a subtle panel background if the screenshot needs contrast.
- Avoid repeating the same image across adjacent slides unless the HTML intentionally does so.
- Do not swap in unrelated images to "fill space".

### 5. Validate Editability

After generating the PPTX, check that it is not a screenshot deck.

Good signs:

- Each slide has many text/shape objects.
- Slide text appears in PPTX XML.
- Images correspond to source assets, not 15 full-slide PNG screenshots.

Quick XML text/font check:

```bash
python3 - <<'PY'
from pathlib import Path
from zipfile import ZipFile

pptx = Path("ppt/deck-name.pptx")
with ZipFile(pptx) as z:
    slides = [n for n in z.namelist() if n.startswith("ppt/slides/slide") and n.endswith(".xml")]
    xml = "\n".join(z.read(n).decode("utf-8", "ignore") for n in slides)

print("slides", len(slides))
for needle in ["Songti SC", "PingFang SC", "Noto Serif SC", "Noto Sans SC", "IBM Plex Mono", "Playfair Display"]:
    print(needle, xml.count(needle))
PY
```

Old fallback fonts from a prior export should not remain if the HTML uses the guizang defaults.

### 6. Visual QA

Render the PPTX and inspect it. Font changes often create wrapping or overflow, so QA after every font or layout pass.

```bash
mkdir -p ppt/pptx-qa
soffice --headless --convert-to pdf --outdir ppt/pptx-qa ppt/deck-name.pptx
pdftoppm -png -r 120 ppt/pptx-qa/deck-name.pdf ppt/pptx-qa/slide
```

Create a contact sheet and inspect it for:

- Missing slides
- Wrong page order
- Text overflow or clipped titles
- Font mismatch against HTML
- Lines crossing text
- Images too small, repeated, stretched, or unrelated
- Footer/chrome collisions
- Placeholder text

If `soffice` fails inside a sandbox because it needs system cache access, rerun it with the required approval instead of skipping QA.

### 7. Deliver Clearly

In the final response, state:

- The PPTX path
- That it is a real editable PPTX, not screenshot slides
- Any caveat about fonts needing to be installed on the user's machine
- What QA was performed

Example:

```text
已导出真正可编辑 PPTX：文字、形状和图片都是独立对象，不是整页截图。
字体已对齐 HTML：Noto Serif SC / Noto Sans SC / Playfair Display / IBM Plex Mono。
我已转 PDF/PNG 做过 15 页目检，没有发现明显溢出或错位。
```

## Common Pitfalls

- **Screenshot deck**: Fast, but wrong for "editable PPTX".
- **Font drift**: HTML uses `Noto Serif SC`, but PPTX silently falls back to Songti or PingFang. Set East Asian fonts explicitly.
- **Over-rewriting**: Exporting should preserve the approved HTML content and structure.
- **Image mismatch**: Do not use decorative images where the HTML used evidence screenshots.
- **Skipping QA**: PPTX layout bugs often only show up after rendering through PowerPoint/LibreOffice.
- **Expecting WebGL/animations to export**: Rebuild the static visual result; PPTX will not preserve the HTML shader or Motion One page animations.

---

更多 AI SEO 技能详见：https://domainrank.app/ai-seo-skills
