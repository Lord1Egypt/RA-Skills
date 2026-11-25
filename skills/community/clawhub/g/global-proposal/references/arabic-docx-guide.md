# Arabic DOCX Guide — Detailed Reference

This guide covers the technical details behind each pattern in the `arabic-docx` skill. Read it before writing generation code — every section addresses a real failure observed in testing.

## Table of contents

1. [Font splitting mechanism](#1-font-splitting-mechanism)
2. [Right-to-left configuration](#2-right-to-left-configuration)
3. [Numeral forms (Arabic-Indic vs Western)](#3-numeral-forms-arabic-indic-vs-western)
4. [Page numbers and PAGE fields](#4-page-numbers-and-page-fields)
5. [Table of contents setup](#5-table-of-contents-setup)
6. [RTL tables](#6-rtl-tables)
7. [Section structure](#7-section-structure)
8. [The numeral conversion script](#8-the-numeral-conversion-script)
9. [Postcheck and verification](#9-postcheck-and-verification)
10. [Common pitfalls and solutions](#10-common-pitfalls-and-solutions)

---

## 1. Font splitting mechanism

### The three font slots

Every text run in OOXML has three font slots, controlled by the `<w:rFonts>` element:

| Slot | XML attribute | docx-js key | Applies to |
|------|--------------|-------------|------------|
| ASCII | `w:ascii` | `ascii` | Basic Latin: A-Z, digits 0-9, basic punctuation |
| High-ANSI | `w:hAnsi` | `hAnsi` | Extended Latin, accented chars, symbols |
| Complex Script | `w:cs` | `cs` | Arabic, Hebrew, Thai, and Arabic-Indic digits (٠-٩) |

Arabic text is classified as "Complex Script" by Word, so it uses the `cs` slot. If you set only `font: "Times New Roman"`, docx-js applies Times New Roman to all three slots, and Arabic characters render in a Latin font that lacks Arabic glyphs — producing broken output (boxes or fallback rendering).

### Correct configuration

```javascript
// Define fonts once
const FONT_EN = "Times New Roman";
const FONT_AR = "Simplified Arabic";

// Apply on EVERY TextRun — never omit the cs slot
font: { ascii: FONT_EN, hAnsi: FONT_EN, cs: FONT_AR }
```

This produces:
```xml
<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Simplified Arabic"/>
```

### Why `ascii` and `hAnsi` can share a value

Most English fonts like Times New Roman cover both basic Latin and extended Latin. Setting `ascii` and `hAnsi` to the same value is standard and correct. You'd only split them if you had a font that covers ASCII but not high-ANSI (rare).

### Default document styles

In addition to per-run fonts, set the **default document style** so any run without explicit fonts inherits the correct split:

```javascript
styles: {
  default: {
    document: {
      run: { font: { ascii: FONT_EN, hAnsi: FONT_EN, cs: FONT_AR }, size: 28, color: "000000" },
    },
    heading1: {
      run: { font: { ascii: FONT_EN, hAnsi: FONT_EN, cs: FONT_AR }, size: 36, bold: true },
    },
    // ... heading2, heading3 similarly
  },
}
```

### Arabic-Indic digits and the cs slot

Arabic-Indic digits (٠-٩, Unicode U+0660–U+0669) are in the Arabic block, so they render with the `cs` font automatically. This means once you convert ASCII digits to Arabic-Indic (via the conversion script), they use the Arabic font without any extra configuration. Western digits (0-9) use the `ascii` font. **The font assignment is a consequence of the character encoding, not a separate setting.**

### Recommended Arabic fonts

| Font | Availability | Characteristics |
|------|-------------|-----------------|
| `Simplified Arabic` | Ships with MS Office (Windows) | Clean, readable, good for body text |
| `Traditional Arabic` | Ships with MS Office (Windows) | Heavier strokes, good for headings |
| `Arial` | Universal | Safe fallback if others unavailable |
| `Sakkal Majalla` | Ships with some Office versions | Modern, elegant |
| `Courier New` | Universal | Monospace — avoid for body |

**Note on Linux:** These fonts may not be installed on the Linux sandbox. LibreOffice will substitute a fallback for rendering the PDF preview, but the `.docx` retains the correct font names and will render correctly in Word on the user's Windows system. The postcheck may warn about "font-fallback" — this is expected and safe to ignore for fonts that ship with Office.

---

## 2. Right-to-left configuration

### Two levels of RTL

RTL requires flags at **both** the paragraph and run level:

**Paragraph level** — `bidirectional: true`:
```javascript
new Paragraph({
  bidirectional: true,  // → <w:bidi/> in <w:pPr>
  // ...
})
```
This sets the paragraph's base direction to RTL, affecting alignment, indentation side, and text flow.

**Run level** — `rightToLeft: true`:
```javascript
new TextRun({
  text: "النص",
  rightToLeft: true,  // → <w:rtl/> in <w:rPr>
  // ...
})
```
This marks the run as RTL, affecting internal character ordering and numeral form.

### Why both are needed

- A paragraph with `bidirectional: true` but runs without `rightToLeft` — the paragraph flows RTL but individual runs may render with LTR ordering, causing garbled text.
- Runs with `rightToLeft` in a paragraph without `bidirectional` — the run is marked RTL but the paragraph alignment and indentation may be wrong.

**Always set both.** The template helpers (`p`, `h1`, `h2`, `h3`, `bullet`, `numItem`, `tCell`, etc.) all set both flags.

### Alignment with RTL

In RTL paragraphs, alignment behaves as expected:
- `AlignmentType.RIGHT` → text starts from the right edge (natural for Arabic headings)
- `AlignmentType.JUSTIFIED` → full justification (natural for body paragraphs)
- `AlignmentType.CENTER` → centered (for titles, captions)
- `AlignmentType.LEFT` → text starts from the left edge (rare in Arabic; use for English-only content)

### Indentation

First-line indent for body paragraphs:
```javascript
indent: { firstLine: 480 }  // 480 twips ≈ 0.33 inch
```

For numbered lists with hanging indent:
```javascript
indent: { left: 720, hanging: 360 }  // left margin 720, hanging 360
```

In RTL paragraphs, `left` indent applies to the **right** side visually (the "start" side), and `right` applies to the left side. This can be confusing — test with the PDF preview.

---

## 3. Numeral forms (Arabic-Indic vs Western)

### The two numeral systems

| System | Characters | Unicode | Used in |
|--------|-----------|---------|---------|
| Western (Arabic) | 0 1 2 3 4 5 6 7 8 9 | U+0030–U+0039 | English text, international formats |
| Arabic-Indic (Hindi) | ٠ ١ ٢ ٣ ٤ ٥ ٦ ٧ ٨ ٩ | U+0660–U+0669 | Arabic text |

In Arabic academic and formal documents, numbers within Arabic text should use Arabic-Indic digits (٠-٩). Numbers in English text (references, DOIs, software version strings) should remain Western.

### The conversion approach

The conversion is done **post-generation** by `scripts/convert_arabic_numerals.py`, not in the source text. This approach has several advantages:

1. **Source text stays readable** — you write "2026" in the source, not "٢٠٢٦".
2. **Content-aware** — the script only converts digits in paragraphs that contain Arabic characters, so English references keep Western digits.
3. **Applies to the final output** — one transformation handles all text uniformly.

### How the script decides what to convert

The script examines each `<w:p>` (paragraph) in `document.xml`:
1. Concatenates all `<w:t>` text in the paragraph.
2. Checks if the combined text contains any Arabic character (U+0600–U+06FF range and Arabic presentation forms).
3. If yes → converts all ASCII digits (0-9) to Arabic-Indic (٠-٩) in every `<w:t>` within that paragraph.
4. If no → leaves the paragraph untouched.

This means:
- `"في عام 2026"` → contains Arabic → converts to `"في عام ٢٠٢٦"` ✓
- `"Smith, J. (2020). Title."` → no Arabic → stays as `"Smith, J. (2020). Title."` ✓
- `"SPSS version 25"` → no Arabic → stays as `"SPSS version 25"` ✓
- `"استخدم الباحث SPSS 25"` → contains Arabic → converts to `"استخدم الباحث SPSS ٢٥"` (the 25 becomes ٢٥ even though SPSS is English — this is correct for Arabic documents)

### What about mixed content?

If a paragraph mixes Arabic and English with digits, all digits in that paragraph convert. This is usually correct: in Arabic documents, numbers are written in Arabic-Indic even when the surrounding term is English (e.g., "استخدم SPSS ٢٥").

The one case to watch: **DOIs and URLs** in references. If a reference is purely English (no Arabic characters), its DOI stays intact. But if you mix a DOI into an Arabic sentence, the digits would convert and break the DOI. Keep references in their own paragraphs.

### What the script does NOT convert

- `<w:instrText>` elements (field instructions like `PAGE`, `TOC \o "1-3"`) — these contain parameters, not display text, and must stay as ASCII.
- Purely English paragraphs (no Arabic characters).
- Non-digit characters (letters, punctuation).

---

## 4. Page numbers and PAGE fields

### The PAGE field

Page numbers in docx use the `PAGE` field, created in docx-js as:
```javascript
new TextRun({ children: [PageNumber.CURRENT] })
```

This generates a dynamic field that Word evaluates when the document opens. The field has no static value in the `.docx` — Word computes the page number at render time.

### Making page numbers Arabic-Indic

Because the PAGE field is dynamic, you cannot statically set the numeral form of its result. The numeral form depends on:

1. **The paragraph direction** — if `bidirectional: true` (RTL paragraph)
2. **The run direction** — if `rightToLeft: true` (RTL run)
3. **Word's numeral application setting** — File → Options → Advanced → "Numeral" (Context / Hindi / Arabic / System)

When the paragraph and run are RTL, and Word's setting is "Context" (the default in Arabic Word installations), the PAGE field renders as Arabic-Indic. **This is why the footer must have `bidirectional: true` and `rightToLeft: true`.**

### The correct footer configuration

```javascript
function buildPageFooter() {
  return new Footer({
    children: [new Paragraph({
      bidirectional: true,        // ← RTL paragraph
      alignment: AlignmentType.CENTER,
      children: [
        new TextRun({ text: "- ", rightToLeft: true, ... }),  // ← RTL run
        new TextRun({ children: [PageNumber.CURRENT], rightToLeft: true, ... }),
        new TextRun({ text: " -", rightToLeft: true, ... }),
      ],
    })],
  });
}
```

### Limitation

If the user's Word is set to "Arabic" (Western numerals) instead of "Context" or "Hindi", page numbers will show as Western regardless of the RTL flags. This is an application preference that cannot be controlled from the document. The RTL configuration maximizes the chance of Arabic-Indic rendering but does not guarantee it across all Word configurations.

### NUMPAGES field

For "page X of Y" footers, use `PageNumber.TOTAL_PAGES` alongside `PageNumber.CURRENT`. The same RTL rules apply.

---

## 5. Table of contents setup

### The TOC field

In docx-js, the TOC is created with:
```javascript
new TableOfContents("Table of Contents", {
  hyperlink: true,
  headingStyleRange: "1-3",
})
```

This inserts a TOC field that Word populates when the document opens (or when the user presses F9). The `headingStyleRange: "1-3"` tells Word to include Heading 1, 2, and 3 styles.

### The empty TOC problem

When the document is first generated, the TOC field exists but has no cached content — it appears empty until Word updates it. This looks broken to users who open the document and see a blank TOC.

### Solution: add_toc_placeholders.py

After generating the `.docx`, run the `docx` skill's `add_toc_placeholders.py` script:
```bash
python3 <docx-skill>/scripts/add_toc_placeholders.py "output.docx" --auto
```

This scans the document for headings (Heading 1/2/3) and inserts placeholder TOC entries with cached text and page numbers. The TOC appears populated immediately. When the user updates the TOC in Word (F9), the page numbers refresh to accurate values.

### TOC heading

The TOC section typically starts with a heading paragraph:
```javascript
new Paragraph({
  bidirectional: true,
  alignment: AlignmentType.CENTER,
  children: [new TextRun({ text: "فهرس المحتويات", rightToLeft: true, size: 36, bold: true, ... })],
})
```

This heading should NOT use `HeadingLevel.HEADING_1` (otherwise it would appear in the TOC itself). Use a plain styled paragraph.

### TOC and Arabic numerals

The placeholder entries inserted by `add_toc_placeholders.py` contain page numbers as ASCII digits. The `convert_arabic_numerals.py` script converts them to Arabic-Indic because the TOC entry text contains Arabic (the heading text). Run numeral conversion **after** TOC placeholder insertion, in this order:

1. Generate `.docx`
2. Add TOC placeholders
3. Convert numerals
4. Postcheck
5. PDF preview

---

## 6. RTL tables

### visuallyRightToLeft

Tables in Arabic documents should read right-to-left: the first column appears on the right, the last on the left. This requires `visuallyRightToLeft: true` on the `Table` object:

```javascript
new Table({
  width: { size: 100, type: WidthType.PERCENTAGE },
  layout: TableLayoutType.FIXED,
  visuallyRightToLeft: true,  // ← columns flow right-to-left
  // ...
})
```

### Cell content

Each cell's paragraphs and runs still need `bidirectional: true` and `rightToLeft: true` respectively (the `tCell` helper handles this). The `visuallyRightToLeft` flag only affects column ordering, not text direction within cells.

### Header row

Mark the header row with `tableHeader: true` so it repeats on each page if the table spans multiple pages:
```javascript
new TableRow({
  tableHeader: true,
  cantSplit: true,
  children: headers.map(h => tCell(h, { header: true })),
})
```

### Alternating row colors

For readability, alternate row background colors:
```javascript
rows.map((row, idx) => new TableRow({
  children: row.map(c => tCell(c, { alt: idx % 2 === 0 })),
}))
```

The `tCell` helper applies `COLOR_TABLE_ALT` (light blue) when `alt: true`.

### Column widths

When using `TableLayoutType.FIXED`, specify column widths as percentages:
```javascript
buildTable(headers, rows, [40, 30, 30])  // 40%, 30%, 30%
```

With `visuallyRightToLeft: true`, the first width applies to the rightmost column.

---

## 7. Section structure

### Typical Arabic document sections

1. **Cover page** — no header/footer, zero margins, no page number
2. **Table of contents** — starts page numbering, has header/footer
3. **Body** — continues page numbering, has header/footer

### Cover page section

```javascript
{
  properties: {
    page: {
      size: { width: 11906, height: 16838 },  // A4 in twips
      margin: { top: 0, bottom: 0, left: 0, right: 0 },
    },
  },
  children: buildCover(),
}
```

No `headers` or `footers` key → no header/footer on this section.

### Content sections

```javascript
{
  properties: {
    type: SectionType.NEXT_PAGE,  // start on a new page
    page: {
      size: { width: 11906, height: 16838 },
      margin: { top: 1440, bottom: 1440, left: 1701, right: 1417, header: 850, footer: 992 },
    },
  },
  headers: { default: buildHeader("Title") },
  footers: { default: buildPageFooter() },
  children: contentArray,
}
```

Margins are in twips (1 inch = 1440 twips). The values above are typical for A4 academic documents.

### Page numbering

Page numbering starts from section 2 (the TOC). The cover page has no page number. If you want the cover to be "page 0" or unnumbered but the TOC to start at page 1, you don't need special configuration — Word handles this automatically based on section breaks.

---

## 8. The numeral conversion script

### Location

`scripts/convert_arabic_numerals.py`

### Usage

```bash
python3 skills/arabic-docx/scripts/convert_arabic_numerals.py "document.docx"
```

The script modifies the `.docx` in-place (it creates a temp file and moves it over the original).

### What it processes

- `word/document.xml` — main document body (content-based conversion)
- `word/header*.xml` — all headers (convert all digits, since headers may contain page numbers)
- `word/footer*.xml` — all footers (convert all digits, for page numbers)

### What it does NOT process

- `word/styles.xml` — style definitions don't contain display text
- `word/numbering.xml` — numbering definitions don't contain display text
- `word/settings.xml` — settings don't contain display text
- `word/_rels/*` — relationship files
- `[Content_Types].xml` — content type declarations

### How it works internally

1. **Unzip** the `.docx` (it's a ZIP archive).
2. For each relevant XML file, **parse** with lxml.
3. **Iterate** paragraphs (`<w:p>`):
   - Gather all text from `<w:t>` elements.
   - Check for Arabic characters (regex `[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]`).
   - If Arabic found, convert ASCII digits to Arabic-Indic in all `<w:t>` within the paragraph.
4. For headers/footers: convert ALL digits (no Arabic check needed — page numbers).
5. **Re-zip** and save.

### Idempotency

The script is idempotent: running it twice produces the same output (Arabic-Indic digits are not further converted). Safe to run multiple times.

### Verification

After conversion, verify with:
```bash
# Count Arabic-Indic and Western digits in the PDF
pdftotext "document.pdf" - | python3 -c "
import sys, re
text = sys.stdin.read()
arabic = len(re.findall(r'[٠-٩]', text))
western = len(re.findall(r'[0-9]', text))
print(f'Arabic-Indic: {arabic}, Western: {western}')
"
```

---

## 9. Postcheck and verification

### postcheck.py

Run the `docx` skill's postcheck after generation:
```bash
python3 <docx-skill>/scripts/postcheck.py "document.docx"
```

This checks for:
- Blank pages
- Cover overflow
- Line spacing consistency
- Image overflow / aspect ratio
- Heading level continuity
- Shading type misuse
- TOC field presence
- Font fallback warnings

### Expected warnings

- **font-fallback: "Simplified Arabic"** — expected on Linux; the font ships with MS Office on Windows and renders correctly there. Safe to ignore.
- **line-spacing inconsistent** — expected if you intentionally use different spacing for headings vs body. Safe to ignore if the spacing variation is intentional.

### Errors to fix

- **heading-levels discontinuous** — fix heading hierarchy (don't jump from H1 to H3).
- **cover-overflow** — cover content exceeds page bounds; reduce content or spacing.
- **blank-pages** — remove empty paragraphs or page breaks.
- **toc missing** — add a `TableOfContents` field.

### PDF visual check

Always generate a PDF preview and inspect pages:
```bash
soffice --headless --convert-to pdf "document.docx"
rm -rf /tmp/render && mkdir -p /tmp/render
pdftoppm -r 60 -jpeg -jpegopt quality=60 "document.pdf" /tmp/render/page
```

Check the first 2 pages, pages with tables/charts, and the last page. Verify:
- Arabic text renders correctly (not boxes or fallback)
- Numbers in Arabic text are Arabic-Indic (٠-٩)
- Tables read right-to-left
- Page numbers appear in the footer
- TOC has entries

**Note:** The PDF preview uses LibreOffice, which may substitute fonts not installed on Linux. The actual Word rendering on the user's system will use the correct fonts. Font substitution in the preview does not indicate a problem in the `.docx`.

---

## 10. Common pitfalls and solutions

### Pitfall: Arabic text in Latin font

**Symptom:** Arabic text appears as boxes, question marks, or a Latin font that lacks Arabic glyphs.

**Cause:** `font` set as a string (`font: "Times New Roman"`) instead of an object, so the `cs` slot gets a Latin font.

**Fix:** Always use `font: { ascii: FONT_EN, hAnsi: FONT_EN, cs: FONT_AR }`.

### Pitfall: Numbers stay as Western in Arabic text

**Symptom:** "في عام 2026" shows as "في عام 2026" instead of "في عام ٢٠٢٦".

**Cause:** Numeral conversion script not run, or run before TOC placeholder insertion.

**Fix:** Run `convert_arabic_numerals.py` after all other post-processing steps.

### Pitfall: Page numbers are Western

**Symptom:** Footer shows "1", "2" instead of "١", "٢".

**Cause:** Footer paragraph or run missing RTL flags.

**Fix:** Add `bidirectional: true` to the footer paragraph and `rightToLeft: true` to all footer runs. (Also depends on Word's numeral setting being "Context" or "Hindi" — the default for Arabic Word.)

### Pitfall: Empty TOC

**Symptom:** TOC heading appears but no entries below it.

**Cause:** TOC field has no cached content; Word hasn't updated it yet.

**Fix:** Run `add_toc_placeholders.py` after generation.

### Pitfall: Table columns flow left-to-right

**Symptom:** Table first column is on the left instead of the right.

**Cause:** Missing `visuallyRightToLeft: true` on the Table object.

**Fix:** Add `visuallyRightToLeft: true` to the `new Table({...})` call.

### Pitfall: Headings don't appear in TOC

**Symptom:** TOC is empty even after placeholder insertion.

**Cause:** Headings not using `HeadingLevel.HEADING_1/2/3`, or TOC `headingStyleRange` doesn't match.

**Fix:** Ensure headings use `heading: HeadingLevel.HEADING_1` etc., and TOC uses `headingStyleRange: "1-3"`.

### Pitfall: Body text too small

**Symptom:** Text looks small compared to standard Arabic documents.

**Cause:** `size: 26` (13pt) is common in templates but small for Arabic.

**Fix:** Use `size: 28` (14pt) for body text.

### Pitfall: English references get Arabic-Indic digits

**Symptom:** Reference "Smith (2020)" becomes "Smith (٢٠٢٠)".

**Cause:** The reference paragraph contains Arabic text (e.g., an Arabic annotation), triggering conversion.

**Fix:** Keep English references in their own paragraphs without any Arabic text. If a reference must mix languages, accept the conversion (Arabic-Indic digits in mixed paragraphs is standard in Arabic academic writing).

### Pitfall: Field codes corrupted

**Symptom:** PAGE field or TOC field broken after processing.

**Cause:** Numeral conversion script modified `<w:instrText>` elements.

**Fix:** The script only processes `<w:t>` elements, not `<w:instrText>`. If this still happens, verify you're using the script from this skill (not a modified version).
