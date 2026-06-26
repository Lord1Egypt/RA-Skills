# Troubleshooting Guide

This guide covers common issues encountered during PDF translation and their solutions.

## Table of Contents

1. [PDF to Image Conversion Issues](#pdf-to-image-conversion-issues)
2. [Image Extraction Problems](#image-extraction-problems)
3. [LaTeX Compilation Errors](#latex-compilation-errors)
4. [Chinese/CJK Rendering Issues](#chinesecjk-rendering-issues)
5. [Layout Problems](#layout-problems)
6. [Performance Issues](#performance-issues)

---

## PDF to Image Conversion Issues

### Error: "PyMuPDF not installed"

**Symptom:** `ModuleNotFoundError: No module named 'fitz'`

**Solution:**
```bash
pip install pymupdf pillow
```

### Error: "PDF file not found"

**Symptom:** FileNotFoundError when running pdf_to_images.py

**Solution:**
- Use absolute path to PDF file
- Check for special characters in path
- Ensure file has .pdf extension

### Low Quality Images

**Symptom:** Blurry or pixelated page images

**Solution:**
- Increase DPI (default is 150, try 300):
  ```bash
  python pdf_to_images.py input.pdf output_dir --dpi 300
  ```

### Memory Error with Large PDFs

**Symptom:** Out of memory when processing large documents

**Solution:**
- Process pages in smaller batches
- Lower DPI for initial analysis
- Close other applications to free memory

---

## Image Extraction Problems

### No Images Extracted

**Symptom:** Empty images/ directory

**Possible Causes:**
1. PDF contains no embedded images (text only)
2. Images are rendered as vector graphics
3. Images are inline within text

**Solution:**
- Check PDF content type
- Use pdf_to_images.py to capture page screenshots instead
- Vector graphics may need to be captured as screenshots

### Corrupted Extracted Images

**Symptom:** Images appear damaged or won't open

**Solution:**
- Try alternative extraction with pdfimages command:
  ```bash
  pdfimages -png input.pdf output_prefix
  ```
- Check if source PDF is corrupted

### Wrong Image Positions

**Symptom:** Image coordinates don't match visual position

**Solution:**
- PDF coordinates start from bottom-left (not top-left)
- Convert coordinates:
  ```python
  # Y coordinate conversion
  page_height = page.rect.height
  top_left_y = page_height - rect.y1
  ```

---

## LaTeX Compilation Errors

### Error: "xelatex not found"

**Symptom:** `xelatex: command not found` or similar

**Solution:**
- Install TeX Live (Linux/Mac):
  ```bash
  # Ubuntu/Debian
  sudo apt install texlive-xetex texlive-lang-chinese
  
  # macOS (Homebrew)
  brew install mactex
  ```
- Install MiKTeX (Windows):
  - Download from https://miktex.org/
  - Include XeLaTeX and Chinese packages

### Error: "Font not found"

**Symptom:** `Font 'SimSun' not found` or similar

**Solution:**
- Check available fonts:
  ```bash
  # Linux
  fc-list :lang=zh
  
  # Windows
  # Check C:\Windows\Fonts\
  ```

- Use fallback fonts:
  ```latex
  \setCJKmainfont{Noto Sans CJK SC}
  % Or let ctex auto-detect:
  \usepackage{ctex}  % Without manual font settings
  ```

### Missing Package Error

**Symptom:** `File 'package.sty' not found`

**Solution:**
- Install missing package:
  ```bash
  # TeX Live
  tlmgr install package-name
  
  # MiKTeX
  # Open MiKTeX Console > Packages > Search and install
  ```

### Compilation Timeout

**Symptom:** Process hangs or takes too long

**Solution:**
- Check for infinite loops in LaTeX code
- Reduce document complexity
- Compile in smaller sections
- Check for very large included images

### Undefined Control Sequence

**Symptom:** `! Undefined control sequence` error

**Solution:**
- Check for typos in command names
- Ensure required packages are loaded
- Common fixes:
  ```latex
  % Add missing packages
  \usepackage{amsmath}    % For math commands
  \usepackage{graphicx}   % For \includegraphics
  \usepackage{booktabs}   % For \toprule, \midrule
  ```

---

## Chinese/CJK Rendering Issues

### Garbled Chinese Characters

**Symptom:** Chinese text appears as boxes or question marks

**Solution:**
- Ensure XeLaTeX is used (not pdfLaTeX):
  ```bash
  xelatex document.tex
  ```
- Add ctex package:
  ```latex
  \usepackage{ctex}
  ```

### Wrong Font for Chinese

**Symptom:** Chinese uses fallback or wrong font

**Solution:**
- Specify CJK fonts:
  ```latex
  \setCJKmainfont{SimSun}[BoldFont=SimHei]
  \setCJKsansfont{Microsoft YaHei}
  ```

### Mixed Language Issues

**Symptom:** English and Chinese don't mix well

**Solution:**
- Use xeCJK for fine control:
  ```latex
  \usepackage{xeCJK}
  \setCJKmainfont{SimSun}
  \setmainfont{Times New Roman}
  ```

---

## Layout Problems

### Content Overflow

**Symptom:** Text or images extend beyond page margins

**Solution:**
- Adjust image sizes:
  ```latex
  \includegraphics[width=\textwidth]{image.png}
  % or
  \includegraphics[scale=0.8]{image.png}
  ```
- Use `\sloppy` for loose line breaking
- Adjust margins in geometry package

### Figures Not Positioned Correctly

**Symptom:** Figures appear on wrong pages

**Solution:**
- Use more specific placement options:
  ```latex
  \begin{figure}[!htbp]  % ! forces attempt to place here
  ```
- For exact placement, use:
  ```latex
  \usepackage{float}
  \begin{figure}[H]  % Exactly here
  ```

### Table Column Width Issues

**Symptom:** Tables overflow page width

**Solution:**
- Use tabularx for auto-width:
  ```latex
  \begin{tabularx}{\textwidth}{X c c}
  ```
- Use longtable for multi-page:
  ```latex
  \begin{longtable}{l c c}
  ```
- Resize table:
  ```latex
  \resizebox{\textwidth}{!}{%
    \begin{tabular}{...}
    ...
    \end{tabular}
  }
  ```

### Paragraph Spacing Issues

**Symptom:** Too much or too little space between paragraphs

**Solution:**
- Adjust globally:
  ```latex
  \setlength{\parskip}{1em}
  \setlength{\parindent}{0em}  % No indent
  ```
- Adjust locally:
  ```latex
  Text here.
  
  \vspace{1em}  % Additional space
  
  Next paragraph.
  ```

---

## Performance Issues

### Slow PDF Processing

**Symptom:** pdf_to_images.py takes very long

**Solution:**
- Reduce DPI for initial analysis
- Process specific pages only:
  ```python
  # Modify script to process range
  for page_num in range(start_page, end_page):
      ...
  ```

### Large Output Files

**Symptom:** Generated PDF is very large

**Solution:**
- Compress images before including:
  ```bash
  # Using ImageMagick
  convert large.png -quality 85 compressed.png
  ```
- Use appropriate image formats:
  - PNG for screenshots/diagrams
  - JPG for photos

### Too Many Auxiliary Files

**Symptom:** Directory cluttered with .aux, .log, etc.

**Solution:**
- The compile_latex.py script auto-cleans these
- Manual cleanup:
  ```bash
  rm *.aux *.log *.out *.toc *.lof *.lot
  ```

---

## Quick Reference: Common Fixes

| Problem | Quick Fix |
|---------|-----------|
| Font missing | `\usepackage{ctex}` + XeLaTeX |
| Image not found | Check `\graphicspath{}` |
| Table too wide | Use `tabularx` or `\resizebox` |
| Chinese garbled | Use XeLaTeX, not pdfLaTeX |
| Figure wrong position | Use `[!htbp]` or `[H]` |
| Compilation fails | Check log file, fix first error |
| Slow compilation | Reduce image sizes, split document |

---

## Getting Help

If issues persist:

1. Check LaTeX log file for detailed errors
2. Search error message on TeX Stack Exchange
3. Try minimal working example (MWE)
4. Check package documentation on CTAN