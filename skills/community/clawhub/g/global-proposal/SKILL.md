---
name: arabic-docx
description: Create Arabic (.docx) Word documents with proper right-to-left (RTL) layout, correct font splitting (Arabic script font for Arabic text + Latin font for English text), Arabic-Indic numerals (٠-٩), working table of contents, and verified formatting. Use this skill whenever the user wants to create, generate, or build an Arabic Word document, Arabic report, Arabic thesis/proposal/research, Arabic letter, or any RTL document that must look correct in Microsoft Word — even if they don't explicitly say "Arabic docx" but the content is clearly Arabic. Also use it when the user asks to fix Arabic font issues, convert numbers to Arabic numerals (٠-٩), or configure RTL page numbers in an existing docx.
---

# Skill: arabic-docx

Create professional Arabic Word documents (`.docx`) that render correctly in Microsoft Word: proper RTL layout, the right fonts for Arabic vs English text, Arabic-Indic numerals (٠-٩), a working table of contents, and clean formatting.

## Why this skill exists

Generating Arabic `.docx` with generic tools produces documents that look wrong in Word: English fonts applied to Arabic text, Western numerals (0-9) where Arabic-Indic (٠-٩) is expected, LTR page numbers, and broken TOC fields. This skill encodes the exact configuration that produces correct output, tested end-to-end in Word.

## The four key principles

### 1. Font splitting (the most important pattern)

In OOXML, a run has three font slots. **You must set all three explicitly on every `TextRun`**, or Arabic text silently falls back to the wrong font:

```javascript
const FONT_EN = "Times New Roman";   // for Latin/English text
const FONT_AR = "Simplified Arabic"; // for Arabic text

font: { ascii: FONT_EN, hAnsi: FONT_EN, cs: FONT_AR }
//         ↑ Latin chars     ↑ high-ANSI     ↑ Complex Script (Arabic)
```

- `ascii` — applied to basic Latin characters (A-Z, 0-9, punctuation)
- `hAnsi` — applied to extended Latin / high-ANSI characters
- `cs` — **Complex Script** slot; this is the one Arabic text actually uses

**Common mistake:** setting only `font: "Times New Roman"` applies Times New Roman to the `cs` slot too, so Arabic renders in a Latin font and looks broken. Always split the three slots.

**Recommended Arabic fonts** (all ship with Microsoft Office on Windows):
| Font | Style | Good for |
|------|-------|----------|
| `Simplified Arabic` | Clean, traditional | Body text, general use |
| `Traditional Arabic` | Heavier, serif-like | Headings, titles |
| `Arial` | Universal | If Simplified Arabic unavailable |
| `Sakkal Majalla` | Modern, elegant | Body or headings |

**Recommended English fonts**: `Times New Roman` (academic), `Arial` (modern), `Calibri` (default).

### 2. Right-to-left layout

Every Arabic paragraph and every run needs RTL flags:

```javascript
new Paragraph({
  bidirectional: true,          // ← paragraph-level RTL
  alignment: AlignmentType.JUSTIFIED,  // or RIGHT / CENTER
  children: [new TextRun({
    text: "النص العربي",
    rightToLeft: true,          // ← run-level RTL
    // ...
  })],
})
```

- `bidirectional: true` → emits `<w:bidi/>` in paragraph properties (sets paragraph direction to RTL)
- `rightToLeft: true` → emits `<w:rtl/>` in run properties (marks the run as RTL)

**Both are needed.** Without `bidirectional`, the paragraph flows left-to-right. Without `rightToLeft`, the run's internal ordering and numeral form may be wrong.

### 3. Arabic-Indic numerals (٠-٩)

Arabic documents should display Arabic-Indic digits (٠١٢٣٤٥٦٧٨٩) in Arabic text, and Western digits (0123456789) in English text. Because Arabic-Indic digits are in the Arabic Unicode block (U+0660–U+0669), they automatically render with the `cs` font (Arabic font) — so the font assignment is already correct once principle #1 is in place. The remaining task is converting the digit *characters*.

**Do not hand-convert digits in source text.** Generate the document normally with ASCII digits, then run the post-processing script (see Pipeline below) that converts them in-place. The script is content-aware: it only converts digits inside paragraphs that contain Arabic text, so English references and DOIs keep their Western digits.

### 4. Font sizes are in half-points

In docx-js / OOXML, `size` values are **half-points**, not points:

| Desired | `size` value |
|---------|-------------|
| 11 pt | 22 |
| 12 pt | 24 |
| **14 pt** (typical Arabic body) | **28** |
| 15 pt | 30 |
| 18 pt (H1) | 36 |

### 5. RTL tables (critical — easily missed)

Every content table must have `visuallyRightToLeft: true` on the `Table` object, or columns flow left-to-right (wrong for Arabic):

```javascript
new Table({
  width: { size: 100, type: WidthType.PERCENTAGE },
  layout: TableLayoutType.FIXED,
  visuallyRightToLeft: true,   // ← emits <w:bidiVisual/>, columns read right-to-left
  // ...
})
```

This is separate from the `bidirectional: true` / `rightToLeft: true` flags on paragraphs and runs inside cells (those control text direction within each cell). **Both are needed**: `visuallyRightToLeft` on the table for column ordering, plus RTL flags on cell content for text direction.

**Common mistake:** adding RTL flags to cell paragraphs but forgetting `visuallyRightToLeft` on the table itself — the text in each cell is RTL, but the columns still read left-to-right, so the first column appears on the left instead of the right.

Check every `new Table(...)` call in your script. Layout-only tables with a single cell (e.g., a full-page cover wrapper) do not need it, but any multi-column table does.

## The pipeline

Generate the document in five stages. Save the generation script to disk first (per project rules about persisting scripts), then run each stage:

```bash
# Stage 1: Generate the .docx with docx-js (Node.js)
node scripts/generate_doc.js

# Stage 2: Insert TOC placeholder entries (so the TOC isn't empty before Word updates it)
python3 <docx-skill>/scripts/add_toc_placeholders.py "output.docx" --auto

# Stage 3: Convert numerals to Arabic-Indic in Arabic text
python3 skills/arabic-docx/scripts/convert_arabic_numerals.py "output.docx"

# Stage 4: Self-check
python3 <docx-skill>/scripts/postcheck.py "output.docx"

# Stage 5: PDF preview for visual verification
soffice --headless --convert-to pdf "output.docx"
```

`<docx-skill>` is the path to the installed `docx` skill's scripts directory.

## Getting started

1. **Read `scripts/arabic_docx_template.js`** — it contains tested helper functions (`p`, `h1`, `h2`, `h3`, `bullet`, `numItem`, `tCell`, `buildTable`, `tableCaption`, `buildHeader`, `buildPageFooter`, plus the default `styles` config and section structure). Copy it as the starting point for your generator script and replace the content.

2. **Read `references/arabic-docx-guide.md`** before writing code — it covers the font split mechanism in depth, RTL table configuration, page numbers and PAGE fields, TOC setup, common pitfalls, and the numeral conversion logic. Read it fully; every section addresses a real failure.

## Helper function reference

The template provides these helpers (all RTL-aware and font-split):

| Helper | Purpose | Default size |
|--------|---------|-------------|
| `p(text, opts)` | Body paragraph (justified, first-line indent) | 28 (14pt) |
| `h1(text)` | Heading 1 (centered, bold) | 36 (18pt) |
| `h2(text)` | Heading 2 (right-aligned, bold) | 30 (15pt) |
| `h3(text)` | Heading 3 (right-aligned, bold) | 28 (14pt) |
| `bullet(text, level)` | Bulleted list item | 28 (14pt) |
| `numItem(text, num)` | Manually-numbered item | 28 (14pt) |
| `tableCaption(text)` | Table/figure caption | 22 (11pt) |
| `tCell(text, opts)` | Table cell (supports `\n` multiline) | 22–24 |
| `buildTable(headers, rows, colWidths)` | Full RTL table with header row | — |
| `buildHeader(title)` | Page header with bottom border | 20 (10pt) |
| `buildPageFooter()` | RTL footer with Arabic page number | 22 (11pt) |

## Common pitfalls (read these — each is a real bug)

1. **Setting `font` as a string instead of an object** — Arabic text renders in a Latin font. Always use `{ ascii, hAnsi, cs }`.

2. **Forgetting `rightToLeft: true` on runs** — even in an RTL paragraph, runs without `<w:rtl/>` may render LTR and use the wrong numeral form.

3. **Page numbers showing as Western digits** — the footer paragraph must have `bidirectional: true` and the page-number run must have `rightToLeft: true`. With Word's default "Context" numeral setting, this makes PAGE fields render as Arabic-Indic.

4. **Empty TOC** — the TOC field exists but shows no entries until Word updates it. Run `add_toc_placeholders.py` to insert cached placeholder entries so the TOC is populated immediately. The user updates it in Word with F9 for live page numbers.

5. **Body text too small** — the default `size: 26` (13pt) is common in templates but too small for Arabic academic documents. Use `size: 28` (14pt) for body.

6. **English references getting Arabic-Indic digits** — the numeral converter is content-aware (only converts in paragraphs containing Arabic characters), so purely English reference entries keep their Western digits. If you mix Arabic and English in one paragraph, all digits convert — keep references in their own paragraphs.

7. **Tables flowing LTR** — add `visuallyRightToLeft: true` on the `Table` object (in addition to RTL on cells) so columns read right-to-left.

## Output

Save the final `.docx` to the project's `download/` directory. Also produce a PDF preview alongside it for visual verification. Link both files in your final reply to the user.
