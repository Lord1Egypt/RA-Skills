#!/usr/bin/env python3
"""_analysis_cache.py — Hash-based caching for analysis results.

Stores analysis JSON next to the input audio file (or in a configurable
cache directory) keyed by file path + mtime + size. If the audio file
hasn't changed since the last analysis, the cached result is returned
instead of recomputing.

Usage in any analysis script:
    from _analysis_cache import cached_or_compute

    def my_analysis(audio_path, ...):
        def compute():
            # ... actual analysis ...
            return result
        return cached_or_compute(audio_path, 'my_analysis', compute)

The cache key includes a version string so that schema changes invalidate
old caches automatically.
"""
import os
import json
import hashlib

CACHE_VERSION = 'v0.6.0'  # bumped in v0.3.0: added camera_motion, vlm_captions, image.caption, image.faces, image.text_in_image, ast_classification fields; schema expanded


def cache_key(audio_path, analysis_name):
    """Generate a cache key from the audio file's path, mtime, and size.

    The key also includes the analysis name and the cache version, so
    upgrading the analysis or the cache schema invalidates old entries.
    """
    try:
        stat = os.stat(audio_path)
        sig = f"{audio_path}|{stat.st_mtime}|{stat.st_size}|{analysis_name}|{CACHE_VERSION}"
        return hashlib.sha256(sig.encode()).hexdigest()[:16]
    except OSError:
        return None


def cache_path(audio_path, analysis_name, cache_dir=None):
    """Return the path where the cached result should be stored.

    Default: a hidden sidecar file next to the audio file.
    """
    key = cache_key(audio_path, analysis_name)
    if not key:
        return None
    if cache_dir is None:
        cache_dir = os.path.dirname(os.path.abspath(audio_path))
    return os.path.join(cache_dir, f".{analysis_name}_{key}.json")


def load_cache(audio_path, analysis_name, cache_dir=None):
    """Load a cached result, or return None if not found / invalid."""
    path = cache_path(audio_path, analysis_name, cache_dir)
    if not path or not os.path.exists(path):
        return None
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def save_cache(audio_path, analysis_name, result, cache_dir=None):
    """Save a result to the cache."""
    path = cache_path(audio_path, analysis_name, cache_dir)
    if not path:
        return
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
    except OSError:
        pass


def cached_or_compute(audio_path, analysis_name, compute_fn, cache_dir=None):
    """Return cached result if available, else call compute_fn and cache.

    Args:
      audio_path: the input file (used for hash key)
      analysis_name: a short string identifying the analysis type
      compute_fn: a zero-arg callable that produces the result dict
      cache_dir: optional override for cache storage location

    Returns: the analysis result dict
    """
    cached = load_cache(audio_path, analysis_name, cache_dir)
    if cached is not None:
        cached['_cache'] = 'hit'
        return cached
    result = compute_fn()
    if isinstance(result, dict):
        save_cache(audio_path, analysis_name, result, cache_dir)
        result['_cache'] = 'miss'
    return result
