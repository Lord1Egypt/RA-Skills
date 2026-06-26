# Invoice Extractor Examples

## Table of Contents
1. [Basic Examples](#basic-examples)
2. [Advanced Usage](#advanced-usage)
3. [Batch Processing](#batch-processing)
4. [Utility Scripts](#utility-scripts)
5. [Integration Examples](#integration-examples)

---

## Basic Examples

### Example 1: Single File Processing

Process one specific invoice file:

```bash
# PDF invoice
python src/main_baidu.py -f invoice.pdf

# Image invoice
python src/main_baidu.py -f "invoice.png"

# With spaces in filename
python src/main_baidu.py -f "path/to/my invoice.pdf"
```

**Output:**
```
============================================================
Invoice Extractor (Baidu OCR)
============================================================
Time: 2026-03-19 10:30:00
============================================================

Scanning files...
Found 1 files to process
[OK] Baidu OCR authentication successful

[1/1] Processing: invoice.pdf
Converting PDF to image...
[OK] Successfully extracted: 26437000000033943419

[OK] Successfully extracted 1 invoices

Extraction Summary:
------------------------------------------------------------
1. Invoice Number: 26437000000033943419
   Date: 2026-01-02
   Seller: China Mobile Communications Group...
   Amount: 169.00

Starting Excel export...
[OK] Successfully exported 1 records to: output/invoice_info_20260319.xlsx
```

---

### Example 2: Multiple Files

Process several specific files:

```bash
python src/main_baidu.py -f invoice1.pdf -f invoice2.png -f invoice3.jpg
```

---

### Example 3: Directory Processing

Process all invoices in a directory:

```bash
# Default fp/ directory
python src/main_baidu.py

# Custom directory
python src/main_baidu.py -i ./my_invoices

# Absolute path
python src/main_baidu.py -i "/Users/accounting/2024/Q1"
```

**Recursive processing:** The tool automatically scans subdirectories.

---

### Example 4: Preview Mode

List files without processing:

```bash
python src/main_baidu.py -i ./fp --list
```

**Output:**
```
Scanning files...
Found 5 files:
  1. fp\invoice_001.pdf
  2. fp\invoice_002.png
  3. fp\invoice_003.jpg
  4. fp\subfolder\invoice_004.pdf
  5. fp\subfolder\invoice_005.png
```

Use this to verify what will be processed before running the actual extraction.

---

## Advanced Usage

### Example 5: Mixed Input Mode

Combine directory and individual files:

```bash
# Process directory plus extra files
python src/main_baidu.py -i ./fp -f ./urgent/invoice.pdf -f ./special/case.png
```

**Use case:** You have most invoices organized in `fp/` but received a few urgent ones elsewhere.

---

### Example 6: Custom Output

Specify output directory and filename:

```bash
python src/main_baidu.py \
  -i ./fp \
  -o ./reports/2024 \
  -n "March_Invoice_Summary"
```

**Result:** `./reports/2024/March_Invoice_Summary_20260319_103000.xlsx`

---

### Example 7: Command Line Authentication

Override config file with command line credentials:

```bash
python src/main_baidu.py \
  -i ./fp \
  --api-key "your_api_key" \
  --secret-key "your_secret_key"
```

**Use case:** Temporary use or testing with different credentials.

---

## Batch Processing

### Example 8: Monthly Report Generation

Create a script for monthly processing:

```bash
#!/bin/bash
# monthly_invoice_report.sh

MONTH=$(date +%Y%m)
INPUT_DIR="/shared/invoices/$MONTH"
OUTPUT_DIR="/reports/$MONTH"

cd /opt/invoice-extractor

echo "Processing invoices for $MONTH..."

python src/main_baidu.py \
  -i "$INPUT_DIR" \
  -o "$OUTPUT_DIR" \
  -n "Invoice_Report_$MONTH"

echo "Report generated: $OUTPUT_DIR/Invoice_Report_$MONTH.xlsx"
```

**Usage:**
```bash
chmod +x monthly_invoice_report.sh
./monthly_invoice_report.sh
```

---

### Example 9: Using Batch Process Helper

Use the provided batch helper script:

```bash
# Simple usage
python scripts/batch_process.py ./invoices

# With custom output
python scripts/batch_process.py ./invoices -o ./output -n "Q1_2024"

# Without item details (faster)
python scripts/batch_process.py ./invoices --no-items
```

---

### Example 10: Process by Date Range

Process invoices from a specific date range:

```bash
# Find invoices from March 2024 and process them
find ./invoices -name "*202403*.pdf" -o -name "*2024-03*.pdf" | \
  xargs -I {} python src/main_baidu.py -f {}
```

---

## Utility Scripts

### Example 11: Verify Export Quality

Check the exported Excel file:

```bash
python scripts/verify_export.py output/invoice_info_20260319.xlsx
```

**Output:**
```
============================================================
Excel File Verification Report
============================================================
File: output/invoice_info_20260319.xlsx
------------------------------------------------------------

Number of sheets: 2
Sheets: 发票信息, 商品明细

【Invoice Information Sheet】
  Records: 50

  Field Completeness:
    Invoice Number: 50/50 (100.0%)
    Invoice Date: 50/50 (100.0%)
    Seller Name: 48/50 (96.0%)
    Total Amount: 50/50 (100.0%)

  Amount Statistics:
    Total: 125,680.50
    Average: 2,513.61
    Maximum: 15,800.00
    Minimum: 120.00

  Date Range:
    Earliest: 2024-03-01
    Latest: 2024-03-31

【Item Details Sheet】
  Records: 156
  Involved Invoices: 50

============================================================
[OK] Verification Complete
============================================================
```

---

### Example 12: Compare Multiple Exports

Compare reports from different months:

```bash
# Generate reports for each month
for month in 01 02 03; do
  python src/main_baidu.py \
    -i "./2024/$month" \
    -o "./reports" \
    -n "2024${month}_Invoices"
done

# Verify all reports
for file in ./reports/2024*_Invoices_*.xlsx; do
  echo "Checking: $file"
  python scripts/verify_export.py "$file"
done
```

---

## Integration Examples

### Example 13: Python Script Integration

Use the tool in your Python script:

```python
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from config import Config
from baidu_ocr_extractor import BaiduInvoiceExtractor
from excel_exporter import ExcelExporter

# Load config
Config.load_from_file()

# Initialize extractor
extractor = BaiduInvoiceExtractor(
    api_key=Config.BAIDU_API_KEY,
    secret_key=Config.BAIDU_SECRET_KEY
)

# Process single file
invoice = extractor.extract_from_file("path/to/invoice.pdf")

if invoice:
    print(f"Invoice Number: {invoice.invoice_number}")
    print(f"Amount: {invoice.total_amount_with_tax}")
    print(f"Items: {len(invoice.items)}")
```

---

### Example 14: Automated Email Report

Send report via email after processing:

```bash
#!/bin/bash
# process_and_email.sh

RECIPIENT="accounting@company.com"
INPUT_DIR="./invoices"
OUTPUT_DIR="./output"

# Process invoices
python src/main_baidu.py -i "$INPUT_DIR" -o "$OUTPUT_DIR" -n "Daily_Report"

# Find latest report
LATEST_REPORT=$(ls -t $OUTPUT_DIR/*.xlsx | head -1)

# Send email with attachment (using mutt or mail)
echo "Invoice processing complete. See attachment." | \
  mutt -s "Daily Invoice Report" -a "$LATEST_REPORT" -- "$RECIPIENT"

echo "Report sent to $RECIPIENT"
```

---

### Example 15: Database Integration

Import extracted data to database:

```python
import pandas as pd
import sqlite3

# Read Excel
df = pd.read_excel('output/invoice_info.xlsx')

# Connect to database
conn = sqlite3.connect('invoices.db')

# Save to database
df.to_sql('invoices', conn, if_exists='append', index=False)

# Query example
result = pd.read_sql_query("""
    SELECT 销售方名称, SUM(价税合计) as total
    FROM invoices
    GROUP BY 销售方名称
    ORDER BY total DESC
""", conn)

print(result)
```

---

## Common Use Cases

### Monthly Expense Report

1. Collect all invoices for the month
2. Place in `fp/` directory
3. Run: `python src/main_baidu.py -n "2024_03_Expenses"`
4. Import Excel into accounting software

### Tax Preparation

1. Gather all invoices for tax year
2. Batch process with custom output name
3. Filter and categorize in Excel
4. Submit to tax authority

### Audit Documentation

1. Scan all paper invoices to PDF
2. Process with invoice extractor
3. Generate complete Excel records
4. Archive digital and physical copies

### Vendor Analysis

```python
import pandas as pd

# Read exported Excel
df = pd.read_excel('output/invoice_info.xlsx')

# Group by vendor
vendor_stats = df.groupby('销售方名称').agg({
    '价税合计': ['count', 'sum', 'mean']
}).round(2)

print(vendor_stats)
```

---

## Tips and Best Practices

### File Organization

```
invoices/
├── 2024/
│   ├── Q1/
│   │   ├── 01/
│   │   ├── 02/
│   │   └── 03/
│   └── Q2/
└── 2023/
    └── ...
```

Process by quarter:
```bash
python src/main_baidu.py -i "./2024/Q1" -n "2024_Q1_Invoices"
```

### Naming Conventions

Use descriptive names for output files:
- `2024_03_Marketing_Invoices`
- `Q1_Travel_Expenses`
- `Project_X_Vendor_Payments`

### Verification Workflow

1. Preview files: `python src/main_baidu.py -i ./fp --list`
2. Process: `python src/main_baidu.py -i ./fp`
3. Verify: `python scripts/verify_export.py output/*.xlsx`
4. Review Excel output before submitting

---

## Troubleshooting Examples

### Handle Failed Extractions

```bash
# Process with verbose output
python src/main_baidu.py -i ./fp 2>&1 | tee processing.log

# Check for failures
grep "FAIL" processing.log

# Re-process failed files only
python src/main_baidu.py -f failed_invoice1.pdf -f failed_invoice2.png
```

### Large Batch Processing

For very large batches (1000+ invoices), process in chunks:

```bash
# Split into subdirectories
mkdir -p batch_{1..10}
ls *.pdf | split -l 100 - batch_

# Process each batch
for i in {1..10}; do
  python src/main_baidu.py -i "./batch_$i" -o "./output" -n "Batch_$i"
done

# Merge results (using Python pandas)
python -c "
import pandas as pd
import glob

files = glob.glob('output/Batch_*.xlsx')
dfs = [pd.read_excel(f) for f in files]
combined = pd.concat(dfs, ignore_index=True)
combined.to_excel('output/Combined_Results.xlsx', index=False)
"
```
