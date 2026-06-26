#!/usr/bin/env python3
"""
Convert between document formats
Usage: convert.py <input> --to <format> [options]
Supported: DOCX→PDF, PPTX→PDF
"""
import sys
import argparse
from pathlib import Path

def import_required_libs():
    """Import required libraries"""
    libs = {}
    try:
        from docx import Document
        libs['docx'] = Document
    except ImportError:
        pass
    try:
        from pptx import Presentation
        libs['pptx'] = Presentation
    except ImportError:
        pass
    try:
        import fitz
        libs['fitz'] = fitz
    except ImportError:
        pass
    return libs

def convert_docx_to_pdf(input_path, output_path):
    """Convert DOCX to PDF using docx2pdf if available, otherwise warn"""
    try:
        from docx2pdf import convert
        convert(input_path, output_path)
        return True
    except ImportError:
        print("Error: docx2pdf not installed.", file=sys.stderr)
        print("Install: pip install docx2pdf", file=sys.stderr)
        print("Note: docx2pdf requires Microsoft Word on Windows or LibreOffice on Linux/Mac", file=sys.stderr)
        return False

def convert_pptx_to_pdf(input_path, output_path):
    """Convert PPTX to PDF (placeholder - requires external tools)"""
    print("Error: PPTX to PDF conversion requires external tools.", file=sys.stderr)
    print("Options:", file=sys.stderr)
    print("  - Use LibreOffice: libreoffice --headless --convert-to pdf", file=sys.stderr)
    print("  - Use Microsoft PowerPoint on Windows", file=sys.stderr)
    return False

def main():
    parser = argparse.ArgumentParser(
        description='Convert between document formats',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Supported conversions:
  DOCX → PDF (requires docx2pdf + Word/LibreOffice)
  PPTX → PDF (requires external tool)

Examples:
  convert.py document.docx --to pdf
  convert.py presentation.pptx --to pdf --output slides.pdf
        """
    )
    parser.add_argument('input', help='Input file')
    parser.add_argument('--to', required=True, choices=['pdf'], help='Output format')
    parser.add_argument('--output', help='Output file path')
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    
    # Validate input file
    if not input_path.exists():
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)
    
    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_suffix(f'.{args.to}')
    
    # Create parent directory
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Perform conversion based on input type
    input_ext = input_path.suffix.lower()
    success = False
    
    if input_ext == '.docx' and args.to == 'pdf':
        success = convert_docx_to_pdf(input_path, output_path)
    elif input_ext == '.pptx' and args.to == 'pdf':
        success = convert_pptx_to_pdf(input_path, output_path)
    else:
        print(f"Error: Conversion from {input_ext} to {args.to} not supported", file=sys.stderr)
        sys.exit(1)
    
    if success:
        print(f"Converted: {input_path} → {output_path}")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
