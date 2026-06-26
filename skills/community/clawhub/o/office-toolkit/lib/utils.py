"""
Utility functions
"""
import sys
from pathlib import Path
from typing import Union, Optional


def ensure_path(path: Union[str, Path]) -> Path:
    """Ensure path is a Path object"""
    return Path(path) if not isinstance(path, Path) else path


def validate_input_file(file_path: Union[str, Path], extensions: list) -> Path:
    """Validate input file exists and has correct extension"""
    path = ensure_path(file_path)
    
    if not path.exists():
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)
    
    if not path.is_file():
        print(f"Error: Not a file: {path}", file=sys.stderr)
        sys.exit(1)
    
    if extensions and path.suffix.lower() not in extensions:
        print(f"Error: Invalid file type. Expected: {', '.join(extensions)}, got: {path.suffix}", file=sys.stderr)
        sys.exit(1)
    
    return path


def validate_output_path(file_path: Union[str, Path], extensions: list) -> Path:
    """Validate output path has correct extension"""
    path = ensure_path(file_path)
    
    if extensions and path.suffix.lower() not in extensions:
        print(f"Error: Invalid output type. Expected: {', '.join(extensions)}, got: {path.suffix}", file=sys.stderr)
        sys.exit(1)
    
    # Create parent directory if needed
    path.parent.mkdir(parents=True, exist_ok=True)
    
    return path


def safe_read(func):
    """Decorator for safe file reading"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    return wrapper


def safe_write(func):
    """Decorator for safe file writing"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error writing file: {e}", file=sys.stderr)
            sys.exit(1)
    return wrapper
