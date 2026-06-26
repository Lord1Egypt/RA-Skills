"""Tests for retry logic."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from engram.retry import with_retry, retry_call


class TestWithRetry:
    def test_succeeds_first_try(self):
        call_count = {"n": 0}
        
        @with_retry(max_retries=3)
        def succeed():
            call_count["n"] += 1
            return "ok"
        
        assert succeed() == "ok"
        assert call_count["n"] == 1
    
    def test_retries_on_429(self):
        call_count = {"n": 0}
        
        @with_retry(max_retries=3, base_delay=0.01)
        def fail_then_succeed():
            call_count["n"] += 1
            if call_count["n"] < 3:
                raise Exception("HTTP Error 429: Too Many Requests")
            return "ok"
        
        assert fail_then_succeed() == "ok"
        assert call_count["n"] == 3
    
    def test_gives_up_after_max_retries(self):
        @with_retry(max_retries=2, base_delay=0.01)
        def always_fail():
            raise Exception("HTTP Error 429: Too Many Requests")
        
        with pytest.raises(Exception, match="429"):
            always_fail()
    
    def test_no_retry_on_non_retryable(self):
        call_count = {"n": 0}
        
        @with_retry(max_retries=3, base_delay=0.01)
        def auth_error():
            call_count["n"] += 1
            raise Exception("HTTP Error 401: Unauthorized")
        
        with pytest.raises(Exception, match="401"):
            auth_error()
        
        assert call_count["n"] == 1  # No retry


class TestRetryCall:
    def test_functional_retry(self):
        call_count = {"n": 0}
        
        def flaky():
            call_count["n"] += 1
            if call_count["n"] < 2:
                raise Exception("HTTP Error 500: Internal Server Error")
            return "recovered"
        
        result = retry_call(flaky, max_retries=3)
        assert result == "recovered"
        assert call_count["n"] == 2
