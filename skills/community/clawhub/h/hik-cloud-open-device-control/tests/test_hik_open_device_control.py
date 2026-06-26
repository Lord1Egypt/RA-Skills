import importlib.util
import json
import os
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "hik_open_device_control.py"
SPEC = importlib.util.spec_from_file_location("hik_open_device_control", MODULE_PATH)
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


class HikOpenDeviceControlTests(unittest.TestCase):
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
        args = MOD.parse_args(
            [
                "arm-get",
                "--device-serial",
                "K05818510",
            ]
        )
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

    def test_build_arm_set_spec_uses_query_contract(self):
        args = MOD.parse_args(
            [
                "arm-set",
                "--device-serial",
                "K05818510",
                "--is-defence",
                "1",
            ]
        )
        spec = MOD.build_arm_set_spec(args)
        self.assertEqual(spec.method, "POST")
        self.assertEqual(spec.query["deviceSerial"], "K05818510")
        self.assertEqual(spec.query["isDefence"], 1)

    def test_build_ptz_start_spec_includes_mode_when_provided(self):
        args = MOD.parse_args(
            [
                "ptz-start",
                "--device-serial",
                "D20591677",
                "--channel-no",
                "1",
                "--direction",
                "9",
                "--speed",
                "2",
                "--mode",
                "0",
            ]
        )
        spec = MOD.build_ptz_start_spec(args)
        self.assertEqual(spec.json_body["mode"], 0)
        self.assertEqual(spec.json_body["direction"], 9)

    def test_validate_ptz_args_rejects_bad_speed_for_mode_zero(self):
        with self.assertRaises(MOD.ApiError):
            MOD.validate_ptz_args(direction=9, speed=7, mode=0)

    def test_build_time_get_spec_uses_query_contract(self):
        args = MOD.parse_args(["time-get", "--device-serial", "C13032017"])
        spec = MOD.build_time_get_spec(args)
        self.assertEqual(spec.method, "GET")
        self.assertEqual(spec.path, MOD.TIME_GET_PATH)
        self.assertEqual(spec.query, {"deviceSerial": "C13032017"})

    def test_build_time_set_spec_uses_json_contract(self):
        args = MOD.parse_args(
            [
                "time-set",
                "--device-serial",
                "C13032017",
                "--time-mode",
                "NTP",
            ]
        )
        spec = MOD.build_time_set_spec(args)
        self.assertEqual(spec.method, "POST")
        self.assertEqual(spec.path, MOD.TIME_SET_PATH)
        self.assertEqual(spec.json_body, {"deviceSerial": "C13032017", "timeMode": "NTP"})

    def test_build_ntp_get_spec_uses_query_contract(self):
        args = MOD.parse_args(["ntp-get", "--device-serial", "C13032017"])
        spec = MOD.build_ntp_get_spec(args)
        self.assertEqual(spec.method, "GET")
        self.assertEqual(spec.path, MOD.NTP_GET_PATH)
        self.assertEqual(spec.query, {"deviceSerial": "C13032017"})

    def test_build_ntp_set_spec_uses_nested_ntp_server_payload(self):
        args = MOD.parse_args(
            [
                "ntp-set",
                "--device-serial",
                "C13032017",
                "--ntp-server-id",
                "1",
                "--addressing-format-type",
                "hostname",
                "--host-name",
                "time.windows.com",
                "--port-no",
                "123",
                "--synchronize-interval",
                "1440",
            ]
        )
        spec = MOD.build_ntp_set_spec(args)
        self.assertEqual(spec.method, "POST")
        self.assertEqual(spec.path, MOD.NTP_SET_PATH)
        self.assertEqual(
            spec.json_body,
            {
                "deviceSerial": "C13032017",
                "ntpServer": {
                    "id": "1",
                    "addressingFormatType": "hostname",
                    "hostName": "time.windows.com",
                    "portNo": 123,
                    "synchronizeInterval": 1440,
                },
            },
        )

    def test_build_ntp_config_get_spec_uses_query_contract(self):
        args = MOD.parse_args(
            [
                "ntp-config-get",
                "--device-serial",
                "C13032017",
                "--ntp-server-id",
                "1",
            ]
        )
        spec = MOD.build_ntp_config_get_spec(args)
        self.assertEqual(spec.method, "GET")
        self.assertEqual(spec.path, MOD.NTP_CONFIG_GET_PATH)
        self.assertEqual(spec.query, {"deviceSerial": "C13032017", "ntpServerId": 1})

    def test_build_ntp_config_set_spec_uses_nested_ntp_server_payload(self):
        args = MOD.parse_args(
            [
                "ntp-config-set",
                "--device-serial",
                "C13032017",
                "--ntp-server-id",
                "1",
                "--addressing-format-type",
                "ipaddress",
                "--ip-address",
                "192.168.1.1",
                "--port-no",
                "123",
                "--synchronize-interval",
                "1440",
            ]
        )
        spec = MOD.build_ntp_config_set_spec(args)
        self.assertEqual(spec.method, "POST")
        self.assertEqual(spec.path, MOD.NTP_CONFIG_SET_PATH)
        self.assertEqual(
            spec.json_body,
            {
                "deviceSerial": "C13032017",
                "ntpServerId": 1,
                "ntpServer": {
                    "id": "1",
                    "addressingFormatType": "ipaddress",
                    "ipAddress": "192.168.1.1",
                    "portNo": 123,
                    "synchronizeInterval": 1440,
                },
            },
        )

    def test_build_storage_init_spec_uses_json_contract(self):
        args = MOD.parse_args(["storage-init", "--device-serial", "123456"])
        spec = MOD.build_storage_init_spec(args)
        self.assertEqual(spec.method, "POST")
        self.assertEqual(spec.path, MOD.STORAGE_INIT_PATH)
        self.assertEqual(spec.json_body, {"devSerial": "123456"})

    def test_build_storage_init_progress_spec_uses_json_contract(self):
        args = MOD.parse_args(["storage-init-progress", "--device-serial", "123456"])
        spec = MOD.build_storage_init_progress_spec(args)
        self.assertEqual(spec.method, "POST")
        self.assertEqual(spec.path, MOD.STORAGE_INIT_PROGRESS_PATH)
        self.assertEqual(spec.json_body, {"devSerial": "123456"})

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
