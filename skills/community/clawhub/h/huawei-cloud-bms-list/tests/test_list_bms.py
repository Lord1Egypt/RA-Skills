import datetime
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from list_bms import (  # noqa: E402
    ALLOWED_OPERATION,
    ApiError,
    AuthError,
    BmsListError,
    ConfigError,
    GuardError,
    MD_TABLE_COLUMNS,
    OutputError,
    active_filter_descriptions,
    build_command,
    classify_hcloud_failure,
    default_markdown_name,
    extract_json,
    extract_servers,
    filter_by_server_id,
    format_query_time,
    guard_operation,
    guard_write_intent,
    list_servers,
    list_servers_via_sdk,
    main,
    normalize_server,
    render_markdown,
    render_table,
    server_names,
    strip_status_tokens,
    write_markdown_file,
)

SERVER_1 = {
    "id": "bms-0001",
    "name": "bms-demo-01",
    "status": "ACTIVE",
    "flavor": {"id": "physical.s4.xlarge", "name": "s4.xlarge"},
    "os_ext_a_zavailability_zone": "cn-north-4a",
    "access_i_pv4": "10.0.0.5",
    "created": "2026-01-01T00:00:00Z",
    "key_name": "kp-1",
    "image": {"id": "img-1"},
    "enterprise_project_id": "0",
}
SERVER_2 = {
    "id": "bms-0002",
    "name": "bms-demo-02",
    "status": "SHUTOFF",
    "flavor": {"id": "physical.s3.large", "name": "s3.large"},
    "os_ext_a_zavailability_zone": "cn-north-4b",
    "access_i_pv4": "10.0.0.6",
    "tags": ["env:test"],
}


def hcloud_result(stdout="", stderr="", returncode=0):
    return subprocess.CompletedProcess(
        args=["hcloud"], returncode=returncode, stdout=stdout, stderr=stderr
    )


class FakeRunner:
    """subprocess.run fake returning canned hcloud outputs per call."""

    def __init__(self, results):
        self.results = list(results)
        self.calls = []

    def __call__(self, cmd, **kwargs):
        self.calls.append(cmd)
        if not self.results:
            raise AssertionError("unexpected extra hcloud call: %s" % cmd)
        out = self.results.pop(0)
        if isinstance(out, Exception):
            raise out
        return hcloud_result(*out)


class TestWriteIntentGuard(unittest.TestCase):
    def test_read_intent_passes(self):
        self.assertFalse(guard_write_intent("--region cn-north-4 --json list servers"))
        self.assertFalse(guard_write_intent("show server details flavors"))

    def test_create_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("CreateBareMetalServers bms-new")

    def test_delete_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--operation DeleteBareMetalServer")

    def test_mutating_verbs_blocked(self):
        for text in ("reboot bms-01", "rebuild server", "resize flavor",
                     "reinstall os", "reset password", "attach volume",
                     "detach volume", "change name", "update metadata",
                     "modify vm nic", "stop server", "start server"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_normalized_separators_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--create-server")
        with self.assertRaises(GuardError):
            guard_write_intent("reboot_server")

    def test_name_value_passes(self):
        # read-only filter value must NOT trip the guard
        self.assertFalse(guard_write_intent("--name bms-demo"))

    def test_operation_guard_rejects_non_list(self):
        with self.assertRaises(GuardError):
            guard_operation("ShowBaremetalServerTags")
        self.assertTrue(guard_operation(ALLOWED_OPERATION))

    def test_strip_status_tokens_exempts_readonly_enumerants(self):
        # REBOOT / HARD_REBOOT / REBUILD legitimately contain write-looking
        # words but are read-only status filters.
        argv = ["--status", "REBOOT", "--region", "cn-north-4"]
        self.assertFalse(guard_write_intent(" ".join(strip_status_tokens(argv))))
        self.assertFalse(
            guard_write_intent(" ".join(strip_status_tokens(["--status=REBUILD"]))))
        # other args in the same argv are still guarded
        with self.assertRaises(GuardError):
            guard_write_intent(
                " ".join(strip_status_tokens(["--status", "REBOOT", "reboot", "x"])))

    def test_strip_status_tokens_exempts_md_file_values(self):
        # The Markdown output path is file-system data, not a cloud operation:
        # a report named `bms-delete-report.md` must not trip the guard.
        self.assertEqual(
            strip_status_tokens(["--md-file", "bms-delete-report.md"]), [])
        self.assertEqual(
            strip_status_tokens(["--md-file=bms-start-report.md"]), [])
        self.assertEqual(
            strip_status_tokens(["--output-md", "bms-reboot-report.md"]), [])
        # `--md-file` takes an optional value: a following *flag* is still
        # scanned, so a mutating flag cannot hide behind it.
        self.assertIn("--operation",
                      strip_status_tokens(["--md-file", "--operation",
                                           "DeleteBareMetalServer"]))
        # A status enumerant is still exempt alongside the md path.
        self.assertFalse(guard_write_intent(" ".join(
            strip_status_tokens(["--status", "REBOOT",
                                 "--md-file", "bms-rebuild-report.md"]))))

    def test_md_file_path_with_write_words_not_blocked(self):
        self.assertFalse(guard_write_intent(
            " ".join(strip_status_tokens(["--md-file", "bms-delete-report.md"]))))
        self.assertFalse(guard_write_intent(
            " ".join(strip_status_tokens(["--md-file=bms-resize-report.md"]))))


class TestBuildCommand(unittest.TestCase):
    def test_basic(self):
        argv = build_command("cn-north-4")
        self.assertEqual(argv[0], "BMS")
        self.assertEqual(argv[1], "ListBareMetalServers")
        self.assertIn("--cli-region=cn-north-4", argv)
        self.assertIn("--limit=100", argv)
        self.assertIn("--offset=1", argv)

    def test_filters_appended(self):
        argv = build_command("cn-south-1", name="bms-01", status="ACTIVE",
                             limit=10, offset=3)
        self.assertIn("--name=bms-01", argv)
        self.assertIn("--status=ACTIVE", argv)
        self.assertIn("--limit=10", argv)
        self.assertIn("--offset=3", argv)

    def test_server_id_never_sent_to_server(self):
        # The real BMS ListBareMetalServers API has no server-id parameter —
        # the CLI argv must never contain a server-id flag.
        argv = build_command("cn-north-4", name="x", status="ACTIVE")
        self.assertFalse(any("server" in flag and flag.startswith("--") and
                             "id" in flag for flag in argv))
        self.assertFalse(any(flag.startswith("--id") for flag in argv))

    def test_no_write_flags_ever_added(self):
        argv = build_command("cn-north-4", status="ACTIVE")
        for flag in argv:
            self.assertFalse(flag.lower().lstrip("-").startswith(("create", "delete", "update")))


class TestExtract(unittest.TestCase):
    def test_extract_json_plain(self):
        data = extract_json(json.dumps({"servers": []}))
        self.assertEqual(data, {"servers": []})

    def test_extract_json_with_noise(self):
        data = extract_json("WARNING some noise\n{\"a\": 1}\n")
        self.assertEqual(data, {"a": 1})

    def test_extract_json_invalid(self):
        with self.assertRaises(ApiError):
            extract_json("<html>not json</html>")

    def test_extract_servers_known_keys(self):
        for key in ("servers", "baremetal_servers", "server_list"):
            self.assertEqual(extract_servers({key: [SERVER_1]}), [SERVER_1])
        self.assertEqual(extract_servers([SERVER_1]), [SERVER_1])
        self.assertEqual(extract_servers({"count": 0}), [])


class TestClassifyFailure(unittest.TestCase):
    def test_missing_credentials(self):
        err = classify_hcloud_failure(
            "", "ERROR: cli-ak is empty, please run hcloud configure", 1)
        self.assertIsInstance(err, ConfigError)
        self.assertIn("AK/SK", str(err))

    def test_missing_profile(self):
        err = classify_hcloud_failure(
            "[USE_ERROR]The configuration file does not contain profile. "
            "Run the `hcloud configure set` command to add profile.", "", 0)
        self.assertIsInstance(err, ConfigError)
        self.assertIn("AK/SK", str(err))

    def test_auth_403(self):
        err = classify_hcloud_failure(
            "", '{"error_code":"ApiGW.0301","error_msg":"403 Forbidden"}', 1)
        self.assertIsInstance(err, AuthError)
        self.assertIn("IAM", str(err))

    def test_auth_unauthorized(self):
        err = classify_hcloud_failure("", "Unauthorized: invalid AK", 1)
        self.assertIsInstance(err, AuthError)

    def test_generic_api_error(self):
        err = classify_hcloud_failure("", "boom", 2)
        self.assertIsInstance(err, ApiError)

    def test_use_error_marker_with_zero_rc(self):
        err = classify_hcloud_failure(
            "[USE_ERROR]Invalid parameter: offset\n\n"
            "Run `hcloud BMS ListBareMetalServers --help` for details.", "", 0)
        self.assertIsInstance(err, ApiError)
        self.assertIn("参数错误", str(err))
        self.assertIn("--help", str(err))


class TestListServers(unittest.TestCase):
    def test_single_page(self):
        fake = FakeRunner([(
            json.dumps({"servers": [SERVER_1, SERVER_2], "count": 2}), "", 0)])
        with mock.patch("list_bms.subprocess.run", fake):
            servers = list_servers("cn-north-4")
        self.assertEqual(servers, [SERVER_1, SERVER_2])
        self.assertEqual(len(fake.calls), 1)

    def test_pagination_via_count(self):
        page1 = {"servers": [SERVER_1], "count": 2}
        page2 = {"servers": [SERVER_2], "count": 2}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("list_bms.subprocess.run", fake):
            servers = list_servers("cn-north-4", limit=1)
        self.assertEqual(servers, [SERVER_1, SERVER_2])
        self.assertEqual(len(fake.calls), 2)
        # BMS offset is a page number: the second request asks for page 2.
        self.assertIn("--offset=2", fake.calls[1])
        self.assertIn("--offset=1", fake.calls[0])

    def test_pagination_via_full_page_without_count(self):
        page1 = {"servers": [SERVER_1]}
        page2 = {"servers": []}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("list_bms.subprocess.run", fake):
            servers = list_servers("cn-north-4", limit=1)
        self.assertEqual(servers, [SERVER_1])

    def test_empty_region(self):
        fake = FakeRunner([(json.dumps({"servers": [], "count": 0}), "", 0)])
        with mock.patch("list_bms.subprocess.run", fake):
            servers = list_servers("cn-north-4")
        self.assertEqual(servers, [])

    def test_status_forwarded_to_server(self):
        # status IS a real server-side parameter for BMS.
        fake = FakeRunner([(
            json.dumps({"servers": [SERVER_1], "count": 1}), "", 0)])
        with mock.patch("list_bms.subprocess.run", fake):
            servers = list_servers("cn-north-4", status="ACTIVE")
        self.assertEqual(servers, [SERVER_1])
        self.assertTrue(any("--status=ACTIVE" in part for part in fake.calls[0]))

    def test_server_id_filter_applied_client_side(self):
        # server-id must NOT be forwarded to hcloud; filtering happens locally
        # on the fetched full list (server has no server-id parameter).
        fake = FakeRunner([(
            json.dumps({"servers": [SERVER_1, SERVER_2], "count": 2}), "", 0)])
        with mock.patch("list_bms.subprocess.run", fake):
            servers = list_servers("cn-north-4", server_id="bms-0001")
        self.assertEqual(servers, [SERVER_1])
        for call in fake.calls:
            self.assertFalse(any("server-id" in part or "--id" in part for part in call))

    def test_use_error_rc0_raises_api_error(self):
        fake = FakeRunner([(
            "[USE_ERROR]Invalid parameter: foo\n\n"
            "Run `hcloud BMS ListBareMetalServers --help` for details.", "", 0)])
        with mock.patch("list_bms.subprocess.run", fake):
            with self.assertRaises(ApiError) as ctx:
                list_servers("cn-north-4")
        self.assertIn("参数错误", str(ctx.exception))

    def test_nonzero_exit_403(self):
        fake = FakeRunner([("", "403 Forbidden", 1)])
        with mock.patch("list_bms.subprocess.run", fake):
            with self.assertRaises(AuthError):
                list_servers("cn-north-4")

    def test_nonzero_exit_credentials(self):
        fake = FakeRunner([("", "ERROR: no AK configured", 1)])
        with mock.patch("list_bms.subprocess.run", fake):
            with self.assertRaises(ConfigError):
                list_servers("cn-north-4")

    def test_timeout(self):
        fake = FakeRunner([subprocess.TimeoutExpired(cmd="hcloud", timeout=120)])
        with mock.patch("list_bms.subprocess.run", fake):
            with self.assertRaises(ApiError):
                list_servers("cn-north-4")

    def test_sdk_fallback_when_hcloud_missing(self):
        with mock.patch("list_bms.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_bms.list_servers_via_sdk",
                           return_value=[SERVER_1, SERVER_2]) as sdk_mock:
            servers = list_servers("cn-north-4", status="ACTIVE",
                                   server_id="bms-0002")
        # server-id is applied client-side even on the SDK fallback path.
        self.assertEqual(servers, [SERVER_2])
        # status IS forwarded to the SDK (native parameter).
        self.assertEqual(sdk_mock.call_args.kwargs.get("status"), "ACTIVE")
        self.assertNotIn("server_id", sdk_mock.call_args.kwargs)

    def test_sdk_fallback_unavailable_raises_config(self):
        with mock.patch("list_bms.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_bms.list_servers_via_sdk",
                           side_effect=ConfigError("huaweicloudsdkbms 未安装")):
            with self.assertRaises(ConfigError):
                list_servers("cn-north-4")

    def test_sdk_request_signature(self):
        # Regression guard: the real huaweicloudsdkbms ListBareMetalServersRequest
        # must be constructible with exactly the kwargs the fallback path sends
        # (status IS supported), and `server_id=` must raise TypeError.
        try:
            from huaweicloudsdkbms.v1 import ListBareMetalServersRequest
        except ImportError:
            self.skipTest("huaweicloudsdkbms not installed")
        request = ListBareMetalServersRequest(
            limit=100, offset=1, name="bms-01", status="ACTIVE",
        )
        self.assertEqual(getattr(request, "status", None), "ACTIVE")
        with self.assertRaises(TypeError):
            ListBareMetalServersRequest(server_id="bms-1")


class _FakeSdkResponse:
    def __init__(self, servers, count):
        self.servers = servers
        self.count = count


class _FakeSdkServer:
    def __init__(self, payload):
        self._payload = payload

    def to_dict(self):
        return self._payload


class _FakeSdkBuilder:
    def __init__(self, test):
        self._test = test

    def with_credentials(self, credentials):
        self._test._captured_credentials = credentials
        return self

    def with_region(self, region):
        self._test._captured_region = region
        return self

    def with_http_config(self, config):
        return self

    def build(self):
        return self._test._fake_client


class TestSdkFallbackFix(unittest.TestCase):
    def setUp(self):
        self._captured_credentials = None
        self._captured_region = None
        self._fake_client = mock.Mock()
        self._fake_client.list_bare_metal_servers.return_value = _FakeSdkResponse(
            [_FakeSdkServer(SERVER_1), _FakeSdkServer(SERVER_2)], 2)
        try:
            import huaweicloudsdkbms.v1 as bms_v1
        except ImportError:
            self.skipTest("huaweicloudsdkbms not installed")
        self._builder_patch = mock.patch.object(
            bms_v1.BmsClient, "new_builder",
            classmethod(lambda cls: _FakeSdkBuilder(self)))
        self._builder_patch.start()
        self.addCleanup(self._builder_patch.stop)

    def _clean_credential_env(self):
        return {
            key: value for key, value in os.environ.items()
            if not key.upper().startswith(("HUAWEI", "HW_", "HWC"))
        }

    def test_official_sdk_imports_resolve(self):
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkbms.v1 import BmsClient, ListBareMetalServersRequest
        from huaweicloudsdkbms.v1.region.bms_region import BmsRegion
        for obj in (BasicCredentials, Region, HttpConfig,
                    BmsClient, ListBareMetalServersRequest, BmsRegion):
            self.assertTrue(callable(obj), obj)

    def test_sdk_fallback_returns_servers_with_env_credentials(self):
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak",
                   HUAWEI_SECRET_KEY="test-sk")
        with mock.patch.dict(os.environ, env, clear=True):
            servers = list_servers_via_sdk("cn-north-4")
        self.assertEqual(servers, [SERVER_1, SERVER_2])
        credentials = self._captured_credentials
        self.assertIsNotNone(credentials)
        self.assertEqual(getattr(credentials, "ak", None), "test-ak")
        self.assertEqual(getattr(credentials, "sk", None), "test-sk")
        self.assertEqual(getattr(self._captured_region, "id", None), "cn-north-4")

    def test_sdk_fallback_missing_env_credentials_raises_config(self):
        with mock.patch.dict(os.environ, self._clean_credential_env(),
                             clear=True):
            with self.assertRaises(ConfigError) as ctx:
                list_servers_via_sdk("cn-north-4")
        message = str(ctx.exception)
        self.assertIn("AK/SK", message)
        # Must not mislead the user into thinking the SDK is missing.
        self.assertNotIn("未安装", message)

    def test_sdk_fallback_alternative_env_prefixes(self):
        env = dict(self._clean_credential_env(),
                   HW_ACCESS_KEY="alt-ak", HW_SECRET_KEY="alt-sk")
        with mock.patch.dict(os.environ, env, clear=True):
            list_servers_via_sdk("cn-north-4")
        self.assertEqual(getattr(self._captured_credentials, "ak", None), "alt-ak")


class TestFilterByServerId(unittest.TestCase):
    def test_no_server_id_returns_all(self):
        result = filter_by_server_id([SERVER_1, SERVER_2], None)
        self.assertEqual(result, [SERVER_1, SERVER_2])

    def test_exact_match(self):
        self.assertEqual(filter_by_server_id([SERVER_1, SERVER_2], "bms-0001"), [SERVER_1])
        self.assertEqual(filter_by_server_id([SERVER_1, SERVER_2], "bms-0002"), [SERVER_2])

    def test_case_insensitive(self):
        self.assertEqual(filter_by_server_id([SERVER_1], "BMS-0001"), [SERVER_1])

    def test_no_match_returns_empty(self):
        self.assertEqual(filter_by_server_id([SERVER_1, SERVER_2], "bms-9999"), [])

    def test_missing_id_field_excluded(self):
        self.assertEqual(filter_by_server_id([{"name": "no-id"}], "bms-0001"), [])

    def test_input_not_mutated(self):
        source = [SERVER_1, SERVER_2]
        filter_by_server_id(source, "bms-0001")
        self.assertEqual(source, [SERVER_1, SERVER_2])


class TestNormalizeAndRender(unittest.TestCase):
    def test_normalize_flattens_flavor_image_az(self):
        flat = normalize_server(SERVER_1)
        self.assertEqual(flat["flavor_id"], "physical.s4.xlarge")
        self.assertEqual(flat["flavor_name"], "s4.xlarge")
        self.assertEqual(flat["image_id"], "img-1")
        self.assertEqual(flat["availability_zone"], "cn-north-4a")

    def test_normalize_missing_fields_dash(self):
        flat = normalize_server({"id": "bms-x"})
        self.assertEqual(flat["flavor_id"], "-")
        self.assertEqual(flat["flavor_name"], "-")
        self.assertEqual(flat["image_id"], "-")
        self.assertEqual(flat["availability_zone"], "-")

    def test_table_contains_basic_info(self):
        table = render_table([SERVER_1, SERVER_2])
        for fragment in ("bms-demo-01", "bms-0001", "ACTIVE", "s4.xlarge",
                         "cn-north-4a", "10.0.0.5", "bms-demo-02", "SHUTOFF", "tags"):
            self.assertIn(fragment, table)

    def test_names(self):
        self.assertEqual(server_names([SERVER_1, SERVER_2]),
                         ["bms-demo-01", "bms-demo-02"])

    def test_names_fallback_to_id(self):
        self.assertEqual(server_names([{"id": "bms-9"}]), ["bms-9"])


class TestMain(unittest.TestCase):
    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("list_bms.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            rc = main(argv)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    def test_table_output(self):
        rc, out, err = self._run(
            ["--region", "cn-north-4"],
            [(json.dumps({"servers": [SERVER_1, SERVER_2], "count": 2}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("裸金属服务器列表", out)
        self.assertIn("bms-demo-01", out)
        self.assertIn("ACTIVE", out)
        self.assertIn("s4.xlarge", out)
        self.assertEqual(err, "")

    def test_json_output(self):
        rc, out, err = self._run(
            ["--json"],
            [(json.dumps({"servers": [SERVER_1], "count": 1}), "", 0)])
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual(payload, [SERVER_1])

    def test_names_only_output(self):
        rc, out, err = self._run(
            ["--names-only"],
            [(json.dumps({"servers": [SERVER_1, SERVER_2], "count": 2}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("bms-demo-01", out)
        self.assertIn("bms-demo-02", out)
        self.assertNotIn("physical.s4.xlarge", out)

    def test_empty_servers_message(self):
        rc, out, err = self._run(
            ["--region", "cn-south-1"],
            [(json.dumps({"servers": [], "count": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("无裸金属服务器", out)
        self.assertIn("cn-south-1", out)

    def test_empty_with_filter_message(self):
        rc, out, _ = self._run(
            ["--status", "ACTIVE"],
            [(json.dumps({"servers": [], "count": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("status=ACTIVE", out)

    def test_server_id_filter_main_client_side(self):
        fake = FakeRunner([
            (json.dumps({"servers": [SERVER_1, SERVER_2], "count": 2}), "", 0)])
        with mock.patch("list_bms.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr"):
            rc = main(["--server-id", "bms-0001"])
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        self.assertEqual(rc, 0)
        self.assertIn("bms-demo-01", out)
        self.assertNotIn("bms-demo-02", out)
        for call in fake.calls:
            self.assertFalse(any("server-id" in part or "--id" in part for part in call))

    def test_status_reboot_allowed(self):
        # REBOOT is a read-only status enumerant despite containing "reboot".
        fake = FakeRunner([
            (json.dumps({"servers": [SERVER_1], "count": 1}), "", 0)])
        with mock.patch("list_bms.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr"):
            rc = main(["--status", "REBOOT"])
        self.assertEqual(rc, 0)
        self.assertTrue(any("--status=REBOOT" in part for part in fake.calls[0]))

    def test_empty_json_output(self):
        rc, out, err = self._run(
            ["--json"],
            [(json.dumps({"servers": [], "count": 0}), "", 0)])
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual(payload, [])

    def test_empty_names_only_output(self):
        rc, out, err = self._run(
            ["--names-only"],
            [(json.dumps({"servers": [], "count": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("共 0 个", out)
        self.assertNotIn("无裸金属服务器", out)

    def test_auth_error_message(self):
        rc, out, err = self._run([], [("", "403 Forbidden", 1)])
        self.assertEqual(rc, 1)
        self.assertIn("[错误]", err)
        self.assertIn("IAM", err)

    def test_missing_ak_sk_error_message(self):
        rc, out, err = self._run([], [("", "ERROR: cli-ak empty", 1)])
        self.assertEqual(rc, 1)
        self.assertIn("AK/SK", err)

    def test_hcloud_not_installed(self):
        with mock.patch("list_bms.list_servers_via_sdk",
                        side_effect=ConfigError("huaweicloudsdkbms 未安装")):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 1)
        self.assertIn("未安装", err)

    def test_hcloud_missing_falls_back_to_sdk(self):
        with mock.patch("list_bms.list_servers_via_sdk",
                        return_value=[SERVER_1]):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 0)
        self.assertIn("bms-demo-01", out)

    def test_write_intent_argv_blocked(self):
        rc, out, err = self._run(["--operation", "DeleteBareMetalServer"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)

    def test_write_keyword_argv_blocked(self):
        rc, out, err = self._run(["--name", "reboot-me"], [])
        self.assertEqual(rc, 1)
        self.assertIn("守卫拦截", err)

    def test_write_intent_via_other_option_value_blocked(self):
        # A mutating intent in a non-status option value is still caught.
        rc, out, err = self._run(["--server-id", "delete-me"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)


class TestMarkdownReport(unittest.TestCase):
    """render_markdown / naming helpers (offline, no file system)."""

    def test_render_contains_region_time_total_and_table(self):
        md = render_markdown("cn-north-4", [SERVER_1, SERVER_2],
                             datetime.datetime(2026, 10, 20, 9, 30, 0))
        self.assertIn("# Huawei Cloud BMS 裸金属服务器清单", md)
        self.assertIn("**Region**: cn-north-4", md)
        self.assertIn("**查询时间**: 2026-10-20 09:30:00", md)
        self.assertIn("**主机总数**: 2", md)
        self.assertIn("| 名称 | ID |", md)
        self.assertIn("| --- | --- |", md)
        self.assertIn("| bms-demo-01 | bms-0001 |", md)
        self.assertIn("| bms-demo-02 | bms-0002 |", md)

    def test_render_generated_at_defaults_to_now(self):
        md = render_markdown("cn-north-4", [SERVER_1])
        self.assertRegex(md, r"\*\*查询时间\*\*: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")

    def test_render_name_falls_back_to_id(self):
        md = render_markdown("cn-north-4", [{"id": "bms-9"}],
                             datetime.datetime(2026, 10, 20))
        self.assertIn("| bms-9 | bms-9 |", md)

    def test_render_empty_list_message_and_filters(self):
        md = render_markdown("cn-south-1", [], datetime.datetime(2026, 10, 20),
                             filters=["status=ACTIVE", "name=bms-01",
                                      "server_id=bms-0001"])
        self.assertIn("**主机总数**: 0", md)
        self.assertIn("共 0 个裸金属服务器", md)
        self.assertIn("status=ACTIVE, name=bms-01, server_id=bms-0001", md)
        self.assertNotIn("| 名称", md)

    def test_render_empty_list_without_filters(self):
        md = render_markdown("cn-south-1", [], datetime.datetime(2026, 10, 20))
        self.assertIn("共 0 个裸金属服务器", md)
        self.assertNotIn("过滤条件", md)

    def test_render_escapes_pipes_and_newlines(self):
        md = render_markdown("cn-north-4", [{"id": "bms|1", "name": "web\n01"}],
                             datetime.datetime(2026, 10, 20))
        self.assertIn("| web 01 | bms\\|1 |", md)

    def test_render_fixed_column_header(self):
        # The inventory table must carry the fixed name/ID/status/flavor/AZ/IP set.
        md = render_markdown("cn-north-4", [SERVER_1, SERVER_2],
                             datetime.datetime(2026, 10, 20))
        header = "| %s |" % " | ".join(label for _, label in MD_TABLE_COLUMNS)
        self.assertIn(header, md)
        self.assertIn("| --- | --- | --- | --- | --- | --- |", md)
        labels = [label for _, label in MD_TABLE_COLUMNS]
        for expected in ("名称", "ID", "状态", "规格", "可用区", "IP"):
            self.assertIn(expected, labels)

    def test_render_fixed_column_rows(self):
        md = render_markdown("cn-north-4", [SERVER_1, SERVER_2],
                             datetime.datetime(2026, 10, 20))
        self.assertIn(
            "| bms-demo-01 | bms-0001 | ACTIVE | s4.xlarge | cn-north-4a | "
            "10.0.0.5 |", md)
        self.assertIn(
            "| bms-demo-02 | bms-0002 | SHUTOFF | s3.large | cn-north-4b | "
            "10.0.0.6 |", md)

    def test_render_missing_columns_render_dash(self):
        md = render_markdown("cn-north-4", [{"id": "bms-9"}],
                             datetime.datetime(2026, 10, 20))
        self.assertIn("| bms-9 | bms-9 | - | - | - | - |", md)

    def test_render_normalizes_flavor_and_az_keys(self):
        # flavor_name / availability_zone are produced by normalize_server.
        md = render_markdown("cn-north-4", [SERVER_1],
                             datetime.datetime(2026, 10, 20))
        self.assertIn("s4.xlarge", md)
        self.assertIn("cn-north-4a", md)

    def test_default_name_uses_region_and_date(self):
        self.assertEqual(
            default_markdown_name("cn-north-4",
                                  datetime.datetime(2026, 10, 20, 23, 59)),
            "bms-list-cn-north-4-20261020.md")
        self.assertEqual(
            default_markdown_name("cn-south-1", datetime.datetime(2026, 1, 2)),
            "bms-list-cn-south-1-20260102.md")

    def test_format_query_time(self):
        self.assertEqual(
            format_query_time(datetime.datetime(2026, 1, 2, 3, 4, 5)),
            "2026-01-02 03:04:05")
        self.assertRegex(format_query_time(), r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")

    def test_active_filter_descriptions(self):
        self.assertEqual(
            active_filter_descriptions("ACTIVE", "bms-01", "bms-0001"),
            ["status=ACTIVE", "name=bms-01", "server_id=bms-0001"])
        self.assertEqual(active_filter_descriptions(status="ACTIVE"),
                         ["status=ACTIVE"])
        self.assertEqual(active_filter_descriptions(), [])


class TestMarkdownFileWrite(unittest.TestCase):
    """write_markdown_file: UTF-8, atomic, no half file on failure."""

    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="bms-md-write-")
        self.addCleanup(shutil.rmtree, self.dir, ignore_errors=True)

    def test_writes_utf8_and_returns_absolute_path(self):
        target = os.path.join(self.dir, "out.md")
        path = write_markdown_file(target, "# 裸金属服务器清单\ntext\n")
        self.assertEqual(path, os.path.abspath(target))
        with open(path, encoding="utf-8") as handle:
            self.assertEqual(handle.read(), "# 裸金属服务器清单\ntext\n")
        # No temporary sibling left behind.
        self.assertEqual(os.listdir(self.dir), ["out.md"])

    def test_overwrites_existing_report(self):
        target = os.path.join(self.dir, "out.md")
        write_markdown_file(target, "old")
        write_markdown_file(target, "new")
        with open(target, encoding="utf-8") as handle:
            self.assertEqual(handle.read(), "new")

    def test_missing_directory_raises_and_leaves_nothing(self):
        target = os.path.join(self.dir, "nope", "out.md")
        with self.assertRaises(OutputError) as ctx:
            write_markdown_file(target, "x")
        self.assertIn("无法写入 Markdown 文件", str(ctx.exception))
        self.assertFalse(os.path.exists(target))
        self.assertFalse(os.path.exists(os.path.dirname(target)))
        self.assertEqual(os.listdir(self.dir), [])

    def test_unwritable_target_raises_and_leaves_no_temp(self):
        # A directory as the target makes the final move fail everywhere
        # (root included, unlike a chmod-based permission test).
        target = os.path.join(self.dir, "target-dir")
        os.mkdir(target)
        with self.assertRaises(OutputError) as ctx:
            write_markdown_file(target, "x")
        self.assertIn("无法写入 Markdown 文件", str(ctx.exception))
        self.assertTrue(os.path.isdir(target))
        self.assertEqual(os.listdir(self.dir), ["target-dir"])


class TestMainMarkdownOutput(unittest.TestCase):
    """`main()` end-to-end for --md-file / --output-md (mocked hcloud)."""

    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="bms-md-main-")
        self.addCleanup(shutil.rmtree, self.dir, ignore_errors=True)
        self._cwd = os.getcwd()
        self.addCleanup(os.chdir, self._cwd)
        os.chdir(self.dir)

    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("list_bms.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            rc = main(argv)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    @staticmethod
    def _page(servers):
        return [(json.dumps({"servers": servers, "count": len(servers)}), "", 0)]

    @staticmethod
    def _read(path):
        with open(path, encoding="utf-8") as handle:
            return handle.read()

    def test_explicit_path_creates_report_and_hints_absolute_path(self):
        target = os.path.join(self.dir, "inventory.md")
        rc, out, err = self._run(
            ["--md-file", target], self._page([SERVER_1, SERVER_2]))
        self.assertEqual(rc, 0)
        self.assertEqual(err, "")
        self.assertTrue(os.path.isfile(target))
        content = self._read(target)
        full_header = "| %s |" % " | ".join(label for _, label in MD_TABLE_COLUMNS)
        for fragment in ("**Region**: cn-north-4", "**查询时间**:",
                         "**主机总数**: 2", full_header,
                         "| bms-demo-01 | bms-0001 | ACTIVE | s4.xlarge | "
                         "cn-north-4a | 10.0.0.5 |"):
            self.assertIn(fragment, content)
        self.assertIn(os.path.abspath(target), out)
        # The default stdout table is still printed (additive, not exclusive).
        self.assertIn("裸金属服务器列表", out)

    def test_no_value_uses_default_file_name(self):
        rc, out, err = self._run(["--md-file"], self._page([SERVER_1]))
        self.assertEqual(rc, 0)
        expected = "bms-list-cn-north-4-%s.md" % datetime.date.today().strftime("%Y%m%d")
        self.assertEqual(os.listdir(self.dir), [expected])
        self.assertIn(os.path.abspath(expected), out)
        self.assertIn("| bms-demo-01 | bms-0001 |", self._read(expected))

    def test_no_value_uses_requested_region_in_default_name(self):
        rc, out, err = self._run(["-r", "cn-south-1", "--md-file"],
                                 self._page([SERVER_1]))
        self.assertEqual(rc, 0)
        expected = "bms-list-cn-south-1-%s.md" % datetime.date.today().strftime("%Y%m%d")
        self.assertEqual(os.listdir(self.dir), [expected])
        self.assertIn("**Region**: cn-south-1", self._read(expected))

    def test_output_md_alias(self):
        rc, out, err = self._run(["--output-md", "alias.md"],
                                 self._page([SERVER_1]))
        self.assertEqual(rc, 0)
        self.assertTrue(os.path.isfile(os.path.join(self.dir, "alias.md")))

    def test_path_with_write_words_not_blocked(self):
        rc, out, err = self._run(["--md-file=bms-delete-report.md"],
                                 self._page([SERVER_1]))
        self.assertEqual(rc, 0)
        self.assertNotIn("写操作意图", err)
        self.assertTrue(
            os.path.isfile(os.path.join(self.dir, "bms-delete-report.md")))

    def test_empty_list_report_exits_zero(self):
        rc, out, err = self._run(["--status", "ACTIVE", "--md-file", "empty.md"],
                                 self._page([]))
        self.assertEqual(rc, 0)
        self.assertEqual(err, "")
        content = self._read(os.path.join(self.dir, "empty.md"))
        self.assertIn("共 0 个裸金属服务器", content)
        self.assertIn("status=ACTIVE", content)
        self.assertIn("**主机总数**: 0", content)
        # stdout behaviour for an empty list is unchanged.
        self.assertIn("无裸金属服务器", out)

    def test_empty_list_with_filter_in_message(self):
        rc, out, err = self._run(
            ["--status", "ACTIVE", "--server-id", "bms-0001"],
            self._page([]))
        self.assertEqual(rc, 0)
        self.assertIn("status=ACTIVE", out)
        self.assertIn("server_id=bms-0001", out)

    def test_write_failure_reports_error_and_exits_one(self):
        target = os.path.join(self.dir, "absent-dir", "out.md")
        rc, out, err = self._run(["--md-file", target], self._page([SERVER_1]))
        self.assertEqual(rc, 1)
        self.assertIn("[错误]", err)
        self.assertIn("无法写入 Markdown 文件", err)
        self.assertFalse(os.path.exists(target))
        self.assertFalse(os.path.exists(os.path.dirname(target)))
        # No half file / temp sibling anywhere.
        self.assertEqual(os.listdir(self.dir), [])

    def test_json_mode_unchanged_and_no_file_without_flag(self):
        rc, out, err = self._run(["--json"], self._page([SERVER_1]))
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out), [SERVER_1])
        self.assertEqual(os.listdir(self.dir), [])

    def test_names_only_md_is_additive(self):
        rc, out, err = self._run(["--names-only", "--md-file", "inv.md"],
                                 self._page([SERVER_1, SERVER_2]))
        self.assertEqual(rc, 0)
        self.assertIn("bms-demo-01", out)
        self.assertNotIn("physical.s4.xlarge", out)
        self.assertIn("| bms-demo-02 | bms-0002 |",
                      self._read(os.path.join(self.dir, "inv.md")))

    def test_md_written_before_write_intent_still_blocked(self):
        rc, out, err = self._run(["--md-file", "out.md", "--operation",
                                  "DeleteBareMetalServer"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)
        self.assertEqual(os.listdir(self.dir), [])

    def test_mutating_flag_after_md_file_still_blocked(self):
        rc, out, err = self._run(["--md-file", "--names-only",
                                  "--operation", "DeleteBareMetalServer"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)
        self.assertEqual(os.listdir(self.dir), [])


class TestErrorHierarchy(unittest.TestCase):
    def test_subclasses(self):
        for exc in (GuardError, ConfigError, AuthError, ApiError, OutputError):
            self.assertTrue(issubclass(exc, BmsListError))


if __name__ == "__main__":
    unittest.main()
