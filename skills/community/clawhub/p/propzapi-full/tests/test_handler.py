"""Smoke tests for the propzapi-full handler. No network — urlopen is mocked."""

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


def _body(mock_urlopen):
    return json.loads(_req(mock_urlopen).data.decode("utf-8"))


class TestAuth(unittest.TestCase):
    def test_missing_key_returns_auth_required(self):
        with patch.dict(os.environ, {}, clear=True):
            result = handler.generate_image(template="tpl_abc")
        self.assertEqual(result["error"], "auth_required")
        self.assertIn("PROPZAPI_KEY", result["detail"])
        self.assertEqual(result["signup_url"], "https://propzapi.com/app")


class TestInputValidation(unittest.TestCase):
    def test_generate_requires_template(self):
        with patch.dict(os.environ, {"PROPZAPI_KEY": "test_key"}):
            self.assertEqual(handler.generate_image(template="")["error"], "invalid_argument")

    def test_generate_rejects_bad_format(self):
        with patch.dict(os.environ, {"PROPZAPI_KEY": "test_key"}):
            self.assertEqual(
                handler.generate_image(template="tpl_abc", format="gif")["error"],
                "invalid_argument",
            )

    def test_screenshot_requires_url(self):
        with patch.dict(os.environ, {"PROPZAPI_KEY": "test_key"}):
            self.assertEqual(handler.screenshot(url="")["error"], "invalid_argument")

    def test_create_template_requires_name_and_html(self):
        with patch.dict(os.environ, {"PROPZAPI_KEY": "test_key"}):
            self.assertEqual(
                handler.create_template(name="", html="", width=800, height=600)["error"],
                "invalid_argument",
            )


class TestEndpoints(unittest.TestCase):
    @patch("handler.urllib.request.urlopen")
    def test_generate_image_posts_v1_images_with_key(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(
            b'{"url": "https://cdn.propzapi.com/x.png", "width": 1200, "height": 630, "format": "png", "bytes": 42}'
        )
        with patch.dict(os.environ, {"PROPZAPI_KEY": "test_key"}):
            out = handler.generate_image(
                template="tpl_abc",
                modifications={"title": "Hello"},
                format="png",
            )
        self.assertEqual(out["width"], 1200)
        req = _req(mock_urlopen)
        self.assertIn("/v1/images", req.full_url)
        self.assertEqual(req.method, "POST")
        self.assertEqual(req.headers["X-api-key"], "test_key")
        body = _body(mock_urlopen)
        self.assertEqual(body["template"], "tpl_abc")
        self.assertEqual(body["modifications"], {"title": "Hello"})
        self.assertEqual(body["format"], "png")

    @patch("handler.urllib.request.urlopen")
    def test_screenshot_posts_v1_screenshot(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b'{"url": "https://cdn.propzapi.com/s.png"}')
        with patch.dict(os.environ, {"PROPZAPI_KEY": "test_key"}):
            handler.screenshot(url="https://example.com", full_page=True, width=1280)
        req = _req(mock_urlopen)
        self.assertIn("/v1/screenshot", req.full_url)
        self.assertEqual(req.method, "POST")
        body = _body(mock_urlopen)
        self.assertEqual(body["url"], "https://example.com")
        self.assertTrue(body["full_page"])
        self.assertEqual(body["width"], 1280)

    @patch("handler.urllib.request.urlopen")
    def test_list_templates_gets_v1_templates(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b'{"count": 0, "data": []}')
        with patch.dict(os.environ, {"PROPZAPI_KEY": "test_key"}):
            out = handler.list_templates()
        self.assertEqual(out, {"count": 0, "data": []})
        req = _req(mock_urlopen)
        self.assertTrue(req.full_url.endswith("/v1/templates"))
        self.assertEqual(req.method, "GET")

    @patch("handler.urllib.request.urlopen")
    def test_create_template_posts_v1_templates(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b'{"template": "tpl_new", "name": "Card"}')
        with patch.dict(os.environ, {"PROPZAPI_KEY": "test_key"}):
            out = handler.create_template(
                name="Card",
                html="<div>{{title}}</div>",
                width=1200,
                height=630,
                variables=["title"],
            )
        self.assertEqual(out["template"], "tpl_new")
        req = _req(mock_urlopen)
        self.assertIn("/v1/templates", req.full_url)
        self.assertEqual(req.method, "POST")
        body = _body(mock_urlopen)
        self.assertEqual(body["name"], "Card")
        self.assertEqual(body["variables"], ["title"])

    @patch("handler.urllib.request.urlopen")
    def test_embed_url_posts_v1_embed_url(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b'{"url": "https://api.propzapi.com/r/signed"}')
        with patch.dict(os.environ, {"PROPZAPI_KEY": "test_key"}):
            handler.embed_url(template="tpl_abc", modifications={"title": "Hi"})
        req = _req(mock_urlopen)
        self.assertIn("/v1/embed-url", req.full_url)
        self.assertEqual(req.method, "POST")


class TestErrorMapping(unittest.TestCase):
    def _raise(self, code):
        return urllib.error.HTTPError("u", code, "e", {}, None)

    @patch("handler.urllib.request.urlopen")
    def test_402_out_of_credits(self, mock_urlopen):
        mock_urlopen.side_effect = self._raise(402)
        with patch.dict(os.environ, {"PROPZAPI_KEY": "test_key"}):
            out = handler.generate_image(template="tpl_abc")
        self.assertEqual(out["error"], "out_of_credits")
        self.assertEqual(out["upgrade_url"], "https://propzapi.com/pricing")

    @patch("handler.urllib.request.urlopen")
    def test_401_auth_invalid(self, mock_urlopen):
        mock_urlopen.side_effect = self._raise(401)
        with patch.dict(os.environ, {"PROPZAPI_KEY": "test_key"}):
            self.assertEqual(handler.generate_image(template="tpl_abc")["error"], "auth_invalid")


if __name__ == "__main__":
    unittest.main()
