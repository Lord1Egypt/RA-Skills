import argparse
import contextlib
import importlib.util
import io
import json
import os
import pathlib
import unittest
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "tuqu_request.py"


def load_module():
    spec = importlib.util.spec_from_file_location("tuqu_request", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class FakeResponse:
    def __init__(self, payload: bytes):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return self.payload


class TuquRequestEnvTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def test_main_supports_pricing_config_without_auth(self):
        request_capture = {}

        def fake_urlopen(request, timeout):
            request_capture["url"] = request.full_url
            request_capture["Authorization"] = request.get_header("Authorization")
            request_capture["X-api-key"] = request.get_header("X-api-key")
            return FakeResponse(json.dumps({"ok": True}).encode("utf-8"))

        args = argparse.Namespace(
            method="GET",
            path="/api/pricing-config",
            base_url=None,
            query=[],
            json=None,
            body_file=None,
            auth_mode="auto",
            service_key=None,
            timeout=5,
        )

        with mock.patch.dict(os.environ, {}, clear=True):
            with mock.patch.object(self.module, "parse_args", return_value=args):
                with mock.patch.object(self.module.urllib.request, "urlopen", side_effect=fake_urlopen):
                    with contextlib.redirect_stdout(io.StringIO()):
                        exit_code = self.module.main()

        self.assertEqual(exit_code, 0)
        self.assertEqual(request_capture["url"], "https://photo.tuqu.ai/api/pricing-config")
        self.assertIsNone(request_capture["Authorization"])
        self.assertIsNone(request_capture["X-api-key"])

    def test_prepare_body_uses_explicit_service_key_for_user_key(self):
        body = self.module.prepare_body("user-key", {}, service_key="role-key")
        self.assertEqual(body["userKey"], "role-key")

    def test_prepare_body_requires_explicit_service_key_when_missing(self):
        with mock.patch.dict(
            os.environ,
            {"TUQU_USER_SERVICE_KEY": "shared-key"},
            clear=True,
        ):
            with self.assertRaisesRegex(ValueError, "--service-key"):
                self.module.prepare_body("user-key", {})

    def test_main_uses_explicit_service_key_for_api_key_header(self):
        request_capture = {}

        def fake_urlopen(request, timeout):
            request_capture["X-api-key"] = request.get_header("X-api-key")
            return FakeResponse(json.dumps({"ok": True}).encode("utf-8"))

        args = argparse.Namespace(
            method="GET",
            path="/api/characters",
            base_url=None,
            query=[],
            json=None,
            body_file=None,
            auth_mode="auto",
            service_key="role-key",
            timeout=5,
        )

        with mock.patch.dict(os.environ, {}, clear=True):
            with mock.patch.object(self.module, "parse_args", return_value=args):
                with mock.patch.object(self.module.urllib.request, "urlopen", side_effect=fake_urlopen):
                    with contextlib.redirect_stdout(io.StringIO()):
                        exit_code = self.module.main()

        self.assertEqual(exit_code, 0)
        self.assertEqual(request_capture["X-api-key"], "role-key")

    def test_main_ignores_tuqu_user_service_key_env_var(self):
        request_called = False

        def fake_urlopen(request, timeout):
            nonlocal request_called
            request_called = True
            return FakeResponse(json.dumps({"ok": True}).encode("utf-8"))

        args = argparse.Namespace(
            method="GET",
            path="/api/characters",
            base_url=None,
            query=[],
            json=None,
            body_file=None,
            auth_mode="auto",
            service_key=None,
            timeout=5,
        )

        with mock.patch.dict(
            os.environ,
            {"TUQU_USER_SERVICE_KEY": "shared-key"},
            clear=True,
        ):
            with mock.patch.object(self.module, "parse_args", return_value=args):
                with mock.patch.object(self.module.urllib.request, "urlopen", side_effect=fake_urlopen):
                    with contextlib.redirect_stderr(io.StringIO()) as stderr:
                        with contextlib.redirect_stdout(io.StringIO()):
                            exit_code = self.module.main()

        self.assertEqual(exit_code, 1)
        self.assertFalse(request_called)
        self.assertIn("--service-key", stderr.getvalue())

    def test_main_uses_explicit_service_key_for_service_key_header(self):
        request_capture = {}

        def fake_urlopen(request, timeout):
            request_capture["Authorization"] = request.get_header("Authorization")
            return FakeResponse(json.dumps({"ok": True}).encode("utf-8"))

        args = argparse.Namespace(
            method="GET",
            path="/api/v1/recharge/plans",
            base_url=None,
            query=[],
            json=None,
            body_file=None,
            auth_mode="auto",
            service_key="role-key",
            timeout=5,
        )

        with mock.patch.dict(os.environ, {}, clear=True):
            with mock.patch.object(self.module, "parse_args", return_value=args):
                with mock.patch.object(self.module.urllib.request, "urlopen", side_effect=fake_urlopen):
                    with contextlib.redirect_stdout(io.StringIO()):
                        exit_code = self.module.main()

        self.assertEqual(exit_code, 0)
        self.assertEqual(request_capture["Authorization"], "Bearer role-key")

    def test_main_uses_explicit_service_key_for_user_key_body(self):
        request_capture = {}

        def fake_urlopen(request, timeout):
            request_capture["body"] = json.loads(request.data.decode("utf-8"))
            return FakeResponse(json.dumps({"ok": True}).encode("utf-8"))

        args = argparse.Namespace(
            method="POST",
            path="/api/v2/generate-image",
            base_url=None,
            query=[],
            json='{"prompt":"portrait"}',
            body_file=None,
            auth_mode="auto",
            service_key="role-key",
            timeout=5,
        )

        with mock.patch.dict(os.environ, {}, clear=True):
            with mock.patch.object(self.module, "parse_args", return_value=args):
                with mock.patch.object(self.module.urllib.request, "urlopen", side_effect=fake_urlopen):
                    with contextlib.redirect_stdout(io.StringIO()):
                        exit_code = self.module.main()

        self.assertEqual(exit_code, 0)
        self.assertEqual(request_capture["body"]["userKey"], "role-key")

    def test_main_requires_explicit_service_key_for_service_key_header(self):
        request_called = False

        def fake_urlopen(request, timeout):
            nonlocal request_called
            request_called = True
            return FakeResponse(json.dumps({"ok": True}).encode("utf-8"))

        args = argparse.Namespace(
            method="GET",
            path="/api/v1/recharge/plans",
            base_url=None,
            query=[],
            json=None,
            body_file=None,
            auth_mode="auto",
            service_key=None,
            timeout=5,
        )

        with mock.patch.dict(os.environ, {}, clear=True):
            with mock.patch.object(self.module, "parse_args", return_value=args):
                with mock.patch.object(self.module.urllib.request, "urlopen", side_effect=fake_urlopen):
                    with contextlib.redirect_stderr(io.StringIO()) as stderr:
                        with contextlib.redirect_stdout(io.StringIO()):
                            exit_code = self.module.main()

        self.assertEqual(exit_code, 1)
        self.assertFalse(request_called)
        self.assertIn("--service-key", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
