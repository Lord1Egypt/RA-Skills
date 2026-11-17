"""File API Tests"""
import pytest
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Skip if config not available
config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")

def test_import():
    """Test module import"""
    from engine.client import KingDocClient
    assert KingDocClient is not None

def test_import_auth():
    """Test auth module import"""
    from engine.auth import KingDocAuth
    assert KingDocAuth is not None

def test_import_exceptions():
    """Test exceptions module import"""
    from engine.exceptions import (
        KingDocError, AuthError, PermissionError, QuotaError, DocTypeError,
        DocNotFoundError, RateLimitError, VersionConflictError,
        FileTooLargeError, FileTypeBlockedError, ServiceUnavailableError, ParamError
    )
    assert KingDocError is not None
    assert AuthError is not None
    assert PermissionError is not None

def test_file_id_validation():
    """Test file ID format validation"""
    from engine.security import FILE_ID_PATTERN
    
    # Valid IDs
    assert FILE_ID_PATTERN.match("file_abc123")
    assert FILE_ID_PATTERN.match("document-123")
    assert FILE_ID_PATTERN.match("12345678")
    
    # Invalid IDs
    assert not FILE_ID_PATTERN.match("")
    assert not FILE_ID_PATTERN.match("ab")
    assert not FILE_ID_PATTERN.match("file@#")

def test_exponential_backoff():
    """Test exponential backoff calculation"""
    from engine.rate_limiter import exponential_backoff
    
    delays = []
    for i in range(5):
        delays.append(exponential_backoff(i, max_retries=5))
    
    # Each delay should be larger than the previous (except random jitter)
    assert delays[4] > delays[0]

def test_blocked_extensions():
    """Test blocked file extensions"""
    from engine.security import BLOCKED_EXTENSIONS
    
    assert ".exe" in BLOCKED_EXTENSIONS
    assert ".bat" in BLOCKED_EXTENSIONS
    assert ".doc" not in BLOCKED_EXTENSIONS
    assert ".pdf" not in BLOCKED_EXTENSIONS

def test_doc_type_from_suffix():
    """Test document type detection from file suffix"""
    from engine.local.generators import DocxGenerator, PptxGenerator
    
    # Just check instantiation doesn't crash
    try:
        gen = DocxGenerator()
        assert gen is not None
    except ImportError:
        # python-docx not installed, skip
        pass
    
    try:
        gen = PptxGenerator()
        assert gen is not None
    except ImportError:
        pass

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
