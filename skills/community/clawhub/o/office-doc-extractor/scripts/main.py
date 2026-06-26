#!/usr/bin/env python3
"""
Office Document Extractor - Unified CLI
Converts DOCX, XLSX, and PPTX files to Markdown.
Pure Python, zero external dependencies.
"""

import argparse
import sys
from pathlib import Path

import docx_extractor
import pptx_extractor
import xlsx_extractor


def detect_format(file_path: str) -> str:
    """Detect file format from extension."""
    ext = Path(file_path).suffix.lower()
    if ext == '.docx':
        return 'docx'
    elif ext == '.xlsx':
        return 'xlsx'
    elif ext == '.pptx':
        return 'pptx'
    else:
        return None


def convert_file(input_path: str, output_path: str = None) -> str:
    """Convert a single file based on its format."""
    fmt = detect_format(input_path)
    if not fmt:
        raise ValueError(f"Unsupported format: {Path(input_path).suffix}. Supports .docx, .xlsx, .pptx")
    
    if fmt == 'docx':
        return docx_extractor.extract_docx(input_path, output_path)
    elif fmt == 'xlsx':
        return xlsx_extractor.extract_xlsx(input_path, output_path)
    elif fmt == 'pptx':
        return pptx_extractor.extract_pptx(input_path, output_path)


def batch_convert(input_dir: str, output_dir: str = None) -> list:
    """Batch convert all supported files in a directory."""
    input_path = Path(input_dir)
    if not input_path.is_dir():
        raise ValueError(f"Not a directory: {input_dir}")
    
    if output_dir is None:
        output_path = input_path / "markdown_output"
    else:
        output_path = Path(output_dir)
    
    output_path.mkdir(exist_ok=True)
    
    supported = {'.docx', '.xlsx', '.pptx'}
    files = [f for f in input_path.iterdir() if f.suffix.lower() in supported]
    
    if not files:
        print(f"⚠️ No supported files found in {input_dir}")
        return []
    
    converted = []
    for file in files:
        out_file = output_path / f"{file.stem}.md"
        try:
            result = convert_file(str(file), str(out_file))
            converted.append(result)
            print(f"✅ {file.name} → {out_file.name}")
        except Exception as e:
            print(f"❌ Failed: {file.name} - {e}")
    
    print(f"\n📊 Converted {len(converted)}/{len(files)} files to {output_path}")
    return converted


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Office documents to Markdown")
    parser.add_argument("input", help="Input file or directory")
    parser.add_argument("-o", "--output", help="Output file or directory")
    parser.add_argument("--batch", action="store_true", help="Batch convert directory")
    
    args = parser.parse_args()
    
    try:
        if args.batch or Path(args.input).is_dir():
            batch_convert(args.input, args.output)
        else:
            result = convert_file(args.input, args.output)
            print(f"✅ Converted: {args.input} → {result}")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
