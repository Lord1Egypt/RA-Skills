# PPTX Skill (Localized)

Professional PowerPoint (.pptx) creation, editing, and analysis skill for WorkBuddy.

Localized from [Anthropic official pptx skill](https://github.com/anthropics/skills/tree/main/skills/pptx), adapted for Windows environment.

## Features

- **Read & Analyze**: Extract text content from .pptx files via markitdown
- **Edit Templates**: Unpack PPTX XML, modify slides, repack with validation
- **Create from Scratch**: Build presentations programmatically using pptxgenjs (Node.js)
- **Visual QA**: Generate slide thumbnails for visual inspection
- **Design System**: Built-in color palettes, typography guides, and layout principles

## File Structure

```
pptx/
├── SKILL.md              # Skill metadata & quick reference
├── README.md             # This file
├── editing.md            # Full guide: edit existing PPTs
├── pptxgenjs.md          # Full guide: create PPTs from scratch
└── scripts/
    ├── add_slide.py      # Duplicate/create slides
    ├── clean.py          # Remove orphaned files
    ├── thumbnail.py      # Generate slide thumbnails
    └── office/
        ├── soffice.py    # LibreOffice runner (Windows-compatible)
        ├── unpack.py     # Unpack PPTX to XML
        └── pack.py       # Repack XML to PPTX
```

## Dependencies

### Required
- `markitdown[pptx]` - text extraction
- `Pillow` - image processing
- `defusedxml` - safe XML parsing
- `pptxgenjs` - Node.js presentation engine (npm)

### Optional
- **LibreOffice** - PDF conversion for visual QA
- **Poppler** (pdftoppm) - PDF to image conversion

## Windows Localization Notes

- Removed Linux-only AF_UNIX socket shim (LD_PRELOAD)
- Added SOFFICE_PATH environment variable for custom LibreOffice path
- Fixed thumbnail.py LABEL_PADDING_RATIO typo
- Node.js uses managed binary path

## Author

yinfeihaaaaaaaaaaa

## License

MIT-0
