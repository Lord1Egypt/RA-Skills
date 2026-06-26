# PDF Extractor Skill

Extract text and mathematical formulas from academic PDF papers. Supports both English and Chinese content.

## When to Use This Skill

Use this skill when:
- User needs to extract text and LaTeX formulas from PDF papers
- User mentions "PDF转文本", "PDF提取公式", "论文OCR"
- User wants to convert academic papers to Markdown format

## Tool Selection

| Tool | Best For | Languages | Math Quality |
|------|----------|-----------|--------------|
| **Marker** (推荐) | 中英文论文、复杂公式 | Chinese + English | Excellent |
| **Nougat** | 纯英文论文、arXiv | English only | Excellent |

**推荐使用 Marker**：支持中英文混排，公式识别效果更好。

---

## Environment Setup

**Conda Environment**: `pdf-extractor`
**Python Path**: `D:\anaconda3\envs\pdf-extractor\python.exe`

### Key Dependencies
- PyTorch 2.10.0+cu128 (CUDA 12.8)
- marker-pdf (Surya OCR + Texify)
- nougat-ocr 0.1.17
- transformers

## Important: Keep This Skill Self-Contained (No Extra Installs)

This skill is expected to run using ONLY the existing `pdf-extractor` conda environment and the scripts in `scripts/`.

Rules:
- Do NOT run `pip install ...` / `conda install ...` / download random libraries during extraction.
- If a dependency is missing (e.g., Nougat crashes due to missing `torchvision`), do NOT try to fix by installing packages. Switch tools (prefer Marker) or report the environment issue.
- Slow runtime is normal for Marker (especially with `--ark-code-latest`). Prefer splitting the PDF rather than changing tools or adding dependencies.

Recommended approach for long PDFs:
- Use `--page-range` (0-based) to extract per page or small page batches.
- Merge the resulting markdown files afterward (simple concatenation is fine). Keep the combined file in the same folder as the per-page outputs so image links remain valid.

Example (per-page extraction with LLM mode):
```bash
D:\anaconda3\envs\pdf-extractor\python.exe C:\Users\cr\.config\opencode\skills\pdf-extractor\scripts\pdf2md_marker.py "paper.pdf" --ark-code-latest --page-range "0" -o "out/page_01.md"
```

---

## Tool 1: Marker (推荐 - 中英文支持)

### Command Line

```bash
# 转换中文论文 (默认支持中英文)
D:\anaconda3\envs\pdf-extractor\python.exe C:\Users\cr\.config\opencode\skills\pdf-extractor\scripts\pdf2md_marker.py "论文.pdf"

# 指定输出路径
D:\anaconda3\envs\pdf-extractor\python.exe C:\Users\cr\.config\opencode\skills\pdf-extractor\scripts\pdf2md_marker.py "paper.pdf" -o "output.md"

# 强制 OCR (用于扫描版 PDF)
D:\anaconda3\envs\pdf-extractor\python.exe C:\Users\cr\.config\opencode\skills\pdf-extractor\scripts\pdf2md_marker.py "scanned.pdf" --force-ocr

# 使用火山方舟 Coding Plan (OpenAI-compatible) 增强转换质量（表格/公式/跨页结构更稳）
# 注意：默认走 ark-code-latest，后台会自动路由到合适的模型
D:\anaconda3\envs\pdf-extractor\python.exe C:\Users\cr\.config\opencode\skills\pdf-extractor\scripts\pdf2md_marker.py "paper.pdf" --ark-code-latest

# 只跑第 1 页做快速验证（0-based page index）
D:\anaconda3\envs\pdf-extractor\python.exe C:\Users\cr\.config\opencode\skills\pdf-extractor\scripts\pdf2md_marker.py "paper.pdf" --ark-code-latest --page-range "0" -o "out_first_page.md"

# 如需自定义（不推荐）：也可以手动指定 --openai-base-url/--openai-api-key/--openai-model

# 指定语言
D:\anaconda3\envs\pdf-extractor\python.exe C:\Users\cr\.config\opencode\skills\pdf-extractor\scripts\pdf2md_marker.py "paper.pdf" --languages Chinese English Japanese
```

### Python API

```python
import sys
sys.path.insert(0, r'C:\Users\cr\.config\opencode\skills\pdf-extractor\scripts')
from pdf2md_marker import convert_pdf, convert_pdf_cli

# 简单用法
output_file = convert_pdf_cli('论文.pdf', 'output.md')

# 完整 API
markdown_text, metadata = convert_pdf(
    'paper.pdf',
    output_dir='./output',
    force_ocr=False,
    batch_multiplier=2,
    languages=['Chinese', 'English']
)
print(markdown_text)
```

### Marker Options

| Option | Description |
|--------|-------------|
| `-o, --output` | Output file (.md) or directory |
| `--force-ocr` | Force OCR even for text PDFs |
| `--batch-multiplier` | Batch size multiplier (default: 2) |
| `--languages` | Languages in document (default: Chinese English) |

---

## Tool 2: Nougat (纯英文论文)

### Command Line

```bash
# Convert entire PDF
D:\anaconda3\envs\pdf-extractor\python.exe C:\Users\cr\.config\opencode\skills\pdf-extractor\scripts\pdf2latex.py "paper.pdf"

# Convert specific pages
D:\anaconda3\envs\pdf-extractor\python.exe C:\Users\cr\.config\opencode\skills\pdf-extractor\scripts\pdf2latex.py "paper.pdf" -p 0-5

# Custom output
D:\anaconda3\envs\pdf-extractor\python.exe C:\Users\cr\.config\opencode\skills\pdf-extractor\scripts\pdf2latex.py "paper.pdf" -o output.mmd

# Save each page separately
D:\anaconda3\envs\pdf-extractor\python.exe C:\Users\cr\.config\opencode\skills\pdf-extractor\scripts\pdf2latex.py "paper.pdf" --per-page
```

### Python API

```python
import sys
sys.path.insert(0, r'C:\Users\cr\.config\opencode\skills\pdf-extractor\scripts')
from pdf2latex import load_model, process_pdf, save_results

# Load model (uses GPU if available)
model, device = load_model()

# Process PDF
results = process_pdf('paper.pdf', model, device)

# Save as single markdown file
save_results(results, 'output.mmd')

# Or save per page
save_results(results, 'output_pages/', format='pages')
```

### Nougat Options

| Option | Description |
|--------|-------------|
| `-o, --output` | Output file or directory |
| `-p, --pages` | Page range (e.g., "0-5" or "1,3,5") |
| `-m, --model` | Model tag (default: 0.1.0-base) |
| `--dpi` | Render DPI (default: 300) |
| `--cpu` | Force CPU mode |
| `--per-page` | Save each page separately |

---

## Output Format

Both tools output Markdown with LaTeX math:
- Text is extracted as regular markdown
- Mathematical formulas are in LaTeX format:
  - Inline: `$formula$`
  - Display: `$$formula$$`
- Tables, figures, and references are preserved
- Marker also extracts images to separate folder

---

## Comparison

| Feature | Marker | Nougat |
|---------|--------|--------|
| Chinese Support | ✓ Excellent | ✗ Poor |
| English Support | ✓ Excellent | ✓ Excellent |
| Math Formulas | ✓ (Texify) | ✓ (Native) |
| Table Extraction | ✓ | ✓ |
| Image Extraction | ✓ | ✗ |
| Speed (RTX 4060) | ~2 min/page | ~10-15 sec/page |
| OCR Quality | Excellent | Good |

---

## Troubleshooting

### Import Errors
Make sure you're using the correct Python:
```bash
D:\anaconda3\envs\pdf-extractor\python.exe your_script.py
```

### CUDA Out of Memory
Try CPU mode (Nougat) or reduce batch size (Marker):
```bash
# Nougat: use CPU
D:\anaconda3\envs\pdf-extractor\python.exe pdf2latex.py paper.pdf --cpu

# Marker: reduce batch multiplier
D:\anaconda3\envs\pdf-extractor\python.exe pdf2md_marker.py paper.pdf --batch-multiplier 1
```

### Chinese Characters Not Recognized
Use Marker instead of Nougat for Chinese documents.

### Slow Processing
- Marker is slower but more accurate (uses multiple ML models)
- For faster processing on English-only papers, use Nougat
- Ensure GPU is being used (check CUDA availability)

---

## Model Information

**Marker Models** (downloaded automatically):
- Surya OCR: Text detection and recognition
- Texify: Math formula recognition
- Layout analysis models

**Nougat Base Model** (1.31 GB):
- Location: `C:\Users\cr\.cache\torch\hub\nougat-0.1.0-base`
- Best for: Standard academic papers, arXiv papers

---

## Example Workflow

```python
import sys
sys.path.insert(0, r'C:\Users\cr\.config\opencode\skills\pdf-extractor\scripts')

def extract_paper(pdf_path, is_chinese=True):
    """
    Extract text and formulas from academic paper.
    
    Args:
        pdf_path: Path to PDF file
        is_chinese: True for Chinese papers, False for English only
    
    Returns:
        Extracted markdown text
    """
    if is_chinese:
        from pdf2md_marker import convert_pdf
        text, _ = convert_pdf(pdf_path, languages=['Chinese', 'English'])
    else:
        from pdf2latex import load_model, process_pdf
        model, device = load_model()
        results = process_pdf(pdf_path, model, device)
        text = '\n\n'.join([t for _, t in results])
    
    return text

# Usage
text = extract_paper('中文论文.pdf', is_chinese=True)
print(text)
```
