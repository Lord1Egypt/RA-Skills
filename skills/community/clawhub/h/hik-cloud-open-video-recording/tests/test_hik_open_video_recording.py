import importlib.util
import os
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "hik_open_video_recording.py"
SPEC = importlib.util.spec_from_file_location("hik_open_video_recording", MODULE_PATH)
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


class HikCloudVideoRecordingTests(unittest.TestCase):
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

        self.assertEqual(stdout.reconfigure_calls, [{"encoding": "utf-8", "errors": "replace"}])
        self.assertEqual(stderr.reconfigure_calls, [{"encoding": "utf-8", "errors": "replace"}])
        kernel32.SetConsoleOutputCP.assert_called_once_with(65001)
        kernel32.SetConsoleCP.assert_called_once_with(65001)

    def test_main_configures_console_output_before_running(self):
        args = types.SimpleNamespace(command="project-list")
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

    def test_build_project_create_spec_uses_json_contract(self):
        args = MOD.parse_args(
            [
                "project-create",
                "--project-name",
                "项目名称",
                "--expire-days",
                "3",
                "--flow-limit",
                "10240000",
            ]
        )
        spec = MOD.build_project_create_spec(args)
        self.assertEqual(spec.method, "POST")
        self.assertEqual(spec.path, MOD.PROJECT_PATH)
        self.assertEqual(
            spec.json_body,
            {"projectName": "项目名称", "expireDays": 3, "flowLimit": 10240000},
        )

    def test_build_project_list_spec_uses_query_contract(self):
        args = MOD.parse_args(["project-list", "--page-no", "1", "--page-size", "20"])
        spec = MOD.build_project_list_spec(args)
        self.assertEqual(spec.method, "GET")
        self.assertEqual(spec.query, {"pageNo": 1, "pageSize": 20})

    def test_build_record_replay_spec_uses_json_contract(self):
        args = MOD.parse_args(
            [
                "record-replay",
                "--project-id",
                "p123",
                "--device-serial",
                "E05426006",
                "--channel-no",
                "1",
                "--start-time",
                "20260324120000",
                "--end-time",
                "20260324120500",
                "--rec-type",
                "cloud",
            ]
        )
        spec = MOD.build_record_replay_spec(args)
        self.assertEqual(spec.method, "POST")
        self.assertEqual(spec.path, MOD.RECORD_VIDEO_PATH)
        self.assertEqual(spec.json_body["projectId"], "p123")
        self.assertEqual(spec.json_body["recType"], "cloud")

    def test_build_task_list_spec_uses_query_contract(self):
        args = MOD.parse_args(["task-list", "--project-id", "p123", "--page-no", "1", "--page-size", "20"])
        spec = MOD.build_task_list_spec(args)
        self.assertEqual(spec.method, "GET")
        self.assertEqual(spec.query, {"projectId": "p123", "pageNo": 1, "pageSize": 20})

    def test_build_file_delete_spec_uses_query_contract(self):
        args = MOD.parse_args(["file-delete", "--project-id", "p123", "--file-id", "f123"])
        spec = MOD.build_file_delete_spec(args)
        self.assertEqual(spec.method, "DELETE")
        self.assertEqual(spec.query, {"projectId": "p123", "fileId": "f123"})

    def test_build_flow_update_spec_uses_query_contract(self):
        args = MOD.parse_args(["flow-update", "--project-id", "p123", "--flow-limit", "2048"])
        spec = MOD.build_flow_update_spec(args)
        self.assertEqual(spec.method, "PUT")
        self.assertEqual(spec.query, {"projectId": "p123", "flowLimit": 2048})

    def test_build_upload_address_spec_uses_json_contract(self):
        args = MOD.parse_args(
            [
                "upload-address",
                "--suffix",
                "jpg",
                "--file-num",
                "1",
                "--file-type",
                "0",
                "--file-child-type",
                "00",
            ]
        )
        spec = MOD.build_upload_address_spec(args)
        self.assertEqual(spec.method, "POST")
        self.assertEqual(spec.json_body["suffix"], "jpg")

    def test_build_save_file_spec_uses_json_contract(self):
        args = MOD.parse_args(
            [
                "save-file",
                "--source-url",
                "https://example.invalid",
                "--source-type",
                "4",
                "--file-type",
                "0",
                "--file-child-type",
                "00",
                "--file-name",
                "测试文件",
            ]
        )
        spec = MOD.build_save_file_spec(args)
        self.assertEqual(spec.method, "POST")
        self.assertEqual(spec.json_body["sourceUrl"], "https://example.invalid")

    def test_build_clip_spec_uses_json_contract(self):
        args = MOD.parse_args(
            [
                "clip",
                "--timeline-json",
                '[{"type":1,"fileId":"testfile","inputProjectId":"testproject","in":"0.0f","out":"30.0f"}]',
            ]
        )
        spec = MOD.build_clip_spec(args)
        self.assertEqual(spec.method, "POST")
        self.assertEqual(spec.path, MOD.CLIP_PATH)
        self.assertIn("timeLines", spec.json_body)

    def test_build_clip_file_query_spec_uses_json_contract(self):
        args = MOD.parse_args(["clip-file-query", "--task-id", "abc123", "--expire-seconds", "1800"])
        spec = MOD.build_clip_file_query_spec(args)
        self.assertEqual(spec.method, "POST")
        self.assertEqual(spec.json_body, {"taskId": "abc123", "expireSeconds": 1800})

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
