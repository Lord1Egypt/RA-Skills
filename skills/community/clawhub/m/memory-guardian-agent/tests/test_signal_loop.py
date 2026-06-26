#!/usr/bin/env python3
"""Tests for signal_loop.py — dual-layer signal collection (v0.4.6 Phase 1)."""

import json
import os
import sys
import tempfile
import time
import unittest
from datetime import datetime, timedelta

# Add scripts dir to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))

from signal_loop import (
    append_access_log,
    check_signal_health,
    count_access_log_hits,
    cron_infer_access,
    get_access_log_path,
    merge_signals,
    read_access_log,
    SIGNAL_STALE_THRESHOLD_HOURS,
    SIGNAL_STALE_THRESHOLD_DEPLOY_HOURS,
)
from mg_utils import load_meta, save_meta


class TestAccessLog(unittest.TestCase):
    """Layer 1: access_log.jsonl read/write."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.workspace = self.tmpdir

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_append_creates_log(self):
        append_access_log(self.workspace, "memory/2026-04-11.md", "讨论信号闭环", ["memory-guardian"])
        log_path = get_access_log_path(self.workspace)
        self.assertTrue(os.path.exists(log_path))

    def test_append_and_read(self):
        append_access_log(self.workspace, "memory/test.md", "测试", ["test"])
        append_access_log(self.workspace, "memory/test2.md", "测试2", ["test2"])
        entries = read_access_log(self.workspace)
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0]["file"], "memory/test.md")
        self.assertEqual(entries[1]["file"], "memory/test2.md")

    def test_read_with_since_filter(self):
        append_access_log(self.workspace, "memory/old.md", "旧的", [])
        time.sleep(0.1)
        cutoff = datetime.now().isoformat()
        time.sleep(0.1)
        append_access_log(self.workspace, "memory/new.md", "新的", [])
        entries = read_access_log(self.workspace, since_ts=cutoff)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["file"], "memory/new.md")

    def test_empty_log_returns_empty(self):
        entries = read_access_log(self.workspace)
        self.assertEqual(entries, [])

    def test_corrupted_lines_skipped(self):
        log_path = get_access_log_path(self.workspace)
        with open(log_path, "w") as f:
            f.write("not json\n")
            f.write('{"file": "test.md", "ts": "2026-01-01", "context": "", "tags": []}\n')
            f.write("\n")
        entries = read_access_log(self.workspace)
        self.assertEqual(len(entries), 1)


class TestCountAccessLogHits(unittest.TestCase):
    """Count access log hits against memory entries."""

    def test_basic_counting(self):
        log_entries = [
            {"file": "memory/a.md", "ts": "2026-01-01"},
            {"file": "memory/a.md", "ts": "2026-01-02"},
            {"file": "memory/b.md", "ts": "2026-01-01"},
        ]
        # Match via content prefix (e.g. [a.md ...])
        memories = [
            {"id": "m1", "content": "[a.md] some content"},
            {"id": "m2", "content": "[b.md] other content"},
            {"id": "m3", "content": "[c.md] no match"},
        ]
        counts = count_access_log_hits(log_entries, memories)
        self.assertEqual(counts["m1"], 2)
        self.assertEqual(counts["m2"], 1)
        self.assertNotIn("m3", counts)

    def test_empty_log(self):
        counts = count_access_log_hits([], [{"id": "m1", "content": "[test.md] x"}])
        self.assertEqual(counts, {})


class TestSignalHealth(unittest.TestCase):
    """Signal health check."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.workspace = self.tmpdir

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_no_log_means_degraded(self):
        result = check_signal_health(self.workspace)
        self.assertFalse(result["layer1_active"])
        self.assertTrue(result["degraded"])

    def test_recent_log_is_healthy(self):
        append_access_log(self.workspace, "test.md", "test")
        result = check_signal_health(self.workspace)
        self.assertTrue(result["layer1_active"])
        self.assertFalse(result["degraded"])

    def test_stale_log_is_degraded(self):
        # Create log, then set mtime to past
        append_access_log(self.workspace, "test.md", "test")
        log_path = get_access_log_path(self.workspace)
        old_time = time.time() - 48 * 3600  # 48 hours ago
        os.utime(log_path, (old_time, old_time))

        result = check_signal_health(self.workspace)
        self.assertFalse(result["layer1_active"])
        self.assertTrue(result["degraded"])
        self.assertGreater(result["stale_hours"], 24)

    def test_custom_threshold(self):
        append_access_log(self.workspace, "test.md", "test")
        log_path = get_access_log_path(self.workspace)
        old_time = time.time() - 3 * 3600  # 3 hours ago
        os.utime(log_path, (old_time, old_time))

        # Default threshold (24h) → healthy
        result = check_signal_health(self.workspace)
        self.assertTrue(result["layer1_active"])

        # Custom threshold 1h → degraded
        config = {"signal_stale_threshold_hours": 1}
        result = check_signal_health(self.workspace, decay_config=config)
        self.assertFalse(result["layer1_active"])


class TestMergeSignals(unittest.TestCase):
    """Full signal merge integration."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.workspace = self.tmpdir
        self.mem_dir = os.path.join(self.tmpdir, "memory")
        os.makedirs(self.mem_dir, exist_ok=True)

        # Create meta.json with test memories
        self.meta_path = os.path.join(self.mem_dir, "meta.json")
        meta = {
            "version": "0.4.5",
            "memories": [
                {
                    "id": "m1",
                    "content": "[2026-04-11.md 信号] 信号闭环讨论",
                    "tags": ["memory-guardian", "v0.4.6"],
                    "title": "信号闭环讨论",
                    "status": "active",
                    "access_count": 0,
                    "trigger_count": 0,
                    "decay_score": 0.8,
                    "importance": 0.7,
                    "created_at": "2026-04-11T10:00:00+08:00",
                },
                {
                    "id": "m2",
                    "content": "[2026-04-10.md 社区] InStreet 社区讨论",
                    "tags": ["instreet", "community"],
                    "title": "InStreet 社区讨论",
                    "status": "active",
                    "access_count": 2,
                    "trigger_count": 1,
                    "decay_score": 0.6,
                    "importance": 0.5,
                    "created_at": "2026-04-10T10:00:00+08:00",
                },
                {
                    "id": "m3",
                    "content": "[2026-03-01.md 旧] 旧笔记",
                    "tags": ["archive"],
                    "title": "旧笔记",
                    "status": "active",
                    "access_count": 0,
                    "trigger_count": 0,
                    "decay_score": 0.3,
                    "importance": 0.3,
                    "created_at": "2026-03-01T10:00:00+08:00",
                },
            ],
        }
        save_meta(self.meta_path, meta)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_layer1_only(self):
        """Layer 1 (access_log) updates access_count."""
        append_access_log(self.workspace, "memory/2026-04-11.md", "信号闭环", ["memory-guardian"])
        append_access_log(self.workspace, "memory/2026-04-11.md", "再次访问", ["memory-guardian"])

        result = merge_signals(self.meta_path, self.workspace, dry_run=False)
        self.assertTrue(result["layer1_active"])
        self.assertEqual(result["layer1_hits"], 2)
        self.assertEqual(result["memories_updated"], 1)  # Only m1 matched

        meta = load_meta(self.meta_path)
        m1 = next(m for m in meta["memories"] if m["id"] == "m1")
        self.assertGreater(m1["access_count"], 0)

    def test_layer2_keyword_match(self):
        """Layer 2 (keyword inference) updates access_count."""
        # Create a daily note that mentions "memory-guardian"
        today = datetime.now().strftime("%Y-%m-%d")
        note_path = os.path.join(self.mem_dir, f"{today}.md")
        with open(note_path, "w") as f:
            f.write("# Daily Note\n\n讨论了 memory-guardian v0.4.6 信号闭环\n")

        result = merge_signals(self.meta_path, self.workspace, dry_run=True)
        # m1 should get an inference hit (tag "memory-guardian" matched)
        self.assertGreater(result["layer2_inferences"], 0)

    def test_degraded_mode(self):
        """When Layer 1 is stale, only Layer 2 is used."""
        append_access_log(self.workspace, "memory/2026-04-11.md", "test")
        # Make log stale
        log_path = get_access_log_path(self.workspace)
        old_time = time.time() - 48 * 3600
        os.utime(log_path, (old_time, old_time))

        config = {"signal_stale_threshold_hours": 24, "signal_weights": {"access_log_weight": 1.0, "infer_weight": 0.5}}
        result = merge_signals(self.meta_path, self.workspace, decay_config=config, dry_run=True)
        self.assertFalse(result["layer1_active"])
        self.assertTrue(result["degraded"])
        self.assertEqual(result["signal_source"], "proxy_only")

    def test_merge_formula(self):
        """Verify access_count = log_count * w1 + infer_count * w2."""
        # Add log entries for m1
        append_access_log(self.workspace, "memory/2026-04-11.md", "访问1", [])
        append_access_log(self.workspace, "memory/2026-04-11.md", "访问2", [])

        # Create daily note with keyword match
        today = datetime.now().strftime("%Y-%m-%d")
        note_path = os.path.join(self.mem_dir, f"{today}.md")
        with open(note_path, "w") as f:
            f.write("memory-guardian 讨论\n")

        config = {
            "signal_weights": {"access_log_weight": 1.0, "infer_weight": 0.5},
            "signal_stale_threshold_hours": 24,
        }
        result = merge_signals(self.meta_path, self.workspace, decay_config=config, dry_run=False)

        meta = load_meta(self.meta_path)
        m1 = next(m for m in meta["memories"] if m["id"] == "m1")
        # Should have: 2 log hits * 1.0 + N infer hits * 0.5, ceiled
        self.assertGreater(m1["access_count"], 0)
        self.assertIsNotNone(m1.get("last_accessed"))

    def test_signal_source_in_meta(self):
        """meta.json gets signal_source and signal_health after merge."""
        append_access_log(self.workspace, "memory/2026-04-11.md", "test")
        merge_signals(self.meta_path, self.workspace, dry_run=False)

        meta = load_meta(self.meta_path)
        self.assertIn("signal_source", meta)
        self.assertIn("signal_health", meta)
        self.assertIn("last_signal_merge", meta)


class TestCronInferAccess(unittest.TestCase):
    """Layer 2: cron inference from daily notes and file mtime."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.workspace = self.tmpdir
        self.mem_dir = os.path.join(self.tmpdir, "memory")
        os.makedirs(self.mem_dir, exist_ok=True)
        self.meta_path = os.path.join(self.mem_dir, "meta.json")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_mtime_inference(self):
        """File modified after last_accessed → infer signal."""
        # Create memory file
        mem_file = os.path.join(self.mem_dir, "test.md")
        with open(mem_file, "w") as f:
            f.write("test content")

        # Set mtime to future
        future = time.time() + 3600
        os.utime(mem_file, (future, future))

        meta = {
            "memories": [{
                "id": "m1",
                "file_path": "memory/test.md",
                "status": "active",
                "last_accessed": "2026-04-10T10:00:00+08:00",
                "created_at": "2026-04-10T10:00:00+08:00",
            }]
        }
        save_meta(self.meta_path, meta)

        counts = cron_infer_access(self.workspace, self.meta_path)
        self.assertIn("m1", counts)
        self.assertGreater(counts["m1"], 0)

    def test_keyword_match(self):
        """Daily note contains memory tags → infer signal."""
        meta = {
            "memories": [{
                "id": "m1",
                "file_path": "memory/test.md",
                "status": "active",
                "tags": ["memory-guardian"],
                "title": "信号闭环",
                "created_at": "2026-04-11T10:00:00+08:00",
            }]
        }
        save_meta(self.meta_path, meta)

        # Create today's daily note
        today = datetime.now().strftime("%Y-%m-%d")
        note_path = os.path.join(self.mem_dir, f"{today}.md")
        with open(note_path, "w") as f:
            f.write("今天讨论了 memory-guardian 的信号闭环设计\n")

        counts = cron_infer_access(self.workspace, self.meta_path)
        self.assertIn("m1", counts)

    def test_no_match(self):
        """No daily notes, no mtime change → no inference."""
        meta = {
            "memories": [{
                "id": "m1",
                "file_path": "memory/test.md",
                "status": "active",
                "tags": ["nonexistent-tag"],
                "title": "不存在的内容",
                "created_at": "2026-04-11T10:00:00+08:00",
            }]
        }
        save_meta(self.meta_path, meta)

        counts = cron_infer_access(self.workspace, self.meta_path)
        self.assertNotIn("m1", counts)


if __name__ == "__main__":
    unittest.main()
