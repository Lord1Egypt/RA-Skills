---
name: ph-hs-code-finder
description: Query Philippines customs HS codes for products exported to the Philippines. Use when user asks about "菲律宾海关编码", "HS code Philippines", "tariff code", "customs classification", "import duty Philippines", or when they need to find the harmonized system code for goods shipped to the Philippines. Supports product name/image input and searches the official Tariff Commission website (tariffcommission.gov.ph).
---

# Philippines HS Code Finder

Query customs harmonized system (HS) codes for products exported to the Philippines using the official Tariff Commission tariff book.

## Data Source

- **Website**: https://www.tariffcommission.gov.ph/tariff-book-2022
- **Storage**: Google Drive (Chapter PDFs are hosted on Google Drive)
- **Chapters**: 01-97 (excl. 77 which is reserved)

## How It Works

**Important Discovery**: The tariff book PDFs are hosted on **Google Drive**, not directly on the government website. The workflow is:

1. Visit https://www.tariffcommission.gov.ph/tariff-book-2022
2. Click a Chapter link → Opens Google Drive file
3. Download PDF from Google Drive
4. Search for HS codes in the PDF

## Quick Start (One Command)

Use the unified query tool for the complete workflow:

```bash
python3 ~/.codex/skills/ph-hs-code-finder/scripts/query_hs_code.py "<product_name>"
```

Example:
```bash
python3 ~/.codex/skills/ph-hs-code-finder/scripts/query_hs_code.py "hair dryer"
```

This will:
1. Analyze the product and suggest chapters
2. Open browser to get Google Drive link
3. Download the PDF
4. Search for matching HS codes
5. Display results with source URL

## Step-by-Step Workflow

### Step 1: Suggest Chapter

First, determine which chapter the product belongs to:

```bash
python3 ~/.codex/skills/ph-hs-code-finder/scripts/suggest_chapter.py "<product_name>"
```

Example:
```bash
python3 ~/.codex/skills/ph-hs-code-finder/scripts/suggest_chapter.py "mobile phone charger"
# Output:
# Product: mobile phone charger
# Matched keywords: phone, charger, mobile
# Suggested chapters:
#   1. Chapter 85: Electrical machinery and equipment (score: 30)
```

### Step 2: Download Chapter PDF

Use Playwright to automatically get the Google Drive link and download:

```bash
python3 ~/.codex/skills/ph-hs-code-finder/scripts/get_chapter_pdf.py <chapter_number> [output_directory]
```

Example:
```bash
python3 ~/.codex/skills/ph-hs-code-finder/scripts/get_chapter_pdf.py 85 ~/Downloads
```

**What happens:**
1. Opens Chrome browser (headed mode)
2. Navigates to tariff book page
3. Clicks the Chapter link
4. Captures Google Drive URL
5. Downloads PDF using curl/wget

### Step 3: Search HS Code

Once you have the PDF, search for the product:

```bash
python3 ~/.codex/skills/ph-hs-code-finder/scripts/search_hs_code.py \
  <pdf_path> <keyword1> [keyword2] ...
```

Example:
```bash
python3 ~/.codex/skills/ph-hs-code-finder/scripts/search_hs_code.py \
  ~/Downloads/Chapter_85.pdf "hair" "dryer" --source "<gdrive_url>"
```

## Common Chapter Reference

| Chapter | Category | Example Products |
|---------|----------|------------------|
| 39 | Plastics | Bags, bottles, containers |
| 61/62 | Apparel | Clothing, garments, fashion |
| 64 | Footwear | Shoes, boots, sandals |
| 73 | Iron/Steel | Hardware, screws, tools |
| 76 | Aluminium | Profiles, sheets, foil |
| 84 | Machinery | Computers, printers, equipment |
| **85** | **Electrical** | **Phones, chargers, electronics** |
| 87 | Vehicles | Cars, motorcycles, parts |
| 90 | Optical/Medical | Cameras, instruments, lenses |
| 94 | Furniture | Chairs, tables, bedding |
| 95 | Toys/Sports | Toys, games, exercise equipment |

## Handling Different Input Types

### 1. Product Name (Text)

```bash
python3 query_hs_code.py "wireless bluetooth headphone"
```

### 2. Product Image

If user provides an image:
1. Analyze the image to identify the product
2. Extract product name/description
3. Run query with identified product name

Example workflow:
```python
# Identify product from image
product = "hair dryer"  # identified from image

# Run query
python3 query_hs_code.py "$product"
```

## Prerequisites

Install required dependencies:

```bash
# Install Python packages
pip install pdfplumber playwright

# Install Playwright browsers
playwright install chromium
```

## Google Drive Download Handling

The script handles Google Drive downloads automatically:

1. **Small files** (< 100MB): Direct download works
2. **Large files**: May require confirmation (script uses wget as fallback)
3. **Virus scan warning**: For executable files (not applicable for PDFs)

If automatic download fails:
- The script will output the Google Drive URL
- User can manually download and provide the file path
- Then run search with `--pdf` flag

## Output Format

Results are displayed as markdown table:

```markdown
## 查询结果: hair dryer

**源文件**: [Google Drive Link](https://drive.google.com/file/d/xxxxx/view)

| HS编码 | 商品描述 | 页码 |
|--------|----------|------|
| 8516.31.00 | Hair dryers | 15 |
| 8516.32.00 | Other hair-dressing apparatus | 15 |

============================================================
  ✓ RECOMMENDED HS CODE: 8516.31.00
  Description: 8516.31.00 - Hair dryers 1 1 1 1 1 1...
============================================================
```

## Troubleshooting

### Browser doesn't open
```bash
# Check Playwright installation
playwright install chromium

# Verify Chrome/Chromium is available
which chromium || which google-chrome || which chromium-browser
```

### Download fails
The website has WAF protection. If direct download fails:
1. Script will open browser automatically
2. Click Chapter link manually if needed
3. Copy Google Drive URL
4. Download manually or provide to script

### PDF not found
Ensure the PDF is a valid file:
```bash
file Chapter_85.pdf
# Should output: PDF document, version 1.x
```

## Example: Complete Hair Dryer Query

```bash
# Step 1: Suggest chapter
$ python3 suggest_chapter.py "hair dryer"
Product: hair dryer
Matched keywords: hair, dryer
Suggested chapters:
  1. Chapter 85: Electrical machinery and equipment
✓ Best match: Chapter 85

# Step 2 & 3: Download and search (combined)
$ python3 query_hs_code.py "hair dryer"

# Output:
============================================================
  Philippines HS Code Query: hair dryer
============================================================

Step 1: Analyzing product category...

Product: hair dryer
Matched keywords: hair, dryer

Suggested chapters:
  1. Chapter 85: Electrical machinery and equipment (score: 20)

Using top suggestion: Chapter 85

Step 2: Downloading Chapter 85 PDF...
Opening browser to find Chapter 85...
Found link: https://drive.google.com/file/d/xxxxx/view
Downloading Chapter 85...
✓ Downloaded: Chapter_85.pdf (1197.0 KB)

Step 3: Searching HS codes for "hair dryer"...

## 查询结果: hair dryer

**源文件**: [Google Drive](https://drive.google.com/file/d/xxxxx/view)

| HS编码 | 商品描述 | 页码 |
|--------|----------|------|
| 8516.31.00 | - Hair dryers | 15 |
| 8516.32.00 | - Other hair-dressing apparatus | 15 |

============================================================
  ✓ RECOMMENDED HS CODE: 8516.31.00
============================================================
```

## Required Output

Every response MUST include:
1. The HS code(s) found
2. Product description from tariff book
3. **Source URL** (Google Drive link)
4. Page number in PDF
