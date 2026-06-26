#!/usr/bin/env python3
"""
PPTX handler - Enhanced PowerPoint handling.
"""

import zipfile
from pathlib import Path
from typing import Dict, List, Optional


def extract_pptx_text(pptx_path: str) -> str:
    """Extract text from PPTX file."""
    text_parts = []
    
    try:
        with zipfile.ZipFile(pptx_path, 'r') as z:
            slides = sorted([n for n in z.namelist() if n.startswith('ppt/slides/slide') and n.endswith('.xml')])
            
            for slide_path in slides:
                import xml.etree.ElementTree as ET
                content = z.read(slide_path)
                root = ET.fromstring(content)
                
                for t in root.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}t'):
                    if t.text:
                        text_parts.append(t.text)
                
                text_parts.append('\n---\n')
    
    except Exception as e:
        return f"Error extracting PPTX: {e}"
    
    return '\n'.join(text_parts)


def get_pptx_info(pptx_path: str) -> Dict:
    """Get PPTX file information."""
    info = {
        'file': Path(pptx_path).name,
        'size': Path(pptx_path).stat().st_size,
    }
    
    try:
        with zipfile.ZipFile(pptx_path, 'r') as z:
            info['slides'] = sum(1 for n in z.namelist() if n.startswith('ppt/slides/slide') and n.endswith('.xml'))
            info['images'] = sum(1 for n in z.namelist() if n.startswith('ppt/media/'))
            info['has_theme'] = any(n.startswith('ppt/theme/') for n in z.namelist())
            info['has_notes'] = any(n.startswith('ppt/notesSlides/') for n in z.namelist())
    except Exception as e:
        info['error'] = str(e)
    
    return info


def extract_pptx_images(pptx_path: str, output_dir: str) -> List[str]:
    """Extract all images from PPTX."""
    images = []
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    try:
        with zipfile.ZipFile(pptx_path, 'r') as z:
            for name in z.namelist():
                if name.startswith('ppt/media/') and not name.endswith('.xml'):
                    img_data = z.read(name)
                    ext = Path(name).suffix.lower()
                    if not ext:
                        if img_data.startswith(b'\xff\xd8'):
                            ext = '.jpg'
                        elif img_data.startswith(b'\x89PNG'):
                            ext = '.png'
                        elif img_data.startswith(b'GIF8'):
                            ext = '.gif'
                    
                    img_name = Path(name).name
                    (output_path / img_name).write_bytes(img_data)
                    images.append(img_name)
    except Exception as e:
        print(f"Error extracting images: {e}")
    
    return images


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="PPTX handler")
    parser.add_argument("file", help="PPTX file")
    parser.add_argument("--info", action="store_true", help="Show file info")
    parser.add_argument("--extract-images", action="store_true", help="Extract images")
    parser.add_argument("-o", "--output", default="output", help="Output directory")
    args = parser.parse_args()
    
    if args.info:
        import json
        print(json.dumps(get_pptx_info(args.file), indent=2))
    
    if args.extract_images:
        images = extract_pptx_images(args.file, args.output)
        print(f"Extracted {len(images)} images")