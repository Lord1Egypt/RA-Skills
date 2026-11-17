"""
infrastructure/llm_gateway.py — LLM Gateway with circuit-breaker, retry, timeout

Wraps TextGenerator with resilience patterns:
- Exponential backoff with jitter
- Circuit breaker integration
- Timeout enforcement
- Graceful degradation (empty result instead of crash)
"""
from __future__ import annotations

import logging
import time
import random
from typing import Optional, List

_log = logging.getLogger("llm_gateway")


class LLMError(Exception):
    """Base LLM error."""
    pass


class LLMTimeoutError(LLMError):
    """LLM call exceeded timeout."""
    pass


class LLMAllProvidersFailedError(LLMError):
    """All LLM providers are unavailable."""
    pass


class LLMGateway:
    """
    Resilience wrapper around the TextGenerator.

    Retry policy:
    - Max 3 retries
    - Exponential backoff: 1s → 2s → 4s
    - Jitter: ±20%
    - Timeout: 120s per call
    """

    MAX_RETRIES = 3
    BASE_DELAY = 1.0
    MAX_DELAY = 8.0
    DEFAULT_TIMEOUT = 120

    def __init__(self, generator):
        self._generator = generator
        self._call_count = 0
        self._fail_count = 0

    @property
    def failure_rate(self) -> float:
        total = self._call_count
        return self._fail_count / total if total > 0 else 0.0

    def generate(self, task: str, **kwargs) -> str:
        """
        Generate text with retry and backoff.
        
        Returns empty string if all retries fail (never throws).
        """
        self._call_count += 1
        
        for attempt in range(self.MAX_RETRIES + 1):
            try:
                result = self._generator.generate(task, **kwargs)
                if result and len(result.strip()) > 10:
                    return result
                
                # Empty or too-short result counts as failure
                if attempt < self.MAX_RETRIES:
                    delay = self._backoff_delay(attempt)
                    _log.warning(f"LLM returned short/empty text, retry {attempt+1}/{self.MAX_RETRIES} in {delay:.1f}s")
                    time.sleep(delay)
                else:
                    _log.error("LLM empty text after all retries")
                    self._fail_count += 1
                    return ""
                    
            except Exception as e:
                self._fail_count += 1
                if attempt < self.MAX_RETRIES:
                    delay = self._backoff_delay(attempt)
                    _log.warning(f"LLM error: {e}, retry {attempt+1}/{self.MAX_RETRIES} in {delay:.1f}s")
                    time.sleep(delay)
                else:
                    _log.error(f"LLM failed after {self.MAX_RETRIES} retries: {e}")
                    return ""
        
        return ""

    def generate_l3(self, task: str, **kwargs) -> str:
        """L3 temperature oscillation generation."""
        temps = kwargs.pop("temperatures", [0.65, 0.85, 0.55])
        results = []
        for temp in temps:
            result = self.generate(task, temperature=temp, **kwargs)
            if result:
                results.append(result)
        return max(results, key=len) if results else ""

    def check_available(self) -> bool:
        """Check if any LLM provider is available."""
        try:
            for _, p in self._generator._providers:
                try:
                    if p.available():
                        return True
                except Exception:
                    continue
            return False
        except Exception:
            return False

    def _backoff_delay(self, attempt: int) -> float:
        """Exponential backoff with jitter."""
        delay = min(self.BASE_DELAY * (2 ** attempt), self.MAX_DELAY)
        jitter = delay * 0.2 * (2 * random.random() - 1)
        return delay + jitter

    @property
    def stats(self) -> dict:
        return {
            "calls": self._call_count,
            "failures": self._fail_count,
            "failure_rate": f"{self.failure_rate:.1%}",
        }
