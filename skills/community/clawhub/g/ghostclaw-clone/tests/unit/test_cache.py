"""Tests for LocalCache and fingerprinting."""

import json
import pytest
import time
from pathlib import Path
from datetime import datetime, timedelta
from ghostclaw.core.cache import LocalCache, compute_fingerprint


@pytest.fixture
def temp_cache(tmp_path):
    """Provide a LocalCache using a temporary directory."""
    return LocalCache(cache_dir=tmp_path / "cache", ttl_days=1)


def test_cache_set_and_get(temp_cache):
    """Test storing and retrieving a report."""
    fingerprint = "test:123"
    report = {"vibe_score": 95, "stack": "python"}

    # Initially miss
    assert temp_cache.get(fingerprint) is None

    # Store and retrieve
    temp_cache.set(fingerprint, report)
    cached = temp_cache.get(fingerprint)
    assert cached == report


def test_cache_ttl_expiration(temp_cache):
    """Test that entries expire after TTL."""
    fingerprint = "test:expire"
    report = {"vibe_score": 80}

    temp_cache.set(fingerprint, report)

    # Find the cache file (compressed or uncompressed)
    cache_files = list(temp_cache.cache_dir.glob("*.json.gz"))
    if not cache_files:
        cache_files = list(temp_cache.cache_dir.glob("*.json"))
    assert len(cache_files) == 1
    cache_file = cache_files[0]

    # Load JSON (handle compressed or plain), set cached_at to 2 days ago, write back
    if cache_file.suffix == ".gz":
        import gzip
        data = json.loads(gzip.decompress(cache_file.read_bytes()).decode('utf-8'))
        data["cached_at"] = (datetime.now() - timedelta(days=2)).isoformat()
        new_content = gzip.compress(json.dumps(data).encode('utf-8'))
        cache_file.write_bytes(new_content)
    else:
        data = json.loads(cache_file.read_text(encoding='utf-8'))
        data["cached_at"] = (datetime.now() - timedelta(days=2)).isoformat()
        cache_file.write_text(json.dumps(data), encoding='utf-8')

    # Should be expired (None)
    assert temp_cache.get(fingerprint) is None


def test_cache_clear(temp_cache):
    """Test clearing all cache entries."""
    for i in range(5):
        temp_cache.set(f"key{i}", {"vibe_score": i})
    assert temp_cache.info()["entries"] == 5

    temp_cache.clear()
    assert temp_cache.info()["entries"] == 0


def test_cache_info(temp_cache):
    """Test cache statistics."""
    for i in range(3):
        temp_cache.set(f"key{i}", {"vibe_score": i})
    info = temp_cache.info()
    assert info["entries"] == 3
    assert info["total_size_bytes"] > 0
    assert str(temp_cache.cache_dir) in info["cache_dir"]


def test_fingerprint_git_repo(tmp_path):
    """Fingerprint for a git repo should include HEAD SHA."""
    # Initialize a minimal git repo
    (tmp_path / "test.txt").write_text("hello")
    import subprocess
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=tmp_path, check=True, capture_output=True)

    fp = compute_fingerprint(tmp_path)
    assert fp.startswith("ghostclaw:v1:git:")


def test_fingerprint_non_git(tmp_path):
    """Fingerprint for non-git should use mtime summary."""
    # Create some Python files
    (tmp_path / "module.py").write_text("def foo():\n    return 1\n")
    (tmp_path / "other.py").write_text("x = 2\n")

    fp = compute_fingerprint(tmp_path)
    assert fp.startswith("ghostclaw:v1:mtime:")

    # Modify a file and fingerprint should change
    time.sleep(0.1)  # Ensure mtime difference
    (tmp_path / "module.py").write_text("def foo():\n    return 2\n")
    fp2 = compute_fingerprint(tmp_path)
    assert fp != fp2


def test_fingerprint_version_prefix():
    """Fingerprint should include version prefix for cache invalidation."""
    fp = compute_fingerprint(Path("/nonexistent"))
    assert fp.startswith("ghostclaw:v1:")
