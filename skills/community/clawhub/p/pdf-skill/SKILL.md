---
name: pdf
version: 2.0.0
description: Create, read, edit, merge, split PDF files. Supports text extraction, table extraction, form filling, watermarks, OCR, and HTML-to-PDF conversion.
category: document-processing
license: MIT
---

# PDF Skill v2.0

## Overview

Complete PDF processing using `pypdf`, `pdfplumber`, `weasyprint`, and command-line tools. Supports all common PDF operations.

## Installation & Dependencies

### Required
```bash
pip install pypdf pdfplumber weasyprint
```

### Optional
```bash
# For image conversion
brew install poppler
pip install pdf2image

# For OCR
pip install pytesseract
brew install tesseract

# For form filling
pip install pypdf-forms
```

## Quick Start

### Read PDF
```python
from pypdf import PdfReader

reader = PdfReader("document.pdf")
print(f"Pages: {len(reader.pages)}")

# Extract text from first page
page = reader.pages[0]
text = page.extract_text()
print(text)
```

### Merge PDFs
```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf in ["doc1.pdf", "doc2.pdf"]:
    reader = PdfReader(pdf)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as f:
    writer.write(f)
```

### Create PDF from HTML
```python
from weasyprint import HTML

HTML(string="<h1>Hello PDF</h1>").write_pdf("output.pdf")
```

## Complete API Reference

### Reading PDFs

```python
from pypdf import PdfReader

# Basic read
reader = PdfReader("document.pdf")

# Get page count
num_pages = len(reader.pages)

# Extract text from all pages
full_text = ""
for page in reader.pages:
    full_text += page.extract_text()

# Extract text from specific page
page = reader.pages[5]  # Page 6 (0-indexed)
text = page.extract_text()

# Get metadata
meta = reader.metadata
print(f"Title: {meta.title}")
print(f"Author: {meta.author}")
print(f"Subject: {meta.subject}")
print(f"Creator: {meta.creator}")
print(f"Creation Date: {meta.creation_date}")

# Get outline/bookmarks
outline = reader.outline
for item in outline:
    print(item.title)

# Check if encrypted
if reader.is_encrypted:
    reader.decrypt("password")
```

### Extracting Tables

```python
import pdfplumber
import pandas as pd

# Open PDF
with pdfplumber.open("document.pdf") as pdf:
    # Get page count
    print(f"Pages: {len(pdf.pages)}")
    
    # Extract tables from first page
    page = pdf.pages[0]
    tables = page.extract_tables()
    
    for i, table in enumerate(tables):
        print(f"Table {i+1}:")
        for row in table:
            print(row)

# Convert all tables to Excel
all_tables = []
with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table and len(table) > 1:
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

# Combine and export
if all_tables:
    combined = pd.concat(all_tables, ignore_index=True)
    combined.to_excel("extracted_tables.xlsx", index=False)
```

### Merging PDFs

```python
from pypdf import PdfWriter, PdfReader

# Merge multiple files
def merge_pdfs(input_files, output_file):
    writer = PdfWriter()
    
    for pdf_file in input_files:
        reader = PdfReader(pdf_file)
        print(f"Adding {pdf_file} ({len(reader.pages)} pages)")
        for page in reader.pages:
            writer.add_page(page)
    
    with open(output_file, "wb") as f:
        writer.write(f)
    
    print(f"✓ Merged {len(input_files)} files into {output_file}")

# Usage
merge_pdfs(["doc1.pdf", "doc2.pdf", "doc3.pdf"], "merged.pdf")
```

### Splitting PDFs

```python
from pypdf import PdfReader, PdfWriter

# Split into individual pages
def split_pdf(input_file, output_prefix):
    reader = PdfReader(input_file)
    
    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)
        
        output_file = f"{output_prefix}_page_{i+1}.pdf"
        with open(output_file, "wb") as f:
            writer.write(f)
    
    print(f"✓ Split into {len(reader.pages)} files")

# Extract specific pages
def extract_pages(input_file, output_file, page_numbers):
    """Extract specific pages (1-indexed)"""
    reader = PdfReader(input_file)
    writer = PdfWriter()
    
    for page_num in page_numbers:
        writer.add_page(reader.pages[page_num - 1])
    
    with open(output_file, "wb") as f:
        writer.write(f)
    
    print(f"✓ Extracted pages {page_numbers}")

# Usage
split_pdf("document.pdf", "page")
extract_pages("document.pdf", "selected.pdf", [1, 3, 5])
```

### Rotating Pages

```python
from pypdf import PdfReader, PdfWriter

# Rotate all pages
def rotate_pdf(input_file, output_file, rotation=90):
    reader = PdfReader(input_file)
    writer = PdfWriter()
    
    for page in reader.pages:
        page.rotate(rotation)  # 90, 180, or 270
        writer.add_page(page)
    
    with open(output_file, "wb") as f:
        writer.write(f)

# Rotate specific page
reader = PdfReader("input.pdf")
writer = PdfWriter()

for i, page in enumerate(reader.pages):
    if i == 0:  # Rotate first page only
        page.rotate(90)
    writer.add_page(page)

with open("output.pdf", "wb") as f:
    writer.write(f)
```

### Creating PDFs from HTML

```python
from weasyprint import HTML, CSS

# Basic HTML to PDF
html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        @page { size: A4; margin: 2cm; }
        body { font-family: Arial, sans-serif; }
        h1 { color: #333; }
    </style>
</head>
<body>
    <h1>Hello PDF</h1>
    <p>This is a test document.</p>
</body>
</html>
"""

HTML(string=html_content).write_pdf("output.pdf")

# With external CSS
HTML(
    string="<h1>Styled PDF</h1>",
    url_stylesheet="style.css"
).write_pdf("styled.pdf")

# Custom page size
HTML(string="<h1>Landscape</h1>").write_pdf(
    "landscape.pdf",
    stylesheets=[CSS(string="@page { size: landscape; }")]
)

# Add header/footer
html_with_pagenum = """
<!DOCTYPE html>
<html>
<head>
    <style>
        @page {
            size: A4;
            margin: 2cm;
            @bottom-center {
                content: "Page " counter(page) " of " counter(pages);
            }
        }
    </style>
</head>
<body>
    <h1>Document with Page Numbers</h1>
    <!-- Content here -->
</body>
</html>
"""
```

### Adding Watermarks

```python
from pypdf import PdfReader, PdfWriter
from io import BytesIO
from reportlab.pdfgen import canvas

def create_watermark(text, output_path):
    """Create a watermark PDF"""
    packet = BytesIO()
    c = canvas.Canvas(packet)
    
    # Draw text
    c.saveState()
    c.translate(300, 400)
    c.rotate(45)
    c.setFont("Helvetica-Bold", 50)
    c.setFillColorRGB(0.5, 0.5, 0.5, 0.3)  # Gray with transparency
    c.drawCentredString(0, 0, text)
    c.restoreState()
    
    c.save()
    packet.seek(0)
    
    return PdfReader(packet)

# Apply watermark
def watermark_pdf(input_file, output_file, watermark_text):
    reader = PdfReader(input_file)
    watermark = create_watermark(watermark_text, "temp.pdf")
    watermark_page = watermark.pages[0]
    writer = PdfWriter()
    
    for page in reader.pages:
        page.merge_page(watermark_page)
        writer.add_page(page)
    
    with open(output_file, "wb") as f:
        writer.write(f)

# Usage
watermark_pdf("document.pdf", "watermarked.pdf", "CONFIDENTIAL")
```

### Adding Password Protection

```python
from pypdf import PdfReader, PdfWriter

# Encrypt PDF
def protect_pdf(input_file, output_file, password):
    reader = PdfReader(input_file)
    writer = PdfWriter()
    
    for page in reader.pages:
        writer.add_page(page)
    
    # Add password
    writer.encrypt(password)
    
    with open(output_file, "wb") as f:
        writer.write(f)

# Usage
protect_pdf("document.pdf", "protected.pdf", "secretpassword")

# Decrypt PDF
reader = PdfReader("protected.pdf")
if reader.is_encrypted:
    reader.decrypt("secretpassword")
```

### Form Filling

```python
from pypdf import PdfReader, PdfWriter

def fill_form(input_pdf, output_pdf, data):
    """
    data: dict with field names and values
    """
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    
    # Get form fields
    fields = reader.get_form_text_fields()
    print("Available fields:", list(fields.keys()))
    
    # Fill fields
    writer.append_pages_from_reader(reader)
    writer.update_page_form_field_values(
        writer.pages[0],
        data
    )
    
    with open(output_pdf, "wb") as f:
        writer.write(f)

# Usage
form_data = {
    'name': 'John Doe',
    'email': 'john@example.com',
    'date': '2024-01-15'
}
fill_form("form.pdf", "filled_form.pdf", form_data)
```

### OCR for Scanned PDFs

```python
import pytesseract
from pdf2image import convert_from_path

def ocr_pdf(input_pdf, output_text):
    """Extract text from scanned PDF using OCR"""
    
    # Convert PDF to images
    images = convert_from_path(input_pdf, dpi=300)
    
    full_text = ""
    for i, image in enumerate(images):
        print(f"Processing page {i+1}...")
        text = pytesseract.image_to_string(image, lang='eng')
        full_text += f"\n--- Page {i+1} ---\n{text}"
    
    with open(output_text, 'w', encoding='utf-8') as f:
        f.write(full_text)
    
    print(f"✓ OCR complete: {output_text}")

# Usage
ocr_pdf("scanned.pdf", "extracted_text.txt")

# Create searchable PDF
def make_searchable(input_pdf, output_pdf):
    """Create searchable PDF from scanned document"""
    from pypdf import PdfReader, PdfWriter
    
    images = convert_from_path(input_pdf, dpi=300)
    writer = PdfWriter()
    
    for image in images:
        # This requires additional libraries for proper OCR PDF creation
        pass
    
    print("Searchable PDF creation requires additional setup")
```

## Complete Examples

### Example 1: PDF Report Generator

```python
from weasyprint import HTML
from datetime import datetime

def generate_report(data, output_file):
    """Generate PDF report from data"""
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            @page {{ size: A4; margin: 2cm; }}
            @bottom-center {{
                content: "Page " counter(page) " of " counter(pages);
                font-size: 10px;
            }}
            body {{ font-family: Arial, sans-serif; }}
            h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; }}
            h2 {{ color: #34495e; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
            th {{ background-color: #3498db; color: white; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
            .header {{ text-align: center; margin-bottom: 40px; }}
            .date {{ color: #7f8c8d; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Monthly Report</h1>
            <p class="date">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        </div>
        
        <h2>Summary</h2>
        <table>
            <tr><th>Metric</th><th>Value</th></tr>
            <tr><td>Total Sales</td><td>${data['total_sales']:,.2f}</td></tr>
            <tr><td>Orders</td><td>{data['orders']}</td></tr>
            <tr><td>Customers</td><td>{data['customers']}</td></tr>
        </table>
        
        <h2>Details</h2>
        <table>
            <tr><th>Product</th><th>Units</th><th>Revenue</th></tr>
    """
    
    for product in data['products']:
        html += f"""
            <tr>
                <td>{product['name']}</td>
                <td>{product['units']}</td>
                <td>${product['revenue']:,.2f}</td>
            </tr>
        """
    
    html += """
        </table>
    </body>
    </html>
    """
    
    HTML(string=html).write_pdf(output_file)
    print(f"✓ Report generated: {output_file}")

# Usage
data = {
    'total_sales': 125000,
    'orders': 450,
    'customers': 320,
    'products': [
        {'name': 'Product A', 'units': 100, 'revenue': 50000},
        {'name': 'Product B', 'units': 150, 'revenue': 75000}
    ]
}
generate_report(data, "monthly-report.pdf")
```

### Example 2: PDF Merger Tool

```python
from pypdf import PdfReader, PdfWriter
import os

class PDFMerger:
    def __init__(self):
        self.writer = PdfWriter()
        self.bookmarks = []
    
    def add_pdf(self, pdf_path, bookmark=None):
        """Add PDF to merger"""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        
        reader = PdfReader(pdf_path)
        start_page = len(self.writer.pages)
        
        for page in reader.pages:
            self.writer.add_page(page)
        
        if bookmark:
            self.bookmarks.append({
                'title': bookmark,
                'page': start_page
            })
        
        print(f"✓ Added {pdf_path} ({len(reader.pages)} pages)")
        return self
    
    def save(self, output_path):
        """Save merged PDF"""
        with open(output_path, "wb") as f:
            self.writer.write(f)
        print(f"✓ Merged PDF saved: {output_path}")
    
    def merge_files(self, input_files, output_file):
        """Merge multiple files at once"""
        for pdf in input_files:
            self.add_pdf(pdf, bookmark=os.path.basename(pdf))
        self.save(output_file)

# Usage
merger = PDFMerger()
merger.merge_files(
    ["doc1.pdf", "doc2.pdf", "doc3.pdf"],
    "merged.pdf"
)
```

### Example 3: PDF Text Extractor

```python
from pypdf import PdfReader
import json

class PDFExtractor:
    def __init__(self, pdf_path):
        self.reader = PdfReader(pdf_path)
        self.metadata = {}
    
    def get_metadata(self):
        """Extract PDF metadata"""
        meta = self.reader.metadata
        self.metadata = {
            'title': meta.title if meta.title else None,
            'author': meta.author if meta.author else None,
            'subject': meta.subject if meta.subject else None,
            'creator': meta.creator if meta.creator else None,
            'pages': len(self.reader.pages),
            'encrypted': self.reader.is_encrypted
        }
        return self.metadata
    
    def extract_text(self, pages=None):
        """Extract text from specified pages or all"""
        if pages is None:
            pages = range(len(self.reader.pages))
        
        text = {}
        for page_num in pages:
            page = self.reader.pages[page_num]
            text[f"page_{page_num + 1}"] = page.extract_text()
        
        return text
    
    def extract_all(self, output_json):
        """Extract everything to JSON"""
        result = {
            'metadata': self.get_metadata(),
            'text': self.extract_text()
        }
        
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Extracted to {output_json}")
        return result

# Usage
extractor = PDFExtractor("document.pdf")
extractor.extract_all("extracted.json")
```

## Error Handling

### Common Errors

#### Error: "PDF read failed"
```python
# Solution: Check if file exists and is valid
from pypdf import PdfReader
import os

if os.path.exists("file.pdf"):
    try:
        reader = PdfReader("file.pdf")
    except Exception as e:
        print(f"Error reading PDF: {e}")
```

#### Error: "Text extraction returned None"
```python
# Solution: PDF may be scanned/image-based
# Use OCR instead
page = reader.pages[0]
text = page.extract_text()
if text is None or text.strip() == "":
    print("PDF may be scanned. Use OCR.")
```

#### Error: "WeasyPrint font warning"
```python
# Solution: Install fonts or use web-safe fonts
# Suppress warnings
import logging
logger = logging.getLogger('weasyprint')
logger.setLevel(logging.ERROR)
```

## Best Practices

### 1. Always Check for Encryption
```python
reader = PdfReader("file.pdf")
if reader.is_encrypted:
    reader.decrypt("password")
```

### 2. Handle Large PDFs Efficiently
```python
# Process page by page instead of loading all
reader = PdfReader("large.pdf")
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    # Process and discard
```

### 3. Use Appropriate DPI for OCR
```python
# 300 DPI is standard for OCR
images = convert_from_path("scanned.pdf", dpi=300)
```

### 4. Validate Before Distribution
```python
# Check PDF is valid
from pypdf import PdfReader
try:
    reader = PdfReader("output.pdf")
    print(f"✓ Valid PDF with {len(reader.pages)} pages")
except Exception as e:
    print(f"✗ Invalid PDF: {e}")
```

## Testing Your Setup

```python
# test-pdf.py
from pypdf import PdfReader, PdfWriter
from weasyprint import HTML
import os

print("Testing PDF setup...")

# Test 1: Create PDF from HTML
HTML(string="<h1>Test PDF</h1>").write_pdf("test-create.pdf")
assert os.path.exists("test-create.pdf")
print("✓ PDF creation test passed")

# Test 2: Read PDF
reader = PdfReader("test-create.pdf")
assert len(reader.pages) == 1
print("✓ PDF read test passed")

# Test 3: Extract text
text = reader.pages[0].extract_text()
assert "Test PDF" in text
print("✓ Text extraction test passed")

# Cleanup
os.remove("test-create.pdf")
print("✓ All tests passed!")
```

Run test:
```bash
python test-pdf.py
```

## License

MIT License - See LICENSE file for details.
