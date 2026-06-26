"""Smoke tests for the mentions-check handler. No network — urlopen is mocked."""

import json
import os
import sys
import unittest
import urllib.error
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import handler  # noqa: E402


def _mock_response(body):
    cm = MagicMock()
    cm.__enter__.return_value.read.return_value = body
    return cm


def _sent_body(mock_urlopen):
    req = mock_urlopen.call_args[0][0]
    return json.loads(req.data.decode("utf-8"))


class TestAuth(unittest.TestCase):
    def test_missing_key_returns_auth_required(self):
        with patch.dict(os.environ, {}, clear=True):
            result = handler.check_mentions(query="best CRM", brand="HubSpot")
        self.assertEqual(result["error"], "auth_required")
        self.assertIn("MENTIONSAPI_KEY", result["detail"])
        self.assertIn("mentionsapi.com/signup", result["detail"])


class TestInputValidation(unittest.TestCase):
    def test_missing_brand_returns_error(self):
        with patch.dict(os.environ, {"MENTIONSAPI_KEY": "lvk_test"}):
            result = handler.check_mentions(query="best CRM", brand="")
        self.assertEqual(result["error"], "invalid_argument")

    def test_missing_query_returns_error(self):
        with patch.dict(os.environ, {"MENTIONSAPI_KEY": "lvk_test"}):
            result = handler.check_mentions(query="", brand="HubSpot")
        self.assertEqual(result["error"], "invalid_argument")


class TestEndpoint(unittest.TestCase):
    @patch("handler.urllib.request.urlopen")
    def test_check_posts_to_v1_check(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b'{"id": "chk_1", "providers": {}}')
        with patch.dict(os.environ, {"MENTIONSAPI_KEY": "lvk_test"}):
            handler.check_mentions(query="best CRM", brand="HubSpot", mode="perplexity_live")
        req = mock_urlopen.call_args[0][0]
        self.assertEqual(req.full_url, "https://api.mentionsapi.com/v1/check")
        self.assertEqual(req.get_method(), "POST")
        body = _sent_body(mock_urlopen)
        self.assertEqual(body["query"], "best CRM")
        self.assertEqual(body["brand"], "HubSpot")
        self.assertEqual(body["mode"], "perplexity_live")

    @patch("handler.urllib.request.urlopen")
    def test_none_params_filtered_from_body(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b"{}")
        with patch.dict(os.environ, {"MENTIONSAPI_KEY": "lvk_test"}):
            handler.check_mentions(query="best CRM", brand="HubSpot")
        body = _sent_body(mock_urlopen)
        self.assertNotIn("providers", body)
        self.assertNotIn("runs", body)
        self.assertNotIn("region", body)
        self.assertEqual(body["mode"], "quick")

    @patch("handler.urllib.request.urlopen")
    def test_providers_array_passes_through(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b"{}")
        with patch.dict(os.environ, {"MENTIONSAPI_KEY": "lvk_test"}):
            handler.check_mentions(query="q", brand="b", providers=["chatgpt", "perplexity"])
        body = _sent_body(mock_urlopen)
        self.assertEqual(body["providers"], ["chatgpt", "perplexity"])

    @patch("handler.urllib.request.urlopen")
    def test_authorization_header_is_set(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b"{}")
        with patch.dict(os.environ, {"MENTIONSAPI_KEY": "lvk_secret"}):
            handler.check_mentions(query="q", brand="b")
        req = mock_urlopen.call_args[0][0]
        self.assertEqual(req.headers["Authorization"], "Bearer lvk_secret")
        self.assertIn("llm-mentions-skills", req.headers["User-agent"])


class TestHttpErrors(unittest.TestCase):
    @patch("handler.urllib.request.urlopen")
    def test_402_maps_to_insufficient_balance(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.HTTPError(
            "https://api.mentionsapi.com/v1/check", 402, "Payment Required", None, None
        )
        with patch.dict(os.environ, {"MENTIONSAPI_KEY": "lvk_test"}):
            result = handler.check_mentions(query="q", brand="b")
        self.assertEqual(result["error"], "insufficient_balance")
        self.assertIn("billing", result["top_up_url"])

    @patch("handler.urllib.request.urlopen")
    def test_401_maps_to_auth_invalid(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.HTTPError(
            "https://api.mentionsapi.com/v1/check", 401, "Unauthorized", None, None
        )
        with patch.dict(os.environ, {"MENTIONSAPI_KEY": "lvk_bad"}):
            result = handler.check_mentions(query="q", brand="b")
        self.assertEqual(result["error"], "auth_invalid")


if __name__ == "__main__":
    unittest.main()
