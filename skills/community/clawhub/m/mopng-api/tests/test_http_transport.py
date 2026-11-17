#!/usr/bin/env python3
"""Tests for the shared transport and for the mopng_agent.py entry point."""

import importlib
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import _http
import mopng_agent


def _response(payload: bytes):
    class _Resp:
        def __enter__(self):
            return self

        def __exit__(self, *exc_info):
            return False

        def read(self):
            return payload

        def close(self):
            pass

    return _Resp()


class TestJsonHttpClient(unittest.TestCase):
    def test_sends_json_body_and_injected_headers(self):
        client = _http.JsonHttpClient("https://api.example", {"X-API-Key": "k"})
        with patch.object(_http.request, "urlopen", return_value=_response(b"{}")) as urlopen:
            client.request("POST", "/session", {"a": 1})
        req = urlopen.call_args.args[0]
        self.assertEqual(req.full_url, "https://api.example/session")
        self.assertEqual(req.get_header("X-api-key"), "k")
        self.assertEqual(req.get_header("Content-type"), "application/json")
        self.assertEqual(req.data, b'{"a": 1}')

    def test_no_body_request_omits_content_type(self):
        client = _http.JsonHttpClient("https://api.example/", {"Accept": "application/json"})
        with patch.object(_http.request, "urlopen", return_value=_response(b'{"ok": 1}')) as urlopen:
            result = client.request("GET", "/models")
        req = urlopen.call_args.args[0]
        self.assertEqual(req.full_url, "https://api.example/models")
        self.assertIsNone(req.data)
        self.assertIsNone(req.get_header("Content-type"))
        self.assertEqual(result, {"ok": 1})

    def test_empty_body_returns_empty_dict(self):
        client = _http.JsonHttpClient("https://api.example", {})
        with patch.object(_http.request, "urlopen", return_value=_response(b"")):
            self.assertEqual(client.request("DELETE", "/x"), {})

    def test_multipart_body_encodes_fields_and_file(self):
        client = _http.JsonHttpClient("https://api.example", {})
        fake = Path("/tmp/pic.png")
        with patch.object(_http.request, "urlopen", return_value=_response(b"{}")) as urlopen:
            client.request("POST", "/upload", {"k": "v"}, {"file": (fake, b"DATA")})
        req = urlopen.call_args.args[0]
        self.assertTrue(req.get_header("Content-type").startswith("multipart/form-data; boundary="))
        self.assertIn(b'name="k"', req.data)
        self.assertIn(b'filename="pic.png"', req.data)
        self.assertIn(b"DATA", req.data)


class TestJsonHttpClientErrors(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = _http.JsonHttpClient("https://api.example", {}, service="svc")

    def test_non_json_success_raises_runtime_error(self):
        with patch.object(_http.request, "urlopen", return_value=_response(b"<html>")):
            with self.assertRaises(RuntimeError) as ctx:
                self.client.request("GET", "/x")
        self.assertEqual(str(ctx.exception), "svc returned non-JSON data")

    def test_http_error_with_json_message(self):
        from urllib.error import HTTPError

        err = HTTPError("https://api.example", 400, "Bad", {}, _response(b'{"message": "bad key"}'))
        with patch.object(_http.request, "urlopen", side_effect=err):
            with self.assertRaises(RuntimeError) as ctx:
                self.client.request("GET", "/x")
        self.assertEqual(str(ctx.exception), "svc API error: bad key")

    def test_http_error_with_non_json_body(self):
        from urllib.error import HTTPError

        err = HTTPError("https://api.example", 502, "Bad", {}, _response(b"gateway down"))
        with patch.object(_http.request, "urlopen", side_effect=err):
            with self.assertRaises(RuntimeError) as ctx:
                self.client.request("GET", "/x")
        self.assertEqual(str(ctx.exception), "svc HTTP 502: gateway down")

    def test_urlerror_is_mapped_to_runtime_error(self):
        from urllib.error import URLError

        with patch.object(_http.request, "urlopen", side_effect=URLError("timed out")):
            with self.assertRaises(RuntimeError) as ctx:
                self.client.request("GET", "/x")
        self.assertIn("unavailable", str(ctx.exception))


class TestAgentClient(unittest.TestCase):
    def test_call_uses_agent_prefix_and_api_key_header(self):
        client = mopng_agent.AgentClient("https://agent.example/", "secret")
        with patch.object(_http.request, "urlopen", return_value=_response(b'{"session_id": "s1"}')) as urlopen:
            result = client.call("POST", "/session", {"intent": "x"})
        req = urlopen.call_args.args[0]
        self.assertEqual(req.full_url, "https://agent.example/api/v1/open/agent/session")
        self.assertEqual(req.get_header("X-api-key"), "secret")
        self.assertEqual(req.get_header("Accept"), "application/json")
        self.assertEqual(result, {"session_id": "s1"})

    def test_network_failure_surfaces_as_runtime_error(self):
        from urllib.error import URLError

        client = mopng_agent.AgentClient("https://agent.example", "secret")
        with patch.object(_http.request, "urlopen", side_effect=URLError("dns")):
            with self.assertRaises(RuntimeError) as ctx:
                client.call("GET", "/models")
        self.assertTrue(str(ctx.exception).startswith("motu-agent unavailable"))


class TestAgentCLI(unittest.TestCase):
    def test_missing_api_key_returns_2(self):
        with patch.dict("os.environ", {}, clear=True):
            self.assertEqual(mopng_agent.main(["models"]), 2)

    def test_runtime_error_returns_2(self):
        with patch.dict("os.environ", {"MOPNG_API_KEY": "k"}), \
                patch.object(mopng_agent.AgentClient, "call", side_effect=RuntimeError("boom")), \
                patch("sys.stdout"):
            self.assertEqual(mopng_agent.main(["models"]), 2)

    def test_models_command_prints_payload(self):
        payload = {"models": [{"name": "m1"}]}
        with patch.dict("os.environ", {"MOPNG_API_KEY": "k"}), \
                patch.object(mopng_agent.AgentClient, "call", return_value=payload) as call, \
                patch("sys.stdout"):
            self.assertEqual(mopng_agent.main(["models", "--capability", "text-to-image"]), 0)
        self.assertIn("capability=text-to-image", call.call_args.args[1])

    def test_brief_rejects_too_many_references(self):
        args = mopng_agent.argparse.Namespace(
            reference_url=[f"https://x/{i}.png" for i in range(15)],
            intent="i", goal="g", usage=None, style_constraint=None, avoid=None,
            format="png", cost_mode="balanced", max_cost_points=10, max_time_sec=120,
            width=None, height=None,
        )
        with self.assertRaises(ValueError):
            mopng_agent._brief(args)

    def test_brief_requires_both_dimensions(self):
        args = mopng_agent.argparse.Namespace(
            reference_url=None, intent="i", goal="g", usage=None, style_constraint=None,
            avoid=None, format="png", cost_mode="balanced", max_cost_points=10,
            max_time_sec=120, width=1024, height=None,
        )
        with self.assertRaises(ValueError):
            mopng_agent._brief(args)


class TestGroupedCommandAlias(unittest.TestCase):
    def test_agent_prefix_is_stripped(self):
        with patch.dict("os.environ", {"MOPNG_API_KEY": "k"}), \
                patch.object(mopng_agent.AgentClient, "call", return_value={}), \
                patch("sys.stdout"):
            self.assertEqual(mopng_agent.main(["agent", "models"]), 0)


class TestModuleImportModes(unittest.TestCase):
    """Both entry points must import when run as a file or via ``-m``."""

    def test_entry_points_and_helper_are_loaded(self):
        for name in ("_http", "mopng_api", "mopng_agent"):
            self.assertIn(name, sys.modules)

    def test_helper_module_is_shared_across_entry_points(self):
        import mopng_api

        self.assertIs(mopng_api.JsonHttpClient, _http.JsonHttpClient)
        self.assertIs(mopng_agent.JsonHttpClient, _http.JsonHttpClient)

    def test_scripts_http_is_a_distinct_module_object(self):
        """Run as a module, ``scripts._http`` is a separate module object.

        The two spelling must stay interchangeable: both are the same source file
        and expose the same client class, so no behaviour drifts between modes.
        """
        module = importlib.import_module("scripts._http")
        self.assertNotIn("scripts.", _http.__name__)
        self.assertEqual(
            Path(module.__file__).resolve(), Path(_http.__file__).resolve()
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)