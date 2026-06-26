# LaTeX Compilation Reference

Production guide for compiling thesis-length documents locally. Covers compiler
selection, installation, workflows, cross-reference auditing, and common pitfalls.

---

## 1. Compiler Comparison

| Compiler | Pros | Cons | Best For |
|----------|------|------|----------|
| **Tectonic** (recommended) | Single binary, auto-downloads packages, no sudo, handles all passes automatically | Less mature ecosystem, slower first run (downloads) | Default choice for new projects |
| **latexmk** | Standard, excellent automation, watches for changes | Requires full TeX Live install (~4 GB) | Teams already on TeX Live |
| **pdflatex + bibtex** (manual) | No wrapper magic, full control | Tedious multi-pass dance, easy to forget a pass | Debugging compilation issues |
| **lualatex** | Native Unicode/OpenType font support, Lua scripting | 2-3x slower than pdflatex | CJK text, custom fonts, Unicode-heavy docs |

**Rule of thumb:** Start with Tectonic. Fall back to latexmk if you hit a
Tectonic-specific bug. Use lualatex only when you need Unicode fonts.

---

## 2. Installing Tectonic

### macOS

```bash
brew install tectonic
```

### Linux

```bash
# Option A: pre-built binary
curl --proto '=https' --tlsv1.2 -fsSL https://drop-sh.fullyjustified.net | sh

# Option B: from source via cargo
cargo install tectonic
```

### Why Tectonic

- No `tlmgr`, no `sudo`, no 4 GB TeX Live download.
- Automatically resolves and downloads only the packages your document needs.
- Runs pdflatex/bibtex passes internally until all references stabilize.
- Reproducible builds: package bundle is versioned.

---

## 3. Compilation Workflows

### Simple (Tectonic)

```bash
tectonic main.tex
```

One command. It runs as many passes as needed and produces `main.pdf`.

### Tectonic v2 (workspace mode)

```bash
tectonic -X compile main.tex
```

Supports `Tectonic.toml` for project-level config.

### latexmk (standard)

```bash
# Single build
latexmk -pdf main.tex

# Continuous watch mode (recompiles on save)
latexmk -pdf -pvc main.tex

# Clean auxiliary files
latexmk -c
```

### Manual multi-pass (for debugging)

```bash
pdflatex main.tex    # Pass 1: generate .aux
bibtex main          # Process citations (no .tex extension)
pdflatex main.tex    # Pass 2: resolve back-references
pdflatex main.tex    # Pass 3: stabilize page numbers
```

Run this sequence when you need to see exactly which pass fails.

### lualatex

```bash
# Replace pdflatex with lualatex in any workflow above
latexmk -lualatex main.tex

# Or manually
lualatex main.tex && bibtex main && lualatex main.tex && lualatex main.tex
```

---

## 4. Cross-Reference Audit

### The Problem

When multiple agents (or authors) write chapters in parallel, collisions happen:
- Duplicate `\label{}` definitions across chapters
- `\ref{}` pointing to labels that were renamed or deleted
- Orphaned labels nobody references
- Missing or misnamed BibTeX keys

These produce silent warnings that become wrong numbers in the PDF.

### The Solution: Automated Audit Script

Create `scripts/cross_ref_audit.py` and run it before every final compile.

```bash
python scripts/cross_ref_audit.py report_dir/
```

What it checks:
1. **Duplicate labels** -- same `\label{X}` in two files
2. **Undefined references** -- `\ref{X}` or `\cref{X}` with no matching `\label{X}`
3. **Orphaned labels** -- defined but never referenced (potential dead code)
4. **BibTeX issues** -- `\cite{key}` with no matching entry in `.bib`
5. **Naming convention violations** -- labels missing chapter prefix

### Prevention: Prefix Convention

Enforce chapter prefixes to eliminate collisions:

```latex
% Chapter 3 — all labels start with ch3:
\label{fig:ch3:architecture}
\label{tab:ch3:comparison}
\label{sec:ch3:design}

% Chapter 5 — all labels start with ch5:
\label{fig:ch5:results}
\label{tab:ch5:ablation}
```

Pattern: `{type}:{chapter}:{descriptive_name}`

Types: `fig`, `tab`, `sec`, `eq`, `alg`, `lst`, `app`

---

## 5. Common Compilation Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Undefined control sequence` | Missing `\usepackage{}` | Identify the command, add the package to `preamble.tex` |
| `Missing \begin{document}` | Syntax error in preamble | Check for unmatched braces or bad `\usepackage` options before `\begin{document}` |
| `Overfull \hbox` | Long word or URL won't break | Wrap URLs with `\url{}`, add `\sloppy` locally, or use `\linebreak` |
| `I couldn't open file name.bib` | Wrong `\bibliography{}` path | Use relative path from `main.tex` location, no `.bib` extension |
| `Option clash for package X` | Package loaded twice with different options | Load the package once in `preamble.tex` with all needed options |
| `Unicode char not set up for use with LaTeX` | Non-ASCII character with pdflatex | Switch to lualatex, or add `\usepackage[utf8]{inputenc}` |
| `Too many unprocessed floats` | Too many figures/tables queued | Add `\clearpage` or use `[H]` placement from `float` package |
| `Citation undefined` | bibtex pass not run, or key typo | Run bibtex, check key spelling matches `.bib` entry |

### Debugging Strategy

1. Read the **first** error, not the last. Later errors cascade from earlier ones.
2. Isolate: comment out `\input{}` chapters with binary search to find the offending file.
3. Check the `.log` file for the full error context (the terminal truncates).

---

## 6. Multi-File Project Structure

```
report/
├── main.tex              # Master file: \input{} all others
├── preamble.tex          # All \usepackage{} declarations
├── front_matter.tex      # Title page, abstract, acknowledgements, TOC
├── chapters/
│   ├── ch1_introduction.tex
│   ├── ch2_literature_review.tex
│   ├── ch3_methodology.tex
│   ├── ch4_implementation.tex
│   ├── ch5_evaluation.tex
│   └── ch6_conclusion.tex
├── appendices/
│   ├── app_a_supplementary.tex
│   └── app_b_code.tex
├── figures/               # PDF for vector, PNG for raster
│   ├── generated/         # Script-generated figures
│   └── screenshots/
├── references.bib         # Single BibTeX database
└── scripts/
    ├── cross_ref_audit.py
    └── build.sh
```

### main.tex Skeleton

```latex
\documentclass[12pt,a4paper]{report}
\input{preamble}

\begin{document}
\input{front_matter}

\input{chapters/ch1_introduction}
\input{chapters/ch2_literature_review}
% ...

\bibliographystyle{plainnat}
\bibliography{references}

\appendix
\input{appendices/app_a_supplementary}
\end{document}
```

Keep `main.tex` minimal. All package imports go in `preamble.tex`.

---

## 7. Useful LaTeX Packages for Thesis

### Tables

| Package | Purpose |
|---------|---------|
| `booktabs` | Professional horizontal rules (`\toprule`, `\midrule`, `\bottomrule`) |
| `multirow` | Cells spanning multiple rows |
| `longtable` | Tables that break across pages |
| `tabularx` | Auto-width columns |

### Figures

| Package | Purpose |
|---------|---------|
| `graphicx` | `\includegraphics{}` |
| `subcaption` | Sub-figures with `(a)`, `(b)` captions |
| `float` | `[H]` placement specifier |

### Algorithms and Code

| Package | Purpose |
|---------|---------|
| `algorithm2e` | Pseudocode with `if/while/for` keywords |
| `algorithmicx` | Alternative pseudocode style |
| `listings` | Code listings (no external deps) |
| `minted` | Syntax-highlighted code (requires Pygments) |

### References and Navigation

| Package | Purpose |
|---------|---------|
| `natbib` | Author-year and numeric citation styles |
| `biblatex` | Modern alternative to natbib (more flexible) |
| `hyperref` | Clickable cross-references and URLs. **Load last.** |
| `cleveref` | Smart `\cref{}` that auto-inserts "Figure", "Table", etc. Load after hyperref. |

### Layout

| Package | Purpose |
|---------|---------|
| `geometry` | Set margins: `\usepackage[margin=2.5cm]{geometry}` |
| `setspace` | Line spacing: `\usepackage{setspace}` then `\onehalfspacing` |
| `fancyhdr` | Custom headers and footers |
| `titlesec` | Customize chapter/section heading format |

### Load Order (matters)

```latex
% preamble.tex — order-sensitive packages at the end
\usepackage{geometry}
\usepackage{graphicx}
\usepackage{booktabs}
% ... all other packages ...
\usepackage{natbib}
\usepackage[colorlinks=true]{hyperref}   % SECOND TO LAST
\usepackage[nameinlink]{cleveref}         % LAST
```

---

## 8. zsh Gotchas

### History expansion breaks grep

```bash
# BROKEN in zsh — the ! triggers history expansion
grep '\\cite{' chapters/*.tex

# Fix option 1: use noglob
noglob grep '\\cite{' chapters/*.tex

# Fix option 2: use double quotes (escapes !)
grep "\\\\cite{" chapters/*.tex

# Fix option 3 (recommended): use Python instead
python3 -c "
import pathlib, re
for f in pathlib.Path('chapters').glob('*.tex'):
    for i, line in enumerate(f.read_text().splitlines(), 1):
        if '\\cite{' in line:
            print(f'{f}:{i}: {line.strip()}')
"
```

### Backslash escaping

LaTeX commands are full of backslashes. In zsh:
- Single quotes preserve backslashes literally: `'\label{}'`
- Double quotes require doubling: `"\\label{}"`
- Heredocs are safest for multi-line LaTeX in shell scripts

```bash
# Safe way to write LaTeX from shell
cat <<'EOF' > test.tex
\documentclass{article}
\begin{document}
Hello \LaTeX
\end{document}
EOF
```

Note the `'EOF'` (quoted) which prevents shell expansion inside the heredoc.

### Build script tip

```bash
#!/bin/zsh
# scripts/build.sh
set -euo pipefail

cd "$(dirname "$0")/.."
python scripts/cross_ref_audit.py . && tectonic main.tex
echo "Build complete: main.pdf ($(wc -c < main.pdf | tr -d ' ') bytes)"
```
