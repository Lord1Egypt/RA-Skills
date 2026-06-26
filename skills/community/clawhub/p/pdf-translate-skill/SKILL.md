---
name: pdf-translator
description: Translate PDF documents while preserving original formatting. Converts PDF pages to images for layout analysis, extracts text and embedded images, translates content using agent's multilingual capabilities, and generates LaTeX code to recreate the original document structure with translated text. Special support for arXiv papers: when user provides arXiv ID (e.g., "2310.12345") or arXiv URL (e.g., "https://arxiv.org/abs/2310.12345" or "https://arxiv.org/pdf/2310.12345.pdf"), automatically download the source TeX files, translate the LaTeX content, and compile to PDF.
---

# PDF Translator Skill

A comprehensive skill for translating PDF documents while maintaining their original layout, formatting, and visual structure. This skill combines multimodal analysis, text extraction, machine translation, and LaTeX typesetting to produce high-quality translated PDFs.

## Two Translation Modes

This skill supports **two distinct translation workflows**. Choose the appropriate mode based on your input:

| Mode | Input | Method | Quality |
|------|-------|--------|---------|
| **arXiv Mode** | arXiv ID or URL | Download source TeX → Translate → Compile | Higher (preserves all formatting) |
| **Local PDF Mode** | Local PDF file | PDF → Images → Layout Analysis → Translate → Recreate in LaTeX | Good (reconstructed layout) |

### When to Use Each Mode

**Use arXiv Mode when:**
- User provides an arXiv ID like `2310.12345`
- User provides an arXiv URL like `https://arxiv.org/abs/2310.12345` or `https://arxiv.org/pdf/2310.12345.pdf`
- The paper has available TeX source files

**Use Local PDF Mode when:**
- User provides a local PDF file path
- The PDF is not from arXiv
- The arXiv paper does not have source available (only PDF)

**Fallback rule:** If arXiv source download fails, fall back to Local PDF Mode.

## Prerequisites

### Required Software
- **Python 3.8+** with pip
- **PyMuPDF** (`pip install pymupdf pillow`)
- **XeLaTeX** (TeX Live or MiKTeX) for PDF compilation
- **ctex LaTeX package** for Chinese support
- **wget or curl** (for downloading arXiv source files)

### Installation Commands
```bash
# Python dependencies
pip install pymupdf pillow requests

# LaTeX (choose one)
# Ubuntu/Debian:
sudo apt install texlive-xetex texlive-lang-chinese

# macOS (Homebrew):
brew install mactex

# Windows: Download MiKTeX from https://miktex.org/
```

---

# Mode 1: arXiv Paper Translation

> **Preferred method** for arXiv papers because source TeX files preserve all formatting automatically.

## Workflow

```
arXiv ID/URL → Download Source TeX → Translate TeX Content → Compile → PDF Output
```

**Advantages over Local PDF Mode:**
- Source TeX files preserve all formatting automatically
- No need for layout analysis or image extraction
- Higher quality translation output
- Faster processing

### Step 1: Detect arXiv Input

Detect if user provided:
- **arXiv ID**: e.g., `2310.12345`, `hep-th/9901001`
- **arXiv URL**: e.g., 
  - `https://arxiv.org/abs/2310.12345`
  - `https://arxiv.org/pdf/2310.12345.pdf`
  - `https://arxiv.org/abs/hep-th/9901001`

**Extract arXiv ID** from input:
- From URL: extract the ID after `/abs/` or `/pdf/`
- From direct ID: use as-is

### Step 2: Download arXiv Source

Download the source TeX files from arXiv:

```bash
# Using the provided script
python scripts/download_arxiv_source.py 2310.12345 output_dir/

# Or with URL
python scripts/download_arxiv_source.py https://arxiv.org/abs/2310.12345 ./
```

**Manual download:**
```bash
# Use arXiv's official source download
# Navigate to: https://arxiv.org/e-print/{arxiv_id}
# Download format: .tar.gz containing all source files

# Or use wget
wget -O source.tar.gz https://arxiv.org/e-print/2310.12345
tar -xzf source.tar.gz
```

The downloaded archive typically contains:
- Main `.tex` file (usually named after the paper ID)
- Style files (`.bst`, `.cls`)
- Bibliography (`.bib`)
- Figures (`.pdf`, `.png`, `.eps`)
- Other source files

### Step 3: Identify Main TeX File

Find the main TeX file in the extracted contents:
- Usually named after the paper ID (e.g., `main.tex`, `paper.tex`)
- Check for `\documentclass` or `\begin{document}` to identify the entry point
- May need to inspect multiple `.tex` files to find the one with `\maketitle` or `\begin{document}`

### Step 4: Translate TeX Content

Read and translate the main TeX file:

**1. Identify translatable content:**
- Text between `{` and `}` in regular text environments
- Section titles, captions, footnotes
- Abstract content

**2. Preserve non-translatable elements:**
- Math formulas (`$...$`, `\[...\]`)
- LaTeX commands (`\ref{...}`, `\cite{...}`)
- Figure/table commands
- Code blocks

**3. Translation approach:**
- Translate text content while keeping LaTeX markup intact
- Use `ctex` or `\usepackage{ctex}` for Chinese support
- Maintain paragraph structure

**4. Key translation rules:**
- Keep all `\section{...}`, `\subsection{...}` content - translate the text inside
- Keep all `\caption{...}` content - translate inside
- Keep all `\footnote{...}` content - translate inside
- Keep math formulas completely unchanged
- Keep `\includegraphics{}` paths unchanged
- Keep `\bibliography{}` unchanged
- Translate abstract text

**Example translation:**
```latex
% Original:
\section{Introduction}
We present a new method for...

% Translated:
\section{介绍}
我们提出了一种新的方法...
```

### Step 5: Compile Translated TeX

**IMPORTANT: Compile THREE times to resolve all citations and references:**

```bash
# Ensure Chinese support
# Add to preamble if not present:
\usepackage{ctex}

# Compile THREE times to resolve all citations and references
xelatex translated.tex  # Pass 1: Initial compilation
xelatex translated.tex  # Pass 2: Resolve citations/references
xelatex translated.tex  # Pass 3: Final resolution
```

Or use the provided script:
```bash
python scripts/compile_latex.py translated.tex output_dir/ --passes 3
```

**Why 3 passes?**
- **Pass 1**: Processes document structure, outputs citations as "?"
- **Pass 2**: Reads citation info from auxiliary file, resolves references
- **Pass 3**: Final resolution ensures all `\ref{}`, `\cite{}`, and bibliography are correctly rendered

### Step 6: Handle Dependencies

If compilation fails due to missing packages or files:
1. Check for missing `.sty`, `.cls`, or `.bst` files
2. Copy missing files from the original arXiv source
3. Check `\graphicspath` for figure locations
4. Ensure all `\input{}` files are present

### arXiv Translation Example

**User Input:**
> "请翻译这篇 arXiv 论文: https://arxiv.org/abs/2310.12345"

**Workflow Execution:**

**Step 1: Detect arXiv ID**
- URL: `https://arxiv.org/abs/2310.12345`
- Extracted ID: `2310.12345`

**Step 2: Download Source**
```bash
python scripts/download_arxiv_source.py 2310.12345 ./arxiv_src
```

**Step 3: Identify Main TeX File**
- Found: `main.tex` (the main entry point)
- Also found: `refs.bib`, `figures/`, `style files`

**Step 4: Translate TeX Content**
- Read `main.tex`
- Translate section titles: `\section{Abstract}` → `\section{摘要}`
- Translate body text while preserving:
  - Math formulas: `$E = mc^2$` (unchanged)
  - Citations: `\cite{author2023}` (unchanged)
  - Figures: `\includegraphics{fig1.pdf}` (unchanged)
- Output: `main_zh.tex`

**Step 5: Add Chinese Support**
- Ensure `\usepackage{ctex}` or `\usepackage[UTF8]{ctex}` is in preamble
- If not present, add it

**Step 6: Compile to PDF**
```bash
python scripts/compile_latex.py main_zh.tex ./output --passes 3
```

**Step 7: Deliver Output**
- Translated PDF saved to: `./output/main_zh.pdf`

### arXiv Specific Issues

**Cannot Download Source:**
- Check if the paper has source available (not all papers have TeX sources)
- Try alternative URL: `https://arxiv.org/e-print/{arxiv_id}`
- Some older papers may not have source available
- **Fallback:** If download fails, use Local PDF Mode

**Missing Package Errors:**
- Copy missing `.sty`, `.cls` files from the original download to your working directory
- Check for `\usepackage{...}` commands and ensure all referenced files exist
- Use `kpsewhich` to check if packages are installed system-wide

**arXiv ID Format:**
- **New format**: `YYMM.NNNNN` (e.g., `2310.12345`)
- **Old format**: `archive/YYMMNNN` (e.g., `hep-th/9901001`)
- Both formats work with the download URL

---

# Mode 2: Local PDF Translation

> Use this mode when translating local PDF files or when arXiv source is unavailable.

## Workflow

```
PDF Input → Page Images → Layout Analysis → Text Extraction → Translation → LaTeX Generation → PDF Output
```

### Step 1: Convert PDF to Page Images

Convert each PDF page to a high-quality image for multimodal analysis:

```bash
python scripts/pdf_to_images.py input.pdf output_pages/ --dpi 150
```

**Output:**
- `page_001.png`, `page_002.png`, ... (page images)
- `manifest.json` (page dimensions and metadata)

### Step 2: Extract Embedded Images

Extract original images from the PDF for reuse in the translated document:

```bash
python scripts/extract_images.py input.pdf output_extracted/
```

**Output:**
- `images/img_001_01.png`, ... (extracted images)
- `images_manifest.json` (image positions and metadata)

### Step 3: Analyze Layout and Extract Content

For each page image, analyze the layout and extract content:

**Using multimodal analysis:**
1. Describe the page layout structure (columns, sections, headers, footers)
2. Identify text blocks, their positions, and reading order
3. Identify figures, tables, and their captions
4. Note any special formatting (lists, equations, quotes)

**Prompt template for layout analysis:**
```
Analyze this PDF page image and describe:
1. Overall layout structure (columns, margins, alignment)
2. Text blocks with their approximate positions and hierarchy
3. Images, figures, or tables with their locations
4. Any special elements (headers, footers, page numbers, footnotes)

Provide a structured description that can be used to recreate this layout in LaTeX.
```

### Step 4: Translate Text Content

Translate the extracted text while maintaining:
- Technical terms accuracy
- Proper nouns (names, places)
- Formatting markers (emphasis, bold)
- Contextual meaning

**Translation guidelines:**
- Preserve original paragraph structure
- Maintain consistent terminology
- Handle inline formatting (bold, italic, code)
- Keep mathematical formulas unchanged

### Step 5: Generate LaTeX Code

Create LaTeX code that recreates the original layout with translated content.

**Key considerations:**
1. **Document class**: `article` for papers, `report` for longer documents
2. **Page geometry**: Match original margins
3. **Multi-column layouts**: Use `multicol` package
4. **Figures**: Use `\includegraphics` with proper positioning (Insert the extracted images into their original positions)
5. **Tables**: Recreate with `tabular` or `longtable` (Insert the identical table at its original position)
6. **Chinese support**: Always use `ctex` package with XeLaTeX
7. **Important**: Modify the template format to match the style of the original PDF. Pay special attention to the switching between single-column and double-column layouts.

**Reference:** See `./references/latex_templates.md` for LaTeX generation details.

**Template structure:**
```latex
\documentclass[12pt, a4paper]{article}
\usepackage{ctex}  % Chinese support
\usepackage{graphicx}
\usepackage{geometry}
% ... other packages

\begin{document}
% Translated content here
\end{document}
```

### Step 6: Compile LaTeX to PDF

**IMPORTANT: Compile THREE times to ensure all citations and references are properly resolved:**

```bash
python scripts/compile_latex.py translated.tex output_dir/ --passes 3
```

**Output:**
- `translated.pdf` (final translated document)

**Troubleshooting:** If errors occur, refer to `./references/troubleshooting.md`.

### Working Directory Structure

```
working_dir/
├── input.pdf
├── pages/           # Page images
├── extracted/       # Extracted images
├── translated.tex   # Generated LaTeX
└── output.pdf       # Final result
```

### Page-by-Page Processing

For each page:

1. **View page image** using multimodal capability
2. **Analyze layout structure:**
   - Number of columns
   - Section headings
   - Paragraph blocks
   - Figure/table positions
   - Header/footer content
3. **Extract text content:**
   - Use vision to identify text regions
   - Transcribe text from image (OCR-like)
   - Note formatting (bold, italic, font sizes)
4. **Translate content:**
   - Translate each text block
   - Maintain structure and formatting
   - Handle technical terms appropriately
5. **Generate LaTeX for page:**
   - Apply appropriate layout template
   - Insert translated text
   - Include images with correct positions
   - Handle special elements (tables, equations)

### Document Assembly

1. **Combine all pages into single LaTeX file:**
   - Create `base_template.tex` as foundation
   - Insert page content in order
   - Handle cross-page elements (tables, figures)

2. **Compile to PDF:**
   - Use `scripts/compile_latex.py`
   - Run multiple passes for references

3. **Verify output:**
   - Check all pages rendered correctly
   - Verify images are included
   - Confirm formatting matches original

---

# Common Layout Patterns

## Single Column Document
```latex
\section{Section Title}
Translated paragraph content here.

\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\textwidth]{image.png}
  \caption{Translated caption}
\end{figure}
```

## Two Column Layout
```latex
\begin{multicols}{2}
\section{Left Column}
Content...

\section{Content Spanning}
...
\end{multicols}
```

## Academic Paper Structure
```latex
\title{Translated Title}
\author{Authors}
\maketitle

\begin{abstract}
Translated abstract...
\end{abstract}

\section{Introduction}
Content...

\section{Methods}
Content...

\bibliographystyle{plain}
\bibliography{references}
```

---

# Reference Files

- `references/latex_templates.md` - LaTeX code patterns for various layouts
- `references/troubleshooting.md` - Common issues and solutions

---

# Troubleshooting

## Font Issues
If Chinese characters don't render:
- Ensure XeLaTeX is used (not pdfLaTeX)
- Check ctex package is installed
- Verify system has Chinese fonts installed

## Image Not Found
If images don't appear in output:
- Check `\graphicspath` includes correct directory
- Verify image files exist and are readable
- Use correct file extensions in `\includegraphics`

## Layout Mismatch
If layout differs from original:
- Adjust geometry settings for margins
- Use appropriate figure placement options
- Check for column count differences

## Compilation Errors
If LaTeX compilation fails:
- Check log file for specific errors
- Verify all required packages are installed
- Ensure no syntax errors in generated code

---

# Best Practices

1. **Quality over speed**: Take time to analyze layout accurately
2. **Iterative refinement**: Generate, compile, review, and improve
3. **Preserve semantics**: Maintain document meaning over exact formatting
4. **Handle edge cases**: Be prepared for tables, equations, code blocks
5. **Test compilation**: Verify LaTeX compiles before final output

---

# Limitations

- **Exact pixel-perfect replication**: LaTeX is not a pixel-based layout engine
- **Complex graphics**: Vector illustrations may need to be captured as images
- **Custom fonts**: May require font substitution
- **Dynamic content**: JavaScript or form fields are not supported
- **Encrypted PDFs**: Cannot process password-protected documents

---

# Output Verification Checklist

- [ ] All pages included in output
- [ ] Text correctly translated
- [ ] Images positioned correctly
- [ ] Tables formatted properly
- [ ] No LaTeX compilation errors
- [ ] Chinese characters render correctly
- [ ] Page numbers and headers present
- [ ] Overall formatting matches original

---

# Notes

- **arXiv fallback:** Some arXiv papers don't have source available (only PDF). In this case, fall back to Local PDF Mode.
- **Complex packages:** For papers with complex LaTeX packages, you may need to install additional packages.
- **Download requirement:** The `download_arxiv_source.py` script requires `curl` or `wget` to be installed.
- **Large files:** When the arXiv TeX or PDF file is large, translate it paragraph by paragraph and gradually write the translated content into the TeX file to be compiled.
- **References:** If the file contains references, please keep them in English and do not translate the reference section.
