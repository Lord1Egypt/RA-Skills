#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""huawei-cloud-ces-alarm-rules-list 的离线单元测试（无凭据、无网络）。

所有 hcloud 调用都被 mock，覆盖：写意图守卫、命令构造、JSON/错误信封解析、
offset 翻页、告警状态补齐（v1）、客户端四类过滤、三种输出形态、单条详情
（策略 + 资源 + 通知）、SDK 回退与主流程退出码。

在 skill 目录下运行：
    python3 -m unittest discover -s tests -v
"""

import io
import json
import os
import sys
import unittest
from contextlib import redirect_stdout, redirect_stderr
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(os.path.dirname(HERE), "scripts")
sys.path.insert(0, SCRIPTS)
sys.dont_write_bytecode = True

import ces_alarm_rules as alarm  # noqa: E402


RULE_CPU = {
    "alarm_id": "al1111111111111111111111",
    "name": "cpu-high",
    "description": "CPU 持续偏高",
    "namespace": "SYS.ECS",
    "policies": [{
        "metric_name": "cpu_util",
        "dimension_name": "instance_id",
        "period": 1,
        "comparison_operator": ">=",
        "value": 80.0,
        "unit": "%",
        "count": 3,
        "level": 1,
    }],
    "resources": [{
        "resource_group_id": "rg-0001",
        "resource_group_name": "prod-ecs",
        "dimensions": [{"name": "instance_id", "value": "i-0001"}],
    }],
    "enabled": True,
    "notification_enabled": True,
    "alarm_notifications": [{"type": "SMN", "notification_list": ["urn:smn:1", "urn:smn:2"]}],
    "ok_notifications": [{"type": "SMN", "notification_list": ["urn:smn:1"]}],
}

RULE_DISK = {
    "alarm_id": "al2222222222222222222222",
    "name": "disk-busy",
    "namespace": "SYS.EVS",
    "policies": [{
        "metric_name": "disk_util_inband",
        "dimension_name": "disk_name",
        "comparison_operator": ">",
        "value": 90,
        "unit": "%",
        "count": 1,
        "level": 2,
    }],
    "resources": [{
        "resource_group_id": "rg-0002",
        "resource_group_name": "prod-evs",
        "dimensions": [{"name": "disk_name", "value": "vdb"}],
    }],
    "enabled": False,
    "notification_enabled": False,
    "alarm_notifications": [],
}


def _single_response(stdout="", stderr="", returncode=0):
    class P:
        pass

    proc = P()
    proc.stdout = stdout
    proc.stderr = stderr
    proc.returncode = returncode
    return proc


class FakeHcloud:
    """按 operation 返回预置 payload 的假 hcloud。"""

    def __init__(self, rules=None, states=None, policies=None, resources=None,
                 count=None, state_pages=None):
        self.rules = list(rules if rules is not None else [RULE_CPU, RULE_DISK])
        self.states = states if states is not None else {
            RULE_CPU["alarm_id"]: "ok",
            RULE_DISK["alarm_id"]: "insufficient_data",
        }
        self.policies = policies if policies is not None else RULE_CPU["policies"]
        self.resources = resources if resources is not None else RULE_CPU["resources"]
        self.count = count
        self.calls = []
        self.state_pages = state_pages

    @staticmethod
    def _param(argv, name, default=None):
        prefix = "--%s=" % name
        for tok in argv:
            if tok.startswith(prefix):
                return tok[len(prefix):]
        return default

    def __call__(self, argv):
        self.calls.append(list(argv))
        operation = argv[1] if len(argv) > 1 else ""
        if operation == alarm.OPERATION_LIST:
            alarm_id = self._param(argv, "alarm_id")
            if alarm_id:
                matched = [r for r in self.rules if r["alarm_id"] == alarm_id]
                return json.dumps({"alarms": matched, "count": len(matched)}), "", 0
            limit = int(self._param(argv, "limit", "50"))
            offset = int(self._param(argv, "offset", "0"))
            page = self.rules[offset:offset + limit]
            count = self.count if self.count is not None else len(self.rules)
            return json.dumps({"alarms": page, "count": count}), "", 0
        if operation == alarm.OPERATION_POLICIES:
            return json.dumps({"policies": self.policies, "count": len(self.policies)}), "", 0
        if operation == alarm.OPERATION_RESOURCES:
            return json.dumps({"resources": self.resources, "count": len(self.resources)}), "", 0
        if operation == alarm.OPERATION_STATE:
            limit = int(self._param(argv, "limit", "50"))
            start = self._param(argv, "start")
            ids = [r["alarm_id"] for r in self.rules]
            if start:
                ids = ids[ids.index(start):]
            page = ids[:limit]
            items = [{"alarm_id": aid, "alarm_state": self.states.get(aid, "ok")}
                     for aid in page]
            return json.dumps({"metric_alarms": items,
                               "meta_data": {"count": len(items),
                                             "total": len(self.rules)}}), "", 0
        return "{}", "", 0


def run_main(argv, fake=None):
    out, err = io.StringIO(), io.StringIO()
    with mock.patch.object(alarm, "run_hcloud", fake or FakeHcloud()), \
            redirect_stdout(out), redirect_stderr(err):
        code = alarm.main(argv)
    return code, out.getvalue(), err.getvalue()


class GuardTests(unittest.TestCase):
    def test_read_vocabulary_passes(self):
        for text in ("ListAlarmRules", "ListAlarmRulePolicies",
                     "ListAlarmRuleResources", "ces:alarm:list",
                     "hcloud CES ListAlarmRules --cli-region=cn-north-4"):
            self.assertFalse(alarm.guard_write_intent(text))

    def test_write_intents_blocked(self):
        for text in ("CreateAlarmRules", "delete-alarm", "UpdateAlarmRulePolicies",
                     "batch-delete", "BatchEnableAlarmRules", "enable alarm",
                     "disable_alarm", "add-alarm-rule-resources",
                     "DeleteAlarmRuleResources", "remove resource"):
            with self.assertRaises(alarm.GuardError):
                alarm.guard_write_intent(text)

    def test_operation_whitelist(self):
        for op in alarm.ALLOWED_OPERATIONS:
            self.assertTrue(alarm.guard_operation(op))
        for op in ("BatchDeleteAlarmRules", "CreateAlarm", "UpdateAlarmAction"):
            with self.assertRaises(alarm.GuardError):
                alarm.guard_operation(op)

    def test_value_flags_stripped(self):
        text = alarm.guard_text_from_argv(
            ["--name", "delete-me", "--resource-type", "batch-svc",
             "--region", "cn-north-4", "--json"])
        self.assertNotIn("delete-me", text)
        self.assertNotIn("batch-svc", text)
        self.assertIn("--json", text)

    def test_following_flag_still_scanned(self):
        text = alarm.guard_text_from_argv(["--name", "--enable-alarm"])
        self.assertIn("--enable-alarm", text)

    def test_main_rejects_write_intent_before_any_call(self):
        fake = mock.Mock(side_effect=AssertionError("hcloud must not be called"))
        code, out, err = run_main(["--region", "cn-north-4", "--delete-rule"], fake)
        self.assertEqual(code, 1)
        self.assertIn("写操作意图", err)
        self.assertEqual(out, "")
        fake.assert_not_called()


class CommandBuildTests(unittest.TestCase):
    def test_list_rules_params(self):
        argv = alarm.build_command(
            alarm.OPERATION_LIST, "cn-north-4", name="cpu", namespace="SYS.ECS",
            resource_id="i-1", enterprise_project_id="0", product_name="SYS.ECS,instance_id",
            resource_level="dimension", limit=100, offset=20)
        self.assertEqual(argv[:3], ["CES", "ListAlarmRules", "--cli-region=cn-north-4"])
        for expected in ("--name=cpu", "--namespace=SYS.ECS", "--resource_id=i-1",
                         "--enterprise_project_id=0",
                         "--product_name=SYS.ECS,instance_id",
                         "--resource_level=dimension", "--limit=100", "--offset=20"):
            self.assertIn(expected, argv)

    def test_list_rules_alarm_id(self):
        argv = alarm.build_command(alarm.OPERATION_LIST, "cn-north-4",
                                   alarm_id="al1", limit=1)
        self.assertIn("--alarm_id=al1", argv)

    def test_policies_and_resources_need_alarm_id(self):
        for op in (alarm.OPERATION_POLICIES, alarm.OPERATION_RESOURCES):
            argv = alarm.build_command(op, "cn-north-4", alarm_id="al1",
                                       limit=100, offset=0)
            self.assertIn("--alarm_id=al1", argv)
            self.assertIn("--limit=100", argv)
            self.assertIn("--offset=0", argv)

    def test_state_command(self):
        argv = alarm.build_command(alarm.OPERATION_STATE, "cn-north-4",
                                   start="al1", limit=100, order="asc")
        self.assertEqual(argv[1], "ListAlarms")
        self.assertIn("--start=al1", argv)
        self.assertIn("--order=asc", argv)
        self.assertIn("--limit=100", argv)

    def test_rest_paths(self):
        self.assertEqual(alarm.REST_PATHS[alarm.OPERATION_LIST],
                         "/v2/{project_id}/alarms")
        self.assertEqual(alarm.REST_PATHS[alarm.OPERATION_STATE],
                         "/V1.0/{project_id}/alarms")


class JsonAndEnvelopeTests(unittest.TestCase):
    def test_extract_json_with_noise(self):
        payload = alarm.extract_json('noise\n{"alarms": []}\n')
        self.assertEqual(payload, {"alarms": []})

    def test_extract_json_empty(self):
        self.assertEqual(alarm.extract_json(""), {})

    def test_extract_json_garbage(self):
        with self.assertRaises(alarm.ApiError):
            alarm.extract_json("not json at all")

    def test_payload_error_variants(self):
        self.assertTrue(alarm._payload_error(
            {"error": {"error_code": "CES.0004", "error_msg": "bad"}}))
        self.assertTrue(alarm._payload_error({"error_code": "X", "error_msg": "Y"}))
        self.assertIsNone(alarm._payload_error({"alarms": []}))

    def test_extract_items(self):
        self.assertEqual(alarm.extract_items({"alarms": [1]}, alarm.OPERATION_LIST), [1])
        self.assertEqual(alarm.extract_items({"metric_alarms": [2]},
                                             alarm.OPERATION_STATE), [2])
        self.assertEqual(alarm.extract_items({"resources": [[{"name": "a"}]]},
                                             alarm.OPERATION_RESOURCES),
                         [[{"name": "a"}]])


class PagingTests(unittest.TestCase):
    def test_offset_paging_until_count(self):
        rules = [dict(RULE_CPU, alarm_id="al%022d" % i, name="r%d" % i) for i in range(5)]
        fake = FakeHcloud(rules=rules)
        with mock.patch.object(alarm, "run_hcloud", fake):
            items = alarm.list_alarm_rules("cn-north-4", limit=2, offset=0,
                                           max_pages=10)
        self.assertEqual(len(items), 5)
        offsets = [FakeHcloud._param(c, "offset") for c in fake.calls]
        self.assertEqual(offsets, ["0", "2", "4"])

    def test_paging_stops_on_short_page(self):
        fake = FakeHcloud(rules=[RULE_CPU])
        with mock.patch.object(alarm, "run_hcloud", fake):
            items = alarm.list_alarm_rules("cn-north-4", limit=50)
        self.assertEqual(len(items), 1)
        self.assertEqual(len(fake.calls), 1)

    def test_start_offset_is_forwarded(self):
        fake = FakeHcloud(rules=[RULE_CPU])
        with mock.patch.object(alarm, "run_hcloud", fake):
            alarm.list_alarm_rules("cn-north-4", limit=1, offset=3)
        self.assertEqual(fake.calls[0][fake.calls[0].index("--offset=3")], "--offset=3")

    def test_name_passthrough_falls_back_when_server_returns_empty(self):
        class ExactNameOnly(FakeHcloud):
            def __call__(self, argv):
                if argv[1] == alarm.OPERATION_LIST and FakeHcloud._param(argv, "name"):
                    self.calls.append(list(argv))
                    return json.dumps({"alarms": [], "count": 0}), "", 0
                return FakeHcloud.__call__(self, argv)

        fake = ExactNameOnly()
        with mock.patch.object(alarm, "run_hcloud", fake):
            items = alarm.list_alarm_rules("cn-north-4", name="cpu", limit=50)
        self.assertEqual(len(items), 2)
        names = [FakeHcloud._param(c, "name") for c in fake.calls]
        self.assertEqual(names[0], "cpu")

    def test_max_pages_guard(self):
        class AlwaysFull(FakeHcloud):
            def __call__(self, argv):
                self.calls.append(list(argv))
                if argv[1] == alarm.OPERATION_LIST:
                    return json.dumps({"alarms": [RULE_CPU], "count": 999}), "", 0
                return "{}", "", 0

        fake = AlwaysFull()
        with mock.patch.object(alarm, "run_hcloud", fake):
            with self.assertRaises(alarm.ApiError):
                alarm.list_alarm_rules("cn-north-4", limit=1, max_pages=2)


class StateMapTests(unittest.TestCase):
    def test_state_map_and_chinese_names(self):
        fake = FakeHcloud()
        with mock.patch.object(alarm, "run_hcloud", fake):
            states = alarm.fetch_alarm_state_map("cn-north-4")
        self.assertEqual(states[RULE_CPU["alarm_id"]], "ok")
        self.assertEqual(states[RULE_DISK["alarm_id"]], "insufficient_data")
        self.assertEqual(alarm.state_name("ok"), "正常")
        self.assertEqual(alarm.state_name("OK"), "正常")
        self.assertEqual(alarm.state_name("insufficient_data"), "数据不足")
        self.assertNotEqual(alarm.state_name("insufficient_data"), "正常")
        self.assertEqual(alarm.state_name(None), alarm.STATE_UNKNOWN)

    def test_state_map_pages_by_start(self):
        rules = [dict(RULE_CPU, alarm_id="al%022d" % i) for i in range(4)]
        fake = FakeHcloud(rules=rules)
        with mock.patch.object(alarm, "run_hcloud", fake):
            states = alarm.fetch_alarm_state_map("cn-north-4", limit=2)
        self.assertEqual(len(states), 4)
        starts = [FakeHcloud._param(c, "start") for c in fake.calls]
        self.assertIsNone(starts[0])
        self.assertGreater(len(starts), 1)


class RuleRowTests(unittest.TestCase):
    def test_row_fields(self):
        row = alarm.rule_row(RULE_CPU, {RULE_CPU["alarm_id"]: "alarm"})
        self.assertEqual(row["规则ID"], RULE_CPU["alarm_id"])
        self.assertEqual(row["名称"], "cpu-high")
        self.assertEqual(row["资源类型"], "SYS.ECS")
        self.assertEqual(row["监控维度"], "instance_id")
        self.assertEqual(row["指标"], "cpu_util")
        self.assertIn(">=80.0%", row["阈值与比较符"])
        self.assertIn("连续 3 次", row["阈值与比较符"])
        self.assertIn("周期 1 秒", row["阈值与比较符"])
        self.assertEqual(row["告警级别"], "紧急")
        self.assertEqual(row["当前状态"], "告警")
        self.assertEqual(row["是否启用"], "启用")
        self.assertEqual(row["通知方式"], "SMN")

    def test_table_column_order(self):
        text = alarm.render_table([alarm.rule_row(RULE_CPU, {})], alarm.TABLE_COLUMNS)
        header = text.splitlines()[0]
        positions = [header.index(col) for col in alarm.TABLE_COLUMNS]
        self.assertEqual(positions, sorted(positions))

    def test_disabled_and_notification_off(self):
        row = alarm.rule_row(RULE_DISK, {RULE_DISK["alarm_id"]: "insufficient_data"})
        self.assertEqual(row["是否启用"], "停用")
        self.assertEqual(row["通知方式"], "未开启通知")
        self.assertEqual(row["当前状态"], "数据不足")

    def test_hierarchical_threshold(self):
        policy = {"comparison_operator": ">", "hierarchical_value":
                  {"critical": 90, "major": 80, "minor": 70}, "unit": "%",
                  "count": 1, "period": 5}
        text = alarm.format_threshold(policy)
        self.assertIn("紧急>90", text)
        self.assertIn("重要>80", text)
        self.assertIn("次要>70", text)
        # 分级阈值优先，单值阈值不重复打印
        self.assertNotIn(">90%", text)

    def test_dimension_without_value(self):
        self.assertEqual(alarm._format_dimension({"name": "rds_cluster_id"}),
                         "rds_cluster_id")
        self.assertEqual(alarm._format_dimension({"name": "instance_id",
                                                  "value": "i-1"}),
                         "instance_id=i-1")

    def test_level_names(self):
        self.assertEqual(alarm.level_name(1), "紧急")
        self.assertEqual(alarm.level_name("4"), "提示")
        self.assertEqual(alarm.level_name(None), "-")


class FilterTests(unittest.TestCase):
    def setUp(self):
        self.rules = [RULE_CPU, RULE_DISK]
        self.states = {RULE_CPU["alarm_id"]: "ok",
                       RULE_DISK["alarm_id"]: "insufficient_data"}

    def test_name_fuzzy(self):
        got = alarm.filter_rules(self.rules, self.states, name="CPU")
        self.assertEqual([r["name"] for r in got], ["cpu-high"])

    def test_name_matches_alarm_id(self):
        got = alarm.filter_rules(self.rules, self.states, name="al2222")
        self.assertEqual([r["name"] for r in got], ["disk-busy"])

    def test_level_filter(self):
        got = alarm.filter_rules(self.rules, self.states, levels={2})
        self.assertEqual([r["name"] for r in got], ["disk-busy"])

    def test_state_filter_keeps_insufficient_data_distinct(self):
        got = alarm.filter_rules(self.rules, self.states, states={"insufficient_data"})
        self.assertEqual([r["name"] for r in got], ["disk-busy"])
        got_ok = alarm.filter_rules(self.rules, self.states, states={"ok"})
        self.assertEqual([r["name"] for r in got_ok], ["cpu-high"])

    def test_parse_state_aliases(self):
        self.assertEqual(alarm.parse_state_filter(["数据不足"]), {"insufficient_data"})
        self.assertEqual(alarm.parse_state_filter(["OK,alarm"]), {"ok", "alarm"})
        with self.assertRaises(alarm.ApiError):
            alarm.parse_state_filter(["bogus"])

    def test_parse_level_filter(self):
        self.assertEqual(alarm.parse_level_filter(["1,提示"]), {1, 4})
        with self.assertRaises(alarm.ApiError):
            alarm.parse_level_filter(["9"])

    def test_resource_type_filter(self):
        self.assertEqual(
            [r["name"] for r in alarm.filter_rules(self.rules, self.states,
                                                   resource_type="sys.evs")],
            ["disk-busy"])
        self.assertEqual(
            [r["name"] for r in alarm.filter_rules(self.rules, self.states,
                                                   resource_type="instance_id")],
            ["cpu-high"])


class DetailTests(unittest.TestCase):
    def test_fetch_detail(self):
        fake = FakeHcloud()
        with mock.patch.object(alarm, "run_hcloud", fake):
            rule, policies, resources, payload = alarm._fetch_detail(
                "cn-north-4", RULE_CPU["alarm_id"])
        self.assertEqual(rule["alarm_id"], RULE_CPU["alarm_id"])
        self.assertEqual(len(policies), 1)
        self.assertEqual(len(resources), 1)
        ops = [c[1] for c in fake.calls]
        self.assertEqual(ops, [alarm.OPERATION_LIST, alarm.OPERATION_POLICIES,
                               alarm.OPERATION_RESOURCES])

    def test_render_detail_sections(self):
        text = alarm.render_detail(RULE_CPU, RULE_CPU["policies"],
                                   RULE_CPU["resources"], "cn-north-4", "ok")
        for expected in ("告警规则详情", "阈值策略", "关联资源", "通知对象",
                         "cpu_util", "prod-ecs", "instance_id=i-0001", "SMN"):
            self.assertIn(expected, text)

    def test_render_detail_marks_insufficient_data(self):
        text = alarm.render_detail(RULE_DISK, [], [], "cn-north-4",
                                   "insufficient_data")
        self.assertIn("数据不足", text)
        self.assertIn("（无策略数据）", text)

    def test_render_detail_tables(self):
        text = alarm.render_detail_tables(RULE_CPU, RULE_CPU["policies"],
                                          RULE_CPU["resources"], "cn-north-4", "alarm")
        self.assertIn("字段", text)
        self.assertIn("阈值策略", text)
        self.assertIn("通知对象", text)

    def test_two_dimensional_resource_shape(self):
        """实测：详情接口 resources 是 list[list[DimensionResp]]。"""
        resources = [[{"name": "rds_cluster_id", "value": "c-1"}]]
        text = alarm.render_detail(RULE_CPU, RULE_CPU["policies"], resources,
                                   "cn-north-4", "ok")
        self.assertIn("关联资源（1 组）", text)
        self.assertIn("rds_cluster_id=c-1", text)
        table = alarm.render_detail_tables(RULE_CPU, RULE_CPU["policies"],
                                           resources, "cn-north-4", "ok")
        self.assertIn("rds_cluster_id=c-1", table)

    def test_main_rule_id_json(self):
        code, out, _ = run_main(["--rule-id", RULE_CPU["alarm_id"], "--json"])
        self.assertEqual(code, 0)
        payload = json.loads(out)
        self.assertIn("alarm", payload)
        self.assertIn("policies", payload)
        self.assertIn("resources", payload)
        self.assertEqual(payload["alarm"]["alarm_id"], RULE_CPU["alarm_id"])

    def test_main_rule_id_not_found(self):
        code, out, _ = run_main(["--rule-id", "al9999999999999999999999"])
        self.assertEqual(code, 0)
        self.assertIn("未找到告警规则", out)

    def test_main_rule_id_default_is_readable(self):
        code, out, _ = run_main(["--rule-id", RULE_CPU["alarm_id"]])
        self.assertEqual(code, 0)
        self.assertIn("阈值策略", out)
        self.assertIn("关联资源", out)


class ErrorClassificationTests(unittest.TestCase):
    def test_403_permission_hint(self):
        exc = alarm.classify_hcloud_failure(
            "", '{"error_msg":"You are not authorized with ces:alarm:list"}', 403)
        self.assertIsInstance(exc, alarm.AuthError)
        self.assertIn("ces:alarms:list", str(exc))
        self.assertIn("ces:alarms:getPolicies", str(exc))

    def test_use_error_hint(self):
        exc = alarm.classify_hcloud_failure(
            "[USE_ERROR]Invalid parameter: --alarm-level", "", 0)
        self.assertIsInstance(exc, alarm.ApiError)
        self.assertIn("--help", str(exc))
        self.assertIn("[USE_ERROR]", str(exc))

    def test_missing_credentials_hint(self):
        exc = alarm.classify_hcloud_failure(
            "", "[USE_ERROR]cli-ak is empty, please configure AK/SK", 1)
        self.assertIsInstance(exc, alarm.ConfigError)
        self.assertIn("严禁在对话中粘贴", str(exc))

    def test_payload_envelope_on_stdout_rc0_is_not_empty_success(self):
        class Envelope(FakeHcloud):
            def __call__(self, argv):
                return json.dumps({"error": {"error_code": "CES.0107",
                                             "error_msg": "Insufficient permission"}}), "", 0

        code, out, err = run_main(["--table"], Envelope())
        self.assertEqual(code, 1)
        self.assertIn("权限", err)
        self.assertEqual(out, "")

    def test_empty_list_message(self):
        fake = FakeHcloud(rules=[])
        code, out, _ = run_main([], fake)
        self.assertEqual(code, 0)
        self.assertIn("无 CES 告警规则", out)

    def test_limit_validation(self):
        code, _, err = run_main(["--limit", "200"], FakeHcloud())
        self.assertEqual(code, 1)
        self.assertIn("1~100", err)


class MainOutputModesTests(unittest.TestCase):
    def test_default_name_list(self):
        code, out, _ = run_main([], FakeHcloud())
        self.assertEqual(code, 0)
        self.assertIn("共 2 条", out)
        self.assertIn("cpu-high", out)
        self.assertIn("disk-busy", out)
        self.assertNotIn("SYS.ECS", out)

    def test_table_mode(self):
        code, out, _ = run_main(["--table"], FakeHcloud())
        self.assertEqual(code, 0)
        header = out.splitlines()[1]
        for col in ("规则ID", "名称", "资源类型", "监控维度", "指标",
                    "阈值与比较符", "告警级别", "当前状态", "是否启用", "通知方式"):
            self.assertIn(col, header)
        self.assertIn("SYS.ECS", out)
        self.assertIn("数据不足", out)

    def test_json_mode_is_raw_structure(self):
        code, out, _ = run_main(["--json"], FakeHcloud())
        self.assertEqual(code, 0)
        payload = json.loads(out)
        self.assertIsInstance(payload, list)
        self.assertEqual(payload[0]["alarm_id"], RULE_CPU["alarm_id"])
        self.assertIn("policies", payload[0])
        self.assertNotIn("规则ID", json.dumps(payload, ensure_ascii=False))

    def test_filters_via_main(self):
        code, out, _ = run_main(["--alarm-state", "insufficient_data"], FakeHcloud())
        self.assertEqual(code, 0)
        self.assertIn("disk-busy", out)
        self.assertNotIn("cpu-high", out)

    def test_state_failure_without_state_filter_degrades(self):
        class NoState(FakeHcloud):
            def __call__(self, argv):
                if argv[1] == alarm.OPERATION_STATE:
                    return "", "[USE_ERROR]boom", 0
                return FakeHcloud.__call__(self, argv)

        code, out, err = run_main(["--table"], NoState())
        self.assertEqual(code, 0)
        self.assertIn("未知", out)
        self.assertIn("警告", err)

    def test_state_failure_with_state_filter_errors(self):
        class NoState(FakeHcloud):
            def __call__(self, argv):
                if argv[1] == alarm.OPERATION_STATE:
                    return "", "[USE_ERROR]boom", 0
                return FakeHcloud.__call__(self, argv)

        code, _, err = run_main(["--alarm-state", "alarm"], NoState())
        self.assertEqual(code, 1)
        self.assertIn("--alarm-state", err)


class _FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def to_dict(self):
        return self._payload


class _FakeRequest:
    def __init__(self, **kwargs):
        self.kwargs = kwargs


class _FakeClient:
    shared_calls = []

    def __init__(self):
        self.calls = _FakeClient.shared_calls

    @classmethod
    def new_builder(cls):
        return cls()

    def with_credentials(self, credentials):
        self.credentials = credentials
        _FakeClient.last_credentials = credentials
        return self

    def with_region(self, region):
        self.region = region
        return self

    def with_http_config(self, config):
        return self

    def build(self):
        return self

    def list_alarm_rules(self, request):
        self.calls.append(("list_alarm_rules", request.kwargs))
        return _FakeResponse({"alarms": [RULE_CPU], "count": 1})

    def list_alarms(self, request):
        self.calls.append(("list_alarms", request.kwargs))
        return _FakeResponse({"metric_alarms": [{"alarm_id": RULE_CPU["alarm_id"],
                                                "alarm_state": "ok"}],
                              "meta_data": {"count": 1, "total": 1}})


class _FakeRegionCatalog:
    @staticmethod
    def value_of(region):
        return region


class _FakeCredentials:
    def __init__(self, **kwargs):
        self.kwargs = kwargs


def fake_loader():
    _FakeClient.shared_calls = []
    client = _FakeClient()
    return {
        "client_v2": _FakeClient,
        "client_v1": _FakeClient,
        "region_v2": _FakeRegionCatalog,
        "region_v1": _FakeRegionCatalog,
        "region_class": lambda r, ep: r,
        "credentials": _FakeCredentials,
        "http_config": type("H", (), {"get_default_config": staticmethod(lambda: None)}),
        "requests": {
            alarm.OPERATION_LIST: _FakeRequest,
            alarm.OPERATION_POLICIES: _FakeRequest,
            alarm.OPERATION_RESOURCES: _FakeRequest,
            alarm.OPERATION_STATE: _FakeRequest,
        },
        "_client": client,
    }


class SdkFallbackTests(unittest.TestCase):
    ENV = {"HUAWEICLOUD_SDK_AK": "ak", "HUAWEICLOUD_SDK_SK": "sk",
           "CES_ALARM_PROJECT_ID": "pid"}

    def test_query_via_sdk_list(self):
        loader = fake_loader()
        with mock.patch.dict(os.environ, self.ENV, clear=False):
            payload, items = alarm.query_via_sdk(
                alarm.OPERATION_LIST, "cn-north-4",
                {"limit": 50, "offset": 0}, loader=loader)
        self.assertEqual(len(items), 1)
        self.assertEqual(payload["count"], 1)
        method, kwargs = loader["_client"].calls[0]
        self.assertEqual(method, "list_alarm_rules")
        self.assertEqual(kwargs["limit"], 50)
        self.assertEqual(_FakeClient.last_credentials.kwargs["project_id"], "pid")

    def test_query_via_sdk_state(self):
        loader = fake_loader()
        with mock.patch.dict(os.environ, self.ENV, clear=False):
            payload, items = alarm.query_via_sdk(
                alarm.OPERATION_STATE, "cn-north-4", {"limit": 50, "order": "asc"},
                loader=loader)
        self.assertEqual(items[0]["alarm_state"], "ok")
        self.assertEqual(loader["_client"].calls[0][0], "list_alarms")

    def test_missing_ak_sk(self):
        loader = fake_loader()
        env = {k: "" for k in ("HUAWEICLOUD_SDK_AK", "HUAWEI_ACCESS_KEY",
                               "HW_ACCESS_KEY", "HWC_ACCESS_KEY", "HUAWEI_AK",
                               "HW_AK", "HUAWEICLOUD_SDK_SK", "HUAWEI_SECRET_KEY",
                               "HW_SECRET_KEY", "HWC_SECRET_KEY", "HUAWEI_SK", "HW_SK")}
        with mock.patch.dict(os.environ, env, clear=False):
            with self.assertRaises(alarm.ConfigError) as ctx:
                alarm.query_via_sdk(alarm.OPERATION_LIST, "cn-north-4", {},
                                    loader=loader)
        self.assertIn("AK/SK", str(ctx.exception))

    def test_missing_project_id(self):
        loader = fake_loader()
        env = dict(self.ENV)
        for name in ("CES_ALARM_PROJECT_ID", "HUAWEICLOUD_SDK_PROJECT_ID",
                     "HUAWEI_PROJECT_ID", "HW_PROJECT_ID"):
            env[name] = ""
        with mock.patch.dict(os.environ, env, clear=False):
            with self.assertRaises(alarm.ConfigError) as ctx:
                alarm.query_via_sdk(alarm.OPERATION_LIST, "cn-north-4", {},
                                    loader=loader)
        self.assertIn("project id", str(ctx.exception))

    def test_missing_hcloud_falls_back_to_sdk(self):
        def boom(argv):
            raise alarm.ConfigError("未找到 hcloud（KooCLI）。")

        def fake_sdk(operation, region, params, loader=None):
            return {"alarms": [RULE_CPU], "count": 1}, [RULE_CPU]

        with mock.patch.object(alarm, "run_hcloud", boom), \
                mock.patch.object(alarm, "query_via_sdk", fake_sdk):
            items = alarm.list_alarm_rules("cn-north-4", limit=50)
        self.assertEqual(len(items), 1)

    def test_credential_error_does_not_fall_back(self):
        def boom(argv):
            return "", "[USE_ERROR]cli-ak is empty", 1

        with mock.patch.object(alarm, "run_hcloud", boom), \
                mock.patch.object(alarm, "query_via_sdk",
                                  mock.Mock(side_effect=AssertionError("no sdk"))):
            with self.assertRaises(alarm.ConfigError):
                alarm.list_alarm_rules("cn-north-4")


class SkillQualityWrapperTests(unittest.TestCase):
    def test_wrapped_with_skill_quality_cli(self):
        with mock.patch.dict(os.environ, {"CES_ALARM_SQC_BIN": "/bin/true",
                                          "SKILL_QUALITY_REPORT": "1"}, clear=False):
            os.environ.pop("CES_ALARM_HCLOUD_BIN", None)
            cmd = alarm.build_hcloud_command(["CES", "ListAlarmRules",
                                              "--cli-region=cn-north-4"])
        self.assertEqual(cmd[0], "/bin/true")
        self.assertEqual(cmd[1:5], ["run", "--skill-name",
                                    alarm.SKILL_NAME, "--"])
        self.assertEqual(cmd[5:7], ["hcloud", "CES"])

    def test_report_disabled_uses_bare_hcloud(self):
        with mock.patch.dict(os.environ, {"CES_ALARM_SQC_BIN": "/bin/true",
                                          "SKILL_QUALITY_REPORT": "0"}, clear=False):
            os.environ.pop("CES_ALARM_HCLOUD_BIN", None)
            cmd = alarm.build_hcloud_command(["CES", "ListAlarmRules"])
        self.assertEqual(cmd[0], "hcloud")

    def test_explicit_bin_runs_verbatim(self):
        with mock.patch.dict(os.environ, {"CES_ALARM_HCLOUD_BIN": "/tmp/mock-hcloud"},
                             clear=False):
            cmd = alarm.build_hcloud_command(["CES", "ListAlarmRules"])
        self.assertEqual(cmd[0], "/tmp/mock-hcloud")


if __name__ == "__main__":
    unittest.main()