#!/usr/bin/env python3
"""
PPTX to Markdown extractor using only Python standard library.
PPTX is a ZIP archive containing XML files.
"""

import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

def extract_pptx(input_path: str, output_path: str = None) -> str:
    """Extract text from PPTX and convert to Markdown."""
    input_file = Path(input_path)
    if not input_file.exists():
        raise FileNotFoundError(f"File not found: {input_path}")
    
    if output_path is None:
        output_path = input_file.with_suffix('.md')
    
    with zipfile.ZipFile(input_file, 'r') as zf:
        # Get all slide XML files sorted
        slide_files = sorted([
            name for name in zf.namelist()
            if name.startswith('ppt/slides/slide') and name.endswith('.xml')
        ], key=lambda x: int(x.replace('ppt/slides/slide', '').replace('.xml', '')))
        
        if not slide_files:
            raise ValueError("Invalid PPTX: no slides found")
        
        md_lines = []
        
        for slide_file in slide_files:
            slide_num = slide_file.replace('ppt/slides/slide', '').replace('.xml', '')
            md_lines.append(f"## Slide {slide_num}")
            md_lines.append('')
            
            with zf.open(slide_file) as f:
                tree = ET.parse(f)
            
            root = tree.getroot()
            
            # Extract text from shapes
            for sp in root.iter():
                if sp.tag.endswith('}sp'):
                    texts = []
                    for t in sp.iter():
                        if t.tag.endswith('}t'):
                            if t.text:
                                texts.append(t.text)
                    
                    if texts:
                        md_lines.append(''.join(texts))
                        md_lines.append('')
            
            md_lines.append('---')
            md_lines.append('')
    
    markdown = '\n'.join(md_lines)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    return str(output_path)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 pptx_extractor.py <input.pptx> [-o output.md]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output = None
    if '-o' in sys.argv:
        idx = sys.argv.index('-o')
        output = sys.argv[idx + 1]
    
    result = extract_pptx(input_file, output)
    print(f"✅ Converted: {input_file} → {result}")
