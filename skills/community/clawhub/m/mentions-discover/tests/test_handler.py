"""Smoke tests for the mentions-discover handler. No network — urlopen is mocked."""

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
            result = handler.discover_queries(brand="Linear")
        self.assertEqual(result["error"], "auth_required")
        self.assertIn("MENTIONSAPI_KEY", result["detail"])


class TestInputValidation(unittest.TestCase):
    def test_missing_brand_returns_error(self):
        with patch.dict(os.environ, {"MENTIONSAPI_KEY": "lvk_test"}):
            result = handler.discover_queries(brand="")
        self.assertEqual(result["error"], "invalid_argument")


class TestEndpoint(unittest.TestCase):
    @patch("handler.urllib.request.urlopen")
    def test_discover_posts_to_v1_discover(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b'{"brand": "Linear", "queries": []}')
        with patch.dict(os.environ, {"MENTIONSAPI_KEY": "lvk_test"}):
            handler.discover_queries(brand="Linear", industry="project management", count=25)
        req = mock_urlopen.call_args[0][0]
        self.assertEqual(req.full_url, "https://api.mentionsapi.com/v1/discover")
        self.assertEqual(req.get_method(), "POST")
        body = _sent_body(mock_urlopen)
        self.assertEqual(body["brand"], "Linear")
        self.assertEqual(body["industry"], "project management")
        self.assertEqual(body["count"], 25)

    @patch("handler.urllib.request.urlopen")
    def test_default_count_and_none_industry_filtered(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b"{}")
        with patch.dict(os.environ, {"MENTIONSAPI_KEY": "lvk_test"}):
            handler.discover_queries(brand="Linear")
        body = _sent_body(mock_urlopen)
        self.assertEqual(body["count"], 50)
        self.assertNotIn("industry", body)

    @patch("handler.urllib.request.urlopen")
    def test_authorization_header_is_set(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b"{}")
        with patch.dict(os.environ, {"MENTIONSAPI_KEY": "lvk_secret"}):
            handler.discover_queries(brand="Linear")
        req = mock_urlopen.call_args[0][0]
        self.assertEqual(req.headers["Authorization"], "Bearer lvk_secret")


class TestHttpErrors(unittest.TestCase):
    @patch("handler.urllib.request.urlopen")
    def test_402_maps_to_insufficient_balance(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.HTTPError(
            "https://api.mentionsapi.com/v1/discover", 402, "Payment Required", None, None
        )
        with patch.dict(os.environ, {"MENTIONSAPI_KEY": "lvk_test"}):
            result = handler.discover_queries(brand="Linear")
        self.assertEqual(result["error"], "insufficient_balance")


if __name__ == "__main__":
    unittest.main()
