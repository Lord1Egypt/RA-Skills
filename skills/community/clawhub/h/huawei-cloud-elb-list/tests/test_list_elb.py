import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from list_elb import (  # noqa: E402
    ALLOWED_OPERATION,
    DEFAULT_MD_OUT,
    ApiError,
    AuthError,
    ConfigError,
    GuardError,
    ElbListError,
    build_command,
    classify_hcloud_failure,
    extract_json,
    extract_loadbalancers,
    guard_operation,
    guard_write_intent,
    list_loadbalancers,
    list_loadbalancers_via_sdk,
    loadbalancer_names,
    main,
    render_markdown,
    render_table,
    standardize_loadbalancers,
    write_markdown_file,
)

LOADBALANCER_1 = {
    "id": "lb-0001",
    "name": "lb-demo-01",
    "description": "demo load balancer",
    "provisioning_status": "ACTIVE",
    "operating_status": "ONLINE",
    "admin_state_up": True,
    "guaranteed": True,
    "vpc_id": "vpc-0001",
    "vip_address": "192.168.0.10",
    "vip_subnet_cidr_id": "subnet-0001",
    "vip_port_id": "port-0001",
    "ipv6_vip_address": "2001:db8::1",
    "ipv6_vip_virsubnet_id": "subnet-0002",
    "availability_zone_list": ["cn-north-4a", "cn-north-4b"],
    "enterprise_project_id": "0",
    "loadbalancer_type": "L7",
    "eips": [
        {"eip_id": "eip-0001", "eip_address": "1.2.3.4", "ip_version": 4}
    ],
    "publicips": [
        {"public_id": "p-0001", "public_address": "1.2.3.4", "ip_version": 4}
    ],
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-02T00:00:00",
}
LOADBALANCER_2 = {
    "id": "lb-0002",
    "name": "lb-demo-02",
    "provisioning_status": "PENDING_DELETE",
    "operating_status": "FROZEN",
    "guaranteed": False,
    "vpc_id": "vpc-0002",
    "vip_address": "192.168.1.10",
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
        self.assertFalse(guard_write_intent("--region cn-north-4 --json list elb"))
        self.assertFalse(guard_write_intent("show load balancer details"))

    def test_create_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("CreateLoadBalancer lb-new")

    def test_delete_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--operation DeleteLoadBalancer")

    def test_mutating_verbs_blocked(self):
        for text in ("create listener", "delete pool",
                     "detach member from pool", "release load balancer",
                     "change charge mode", "update listener",
                     "clone load balancer", "restore load balancer",
                     "enable deletion protection", "disable log"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_normalized_separators_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--create-elb")
        with self.assertRaises(GuardError):
            guard_write_intent("update_loadbalancer_name")

    def test_read_filter_value_passes(self):
        self.assertFalse(guard_write_intent("--provisioning_status ACTIVE"))
        self.assertFalse(guard_write_intent("--vip-address 192.168.0.10"))
        self.assertFalse(guard_write_intent("--vpc-id vpc-0001"))

    def test_operation_guard_rejects_non_list(self):
        with self.assertRaises(GuardError):
            guard_operation("ShowLoadBalancer")
        self.assertTrue(guard_operation(ALLOWED_OPERATION))


class TestBuildCommand(unittest.TestCase):
    def test_basic(self):
        argv = build_command("cn-north-4")
        self.assertEqual(argv[0], "ELB")
        self.assertEqual(argv[1], "ListLoadbalancers")
        self.assertIn("--cli-region=cn-north-4", argv)
        self.assertIn("--limit=100", argv)
        self.assertFalse(any(flag.startswith("--marker") for flag in argv))

    def test_marker_appended(self):
        argv = build_command("cn-north-4", marker="tok-123", limit=10)
        self.assertIn("--marker=tok-123", argv)
        self.assertIn("--limit=10", argv)

    def test_filters_forwarded_server_side(self):
        argv = build_command("cn-south-1", lb_id="lb-9", name="lb-demo",
                             vpc_id="vpc-1", provisioning_status="ACTIVE",
                             operating_status="ONLINE", enterprise_project_id="0",
                             vip_address="192.168.0.10", limit=10)
        # Array-typed ListLoadbalancers filters must use the KooCLI indexed
        # form --key.1=value; a bare --key=value is rejected by KooCLI.
        self.assertIn("--id.1=lb-9", argv)
        self.assertIn("--name.1=lb-demo", argv)
        self.assertIn("--vpc_id.1=vpc-1", argv)
        self.assertIn("--provisioning_status.1=ACTIVE", argv)
        self.assertIn("--operating_status.1=ONLINE", argv)
        self.assertIn("--enterprise_project_id.1=0", argv)
        self.assertIn("--vip_address.1=192.168.0.10", argv)
        self.assertIn("--limit=10", argv)
        # Scalars keep the plain form.
        self.assertNotIn("--limit.1=10", argv)

    def test_filters_never_use_bare_single_value_form(self):
        # Regression: KooCLI rejects a bare --key=value for array-typed filters.
        argv = build_command("cn-south-1", lb_id="lb-9", name="lb-demo",
                             vpc_id="vpc-1", provisioning_status="ACTIVE",
                             operating_status="ONLINE", enterprise_project_id="0",
                             vip_address="192.168.0.10")
        for bare in ("--id=lb-9", "--name=lb-demo", "--vpc_id=vpc-1",
                     "--provisioning_status=ACTIVE", "--operating_status=ONLINE",
                     "--enterprise_project_id=0", "--vip_address=192.168.0.10"):
            self.assertNotIn(bare, argv)

    def test_no_write_flags_ever_added(self):
        argv = build_command("cn-north-4", provisioning_status="ACTIVE")
        for flag in argv:
            self.assertFalse(flag.lower().lstrip("-").startswith(
                ("create", "delete", "update", "associate", "release", "clone")))


class TestExtract(unittest.TestCase):
    def test_extract_json_plain(self):
        data = extract_json(json.dumps({"loadbalancers": []}))
        self.assertEqual(data, {"loadbalancers": []})

    def test_extract_json_with_noise(self):
        data = extract_json("WARNING some noise\n{\"a\": 1}\n")
        self.assertEqual(data, {"a": 1})

    def test_extract_json_invalid(self):
        with self.assertRaises(ApiError):
            extract_json("<html>not json</html>")

    def test_extract_loadbalancers_known_keys(self):
        for key in ("loadbalancers", "load_balancers"):
            self.assertEqual(extract_loadbalancers({key: [LOADBALANCER_1]}), [LOADBALANCER_1])
        self.assertEqual(extract_loadbalancers([LOADBALANCER_1]), [LOADBALANCER_1])
        self.assertEqual(extract_loadbalancers({"page_info": {}}), [])


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
            "[USE_ERROR]Invalid parameter: provisioning_status\n\n"
            "Run `hcloud ELB ListLoadbalancers --help` for details.", "", 0)
        self.assertIsInstance(err, ApiError)
        self.assertIn("参数错误", str(err))
        self.assertIn("--help", str(err))


class TestListLoadbalancers(unittest.TestCase):
    def test_single_page(self):
        fake = FakeRunner([(
            json.dumps({"loadbalancers": [LOADBALANCER_1, LOADBALANCER_2]}), "", 0)])
        with mock.patch("list_elb.subprocess.run", fake):
            loadbalancers = list_loadbalancers("cn-north-4")
        self.assertEqual(loadbalancers, [LOADBALANCER_1, LOADBALANCER_2])
        self.assertEqual(len(fake.calls), 1)

    def test_pagination_via_next_marker(self):
        page1 = {"loadbalancers": [LOADBALANCER_1],
                 "page_info": {"next_marker": "tok-2", "current_count": 1}}
        page2 = {"loadbalancers": [LOADBALANCER_2],
                 "page_info": {"next_marker": None, "current_count": 1}}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("list_elb.subprocess.run", fake):
            loadbalancers = list_loadbalancers("cn-north-4", limit=1)
        self.assertEqual(loadbalancers, [LOADBALANCER_1, LOADBALANCER_2])
        self.assertEqual(len(fake.calls), 2)
        self.assertIn("--marker=tok-2", fake.calls[1])

    def test_pagination_via_full_page_without_marker(self):
        page1 = {"loadbalancers": [LOADBALANCER_1]}
        page2 = {"loadbalancers": []}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("list_elb.subprocess.run", fake):
            loadbalancers = list_loadbalancers("cn-north-4", limit=1)
        self.assertEqual(loadbalancers, [LOADBALANCER_1])

    def test_empty_region(self):
        fake = FakeRunner([(json.dumps({"loadbalancers": []}), "", 0)])
        with mock.patch("list_elb.subprocess.run", fake):
            loadbalancers = list_loadbalancers("cn-north-4")
        self.assertEqual(loadbalancers, [])

    def test_filters_forwarded_to_cli(self):
        fake = FakeRunner([(
            json.dumps({"loadbalancers": [LOADBALANCER_1]}), "", 0)])
        with mock.patch("list_elb.subprocess.run", fake):
            list_loadbalancers("cn-north-4", name="lb-demo-01", lb_id="lb-0001",
                               vpc_id="vpc-0001", provisioning_status="ACTIVE",
                               operating_status="ONLINE")
        call = fake.calls[0]
        self.assertTrue(any("--name.1=lb-demo-01" in part for part in call))
        self.assertTrue(any("--id.1=lb-0001" in part for part in call))
        self.assertTrue(any("--vpc_id.1=vpc-0001" in part for part in call))
        self.assertTrue(any("--provisioning_status.1=ACTIVE" in part for part in call))
        self.assertTrue(any("--operating_status.1=ONLINE" in part for part in call))

    def test_use_error_rc0_raises_api_error(self):
        fake = FakeRunner([(
            "[USE_ERROR]Invalid parameter: provisioning_status\n\n"
            "Run `hcloud ELB ListLoadbalancers --help` for details.", "", 0)])
        with mock.patch("list_elb.subprocess.run", fake):
            with self.assertRaises(ApiError) as ctx:
                list_loadbalancers("cn-north-4")
        self.assertIn("参数错误", str(ctx.exception))

    def test_nonzero_exit_403(self):
        fake = FakeRunner([("", "403 Forbidden", 1)])
        with mock.patch("list_elb.subprocess.run", fake):
            with self.assertRaises(AuthError):
                list_loadbalancers("cn-north-4")

    def test_nonzero_exit_credentials(self):
        fake = FakeRunner([("", "ERROR: no AK configured", 1)])
        with mock.patch("list_elb.subprocess.run", fake):
            with self.assertRaises(ConfigError):
                list_loadbalancers("cn-north-4")

    def test_timeout(self):
        fake = FakeRunner([subprocess.TimeoutExpired(cmd="hcloud", timeout=120)])
        with mock.patch("list_elb.subprocess.run", fake):
            with self.assertRaises(ApiError):
                list_loadbalancers("cn-north-4")

    def test_sdk_fallback_when_hcloud_missing(self):
        with mock.patch("list_elb.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_elb.list_loadbalancers_via_sdk",
                           return_value=[LOADBALANCER_1, LOADBALANCER_2]) as sdk_mock:
            loadbalancers = list_loadbalancers(
                "cn-north-4", name="lb-demo-01", lb_id="lb-1",
                provisioning_status="ACTIVE", project_id="proj-1")
        self.assertEqual(loadbalancers, [LOADBALANCER_1, LOADBALANCER_2])
        self.assertEqual(sdk_mock.call_args.kwargs.get("name"), "lb-demo-01")
        self.assertEqual(sdk_mock.call_args.kwargs.get("project_id"), "proj-1")

    def test_sdk_fallback_unavailable_raises_config(self):
        with mock.patch("list_elb.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_elb.list_loadbalancers_via_sdk",
                           side_effect=ConfigError("huaweicloudsdkelb 未安装")):
            with self.assertRaises(ConfigError):
                list_loadbalancers("cn-north-4")

    def test_sdk_request_signature(self):
        # Regression guard: the real huaweicloudsdkelb ListLoadBalancersRequest
        # must be constructible with exactly the kwargs the fallback path sends.
        try:
            from huaweicloudsdkelb.v3 import ListLoadBalancersRequest
        except ImportError:
            self.skipTest("huaweicloudsdkelb not installed")
        request = ListLoadBalancersRequest(
            limit=100, marker=None, id=["lb-9"], name=["lb-demo"],
            vpc_id=["vpc-1"], provisioning_status=["ACTIVE"],
            operating_status=["ONLINE"], enterprise_project_id=["0"],
            vip_address=["192.168.0.10"],
        )
        self.assertEqual(request.id, ["lb-9"])
        self.assertEqual(request.name, ["lb-demo"])
        self.assertEqual(request.vpc_id, ["vpc-1"])
        self.assertEqual(request.provisioning_status, ["ACTIVE"])
        self.assertEqual(request.operating_status, ["ONLINE"])
        self.assertEqual(request.vip_address, ["192.168.0.10"])
        with self.assertRaises(TypeError):
            ListLoadBalancersRequest(no_such_param=1)


class _FakeSdkResponse:
    def __init__(self, loadbalancers, next_marker):
        self.loadbalancers = loadbalancers

        class _PageInfo:
            pass

        page = _PageInfo()
        page.next_marker = next_marker
        self.page_info = page


class _FakeSdkLoadBalancer:
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
    """Regression: the SDK fallback must use modules that exist in the official
    huaweicloudsdkelb package and wire credentials (including the project id
    required by /v3/{project_id}/elb/loadbalancers) from environment variables
    (BasicCredentials has no env auto-discovery)."""

    def setUp(self):
        self._captured_credentials = None
        self._captured_region = None
        self._fake_client = mock.Mock()
        self._fake_client.list_load_balancers.return_value = _FakeSdkResponse(
            [_FakeSdkLoadBalancer(LOADBALANCER_1), _FakeSdkLoadBalancer(LOADBALANCER_2)], None)
        try:
            import huaweicloudsdkelb.v3 as elb_v3
        except ImportError:
            self.skipTest("huaweicloudsdkelb not installed")
        self._builder_patch = mock.patch.object(
            elb_v3.ElbClient, "new_builder",
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
        from huaweicloudsdkelb.v3 import ElbClient, ListLoadBalancersRequest
        from huaweicloudsdkelb.v3.region.elb_region import ElbRegion
        for obj in (BasicCredentials, Region, HttpConfig,
                    ElbClient, ListLoadBalancersRequest, ElbRegion):
            self.assertTrue(callable(obj), obj)

    def test_sdk_fallback_returns_loadbalancers_with_env_credentials(self):
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak",
                   HUAWEI_SECRET_KEY="test-sk",
                   HUAWEI_PROJECT_ID="test-project")
        with mock.patch.dict(os.environ, env, clear=True):
            loadbalancers = list_loadbalancers_via_sdk("cn-north-4")
        self.assertEqual(loadbalancers, [LOADBALANCER_1, LOADBALANCER_2])
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
            list_loadbalancers_via_sdk("cn-north-4", project_id="cli-project")
        self.assertEqual(
            getattr(self._captured_credentials, "project_id", None), "cli-project")

    def test_sdk_fallback_missing_env_credentials_raises_config(self):
        env = dict(self._clean_credential_env(), HUAWEI_PROJECT_ID="test-project")
        with mock.patch.dict(os.environ, env, clear=True):
            with self.assertRaises(ConfigError) as ctx:
                list_loadbalancers_via_sdk("cn-north-4")
        message = str(ctx.exception)
        self.assertIn("AK/SK", message)
        self.assertNotIn("未安装", message)

    def test_sdk_fallback_missing_project_id_raises_config(self):
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak", HUAWEI_SECRET_KEY="test-sk")
        with mock.patch.dict(os.environ, env, clear=True):
            with self.assertRaises(ConfigError) as ctx:
                list_loadbalancers_via_sdk("cn-north-4")
        self.assertIn("project_id", str(ctx.exception))

    def test_sdk_pagination_via_next_marker(self):
        first = _FakeSdkResponse([_FakeSdkLoadBalancer(LOADBALANCER_1)], "tok-2")
        second = _FakeSdkResponse([_FakeSdkLoadBalancer(LOADBALANCER_2)], None)
        self._fake_client.list_load_balancers.side_effect = [first, second]
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak",
                   HUAWEI_SECRET_KEY="test-sk",
                   HUAWEI_PROJECT_ID="test-project")
        with mock.patch.dict(os.environ, env, clear=True):
            loadbalancers = list_loadbalancers_via_sdk("cn-north-4")
        self.assertEqual(loadbalancers, [LOADBALANCER_1, LOADBALANCER_2])
        second_request = self._fake_client.list_load_balancers.call_args_list[1][0][0]
        self.assertEqual(second_request.marker, "tok-2")


class TestStandardizeAndRender(unittest.TestCase):
    def test_standardize_keeps_id_and_name_only(self):
        standardized = standardize_loadbalancers([LOADBALANCER_1])
        self.assertEqual(standardized, [{"id": "lb-0001", "name": "lb-demo-01"}])

    def test_standardize_name_falls_back_to_id(self):
        self.assertEqual(standardize_loadbalancers([{"id": "lb-9"}]),
                         [{"id": "lb-9", "name": "lb-9"}])

    def test_standardize_missing_fields_become_dash(self):
        self.assertEqual(standardize_loadbalancers([{}]),
                         [{"id": "-", "name": "-"}])

    def test_table_is_id_name_only(self):
        table = render_table([LOADBALANCER_1, LOADBALANCER_2])
        for fragment in ("lb-0001", "lb-demo-01", "lb-0002", "lb-demo-02"):
            self.assertIn(fragment, table)
        for dropped in ("ACTIVE", "ONLINE", "vpc-0001", "192.168.0.10",
                        "2024-01-01T00:00:00", "provisioning_status"):
            self.assertNotIn(dropped, table)

    def test_table_header_exactly_two_columns(self):
        header = render_table([LOADBALANCER_1]).splitlines()[0]
        self.assertEqual(header.split(), ["id", "name"])

    def test_markdown_table_contains_standardized_rows(self):
        markdown = render_markdown([LOADBALANCER_1, LOADBALANCER_2], region="cn-north-4")
        self.assertIn("| ID | 名称 |", markdown)
        self.assertIn("| lb-0001 | lb-demo-01 |", markdown)
        self.assertIn("| lb-0002 | lb-demo-02 |", markdown)
        self.assertIn("cn-north-4", markdown)
        for dropped in ("ACTIVE", "vpc-0001", "192.168.0.10"):
            self.assertNotIn(dropped, markdown)

    def test_markdown_empty_document(self):
        markdown = render_markdown([], region="cn-south-1")
        self.assertIn("| ID | 名称 |", markdown)
        self.assertIn("共 0 个", markdown)

    def test_markdown_escapes_pipe(self):
        markdown = render_markdown([{"id": "lb-1", "name": "a|b"}])
        self.assertIn("| lb-1 | a\\|b |", markdown)

    def test_names(self):
        self.assertEqual(
            loadbalancer_names([LOADBALANCER_1, LOADBALANCER_2]),
            ["lb-demo-01", "lb-demo-02"])

    def test_names_fallback_to_id(self):
        self.assertEqual(loadbalancer_names([{"id": "lb-9"}]), ["lb-9"])
        self.assertEqual(loadbalancer_names([{}]), ["-"])


class TestMain(unittest.TestCase):
    def _run(self, argv, results):
        fake = FakeRunner(results)
        argv = list(argv)
        # Keep stdout-only assertions from writing elb-list.md into the repo;
        # Markdown-specific tests pass an explicit --md-out instead.
        if "--no-md" not in argv and "--md-out" not in argv:
            argv.append("--no-md")
        with mock.patch("list_elb.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            rc = main(argv)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    def test_table_output(self):
        rc, out, err = self._run(
            ["--region", "cn-north-4"],
            [(json.dumps({"loadbalancers": [LOADBALANCER_1, LOADBALANCER_2]}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("弹性负载均衡（ELB）列表", out)
        self.assertIn("lb-0001", out)
        self.assertIn("lb-demo-01", out)
        # Standardized: no full-field columns leak into the default table.
        self.assertNotIn("ACTIVE", out)
        self.assertNotIn("vip_address", out)
        self.assertEqual(err, "")

    def test_markdown_file_generated_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            md_path = os.path.join(tmp, "elb-list.md")
            rc, out, err = self._run(
                ["--region", "cn-north-4", "--md-out", md_path],
                [(json.dumps({"loadbalancers": [LOADBALANCER_1, LOADBALANCER_2]}), "", 0)])
            self.assertEqual(rc, 0)
            self.assertIn(md_path, out)
            with open(md_path, encoding="utf-8") as handle:
                content = handle.read()
            self.assertIn("| ID | 名称 |", content)
            self.assertIn("| lb-0001 | lb-demo-01 |", content)
            self.assertIn("| lb-0002 | lb-demo-02 |", content)
            self.assertNotIn("ACTIVE", content)

    def test_markdown_file_creates_missing_parent_dir(self):
        # Regression: `--md-out inventory/elb-list.md` must create the missing
        # `inventory/` parent directory instead of failing with ENOENT.
        with tempfile.TemporaryDirectory() as tmp:
            md_path = os.path.join(tmp, "inventory", "elb-list.md")
            rc, out, err = self._run(
                ["--region", "cn-north-4", "--md-out", md_path],
                [(json.dumps({"loadbalancers": [LOADBALANCER_1]}), "", 0)])
            self.assertEqual(rc, 0)
            self.assertEqual(err, "")
            self.assertTrue(os.path.exists(md_path))
            with open(md_path, encoding="utf-8") as handle:
                self.assertIn("| lb-0001 | lb-demo-01 |", handle.read())

    def test_write_markdown_file_creates_nested_parent_dirs(self):
        with tempfile.TemporaryDirectory() as tmp:
            md_path = os.path.join(tmp, "a", "b", "elb-list.md")
            returned = write_markdown_file(md_path, "| ID | 名称 |\n")
            self.assertEqual(returned, md_path)
            self.assertTrue(os.path.isfile(md_path))
            with open(md_path, encoding="utf-8") as handle:
                self.assertEqual(handle.read(), "| ID | 名称 |\n")

    def test_write_markdown_file_unwritable_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            blocker = os.path.join(tmp, "blocker")
            with open(blocker, "w", encoding="utf-8") as handle:
                handle.write("x")
            # `blocker` is a file → using it as a parent directory must fail.
            with self.assertRaises(ElbListError):
                write_markdown_file(os.path.join(blocker, "elb-list.md"), "x")

    def test_no_md_suppresses_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            md_path = os.path.join(tmp, "elb-list.md")
            rc, out, err = self._run(
                ["--no-md", "--md-out", md_path],
                [(json.dumps({"loadbalancers": [LOADBALANCER_1]}), "", 0)])
            self.assertEqual(rc, 0)
            self.assertFalse(os.path.exists(md_path))
            self.assertNotIn("Markdown 文档已生成", out)

    def test_json_mode_never_writes_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            md_path = os.path.join(tmp, "elb-list.md")
            rc, out, err = self._run(
                ["--json", "--md-out", md_path],
                [(json.dumps({"loadbalancers": [LOADBALANCER_1]}), "", 0)])
            self.assertEqual(rc, 0)
            self.assertEqual(json.loads(out), [LOADBALANCER_1])
            self.assertFalse(os.path.exists(md_path))

    def test_default_md_path_constant(self):
        self.assertEqual(DEFAULT_MD_OUT, "elb-list.md")

    def test_json_output(self):
        rc, out, err = self._run(
            ["--json"],
            [(json.dumps({"loadbalancers": [LOADBALANCER_1]}), "", 0)])
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual(payload, [LOADBALANCER_1])

    def test_names_only_output(self):
        rc, out, err = self._run(
            ["--names-only"],
            [(json.dumps({"loadbalancers": [LOADBALANCER_1, LOADBALANCER_2]}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("lb-demo-01", out)
        self.assertIn("lb-demo-02", out)
        self.assertNotIn("vip_address", out)

    def test_empty_instances_message(self):
        rc, out, err = self._run(
            ["--region", "cn-south-1"],
            [(json.dumps({"loadbalancers": []}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("无负载均衡器（ELB）", out)
        self.assertIn("cn-south-1", out)

    def test_empty_with_filter_message(self):
        rc, out, _ = self._run(
            ["--provisioning-status", "ACTIVE"],
            [(json.dumps({"loadbalancers": []}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("provisioning_status=ACTIVE", out)

    def test_status_filter_main_forwarded(self):
        fake = FakeRunner([
            (json.dumps({"loadbalancers": [LOADBALANCER_1]}), "", 0)])
        with mock.patch("list_elb.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr"):
            rc = main(["--provisioning-status", "ACTIVE", "--no-md"])
        self.assertEqual(rc, 0)
        self.assertTrue(any("--provisioning_status.1=ACTIVE" in part for part in fake.calls[0]))

    def test_empty_json_output(self):
        rc, out, err = self._run(
            ["--json"],
            [(json.dumps({"loadbalancers": []}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out), [])

    def test_empty_names_only_output(self):
        rc, out, err = self._run(
            ["--names-only"],
            [(json.dumps({"loadbalancers": []}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("共 0 个", out)
        self.assertNotIn("无负载均衡器（ELB）", out)

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
        with mock.patch("list_elb.list_loadbalancers_via_sdk",
                        side_effect=ConfigError("huaweicloudsdkelb 未安装")):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 1)
        self.assertIn("未安装", err)

    def test_hcloud_missing_falls_back_to_sdk(self):
        with mock.patch("list_elb.list_loadbalancers_via_sdk",
                        return_value=[LOADBALANCER_1]):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 0)
        self.assertIn("lb-0001", out)

    def test_project_id_forwarded_to_sdk(self):
        with mock.patch("list_elb.list_loadbalancers_via_sdk",
                        return_value=[LOADBALANCER_1]) as sdk_mock:
            rc, out, err = self._run(["--project-id", "proj-9"],
                                     [FileNotFoundError()])
        self.assertEqual(rc, 0)
        self.assertEqual(sdk_mock.call_args.kwargs.get("project_id"), "proj-9")

    def test_write_intent_argv_blocked(self):
        rc, out, err = self._run(["--operation", "DeleteLoadBalancer"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)

    def test_write_keyword_argv_blocked(self):
        rc, out, err = self._run(["--id", "release-me"], [])
        self.assertEqual(rc, 1)
        self.assertIn("守卫拦截", err)

    def test_status_write_word_blocked(self):
        rc, out, err = self._run(["--provisioning-status", "deleting-now"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)


class TestErrorHierarchy(unittest.TestCase):
    def test_subclasses(self):
        for exc in (GuardError, ConfigError, AuthError, ApiError):
            self.assertTrue(issubclass(exc, ElbListError))


if __name__ == "__main__":
    unittest.main()