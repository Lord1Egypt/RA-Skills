---
name: latex-studio
description: LaTeX document generator for academic papers and technical reports. Use when user needs to create professional academic papers, theses, or technical documents with math formulas, tables, and citations. Generates publication-ready .tex files compatible with Overleaf and all LaTeX compilers.
version: 1.0.5
license: MIT-0
metadata: {"openclaw": {"emoji": "📐", "requires": {"bins": ["python3"], "env": []}}}
---

# LaTeX Studio

Professional LaTeX document generator for academic papers and technical reports.

## Features

- 📄 **Academic Papers**: Standard paper formatting
- 📐 **Math Formulas**: Full LaTeX math support
- 📑 **Tables**: Professional table layouts
- 📝 **Citations**: Reference management
- 📊 **Charts**: Integration with data
- ✅ **Compatible**: Works with Overleaf, TeX Live, MiKTeX

## Main Use Case

LaTeX is primarily used for academic paper writing. This skill focuses on English language support for maximum compatibility and professional quality.

## Supported Document Types

| Type | Use Case |
|------|----------|
| Research Paper | Academic publication |
| Technical Report | Documentation |
| Thesis | Graduate work |
| White Paper | Business/technical |
| Conference Paper | IEEE/ACM format |

## Trigger Conditions

- "Write a paper" / "Create a LaTeX document"
- "Generate academic paper"
- "LaTeX report" / "Research paper"
- "latex-studio"

---

## LaTeX Template

```latex
\documentclass[12pt, a4paper]{article}

% Packages
\usepackage[margin=2.5cm, headheight=14pt]{geometry}
\usepackage{amsmath, amssymb}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{booktabs}
\usepackage{xcolor}
\usepackage{colortbl}
\usepackage{enumitem}
\usepackage{fancyhdr}

% Colors
\definecolor{primary}{RGB}{30, 60, 114}
\definecolor{secondary}{RGB}{100, 100, 100}

% Header/Footer
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\color{secondary}Document Title}
\fancyfoot[C]{\thepage}

% Title
\title{\color{primary}\textbf{Paper Title}}
\author{Author Name}
\date{\today}

\begin{document}

\maketitle

\begin{abstract}
Abstract text goes here.
\end{abstract}

\tableofcontents
\newpage

\section{Introduction}

Introduction content...

\section{Methodology}

Method content...

\begin{table}[h]
\centering
\renewcommand{\arraystretch}{1.3}
\begin{tabular}{|l|c|c|c|}
\hline
\rowcolor{primary}
\textcolor{white}{\textbf{Header1}} & \textcolor{white}{\textbf{Header2}} & \textcolor{white}{\textbf{Header3}} \\
\hline
Row1 & Data1 & Data2 \\
\hline
\end{tabular}
\caption{Table Title}
\label{tab:example}
\end{table}

\section{Results}

Results content...

\section{Conclusion}

Conclusion content...

\end{document}
```

---

## Usage Examples

```
User: "Write a research paper about AI"
Agent: Generate LaTeX document with proper formatting

User: "Create a technical report"
Agent: Generate professional report template
```

---

## Notes

- Generates .tex files
- Compatible with Overleaf and all LaTeX compilers
- Requires LaTeX environment to compile to PDF
- Focuses on English language support
