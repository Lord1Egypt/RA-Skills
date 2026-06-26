"""Tests for concurrency safety — file locking on writes."""

import sys
import threading
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from engram.filelock import file_lock, safe_write, safe_append


class TestFileLock:
    def test_basic_lock(self, tmp_path):
        f = tmp_path / "test.txt"
        f.write_text("original")
        with file_lock(f):
            f.write_text("locked write")
        assert f.read_text() == "locked write"
    
    def test_lock_cleans_up(self, tmp_path):
        f = tmp_path / "test.txt"
        f.write_text("data")
        with file_lock(f):
            pass
        assert not (tmp_path / "test.txt.lock").exists()
    
    def test_concurrent_appends(self, tmp_path):
        """Two threads appending to same file shouldn't lose data."""
        f = tmp_path / "graph.jsonl"
        f.write_text("")
        
        errors = []
        
        def writer(thread_id, count):
            try:
                for i in range(count):
                    safe_append(f, f"thread-{thread_id}-line-{i}\n")
            except Exception as e:
                errors.append(e)
        
        t1 = threading.Thread(target=writer, args=(1, 50))
        t2 = threading.Thread(target=writer, args=(2, 50))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        
        assert not errors
        lines = [l for l in f.read_text().strip().split("\n") if l]
        assert len(lines) == 100  # No lost writes
    
    def test_concurrent_writes(self, tmp_path):
        """Two threads writing to same file — last one wins, no corruption."""
        f = tmp_path / "entity.md"
        f.write_text("# Original")
        
        results = []
        
        def writer(thread_id):
            for i in range(20):
                safe_write(f, f"# Thread {thread_id} write {i}\n")
                time.sleep(0.001)
            results.append(thread_id)
        
        t1 = threading.Thread(target=writer, args=(1,))
        t2 = threading.Thread(target=writer, args=(2,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        
        # File should be valid (not corrupted)
        content = f.read_text()
        assert content.startswith("# Thread")
        assert len(results) == 2
    
    def test_safe_write_atomic(self, tmp_path):
        """safe_write should use temp file → rename (atomic)."""
        f = tmp_path / "entity.md"
        safe_write(f, "# Test Entity\n**Type:** person\n")
        assert f.read_text() == "# Test Entity\n**Type:** person\n"
        # No leftover .tmp file
        assert not (tmp_path / "entity.tmp").exists()
    
    def test_lock_timeout(self, tmp_path):
        """Lock should timeout gracefully, not deadlock."""
        f = tmp_path / "test.txt"
        f.write_text("data")
        
        # Acquire lock in another thread and hold it
        lock_acquired = threading.Event()
        release = threading.Event()
        
        def holder():
            with file_lock(f, timeout=10.0):
                lock_acquired.set()
                release.wait(timeout=5.0)
        
        t = threading.Thread(target=holder)
        t.start()
        lock_acquired.wait()
        
        # Try to acquire with short timeout — should not deadlock
        start = time.monotonic()
        with file_lock(f, timeout=0.2):
            pass  # Proceeds after timeout
        elapsed = time.monotonic() - start
        
        release.set()
        t.join()
        
        # Should have waited ~0.2s, not forever
        assert elapsed < 2.0


class TestIntegrationLocking:
    """Test that actual module writes use locking."""
    
    def test_fix_uses_safe_write(self, tmp_path):
        """fix.py operations should use safe_write (atomic)."""
        entities = tmp_path / "entities"
        entities.mkdir()
        (entities / "Test.md").write_text("# Test\n**Type:** person\n\n## Facts\n- fact1\n")
        
        from engram.fix import fix_type
        result = fix_type(entities, "Test", "tool")
        
        assert "Updated" in result
        assert "**Type:** tool" in (entities / "Test.md").read_text()
        # No .tmp files left
        assert not list(entities.glob("*.tmp"))
    
    def test_concurrent_fix_operations(self, tmp_path):
        """Multiple fix operations on different entities shouldn't conflict."""
        entities = tmp_path / "entities"
        entities.mkdir()
        
        for i in range(10):
            (entities / f"Entity{i}.md").write_text(
                f"# Entity{i}\n**Type:** person\n\n## Facts\n- fact\n"
            )
        
        from engram.fix import fix_type
        errors = []
        
        def fixer(idx):
            try:
                fix_type(entities, f"Entity{idx}", "tool")
            except Exception as e:
                errors.append(e)
        
        threads = [threading.Thread(target=fixer, args=(i,)) for i in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert not errors
        for i in range(10):
            content = (entities / f"Entity{i}.md").read_text()
            assert "**Type:** tool" in content
