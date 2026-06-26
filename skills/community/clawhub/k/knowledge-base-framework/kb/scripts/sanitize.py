#!/usr/bin/env python3
"""
Input Sanitization Utilities for KB Framework

Provides protection against path traversal attacks and other
security issues in file handling.
"""

import os
import re
from pathlib import Path
from typing import Optional


def sanitize_path(input_path: str, base_dir: Optional[str] = None) -> Path:
    """
    Sanitize and validate a file path.
    
    Prevents path traversal attacks by:
    1. Resolving the path to absolute
    2. Checking it's within the base directory
    3. Removing null bytes and other dangerous characters
    
    Args:
        input_path: The path to sanitize
        base_dir: The base directory to restrict access to (optional)
        
    Returns:
        Sanitized Path object
        
    Raises:
        ValueError: If path is dangerous or outside base_dir
        TypeError: If input_path is not a string
    """
    if not isinstance(input_path, str):
        raise TypeError(f"Path must be string, got {type(input_path).__name__}")
    
    if not input_path or not input_path.strip():
        raise ValueError("Path cannot be empty")
    
    # Remove null bytes and other dangerous characters
    if '\x00' in input_path:
        raise ValueError("Null byte in path not allowed")
    
    # Remove control characters
    sanitized = ''.join(c for c in input_path if ord(c) >= 32 or c in '/.-_')
    
    # Resolve path (handles .., ., etc)
    try:
        path = Path(sanitized).resolve()
    except (ValueError, OSError) as e:
        raise ValueError(f"Invalid path: {e}")
    
    # Check if path is within base_dir
    if base_dir:
        base = Path(base_dir).resolve()
        try:
            path.relative_to(base)
        except ValueError:
            raise ValueError(f"Path '{path}' is outside base directory '{base}'")
    
    return path


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename to only contain safe characters.
    
    Args:
        filename: The filename to sanitize
        
    Returns:
        Sanitized filename
    """
    if not filename:
        return "unnamed"
    
    # Remove any path components
    filename = Path(filename).name
    
    # Only allow safe characters
    safe_chars = re.compile(r'[^a-zA-Z0-9._-]')
    sanitized = safe_chars.sub('_', filename)
    
    # Limit length
    if len(sanitized) > 255:
        stem = Path(sanitized).stem
        ext = Path(sanitized).suffix
        sanitized = stem[:250] + ext
    
    return sanitized or "unnamed"


def is_safe_query(query: str, max_length: int = 1000) -> bool:
    """
    Check if a search query is safe.
    
    Args:
        query: The query to check
        max_length: Maximum allowed query length
        
    Returns:
        True if query is safe
    """
    if not query or not isinstance(query, str):
        return False
    
    if len(query) > max_length:
        return False
    
    # Check for SQL injection patterns (basic protection)
    # Note: We use parameterized queries, but this adds a layer
    dangerous_patterns = [
        '--', ';--', ';', '/*', '*/', '@@', 'char', 'nchar',
        'varchar', 'nvarchar', 'alter', 'begin', 'cast',
        'create', 'cursor', 'declare', 'delete', 'drop',
        'end', 'exec', 'execute', 'fetch', 'insert',
        'kill', 'select', 'sys', 'sysobjects', 'syscolumns',
        'table', 'update', 'xp_', '0x'
    ]
    
    query_lower = query.lower()
    for pattern in dangerous_patterns:
        if pattern.lower() in query_lower:
            return False
    
    return True


def sanitize_search_query(query: str) -> str:
    """
    Sanitize a search query for safe use.
    
    Args:
        query: The query to sanitize
        
    Returns:
        Sanitized query
    """
    if not query:
        return ""
    
    # Remove null bytes
    query = query.replace('\x00', '')
    
    # Remove control characters
    query = ''.join(c for c in query if ord(c) >= 32)
    
    # Limit length
    if len(query) > 1000:
        query = query[:1000]
    
    # Strip whitespace
    return query.strip()


# CLI test
if __name__ == "__main__":
    print("Testing Sanitization Utilities")
    print("=" * 50)
    
    # Test path sanitization
    test_paths = [
        str(Path.home() / "file.txt"),
        "relative/path/file.md",
        "../../../etc/passwd",
        str(Path.home() / "../../../etc/passwd"),
        "file\x00.txt",
    ]
    
    print("\nPath Sanitization Tests:")
    for path in test_paths:
        try:
            result = sanitize_path(path, base_dir=str(Path.home()))
            print(f"  ✅ {path} -> {result}")
        except ValueError as e:
            print(f"  ❌ {path} -> {e}")
    
    # Test filename sanitization
    test_filenames = [
        "normal_file.md",
        "file with spaces.md",
        "../../../dangerous.txt",
        "file<>:\"?.txt",
        "a" * 300 + ".md",
    ]
    
    print("\nFilename Sanitization Tests:")
    for name in test_filenames:
        result = sanitize_filename(name)
        print(f"  {name} -> {result}")
    
    # Test query sanitization
    test_queries = [
        "MTHFR Genmutation",
        "'; DROP TABLE users;--",
        "a" * 2000,
    ]
    
    print("\nQuery Sanitization Tests:")
    for query in test_queries:
        safe = is_safe_query(query)
        sanitized = sanitize_search_query(query)
        print(f"  {'✅' if safe else '❌'} '{query[:50]}...' -> '{sanitized[:30]}...'")