# Capabilities and Boundaries

This skill is a text-first office document extraction skill.

## What it does well

- Reads common office document formats: PDF, DOCX, DOC, XLSX, XLS, PPTX, PPT
- Extracts text from modern Office documents with deterministic libraries
- Falls back to OCR for scanned PDFs when embedded text is missing
- Returns a stable JSON shape that is easy for agents to summarize
- Works well for summary, key-point extraction, field extraction, and rough structure recovery
- Handles Chinese PDFs better when `tesseract-ocr-chi-sim` is installed

## What it does only partially

### PDF layout fidelity
The skill can extract text, but it does not preserve complex visual layout exactly.
Multi-column PDFs, tables, footers, and sidebars may read in imperfect order.

### Spreadsheet structure
The skill reads sheet names and rows, but it does not fully reconstruct merged-cell semantics, formulas, formatting logic, pivot tables, or business meaning automatically.

### PowerPoint visuals
The skill extracts slide text and notes, but it does not deeply interpret diagrams, animations, screenshots, or design intent.

### OCR accuracy
OCR is a recovery path, not a guarantee. Accuracy depends on scan quality, language pack availability, rotation, contrast, and font clarity.

## What it does not aim to do

- Exact page layout recreation
- Rich image/chart understanding
- Password cracking or decryption
- Full redline / tracked-changes analysis
- Spreadsheet auditing at BI / finance-tool level
- Perfect table recovery from arbitrary scanned documents

## Recommended positioning

Present this skill as:
- a reliable document text extraction and summarization helper
- a strong default for uploaded office files in chat
- a practical OCR-backed PDF reader for Chinese/English content

Do not present it as:
- a desktop publishing parser
- a visual document AI system
- a forensic Office analysis tool
