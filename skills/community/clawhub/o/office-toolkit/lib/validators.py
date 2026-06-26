"""
Input validation utilities
"""
from pathlib import Path
from typing import Union, List, Optional


VALID_EXTENSIONS = {
    'docx': ['.docx'],
    'pptx': ['.pptx'],
    'xlsx': ['.xlsx', '.xlsm'],
    'pdf': ['.pdf'],
}


def validate_file_extension(file_path: Union[str, Path], doc_type: str) -> bool:
    """Validate file has correct extension for document type"""
    path = Path(file_path) if isinstance(file_path, str) else file_path
    valid_exts = VALID_EXTENSIONS.get(doc_type.lower(), [])
    return path.suffix.lower() in valid_exts


def get_file_type(file_path: Union[str, Path]) -> Optional[str]:
    """Detect document type from file extension"""
    path = Path(file_path) if isinstance(file_path, str) else file_path
    suffix = path.suffix.lower()
    
    for doc_type, extensions in VALID_EXTENSIONS.items():
        if suffix in extensions:
            return doc_type
    
    return None
