import importlib.util
import os
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "hik_open_device_management.py"
SPEC = importlib.util.spec_from_file_location("hik_open_device_management", MODULE_PATH)
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC is not None and SPEC.loader is not None
sys.modules[SPEC.name] = MOD
SPEC.loader.exec_module(MOD)

CUSTOM_TEST_BASE_URL = "https://custom-test.invalid/"


class FakeStream:
    def __init__(self, is_tty: bool = True):
        self._is_tty = is_tty
        self.reconfigure_calls = []

    def isatty(self) -> bool:
        return self._is_tty

    def reconfigure(self, **kwargs) -> None:
        self.reconfigure_calls.append(kwargs)


class HikOpenDeviceManagementTests(unittest.TestCase):
    def test_default_token_cache_uses_shared_path(self):
        self.assertEqual(
            MOD.DEFAULT_TOKEN_CACHE,
            Path.home() / ".cache" / "hik_open" / "token.json",
        )

    def test_configure_windows_utf8_output_switches_console_to_utf8(self):
        stdout = FakeStream()
        stderr = FakeStream()
        kernel32 = types.SimpleNamespace(
            SetConsoleOutputCP=mock.Mock(return_value=1),
            SetConsoleCP=mock.Mock(return_value=1),
        )

        with mock.patch.object(MOD.os, "name", "nt"), mock.patch.object(
            MOD.ctypes,
            "windll",
            types.SimpleNamespace(kernel32=kernel32),
            create=True,
        ):
            MOD.configure_windows_utf8_output(stdout=stdout, stderr=stderr)

        self.assertEqual(
            stdout.reconfigure_calls,
            [{"encoding": "utf-8", "errors": "replace"}],
        )
        self.assertEqual(
            stderr.reconfigure_calls,
            [{"encoding": "utf-8", "errors": "replace"}],
        )
        kernel32.SetConsoleOutputCP.assert_called_once_with(65001)
        kernel32.SetConsoleCP.assert_called_once_with(65001)

    def test_main_configures_console_output_before_running(self):
        args = types.SimpleNamespace(command="count")
        with mock.patch.object(MOD, "parse_args", return_value=args), mock.patch.object(
            MOD, "configure_windows_utf8_output"
        ) as configure_mock, mock.patch.object(
            MOD, "run_command", return_value=0
        ) as run_command_mock:
            exit_code = MOD.main()

        self.assertEqual(exit_code, 0)
        configure_mock.assert_called_once_with()
        run_command_mock.assert_called_once_with(args)

    def test_resolve_base_url_uses_default_prod_domain(self):
        with mock.patch.dict(os.environ, {}, clear=False):
            self.assertEqual(MOD.resolve_base_url(None), MOD.DEFAULT_BASE_URL)

    def test_resolve_base_url_prefers_env_for_internal_test_domain(self):
        with mock.patch.dict(os.environ, {"HIK_OPEN_BASE_URL": CUSTOM_TEST_BASE_URL}, clear=False):
            self.assertEqual(MOD.resolve_base_url(None), "https://custom-test.invalid")

    def test_resolve_base_url_cli_overrides_env(self):
        with mock.patch.dict(os.environ, {"HIK_OPEN_BASE_URL": CUSTOM_TEST_BASE_URL}, clear=False):
            self.assertEqual(MOD.resolve_base_url("https://api2.hik-cloud.com/"), "https://api2.hik-cloud.com")

    def test_build_create_spec_uses_json_contract(self):
        args = MOD.parse_args(
            [
                "create",
                "--device-serial",
                "E05426006",
                "--group-no",
                "fsdfe",
                "--validate-code",
                "ADSEFE",
            ]
        )
        spec = MOD.build_create_spec(args)
        self.assertEqual(spec.method, "POST")
        self.assertEqual(spec.path, MOD.CREATE_PATH)
        self.assertEqual(
            spec.json_body,
            {
                "deviceSerial": "E05426006",
                "groupNo": "fsdfe",
                "validateCode": "ADSEFE",
            },
        )

    def test_build_delete_spec_uses_query_contract(self):
        args = MOD.parse_args(["delete", "--device-serial", "123456"])
        spec = MOD.build_delete_spec(args)
        self.assertEqual(spec.method, "POST")
        self.assertEqual(spec.query, {"deviceSerial": "123456"})

    def test_build_rename_spec_uses_json_contract(self):
        args = MOD.parse_args(
            ["rename", "--device-serial", "E05426006", "--device-name", "设备名称"]
        )
        spec = MOD.build_rename_spec(args)
        self.assertEqual(spec.method, "POST")
        self.assertEqual(
            spec.json_body,
            {"deviceSerial": "E05426006", "deviceName": "设备名称"},
        )

    def test_build_get_spec_includes_need_defence_when_requested(self):
        args = MOD.parse_args(["get", "--device-serial", "D05215100", "--need-defence"])
        spec = MOD.build_get_spec(args)
        self.assertEqual(spec.method, "GET")
        self.assertEqual(
            spec.query,
            {"deviceSerial": "D05215100", "needDefence": "true"},
        )

    def test_build_list_spec_uses_query_contract(self):
        args = MOD.parse_args(
            ["list", "--group-no", "1", "--page-no", "1", "--page-size", "50"]
        )
        spec = MOD.build_list_spec(args)
        self.assertEqual(spec.method, "GET")
        self.assertEqual(
            spec.query,
            {"groupNo": "1", "pageNo": 1, "pageSize": 50},
        )

    def test_build_count_spec_has_no_query(self):
        args = MOD.parse_args(["count"])
        spec = MOD.build_count_spec(args)
        self.assertEqual(spec.method, "GET")
        self.assertEqual(spec.path, MOD.COUNT_PATH)
        self.assertIsNone(spec.query)

    def test_build_status_spec_uses_query_contract(self):
        args = MOD.parse_args(["status", "--device-serial", "C01563792"])
        spec = MOD.build_status_spec(args)
        self.assertEqual(spec.method, "GET")
        self.assertEqual(spec.query, {"deviceSerial": "C01563792"})

    def test_build_reboot_spec_uses_json_contract(self):
        args = MOD.parse_args(["reboot", "--device-serial", "123456789"])
        spec = MOD.build_reboot_spec(args)
        self.assertEqual(spec.method, "POST")
        self.assertEqual(spec.json_body, {"deviceSerial": "123456789"})

    def test_token_cache_round_trip(self):
        with tempfile.TemporaryDirectory() as td:
            cache_file = Path(td) / "token.json"
            payload = {
                "access_token": "abc",
                "expires_at": MOD.time.time() + 3600,
            }
            MOD.save_token_cache(cache_file, payload)
            loaded = MOD.load_token_cache(cache_file)
            self.assertEqual(loaded["access_token"], "abc")

    def test_fetch_access_token_error_omits_raw_payload(self):
        with mock.patch.object(
            MOD,
            "http_json_request",
            return_value=(400, {"code": "bad_client", "message": "invalid client", "access_token": "leak"}),
        ):
            with self.assertRaises(MOD.ApiError) as ctx:
                MOD.fetch_access_token("https://example.com", "id", "secret", 5.0)

        message = str(ctx.exception)
        self.assertIn("http=400", message)
        self.assertIn("code=bad_client", message)
        self.assertIn("message=invalid client", message)
        self.assertNotIn("access_token", message)

    def test_api_request_error_omits_raw_payload(self):
        spec = MOD.RequestSpec(method="GET", path="/x")
        with mock.patch.object(MOD, "resolve_access_token", return_value=("token", False)), mock.patch.object(
            MOD,
            "http_json_request",
            return_value=(400, {"code": "bad_request", "message": "invalid input", "secret": "hidden"}),
        ):
            with self.assertRaises(MOD.ApiError) as ctx:
                MOD.api_request(
                    base_url="https://example.com",
                    timeout=5.0,
                    cache_file=Path("/tmp/mock-token.json"),
                    explicit_token=None,
                    spec=spec,
                )

        message = str(ctx.exception)
        self.assertIn("http=400", message)
        self.assertIn("code=bad_request", message)
        self.assertIn("message=invalid input", message)
        self.assertNotIn("secret", message)


if __name__ == "__main__":
    unittest.main()
