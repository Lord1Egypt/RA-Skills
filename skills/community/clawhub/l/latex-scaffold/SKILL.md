---
name: latex-scaffold
description: Scaffold LaTeX papers into modular structure. Use for organizing .tex files, generating figure code, and table highlighting. Trigger on LaTeX paper organization, figure management, or academic paper formatting.
---

# LaTeX Scaffold

Standardize LaTeX academic paper projects with modular structure and automated asset management.

## Project Structure

```
project-root/
├── assets/                 # Images and auto-generated .tex files
│   ├── figure1.png
│   ├── figure1.tex         # Auto-generated
│   └── table1.tex
├── src/                    # Modular sections
│   ├── introduction.tex
│   ├── methods.tex
│   └── references.bib
└── main.tex                # Entry point with \input{src/...}
```

## Workflow

### Step 0: Get Template (if needed)

If user has no LaTeX project, download the default IEEE conference template:  
`https://ras.papercept.net/conferences/support/files/ieeeconf.zip`

### Step 1: Structure the Project

Split large `.tex` files. In `main.tex`, use:
```latex
\input{src/introduction}
\input{src/methods}
\input{src/results}
```

### Step 2: Generate LaTeX for Assets

```bash
python <skill-dir>/scripts/generate_tex_for_assets.py <project-root>
```

Requires in preamble:
```latex
\usepackage{graphicx}
\usepackage{caption}
```

### Step 3: Add Table Highlighting

```latex
\usepackage[table]{xcolor}
% \cellcolor{top1}3.14
\definecolor{top1}{rgb}{0.996, 0.851, 0.380}  % Gold
\definecolor{top2}{rgb}{0.675, 0.843, 0.557}  % Light green
\definecolor{top3}{rgb}{0.663, 0.914, 0.894}  % Cyan
```

## Trigger Guidelines

**USE this skill when:**
- User has a `.tex` file to organize
- "Organize my LaTeX paper"
- "Split this tex file into sections"
- "Generate LaTeX for my figures"
- "Set up table colors in LaTeX"
- "Make my LaTeX project modular"

**DO NOT use when:**
- "How do I install LaTeX?" (installation question)
- "What does \\textbf do?" (syntax question)
- "Create a LaTeX presentation" (wrong document type)
- "Convert PDF to LaTeX" (unrelated task)
- User just mentions "LaTeX" without context of organizing/managing papers

## Notes

- Main filename is flexible
- Generated `.tex` files in `assets/` can be customized after generation
- Color definitions are optional but recommended
