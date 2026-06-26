---
name: invoice-extractor
description: Extract invoice information from images and PDF files using Baidu OCR API, export to Excel. Supports single file, multiple files, or entire directory processing. Use when the user mentions invoices, invoice recognition, extracting invoice data, processing receipts, converting invoices to Excel, or batch processing invoice files.
---

# Invoice Extractor

Extract invoice information from images (PNG, JPG) and PDF files, then export to Excel format.

## Capabilities

- **Multi-format support**: PNG, JPG, JPEG, BMP, TIFF, PDF
- **High accuracy**: Uses Baidu OCR API specialized for invoice recognition
- **Complete fields**: Extracts all invoice fields including buyer/seller info, amounts, items
- **Excel export**: Formatted Excel output with summary and detail sheets
- **Flexible input**: Single file, multiple files, or entire directory processing
- **Batch processing**: Process hundreds of invoices in one command
- **Preview mode**: List files before processing

## Prerequisites

1. Baidu Cloud OCR API credentials (free tier: 50,000 requests/day)
2. Python environment with required packages

## Quick Start

### 1. Setup Baidu OCR

Get API credentials from https://cloud.baidu.com/product/ocr:
1. Register/login to Baidu Cloud
2. Create an application
3. Get API Key and Secret Key

### 2. Configure

Create `config.txt` in the project root:
```
BAIDU_API_KEY=your_api_key_here
BAIDU_SECRET_KEY=your_secret_key_here
```

Or run the setup wizard:
```bash
python main_baidu.py --setup
```

### 3. Run

**Process a single file:**
```bash
python main_baidu.py -f invoice.pdf
```

**Process multiple files:**
```bash
python main_baidu.py -f invoice1.pdf -f invoice2.png
```

**Process entire directory:**
```bash
python main_baidu.py -i ./fp
```

**Mixed mode (directory + extra files):**
```bash
python main_baidu.py -i ./fp -f extra_invoice.pdf
```

Output will be saved to `output/` directory as Excel file.

## Workflow

```
Task Progress:
- [ ] Check prerequisites (Baidu API credentials)
- [ ] Choose input method (single file / multiple files / directory)
- [ ] Scan and collect invoice files
- [ ] Preview files (optional with --list)
- [ ] Process each file with Baidu OCR
- [ ] Parse invoice fields
- [ ] Export to Excel
- [ ] Verify output
```

## Input Methods

### Single File
Process one specific invoice file:
```bash
python main_baidu.py -f invoice.pdf
python main_baidu.py -f "path/to/invoice.png"
```

### Multiple Files
Process several specific files:
```bash
python main_baidu.py -f file1.pdf -f file2.png -f file3.jpg
```

### Entire Directory
Process all invoice files in a directory (recursive):
```bash
python main_baidu.py -i ./my_invoices
python main_baidu.py -i "/path/to/invoice/folder"
```

### Mixed Mode
Combine directory and individual files:
```bash
python main_baidu.py -i ./fp -f ./extra/invoice.pdf
```

### Preview Mode
List files without processing:
```bash
python main_baidu.py -i ./fp --list
```

## Extracted Fields

### Basic Information
- Invoice code (发票代码)
- Invoice number (发票号码)
- Invoice date (开票日期)
- Invoice type (发票类型)

### Buyer Information
- Name (购买方名称)
- Tax number (纳税人识别号)
- Address and phone (地址电话)
- Bank account (开户行及账号)

### Seller Information
- Name (销售方名称)
- Tax number (纳税人识别号)
- Address and phone (地址电话)
- Bank account (开户行及账号)

### Amounts
- Total amount (合计金额)
- Total tax (合计税额)
- Amount with tax (价税合计)

### Items
- Product name (货物名称)
- Specification (规格型号)
- Unit (单位)
- Quantity (数量)
- Unit price (单价)
- Amount (金额)
- Tax rate (税率)
- Tax amount (税额)

## Command Line Options

```bash
python main_baidu.py [options]

Input Options:
  -f FILE, --file FILE     Specify invoice file (can be used multiple times)
  -i DIR, --input DIR      Input directory (default: fp)

Output Options:
  -o DIR, --output DIR     Output directory (default: output)
  -n NAME, --name NAME     Output filename prefix (default: 发票信息)

Authentication Options:
  --api-key KEY            Baidu API Key
  --secret-key KEY         Baidu Secret Key

Other Options:
  --setup                  Run configuration wizard
  --list                   List files to be processed without processing
  -h, --help              Show help
```

## Usage Examples

### Example 1: Single File
```bash
python main_baidu.py -f "invoice.pdf"
```

### Example 2: Multiple Files
```bash
python main_baidu.py -f "1.pdf" -f "2.png" -f "3.jpg"
```

### Example 3: Entire Directory
```bash
python main_baidu.py -i "./2024_invoices"
```

### Example 4: Preview Before Processing
```bash
python main_baidu.py -i ./fp --list
# Then process:
python main_baidu.py -i ./fp
```

### Example 5: Mixed Input
```bash
python main_baidu.py -i ./fp -f ./urgent/invoice.pdf -o ./output -n "March_2024"
```

### Example 6: Custom Output
```bash
python main_baidu.py -i ./fp -o ./reports -n "Q1_Invoice_Summary"
```

## Project Structure

```
.
├── fp/                      # Place invoice files here
├── output/                  # Excel output directory
├── src/
│   ├── main_baidu.py       # Main entry point
│   ├── baidu_ocr_extractor.py  # Baidu OCR wrapper
│   ├── invoice_model.py    # Data models
│   ├── excel_exporter.py   # Excel export
│   └── config.py           # Configuration
├── scripts/                 # Utility scripts
│   ├── batch_process.py    # Batch processing helper
│   └── verify_export.py    # Verify Excel export
├── config.txt              # API credentials
├── requirements.txt        # Dependencies
├── SKILL.md                # This file
├── setup.md                # Detailed setup guide
└── examples.md             # Usage examples
```

## Utility Scripts

### Batch Processing Helper
```bash
python scripts/batch_process.py /path/to/invoices
```

### Verify Export
```bash
python scripts/verify_export.py output/invoice_info.xlsx
```

## Error Handling

Common issues and solutions:

**"Baidu OCR authentication failed"**
- Check API Key and Secret Key in config.txt
- Verify credentials are correct in Baidu Cloud console

**"No invoice files found"**
- Ensure files are in the specified directory
- Check file formats (supported: png, jpg, jpeg, bmp, tiff, pdf)
- Use `--list` to see what files are detected

**"Image format error"**
- PDF files are automatically converted to images
- Ensure PDF is not corrupted or password-protected

**"File not found"**
- Check file path is correct
- Use quotes for paths with spaces: `"path/to/file name.pdf"`

## Advanced Usage

### Environment Variables
Set credentials via environment:
```bash
export BAIDU_API_KEY="your_key"
export BAIDU_SECRET_KEY="your_secret"
```

### Batch Processing Script
Create a script for monthly processing:
```bash
#!/bin/bash
MONTH=$(date +%Y%m)
python main_baidu.py \
  -i "/invoices/$MONTH" \
  -o "/reports/$MONTH" \
  -n "Invoice_Report_$MONTH"
```

## Additional Resources

- For detailed setup instructions, see [setup.md](setup.md)
- For more examples, see [examples.md](examples.md)
- For API documentation, visit https://cloud.baidu.com/doc/OCR/index.html
