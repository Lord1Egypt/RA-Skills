# LaTeX Resume Template Reference

This document contains the LaTeX template structure and compilation instructions for the one-page-cv skill.

## Font Selection by OS

Detect the OS first, then choose fonts accordingly:

```bash
uname -s  # Darwin = macOS, Linux = Linux
# Windows: check via systeminfo or $env:OS in PowerShell
```

### macOS (Darwin)
- **English main font**: Times New Roman
- **Chinese font**: PingFang SC (Bold: PingFangSC-Semibold)
- **Mono font**: Maple Mono (if available, otherwise Menlo)

### Windows
- **English main font**: Times New Roman
- **Chinese font**: Microsoft YaHei (Bold: Microsoft YaHei Bold)
- **Mono font**: Maple Mono (if available, otherwise Consolas)

### Linux
- **English main font**: Times New Roman or Liberation Serif (fallback)
- **Chinese font**: Noto Sans CJK SC (Bold: Noto Sans CJK SC Bold)
- **Mono font**: Maple Mono (if available, otherwise DejaVu Sans Mono)

### Maple Mono Detection & Installation

Maple Mono is the preferred monospace font for resumes. Check if it's installed, and offer to install if not:

```bash
# Check if Maple Mono is available
fc-list | grep -i "maple mono"
```

If **not found**, offer to install it. Source: https://github.com/subframe7536/maple-font

**macOS** (via Homebrew):
```bash
brew install --cask font-maple-mono
```

**Linux** (manual install):
```bash
# Download the latest release
curl -L -o /tmp/MapleMono.zip "https://github.com/subframe7536/maple-font/releases/latest/download/MapleMono.zip"
mkdir -p ~/.local/share/fonts
unzip -o /tmp/MapleMono.zip -d ~/.local/share/fonts/MapleMono
fc-cache -fv
rm /tmp/MapleMono.zip
```

**Windows** (manual):
- Download from https://github.com/subframe7536/maple-font/releases
- Extract and install the `.ttf` or `.otf` files

If the user declines installation, fall back to the OS default mono font (Menlo / Consolas / DejaVu Sans Mono).

### Check All Font Availability

```bash
# macOS
fc-list | grep -i "times new roman"
fc-list | grep -i "pingfang"
fc-list | grep -i "maple mono"

# Linux
fc-list | grep -i "liberation serif"
fc-list | grep -i "noto sans cjk"
fc-list | grep -i "maple mono"
```

## English Resume Template

```latex
% !TEX program = xelatex
\documentclass[a4paper, 9pt]{extarticle}

% ─── Packages ───
\usepackage[top=0.35in, bottom=0.35in, left=0.5in, right=0.5in]{geometry}
\usepackage[hidelinks]{hyperref}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{xcolor}
\usepackage{fontspec}
\usepackage{tabularx}

% ─── Colors ───
\definecolor{linkblue}{HTML}{1A73E8}

% ─── Fonts (adjust per OS — see font selection above) ───
\setmainfont{Times New Roman}
\setmonofont{Maple Mono}  % fallback: Menlo / Consolas / DejaVu Sans Mono
% For Chinese content in an English resume (e.g., company names):
% \newfontfamily\zhfont{PingFang SC}[BoldFont=PingFangSC-Semibold]

\hypersetup{colorlinks=true, urlcolor=linkblue}

% ─── Page style ───
\pagestyle{empty}

% ─── Spacing ───
\setlength{\parindent}{0pt}
\setlength{\parskip}{0pt}
\linespread{1.03}  % adjust between 1.0-1.08 to fill the page

% ─── Section headers ───
\titleformat{\section}
  {\normalsize\bfseries}{}
  {0pt}{}
  [\vspace{-6pt}\rule{\textwidth}{0.5pt}]
\titlespacing*{\section}{0pt}{7pt}{3.5pt}

% ─── Lists ───
\setlist[itemize]{
  leftmargin=1.2em, itemsep=2pt, parsep=0pt, topsep=2pt, label=--,
}

% ─── Custom commands ───
\newcommand{\experienceheader}[2]{%
  \vspace{4pt}%
  \begin{tabularx}{\textwidth}{@{}X r@{}}
    \textbf{#1} & \textit{#2}
  \end{tabularx}%
}
\newcommand{\experiencerole}[2]{%
  \begin{tabularx}{\textwidth}{@{}X r@{}}
    #1 & \textit{#2}
  \end{tabularx}\vspace{0.5pt}%
}
\newcommand{\expsubsection}[1]{%
  \vspace{2.5pt}\textbf{#1}\vspace{0.5pt}%
}
\newcommand{\edurow}[4]{%
  \begin{tabularx}{\textwidth}{@{}X r@{}}
    \textbf{#1} \,|\, \textit{#2} & #3 \,|\, \textit{#4}
  \end{tabularx}%
}

% ───────────────────────────────────────
\begin{document}

\begin{center}
  {\LARGE\bfseries CANDIDATE NAME}\\[4pt]
  {\small +XX XXX XXXX XXXX \,|\, \href{mailto:email@example.com}{email@example.com} \,|\, \href{https://linkedin.com/in/xxx}{linkedin.com/in/xxx} \,|\, City}
\end{center}

\section*{Profile}
% 2-3 concise sentences positioning the candidate for this specific role.

\section*{Education}
\edurow{University Name}{Degree, Honors}{City, Country}{Start -- End}
\vspace{2pt}
\edurow{University Name}{Degree, GPA}{City, Country}{Start -- End}

\section*{Professional Experience}
\experienceheader{Company Name}{City, Country}
\experiencerole{Job Title}{Start -- End}
\expsubsection{Sub-category of Work}
\begin{itemize}
  \item Bullet point with \textbf{bolded skills/tools} and \textbf{quantified results}
\end{itemize}

\section*{Project Experience}
\experienceheader{Project Name}{City, Country}
\experiencerole{Role}{Start -- End}
\begin{itemize}
  \item Bullet point...
\end{itemize}

\section*{Skills}
\begin{itemize}
  \item \textbf{Category:} Skill 1, Skill 2, \textbf{Tool 1}, \textbf{Tool 2}
  \item \textbf{Languages:} Chinese (Native), English (Professional Working Proficiency)
\end{itemize}

\end{document}
```

## Chinese Resume Template

The Chinese template is nearly identical but with different font configuration:

```latex
% ─── Fonts (Chinese resume on macOS) ───
\usepackage{xeCJK}
\setCJKmainfont{PingFang SC}[BoldFont=PingFangSC-Semibold]
\setmainfont{Times New Roman}  % for English text within Chinese resume
\setmonofont{Maple Mono}

% On Windows:
% \setCJKmainfont{Microsoft YaHei}[BoldFont=Microsoft YaHei Bold]

% On Linux:
% \setCJKmainfont{Noto Sans CJK SC}[BoldFont=Noto Sans CJK SC Bold]
```

Key differences for Chinese resumes:
- Use `xeCJK` package instead of just `fontspec`
- Section headers in Chinese: `个人总结`, `教育背景`, `工作经历`, `项目经历`, `核心技能`
- Use Chinese punctuation (，、。）
- Bullet label can be `\textbullet` or `--` (both are acceptable)

## Compilation Procedure

```bash
TEXDIR=".tex"
TEXFILE="$TEXDIR/resume.tex"

# 1. Create .tex directory
mkdir -p "$TEXDIR"

# 2. Write .tex file (done by the skill)

# 3. Compile
cd "$TEXDIR" && xelatex -interaction=nonstopmode "$(basename "$TEXFILE")"

# 4. Move PDF to parent (working directory)
mv *.pdf ../  # rename to proper filename

# 5. Clean up intermediate files
rm -f *.aux *.log *.out *.toc *.fls *.fdb_latexmk *.synctex.gz

# 6. Return to working directory
cd ..
```

## Page Fitting Strategy

The resume MUST be exactly 1 page. After first compile, check page count:

```bash
# Check page count (requires pdfinfo or similar)
pdfinfo output.pdf | grep Pages
# Or check xelatex output for page count
```

**If 2 pages** (too much content): Tighten in this order:
1. `\linespread{1.0}` (minimum)
2. Reduce `\titlespacing` before/after values by 1-2pt
3. Reduce `itemsep` to 1pt
4. Reduce font size: try 9pt (minimum practical size)
5. Trim bullet points — cut words, not information
6. Reduce margins to 0.4in top/bottom, 0.45in left/right (minimum)

**If too much whitespace** (page not filled): Expand in this order:
1. `\linespread{1.08}` (maximum)
2. Increase `\titlespacing` values by 1-2pt
3. Increase `itemsep` to 3pt
4. Try 10pt font size
5. Add more detail to existing bullet points
6. Slightly increase margins for breathing room

Always recompile after adjustments and verify the page count.
