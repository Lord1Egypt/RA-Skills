import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from list_vpc import (  # noqa: E402
    ALLOWED_OPERATION,
    MD_HEADERS,
    PEERING_OPERATION,
    ApiError,
    AuthError,
    ConfigError,
    ExportError,
    GuardError,
    VpcListError,
    build_command,
    build_peering_command,
    classify_hcloud_failure,
    default_output_path,
    export_markdown,
    extract_json,
    extract_peerings,
    extract_vpcs,
    guard_operation,
    guard_text_from_argv,
    guard_write_intent,
    list_peerings,
    list_peerings_via_sdk,
    list_vpcs,
    list_vpcs_via_sdk,
    main,
    normalize_peering,
    normalize_vpc,
    normalized_row,
    peering_names,
    render_markdown,
    render_peering_table,
    render_table,
    vpc_names,
)

VPC_1 = {
    "id": "vpc-0001",
    "name": "vpc-demo-01",
    "cidr": "192.168.0.0/16",
    "status": "OK",
    "description": "demo vpc",
    "routes": [
        {"destination": "0.0.0.0/0", "nexthop": "10.0.0.1"},
    ],
    "enterprise_project_id": "0",
    "tenant_id": "tenant-0001",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-02T00:00:00",
    "block_service_endpoint_states": "off",
    "enable_network_address_usage_metrics": False,
}
VPC_2 = {
    "id": "vpc-0002",
    "name": "vpc-demo-02",
    "cidr": "10.0.0.0/8",
    "status": "CREATING",
    "routes": [],
    "enterprise_project_id": "0",
    "tenant_id": "tenant-0001",
}
PEERING_1 = {
    "id": "peering-0001",
    "name": "peering-a-to-b",
    "status": "ACTIVE",
    "request_vpc_info": {"vpc_id": "vpc-0001", "tenant_id": "tenant-0001"},
    "accept_vpc_info": {"vpc_id": "vpc-0002", "tenant_id": "tenant-0001"},
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-02T00:00:00",
}
PEERING_2 = {
    "id": "peering-0002",
    "name": "peering-c-to-d",
    "status": "PENDING_ACCEPTANCE",
    "request_vpc_info": {"vpc_id": "vpc-0003"},
    "accept_vpc_info": {"vpc_id": "vpc-0004"},
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
        self.assertFalse(guard_write_intent("--region cn-north-4 --json list vpcs"))
        self.assertFalse(guard_write_intent("show vpc details"))

    def test_create_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("CreateVpc vpc-new")

    def test_delete_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--operation DeleteVpc")

    def test_mutating_verbs_blocked(self):
        for text in ("associate route", "disassociate port",
                     "detach subnet from vpc", "release vpc-01",
                     "update vpc name", "bind bandwidth"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_normalized_separators_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--create-vpc")
        with self.assertRaises(GuardError):
            guard_write_intent("delete_subnet_route")

    def test_read_filter_value_passes(self):
        self.assertFalse(guard_write_intent("--id 1234abcd-0000-0000-0000-000000000000"))
        self.assertFalse(guard_write_intent("--enterprise-project-id 0"))

    def test_operation_guard_rejects_non_list(self):
        with self.assertRaises(GuardError):
            guard_operation("ShowVpc")
        self.assertTrue(guard_operation(ALLOWED_OPERATION))

    def test_guard_text_strips_output_value(self):
        text = guard_text_from_argv(
            ["--format", "md", "--output", "/tmp/vpc-delete-report.md"])
        self.assertNotIn("delete", text)
        self.assertFalse(guard_write_intent(text))

    def test_guard_text_strips_equals_form(self):
        text = guard_text_from_argv(["--output=/tmp/vpc-delete.md", "-f=md"])
        self.assertNotIn("delete", text)
        self.assertFalse(guard_write_intent(text))

    def test_guard_text_keeps_filter_values_scanned(self):
        text = guard_text_from_argv(["--id", "release-me"])
        with self.assertRaises(GuardError):
            guard_write_intent(text)

    def test_guard_text_still_scans_following_flag(self):
        text = guard_text_from_argv(
            ["--output", "/tmp/report.md", "--operation", "DeleteVpc"])
        with self.assertRaises(GuardError):
            guard_write_intent(text)


class TestBuildCommand(unittest.TestCase):
    def test_basic(self):
        argv = build_command("cn-north-4")
        self.assertEqual(argv[0], "VPC")
        self.assertEqual(argv[1], "ListVpcs")
        self.assertIn("--cli-region=cn-north-4", argv)
        self.assertIn("--limit=100", argv)
        self.assertFalse(any(flag.startswith("--marker") for flag in argv))

    def test_marker_appended(self):
        argv = build_command("cn-north-4", marker="tok-123", limit=10)
        self.assertIn("--marker=tok-123", argv)
        self.assertIn("--limit=10", argv)

    def test_filters_forwarded_server_side(self):
        argv = build_command("cn-south-1", vpc_id="vpc-9",
                             enterprise_project_id="0", limit=10)
        self.assertIn("--id.1=vpc-9", argv)
        self.assertIn("--enterprise_project_id=0", argv)
        self.assertIn("--limit=10", argv)

    def test_id_uses_indexed_array_form(self):
        # VPC ListVpcs v3 declares id as array<string>; KooCLI rejects a bare
        # --id with "[USE_ERROR]Invalid parameter: id".
        argv = build_command("cn-north-4", vpc_id="vpc-0001")
        self.assertIn("--id.1=vpc-0001", argv)
        self.assertNotIn("--id=vpc-0001", argv)
        self.assertFalse(any(a == "--id" or a.startswith("--id=") for a in argv))

    def test_no_write_flags_ever_added(self):
        argv = build_command("cn-north-4", enterprise_project_id="0")
        for flag in argv:
            self.assertFalse(flag.lower().lstrip("-").startswith(
                ("create", "delete", "update", "associate", "release")))


class TestExtract(unittest.TestCase):
    def test_extract_json_plain(self):
        data = extract_json(json.dumps({"vpcs": []}))
        self.assertEqual(data, {"vpcs": []})

    def test_extract_json_with_noise(self):
        data = extract_json("WARNING some noise\n{\"a\": 1}\n")
        self.assertEqual(data, {"a": 1})

    def test_extract_json_invalid(self):
        with self.assertRaises(ApiError):
            extract_json("<html>not json</html>")

    def test_extract_vpcs_known_keys(self):
        for key in ("vpcs", "vpc"):
            self.assertEqual(extract_vpcs({key: [VPC_1]}), [VPC_1])
        self.assertEqual(extract_vpcs([VPC_1]), [VPC_1])
        self.assertEqual(extract_vpcs({"page_info": {}}), [])


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
            "[USE_ERROR]Invalid parameter: enterprise_project_id\n\n"
            "Run `hcloud VPC ListVpcs --help` for details.", "", 0)
        self.assertIsInstance(err, ApiError)
        self.assertIn("参数错误", str(err))
        self.assertIn("--help", str(err))


class TestListVpcs(unittest.TestCase):
    def test_single_page(self):
        fake = FakeRunner([(
            json.dumps({"vpcs": [VPC_1, VPC_2]}), "", 0)])
        with mock.patch("list_vpc.subprocess.run", fake):
            vpcs = list_vpcs("cn-north-4")
        self.assertEqual(vpcs, [VPC_1, VPC_2])
        self.assertEqual(len(fake.calls), 1)

    def test_pagination_via_next_marker(self):
        page1 = {"vpcs": [VPC_1],
                 "page_info": {"next_marker": "tok-2", "current_count": 1}}
        page2 = {"vpcs": [VPC_2],
                 "page_info": {"next_marker": None, "current_count": 1}}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("list_vpc.subprocess.run", fake):
            vpcs = list_vpcs("cn-north-4", limit=1)
        self.assertEqual(vpcs, [VPC_1, VPC_2])
        self.assertEqual(len(fake.calls), 2)
        self.assertIn("--marker=tok-2", fake.calls[1])

    def test_pagination_via_full_page_without_marker(self):
        page1 = {"vpcs": [VPC_1]}
        page2 = {"vpcs": []}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("list_vpc.subprocess.run", fake):
            vpcs = list_vpcs("cn-north-4", limit=1)
        self.assertEqual(vpcs, [VPC_1])

    def test_empty_region(self):
        fake = FakeRunner([(json.dumps({"vpcs": []}), "", 0)])
        with mock.patch("list_vpc.subprocess.run", fake):
            vpcs = list_vpcs("cn-north-4")
        self.assertEqual(vpcs, [])

    def test_filters_forwarded_to_cli(self):
        fake = FakeRunner([(
            json.dumps({"vpcs": [VPC_1]}), "", 0)])
        with mock.patch("list_vpc.subprocess.run", fake):
            list_vpcs("cn-north-4", vpc_id="vpc-0001", enterprise_project_id="0")
        call = fake.calls[0]
        self.assertTrue(any("--id.1=vpc-0001" in part for part in call))
        self.assertTrue(any("--enterprise_project_id=0" in part for part in call))

    def test_use_error_rc0_raises_api_error(self):
        fake = FakeRunner([(
            "[USE_ERROR]Invalid parameter: enterprise_project_id\n\n"
            "Run `hcloud VPC ListVpcs --help` for details.", "", 0)])
        with mock.patch("list_vpc.subprocess.run", fake):
            with self.assertRaises(ApiError) as ctx:
                list_vpcs("cn-north-4")
        self.assertIn("参数错误", str(ctx.exception))

    def test_nonzero_exit_403(self):
        fake = FakeRunner([("", "403 Forbidden", 1)])
        with mock.patch("list_vpc.subprocess.run", fake):
            with self.assertRaises(AuthError):
                list_vpcs("cn-north-4")

    def test_nonzero_exit_credentials(self):
        fake = FakeRunner([("", "ERROR: no AK configured", 1)])
        with mock.patch("list_vpc.subprocess.run", fake):
            with self.assertRaises(ConfigError):
                list_vpcs("cn-north-4")

    def test_timeout(self):
        fake = FakeRunner([subprocess.TimeoutExpired(cmd="hcloud", timeout=120)])
        with mock.patch("list_vpc.subprocess.run", fake):
            with self.assertRaises(ApiError):
                list_vpcs("cn-north-4")

    def test_sdk_fallback_when_hcloud_missing(self):
        with mock.patch("list_vpc.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_vpc.list_vpcs_via_sdk",
                           return_value=[VPC_1, VPC_2]) as sdk_mock:
            vpcs = list_vpcs("cn-north-4", vpc_id="vpc-1",
                             enterprise_project_id="0", project_id="proj-1")
        self.assertEqual(vpcs, [VPC_1, VPC_2])
        self.assertEqual(sdk_mock.call_args.kwargs.get("vpc_id"), "vpc-1")
        self.assertEqual(sdk_mock.call_args.kwargs.get("project_id"), "proj-1")

    def test_sdk_fallback_unavailable_raises_config(self):
        with mock.patch("list_vpc.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_vpc.list_vpcs_via_sdk",
                           side_effect=ConfigError("huaweicloudsdkvpc 未安装")):
            with self.assertRaises(ConfigError):
                list_vpcs("cn-north-4")

    def test_sdk_request_signature(self):
        # Regression guard: the real huaweicloudsdkvpc ListVpcsRequest must be
        # constructible with exactly the kwargs the fallback path sends.
        try:
            from huaweicloudsdkvpc.v2 import ListVpcsRequest
        except ImportError:
            self.skipTest("huaweicloudsdkvpc not installed")
        request = ListVpcsRequest(
            limit=100, marker=None, id="vpc-9", enterprise_project_id="0",
        )
        self.assertEqual(request.id, "vpc-9")
        self.assertEqual(request.enterprise_project_id, "0")
        with self.assertRaises(TypeError):
            ListVpcsRequest(no_such_param=1)


class _FakeSdkResponse:
    def __init__(self, vpcs, next_marker=None):
        self.vpcs = vpcs

        class _PageInfo:
            pass

        if next_marker is not None:
            page = _PageInfo()
            page.next_marker = next_marker
            self.page_info = page


class _FakeSdkVpc:
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
    """The SDK fallback must use modules that exist in the official
    huaweicloudsdkvpc package and wire credentials (including the project id
    required by /v1/{project_id}/...) from environment variables
    (BasicCredentials has no env auto-discovery)."""

    def setUp(self):
        self._captured_credentials = None
        self._captured_region = None
        self._fake_client = mock.Mock()
        self._fake_client.list_vpcs.return_value = _FakeSdkResponse(
            [_FakeSdkVpc(VPC_1), _FakeSdkVpc(VPC_2)], None)
        try:
            import huaweicloudsdkvpc.v2 as vpc_v2
        except ImportError:
            self.skipTest("huaweicloudsdkvpc not installed")
        self._builder_patch = mock.patch.object(
            vpc_v2.VpcClient, "new_builder",
            classmethod(lambda cls: _FakeSdkBuilder(self)))
        self._builder_patch.start()
        self.addCleanup(self._builder_patch.stop)

    def _clean_credential_env(self):
        credential_vars = (
            "HW_ACCESS_KEY",
            "HUAWEI_ACCESS_KEY",
            "HUAWEICLOUD_SDK_AK",
            "HUAWEI_CLOUD_ACCESS_KEY",
            "HW_SECRET_KEY",
            "HUAWEI_SECRET_KEY",
            "HUAWEICLOUD_SDK_SK",
            "HUAWEI_CLOUD_SECRET_KEY",
            "HW_PROJECT_ID",
            "HUAWEI_PROJECT_ID",
            "HUAWEICLOUD_SDK_PROJECT_ID",
            "HUAWEI_CLOUD_PROJECT_ID",
        )
        return {name: "" for name in credential_vars}

    def test_official_sdk_imports_resolve(self):
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkvpc.v2 import VpcClient, ListVpcsRequest
        from huaweicloudsdkvpc.v2.region.vpc_region import VpcRegion
        for obj in (BasicCredentials, Region, HttpConfig,
                    VpcClient, ListVpcsRequest, VpcRegion):
            self.assertTrue(callable(obj), obj)

    def test_sdk_fallback_returns_vpcs_with_env_credentials(self):
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak",
                   HUAWEI_SECRET_KEY="test-sk",
                   HUAWEI_PROJECT_ID="test-project")
        with mock.patch.dict(os.environ, env, clear=True):
            vpcs = list_vpcs_via_sdk("cn-north-4")
        self.assertEqual(vpcs, [VPC_1, VPC_2])
        credentials = self._captured_credentials
        self.assertIsNotNone(credentials)
        self.assertEqual(getattr(credentials, "ak", None), "test-ak")
        self.assertEqual(getattr(credentials, "sk", None), "test-sk")
        self.assertEqual(getattr(credentials, "project_id", None), "test-project")
        self.assertEqual(getattr(self._captured_region, "id", None), "cn-north-4")

    def test_explicit_project_id_overrides_env(self):
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak",
                   HUAWEI_SECRET_KEY="test-sk",
                   HUAWEI_PROJECT_ID="env-project")
        with mock.patch.dict(os.environ, env, clear=True):
            list_vpcs_via_sdk("cn-north-4", project_id="cli-project")
        self.assertEqual(
            getattr(self._captured_credentials, "project_id", None), "cli-project")

    def test_sdk_fallback_missing_env_credentials_raises_config(self):
        env = dict(self._clean_credential_env(), HUAWEI_PROJECT_ID="test-project")
        with mock.patch.dict(os.environ, env, clear=True):
            with self.assertRaises(ConfigError) as ctx:
                list_vpcs_via_sdk("cn-north-4")
        message = str(ctx.exception)
        self.assertIn("AK/SK", message)
        self.assertNotIn("未安装", message)

    def test_sdk_fallback_missing_project_id_raises_config(self):
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak", HUAWEI_SECRET_KEY="test-sk")
        with mock.patch.dict(os.environ, env, clear=True):
            with self.assertRaises(ConfigError) as ctx:
                list_vpcs_via_sdk("cn-north-4")
        self.assertIn("project_id", str(ctx.exception))

    def test_sdk_pagination_via_page_info(self):
        first = _FakeSdkResponse([_FakeSdkVpc(VPC_1)], "tok-2")
        second = _FakeSdkResponse([_FakeSdkVpc(VPC_2)], None)
        self._fake_client.list_vpcs.side_effect = [first, second]
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak",
                   HUAWEI_SECRET_KEY="test-sk",
                   HUAWEI_PROJECT_ID="test-project")
        with mock.patch.dict(os.environ, env, clear=True):
            vpcs = list_vpcs_via_sdk("cn-north-4")
        self.assertEqual(vpcs, [VPC_1, VPC_2])
        second_request = self._fake_client.list_vpcs.call_args_list[1][0][0]
        self.assertEqual(second_request.marker, "tok-2")

    def test_sdk_pagination_via_last_id_when_page_full(self):
        # Typed ListVpcsResponse carries no page_info; a full page continues
        # from the last returned VPC id.
        first = _FakeSdkResponse([_FakeSdkVpc(VPC_1), _FakeSdkVpc(VPC_2)], None)
        second = _FakeSdkResponse([], None)
        self._fake_client.list_vpcs.side_effect = [first, second]
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak",
                   HUAWEI_SECRET_KEY="test-sk",
                   HUAWEI_PROJECT_ID="test-project")
        with mock.patch.dict(os.environ, env, clear=True):
            vpcs = list_vpcs_via_sdk("cn-north-4", limit=2)
        self.assertEqual(vpcs, [VPC_1, VPC_2])
        second_request = self._fake_client.list_vpcs.call_args_list[1][0][0]
        self.assertEqual(second_request.marker, "vpc-0002")


class TestNormalizeAndRender(unittest.TestCase):
    def test_normalize_compacts_routes(self):
        flat = normalize_vpc(VPC_1)
        self.assertIsInstance(flat["routes"], str)
        self.assertIn("0.0.0.0/0", flat["routes"])
        self.assertEqual(flat["name"], "vpc-demo-01")

    def test_normalize_empty_routes(self):
        flat = normalize_vpc(VPC_2)
        self.assertEqual(flat["routes"], "[]")

    def test_table_contains_basic_info(self):
        table = render_table([VPC_1, VPC_2])
        for fragment in ("vpc-0001", "vpc-demo-01", "192.168.0.0/16", "OK",
                         "vpc-0002", "10.0.0.0/8", "CREATING"):
            self.assertIn(fragment, table)

    def test_names(self):
        self.assertEqual(
            vpc_names([VPC_1, VPC_2]), ["vpc-demo-01", "vpc-demo-02"])

    def test_names_fallback_to_id(self):
        self.assertEqual(vpc_names([{"id": "vpc-9"}]), ["vpc-9"])


class TestMain(unittest.TestCase):
    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("list_vpc.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            rc = main(argv)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    def test_table_output(self):
        rc, out, err = self._run(
            ["--region", "cn-north-4"],
            [(json.dumps({"vpcs": [VPC_1, VPC_2]}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("虚拟私有云（VPC）列表", out)
        self.assertIn("vpc-0001", out)
        self.assertIn("OK", out)
        self.assertEqual(err, "")

    def test_json_output(self):
        rc, out, err = self._run(
            ["--json"],
            [(json.dumps({"vpcs": [VPC_1]}), "", 0)])
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual(payload, [VPC_1])

    def test_names_only_output(self):
        rc, out, err = self._run(
            ["--names-only"],
            [(json.dumps({"vpcs": [VPC_1, VPC_2]}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("vpc-demo-01", out)
        self.assertIn("vpc-demo-02", out)
        self.assertNotIn("cidr", out)

    def test_empty_vpcs_message(self):
        rc, out, err = self._run(
            ["--region", "cn-south-1"],
            [(json.dumps({"vpcs": []}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("无虚拟私有云（VPC）", out)
        self.assertIn("cn-south-1", out)

    def test_empty_with_filter_message(self):
        rc, out, _ = self._run(
            ["--enterprise-project-id", "0"],
            [(json.dumps({"vpcs": []}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("enterprise_project_id=0", out)

    def test_id_filter_main_forwarded(self):
        fake = FakeRunner([
            (json.dumps({"vpcs": [VPC_1]}), "", 0)])
        with mock.patch("list_vpc.subprocess.run", fake), \
                mock.patch("sys.stdout"), \
                mock.patch("sys.stderr"):
            rc = main(["--id", "vpc-0001"])
        self.assertEqual(rc, 0)
        self.assertTrue(any("--id.1=vpc-0001" in part for part in fake.calls[0]))

    def test_empty_json_output(self):
        rc, out, err = self._run(
            ["--json"],
            [(json.dumps({"vpcs": []}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out), [])

    def test_empty_names_only_output(self):
        rc, out, err = self._run(
            ["--names-only"],
            [(json.dumps({"vpcs": []}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("共 0 个", out)
        self.assertNotIn("无虚拟私有云（VPC）", out)

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
        with mock.patch("list_vpc.list_vpcs_via_sdk",
                        side_effect=ConfigError("huaweicloudsdkvpc 未安装")):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 1)
        self.assertIn("未安装", err)

    def test_hcloud_missing_falls_back_to_sdk(self):
        with mock.patch("list_vpc.list_vpcs_via_sdk",
                        return_value=[VPC_1]):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 0)
        self.assertIn("vpc-0001", out)

    def test_project_id_forwarded_to_sdk(self):
        with mock.patch("list_vpc.list_vpcs_via_sdk",
                        return_value=[VPC_1]) as sdk_mock:
            rc, out, err = self._run(["--project-id", "proj-9"],
                                     [FileNotFoundError()])
        self.assertEqual(rc, 0)
        self.assertEqual(sdk_mock.call_args.kwargs.get("project_id"), "proj-9")

    def test_write_intent_argv_blocked(self):
        rc, out, err = self._run(["--operation", "DeleteVpc"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)

    def test_write_keyword_argv_blocked(self):
        rc, out, err = self._run(["--id", "release-me"], [])
        self.assertEqual(rc, 1)
        self.assertIn("守卫拦截", err)


class TestMarkdownRender(unittest.TestCase):
    def test_headers_fixed_name_first(self):
        text = render_markdown([VPC_1], region="cn-north-4")
        self.assertEqual(
            text.splitlines()[0],
            "| VPC 名称 | VPC ID | 区域 | 网段 | 状态 | 企业项目 ID | 描述 | 创建时间 |")
        self.assertEqual(len(MD_HEADERS), 8)
        self.assertEqual(MD_HEADERS[0], "VPC 名称")

    def test_separator_row(self):
        lines = render_markdown([VPC_1], region="cn-north-4").splitlines()
        self.assertEqual(lines[1], "| " + " | ".join(["---"] * 8) + " |")

    def test_row_has_eight_columns(self):
        row = normalized_row(VPC_1, region="cn-north-4")
        self.assertEqual(len(row), 8)
        self.assertEqual(row[0], "vpc-demo-01")
        self.assertEqual(row[1], "vpc-0001")
        self.assertEqual(row[2], "cn-north-4")
        self.assertEqual(row[3], "192.168.0.0/16")
        self.assertEqual(row[4], "OK")
        self.assertEqual(row[5], "0")
        self.assertEqual(row[6], "demo vpc")
        self.assertEqual(row[7], "2024-01-01T00:00:00")

    def test_missing_fields_render_dash(self):
        row = normalized_row(VPC_2, region="cn-north-4")
        self.assertEqual(row[6], "-")
        self.assertEqual(row[7], "-")
        self.assertIn("| vpc-demo-02 | vpc-0002 | cn-north-4 | 10.0.0.0/8 | CREATING | 0 | - | - |",
                      render_markdown([VPC_2], region="cn-north-4"))

    def test_empty_list_renders_header_only_table(self):
        lines = render_markdown([], region="cn-north-4").splitlines()
        self.assertEqual(len(lines), 2)
        self.assertTrue(lines[0].startswith("| VPC 名称 |"))

    def test_summary_line(self):
        text = render_markdown([VPC_1, VPC_2], summary=True, region="cn-north-4")
        self.assertIn("**汇总**：共 2 个 VPC（Region cn-north-4）。", text)

    def test_pipe_in_value_escaped(self):
        vpc = {"id": "vpc-9", "name": "a|b"}
        self.assertIn("a\\|b", render_markdown([vpc], region="cn-north-4"))

    def test_contract_matches_export_markdown(self):
        try:
            sys.path.insert(0, os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "..", "huawei-cloud-vpc-export-markdown", "scripts"))
            import export_vpc_markdown as ref
        finally:
            sys.path.pop(0)
        self.assertEqual(MD_HEADERS, ref.MD_HEADERS)
        self.assertEqual(normalized_row(VPC_1, region="cn-north-4"),
                         ref.normalized_row(VPC_1, region="cn-north-4"))
        self.assertEqual(render_markdown([], region="cn-north-4"),
                         ref.render_markdown([], region="cn-north-4"))
        self.assertEqual(render_markdown([VPC_1, VPC_2], summary=True, region="cn-north-4"),
                         ref.render_markdown([VPC_1, VPC_2], summary=True,
                                             region="cn-north-4"))


class TestMarkdownExport(unittest.TestCase):
    def test_writes_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "out.md")
            written = export_markdown([VPC_1], path, region="cn-north-4")
            self.assertEqual(written, os.path.abspath(path))
            with open(path, encoding="utf-8") as handle:
                text = handle.read()
            self.assertIn("VPC 名称", text)
            self.assertIn("vpc-demo-01", text)
            self.assertEqual(text.count("\n"), 3)

    def test_empty_list_writes_header_only_table(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "empty.md")
            export_markdown([], path, region="cn-north-4")
            with open(path, encoding="utf-8") as handle:
                lines = handle.read().splitlines()
            self.assertEqual(len(lines), 2)
            self.assertTrue(lines[0].startswith("| VPC 名称 |"))

    def test_creates_missing_parent_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "nested", "deep", "out.md")
            export_markdown([VPC_1], path)
            self.assertTrue(os.path.isfile(path))

    def test_summary_written(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "out.md")
            export_markdown([VPC_1], path, summary=True, region="cn-south-1")
            with open(path, encoding="utf-8") as handle:
                text = handle.read()
            self.assertIn("**汇总**：共 1 个 VPC（Region cn-south-1）。", text)

    def test_bad_path_raises_and_leaves_no_partial_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            blocker = os.path.join(tmp, "not-a-dir")
            with open(blocker, "w", encoding="utf-8") as handle:
                handle.write("x")
            path = os.path.join(blocker, "out.md")
            with self.assertRaises(ExportError):
                export_markdown([VPC_1], path)
            self.assertFalse(os.path.exists(path))
            self.assertEqual(sorted(os.listdir(tmp)), ["not-a-dir"])

    def test_no_temp_file_left_after_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "out.md")
            export_markdown([VPC_1], path)
            self.assertEqual(sorted(os.listdir(tmp)), ["out.md"])

    def test_default_output_path_format(self):
        import re as _re
        name = default_output_path("cn-north-4")
        self.assertRegex(
            name, _re.compile(r"^vpc_list_cn-north-4_\d{8}_\d{6}\.md$"))


class TestMainMarkdown(unittest.TestCase):
    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("list_vpc.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            rc = main(argv)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    def test_md_output_writes_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "sub", "report.md")
            rc, out, err = self._run(
                ["--format", "md", "--output", path],
                [(json.dumps({"vpcs": [VPC_1, VPC_2]}), "", 0)])
            self.assertEqual(rc, 0, err)
            self.assertTrue(os.path.isfile(path))
            with open(path, encoding="utf-8") as handle:
                text = handle.read()
            self.assertTrue(text.splitlines()[0].startswith("| VPC 名称 |"))
            self.assertIn("vpc-demo-01", text)
            self.assertIn("已生成", out)

    def test_md_short_flags(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "report.md")
            rc, _, err = self._run(
                ["-f", "md", "-o", path],
                [(json.dumps({"vpcs": [VPC_1]}), "", 0)])
            self.assertEqual(rc, 0, err)
            self.assertTrue(os.path.isfile(path))

    def test_empty_md_writes_empty_table(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "empty.md")
            rc, out, err = self._run(
                ["--format", "md", "--output", path],
                [(json.dumps({"vpcs": []}), "", 0)])
            self.assertEqual(rc, 0, err)
            with open(path, encoding="utf-8") as handle:
                self.assertEqual(len(handle.read().splitlines()), 2)
            self.assertIn("仅表头", out)
            self.assertIn("无虚拟私有云（VPC）", out)

    def test_empty_filtered_md_mentions_filters(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "empty.md")
            rc, out, _ = self._run(
                ["--format", "md", "--output", path,
                 "--enterprise-project-id", "0"],
                [(json.dumps({"vpcs": []}), "", 0)])
            self.assertEqual(rc, 0)
            self.assertIn("enterprise_project_id=0", out)

    def test_default_md_path_used(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "vpc_list_cn-north-4_20240101_000000.md")
            with mock.patch("list_vpc.default_output_path", return_value=path):
                rc, _, err = self._run(
                    ["--format", "md"],
                    [(json.dumps({"vpcs": [VPC_1]}), "", 0)])
            self.assertEqual(rc, 0, err)
            self.assertTrue(os.path.isfile(path))

    def test_summary_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "s.md")
            rc, _, _ = self._run(
                ["--format", "md", "--output", path, "--summary"],
                [(json.dumps({"vpcs": [VPC_1]}), "", 0)])
            self.assertEqual(rc, 0)
            with open(path, encoding="utf-8") as handle:
                self.assertIn("**汇总**", handle.read())

    def test_output_path_with_delete_not_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "vpc-delete-report.md")
            rc, _, err = self._run(
                ["--format", "md", "--output", path],
                [(json.dumps({"vpcs": [VPC_1]}), "", 0)])
            self.assertEqual(rc, 0, err)
            self.assertTrue(os.path.isfile(path))

    def test_md_auth_error_no_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "report.md")
            rc, _, err = self._run(
                ["--format", "md", "--output", path], [("", "403 Forbidden", 1)])
            self.assertEqual(rc, 1)
            self.assertIn("IAM", err)
            self.assertFalse(os.path.exists(path))

    def test_format_json_mode(self):
        rc, out, _ = self._run(
            ["--format", "json"],
            [(json.dumps({"vpcs": [VPC_1]}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out), [VPC_1])

    def test_format_names_mode(self):
        rc, out, _ = self._run(
            ["--format", "names"],
            [(json.dumps({"vpcs": [VPC_1, VPC_2]}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("vpc-demo-01", out)
        self.assertNotIn("cidr", out)

    def test_format_table_mode(self):
        rc, out, _ = self._run(
            ["--format", "table"],
            [(json.dumps({"vpcs": [VPC_1]}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("完整字段", out)

    def test_legacy_json_wins_over_md(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "report.md")
            rc, out, _ = self._run(
                ["--json", "--format", "md", "--output", path],
                [(json.dumps({"vpcs": [VPC_1]}), "", 0)])
            self.assertEqual(rc, 0)
            self.assertEqual(json.loads(out), [VPC_1])
            self.assertFalse(os.path.exists(path))


class TestErrorHierarchy(unittest.TestCase):
    def test_subclasses(self):
        for exc in (GuardError, ConfigError, AuthError, ApiError, ExportError):
            self.assertTrue(issubclass(exc, VpcListError))


class TestPeeringGuard(unittest.TestCase):
    def test_peering_operation_allowed(self):
        self.assertTrue(guard_operation(PEERING_OPERATION, allowed=PEERING_OPERATION))

    def test_peering_write_operation_blocked(self):
        with self.assertRaises(GuardError):
            guard_operation("CreateVpcPeering", allowed=PEERING_OPERATION)

    def test_peering_write_intent_blocked(self):
        for text in ("CreateVpcPeering", "DeleteVpcPeering",
                     "AcceptVpcPeering", "RejectVpcPeering",
                     "UpdateVpcPeering", "--create-vpc-peering"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_peering_resource_flag_passes(self):
        self.assertFalse(guard_write_intent("--resource peering --region cn-north-4"))

    def test_vpc_operation_not_allowed_in_peering_mode(self):
        with self.assertRaises(GuardError):
            guard_operation(ALLOWED_OPERATION, allowed=PEERING_OPERATION)


class TestBuildPeeringCommand(unittest.TestCase):
    def test_basic(self):
        argv = build_peering_command("cn-north-4")
        self.assertEqual(argv[0], "VPC")
        self.assertEqual(argv[1], "ListVpcPeerings")
        self.assertIn("--cli-region=cn-north-4", argv)
        self.assertIn("--limit=100", argv)
        self.assertFalse(any(flag.startswith("--marker") for flag in argv))

    def test_marker_appended(self):
        argv = build_peering_command("cn-north-4", marker="tok-123", limit=10)
        self.assertIn("--marker=tok-123", argv)
        self.assertIn("--limit=10", argv)

    def test_no_write_flags_ever_added(self):
        argv = build_peering_command("cn-north-4")
        for flag in argv:
            self.assertFalse(flag.lower().lstrip("-").startswith(
                ("create", "delete", "update", "accept", "reject")))


class TestExtractPeerings(unittest.TestCase):
    def test_extract_peerings_known_keys(self):
        for key in ("peerings", "peering"):
            self.assertEqual(extract_peerings({key: [PEERING_1]}), [PEERING_1])
        self.assertEqual(extract_peerings([PEERING_1]), [PEERING_1])
        self.assertEqual(extract_peerings({"page_info": {}}), [])


class TestListPeerings(unittest.TestCase):
    def test_single_page(self):
        fake = FakeRunner([(
            json.dumps({"peerings": [PEERING_1, PEERING_2]}), "", 0)])
        with mock.patch("list_vpc.subprocess.run", fake):
            peerings = list_peerings("cn-north-4")
        self.assertEqual(peerings, [PEERING_1, PEERING_2])
        self.assertEqual(len(fake.calls), 1)
        self.assertIn("ListVpcPeerings", fake.calls[0])

    def test_pagination_via_next_marker(self):
        page1 = {"peerings": [PEERING_1],
                 "page_info": {"next_marker": "tok-2", "current_count": 1}}
        page2 = {"peerings": [PEERING_2],
                 "page_info": {"next_marker": None, "current_count": 1}}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("list_vpc.subprocess.run", fake):
            peerings = list_peerings("cn-north-4", limit=1)
        self.assertEqual(peerings, [PEERING_1, PEERING_2])
        self.assertEqual(len(fake.calls), 2)
        self.assertIn("--marker=tok-2", fake.calls[1])

    def test_pagination_via_full_page_without_marker(self):
        page1 = {"peerings": [PEERING_1]}
        page2 = {"peerings": []}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("list_vpc.subprocess.run", fake):
            peerings = list_peerings("cn-north-4", limit=1)
        self.assertEqual(peerings, [PEERING_1])

    def test_empty_region(self):
        fake = FakeRunner([(json.dumps({"peerings": []}), "", 0)])
        with mock.patch("list_vpc.subprocess.run", fake):
            peerings = list_peerings("cn-north-4")
        self.assertEqual(peerings, [])

    def test_use_error_rc0_raises_api_error(self):
        fake = FakeRunner([(
            "[USE_ERROR]Invalid parameter: status\n\n"
            "Run `hcloud VPC ListVpcPeerings --help` for details.", "", 0)])
        with mock.patch("list_vpc.subprocess.run", fake):
            with self.assertRaises(ApiError) as ctx:
                list_peerings("cn-north-4")
        self.assertIn("参数错误", str(ctx.exception))
        self.assertIn("ListVpcPeerings", str(ctx.exception))

    def test_nonzero_exit_403(self):
        fake = FakeRunner([("", "403 Forbidden", 1)])
        with mock.patch("list_vpc.subprocess.run", fake):
            with self.assertRaises(AuthError):
                list_peerings("cn-north-4")

    def test_nonzero_exit_credentials(self):
        fake = FakeRunner([("", "ERROR: no AK configured", 1)])
        with mock.patch("list_vpc.subprocess.run", fake):
            with self.assertRaises(ConfigError):
                list_peerings("cn-north-4")

    def test_timeout(self):
        fake = FakeRunner([subprocess.TimeoutExpired(cmd="hcloud", timeout=120)])
        with mock.patch("list_vpc.subprocess.run", fake):
            with self.assertRaises(ApiError):
                list_peerings("cn-north-4")

    def test_sdk_fallback_when_hcloud_missing(self):
        with mock.patch("list_vpc.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_vpc.list_peerings_via_sdk",
                           return_value=[PEERING_1, PEERING_2]) as sdk_mock:
            peerings = list_peerings("cn-north-4", project_id="proj-1")
        self.assertEqual(peerings, [PEERING_1, PEERING_2])
        self.assertEqual(sdk_mock.call_args.kwargs.get("project_id"), "proj-1")

    def test_sdk_fallback_unavailable_raises_config(self):
        with mock.patch("list_vpc.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_vpc.list_peerings_via_sdk",
                           side_effect=ConfigError("huaweicloudsdkvpc 未安装")):
            with self.assertRaises(ConfigError):
                list_peerings("cn-north-4")

    def test_sdk_request_signature(self):
        try:
            from huaweicloudsdkvpc.v2 import ListVpcPeeringsRequest
        except ImportError:
            self.skipTest("huaweicloudsdkvpc not installed")
        request = ListVpcPeeringsRequest(limit=100, marker=None)
        self.assertEqual(request.limit, 100)
        with self.assertRaises(TypeError):
            ListVpcPeeringsRequest(no_such_param=1)


class _FakeSdkPeeringResponse:
    def __init__(self, peerings, next_marker=None):
        self.peerings = peerings

        class _PageInfo:
            pass

        if next_marker is not None:
            page = _PageInfo()
            page.next_marker = next_marker
            self.page_info = page


class _FakeSdkPeering:
    def __init__(self, payload):
        self._payload = payload

    def to_dict(self):
        return self._payload


class _FakeSdkPeeringBuilder:
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


class TestPeeringSdkFallback(unittest.TestCase):
    def setUp(self):
        self._captured_credentials = None
        self._captured_region = None
        self._fake_client = mock.Mock()
        self._fake_client.list_vpc_peerings.return_value = (
            _FakeSdkPeeringResponse(
                [_FakeSdkPeering(PEERING_1), _FakeSdkPeering(PEERING_2)], None))
        try:
            import huaweicloudsdkvpc.v2 as vpc_v2
        except ImportError:
            self.skipTest("huaweicloudsdkvpc not installed")
        self._builder_patch = mock.patch.object(
            vpc_v2.VpcClient, "new_builder",
            classmethod(lambda cls: _FakeSdkPeeringBuilder(self)))
        self._builder_patch.start()
        self.addCleanup(self._builder_patch.stop)

    def _clean_credential_env(self):
        credential_vars = (
            "HW_ACCESS_KEY", "HUAWEI_ACCESS_KEY", "HUAWEICLOUD_SDK_AK",
            "HUAWEI_CLOUD_ACCESS_KEY", "HW_SECRET_KEY", "HUAWEI_SECRET_KEY",
            "HUAWEICLOUD_SDK_SK", "HUAWEI_CLOUD_SECRET_KEY", "HW_PROJECT_ID",
            "HUAWEI_PROJECT_ID", "HUAWEICLOUD_SDK_PROJECT_ID",
            "HUAWEI_CLOUD_PROJECT_ID",
        )
        return {name: "" for name in credential_vars}

    def test_official_peering_imports_resolve(self):
        from huaweicloudsdkvpc.v2 import VpcClient, ListVpcPeeringsRequest
        for obj in (VpcClient, ListVpcPeeringsRequest):
            self.assertTrue(callable(obj), obj)

    def test_sdk_fallback_returns_peerings_with_env_credentials(self):
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak",
                   HUAWEI_SECRET_KEY="test-sk",
                   HUAWEI_PROJECT_ID="test-project")
        with mock.patch.dict(os.environ, env, clear=True):
            peerings = list_peerings_via_sdk("cn-north-4")
        self.assertEqual(peerings, [PEERING_1, PEERING_2])
        self.assertEqual(getattr(self._captured_credentials, "ak", None), "test-ak")
        self.assertEqual(getattr(self._captured_region, "id", None), "cn-north-4")

    def test_sdk_pagination_via_page_info(self):
        first = _FakeSdkPeeringResponse([_FakeSdkPeering(PEERING_1)], "tok-2")
        second = _FakeSdkPeeringResponse([_FakeSdkPeering(PEERING_2)], None)
        self._fake_client.list_vpc_peerings.side_effect = [first, second]
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak",
                   HUAWEI_SECRET_KEY="test-sk",
                   HUAWEI_PROJECT_ID="test-project")
        with mock.patch.dict(os.environ, env, clear=True):
            peerings = list_peerings_via_sdk("cn-north-4")
        self.assertEqual(peerings, [PEERING_1, PEERING_2])
        second_request = self._fake_client.list_vpc_peerings.call_args_list[1][0][0]
        self.assertEqual(second_request.marker, "tok-2")

    def test_sdk_pagination_via_last_id_when_page_full(self):
        first = _FakeSdkPeeringResponse(
            [_FakeSdkPeering(PEERING_1), _FakeSdkPeering(PEERING_2)], None)
        second = _FakeSdkPeeringResponse([], None)
        self._fake_client.list_vpc_peerings.side_effect = [first, second]
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak",
                   HUAWEI_SECRET_KEY="test-sk",
                   HUAWEI_PROJECT_ID="test-project")
        with mock.patch.dict(os.environ, env, clear=True):
            peerings = list_peerings_via_sdk("cn-north-4", limit=2)
        self.assertEqual(peerings, [PEERING_1, PEERING_2])
        second_request = self._fake_client.list_vpc_peerings.call_args_list[1][0][0]
        self.assertEqual(second_request.marker, "peering-0002")


class TestPeeringNormalizeAndRender(unittest.TestCase):
    def test_normalize_maps_local_and_peer_vpc(self):
        row = normalize_peering(PEERING_1)
        self.assertEqual(row["name"], "peering-a-to-b")
        self.assertEqual(row["local_vpc"], "vpc-0001")
        self.assertEqual(row["peer_vpc"], "vpc-0002")
        self.assertEqual(row["status"], "ACTIVE")

    def test_normalize_missing_info_uses_dash(self):
        row = normalize_peering({"id": "peering-9", "status": "ACTIVE"})
        self.assertEqual(row["name"], "peering-9")
        self.assertEqual(row["local_vpc"], "-")
        self.assertEqual(row["peer_vpc"], "-")

    def test_table_has_four_columns(self):
        table = render_peering_table([PEERING_1, PEERING_2])
        header = table.splitlines()[0]
        for col in ("name", "local_vpc", "peer_vpc", "status"):
            self.assertIn(col, header)
        for fragment in ("peering-a-to-b", "vpc-0001", "vpc-0002", "ACTIVE",
                         "peering-c-to-d", "PENDING_ACCEPTANCE"):
            self.assertIn(fragment, table)

    def test_peering_names(self):
        self.assertEqual(
            peering_names([PEERING_1, PEERING_2]),
            ["peering-a-to-b", "peering-c-to-d"])
        self.assertEqual(peering_names([{"id": "peering-9"}]), ["peering-9"])


class TestPeeringMain(unittest.TestCase):
    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("list_vpc.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            rc = main(argv)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    def test_peering_table_output(self):
        rc, out, err = self._run(
            ["--resource", "peering", "--region", "cn-north-4"],
            [(json.dumps({"peerings": [PEERING_1, PEERING_2]}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("VPC 对等连接列表", out)
        self.assertIn("local_vpc", out)
        self.assertIn("peer_vpc", out)
        self.assertIn("vpc-0001", out)
        self.assertIn("vpc-0002", out)
        self.assertEqual(err, "")

    def test_peering_json_raw_output(self):
        rc, out, err = self._run(
            ["--resource", "peering", "--json"],
            [(json.dumps({"peerings": [PEERING_1]}), "", 0)])
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual(payload, [PEERING_1])
        self.assertIn("request_vpc_info", payload[0])

    def test_peering_names_only_output(self):
        rc, out, err = self._run(
            ["--resource", "peering", "--names-only"],
            [(json.dumps({"peerings": [PEERING_1, PEERING_2]}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("peering-a-to-b", out)
        self.assertIn("peering-c-to-d", out)
        self.assertNotIn("local_vpc", out)

    def test_peering_empty_message(self):
        rc, out, err = self._run(
            ["--resource", "peering", "--region", "cn-south-1"],
            [(json.dumps({"peerings": []}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("无对等连接（VPC Peering）", out)
        self.assertIn("cn-south-1", out)

    def test_peering_auth_error_message(self):
        rc, out, err = self._run(["--resource", "peering"],
                                 [("", "403 Forbidden", 1)])
        self.assertEqual(rc, 1)
        self.assertIn("[错误]", err)
        self.assertIn("IAM", err)

    def test_peering_missing_ak_sk_error_message(self):
        rc, out, err = self._run(["--resource", "peering"],
                                 [("", "ERROR: cli-ak empty", 1)])
        self.assertEqual(rc, 1)
        self.assertIn("AK/SK", err)

    def test_peering_write_intent_blocked(self):
        rc, out, err = self._run(
            ["--resource", "peering", "--operation", "CreateVpcPeering"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)

    def test_peering_unsupported_filters_rejected(self):
        rc, out, err = self._run(
            ["--resource", "peering", "--id", "vpc-0001"], [])
        self.assertEqual(rc, 1)
        self.assertIn("不支持", err)

    def test_peering_sdk_fallback_via_main(self):
        with mock.patch("list_vpc.list_peerings_via_sdk",
                        return_value=[PEERING_1]):
            rc, out, err = self._run(
                ["--resource", "peering"], [FileNotFoundError()])
        self.assertEqual(rc, 0)
        self.assertIn("peering-a-to-b", out)

    def test_default_resource_still_vpc(self):
        rc, out, err = self._run(
            ["--region", "cn-north-4"],
            [(json.dumps({"vpcs": [VPC_1]}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("虚拟私有云（VPC）列表", out)
        self.assertNotIn("对等连接", out)


if __name__ == "__main__":
    unittest.main()