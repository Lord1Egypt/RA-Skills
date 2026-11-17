import json
import os
import subprocess
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from list_cc import (  # noqa: E402
    ALLOWED_OPERATION,
    ApiError,
    AuthError,
    ConfigError,
    GuardError,
    CcListError,
    build_command,
    classify_hcloud_failure,
    connection_names,
    extract_connections,
    extract_json,
    guard_operation,
    guard_write_intent,
    list_connections,
    list_connections_via_sdk,
    main,
    normalize_connection,
    render_table,
)

CONNECTION_1 = {
    "id": "cc-0001",
    "name": "cc-demo-01",
    "status": "ACTIVE",
    "used_scene": "VPC",
    "network_instance_number": 2,
    "bandwidth_package_number": 1,
    "inter_region_bandwidth_number": 0,
    "admin_state_up": True,
    "enterprise_project_id": "0",
    "domain_id": "123456789",
    "tags": [{"key": "env", "value": "test"}],
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-02T00:00:00",
}
CONNECTION_2 = {
    "id": "cc-0002",
    "name": "cc-demo-02",
    "status": "ACTIVE",
    "used_scene": "VPC",
    "network_instance_number": 0,
    "bandwidth_package_number": 0,
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
        self.assertFalse(guard_write_intent("--region cn-north-4 --json list cloud connections"))
        self.assertFalse(guard_write_intent("show connection details routes"))

    def test_create_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("CreateCloudConnection cc-new")

    def test_delete_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--operation DeleteCloudConnection")

    def test_mutating_verbs_blocked(self):
        for text in ("associate bandwidth package", "disassociate bandwidth",
                     "detach network instance", "restart cc-01",
                     "update connection name", "modify connection"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_normalized_separators_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--create-connection")
        with self.assertRaises(GuardError):
            guard_write_intent("update_connection_name")

    def test_read_filter_value_passes(self):
        self.assertFalse(guard_write_intent("--status ACTIVE"))
        self.assertFalse(guard_write_intent("--used-scene VPC"))

    def test_operation_guard_rejects_non_list(self):
        with self.assertRaises(GuardError):
            guard_operation("ShowCloudConnection")
        self.assertTrue(guard_operation(ALLOWED_OPERATION))


class TestBuildCommand(unittest.TestCase):
    def test_basic(self):
        argv = build_command("cn-north-4")
        self.assertEqual(argv[0], "CC")
        self.assertEqual(argv[1], "ListCloudConnections")
        self.assertIn("--cli-region=cn-north-4", argv)
        self.assertIn("--limit=100", argv)
        self.assertFalse(any(flag.startswith("--marker") for flag in argv))

    def test_marker_appended(self):
        argv = build_command("cn-north-4", marker="tok-123", limit=10)
        self.assertIn("--marker=tok-123", argv)
        self.assertIn("--limit=10", argv)

    def test_filters_forwarded_server_side(self):
        argv = build_command("cn-south-1", name="cc-01", status="ACTIVE",
                             connection_id="cc-9", limit=10)
        self.assertIn("--name=cc-01", argv)
        self.assertIn("--status=ACTIVE", argv)
        self.assertIn("--id=cc-9", argv)
        self.assertIn("--limit=10", argv)

    def test_no_write_flags_ever_added(self):
        argv = build_command("cn-north-4", status="ACTIVE")
        for flag in argv:
            self.assertFalse(flag.lower().lstrip("-").startswith(
                ("create", "delete", "update", "associate", "detach")))


class TestExtract(unittest.TestCase):
    def test_extract_json_plain(self):
        data = extract_json(json.dumps({"cloud_connections": []}))
        self.assertEqual(data, {"cloud_connections": []})

    def test_extract_json_with_noise(self):
        data = extract_json("WARNING some noise\n{\"a\": 1}\n")
        self.assertEqual(data, {"a": 1})

    def test_extract_json_invalid(self):
        with self.assertRaises(ApiError):
            extract_json("<html>not json</html>")

    def test_extract_connections_known_keys(self):
        for key in ("cloud_connections", "cloudConnections"):
            self.assertEqual(extract_connections({key: [CONNECTION_1]}), [CONNECTION_1])
        self.assertEqual(extract_connections([CONNECTION_1]), [CONNECTION_1])
        self.assertEqual(extract_connections({"page_info": {}}), [])


class TestClassifyFailure(unittest.TestCase):
    def test_missing_credentials(self):
        err = classify_hcloud_failure(
            "", "ERROR: cli-ak is empty, please run hcloud configure", 1)
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
            "[USE_ERROR]Invalid parameter: status\n\n"
            "Run `hcloud CC ListCloudConnections --help` for details.", "", 0)
        self.assertIsInstance(err, ApiError)
        self.assertIn("参数错误", str(err))
        self.assertIn("--help", str(err))


class TestListConnections(unittest.TestCase):
    def test_single_page(self):
        fake = FakeRunner([(
            json.dumps({"cloud_connections": [CONNECTION_1, CONNECTION_2]}), "", 0)])
        with mock.patch("list_cc.subprocess.run", fake):
            connections = list_connections("cn-north-4")
        self.assertEqual(connections, [CONNECTION_1, CONNECTION_2])
        self.assertEqual(len(fake.calls), 1)

    def test_pagination_via_next_marker(self):
        page1 = {"cloud_connections": [CONNECTION_1],
                 "page_info": {"next_marker": "tok-2", "current_count": 1}}
        page2 = {"cloud_connections": [CONNECTION_2],
                 "page_info": {"next_marker": None, "current_count": 1}}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("list_cc.subprocess.run", fake):
            connections = list_connections("cn-north-4", limit=1)
        self.assertEqual(connections, [CONNECTION_1, CONNECTION_2])
        self.assertEqual(len(fake.calls), 2)
        self.assertIn("--marker=tok-2", fake.calls[1])

    def test_pagination_via_full_page_without_marker(self):
        page1 = {"cloud_connections": [CONNECTION_1]}
        page2 = {"cloud_connections": []}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("list_cc.subprocess.run", fake):
            connections = list_connections("cn-north-4", limit=1)
        self.assertEqual(connections, [CONNECTION_1])

    def test_empty_region(self):
        fake = FakeRunner([(json.dumps({"cloud_connections": []}), "", 0)])
        with mock.patch("list_cc.subprocess.run", fake):
            connections = list_connections("cn-north-4")
        self.assertEqual(connections, [])

    def test_filters_forwarded_to_cli(self):
        fake = FakeRunner([(
            json.dumps({"cloud_connections": [CONNECTION_1]}), "", 0)])
        with mock.patch("list_cc.subprocess.run", fake):
            list_connections("cn-north-4", status="ACTIVE", name="cc-demo-01",
                             connection_id="cc-0001")
        call = fake.calls[0]
        self.assertTrue(any("--status=ACTIVE" in part for part in call))
        self.assertTrue(any("--name=cc-demo-01" in part for part in call))
        self.assertTrue(any("--id=cc-0001" in part for part in call))

    def test_use_error_rc0_raises_api_error(self):
        fake = FakeRunner([(
            "[USE_ERROR]Invalid parameter: status\n\n"
            "Run `hcloud CC ListCloudConnections --help` for details.", "", 0)])
        with mock.patch("list_cc.subprocess.run", fake):
            with self.assertRaises(ApiError) as ctx:
                list_connections("cn-north-4")
        self.assertIn("参数错误", str(ctx.exception))

    def test_nonzero_exit_403(self):
        fake = FakeRunner([("", "403 Forbidden", 1)])
        with mock.patch("list_cc.subprocess.run", fake):
            with self.assertRaises(AuthError):
                list_connections("cn-north-4")

    def test_nonzero_exit_credentials(self):
        fake = FakeRunner([("", "ERROR: no AK configured", 1)])
        with mock.patch("list_cc.subprocess.run", fake):
            with self.assertRaises(ConfigError):
                list_connections("cn-north-4")

    def test_timeout(self):
        fake = FakeRunner([subprocess.TimeoutExpired(cmd="hcloud", timeout=120)])
        with mock.patch("list_cc.subprocess.run", fake):
            with self.assertRaises(ApiError):
                list_connections("cn-north-4")

    def test_sdk_fallback_when_hcloud_missing(self):
        with mock.patch("list_cc.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_cc.list_connections_via_sdk",
                           return_value=[CONNECTION_1, CONNECTION_2]) as sdk_mock:
            connections = list_connections("cn-north-4", status="ACTIVE",
                                           name="cc-demo", connection_id="cc-1")
        self.assertEqual(connections, [CONNECTION_1, CONNECTION_2])
        self.assertEqual(sdk_mock.call_args.kwargs.get("status"), "ACTIVE")

    def test_sdk_fallback_unavailable_raises_config(self):
        with mock.patch("list_cc.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_cc.list_connections_via_sdk",
                           side_effect=ConfigError("huaweicloudsdkcc 未安装")):
            with self.assertRaises(ConfigError):
                list_connections("cn-north-4")

    def test_sdk_request_signature(self):
        # Regression guard: the real huaweicloudsdkcc ListCloudConnectionsRequest
        # must be constructible with exactly the kwargs the fallback path sends.
        try:
            from huaweicloudsdkcc.v3 import ListCloudConnectionsRequest
        except ImportError:
            self.skipTest("huaweicloudsdkcc not installed")
        request = ListCloudConnectionsRequest(
            limit=100, marker=None, id=["cc-9"], name=["cc-01"], status=["ACTIVE"],
        )
        self.assertEqual(request.name, ["cc-01"])
        self.assertEqual(request.status, ["ACTIVE"])
        self.assertEqual(request.id, ["cc-9"])
        with self.assertRaises(TypeError):
            ListCloudConnectionsRequest(no_such_param=1)


class _FakeSdkResponse:
    def __init__(self, connections, next_marker):
        self.cloud_connections = connections

        class _PageInfo:
            pass

        page = _PageInfo()
        page.next_marker = next_marker
        self.page_info = page


class _FakeSdkConnection:
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


class TestSdkFallback(unittest.TestCase):
    """P2 regression: the SDK fallback must use modules that exist in the
    official huaweicloudsdkcc package and wire credentials from environment
    variables (BasicCredentials has no env auto-discovery)."""

    def setUp(self):
        self._captured_credentials = None
        self._captured_region = None
        self._fake_client = mock.Mock()
        self._fake_client.list_cloud_connections.return_value = _FakeSdkResponse(
            [_FakeSdkConnection(CONNECTION_1), _FakeSdkConnection(CONNECTION_2)], None)
        try:
            import huaweicloudsdkcc.v3 as cc_v3
        except ImportError:
            self.skipTest("huaweicloudsdkcc not installed")
        self._builder_patch = mock.patch.object(
            cc_v3.CcClient, "new_builder",
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
        from huaweicloudsdkcc.v3 import CcClient, ListCloudConnectionsRequest
        from huaweicloudsdkcc.v3.region.cc_region import CcRegion
        for obj in (BasicCredentials, Region, HttpConfig,
                    CcClient, ListCloudConnectionsRequest, CcRegion):
            self.assertTrue(callable(obj), obj)

    def test_sdk_fallback_returns_connections_with_env_credentials(self):
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak",
                   HUAWEI_SECRET_KEY="test-sk")
        with mock.patch.dict(os.environ, env, clear=True):
            connections = list_connections_via_sdk("cn-north-4")
        self.assertEqual(connections, [CONNECTION_1, CONNECTION_2])
        credentials = self._captured_credentials
        self.assertIsNotNone(credentials)
        self.assertEqual(getattr(credentials, "ak", None), "test-ak")
        self.assertEqual(getattr(credentials, "sk", None), "test-sk")
        self.assertEqual(getattr(self._captured_region, "id", None), "cn-north-4")

    def test_sdk_fallback_missing_env_credentials_raises_config(self):
        with mock.patch.dict(os.environ, self._clean_credential_env(), clear=True):
            with self.assertRaises(ConfigError) as ctx:
                list_connections_via_sdk("cn-north-4")
        message = str(ctx.exception)
        self.assertIn("AK/SK", message)
        self.assertNotIn("未安装", message)

    def test_sdk_pagination_via_next_marker(self):
        first = _FakeSdkResponse([_FakeSdkConnection(CONNECTION_1)], "tok-2")
        second = _FakeSdkResponse([_FakeSdkConnection(CONNECTION_2)], None)
        self._fake_client.list_cloud_connections.side_effect = [first, second]
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak", HUAWEI_SECRET_KEY="test-sk")
        with mock.patch.dict(os.environ, env, clear=True):
            connections = list_connections_via_sdk("cn-north-4")
        self.assertEqual(connections, [CONNECTION_1, CONNECTION_2])
        second_request = self._fake_client.list_cloud_connections.call_args_list[1][0][0]
        self.assertEqual(second_request.marker, "tok-2")


class TestNormalizeAndRender(unittest.TestCase):
    def test_normalize_flattens_tags(self):
        flat = normalize_connection(CONNECTION_1)
        self.assertEqual(flat["tags"], "env=test")

    def test_normalize_missing_tags_dash(self):
        flat = normalize_connection(CONNECTION_2)
        self.assertEqual(flat["tags"], "-")

    def test_table_contains_basic_info(self):
        table = render_table([CONNECTION_1, CONNECTION_2])
        for fragment in ("cc-demo-01", "cc-0001", "ACTIVE", "VPC", "2", "1",
                         "enterprise_project_id", "env=test"):
            self.assertIn(fragment, table)

    def test_names(self):
        self.assertEqual(
            connection_names([CONNECTION_1, CONNECTION_2]), ["cc-demo-01", "cc-demo-02"])

    def test_names_fallback_to_id(self):
        self.assertEqual(connection_names([{"id": "cc-9"}]), ["cc-9"])


class TestMain(unittest.TestCase):
    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("list_cc.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            rc = main(argv)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    def test_table_output(self):
        rc, out, err = self._run(
            ["--region", "cn-north-4"],
            [(json.dumps({"cloud_connections": [CONNECTION_1, CONNECTION_2]}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("云连接（CC）实例列表", out)
        self.assertIn("cc-demo-01", out)
        self.assertIn("ACTIVE", out)
        self.assertEqual(err, "")

    def test_json_output(self):
        rc, out, err = self._run(
            ["--json"],
            [(json.dumps({"cloud_connections": [CONNECTION_1]}), "", 0)])
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual(payload, [CONNECTION_1])

    def test_names_only_output(self):
        rc, out, err = self._run(
            ["--names-only"],
            [(json.dumps({"cloud_connections": [CONNECTION_1, CONNECTION_2]}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("cc-demo-01", out)
        self.assertIn("cc-demo-02", out)
        self.assertNotIn("bandwidth_package_number", out)

    def test_empty_instances_message(self):
        rc, out, err = self._run(
            ["--region", "cn-south-1"],
            [(json.dumps({"cloud_connections": []}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("无云连接（CC）实例", out)
        self.assertIn("cn-south-1", out)

    def test_empty_with_filter_message(self):
        rc, out, _ = self._run(
            ["--status", "ACTIVE"],
            [(json.dumps({"cloud_connections": []}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("status=ACTIVE", out)

    def test_status_filter_main_forwarded(self):
        fake = FakeRunner([
            (json.dumps({"cloud_connections": [CONNECTION_1]}), "", 0)])
        with mock.patch("list_cc.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr"):
            rc = main(["--status", "ACTIVE"])
        self.assertEqual(rc, 0)
        self.assertTrue(any("--status=ACTIVE" in part for part in fake.calls[0]))

    def test_empty_json_output(self):
        rc, out, err = self._run(
            ["--json"],
            [(json.dumps({"cloud_connections": []}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out), [])

    def test_empty_names_only_output(self):
        rc, out, err = self._run(
            ["--names-only"],
            [(json.dumps({"cloud_connections": []}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("共 0 个", out)
        self.assertNotIn("无云连接（CC）实例", out)

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
        with mock.patch("list_cc.list_connections_via_sdk",
                        side_effect=ConfigError("huaweicloudsdkcc 未安装")):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 1)
        self.assertIn("未安装", err)

    def test_hcloud_missing_falls_back_to_sdk(self):
        with mock.patch("list_cc.list_connections_via_sdk",
                        return_value=[CONNECTION_1]):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 0)
        self.assertIn("cc-demo-01", out)

    def test_write_intent_argv_blocked(self):
        rc, out, err = self._run(["--operation", "DeleteCloudConnection"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)

    def test_write_keyword_argv_blocked(self):
        rc, out, err = self._run(["--name", "detach-me"], [])
        self.assertEqual(rc, 1)
        self.assertIn("守卫拦截", err)

    def test_status_write_word_blocked(self):
        rc, out, err = self._run(["--status", "deleting-now"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)


class TestErrorHierarchy(unittest.TestCase):
    def test_subclasses(self):
        for exc in (GuardError, ConfigError, AuthError, ApiError):
            self.assertTrue(issubclass(exc, CcListError))


if __name__ == "__main__":
    unittest.main()
