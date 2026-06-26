#!/usr/bin/env python3
"""
DOCX to Markdown extractor using only Python standard library.
DOCX is a ZIP archive containing XML files.
"""

import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

NAMESPACES = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
}

def extract_docx(input_path: str, output_path: str = None) -> str:
    """Extract text from DOCX and convert to Markdown."""
    input_file = Path(input_path)
    if not input_file.exists():
        raise FileNotFoundError(f"File not found: {input_path}")
    
    if output_path is None:
        output_path = input_file.with_suffix('.md')
    
    with zipfile.ZipFile(input_file, 'r') as zf:
        if 'word/document.xml' not in zf.namelist():
            raise ValueError("Invalid DOCX: word/document.xml not found")
        
        with zf.open('word/document.xml') as f:
            tree = ET.parse(f)
    
    root = tree.getroot()
    md_lines = []
    
    # Extract headings and paragraphs
    for p in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
        texts = []
        pStyle = None
        
        # Check paragraph style for heading
        for pPr in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pPr'):
            for style in pPr.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pStyle'):
                pStyle = style.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
        
        # Extract text runs
        for r in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}r'):
            for t in r.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'):
                if t.text:
                    texts.append(t.text)
        
        if texts:
            paragraph_text = ''.join(texts)
            # Determine heading level
            if pStyle and pStyle.startswith('Heading'):
                try:
                    level = int(pStyle.replace('Heading', ''))
                    md_lines.append(f"{'#' * level} {paragraph_text}")
                except ValueError:
                    md_lines.append(paragraph_text)
            else:
                md_lines.append(paragraph_text)
            md_lines.append('')  # Empty line after paragraph
    
    markdown = '\n'.join(md_lines)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    return str(output_path)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 docx_extractor.py <input.docx> [-o output.md]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output = None
    if '-o' in sys.argv:
        idx = sys.argv.index('-o')
        output = sys.argv[idx + 1]
    
    result = extract_docx(input_file, output)
    print(f"✅ Converted: {input_file} → {result}")
