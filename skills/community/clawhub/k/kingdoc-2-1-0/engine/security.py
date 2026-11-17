"""Security utilities for KingDoc"""
import re
from pathlib import Path
from typing import Optional

# File ID format validation
FILE_ID_PATTERN = re.compile(r'^[a-zA-Z0-9_-]{8,64}$')

# Blocked file extensions for upload
BLOCKED_EXTENSIONS = {
    '.exe', '.bat', '.ps1', '.cmd', '.com', '.scr',
    '.vbs', '.js', '.wsf', '.msi', '.msp', '.mst',
    '.cpl', '.ins', '.isp', '.jse', '.lnk', '.pif',
    '.reg', '.sct', '.shb', '.shs', '.vb', '.vbe',
    '.wsc', '.wsf', '.wsh'
}

# Blocked MIME types
BLOCKED_MIME_TYPES = {
    'application/x-msdownload',
    'application/x-executable',
    'application/x-dosexec',
    'application/x-msdos-program',
    'application/x-powershell',
    'text/javascript',
    'application/javascript',
    'application/x-vbs',
    'application/x-bat'
}

# Size limits (bytes)
SIZE_LIMITS = {
    'doc': 100 * 1024 * 1024,     # 100MB
    'sheet': 100 * 1024 * 1024,    # 100MB
    'ppt': 100 * 1024 * 1024,      # 100MB
    'image': 20 * 1024 * 1024,     # 20MB
    'attachment': 500 * 1024 * 1024  # 500MB
}


def validate_file_id(file_id: str) -> bool:
    """Validate file ID format"""
    return bool(FILE_ID_PATTERN.match(file_id))


def is_blocked_extension(filename: str) -> bool:
    """Check if file extension is in blocklist"""
    ext = Path(filename).suffix.lower()
    return ext in BLOCKED_EXTENSIONS


def is_blocked_mime(content_type: str) -> bool:
    """Check if MIME type is in blocklist"""
    return content_type.lower() in BLOCKED_MIME_TYPES


def check_size_limit(doc_type: int, file_size: int) -> bool:
    """Check if file size exceeds limit for document type"""
    limit = SIZE_LIMITS.get(doc_type, SIZE_LIMITS['attachment'])
    return file_size <= limit
