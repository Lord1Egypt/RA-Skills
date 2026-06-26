#!/usr/bin/env python3
"""
NCBI Utility Functions

Shared utilities for NCBI E-Utilities API calls with built-in SQLite caching.
"""

import os
import sys
import time
import sqlite3
import hashlib
import json
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Optional

# Rate limiting state
LAST_REQUEST_TIME = 0
MIN_REQUEST_INTERVAL = 0.34  # ~3 requests/second without API key
SESSION = None

# Cache Settings
CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".ncbi_cache")
CACHE_DB_PATH = os.path.join(CACHE_DIR, "cache.db")
CACHE_EXPIRE_HOURS = int(os.environ.get("NCBI_CACHE_EXPIRE_HOURS", 24))


def create_session():
    """Create a session with retry logic."""
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def get_session():
    """Get or create the global session."""
    global SESSION
    if SESSION is None:
        SESSION = create_session()
    return SESSION


def rate_limit(api_key: Optional[str] = None):
    """Enforce rate limiting."""
    global LAST_REQUEST_TIME
    interval = 0.11 if api_key else MIN_REQUEST_INTERVAL
    elapsed = time.time() - LAST_REQUEST_TIME
    if elapsed < interval:
        time.sleep(interval - elapsed)
    LAST_REQUEST_TIME = time.time()


def clean_xml_tags(text: str) -> str:
    """Remove XML tags and clean whitespace."""
    import re
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def init_cache():
    """Initialize the SQLite database for caching."""
    if os.environ.get("NCBI_NO_CACHE") == "1":
        return
    try:
        os.makedirs(CACHE_DIR, exist_ok=True)
        conn = sqlite3.connect(CACHE_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS api_cache (
                key TEXT PRIMARY KEY,
                value TEXT,
                expires_at REAL
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_expires_at ON api_cache(expires_at)")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Warning: Failed to initialize cache database: {e}", file=sys.stderr)


def get_cache_key(url: str, params: dict) -> str:
    """Generate a unique SHA256 key for URL and sorted params."""
    serialized_params = json.dumps(params, sort_keys=True)
    raw_key = f"{url}?{serialized_params}"
    return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()


def get_cached_response(url: str, params: dict) -> Optional[str]:
    """Retrieve cached response if it exists and has not expired."""
    if os.environ.get("NCBI_NO_CACHE") == "1":
        return None
    
    init_cache()
    
    try:
        conn = sqlite3.connect(CACHE_DB_PATH)
        cursor = conn.cursor()
        
        # Clean up expired items
        cursor.execute("DELETE FROM api_cache WHERE expires_at < ?", (time.time(),))
        conn.commit()
        
        key = get_cache_key(url, params)
        cursor.execute("SELECT value FROM api_cache WHERE key = ? AND expires_at >= ?", (key, time.time()))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return row[0]
    except Exception as e:
        print(f"Warning: Failed to read from cache: {e}", file=sys.stderr)
        
    return None


def set_cache_response(url: str, params: dict, value: str):
    """Save response to local cache with an expiration time."""
    if os.environ.get("NCBI_NO_CACHE") == "1":
        return
        
    init_cache()
    
    try:
        conn = sqlite3.connect(CACHE_DB_PATH)
        cursor = conn.cursor()
        key = get_cache_key(url, params)
        expires_at = time.time() + (CACHE_EXPIRE_HOURS * 3600)
        cursor.execute(
            "INSERT OR REPLACE INTO api_cache (key, value, expires_at) VALUES (?, ?, ?)",
            (key, value, expires_at)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Warning: Failed to write to cache: {e}", file=sys.stderr)


def http_get(url: str, params: dict, api_key: Optional[str] = None, timeout: int = 30, verbose: bool = False) -> str:
    """
    Perform a GET request with rate limiting and local SQLite caching.
    Returns response text.
    """
    # Try local cache first
    cached = get_cached_response(url, params)
    if cached is not None:
        if verbose:
            print(f"[Cache Hit] URL: {url}", file=sys.stderr)
        return cached
        
    if verbose:
        print(f"[Cache Miss] Fetching from NCBI: {url}", file=sys.stderr)
        
    # Enforce rate limit
    rate_limit(api_key)
    
    # Request from NCBI
    session = get_session()
    response = session.get(url, params=params, timeout=timeout)
    response.raise_for_status()
    
    response_text = response.text
    
    # Save to cache
    set_cache_response(url, params, response_text)
    
    return response_text