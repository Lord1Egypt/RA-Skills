import io
import json
import os
import sys
import types
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest import mock

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

import list_apig_instances as apig  # noqa: E402

INSTANCE_1 = {
    "id": "c16795b9553d422a8cb1977a2279113f",
    "instance_name": "apig-prod-01",
    "status": "Running",
    "spec": "BASIC",
    "project_id": "01a047a388a673259d93fb7137dbbb8a",
    "eip_address": "1.2.3.4",
    "create_time": 1791624977086,
    "type": "apig",
    "instance_status": 6,
}
INSTANCE_2 = {
    "id": "0f0e0d0c0b0a09080706050403020100",
    "instance_name": "apig-test-02",
    "status": "CreateSuccess",
    "spec": "PROFESSIONAL",
    "create_time": "2024-05-01T08:00:00Z",
}
API_1 = {
    "id": "bb1d768e81b1413ca646076eeedb9f56",
    "name": "community-skill-ranking",
    "type": 1,
    "version": "V0.0.1",
    "req_method": "POST",
    "req_protocol": "HTTPS",
    "req_uri": "/v1/community-skills/ranking",
    "auth_type": "APP",
    "status": 1,
    "group_name": "hdskills-community",
    "register_time": "2026-11-05T03:46:48Z",
}
API_2 = {
    "id": "a9bd25c4e3a2420aaed9bcee5fddf1d7",
    "name": "latest",
    "req_method": "GET",
    "req_protocol": "HTTPS",
    "req_uri": "/api/quality/cli/latest",
    "status": 2,
}


def instances_payload(records, total=None):
    return json.dumps({
        "total": len(records) if total is None else total,
        "size": len(records),
        "instances": records,
    })


def apis_payload(records, total=None):
    return json.dumps({
        "total": len(records) if total is None else total,
        "size": len(records),
        "apis": records,
    })


class FakeHcloud:
    """Replacement for run_hcloud returning canned (stdout, stderr, rc)."""

    def __init__(self, results):
        self.results = list(results)
        self.calls = []

    def __call__(self, argv):
        self.calls.append(list(argv))
        if not self.results:
            raise AssertionError("unexpected extra hcloud call: %s" % argv)
        result = self.results.pop(0)
        if isinstance(result, Exception):
            raise result
        return result


class TestWriteIntentGuard(unittest.TestCase):
    def test_read_intent_passes(self):
        self.assertFalse(apig.guard_write_intent("--region cn-north-4 --json"))
        self.assertFalse(apig.guard_write_intent("list apig instances"))
        self.assertFalse(apig.guard_write_intent("show apis of instance"))

    def test_create_delete_blocked(self):
        for text in ("create instance", "delete instance",
                     "CreateInstanceV2", "DeleteInstanceV2"):
            with self.assertRaises(apig.GuardError):
                apig.guard_write_intent(text)

    def test_update_publish_offline_blocked(self):
        for text in ("update api", "publish api", "offline api",
                     "PublishApiV2", "OfflineApiV2",
                     "batch-publish-api", "batch_offline_api"):
            with self.assertRaises(apig.GuardError):
                apig.guard_write_intent(text)

    def test_eip_binding_blocked(self):
        for text in ("bind-eip", "unbind-eip", "BindEip", "unbind_eip",
                     "add-eip", "delete eip"):
            with self.assertRaises(apig.GuardError):
                apig.guard_write_intent(text)

    def test_normalized_separators_blocked(self):
        with self.assertRaises(apig.GuardError):
            apig.guard_write_intent("--delete-api")
        with self.assertRaises(apig.GuardError):
            apig.guard_write_intent("delete_api_v2")

    def test_filter_values_not_scanned(self):
        # A resource literally named `create-api` must stay queryable.
        text = apig.guard_scan_text(["--name", "create-api", "--fuzzy"])
        self.assertFalse(apig.guard_write_intent(text))
        text = apig.guard_scan_text(["--instance-id=delete-me-01"])
        self.assertFalse(apig.guard_write_intent(text))

    def test_scan_text_keeps_flags(self):
        text = apig.guard_scan_text(["--delete-api", "--name", "x"])
        self.assertIn("--delete-api", text)

    def test_operation_whitelist(self):
        with self.assertRaises(apig.GuardError):
            apig.guard_operation("DeleteApiV2")
        with self.assertRaises(apig.GuardError):
            apig.guard_operation("ShowInstanceV2")
        self.assertTrue(apig.guard_operation(apig.OP_LIST_INSTANCES))
        self.assertTrue(apig.guard_operation(apig.OP_LIST_APIS))


class TestBuildCommands(unittest.TestCase):
    def test_instance_command(self):
        argv = apig.build_instance_command("cn-north-4", limit=10, offset=20)
        self.assertEqual(argv[0], "APIG")
        self.assertEqual(argv[1], "ListInstancesV2")
        self.assertIn("--cli-region=cn-north-4", argv)
        self.assertIn("--limit=10", argv)
        self.assertIn("--offset=20", argv)
        self.assertFalse(any(a.startswith("--instance_id") for a in argv))

    def test_instance_command_with_id(self):
        argv = apig.build_instance_command("cn-south-1", limit=1, offset=0,
                                           instance_id=INSTANCE_1["id"])
        self.assertIn("--instance_id=%s" % INSTANCE_1["id"], argv)
        self.assertIn("--cli-region=cn-south-1", argv)

    def test_instance_command_clamps_limit(self):
        argv = apig.build_instance_command("cn-north-4", limit=5000)
        self.assertIn("--limit=100", argv)
        argv = apig.build_instance_command("cn-north-4", limit=0)
        self.assertIn("--limit=1", argv)

    def test_apis_command(self):
        argv = apig.build_apis_command("cn-north-4", "inst-1", limit=5, offset=10)
        self.assertEqual(argv[1], "ListApisV2")
        self.assertIn("--instance_id=inst-1", argv)
        self.assertIn("--limit=5", argv)
        self.assertIn("--offset=10", argv)

    def test_apis_command_requires_instance_id(self):
        with self.assertRaises(apig.GuardError):
            apig.build_apis_command("cn-north-4", "")

    def test_only_read_operations_constructed(self):
        for argv in (apig.build_instance_command("cn-north-4"),
                     apig.build_apis_command("cn-north-4", "inst-1")):
            self.assertIn(argv[1], apig.ALLOWED_OPERATIONS)


class TestPaging(unittest.TestCase):
    def test_page_size(self):
        self.assertEqual(apig._page_size(10), 10)
        self.assertEqual(apig._page_size(100), apig.PAGE_STEP)
        self.assertEqual(apig._page_size(5000), apig.PAGE_STEP)

    def test_two_pages_offset_advances(self):
        page_one = [dict(INSTANCE_1, id="inst-%03d" % index) for index in range(50)]
        page_two = [dict(INSTANCE_2, id="inst-%03d" % index) for index in range(50)]
        runner = FakeHcloud([
            (instances_payload(page_one, total=120), "", 0),
            (instances_payload(page_two, total=120), "", 0),
        ])
        with mock.patch.object(apig, "run_hcloud", runner):
            records = apig.list_instances("cn-north-4", limit=100)
        self.assertEqual(len(records), 100)
        self.assertEqual(len(runner.calls), 2)
        self.assertIn("--offset=0", runner.calls[0])
        self.assertIn("--offset=50", runner.calls[1])
        self.assertIn("--limit=50", runner.calls[0])

    def test_stops_at_limit(self):
        runner = FakeHcloud([
            (instances_payload([INSTANCE_1, INSTANCE_2]), "", 0),
            (instances_payload([INSTANCE_1, INSTANCE_2]), "", 0),
        ])
        with mock.patch.object(apig, "run_hcloud", runner):
            records = apig.list_instances("cn-north-4", limit=2)
        self.assertEqual(len(records), 2)
        self.assertEqual(len(runner.calls), 1)

    def test_total_bound_prevents_extra_page(self):
        runner = FakeHcloud([
            (instances_payload([INSTANCE_1], total=1), "", 0),
        ])
        with mock.patch.object(apig, "run_hcloud", runner):
            records = apig.list_instances("cn-north-4", limit=1)
        self.assertEqual(len(records), 1)
        self.assertEqual(len(runner.calls), 1)

    def test_empty_page_breaks(self):
        runner = FakeHcloud([(instances_payload([], total=0), "", 0)])
        with mock.patch.object(apig, "run_hcloud", runner):
            self.assertEqual(apig.list_instances("cn-north-4", limit=10), [])


class TestParsingAndErrors(unittest.TestCase):
    def test_extract_json_with_noise(self):
        payload = apig.extract_json('tofu> %s\n100' % instances_payload([INSTANCE_1]))
        self.assertIn("instances", payload)

    def test_extract_json_garbage(self):
        with self.assertRaises(apig.ApiError):
            apig.extract_json("not json at all")

    def test_extract_records(self):
        records, total = apig.extract_records(
            {"total": 7, "apis": [API_1]}, "apis")
        self.assertEqual(len(records), 1)
        self.assertEqual(total, 7)

    def test_extract_records_missing_key(self):
        self.assertEqual(apig.extract_records({"total": 0}, "instances"), ([], None))

    def test_payload_error_detects_envelope(self):
        self.assertEqual(
            apig._payload_error({"error_code": "APIGW.0301", "error_msg": "denied"}),
            "APIGW.0301 denied")

    def test_payload_error_ignores_success(self):
        self.assertIsNone(apig._payload_error({"instances": []}))
        self.assertIsNone(apig._payload_error({"apis": []}))

    def test_use_error_marker_failure(self):
        err = apig.classify_hcloud_failure(
            "[USE_ERROR]Invalid parameter", "", 0)
        self.assertIsInstance(err, apig.ApiError)
        self.assertIn("hcloud 参数错误", str(err))

    def test_missing_credentials_failure(self):
        err = apig.classify_hcloud_failure(
            "", "cli-ak is empty, please configure credentials", 1)
        self.assertIsInstance(err, apig.ConfigError)
        self.assertIn("缺少 AK/SK", str(err))

    def test_401_reported_as_auth(self):
        err = apig.classify_hcloud_failure("", "401 Unauthorized", 1)
        self.assertIsInstance(err, apig.AuthError)
        self.assertIn("凭证无效", str(err))

    def test_403_reported_as_permission(self):
        err = apig.classify_hcloud_failure("", "403 Forbidden", 1)
        self.assertIsInstance(err, apig.AuthError)
        self.assertIn("无权限访问 APIG", str(err))
        self.assertIn("apig:instances:list", str(err))

    def test_generic_failure(self):
        err = apig.classify_hcloud_failure("", "boom", 1)
        self.assertIsInstance(err, apig.ApiError)

    def test_sdk_auth_error_split(self):
        exc = Exception("APIGW.0301 unauthorized")
        exc.status_code = 401
        self.assertIn("凭证无效", str(apig._sdk_auth_error(exc)))
        exc = Exception("permission denied")
        exc.status_code = 403
        self.assertIn("无权限访问 APIG", str(apig._sdk_auth_error(exc)))


class TestSdkFallback(unittest.TestCase):
    def test_cli_missing_falls_back_to_sdk(self):
        runner = FakeHcloud([apig.ConfigError("no hcloud")])
        with mock.patch.object(apig, "run_hcloud", runner), \
                mock.patch.object(apig, "list_instances_via_sdk",
                                 return_value=[INSTANCE_1]) as sdk:
            records = apig.list_instances("cn-north-4", limit=10)
        self.assertEqual(records, [INSTANCE_1])
        sdk.assert_called_once()
        self.assertEqual(len(runner.calls), 1)

    def test_apis_cli_missing_falls_back_to_sdk(self):
        runner = FakeHcloud([apig.ConfigError("no hcloud")])
        with mock.patch.object(apig, "run_hcloud", runner), \
                mock.patch.object(apig, "list_apis_via_sdk",
                                 return_value=[API_1]) as sdk:
            records = apig.list_apis("cn-north-4", INSTANCE_1["id"], limit=10)
        self.assertEqual(records, [API_1])
        sdk.assert_called_once()

    def test_sdk_missing_credentials(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(apig.ConfigError):
                apig._build_sdk_client("cn-north-4")

    def test_sdk_sdk_unavailable_message(self):
        with mock.patch.dict(sys.modules,
                             {"huaweicloudsdkapig": None}):
            with self.assertRaises(apig.ConfigError):
                apig._build_sdk_client("cn-north-4")


class FakeRequest(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)


class FakeItem(object):
    def __init__(self, data):
        self._data = data

    def to_dict(self):
        return dict(self._data)


class FakeResponse(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class TestSdkRequests(unittest.TestCase):
    def _fake_modules(self):
        module = types.ModuleType("huaweicloudsdkapig.v2")
        module.ListInstancesV2Request = FakeRequest
        module.ListApisV2Request = FakeRequest
        package = types.ModuleType("huaweicloudsdkapig")
        return {"huaweicloudsdkapig": package, "huaweicloudsdkapig.v2": module}

    def test_list_instances_request_signature(self):
        client = mock.Mock()
        client.list_instances_v2.return_value = FakeResponse(
            instances=[FakeItem(INSTANCE_1)], total=1)
        with mock.patch.dict(sys.modules, self._fake_modules()), \
                mock.patch.object(apig, "_build_sdk_client", return_value=client):
            records = apig.list_instances_via_sdk("cn-north-4", limit=10)
        self.assertEqual(records[0]["id"], INSTANCE_1["id"])
        request = client.list_instances_v2.call_args[0][0]
        self.assertEqual(request.limit, 10)
        self.assertEqual(request.offset, 0)

    def test_list_apis_request_signature(self):
        client = mock.Mock()
        client.list_apis_v2.return_value = FakeResponse(apis=[FakeItem(API_1)],
                                                        total=1)
        with mock.patch.dict(sys.modules, self._fake_modules()), \
                mock.patch.object(apig, "_build_sdk_client", return_value=client):
            records = apig.list_apis_via_sdk("cn-north-4", "inst-1", limit=5)
        self.assertEqual(records[0]["name"], API_1["name"])
        request = client.list_apis_v2.call_args[0][0]
        self.assertEqual(request.instance_id, "inst-1")
        self.assertEqual(request.limit, 5)

    def test_list_apis_sdk_requires_instance_id(self):
        with self.assertRaises(apig.GuardError):
            apig.list_apis_via_sdk("cn-north-4", "")


class TestFiltersAndRendering(unittest.TestCase):
    def test_exact_name_filter(self):
        result = apig.filter_records([INSTANCE_1, INSTANCE_2], name="apig-prod-01")
        self.assertEqual(len(result), 1)

    def test_fuzzy_name_filter(self):
        result = apig.filter_records([INSTANCE_1, INSTANCE_2], name="TEST",
                                     fuzzy=True)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], INSTANCE_2["id"])

    def test_status_filter_client_side(self):
        result = apig.filter_records([INSTANCE_1, INSTANCE_2], status="Running")
        self.assertEqual(len(result), 1)

    def test_api_name_filter_uses_api_key(self):
        result = apig.filter_records([API_1, API_2], name="latest",
                                     name_keys=("name", "id"))
        self.assertEqual(len(result), 1)

    def test_format_create_time_millis(self):
        self.assertEqual(apig.format_create_time(1791624977086),
                         "2026-10-10 09:36:17 UTC")

    def test_format_create_time_passthrough(self):
        self.assertEqual(apig.format_create_time("2024-05-01T08:00:00Z"),
                         "2024-05-01T08:00:00Z")
        self.assertEqual(apig.format_create_time(None), "-")

    def test_instance_table_columns(self):
        table = apig.render_instance_table([INSTANCE_1])
        for header in ("实例ID", "名称", "状态", "规格", "版本", "可用区",
                       "EIP", "VPC", "创建时间"):
            self.assertIn(header, table)
        self.assertIn("apig-prod-01", table)
        self.assertIn("2026-10-10 09:36:17 UTC", table)

    def test_instance_table_missing_field_is_dash(self):
        table = apig.render_instance_table([INSTANCE_1])
        row = [line for line in table.splitlines() if "apig-prod-01" in line][0]
        self.assertIn("BASIC", row)

    def test_api_table_columns(self):
        table = apig.render_api_table([API_1])
        for header in ("API_ID", "名称", "请求方法", "路径", "状态"):
            self.assertIn(header, table)

    def test_compact_lines(self):
        line = apig.compact_instance_lines([INSTANCE_1])[0]
        self.assertIn("apig-prod-01", line)
        self.assertIn(INSTANCE_1["id"], line)
        self.assertIn("Running", line)
        api_line = apig.compact_api_lines([API_1])[0]
        self.assertIn("POST", api_line)
        self.assertIn("/v1/community-skills/ranking", api_line)


class TestMain(unittest.TestCase):
    def _run(self, argv, results, sdk_instances=None, sdk_apis=None):
        runner = FakeHcloud(results)
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.object(apig, "run_hcloud", runner), \
                mock.patch.object(apig, "list_instances_via_sdk",
                                  return_value=sdk_instances or []), \
                mock.patch.object(apig, "list_apis_via_sdk",
                                  return_value=sdk_apis or []), \
                redirect_stdout(out), redirect_stderr(err):
            code = apig.main(argv)
        return code, out.getvalue(), err.getvalue(), runner

    def test_default_compact_list(self):
        code, out, _err, _ = self._run(
            ["--region", "cn-north-4"], [(instances_payload([INSTANCE_1]), "", 0)])
        self.assertEqual(code, 0)
        self.assertIn("APIG 专享版实例", out)
        self.assertIn("apig-prod-01", out)
        self.assertNotIn("实例ID", out)

    def test_table_mode(self):
        code, out, _err, _ = self._run(
            ["--table"], [(instances_payload([INSTANCE_1]), "", 0)])
        self.assertEqual(code, 0)
        self.assertIn("实例ID", out)
        self.assertIn("BASIC", out)

    def test_json_mode(self):
        code, out, _err, _ = self._run(
            ["--json"], [(instances_payload([INSTANCE_1]), "", 0)])
        self.assertEqual(code, 0)
        payload = json.loads(out)
        self.assertEqual(payload["region"], "cn-north-4")
        self.assertEqual(payload["count"], 1)
        self.assertEqual(payload["instances"][0]["id"], INSTANCE_1["id"])

    def test_empty_list_hint_exit_zero(self):
        code, out, _err, _ = self._run(
            ["--name", "nope"], [(instances_payload([], total=0), "", 0)])
        self.assertEqual(code, 0)
        self.assertIn("无 APIG 专享版实例", out)
        self.assertIn("name=nope", out)

    def test_empty_list_no_filter_hint(self):
        code, out, _err, _ = self._run([], [(instances_payload([], total=0), "", 0)])
        self.assertEqual(code, 0)
        self.assertIn("当前区域（cn-north-4）无 APIG 专享版实例", out)

    def test_client_side_name_filter(self):
        code, out, _err, runner = self._run(
            ["--name", "apig-test-02"],
            [(instances_payload([INSTANCE_1, INSTANCE_2]), "", 0)])
        self.assertEqual(code, 0)
        self.assertIn("apig-test-02", out)
        self.assertNotIn("apig-prod-01", out)
        # --name is client-side: no server-side instance_name parameter.
        self.assertFalse(any("instance_name" in call[3] or
                             any(a.startswith("--instance_name") for a in call)
                             for call in runner.calls))

    def test_instance_drill_down_compact(self):
        code, out, _err, _ = self._run(
            ["--instance-id", INSTANCE_1["id"]],
            [(instances_payload([INSTANCE_1]), "", 0),
             (apis_payload([API_1, API_2]), "", 0)])
        self.assertEqual(code, 0)
        self.assertIn("API 列表", out)
        self.assertIn("community-skill-ranking", out)

    def test_instance_drill_down_table(self):
        code, out, _err, _ = self._run(
            ["--instance-id", INSTANCE_1["id"], "--table"],
            [(instances_payload([INSTANCE_1]), "", 0),
             (apis_payload([API_1]), "", 0)])
        self.assertEqual(code, 0)
        self.assertIn("API_ID", out)
        self.assertIn("POST", out)

    def test_instance_drill_down_json(self):
        code, out, _err, _ = self._run(
            ["--instance-id", INSTANCE_1["id"], "--json"],
            [(instances_payload([INSTANCE_1]), "", 0),
             (apis_payload([API_1]), "", 0)])
        self.assertEqual(code, 0)
        payload = json.loads(out)
        self.assertEqual(payload["instance_id"], INSTANCE_1["id"])
        self.assertEqual(payload["count"], 1)
        self.assertEqual(payload["apis"][0]["name"], API_1["name"])

    def test_instance_drill_down_empty_apis(self):
        code, out, _err, _ = self._run(
            ["--instance-id", INSTANCE_1["id"], "--name", "missing"],
            [(instances_payload([INSTANCE_1]), "", 0),
             (apis_payload([API_1]), "", 0)])
        self.assertEqual(code, 0)
        self.assertIn("下无 API", out)

    def test_invalid_instance_id_exit_one(self):
        code, _out, err, _ = self._run(
            ["--instance-id", "0" * 32], [(instances_payload([], total=0), "", 0)])
        self.assertEqual(code, 1)
        self.assertIn("实例不存在", err)

    def test_write_intent_exit_one(self):
        code, _out, err, runner = self._run(["--delete-api"], [])
        self.assertEqual(code, 1)
        self.assertIn("写操作意图", err)
        self.assertEqual(runner.calls, [])

    def test_publish_intent_exit_one(self):
        code, _out, err, _ = self._run(["--publish"], [])
        self.assertEqual(code, 1)
        self.assertIn("写操作意图", err)

    def test_limit_out_of_range_rejected(self):
        for value in ("0", "101", "abc"):
            with redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as ctx:
                    apig.main(["--limit", value])
            self.assertEqual(ctx.exception.code, 2)

    def test_limit_bounds_accepted(self):
        code, _out, _err, _ = self._run(["--limit", "1"],
                                        [(instances_payload([INSTANCE_1]), "", 0)])
        self.assertEqual(code, 0)
        code, _out, _err, _ = self._run(["--limit", "100"],
                                        [(instances_payload([INSTANCE_1]), "", 0)])
        self.assertEqual(code, 0)

    def test_403_surfaces_error_and_exit_one(self):
        code, _out, err, _ = self._run(
            [], [(None, "403 Forbidden", 1)])
        self.assertEqual(code, 1)
        self.assertIn("无权限访问 APIG", err)

    def test_api_error_envelope_with_rc_zero(self):
        code, _out, err, _ = self._run(
            [], [(json.dumps({"error_code": "APIGW.0301",
                              "error_msg": "authentication failed"}), "", 0)])
        self.assertEqual(code, 1)
        self.assertIn("凭证无效", err)

    def test_missing_credentials_exit_one(self):
        code, _out, err, _ = self._run(
            [], [("", "cli-ak not configured", 1)])
        self.assertEqual(code, 1)
        self.assertIn("缺少 AK/SK", err)

    def test_sdk_fallback_in_main(self):
        runner = FakeHcloud([apig.ConfigError("no hcloud")])
        out = io.StringIO()
        with mock.patch.object(apig, "run_hcloud", runner), \
                mock.patch.object(apig, "list_instances_via_sdk",
                                  return_value=[INSTANCE_1]), \
                redirect_stdout(out), redirect_stderr(io.StringIO()):
            code = apig.main([])
        self.assertEqual(code, 0)
        self.assertIn("apig-prod-01", out.getvalue())


if __name__ == "__main__":
    unittest.main()