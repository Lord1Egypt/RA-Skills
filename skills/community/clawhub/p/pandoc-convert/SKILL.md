---
name: pandoc-convert
description: "Convert documents between formats using Pandoc CLI (Markdown, DOCX, PDF, HTML, EPUB, PPTX, ODT, RTF, LaTeX, CSV/TSV, Jupyter, etc.). Use when: (1) converting file formats, (2) generating DOCX/PDF from Markdown, (3) creating slide decks (PPTX/Beamer/Reveal.js), (4) extracting text from DOCX/EPUB/ODT, (5) producing EPUBs, (6) any Pandoc conversion task."
---

# Pandoc Document Conversion

Pandoc 3.6.3 installed at `~/.local/bin/pandoc`. Features: +server +lua.

## Quick Reference

```bash
# Basic conversion
pandoc input.md -o output.docx          # MD → Word
pandoc input.md -o output.pdf           # MD → PDF (needs LaTeX)
pandoc input.md -o output.html          # MD → HTML
pandoc input.md -o output.epub          # MD → EPUB
pandoc input.md -o output.pptx          # MD → PowerPoint
pandoc input.md -o output.odt           # MD → OpenDocument
pandoc input.md -o output.rtf           # MD → RTF
pandoc input.md -o output.tex           # MD → LaTeX
pandoc input.docx -o output.md          # Word → Markdown
pandoc input.html -o output.md          # HTML → Markdown
pandoc input.epub -o output.md          # EPUB → Markdown

# Standalone document (with headers/footers/styles)
pandoc -s input.md -o output.html

# With metadata
pandoc -s --metadata title="Report" --metadata author="Kairo" input.md -o output.docx

# With table of contents
pandoc -s --toc input.md -o output.docx

# With custom reference doc (Word styles)
pandoc --reference-doc=custom-reference.docx input.md -o output.docx

# With CSS (HTML/EPUB)
pandoc -s --css=style.css input.md -o output.html

# Extract media from document
pandoc --extract-media=./media input.docx -o output.md

# Self-contained HTML (no external dependencies)
pandoc -s --embed-resources input.md -o output.html

# Number sections
pandoc -s --number-sections input.md -o output.docx

# Read from URL
pandoc -f html -t markdown https://example.com -o page.md

# Custom request header for URL fetch
pandoc -f html -t markdown --request-header User-Agent:"Mozilla/5.0" https://example.com -o page.md
```

## Key Options

### General Options

| Option | Effect |
|---|---|
| `-f FORMAT` | Input format (default: auto-detect by extension) |
| `-t FORMAT` | Output format (default: auto-detect by extension) |
| `-o FILE` | Output file path (`-` for stdout) |
| `-s, --standalone` | Produce complete document (header, footer, etc.) |
| `--template=FILE\|URL` | Custom template (implies --standalone) |
| `-M KEY[=VAL]` | Set metadata field (overrides YAML block) |
| `--metadata-file=FILE` | Read metadata from YAML/JSON file |
| `-V KEY[=VAL]` | Set template variable |
| `--variable-json=KEY=JSON` | Set template variable to JSON value (bool, list, map) |
| `-d FILE, --defaults=FILE` | Load options from YAML/JSON defaults file |
| `--data-dir=DIRECTORY` | User data directory for templates, reference docs, etc. |
| `--sandbox` | Limit IO operations (for untrusted input) |
| `--verbose` | Verbose debugging output |
| `--quiet` | Suppress warning messages |
| `--fail-if-warnings` | Exit with error if any warnings |
| `--log=FILE` | Write log messages as JSON to FILE |

### Reader Options

| Option | Effect |
|---|---|
| `--shift-heading-level-by=N` | Shift heading levels (positive or negative) |
| `--file-scope` | Parse each file individually (multi-file) |
| `-F PROGRAM, --filter=PROGRAM` | JSON filter to transform AST |
| `-L SCRIPT, --lua-filter=SCRIPT` | Lua filter to transform AST |
| `--extract-media=DIR\|FILE.zip` | Extract embedded media |
| `--track-changes=accept\|reject\|all` | Handle Word Track Changes |
| `--preserve-tabs` | Keep tabs instead of converting to spaces |
| `--tab-stop=NUMBER` | Spaces per tab (default 4) |

### Writer Options

| Option | Effect |
|---|---|
| `--toc` | Include table of contents |
| `--toc-depth=N` | TOC depth (default 3) |
| `--lof` | List of figures |
| `--lot` | List of tables |
| `-N, --number-sections` | Number section headings |
| `--number-offset=N[,N…]` | Offset section numbers |
| `--wrap=auto\|none\|preserve` | Text wrapping (default: auto) |
| `--columns=N` | Line width in chars (default 72) |
| `--resource-path=DIR:DIR` | Resource search paths (default: working dir) |
| `--embed-resources` | Self-contained HTML (no external deps) |
| `--reference-doc=FILE\|URL` | Custom styles for DOCX/ODT/PPTX |
| `--css=URL` | Link CSS stylesheet (repeatable) |
| `--reference-links` | Use reference-style links in MD output |
| `--top-level-division=section\|chapter\|part` | Top-level heading division type |
| `--ascii` | Use only ASCII in output |
| `--dpi=NUMBER` | Default DPI for image conversion (default 96) |
| `--eol=crlf\|lf\|native` | Line ending style |
| `--pdf-engine=ENGINE` | PDF engine (see below) |
| `--pdf-engine-opt=STRING` | Extra args for PDF engine |
| `-i, --incremental` | Incremental lists in slide shows |
| `--slide-level=N` | Heading level that creates slides |
| `--split-level=N` | Heading level for EPUB/chunked HTML splitting |
| `--epub-cover-image=FILE` | EPUB cover image |
| `--epub-title-page=true\|false` | Include EPUB title page (default true) |
| `--epub-embed-font=FILE` | Embed font in EPUB (repeatable) |
| `--epub-metadata=FILE` | XML file with Dublin Core metadata |
| `--epub-subdirectory=DIR` | EPUB subdirectory in OCF container |
| `--highlight-style=STYLE\|FILE` | **(Deprecated)** Use `--syntax-highlighting` |
| `--syntax-highlighting=default\|none\|idiomatic\|STYLE\|FILE` | Code highlighting method |
| `--no-highlight` | **(Deprecated)** Use `--syntax-highlighting=none` |
| `-H FILE` | Include in header (CSS/JS for HTML, raw LaTeX) |
| `-B FILE` | Include before body |
| `-A FILE` | Include after body |

### Citation Options

| Option | Effect |
|---|---|
| `-C, --citeproc` | Process citations, render bibliography |
| `--bibliography=FILE` | Bibliography file (.bib, .bibtex, .json, .yaml, .ris) |
| `--csl=FILE` | CSL citation style file |
| `--citation-abbreviations=FILE` | Journal abbreviation JSON |
| `--natbib` | Use natbib for LaTeX citations (no --citeproc) |
| `--biblatex` | Use biblatex for LaTeX citations (no --citeproc) |

### Math Rendering (HTML)

| Option | Effect |
|---|---|
| `--mathjax[=URL]` | Render math with MathJax |
| `--mathml` | Render math as MathML |
| `--webtex[=URL]` | Convert math to images via external service |
| `--katex[=URL]` | Render math with KaTeX |
| `--gladtex` | Use GladTeX for math rendering |

## PDF Generation

```bash
# Default (LaTeX via pdflatex)
pandoc input.md -o output.pdf

# Chinese support (XeLaTeX)
pandoc --pdf-engine=xelatex -V CJKmainfont="Noto Sans CJK SC" input.md -o output.pdf

# LuaLaTeX (alternative CJK)
pandoc --pdf-engine=lualatex -V CJKmainfont="Noto Sans CJK SC" input.md -o output.pdf

# HTML intermediate (wkhtmltopdf)
pandoc --pdf-engine=wkhtmltopdf -s input.md -o output.pdf

# WeasyPrint (HTML intermediate)
pandoc --pdf-engine=weasyprint -s input.md -o output.pdf

# Typst (fast, no LaTeX needed)
pandoc --pdf-engine=typst input.md -o output.pdf

# ConTeXt
pandoc -t context input.md -o output.pdf

# roff ms (via pdfroff)
pandoc -t ms input.md -o output.pdf

# latexmk (auto-run LaTeX as needed)
pandoc --pdf-engine=latexmk input.md -o output.pdf

# Pass extra options to PDF engine
pandoc --pdf-engine=xelatex --pdf-engine-opt=-shell-escape input.md -o output.pdf

# Debug: output intermediate LaTeX
pandoc -s -o output.tex input.md
# Then test: pdflatex output.tex
```

**Supported PDF engines**: pdflatex, xelatex, lualatex, latexmk, tectonic, wkhtmltopdf, weasyprint, pagedjs-cli, prince, context, groff, pdfroff, typst.

**Default engines by intermediate format**:
- `-t latex` (or none): pdflatex
- `-t context`: context
- `-t html`: weasyprint
- `-t ms`: pdfroff
- `-t typst`: typst

**Chinese PDF requirements**: XeLaTeX or LuaLaTeX + CJK font. If CJKmainfont is set, xeCJK is needed (xelatex) or luatexja (lualatex). fontspec is required for xelatex/lualatex.

**LaTeX packages needed**: amsfonts, amsmath, lm, unicode-math, iftex, fancyvrb, longtable, booktabs, multirow, graphicx, bookmark, xcolor, soul, geometry (with geometry variable), setspace (with linestretch), babel (with lang).

### 默认中英混排 PDF 字体方案（实测可用）

Linux 系统字体路径：`/usr/share/fonts/`

| 用途 | 字体包 | 字体名（pandoc -V 参数） |
|------|--------|------------------------|
| 中文正文/标题 | 文泉驿正黑 | `wqy-zenhei` |
| 英文正文/标题 | Helvetica Neue | `helvetiker` |
| 代码块 | Courier New / Latin Modern Mono | 默认 monospace 即可 |

**标准生成命令（中英混排）**：
```bash
pandoc input.md \
  -o output.pdf \
  --pdf-engine=xelatex \
  -V CJKmainfont="wqy-zenhei" \
  -V mainfont="helvetiker" \
  -V monofont="Courier New" \
  -V geometry:margin=1in \
  -V linestretch=1.1 \
  -V fontsize=12pt
```

**注意事项**：
- `mainfont`（英文）和 `CJKmainfont`（中文）必须同时设置，否则中英文混排时其中一种会回退到默认 CM 字体
- 不要混用 pdflatex（不支持中文）和 xelatex
- 代码块默认用 Latin Modern Mono，若要 Courier 风格可加 `-V monofont="Courier New"`
- 字体名大小写敏感，敲错 Pandoc 只给警告但仍出 PDF（回退到默认字体），需注意检查输出

**字体名参考**（xelatex + fontspec）：
```
# 查看已安装的中文字体（Linux）
fc-list :lang=zh -f '%{family}\n' | sort -u

# 查看已安装的英文无衬线字体
fc-list | grep -i 'helvetica\|arial\|sans' | head -20

# 测试字体是否可用（直接 pandoc -V CJKmainfont="字体名"）
```

## DOCX Customization

Generate a reference doc to customize styles:
```bash
pandoc -o custom-reference.docx --print-default-data-file reference.docx
```
Open in Word, modify styles, save. Then use `--reference-doc=custom-reference.docx`.

**Paragraph styles**: Normal, Body Text, First Paragraph, Compact, Title, Subtitle, Author, Date, Abstract, AbstractTitle, Bibliography, Heading 1–9, Block Text, Footnote Block Text, Source Code, Footnote Text, Definition Term, Definition, Caption, Table Caption, Image Caption, Figure, Captioned Figure, TOC Heading.

**Character styles**: Default Paragraph Font, Verbatim Char, Footnote Reference, Hyperlink, Section Number.

**Table style**: Table.

**Custom block styles** (via `custom-style` attribute):
```markdown
::: {custom-style="My Special Style"}
This paragraph gets the "My Special Style" style.
:::
```

## ODT Customization

```bash
pandoc -o custom-reference.odt --print-default-data-file reference.odt
```
Open in LibreOffice, modify styles, save. Use `--reference-doc=custom-reference.odt`.

## PowerPoint Customization

Templates included with MS PowerPoint 2013+ work. Required layout names:
- Title Slide, Title and Content, Section Header, Two Content, Comparison, Content with Caption, Blank.

```bash
pandoc -o custom-reference.pptx --print-default-data-file reference.pptx
```

**Layout choice** (automatic based on content):
- **Title Slide**: Initial slide from metadata (title, author, date)
- **Section Header**: Title slides (heading above slide level)
- **Two Content**: Two-column slides (div.columns with div.column)
- **Comparison**: Two-column with text + non-text (image/table)
- **Content with Caption**: Text followed by non-text
- **Blank**: Only blank content or speaker notes
- **Title and Content**: Default for everything else

## Slide Shows

```bash
# PowerPoint
pandoc -t pptx slides.md -o presentation.pptx

# Beamer (LaTeX PDF)
pandoc -t beamer slides.md -o presentation.pdf --pdf-engine=xelatex

# Reveal.js
pandoc -s -t revealjs slides.md -o presentation.html

# S5, Slidy, Slideous, DZSlides
pandoc -s -t slidy slides.md -o presentation.html
pandoc -s -t s5 slides.md -o presentation.html
pandoc -s -t slideous slides.md -o presentation.html
pandoc -s -t dzslides slides.md -o presentation.html

# Set slide level (which heading level creates slides)
pandoc -t pptx --slide-level=2 slides.md -o presentation.pptx

# Incremental lists
pandoc -t pptx -i slides.md -o presentation.pptx

# Beamer theme
pandoc -t beamer -V theme:Warsaw -V colortheme:beaver slides.md -o presentation.pdf

# Reveal.js theme
pandoc -s -t revealjs -V theme=moon slides.md -o presentation.html

# Self-contained reveal.js
pandoc -s -t revealjs --embed-resources slides.md -o presentation.html

# Speaker notes (reveal.js, pptx, beamer)
::: notes
This is a speaker note.
:::

# PowerPoint title slide speaker notes (via metadata)
---
title: My Talk
author: Jane Doe
notes: |
  Welcome everyone. Remember to introduce yourself.
---

# Pauses within a slide (not for PPTX)
content before
. . .
content after

# Columns
:::::::::::::: {.columns}
::: {.column width="40%"}
Left column
:::
::: {.column width="60%"}
Right column
:::
::::::::::::::

# Background images (reveal.js, beamer, pptx)
## {background-image="/path/to/image.jpg"}
```

## Supported Formats

**Input**: markdown, gfm, commonmark, commonmark_x, html, latex, docx, odt, epub, pptx, rtf, csv, tsv, org, rst, mediawiki, textile, json, ipynb, jira, djot, typst, vimwiki, xml, native, bibtex, biblatex, csljson, ris, docbook, jats, haddock, man, mdoc, fb2, opml, dokuwiki, muse, t2t, twiki, tikiwiki, creole, endnotexml, asciidoc, xlsx, pod, and more.

**Output**: markdown, gfm, commonmark, html, html4, html5, latex, docx, odt, epub, epub2, epub3, pptx, pdf, rtf, plain, beamer, revealjs, slidy, s5, dzslides, slideous, typst, context, man, ms, texinfo, opendocument, icml, ipynb, rst, asciidoc, mediawiki, textile, jats, tei, vimdoc, chunkedhtml, fb2, docbook, docbook4, docbook5, jats_archiving, jats_articleauthoring, jats_publishing, json, native, xml, ansi, bbcode, markua, xwiki, zimwiki, bibtex, biblatex, csljson, and more.

List formats: `pandoc --list-input-formats` / `pandoc --list-output-formats`

## Metadata in Markdown

```markdown
---
title: "Document Title"
author: "Author Name"
date: 2026-04-12
lang: zh-CN
subtitle: "Optional Subtitle"
abstract: "Optional abstract"
keywords: [keyword1, keyword2]
subject: "Document subject"
description: "Document description"
category: "Document category"
toc: true
---

Content here...
```

Multiple authors:
```markdown
---
author:
  - Aristotle
  - Peter Abelard
---
```

Structured authors:
```markdown
---
author:
  - name: Author One
    affiliation: University of Somewhere
  - name: Author Two
    affiliation: University of Nowhere
---
```

## Extensions

Enable/disable per format: `-f markdown+footnotes-tex_math_dollars` or `-f gfm+raw_html`.

Common useful extensions:
- `+footnotes` — footnotes
- `+inline_notes` — inline footnotes `^[note text]`
- `+tex_math_dollars` — `$...$` inline math, `$$...$$` display math
- `+raw_html` — raw HTML in Markdown
- `+smart` — smart typography (em dashes, quotes, etc.)
- `+yaml_metadata_block` — YAML front matter
- `+table_captions` — table captions
- `+implicit_figures` — standalone images become figures
- `+fenced_divs` — `:::` fenced divs
- `+bracketed_spans` — `[text]{.class}` spans
- `+citations` — citation syntax `@key`
- `+definition_lists` — definition lists
- `+fancy_lists` — ordered lists with letters/roman numerals
- `+task_lists` — `- [ ]` / `- [x]` task lists
- `+example_lists` — `@` numbered examples
- `+pipe_tables` — pipe tables
- `+grid_tables` — grid tables
- `+emoji` — `:smile:` emoji parsing
- `+alerts` — GitHub-style `> [!TIP]` alerts
- `-` prefix disables: `-smart`, `-raw_html`

List: `pandoc --list-extensions=markdown`

## Filters & Lua Filters

```bash
# JSON filter
pandoc --filter ./filter.py input.md -o output.html

# Lua filter
pandoc --lua-filter=./filter.lua input.md -o output.html

# Combine filters (applied in command-line order)
pandoc --filter ./first.py --lua-filter=./second.lua -C input.md -o output.html

# Lua filter path lookup order:
# 1. Specified path (full or relative)
# 2. $DATADIR/filters
# JSON filter lookup adds: 3. $PATH (executable only)
```

## Citations

```bash
# With citeproc
pandoc --citeproc --bibliography=refs.bib --csl=apa.csl input.md -o output.docx

# In-text citation syntax
@key                    # Author-in-text
[@key]                  # Parenthetical
[@key, p. 33]           # With locator
[-@key]                 # Suppress author
[@key1; @key2]          # Multiple
see [@key, pp. 33-35]   # With prefix/suffix

# Include all references without citing
nocite: |
  @*

# Custom bibliography placement
::: {#refs}
:::

# Suppress bibliography
suppress-bibliography: true
```

**Bibliography formats**: BibLaTeX (.bib), BibTeX (.bibtex), CSL JSON (.json), CSL YAML (.yaml), RIS (.ris).

## Common Patterns

```bash
# Concatenate multiple files into book
pandoc ch1.md ch2.md ch3.md -o book.docx -s --toc

# Convert web page
pandoc -f html -t markdown https://example.com -o page.md

# Batch convert (shell)
for f in *.md; do pandoc "$f" -o "${f%.md}.docx" -s; done

# Extract text from Word (for processing)
pandoc document.docx -t plain -o text.txt

# Markdown to styled HTML with TOC
pandoc -s --toc --toc-depth=2 --css=style.css --metadata title="Report" input.md -o output.html

# Number sections with offset
pandoc -s --number-sections --number-offset=5 input.md -o output.docx

# EPUB with metadata
pandoc -s --toc --epub-cover-image=cover.jpg --metadata lang=zh-CN \
  --css=epub.css input.md -o output.epub

# Chunked HTML (split into multiple files)
pandoc -s --toc -t chunkedhtml input.md -o output

# Jupyter notebook
pandoc input.ipynb -o output.md
pandoc input.md -o output.ipynb

# Convert between bibliography formats
pandoc chem.bib -s -f biblatex -t csljson -o chem.json
pandoc chem.json -s -f csljson -t biblatex -o chem.bib

# Shift heading levels (e.g., HTML docs with H1 title → make H2 the top section)
pandoc --shift-heading-level-by=-1 input.md -o output.md
```

## Troubleshooting

- **PDF fails**: Ensure LaTeX is installed (`which pdflatex`). Try `--pdf-engine=xelatex` for CJK.
- **Chinese garbled**: Use `--pdf-engine=xelatex -V CJKmainfont="FontName"`.
- **Images not found**: Use `--resource-path=.:images` to set search paths.
- **Missing styles in DOCX**: Use `--reference-doc=reference.docx`.
- **Code blocks not highlighted**: Use `--syntax-highlighting=pygments` (not `--highlight-style`).
- **List all extensions**: `pandoc --list-extensions=markdown`
- **Debug PDF**: Output intermediate: `-o output.tex` instead of `.pdf`.
- **Exit codes**: See `references/advanced.md` for full exit code table.
- **Untrusted input**: Use `--sandbox` to limit IO operations.

## Advanced Reference

For detailed template variables, custom writers, Lua scripting, citation management, EPUB creation, chunked HTML, and exit codes, see [references/advanced.md](references/advanced.md).
