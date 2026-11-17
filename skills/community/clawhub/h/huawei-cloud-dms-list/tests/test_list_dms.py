import json
import os
import subprocess
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from list_dms import (  # noqa: E402
    ENGINE_OPERATION,
    ApiError,
    AuthError,
    ConfigError,
    DmsListError,
    GuardError,
    build_command,
    classify_hcloud_failure,
    extract_instances,
    extract_json,
    guard_operation,
    guard_write_intent,
    instance_names,
    list_all_engines,
    list_instances,
    list_instances_via_sdk,
    main,
    render_table,
)

try:
    import huaweicloudsdkkafka  # noqa: F401
    import huaweicloudsdkrabbitmq  # noqa: F401
    HAS_SDK = True
except ImportError:  # pragma: no cover - environment dependent
    HAS_SDK = False

INSTANCE_KAFKA = {
    "name": "dms-kafka-demo-01",
    "instance_id": "6c7f2f0e-0001-4f1f-9a11-111111111111",
    "engine": "kafka",
    "engine_version": "2.7",
    "specification": "c6.2u4g.cluster",
    "status": "RUNNING",
    "node_num": 3,
    "broker_num": 3,
    "storage_space": 300,
    "created_at": "2026-01-01T00:00:00Z",
    "vpc_name": "vpc-demo",
    "vpc_id": "vpc-0001",
    "subnet_name": "subnet-demo",
    "subnet_id": "subnet-0001",
    "connect_address": "192.168.0.10:9092",
    "port": 9092,
}
INSTANCE_RABBIT = {
    "name": "dms-rabbit-demo-02",
    "instance_id": "6c7f2f0e-0002-4f1f-9a11-222222222222",
    "engine": "rabbitmq",
    "engine_version": "3.8.35",
    "specification": "rabbitmq.2u4g.cluster",
    "status": "ERROR",
    "broker_num": 3,
    "storage_space": 100,
    "created_at": "2026-02-01T00:00:00Z",
    "vpc_id": "vpc-0002",
    "subnet_id": "subnet-0002",
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
            guard_write_intent("CreateInstance kafka-new")

    def test_delete_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--operation DeleteInstance")

    def test_batch_delete_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("BatchDeleteInstance")

    def test_mutating_verbs_blocked(self):
        for text in ("resize instance", "restart kafka-01", "update instance name",
                     "flush instance", "clear data", "restore backup",
                     "upgrade instance", "reset instance password",
                     "backup instance", "freeze instance", "release instance",
                     "migrate instance", "scale out"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_normalized_separators_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--create-instance")
        with self.assertRaises(GuardError):
            guard_write_intent("resize_instance")

    def test_readonly_values_pass(self):
        self.assertFalse(guard_write_intent("--status RUNNING"))
        self.assertFalse(guard_write_intent("--name dms-analytics"))
        # Gerund status values are legitimate DMS states, not write intents.
        self.assertFalse(guard_write_intent("--status CREATING"))
        self.assertFalse(guard_write_intent("--status DELETING"))

    def test_operation_guard_rejects_non_list(self):
        with self.assertRaises(GuardError):
            guard_operation("kafka", "CreateInstance")
        self.assertTrue(guard_operation("kafka", ENGINE_OPERATION["kafka"]))
        self.assertTrue(guard_operation("rabbitmq", ENGINE_OPERATION["rabbitmq"]))

    def test_operation_guard_rejects_unknown_engine(self):
        with self.assertRaises(GuardError):
            guard_operation("rocketmq", "ListInstances")


class TestBuildCommand(unittest.TestCase):
    def test_kafka_uses_kafka_service(self):
        # KooCLI has no "DMS" service; the engine name is the service name.
        argv = build_command("kafka", "cn-north-4")
        self.assertEqual(argv[0], "Kafka")
        self.assertEqual(argv[1], "ListInstances")
        self.assertIn("--engine=kafka", argv)
        self.assertIn("--cli-region=cn-north-4", argv)
        self.assertIn("--limit=50", argv)
        self.assertIn("--offset=0", argv)

    def test_rabbitmq_uses_rabbitmq_service(self):
        argv = build_command("rabbitmq", "cn-north-4")
        self.assertEqual(argv[0], "RabbitMQ")
        self.assertEqual(argv[1], "ListInstancesDetails")
        self.assertIn("--engine=rabbitmq", argv)

    def test_filters_forwarded_to_server(self):
        argv = build_command("kafka", "cn-north-4", name="dms", instance_id="id-9",
                             status="RUNNING", enterprise_project_id="0",
                             project_id="proj-1")
        self.assertIn("--name=dms", argv)
        self.assertIn("--instance_id=id-9", argv)
        self.assertIn("--status=RUNNING", argv)
        self.assertIn("--enterprise_project_id=0", argv)
        self.assertIn("--project_id=proj-1", argv)

    def test_exact_match_name_only_with_name(self):
        argv = build_command("kafka", "cn-north-4", name="dms", exact_match_name=True)
        self.assertIn("--exact_match_name=true", argv)
        argv = build_command("kafka", "cn-north-4", exact_match_name=True)
        self.assertNotIn("--exact_match_name=true", argv)

    def test_page_params(self):
        argv = build_command("rabbitmq", "cn-north-4", limit=10, offset=20)
        self.assertIn("--limit=10", argv)
        self.assertIn("--offset=20", argv)

    def test_no_write_flags_ever_added(self):
        argv = build_command("kafka", "cn-north-4", name="dms", status="RUNNING")
        joined = " ".join(argv).lower()
        for flag in ("create", "delete", "resize", "restart", "flush"):
            self.assertNotIn(flag, joined)

    def test_unknown_engine_rejected(self):
        with self.assertRaises(GuardError):
            build_command("rocketmq", "cn-north-4")


class TestExtractAndClassify(unittest.TestCase):
    def test_extract_instances_variants(self):
        self.assertEqual(extract_instances({"instances": [INSTANCE_KAFKA]}), [INSTANCE_KAFKA])
        self.assertEqual(extract_instances({"instance_list": [INSTANCE_RABBIT]}), [INSTANCE_RABBIT])
        self.assertEqual(extract_instances([INSTANCE_KAFKA]), [INSTANCE_KAFKA])
        self.assertEqual(extract_instances({"unknown": 1}), [])
        self.assertEqual(extract_instances({}), [])

    def test_extract_json_tolerates_noise(self):
        self.assertEqual(extract_json('{"instances": []}'), {"instances": []})
        self.assertEqual(extract_json('notice\n{"instances": []}\n'), {"instances": []})
        with self.assertRaises(ApiError):
            extract_json("not json at all")

    def test_use_error_is_hard_failure_even_at_rc0(self):
        exc = classify_hcloud_failure("[USE_ERROR]Invalid parameter: xxx", "", 0)
        self.assertIsInstance(exc, ApiError)
        self.assertIn("参数错误", str(exc))

    def test_403_maps_to_auth_error(self):
        exc = classify_hcloud_failure("", "403 Forbidden", 1)
        self.assertIsInstance(exc, AuthError)
        self.assertIn("IAM", str(exc))

    def test_missing_credentials_maps_to_config_error(self):
        exc = classify_hcloud_failure("", "ERROR: cli-ak empty", 1)
        self.assertIsInstance(exc, ConfigError)
        self.assertIn("AK/SK", str(exc))

    def test_generic_failure_maps_to_api_error(self):
        exc = classify_hcloud_failure("", "boom", 2)
        self.assertIsInstance(exc, ApiError)
        self.assertIn("退出码 2", str(exc))


class TestPaging(unittest.TestCase):
    def test_paging_follows_instance_num(self):
        results = [
            (json.dumps({"instances": [INSTANCE_KAFKA], "instance_num": 2}), "", 0),
            (json.dumps({"instances": [INSTANCE_RABBIT], "instance_num": 2}), "", 0),
        ]
        fake = FakeRunner(results)
        with mock.patch("list_dms.subprocess.run", fake):
            instances = list_instances("kafka", "cn-north-4", limit=1)
        self.assertEqual(len(instances), 2)
        self.assertIn("--offset=1", fake.calls[1])

    def test_short_page_stops_paging(self):
        fake = FakeRunner([
            (json.dumps({"instances": [INSTANCE_KAFKA]}), "", 0),
        ])
        with mock.patch("list_dms.subprocess.run", fake):
            instances = list_instances("kafka", "cn-north-4", limit=50)
        self.assertEqual(instances, [INSTANCE_KAFKA])
        self.assertEqual(len(fake.calls), 1)

    def test_empty_page_stops(self):
        fake = FakeRunner([(json.dumps({"instances": [], "instance_num": 0}), "", 0)])
        with mock.patch("list_dms.subprocess.run", fake):
            self.assertEqual(list_instances("rabbitmq", "cn-north-4"), [])

    def test_max_pages_guard(self):
        fake = FakeRunner([
            (json.dumps({"instances": [INSTANCE_KAFKA], "instance_num": 5}), "", 0),
            (json.dumps({"instances": [INSTANCE_KAFKA], "instance_num": 5}), "", 0),
        ])
        with mock.patch("list_dms.subprocess.run", fake):
            with self.assertRaises(ApiError):
                list_instances("kafka", "cn-north-4", limit=1, max_pages=2)

    def test_all_engines_queries_both_services(self):
        fake = FakeRunner([
            (json.dumps({"instances": [INSTANCE_KAFKA], "instance_num": 1}), "", 0),
            (json.dumps({"instances": [INSTANCE_RABBIT], "instance_num": 1}), "", 0),
        ])
        with mock.patch("list_dms.subprocess.run", fake):
            instances = list_all_engines("cn-north-4", ["kafka", "rabbitmq"])
        self.assertEqual(len(instances), 2)
        self.assertEqual(fake.calls[0][1], "Kafka")
        self.assertEqual(fake.calls[1][1], "RabbitMQ")


class _FakeSdkInstance:
    def __init__(self, data):
        self._data = data

    def to_dict(self):
        return dict(self._data)


class _FakeSdkResponse:
    def __init__(self, items, total):
        self.instances = [_FakeSdkInstance(i) for i in items]
        self.instance_num = total


class _FakeSdkClient:
    def __init__(self, engine, responses):
        call = mock.Mock(side_effect=responses)
        self.calls = call
        if engine == "kafka":
            self.list_instances = call
        else:
            self.list_instances_details = call


@unittest.skipUnless(HAS_SDK, "official DMS SDKs are not installed")
class TestSdkFallback(unittest.TestCase):
    def _clean_env(self, **overrides):
        env = {
            name: ""
            for name in (
                "HW_ACCESS_KEY", "HUAWEI_ACCESS_KEY", "HUAWEICLOUD_SDK_AK",
                "HUAWEI_CLOUD_ACCESS_KEY", "HW_SECRET_KEY", "HUAWEI_SECRET_KEY",
                "HUAWEICLOUD_SDK_SK", "HUAWEI_CLOUD_SECRET_KEY",
                "HW_PROJECT_ID", "HUAWEI_PROJECT_ID",
                "HUAWEICLOUD_SDK_PROJECT_ID", "HUAWEI_CLOUD_PROJECT_ID",
            )
        }
        env.update(overrides)
        return env

    def test_official_sdk_imports_resolve(self):
        from huaweicloudsdkkafka.v2 import KafkaClient, ListInstancesRequest
        from huaweicloudsdkkafka.v2.region.kafka_region import KafkaRegion
        from huaweicloudsdkrabbitmq.v2 import (
            RabbitMQClient, ListInstancesDetailsRequest,
        )
        from huaweicloudsdkrabbitmq.v2.region.rabbitmq_region import RabbitMQRegion
        for obj in (KafkaClient, ListInstancesRequest, KafkaRegion,
                    RabbitMQClient, ListInstancesDetailsRequest, RabbitMQRegion):
            self.assertTrue(callable(obj), obj)

    def test_sdk_fallback_kafka_returns_instances(self):
        client = _FakeSdkClient("kafka", [_FakeSdkResponse([INSTANCE_KAFKA], 1)])
        env = self._clean_env(HUAWEI_ACCESS_KEY="ak", HUAWEI_SECRET_KEY="sk",
                              HUAWEI_PROJECT_ID="proj")
        with mock.patch.dict(os.environ, env, clear=True):
            instances = list_instances_via_sdk("kafka", "cn-north-4", client=client)
        self.assertEqual(instances, [INSTANCE_KAFKA])
        request = client.calls.call_args_list[0][0][0]
        self.assertEqual(request.engine, "kafka")
        self.assertEqual(request.limit, "50")
        self.assertEqual(request.offset, "0")

    def test_sdk_fallback_rabbitmq_uses_details_operation(self):
        client = _FakeSdkClient("rabbitmq", [_FakeSdkResponse([INSTANCE_RABBIT], 1)])
        instances = list_instances_via_sdk("rabbitmq", "cn-north-4", client=client)
        self.assertEqual(instances, [INSTANCE_RABBIT])
        request = client.calls.call_args_list[0][0][0]
        self.assertEqual(request.engine, "rabbitmq")

    def test_sdk_filters_forwarded(self):
        client = _FakeSdkClient("kafka", [_FakeSdkResponse([], 0)])
        list_instances_via_sdk("kafka", "cn-north-4", name="demo", status="RUNNING",
                               instance_id="id-1", enterprise_project_id="0",
                               exact_match_name=True, client=client)
        request = client.calls.call_args_list[0][0][0]
        self.assertEqual(request.name, "demo")
        self.assertEqual(request.status, "RUNNING")
        self.assertEqual(request.instance_id, "id-1")
        self.assertEqual(request.enterprise_project_id, "0")
        self.assertEqual(request.exact_match_name, "true")

    def test_sdk_pagination_via_instance_num(self):
        client = _FakeSdkClient("kafka", [
            _FakeSdkResponse([INSTANCE_KAFKA], 2),
            _FakeSdkResponse([INSTANCE_RABBIT], 2),
        ])
        instances = list_instances_via_sdk("kafka", "cn-north-4", limit=1, client=client)
        self.assertEqual(len(instances), 2)
        second = client.calls.call_args_list[1][0][0]
        self.assertEqual(second.offset, "1")

    def test_sdk_missing_credentials_raises_config(self):
        env = self._clean_env(HUAWEI_PROJECT_ID="proj")
        with mock.patch.dict(os.environ, env, clear=True):
            with self.assertRaises(ConfigError) as ctx:
                list_instances_via_sdk("kafka", "cn-north-4")
        self.assertIn("AK/SK", str(ctx.exception))
        self.assertNotIn("未安装", str(ctx.exception))

    def test_sdk_missing_project_id_raises_config(self):
        env = self._clean_env(HUAWEI_ACCESS_KEY="ak", HUAWEI_SECRET_KEY="sk")
        with mock.patch.dict(os.environ, env, clear=True):
            with self.assertRaises(ConfigError) as ctx:
                list_instances_via_sdk("kafka", "cn-north-4")
        self.assertIn("project_id", str(ctx.exception))

    def test_sdk_client_build_uses_env_credentials(self):
        env = self._clean_env(HUAWEI_ACCESS_KEY="ak", HUAWEI_SECRET_KEY="sk",
                              HUAWEI_PROJECT_ID="proj")
        with mock.patch.dict(os.environ, env, clear=True):
            client = __import__("list_dms")._sdk_client("rabbitmq", "cn-north-4")
        self.assertEqual(client._credentials.ak, "ak")
        self.assertEqual(client._credentials.sk, "sk")
        self.assertEqual(client._credentials.project_id, "proj")
        # The SDK client exposes the resolved endpoints, not a Region object.
        self.assertEqual(client._endpoints, ["https://dms.cn-north-4.myhuaweicloud.com"])


class TestRender(unittest.TestCase):
    def test_names(self):
        self.assertEqual(instance_names([INSTANCE_KAFKA, INSTANCE_RABBIT]),
                         ["dms-kafka-demo-01", "dms-rabbit-demo-02"])

    def test_names_fallback_to_instance_id(self):
        self.assertEqual(instance_names([{"instance_id": "id-9"}]), ["id-9"])

    def test_table_headers_follow_acceptance_columns(self):
        table = render_table([INSTANCE_KAFKA])
        header = table.splitlines()[0]
        for col in ("实例ID", "名称", "引擎", "版本", "规格", "状态",
                    "节点数", "存储空间", "创建时间", "VPC", "子网", "连接地址"):
            self.assertIn(col, header)

    def test_table_values(self):
        table = render_table([INSTANCE_KAFKA, INSTANCE_RABBIT])
        for fragment in ("dms-kafka-demo-01", "6c7f2f0e-0001", "kafka", "2.7",
                         "c6.2u4g.cluster", "RUNNING", "300 GB",
                         "2026-01-01T00:00:00Z", "vpc-demo", "subnet-demo",
                         "192.168.0.10:9092", "dms-rabbit-demo-02", "ERROR"):
            self.assertIn(fragment, table)

    def test_missing_fields_render_dash(self):
        table = render_table([{"instance_id": "idx"}])
        row = table.splitlines()[2]
        self.assertEqual(row.count("-"), 11)

    def test_vpc_and_subnet_fall_back_to_ids(self):
        table = render_table([INSTANCE_RABBIT])
        self.assertIn("vpc-0002", table)
        self.assertIn("subnet-0002", table)

    def test_node_num_falls_back_to_broker_num(self):
        table = render_table([{"instance_id": "id", "broker_num": 3}])
        self.assertIn("3", table.splitlines()[2])


class TestMain(unittest.TestCase):
    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("list_dms.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            rc = main(argv)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    def test_default_output_is_names_list(self):
        for argv in ([], ["--names-only"]):
            rc, out, err = self._run(
                argv,
                [(json.dumps({"instances": [INSTANCE_KAFKA], "instance_num": 1}), "", 0),
                 (json.dumps({"instances": [INSTANCE_RABBIT], "instance_num": 1}), "", 0)])
            self.assertEqual(rc, 0)
            self.assertIn("DMS 实例名称列表", out)
            self.assertIn("- dms-kafka-demo-01", out)
            self.assertIn("- dms-rabbit-demo-02", out)
            self.assertNotIn("instance_id", out)

    def test_table_output(self):
        rc, out, err = self._run(
            ["--table"],
            [(json.dumps({"instances": [INSTANCE_KAFKA], "instance_num": 1}), "", 0),
             (json.dumps({"instances": [], "instance_num": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("DMS 实例列表", out)
        self.assertIn("dms-kafka-demo-01", out)
        self.assertEqual(err, "")

    def test_json_output(self):
        rc, out, err = self._run(
            ["--json"],
            [(json.dumps({"instances": [INSTANCE_KAFKA], "instance_num": 1}), "", 0),
             (json.dumps({"instances": [], "instance_num": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out), [INSTANCE_KAFKA])

    def test_empty_region_message(self):
        rc, out, err = self._run(
            ["--region", "cn-south-1"],
            [(json.dumps({"instances": [], "instance_num": 0}), "", 0),
             (json.dumps({"instances": [], "instance_num": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("当前区域（cn-south-1）无 DMS 实例", out)

    def test_empty_with_filter_message(self):
        rc, out, _ = self._run(
            ["--table", "--status", "RUNNING"],
            [(json.dumps({"instances": [], "instance_num": 0}), "", 0),
             (json.dumps({"instances": [], "instance_num": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("status=RUNNING", out)

    def test_engine_filter_runs_single_service(self):
        fake = FakeRunner([
            (json.dumps({"instances": [INSTANCE_RABBIT], "instance_num": 1}), "", 0),
        ])
        with mock.patch("list_dms.subprocess.run", fake), \
                mock.patch("sys.stdout"), mock.patch("sys.stderr"):
            rc = main(["--engine", "rabbitmq"])
        self.assertEqual(rc, 0)
        self.assertEqual(len(fake.calls), 1)
        self.assertEqual(fake.calls[0][1], "RabbitMQ")

    def test_filters_forwarded_to_hcloud(self):
        fake = FakeRunner([
            (json.dumps({"instances": [INSTANCE_KAFKA], "instance_num": 1}), "", 0),
        ])
        with mock.patch("list_dms.subprocess.run", fake), \
                mock.patch("sys.stdout"), mock.patch("sys.stderr"):
            rc = main(["--engine", "kafka", "--name", "dms-kafka-demo-01",
                       "--name-equal", "--status", "RUNNING", "--instance-id", "id-1"])
        self.assertEqual(rc, 0)
        joined = " ".join(fake.calls[0])
        for fragment in ("--name=dms-kafka-demo-01", "--exact_match_name=true",
                         "--status=RUNNING", "--instance_id=id-1"):
            self.assertIn(fragment, joined)

    def test_limit_and_offset_forwarded(self):
        fake = FakeRunner([
            (json.dumps({"instances": [INSTANCE_KAFKA], "instance_num": 10}), "", 0),
            (json.dumps({"instances": [], "instance_num": 10}), "", 0),
        ])
        with mock.patch("list_dms.subprocess.run", fake), \
                mock.patch("sys.stdout"), mock.patch("sys.stderr"):
            main(["--engine", "kafka", "--limit", "10", "--offset", "5"])
        joined = " ".join(fake.calls[0])
        self.assertIn("--limit=10", joined)
        self.assertIn("--offset=5", joined)

    def test_single_page_sends_one_call(self):
        fake = FakeRunner([
            (json.dumps({"instances": [INSTANCE_KAFKA], "instance_num": 10}), "", 0),
        ])
        with mock.patch("list_dms.subprocess.run", fake), \
                mock.patch("sys.stdout"), mock.patch("sys.stderr"):
            rc = main(["--engine", "kafka", "--limit", "1", "--single-page"])
        self.assertEqual(rc, 0)
        self.assertEqual(len(fake.calls), 1)

    def test_limit_out_of_range(self):
        rc, out, err = self._run(["--limit", "51"], [])
        self.assertEqual(rc, 1)
        self.assertIn("limit", err)

    def test_negative_offset_rejected(self):
        rc, out, err = self._run(["--offset", "-1"], [])
        self.assertEqual(rc, 1)
        self.assertIn("offset", err)

    def test_auth_error_message(self):
        rc, out, err = self._run(["--engine", "kafka"], [("", "403 Forbidden", 1)])
        self.assertEqual(rc, 1)
        self.assertIn("[错误]", err)
        self.assertIn("IAM", err)

    def test_missing_ak_sk_error_message(self):
        rc, out, err = self._run(["--engine", "kafka"], [("", "ERROR: cli-ak empty", 1)])
        self.assertEqual(rc, 1)
        self.assertIn("AK/SK", err)

    def test_use_error_exit_code(self):
        rc, out, err = self._run(["--engine", "kafka"],
                                 [("[USE_ERROR]Invalid parameter: engine", "", 0)])
        self.assertEqual(rc, 1)
        self.assertIn("参数错误", err)

    def test_hcloud_not_installed_and_sdk_missing(self):
        with mock.patch("list_dms.list_instances_via_sdk",
                        side_effect=ConfigError("官方 SDK 未安装")):
            rc, out, err = self._run(["--engine", "kafka"], [FileNotFoundError()])
        self.assertEqual(rc, 1)
        self.assertIn("未安装", err)

    def test_hcloud_missing_falls_back_to_sdk(self):
        with mock.patch("list_dms.list_instances_via_sdk",
                        return_value=[INSTANCE_KAFKA]):
            rc, out, err = self._run(["--engine", "kafka"], [FileNotFoundError()])
        self.assertEqual(rc, 0)
        self.assertIn("dms-kafka-demo-01", out)

    def test_project_id_forwarded_to_sdk(self):
        with mock.patch("list_dms.list_instances_via_sdk",
                        return_value=[INSTANCE_KAFKA]) as sdk_mock:
            rc, out, err = self._run(
                ["--engine", "kafka", "--project-id", "proj-9"], [FileNotFoundError()])
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

    def test_no_write_intent_executes_no_command(self):
        fake = FakeRunner([])
        with mock.patch("list_dms.subprocess.run", fake), \
                mock.patch("sys.stdout"), mock.patch("sys.stderr"):
            rc = main(["--operation", "CreateInstance"])
        self.assertEqual(rc, 1)
        self.assertEqual(fake.calls, [])


class TestErrorHierarchy(unittest.TestCase):
    def test_subclasses(self):
        for exc in (GuardError, ConfigError, AuthError, ApiError):
            self.assertTrue(issubclass(exc, DmsListError))


if __name__ == "__main__":
    unittest.main()