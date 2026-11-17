import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

# Never emit __pycache__/*.pyc for the bundled scripts module.
sys.dont_write_bytecode = True

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from export_vpc_markdown import (  # noqa: E402
    ALLOWED_OPERATION,
    ApiError,
    AuthError,
    ConfigError,
    ExportError,
    GuardError,
    MD_HEADERS,
    VpcExportError,
    active_filter_descriptions,
    build_command,
    build_hcloud_command,
    classify_hcloud_failure,
    default_output_path,
    export_markdown,
    extract_json,
    extract_vpcs,
    guard_operation,
    guard_text_from_argv,
    guard_write_intent,
    list_vpcs,
    list_vpcs_via_sdk,
    main,
    normalize_vpc,
    render_markdown,
    render_table,
    run_hcloud,
    vpc_names,
)

VPC_1 = {
    "id": "vpc-0001",
    "name": "vpc-demo-01",
    "cidr": "192.168.0.0/16",
    "status": "OK",
    "description": "demo vpc",
    "routes": [
        {"destination": "0.0.0.0/0", "nexthop": "10.0.0.1"},
    ],
    "enterprise_project_id": "0",
    "tenant_id": "tenant-0001",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-02T00:00:00",
}
VPC_2 = {
    "id": "vpc-0002",
    "name": "vpc-demo-02",
    "cidr": "10.0.0.0/8",
    "status": "CREATING",
    "routes": [],
    "enterprise_project_id": "0",
    "tenant_id": "tenant-0001",
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
        self.assertFalse(guard_write_intent("--region cn-north-4 --format table list vpcs"))
        self.assertFalse(guard_write_intent("show vpc details"))

    def test_create_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("CreateVpc vpc-new")

    def test_delete_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--operation DeleteVpc")

    def test_mutating_verbs_blocked(self):
        for text in ("associate route", "disassociate port",
                     "detach subnet from vpc", "release vpc-01",
                     "update vpc name", "bind bandwidth"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_normalized_separators_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--create-vpc")
        with self.assertRaises(GuardError):
            guard_write_intent("delete_subnet_route")

    def test_operation_guard_rejects_non_list(self):
        with self.assertRaises(GuardError):
            guard_operation("ShowVpc")
        with self.assertRaises(GuardError):
            guard_operation("DeleteVpc")
        self.assertTrue(guard_operation(ALLOWED_OPERATION))

    def test_guard_text_strips_filter_values(self):
        self.assertEqual(guard_text_from_argv(["--region", "cn-north-4"]), "")
        self.assertEqual(guard_text_from_argv(["--id", "vpc-1"]), "")
        self.assertEqual(guard_text_from_argv(["--enterprise-project-id", "0"]), "")
        self.assertEqual(guard_text_from_argv(["--output", "vpc-delete-report.md"]), "")
        self.assertEqual(guard_text_from_argv(["--output=vpc-restart-report.md"]), "")
        self.assertIn("DeleteVpc",
                      guard_text_from_argv(["--operation", "DeleteVpc"]))
        self.assertIn("--create-vpc",
                      guard_text_from_argv(["--create-vpc"]))
        # A following *flag* is still scanned.
        self.assertIn("--create-vpc",
                      guard_text_from_argv(["--output", "--create-vpc"]))

    def test_output_path_with_write_words_not_blocked(self):
        self.assertFalse(guard_write_intent(
            guard_text_from_argv(["--output", "vpc-delete-report.md"])))


class TestBuildCommand(unittest.TestCase):
    def test_basic(self):
        argv = build_command("cn-north-4")
        self.assertEqual(argv[0], "VPC")
        self.assertEqual(argv[1], "ListVpcs")
        self.assertIn("--cli-region=cn-north-4", argv)
        self.assertIn("--limit=100", argv)
        self.assertFalse(any(flag.startswith("--marker") for flag in argv))

    def test_marker_appended(self):
        argv = build_command("cn-north-4", marker="tok-123", limit=10)
        self.assertIn("--marker=tok-123", argv)
        self.assertIn("--limit=10", argv)

    def test_filters_forwarded_server_side(self):
        argv = build_command("cn-south-1", vpc_id="vpc-9",
                             enterprise_project_id="0", limit=10)
        self.assertIn("--id=vpc-9", argv)
        self.assertIn("--enterprise_project_id=0", argv)
        self.assertIn("--limit=10", argv)

    def test_no_write_flags_ever_added(self):
        argv = build_command("cn-north-4", enterprise_project_id="0")
        for flag in argv:
            self.assertFalse(flag.lower().lstrip("-").startswith(
                ("create", "delete", "update", "associate", "release")))


class TestQualityWrapper(unittest.TestCase):
    def _env(self, **kwargs):
        base = {"VPC_EXPORT_MARKDOWN_HCLOUD_BIN": "", "VPC_EXPORT_MARKDOWN_SQC_BIN": "",
                "SKILL_QUALITY_REPORT": ""}
        base.update(kwargs)
        return base

    def test_wrapped_with_skill_quality_cli(self):
        with mock.patch.dict(os.environ, self._env(VPC_EXPORT_MARKDOWN_SQC_BIN="/usr/bin/sqc")):
            cmd = build_hcloud_command(build_command("cn-north-4"))
        self.assertEqual(cmd[0], "/usr/bin/sqc")
        self.assertEqual(cmd[1:4], ["run", "--skill-name",
                                    "huawei-cloud-vpc-export-markdown"])
        self.assertEqual(cmd[4], "--")
        self.assertEqual(cmd[5:7], ["hcloud", "VPC"])

    def test_bin_override_runs_bare(self):
        with mock.patch.dict(os.environ, self._env(VPC_EXPORT_MARKDOWN_HCLOUD_BIN="/mock/hcloud")):
            cmd = build_hcloud_command(build_command("cn-north-4"))
        self.assertEqual(cmd[0], "/mock/hcloud")
        self.assertEqual(cmd[1:3], ["VPC", "ListVpcs"])

    def test_report_disabled_runs_bare(self):
        with mock.patch.dict(os.environ, self._env(
                VPC_EXPORT_MARKDOWN_SQC_BIN="/usr/bin/sqc", SKILL_QUALITY_REPORT="0")):
            cmd = build_hcloud_command(build_command("cn-north-4"))
        self.assertEqual(cmd[0], "hcloud")

    def test_extra_args_tail(self):
        calls = []

        def fake(cmd, **kwargs):
            calls.append(cmd)
            return hcloud_result(json.dumps({"vpcs": [VPC_1]}))

        with mock.patch("export_vpc_markdown.subprocess.run", fake), \
                mock.patch.dict(os.environ, self._env(
                    VPC_EXPORT_MARKDOWN_HCLOUD_BIN="/mock/hcloud",
                    VPC_EXPORT_MARKDOWN_HCLOUD_ARGS="-v")):
            run_hcloud(build_command("cn-north-4"))
        self.assertEqual(calls[0][1:3], ["VPC", "ListVpcs"])
        self.assertEqual(calls[0][-1], "-v")

    def test_extra_args_write_intent_blocked(self):
        with mock.patch.dict(os.environ, self._env(
                VPC_EXPORT_MARKDOWN_HCLOUD_BIN="/mock/hcloud",
                VPC_EXPORT_MARKDOWN_HCLOUD_ARGS="--operation DeleteVpc")):
            with self.assertRaises(GuardError):
                run_hcloud(build_command("cn-north-4"))


class TestExtract(unittest.TestCase):
    def test_extract_json_plain(self):
        self.assertEqual(extract_json(json.dumps({"vpcs": []})), {"vpcs": []})

    def test_extract_json_with_noise(self):
        self.assertEqual(extract_json('WARNING noise\n{"vpcs": []}\n'), {"vpcs": []})

    def test_extract_json_invalid(self):
        with self.assertRaises(ApiError):
            extract_json("<html>not json</html>")

    def test_extract_vpcs_known_keys(self):
        for key in ("vpcs", "vpc"):
            self.assertEqual(extract_vpcs({key: [VPC_1]}), [VPC_1])
        self.assertEqual(extract_vpcs([VPC_1]), [VPC_1])
        self.assertEqual(extract_vpcs({"page_info": {}}), [])


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
            "[USE_ERROR]Invalid parameter: enterprise_project_id\n\n"
            "Run `hcloud VPC ListVpcs --help` for details.", "", 0)
        self.assertIsInstance(err, ApiError)
        self.assertIn("参数错误", str(err))
        self.assertIn("--help", str(err))


class TestListVpcs(unittest.TestCase):
    def _patch(self, results):
        return mock.patch("export_vpc_markdown.subprocess.run", FakeRunner(results))

    def test_single_page(self):
        fake = FakeRunner([(json.dumps({"vpcs": [VPC_1, VPC_2]}), "", 0)])
        with mock.patch("export_vpc_markdown.subprocess.run", fake), \
                mock.patch.dict(os.environ, {"VPC_EXPORT_MARKDOWN_HCLOUD_BIN": "/mock/hcloud"}):
            vpcs = list_vpcs("cn-north-4")
        self.assertEqual(vpcs, [VPC_1, VPC_2])
        self.assertEqual(len(fake.calls), 1)

    def test_pagination_via_next_marker(self):
        page1 = {"vpcs": [VPC_1], "page_info": {"next_marker": "tok-2"}}
        page2 = {"vpcs": [VPC_2], "page_info": {"next_marker": None}}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("export_vpc_markdown.subprocess.run", fake), \
                mock.patch.dict(os.environ, {"VPC_EXPORT_MARKDOWN_HCLOUD_BIN": "/mock/hcloud"}):
            vpcs = list_vpcs("cn-north-4", limit=1)
        self.assertEqual(vpcs, [VPC_1, VPC_2])
        self.assertIn("--marker=tok-2", fake.calls[1])

    def test_pagination_full_page_without_marker(self):
        fake = FakeRunner([(json.dumps({"vpcs": [VPC_1]}), "", 0),
                           (json.dumps({"vpcs": []}), "", 0)])
        with mock.patch("export_vpc_markdown.subprocess.run", fake), \
                mock.patch.dict(os.environ, {"VPC_EXPORT_MARKDOWN_HCLOUD_BIN": "/mock/hcloud"}):
            vpcs = list_vpcs("cn-north-4", limit=1)
        self.assertEqual(vpcs, [VPC_1])

    def test_empty_region(self):
        fake = FakeRunner([(json.dumps({"vpcs": []}), "", 0)])
        with mock.patch("export_vpc_markdown.subprocess.run", fake), \
                mock.patch.dict(os.environ, {"VPC_EXPORT_MARKDOWN_HCLOUD_BIN": "/mock/hcloud"}):
            vpcs = list_vpcs("cn-north-4")
        self.assertEqual(vpcs, [])

    def test_filters_forwarded_to_cli(self):
        fake = FakeRunner([(json.dumps({"vpcs": [VPC_1]}), "", 0)])
        with mock.patch("export_vpc_markdown.subprocess.run", fake), \
                mock.patch.dict(os.environ, {"VPC_EXPORT_MARKDOWN_HCLOUD_BIN": "/mock/hcloud"}):
            list_vpcs("cn-north-4", vpc_id="vpc-0001", enterprise_project_id="0")
        call = fake.calls[0]
        self.assertTrue(any("--id=vpc-0001" in part for part in call))
        self.assertTrue(any("--enterprise_project_id=0" in part for part in call))

    def test_use_error_rc0_raises(self):
        fake = FakeRunner([("[USE_ERROR]Invalid parameter: xxx", "", 0)])
        with mock.patch("export_vpc_markdown.subprocess.run", fake), \
                mock.patch.dict(os.environ, {"VPC_EXPORT_MARKDOWN_HCLOUD_BIN": "/mock/hcloud"}):
            with self.assertRaises(ApiError):
                list_vpcs("cn-north-4")

    def test_nonzero_exit_403(self):
        fake = FakeRunner([("", "403 Forbidden", 1)])
        with mock.patch("export_vpc_markdown.subprocess.run", fake), \
                mock.patch.dict(os.environ, {"VPC_EXPORT_MARKDOWN_HCLOUD_BIN": "/mock/hcloud"}):
            with self.assertRaises(AuthError):
                list_vpcs("cn-north-4")

    def test_timeout(self):
        fake = FakeRunner([subprocess.TimeoutExpired(cmd="hcloud", timeout=120)])
        with mock.patch("export_vpc_markdown.subprocess.run", fake), \
                mock.patch.dict(os.environ, {"VPC_EXPORT_MARKDOWN_HCLOUD_BIN": "/mock/hcloud"}):
            with self.assertRaises(ApiError):
                list_vpcs("cn-north-4")

    def test_sdk_fallback_when_hcloud_missing(self):
        with mock.patch("export_vpc_markdown.subprocess.run", FakeRunner([FileNotFoundError()])), \
                mock.patch("export_vpc_markdown.list_vpcs_via_sdk",
                           return_value=[VPC_1]) as sdk_mock:
            vpcs = list_vpcs("cn-north-4", vpc_id="vpc-1",
                             enterprise_project_id="0", project_id="proj-1")
        self.assertEqual(vpcs, [VPC_1])
        self.assertEqual(sdk_mock.call_args.kwargs.get("vpc_id"), "vpc-1")
        self.assertEqual(sdk_mock.call_args.kwargs.get("project_id"), "proj-1")


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
                list_vpcs_via_sdk("cn-north-4")
        self.assertIn("AK/SK", str(ctx.exception))

    def test_missing_project_id_raises_config(self):
        env = {
            "HUAWEI_ACCESS_KEY": "x", "HUAWEI_SECRET_KEY": "y",
            "HUAWEI_PROJECT_ID": "", "HW_PROJECT_ID": "",
            "HUAWEICLOUD_SDK_PROJECT_ID": "", "HUAWEI_CLOUD_PROJECT_ID": "",
        }
        with mock.patch.dict(os.environ, env):
            with self.assertRaises(ConfigError) as ctx:
                list_vpcs_via_sdk("cn-north-4")
        self.assertIn("project_id", str(ctx.exception))


class TestNormalizeAndRender(unittest.TestCase):
    def test_normalize_compacts_routes(self):
        flat = normalize_vpc(VPC_1)
        self.assertIsInstance(flat["routes"], str)
        self.assertIn("0.0.0.0/0", flat["routes"])
        self.assertEqual(flat["name"], "vpc-demo-01")

    def test_normalize_empty_routes(self):
        self.assertEqual(normalize_vpc(VPC_2)["routes"], "[]")

    def test_table_contains_basic_info(self):
        table = render_table([VPC_1, VPC_2])
        for fragment in ("vpc-0001", "vpc-demo-01", "192.168.0.0/16", "OK",
                         "vpc-0002", "10.0.0.0/8", "CREATING"):
            self.assertIn(fragment, table)

    def test_names(self):
        self.assertEqual(vpc_names([VPC_1, VPC_2]), ["vpc-demo-01", "vpc-demo-02"])

    def test_names_fallback_to_id(self):
        self.assertEqual(vpc_names([{"id": "vpc-9"}]), ["vpc-9"])

    def test_active_filter_descriptions(self):
        self.assertEqual(
            active_filter_descriptions(vpc_id="vpc-1", enterprise_project_id="0"),
            ["id=vpc-1", "enterprise_project_id=0"])
        self.assertEqual(active_filter_descriptions(), [])


class TestRenderMarkdown(unittest.TestCase):
    def test_headers_and_rows(self):
        text = render_markdown([VPC_1], region="cn-north-4")
        header = "| " + " | ".join(MD_HEADERS) + " |"
        self.assertIn(header, text)
        self.assertIn("| vpc-demo-01 | vpc-0001 | cn-north-4 | 192.168.0.0/16 | OK | 0 | demo vpc | 2024-01-01T00:00:00 |",
                      text)

    def test_name_column_present(self):
        self.assertEqual(MD_HEADERS[0], "VPC 名称")

    def test_missing_fields_render_dash(self):
        text = render_markdown([{"id": "vpc-x"}], region="cn-north-4")
        self.assertIn("| - | vpc-x | cn-north-4 | - | - | - | - | - |", text)

    def test_empty_list_renders_header_only_table(self):
        text = render_markdown([], region="cn-north-4")
        self.assertIn("| " + " | ".join(MD_HEADERS) + " |", text)
        self.assertEqual(len([ln for ln in text.splitlines() if ln.strip()]), 2)

    def test_summary_line(self):
        text = render_markdown([VPC_1], summary=True, region="cn-north-4")
        self.assertIn("**汇总**：共 1 个 VPC（Region cn-north-4）。", text)
        self.assertNotIn("汇总", render_markdown([], summary=False))

    def test_pipe_in_value_escaped(self):
        text = render_markdown([{"name": "a|b"}])
        self.assertIn("a\\|b", text)


class TestExportMarkdown(unittest.TestCase):
    def test_export_writes_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "vpc.md")
            written = export_markdown([VPC_1], path, summary=True, region="cn-north-4")
            self.assertEqual(written, os.path.abspath(path))
            with open(path, encoding="utf-8") as fh:
                content = fh.read()
            self.assertIn("| VPC 名称 | VPC ID | 区域 | 网段 | 状态 | 企业项目 ID | 描述 | 创建时间 |", content)
            self.assertIn("vpc-demo-01", content)
            self.assertIn("汇总", content)

    def test_export_empty_list_writes_empty_table(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "empty.md")
            export_markdown([], path, region="cn-north-4")
            self.assertTrue(os.path.isfile(path))
            with open(path, encoding="utf-8") as fh:
                content = fh.read()
            self.assertIn("| VPC 名称 |", content)
            self.assertEqual(len(content.strip().splitlines()), 2)

    def test_export_creates_missing_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "nested", "dir", "vpc.md")
            export_markdown([VPC_1], path)
            self.assertTrue(os.path.isfile(path))

    def test_export_bad_path_raises_and_leaves_no_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            blocker = os.path.join(tmp, "blocker")
            with open(blocker, "w") as fh:
                fh.write("x")
            bad = os.path.join(blocker, "sub", "vpc.md")
            with self.assertRaises(ExportError):
                export_markdown([VPC_1], bad)
            self.assertFalse(os.path.exists(bad))

    def test_default_output_path_format(self):
        path = default_output_path("cn-north-4")
        self.assertTrue(re.match(r"vpc_list_cn-north-4_\d{8}_\d{6}\.md$", path))


class TestMain(unittest.TestCase):
    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("export_vpc_markdown.subprocess.run", fake), \
                mock.patch.dict(os.environ, {"VPC_EXPORT_MARKDOWN_HCLOUD_BIN": "/mock/hcloud"}), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            rc = main(argv)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    def _page(self, vpcs):
        return [(json.dumps({"vpcs": vpcs}), "", 0)]

    def test_md_output_writes_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "vpc.md")
            rc, stdout, err = self._run(
                ["--region", "cn-north-4", "--output", out, "--summary"],
                self._page([VPC_1, VPC_2]))
            self.assertEqual(rc, 0)
            self.assertTrue(os.path.isfile(out))
            with open(out, encoding="utf-8") as fh:
                self.assertIn("VPC 名称", fh.read())
            self.assertIn("vpc.md", stdout)
            self.assertEqual(err, "")

    def test_empty_md_writes_empty_table(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "empty.md")
            rc, stdout, err = self._run(
                ["--region", "cn-north-4", "--output", out],
                self._page([]))
            self.assertEqual(rc, 0)
            self.assertTrue(os.path.isfile(out))
            self.assertIn("空表", stdout)
            with open(out, encoding="utf-8") as fh:
                self.assertIn("VPC 名称", fh.read())

    def test_default_md_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            old = os.getcwd()
            os.chdir(tmp)
            try:
                import export_vpc_markdown as mod
                with mock.patch.object(mod, "default_output_path",
                                       return_value=os.path.join(tmp, "default.md")):
                    fake = FakeRunner(self._page([VPC_1]))
                    with mock.patch("export_vpc_markdown.subprocess.run", fake), \
                            mock.patch.dict(os.environ, {"VPC_EXPORT_MARKDOWN_HCLOUD_BIN": "/mock/hcloud"}), \
                            mock.patch("sys.stdout") as stdout:
                        rc = mod.main([])
                    out = "".join(c[0][0] for c in stdout.write.call_args_list)
                    self.assertEqual(rc, 0)
                    self.assertTrue(os.path.isfile(os.path.join(tmp, "default.md")))
            finally:
                os.chdir(old)

    def test_table_output(self):
        rc, out, err = self._run(["--format", "table"], self._page([VPC_1, VPC_2]))
        self.assertEqual(rc, 0)
        self.assertIn("虚拟私有云（VPC）列表", out)
        self.assertIn("vpc-demo-01", out)

    def test_empty_table_message_and_header(self):
        rc, out, _ = self._run(["--format", "table"], self._page([]))
        self.assertEqual(rc, 0)
        self.assertIn("无虚拟私有云（VPC）", out)
        self.assertIn("id", out)

    def test_json_output(self):
        rc, out, err = self._run(["--format", "json"], self._page([VPC_1]))
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out), [VPC_1])

    def test_empty_json_output(self):
        rc, out, err = self._run(["--format", "json"], self._page([]))
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out), [])

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
        rc, out, err = self._run(["--operation", "DeleteVpc"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)

    def test_write_flag_argv_blocked(self):
        rc, out, err = self._run(["--create-vpc"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)

    def test_page_size_out_of_range(self):
        rc, out, err = self._run(["--page-size", "5000"], [])
        self.assertEqual(rc, 1)
        self.assertIn("page-size", err)

    def test_hcloud_missing_falls_back_to_sdk(self):
        with mock.patch("export_vpc_markdown.list_vpcs_via_sdk",
                        return_value=[VPC_1]):
            rc, out, err = self._run(["--format", "table"], [FileNotFoundError()])
        self.assertEqual(rc, 0)
        self.assertIn("vpc-0001", out)

    def test_help_exits_zero(self):
        with mock.patch("sys.stdout"), self.assertRaises(SystemExit) as ctx:
            main(["--help"])
        self.assertEqual(ctx.exception.code, 0)


class TestErrorHierarchy(unittest.TestCase):
    def test_subclasses(self):
        for exc in (GuardError, ConfigError, AuthError, ApiError, ExportError):
            self.assertTrue(issubclass(exc, VpcExportError))


if __name__ == "__main__":
    unittest.main()