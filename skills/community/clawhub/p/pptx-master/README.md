# PPT Master

AI-driven multi-format SVG content generation system for professional presentations.

## Version History

### v1.2.1 (2026-04-19) - XML Validation Enhancement

**Fixed:**
- **SVG Content Checker** now validates XML syntax before content analysis
- Detects mismatched tags (e.g., `<tspan>...</text>`)
- Catches malformed SVG that would cause rendering failures

**Technical Details:**
- Added `xml.etree.ElementTree.fromstring()` validation in `_check_content_elements()`
- XML parse errors now block the workflow with clear error messages
- Prevents false-positive "passes" on malformed SVG files

**Issue Resolved:**
- Page 7 of AI Weekly Report PPT was blank due to XML tag mismatch
- Root cause: `<tspan>` closed with `</text>` instead of `</tspan>`
- Old checker missed it because it only counted string occurrences

---

### v1.2.0 (2026-04-18) - Content Review & Auto-Repair

**Added:**
- **SVG Content Checker** (`scripts/svg_content_checker.py`)
  - Blank page detection (text elements < 2 AND file size < 500 bytes)
  - Content density scoring (0-100%)
  - Design consistency checking (colors, fonts)
  - Structure completeness evaluation
- **SVG Repair Coordinator** (`scripts/svg_repair_coordinator.py`)
  - Automatic repair workflow
  - Regeneration prompt generation for blank pages
  - Fallback to placeholder pages when repair fails
- **Step 6.5** in workflow: Content Review & Auto-Repair
  - Automatic check after SVG generation
  - Non-blocking: warnings allow continuation
  - Blocking: blank pages trigger repair workflow

**Changed:**
- `SKILL.md`: Added Step 6.5 between SVG generation and post-processing
- Tool list: Added svg_content_checker.py and svg_repair_coordinator.py

**Use Case:**
- Automatically detect blank pages before PPTX export
- Generate repair prompts for manual regeneration
- Ensure presentation quality before delivery

---

### v1.1.1 (2026-04-11) - Huawei Template Integration

**Added:**
- Huawei Technologies brand template (`华为技术`)
- New `enterprise` quick lookup category in template index
- Template count updated to 21

**Changed:**
- `layouts_index.json`: Added Huawei template to brand category and technology/enterprise lookups
- `README.md`: Updated template index with Huawei template details

**Use Case:**
- Enterprise reports, solution showcases, annual reports, B2B client communication
- Minimalist tech style with Huawei red accents and professional gray tones

---

### v1.1.0 (2026-04-09) - Source File Handling Update

**Changed:**
- Source files are now **copied** (not moved) to `sources/` directory by default
- Original files are preserved at their source location
- Use `--move` flag if you want to move files instead of copying

**Previous behavior (v1.0.x):**
- Source files were moved to `sources/`, removing them from original location

**Rationale:**
- Safer default behavior - originals are preserved
- Users can still opt-in to move behavior with `--move` flag
- Reduces risk of accidental data loss

---

### v1.0.0 (2026-04-08) - Initial Release

**Features:**
- Multi-format input support (PDF, DOCX, EPUB, HTML, URL, Markdown)
- Professional SVG generation with design system
- Template-based and free-design modes
- Eight Confirmations design specification
- PPTX export with speaker notes
- Icon embedding and image processing

---

## Usage

```bash
# Initialize project
python3 scripts/project_manager.py init <project_name> --format ppt169

# Import source files (default: copy, preserve originals)
python3 scripts/project_manager.py import-sources <project_path> <source_files...>

# Import source files (move mode - remove originals)
python3 scripts/project_manager.py import-sources <project_path> <source_files...> --move

# Generate PPTX
python3 scripts/svg_to_pptx.py <project_path> -s final
```

## License

MIT
