import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from list_gaussdb import (  # noqa: E402
    ALLOWED_OPERATION,
    ApiError,
    AuthError,
    ConfigError,
    GuardError,
    GaussdbListError,
    default_output_path,
    filter_by_status,
    guard_operation,
    guard_write_intent,
    list_instances,
    main,
    normalize_instance,
    render_markdown,
    render_table,
    write_markdown,
)

INSTANCE_1 = {
    "id": "gauss-0001",
    "name": "gauss-demo-01",
    "status": "ACTIVE",
    "datastore": {"type": "gaussdb-mysql", "version": "8.0",
                  "kernel_version": "3.2.0"},
    "flavor_ref": "gaussdb.mysql.xlarge.x86.4",
    "flavor_info": {"vcpus": 4, "ram": 16},
    "volume": {"type": "ULTRAHIGH", "size": 100},
    "private_ips": ["192.168.0.10"],
    "public_ips": ["1.2.3.4"],
    "port": 3306,
    "type": "Cluster",
    "vpc_id": "vpc-1",
    "subnet_id": "subnet-1",
    "created": "2026-01-01T00:00:00Z",
}
INSTANCE_2 = {
    "id": "gauss-0002",
    "name": "gauss-demo-02",
    "status": "FAILED",
    "datastore": {"type": "gaussdb-mysql", "version": "8.0"},
    "flavor_ref": "gaussdb.mysql.large.x86.2",
    "flavor_info": {"vcpus": 2, "ram": 8},
    "volume": {"type": "COMMON", "size": 40},
    "private_ips": ["192.168.0.11", "192.168.0.12"],
    "public_ips": [],
    "port": 3306,
    "type": "Cluster",
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


class TestGuard(unittest.TestCase):
    def test_read_only_operation_allowed(self):
        self.assertTrue(guard_operation(ALLOWED_OPERATION))

    def test_non_list_operation_blocked(self):
        with self.assertRaises(GuardError):
            guard_operation("DeleteGaussMySqlInstance")

    def test_write_intent_blocked(self):
        for text in ("create instance", "delete gaussdb", "restart gauss-01",
                     "resize flavor", "update spec"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_read_only_filter_values_pass(self):
        self.assertFalse(guard_write_intent("--status ACTIVE"))
        self.assertFalse(guard_write_intent("--datastore-type gaussdb-mysql"))


class TestNormalizeAndRender(unittest.TestCase):
    def test_normalize_flattens_nested_fields(self):
        flat = normalize_instance(INSTANCE_1)
        self.assertEqual(flat["engine_type"], "gaussdb-mysql")
        self.assertEqual(flat["engine_version"], "8.0")
        self.assertEqual(flat["kernel_version"], "3.2.0")
        self.assertEqual(flat["cpu_mem"], "4C16GB")
        self.assertEqual(flat["volume_type"], "ULTRAHIGH")
        self.assertEqual(flat["volume_size"], 100)
        self.assertEqual(flat["private_ips"], "192.168.0.10")
        self.assertEqual(flat["public_ips"], "1.2.3.4")

    def test_normalize_missing_fields_dash(self):
        flat = normalize_instance({"id": "gauss-x"})
        self.assertEqual(flat["private_ips"], "-")
        self.assertEqual(flat["public_ips"], "-")
        self.assertEqual(flat["cpu_mem"], "-")

    def test_table_contains_basic_info(self):
        table = render_table([INSTANCE_1, INSTANCE_2])
        for fragment in ("gauss-demo-01", "gauss-0001", "ACTIVE",
                         "gaussdb-mysql", "192.168.0.10", "gauss-demo-02"):
            self.assertIn(fragment, table)


class TestMarkdownRender(unittest.TestCase):
    def test_document_has_title_header_separator_and_rows(self):
        doc = render_markdown([INSTANCE_1, INSTANCE_2], "cn-north-4")
        self.assertIn("# 华为云 GaussDB 实例列表", doc)
        self.assertIn("cn-north-4", doc)
        for label in ("名称", "实例ID", "状态", "引擎", "引擎版本", "规格",
                      "CPU/内存", "存储类型", "存储(GB)", "私网IP", "公网IP",
                      "端口", "类型", "区域", "VPC", "子网", "创建时间"):
            self.assertIn(label, doc)
        lines = doc.splitlines()
        header = next(i for i, line in enumerate(lines)
                      if line.startswith("| 名称 |"))
        self.assertTrue(lines[header + 1].startswith("| --- | --- |"))
        row_lines = [line for line in lines[header + 2:] if line.startswith("| ")]
        self.assertEqual(len(row_lines), 2)
        for fragment in ("gauss-0001", "gauss-demo-01", "ACTIVE",
                         "gaussdb-mysql", "4C16GB", "ULTRAHIGH",
                         "192.168.0.10", "1.2.3.4", "gauss-demo-02"):
            self.assertIn(fragment, doc)

    def test_region_cell_falls_back_to_queried_region(self):
        doc = render_markdown([{"id": "gauss-x", "name": "gauss-x"}], "cn-south-1")
        self.assertIn("| gauss-x | gauss-x |", doc)
        self.assertIn("| cn-south-1 |", doc)

    def test_region_cell_uses_instance_value_when_present(self):
        doc = render_markdown([dict(INSTANCE_1, region="cn-east-3")], "cn-north-4")
        self.assertIn("| cn-east-3 |", doc)

    def test_cell_escapes_pipe_and_collapses_newlines(self):
        instance = {"id": "gauss|1", "name": "demo\n02",
                    "status": "ACTIVE\r\nOK",
                    "datastore": {"type": "mysql|type"}}
        doc = render_markdown([instance], "cn-north-4")
        self.assertIn(r"gauss\|1", doc)
        self.assertIn("demo 02", doc)
        self.assertIn("ACTIVE OK", doc)
        self.assertIn(r"mysql\|type", doc)

    def test_empty_result_has_header_and_explicit_note(self):
        doc = render_markdown([], "cn-south-1")
        self.assertIn("| 名称 |", doc)
        self.assertIn("| --- |", doc)
        self.assertIn("无 GaussDB 实例", doc)
        self.assertIn("cn-south-1", doc)
        self.assertEqual(doc.count("| 名称 |"), 1)

    def test_generated_at_line_included_when_provided(self):
        doc = render_markdown([INSTANCE_1], "cn-north-4", "2026-01-02T03:04:05Z")
        self.assertIn("Generated at: 2026-01-02T03:04:05Z", doc)


class TestDefaultOutputPath(unittest.TestCase):
    def test_default_name_contains_region_and_timestamp(self):
        path = default_output_path("cn-south-1")
        name = os.path.basename(path)
        self.assertTrue(name.startswith("gaussdb_instances_cn-south-1_"))
        self.assertTrue(name.endswith(".md"))


class TestWriteMarkdown(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmpdir, True)

    def test_atomic_write_and_no_leftover_temp(self):
        out_path = os.path.join(self.tmpdir, "atomic.md")
        write_markdown("hello", out_path)
        with open(out_path, encoding="utf-8") as handle:
            self.assertEqual(handle.read(), "hello")
        self.assertEqual([n for n in os.listdir(self.tmpdir)
                          if n.startswith(".gaussdb-md-")], [])

    def test_creates_parent_directories(self):
        out_path = os.path.join(self.tmpdir, "a", "b", "x.md")
        write_markdown("x", out_path)
        self.assertTrue(os.path.isfile(out_path))


class TestMainTableAndJson(unittest.TestCase):
    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("list_gaussdb.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            try:
                rc = main(argv)
            except SystemExit as exc:
                rc = exc.code
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    @staticmethod
    def _payload(instances=None):
        instances = [INSTANCE_1, INSTANCE_2] if instances is None else instances
        return (json.dumps({"instances": instances,
                            "total_count": len(instances)}), "", 0)

    def test_default_table_output_unchanged(self):
        rc, out, err = self._run(["--region", "cn-north-4"], [self._payload()])
        self.assertEqual(rc, 0)
        self.assertIn("GaussDB 实例列表（共 2 个）", out)
        self.assertIn("gauss-demo-01", out)
        self.assertIn("ACTIVE", out)
        self.assertEqual(err, "")

    def test_explicit_table_format_matches_default(self):
        rc, out, _ = self._run(["--format", "table"], [self._payload()])
        self.assertEqual(rc, 0)
        self.assertIn("GaussDB 实例列表（共 2 个）", out)

    def test_table_flag_unchanged(self):
        rc, out, _ = self._run(["--table"], [self._payload()])
        self.assertEqual(rc, 0)
        self.assertIn("GaussDB 实例列表（共 2 个）", out)

    def test_json_output_unchanged(self):
        rc, out, err = self._run(["--json"], [self._payload()])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out), [INSTANCE_1, INSTANCE_2])
        self.assertEqual(err, "")

    def test_empty_table_message(self):
        rc, out, _ = self._run(["--region", "cn-south-1"], [self._payload([])])
        self.assertEqual(rc, 0)
        self.assertIn("无 GaussDB 实例", out)
        self.assertIn("cn-south-1", out)

    def test_status_filter_client_side(self):
        rc, out, _ = self._run(["--status", "ACTIVE"], [self._payload()])
        self.assertEqual(rc, 0)
        self.assertIn("gauss-demo-01", out)
        self.assertNotIn("gauss-demo-02", out)

    def test_write_intent_blocked(self):
        rc, out, err = self._run(
            ["--operation", "DeleteGaussMySqlInstance"], [])
        self.assertEqual(rc, 1)
        self.assertIn("不允许的操作", err)

    def test_read_only_filter_value_not_blocked(self):
        # Filter values are caller data, not operations (existing behaviour):
        # a status value such as CREATING must not trip the guard.
        rc, out, err = self._run(
            ["--status", "CREATING"], [self._payload([])])
        self.assertEqual(rc, 0)
        self.assertNotIn("写操作意图", err)


class TestMarkdownExportMain(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmpdir, True)
        self._cwd = os.getcwd()

    def tearDown(self):
        os.chdir(self._cwd)

    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("list_gaussdb.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            try:
                rc = main(argv)
            except SystemExit as exc:
                rc = exc.code
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    @staticmethod
    def _payload(instances=None):
        instances = [INSTANCE_1, INSTANCE_2] if instances is None else instances
        return (json.dumps({"instances": instances,
                            "total_count": len(instances)}), "", 0)

    def test_format_md_writes_file(self):
        out_path = os.path.join(self.tmpdir, "gaussdb.md")
        rc, out, err = self._run(["--format", "md", "--output", out_path],
                                 [self._payload()])
        self.assertEqual(rc, 0)
        self.assertEqual(err, "")
        self.assertIn("已生成 Markdown 文件", out)
        self.assertIn(os.path.abspath(out_path), out)
        with open(out_path, encoding="utf-8") as handle:
            content = handle.read()
        self.assertIn("# 华为云 GaussDB 实例列表", content)
        self.assertIn("| 名称 |", content)
        self.assertIn("gauss-demo-01", content)
        self.assertIn("gauss-demo-02", content)
        self.assertEqual([n for n in os.listdir(self.tmpdir)
                          if n.startswith(".gaussdb-md-")], [])

    def test_output_implies_md_format(self):
        out_path = os.path.join(self.tmpdir, "implied.md")
        rc, out, _ = self._run(["--output", out_path], [self._payload()])
        self.assertEqual(rc, 0)
        self.assertTrue(os.path.isfile(out_path))

    def test_short_output_flag_works(self):
        out_path = os.path.join(self.tmpdir, "short.md")
        rc, _, _ = self._run(["-o", out_path], [self._payload()])
        self.assertEqual(rc, 0)
        self.assertTrue(os.path.isfile(out_path))

    def test_relative_output_creates_parent_directories(self):
        os.chdir(self.tmpdir)
        rc, out, _ = self._run(
            ["--format", "md", "--output", "reports/2026/gaussdb.md"],
            [self._payload()])
        self.assertEqual(rc, 0)
        self.assertTrue(os.path.isfile(
            os.path.join(self.tmpdir, "reports", "2026", "gaussdb.md")))
        self.assertIn("reports/2026/gaussdb.md", out)

    def test_default_filename_uses_region_and_timestamp(self):
        os.chdir(self.tmpdir)
        rc, out, _ = self._run(
            ["--format", "md", "--region", "cn-south-1"], [self._payload()])
        self.assertEqual(rc, 0)
        files = os.listdir(self.tmpdir)
        self.assertEqual(len(files), 1)
        self.assertTrue(files[0].startswith("gaussdb_instances_cn-south-1_"))
        self.assertTrue(files[0].endswith(".md"))

    def test_empty_result_writes_table_and_note_exit_zero(self):
        out_path = os.path.join(self.tmpdir, "empty.md")
        rc, out, err = self._run(
            ["--format", "md", "--output", out_path], [self._payload([])])
        self.assertEqual(rc, 0)
        self.assertEqual(err, "")
        self.assertIn("无 GaussDB 实例", out)
        with open(out_path, encoding="utf-8") as handle:
            content = handle.read()
        self.assertIn("| 名称 |", content)
        self.assertIn("无 GaussDB 实例", content)

    def test_write_failure_reports_error_nonzero_and_no_partial_file(self):
        out_path = os.path.join(self.tmpdir, "broken.md")
        with mock.patch("list_gaussdb.os.replace", side_effect=OSError("disk full")):
            rc, out, err = self._run(
                ["--format", "md", "--output", out_path], [self._payload()])
        self.assertEqual(rc, 1)
        self.assertIn("[错误]", err)
        self.assertIn("Markdown 文件写出失败", err)
        self.assertFalse(os.path.exists(out_path))
        self.assertEqual([n for n in os.listdir(self.tmpdir)
                          if n.startswith(".gaussdb-md-")], [])

    def test_uncreatable_parent_directory_reports_error(self):
        blocker = os.path.join(self.tmpdir, "blocker")
        with open(blocker, "w", encoding="utf-8") as handle:
            handle.write("x")
        out_path = os.path.join(blocker, "gaussdb.md")
        rc, out, err = self._run(
            ["--format", "md", "--output", out_path], [self._payload()])
        self.assertEqual(rc, 1)
        self.assertIn("Markdown 文件写出失败", err)

    def test_md_mutually_exclusive_with_json(self):
        rc, out, err = self._run(["--format", "md", "--json"], [])
        self.assertEqual(rc, 2)
        self.assertIn("不能同时使用", err)

    def test_output_mutually_exclusive_with_json(self):
        rc, out, err = self._run(
            ["--output", os.path.join(self.tmpdir, "x.md"), "--json"], [])
        self.assertEqual(rc, 2)
        self.assertIn("不能同时使用", err)

    def test_md_mutually_exclusive_with_table_flag(self):
        rc, out, err = self._run(["--format", "md", "--table"], [])
        self.assertEqual(rc, 2)
        self.assertIn("不能同时使用", err)

    def test_output_path_with_mutating_word_is_allowed(self):
        out_path = os.path.join(self.tmpdir, "update-reports", "gaussdb.md")
        rc, out, err = self._run(["--output", out_path], [self._payload()])
        self.assertEqual(rc, 0)
        self.assertEqual(err, "")
        self.assertTrue(os.path.isfile(out_path))


class TestListInstances(unittest.TestCase):
    def test_single_page(self):
        fake = FakeRunner([(json.dumps({"instances": [INSTANCE_1, INSTANCE_2],
                                        "total_count": 2}), "", 0)])
        with mock.patch("list_gaussdb.subprocess.run", fake):
            instances = list_instances("cn-north-4")
        self.assertEqual(instances, [INSTANCE_1, INSTANCE_2])
        self.assertEqual(len(fake.calls), 1)

    def test_pagination_via_total(self):
        page1 = {"instances": [INSTANCE_1], "total_count": 2}
        page2 = {"instances": [INSTANCE_2], "total_count": 2}
        fake = FakeRunner([(json.dumps(page1), "", 0),
                           (json.dumps(page2), "", 0)])
        with mock.patch("list_gaussdb.subprocess.run", fake):
            instances = list_instances("cn-north-4", limit=1)
        self.assertEqual(instances, [INSTANCE_1, INSTANCE_2])
        self.assertIn("--offset=1", fake.calls[1])

    def test_empty_region(self):
        fake = FakeRunner([(json.dumps({"instances": [], "total_count": 0}),
                            "", 0)])
        with mock.patch("list_gaussdb.subprocess.run", fake):
            self.assertEqual(list_instances("cn-north-4"), [])

    def test_auth_error(self):
        fake = FakeRunner([("", "403 Forbidden", 1)])
        with mock.patch("list_gaussdb.subprocess.run", fake):
            with self.assertRaises(AuthError):
                list_instances("cn-north-4")

    def test_missing_credentials(self):
        fake = FakeRunner([("", "ERROR: cli-ak is empty", 1)])
        with mock.patch("list_gaussdb.subprocess.run", fake):
            with self.assertRaises(ConfigError):
                list_instances("cn-north-4")

    def test_sdk_fallback_when_hcloud_missing(self):
        with mock.patch("list_gaussdb.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_gaussdb.list_instances_via_sdk",
                           return_value=[INSTANCE_1]) as sdk_mock:
            instances = list_instances("cn-north-4")
        self.assertEqual(instances, [INSTANCE_1])
        self.assertTrue(sdk_mock.called)


class TestFilterByStatus(unittest.TestCase):
    def test_no_status_returns_all(self):
        self.assertEqual(filter_by_status([INSTANCE_1, INSTANCE_2], None),
                         [INSTANCE_1, INSTANCE_2])

    def test_exact_and_case_insensitive(self):
        self.assertEqual(filter_by_status([INSTANCE_1, INSTANCE_2], "ACTIVE"),
                         [INSTANCE_1])
        self.assertEqual(filter_by_status([INSTANCE_1], "active"), [INSTANCE_1])

    def test_no_match_returns_empty(self):
        self.assertEqual(filter_by_status([INSTANCE_1, INSTANCE_2], "BUILDING"), [])


class TestErrorHierarchy(unittest.TestCase):
    def test_subclasses(self):
        for exc in (GuardError, ConfigError, AuthError, ApiError):
            self.assertTrue(issubclass(exc, GaussdbListError))


if __name__ == "__main__":
    unittest.main()