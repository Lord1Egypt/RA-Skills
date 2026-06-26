#!/usr/bin/env python3
"""
Format detector - Auto-detect file format and select best converter.
"""

import mimetypes
import os
from pathlib import Path
from typing import Optional, Dict, List


# Extended format mapping
FORMAT_MAP = {
    # Word
    '.docx': {'type': 'word', 'backend': 'pandoc', 'mime': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'},
    '.doc': {'type': 'word', 'backend': 'markitdown', 'mime': 'application/msword'},
    '.rtf': {'type': 'word', 'backend': 'pandoc', 'mime': 'application/rtf'},
    '.odt': {'type': 'word', 'backend': 'pandoc', 'mime': 'application/vnd.oasis.opendocument.text'},
    
    # Excel
    '.xlsx': {'type': 'excel', 'backend': 'markitdown', 'mime': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'},
    '.xls': {'type': 'excel', 'backend': 'markitdown', 'mime': 'application/vnd.ms-excel'},
    '.xlsm': {'type': 'excel', 'backend': 'markitdown', 'mime': 'application/vnd.ms-excel.sheet.macroenabled'},
    '.ods': {'type': 'excel', 'backend': 'markitdown', 'mime': 'application/vnd.oasis.opendocument.spreadsheet'},
    '.csv': {'type': 'csv', 'backend': 'pandoc', 'mime': 'text/csv'},
    
    # PowerPoint
    '.pptx': {'type': 'ppt', 'backend': 'pandoc', 'mime': 'application/vnd.openxmlformats-officedocument.presentationml.presentation'},
    '.ppt': {'type': 'ppt', 'backend': 'markitdown', 'mime': 'application/vnd.ms-powerpoint'},
    '.odp': {'type': 'ppt', 'backend': 'pandoc', 'mime': 'application/vnd.oasis.opendocument.presentation'},
    
    # PDF
    '.pdf': {'type': 'pdf', 'backend': 'markitdown', 'mime': 'application/pdf'},
    
    # Images
    '.png': {'type': 'image', 'backend': 'markitdown', 'mime': 'image/png'},
    '.jpg': {'type': 'image', 'backend': 'markitdown', 'mime': 'image/jpeg'},
    '.jpeg': {'type': 'image', 'backend': 'markitdown', 'mime': 'image/jpeg'},
    '.gif': {'type': 'image', 'backend': 'markitdown', 'mime': 'image/gif'},
    '.bmp': {'type': 'image', 'backend': 'markitdown', 'mime': 'image/bmp'},
    '.webp': {'type': 'image', 'backend': 'markitdown', 'mime': 'image/webp'},
    '.tiff': {'type': 'image', 'backend': 'markitdown', 'mime': 'image/tiff'},
    '.tif': {'type': 'image', 'backend': 'markitdown', 'mime': 'image/tiff'},
    
    # Text/Markdown
    '.md': {'type': 'markdown', 'backend': 'copy', 'mime': 'text/markdown'},
    '.markdown': {'type': 'markdown', 'backend': 'copy', 'mime': 'text/markdown'},
    '.txt': {'type': 'text', 'backend': 'copy', 'mime': 'text/plain'},
    '.html': {'type': 'html', 'backend': 'pandoc', 'mime': 'text/html'},
    '.htm': {'type': 'html', 'backend': 'pandoc', 'mime': 'text/html'},
    
    # Data formats
    '.json': {'type': 'json', 'backend': 'copy', 'mime': 'application/json'},
    '.xml': {'type': 'xml', 'backend': 'pandoc', 'mime': 'application/xml'},
    '.yaml': {'type': 'yaml', 'backend': 'copy', 'mime': 'application/x-yaml'},
    '.yml': {'type': 'yaml', 'backend': 'copy', 'mime': 'application/x-yaml'},
    
    # Archives
    '.epub': {'type': 'ebook', 'backend': 'pandoc', 'mime': 'application/epub+zip'},
    '.mobi': {'type': 'ebook', 'backend': 'pandoc', 'mime': 'application/x-mobipocket-ebook'},
    
    # Audio (markitdown only)
    '.mp3': {'type': 'audio', 'backend': 'markitdown', 'mime': 'audio/mpeg'},
    '.wav': {'type': 'audio', 'backend': 'markitdown', 'mime': 'audio/wav'},
    '.m4a': {'type': 'audio', 'backend': 'markitdown', 'mime': 'audio/mp4'},
    
    # Archives (for embedded content)
    '.zip': {'type': 'archive', 'backend': 'markitdown', 'mime': 'application/zip'},
}


def detect_format(file_path: str) -> Dict:
    """Detect file format and return metadata."""
    path = Path(file_path)
    ext = path.suffix.lower()
    
    if ext in FORMAT_MAP:
        info = FORMAT_MAP[ext].copy()
    else:
        mime = None
        try:
            mime = mimetypes.guess_type(str(path))[0]
        except Exception:
            pass
        
        info = {
            'type': 'unknown',
            'backend': 'auto',
            'mime': mime or 'application/octet-stream'
        }
    
    info['extension'] = ext
    info['name'] = path.stem
    
    return info


def get_supported_formats() -> List[str]:
    """Return list of supported format extensions."""
    return list(FORMAT_MAP.keys())


def is_supported(file_path: str) -> bool:
    """Check if file format is supported."""
    ext = Path(file_path).suffix.lower()
    return ext in FORMAT_MAP


def suggest_backend(file_path: str, preferred: Optional[str] = None) -> str:
    """Suggest best backend for the file."""
    if preferred and preferred != 'auto':
        return preferred
    
    info = detect_format(file_path)
    return info.get('backend', 'auto')


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Detect file format")
    parser.add_argument("file", help="File to detect")
    args = parser.parse_args()
    
    info = detect_format(args.file)
    print(f"Format: {info}")