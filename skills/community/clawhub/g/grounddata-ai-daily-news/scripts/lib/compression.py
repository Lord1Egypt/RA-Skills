"""
compression.py — gzip decompression utility
"""


def decompress(data: bytes) -> str:
    """Decompress gzip data, return UTF-8 string"""
    import gzip
    return gzip.decompress(data).decode("utf-8")
