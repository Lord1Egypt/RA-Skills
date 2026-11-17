# -*- coding: utf-8 -*-
"""Offline unit tests for huawei-cloud-ces-eps-query.

No credentials and no network are required: the hcloud subprocess and the SDK
loader are mocked, and the write-intent guard / natural-language router are
pure functions.
"""

import io
import json
import os
import subprocess
import sys
import unittest
from contextlib import redirect_stdout, redirect_stderr
from unittest import mock

sys.path.insert(
    0,
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"),
)

from ces_eps_query import (  # noqa: E402
    ApiError,
    AuthError,
    CATEGORIES,
    CES_CATEGORIES,
    ConfigError,
    EPS_CATEGORIES,
    GuardError,
    _extract_list_from_payload,
    _quality_report_enabled,
    build_cli_command,
    build_hcloud_command,
    build_parser,
    build_sdk_request,
    classify_hcloud_failure,
    classify_query,
    extract_json,
    extract_result,
    guard_operation,
    guard_text_from_argv,
    guard_write_intent,
    main,
    print_result,
    query,
    query_via_sdk,
    render_table,
    run_hcloud,
    to_plain,
)


def hcloud_result(stdout="", stderr="", returncode=0):
    return subprocess.CompletedProcess(
        args=["hcloud"], returncode=returncode, stdout=stdout, stderr=stderr
    )


class FakeRunner:
    def __init__(self, results):
        self.results = list(results)
        self.calls = []

    def __call__(self, cmd, **kwargs):
        self.calls.append(cmd)
        out = self.results.pop(0)
        if isinstance(out, Exception):
            raise out
        return hcloud_result(*out)


# ---------------------------------------------------------------------------
# Fake SDK symbols for query_via_sdk(category, region, params, loader=...)
# ---------------------------------------------------------------------------
class _Obj:
    def __init__(self, data):
        self._data = data

    def to_dict(self):
        return dict(self._data)

    def __getattr__(self, item):
        try:
            return self._data[item]
        except KeyError:
            raise AttributeError(item)


class FakeLoader:
    def __init__(self, category, response):
        self.spec = CATEGORIES[category]
        self.response = response
        self.calls = []

        class _ClientImpl:
            def __init__(self, response, calls):
                self._response = response
                self._calls = calls

            @classmethod
            def new_builder(cls):
                outer = self

                class _B:
                    def with_credentials(self, _c):
                        return self

                    def with_region(self, _r):
                        return self

                    def with_http_config(self, _h):
                        return self

                    def build(self):
                        return _ClientImpl(outer.response, outer.calls)
                return _B()

            def __getattr__(self, item):
                def _call(request):
                    self._calls.append((item, request))
                    return self._response
                return _call

        self._client_impl = _ClientImpl

        class _RegionCatalog:
            @staticmethod
            def value_of(region):
                return "region:%s" % region

        class _Creds:
            def __init__(self, ak=None, sk=None):
                self.ak = ak
                self.sk = sk

        class _Region:
            def __init__(self, i, endpoint):
                self.id = i
                self.endpoint = endpoint

        class _HttpConfig:
            @staticmethod
            def get_default_config():
                return object()

        class _Request:
            def __init__(self, **kwargs):
                self.kwargs = kwargs

        self.symbols = {
            "spec": self.spec,
            "client": self._client_impl,
            "request": _Request,
            "credentials": _Creds,
            "region": _Region,
            "region_catalog": _RegionCatalog,
            "http_config": _HttpConfig,
        }

    def __call__(self, category):
        return self.symbols


# ---------------------------------------------------------------------------
class TestCategoryRegistry(unittest.TestCase):
    def test_ces_has_seven(self):
        self.assertEqual(len(CES_CATEGORIES), 7)

    def test_eps_has_five(self):
        self.assertEqual(len(EPS_CATEGORIES), 5)

    def test_total_twelve(self):
        self.assertEqual(len(CATEGORIES), 12)

    def test_each_category_has_required_fields(self):
        for key, spec in CATEGORIES.items():
            for field in ("label", "service", "group", "cli_operation",
                          "sdk_package", "sdk_client", "sdk_method",
                          "request", "rest_path", "result", "params"):
                self.assertIn(field, spec, "%s missing %s" % (key, field))
            self.assertIn(spec["group"], ("ces", "eps"))

    def test_rest_paths_use_verified_prefixes(self):
        for key, spec in CATEGORIES.items():
            path = spec["rest_path"]
            if spec["group"] == "ces":
                self.assertTrue(path.startswith("/v2/{project_id}/"), key)
            else:
                self.assertTrue(path.startswith("/v1.0/"), key)


class TestNaturalLanguageRouting(unittest.TestCase):
    def test_ces_phrases(self):
        self.assertEqual(classify_query("查询告警规则"), "alarm-rules")
        self.assertEqual(classify_query("查看告警历史"), "alarm-histories")
        self.assertEqual(classify_query("列出告警模板"), "alarm-templates")
        self.assertEqual(classify_query("查询仪表盘"), "dashboards")
        self.assertEqual(classify_query("通知掩码列表"), "notification-masks")
        self.assertEqual(classify_query("资源分组查询"), "resource-groups")
        self.assertEqual(classify_query("一键告警"), "one-click-alarms")

    def test_eps_phrases(self):
        self.assertEqual(classify_query("企业项目列表"), "eps-projects")
        self.assertEqual(classify_query("企业项目详情"), "eps-project-detail")
        self.assertEqual(classify_query("企业项目配额"), "eps-quotas")
        self.assertEqual(classify_query("查询企业项目绑定资源"), "eps-resources")
        self.assertEqual(classify_query("迁移记录"), "eps-migration-records")

    def test_english_phrases(self):
        self.assertEqual(classify_query("list alarm rules"), "alarm-rules")
        self.assertEqual(classify_query("enterprise project quota"), "eps-quotas")
        self.assertEqual(classify_query("migration record"), "eps-migration-records")

    def test_specific_beats_generic(self):
        self.assertEqual(classify_query("企业项目详情"), "eps-project-detail")
        self.assertEqual(classify_query("企业项目"), "eps-projects")

    def test_unknown_returns_none(self):
        self.assertIsNone(classify_query("今天天气怎么样"))
        self.assertIsNone(classify_query(""))


class TestWriteIntentGuard(unittest.TestCase):
    def test_read_query_passes(self):
        self.assertFalse(guard_write_intent("查询告警规则列表"))
        self.assertFalse(guard_write_intent("list alarm rules"))
        self.assertFalse(guard_write_intent("查询企业项目绑定资源"))
        self.assertFalse(guard_write_intent("查询迁移记录"))

    def test_english_write_blocked(self):
        for text in ("CreateAlarm", "DeleteAlarmRule", "UpdateAlarm ",
                     "batch delete alarm rules", "MigrateResource",
                     "associate resources"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_chinese_write_blocked(self):
        for text in ("删除告警规则", "创建企业项目", "更新告警模板",
                     "启用一键告警", "迁移资源"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_normalized_separators_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("create_alarm_rule")
        with self.assertRaises(GuardError):
            guard_write_intent("delete-alarm")

    def test_query_value_is_scanned(self):
        # --query is NOT stripped, so a write intent in natural language is caught
        with self.assertRaises(GuardError):
            guard_write_intent(guard_text_from_argv(["--query", "删除告警规则"]))

    def test_data_values_stripped(self):
        # a filter value that looks like a write word must not trip the guard
        self.assertFalse(
            guard_write_intent(guard_text_from_argv(["--name", "create-prod"])))
        self.assertFalse(
            guard_write_intent(guard_text_from_argv(["--id", "delete-me"])))

    def test_operation_guard(self):
        self.assertTrue(guard_operation("alarm-rules", "ListAlarmRules"))
        self.assertTrue(guard_operation("alarm-rules", "list_alarm_rules"))
        with self.assertRaises(GuardError):
            guard_operation("alarm-rules", "CreateAlarm")
        with self.assertRaises(GuardError):
            guard_operation("not-a-category")


class TestCliCommand(unittest.TestCase):
    def test_build_command_basic(self):
        argv = build_cli_command("alarm-rules", "cn-north-4", 50, 0, {})
        self.assertEqual(argv[0], "CES")
        self.assertEqual(argv[1], "ListAlarmRules")
        self.assertIn("--cli-region=cn-north-4", argv)
        self.assertIn("--limit=50", argv)
        self.assertNotIn("--offset=0", argv)

    def test_build_command_eps(self):
        argv = build_cli_command("eps-projects", "cn-south-1", 10, 20,
                                 {"name": "prod"})
        self.assertEqual(argv[0], "EPS")
        self.assertEqual(argv[1], "ListEnterpriseProject")
        self.assertIn("--offset=20", argv)
        self.assertIn("--name=prod", argv)

    def test_region_always_present(self):
        for category in CATEGORIES:
            argv = build_cli_command(category, "cn-north-4", 1, 0, {})
            self.assertTrue(any(a.startswith("--cli-region=") for a in argv),
                            category)


class TestParsingAndClassification(unittest.TestCase):
    def test_extract_json_plain(self):
        self.assertEqual(extract_json('{"a": 1}'), {"a": 1})

    def test_extract_json_with_noise(self):
        self.assertEqual(extract_json('noise {"a": 1} tail'), {"a": 1})

    def test_extract_json_bad(self):
        with self.assertRaises(ApiError):
            extract_json("not json at all")

    def test_classify_use_error(self):
        err = classify_hcloud_failure("[USE_ERROR]op not supported", "", 0)
        self.assertIsInstance(err, ApiError)
        self.assertIn("hcloud 参数错误", str(err))

    def test_classify_missing_credentials(self):
        err = classify_hcloud_failure("", "no ak/sk configured", 1)
        self.assertIsInstance(err, ConfigError)

    def test_classify_auth(self):
        err = classify_hcloud_failure("", "401 unauthorized", 1)
        self.assertIsInstance(err, AuthError)


class TestResultExtraction(unittest.TestCase):
    def test_extract_list_from_sdk_response(self):
        response = _Obj({"alarms": [_obj({"name": "a"})], "count": 1})
        rows = extract_result("alarm-rules", response)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["name"], "a")

    def test_extract_single(self):
        response = _Obj({"enterprise_project": _obj({"id": "p1"})})
        result = extract_result("eps-project-detail", response)
        self.assertEqual(result["id"], "p1")

    def test_extract_empty_list(self):
        self.assertEqual(extract_result("alarm-rules", _Obj({})), [])

    def test_to_plain_nested(self):
        plain = to_plain({"a": _obj({"b": 1}), "c": [_obj({"d": 2})]})
        self.assertEqual(plain, {"a": {"b": 1}, "c": [{"d": 2}]})

    def test_raw_payload_list(self):
        payload = {"alarms": [{"name": "a"}]}
        self.assertEqual(_extract_list_from_payload("alarm-rules", payload),
                         [{"name": "a"}])

    def test_raw_payload_single_unwraps(self):
        payload = {"enterprise_project": {"id": "p1"}}
        self.assertEqual(_extract_list_from_payload("eps-project-detail", payload),
                         {"id": "p1"})


def _obj(data):
    return _Obj(data)


class TestSdkPath(unittest.TestCase):
    def test_missing_credentials(self):
        loader = FakeLoader("alarm-rules", _Obj({"alarms": []}))
        clean = {k: "" for k in (
            "HW_ACCESS_KEY", "HUAWEI_ACCESS_KEY", "HUAWEICLOUD_SDK_AK",
            "HUAWEI_CLOUD_ACCESS_KEY", "HUAWEI_AK", "HW_AK", "HWC_ACCESS_KEY",
            "HW_SECRET_KEY", "HUAWEI_SECRET_KEY", "HUAWEICLOUD_SDK_SK",
            "HUAWEI_CLOUD_SECRET_KEY", "HUAWEI_SK", "HW_SK", "HWC_SECRET_KEY")}
        with mock.patch.dict(os.environ, clean, clear=False):
            with self.assertRaises(ConfigError):
                query_via_sdk("alarm-rules", "cn-north-4", {}, loader=loader.symbols)

    def test_success(self):
        loader = FakeLoader("alarm-rules", _Obj({"alarms": [_obj({"name": "x"})]}))
        env = {"HUAWEICLOUD_SDK_AK": "A", "HUAWEICLOUD_SDK_SK": "S"}
        with mock.patch.dict(os.environ, env, clear=False):
            result, = (query_via_sdk("alarm-rules", "cn-north-4", {}, loader=loader.symbols),)
        self.assertEqual(result, [{"name": "x"}])
        method, request = loader.calls[0]
        self.assertEqual(method, "list_alarm_rules")
        self.assertEqual(request.kwargs, {})

    def test_request_building(self):
        loader = FakeLoader("eps-resources",
                            _Obj({"resources": []}))
        request = build_sdk_request("eps-resources", loader.symbols, {
            "enterprise_project_id": "p1", "limit": 5, "unknown": 9})
        self.assertEqual(request.kwargs, {"enterprise_project_id": "p1", "limit": 5})


class TestBackendFallback(unittest.TestCase):
    def _args(self):
        return build_parser().parse_args(["--category", "alarm-rules", "--limit", "5"])

    def test_cli_success(self):
        runner = FakeRunner([('{"alarms": [{"name": "a"}]}', "", 0)])
        with mock.patch("ces_eps_query.subprocess.run", runner):
            result, backend = query("alarm-rules", "cn-north-4", self._args())
        self.assertEqual(backend, "cli")
        self.assertEqual(result, [{"name": "a"}])

    def test_cli_missing_falls_back_to_sdk(self):
        loader = FakeLoader("alarm-rules", _Obj({"alarms": [_obj({"name": "s"})]}))
        env = {"HUAWEICLOUD_SDK_AK": "A", "HUAWEICLOUD_SDK_SK": "S"}
        with mock.patch("ces_eps_query.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("ces_eps_query._load_sdk", loader), \
                mock.patch.dict(os.environ, env, clear=False):
            result, backend = query("alarm-rules", "cn-north-4", self._args())
        self.assertEqual(backend, "sdk")
        self.assertEqual(result, [{"name": "s"}])

    def test_cli_and_sdk_unavailable_raises(self):
        with mock.patch("ces_eps_query.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch.dict(os.environ, {
                    "HUAWEICLOUD_SDK_AK": "", "HUAWEICLOUD_SDK_SK": "",
                    "CES_EPS_TOKEN": "", "HW_AUTH_TOKEN": ""}, clear=False):
            with self.assertRaises(ConfigError):
                query("alarm-rules", "cn-north-4", self._args())

    def test_missing_required_id(self):
        args = build_parser().parse_args(["--category", "eps-project-detail"])
        with self.assertRaises(ApiError):
            query("eps-project-detail", "cn-north-4", args)


class TestRendering(unittest.TestCase):
    def test_render_table(self):
        table = render_table([{"name": "a", "status": "ok"}])
        self.assertIn("name", table)
        self.assertIn("a", table)

    def test_print_empty(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            print_result("alarm-rules", [], "cn-north-4", "sdk", False)
        self.assertIn("无数据", buf.getvalue())

    def test_print_json(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            print_result("alarm-rules", [{"name": "a"}], "cn-north-4", "cli", True)
        self.assertEqual(json.loads(buf.getvalue()), [{"name": "a"}])


class TestMain(unittest.TestCase):
    def test_list_categories(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = main(["--list-categories"])
        self.assertEqual(rc, 0)
        self.assertIn("alarm-rules", buf.getvalue())
        self.assertIn("eps-projects", buf.getvalue())

    def test_guard_blocks_write_query(self):
        buf = io.StringIO()
        with redirect_stderr(buf):
            rc = main(["--query", "删除告警规则"])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", buf.getvalue())

    def test_unknown_query(self):
        buf = io.StringIO()
        with redirect_stderr(buf):
            rc = main(["--query", "今天天气"])
        self.assertEqual(rc, 1)
        self.assertIn("无法识别查询意图", buf.getvalue())

    def test_query_routes_and_runs(self):
        buf = io.StringIO()
        with mock.patch("ces_eps_query.query",
                        return_value=([{"name": "a"}], "cli")) as q, \
                redirect_stdout(buf):
            rc = main(["--query", "查询告警规则"])
        self.assertEqual(rc, 0)
        self.assertEqual(q.call_args[0][0], "alarm-rules")

    def test_json_mode(self):
        buf = io.StringIO()
        with mock.patch("ces_eps_query.query",
                        return_value=([{"name": "a"}], "sdk")), \
                redirect_stdout(buf):
            rc = main(["--category", "alarm-rules", "--json"])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(buf.getvalue()), [{"name": "a"}])

    def test_error_path(self):
        buf = io.StringIO()
        with mock.patch("ces_eps_query.query",
                        side_effect=ConfigError("boom")), redirect_stderr(buf):
            rc = main(["--category", "alarm-rules"])
        self.assertEqual(rc, 1)
        self.assertIn("boom", buf.getvalue())


class TestQualityWrapper(unittest.TestCase):
    """The CLI path wraps hcloud with skill-quality-cli (with a bare fallback)."""

    def test_wraps_when_cli_available(self):
        with mock.patch.dict(os.environ, {"CES_EPS_SQC_BIN": "/fake/sqc"}, clear=True):
            cmd = build_hcloud_command(["CES", "ListAlarmRules"])
        self.assertEqual(cmd, [
            "/fake/sqc", "run", "--skill-name", "huawei-cloud-ces-eps-query",
            "--", "hcloud", "CES", "ListAlarmRules"])

    def test_bare_when_report_disabled(self):
        env = {"CES_EPS_SQC_BIN": "/fake/sqc", "SKILL_QUALITY_REPORT": "0"}
        with mock.patch.dict(os.environ, env, clear=True):
            cmd = build_hcloud_command(["CES", "ListAlarmRules"])
        self.assertEqual(cmd, ["hcloud", "CES", "ListAlarmRules"])

    def test_bare_when_cli_missing(self):
        with mock.patch.dict(os.environ, {}, clear=True), \
                mock.patch("ces_eps_query._skill_quality_executable",
                           return_value=None):
            cmd = build_hcloud_command(["CES", "ListAlarmRules"])
        self.assertEqual(cmd, ["hcloud", "CES", "ListAlarmRules"])

    def test_explicit_hcloud_bin_bypasses_wrapper(self):
        env = {"CES_EPS_SQC_BIN": "/fake/sqc", "CES_EPS_HCLOUD_BIN": "/mock/hcloud"}
        with mock.patch.dict(os.environ, env, clear=True):
            cmd = build_hcloud_command(["CES", "ListAlarmRules"])
        self.assertEqual(cmd, ["/mock/hcloud", "CES", "ListAlarmRules"])

    def test_hcloud_extra_args_preserved_inside_wrapper(self):
        env = {"CES_EPS_SQC_BIN": "/fake/sqc", "CES_EPS_HCLOUD_ARGS": "--debug"}
        with mock.patch.dict(os.environ, env, clear=True):
            cmd = build_hcloud_command(["EPS", "ListEnterpriseProject"])
        self.assertEqual(cmd[:5], [
            "/fake/sqc", "run", "--skill-name", "huawei-cloud-ces-eps-query", "--"])
        self.assertEqual(cmd[5:],
                         ["hcloud", "--debug", "EPS", "ListEnterpriseProject"])

    def test_run_hcloud_dispatches_through_wrapper(self):
        captured = {}

        def fake_run(cmd, **kwargs):
            captured["cmd"] = cmd
            return hcloud_result('{"ok": 1}', "", 0)

        with mock.patch.dict(os.environ, {"CES_EPS_SQC_BIN": "/fake/sqc"}, clear=True), \
                mock.patch("ces_eps_query.subprocess.run", fake_run):
            stdout, stderr, rc = run_hcloud(["CES", "ListAlarmRules"])
        self.assertEqual(captured["cmd"][0], "/fake/sqc")
        self.assertEqual((stdout, stderr, rc), ('{"ok": 1}', "", 0))

    def test_quality_report_default_enabled(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertTrue(_quality_report_enabled())

    def test_quality_report_falsy_values(self):
        for value in ("0", "false", "NO", "off"):
            with mock.patch.dict(os.environ, {"SKILL_QUALITY_REPORT": value},
                                 clear=True):
                self.assertFalse(_quality_report_enabled(), value)

    def test_quality_report_truthy_values(self):
        for value in ("1", "true", "yes"):
            with mock.patch.dict(os.environ, {"SKILL_QUALITY_REPORT": value},
                                 clear=True):
                self.assertTrue(_quality_report_enabled(), value)


if __name__ == "__main__":
    unittest.main()
