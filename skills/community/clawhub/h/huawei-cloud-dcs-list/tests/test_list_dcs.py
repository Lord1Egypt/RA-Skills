import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from list_dcs import (  # noqa: E402
    ALLOWED_OPERATION,
    MD_COLUMNS,
    MD_HEADERS,
    MODE_JSON,
    MODE_MD,
    MODE_NAMES,
    MODE_TABLE,
    ApiError,
    AuthError,
    ConfigError,
    DcsListError,
    GuardError,
    OutputError,
    build_command,
    classify_hcloud_failure,
    extract_instances,
    extract_json,
    guard_argv,
    guard_operation,
    guard_write_intent,
    instance_names,
    list_instances,
    list_instances_via_sdk,
    main,
    normalize_instance,
    normalized_row,
    render_markdown,
    render_table,
    resolve_mode,
    sort_instances,
    write_markdown_file,
)

INSTANCE_1 = {
    "name": "cache-demo-01",
    "instance_id": "55f47f3d-0001-4a54-a362-a07c9d7f7a02",
    "engine": "Redis",
    "engine_version": "5.0",
    "capacity": 4,
    "spec_code": "redis.ha.xu1.large.r2.4-h",
    "status": "RUNNING",
    "port": 6379,
    "ip": "192.168.0.10",
    "domain_name": "redis-xxx.dcs.huawei.com",
    "no_password_access": "true",
    "enable_ssl": False,
    "charging_mode": "prePaid",
    "vpc_name": "vpc-demo",
    "vpc_id": "vpc-0001",
    "subnet_id": "subnet-0001",
    "security_group_id": "sg-0001",
    "az_codes": ["cn-north-4a"],
    "user_name": "r00256513",
    "tags": [{"key": "env", "value": "prod"}],
    "enterprise_project_id": "0",
    "created_at": "2026-01-01T00:00:00+08:00",
    "updated_at": "2026-01-02T00:00:00+08:00",
}
INSTANCE_2 = {
    "name": "cache-demo-02",
    "instance_id": "55f47f3d-0002-4a54-a362-a07c9d7f7a03",
    "engine": "Memcached",
    "engine_version": "1.5.17",
    "capacity": 2,
    "status": "ERROR",
    "port": 11211,
    "ip": "192.168.0.11",
    "az_codes": ["cn-north-4b"],
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
        self.assertFalse(guard_write_intent("--region cn-north-4 --names-only list instances"))
        self.assertFalse(guard_write_intent("show instance details"))

    def test_create_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("CreateInstance cache-new")

    def test_delete_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--operation DeleteInstance")

    def test_batch_delete_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("BatchDeleteInstances")

    def test_mutating_verbs_blocked(self):
        for text in ("resize instance", "restart cache-01", "update instance name",
                     "flush instance", "clear cache", "restore backup",
                     "upgrade instance", "reset instance password",
                     "backup instance", "freeze instance", "release instance"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_normalized_separators_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--create-instance")
        with self.assertRaises(GuardError):
            guard_write_intent("resize_instance")

    def test_readonly_filter_value_passes(self):
        self.assertFalse(guard_write_intent("--status RUNNING"))
        self.assertFalse(guard_write_intent("--name cache-analytics"))

    def test_operation_guard_rejects_non_list(self):
        with self.assertRaises(GuardError):
            guard_operation("ShowInstance")
        self.assertTrue(guard_operation(ALLOWED_OPERATION))


class TestBuildCommand(unittest.TestCase):
    def test_basic(self):
        argv = build_command("cn-north-4")
        self.assertEqual(argv[0], "DCS")
        self.assertEqual(argv[1], "ListInstances")
        self.assertIn("--cli-region=cn-north-4", argv)
        self.assertIn("--limit=100", argv)
        self.assertIn("--offset=0", argv)

    def test_filters_forwarded_to_server(self):
        # name / instance_id / ip / status / tags are all real server-side
        # ListInstances query parameters (hcloud DCS ListInstances --help).
        argv = build_command("cn-north-4", name="cache", instance_id="id-9",
                             ip="192.168.0.10", status="RUNNING",
                             tags="env=prod")
        self.assertIn("--name=cache", argv)
        self.assertIn("--instance_id=id-9", argv)
        self.assertIn("--ip=192.168.0.10", argv)
        self.assertIn("--status=RUNNING", argv)
        self.assertIn("--tags=env=prod", argv)

    def test_page_params(self):
        argv = build_command("cn-north-4", limit=500, offset=500)
        self.assertIn("--limit=500", argv)
        self.assertIn("--offset=500", argv)

    def test_no_write_flags_ever_added(self):
        argv = build_command("cn-north-4", name="cache", status="RUNNING")
        for flag in argv:
            self.assertFalse(
                flag.lower().lstrip("-").startswith(
                    ("create", "delete", "update", "resize", "restart")))


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

    def test_extract_json_ignores_trailing_diagnostic_table(self):
        stdout = (
            '{"instances": [], "instance_num": 0}\n'
            "Failed to get terminal width, use default value 120.\n"
            "+--------+--------+\n"
            "| Key    | Value  |\n"
            "+--------+--------+\n"
        )
        self.assertEqual(extract_json(stdout), {"instances": [], "instance_num": 0})

    def test_extract_json_error_body_with_diagnostic_table(self):
        # DCS error body + KooCLI diagnostic table, rc=0: the first complete
        # JSON object must be decoded and surfaced as an explicit API error.
        stdout = (
            '{"error_msg": "Invalid status parameter in the request.", '
            '"error_code": "DCS.4062"}\n'
            "Failed to get terminal width, use default value 120.\n"
            "+--------+--------+\n"
            "| Key    | Value  |\n"
            "+--------+--------+\n"
        )
        with self.assertRaises(ApiError) as ctx:
            extract_json(stdout)
        self.assertIn("DCS.4062", str(ctx.exception))
        self.assertIn("Invalid status parameter", str(ctx.exception))

    def test_extract_instances_known_keys(self):
        for key in ("instances", "instance_list"):
            self.assertEqual(extract_instances({key: [INSTANCE_1]}), [INSTANCE_1])
        self.assertEqual(extract_instances([INSTANCE_1]), [INSTANCE_1])
        self.assertEqual(extract_instances({"instance_num": 0}), [])


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
            "[USE_ERROR]Invalid parameter: name\n\n"
            "Run `hcloud DCS ListInstances --help` for details.", "", 0)
        self.assertIsInstance(err, ApiError)
        self.assertIn("参数错误", str(err))
        self.assertIn("--help", str(err))


class TestListInstances(unittest.TestCase):
    def test_single_page(self):
        fake = FakeRunner([(
            json.dumps({"instances": [INSTANCE_1, INSTANCE_2], "instance_num": 2}), "", 0)])
        with mock.patch("list_dcs.subprocess.run", fake):
            instances = list_instances("cn-north-4")
        self.assertEqual(instances, [INSTANCE_1, INSTANCE_2])
        self.assertEqual(len(fake.calls), 1)

    def test_pagination_via_instance_num(self):
        # instance_num drives the paging decision (hcloud/SDK response field).
        page1 = {"instances": [INSTANCE_1], "instance_num": 2}
        page2 = {"instances": [INSTANCE_2], "instance_num": 2}
        fake = FakeRunner([(json.dumps(page1), "", 0),
                           (json.dumps(page2), "", 0)])
        with mock.patch("list_dcs.subprocess.run", fake):
            instances = list_instances("cn-north-4", limit=1)
        self.assertEqual(instances, [INSTANCE_1, INSTANCE_2])
        self.assertEqual(len(fake.calls), 2)
        self.assertIn("--offset=1", fake.calls[1])

    def test_pagination_via_full_page_without_total(self):
        # No instance_num in the payload: a full page keeps paging until a
        # short/empty page arrives.
        page1 = {"instances": [INSTANCE_1]}
        page2 = {"instances": []}
        fake = FakeRunner([(json.dumps(page1), "", 0),
                           (json.dumps(page2), "", 0)])
        with mock.patch("list_dcs.subprocess.run", fake):
            instances = list_instances("cn-north-4", limit=1)
        self.assertEqual(instances, [INSTANCE_1])

    def test_empty_region(self):
        fake = FakeRunner([(json.dumps({"instances": [], "instance_num": 0}), "", 0)])
        with mock.patch("list_dcs.subprocess.run", fake):
            instances = list_instances("cn-north-4")
        self.assertEqual(instances, [])

    def test_filters_forwarded_to_cli(self):
        fake = FakeRunner([(
            json.dumps({"instances": [INSTANCE_1], "instance_num": 1}), "", 0)])
        with mock.patch("list_dcs.subprocess.run", fake):
            list_instances("cn-north-4", name="cache", instance_id="id-9",
                           ip="192.168.0.10", status="RUNNING", tags="env=prod")
        call = fake.calls[0]
        self.assertTrue(any("--name=cache" in part for part in call))
        self.assertTrue(any("--instance_id=id-9" in part for part in call))
        self.assertTrue(any("--ip=192.168.0.10" in part for part in call))
        self.assertTrue(any("--status=RUNNING" in part for part in call))
        self.assertTrue(any("--tags=env=prod" in part for part in call))

    def test_use_error_rc0_raises_api_error(self):
        fake = FakeRunner([(
            "[USE_ERROR]Invalid parameter: name\n\n"
            "Run `hcloud DCS ListInstances --help` for details.", "", 0)])
        with mock.patch("list_dcs.subprocess.run", fake):
            with self.assertRaises(ApiError) as ctx:
                list_instances("cn-north-4")
        self.assertIn("参数错误", str(ctx.exception))

    def test_error_body_rc0_with_diagnostic_table_raises_api_error(self):
        # Regression: DCS parameter errors come back as an error body on
        # stdout with rc=0 plus a trailing diagnostic table; they must be
        # reported as an API error (with error_code), not a parse failure.
        fake = FakeRunner([(
            '{"error_msg": "Invalid status parameter in the request.", '
            '"error_code": "DCS.4062"}\n'
            "Failed to get terminal width, use default value 120.\n"
            "+--------+--------+\n"
            "| Key    | Value  |\n"
            "+--------+--------+\n", "", 0)])
        with mock.patch("list_dcs.subprocess.run", fake):
            with self.assertRaises(ApiError) as ctx:
                list_instances("cn-north-4", status="INVALID_STATUS")
        self.assertIn("DCS.4062", str(ctx.exception))
        self.assertIn("Invalid status parameter", str(ctx.exception))

    def test_nonzero_exit_403(self):
        fake = FakeRunner([("", "403 Forbidden", 1)])
        with mock.patch("list_dcs.subprocess.run", fake):
            with self.assertRaises(AuthError):
                list_instances("cn-north-4")

    def test_nonzero_exit_credentials(self):
        fake = FakeRunner([("", "ERROR: no AK configured", 1)])
        with mock.patch("list_dcs.subprocess.run", fake):
            with self.assertRaises(ConfigError):
                list_instances("cn-north-4")

    def test_timeout(self):
        fake = FakeRunner([subprocess.TimeoutExpired(cmd="hcloud", timeout=120)])
        with mock.patch("list_dcs.subprocess.run", fake):
            with self.assertRaises(ApiError):
                list_instances("cn-north-4")

    def test_sdk_fallback_when_hcloud_missing(self):
        with mock.patch("list_dcs.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_dcs.list_instances_via_sdk",
                           return_value=[INSTANCE_1, INSTANCE_2]) as sdk_mock:
            instances = list_instances("cn-north-4", name="cache",
                                       project_id="proj-9")
        self.assertEqual(instances, [INSTANCE_1, INSTANCE_2])
        self.assertEqual(sdk_mock.call_args.kwargs.get("name"), "cache")
        self.assertEqual(sdk_mock.call_args.kwargs.get("project_id"), "proj-9")

    def test_sdk_fallback_unavailable_raises_config(self):
        with mock.patch("list_dcs.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_dcs.list_instances_via_sdk",
                           side_effect=ConfigError("huaweicloudsdkdcs 未安装")):
            with self.assertRaises(ConfigError):
                list_instances("cn-north-4")

    def test_sdk_request_signature(self):
        # Regression guard: the real huaweicloudsdkdcs ListInstancesRequest
        # must accept exactly the kwargs the fallback path sends, and reject
        # unknown kwargs.
        try:
            from huaweicloudsdkdcs.v2 import ListInstancesRequest
        except ImportError:
            self.skipTest("huaweicloudsdkdcs not installed")
        request = ListInstancesRequest(
            limit=100, offset=0, name="cache", instance_id="id-9",
            ip="192.168.0.10", status="RUNNING", tags="env=prod")
        self.assertEqual(request.name, "cache")
        self.assertEqual(request.limit, 100)
        with self.assertRaises(TypeError):
            ListInstancesRequest(no_such_param=1)


class _FakeSdkResponse:
    def __init__(self, instances, instance_num):
        self.instances = instances
        self.instance_num = instance_num


class _FakeSdkInstance:
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
    """The SDK fallback must use modules that exist in the official SDK and
    wire credentials from whitelisted environment variables (no env
    enumeration)."""

    def setUp(self):
        self._captured_credentials = None
        self._captured_region = None
        self._fake_client = mock.Mock()
        self._fake_client.list_instances.return_value = _FakeSdkResponse(
            [_FakeSdkInstance(INSTANCE_1), _FakeSdkInstance(INSTANCE_2)], 2)
        try:
            import huaweicloudsdkdcs.v2 as dcs_v2
        except ImportError:
            self.skipTest("huaweicloudsdkdcs not installed")
        self._builder_patch = mock.patch.object(
            dcs_v2.DcsClient, "new_builder",
            classmethod(lambda cls: _FakeSdkBuilder(self)))
        self._builder_patch.start()
        self.addCleanup(self._builder_patch.stop)

    def _clean_credential_env(self):
        # Whitelist-only credential cleanup: blank exactly the env names the
        # script may read — os.environ is never enumerated (skillspector E2).
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
        from huaweicloudsdkdcs.v2 import DcsClient, ListInstancesRequest
        from huaweicloudsdkdcs.v2.region.dcs_region import DcsRegion
        for obj in (BasicCredentials, Region, HttpConfig,
                    DcsClient, ListInstancesRequest, DcsRegion):
            self.assertTrue(callable(obj), obj)

    def test_sdk_fallback_returns_instances_with_env_credentials(self):
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak",
                   HUAWEI_SECRET_KEY="test-sk",
                   HUAWEI_PROJECT_ID="test-project")
        with mock.patch.dict(os.environ, env, clear=True):
            instances = list_instances_via_sdk("cn-north-4")
        self.assertEqual(instances, [INSTANCE_1, INSTANCE_2])
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
            list_instances_via_sdk("cn-north-4", project_id="cli-project")
        self.assertEqual(
            getattr(self._captured_credentials, "project_id", None), "cli-project")

    def test_sdk_fallback_missing_env_credentials_raises_config(self):
        env = dict(self._clean_credential_env(), HUAWEI_PROJECT_ID="test-project")
        with mock.patch.dict(os.environ, env, clear=True):
            with self.assertRaises(ConfigError) as ctx:
                list_instances_via_sdk("cn-north-4")
        message = str(ctx.exception)
        self.assertIn("AK/SK", message)
        # Must not mislead the user into thinking the SDK is missing.
        self.assertNotIn("未安装", message)

    def test_sdk_fallback_missing_project_id_raises_config(self):
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak", HUAWEI_SECRET_KEY="test-sk")
        with mock.patch.dict(os.environ, env, clear=True):
            with self.assertRaises(ConfigError) as ctx:
                list_instances_via_sdk("cn-north-4")
        self.assertIn("project_id", str(ctx.exception))

    def test_sdk_fallback_alternative_env_prefixes(self):
        env = dict(self._clean_credential_env(),
                   HW_ACCESS_KEY="alt-ak", HW_SECRET_KEY="alt-sk",
                   HUAWEI_PROJECT_ID="test-project")
        with mock.patch.dict(os.environ, env, clear=True):
            list_instances_via_sdk("cn-north-4")
        self.assertEqual(getattr(self._captured_credentials, "ak", None), "alt-ak")

    def test_sdk_pagination_via_instance_num(self):
        first = _FakeSdkResponse([_FakeSdkInstance(INSTANCE_1)], 2)
        second = _FakeSdkResponse([_FakeSdkInstance(INSTANCE_2)], 2)
        self._fake_client.list_instances.side_effect = [first, second]
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak",
                   HUAWEI_SECRET_KEY="test-sk",
                   HUAWEI_PROJECT_ID="test-project")
        with mock.patch.dict(os.environ, env, clear=True):
            instances = list_instances_via_sdk("cn-north-4", limit=1)
        self.assertEqual(instances, [INSTANCE_1, INSTANCE_2])
        second_request = self._fake_client.list_instances.call_args_list[1][0][0]
        self.assertEqual(second_request.offset, 1)

    def test_sdk_filters_forwarded(self):
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak",
                   HUAWEI_SECRET_KEY="test-sk",
                   HUAWEI_PROJECT_ID="test-project")
        with mock.patch.dict(os.environ, env, clear=True):
            list_instances_via_sdk("cn-north-4", name="cache", status="RUNNING")
        request = self._fake_client.list_instances.call_args_list[0][0][0]
        self.assertEqual(request.name, "cache")
        self.assertEqual(request.status, "RUNNING")


class TestNormalizeAndRender(unittest.TestCase):
    def test_normalize_flattens_lists(self):
        flat = normalize_instance(INSTANCE_1)
        self.assertEqual(flat["az_codes"], "cn-north-4a")
        self.assertEqual(flat["tags"], "env=prod")

    def test_normalize_id_fallback(self):
        flat = normalize_instance({"id": "raw-9"})
        self.assertEqual(flat["instance_id"], "raw-9")

    def test_normalize_missing_fields(self):
        flat = normalize_instance({"instance_id": "id-x"})
        self.assertNotIn("az_codes", flat)

    def test_table_contains_basic_info(self):
        table = render_table([INSTANCE_1, INSTANCE_2])
        for fragment in ("cache-demo-01", "55f47f3d-0001", "Redis", "5.0",
                         "4", "RUNNING", "192.168.0.10", "6379",
                         "cn-north-4a", "cache-demo-02", "Memcached",
                         "ERROR", "11211"):
            self.assertIn(fragment, table)

    def test_names(self):
        self.assertEqual(
            instance_names([INSTANCE_1, INSTANCE_2]),
            ["cache-demo-01", "cache-demo-02"])

    def test_names_fallback_to_instance_id(self):
        self.assertEqual(instance_names([{"instance_id": "id-9"}]), ["id-9"])


class TestSortInstances(unittest.TestCase):
    """Client-side --sort-by ordering (ascending, stable)."""

    def test_sort_by_name_case_insensitive(self):
        instances = [
            {"name": "beta", "instance_id": "id-2"},
            {"name": "Alpha", "instance_id": "id-1"},
            {"name": "cache", "instance_id": "id-3"},
        ]
        ordered = sort_instances(instances, "name")
        self.assertEqual([i["name"] for i in ordered], ["Alpha", "beta", "cache"])

    def test_sort_by_name_falls_back_to_instance_id(self):
        instances = [
            {"instance_id": "id-z"},
            {"name": "alpha", "instance_id": "id-a"},
            {"name": "", "instance_id": "id-b"},
        ]
        ordered = sort_instances(instances, "name")
        self.assertEqual([i["instance_id"] for i in ordered],
                         ["id-a", "id-b", "id-z"])

    def test_sort_by_name_is_stable_for_ties(self):
        instances = [
            {"name": "same", "instance_id": "first"},
            {"name": "Same", "instance_id": "second"},
        ]
        ordered = sort_instances(instances, "name")
        self.assertEqual([i["instance_id"] for i in ordered],
                         ["first", "second"])

    def test_sort_by_created_ascending_missing_last(self):
        instances = [
            {"name": "new", "created_at": "2026-03-01T00:00:00+08:00"},
            {"name": "missing"},
            {"name": "old", "created_at": "2026-01-01T00:00:00+08:00"},
        ]
        ordered = sort_instances(instances, "created")
        self.assertEqual([i["name"] for i in ordered], ["old", "new", "missing"])

    def test_sort_by_created_is_stable_for_ties(self):
        instances = [
            {"name": "first", "created_at": "2026-01-01T00:00:00+08:00"},
            {"name": "second", "created_at": "2026-01-01T00:00:00+08:00"},
        ]
        ordered = sort_instances(instances, "created")
        self.assertEqual([i["name"] for i in ordered], ["first", "second"])

    def test_no_sort_preserves_api_order(self):
        instances = [{"name": "b"}, {"name": "a"}]
        ordered = sort_instances(instances, None)
        self.assertEqual([i["name"] for i in ordered], ["b", "a"])
        self.assertIsNot(ordered, instances)


class TestMain(unittest.TestCase):
    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("list_dcs.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            rc = main(argv)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    def test_default_output_is_names_list(self):
        # Default (no flag) and --names-only both print the instance-name list.
        for argv in ([], ["--names-only"]):
            rc, out, err = self._run(
                argv,
                [(json.dumps({"instances": [INSTANCE_1, INSTANCE_2],
                              "instance_num": 2}), "", 0)])
            self.assertEqual(rc, 0)
            self.assertIn("DCS 实例名称列表", out)
            self.assertIn("cache-demo-01", out)
            self.assertIn("cache-demo-02", out)
            self.assertNotIn("instance_id", out)

    def test_names_only_output(self):
        rc, out, err = self._run(
            ["--names-only"],
            [(json.dumps({"instances": [INSTANCE_1, INSTANCE_2],
                          "instance_num": 2}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("cache-demo-01", out)
        self.assertNotIn("spec_code", out)

    def test_table_output(self):
        rc, out, err = self._run(
            ["--table"],
            [(json.dumps({"instances": [INSTANCE_1, INSTANCE_2],
                          "instance_num": 2}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("DCS 实例列表", out)
        self.assertIn("cache-demo-01", out)
        self.assertIn("RUNNING", out)
        self.assertIn("192.168.0.10", out)
        self.assertEqual(err, "")

    def test_json_output(self):
        rc, out, err = self._run(
            ["--json"],
            [(json.dumps({"instances": [INSTANCE_1], "instance_num": 1}), "", 0)])
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual(payload, [INSTANCE_1])

    def test_empty_names_message(self):
        # Empty region under the default names mode: explicit hint, exit 0.
        rc, out, err = self._run(
            ["--region", "cn-south-1"],
            [(json.dumps({"instances": [], "instance_num": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("无 DCS 实例", out)
        self.assertIn("cn-south-1", out)

    def test_empty_table_message(self):
        rc, out, err = self._run(
            ["--table"],
            [(json.dumps({"instances": [], "instance_num": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("无 DCS 实例", out)

    def test_empty_with_filter_message(self):
        rc, out, _ = self._run(
            ["--table", "--status", "RUNNING"],
            [(json.dumps({"instances": [], "instance_num": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("status=RUNNING", out)

    def test_name_filter_forwarded(self):
        # --name is a real server-side query parameter — it is forwarded.
        fake = FakeRunner([(
            json.dumps({"instances": [INSTANCE_1], "instance_num": 1}), "", 0)])
        with mock.patch("list_dcs.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr"):
            rc = main(["--name", "cache-demo-01"])
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        self.assertEqual(rc, 0)
        self.assertTrue(any("--name=cache-demo-01" in part for part in fake.calls[0]))

    def test_name_equal_client_side_exact(self):
        # --name-equal drops the fuzzy server param and matches exactly.
        fake = FakeRunner([(
            json.dumps({"instances": [INSTANCE_1, INSTANCE_2],
                        "instance_num": 2}), "", 0)])
        with mock.patch("list_dcs.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr"):
            rc = main(["--name-equal", "--name", "CACHE-DEMO-01"])
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        self.assertEqual(rc, 0)
        self.assertIn("cache-demo-01", out)
        self.assertNotIn("- cache-demo-02", out)
        self.assertFalse(any("--name=" in part for part in fake.calls[0]))

    def test_sort_by_invalid_value_lists_choices(self):
        # ``created`` must never reach the write-intent guard as ``create``;
        # an unknown value is still rejected with the allowed choices.
        rc, out, err = self._run(["--sort-by", "create"], [])
        self.assertEqual(rc, 1)
        self.assertIn("name", err)
        self.assertIn("created", err)
        self.assertNotIn("写操作意图", err)

    def test_sort_by_unknown_value_rejected(self):
        rc, out, err = self._run(["--sort-by", "size"], [])
        self.assertEqual(rc, 1)
        self.assertIn("--sort-by", err)
        self.assertIn("name", err)
        self.assertIn("created", err)

    def test_sort_by_name_orders_names_output(self):
        rc, out, err = self._run(
            ["--sort-by", "name", "--names-only"],
            [(json.dumps({"instances": [
                {"name": "zeta", "instance_id": "id-z"},
                {"name": "Alpha", "instance_id": "id-a"},
                {"name": "beta", "instance_id": "id-b"},
            ], "instance_num": 3}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertLess(out.index("- Alpha"), out.index("- beta"))
        self.assertLess(out.index("- beta"), out.index("- zeta"))

    def test_sort_by_created_orders_json_output(self):
        rc, out, err = self._run(
            ["--json", "--sort-by", "created"],
            [(json.dumps({"instances": [
                {"name": "new", "created_at": "2026-03-01T00:00:00+08:00"},
                {"name": "missing"},
                {"name": "old", "created_at": "2026-01-01T00:00:00+08:00"},
            ], "instance_num": 3}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertEqual([i["name"] for i in json.loads(out)],
                         ["old", "new", "missing"])

    def test_sort_by_created_orders_table_and_md_output(self):
        payload = json.dumps({"instances": [
            {"name": "new", "instance_id": "id-n",
             "created_at": "2026-03-01T00:00:00+08:00"},
            {"name": "old", "instance_id": "id-o",
             "created_at": "2026-01-01T00:00:00+08:00"},
        ], "instance_num": 2})
        for argv in (["--table", "--sort-by", "created"],
                     ["--md", "--sort-by", "created"],
                     ["--format", "md", "--sort-by", "created"]):
            rc, out, err = self._run(argv, [(payload, "", 0)])
            self.assertEqual(rc, 0, err)
            self.assertLess(out.index("id-o"), out.index("id-n"))

    def test_sort_by_name_still_applies_after_name_equal_filter(self):
        rc, out, err = self._run(
            ["--names-only", "--name-equal", "--name", "cAcHe-A",
             "--sort-by", "name"],
            [(json.dumps({"instances": [
                {"name": "cache-b"},
                {"name": "Cache-A"},
                {"name": "cache-a"},
                {"name": "other"},
            ], "instance_num": 4}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertLess(out.index("- Cache-A"), out.index("- cache-a"))
        self.assertNotIn("- cache-b", out)
        self.assertNotIn("- other", out)

    def test_sort_by_created_stays_ordered_across_pages(self):
        page1 = json.dumps({"instances": [
            {"name": "p1-new", "created_at": "2026-04-01T00:00:00+08:00"},
            {"name": "p1-old", "created_at": "2026-02-01T00:00:00+08:00"},
        ], "instance_num": 4})
        page2 = json.dumps({"instances": [
            {"name": "p2-new", "created_at": "2026-05-01T00:00:00+08:00"},
            {"name": "p2-old", "created_at": "2026-01-01T00:00:00+08:00"},
        ], "instance_num": 4})
        rc, out, err = self._run(
            ["--json", "--sort-by", "created", "--page-size", "2"],
            [(page1, "", 0), (page2, "", 0)])
        self.assertEqual(rc, 0)
        self.assertEqual([i["name"] for i in json.loads(out)],
                         ["p2-old", "p1-old", "p1-new", "p2-new"])

    def test_sort_by_absent_keeps_api_order(self):
        rc, out, err = self._run(
            ["--json"],
            [(json.dumps({"instances": [
                {"name": "zeta"}, {"name": "alpha"},
            ], "instance_num": 2}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertEqual([i["name"] for i in json.loads(out)],
                         ["zeta", "alpha"])

    def test_guard_argv_strips_sort_by_value(self):
        # ``created`` contains ``create``; the value must be exempted while
        # every other argument is still scanned.
        self.assertFalse(guard_argv(["--sort-by", "created"]))
        self.assertFalse(guard_argv(["--sort-by=created"]))
        self.assertFalse(guard_argv(["--sort_by", "name"]))
        with self.assertRaises(GuardError):
            guard_argv(["--sort-by", "created", "--name", "delete-me"])

    def test_page_size_out_of_range(self):
        rc, out, err = self._run(["--page-size", "0"], [])
        self.assertEqual(rc, 1)
        self.assertIn("page-size", err)

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
        with mock.patch("list_dcs.list_instances_via_sdk",
                        side_effect=ConfigError("huaweicloudsdkdcs 未安装")):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 1)
        self.assertIn("未安装", err)

    def test_hcloud_missing_falls_back_to_sdk(self):
        with mock.patch("list_dcs.list_instances_via_sdk",
                        return_value=[INSTANCE_1]):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 0)
        self.assertIn("cache-demo-01", out)

    def test_project_id_forwarded_to_sdk(self):
        with mock.patch("list_dcs.list_instances_via_sdk",
                        return_value=[INSTANCE_1]) as sdk_mock:
            rc, out, err = self._run(["--project-id", "proj-9"],
                                     [FileNotFoundError()])
        self.assertEqual(rc, 0)
        self.assertEqual(sdk_mock.call_args.kwargs.get("project_id"), "proj-9")

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


class TestMarkdownOutput(unittest.TestCase):
    """Markdown mode (--md / --format md / --md-output)."""

    HEADER_LINE = "| " + " | ".join([
        "名称", "ID", "引擎", "版本", "容量", "规格", "状态",
        "连接地址", "端口", "可用区"]) + " |"
    SEPARATOR_LINE = "| " + " | ".join(["---"] * 10) + " |"
    PAYLOAD = json.dumps({"instances": [INSTANCE_1, INSTANCE_2],
                          "instance_num": 2})

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="dcs-md-test-")
        self.addCleanup(shutil.rmtree, self.tmpdir, True)

    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("list_dcs.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            rc = main(argv)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    # --- column contract -------------------------------------------------
    def test_headers_are_the_export_markdown_ten_columns(self):
        # Must stay byte-identical to huawei-cloud-dcs-export-markdown.
        self.assertEqual(MD_HEADERS, [
            "名称", "ID", "引擎", "版本", "容量", "规格", "状态",
            "连接地址", "端口", "可用区"])
        self.assertEqual(len(MD_HEADERS), 10)
        self.assertEqual(len(MD_COLUMNS), len(MD_HEADERS))

    def test_row_column_order_and_values(self):
        row = normalized_row(INSTANCE_1)
        self.assertEqual(len(row), 10)
        self.assertEqual(row[0], "cache-demo-01")
        self.assertEqual(row[1], "55f47f3d-0001-4a54-a362-a07c9d7f7a02")
        self.assertEqual(row[2], "Redis")
        self.assertEqual(row[3], "5.0")
        self.assertEqual(row[4], "4")
        self.assertEqual(row[5], "redis.ha.xu1.large.r2.4-h")
        self.assertEqual(row[6], "RUNNING")
        self.assertEqual(row[7], "192.168.0.10")
        self.assertEqual(row[8], "6379")
        self.assertEqual(row[9], "cn-north-4a")

    def test_missing_fields_render_dash(self):
        row = normalized_row({"instance_id": "id-only"})
        self.assertEqual(row, ["-", "id-only", "-", "-", "-", "-", "-",
                               "-", "-", "-"])

    def test_pipe_and_newline_are_escaped(self):
        row = normalized_row({"name": "a|b", "status": "RUN\nNING",
                              "spec_code": "x\r\ny"})
        self.assertEqual(row[0], "a\\|b")
        self.assertEqual(row[6], "RUN NING")
        self.assertEqual(row[5], "x  y")

    def test_render_markdown_table_shape(self):
        text = render_markdown([INSTANCE_1, INSTANCE_2])
        lines = text.split("\n")
        self.assertEqual(len(lines), 4)  # header + separator + 2 rows
        self.assertEqual(lines[0], self.HEADER_LINE)
        self.assertEqual(lines[1], self.SEPARATOR_LINE)
        self.assertTrue(lines[2].startswith("| cache-demo-01 |"))
        self.assertTrue(lines[2].endswith(" |"))
        self.assertEqual(lines[2].count(" | "), 9)  # 10 cells

    # --- CLI behaviour ---------------------------------------------------
    def test_md_flag_prints_valid_table(self):
        rc, out, err = self._run(["--md"], [(self.PAYLOAD, "", 0)])
        self.assertEqual(rc, 0)
        self.assertEqual(err, "")
        lines = out.strip("\n").split("\n")
        self.assertEqual(lines[0], self.HEADER_LINE)
        self.assertEqual(lines[1], self.SEPARATOR_LINE)
        self.assertIn("cache-demo-01", lines[2])
        self.assertIn("cache-demo-02", lines[3])

    def test_format_md_matches_md_flag(self):
        _, out_flag, _ = self._run(["--md"], [(self.PAYLOAD, "", 0)])
        _, out_fmt, _ = self._run(["--format", "md"], [(self.PAYLOAD, "", 0)])
        self.assertEqual(out_flag, out_fmt)

    def test_format_values_select_each_mode(self):
        cases = {
            "names": "DCS 实例名称列表",
            "table": "完整字段",
            "md": "| 名称 | ID |",
        }
        for fmt, marker in cases.items():
            rc, out, _ = self._run(["--format", fmt], [(self.PAYLOAD, "", 0)])
            self.assertEqual(rc, 0)
            self.assertIn(marker, out)
        rc, out, _ = self._run(["--format", "json"], [(self.PAYLOAD, "", 0)])
        self.assertEqual(json.loads(out), [INSTANCE_1, INSTANCE_2])

    def test_md_combines_with_filters_and_page_size(self):
        fake = FakeRunner([(self.PAYLOAD, "", 0)])
        with mock.patch("list_dcs.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, mock.patch("sys.stderr"):
            rc = main(["--md", "--status", "RUNNING", "--page-size", "10"])
        self.assertEqual(rc, 0)
        call = " ".join(fake.calls[0])
        self.assertIn("--status=RUNNING", call)
        self.assertIn("--limit=10", call)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        self.assertIn(self.HEADER_LINE, out)

    def test_empty_md_prints_hint_without_header_or_file(self):
        target = os.path.join(self.tmpdir, "empty.md")
        rc, out, err = self._run(
            ["--md", "--md-output", target, "--status", "RUNNING"],
            [(json.dumps({"instances": [], "instance_num": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("无 DCS 实例", out)
        self.assertIn("status=RUNNING", out)
        self.assertNotIn("|", out)
        self.assertFalse(os.path.exists(target))

    def test_md_output_writes_identical_content(self):
        target = os.path.join(self.tmpdir, "dcs.md")
        rc, out, err = self._run(
            ["--md", "--md-output", target], [(self.PAYLOAD, "", 0)])
        self.assertEqual(rc, 0)
        with open(target, encoding="utf-8") as handle:
            written = handle.read()
        self.assertEqual(written, out)
        self.assertIn("[已写入]", err)

    def test_md_output_write_failure_is_nonzero_and_leaves_nothing(self):
        target = os.path.join(self.tmpdir, "sub", "dcs.md")
        with mock.patch("list_dcs.os.replace", side_effect=OSError("disk full")):
            rc, out, err = self._run(
                ["--md", "--md-output", target], [(self.PAYLOAD, "", 0)])
        self.assertEqual(rc, 1)
        self.assertIn("[错误]", err)
        self.assertIn("未留下残缺文件", err)
        self.assertFalse(os.path.exists(target))
        self.assertEqual(
            [n for n in os.listdir(os.path.dirname(target))
             if n.endswith(".tmp")], [])

    def test_md_output_rejected_outside_md_mode(self):
        rc, out, err = self._run(
            ["--table", "--md-output", os.path.join(self.tmpdir, "x.md")], [])
        self.assertEqual(rc, 1)
        self.assertIn("--md-output", err)

    def test_md_mode_still_blocks_write_intent(self):
        rc, out, err = self._run(["--md", "--name", "delete-me"], [])
        self.assertEqual(rc, 1)
        self.assertIn("守卫拦截", err)

    def test_md_output_path_write_word_not_blocked(self):
        # The local output path is not a DCS operation.
        target = os.path.join(self.tmpdir, "dcs-backup-restore.md")
        rc, out, err = self._run(
            ["--md", "--md-output", target], [(self.PAYLOAD, "", 0)])
        self.assertEqual(rc, 0)
        self.assertTrue(os.path.exists(target))

    def test_guard_argv_strips_md_output_value(self):
        self.assertFalse(guard_argv(["--md", "--md-output", "/tmp/delete-me.md"]))
        self.assertFalse(guard_argv(["--md", "--md-output=/tmp/delete-me.md"]))
        with self.assertRaises(GuardError):
            guard_argv(["--md", "--name", "delete-me"])

    # --- legacy outputs stay byte-identical ------------------------------
    def test_legacy_outputs_unchanged(self):
        rc, names_out, _ = self._run([], [(self.PAYLOAD, "", 0)])
        self.assertEqual(rc, 0)
        self.assertEqual(names_out,
                         "Region cn-north-4 的 DCS 实例名称列表（共 2 个）：\n"
                         "- cache-demo-01\n- cache-demo-02\n")
        rc, table_out, _ = self._run(["--table"], [(self.PAYLOAD, "", 0)])
        self.assertEqual(rc, 0)
        self.assertEqual(table_out,
                         "Region cn-north-4 的 DCS 实例列表（共 2 个，完整字段）：\n"
                         + render_table([INSTANCE_1, INSTANCE_2]) + "\n")
        rc, json_out, _ = self._run(["--json"], [(self.PAYLOAD, "", 0)])
        self.assertEqual(rc, 0)
        self.assertEqual(json_out,
                         json.dumps([INSTANCE_1, INSTANCE_2],
                                    ensure_ascii=False, indent=2) + "\n")


class TestResolveMode(unittest.TestCase):
    def test_default_is_names(self):
        self.assertEqual(resolve_mode(), MODE_NAMES)

    def test_flag_precedence_is_backwards_compatible(self):
        # json > names-only > table > md > --format > default
        self.assertEqual(resolve_mode("md", as_json=True, as_md=True), MODE_JSON)
        self.assertEqual(resolve_mode("md", names_only=True, as_table=True),
                         MODE_NAMES)
        self.assertEqual(resolve_mode("md", as_table=True, as_md=True), MODE_TABLE)
        self.assertEqual(resolve_mode("table", as_md=True), MODE_MD)

    def test_format_value_used_without_flags(self):
        self.assertEqual(resolve_mode("md"), MODE_MD)
        self.assertEqual(resolve_mode("table"), MODE_TABLE)
        self.assertEqual(resolve_mode("json"), MODE_JSON)


class TestMarkdownFileHelper(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="dcs-md-helper-")
        self.addCleanup(shutil.rmtree, self.tmpdir, True)

    def test_writes_and_creates_parent_dir(self):
        target = os.path.join(self.tmpdir, "a", "b", "out.md")
        path = write_markdown_file("| a |", target)
        self.assertEqual(path, os.path.abspath(target))
        with open(target, encoding="utf-8") as handle:
            self.assertEqual(handle.read(), "| a |\n")

    def test_failure_raises_output_error_and_cleans_temp(self):
        target = os.path.join(self.tmpdir, "out.md")
        with mock.patch("list_dcs.os.replace", side_effect=OSError("boom")):
            with self.assertRaises(OutputError):
                write_markdown_file("| a |", target)
        self.assertEqual([n for n in os.listdir(self.tmpdir)
                          if n.endswith(".tmp")], [])
        self.assertFalse(os.path.exists(target))

    def test_empty_path_rejected(self):
        with self.assertRaises(OutputError):
            write_markdown_file("| a |", "")


class TestErrorHierarchy(unittest.TestCase):
    def test_subclasses(self):
        for exc in (GuardError, ConfigError, AuthError, ApiError):
            self.assertTrue(issubclass(exc, DcsListError))


if __name__ == "__main__":
    unittest.main()
