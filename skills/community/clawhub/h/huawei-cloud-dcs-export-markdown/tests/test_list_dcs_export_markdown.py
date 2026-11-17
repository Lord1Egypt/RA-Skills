import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

# Never emit __pycache__/*.pyc for the bundled scripts modules.
sys.dont_write_bytecode = True

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from export_markdown import (  # noqa: E402
    MD_HEADERS,
    ExportError,
    default_output_path,
    export_markdown,
    render_markdown,
)
from list_dcs_export_markdown import (  # noqa: E402
    ALLOWED_OPERATION,
    ApiError,
    AuthError,
    ConfigError,
    DcsExportError,
    GuardError,
    active_filter_descriptions,
    build_command,
    build_hcloud_command,
    classify_hcloud_failure,
    extract_instances,
    extract_json,
    guard_operation,
    guard_text_from_argv,
    guard_write_intent,
    list_instances,
    list_instances_via_sdk,
    main,
    normalize_instance,
    render_table,
    run_hcloud,
)

INSTANCE_1 = {
    "instance_id": "dcs-0001",
    "name": "cache-demo-01",
    "engine": "Redis",
    "engine_version": "5.0",
    "capacity": "2",
    "spec_code": "redis.ha.xu1.large.r2.2",
    "status": "RUNNING",
    "ip": "192.168.0.10",
    "port": 6379,
    "az_codes": ["cn-north-4a"],
    "tags": [{"key": "env", "value": "prod"}],
    "charging_mode": "0",
}
INSTANCE_2 = {
    "instance_id": "dcs-0002",
    "name": "cache-demo-02",
    "engine": "Memcached",
    "engine_version": "1.6",
    "capacity": "4",
    "spec_code": "memcached.ha.xu1.large.r2.4",
    "status": "RUNNING",
    "ip": "192.168.0.11",
    "port": 11211,
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
        self.assertFalse(guard_write_intent("--region cn-north-4 --format table list instances"))
        self.assertFalse(guard_write_intent("show instance details"))

    def test_create_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("CreateInstance cache-new")

    def test_delete_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--operation DeleteSingleInstance")

    def test_resize_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("ResizeInstance dcs-01")

    def test_restart_flush_blocked(self):
        for text in ("restart instance", "flush data", "clear cache",
                     "backup instance", "restore backup", "freeze instance"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_normalized_separators_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--create-instance")
        with self.assertRaises(GuardError):
            guard_write_intent("delete_instance")

    def test_operation_guard_rejects_non_list(self):
        with self.assertRaises(GuardError):
            guard_operation("ResizeInstance")
        with self.assertRaises(GuardError):
            guard_operation("CreateInstance")
        self.assertTrue(guard_operation(ALLOWED_OPERATION))

    def test_guard_text_strips_filter_values(self):
        self.assertEqual(guard_text_from_argv(["--status", "RUNNING"]), "")
        self.assertEqual(guard_text_from_argv(["--status=RESIZE"]), "")
        self.assertEqual(guard_text_from_argv(["--name", "restart-me"]), "")
        self.assertEqual(guard_text_from_argv(["--region", "cn-north-4"]), "")
        self.assertEqual(guard_text_from_argv(["--tags", "env=delete-me"]), "")
        self.assertIn("DeleteSingleInstance",
                      guard_text_from_argv(["--operation", "DeleteSingleInstance"]))
        self.assertIn("--create-instance",
                      guard_text_from_argv(["--create-instance"]))

    def test_status_value_not_blocked(self):
        self.assertFalse(
            guard_write_intent(guard_text_from_argv(["--status", "RUNNING"])))
        self.assertFalse(
            guard_write_intent(guard_text_from_argv(["--name", "stop-me"])))
        self.assertFalse(
            guard_write_intent(guard_text_from_argv(["--tags", "env=clear-me"])))

    def test_guard_text_strips_output_and_format_values(self):
        self.assertEqual(
            guard_text_from_argv(["--output", "cache-delete-report.md"]), "")
        self.assertEqual(
            guard_text_from_argv(["--output=cache-restart-report.md"]), "")
        self.assertEqual(guard_text_from_argv(["-o", "cache-flush-report.md"]), "")
        self.assertEqual(guard_text_from_argv(["--format", "md"]), "")
        # A following *flag* is still scanned.
        self.assertIn("--create-instance",
                      guard_text_from_argv(["--output", "--create-instance"]))

    def test_output_path_with_write_words_not_blocked(self):
        self.assertFalse(guard_write_intent(
            guard_text_from_argv(["--output", "cache-delete-report.md"])))
        self.assertFalse(guard_write_intent(
            guard_text_from_argv(["--output", "cache-restart-report.md"])))


class TestBuildCommand(unittest.TestCase):
    def test_basic(self):
        argv = build_command("cn-north-4")
        self.assertEqual(argv[0], "DCS")
        self.assertEqual(argv[1], "ListInstances")
        self.assertIn("--cli-region=cn-north-4", argv)
        self.assertIn("--limit=100", argv)
        self.assertIn("--offset=0", argv)

    def test_filters_appended(self):
        argv = build_command("cn-south-1", name="cache", instance_id="dcs-1",
                             ip="192.168.0.10", status="RUNNING", tags="env=prod",
                             limit=10, offset=20)
        self.assertIn("--name=cache", argv)
        self.assertIn("--instance_id=dcs-1", argv)
        self.assertIn("--ip=192.168.0.10", argv)
        self.assertIn("--status=RUNNING", argv)
        self.assertIn("--tags=env=prod", argv)
        self.assertIn("--limit=10", argv)
        self.assertIn("--offset=20", argv)

    def test_no_write_flags_ever_added(self):
        argv = build_command("cn-north-4", status="RUNNING", name="cache")
        for flag in argv:
            self.assertFalse(
                flag.lower().lstrip("-").startswith(
                    ("create", "delete", "update", "resize", "restart")))


class TestQualityWrapper(unittest.TestCase):
    def _env(self, **kwargs):
        base = {"DCS_EXPORT_MARKDOWN_HCLOUD_BIN": "", "DCS_EXPORT_MARKDOWN_SQC_BIN": "",
                "SKILL_QUALITY_REPORT": ""}
        base.update(kwargs)
        return base

    def test_wrapped_with_skill_quality_cli(self):
        with mock.patch.dict(os.environ, self._env(DCS_EXPORT_MARKDOWN_SQC_BIN="/usr/bin/sqc")):
            cmd = build_hcloud_command(build_command("cn-north-4"))
        self.assertEqual(cmd[0], "/usr/bin/sqc")
        self.assertEqual(cmd[1:4], ["run", "--skill-name",
                                    "huawei-cloud-dcs-export-markdown"])
        self.assertEqual(cmd[4], "--")
        self.assertEqual(cmd[5:7], ["hcloud", "DCS"])

    def test_bin_override_runs_bare(self):
        with mock.patch.dict(os.environ, self._env(DCS_EXPORT_MARKDOWN_HCLOUD_BIN="/mock/hcloud")):
            cmd = build_hcloud_command(build_command("cn-north-4"))
        self.assertEqual(cmd[0], "/mock/hcloud")
        self.assertEqual(cmd[1:3], ["DCS", "ListInstances"])

    def test_report_disabled_runs_bare(self):
        with mock.patch.dict(os.environ, self._env(
                DCS_EXPORT_MARKDOWN_SQC_BIN="/usr/bin/sqc", SKILL_QUALITY_REPORT="0")):
            cmd = build_hcloud_command(build_command("cn-north-4"))
        self.assertEqual(cmd[0], "hcloud")

    def test_extra_args_tail(self):
        calls = []

        def fake(cmd, **kwargs):
            calls.append(cmd)
            return hcloud_result(json.dumps({"instances": [INSTANCE_1], "instance_num": 1}))

        with mock.patch("list_dcs_export_markdown.subprocess.run", fake), \
                mock.patch.dict(os.environ, self._env(
                    DCS_EXPORT_MARKDOWN_HCLOUD_BIN="/mock/hcloud",
                    DCS_EXPORT_MARKDOWN_HCLOUD_ARGS="-v")):
            run_hcloud(build_command("cn-north-4"))
        self.assertEqual(calls[0][1:3], ["DCS", "ListInstances"])
        self.assertEqual(calls[0][-1], "-v")

    def test_extra_args_write_intent_blocked(self):
        with mock.patch.dict(os.environ, self._env(
                DCS_EXPORT_MARKDOWN_HCLOUD_BIN="/mock/hcloud",
                DCS_EXPORT_MARKDOWN_HCLOUD_ARGS="--operation ResizeInstance")):
            with self.assertRaises(GuardError):
                run_hcloud(build_command("cn-north-4"))


class TestExtract(unittest.TestCase):
    def test_extract_json_plain(self):
        self.assertEqual(extract_json(json.dumps({"instances": []})), {"instances": []})

    def test_extract_json_with_noise(self):
        self.assertEqual(extract_json('WARNING noise\n{"instance_num": 1}\n'),
                         {"instance_num": 1})

    def test_extract_json_invalid(self):
        with self.assertRaises(ApiError):
            extract_json("<html>not json</html>")

    def test_extract_instances_known_keys(self):
        for key in ("instances", "instance_list", "instances_detail"):
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

    def test_generic_api_error(self):
        self.assertIsInstance(classify_hcloud_failure("", "boom", 2), ApiError)

    def test_use_error_marker_with_zero_rc(self):
        err = classify_hcloud_failure(
            "[USE_ERROR]Invalid parameter: xxx\n\n"
            "Run `hcloud DCS ListInstances --help` for details.", "", 0)
        self.assertIsInstance(err, ApiError)
        self.assertIn("参数错误", str(err))


class TestListInstances(unittest.TestCase):
    def _patch(self, results):
        return mock.patch("list_dcs_export_markdown.subprocess.run", FakeRunner(results))

    def test_single_page(self):
        fake = FakeRunner([(json.dumps({"instances": [INSTANCE_1, INSTANCE_2], "instance_num": 2}), "", 0)])
        with mock.patch("list_dcs_export_markdown.subprocess.run", fake), \
                mock.patch.dict(os.environ, {"DCS_EXPORT_MARKDOWN_HCLOUD_BIN": "/mock/hcloud"}):
            instances = list_instances("cn-north-4")
        self.assertEqual(instances, [INSTANCE_1, INSTANCE_2])
        self.assertEqual(len(fake.calls), 1)

    def test_pagination_via_instance_num(self):
        page1 = {"instances": [INSTANCE_1], "instance_num": 2}
        page2 = {"instances": [INSTANCE_2], "instance_num": 2}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("list_dcs_export_markdown.subprocess.run", fake), \
                mock.patch.dict(os.environ, {"DCS_EXPORT_MARKDOWN_HCLOUD_BIN": "/mock/hcloud"}):
            instances = list_instances("cn-north-4", limit=1)
        self.assertEqual(instances, [INSTANCE_1, INSTANCE_2])
        self.assertIn("--offset=1", fake.calls[1])

    def test_pagination_full_page_without_total(self):
        fake = FakeRunner([(json.dumps({"instances": [INSTANCE_1]}), "", 0),
                           (json.dumps({"instances": []}), "", 0)])
        with mock.patch("list_dcs_export_markdown.subprocess.run", fake), \
                mock.patch.dict(os.environ, {"DCS_EXPORT_MARKDOWN_HCLOUD_BIN": "/mock/hcloud"}):
            instances = list_instances("cn-north-4", limit=1)
        self.assertEqual(instances, [INSTANCE_1])

    def test_empty_region(self):
        fake = FakeRunner([(json.dumps({"instances": [], "instance_num": 0}), "", 0)])
        with mock.patch("list_dcs_export_markdown.subprocess.run", fake), \
                mock.patch.dict(os.environ, {"DCS_EXPORT_MARKDOWN_HCLOUD_BIN": "/mock/hcloud"}):
            instances = list_instances("cn-north-4")
        self.assertEqual(instances, [])

    def test_filters_forwarded_server_side(self):
        fake = FakeRunner([(json.dumps({"instances": [INSTANCE_1], "instance_num": 1}), "", 0)])
        with mock.patch("list_dcs_export_markdown.subprocess.run", fake), \
                mock.patch.dict(os.environ, {"DCS_EXPORT_MARKDOWN_HCLOUD_BIN": "/mock/hcloud"}):
            list_instances("cn-north-4", name="cache", status="RUNNING", tags="env=prod")
        call = fake.calls[0]
        self.assertIn("--name=cache", call)
        self.assertIn("--status=RUNNING", call)
        self.assertIn("--tags=env=prod", call)

    def test_use_error_rc0_raises(self):
        fake = FakeRunner([("[USE_ERROR]Invalid parameter: xxx", "", 0)])
        with mock.patch("list_dcs_export_markdown.subprocess.run", fake), \
                mock.patch.dict(os.environ, {"DCS_EXPORT_MARKDOWN_HCLOUD_BIN": "/mock/hcloud"}):
            with self.assertRaises(ApiError):
                list_instances("cn-north-4")

    def test_nonzero_exit_403(self):
        fake = FakeRunner([("", "403 Forbidden", 1)])
        with mock.patch("list_dcs_export_markdown.subprocess.run", fake), \
                mock.patch.dict(os.environ, {"DCS_EXPORT_MARKDOWN_HCLOUD_BIN": "/mock/hcloud"}):
            with self.assertRaises(AuthError):
                list_instances("cn-north-4")

    def test_timeout(self):
        fake = FakeRunner([subprocess.TimeoutExpired(cmd="hcloud", timeout=120)])
        with mock.patch("list_dcs_export_markdown.subprocess.run", fake), \
                mock.patch.dict(os.environ, {"DCS_EXPORT_MARKDOWN_HCLOUD_BIN": "/mock/hcloud"}):
            with self.assertRaises(ApiError):
                list_instances("cn-north-4")

    def test_sdk_fallback_when_hcloud_missing(self):
        with mock.patch("list_dcs_export_markdown.subprocess.run", FakeRunner([FileNotFoundError()])), \
                mock.patch("list_dcs_export_markdown.list_instances_via_sdk",
                           return_value=[INSTANCE_1]) as sdk_mock:
            instances = list_instances("cn-north-4", status="RUNNING")
        self.assertEqual(instances, [INSTANCE_1])
        self.assertEqual(sdk_mock.call_args.kwargs.get("status"), "RUNNING")


class TestSdkFallback(unittest.TestCase):
    def test_missing_env_credentials_raises_config(self):
        credential_vars = (
            "HUAWEI_ACCESS_KEY", "HW_ACCESS_KEY", "HWC_ACCESS_KEY",
            "HUAWEICLOUD_SDK_AK", "HUAWEI_CLOUD_ACCESS_KEY",
            "HUAWEI_SECRET_KEY", "HW_SECRET_KEY", "HWC_SECRET_KEY",
            "HUAWEICLOUD_SDK_SK", "HUAWEI_CLOUD_SECRET_KEY",
        )
        with mock.patch.dict(os.environ, {name: "" for name in credential_vars}):
            with self.assertRaises(ConfigError) as ctx:
                list_instances_via_sdk("cn-north-4")
        self.assertIn("AK/SK", str(ctx.exception))

    def test_missing_project_id_raises_config(self):
        env = {
            "HUAWEI_ACCESS_KEY": "x", "HUAWEI_SECRET_KEY": "y",
            "HUAWEI_PROJECT_ID": "", "HW_PROJECT_ID": "",
            "HUAWEICLOUD_SDK_PROJECT_ID": "", "HUAWEI_CLOUD_PROJECT_ID": "",
        }
        with mock.patch.dict(os.environ, env):
            with self.assertRaises(ConfigError) as ctx:
                list_instances_via_sdk("cn-north-4")
        self.assertIn("project_id", str(ctx.exception))


class TestNormalizeAndRender(unittest.TestCase):
    def test_normalize_flattens_az_and_tags(self):
        flat = normalize_instance(INSTANCE_1)
        self.assertEqual(flat["az_codes"], "cn-north-4a")
        self.assertEqual(flat["tags"], "env=prod")

    def test_normalize_id_to_instance_id(self):
        flat = normalize_instance({"id": "dcs-x"})
        self.assertEqual(flat["instance_id"], "dcs-x")

    def test_table_contains_basic_info(self):
        table = render_table([INSTANCE_1, INSTANCE_2])
        for fragment in ("cache-demo-01", "dcs-0001", "Redis", "RUNNING",
                         "192.168.0.10", "cache-demo-02", "Memcached"):
            self.assertIn(fragment, table)

    def test_active_filter_descriptions(self):
        self.assertEqual(
            active_filter_descriptions(name="cache", status="RUNNING"),
            ["name=cache", "status=RUNNING"])
        self.assertEqual(active_filter_descriptions(), [])


class TestRenderMarkdown(unittest.TestCase):
    def test_headers_and_rows(self):
        text = render_markdown([normalize_instance(INSTANCE_1)])
        header = "| " + " | ".join(MD_HEADERS) + " |"
        self.assertIn(header, text)
        self.assertIn("| cache-demo-01 | dcs-0001 | Redis | 5.0 | 2 | "
                      "redis.ha.xu1.large.r2.2 | RUNNING | 192.168.0.10 | 6379 | cn-north-4a |",
                      text)

    def test_missing_fields_render_dash(self):
        text = render_markdown([{"instance_id": "dcs-x"}])
        self.assertIn("| - | dcs-x | - | - | - | - | - | - | - | - |", text)

    def test_summary_line(self):
        text = render_markdown([normalize_instance(INSTANCE_1)],
                               summary=True, region="cn-north-4")
        self.assertIn("**汇总**：共 1 个 DCS 实例（Region cn-north-4）。", text)
        self.assertNotIn("汇总", render_markdown([], summary=False))

    def test_pipe_in_value_escaped(self):
        text = render_markdown([{"name": "a|b"}])
        self.assertIn("a\\|b", text)


class TestExportMarkdown(unittest.TestCase):
    def test_export_writes_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "dcs.md")
            written = export_markdown([normalize_instance(INSTANCE_1)], path,
                                      summary=True, region="cn-north-4")
            self.assertEqual(written, os.path.abspath(path))
            self.assertTrue(os.path.isfile(path))
            with open(path, encoding="utf-8") as fh:
                content = fh.read()
            self.assertIn("| 名称 | ID | 引擎 | 版本 | 容量 | 规格 | 状态 | 连接地址 | 端口 | 可用区 |", content)
            self.assertIn("cache-demo-01", content)
            self.assertIn("汇总", content)

    def test_export_creates_missing_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "nested", "dir", "dcs.md")
            export_markdown([normalize_instance(INSTANCE_1)], path)
            self.assertTrue(os.path.isfile(path))

    def test_export_bad_path_raises_and_leaves_no_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            blocker = os.path.join(tmp, "blocker")
            with open(blocker, "w") as fh:
                fh.write("x")
            bad = os.path.join(blocker, "sub", "dcs.md")
            with self.assertRaises(ExportError):
                export_markdown([normalize_instance(INSTANCE_1)], bad)
            self.assertFalse(os.path.exists(bad))

    def test_default_output_path_format(self):
        path = default_output_path("cn-north-4")
        self.assertTrue(re.match(r"dcs_instances_cn-north-4_\d{8}_\d{6}\.md$", path))


class TestMain(unittest.TestCase):
    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("list_dcs_export_markdown.subprocess.run", fake), \
                mock.patch.dict(os.environ, {"DCS_EXPORT_MARKDOWN_HCLOUD_BIN": "/mock/hcloud"}), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            rc = main(argv)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    def _page(self, instances):
        return [(json.dumps({"instances": instances, "instance_num": len(instances)}), "", 0)]

    def test_md_output_writes_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "dcs.md")
            rc, stdout, err = self._run(
                ["--region", "cn-north-4", "--output", out, "--summary"],
                self._page([INSTANCE_1, INSTANCE_2]))
            self.assertEqual(rc, 0)
            self.assertTrue(os.path.isfile(out))
            self.assertIn("dcs.md", stdout)
            self.assertEqual(err, "")

    def test_default_md_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            old = os.getcwd()
            os.chdir(tmp)
            try:
                import list_dcs_export_markdown as mod
                with mock.patch.object(mod, "default_output_path",
                                       return_value=os.path.join(tmp, "default.md")):
                    fake = FakeRunner(self._page([INSTANCE_1]))
                    with mock.patch("list_dcs_export_markdown.subprocess.run", fake), \
                            mock.patch.dict(os.environ, {"DCS_EXPORT_MARKDOWN_HCLOUD_BIN": "/mock/hcloud"}), \
                            mock.patch("sys.stdout") as stdout:
                        rc = mod.main([])
                    out = "".join(c[0][0] for c in stdout.write.call_args_list)
                    self.assertEqual(rc, 0)
                    self.assertTrue(os.path.isfile(os.path.join(tmp, "default.md")))
            finally:
                os.chdir(old)

    def test_table_output(self):
        rc, out, err = self._run(["--format", "table"], self._page([INSTANCE_1, INSTANCE_2]))
        self.assertEqual(rc, 0)
        self.assertIn("DCS 实例列表", out)
        self.assertIn("cache-demo-01", out)

    def test_json_output(self):
        rc, out, err = self._run(["--format", "json"], self._page([INSTANCE_1]))
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out), [INSTANCE_1])

    def test_empty_md_no_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "empty.md")
            rc, stdout, err = self._run(["--output", out], self._page([]))
            self.assertEqual(rc, 0)
            self.assertIn("无 DCS 实例", stdout)
            self.assertFalse(os.path.exists(out))

    def test_empty_table_message_with_filter(self):
        rc, out, _ = self._run(["--format", "table", "--status", "RUNNING"], self._page([]))
        self.assertEqual(rc, 0)
        self.assertIn("status=RUNNING", out)

    def test_auth_error_no_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "nope.md")
            rc, stdout, err = self._run(["--output", out], [("", "403 Forbidden", 1)])
            self.assertEqual(rc, 1)
            self.assertIn("IAM", err)
            self.assertFalse(os.path.exists(out))

    def test_missing_ak_sk_no_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "nope.md")
            rc, stdout, err = self._run(["--output", out], [("", "ERROR: no AK configured", 1)])
            self.assertEqual(rc, 1)
            self.assertIn("AK/SK", err)
            self.assertFalse(os.path.exists(out))

    def test_write_intent_operation_blocked(self):
        rc, out, err = self._run(["--operation", "ResizeInstance"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)

    def test_write_flag_argv_blocked(self):
        rc, out, err = self._run(["--create-instance"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)

    def test_page_size_out_of_range(self):
        rc, out, err = self._run(["--page-size", "5000"], [])
        self.assertEqual(rc, 1)
        self.assertIn("page-size", err)

    def test_valid_status_not_blocked(self):
        rc, out, err = self._run(["--format", "table", "--status", "RUNNING"],
                                 self._page([INSTANCE_1]))
        self.assertEqual(rc, 0)
        self.assertNotIn("写操作意图", err)


class TestErrorHierarchy(unittest.TestCase):
    def test_subclasses(self):
        for exc in (GuardError, ConfigError, AuthError, ApiError):
            self.assertTrue(issubclass(exc, DcsExportError))


if __name__ == "__main__":
    unittest.main()