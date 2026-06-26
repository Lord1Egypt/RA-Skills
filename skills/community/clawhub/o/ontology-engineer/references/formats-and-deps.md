# Supported Formats and Dependencies

## File Format Support

| Format | Extensions | Processing | Dependencies |
|--------|-----------|------------|--------------|
| Word (new) | .docx | python-docx: text + tables + images | python-docx, Pillow |
| Word (legacy) | .doc | temp-copy + COM read (Win) / libreoffice (Linux) | pywin32 (Win) / libreoffice |
| WPS Office | .wps .et .dps | LibreOffice convert → standard format | libreoffice |
| Excel (new) | .xlsx | openpyxl: all sheets, headers, data | openpyxl |
| Excel (legacy) | .xls | xlrd | xlrd |
| PDF | .pdf | PyMuPDF: text + images (Read tool also works) | PyMuPDF (fitz) |
| Presentations | .pptx .ppt | python-pptx: slides + notes | python-pptx |
| Markdown/Text | .md .txt | Direct read | — |
| SQL/DDL | .sql .ddl | Direct read | — |
| JSON/YAML | .json .yaml .yml | Direct read | — |
| CSV/TSV | .csv .tsv | Direct read | — |
| XML | .xml | Direct read | — |
| RTF | .rtf | striprtf | striprtf (optional) |
| OpenDocument | .odt .ods .odp | odfpy or LibreOffice | odfpy (optional) |
| macOS Office | .pages .numbers .key | macOS iWork export only | macOS only |

### .xlsx/.pptx Special Notes

- **.xlsx**: Not just "data." May contain client lists, budgets, project tracking, KPI dashboards, personnel rosters. Iterate ALL sheets. Sheet names are domain signals.
- **.pptx**: Strategy summaries, client pitches, competitive analysis. Info density often higher than corresponding Word docs. Read ALL slides + speaker notes.
- Both formats have priority equal to .docx. Never deprioritize.

### .doc Extraction: Temp-Copy COM Pattern (Windows)

Direct COM opening fails when file paths contain CJK characters (garbled encoding in COM API). Solution:

```python
import shutil, tempfile, win32com.client, pythoncom

def extract_doc(filepath):
    tmp_dir = tempfile.mkdtemp(prefix='doc_')
    tmp_path = os.path.join(tmp_dir, f'doc_{seq}.doc')  # unique name per file
    shutil.copy2(filepath, tmp_path)

    pythoncom.CoInitialize()
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0

    doc = word.Documents.Open(str(Path(tmp_path).resolve()), ReadOnly=True)
    text = doc.Content.Text
    doc.Close(False)
    word.Quit()
    pythoncom.CoUninitialize()

    shutil.rmtree(tmp_dir, ignore_errors=True)
    return text
```

**Key points**:
- Use **unique temp file names** per document (avoid lock collisions — Word may not release the file immediately after `Close`)
- Keep ONE Word instance for batch processing (creating Word is slow, ~2s each)
- If a file causes Word to hang, restart the Word instance and continue
- `._` prefix files are macOS resource forks — skip them
- Tested: **99% success rate** on 500 CJK-path .doc files

### WPS Format Notes

`.wps` (doc), `.et` (spreadsheet), `.dps` (presentation) — WPS Office formats, common in China. Convert via LibreOffice `--convert-to` to standard formats, then extract normally.

### Image Processing

.docx/.pdf embedded images (architecture diagrams, ER diagrams, flowcharts):
- .docx: python-docx `document.inline_shapes` and `document.part.rels`
- .pdf: PyMuPDF per-page or per-image extraction
- Feed to multimodal LLM for visual analysis
- If LLM doesn't support images: note in review.md for manual review

## Python Dependencies

### Core (required)

```bash
pip install python-docx openpyxl xlrd PyMuPDF Pillow python-pptx pyyaml
```

| Package | Purpose |
|---------|---------|
| python-docx | .docx text/tables/images |
| openpyxl | .xlsx reading |
| xlrd | .xls (legacy) reading |
| PyMuPDF (fitz) | .pdf text/images |
| Pillow | Image processing |
| python-pptx | .pptx slides/notes |
| pyyaml | schema.yaml read/write |

### Platform-specific

```bash
# Windows .doc conversion (requires Microsoft Word installed)
pip install pywin32

# Linux/macOS .doc/.wps conversion
sudo apt install libreoffice  # or: brew install libreoffice
```

### Optional

```bash
pip install striprtf odfpy olefile
```

| Package | Purpose |
|---------|---------|
| striprtf | .rtf text extraction |
| odfpy | OpenDocument (.odt/.ods/.odp) |
| olefile | .doc OLE2 structure parsing (fallback when COM unavailable) |

### LLM Requirements

| Capability | Purpose | Minimum |
|-----------|---------|---------|
| Text understanding | Phase 2.2 semantic reading | Any long-context LLM |
| Multimodal image input | Phase 2.2 image analysis | Claude Opus/Sonnet, GPT-4o |
| Tool use | Phase 2.2 structured output | Recommended, not required |

Step 1 (scan_filesystem.py) uses only Python stdlib — no extra deps.
