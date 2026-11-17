import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from list_rds import (  # noqa: E402
    ALLOWED_OPERATION,
    ApiError,
    AuthError,
    ConfigError,
    GuardError,
    RdsListError,
    build_command,
    classify_hcloud_failure,
    instance_names,
    extract_instances,
    extract_json,
    filter_by_status,
    guard_operation,
    guard_write_intent,
    list_instances,
    list_instances_via_sdk,
    main,
    normalize_instance,
    render_markdown,
    render_table,
    write_markdown,
)

INSTANCE_1 = {
    "id": "rds-0001",
    "name": "rds-demo-01",
    "status": "ACTIVE",
    "datastore": {"type": "MySQL", "version": "8.0"},
    "flavor_ref": "rds.mysql.x1.large.2.ha",
    "private_ips": ["192.168.0.10"],
    "nodes": [{"availability_zone": "cn-north-4a"}],
    "vpc_id": "vpc-1",
    "enterprise_project_id": "0",
}
INSTANCE_2 = {
    "id": "rds-0002",
    "name": "rds-demo-02",
    "status": "FAILED",
    "datastore": {"type": "PostgreSQL", "version": "15"},
    "flavor_ref": "rds.pg.x1.large.2",
    "private_ips": ["192.168.0.11", "192.168.0.12"],
    "tags": {"env": "test"},
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
        self.assertFalse(guard_write_intent("--region cn-north-4 --json list instances"))
        self.assertFalse(guard_write_intent("show instance details flavors"))

    def test_create_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("CreateInstance rds-new")

    def test_delete_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--operation DeleteInstance")

    def test_mutating_verbs_blocked(self):
        for text in ("resize flavor", "restart rds-01", "stop instance",
                     "update instance name", "restore backup"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_normalized_separators_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--create-instance")
        with self.assertRaises(GuardError):
            guard_write_intent("update_instance_name")

    def test_datastore_type_value_passes(self):
        # read-only filter value must NOT trip the guard
        self.assertFalse(guard_write_intent("--datastore-type PostgreSQL"))

    def test_operation_guard_rejects_non_list(self):
        with self.assertRaises(GuardError):
            guard_operation("ShowInstance")
        self.assertTrue(guard_operation(ALLOWED_OPERATION))


class TestBuildCommand(unittest.TestCase):
    def test_basic(self):
        argv = build_command("cn-north-4")
        self.assertEqual(argv[0], "RDS")
        self.assertEqual(argv[1], "ListInstances")
        self.assertIn("--cli-region=cn-north-4", argv)
        self.assertIn("--limit=100", argv)
        self.assertIn("--offset=0", argv)

    def test_filters_appended(self):
        argv = build_command("cn-south-1", name="rds-01",
                             datastore_type="MySQL", instance_id="rds-9",
                             limit=10, offset=20)
        self.assertIn("--name=rds-01", argv)
        self.assertIn("--datastore_type=MySQL", argv)
        self.assertIn("--id=rds-9", argv)
        self.assertIn("--limit=10", argv)
        self.assertIn("--offset=20", argv)

    def test_status_never_sent_to_server(self):
        # The real RDS ListInstances API has no status parameter — the CLI
        # argv must never contain --status (QA-verified [USE_ERROR]).
        argv = build_command("cn-north-4")
        self.assertNotIn("--status=ACTIVE", argv)
        self.assertFalse(any(flag.startswith("--status") for flag in argv))

    def test_no_write_flags_ever_added(self):
        argv = build_command("cn-north-4", datastore_type="MySQL")
        for flag in argv:
            self.assertFalse(flag.lower().lstrip("-").startswith(("create", "delete", "update")))


class TestExtract(unittest.TestCase):
    def test_extract_json_plain(self):
        data = extract_json(json.dumps({"instances": []}))
        self.assertEqual(data, {"instances": []})

    def test_extract_json_with_noise(self):
        data = extract_json("WARNING some noise\n{\"a\": 1}\n")
        self.assertEqual(data, {"a": 1})

    def test_extract_json_invalid(self):
        with self.assertRaises(ApiError):
            extract_json("<html>not json</html>")

    def test_extract_instances_known_keys(self):
        for key in ("instances", "instance_list"):
            self.assertEqual(extract_instances({key: [INSTANCE_1]}), [INSTANCE_1])
        self.assertEqual(extract_instances([INSTANCE_1]), [INSTANCE_1])
        self.assertEqual(extract_instances({"total_count": 0}), [])


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
        # KooCLI usage errors exit rc=0 with [USE_ERROR] on stdout — must be
        # classified as an explicit parameter error, not a JSON parse issue.
        err = classify_hcloud_failure(
            "[USE_ERROR]Invalid parameter: status\n\n"
            "Run `hcloud RDS ListInstances --help` for details.", "", 0)
        self.assertIsInstance(err, ApiError)
        self.assertIn("参数错误", str(err))
        self.assertIn("--help", str(err))


class TestListInstances(unittest.TestCase):
    def test_single_page(self):
        fake = FakeRunner([(
            json.dumps({"instances": [INSTANCE_1, INSTANCE_2], "total_count": 2}), "", 0)])
        with mock.patch("list_rds.subprocess.run", fake):
            instances = list_instances("cn-north-4")
        self.assertEqual(instances, [INSTANCE_1, INSTANCE_2])
        self.assertEqual(len(fake.calls), 1)

    def test_pagination_via_total(self):
        page1 = {"instances": [INSTANCE_1], "total_count": 2}
        page2 = {"instances": [INSTANCE_2], "total_count": 2}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("list_rds.subprocess.run", fake):
            instances = list_instances("cn-north-4", limit=1)
        self.assertEqual(instances, [INSTANCE_1, INSTANCE_2])
        self.assertEqual(len(fake.calls), 2)
        self.assertIn("--offset=1", fake.calls[1])

    def test_pagination_via_full_page_without_total(self):
        page1 = {"instances": [INSTANCE_1]}
        page2 = {"instances": []}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("list_rds.subprocess.run", fake):
            instances = list_instances("cn-north-4", limit=1)
        self.assertEqual(instances, [INSTANCE_1])

    def test_empty_region(self):
        fake = FakeRunner([(json.dumps({"instances": [], "total_count": 0}), "", 0)])
        with mock.patch("list_rds.subprocess.run", fake):
            instances = list_instances("cn-north-4")
        self.assertEqual(instances, [])

    def test_status_filter_applied_client_side(self):
        # status must NOT be forwarded to hcloud; filtering happens locally
        # on the fetched full list (server has no status parameter).
        fake = FakeRunner([(
            json.dumps({"instances": [INSTANCE_1, INSTANCE_2], "total_count": 2}), "", 0)])
        with mock.patch("list_rds.subprocess.run", fake):
            instances = list_instances("cn-north-4", status="ACTIVE")
        self.assertEqual(instances, [INSTANCE_1])
        self.assertTrue(fake.calls)
        for call in fake.calls:
            self.assertFalse(any("--status" in part for part in call))

    def test_status_filter_case_insensitive_and_empty(self):
        fake = FakeRunner([(
            json.dumps({"instances": [INSTANCE_1, INSTANCE_2], "total_count": 2}), "", 0)])
        with mock.patch("list_rds.subprocess.run", fake):
            self.assertEqual(list_instances("cn-north-4", status="active"), [INSTANCE_1])
        fake = FakeRunner([(
            json.dumps({"instances": [INSTANCE_1, INSTANCE_2], "total_count": 2}), "", 0)])
        with mock.patch("list_rds.subprocess.run", fake):
            self.assertEqual(list_instances("cn-north-4", status="BUILDING"), [])
        fake = FakeRunner([(
            json.dumps({"instances": [INSTANCE_1, INSTANCE_2], "total_count": 2}), "", 0)])
        with mock.patch("list_rds.subprocess.run", fake):
            both = list_instances("cn-north-4")
        self.assertEqual(both, [INSTANCE_1, INSTANCE_2])

    def test_use_error_rc0_raises_api_error(self):
        # hcloud prints [USE_ERROR] on stdout with return code 0 — the
        # pipeline must fail with an explicit parameter error.
        fake = FakeRunner([(
            "[USE_ERROR]Invalid parameter: status\n\n"
            "Run `hcloud RDS ListInstances --help` for details.", "", 0)])
        with mock.patch("list_rds.subprocess.run", fake):
            with self.assertRaises(ApiError) as ctx:
                list_instances("cn-north-4")
        self.assertIn("参数错误", str(ctx.exception))

    def test_nonzero_exit_403(self):
        fake = FakeRunner([("", "403 Forbidden", 1)])
        with mock.patch("list_rds.subprocess.run", fake):
            with self.assertRaises(AuthError):
                list_instances("cn-north-4")

    def test_nonzero_exit_credentials(self):
        fake = FakeRunner([("", "ERROR: no AK configured", 1)])
        with mock.patch("list_rds.subprocess.run", fake):
            with self.assertRaises(ConfigError):
                list_instances("cn-north-4")

    def test_timeout(self):
        fake = FakeRunner([subprocess.TimeoutExpired(cmd="hcloud", timeout=120)])
        with mock.patch("list_rds.subprocess.run", fake):
            with self.assertRaises(ApiError):
                list_instances("cn-north-4")

    def test_sdk_fallback_when_hcloud_missing(self):
        with mock.patch("list_rds.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_rds.list_instances_via_sdk",
                           return_value=[INSTANCE_1, INSTANCE_2]) as sdk_mock:
            instances = list_instances("cn-north-4", status="ACTIVE")
        # status is applied client-side even on the SDK fallback path.
        self.assertEqual(instances, [INSTANCE_1])
        self.assertEqual(
            sdk_mock.call_args.kwargs.get("status"),
            None,
            "status must never be passed to the SDK path (no such request attr)",
        )

    def test_sdk_fallback_unavailable_raises_config(self):
        with mock.patch("list_rds.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_rds.list_instances_via_sdk",
                           side_effect=ConfigError("huaweicloudsdkrds 未安装")):
            with self.assertRaises(ConfigError):
                list_instances("cn-north-4")

    def test_sdk_request_has_no_status_attribute(self):
        # Regression guard: the real huaweicloudsdkrds ListInstancesRequest
        # must be constructible with exactly the kwargs the fallback path
        # sends — and `status=` must raise TypeError (no such attribute).
        try:
            from huaweicloudsdkrds.v3 import ListInstancesRequest
        except ImportError:
            self.skipTest("huaweicloudsdkrds not installed")
        request = ListInstancesRequest(
            limit=100, offset=0, id="rds-9", name="rds-01",
            datastore_type="MySQL",
        )
        self.assertIsNone(getattr(request, "status", None))
        with self.assertRaises(TypeError):
            ListInstancesRequest(status="ACTIVE")


class _FakeSdkResponse:
    def __init__(self, instances, total_count):
        self.instances = instances
        self.total_count = total_count


class _FakeSdkInstance:
    def __init__(self, payload):
        self._payload = payload

    def to_dict(self):
        return self._payload


class _FakeSdkBuilder:
    def __init__(self, test):
        self._test = test
        self._credentials = None

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
    """P2 regression: the SDK fallback must use modules that exist in the
    official huaweicloudsdk packages and wire credentials from environment
    variables (BasicCredentials has no env auto-discovery)."""

    def setUp(self):
        self._captured_credentials = None
        self._captured_region = None
        self._fake_client = mock.Mock()
        self._fake_client.list_instances.return_value = _FakeSdkResponse(
            [_FakeSdkInstance(INSTANCE_1), _FakeSdkInstance(INSTANCE_2)], 2)
        try:
            import huaweicloudsdkrds.v3 as rds_v3
        except ImportError:
            self.skipTest("huaweicloudsdkrds not installed")
        self._builder_patch = mock.patch.object(
            rds_v3.RdsClient, "new_builder",
            classmethod(lambda cls: _FakeSdkBuilder(self)))
        self._builder_patch.start()
        self.addCleanup(self._builder_patch.stop)

    def _clean_credential_env(self):
        credential_vars = (
            "HW_ACCESS_KEY", "HUAWEI_ACCESS_KEY", "HUAWEICLOUD_SDK_AK",
            "HUAWEI_CLOUD_ACCESS_KEY", "HW_SECRET_KEY", "HUAWEI_SECRET_KEY",
            "HUAWEICLOUD_SDK_SK", "HUAWEI_CLOUD_SECRET_KEY",
        )
        return {name: "" for name in credential_vars}

    def test_official_sdk_imports_resolve(self):
        # The exact import block of list_instances_via_sdk — every module
        # must exist in the official SDK (the P2 defect was nonexistent
        # huaweicloudsdkcore.http.region_config / sdk.http_client paths).
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkrds.v3 import RdsClient, ListInstancesRequest
        from huaweicloudsdkrds.v3.region.rds_region import RdsRegion
        for obj in (BasicCredentials, Region, HttpConfig,
                    RdsClient, ListInstancesRequest, RdsRegion):
            self.assertTrue(callable(obj), obj)

    def test_sdk_fallback_returns_instances_with_env_credentials(self):
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak",
                   HUAWEI_SECRET_KEY="test-sk")
        with mock.patch.dict(os.environ, env, clear=True):
            instances = list_instances_via_sdk("cn-north-4")
        self.assertEqual(instances, [INSTANCE_1, INSTANCE_2])
        credentials = self._captured_credentials
        self.assertIsNotNone(credentials)
        self.assertEqual(getattr(credentials, "ak", None), "test-ak")
        self.assertEqual(getattr(credentials, "sk", None), "test-sk")
        self.assertEqual(getattr(self._captured_region, "id", None), "cn-north-4")

    def test_sdk_fallback_missing_env_credentials_raises_config(self):
        with mock.patch.dict(os.environ, self._clean_credential_env(),
                             clear=True):
            with self.assertRaises(ConfigError) as ctx:
                list_instances_via_sdk("cn-north-4")
        message = str(ctx.exception)
        self.assertIn("AK/SK", message)
        # Must not mislead the user into thinking the SDK is missing.
        self.assertNotIn("未安装", message)

    def test_sdk_fallback_alternative_env_prefixes(self):
        env = dict(self._clean_credential_env(),
                   HW_ACCESS_KEY="alt-ak", HW_SECRET_KEY="alt-sk")
        with mock.patch.dict(os.environ, env, clear=True):
            list_instances_via_sdk("cn-north-4")
        self.assertEqual(getattr(self._captured_credentials, "ak", None), "alt-ak")

    def test_sdk_fallback_ignores_non_whitelisted_env_vars(self):
        # Credentials are read by explicit whitelist name only: a variable
        # that merely *looks* like an AK/SK (e.g. MY_ACCESS_KEY) must never be
        # harvested, even though it is the only AK present.
        env = dict(self._clean_credential_env(),
                   MY_ACCESS_KEY="bogus",
                   TEAM_SECRET_KEY="bogus")
        with mock.patch.dict(os.environ, env, clear=True):
            with self.assertRaises(ConfigError):
                list_instances_via_sdk("cn-north-4")


class TestFilterByStatus(unittest.TestCase):
    """Client-side status filter (server API has no status parameter)."""

    def test_no_status_returns_all(self):
        result = filter_by_status([INSTANCE_1, INSTANCE_2], None)
        self.assertEqual(result, [INSTANCE_1, INSTANCE_2])

    def test_exact_match(self):
        self.assertEqual(filter_by_status([INSTANCE_1, INSTANCE_2], "ACTIVE"), [INSTANCE_1])
        self.assertEqual(filter_by_status([INSTANCE_1, INSTANCE_2], "FAILED"), [INSTANCE_2])

    def test_case_insensitive(self):
        self.assertEqual(filter_by_status([INSTANCE_1], "active"), [INSTANCE_1])

    def test_no_match_returns_empty(self):
        self.assertEqual(filter_by_status([INSTANCE_1, INSTANCE_2], "BUILDING"), [])

    def test_missing_status_field_excluded(self):
        self.assertEqual(filter_by_status([{"id": "rds-x"}], "ACTIVE"), [])

    def test_input_not_mutated(self):
        source = [INSTANCE_1, INSTANCE_2]
        filter_by_status(source, "ACTIVE")
        self.assertEqual(source, [INSTANCE_1, INSTANCE_2])


class TestNormalizeAndRender(unittest.TestCase):
    def test_normalize_flattens_datastore_and_ips(self):
        flat = normalize_instance(INSTANCE_1)
        self.assertEqual(flat["engine"], "MySQL")
        self.assertEqual(flat["engineVersion"], "8.0")
        self.assertEqual(flat["privateIps"], "192.168.0.10")
        self.assertEqual(flat["availability_zone"], "cn-north-4a")

    def test_normalize_multiple_ips_joined(self):
        flat = normalize_instance(INSTANCE_2)
        self.assertEqual(flat["privateIps"], "192.168.0.11,192.168.0.12")

    def test_normalize_missing_fields_dash(self):
        flat = normalize_instance({"id": "rds-x"})
        self.assertEqual(flat["engine"], "-")
        self.assertEqual(flat["privateIps"], "-")

    def test_table_contains_basic_info(self):
        table = render_table([INSTANCE_1, INSTANCE_2])
        for fragment in ("rds-demo-01", "rds-0001", "ACTIVE", "MySQL", "8.0",
                         "rds.mysql.x1.large.2.ha", "192.168.0.10", "cn-north-4a",
                         "rds-demo-02", "PostgreSQL", "tags"):
            self.assertIn(fragment, table)

    def test_names(self):
        self.assertEqual(
            instance_names([INSTANCE_1, INSTANCE_2]), ["rds-demo-01", "rds-demo-02"])

    def test_names_fallback_to_id(self):
        self.assertEqual(instance_names([{"id": "rds-9"}]), ["rds-9"])


class TestMain(unittest.TestCase):
    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("list_rds.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            rc = main(argv)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    def test_table_output(self):
        rc, out, err = self._run(
            ["--region", "cn-north-4"],
            [(json.dumps({"instances": [INSTANCE_1, INSTANCE_2], "total_count": 2}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("RDS 实例列表", out)
        self.assertIn("rds-demo-01", out)
        self.assertIn("ACTIVE", out)
        self.assertIn("MySQL", out)
        self.assertEqual(err, "")

    def test_json_output(self):
        rc, out, err = self._run(
            ["--json"],
            [(json.dumps({"instances": [INSTANCE_1], "total_count": 1}), "", 0)])
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual(payload, [INSTANCE_1])

    def test_names_only_output(self):
        rc, out, err = self._run(
            ["--names-only"],
            [(json.dumps({"instances": [INSTANCE_1, INSTANCE_2], "total_count": 2}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("rds-demo-01", out)
        self.assertIn("rds-demo-02", out)
        self.assertNotIn("flavor_ref", out)

    def test_empty_instances_message(self):
        rc, out, err = self._run(
            ["--region", "cn-south-1"],
            [(json.dumps({"instances": [], "total_count": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("无 RDS 实例", out)
        self.assertIn("cn-south-1", out)

    def test_empty_with_filter_message(self):
        rc, out, _ = self._run(
            ["--status", "ACTIVE"],
            [(json.dumps({"instances": [], "total_count": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("status=ACTIVE", out)

    def test_status_filter_main_client_side(self):
        # End-to-end: --status ACTIVE fetches the full list from the server
        # (no --status in the CLI argv) and filters locally.
        fake = FakeRunner([
            (json.dumps({"instances": [INSTANCE_1, INSTANCE_2], "total_count": 2}), "", 0)])
        with mock.patch("list_rds.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr"):
            rc = main(["--status", "ACTIVE"])
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        self.assertEqual(rc, 0)
        self.assertIn("rds-demo-01", out)
        self.assertNotIn("rds-demo-02", out)
        for call in fake.calls:
            self.assertFalse(any("--status" in part for part in call))

    def test_empty_json_output(self):
        rc, out, err = self._run(
            ["--json"],
            [(json.dumps({"instances": [], "total_count": 0}), "", 0)])
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual(payload, [])

    def test_empty_names_only_output(self):
        rc, out, err = self._run(
            ["--names-only"],
            [(json.dumps({"instances": [], "total_count": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("共 0 个", out)
        self.assertNotIn("无 RDS 实例", out)

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
        with mock.patch("list_rds.list_instances_via_sdk",
                        side_effect=ConfigError("huaweicloudsdkrds 未安装")):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 1)
        self.assertIn("未安装", err)

    def test_hcloud_missing_falls_back_to_sdk(self):
        with mock.patch("list_rds.list_instances_via_sdk",
                        return_value=[INSTANCE_1]):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 0)
        self.assertIn("rds-demo-01", out)

    def test_write_intent_argv_blocked(self):
        rc, out, err = self._run(["--operation", "DeleteInstance"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)

    def test_write_keyword_argv_blocked(self):
        rc, out, err = self._run(["--name", "restart-me"], [])
        self.assertEqual(rc, 1)
        self.assertIn("守卫拦截", err)

    def test_status_write_word_blocked(self):
        rc, out, err = self._run(["--status", "deleting-now"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)


class TestMarkdownRender(unittest.TestCase):
    def test_document_has_title_headers_separator_and_rows(self):
        doc = render_markdown([INSTANCE_1, INSTANCE_2], "cn-north-4")
        self.assertIn("# 华为云 RDS 实例列表", doc)
        self.assertIn("cn-north-4", doc)
        for label in ("实例 ID", "名称", "状态", "引擎", "版本", "规格",
                      "私有 IP", "可用区", "区域", "创建时间"):
            self.assertIn(label, doc)
        lines = doc.splitlines()
        header = next(i for i, line in enumerate(lines)
                      if line.startswith("| 实例 ID |"))
        self.assertTrue(lines[header + 1].startswith("| --- | --- |"))
        row_lines = [line for line in lines[header + 2:] if line.startswith("| ")]
        self.assertEqual(len(row_lines), 2)
        for fragment in ("rds-0001", "rds-demo-01", "ACTIVE", "MySQL", "8.0",
                         "rds.mysql.x1.large.2.ha", "192.168.0.10",
                         "cn-north-4a", "rds-demo-02", "PostgreSQL"):
            self.assertIn(fragment, doc)

    def test_region_cell_falls_back_to_queried_region(self):
        doc = render_markdown([{"id": "rds-x", "name": "rds-x"}], "cn-south-1")
        self.assertIn("| rds-x | rds-x |", doc)
        self.assertIn("| cn-south-1 |", doc)

    def test_region_cell_uses_instance_value_when_present(self):
        doc = render_markdown([dict(INSTANCE_1, region="cn-east-3")], "cn-north-4")
        self.assertIn("| cn-east-3 |", doc)

    def test_created_at_fallback_key(self):
        doc = render_markdown([{"id": "rds-x", "created_at": "2026-01-02"}],
                              "cn-north-4")
        self.assertIn("2026-01-02", doc)

    def test_cell_escapes_pipe_and_collapses_newlines(self):
        instance = {"id": "rds|1", "name": "demo\n02", "status": "ACTIVE\r\nOK",
                    "flavor_ref": {"a": "b|c"}}
        doc = render_markdown([instance], "cn-north-4")
        self.assertIn(r"rds\|1", doc)
        self.assertIn("demo 02", doc)
        self.assertIn("ACTIVE OK", doc)
        self.assertIn(r'{"a":"b\|c"}', doc)

    def test_empty_result_has_header_and_explicit_note(self):
        doc = render_markdown([], "cn-south-1")
        self.assertIn("| 实例 ID |", doc)
        self.assertIn("| --- |", doc)
        self.assertIn("无 RDS 实例", doc)
        self.assertIn("cn-south-1", doc)
        self.assertEqual(doc.count("| 实例 ID |"), 1)


class TestMarkdownExportMain(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmpdir, True)
        self._cwd = os.getcwd()

    def tearDown(self):
        os.chdir(self._cwd)

    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("list_rds.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            try:
                rc = main(argv)
            except SystemExit as exc:
                rc = exc.code
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    @staticmethod
    def _payload():
        return (json.dumps({"instances": [INSTANCE_1, INSTANCE_2],
                            "total_count": 2}), "", 0)

    def test_format_md_writes_file(self):
        out_path = os.path.join(self.tmpdir, "rds.md")
        rc, out, err = self._run(["--format", "md", "--output", out_path],
                                 [self._payload()])
        self.assertEqual(rc, 0)
        self.assertEqual(err, "")
        self.assertIn("已生成 Markdown 文件", out)
        self.assertIn(os.path.abspath(out_path), out)
        with open(out_path, encoding="utf-8") as handle:
            content = handle.read()
        self.assertIn("# 华为云 RDS 实例列表", content)
        self.assertIn("| 实例 ID |", content)
        self.assertIn("rds-demo-01", content)
        self.assertIn("rds-demo-02", content)
        self.assertEqual([n for n in os.listdir(self.tmpdir)
                          if n.startswith(".rds-md-")], [])

    def test_output_implies_md_format(self):
        out_path = os.path.join(self.tmpdir, "implied.md")
        rc, out, _ = self._run(["--output", out_path], [self._payload()])
        self.assertEqual(rc, 0)
        self.assertTrue(os.path.isfile(out_path))

    def test_relative_output_creates_parent_directories(self):
        os.chdir(self.tmpdir)
        rc, out, _ = self._run(
            ["--format", "md", "--output", "reports/2026/rds.md"],
            [self._payload()])
        self.assertEqual(rc, 0)
        self.assertTrue(os.path.isfile(
            os.path.join(self.tmpdir, "reports", "2026", "rds.md")))
        self.assertIn("reports/2026/rds.md", out)

    def test_default_filename_uses_region_and_timestamp(self):
        os.chdir(self.tmpdir)
        rc, out, _ = self._run(
            ["--format", "md", "--region", "cn-south-1"], [self._payload()])
        self.assertEqual(rc, 0)
        files = os.listdir(self.tmpdir)
        self.assertEqual(len(files), 1)
        self.assertTrue(files[0].startswith("rds_instances_cn-south-1_"))
        self.assertTrue(files[0].endswith(".md"))

    def test_empty_result_writes_table_and_note_exit_zero(self):
        out_path = os.path.join(self.tmpdir, "empty.md")
        rc, out, err = self._run(
            ["--format", "md", "--output", out_path],
            [(json.dumps({"instances": [], "total_count": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertEqual(err, "")
        self.assertIn("无 RDS 实例", out)
        with open(out_path, encoding="utf-8") as handle:
            content = handle.read()
        self.assertIn("| 实例 ID |", content)
        self.assertIn("无 RDS 实例", content)

    def test_write_failure_reports_error_nonzero_and_no_partial_file(self):
        out_path = os.path.join(self.tmpdir, "broken.md")
        with mock.patch("list_rds.os.replace", side_effect=OSError("disk full")):
            rc, out, err = self._run(
                ["--format", "md", "--output", out_path], [self._payload()])
        self.assertEqual(rc, 1)
        self.assertIn("[错误]", err)
        self.assertIn("Markdown 文件写出失败", err)
        self.assertFalse(os.path.exists(out_path))
        self.assertEqual([n for n in os.listdir(self.tmpdir)
                          if n.startswith(".rds-md-")], [])

    def test_uncreatable_parent_directory_reports_error(self):
        blocker = os.path.join(self.tmpdir, "blocker")
        with open(blocker, "w", encoding="utf-8") as handle:
            handle.write("x")
        out_path = os.path.join(blocker, "rds.md")
        rc, out, err = self._run(
            ["--format", "md", "--output", out_path], [self._payload()])
        self.assertEqual(rc, 1)
        self.assertIn("Markdown 文件写出失败", err)

    def test_md_mutually_exclusive_with_json(self):
        rc, out, err = self._run(["--format", "md", "--json"], [])
        self.assertEqual(rc, 2)
        self.assertIn("不能同时使用", err)

    def test_output_mutually_exclusive_with_names_only(self):
        rc, out, err = self._run(
            ["--output", os.path.join(self.tmpdir, "x.md"), "--names-only"], [])
        self.assertEqual(rc, 2)
        self.assertIn("不能同时使用", err)

    def test_explicit_table_format_matches_default_output(self):
        rc, out, _ = self._run(["--format", "table"], [self._payload()])
        self.assertEqual(rc, 0)
        self.assertIn("RDS 实例列表（共 2 个，完整字段）", out)
        self.assertFalse(os.path.exists(
            os.path.join(self.tmpdir, "rds_instances.md")))

    def test_output_path_with_mutating_word_is_allowed(self):
        out_path = os.path.join(self.tmpdir, "update-reports", "rds.md")
        rc, out, err = self._run(["--output", out_path], [self._payload()])
        self.assertEqual(rc, 0)
        self.assertEqual(err, "")
        self.assertTrue(os.path.isfile(out_path))

    def test_write_markdown_is_atomic_on_success(self):
        out_path = os.path.join(self.tmpdir, "atomic.md")
        write_markdown("hello", out_path)
        with open(out_path, encoding="utf-8") as handle:
            self.assertEqual(handle.read(), "hello")
        self.assertEqual([n for n in os.listdir(self.tmpdir)
                          if n.startswith(".rds-md-")], [])


class TestErrorHierarchy(unittest.TestCase):
    def test_subclasses(self):
        for exc in (GuardError, ConfigError, AuthError, ApiError):
            self.assertTrue(issubclass(exc, RdsListError))


if __name__ == "__main__":
    unittest.main()
