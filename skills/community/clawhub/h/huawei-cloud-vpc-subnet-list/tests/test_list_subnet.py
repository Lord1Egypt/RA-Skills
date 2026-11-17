import json
import os
import subprocess
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from list_subnet import (  # noqa: E402
    ALLOWED_OPERATION,
    ApiError,
    AuthError,
    ConfigError,
    GuardError,
    SubnetListError,
    build_command,
    classify_hcloud_failure,
    extract_json,
    extract_subnets,
    guard_operation,
    guard_write_intent,
    list_subnets,
    list_subnets_via_sdk,
    main,
    normalize_subnet,
    render_table,
    subnet_names,
)

SUBNET_1 = {
    "id": "subnet-0001",
    "name": "subnet-demo-01",
    "vpc_id": "vpc-0001",
    "cidr": "192.168.0.0/24",
    "gateway_ip": "192.168.0.1",
    "status": "ACTIVE",
    "description": "demo subnet",
    "availability_zone": "cn-north-4a",
    "available_ip_address_count": 251,
    "dns_list": ["100.125.1.250", "100.125.129.250"],
    "extra_dhcp_opts": [{"opt_name": "addresstime", "opt_value": "1"}],
    "neutron_network_id": "net-0001",
    "neutron_subnet_id": "nsub-0001",
    "tenant_id": "tenant-0001",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-02T00:00:00",
}
SUBNET_2 = {
    "id": "subnet-0002",
    "name": "subnet-demo-02",
    "vpc_id": "vpc-0002",
    "cidr": "10.0.0.0/24",
    "gateway_ip": "10.0.0.1",
    "status": "PENDING",
    "dns_list": [],
    "tenant_id": "tenant-0001",
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
        self.assertFalse(guard_write_intent("--region cn-north-4 --json list subnets"))
        self.assertFalse(guard_write_intent("show subnet details"))

    def test_create_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("CreateSubnet subnet-new")

    def test_delete_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--operation DeleteSubnet")

    def test_mutating_verbs_blocked(self):
        for text in ("associate route", "disassociate port",
                     "detach subnet from vpc", "release subnet-01",
                     "update subnet name", "bind bandwidth"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_normalized_separators_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--create-subnet")
        with self.assertRaises(GuardError):
            guard_write_intent("delete_subnet_route")

    def test_read_filter_value_passes(self):
        self.assertFalse(guard_write_intent("--vpc-id 1234abcd-0000-0000-0000-000000000000"))

    def test_operation_guard_rejects_non_list(self):
        with self.assertRaises(GuardError):
            guard_operation("ShowSubnet")
        self.assertTrue(guard_operation(ALLOWED_OPERATION))


class TestBuildCommand(unittest.TestCase):
    def test_basic(self):
        argv = build_command("cn-north-4")
        self.assertEqual(argv[0], "VPC")
        self.assertEqual(argv[1], "ListSubnets")
        self.assertIn("--cli-region=cn-north-4", argv)
        self.assertIn("--limit=100", argv)
        self.assertFalse(any(flag.startswith("--marker") for flag in argv))
        self.assertFalse(any(flag.startswith("--vpc_id") for flag in argv))

    def test_marker_appended(self):
        argv = build_command("cn-north-4", marker="tok-123", limit=10)
        self.assertIn("--marker=tok-123", argv)
        self.assertIn("--limit=10", argv)

    def test_vpc_id_forwarded_server_side(self):
        argv = build_command("cn-south-1", vpc_id="vpc-9", limit=10)
        self.assertIn("--vpc_id=vpc-9", argv)
        self.assertIn("--limit=10", argv)

    def test_no_write_flags_ever_added(self):
        argv = build_command("cn-north-4", vpc_id="vpc-9")
        for flag in argv:
            self.assertFalse(flag.lower().lstrip("-").startswith(
                ("create", "delete", "update", "associate", "release")))


class TestExtract(unittest.TestCase):
    def test_extract_json_plain(self):
        data = extract_json(json.dumps({"subnets": []}))
        self.assertEqual(data, {"subnets": []})

    def test_extract_json_with_noise(self):
        data = extract_json("WARNING some noise\n{\"a\": 1}\n")
        self.assertEqual(data, {"a": 1})

    def test_extract_json_invalid(self):
        with self.assertRaises(ApiError):
            extract_json("<html>not json</html>")

    def test_extract_subnets_known_keys(self):
        for key in ("subnets", "subnet"):
            self.assertEqual(extract_subnets({key: [SUBNET_1]}), [SUBNET_1])
        self.assertEqual(extract_subnets([SUBNET_1]), [SUBNET_1])
        self.assertEqual(extract_subnets({"page_info": {}}), [])


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
            "[USE_ERROR]Invalid parameter: vpc_id\n\n"
            "Run `hcloud VPC ListSubnets --help` for details.", "", 0)
        self.assertIsInstance(err, ApiError)
        self.assertIn("参数错误", str(err))
        self.assertIn("--help", str(err))


class TestListSubnets(unittest.TestCase):
    def test_single_page(self):
        fake = FakeRunner([(
            json.dumps({"subnets": [SUBNET_1, SUBNET_2]}), "", 0)])
        with mock.patch("list_subnet.subprocess.run", fake):
            subnets = list_subnets("cn-north-4")
        self.assertEqual(subnets, [SUBNET_1, SUBNET_2])
        self.assertEqual(len(fake.calls), 1)

    def test_pagination_via_next_marker(self):
        page1 = {"subnets": [SUBNET_1],
                 "page_info": {"next_marker": "tok-2", "current_count": 1}}
        page2 = {"subnets": [SUBNET_2],
                 "page_info": {"next_marker": None, "current_count": 1}}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("list_subnet.subprocess.run", fake):
            subnets = list_subnets("cn-north-4", limit=1)
        self.assertEqual(subnets, [SUBNET_1, SUBNET_2])
        self.assertEqual(len(fake.calls), 2)
        self.assertIn("--marker=tok-2", fake.calls[1])

    def test_pagination_via_full_page_without_marker(self):
        page1 = {"subnets": [SUBNET_1]}
        page2 = {"subnets": []}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("list_subnet.subprocess.run", fake):
            subnets = list_subnets("cn-north-4", limit=1)
        self.assertEqual(subnets, [SUBNET_1])

    def test_empty_region(self):
        fake = FakeRunner([(json.dumps({"subnets": []}), "", 0)])
        with mock.patch("list_subnet.subprocess.run", fake):
            subnets = list_subnets("cn-north-4")
        self.assertEqual(subnets, [])

    def test_vpc_id_forwarded_to_cli(self):
        fake = FakeRunner([(
            json.dumps({"subnets": [SUBNET_1]}), "", 0)])
        with mock.patch("list_subnet.subprocess.run", fake):
            list_subnets("cn-north-4", vpc_id="vpc-0001")
        call = fake.calls[0]
        self.assertTrue(any("--vpc_id=vpc-0001" in part for part in call))

    def test_use_error_rc0_raises_api_error(self):
        fake = FakeRunner([(
            "[USE_ERROR]Invalid parameter: vpc_id\n\n"
            "Run `hcloud VPC ListSubnets --help` for details.", "", 0)])
        with mock.patch("list_subnet.subprocess.run", fake):
            with self.assertRaises(ApiError) as ctx:
                list_subnets("cn-north-4")
        self.assertIn("参数错误", str(ctx.exception))

    def test_nonzero_exit_403(self):
        fake = FakeRunner([("", "403 Forbidden", 1)])
        with mock.patch("list_subnet.subprocess.run", fake):
            with self.assertRaises(AuthError):
                list_subnets("cn-north-4")

    def test_nonzero_exit_credentials(self):
        fake = FakeRunner([("", "ERROR: no AK configured", 1)])
        with mock.patch("list_subnet.subprocess.run", fake):
            with self.assertRaises(ConfigError):
                list_subnets("cn-north-4")

    def test_timeout(self):
        fake = FakeRunner([subprocess.TimeoutExpired(cmd="hcloud", timeout=120)])
        with mock.patch("list_subnet.subprocess.run", fake):
            with self.assertRaises(ApiError):
                list_subnets("cn-north-4")

    def test_sdk_fallback_when_hcloud_missing(self):
        with mock.patch("list_subnet.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_subnet.list_subnets_via_sdk",
                           return_value=[SUBNET_1, SUBNET_2]) as sdk_mock:
            subnets = list_subnets("cn-north-4", vpc_id="vpc-1",
                                   project_id="proj-1")
        self.assertEqual(subnets, [SUBNET_1, SUBNET_2])
        self.assertEqual(sdk_mock.call_args.kwargs.get("vpc_id"), "vpc-1")
        self.assertEqual(sdk_mock.call_args.kwargs.get("project_id"), "proj-1")

    def test_sdk_fallback_unavailable_raises_config(self):
        with mock.patch("list_subnet.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_subnet.list_subnets_via_sdk",
                           side_effect=ConfigError("huaweicloudsdkvpc 未安装")):
            with self.assertRaises(ConfigError):
                list_subnets("cn-north-4")

    def test_sdk_request_signature(self):
        # Regression guard: the real huaweicloudsdkvpc ListSubnetsRequest must be
        # constructible with exactly the kwargs the fallback path sends.
        try:
            from huaweicloudsdkvpc.v2 import ListSubnetsRequest
        except ImportError:
            self.skipTest("huaweicloudsdkvpc not installed")
        request = ListSubnetsRequest(limit=100, marker=None, vpc_id="vpc-9")
        self.assertEqual(request.vpc_id, "vpc-9")
        with self.assertRaises(TypeError):
            ListSubnetsRequest(no_such_param=1)


class _FakeSdkResponse:
    def __init__(self, subnets, next_marker=None):
        self.subnets = subnets

        class _PageInfo:
            pass

        if next_marker is not None:
            page = _PageInfo()
            page.next_marker = next_marker
            self.page_info = page


class _FakeSdkSubnet:
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
        self._fake_client.list_subnets.return_value = _FakeSdkResponse(
            [_FakeSdkSubnet(SUBNET_1), _FakeSdkSubnet(SUBNET_2)], None)
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
        from huaweicloudsdkvpc.v2 import VpcClient, ListSubnetsRequest
        from huaweicloudsdkvpc.v2.region.vpc_region import VpcRegion
        for obj in (BasicCredentials, Region, HttpConfig,
                    VpcClient, ListSubnetsRequest, VpcRegion):
            self.assertTrue(callable(obj), obj)

    def test_sdk_fallback_returns_subnets_with_env_credentials(self):
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak",
                   HUAWEI_SECRET_KEY="test-sk",
                   HUAWEI_PROJECT_ID="test-project")
        with mock.patch.dict(os.environ, env, clear=True):
            subnets = list_subnets_via_sdk("cn-north-4")
        self.assertEqual(subnets, [SUBNET_1, SUBNET_2])
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
            list_subnets_via_sdk("cn-north-4", project_id="cli-project")
        self.assertEqual(
            getattr(self._captured_credentials, "project_id", None), "cli-project")

    def test_sdk_fallback_missing_env_credentials_raises_config(self):
        env = dict(self._clean_credential_env(), HUAWEI_PROJECT_ID="test-project")
        with mock.patch.dict(os.environ, env, clear=True):
            with self.assertRaises(ConfigError) as ctx:
                list_subnets_via_sdk("cn-north-4")
        message = str(ctx.exception)
        self.assertIn("AK/SK", message)
        self.assertNotIn("未安装", message)

    def test_sdk_fallback_missing_project_id_raises_config(self):
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak", HUAWEI_SECRET_KEY="test-sk")
        with mock.patch.dict(os.environ, env, clear=True):
            with self.assertRaises(ConfigError) as ctx:
                list_subnets_via_sdk("cn-north-4")
        self.assertIn("project_id", str(ctx.exception))

    def test_sdk_pagination_via_page_info(self):
        first = _FakeSdkResponse([_FakeSdkSubnet(SUBNET_1)], "tok-2")
        second = _FakeSdkResponse([_FakeSdkSubnet(SUBNET_2)], None)
        self._fake_client.list_subnets.side_effect = [first, second]
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak",
                   HUAWEI_SECRET_KEY="test-sk",
                   HUAWEI_PROJECT_ID="test-project")
        with mock.patch.dict(os.environ, env, clear=True):
            subnets = list_subnets_via_sdk("cn-north-4")
        self.assertEqual(subnets, [SUBNET_1, SUBNET_2])
        second_request = self._fake_client.list_subnets.call_args_list[1][0][0]
        self.assertEqual(second_request.marker, "tok-2")

    def test_sdk_pagination_via_last_id_when_page_full(self):
        # Typed ListSubnetsResponse carries no page_info; a full page continues
        # from the last returned subnet id.
        first = _FakeSdkResponse([_FakeSdkSubnet(SUBNET_1), _FakeSdkSubnet(SUBNET_2)], None)
        second = _FakeSdkResponse([], None)
        self._fake_client.list_subnets.side_effect = [first, second]
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak",
                   HUAWEI_SECRET_KEY="test-sk",
                   HUAWEI_PROJECT_ID="test-project")
        with mock.patch.dict(os.environ, env, clear=True):
            subnets = list_subnets_via_sdk("cn-north-4", limit=2)
        self.assertEqual(subnets, [SUBNET_1, SUBNET_2])
        second_request = self._fake_client.list_subnets.call_args_list[1][0][0]
        self.assertEqual(second_request.marker, "subnet-0002")

    def test_sdk_vpc_id_forwarded(self):
        self._fake_client.list_subnets.return_value = _FakeSdkResponse(
            [_FakeSdkSubnet(SUBNET_1)], None)
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak",
                   HUAWEI_SECRET_KEY="test-sk",
                   HUAWEI_PROJECT_ID="test-project")
        with mock.patch.dict(os.environ, env, clear=True):
            list_subnets_via_sdk("cn-north-4", vpc_id="vpc-0001")
        request = self._fake_client.list_subnets.call_args_list[0][0][0]
        self.assertEqual(request.vpc_id, "vpc-0001")


class TestNormalizeAndRender(unittest.TestCase):
    def test_normalize_compacts_nested_cells(self):
        flat = normalize_subnet(SUBNET_1)
        self.assertIsInstance(flat["extra_dhcp_opts"], str)
        self.assertIn("addresstime", flat["extra_dhcp_opts"])
        self.assertIsInstance(flat["dns_list"], str)
        self.assertEqual(flat["name"], "subnet-demo-01")

    def test_normalize_empty_nested_cells(self):
        flat = normalize_subnet(SUBNET_2)
        self.assertEqual(flat["dns_list"], "[]")

    def test_table_contains_basic_info(self):
        table = render_table([SUBNET_1, SUBNET_2])
        for fragment in ("subnet-0001", "subnet-demo-01", "vpc-0001",
                         "192.168.0.0/24", "192.168.0.1", "ACTIVE",
                         "subnet-0002", "vpc-0002", "10.0.0.0/24", "PENDING"):
            self.assertIn(fragment, table)

    def test_names(self):
        self.assertEqual(
            subnet_names([SUBNET_1, SUBNET_2]), ["subnet-demo-01", "subnet-demo-02"])

    def test_names_fallback_to_id(self):
        self.assertEqual(subnet_names([{"id": "subnet-9"}]), ["subnet-9"])


class TestMain(unittest.TestCase):
    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("list_subnet.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            rc = main(argv)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    def test_table_output(self):
        rc, out, err = self._run(
            ["--region", "cn-north-4"],
            [(json.dumps({"subnets": [SUBNET_1, SUBNET_2]}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("VPC 子网（Subnet）列表", out)
        self.assertIn("subnet-0001", out)
        self.assertIn("ACTIVE", out)
        self.assertEqual(err, "")

    def test_json_output(self):
        rc, out, err = self._run(
            ["--json"],
            [(json.dumps({"subnets": [SUBNET_1]}), "", 0)])
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual(payload, [SUBNET_1])

    def test_names_only_output(self):
        rc, out, err = self._run(
            ["--names-only"],
            [(json.dumps({"subnets": [SUBNET_1, SUBNET_2]}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("subnet-demo-01", out)
        self.assertIn("subnet-demo-02", out)
        self.assertNotIn("cidr", out)

    def test_empty_subnets_message(self):
        rc, out, err = self._run(
            ["--region", "cn-south-1"],
            [(json.dumps({"subnets": []}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("无 VPC 子网（Subnet）", out)
        self.assertIn("cn-south-1", out)

    def test_empty_with_filter_message(self):
        rc, out, _ = self._run(
            ["--vpc-id", "vpc-0001"],
            [(json.dumps({"subnets": []}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("vpc_id=vpc-0001", out)

    def test_vpc_id_filter_main_forwarded(self):
        fake = FakeRunner([
            (json.dumps({"subnets": [SUBNET_1]}), "", 0)])
        with mock.patch("list_subnet.subprocess.run", fake), \
                mock.patch("sys.stdout"), \
                mock.patch("sys.stderr"):
            rc = main(["--vpc-id", "vpc-0001"])
        self.assertEqual(rc, 0)
        self.assertTrue(any("--vpc_id=vpc-0001" in part for part in fake.calls[0]))

    def test_empty_json_output(self):
        rc, out, err = self._run(
            ["--json"],
            [(json.dumps({"subnets": []}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out), [])

    def test_empty_names_only_output(self):
        rc, out, err = self._run(
            ["--names-only"],
            [(json.dumps({"subnets": []}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("共 0 个", out)
        self.assertNotIn("无 VPC 子网（Subnet）", out)

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
        with mock.patch("list_subnet.list_subnets_via_sdk",
                        side_effect=ConfigError("huaweicloudsdkvpc 未安装")):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 1)
        self.assertIn("未安装", err)

    def test_hcloud_missing_falls_back_to_sdk(self):
        with mock.patch("list_subnet.list_subnets_via_sdk",
                        return_value=[SUBNET_1]):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 0)
        self.assertIn("subnet-0001", out)

    def test_project_id_forwarded_to_sdk(self):
        with mock.patch("list_subnet.list_subnets_via_sdk",
                        return_value=[SUBNET_1]) as sdk_mock:
            rc, out, err = self._run(["--project-id", "proj-9"],
                                     [FileNotFoundError()])
        self.assertEqual(rc, 0)
        self.assertEqual(sdk_mock.call_args.kwargs.get("project_id"), "proj-9")

    def test_write_intent_argv_blocked(self):
        rc, out, err = self._run(["--operation", "DeleteSubnet"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)

    def test_write_keyword_argv_blocked(self):
        rc, out, err = self._run(["--vpc-id", "release-me"], [])
        self.assertEqual(rc, 1)
        self.assertIn("守卫拦截", err)


class TestErrorHierarchy(unittest.TestCase):
    def test_subclasses(self):
        for exc in (GuardError, ConfigError, AuthError, ApiError):
            self.assertTrue(issubclass(exc, SubnetListError))


if __name__ == "__main__":
    unittest.main()