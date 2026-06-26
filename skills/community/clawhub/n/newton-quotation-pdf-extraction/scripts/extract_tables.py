#!/usr/bin/env python3
"""
Extract tables from PDF file.
Usage: python extract_tables.py <input.pdf> [--output output.xlsx] [--format csv|xlsx|json]
"""

import argparse
import json
import sys
import pdfplumber


def extract_tables(pdf_path):
    """Extract all tables from PDF file."""
    tables_data = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            tables = page.extract_tables()
            for table_num, table in enumerate(tables, 1):
                if table:
                    tables_data.append({
                        "page": page_num,
                        "table": table_num,
                        "data": table
                    })

    return tables_data


def save_as_json(tables_data, output_path):
    """Save tables as JSON."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(tables_data, f, ensure_ascii=False, indent=2)


def save_as_csv(tables_data, output_path):
    """Save tables as CSV (multiple sheets/files)."""
    import csv

    for item in tables_data:
        page = item["page"]
        table_num = item["table"]
        data = item["data"]

        filename = f"{output_path.rsplit('.', 1)[0]}_p{page}_t{table_num}.csv"
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(data)
        print(f"Saved: {filename}", file=sys.stderr)


def save_as_xlsx(tables_data, output_path):
    """Save tables as Excel with multiple sheets."""
    try:
        import pandas as pd
    except ImportError:
        print("Error: pandas required for Excel output. Install with: pip install pandas openpyxl", file=sys.stderr)
        sys.exit(1)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        for item in tables_data:
            page = item["page"]
            table_num = item["table"]
            data = item["data"]

            if data:
                df = pd.DataFrame(data[1:], columns=data[0])
                sheet_name = f"P{page}_T{table_num}"
                df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"Tables saved to: {output_path}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Extract tables from PDF")
    parser.add_argument("input", help="Input PDF file path")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--format", choices=["csv", "xlsx", "json"], default="xlsx",
                        help="Output format (default: xlsx)")

    args = parser.parse_args()

    try:
        tables_data = extract_tables(args.input)

        if not tables_data:
            print("No tables found in PDF.", file=sys.stderr)
            sys.exit(0)

        print(f"Found {len(tables_data)} table(s)", file=sys.stderr)

        if args.format == "json":
            output_path = args.output or "tables.json"
            save_as_json(tables_data, output_path)
        elif args.format == "csv":
            output_path = args.output or "tables"
            save_as_csv(tables_data, output_path)
        else:  # xlsx
            output_path = args.output or "tables.xlsx"
            save_as_xlsx(tables_data, output_path)

    except FileNotFoundError:
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
