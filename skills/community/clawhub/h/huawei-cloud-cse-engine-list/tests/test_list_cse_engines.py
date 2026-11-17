import json
import os
import subprocess
import sys
import types
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from list_cse_engines import (  # noqa: E402
    ALLOWED_OPERATIONS,
    ApiError,
    AuthError,
    ConfigError,
    CseListError,
    GuardError,
    OPERATION,
    REST_PATH,
    _collect,
    _env_credential,
    build_command,
    classify_hcloud_failure,
    error_from_payload,
    extract_engines,
    extract_json,
    filter_by_name,
    format_time,
    guard_operation,
    guard_text_from_argv,
    guard_write_intent,
    item_summary_lines,
    list_cse_engines,
    list_engines_via_sdk,
    main,
    normalize_engine,
    render_table,
)

ENGINE_1 = {
    "id": "e-0001", "name": "cse-alpha", "type": "CSE",
    "version": "2.0.0", "status": "Available", "flavor": "cse.s1.small2",
    "totalInstance": 2, "usedInstance": 1, "availableInstance": 1,
    "createTime": 1700000000000, "enterpriseProjectId": "0",
}
ENGINE_2 = {
    "id": "e-0002", "name": "nacos-beta", "type": "Nacos",
    "version": "2.1.0", "status": "Available", "flavor": "microgateway.small",
    "totalInstance": 3, "usedInstance": 2, "availableInstance": 1,
    "createTime": 1700000001000,
}


def hcloud_result(stdout="", stderr="", returncode=0):
    return subprocess.CompletedProcess(
        args=["hcloud"], returncode=returncode, stdout=stdout, stderr=stderr)


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


def page(engines, total=None):
    payload = {"data": engines}
    if total is not None:
        payload["total"] = total
    return json.dumps(payload)


class TestWriteIntentGuard(unittest.TestCase):
    def test_read_intent_passes(self):
        for text in ("--region cn-north-4 --type CSE list",
                     "ListEngines", "show get describe query"):
            self.assertFalse(guard_write_intent(text))

    def test_create_delete_update_blocked(self):
        for text in ("CreateEngine", "DeleteEngine", "UpdateEngine",
                     "UpgradeEngine", "ModifyEngine"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_mutating_verbs_blocked(self):
        for text in ("--reboot-engine", "resize_engine", "stopEngine",
                     "startEngine", "batch-delete"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_selector_values_not_scanned(self):
        text = guard_text_from_argv(
            ["--name", "update-prod", "--region", "cn-north-4",
             "--type", "CSE", "--project-id", "delete-me", "--json"])
        for leaked in ("update-prod", "delete-me", "cn-north-4", "CSE"):
            self.assertNotIn(leaked, text)
        self.assertIn("--json", text)
        guard_write_intent(text)

    def test_operation_guard(self):
        self.assertTrue(guard_operation("ListEngines"))
        for bad in ("DeleteEngine", "CreateEngine", "ListEngine"):
            with self.assertRaises(GuardError):
                guard_operation(bad)

    def test_operation_value_still_scanned(self):
        with self.assertRaises(GuardError):
            guard_write_intent(
                guard_text_from_argv(["--operation", "DeleteEngine"]))


class TestBuildCommand(unittest.TestCase):
    def test_defaults(self):
        argv = build_command("cn-north-4")
        self.assertEqual(argv[:2], ["CSE", "ListEngines"])
        self.assertIn("--cli-region=cn-north-4", argv)
        self.assertIn("--limit=100", argv)
        self.assertIn("--offset=0", argv)
        self.assertIn("--type=ALL", argv)
        self.assertFalse(any(p.startswith("--project_id") for p in argv))

    def test_filters_and_project(self):
        argv = build_command("cn-south-1", engine_type="Nacos",
                             project_id="p-1", limit=20, offset=40)
        self.assertIn("--cli-region=cn-south-1", argv)
        self.assertIn("--limit=20", argv)
        self.assertIn("--offset=40", argv)
        self.assertIn("--type=Nacos", argv)
        self.assertIn("--project_id=p-1", argv)

    def test_limit_is_string_like_koocli(self):
        argv = build_command("cn-north-4", limit=50)
        self.assertIn("--limit=50", argv)

    def test_no_write_operation(self):
        self.assertEqual(ALLOWED_OPERATIONS, frozenset((OPERATION,)))
        self.assertEqual(OPERATION, "ListEngines")
        self.assertEqual(REST_PATH, "GET /v2/{project_id}/enginemgr/engines")

    def test_no_write_flags(self):
        argv = build_command("cn-north-4")
        for flag in argv:
            stripped = flag.lower().lstrip("-")
            self.assertFalse(
                stripped.startswith(("create", "delete", "update", "upgrade")))


class TestExtract(unittest.TestCase):
    def test_extract_json_object(self):
        self.assertEqual(extract_json('{"total": 1}'), {"total": 1})

    def test_extract_json_array(self):
        self.assertEqual(extract_json('[{"id": 1}]'), [{"id": 1}])

    def test_extract_json_with_noise(self):
        self.assertEqual(extract_json('WARNING\n{"total": 1}\n'), {"total": 1})
        self.assertEqual(extract_json('INFO\n[{"id": 1}]\n'), [{"id": 1}])

    def test_extract_json_invalid(self):
        with self.assertRaises(ApiError):
            extract_json("<html>not json</html>")

    def test_extract_engines_wrapped(self):
        items, total = extract_engines({"total": 2, "data": [ENGINE_1, ENGINE_2]})
        self.assertEqual(total, 2)
        self.assertEqual(len(items), 2)

    def test_extract_engines_bare_array(self):
        items, total = extract_engines([ENGINE_1])
        self.assertEqual(total, None)
        self.assertEqual(len(items), 1)

    def test_extract_engines_unknown_shape(self):
        items, total = extract_engines({"foo": "bar"})
        self.assertEqual(items, [])
        self.assertIsNone(total)


class TestNormalizeAndRender(unittest.TestCase):
    def test_normalize_camel_case(self):
        flat = normalize_engine(ENGINE_1, "cn-north-4")
        self.assertEqual(flat["name"], "cse-alpha")
        self.assertEqual(flat["id"], "e-0001")
        self.assertEqual(flat["total_instance"], 2)
        self.assertEqual(flat["used_instance"], 1)
        self.assertEqual(flat["create_time"], 1700000000000)
        self.assertEqual(flat["region"], "cn-north-4")

    def test_normalize_snake_case(self):
        flat = normalize_engine(
            {"id": "e-1", "name": "n", "total_instance": 4,
             "create_time": 1700000000}, "cn-south-1")
        self.assertEqual(flat["total_instance"], 4)
        self.assertEqual(flat["region"], "cn-south-1")

    def test_missing_fields_render_dash(self):
        table = render_table([{"name": "bare"}], "cn-north-4")
        self.assertIn("bare", table)
        self.assertIn("-", table)

    def test_table_has_expected_columns(self):
        table = render_table([ENGINE_1, ENGINE_2], "cn-north-4")
        for column in ("name", "id", "type", "version", "status",
                       "flavor", "total_instance", "create_time", "region"):
            self.assertIn(column, table)

    def test_format_time(self):
        self.assertEqual(format_time(1700000000000),
                         "2023-11-14 22:13:20 UTC")
        self.assertEqual(format_time(1700000000),
                         "2023-11-14 22:13:20 UTC")
        self.assertEqual(format_time("2024-01-01"), "2024-01-01")
        self.assertEqual(format_time(None), "-")

    def test_concise_lines(self):
        lines = item_summary_lines([ENGINE_1], "cn-north-4")
        self.assertIn("cse-alpha", lines[0])
        self.assertIn("id: e-0001", lines[0])
        self.assertIn("instances: 1/2", lines[0])
        self.assertIn("region: cn-north-4", lines[0])


class TestFilters(unittest.TestCase):
    def test_name_exact(self):
        out = filter_by_name([ENGINE_1, ENGINE_2], "cse-alpha")
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["id"], "e-0001")

    def test_name_exact_is_case_insensitive(self):
        self.assertEqual(len(filter_by_name([ENGINE_1], "CSE-ALPHA")), 1)

    def test_name_exact_does_not_substring(self):
        self.assertEqual(filter_by_name([ENGINE_1], "cse"), [])

    def test_name_fuzzy(self):
        out = filter_by_name([ENGINE_1, ENGINE_2], "nacos", fuzzy=True)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["id"], "e-0002")

    def test_name_empty(self):
        self.assertEqual(len(filter_by_name([ENGINE_1], None)), 1)


class TestPaging(unittest.TestCase):
    def _run(self, results, limit=2, max_pages=10):
        runner = FakeRunner(results)
        with mock.patch("list_cse_engines.subprocess.run", side_effect=runner):
            items = _collect("cn-north-4", limit=limit, max_pages=max_pages)
        return items, runner

    def test_total_driven_paging(self):
        items, runner = self._run([
            (page([ENGINE_1, ENGINE_2], total=3), "", 0),
            (page([{'id': 'e-3', 'name': 'c'}], total=3), "", 0),
        ])
        self.assertEqual(len(items), 3)
        self.assertEqual(len(runner.calls), 2)
        self.assertIn("--offset=0", runner.calls[0])
        self.assertIn("--offset=2", runner.calls[1])

    def test_full_page_fallback_without_total(self):
        items, runner = self._run([
            (page([ENGINE_1, ENGINE_2]), "", 0),
            (page([{'id': 'e-3', 'name': 'c'}]), "", 0),
        ])
        self.assertEqual(len(items), 3)
        self.assertEqual(len(runner.calls), 2)

    def test_stops_on_short_page(self):
        items, runner = self._run([(page([ENGINE_1]), "", 0)])
        self.assertEqual(len(items), 1)
        self.assertEqual(len(runner.calls), 1)

    def test_type_and_region_forwarded_each_page(self):
        _items, runner = self._run([
            (page([ENGINE_1, ENGINE_2], total=3), "", 0),
            (page([{'id': 'e-3'}], total=3), "", 0),
        ])
        for call in runner.calls:
            self.assertIn("--type=ALL", call)
            self.assertIn("--cli-region=cn-north-4", call)

    def test_paging_guard_raises_after_max_pages(self):
        with self.assertRaises(ApiError):
            self._run([
                (page([ENGINE_1, ENGINE_2], total=99), "", 0),
                (page([ENGINE_1, ENGINE_2], total=99), "", 0),
            ], limit=2, max_pages=2)


class TestErrorClassification(unittest.TestCase):
    def test_missing_credentials(self):
        err = classify_hcloud_failure(
            "", "ERROR: The AK/SK is not configured", 1)
        self.assertIsInstance(err, ConfigError)
        self.assertIn("AK/SK", str(err))

    def test_403(self):
        err = classify_hcloud_failure("", "403 Forbidden", 1)
        self.assertIsInstance(err, AuthError)
        self.assertIn("IAM", str(err))

    def test_use_error_with_rc0(self):
        err = classify_hcloud_failure(
            "[USE_ERROR]Invalid parameter: xxx", "", 0)
        self.assertIsInstance(err, ApiError)
        self.assertIn("hcloud 参数错误", str(err))

    def test_network(self):
        err = classify_hcloud_failure(
            "", "Connection timed out", 1)
        self.assertIsInstance(err, ApiError)
        self.assertIn("网络异常", str(err))

    def test_generic(self):
        err = classify_hcloud_failure("", "boom", 1)
        self.assertIsInstance(err, ApiError)

    def test_error_body_with_rc0_is_auth(self):
        payload = {
            "error_code": "SVCSTG.00509431",
            "error_message": "User is not authorized to perform: cse:engine:list",
        }
        err = error_from_payload(payload)
        self.assertIsInstance(err, AuthError)
        self.assertIn("cse:engine:list", str(err))

    def test_error_body_generic(self):
        err = error_from_payload(
            {"error_code": "CSE.0001", "error_message": "bad request"})
        self.assertIsInstance(err, ApiError)

    def test_success_payload_has_no_error(self):
        self.assertIsNone(error_from_payload({"total": 0, "data": []}))

    def test_auth_body_raises_from_collect(self):
        runner = FakeRunner([(
            json.dumps({"error_code": "SVCSTG.00509431",
                        "error_message": "User is not authorized to perform: "
                                         "cse:engine:list"}), "", 0)])
        with mock.patch("list_cse_engines.subprocess.run", side_effect=runner):
            with self.assertRaises(AuthError):
                _collect("cn-north-4")


class TestSdkFallback(unittest.TestCase):
    def _fake_modules(self, captured, response, auth_ok=True):
        core = types.ModuleType("huaweicloudsdkcore")
        auth = types.ModuleType("huaweicloudsdkcore.auth")
        cred_mod = types.ModuleType("huaweicloudsdkcore.auth.credentials")
        region_mod = types.ModuleType("huaweicloudsdkcore.region.region")
        http_mod = types.ModuleType("huaweicloudsdkcore.http.http_config")

        class BasicCredentials:
            def __init__(self, ak=None, sk=None, project_id=None):
                captured["ak"] = ak
                captured["sk"] = sk
                self.project_id = project_id

            def with_project_id(self, project_id):
                self.project_id = project_id
                captured["project_id"] = project_id
                return self

        class Region:
            def __init__(self, id_, endpoint):
                captured["region"] = (id_, endpoint)

        class HttpConfig:
            @staticmethod
            def get_default_config():
                return object()

        cred_mod.BasicCredentials = BasicCredentials
        region_mod.Region = Region
        http_mod.HttpConfig = HttpConfig

        cse = types.ModuleType("huaweicloudsdkcse")
        cse_v1 = types.ModuleType("huaweicloudsdkcse.v1")
        cse_region = types.ModuleType("huaweicloudsdkcse.v1.region")
        cse_region_mod = types.ModuleType(
            "huaweicloudsdkcse.v1.region.cse_region")

        class ListEnginesRequest:
            def __init__(self, offset=None, limit=None, type=None):
                captured.setdefault("requests", []).append(
                    {"offset": offset, "limit": limit, "type": type})

        class _Client:
            def list_engines(self, request):
                return response

        class _Builder:
            def with_credentials(self, _c):
                return self

            def with_region(self, _r):
                return self

            def with_http_config(self, _h):
                return self

            def build(self):
                return _Client()

        class CseClient:
            @staticmethod
            def new_builder():
                return _Builder()

        class CseRegion:
            @staticmethod
            def value_of(region):
                raise ValueError("custom region")

        cse_v1.CseClient = CseClient
        cse_v1.ListEnginesRequest = ListEnginesRequest
        cse_region_mod.CseRegion = CseRegion

        return {
            "huaweicloudsdkcore": core,
            "huaweicloudsdkcore.auth": auth,
            "huaweicloudsdkcore.auth.credentials": cred_mod,
            "huaweicloudsdkcore.region": types.ModuleType(
                "huaweicloudsdkcore.region"),
            "huaweicloudsdkcore.region.region": region_mod,
            "huaweicloudsdkcore.http": types.ModuleType(
                "huaweicloudsdkcore.http"),
            "huaweicloudsdkcore.http.http_config": http_mod,
            "huaweicloudsdkcse": cse,
            "huaweicloudsdkcse.v1": cse_v1,
            "huaweicloudsdkcse.v1.region": cse_region,
            "huaweicloudsdkcse.v1.region.cse_region": cse_region_mod,
        }

    def test_sdk_success(self):
        captured = {}

        class Response:
            total = 2
            data = [
                types.SimpleNamespace(to_dict=lambda: dict(ENGINE_1)),
                types.SimpleNamespace(to_dict=lambda: dict(ENGINE_2)),
            ]

        modules = self._fake_modules(captured, Response())
        env = {"HUAWEI_ACCESS_KEY": "ak", "HUAWEI_SECRET_KEY": "sk"}
        with mock.patch.dict(sys.modules, modules), \
                mock.patch.dict(os.environ, env, clear=True):
            items = list_engines_via_sdk("cn-north-4", engine_type="Nacos",
                                         project_id="p-9", limit=50)
        self.assertEqual(len(items), 2)
        self.assertEqual(captured["ak"], "ak")
        self.assertEqual(captured["project_id"], "p-9")
        self.assertEqual(captured["requests"],
                         [{"offset": 0, "limit": "50", "type": "Nacos"}])

    def test_sdk_missing_credentials(self):
        modules = self._fake_modules({}, object())
        with mock.patch.dict(sys.modules, modules), \
                mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ConfigError):
                list_engines_via_sdk("cn-north-4")

    def test_env_credential_ignores_non_credential_variables(self):
        env = {
            "HUAWEI_TOKEN": "not-a-credential",
            "HUAWEI_REGION": "cn-north-4",
            "HWC_ENDPOINT": "https://example.invalid",
            "HW_PROJECT_ID": "p-1",
        }
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertIsNone(_env_credential(("HUAWEI_ACCESS_KEY",)))
            self.assertIsNone(_env_credential(("HUAWEI_SECRET_KEY",)))

    def test_env_credential_reads_explicit_allowlist_name(self):
        with mock.patch.dict(os.environ, {"HWC_AK": "ak-1"}, clear=True):
            self.assertEqual(_env_credential(("HW_AK", "HWC_AK")), "ak-1")

    def test_sdk_auth_error(self):
        captured = {}

        class Response:
            total = 0
            data = []

        class _Client:
            def list_engines(self, request):
                raise RuntimeError("not authorized to perform cse:engine:list")

        modules = self._fake_modules(captured, Response())
        modules["huaweicloudsdkcse.v1"].CseClient.new_builder = staticmethod(
            lambda: types.SimpleNamespace(
                with_credentials=lambda c: types.SimpleNamespace(
                    with_region=lambda r: types.SimpleNamespace(
                        with_http_config=lambda h: types.SimpleNamespace(
                            build=lambda: _Client())))))
        env = {"HUAWEI_ACCESS_KEY": "ak", "HUAWEI_SECRET_KEY": "sk"}
        with mock.patch.dict(sys.modules, modules), \
                mock.patch.dict(os.environ, env, clear=True):
            with self.assertRaises(AuthError):
                list_engines_via_sdk("cn-north-4")

    def test_collect_falls_back_when_hcloud_missing(self):
        with mock.patch("list_cse_engines.subprocess.run",
                        side_effect=FileNotFoundError), \
                mock.patch("list_cse_engines.list_engines_via_sdk",
                           return_value=[ENGINE_1]) as fallback:
            items = _collect("cn-north-4", engine_type="CSE")
        self.assertEqual(items, [ENGINE_1])
        fallback.assert_called_once()


class TestMain(unittest.TestCase):
    def _main(self, argv, results):
        runner = FakeRunner(results)
        with mock.patch("list_cse_engines.subprocess.run", side_effect=runner):
            return main(argv)

    def test_table_mode(self):
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = self._main(
                ["--region", "cn-north-4", "--table"],
                [(page([ENGINE_1, ENGINE_2], total=2), "", 0)])
        self.assertEqual(rc, 0)
        out = buf.getvalue()
        self.assertIn("完整字段", out)
        self.assertIn("cse-alpha", out)
        self.assertIn("total_instance", out)

    def test_json_mode(self):
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = self._main(
                ["--region", "cn-north-4", "--json"],
                [(page([ENGINE_1], total=1), "", 0)])
        self.assertEqual(rc, 0)
        data = json.loads(buf.getvalue())
        self.assertEqual(data[0]["name"], "cse-alpha")
        self.assertEqual(data[0]["region"], "cn-north-4")

    def test_concise_mode_default(self):
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = self._main(
                ["--region", "cn-north-4"],
                [(page([ENGINE_1], total=1), "", 0)])
        self.assertEqual(rc, 0)
        out = buf.getvalue()
        self.assertIn("cse-alpha", out)
        self.assertIn("instances: 1/2", out)
        self.assertNotIn("完整字段", out)

    def test_empty_list_rc0(self):
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = self._main(
                ["--region", "cn-north-4"],
                [(page([], total=0), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("未找到微服务引擎", buf.getvalue())

    def test_type_filter_forwarded(self):
        runner = FakeRunner([(page([], total=0), "", 0)])
        with mock.patch("list_cse_engines.subprocess.run", side_effect=runner):
            main(["--type", "nacos"])
        self.assertIn("--type=Nacos", runner.calls[0])

    def test_name_filter_exact(self):
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = self._main(
                ["--name", "nacos-beta"],
                [(page([ENGINE_1, ENGINE_2], total=2), "", 0)])
        self.assertEqual(rc, 0)
        out = buf.getvalue()
        self.assertIn("nacos-beta", out)
        self.assertNotIn("cse-alpha", out)

    def test_name_filter_fuzzy(self):
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = self._main(
                ["--name", "cse", "--fuzzy"],
                [(page([ENGINE_1, ENGINE_2], total=2), "", 0)])
        self.assertEqual(rc, 0)
        out = buf.getvalue()
        self.assertIn("cse-alpha", out)
        self.assertNotIn("nacos-beta", out)

    def test_write_intent_rejected_before_any_call(self):
        import io
        from contextlib import redirect_stderr
        runner = FakeRunner([])
        buf = io.StringIO()
        with mock.patch("list_cse_engines.subprocess.run",
                        side_effect=runner), redirect_stderr(buf):
            rc = main(["--operation", "DeleteEngine"])
        self.assertEqual(rc, 1)
        self.assertEqual(runner.calls, [])
        self.assertIn("写操作意图", buf.getvalue())

    def test_mutating_flag_rejected(self):
        import io
        from contextlib import redirect_stderr
        buf = io.StringIO()
        with redirect_stderr(buf):
            rc = main(["--create-engine", "demo"])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", buf.getvalue())

    def test_error_has_no_traceback(self):
        import io
        from contextlib import redirect_stderr
        buf = io.StringIO()
        with redirect_stderr(buf):
            rc = self._main([], [("", "403 Forbidden", 1)])
        self.assertEqual(rc, 1)
        err = buf.getvalue()
        self.assertIn("IAM", err)
        self.assertNotIn("Traceback", err)

    def test_project_id_forwarded(self):
        runner = FakeRunner([(page([], total=0), "", 0)])
        with mock.patch("list_cse_engines.subprocess.run", side_effect=runner):
            main(["--project-id", "p-1"])
        self.assertIn("--project_id=p-1", runner.calls[0])

    def test_invalid_type_exits_nonzero(self):
        with self.assertRaises(SystemExit):
            main(["--type", "BOGUS"])


class TestPublicApi(unittest.TestCase):
    def test_list_cse_engines_applies_filter(self):
        runner = FakeRunner([(page([ENGINE_1, ENGINE_2], total=2), "", 0)])
        with mock.patch("list_cse_engines.subprocess.run", side_effect=runner):
            items = list_cse_engines("cn-north-4", name="cse-alpha")
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["id"], "e-0001")

    def test_error_type_hierarchy(self):
        for cls in (GuardError, ConfigError, AuthError, ApiError):
            self.assertTrue(issubclass(cls, CseListError))


if __name__ == "__main__":
    unittest.main()