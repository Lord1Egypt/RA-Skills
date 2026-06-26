"""
tests/test_models.py

Unit tests for pure scoring and filtering logic.
No network calls — all tests run offline.
"""

import time
import pytest

from infinity_router.models import _is_free, score_model


# ──────────────────────────────────────────────────────────────────────────────
# _is_free
# ──────────────────────────────────────────────────────────────────────────────

class TestIsFree:
    def test_free_suffix(self):
        assert _is_free({"id": "google/gemma-3:free", "pricing": {}}) is True

    def test_zero_prompt_cost(self):
        assert _is_free({"id": "some/model", "pricing": {"prompt": "0"}}) is True

    def test_zero_prompt_cost_float(self):
        assert _is_free({"id": "some/model", "pricing": {"prompt": 0.0}}) is True

    def test_paid_model(self):
        assert _is_free({"id": "some/model", "pricing": {"prompt": "0.000001"}}) is False

    def test_no_pricing_key(self):
        assert _is_free({"id": "some/model", "pricing": {}}) is False

    def test_invalid_pricing_value(self):
        assert _is_free({"id": "some/model", "pricing": {"prompt": "free"}}) is False


# ──────────────────────────────────────────────────────────────────────────────
# score_model
# ──────────────────────────────────────────────────────────────────────────────

class TestScoreModel:
    def _make(self, **kwargs) -> dict:
        defaults = {
            "id": "test/model",
            "context_length": 0,
            "supported_parameters": [],
            "created": 0,
        }
        return {**defaults, **kwargs}

    def test_empty_model_scores_zero(self):
        assert score_model(self._make()) == 0.0

    def test_score_is_between_0_and_1(self):
        m = self._make(
            id="google/gemma-3:free",
            context_length=1_000_000,
            supported_parameters=["tools"] * 10,
            created=int(time.time()),
        )
        s = score_model(m)
        assert 0.0 <= s <= 1.0

    def test_longer_context_scores_higher(self):
        short = self._make(context_length=4_000)
        long  = self._make(context_length=128_000)
        assert score_model(long) > score_model(short)

    def test_more_capabilities_scores_higher(self):
        few  = self._make(supported_parameters=["tools"])
        many = self._make(supported_parameters=["tools"] * 8)
        assert score_model(many) > score_model(few)

    def test_newer_model_scores_higher(self):
        old = self._make(created=int(time.time()) - 400 * 86_400)
        new = self._make(created=int(time.time()) - 10 * 86_400)
        assert score_model(new) > score_model(old)

    def test_trusted_provider_scores_higher(self):
        trusted   = self._make(id="google/some-model:free")
        untrusted = self._make(id="unknown-provider/some-model:free")
        assert score_model(trusted) > score_model(untrusted)

    def test_score_is_deterministic(self):
        m = self._make(
            id="nvidia/nemotron:free",
            context_length=256_000,
            supported_parameters=["tools", "json"],
            created=int(time.time()) - 30 * 86_400,
        )
        assert score_model(m) == score_model(m)

    def test_context_ceiling_at_1m(self):
        at_1m   = self._make(context_length=1_000_000)
        over_1m = self._make(context_length=5_000_000)
        # Both should produce the same context contribution
        assert score_model(at_1m) == score_model(over_1m)
