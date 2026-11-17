"""Unit tests for imagenCN providers — exceptions, size resolution,
generation, error formatting, backward-compatible exports.

Run with: python -m pytest skills/imagenCN/tests/ -v
"""

import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

# Allow imports from the scripts package
_skill_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_skill_root / "scripts"))

from providers.base import (
    OpenAICompatibleProvider, ConfigError, APIError, IOError_, ImageGenError,
    safe_request, safe_json,
)


# ---------------------------------------------------------------------------
# Exception hierarchy
# ---------------------------------------------------------------------------

class TestExceptions:
    def test_config_error(self):
        e = ConfigError("missing key")
        assert isinstance(e, ImageGenError)
        assert e.exit_code == 2

    def test_api_error(self):
        e = APIError("api fail")
        assert isinstance(e, ImageGenError)
        assert e.exit_code == 3

    def test_io_error(self):
        e = IOError_("write fail")
        assert isinstance(e, ImageGenError)
        assert e.exit_code == 4


# ---------------------------------------------------------------------------
# Size resolution
# ---------------------------------------------------------------------------

class TestSizeResolution:
    def test_ark_default(self):
        from volcano_ark import resolve_ark_size
        assert resolve_ark_size(None) == "2048x2048"

    def test_ark_preset(self):
        from volcano_ark import resolve_ark_size
        assert resolve_ark_size("16:9") == "2848x1600"

    def test_ark_custom_star_separator(self):
        from volcano_ark import resolve_ark_size
        assert resolve_ark_size("1024*768") == "1024x768"

    def test_hunyuan_colon_format(self):
        from hunyuan import resolve_hunyuan_size
        assert resolve_hunyuan_size(None) == "1024:1024"
        assert resolve_hunyuan_size("16:9") == "1920:1080"
        assert resolve_hunyuan_size("1024*768") == "1024:768"

    def test_zhipu_default(self):
        from zhipu import resolve_zhipu_size
        assert resolve_zhipu_size(None) == "1024x1024"

    def test_stepfun_default(self):
        from stepfun import resolve_stepfun_size
        assert resolve_stepfun_size(None) == "1024x1024"


# ---------------------------------------------------------------------------
# Model sets
# ---------------------------------------------------------------------------

class TestModelSets:
    def test_ark_models(self):
        from volcano_ark import ARK_MODELS
        assert "doubao-seedream-5-0-260128" in ARK_MODELS
        assert len(ARK_MODELS) == 3

    def test_hunyuan_models(self):
        from hunyuan import HUNYUAN_MODELS
        assert "hy-image-v3.0" in HUNYUAN_MODELS

    def test_zhipu_models(self):
        from zhipu import ZHIPU_MODELS
        assert "cogview-4" in ZHIPU_MODELS
        assert "glm-image" in ZHIPU_MODELS

    def test_stepfun_models(self):
        from stepfun import STEPFUN_MODELS
        assert "step-2x-large" in STEPFUN_MODELS


# ---------------------------------------------------------------------------
# API key handling
# ---------------------------------------------------------------------------

class TestApiKey:
    def test_missing_key_raises_config_error(self):
        p = OpenAICompatibleProvider()
        p.env_var = "NONEXISTENT_KEY_12345"
        with pytest.raises(ConfigError, match="NONEXISTENT_KEY_12345"):
            p.get_api_key()

    def test_existing_key_returns_value(self):
        p = OpenAICompatibleProvider()
        p.env_var = "TEST_KEY"
        os.environ["TEST_KEY"] = "test-value-123"
        try:
            assert p.get_api_key() == "test-value-123"
        finally:
            del os.environ["TEST_KEY"]


# ---------------------------------------------------------------------------
# Generation (mocked HTTP)
# ---------------------------------------------------------------------------

class TestGeneration:
    def test_generate_success(self):
        p = OpenAICompatibleProvider()
        p.name = "Test"
        p.api_base = "https://test.example.com/v1/images/generations"
        mock_rsp = MagicMock()
        mock_rsp.status_code = 200
        mock_rsp.json.return_value = {"data": [{"url": "https://cdn.example.com/img.png"}]}

        with patch("providers.base.requests") as mock_requests:
            mock_requests.request.return_value = mock_rsp
            url = p.generate("key123", "model-x", "a cat", "1024x1024")
            assert url == "https://cdn.example.com/img.png"

    def test_generate_http_error_raises_api_error(self):
        p = OpenAICompatibleProvider()
        p.name = "Test"
        p.api_base = "https://test.example.com/v1/images/generations"
        mock_rsp = MagicMock()
        mock_rsp.status_code = 401
        mock_rsp.text = "Unauthorized"

        with patch("providers.base.requests") as mock_requests:
            mock_requests.request.return_value = mock_rsp
            with pytest.raises(APIError):
                p.generate("bad-key", "model-x", "a cat", "1024x1024")

    def test_generate_malformed_response_raises(self):
        p = OpenAICompatibleProvider()
        p.name = "Test"
        p.api_base = "https://test.example.com/v1/images/generations"
        mock_rsp = MagicMock()
        mock_rsp.status_code = 200
        mock_rsp.json.return_value = {"data": []}  # no url

        with patch("providers.base.requests") as mock_requests:
            mock_requests.request.return_value = mock_rsp
            with pytest.raises(APIError):
                p.generate("key", "model-x", "a cat", "1024x1024")


# ---------------------------------------------------------------------------
# Backward-compatible exports
# ---------------------------------------------------------------------------

class TestBackwardCompat:
    def test_ark_module_exports(self):
        from volcano_ark import (get_ark_api_key, resolve_ark_size,
                                 generate_with_ark, ARK_MODELS, ARK_SIZES)
        assert callable(get_ark_api_key)
        assert callable(resolve_ark_size)
        assert callable(generate_with_ark)
        assert isinstance(ARK_MODELS, set)
        assert isinstance(ARK_SIZES, dict)

    def test_hunyuan_module_exports(self):
        from hunyuan import (get_hunyuan_api_key, resolve_hunyuan_size,
                             generate_with_hunyuan, HUNYUAN_MODELS, HUNYUAN_SIZES)
        assert callable(get_hunyuan_api_key)
        assert callable(resolve_hunyuan_size)
        assert callable(generate_with_hunyuan)
        assert isinstance(HUNYUAN_MODELS, set)
        assert isinstance(HUNYUAN_SIZES, dict)

    def test_zhipu_module_exports(self):
        from zhipu import (get_zhipu_api_key, resolve_zhipu_size,
                           generate_with_zhipu, ZHIPU_MODELS, ZHIPU_SIZES)
        assert callable(get_zhipu_api_key)
        assert callable(resolve_zhipu_size)
        assert callable(generate_with_zhipu)
        assert isinstance(ZHIPU_MODELS, set)
        assert isinstance(ZHIPU_SIZES, dict)

    def test_stepfun_module_exports(self):
        from stepfun import (get_stepfun_api_key, resolve_stepfun_size,
                             generate_with_stepfun, STEPFUN_MODELS, STEPFUN_SIZES)
        assert callable(get_stepfun_api_key)
        assert callable(resolve_stepfun_size)
        assert callable(generate_with_stepfun)
        assert isinstance(STEPFUN_MODELS, set)
        assert isinstance(STEPFUN_SIZES, dict)


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

class TestHttpHelpers:
    def test_safe_json_valid(self):
        mock = MagicMock()
        mock.json.return_value = {"ok": True}
        assert safe_json(mock) == {"ok": True}

    def test_safe_json_invalid(self):
        mock = MagicMock()
        mock.headers = {"content-type": "text/html"}
        mock.text = "<html>error</html>"
        mock.status_code = 502
        mock.json.side_effect = ValueError
        with pytest.raises(APIError, match="non-JSON"):
            safe_json(mock)
