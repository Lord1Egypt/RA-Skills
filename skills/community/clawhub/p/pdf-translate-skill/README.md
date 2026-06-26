# PDF Translator Skill

A comprehensive PDF document translation tool that enables multilingual translation of PDF documents while preserving the original document layout.

## Features

- **Intelligent Layout Preservation** - Converts PDF pages to images for layout analysis, maintaining the original typography
- **Content Extraction and Translation** - Extracts text and embedded images, utilizing AI for content translation
- **LaTeX Recomposition** - Reconstructs the original document structure using LaTeX, generating professionally typeset translated PDFs
- **arXiv Paper Support** - Direct translation of arXiv papers by downloading source TeX files, preserving all formatting automatically

## Basic Workflow

The agent will leverage multimodal capabilities to recognize the text and diagram arrangement of the PDF, completing the full document translation through the generation of LaTeX source code and subsequent compilation.

## Project Structure

```
pdf-translate-skill/
├── SKILL.md                 # Skill definition and usage instructions
├── references/              # Reference documents directory
│   ├── latex_templates.md   # LaTeX layout template collection
│   └── troubleshooting.md   # Troubleshooting guide
└── scripts/                 # Utility scripts directory
    ├── pdf_to_images.py     # PDF to image conversion tool
    ├── extract_images.py    # PDF image extraction tool
    ├── compile_latex.py     # LaTeX compilation tool
    └── download_arxiv_source.py  # arXiv source downloader
```

