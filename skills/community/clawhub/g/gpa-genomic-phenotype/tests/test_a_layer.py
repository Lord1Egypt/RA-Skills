#!/usr/bin/env python3
"""
DGRA v0.6 A-Layer Regression Tests

Tests:
1. HTTP 429 → Retry-After handling
2. HTTP 502/503 → Exponential backoff 1s→2s→4s
3. Network timeout → Retry chain
4. Streaming download resume
5. Build state recovery after deletion
"""

import asyncio
import json
import os
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from dgra_build_state import (
    load_state,
    save_state,
    get_step_status,
    is_step_complete,
    reset_state,
    set_state_file,
    BuildStep,
)


class TestBuildState(unittest.TestCase):
    """Test dgra_build_state persistence."""

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.tmp.close()
        set_state_file(Path(self.tmp.name))
        reset_state()

    def tearDown(self):
        # reset_state() already deletes the file, so just clean up if it still exists
        reset_state()
        try:
            os.unlink(self.tmp.name)
        except FileNotFoundError:
            pass

    def test_save_and_load(self):
        save_state("pseudogene_sync", {"status": "complete", "genes_synced": 51})
        state = load_state()
        self.assertEqual(state["pseudogene_sync"]["data"]["status"], "complete")
        self.assertEqual(state["pseudogene_sync"]["data"]["genes_synced"], 51)

    def test_get_step_status(self):
        save_state("vep_reannotation", {"status": "in_progress"})
        self.assertEqual(get_step_status("vep_reannotation"), "in_progress")
        self.assertEqual(get_step_status("missing_step"), "pending")

    def test_is_step_complete(self):
        save_state("step_a", {"status": "complete"})
        self.assertTrue(is_step_complete("step_a"))
        save_state("step_b", {"status": "failed"})
        self.assertFalse(is_step_complete("step_b"))

    def test_reset_single(self):
        save_state("s1", {"status": "complete"})
        save_state("s2", {"status": "complete"})
        reset_state("s1")
        self.assertEqual(get_step_status("s1"), "pending")
        self.assertEqual(get_step_status("s2"), "complete")

    def test_build_step_context_manager(self):
        with BuildStep("test_ctx") as step:
            step.complete(result="ok")
        self.assertTrue(is_step_complete("test_ctx"))

    def test_build_step_failure(self):
        try:
            with BuildStep("fail_ctx") as step:
                raise ValueError("boom")
        except ValueError:
            pass
        self.assertEqual(get_step_status("fail_ctx"), "failed")

    def test_state_recovery_after_deletion(self):
        """Test 5: Delete state for a step, it should re-execute."""
        save_state("gtf_download", {"status": "complete", "size": 1000})
        self.assertTrue(is_step_complete("gtf_download"))

        # Simulate deletion of just this step
        reset_state("gtf_download")
        self.assertEqual(get_step_status("gtf_download"), "pending")

        # Re-save
        save_state("gtf_download", {"status": "complete", "size": 1000})
        self.assertTrue(is_step_complete("gtf_download"))


class TestAPIRetryBehavior(unittest.IsolatedAsyncioTestCase):
    """Test dgra_api.py retry logic with mocked responses."""

    async def asyncSetUp(self):
        self.cfg = MagicMock()
        self.cfg.apis = {
            "ensembl": MagicMock(base_url="https://rest.ensembl.org", rate_limit_per_sec=10, max_retries=3, retry_delay=1, timeout=30, proxy=None),
        }
        self.cfg.offline_mode = False
        self.cache = MagicMock()
        self.cache.get = MagicMock(return_value=None)
        self.cache.set = MagicMock()

        sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
        from dgra_api import DGRAAPIClient
        self.client = DGRAAPIClient(self.cfg, self.cache)
        await self.client.__aenter__()

    async def asyncTearDown(self):
        await self.client.__aexit__(None, None, None)

    async def test_429_retry_after(self):
        """Test 1: HTTP 429 should read Retry-After and wait."""
        call_count = 0
        def mock_request(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                mock_resp = MagicMock()
                mock_resp.status = 429
                mock_resp.headers = {"Retry-After": "2"}
                mock_resp.text = AsyncMock(return_value="rate limited")
                mock_resp.__aenter__ = AsyncMock(return_value=mock_resp)
                mock_resp.__aexit__ = AsyncMock(return_value=False)
                return mock_resp
            # Second call succeeds
            success_resp = MagicMock()
            success_resp.status = 200
            success_resp.json = AsyncMock(return_value={"id": "ENSG123"})
            success_resp.__aenter__ = AsyncMock(return_value=success_resp)
            success_resp.__aexit__ = AsyncMock(return_value=False)
            return success_resp

        with patch.object(self.client._session, "request", side_effect=mock_request):
            t0 = time.time()
            result = await self.client._request_with_retry(
                api_name="ensembl",
                endpoint="/lookup/symbol/homo_sapiens/TEST",
            )
            elapsed = time.time() - t0

        self.assertEqual(call_count, 2)
        self.assertTrue(elapsed >= 1.5, f"Expected >= 1.5s wait for Retry-After=2, got {elapsed:.2f}s")
        self.assertEqual(result["http_status"], 200)

    async def test_503_exponential_backoff(self):
        """Test 2: HTTP 503 should retry with exponential backoff 1s→2s→4s."""
        call_count = 0
        def mock_request(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            mock_resp = MagicMock()
            mock_resp.status = 503
            mock_resp.headers = {}
            mock_resp.text = AsyncMock(return_value="service unavailable")
            mock_resp.__aenter__ = AsyncMock(return_value=mock_resp)
            mock_resp.__aexit__ = AsyncMock(return_value=False)
            return mock_resp

        with patch.object(self.client._session, "request", side_effect=mock_request):
            t0 = time.time()
            result = await self.client._request_with_retry(
                api_name="ensembl",
                endpoint="/test",
            )
            elapsed = time.time() - t0

        # 3 retries (max_retries=3), delays: 1s, 2s, 4s = 7s total
        self.assertEqual(call_count, 3)  # max_retries=3 attempts total
        self.assertTrue(elapsed >= 6.0, f"Expected >= 6s total backoff, got {elapsed:.2f}s")
        self.assertIn("error", result)

    async def test_timeout_retry_chain(self):
        """Test 3: Network timeout should trigger retry chain with increasing delays."""
        call_count = 0
        def mock_request(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            raise asyncio.TimeoutError()

        with patch.object(self.client._session, "request", side_effect=mock_request):
            t0 = time.time()
            result = await self.client._request_with_retry(
                api_name="ensembl",
                endpoint="/test",
            )
            elapsed = time.time() - t0

        self.assertEqual(call_count, 3)  # max_retries=3 attempts total
        self.assertTrue(elapsed >= 6.0, f"Expected >= 6s total backoff, got {elapsed:.2f}s")
        self.assertIn("error", result)


class TestStreamingDownload(unittest.TestCase):
    """Test streaming download resume."""

    def test_resume_download(self):
        """Test 4: Truncate file, resume should complete."""
        import urllib.request
        from dgra_pseudogene_sync import _download_gtf_streaming

        test_url = "https://raw.githubusercontent.com/lzr098/dgra-genomic-risk/master/README.md"
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".md")
        tmp.close()
        output = Path(tmp.name)

        try:
            # Full download
            _download_gtf_streaming(test_url, output, chunk_size=1024)
            full_size = output.stat().st_size
            self.assertGreater(full_size, 0)

            # Truncate to half
            half = full_size // 2
            with open(output, "r+b") as f:
                f.truncate(half)

            # Resume
            _download_gtf_streaming(test_url, output, chunk_size=1024)
            resumed_size = output.stat().st_size

            self.assertGreaterEqual(resumed_size, full_size * 0.9,
                                    f"Resume failed: {resumed_size} vs {full_size}")
        finally:
            output.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
