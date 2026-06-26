---
description: Converts PDF documents (invoices, reports) to High-Fidelity OFD format with pixel-perfect precision.
name: pdf2ofd
version: "1.1.0"
---

# PDF to OFD High-Fidelity Converter

## 🎯 Purpose
A specialized skill for converting PDF documents into the Chinese National Standard **OFD (GB/T 33190-2016)** format. Optimized for **Electronic Invoices (OFD版式发票)** with advanced rendering capabilities that exceed standard conversion libraries.

## ✨ Key Features
- **High-Fidelity Text Placement**: Uses character-level positioning (`DeltaX` arrays) and baseline origin data extracted via `rawdict` to ensure text layout is 100% identical to the source PDF.
- **Advanced Vector Graphics**: Directly extracts original stroke colors, fill colors, and line widths. Supports complex path types and fill instructions.
- **Transparency Preservation**: Fully supports `Alpha` and `FillOpacity` for vector paths and `SMask` transparency for images (e.g., electronic seals and signatures).
- **Cross-Platform Font Mapping**: Intelligent mapping of macOS-specific (STSong, STKaiti) and Windows-specific font names to standardized OFD font names (宋体, 楷体, 黑体).
- **In-Memory Packaging**: Generates the final OFD zip structure entirely in memory to avoid temporary file clutter and ensure security.
- **Color Snapping**: Heuristic "Invoice Red" correction (`128 0 0`) for financial documents while preserving non-standard colors.

## 🛠️ Usage Instructions
When a user asks to convert a PDF or a "High-Fidelity" invoice to OFD:

1.  **Direct Execution**:
    ```bash
    python3 pdf2ofd.py <input_path.pdf> [output_path.ofd]
    ```

2.  **Plugin Integration**:
    The script implements a `PDF2OFDConverter` class that can be easily imported and used in other Python workflows.

### Example Output
```text
Success: /path/to/invoice.ofd
```

## 📦 Requirements
Dependencies required in the environment:
- `PyMuPDF (fitz)`: For advanced PDF parsing and raw character data extraction.
- `Pillow`: For image processing and transparency handling.
- `easyofd`: The base library for OFD structure (extended via internal monkey patches).
- `xmltodict`: For XML manipulation.

## 💡 Notes
- This skill uses deep monkey-patching on `easyofd` to fix known library limitations regarding character positioning and resource ID tracking.
- The conversion process assumes standard Chinese fonts (SimSun, KaiTi, SimHei) are available on the viewing system.
- Zero-copy resource handling: Images are extracted and re-compressed as PNG/JPG only when necessary to preserve quality.
