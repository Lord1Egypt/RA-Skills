#!/usr/bin/env python3
"""Parse multiple PDF invoices from a directory and output consolidated CSV/Excel."""

import sys
import os
import glob
import csv
import json
from datetime import datetime

# Import the single-invoice parser
sys.path.insert(0, os.path.dirname(__file__))
from parse_invoice import extract_text_pymupdf, extract_text_pypdf2, extract_text_ocr, extract_invoice_fields, write_csv


def parse_directory(input_dir, output_path, use_ocr=False):
    """Parse all PDFs in a directory and create consolidated output."""
    pdf_files = glob.glob(os.path.join(input_dir, '*.pdf'))
    pdf_files += glob.glob(os.path.join(input_dir, '*.PDF'))
    pdf_files = list(set(pdf_files))  # Deduplicate

    if not pdf_files:
        print(f"No PDF files found in {input_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(pdf_files)} PDF files")

    all_data = []
    failed = []

    for pdf_path in sorted(pdf_files):
        filename = os.path.basename(pdf_path)
        print(f"Processing: {filename}...", end=" ")

        # Extract text
        text = None
        if use_ocr:
            text = extract_text_ocr(pdf_path)
        else:
            text = extract_text_pymupdf(pdf_path)
            if not text:
                text = extract_text_pypdf2(pdf_path)

        if not text:
            print("FAILED (could not extract text)")
            failed.append(filename)
            continue

        # Extract fields
        data = extract_invoice_fields(text)
        all_data.append(data)
        print(f"OK (vendor: {data['vendor_name']}, total: {data['total']})")

    if not all_data:
        print("Error: No invoices were successfully parsed.", file=sys.stderr)
        sys.exit(1)

    # Write consolidated output
    output_ext = os.path.splitext(output_path)[1].lower()

    if output_ext == '.json':
        with open(output_path, 'w') as f:
            json.dump(all_data, f, indent=2)
        print(f"\nJSON output written to {output_path}")
    else:
        # CSV output (default)
        fieldnames = ['vendor_name', 'invoice_number', 'invoice_date', 'due_date',
                      'description', 'quantity', 'unit_price', 'line_total',
                      'subtotal', 'tax', 'total', 'currency']

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for invoice in all_data:
                for item in invoice['line_items']:
                    row = {
                        'vendor_name': invoice['vendor_name'],
                        'invoice_number': invoice['invoice_number'],
                        'invoice_date': invoice['invoice_date'],
                        'due_date': invoice['due_date'],
                        'description': item.get('description', ''),
                        'quantity': item.get('quantity', ''),
                        'unit_price': item.get('unit_price', ''),
                        'line_total': item.get('line_total', ''),
                        'subtotal': invoice['subtotal'],
                        'tax': invoice['tax'],
                        'total': invoice['total'],
                        'currency': invoice['currency']
                    }
                    writer.writerow(row)

        print(f"\nCSV output written to {output_path}")
        print(f"Total invoices processed: {len(all_data)}")
        print(f"Total line items: {sum(len(i['line_items']) for i in all_data)}")

    if failed:
        print(f"\nFailed to parse {len(failed)} files:")
        for f in failed:
            print(f"  - {f}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Parse multiple PDF invoices from a directory')
    parser.add_argument('input_dir', help='Directory containing PDF invoices')
    parser.add_argument('--output', '-o', default='consolidated.csv', help='Output file path')
    parser.add_argument('--ocr', action='store_true', help='Use OCR for scanned PDFs')
    args = parser.parse_args()

    if not os.path.isdir(args.input_dir):
        print(f"Error: Not a directory: {args.input_dir}", file=sys.stderr)
        sys.exit(1)

    parse_directory(args.input_dir, args.output, use_ocr=args.ocr)


if __name__ == '__main__':
    main()
