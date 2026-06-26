#!/usr/bin/env python3
"""Parse a single PDF invoice and output structured CSV data."""

import sys
import os
import csv
import re
import json
from datetime import datetime

try:
    import fitz  # PyMuPDF
    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False

try:
    from PIL import Image
    import pytesseract
    HAS_OCR = True
except ImportError:
    HAS_OCR = False

try:
    import PyPDF2
    HAS_PYPDF2 = True
except ImportError:
    HAS_PYPDF2 = False


def extract_text_pymupdf(pdf_path):
    """Extract text from PDF using PyMuPDF."""
    if not HAS_PYMUPDF:
        return None
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        print(f"PyMuPDF error: {e}", file=sys.stderr)
        return None


def extract_text_pypdf2(pdf_path):
    """Extract text from PDF using PyPDF2."""
    if not HAS_PYPDF2:
        return None
    try:
        text = ""
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"PyPDF2 error: {e}", file=sys.stderr)
        return None


def extract_text_ocr(pdf_path):
    """Extract text from scanned PDF using OCR."""
    if not HAS_OCR or not HAS_PYMUPDF:
        return None
    try:
        doc = fitz.open(pdf_path)
        full_text = ""
        for page_num in range(len(doc)):
            page = doc[page_num]
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text = pytesseract.image_to_string(img)
            full_text += text + "\n"
        doc.close()
        return full_text
    except Exception as e:
        print(f"OCR error: {e}", file=sys.stderr)
        return None


def extract_invoice_fields(text):
    """Extract structured invoice fields from text."""
    data = {
        'vendor_name': '',
        'invoice_number': '',
        'invoice_date': '',
        'due_date': '',
        'line_items': [],
        'subtotal': '',
        'tax': '',
        'total': '',
        'currency': 'USD'
    }

    # Vendor name (usually at top)
    lines = text.strip().split('\n')
    if lines:
        data['vendor_name'] = lines[0].strip()

    # Invoice number patterns
    invoice_patterns = [
        r'[Ii]nvoice\s*[#:\s]*([A-Z0-9-]+)',
        r'Invoice\s+No\.?\s*[:\s]*([A-Z0-9-]+)',
        r'INV[-\s]?(\d+)',
    ]
    for pattern in invoice_patterns:
        match = re.search(pattern, text)
        if match:
            data['invoice_number'] = match.group(1)
            break

    # Date patterns
    date_patterns = [
        r'[Dd]ate[:\s]*(\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4})',
        r'[Ii]nvoice\s+[Dd]ate[:\s]*(\d{4}[/\-\.]\d{1,2}[/\-\.]\d{1,2})',
        r'(\d{1,2}/\d{1,2}/\d{2,4})',
    ]
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            data['invoice_date'] = match.group(1)
            break

    # Due date
    due_patterns = [
        r'[Dd]ue\s+[Dd]ate[:\s]*(\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4})',
        r'[Pp]ayment\s+[Dd]ue[:\s]*(\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4})',
    ]
    for pattern in due_patterns:
        match = re.search(pattern, text)
        if match:
            data['due_date'] = match.group(1)
            break

    # Total amount
    total_patterns = [
        r'[Tt]otal[:\s]*\$?([\d,]+\.?\d*)',
        r'Grand\s+[Tt]otal[:\s]*\$?([\d,]+\.?\d*)',
        r'Amount\s+[Dd]ue[:\s]*\$?([\d,]+\.?\d*)',
    ]
    for pattern in total_patterns:
        match = re.search(pattern, text)
        if match:
            data['total'] = match.group(1).replace(',', '')
            break

    # Subtotal
    subtotal_match = re.search(r'[Ss]ubtotal[:\s]*\$?([\d,]+\.?\d*)', text)
    if subtotal_match:
        data['subtotal'] = subtotal_match.group(1).replace(',', '')

    # Tax
    tax_match = re.search(r'[Tt]ax[:\s]*\$?([\d,]+\.?\d*)', text)
    if tax_match:
        data['tax'] = tax_match.group(1).replace(',', '')

    # Currency detection
    if '€' in text or 'EUR' in text:
        data['currency'] = 'EUR'
    elif '£' in text or 'GBP' in text:
        data['currency'] = 'GBP'

    # Simple line item detection (description + amount patterns)
    # This is a basic heuristic - complex invoices may need manual review
    line_item_pattern = re.findall(r'([A-Za-z][\w\s\-\.]+?)[\s]+([\d,]+\.?\d*)[\s]+([\d,]+\.?\d*)[\s]+([\d,]+\.?\d*)', text)
    if line_item_pattern:
        for item in line_item_pattern[:10]:  # Limit to 10 items
            desc, qty, unit_price, line_total = item
            data['line_items'].append({
                'description': desc.strip(),
                'quantity': qty.replace(',', ''),
                'unit_price': unit_price.replace(',', ''),
                'line_total': line_total.replace(',', '')
            })
    else:
        # Fallback: create a single line item with total
        if data['total']:
            data['line_items'].append({
                'description': 'Invoice total',
                'quantity': '1',
                'unit_price': data['total'],
                'line_total': data['total']
            })

    return data


def write_csv(data, output_path):
    """Write invoice data to CSV."""
    fieldnames = ['vendor_name', 'invoice_number', 'invoice_date', 'due_date',
                  'description', 'quantity', 'unit_price', 'line_total',
                  'subtotal', 'tax', 'total', 'currency']

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for item in data['line_items']:
            row = {
                'vendor_name': data['vendor_name'],
                'invoice_number': data['invoice_number'],
                'invoice_date': data['invoice_date'],
                'due_date': data['due_date'],
                'description': item.get('description', ''),
                'quantity': item.get('quantity', ''),
                'unit_price': item.get('unit_price', ''),
                'line_total': item.get('line_total', ''),
                'subtotal': data['subtotal'],
                'tax': data['tax'],
                'total': data['total'],
                'currency': data['currency']
            }
            writer.writerow(row)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Parse a PDF invoice and extract structured data')
    parser.add_argument('pdf_path', help='Path to the PDF invoice')
    parser.add_argument('--output', '-o', default='output.csv', help='Output CSV file path')
    parser.add_argument('--ocr', action='store_true', help='Use OCR for scanned PDFs')
    parser.add_argument('--json', action='store_true', help='Output JSON instead of CSV')
    args = parser.parse_args()

    if not os.path.exists(args.pdf_path):
        print(f"Error: File not found: {args.pdf_path}", file=sys.stderr)
        sys.exit(1)

    # Extract text
    text = None
    methods_tried = []

    if args.ocr:
        text = extract_text_ocr(args.pdf_path)
        methods_tried.append('OCR')
    else:
        text = extract_text_pymupdf(args.pdf_path)
        if text:
            methods_tried.append('PyMuPDF')
        else:
            text = extract_text_pypdf2(args.pdf_path)
            if text:
                methods_tried.append('PyPDF2')

    if not text:
        print("Error: Could not extract text from PDF. Try --ocr flag for scanned PDFs.", file=sys.stderr)
        print(f"Methods tried: {', '.join(methods_tried) if methods_tried else 'none'}", file=sys.stderr)
        sys.exit(1)

    # Extract fields
    data = extract_invoice_fields(text)

    if args.json:
        print(json.dumps(data, indent=2))
    else:
        write_csv(data, args.output)
        print(f"Data written to {args.output}")
        print(f"Vendor: {data['vendor_name']}")
        print(f"Invoice: {data['invoice_number']}")
        print(f"Total: {data['total']} {data['currency']}")
        print(f"Line items: {len(data['line_items'])}")


if __name__ == '__main__':
    main()
