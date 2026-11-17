# -*- coding: utf-8 -*-
"""Offline unit tests for huawei-cloud-aom-list.

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

from list_aom import (  # noqa: E402
    ApiError,
    AOM_CATEGORIES,
    AuthError,
    CATEGORIES,
    ConfigError,
    GuardError,
    _is_permission_degrade,
    _params_from_args,
    build_cli_command,
    build_parser,
    build_sdk_request,
    classify_hcloud_failure,
    classify_query,
    _extract_list_from_payload,
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


def _obj(data):
    return _Obj(data)


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


class TestCategoryRegistry(unittest.TestCase):
    def test_has_twelve(self):
        self.assertEqual(len(CATEGORIES), 12)
        self.assertEqual(len(AOM_CATEGORIES), 12)

    def test_each_category_has_required_fields(self):
        for key, spec in CATEGORIES.items():
            for field in ("label", "service", "group", "cli_operation",
                          "sdk_package", "sdk_client", "sdk_method",
                          "request", "rest_path", "result", "params",
                          "name_field"):
                self.assertIn(field, spec, "%s missing %s" % (key, field))
            self.assertEqual(spec["group"], "aom")
            self.assertEqual(spec["service"], "AOM")

    def test_rest_paths_use_verified_prefixes(self):
        for key, spec in CATEGORIES.items():
            path = spec["rest_path"]
            self.assertRegex(path, r"^/v[0-9]+/\{project_id\}/", key)

    def test_sdk_and_cli_names_are_consistent(self):
        for key, spec in CATEGORIES.items():
            self.assertTrue(spec["sdk_package"].startswith("huaweicloudsdkaom."), key)
            self.assertTrue(spec["rest_path"].startswith("/v"), key)


class TestNaturalLanguageRouting(unittest.TestCase):
    def test_chinese_phrases(self):
        self.assertEqual(classify_query("查询告警规则"), "alarm-rules")
        self.assertEqual(classify_query("告警规则模板列表"), "alarm-rule-templates")
        self.assertEqual(classify_query("查询事件告警规则"), "event2alarm-rules")
        self.assertEqual(classify_query("行动规则"), "action-rules")
        self.assertEqual(classify_query("静默规则列表"), "mute-rules")
        self.assertEqual(classify_query("查询仪表盘"), "dashboards")
        self.assertEqual(classify_query("仪表盘分组"), "dashboard-folders")
        self.assertEqual(classify_query("通知模板"), "notification-templates")
        self.assertEqual(classify_query("Prometheus 实例列表"), "prom-instances")
        self.assertEqual(classify_query("接入码"), "access-codes")
        self.assertEqual(classify_query("服务发现规则"), "service-discovery-rules")

    def test_english_phrases(self):
        self.assertEqual(classify_query("list alarm rules"), "alarm-rules")
        self.assertEqual(classify_query("notification template list"),
                         "notification-templates")
        self.assertEqual(classify_query("prometheus instances"), "prom-instances")
        self.assertEqual(classify_query("service discovery rule"), "service-discovery-rules")

    def test_specific_beats_generic(self):
        self.assertEqual(classify_query("告警规则模板"), "alarm-rule-templates")
        self.assertEqual(classify_query("仪表盘分组"), "dashboard-folders")
        self.assertEqual(classify_query("指标告警规则"), "metric-or-event-alarm-rules")

    def test_aom_qualified_phrases(self):
        self.assertEqual(classify_query("查询AOM告警规则"), "alarm-rules")
        self.assertEqual(classify_query("AOM 告警规则模板"), "alarm-rule-templates")
        self.assertEqual(classify_query("AOM 指标告警规则"), "metric-or-event-alarm-rules")
        self.assertEqual(classify_query("AOM 事件告警规则"), "event2alarm-rules")
        self.assertEqual(classify_query("AOM 监控看板列表"), "dashboards")
        self.assertEqual(classify_query("AOM 监控看板分组"), "dashboard-folders")

    def test_unknown_returns_none(self):
        self.assertIsNone(classify_query("今天天气怎么样"))
        self.assertIsNone(classify_query(""))


class TestWriteIntentGuard(unittest.TestCase):
    def test_read_query_passes(self):
        self.assertFalse(guard_write_intent("查询告警规则列表"))
        self.assertFalse(guard_write_intent("list notification templates"))
        self.assertFalse(guard_write_intent("查询服务发现规则"))
        self.assertFalse(guard_write_intent("查询静默规则"))

    def test_english_write_blocked(self):
        for text in ("CreateAlarmRule", "DeleteAlarmRule", "UpdateAlarm",
                     "BatchUpdateAlarmRule", "AddActionRule", "DeleteDashboard",
                     "associate resources", "CreatePromInstance"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_chinese_write_blocked(self):
        for text in ("删除告警规则", "创建仪表盘", "更新通知模板",
                     "启用静默规则", "升级 Prometheus 实例"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_normalized_separators_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("create_alarm_rule")
        with self.assertRaises(GuardError):
            guard_write_intent("delete-dashboard")

    def test_query_value_is_scanned(self):
        with self.assertRaises(GuardError):
            guard_write_intent(guard_text_from_argv(["--query", "删除告警规则"]))

    def test_data_values_stripped(self):
        self.assertFalse(
            guard_write_intent(guard_text_from_argv(["--name", "create-prod"])))
        self.assertFalse(
            guard_write_intent(guard_text_from_argv(["--id", "delete-me"])))

    def test_operation_guard(self):
        self.assertTrue(guard_operation("alarm-rules", "ListAlarmRule"))
        self.assertTrue(guard_operation("alarm-rules", "list_alarm_rule"))
        with self.assertRaises(GuardError):
            guard_operation("alarm-rules", "CreateAlarmRule")
        with self.assertRaises(GuardError):
            guard_operation("not-a-category")


class TestCliCommand(unittest.TestCase):
    def test_build_command_basic(self):
        argv = build_cli_command("alarm-rules", "cn-north-4", {"limit": 50})
        self.assertEqual(argv[0], "AOM")
        self.assertEqual(argv[1], "ListAlarmRule")
        self.assertIn("--cli-region=cn-north-4", argv)
        self.assertIn("--limit=50", argv)

    def test_build_command_prom(self):
        argv = build_cli_command("prom-instances", "cn-south-1",
                                 {"prom_type": "default"})
        self.assertEqual(argv[0], "AOM")
        self.assertEqual(argv[1], "ListPromInstance")
        self.assertIn("--prom_type=default", argv)

    def test_header_param_uses_koocli_header_name(self):
        # KooCLI only accepts the Enterprise-Project-Id header form; the SDK
        # snake_case name must never reach the CLI argv.
        argv = build_cli_command("prom-instances", "cn-north-4",
                                 {"enterprise_project_id": "0"})
        self.assertIn("--Enterprise-Project-Id=0", argv)
        self.assertNotIn("--enterprise_project_id=0", argv)

    def test_header_mapping_applies_to_every_eps_category(self):
        for category in ("alarm-rule-templates", "metric-or-event-alarm-rules",
                         "dashboards", "dashboard-folders",
                         "notification-templates", "prom-instances"):
            argv = build_cli_command(category, "cn-north-4",
                                     {"enterprise_project_id": "eps-1"})
            self.assertIn("--Enterprise-Project-Id=eps-1", argv, category)
            self.assertFalse(any(a.startswith("--enterprise_project_id=")
                                 for a in argv), category)

    def test_region_always_present(self):
        for category in CATEGORIES:
            argv = build_cli_command(category, "cn-north-4", {})
            self.assertTrue(any(a.startswith("--cli-region=") for a in argv),
                            category)
            self.assertTrue(argv[1][0].isupper(), category)


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
        response = _Obj({"prometheus": [_obj({"prom_name": "p"})]})
        rows = extract_result("prom-instances", response)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["prom_name"], "p")

    def test_extract_dashboard_list(self):
        response = _Obj({"dashboards": [_obj({"dashboard_title": "t"})]})
        rows = extract_result("dashboards", response)
        self.assertEqual(rows[0]["dashboard_title"], "t")

    def test_extract_empty_list(self):
        self.assertEqual(extract_result("alarm-rules", _Obj({})), [])

    def test_to_plain_nested(self):
        plain = to_plain({"a": _obj({"b": 1}), "c": [_obj({"d": 2})]})
        self.assertEqual(plain, {"a": {"b": 1}, "c": [{"d": 2}]})

    def test_raw_payload_list(self):
        payload = {"alarm_rules": [{"alarm_rule_name": "a"}]}
        self.assertEqual(_extract_list_from_payload("metric-or-event-alarm-rules", payload),
                         [{"alarm_rule_name": "a"}])

    def test_raw_payload_body(self):
        payload = {"body": [{"name": "n"}]}
        self.assertEqual(_extract_list_from_payload("notification-templates", payload),
                         [{"name": "n"}])


class TestSdkPath(unittest.TestCase):
    def _clean_env(self):
        names = ("HW_ACCESS_KEY", "HUAWEI_ACCESS_KEY", "HUAWEICLOUD_SDK_AK",
                 "HUAWEI_CLOUD_ACCESS_KEY", "HUAWEI_AK", "HW_AK", "HWC_ACCESS_KEY",
                 "HW_SECRET_KEY", "HUAWEI_SECRET_KEY", "HUAWEICLOUD_SDK_SK",
                 "HUAWEI_CLOUD_SECRET_KEY", "HUAWEI_SK", "HW_SK", "HWC_SECRET_KEY")
        return {k: "" for k in names}

    def test_missing_credentials(self):
        loader = FakeLoader("prom-instances", _Obj({"prometheus": []}))
        with mock.patch.dict(os.environ, self._clean_env(), clear=False):
            with self.assertRaises(ConfigError):
                query_via_sdk("prom-instances", "cn-north-4", {},
                              loader=loader.symbols)

    def test_success(self):
        loader = FakeLoader("prom-instances",
                            _Obj({"prometheus": [_obj({"prom_name": "x"})]}))
        env = {"HUAWEICLOUD_SDK_AK": "A", "HUAWEICLOUD_SDK_SK": "S"}
        with mock.patch.dict(os.environ, env, clear=False):
            result, = (query_via_sdk("prom-instances", "cn-north-4", {},
                                     loader=loader.symbols),)
        self.assertEqual(result, [{"prom_name": "x"}])
        method, request = loader.calls[0]
        self.assertEqual(method, "list_prom_instance")
        self.assertEqual(request.kwargs, {})

    def test_request_building(self):
        loader = FakeLoader("metric-or-event-alarm-rules",
                            _Obj({"alarm_rules": []}))
        request = build_sdk_request("metric-or-event-alarm-rules", loader.symbols, {
            "name": "prod", "limit": 5, "unknown": 9})
        self.assertEqual(request.kwargs, {"name": "prod", "limit": 5})


class TestBackendFallback(unittest.TestCase):
    def _args(self):
        return build_parser().parse_args(["--category", "alarm-rules", "--limit", "5"])

    def test_cli_success(self):
        runner = FakeRunner([('{"thresholds": [{"alarm_rule_name": "a"}]}', "", 0)])
        with mock.patch("list_aom.subprocess.run", runner):
            result, backend = query("alarm-rules", "cn-north-4", self._args())
        self.assertEqual(backend, "cli")
        self.assertEqual(result, [{"alarm_rule_name": "a"}])

    def test_cli_missing_falls_back_to_sdk(self):
        loader = FakeLoader("alarm-rules",
                            _Obj({"thresholds": [_obj({"alarm_rule_name": "s"})]}))
        env = {"HUAWEICLOUD_SDK_AK": "A", "HUAWEICLOUD_SDK_SK": "S"}
        with mock.patch("list_aom.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_aom._load_sdk", loader), \
                mock.patch.dict(os.environ, env, clear=False):
            result, backend = query("alarm-rules", "cn-north-4", self._args())
        self.assertEqual(backend, "sdk")
        self.assertEqual(result, [{"alarm_rule_name": "s"}])

    def test_cli_and_sdk_unavailable_raises(self):
        with mock.patch("list_aom.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch.dict(os.environ, {
                    "HUAWEICLOUD_SDK_AK": "", "HUAWEICLOUD_SDK_SK": "",
                    "AOM_TOKEN": "", "HW_AUTH_TOKEN": ""}, clear=False):
            with self.assertRaises(ConfigError):
                query("alarm-rules", "cn-north-4", self._args())


class TestPromInstanceBackendFix(unittest.TestCase):
    """ListPromInstance must stay on the CLI path (default EPS) and degrade
    from a permission-scoped SDK 403 back to CLI instead of hard-failing."""

    def _nl_args(self):
        return build_parser().parse_args(["--query", "查询 Prometheus 实例列表"])

    def test_default_enterprise_project_id_applied(self):
        params = _params_from_args(self._nl_args(), "prom-instances")
        self.assertEqual(params.get("enterprise_project_id"), "0")

    def test_explicit_eps_not_overridden(self):
        args = build_parser().parse_args(
            ["--category", "prom-instances", "--enterprise-project-id", "abc"])
        params = _params_from_args(args, "prom-instances")
        self.assertEqual(params["enterprise_project_id"], "abc")

    def test_non_prom_category_has_no_eps_default(self):
        args = build_parser().parse_args(["--category", "alarm-rules"])
        self.assertNotIn("enterprise_project_id",
                         _params_from_args(args, "alarm-rules"))

    def test_cli_first_uses_eps_default(self):
        runner = FakeRunner([('{"prometheus": [{"prom_name": "p"}]}', "", 0)])
        with mock.patch("list_aom.subprocess.run", runner):
            result, backend = query("prom-instances", "cn-north-4", self._nl_args())
        self.assertEqual(backend, "cli")
        self.assertEqual(result, [{"prom_name": "p"}])
        self.assertIn("--Enterprise-Project-Id=0", runner.calls[0])

    def test_permission_degrade_detection(self):
        self.assertTrue(_is_permission_degrade(
            AuthError("AOM.0403 aom:metric:list not authorized")))
        self.assertFalse(_is_permission_degrade(AuthError("plain 403")))

    def test_sdk_403_permission_degrades_to_cli(self):
        def sdk_raises(*a, **k):
            raise AuthError("AOM.0403 ... the action aom:metric:list is not authorized")

        runner = FakeRunner([
            FileNotFoundError(),                                  # CLI unavailable
            ('{"prometheus": [{"prom_name": "cli"}]}', "", 0),    # CLI retry succeeds
        ])
        with mock.patch("list_aom.subprocess.run", runner), \
                mock.patch("list_aom.query_via_sdk", side_effect=sdk_raises):
            result, backend = query("prom-instances", "cn-north-4", self._nl_args())
        self.assertEqual(backend, "cli")
        self.assertEqual(result, [{"prom_name": "cli"}])

    def test_sdk_403_without_hint_propagates(self):
        def sdk_raises(*a, **k):
            raise AuthError("unrelated authorization failure")

        runner = FakeRunner([FileNotFoundError(), FileNotFoundError()])
        with mock.patch("list_aom.subprocess.run", runner), \
                mock.patch("list_aom.query_via_sdk", side_effect=sdk_raises):
            with self.assertRaises(AuthError):
                query("prom-instances", "cn-north-4", self._nl_args())


class TestRendering(unittest.TestCase):
    def test_render_table_name_first(self):
        table = render_table([{"prom_name": "p1", "prom_status": "ok"}], "prom_name")
        first_line = table.splitlines()[0]
        self.assertTrue(first_line.startswith("prom_name"))

    def test_print_empty(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            print_result("alarm-rules", [], "cn-north-4", "sdk", False)
        self.assertIn("无数据", buf.getvalue())

    def test_print_json(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            print_result("alarm-rules", [{"alarm_rule_name": "a"}], "cn-north-4",
                         "cli", True)
        self.assertEqual(json.loads(buf.getvalue()), [{"alarm_rule_name": "a"}])

    def test_names_only(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            print_result("dashboards", [{"dashboard_title": "d1"},
                                        {"dashboard_title": "d2"}],
                         "cn-north-4", "cli", False, names_only=True)
        self.assertEqual(buf.getvalue().split(), ["d1", "d2"])


class TestMain(unittest.TestCase):
    def test_list_categories(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = main(["--list-categories"])
        self.assertEqual(rc, 0)
        self.assertIn("alarm-rules", buf.getvalue())
        self.assertIn("prom-instances", buf.getvalue())

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
        with mock.patch("list_aom.query",
                        return_value=([{"alarm_rule_name": "a"}], "cli")) as q, \
                redirect_stdout(buf):
            rc = main(["--query", "查询告警规则"])
        self.assertEqual(rc, 0)
        self.assertEqual(q.call_args[0][0], "alarm-rules")

    def test_json_mode(self):
        buf = io.StringIO()
        with mock.patch("list_aom.query",
                        return_value=([{"name": "a"}], "sdk")), \
                redirect_stdout(buf):
            rc = main(["--category", "action-rules", "--json"])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(buf.getvalue()), [{"name": "a"}])

    def test_error_path(self):
        buf = io.StringIO()
        with mock.patch("list_aom.query",
                        side_effect=ConfigError("boom")), redirect_stderr(buf):
            rc = main(["--category", "alarm-rules"])
        self.assertEqual(rc, 1)
        self.assertIn("boom", buf.getvalue())


if __name__ == "__main__":
    unittest.main()