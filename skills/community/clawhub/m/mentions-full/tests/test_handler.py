"""Smoke tests for the mentions-full handler. No network — urlopen is mocked."""

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


def _req(mock_urlopen):
    return mock_urlopen.call_args[0][0]


def _sent_body(mock_urlopen):
    return json.loads(_req(mock_urlopen).data.decode("utf-8"))


class TestAuth(unittest.TestCase):
    def test_missing_key_returns_auth_required(self):
        with patch.dict(os.environ, {}, clear=True):
            result = handler.check_mentions(query="q", brand="b")
        self.assertEqual(result["error"], "auth_required")
        self.assertIn("MENTIONSAPI_KEY", result["detail"])
        self.assertEqual(result["signup_url"], "https://mentionsapi.com/signup")


class TestInputValidation(unittest.TestCase):
    def test_check_requires_query_and_brand(self):
        with patch.dict(os.environ, {"MENTIONSAPI_KEY": "lvk_test"}):
            self.assertEqual(handler.check_mentions(query="", brand="b")["error"], "invalid_argument")

    def test_compare_requires_query_a_and_brand_a(self):
        with patch.dict(os.environ, {"MENTIONSAPI_KEY": "lvk_test"}):
            self.assertEqual(
                handler.compare_mentions(query_a="", brand_a="b")["error"], "invalid_argument"
            )

    def test_watch_requires_long_secret(self):
        with patch.dict(os.environ, {"MENTIONSAPI_KEY": "lvk_test"}):
            result = handler.watch_brand(
                query="q", brand="b", webhook_url="https://x.com/h", webhook_secret="short"
            )
        self.assertEqual(result["error"], "invalid_argument")
        self.assertIn("16 characters", result["detail"])


class TestEndpoints(unittest.TestCase):
    @patch("handler.urllib.request.urlopen")
    def test_check_posts_to_v1_check(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b"{}")
        with patch.dict(os.environ, {"MENTIONSAPI_KEY": "lvk_test"}):
            handler.check_mentions(query="best CRM", brand="HubSpot", mode="all_live")
        self.assertEqual(_req(mock_urlopen).full_url, "https://api.mentionsapi.com/v1/check")
        body = _sent_body(mock_urlopen)
        self.assertEqual(body["mode"], "all_live")
        self.assertNotIn("providers", body)

    @patch("handler.urllib.request.urlopen")
    def test_discover_posts_to_v1_discover(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b"{}")
        with patch.dict(os.environ, {"MENTIONSAPI_KEY": "lvk_test"}):
            handler.discover_queries(brand="Linear")
        self.assertEqual(_req(mock_urlopen).full_url, "https://api.mentionsapi.com/v1/discover")
        self.assertEqual(_sent_body(mock_urlopen)["count"], 50)

    @patch("handler.urllib.request.urlopen")
    def test_compare_posts_to_v1_compare(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b"{}")
        with patch.dict(os.environ, {"MENTIONSAPI_KEY": "lvk_test"}):
            handler.compare_mentions(query_a="best CRM", brand_a="HubSpot", brand_b="Salesforce")
        self.assertEqual(_req(mock_urlopen).full_url, "https://api.mentionsapi.com/v1/compare")
        body = _sent_body(mock_urlopen)
        self.assertEqual(body["brand_a"], "HubSpot")
        self.assertEqual(body["brand_b"], "Salesforce")
        self.assertNotIn("query_b", body)

    @patch("handler.urllib.request.urlopen")
    def test_watch_posts_to_v1_watch(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b"{}")
        with patch.dict(os.environ, {"MENTIONSAPI_KEY": "lvk_test"}):
            handler.watch_brand(
                query="best CRM",
                brand="HubSpot",
                webhook_url="https://example.com/hook",
                webhook_secret="0123456789abcdef0123",
                interval="hourly",
            )
        self.assertEqual(_req(mock_urlopen).full_url, "https://api.mentionsapi.com/v1/watch")
        body = _sent_body(mock_urlopen)
        self.assertEqual(body["interval"], "hourly")
        self.assertEqual(body["webhook_url"], "https://example.com/hook")

    @patch("handler.urllib.request.urlopen")
    def test_authorization_header_is_set(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b"{}")
        with patch.dict(os.environ, {"MENTIONSAPI_KEY": "lvk_secret"}):
            handler.check_mentions(query="q", brand="b")
        req = _req(mock_urlopen)
        self.assertEqual(req.headers["Authorization"], "Bearer lvk_secret")
        self.assertIn("llm-mentions-skills", req.headers["User-agent"])


class TestHttpErrors(unittest.TestCase):
    @patch("handler.urllib.request.urlopen")
    def test_501_maps_to_mode_roadmap(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.HTTPError(
            "https://api.mentionsapi.com/v1/check", 501, "Not Implemented", None, None
        )
        with patch.dict(os.environ, {"MENTIONSAPI_KEY": "lvk_test"}):
            result = handler.check_mentions(query="q", brand="b", mode="deep")
        self.assertEqual(result["error"], "mode_roadmap")
        self.assertIn("quick", result["detail"])

    @patch("handler.urllib.request.urlopen")
    def test_429_maps_to_rate_limit(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.HTTPError(
            "https://api.mentionsapi.com/v1/check", 429, "Too Many Requests", None, None
        )
        with patch.dict(os.environ, {"MENTIONSAPI_KEY": "lvk_test"}):
            result = handler.check_mentions(query="q", brand="b")
        self.assertEqual(result["error"], "rate_limit_exceeded")


if __name__ == "__main__":
    unittest.main()
