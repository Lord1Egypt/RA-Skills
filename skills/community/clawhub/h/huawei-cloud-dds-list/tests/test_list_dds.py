import datetime
import json
import os
import re
import subprocess
import sys
import unicodedata
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from list_dds import (  # noqa: E402
    MAX_LIMIT,
    ApiError,
    AuthError,
    ConfigError,
    DdsListError,
    GuardError,
    _node_count,
    _sign_headers,
    build_command,
    build_rest_url,
    classify_hcloud_failure,
    extract_instances,
    extract_json,
    filter_by_status,
    guard_operation,
    guard_write_intent,
    instance_names,
    list_instances,
    list_instances_via_rest,
    list_instances_via_sdk,
    main,
    render_table,
    _sdk_api,
)

try:
    import huaweicloudsdkdds  # noqa: F401
    HAS_SDK = True
except ImportError:  # pragma: no cover - environment dependent
    HAS_SDK = False

# Official ListInstances response shape (GET /v3/{project_id}/instances →
# QueryInstanceResponse in huaweicloudsdkdds v3): creation time is `created`
# (`updated` for the update time), the instance type is `mode` (no top-level
# `type`) and the flavor spec lives at `groups[].nodes[].spec_code` (no
# top-level `flavor`).
INSTANCE_SHARDING = {
    "id": "6c7f2f0e-0001-4f1f-9a11-111111111111",
    "name": "dds-sharding-demo-01",
    "status": "normal",
    "mode": "Sharding",
    "datastore": {"type": "DDS-Community", "version": "4.0", "storage_engine": "wiredTiger"},
    "created": "2026-01-01T00:00:00Z",
    "updated": "2026-01-02T00:00:00Z",
    "vpc_id": "vpc-0001",
    "subnet_id": "subnet-0001",
    "security_group_id": "sg-0001",
    "groups": [
        {
            "type": "shard",
            "id": "grp-0001",
            "name": "shard-0001",
            "status": "normal",
            "nodes": [
                {"id": "node-0001", "name": "node-0001", "status": "normal",
                 "role": "Primary", "private_ip": "192.168.0.10",
                 "spec_code": "dds.mongodb.s3.medium.4.shard"},
                {"id": "node-0002", "name": "node-0002", "status": "normal",
                 "role": "Secondary", "private_ip": "192.168.0.11",
                 "spec_code": "dds.mongodb.s3.medium.4.shard"},
            ],
        },
        {
            "type": "mongos",
            "id": "grp-0002",
            "name": "mongos-0001",
            "status": "normal",
            "nodes": [
                {"id": "node-0003", "name": "node-0003", "status": "normal",
                 "role": "Primary", "private_ip": "192.168.0.12",
                 "spec_code": "dds.mongodb.s3.medium.4.mongos"},
            ],
        },
    ],
}

# Legacy payload shape: `created_at` + top-level `flavor[]` (still accepted as
# a fallback so hand-built/older payloads keep working).
INSTANCE_REPLICA = {
    "id": "6c7f2f0e-0002-4f1f-9a11-222222222222",
    "name": "dds-replica-demo-02",
    "status": "abnormal",
    "mode": "ReplicaSet",
    "datastore": {"type": "DDS-Community", "version": "4.2", "storage_engine": "wiredTiger"},
    "created_at": "2026-02-01T00:00:00Z",
    "vpc_id": "vpc-0002",
    "subnet_id": "subnet-0002",
    "flavor": [{"num": 1, "spec_code": "dds.mongodb.s3.medium.4.repset", "size": 100, "type": "replica"}],
}

INSTANCE_SINGLE = {
    "id": "6c7f2f0e-0003-4f1f-9a11-333333333333",
    "name": "dds-single-demo-03",
    "status": "creating",
    "mode": "Single",
    "datastore": {"type": "DDS-Community", "version": "4.4", "storage_engine": "wiredTiger"},
    "created": "2026-03-01T00:00:00Z",
}

PAGE_RESPONSE = {"instances": [INSTANCE_SHARDING], "total_count": 1}
EMPTY_RESPONSE = {"instances": [], "total_count": 0}


def display_width(text):
    return sum(2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
               for ch in text)


def table_rows(table):
    return [re.split(r"\s{2,}", line.strip()) for line in table.splitlines()]


def first_table_row(table):
    """Header + first data row of a rendered table, as {header: value}."""
    rows = table_rows(table)
    return dict(zip(rows[0], rows[2]))


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
        self.assertFalse(guard_write_intent("query dds instance list"))

    def test_create_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("CreateInstance dds-new")

    def test_delete_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("delete instance dds-demo")

    def test_dds_write_operations_blocked(self):
        for text in ("RestartInstance dds-01", "resize instance",
                     "ResizeInstance", "backup now", "restore backup",
                     "modify instance name", "scale up", "upgrade database",
                     "restart me", "migrate az"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_status_values_not_blocked(self):
        guard_write_intent("--status creating --status deleting --status resizing")
        guard_write_intent("--status frozen")

    def test_normalized_separators_blocked(self):
        for text in ("--create-instance", "create_instance", "CREATE-INSTANCE"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_compound_operation_names_blocked(self):
        for text in ("SwitchInstance", "StopInstance", "StartupInstance",
                     "UnbindEip", "BatchDeleteBackup", "CreateManualBackup"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_ambiguous_words_in_readonly_names_pass(self):
        # "check" / "copy" are not write verbs on their own — read-only filter
        # values containing them must not be rejected.
        for text in ("--name checkpoint-demo", "--name dds-copy-01",
                     "--name copycat", "--name checkup"):
            self.assertFalse(guard_write_intent(text))

    def test_readonly_values_containing_verbs_pass(self):
        # A value is data, not a command: an instance legitimately named
        # `create-me` must not be blocked just because the value spells a verb.
        for text in (
            "--name create-me",
            "--name delete-me",
            "--name update-demo",
            "--name restart-box",
            "--name backup-job",
            "--name=create-me",
            "--instance-id create-instance-01",
            "--instance-id delete-instance-01",
            "--vpc-id create-vpc",
            "--subnet-id delete-subnet",
            "--tags create=1,delete=0",
            "--status creating",
            "--project-id 05f6c1d2e3b4a5968778695a4b3c2d1e",
            "--region cn-north-4 --name create-me --table",
        ):
            self.assertFalse(guard_write_intent(text))

    def test_operation_positions_still_blocked(self):
        # Exempting filter values must not weaken operation/flag scanning.
        for text in ("CreateInstance", "DeleteInstance", "--create-instance",
                     "--delete-instance=foo", "create-me",
                     "--name create-me --create-instance", "DeleteInstance --name x"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_operation_whitelist(self):
        guard_operation("ListInstances")
        with self.assertRaises(GuardError):
            guard_operation("CreateInstance")
        with self.assertRaises(GuardError):
            guard_operation("DeleteInstance")


class TestBuildCommand(unittest.TestCase):
    def test_minimal_command(self):
        argv = build_command("cn-north-4")
        self.assertEqual(argv[:3], ["DDS", "ListInstances", "--cli-region=cn-north-4"])
        self.assertIn("--limit=100", argv)
        self.assertIn("--offset=0", argv)

    def test_server_filters_forwarded(self):
        argv = build_command("cn-north-4", name="dds-demo", instance_id="id-1",
                             mode="ReplicaSet", datastore_type="DDS-Community",
                             vpc_id="vpc-1", subnet_id="subnet-1",
                             tags="env=prod", project_id="proj-1")
        for expected in ("--id=id-1", "--cli-mode=AKSK", "--mode=ReplicaSet",
                         "--name=dds-demo", "--datastore_type=DDS-Community",
                         "--vpc_id=vpc-1", "--subnet_id=subnet-1",
                         "--tags=env=prod", "--project_id=proj-1"):
            self.assertIn(expected, argv)

    def test_mode_filter_avoids_cli_system_parameter_collision(self):
        argv = build_command("cn-north-4", mode="Sharding", cli_mode="SSO")
        self.assertIn("--cli-mode=SSO", argv)
        self.assertIn("--mode=Sharding", argv)
        # The system parameter must precede the API parameter of the same name.
        self.assertLess(argv.index("--cli-mode=SSO"),
                        argv.index("--mode=Sharding"))

    def test_fuzzy_name_prefixes_asterisk(self):
        argv = build_command("cn-north-4", name="dds", fuzzy=True)
        self.assertIn("--name=*dds", argv)

    def test_exact_name_no_asterisk(self):
        argv = build_command("cn-north-4", name="dds")
        self.assertIn("--name=dds", argv)
        self.assertNotIn("--name=*dds", argv)

    def test_invalid_mode_rejected(self):
        with self.assertRaises(ApiError):
            build_command("cn-north-4", mode="Cluster")

    def test_invalid_datastore_type_rejected(self):
        with self.assertRaises(ApiError):
            build_command("cn-north-4", datastore_type="MongoDB")

    def test_no_write_flags_ever(self):
        argv = " ".join(build_command("cn-north-4", name="x"))
        for verb in ("create", "delete", "restart", "resize", "backup"):
            self.assertNotIn(verb, argv.lower())


class TestJsonExtraction(unittest.TestCase):
    def test_plain_json(self):
        self.assertEqual(extract_json('{"instances": [], "total_count": 0}'),
                         {"instances": [], "total_count": 0})

    def test_wrapped_json(self):
        text = "some notice line\n{\"instances\": [1], \"total_count\": 1}\n"
        self.assertEqual(extract_json(text), {"instances": [1], "total_count": 1})

    def test_invalid_json_raises(self):
        with self.assertRaises(ApiError):
            extract_json("not json at all")

    def test_extract_instances_shapes(self):
        self.assertEqual(extract_instances([{"id": 1}]), [{"id": 1}])
        self.assertEqual(extract_instances({"instances": [1]}), [1])
        self.assertEqual(extract_instances({}), [])


class TestFailureClassification(unittest.TestCase):
    def test_missing_credentials(self):
        err = classify_hcloud_failure(
            "", "hcloud: CLI-AK is required but not configured", 1)
        self.assertIsInstance(err, ConfigError)
        self.assertIn("缺少 AK/SK 凭证", str(err))

    def test_403_auth(self):
        err = classify_hcloud_failure("", '{"error_code":"IAM.0003"} 403 forbidden', 1)
        self.assertIsInstance(err, AuthError)
        self.assertIn("无权限访问文档数据库服务（DDS）", str(err))

    def test_use_error_with_rc0_is_hard_failure(self):
        err = classify_hcloud_failure(
            "[USE_ERROR]Unsupported parameter: status", "", 0)
        self.assertIsInstance(err, ApiError)
        self.assertIn("hcloud 参数错误", str(err))
        self.assertIn("DDS ListInstances", str(err))
        self.assertIn("--help", str(err))

    def test_generic_api_error(self):
        err = classify_hcloud_failure("", "connect timeout", 7)
        self.assertIsInstance(err, ApiError)
        self.assertIn("hcloud 调用失败（退出码 7）", str(err))


class TestListInstances(unittest.TestCase):
    def test_paging_until_total_count(self):
        runner = FakeRunner([
            (json.dumps({"instances": [INSTANCE_SHARDING] * 2, "total_count": 3}), "", 0),
            (json.dumps({"instances": [INSTANCE_REPLICA], "total_count": 3}), "", 0),
        ])
        with mock.patch("list_dds.subprocess.run", runner):
            instances = list_instances("cn-north-4", limit=2)
        self.assertEqual(len(instances), 3)
        first = runner.calls[0]
        self.assertIn("--limit=2", first)
        self.assertIn("--offset=0", first)
        self.assertIn("--offset=2", runner.calls[1])

    def test_single_page_no_extra_call(self):
        runner = FakeRunner([(json.dumps(PAGE_RESPONSE), "", 0)])
        with mock.patch("list_dds.subprocess.run", runner):
            instances = list_instances("cn-north-4", limit=1,
                                       max_pages=1, allow_truncation=True)
        self.assertEqual(len(instances), 1)
        self.assertEqual(len(runner.calls), 1)

    def test_empty_list_stops_immediately(self):
        runner = FakeRunner([(json.dumps(EMPTY_RESPONSE), "", 0)])
        with mock.patch("list_dds.subprocess.run", runner):
            instances = list_instances("cn-north-4")
        self.assertEqual(instances, [])

    def test_max_pages_guard(self):
        payload = json.dumps({"instances": [{"id": "x"}], "total_count": 9999})
        runner = FakeRunner([(payload, "", 0)] * 2)
        with mock.patch("list_dds.subprocess.run", runner):
            with self.assertRaises(ApiError):
                list_instances("cn-north-4", limit=1, max_pages=2)

    def test_hcloud_missing_raises(self):
        with mock.patch("list_dds.subprocess.run",
                        side_effect=FileNotFoundError("no hcloud")):
            with self.assertRaises(ConfigError):
                list_instances("cn-north-4")

    def test_failure_propagates(self):
        with mock.patch("list_dds.subprocess.run",
                        return_value=hcloud_result("", "403 forbidden", 1)):
            with self.assertRaises(AuthError):
                list_instances("cn-north-4")


class TestStatusFilter(unittest.TestCase):
    def test_client_side_filter(self):
        instances = [INSTANCE_SHARDING, INSTANCE_REPLICA, INSTANCE_SINGLE]
        self.assertEqual(
            [i["id"] for i in filter_by_status(instances, "normal")],
            [INSTANCE_SHARDING["id"]])
        self.assertEqual(
            [i["id"] for i in filter_by_status(instances, "CREATING")],
            [INSTANCE_SINGLE["id"]])
        self.assertEqual(filter_by_status(instances, None), instances)
        self.assertEqual(filter_by_status(instances, "frozen"), [])


class TestRendering(unittest.TestCase):
    def test_instance_names(self):
        self.assertEqual(
            instance_names([INSTANCE_SHARDING, INSTANCE_REPLICA]),
            ["dds-sharding-demo-01", "dds-replica-demo-02"])

    def test_instance_names_fallback_to_id(self):
        self.assertEqual(instance_names([{"id": "id-9"}]), ["id-9"])

    def test_table_headers_are_fixed(self):
        table = render_table([INSTANCE_SHARDING, INSTANCE_REPLICA])
        headers = table_rows(table)[0]
        self.assertEqual(
            headers,
            ["实例ID", "名称", "状态", "引擎版本", "规格", "节点数",
             "创建时间", "模式"])
        self.assertIn("集群", table)
        self.assertIn("副本集", table)
        self.assertIn("4.0", table)
        self.assertIn("dds.mongodb.s3.medium.4", table)

    def test_table_missing_values_render_dash(self):
        table = render_table([{"id": "id-1", "name": "n1", "status": "normal"}])
        self.assertIn("-", table)
        self.assertNotIn("None", table)

    def test_single_node_label(self):
        self.assertIn("单节点", render_table([INSTANCE_SINGLE]))

    def test_official_response_fields_are_populated(self):
        """created + groups[].nodes[].spec_code must reach the table."""
        values = first_table_row(render_table([INSTANCE_SHARDING]))
        self.assertEqual(values["创建时间"], "2026-01-01T00:00:00Z")
        self.assertEqual(values["规格"],
                         "dds.mongodb.s3.medium.4.shard,"
                         "dds.mongodb.s3.medium.4.mongos")
        self.assertEqual(values["模式"], "集群")
        self.assertEqual(values["引擎版本"], "4.0")
        self.assertEqual(values["节点数"], "3")

    def test_node_count_across_groups(self):
        self.assertEqual(_node_count(INSTANCE_SHARDING), 3)
        self.assertIsNone(_node_count(INSTANCE_REPLICA))
        self.assertIsNone(_node_count(INSTANCE_SINGLE))
        self.assertEqual(_node_count({"groups": [
            {"nodes": [{"id": "n1"}]}, {"nodes": [{"id": "n2"}, {"id": "n3"}]},
        ]}), 3)
        self.assertEqual(_node_count({"nodes": [{"id": "n1"}]}), 1)

    def test_spec_codes_deduplicated_across_nodes(self):
        values = first_table_row(render_table([INSTANCE_SHARDING]))
        self.assertEqual(values["规格"].count("dds.mongodb.s3.medium.4.shard"), 1)

    def test_legacy_created_at_and_flavor_still_supported(self):
        values = first_table_row(render_table([INSTANCE_REPLICA]))
        self.assertEqual(values["创建时间"], "2026-02-01T00:00:00Z")
        self.assertEqual(values["规格"], "dds.mongodb.s3.medium.4.repset")

    def test_missing_groups_renders_dash_for_spec_and_node_count(self):
        values = first_table_row(render_table([INSTANCE_SINGLE]))
        self.assertEqual(values["规格"], "-")
        self.assertEqual(values["节点数"], "-")
        self.assertEqual(values["创建时间"], "2026-03-01T00:00:00Z")

    def test_empty_table_renders_header_only(self):
        table = render_table([])
        lines = table.splitlines()
        self.assertEqual(len(lines), 2)
        self.assertIn("实例ID", lines[0])
        self.assertTrue(set(lines[1]) == {"-", " "})

    def test_table_aligned_by_display_width(self):
        table = render_table([INSTANCE_SHARDING, INSTANCE_REPLICA])
        widths = {display_width(line) for line in table.splitlines()}
        self.assertEqual(len(widths), 1, "columns are not visually aligned")


class TestMain(unittest.TestCase):
    def run_main(self, argv, runner=None):
        buf_out, buf_err = [], []
        with mock.patch("list_dds.subprocess.run", runner or FakeRunner([])):
            with mock.patch("sys.stdout", new=_Sink(buf_out)):
                with mock.patch("sys.stderr", new=_Sink(buf_err)):
                    code = main(argv)
        return code, "".join(buf_out), "".join(buf_err)

    def test_default_names_output(self):
        runner = FakeRunner([(json.dumps(PAGE_RESPONSE), "", 0)])
        code, out, _ = self.run_main(["--region", "cn-north-4"], runner)
        self.assertEqual(code, 0)
        self.assertIn("DDS 实例名称列表", out)
        self.assertIn("- dds-sharding-demo-01", out)

    def test_table_output(self):
        runner = FakeRunner([(json.dumps(PAGE_RESPONSE), "", 0)])
        code, out, _ = self.run_main(["--table"], runner)
        self.assertEqual(code, 0)
        self.assertIn("名称", out)
        self.assertIn("集群", out)

    def test_json_output(self):
        runner = FakeRunner([(json.dumps(PAGE_RESPONSE), "", 0)])
        code, out, _ = self.run_main(["--json"], runner)
        self.assertEqual(code, 0)
        parsed = json.loads(out)
        self.assertEqual(parsed[0]["id"], INSTANCE_SHARDING["id"])

    def test_empty_region_hint(self):
        runner = FakeRunner([(json.dumps(EMPTY_RESPONSE), "", 0)])
        code, out, _ = self.run_main([], runner)
        self.assertEqual(code, 0)
        self.assertIn("当前区域（cn-north-4）无 DDS 实例", out)

    def test_empty_region_with_filters_hint(self):
        runner = FakeRunner([(json.dumps(EMPTY_RESPONSE), "", 0)])
        code, out, _ = self.run_main(["--name", "dds-demo", "--status", "normal"], runner)
        self.assertEqual(code, 0)
        self.assertIn("name=dds-demo", out)
        self.assertIn("status=normal（客户端过滤）", out)

    def test_write_intent_blocked_before_any_call(self):
        runner = FakeRunner([])
        code, _, err = self.run_main(["DeleteInstance"], runner)
        self.assertEqual(code, 1)
        self.assertIn("已被守卫拦截", err)
        self.assertEqual(runner.calls, [])

    def test_write_flag_blocked_before_any_call(self):
        runner = FakeRunner([])
        code, _, err = self.run_main(["--delete-instance"], runner)
        self.assertEqual(code, 1)
        self.assertIn("已被守卫拦截", err)
        self.assertEqual(runner.calls, [])

    def test_readonly_name_with_ambiguous_word_not_blocked(self):
        runner = FakeRunner([(json.dumps(PAGE_RESPONSE), "", 0)])
        code, _, _ = self.run_main(["--name", "checkpoint-demo", "--table"], runner)
        self.assertEqual(code, 0)
        cmd = " ".join(runner.calls[0])
        self.assertIn("--name=checkpoint-demo", cmd)

    def test_readonly_name_containing_verb_not_blocked(self):
        runner = FakeRunner([(json.dumps(PAGE_RESPONSE), "", 0)])
        code, _, _ = self.run_main(["--name", "create-me", "--table"], runner)
        self.assertEqual(code, 0)
        cmd = " ".join(runner.calls[0])
        self.assertIn("--name=create-me", cmd)

    def test_readonly_instance_id_containing_verb_not_blocked(self):
        runner = FakeRunner([(json.dumps(EMPTY_RESPONSE), "", 0)])
        code, _, _ = self.run_main(
            ["--instance-id", "create-instance-01"], runner)
        self.assertEqual(code, 0)
        cmd = " ".join(runner.calls[0])
        self.assertIn("--id=create-instance-01", cmd)

    def test_limit_out_of_range(self):
        code, _, err = self.run_main(["--limit", str(MAX_LIMIT + 1)])
        self.assertEqual(code, 1)
        self.assertIn("--limit 超出范围", err)

    def test_offset_negative(self):
        code, _, err = self.run_main(["--offset", "-1"])
        self.assertEqual(code, 1)
        self.assertIn("--offset 不能为负数", err)

    def test_server_filters_forwarded(self):
        runner = FakeRunner([(json.dumps(EMPTY_RESPONSE), "", 0)])
        argv = ["--name", "dds", "--fuzzy", "--instance-id", "id-1",
                "--mode", "Single", "--datastore-type", "DDS-Community",
                "--vpc-id", "vpc-1", "--subnet-id", "subnet-1",
                "--tags", "env=prod"]
        code, _, _ = self.run_main(argv, runner)
        self.assertEqual(code, 0)
        cmd = " ".join(runner.calls[0])
        for expected in ("--name=*dds", "--id=id-1", "--mode=Single",
                         "--datastore_type=DDS-Community",
                         "--vpc_id=vpc-1", "--subnet_id=subnet-1",
                         "--tags=env=prod"):
            self.assertIn(expected, cmd)


class _Sink:
    def __init__(self, buffer):
        self.buffer = buffer

    def write(self, text):
        self.buffer.append(text)

    def flush(self):
        pass


@unittest.skipUnless(HAS_SDK, "huaweicloudsdkdds not installed")
class TestSdkFallback(unittest.TestCase):
    def test_sdk_pagination_and_signature(self):
        api, _client_class, request_class, _region = _sdk_api()

        class FakeResponse:
            def __init__(self, instances, total):
                self.instances = instances
                self.total_count = total

        class FakeClient:
            def __init__(self):
                self.requests = []

            def list_instances(self, request):
                self.requests.append(request)
                if len(self.requests) == 1:
                    return FakeResponse([type("I", (), {
                        "to_dict": lambda self: dict(INSTANCE_SHARDING)})()] * 2, 3)
                return FakeResponse([type("I", (), {
                    "to_dict": lambda self: dict(INSTANCE_REPLICA)})()], 3)

        client = FakeClient()
        instances = list_instances_via_sdk(
            "cn-north-4", name="dds", limit=2, project_id="proj-1", client=client)
        self.assertEqual(len(instances), 3)
        request = client.requests[0]
        self.assertIsInstance(request, request_class)
        self.assertEqual(int(request.limit), 2)
        self.assertEqual(int(request.offset), 0)
        self.assertEqual(request.name, "dds")
        self.assertEqual(request.id, None)
        self.assertEqual(int(client.requests[1].offset), 2)

    def test_sdk_api_module_is_v3(self):
        # The published huaweicloudsdkdds package ships only a v3 module.
        api, _client_class, request_class, _region = _sdk_api()
        self.assertEqual(api, "v3")
        self.assertIn("huaweicloudsdkdds.v3", request_class.__module__)

    def test_sdk_auth_error_mapping(self):
        class FakeClient:
            def list_instances(self, request):
                raise Exception("403 forbidden")

        with self.assertRaises(AuthError):
            list_instances_via_sdk("cn-north-4", client=FakeClient())


class TestRestFallback(unittest.TestCase):
    ENV = {
        "HUAWEICLOUD_SDK_AK": "ak-test",
        "HUAWEICLOUD_SDK_SK": "sk-test",
        "HUAWEICLOUD_SDK_PROJECT_ID": "proj-1",
    }

    def test_build_rest_url(self):
        url = build_rest_url("cn-north-4", "proj-1", {
            "name": "*dds demo", "limit": 10, "offset": 0, "id": None,
        })
        self.assertTrue(url.startswith(
            "https://dds.cn-north-4.myhuaweicloud.com/v3/proj-1/instances?"))
        self.assertIn("limit=10", url)
        self.assertIn("offset=0", url)
        self.assertIn("name=%2Adds%20demo", url)
        self.assertNotIn("id=", url)

    def test_sign_headers_are_deterministic(self):
        now = datetime.datetime(2026, 1, 2, 3, 4, 5, tzinfo=datetime.timezone.utc)
        args = ("GET", "/v3/proj-1/instances", {"limit": 1},
                "dds.cn-north-4.myhuaweicloud.com", "ak-test", "sk-test")
        first = _sign_headers(*args, now=now)
        second = _sign_headers(*args, now=now)
        self.assertEqual(first["Authorization"], second["Authorization"])
        self.assertEqual(first["X-Sdk-Date"], "20260102T030405Z")
        self.assertIn("SDK-HMAC-SHA256 Access=ak-test", first["Authorization"])
        self.assertIn("SignedHeaders=host;x-sdk-date", first["Authorization"])
        other = _sign_headers(*args[:5], "sk-other", now=now)
        self.assertNotEqual(first["Authorization"], other["Authorization"])

    def test_sign_headers_includes_security_token(self):
        headers = _sign_headers(
            "GET", "/v3/proj-1/instances", {}, "dds.cn-north-4.myhuaweicloud.com",
            "ak", "sk", security_token="tok")
        self.assertEqual(headers["X-Security-Token"], "tok")
        self.assertIn("x-security-token",
                      headers["Authorization"].split("SignedHeaders=")[1])

    def test_rest_pagination_and_filters(self):
        calls = []
        pages = [
            {"instances": [INSTANCE_SHARDING], "total_count": 2},
            {"instances": [INSTANCE_REPLICA], "total_count": 2},
        ]

        def fake_get(url, headers):
            calls.append((url, headers))
            return pages[len(calls) - 1]

        with mock.patch.dict(os.environ, self.ENV):
            instances = list_instances_via_rest(
                "cn-north-4", name="*dds", mode="Sharding", limit=1,
                project_id="proj-1", get_json=fake_get)
        self.assertEqual(len(instances), 2)
        self.assertEqual(len(calls), 2)
        self.assertIn("offset=0", calls[0][0])
        self.assertIn("offset=1", calls[1][0])
        self.assertIn("mode=Sharding", calls[0][0])
        self.assertIn("Authorization", calls[0][1])

    def test_rest_missing_credentials(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ConfigError):
                list_instances_via_rest(
                    "cn-north-4", project_id="proj-1", get_json=lambda *_: {})

    def test_rest_missing_project_id(self):
        env = {k: v for k, v in self.ENV.items()
               if k != "HUAWEICLOUD_SDK_PROJECT_ID"}
        with mock.patch.dict(os.environ, env, clear=True):
            with self.assertRaises(ConfigError):
                list_instances_via_rest(
                    "cn-north-4", project_id=None, get_json=lambda *_: {})

    def test_rest_error_body_mapping(self):
        with mock.patch.dict(os.environ, self.ENV):
            with self.assertRaises(AuthError):
                list_instances_via_rest(
                    "cn-north-4", project_id="proj-1",
                    get_json=lambda *_: {"error_code": "DBS.200001",
                                         "error_msg": "forbidden"})
            with self.assertRaises(ApiError):
                list_instances_via_rest(
                    "cn-north-4", project_id="proj-1",
                    get_json=lambda *_: {"error_code": "DBS.200002",
                                         "error_msg": "bad request"})

    def test_sdk_missing_falls_back_to_rest(self):
        with mock.patch.dict(os.environ, self.ENV):
            with mock.patch("list_dds._sdk_imports", side_effect=ImportError("no sdk")):
                with mock.patch("list_dds._http_get_json",
                                return_value=PAGE_RESPONSE):
                    instances = list_instances_via_sdk(
                        "cn-north-4", limit=10, project_id="proj-1")
        self.assertEqual(len(instances), 1)
        self.assertEqual(instances[0]["id"], INSTANCE_SHARDING["id"])


if __name__ == "__main__":
    unittest.main()
