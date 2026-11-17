import datetime
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from list_rds_export_markdown import (  # noqa: E402
    ALLOWED_OPERATION,
    ApiError,
    AuthError,
    ConfigError,
    GuardError,
    RdsListError,
    SortError,
    build_command,
    classify_hcloud_failure,
    extract_instances,
    extract_json,
    filter_by_status,
    guard_operation,
    guard_write_intent,
    instance_names,
    list_instances,
    list_instances_via_sdk,
    main,
    normalize_instance,
    parse_created,
    render_markdown,
    resolve_sort_by,
    scrub_read_only_values,
    sort_instances,
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
    "created": "2026-01-02T03:04:05+0800",
}
INSTANCE_2 = {
    "id": "rds-0002",
    "name": "rds-demo-02",
    "status": "FAILED",
    "datastore": {"type": "PostgreSQL", "version": "15"},
    "flavor_ref": "rds.pg.x1.large.2",
    "private_ips": ["192.168.0.11", "192.168.0.12"],
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
        self.assertFalse(guard_write_intent("--region cn-north-4 list instances"))
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

    def test_operation_guard_rejects_non_list(self):
        with self.assertRaises(GuardError):
            guard_operation("ShowInstance")
        self.assertTrue(guard_operation(ALLOWED_OPERATION))

    def test_scrub_drops_output_path_value(self):
        # A local path containing a mutating word must not trip the guard.
        argv = ["--output", "downloads/update-report.md", "--region", "cn-north-4"]
        self.assertNotIn("update-report", scrub_read_only_values(argv))
        self.assertFalse(guard_write_intent(scrub_read_only_values(argv)))

    def test_scrub_drops_name_status_values(self):
        argv = ["--name", "restart-me", "--status", "deleting"]
        self.assertFalse(guard_write_intent(scrub_read_only_values(argv)))

    def test_scrub_keeps_flag_itself_and_operation(self):
        argv = ["--operation", "DeleteInstance"]
        self.assertIn("DeleteInstance", scrub_read_only_values(argv))

    def test_scrub_drops_sort_by_value(self):
        # Regression: "created" contains the mutating keyword "create".
        argv = ["--sort-by", "created", "--region", "cn-north-4"]
        scrubbed = scrub_read_only_values(argv)
        self.assertNotIn("created", scrubbed)
        self.assertFalse(guard_write_intent(scrubbed))

    def test_scrub_drops_inline_read_only_values(self):
        for argv, leaked in ((["--sort-by=created"], "created"),
                             (["--sort-by=name"], "name"),
                             (["--output=/tmp/update-report.md"], "update-report")):
            scrubbed = scrub_read_only_values(argv)
            self.assertNotIn(leaked, scrubbed)
            self.assertFalse(guard_write_intent(scrubbed))

    def test_inline_mutating_operation_still_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent(scrub_read_only_values(["--operation=DeleteInstance"]))


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

    def test_project_id_becomes_global_cli_param(self):
        argv = build_command("cn-north-4", project_id="proj-1")
        self.assertIn("--cli-project-id=proj-1", argv)

    def test_project_id_absent_by_default(self):
        argv = build_command("cn-north-4")
        self.assertFalse(any("project-id" in flag for flag in argv))

    def test_status_never_sent_to_server(self):
        argv = build_command("cn-north-4")
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
        with mock.patch("list_rds_export_markdown.subprocess.run", fake):
            instances = list_instances("cn-north-4")
        self.assertEqual(instances, [INSTANCE_1, INSTANCE_2])
        self.assertEqual(len(fake.calls), 1)

    def test_pagination_via_total(self):
        page1 = {"instances": [INSTANCE_1], "total_count": 2}
        page2 = {"instances": [INSTANCE_2], "total_count": 2}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("list_rds_export_markdown.subprocess.run", fake):
            instances = list_instances("cn-north-4", limit=1)
        self.assertEqual(instances, [INSTANCE_1, INSTANCE_2])
        self.assertEqual(len(fake.calls), 2)
        self.assertIn("--offset=1", fake.calls[1])

    def test_pagination_via_full_page_without_total(self):
        page1 = {"instances": [INSTANCE_1]}
        page2 = {"instances": []}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("list_rds_export_markdown.subprocess.run", fake):
            instances = list_instances("cn-north-4", limit=1)
        self.assertEqual(instances, [INSTANCE_1])

    def test_empty_region(self):
        fake = FakeRunner([(json.dumps({"instances": [], "total_count": 0}), "", 0)])
        with mock.patch("list_rds_export_markdown.subprocess.run", fake):
            instances = list_instances("cn-north-4")
        self.assertEqual(instances, [])

    def test_status_filter_applied_client_side(self):
        fake = FakeRunner([(
            json.dumps({"instances": [INSTANCE_1, INSTANCE_2], "total_count": 2}), "", 0)])
        with mock.patch("list_rds_export_markdown.subprocess.run", fake):
            instances = list_instances("cn-north-4", status="ACTIVE")
        self.assertEqual(instances, [INSTANCE_1])
        for call in fake.calls:
            self.assertFalse(any("--status" in part for part in call))

    def test_status_filter_case_insensitive_and_empty(self):
        fake = FakeRunner([(
            json.dumps({"instances": [INSTANCE_1, INSTANCE_2], "total_count": 2}), "", 0)])
        with mock.patch("list_rds_export_markdown.subprocess.run", fake):
            self.assertEqual(list_instances("cn-north-4", status="active"), [INSTANCE_1])
        fake = FakeRunner([(
            json.dumps({"instances": [INSTANCE_1, INSTANCE_2], "total_count": 2}), "", 0)])
        with mock.patch("list_rds_export_markdown.subprocess.run", fake):
            self.assertEqual(list_instances("cn-north-4", status="BUILDING"), [])

    def test_use_error_rc0_raises_api_error(self):
        fake = FakeRunner([(
            "[USE_ERROR]Invalid parameter: status\n\n"
            "Run `hcloud RDS ListInstances --help` for details.", "", 0)])
        with mock.patch("list_rds_export_markdown.subprocess.run", fake):
            with self.assertRaises(ApiError) as ctx:
                list_instances("cn-north-4")
        self.assertIn("参数错误", str(ctx.exception))

    def test_nonzero_exit_403(self):
        fake = FakeRunner([("", "403 Forbidden", 1)])
        with mock.patch("list_rds_export_markdown.subprocess.run", fake):
            with self.assertRaises(AuthError):
                list_instances("cn-north-4")

    def test_nonzero_exit_credentials(self):
        fake = FakeRunner([("", "ERROR: no AK configured", 1)])
        with mock.patch("list_rds_export_markdown.subprocess.run", fake):
            with self.assertRaises(ConfigError):
                list_instances("cn-north-4")

    def test_timeout(self):
        fake = FakeRunner([subprocess.TimeoutExpired(cmd="hcloud", timeout=120)])
        with mock.patch("list_rds_export_markdown.subprocess.run", fake):
            with self.assertRaises(ApiError):
                list_instances("cn-north-4")

    def test_sdk_fallback_when_hcloud_missing(self):
        with mock.patch("list_rds_export_markdown.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_rds_export_markdown.list_instances_via_sdk",
                           return_value=[INSTANCE_1, INSTANCE_2]) as sdk_mock:
            instances = list_instances("cn-north-4", status="ACTIVE")
        self.assertEqual(instances, [INSTANCE_1])
        self.assertEqual(sdk_mock.call_args.kwargs.get("status"), None)

    def test_sdk_fallback_unavailable_raises_config(self):
        with mock.patch("list_rds_export_markdown.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_rds_export_markdown.list_instances_via_sdk",
                           side_effect=ConfigError("huaweicloudsdkrds 未安装")):
            with self.assertRaises(ConfigError):
                list_instances("cn-north-4")

    def test_sdk_request_has_no_status_attribute(self):
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


class TestSdkFallback(unittest.TestCase):
    """The SDK fallback must use modules that exist in the official packages
    and wire credentials from environment variables (BasicCredentials has no
    env auto-discovery)."""

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
        with mock.patch.dict(os.environ, self._clean_credential_env(), clear=True):
            with self.assertRaises(ConfigError) as ctx:
                list_instances_via_sdk("cn-north-4")
        message = str(ctx.exception)
        self.assertIn("AK/SK", message)
        self.assertNotIn("未安装", message)


class TestFilterByStatus(unittest.TestCase):
    def test_no_status_returns_all(self):
        self.assertEqual(filter_by_status([INSTANCE_1, INSTANCE_2], None),
                         [INSTANCE_1, INSTANCE_2])

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


class TestNormalize(unittest.TestCase):
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

    def test_names(self):
        self.assertEqual(instance_names([INSTANCE_1, INSTANCE_2]),
                         ["rds-demo-01", "rds-demo-02"])

    def test_names_fallback_to_id(self):
        self.assertEqual(instance_names([{"id": "rds-9"}]), ["rds-9"])


class TestRenderMarkdown(unittest.TestCase):
    def test_contains_title_header_and_rows(self):
        doc = render_markdown([INSTANCE_1, INSTANCE_2], "cn-north-4")
        self.assertIn("# Huawei Cloud RDS Instances — cn-north-4", doc)
        self.assertIn("| 实例名称 | 实例ID | 状态 | 引擎 | 版本 | 规格 | 私网IP | 可用区 | 创建时间 |", doc)
        for fragment in ("rds-demo-01", "rds-0001", "ACTIVE", "MySQL", "8.0",
                         "rds.mysql.x1.large.2.ha", "192.168.0.10", "cn-north-4a",
                         "rds-demo-02", "PostgreSQL"):
            self.assertIn(fragment, doc)

    def test_row_count(self):
        doc = render_markdown([INSTANCE_1, INSTANCE_2], "cn-north-4")
        data_rows = [line for line in doc.splitlines() if line.startswith("| rds-")]
        self.assertEqual(len(data_rows), 2)

    def test_empty_still_valid_with_note(self):
        doc = render_markdown([], "cn-south-1")
        self.assertIn("| 实例名称 |", doc)
        self.assertIn("| --- |", doc)
        self.assertIn("无 RDS 实例", doc)
        self.assertIn("cn-south-1", doc)
        self.assertIn("Instances: 0", doc)

    def test_missing_fields_render_dash(self):
        doc = render_markdown([{"id": "rds-x"}], "cn-north-4")
        self.assertIn("| - | rds-x |", doc)

    def test_pipe_and_newline_escaped(self):
        doc = render_markdown([{"name": "a|b", "id": "x\ny"}], "cn-north-4")
        self.assertIn("a\\|b", doc)
        self.assertIn("x y", doc)


class TestWriteMarkdown(unittest.TestCase):
    def test_writes_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "out.md")
            write_markdown("# hello\n", path)
            with open(path, encoding="utf-8") as handle:
                self.assertEqual(handle.read(), "# hello\n")

    def test_creates_missing_dirs(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "nested", "dir", "out.md")
            write_markdown("content", path)
            self.assertTrue(os.path.isfile(path))

    def test_bad_path_raises_api_error(self):
        with self.assertRaises(ApiError):
            write_markdown("content", "\0bad\0path.md")


class TestSortInstances(unittest.TestCase):
    """Local ordering for --sort-by (the RDS ListInstances API has no ordering
    parameter, so sorting is applied client-side after the full list is fetched)."""

    def test_no_sort_by_preserves_api_order_and_copies(self):
        source = [INSTANCE_2, INSTANCE_1]
        result = sort_instances(source)
        self.assertEqual(result, [INSTANCE_2, INSTANCE_1])
        self.assertIsNot(result, source)
        self.assertEqual(source, [INSTANCE_2, INSTANCE_1])

    def test_empty_sort_by_is_a_no_op(self):
        self.assertEqual(sort_instances([INSTANCE_1, INSTANCE_2], ""),
                         [INSTANCE_1, INSTANCE_2])

    def test_sort_by_name_case_insensitive_ascending(self):
        items = [{"name": "zeta"}, {"name": "Alpha"}, {"name": "beta"}]
        self.assertEqual([i["name"] for i in sort_instances(items, "name")],
                         ["Alpha", "beta", "zeta"])

    def test_sort_by_value_is_case_insensitive(self):
        items = [{"name": "b"}, {"name": "a"}]
        self.assertEqual([i["name"] for i in sort_instances(items, "NAME")], ["a", "b"])

    def test_sort_by_name_falls_back_to_id(self):
        items = [{"name": "rds-demo-01", "id": "rds-2"}, {"id": "rds-1"}]
        self.assertEqual([i["id"] for i in sort_instances(items, "name")],
                         ["rds-1", "rds-2"])

    def test_sort_by_name_missing_key_last(self):
        items = [{"status": "ACTIVE"}, {"name": "b"}, {"name": "a"}]
        result = sort_instances(items, "name")
        self.assertEqual([i.get("name") for i in result], ["a", "b", None])

    def test_sort_by_created_mixed_formats_ascending(self):
        # ISO8601 with Z, space-separated naive, and +0800 offsets must all be
        # comparable (naive values are treated as UTC instead of raising
        # TypeError on aware/naive comparison).
        items = [
            {"name": "newest", "created": "2026-03-01T10:00:00Z"},
            {"name": "oldest", "created": "2025-12-31 23:59:59"},
            {"name": "middle", "created": "2026-01-02T03:04:05+0800"},
        ]
        self.assertEqual([i["name"] for i in sort_instances(items, "created")],
                         ["oldest", "middle", "newest"])

    def test_sort_by_created_unparseable_falls_back_to_text(self):
        items = [
            {"name": "bad-b", "created": "zzz"},
            {"name": "bad-a", "created": "aaa"},
            {"name": "good", "created": "2026-01-01T00:00:00Z"},
        ]
        self.assertEqual([i["name"] for i in sort_instances(items, "created")],
                         ["good", "bad-a", "bad-b"])

    def test_sort_by_created_missing_key_last(self):
        items = [
            {"name": "none"},
            {"name": "later", "created": "2026-02-01T00:00:00Z"},
            {"name": "earlier", "created": "2026-01-01T00:00:00Z"},
        ]
        self.assertEqual([i["name"] for i in sort_instances(items, "created")],
                         ["earlier", "later", "none"])

    def test_sort_is_stable_for_equal_keys(self):
        items = [
            {"name": "same", "id": "rds-3", "created": "2026-01-01T00:00:00Z"},
            {"name": "Same", "id": "rds-1", "created": "2026-01-01T00:00:00Z"},
            {"name": "alpha", "id": "rds-2", "created": "2025-01-01T00:00:00Z"},
        ]
        self.assertEqual([i["id"] for i in sort_instances(items, "name")],
                         ["rds-2", "rds-3", "rds-1"])
        self.assertEqual([i["id"] for i in sort_instances(items, "created")],
                         ["rds-2", "rds-3", "rds-1"])

    def test_sort_does_not_mutate_input(self):
        source = [INSTANCE_2, INSTANCE_1]
        sort_instances(source, "name")
        self.assertEqual(source, [INSTANCE_2, INSTANCE_1])

    def test_empty_list_stays_empty(self):
        self.assertEqual(sort_instances([], "name"), [])
        self.assertEqual(sort_instances([], "created"), [])

    def test_invalid_sort_by_raises_sort_error(self):
        with self.assertRaises(SortError) as ctx:
            sort_instances([INSTANCE_1], "status")
        self.assertIn("--sort-by 仅支持 name 或 created", str(ctx.exception))
        self.assertIn("status", str(ctx.exception))

    def test_resolve_sort_by(self):
        self.assertIsNone(resolve_sort_by(None))
        self.assertIsNone(resolve_sort_by("   "))
        self.assertEqual(resolve_sort_by(" NAME "), "name")
        self.assertEqual(resolve_sort_by("created"), "created")
        with self.assertRaises(SortError):
            resolve_sort_by("create")

    def test_parse_created_accepts_common_formats(self):
        utc = datetime.timezone.utc
        expected = datetime.datetime(2026, 1, 2, 3, 4, 5, tzinfo=utc)
        for value in ("2026-01-02T03:04:05Z", "2026-01-02 03:04:05",
                      "2026-01-02T03:04:05+00:00", "2026-01-02T03:04:05+0000"):
            self.assertEqual(parse_created(value), expected, value)
        self.assertEqual(parse_created("2026-01-02T11:04:05+0800"), expected)
        self.assertIsNone(parse_created("not-a-date"))
        self.assertIsNone(parse_created(""))


def data_row_names(content):
    """First-column values of the Markdown data rows (in file order)."""
    names = []
    for line in content.splitlines():
        if not line.startswith("| "):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells[0] in ("实例名称", "---"):
            continue
        names.append(cells[0])
    return names


class TestMain(unittest.TestCase):
    def _run(self, argv, results, cwd=None):
        fake = FakeRunner(results)
        old = os.getcwd()
        if cwd:
            os.chdir(cwd)
        try:
            with mock.patch("list_rds_export_markdown.subprocess.run", fake), \
                    mock.patch("sys.stdout") as stdout, \
                    mock.patch("sys.stderr") as stderr:
                rc = main(argv)
            out = "".join(c[0][0] for c in stdout.write.call_args_list)
            err = "".join(c[0][0] for c in stderr.write.call_args_list)
        finally:
            os.chdir(old)
        return rc, out, err

    def test_default_output_in_cwd(self):
        with tempfile.TemporaryDirectory() as tmp:
            rc, out, err = self._run(
                ["--region", "cn-north-4"],
                [(json.dumps({"instances": [INSTANCE_1, INSTANCE_2], "total_count": 2}), "", 0)],
                cwd=tmp)
            self.assertEqual(rc, 0)
            path = os.path.join(tmp, "rds_instances.md")
            self.assertTrue(os.path.isfile(path))
            with open(path, encoding="utf-8") as handle:
                content = handle.read()
            self.assertIn("rds-demo-01", content)
            self.assertIn(os.path.abspath(path), out)
            self.assertEqual(err, "")

    def test_explicit_output_and_stdout(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "report.md")
            rc, out, err = self._run(
                ["--region", "cn-north-4", "--output", path, "--stdout"],
                [(json.dumps({"instances": [INSTANCE_1], "total_count": 1}), "", 0)])
            self.assertEqual(rc, 0)
            self.assertTrue(os.path.isfile(path))
            self.assertIn("| 实例名称 |", out)

    def test_empty_result_writes_file_exit_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "empty.md")
            rc, out, err = self._run(
                ["--region", "cn-south-1", "--output", path],
                [(json.dumps({"instances": [], "total_count": 0}), "", 0)])
            self.assertEqual(rc, 0)
            self.assertTrue(os.path.isfile(path))
            with open(path, encoding="utf-8") as handle:
                content = handle.read()
            self.assertIn("无 RDS 实例", content)
            self.assertIn("cn-south-1", out)
            self.assertEqual(err, "")

    def test_status_filter_main_client_side(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "f.md")
            fake = FakeRunner([
                (json.dumps({"instances": [INSTANCE_1, INSTANCE_2], "total_count": 2}), "", 0)])
            with mock.patch("list_rds_export_markdown.subprocess.run", fake), \
                    mock.patch("sys.stdout"):
                rc = main(["--status", "ACTIVE", "--output", path])
            self.assertEqual(rc, 0)
            with open(path, encoding="utf-8") as handle:
                content = handle.read()
            self.assertIn("rds-demo-01", content)
            self.assertNotIn("rds-demo-02", content)
            for call in fake.calls:
                self.assertFalse(any("--status" in part for part in call))

    def test_project_id_passed_to_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "p.md")
            fake = FakeRunner([(json.dumps({"instances": [], "total_count": 0}), "", 0)])
            with mock.patch("list_rds_export_markdown.subprocess.run", fake), \
                    mock.patch("sys.stdout"):
                main(["--project_id", "proj-1", "--output", path])
            self.assertIn("--cli-project-id=proj-1", fake.calls[0])

    def test_auth_error_message(self):
        with tempfile.TemporaryDirectory() as tmp:
            rc, out, err = self._run(
                ["--output", os.path.join(tmp, "x.md")], [("", "403 Forbidden", 1)])
            self.assertEqual(rc, 1)
            self.assertIn("[错误]", err)
            self.assertIn("IAM", err)
            self.assertFalse(os.path.exists(os.path.join(tmp, "x.md")))

    def test_missing_ak_sk_error_message(self):
        with tempfile.TemporaryDirectory() as tmp:
            rc, out, err = self._run(
                ["--output", os.path.join(tmp, "x.md")], [("", "ERROR: cli-ak empty", 1)])
            self.assertEqual(rc, 1)
            self.assertIn("AK/SK", err)

    def test_hcloud_not_installed(self):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch("list_rds_export_markdown.list_instances_via_sdk",
                            side_effect=ConfigError("huaweicloudsdkrds 未安装")):
                rc, out, err = self._run(
                    ["--output", os.path.join(tmp, "x.md")], [FileNotFoundError()])
            self.assertEqual(rc, 1)
            self.assertIn("未安装", err)

    def test_hcloud_missing_falls_back_to_sdk(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "s.md")
            with mock.patch("list_rds_export_markdown.list_instances_via_sdk",
                            return_value=[INSTANCE_1]):
                rc, out, err = self._run(["--output", path], [FileNotFoundError()])
            self.assertEqual(rc, 0)
            self.assertTrue(os.path.isfile(path))
            with open(path, encoding="utf-8") as handle:
                self.assertIn("rds-demo-01", handle.read())

    def test_write_intent_argv_blocked(self):
        rc, out, err = self._run(["--operation", "DeleteInstance"], [])
        self.assertEqual(rc, 1)
        self.assertIn("守卫拦截", err)

    def test_output_path_with_mutating_word_allowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "update-report.md")
            rc, out, err = self._run(
                ["--output", path],
                [(json.dumps({"instances": [INSTANCE_1], "total_count": 1}), "", 0)])
            self.assertEqual(rc, 0)
            self.assertTrue(os.path.isfile(path))

    def test_sort_by_name_orders_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "sorted-name.md")
            payload = {"instances": [
                {"name": "rds-zulu", "id": "rds-9", "created": "2026-01-01T00:00:00Z"},
                {"name": "rds-alpha", "id": "rds-1", "created": "2026-02-01T00:00:00Z"},
                {"name": "rds-Mike", "id": "rds-5", "created": "2026-03-01T00:00:00Z"},
            ], "total_count": 3}
            rc, out, err = self._run(
                ["--region", "cn-north-4", "--sort-by", "name", "--output", path],
                [(json.dumps(payload), "", 0)])
            self.assertEqual(rc, 0)
            self.assertEqual(err, "")
            with open(path, encoding="utf-8") as handle:
                self.assertEqual(data_row_names(handle.read()),
                                 ["rds-alpha", "rds-Mike", "rds-zulu"])

    def test_sort_by_created_orders_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "sorted-created.md")
            payload = {"instances": [
                {"name": "rds-new", "id": "rds-3", "created": "2026-05-01T00:00:00Z"},
                {"name": "rds-old", "id": "rds-1", "created": "2025-01-01 08:00:00"},
                {"name": "rds-mid", "id": "rds-2", "created": "2026-01-01T00:00:00+0800"},
            ], "total_count": 3}
            rc, out, err = self._run(
                ["--region", "cn-north-4", "--sort-by", "created", "--output", path],
                [(json.dumps(payload), "", 0)])
            self.assertEqual(rc, 0)
            with open(path, encoding="utf-8") as handle:
                self.assertEqual(data_row_names(handle.read()),
                                 ["rds-old", "rds-mid", "rds-new"])

    def test_sort_by_created_passes_write_intent_guard(self):
        # "created" must not be mistaken for the mutating keyword "create".
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "guarded.md")
            rc, out, err = self._run(
                ["--sort-by", "created", "--output", path],
                [(json.dumps({"instances": [INSTANCE_1], "total_count": 1}), "", 0)])
            self.assertEqual(rc, 0)
            self.assertEqual(err, "")
            self.assertTrue(os.path.isfile(path))

    def test_no_sort_by_keeps_api_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "unordered.md")
            payload = {"instances": [
                {"name": "rds-demo-02", "id": "rds-2"},
                {"name": "rds-demo-01", "id": "rds-1"},
            ], "total_count": 2}
            rc, out, err = self._run(["--output", path],
                                     [(json.dumps(payload), "", 0)])
            self.assertEqual(rc, 0)
            with open(path, encoding="utf-8") as handle:
                self.assertEqual(data_row_names(handle.read()),
                                 ["rds-demo-02", "rds-demo-01"])

    def test_invalid_sort_by_exits_1_without_query_or_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "bad-sort.md")
            # FakeRunner([]) asserts no hcloud call is ever made.
            rc, out, err = self._run(
                ["--sort-by", "status", "--output", path], [])
            self.assertEqual(rc, 1)
            self.assertIn("--sort-by 仅支持 name 或 created", err)
            self.assertIn("status", err)
            self.assertFalse(os.path.exists(path))


class TestErrorHierarchy(unittest.TestCase):
    def test_subclasses(self):
        for exc in (GuardError, ConfigError, AuthError, ApiError, SortError):
            self.assertTrue(issubclass(exc, RdsListError))


if __name__ == "__main__":
    unittest.main()