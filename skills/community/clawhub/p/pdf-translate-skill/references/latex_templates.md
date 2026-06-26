# LaTeX Layout Templates

This reference provides LaTeX templates for common document layouts encountered during PDF translation. Use these as building blocks when generating LaTeX code.

## Table of Contents

1. [Single Column Layout](#single-column-layout)
2. [Two Column Layout](#two-column-layout)
3. [Figure Placement](#figure-placement)
4. [Table Templates](#table-templates)
5. [Mathematical Content](#mathematical-content)
6. [List Templates](#list-templates)
7. [Header/Footer Variations](#headerfooter-variations)

---

## Single Column Layout

### Basic Paragraph
```latex
\section{Section Title}

This is a paragraph of text. It will be formatted with the default
paragraph settings including indentation for the first line.

This is another paragraph. Note that LaTeX automatically handles
paragraph spacing.
```

### With Image
```latex
\section{Section with Image}

\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.8\textwidth]{image_name.png}
    \caption{Figure caption here (translated)}
    \label{fig:label}
\end{figure}

Text content continues below the figure...
```

---

## Two Column Layout

### Document-wide Two Columns
```latex
\documentclass[twocolumn]{article}
% ... rest of preamble
```

### Local Two Column Section
```latex
\begin{multicols}{2}
\section{Left Column Content}
Content for the left column...

\section{Right Column Content}
Content for the right column...
\end{multicols}
```

### Figure Spanning Two Columns
```latex
\begin{figure*}[htbp]
    \centering
    \includegraphics[width=\textwidth]{wide_image.png}
    \caption{Wide figure spanning both columns}
    \label{fig:wide}
\end{figure*}
```

---

## Figure Placement

### Inline Figure
```latex
\begin{figure}[h]
    \centering
    \includegraphics[width=0.5\textwidth]{inline_fig.png}
    \caption{Inline figure}
\end{figure}
```

### Positioned Figure
```latex
% h = here, t = top, b = bottom, p = page, ! = force
\begin{figure}[!htbp]
    \centering
    \includegraphics[
        width=0.6\textwidth,
        height=5cm,
        keepaspectratio
    ]{positioned_fig.png}
    \caption{Positioned figure with size constraints}
\end{figure}
```

### Side-by-side Figures
```latex
\begin{figure}[htbp]
    \centering
    \begin{minipage}{0.45\textwidth}
        \centering
        \includegraphics[width=\textwidth]{left_image.png}
        \caption{Left image}
    \end{minipage}
    \hfill
    \begin{minipage}{0.45\textwidth}
        \centering
        \includegraphics[width=\textwidth]{right_image.png}
        \caption{Right image}
    \end{minipage}
\end{figure}
```

---

## Table Templates

### Simple Table
```latex
\begin{table}[htbp]
    \centering
    \caption{Table caption (translated)}
    \begin{tabular}{lcc}
        \toprule
        Header 1 & Header 2 & Header 3 \\
        \midrule
        Row 1 Col 1 & Row 1 Col 2 & Row 1 Col 3 \\
        Row 2 Col 1 & Row 2 Col 2 & Row 2 Col 3 \\
        \bottomrule
    \end{tabular}
    \label{tab:label}
\end{table}
```

### Multi-page Table
```latex
\begin{longtable}{lcc}
    \caption{Long table spanning multiple pages} \\
    \toprule
    Header 1 & Header 2 & Header 3 \\
    \midrule
    \endfirsthead
    
    \multicolumn{3}{c}{\textit{Continued from previous page}} \\
    \toprule
    Header 1 & Header 2 & Header 3 \\
    \midrule
    \endhead
    
    \midrule
    \multicolumn{3}{r}{\textit{Continued on next page}} \\
    \endfoot
    
    \bottomrule
    \endlastfoot
    
    % Table content
    Row 1 & Data & Data \\
    Row 2 & Data & Data \\
    % ... more rows
\end{longtable}
```

### Table with Fixed Width Columns
```latex
\begin{table}[htbp]
    \centering
    \begin{tabularx}{\textwidth}{X c c}
        \toprule
        Description (auto-width) & Value 1 & Value 2 \\
        \midrule
        Long text that will wrap automatically & 100 & 200 \\
        Short text & 50 & 75 \\
        \bottomrule
    \end{tabularx}
\end{table}
```

---

## Mathematical Content

### Inline Math
```latex
The equation $E = mc^2$ is famous. Or use $f(x) = \int_{0}^{\infty} e^{-x^2} dx$.
```

### Display Math
```latex
\begin{equation}
    f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}
\end{equation}
```

### Multi-line Equations
```latex
\begin{align}
    \nabla \cdot \mathbf{E} &= \frac{\rho}{\epsilon_0} \\
    \nabla \cdot \mathbf{B} &= 0 \\
    \nabla \times \mathbf{E} &= -\frac{\partial \mathbf{B}}{\partial t} \\
    \nabla \times \mathbf{B} &= \mu_0 \mathbf{J} + \mu_0 \epsilon_0 \frac{\partial \mathbf{E}}{\partial t}
\end{align}
```

### Theorem Environment
```latex
\begin{theorem}[Theorem Name]
    Statement of the theorem.
\end{theorem}

\begin{proof}
    Proof content here.
\end{proof}
```

---

## List Templates

### Bullet List
```latex
\begin{itemize}
    \item First item
    \item Second item
        \begin{itemize}
            \item Nested item
        \end{itemize}
    \item Third item
\end{itemize}
```

### Numbered List
```latex
\begin{enumerate}
    \item First item
    \item Second item
    \item Third item
\end{enumerate}
```

### Description List
```latex
\begin{description}
    \item[Term 1] Description of term 1
    \item[Term 2] Description of term 2
    \item[Term 3] Description of term 3
\end{description}
```

---

## Header/Footer Variations

### Simple Header
```latex
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{Document Title}
\fancyhead[R]{\thepage}
```

### With Section Name
```latex
\fancyhead[L]{\leftmark}  % Current section
\fancyhead[R]{\rightmark} % Current subsection
\fancyfoot[C]{\thepage}
```

### Chapter Style (for books/reports)
```latex
\documentclass{report}
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[LE,RO]{\thepage}
\fancyhead[RE]{\leftmark}
\fancyhead[LO]{\rightmark}
```

---

## Common Layout Patterns

### Title Block
```latex
\begin{center}
    {\LARGE\bfseries Document Title}\\[1em]
    {\large Subtitle}\\[2em]
    {\normalsize Author Name}\\
    {\small\textit{Affiliation}}\\[1em]
    {\small \today}
\end{center}
\vspace{2em}
```

### Abstract Box
```latex
\begin{abstract}
    This is the abstract text. It summarizes the document content.
    The abstract should be concise and informative.
\end{abstract}
```

### Highlighted Box
```latex
\usepackage{tcolorbox}
\begin{tcolorbox}[colback=blue!5, colframe=blue!50, title=Important Note]
    This is highlighted content that stands out from regular text.
\end{tcolorbox}
```

---

## Citation

### Construct The Reference List
```latex
\begin{thebibliography}{99}
\bibitem{ref1}This is the first citation.
\bibitem{ref2}This is the second citation.
\end{thebibliography}
```
```
```

### Cite In The Main Text
```latex
\cite{ref1}
\cite{ref1, ref2}
```

---

## Tips for Layout Preservation

1. **Measure approximately**: Use `\vspace{}` and `\hspace{}` for spacing adjustments
2. **Check image paths**: Ensure `\graphicspath` includes all image directories
3. **Use relative sizes**: Prefer `\textwidth` over absolute `cm` values
4. **Test compilation**: Run xelatex twice for references and TOC
5. **Debug gradually**: Comment out sections if compilation fails
