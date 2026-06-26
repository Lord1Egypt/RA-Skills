#!/usr/bin/env python3
"""
PDF to Markdown converter
Simple rule-based extraction without any external API calls
"""

import sys
import re
from pathlib import Path


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF using pdfplumber"""
    try:
        import pdfplumber
    except ImportError:
        return "Error: pdfplumber not installed"
    
    text_parts = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)
    
    return "\n\n".join(text_parts)


def clean_text(text: str) -> str:
    """Clean and format extracted text"""
    # Remove extra whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    
    # Fix common extraction issues
    text = re.sub(r'(\w)-\n(\w)', r'\1\2', text)  # Hyphenated words
    
    return text.strip()


def convert_to_markdown(text: str) -> str:
    """Convert plain text to markdown format"""
    lines = text.split('\n')
    md_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            md_lines.append('')
            continue
        
        # Detect potential headers (all caps, short lines)
        if len(line) < 50 and line.isupper():
            md_lines.append(f'# {line.title()}')
        # Detect bullet points
        elif line.startswith('•') or line.startswith('-'):
            md_lines.append(f'- {line[1:].strip()}')
        # Detect numbered lists
        elif re.match(r'^\d+[\.\)]', line):
            md_lines.append(f'{line}')
        else:
            md_lines.append(line)
    
    return '\n'.join(md_lines)


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python pdf2md.py <input.pdf> [output.md]")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not Path(input_path).exists():
        print(f"Error: File not found: {input_path}")
        sys.exit(1)
    
    # Extract text
    text = extract_text_from_pdf(input_path)
    
    if text.startswith("Error:"):
        print(text)
        sys.exit(1)
    
    # Clean and convert
    text = clean_text(text)
    markdown = convert_to_markdown(text)
    
    # Output
    if output_path:
        Path(output_path).write_text(markdown, encoding='utf-8')
        print(f"✓ Converted to {output_path}")
    else:
        print(markdown)


if __name__ == "__main__":
    main()
