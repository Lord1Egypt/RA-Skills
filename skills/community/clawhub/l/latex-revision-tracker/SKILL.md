---
name: latex-revision-tracker
description: Systematic workflow for tracking, managing, and revising large LaTeX academic papers with version control, content integration, and quality assurance.
version: 1.0.0
homepage: https://github.com/Larry-of-cosmotim/latex-revision-tracker
metadata:
  openclaw:
    emoji: 📐
---

# LaTeX Revision Tracker Skill

## Overview

This skill provides a comprehensive workflow for managing revisions to large LaTeX academic papers (10+ pages, multiple sections, complex bibliographies). It emphasizes systematic version control, careful content integration, and quality assurance throughout the revision process.

## When to Use

Use this skill when:
- Revising large academic papers or dissertations in LaTeX
- Integrating new content (figures, data, analysis) into existing manuscripts
- Collaborating on multi-author academic documents
- Preparing papers for journal submission with multiple revision rounds
- Managing complex manuscripts with extensive bibliographies and cross-references

## Core Workflow

### 1. Version Control Setup

**File Naming Convention:**
```
manuscript_v1_initial.tex
manuscript_v2_reviewer_response.tex  
manuscript_v3_final_submission.tex
```

**Change Documentation:**
Create `version_changes.md` for each revision:
```markdown
# V2 TO V3 CHANGES SUMMARY

## CHANGES MADE:
### ✅ NEW SECTION ADDED:
- **Section 4.2**: Glass Limit Analysis  
- **Location**: After thermal conductivity discussion
- **Content**: 3 paragraphs + 1 figure

### ✅ NEW FIGURE:
- **cahill_plot.pdf** - Publication-ready (300 DPI)
- **Reference**: Figure~\ref{fig:cahill_plot}
- **Caption**: [Complete caption text]

### ✅ CONTENT MODIFICATIONS:
- Updated abstract (lines 25-35)
- Revised conclusion (Section 6, paragraph 2)
- Added 12 new citations

## INTEGRATION DETAILS:
- **Placement**: After existing analysis, before discussion
- **Line numbers**: Approximately 450-480
- **Compilation status**: ✅ Success / ❌ Unicode issues
```

### 2. Content Integration Strategy

**Pre-Integration Checklist:**
- [ ] New content reviewed for accuracy and style
- [ ] Figures prepared in publication quality (PDF/EPS preferred)
- [ ] All citations properly formatted and verified
- [ ] Mathematical notation consistent with existing document
- [ ] Cross-references planned (`\label{}` and `\ref{}` commands)

**Integration Process:**
```
1. Backup current working version
2. Identify integration point in document structure
3. Plan figure/table placement and numbering
4. Insert content with proper sectioning
5. Update cross-references throughout document
6. Compile and resolve errors iteratively
```

### 3. LaTeX-Specific Quality Control

**Compilation Workflow:**
```bash
# For bibliography updates (full workflow)
pdflatex manuscript.tex
bibtex manuscript
pdflatex manuscript.tex
pdflatex manuscript.tex

# For minor changes (quick check)
pdflatex manuscript.tex
pdflatex manuscript.tex
```

**Common Issues and Solutions:**

**Unicode Characters:**
```latex
% Problem: Special characters (κ, α, β) in text
% Solution: Use math mode or proper packages
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}

% In text: $\kappa$ not κ
% In equations: \begin{equation} \kappa = ... \end{equation}
```

**Reference Resolution:**
```latex
% Ensure labels come after what they reference
\section{Results}
\label{sec:results}  % ✅ After section

\begin{figure}
\includegraphics{plot.pdf}
\caption{Important results}
\label{fig:results}  % ✅ After caption
\end{figure}
```

**Float Management:**
```latex
% For flexible placement
\begin{figure}[htbp]

% To force exact position (use sparingly)
\usepackage{float}
\begin{figure}[H]

% For wide figures in two-column format
\begin{figure*}[t]
```

### 4. Academic Content Integration

**Section-Specific Integration Guidelines:**

**Abstract Updates:**
- Maintain 150-250 word limit
- Update contribution statements to reflect new content
- Ensure keywords remain accurate

**Introduction Modifications:**
- Integrate new motivation naturally
- Update contribution list if needed
- Maintain logical flow from general to specific

**Related Work Additions:**
- Group new citations thematically
- Compare explicitly with existing approaches
- Maintain chronological awareness

**Results Section Integration:**
- Number figures/tables consecutively
- Reference all new content in text
- Maintain consistent data presentation style

**Discussion/Conclusion Updates:**
- Integrate implications of new findings
- Update limitations section if applicable
- Revise future work based on new insights

### 5. Bibliography Management

**Citation Integration Process:**
1. Add new entries to `.bib` file
2. Use consistent citation keys (`author2024keyword`)
3. Verify all required fields (author, title, year, venue)
4. Check for duplicate entries
5. Run `bibtex` to update references
6. Resolve any citation warnings

**Citation Style Consistency:**
```latex
% In-text citations
Recent work has shown \cite{smith2024analysis}...
Multiple studies \cite{jones2023,brown2024,wilson2024} have...
As demonstrated by Smith et al.~\cite{smith2024analysis}...

% Reference formatting (depends on journal style)
% IEEE: [1] A. Smith, "Title," Journal, vol. 1, pp. 1-10, 2024.
% ACM: [1] Smith, A. 2024. Title. Journal 1, 1 (2024), 1-10.
```

### 6. Quality Assurance Process

**Pre-Submission Checklist:**
- [ ] Document compiles without errors or warnings
- [ ] All figures appear correctly and are referenced in text
- [ ] All tables are properly formatted and referenced
- [ ] Bibliography is complete and properly formatted
- [ ] Cross-references resolve correctly
- [ ] Page layout is consistent with journal requirements
- [ ] Mathematical notation is consistent throughout
- [ ] Acronyms defined on first use
- [ ] Line spacing and margins correct for submission

**Collaboration Workflow:**
```
1. Author A makes changes → commits with detailed message
2. Author B reviews changes → suggests modifications
3. Changes documented in version log
4. Final integration by designated "manuscript manager"
5. All co-authors review final version before submission
```

### 7. Error Resolution Strategies

**Common LaTeX Errors:**

**Missing References:**
```
LaTeX Warning: Reference `fig:unknown' undefined
Solution: Check \label{} and \ref{} spelling, compile twice
```

**Overfull/Underfull Boxes:**
```
Overfull \hbox (15.0pt too wide)
Solution: Rephrase text, add hyphenation hints (\-), or use \sloppy
```

**Float Issues:**
```
Too many unprocessed floats
Solution: Add \clearpage or adjust float placement options
```

**Bibliography Errors:**
```
Citation `unknown2024' undefined
Solution: Check .bib file, run bibtex, compile again
```

### 8. Performance Optimization

**For Large Documents (50+ pages):**
- Use `\includeonly{}` to compile specific chapters
- Split large documents with `\input{}` or `\include{}`
- Use `\graphicspath{}` for organized figure directories
- Consider `latexmk` for automated compilation management

**Memory Management:**
```latex
% For documents with many figures
\usepackage{graphicx}
\DeclareGraphicsExtensions{.pdf,.eps,.png,.jpg}

% For complex bibliographies
\usepackage[backend=bibtex,style=ieee]{biblatex}
```

## Advanced Features

### 1. Diff Tracking

**CRITICAL:** Diff files inherit ALL citation dependencies from the source documents. You MUST run the full bibliography workflow — a single `pdflatex` pass will ALWAYS produce citation errors (`[?]` markers) in diff files. This is the most common mistake.

**Full diff workflow (mandatory — no shortcuts):**
```bash
# Step 1: Generate the diff .tex
latexdiff manuscript_v1.tex manuscript_v2.tex > diff_v1_v2.tex

# Step 2: Copy bibliography files to the same directory
# The diff file needs access to the SAME .bib files and .bst style
cp manuscript.bib .    # if not already present

# Step 3: Full compilation (ALL steps required)
pdflatex diff_v1_v2.tex      # First pass — generates .aux with citation keys
bibtex diff_v1_v2            # Resolves citations from .bib file
pdflatex diff_v1_v2.tex      # Second pass — incorporates bibliography
pdflatex diff_v1_v2.tex      # Third pass — resolves all cross-references
```

**Never do this:**
```bash
# WRONG — will produce [?] for every citation
pdflatex diff_v1_v2.tex   # single pass = broken citations
```

**Troubleshooting citation errors in diff files:**
- `[?]` markers → you skipped `bibtex`. Run the full 4-step workflow above.
- `I couldn't open file name.bib` → copy the `.bib` file to the diff directory.
- `I couldn't open style file name.bst` → copy the `.bst` file too.
- Still broken → check that `\bibliography{}` and `\bibliographystyle{}` paths are correct in the source `.tex` files before running `latexdiff`.

**Post-diff cleanup:** After the diff PDF is verified, remove all intermediate files. Only the final PDF should remain.
```bash
# Clean up all auxiliary and intermediate files
rm -f diff_v1_v2.tex diff_v1_v2.aux diff_v1_v2.log diff_v1_v2.out \
      diff_v1_v2.bbl diff_v1_v2.blg diff_v1_v2.toc diff_v1_v2.lof \
      diff_v1_v2.lot diff_v1_v2.synctex.gz diff_v1_v2.fls \
      diff_v1_v2.fdb_latexmk diff_v1_v2.nav diff_v1_v2.snm
# Keep only: diff_v1_v2.pdf
```

**Rule:** Always clean up after generating a diff PDF. The diff `.tex` file is a throwaway — it's auto-generated and can be recreated anytime from the two source versions. Never keep it around to clutter the workspace.

### 2. Automated Quality Checks
```bash
# Check for common LaTeX issues
lacheck manuscript.tex

# Count words (approximate)
texcount manuscript.tex

# Validate bibliography
bibtex manuscript 2>&1 | grep -i warning
```

### 3. Collaborative Tools
```bash
# Git integration for version control
git add manuscript_v3.tex version_changes.md
git commit -m "Add glass limit analysis section, update abstract"
git tag v3.0-submission

# Overleaf sync for real-time collaboration
git push overleaf master
```

## Templates

### Change Log Template
```markdown
# VERSION X.Y CHANGES

## SUMMARY
Brief description of major changes

## NEW CONTENT
- Section/subsection additions
- Figure/table additions  
- New citations (count)

## MODIFICATIONS
- Sections revised
- Figures updated
- Text corrections

## TECHNICAL NOTES
- Compilation status
- Package updates needed
- Known issues

## REVIEW STATUS
- [ ] Content reviewed by Author A
- [ ] Figures checked by Author B  
- [ ] Bibliography verified
- [ ] Final compilation successful
```

### Integration Checklist Template
```markdown
## PRE-INTEGRATION
- [ ] Content accuracy verified
- [ ] Style guide compliance checked
- [ ] Citations properly formatted
- [ ] Figures publication-ready

## INTEGRATION
- [ ] Placement planned
- [ ] Cross-references updated
- [ ] Numbering scheme maintained
- [ ] LaTeX syntax verified

## POST-INTEGRATION
- [ ] Document compiles successfully
- [ ] All references resolve
- [ ] Visual layout acceptable
- [ ] Change log updated
```

## Best Practices

1. **Always backup** before major changes
2. **Document everything** in change logs
3. **Test compilation early** and often
4. **Use consistent naming** for files and labels
5. **Review systematically** with checklists
6. **Collaborate deliberately** with clear ownership
7. **Plan integration** before making changes
8. **Maintain quality** throughout the process

## Common Pitfalls

- **Skipping documentation**: Change logs save time later
- **Inconsistent compilation**: Always run full workflow for bibliography
- **Poor float placement**: Plan figure integration carefully
- **Missing backups**: One corrupted file can lose days of work
- **Rushed integration**: Quality issues compound in large documents
- **Ignoring warnings**: Small issues become large problems

## Tools and Resources

**Essential Tools:**
- LaTeX distribution (TeX Live, MiKTeX)
- PDF viewer with refresh capability (SumatraPDF, Skim)
- Text editor with LaTeX support (TeXstudio, VS Code with LaTeX Workshop)
- Reference manager (Mendeley, Zotero, BibTeX)

**Quality Assurance:**
- `latexdiff` for visual change tracking
- `lacheck` for syntax validation
- `texcount` for word counting
- Git for version control

This skill provides the systematic approach needed to manage complex LaTeX academic papers while maintaining quality and avoiding common pitfalls that plague large document revision processes.