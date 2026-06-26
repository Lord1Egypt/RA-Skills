# Pandoc Advanced Reference

## Exit Codes

| Code | Error |
|---|---|
| 0 | Success |
| 1 | PandocIOError |
| 3 | PandocFailOnWarningError |
| 4 | PandocAppError |
| 5 | PandocTemplateError |
| 6 | PandocOptionError |
| 21 | PandocUnknownReaderError |
| 22 | PandocUnknownWriterError |
| 23 | PandocUnsupportedExtensionError |
| 24 | PandocCiteprocError |
| 25 | PandocBibliographyError |
| 31 | PandocEpubSubdirectoryError |
| 43 | PandocPDFError |
| 44 | PandocXMLError |
| 47 | PandocPDFProgramNotFoundError |
| 61 | PandocHttpError |
| 62 | PandocShouldNeverHappenError |
| 63 | PandocSomeError |
| 64 | PandocParseError |
| 66 | PandocMakePDFError |
| 67 | PandocSyntaxMapError |
| 83 | PandocFilterError |
| 84 | PandocLuaError |
| 89 | PandocNoScriptingEngine |
| 91 | PandocMacroLoop |
| 92 | PandocUTF8DecodingError |
| 93 | PandocIpynbDecodingError |
| 94 | PandocUnsupportedCharsetError |
| 95 | PandocInputNotTextError |
| 97 | PandocCouldNotFindDataFileError |
| 98 | PandocCouldNotFindMetadataFileError |
| 99 | PandocResourceNotFound |

## Template Variables

### Metadata Variables
Set via YAML front matter or `-M/--metadata`:

| Variable | Description |
|---|---|
| `title` | Document title |
| `title-meta` | PDF/HTML metadata title (without body title) |
| `author` | Author(s) (string or list) |
| `author-meta` | PDF/HTML metadata author |
| `date` | Date |
| `date-meta` | PDF/HTML metadata date |
| `lang` | Language (e.g., `zh-CN`, `en`), BCP 47 tags |
| `subtitle` | Subtitle (HTML, EPUB, LaTeX, ConTeXt, docx) |
| `abstract` | Abstract text (HTML, LaTeX, ConTeXt, AsciiDoc, docx) |
| `abstract-title` | Title of abstract (HTML, EPUB, docx, Typst) |
| `keywords` | Keywords (HTML, PDF, ODT, pptx, docx, AsciiDoc) |
| `subject` | Subject (ODT, PDF, docx, EPUB, pptx) |
| `description` | Description (ODT, docx, pptx) |
| `category` | Category (docx, pptx) |
| `copyright` | Copyright |
| `pagetitle` | HTML page title (defaults to title) |
| `institute` | Institution (Beamer) |

### CJK / Chinese Variables
| Variable | Description |
|---|---|
| `CJKmainfont` | CJK main font (XeLaTeX/LuaLaTeX) |
| `CJKsansfont` | CJK sans-serif font |
| `CJKmonofont` | CJK monospace font |
| `mainfont` | Latin main font |
| `sansfont` | Latin sans-serif font |
| `monofont` | Latin monospace font |

### LaTeX Variables
| Variable | Description |
|---|---|
| `classoption` | Document class options |
| `documentclass` | LaTeX class (article, report, book) |
| `header-includes` | Raw LaTeX for header |
| `include-before` | Content before body |
| `include-after` | Content after body |
| `toc` | Include TOC |
| `toc-depth` | TOC nesting depth |
| `toc-title` | TOC heading text |
| `lof` | List of figures |
| `lot` | List of tables |
| `bibliography` | Bibliography file |
| `csl` | CSL style file |
| `nocite` | Include uncited items |
| `secnumdepth` | Section numbering depth |
| `geometry` | Page geometry (e.g., `margin=1in`) |
| `linestretch` | Line spacing |
| `fontsize` | Font size (e.g., `12pt`) |
| `papersize` | Paper size (a4, letter) |
| `margin-top`, `margin-bottom`, `margin-left`, `margin-right` | Page margins |
| `colorlinks` | `true` for colored links |
| `linkcolor` | Link color (e.g., `blue`) |
| `urlcolor` | URL color |
| `citecolor` | Citation color |
| `urlcolor` | URL color |
| `toccolor` | TOC link color |
| `links-as-notes` | `true` to show URLs as footnotes |

### HTML Variables
| Variable | Description |
|---|---|
| `css` | CSS stylesheet(s) |
| `header-includes` | Raw HTML for `<head>` |
| `include-before` | Content after `<body>` |
| `include-after` | Content before `</body>` |
| `lang` | Language for HTML lang attribute |
| `dir` | Text direction (ltr or rtl) |

### HTML Math Variables
| Variable | Description |
|---|---|
| `math` | Math rendering method |
| `mathjax` | MathJax URL (for `--mathjax`) |
| `katex` | KaTeX URL (for `--katex`) |
| `webtex` | WebTeX URL (for `--webtex`) |
| `gladtex` | GladTeX boolean |

### HTML Slide Variables
| Variable | Description |
|---|---|
| `theme` | Reveal.js / Slidy / S5 / Slideous theme |
| `colortheme` | Beamer color theme |
| `fonttheme` | Beamer font theme |
| `innertheme` | Beamer inner theme |
| `outertheme` | Beamer outer theme |
| `fontfamily` | Font family |
| `fontsize` | Base font size |
| `s5-url`, `slidy-url`, `slideous-url`, `revealjs-url` | JS/CSS URL paths |
| `title-slide-attributes` | Attributes for reveal.js/pptx title slide |
| `parallaxBackgroundImage` | Reveal.js parallax background |
| `parallaxBackgroundSize` | Reveal.js parallax size |
| `background-image` | Background image for all slides (beamer, reveal.js, pptx) |

### PowerPoint Variables
| Variable | Description |
|---|---|
| `aspectratio` | 43 (default) or 169 |
| `navigation` | symbols, frames, or empty |
| `incremental` | true/false |

### Variables Set Automatically
| Variable | Description |
|---|---|
| `sourcefile` | Source file path |
| `outputfile` | Output file path |
| `date` | Current date if not set in metadata |
| `lang` | Locale language if not set |
| `fontsize` | Default font size for format |
| `papersize` | Default paper size for format |
| `documentclass` | Default document class for format |

## Defaults Files

Place in `~/.local/share/pandoc/defaults/` (YAML or JSON):

```yaml
# ~/.local/share/pandoc/defaults/docx-chinese.yaml
from: markdown
to: docx
standalone: true
metadata:
  lang: zh-CN
variables:
  CJKmainfont: "Noto Sans CJK SC"
toc: true
toc-depth: 3
```

Usage: `pandoc -d docx-chinese input.md -o output.docx`

**Environment variable interpolation** in file path fields:
```yaml
csl: ${HOME}/mycsldir/special.csl   # User home
epub-cover-image: ${.}/cover.jpg     # Dir containing defaults file
resource-path:
  - .
  - ${.}/images
```

**Defaults file key mappings** (selected):
| Command line | Defaults file |
|---|---|
| `--from FORMAT` | `from:` / `reader:` |
| `--to FORMAT` | `to:` / `writer:` |
| `--output FILE` | `output-file:` |
| `--standalone` | `standalone: true` |
| `--metadata key=val` | `metadata: {key: val}` |
| `--variable key=val` | `variables: {key: val}` |
| `--toc` | `toc: true` |
| `--number-sections` | `number-sections: true` |
| `--pdf-engine xelatex` | `pdf-engine: xelatex` |
| `--citeproc` | `citeproc: true` |
| `--bibliography refs.bib` | `bibliography: refs.bib` |
| `--verbose` | `verbosity: INFO` |
| `--quiet` | `verbosity: ERROR` |

Multiple defaults combine; command-line values merge with defaults (don't replace for repeatable options like --metadata, --css, --filter).

## EPUB Creation

```bash
# Basic EPUB
pandoc -s --toc input.md -o output.epub

# With metadata and cover
pandoc -s --toc --metadata title="My Book" --metadata author="Author" \
  --metadata lang=zh-CN --epub-cover-image=cover.jpg --css=epub.css \
  input.md -o output.epub

# From multiple chapters
pandoc -s --toc ch1.md ch2.md ch3.md -o book.epub \
  --metadata title="Book Title"

# Keep footnotes separate per file
pandoc -s --toc --file-scope ch1.md ch2.md ch3.md -o book.epub

# Embed custom fonts
pandoc -s --toc --epub-embed-font=DejaVuSans-Regular.ttf \
  --epub-embed-font=DejaVuSans-Bold.ttf input.md -o output.epub

# EPUB metadata via XML
pandoc -s --toc --epub-metadata=meta.xml input.md -o output.epub

# Custom chapter split level (default 1)
pandoc -s --toc --split-level=2 input.md -o output.epub

# Suppress title page
pandoc -s --toc --epub-title-page=false input.md -o output.epub
```

**EPUB metadata YAML fields**: title (string or list with type), creator (string or list with role), identifier, publisher, rights, date, lang, subject, description, type, format, relation, coverage, belongs-to-collection, group-position, cover-image, css, page-progression-direction (ltr/rtl), accessibility features/summary/hazards/modes.

## Chunked HTML

```bash
# Create chunked HTML (zip archive of linked HTML files)
pandoc -s --toc -t chunkedhtml input.md -o output.zip

# Or output to directory (if no extension)
pandoc -s --toc -t chunkedhtml input.md -o output_dir

# Custom chunk template
pandoc -s --toc -t chunkedhtml --chunk-template="%i.html" input.md -o output

# Custom split level (default: level-1 headings)
pandoc -s --toc -t chunkedhtml --split-level=2 input.md -o output
```

## Template Syntax

Delimiters: `$...$` or `${...}` (can mix). Literal `$` → `$$`.

```text
$if(foo)$content$endif$           # Conditional
$if(foo)$yes$else$no$endif$       # If/else
${if(foo)}yes${endif}

$for(item)$$item$$endfor$         # Loop
$for(item)$$item$$sep$, $endfor$  # Loop with separator
${for(item)}${item}${sep}, ${endfor}

$it.key$                          # Anaphoric keyword in loops
$for(author)$  $it.name$ ($it.affiliation$) $endfor$

$partial_name()                   # Include partial template
${ styles() }                     # Same with braces
${ articles:bibentry() }          # Apply partial to each item

${ foo/uppercase }                # Pipe (transform)
${ foo/alpha }                    # Array index → letter (a, b, c...)
${ foo/roman }                    # Array index → roman numeral
${ foo/left 20 "|" " |" }        # Left-aligned in 20 chars
${ foo/right 10 " |" }           # Right-aligned in 10 chars
```

**Available pipes**: pairs, uppercase, lowercase, length, reverse, first, last, rest, allbutlast, chomp, nowrap, alpha, roman, left, right, center.

## Pandoc Server Mode

```bash
# Start server
pandoc --server localhost:3000

# Convert via HTTP
curl -X POST http://localhost:3000 \
  --data-binary @input.md \
  -H "Content-Type: text/markdown" \
  -H "Accept: application/vnd.openxmlformats-officedocument.wordprocessingml.document" \
  -o output.docx
```

## Pandoc as Lua Interpreter

```bash
pandoc -l script.lua
```

## Custom Readers and Writers

Custom Lua readers/writers can be specified as file paths in `-f` or `-t` options. They must return appropriate functions.

## Reproducible Builds

For LaTeX: the `--lua-filter` option can be used with a filter that normalizes metadata.
For ConTeXt, WeasyPrint, Prince XML, Typst: see the manual's "Reproducible builds" section.

## Accessible PDFs

LaTeX, ConTeXt, WeasyPrint, Prince XML, and Typst all support generating accessible (tagged) PDFs. See the manual's specific instructions for each engine.
