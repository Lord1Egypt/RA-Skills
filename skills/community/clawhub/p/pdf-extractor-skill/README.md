# PDF Extractor Skill

Extract text and mathematical formulas from academic PDF papers. Supports both English and Chinese content.

## Installation

### 1. Create Conda Environment

```bash
conda create -n pdf-extractor python=3.10 -y
conda activate pdf-extractor
```

### 2. Install Dependencies

```bash
# PyTorch (CUDA 12.8)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128

# Marker (recommended for Chinese + English)
pip install marker-pdf

# Nougat (optional, for English-only papers)
pip install nougat-ocr

# Transformers
pip install transformers
```

### 3. Copy this skill to your device

```bash
# Option A: Clone from git (if you've pushed to a remote)
git clone <your-repo-url> ~/.config/opencode/skills/pdf-extractor

# Option B: Copy the directory manually
# Copy this entire folder to:
# - Windows: C:\Users\<username>\.config\opencode\skills\pdf-extractor
# - Linux/Mac: ~/.config/opencode/skills/pdf-extractor
```

## Usage

### Marker (Recommended - Chinese + English Support)

```bash
# Convert Chinese paper (default supports Chinese + English)
D:\anaconda3\envs\pdf-extractor\python.exe scripts/pdf2md_marker.py "论文.pdf"

# Specify output path
D:\anaconda3\envs\pdf-extractor\python.exe scripts/pdf2md_marker.py "paper.pdf" -o "output.md"

# Force OCR (for scanned PDFs)
D:\anaconda3\envs\pdf-extractor\python.exe scripts/pdf2md_marker.py "scanned.pdf" --force-ocr

# Use LLM enhancement (火山方舟 Coding Plan for better tables/formulas)
D:\anaconda3\envs\pdf-extractor\python.exe scripts/pdf2md_marker.py "paper.pdf" --ark-code-latest

# Extract only page 1 (0-based index)
D:\anaconda3\envs\pdf-extractor\python.exe scripts/pdf2md_marker.py "paper.pdf" --ark-code-latest --page-range "0" -o "out_first_page.md"
```

### Nougat (English-only Papers)

```bash
# Convert entire PDF
D:\anaconda3\envs\pdf-extractor\python.exe scripts/pdf2latex.py "paper.pdf"

# Convert specific pages
D:\anaconda3\envs\pdf-extractor\python.exe scripts/pdf2latex.py "paper.pdf" -p 0-5

# Custom output
D:\anaconda3\envs\pdf-extractor\python.exe scripts/pdf2latex.py "paper.pdf" -o output.mmd
```

## Tool Comparison

| Feature | Marker | Nougat |
|---------|--------|--------|
| Chinese Support | ✓ Excellent | ✗ Poor |
| English Support | ✓ Excellent | ✓ Excellent |
| Math Formulas | ✓ (Texify) | ✓ (Native) |
| Table Extraction | ✓ | ✓ |
| Image Extraction | ✓ | ✗ |
| Speed (RTX 4060) | ~2 min/page | ~10-15 sec/page |

## Output Format

Both tools output Markdown with LaTeX math:
- Inline: `$formula$`
- Display: `$$formula$$`

## Troubleshooting

### CUDA Out of Memory
```bash
# Nougat: use CPU
D:\anaconda3\envs\pdf-extractor\python.exe scripts/pdf2latex.py paper.pdf --cpu

# Marker: reduce batch multiplier
D:\anaconda3\envs\pdf-extractor\python.exe scripts/pdf2md_marker.py paper.pdf --batch-multiplier 1
```

### Chinese Characters Not Recognized
Use Marker instead of Nougat for Chinese documents.

## Model Cache Locations

Models are downloaded automatically on first use:
- **Nougat**: `C:\Users\<username>\.cache\torch\hub\nougat-0.1.0-base` (~1.31 GB)
- **Marker Models**: Downloaded by marker-pdf automatically
