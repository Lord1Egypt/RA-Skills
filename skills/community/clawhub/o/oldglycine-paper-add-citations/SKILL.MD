---
name: oldglycine-paper-add-citations
description: Automatically adds relevant academic references to research papers. Supports Overleaf project directories, extracts keywords from TeX files, searches Google Scholar for relevant papers, adds BibTeX entries to the project's bib file, and inserts citation markers in key sections.
metadata: 
  versions: 1.0.0
---
# Paper Reference Adder Skill

## When to Use
- When a research paper needs additional citations in specific sections (Introduction, Related Work, Method)
- When you want to find relevant papers to cite based on the paper's content
- When you need to ensure no duplicate references are added

## How It Works
1. **Backup**: Creates a backup of the project directory to prevent data loss
2. **Content Analysis**: Reads TeX files and extracts keywords and existing references
3. **Reference Search**: Uses Google Scholar (via scholarly library) to find relevant papers
4. **BibTeX Generation**: Generates BibTeX entries for new references
5. **Integration**: Adds new references to the bib file and inserts citation markers in key sections
6. **Reporting**: Generates an ADD.MD file with all added references and their positions

## Codes references & Parameters
- Codes references [ref](./reference/TOOL.MD)
- `input`: Path to Overleaf project directory
- `num_references`: Number of references to find (default: 10)
- `output_report`: Path for the ADD.MD report (default: ./ADD.MD)

## Dependencies
- scholarly (for Google Scholar search)
- bibtexparser (for BibTeX handling)
- pdflatex (optional, for compiling the paper)

## Notes
- Handles existing citations to avoid duplicates
- Focuses on key sections (Introduction, Related Work, Method) for citation insertion
- Generates a detailed report of all added references
- Compatible with Overleaf project structure
- Uses scholarly library as an alternative to Google Scholar API
