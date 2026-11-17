import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from list_sfs_export_markdown import (  # noqa: E402
    ALLOWED_OPERATION,
    ApiError,
    AuthError,
    ConfigError,
    GuardError,
    SfsExportError,
    active_filter_descriptions,
    build_command,
    classify_hcloud_failure,
    clamp_page_size,
    extract_json,
    extract_shares,
    filter_shares,
    guard_operation,
    guard_write_intent,
    list_shares,
    list_shares_via_sdk,
    main,
    normalize_share,
    render_markdown,
    scrub_read_only_values,
    share_names,
    write_markdown,
)

SHARE_1 = {
    "id": "sfs-0001",
    "name": "sfs-demo-01",
    "status": "available",
    "share_proto": "NFS",
    "size": 500,
    "availability_zone": "cn-north-4a",
    "share_type": "STANDARD",
    "created_at": "2026-01-02T03:04:05+0800",
}
SHARE_2 = {
    "id": "sfs-0002",
    "name": "sfs-demo-02",
    "status": "creating",
    "share_proto": "CIFS",
    "size": 1000,
    "availability_zone": "cn-north-4b",
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
        self.assertFalse(guard_write_intent("--region cn-north-4 list shares"))
        self.assertFalse(guard_write_intent("show file system details"))

    def test_create_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("CreateShare sfs-new")

    def test_delete_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--operation DeleteShare")

    def test_mutating_verbs_blocked(self):
        for text in ("expand share", "shrink sfs-01", "resize share",
                     "mount share", "unmount share", "restore backup",
                     "detach target"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_normalized_separators_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--create-share")
        with self.assertRaises(GuardError):
            guard_write_intent("expand_share_size")

    def test_operation_guard_rejects_non_list(self):
        with self.assertRaises(GuardError):
            guard_operation("ShowShare")
        self.assertTrue(guard_operation(ALLOWED_OPERATION))

    def test_scrub_drops_output_path_value(self):
        # A local path containing a mutating word must not trip the guard.
        argv = ["--output", "downloads/update-report.md", "--region", "cn-north-4"]
        self.assertNotIn("update-report", scrub_read_only_values(argv))
        self.assertFalse(guard_write_intent(scrub_read_only_values(argv)))

    def test_scrub_drops_name_status_values(self):
        argv = ["--name", "delete-test", "--status", "deleting"]
        self.assertFalse(guard_write_intent(scrub_read_only_values(argv)))

    def test_scrub_drops_id_proto_and_az_values(self):
        argv = ["--id", "delete-0001", "--share-proto", "NFS",
                "--az", "expand-zone-a"]
        scrubbed = scrub_read_only_values(argv)
        self.assertNotIn("delete-0001", scrubbed)
        self.assertNotIn("expand-zone-a", scrubbed)
        self.assertFalse(guard_write_intent(scrubbed))

    def test_scrub_drops_flag_equals_value_pairs(self):
        argv = ["--output=/tmp/expand-report.md", "--region=cn-north-4"]
        self.assertNotIn("expand-report", scrub_read_only_values(argv))
        self.assertFalse(guard_write_intent(scrub_read_only_values(argv)))

    def test_scrub_keeps_flag_itself_and_operation(self):
        argv = ["--operation", "DeleteShare"]
        self.assertIn("DeleteShare", scrub_read_only_values(argv))


class TestClampPageSize(unittest.TestCase):
    def test_clamps_high(self):
        self.assertEqual(clamp_page_size(5000), 200)

    def test_clamps_low(self):
        self.assertEqual(clamp_page_size(0), 1)
        self.assertEqual(clamp_page_size(-3), 1)

    def test_non_numeric_falls_back(self):
        self.assertEqual(clamp_page_size("abc"), 200)

    def test_valid_passthrough(self):
        self.assertEqual(clamp_page_size(100), 100)


class TestBuildCommand(unittest.TestCase):
    def test_basic(self):
        argv = build_command("cn-north-4")
        self.assertEqual(argv[0], "SFSTurbo")
        self.assertEqual(argv[1], "ListShares")
        self.assertIn("--cli-region=cn-north-4", argv)
        self.assertIn("--limit=200", argv)
        self.assertIn("--offset=0", argv)

    def test_paging_params(self):
        argv = build_command("cn-south-1", limit=10, offset=20)
        self.assertIn("--limit=10", argv)
        self.assertIn("--offset=20", argv)

    def test_no_filter_or_write_flags_ever_added(self):
        argv = build_command("cn-north-4")
        for flag in argv:
            self.assertFalse(flag.startswith("--status"))
            self.assertFalse(flag.startswith("--name"))
            self.assertFalse(flag.lower().lstrip("-").startswith(
                ("create", "delete", "update", "expand")))


class TestExtract(unittest.TestCase):
    def test_extract_json_plain(self):
        data = extract_json(json.dumps({"shares": []}))
        self.assertEqual(data, {"shares": []})

    def test_extract_json_with_noise(self):
        data = extract_json("WARNING some noise\n{\"a\": 1}\n")
        self.assertEqual(data, {"a": 1})

    def test_extract_json_list_payload(self):
        data = extract_json("[{\"name\": \"a\"}]")
        self.assertEqual(data, [{"name": "a"}])

    def test_extract_json_invalid(self):
        with self.assertRaises(ApiError):
            extract_json("<html>not json</html>")

    def test_extract_shares_known_keys(self):
        for key in ("shares", "file_systems", "share_list"):
            self.assertEqual(extract_shares({key: [SHARE_1]}), [SHARE_1])
        self.assertEqual(extract_shares([SHARE_1]), [SHARE_1])
        self.assertEqual(extract_shares({"count": 0}), [])


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

    def test_auth_unauthorized(self):
        err = classify_hcloud_failure("", "Unauthorized: invalid AK", 1)
        self.assertIsInstance(err, AuthError)

    def test_generic_api_error(self):
        err = classify_hcloud_failure("", "boom", 2)
        self.assertIsInstance(err, ApiError)

    def test_use_error_marker_with_zero_rc(self):
        err = classify_hcloud_failure(
            "[USE_ERROR]limit invalid (max 200)\n\n"
            "Run `hcloud SFSTurbo ListShares --help` for details.", "", 0)
        self.assertIsInstance(err, ApiError)
        self.assertIn("参数错误", str(err))
        self.assertIn("--help", str(err))


class TestListShares(unittest.TestCase):
    def test_single_page(self):
        fake = FakeRunner([(
            json.dumps({"shares": [SHARE_1, SHARE_2], "count": 2}), "", 0)])
        with mock.patch("list_sfs_export_markdown.subprocess.run", fake):
            shares = list_shares("cn-north-4")
        self.assertEqual(shares, [SHARE_1, SHARE_2])
        self.assertEqual(len(fake.calls), 1)

    def test_pagination_via_total(self):
        page1 = {"shares": [SHARE_1], "count": 2}
        page2 = {"shares": [SHARE_2], "count": 2}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("list_sfs_export_markdown.subprocess.run", fake):
            shares = list_shares("cn-north-4", limit=1)
        self.assertEqual(shares, [SHARE_1, SHARE_2])
        self.assertEqual(len(fake.calls), 2)
        self.assertIn("--offset=1", fake.calls[1])

    def test_pagination_via_full_page_without_total(self):
        page1 = {"shares": [SHARE_1]}
        page2 = {"shares": []}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("list_sfs_export_markdown.subprocess.run", fake):
            shares = list_shares("cn-north-4", limit=1)
        self.assertEqual(shares, [SHARE_1])

    def test_empty_region(self):
        fake = FakeRunner([(json.dumps({"shares": [], "count": 0}), "", 0)])
        with mock.patch("list_sfs_export_markdown.subprocess.run", fake):
            shares = list_shares("cn-north-4")
        self.assertEqual(shares, [])

    def test_status_filter_applied_client_side(self):
        fake = FakeRunner([(
            json.dumps({"shares": [SHARE_1, SHARE_2], "count": 2}), "", 0)])
        with mock.patch("list_sfs_export_markdown.subprocess.run", fake):
            shares = list_shares("cn-north-4", status="available")
        self.assertEqual(shares, [SHARE_1])
        for call in fake.calls:
            self.assertFalse(any("--status" in part for part in call))

    def test_status_filter_case_insensitive_and_empty(self):
        fake = FakeRunner([(
            json.dumps({"shares": [SHARE_1, SHARE_2], "count": 2}), "", 0)])
        with mock.patch("list_sfs_export_markdown.subprocess.run", fake):
            self.assertEqual(list_shares("cn-north-4", status="AVAILABLE"), [SHARE_1])
        fake = FakeRunner([(
            json.dumps({"shares": [SHARE_1, SHARE_2], "count": 2}), "", 0)])
        with mock.patch("list_sfs_export_markdown.subprocess.run", fake):
            self.assertEqual(list_shares("cn-north-4", status="error"), [])

    def test_use_error_rc0_raises_api_error(self):
        fake = FakeRunner([(
            "[USE_ERROR]limit invalid (max 200)\n\n"
            "Run `hcloud SFSTurbo ListShares --help` for details.", "", 0)])
        with mock.patch("list_sfs_export_markdown.subprocess.run", fake):
            with self.assertRaises(ApiError) as ctx:
                list_shares("cn-north-4")
        self.assertIn("参数错误", str(ctx.exception))

    def test_nonzero_exit_403(self):
        fake = FakeRunner([("", "403 Forbidden", 1)])
        with mock.patch("list_sfs_export_markdown.subprocess.run", fake):
            with self.assertRaises(AuthError):
                list_shares("cn-north-4")

    def test_nonzero_exit_credentials(self):
        fake = FakeRunner([("", "ERROR: no AK configured", 1)])
        with mock.patch("list_sfs_export_markdown.subprocess.run", fake):
            with self.assertRaises(ConfigError):
                list_shares("cn-north-4")

    def test_timeout(self):
        fake = FakeRunner([subprocess.TimeoutExpired(cmd="hcloud", timeout=120)])
        with mock.patch("list_sfs_export_markdown.subprocess.run", fake):
            with self.assertRaises(ApiError):
                list_shares("cn-north-4")

    def test_sdk_fallback_when_hcloud_missing(self):
        with mock.patch("list_sfs_export_markdown.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_sfs_export_markdown.list_shares_via_sdk",
                           return_value=[SHARE_1, SHARE_2]) as sdk_mock:
            shares = list_shares("cn-north-4", status="available")
        self.assertEqual(shares, [SHARE_1])
        # The SDK layer is queried for the full list; filtering stays client-side.
        self.assertEqual(sdk_mock.call_args.kwargs.get("status"), None)

    def test_sdk_fallback_unavailable_raises_config(self):
        with mock.patch("list_sfs_export_markdown.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_sfs_export_markdown.list_shares_via_sdk",
                           side_effect=ConfigError("huaweicloudsdksfsturbo 未安装")):
            with self.assertRaises(ConfigError):
                list_shares("cn-north-4")


class TestFilterShares(unittest.TestCase):
    def test_no_filter_returns_all(self):
        self.assertEqual(filter_shares([SHARE_1, SHARE_2]), [SHARE_1, SHARE_2])

    def test_name_substring_ci(self):
        self.assertEqual(filter_shares([SHARE_1, SHARE_2], name="DEMO-01"), [SHARE_1])

    def test_status_exact_ci(self):
        self.assertEqual(filter_shares([SHARE_1, SHARE_2], status="CREATING"), [SHARE_2])

    def test_id_substring_ci(self):
        self.assertEqual(filter_shares([SHARE_1, SHARE_2], share_id="SFS-0002"),
                         [SHARE_2])
        self.assertEqual(filter_shares([SHARE_1, SHARE_2], share_id="000"),
                         [SHARE_1, SHARE_2])

    def test_share_proto_exact_ci(self):
        self.assertEqual(filter_shares([SHARE_1, SHARE_2], share_proto="cifs"),
                         [SHARE_2])
        self.assertEqual(filter_shares([SHARE_1, SHARE_2], share_proto="NFS"),
                         [SHARE_1])
        self.assertEqual(filter_shares([SHARE_1, SHARE_2], share_proto="SMB"), [])

    def test_az_substring_ci(self):
        self.assertEqual(filter_shares([SHARE_1, SHARE_2], az="4A"), [SHARE_1])
        self.assertEqual(filter_shares([SHARE_1, SHARE_2], az="4b"), [SHARE_2])

    def test_az_filter_uses_az_name_fallback_key(self):
        shares = [{"id": "a", "az_name": "cn-south-1a"},
                  {"id": "b", "availability_zone": "cn-south-1b"}]
        self.assertEqual(filter_shares(shares, az="south-1a"), [shares[0]])

    def test_all_five_filters_combined(self):
        self.assertEqual(
            filter_shares([SHARE_1, SHARE_2], name="demo", share_id="0001",
                          status="available", share_proto="NFS",
                          az="north-4a"), [SHARE_1])
        self.assertEqual(
            filter_shares([SHARE_1, SHARE_2], name="demo", share_id="0001",
                          status="available", share_proto="CIFS"),
            [])

    def test_combined(self):
        self.assertEqual(filter_shares([SHARE_1, SHARE_2], name="sfs-demo",
                                       status="available"), [SHARE_1])

    def test_no_match_returns_empty(self):
        self.assertEqual(filter_shares([SHARE_1, SHARE_2], status="error"), [])

    def test_input_not_mutated(self):
        source = [SHARE_1, SHARE_2]
        filter_shares(source, name="sfs-demo-01")
        self.assertEqual(source, [SHARE_1, SHARE_2])


class TestActiveFilterDescriptions(unittest.TestCase):
    def test_empty_when_no_filter(self):
        self.assertEqual(active_filter_descriptions(), [])

    def test_all_filters_ordered(self):
        self.assertEqual(
            active_filter_descriptions(name="a", share_id="b", status="c",
                                       share_proto="d", az="e"),
            ["name=a", "id=b", "status=c", "share_proto=d", "az=e"])


class TestNormalize(unittest.TestCase):
    def test_normalize_keeps_availability_zone(self):
        flat = normalize_share(SHARE_1)
        self.assertEqual(flat["availability_zone"], "cn-north-4a")

    def test_normalize_az_fallback_key(self):
        flat = normalize_share({"id": "sfs-x", "az_name": "cn-south-1a"})
        self.assertEqual(flat["availability_zone"], "cn-south-1a")

    def test_normalize_missing_az_dash(self):
        flat = normalize_share({"id": "sfs-x"})
        self.assertEqual(flat["availability_zone"], "-")

    def test_names(self):
        self.assertEqual(share_names([SHARE_1, SHARE_2]),
                         ["sfs-demo-01", "sfs-demo-02"])

    def test_names_fallback_to_id(self):
        self.assertEqual(share_names([{"id": "sfs-9"}]), ["sfs-9"])


class TestRenderMarkdown(unittest.TestCase):
    def test_contains_title_header_and_rows(self):
        doc = render_markdown([SHARE_1, SHARE_2], "cn-north-4")
        self.assertIn("# Huawei Cloud SFS File Systems — cn-north-4", doc)
        self.assertIn(
            "| 文件系统名称 | 文件系统ID | 状态 | 协议 | 容量(GB) | "
            "可用区 | 类型 | 企业项目 | 创建时间 |", doc)
        for fragment in ("sfs-demo-01", "sfs-0001", "available", "NFS", "500",
                         "cn-north-4a", "STANDARD", "sfs-demo-02", "CIFS"):
            self.assertIn(fragment, doc)

    def test_row_count(self):
        doc = render_markdown([SHARE_1, SHARE_2], "cn-north-4")
        data_rows = [line for line in doc.splitlines() if line.startswith("| sfs-")]
        self.assertEqual(len(data_rows), 2)

    def test_empty_still_valid_with_note(self):
        doc = render_markdown([], "cn-south-1")
        self.assertIn("| 文件系统名称 |", doc)
        self.assertIn("| --- |", doc)
        self.assertIn("无 SFS 文件系统", doc)
        self.assertIn("cn-south-1", doc)
        self.assertIn("File systems: 0", doc)

    def test_missing_fields_render_dash(self):
        doc = render_markdown([{"id": "sfs-x", "name": "sfs-x"}], "cn-north-4")
        self.assertIn("| sfs-x | sfs-x | - |", doc)

    def test_pipe_and_newline_escaped(self):
        doc = render_markdown([{"name": "a|b", "id": "x\ny"}], "cn-north-4")
        self.assertIn("a\\|b", doc)
        self.assertIn("x y", doc)

    def test_meta_line_without_filters(self):
        doc = render_markdown([SHARE_1], "cn-north-4")
        self.assertIn(
            "> Region: cn-north-4 | File systems: 1 | 无过滤条件", doc)

    def test_meta_line_with_filters(self):
        doc = render_markdown(
            [SHARE_1], "cn-north-4",
            filters=["name=demo", "share_proto=NFS", "az=cn-north-4a"])
        self.assertIn(
            "> Region: cn-north-4 | File systems: 1 | "
            "过滤条件: name=demo, share_proto=NFS, az=cn-north-4a", doc)

    def test_filter_no_match_note(self):
        doc = render_markdown([], "cn-north-4", filters=["name=nope"],
                              total_before_filter=2)
        self.assertIn("当前过滤条件下无匹配的 SFS 文件系统", doc)
        self.assertIn("过滤条件：name=nope", doc)
        self.assertNotIn("当前区域（cn-north-4）无 SFS 文件系统", doc)
        self.assertIn("| 文件系统名称 |", doc)
        self.assertIn("File systems: 0", doc)

    def test_filter_with_empty_region_keeps_region_note(self):
        doc = render_markdown([], "cn-south-1", filters=["name=nope"],
                              total_before_filter=0)
        self.assertIn("当前区域（cn-south-1）无 SFS 文件系统", doc)


class TestWriteMarkdown(unittest.TestCase):
    def test_writes_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "out.md")
            write_markdown("# hello\n", path)
            with open(path, encoding="utf-8") as handle:
                self.assertEqual(handle.read(), "# hello\n")

    def test_creates_missing_dirs(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "nested", "dir", "out.md")
            write_markdown("content", path)
            self.assertTrue(os.path.isfile(path))

    def test_bad_path_raises_api_error(self):
        with self.assertRaises(ApiError):
            write_markdown("content", "\0bad\0path.md")


class TestMain(unittest.TestCase):
    def _run(self, argv, results, cwd=None):
        fake = FakeRunner(results)
        old = os.getcwd()
        if cwd:
            os.chdir(cwd)
        try:
            with mock.patch("list_sfs_export_markdown.subprocess.run", fake), \
                    mock.patch("sys.stdout") as stdout, \
                    mock.patch("sys.stderr") as stderr:
                rc = main(argv)
            out = "".join(c[0][0] for c in stdout.write.call_args_list)
            err = "".join(c[0][0] for c in stderr.write.call_args_list)
        finally:
            os.chdir(old)
        return rc, out, err

    def test_default_output_in_cwd(self):
        with tempfile.TemporaryDirectory() as tmp:
            rc, out, err = self._run(
                ["--region", "cn-north-4"],
                [(json.dumps({"shares": [SHARE_1, SHARE_2], "count": 2}), "", 0)],
                cwd=tmp)
            self.assertEqual(rc, 0)
            path = os.path.join(tmp, "sfs_share_list.md")
            self.assertTrue(os.path.isfile(path))
            with open(path, encoding="utf-8") as handle:
                content = handle.read()
            self.assertIn("sfs-demo-01", content)
            self.assertIn(os.path.abspath(path), out)
            self.assertEqual(err, "")

    def test_explicit_output_and_stdout(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "report.md")
            rc, out, err = self._run(
                ["--region", "cn-north-4", "--output", path, "--stdout"],
                [(json.dumps({"shares": [SHARE_1], "count": 1}), "", 0)])
            self.assertEqual(rc, 0)
            self.assertTrue(os.path.isfile(path))
            self.assertIn("| 文件系统名称 |", out)

    def test_empty_result_writes_file_exit_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "empty.md")
            rc, out, err = self._run(
                ["--region", "cn-south-1", "--output", path],
                [(json.dumps({"shares": [], "count": 0}), "", 0)])
            self.assertEqual(rc, 0)
            self.assertTrue(os.path.isfile(path))
            with open(path, encoding="utf-8") as handle:
                content = handle.read()
            self.assertIn("无 SFS 文件系统", content)
            self.assertIn("cn-south-1", out)
            self.assertEqual(err, "")

    def test_name_filter_main_client_side(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "f.md")
            fake = FakeRunner([(
                json.dumps({"shares": [SHARE_1, SHARE_2], "count": 2}), "", 0)])
            with mock.patch("list_sfs_export_markdown.subprocess.run", fake), \
                    mock.patch("sys.stdout"):
                rc = main(["--name", "sfs-demo-01", "--output", path])
            self.assertEqual(rc, 0)
            with open(path, encoding="utf-8") as handle:
                content = handle.read()
            self.assertIn("sfs-demo-01", content)
            self.assertNotIn("sfs-demo-02", content)
            for call in fake.calls:
                self.assertFalse(any("--name" in part for part in call))

    def test_status_filter_main_client_side(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "s.md")
            fake = FakeRunner([(
                json.dumps({"shares": [SHARE_1, SHARE_2], "count": 2}), "", 0)])
            with mock.patch("list_sfs_export_markdown.subprocess.run", fake), \
                    mock.patch("sys.stdout"):
                rc = main(["--status", "available", "--output", path])
            self.assertEqual(rc, 0)
            with open(path, encoding="utf-8") as handle:
                content = handle.read()
            self.assertIn("sfs-demo-01", content)
            self.assertNotIn("sfs-demo-02", content)

    def test_id_filter_main_client_side(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "i.md")
            fake = FakeRunner([(
                json.dumps({"shares": [SHARE_1, SHARE_2], "count": 2}), "", 0)])
            with mock.patch("list_sfs_export_markdown.subprocess.run", fake), \
                    mock.patch("sys.stdout"):
                rc = main(["--id", "0002", "--output", path])
            self.assertEqual(rc, 0)
            with open(path, encoding="utf-8") as handle:
                content = handle.read()
            self.assertIn("sfs-demo-02", content)
            self.assertNotIn("sfs-demo-01", content)
            self.assertIn("过滤条件: id=0002", content)
            for call in fake.calls:
                self.assertFalse(any("--id" in part for part in call))

    def test_share_proto_filter_main_client_side(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "p.md")
            fake = FakeRunner([(
                json.dumps({"shares": [SHARE_1, SHARE_2], "count": 2}), "", 0)])
            with mock.patch("list_sfs_export_markdown.subprocess.run", fake), \
                    mock.patch("sys.stdout"):
                rc = main(["--share-proto", "CIFS", "--output", path])
            self.assertEqual(rc, 0)
            with open(path, encoding="utf-8") as handle:
                content = handle.read()
            self.assertIn("sfs-demo-02", content)
            self.assertNotIn("sfs-demo-01", content)
            for call in fake.calls:
                self.assertFalse(any("--share-proto" in part for part in call))

    def test_az_filter_main_client_side(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "az.md")
            fake = FakeRunner([(
                json.dumps({"shares": [SHARE_1, SHARE_2], "count": 2}), "", 0)])
            with mock.patch("list_sfs_export_markdown.subprocess.run", fake), \
                    mock.patch("sys.stdout"):
                rc = main(["--az", "cn-north-4A", "--output", path])
            self.assertEqual(rc, 0)
            with open(path, encoding="utf-8") as handle:
                content = handle.read()
            self.assertIn("sfs-demo-01", content)
            self.assertNotIn("sfs-demo-02", content)

    def test_filter_no_match_writes_file_exit_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "nomatch.md")
            rc, out, err = self._run(
                ["--region", "cn-north-4", "--name", "nope", "--output", path],
                [(json.dumps({"shares": [SHARE_1, SHARE_2], "count": 2}), "", 0)])
            self.assertEqual(rc, 0)
            self.assertEqual(err, "")
            self.assertTrue(os.path.isfile(path))
            with open(path, encoding="utf-8") as handle:
                content = handle.read()
            self.assertIn("当前过滤条件下无匹配的 SFS 文件系统", content)
            self.assertIn("过滤条件：name=nope", content)
            self.assertIn("File systems: 0 | 过滤条件: name=nope", content)
            self.assertNotIn("当前区域（cn-north-4）无 SFS 文件系统", content)
            self.assertIn("当前过滤条件下无匹配的 SFS 文件系统", out)

    def test_empty_region_with_filter_keeps_region_wording(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "empty.md")
            rc, out, err = self._run(
                ["--region", "cn-south-1", "--name", "nope",
                 "--output", path],
                [(json.dumps({"shares": [], "count": 0}), "", 0)])
            self.assertEqual(rc, 0)
            with open(path, encoding="utf-8") as handle:
                content = handle.read()
            self.assertIn("当前区域（cn-south-1）无 SFS 文件系统", content)
            self.assertNotIn("当前过滤条件下无匹配", content)

    def test_auth_error_message(self):
        with tempfile.TemporaryDirectory() as tmp:
            rc, out, err = self._run(
                ["--output", os.path.join(tmp, "x.md")], [("", "403 Forbidden", 1)])
            self.assertEqual(rc, 1)
            self.assertIn("[错误]", err)
            self.assertIn("IAM", err)
            self.assertFalse(os.path.exists(os.path.join(tmp, "x.md")))

    def test_missing_ak_sk_error_message(self):
        with tempfile.TemporaryDirectory() as tmp:
            rc, out, err = self._run(
                ["--output", os.path.join(tmp, "x.md")], [("", "ERROR: cli-ak empty", 1)])
            self.assertEqual(rc, 1)
            self.assertIn("AK/SK", err)

    def test_hcloud_not_installed(self):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch("list_sfs_export_markdown.list_shares_via_sdk",
                            side_effect=ConfigError("huaweicloudsdksfsturbo 未安装")):
                rc, out, err = self._run(
                    ["--output", os.path.join(tmp, "x.md")], [FileNotFoundError()])
            self.assertEqual(rc, 1)
            self.assertIn("未安装", err)

    def test_hcloud_missing_falls_back_to_sdk(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "s.md")
            with mock.patch("list_sfs_export_markdown.list_shares_via_sdk",
                            return_value=[SHARE_1]):
                rc, out, err = self._run(["--output", path], [FileNotFoundError()])
            self.assertEqual(rc, 0)
            self.assertTrue(os.path.isfile(path))
            with open(path, encoding="utf-8") as handle:
                self.assertIn("sfs-demo-01", handle.read())

    def test_write_intent_argv_blocked(self):
        rc, out, err = self._run(["--operation", "DeleteShare"], [])
        self.assertEqual(rc, 1)
        self.assertIn("守卫拦截", err)

    def test_output_path_with_mutating_word_allowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "expand-report.md")
            rc, out, err = self._run(
                ["--output", path],
                [(json.dumps({"shares": [SHARE_1], "count": 1}), "", 0)])
            self.assertEqual(rc, 0)
            self.assertTrue(os.path.isfile(path))


class TestSdkFallback(unittest.TestCase):
    """The SDK fallback must use modules that exist in the official packages
    and wire credentials from environment variables (BasicCredentials has no
    env auto-discovery)."""

    def setUp(self):
        self._captured_credentials = None
        self._captured_region = None
        self._fake_client = mock.Mock()
        try:
            import huaweicloudsdksfsturbo.v1 as sfs_v1
        except ImportError:
            self.skipTest("huaweicloudsdksfsturbo not installed")
        self._builder_patch = mock.patch.object(
            sfs_v1.SFSTurboClient, "new_builder",
            classmethod(lambda cls: _FakeSdkBuilder(self)))
        self._builder_patch.start()
        self.addCleanup(self._builder_patch.stop)

    def _clean_credential_env(self):
        credential_vars = (
            "HW_ACCESS_KEY", "HUAWEI_ACCESS_KEY", "HUAWEICLOUD_SDK_AK",
            "HUAWEI_CLOUD_ACCESS_KEY", "HW_SECRET_KEY", "HUAWEI_SECRET_KEY",
            "HUAWEICLOUD_SDK_SK", "HUAWEI_CLOUD_SECRET_KEY",
        )
        return {name: "" for name in credential_vars}

    def test_official_sdk_imports_resolve(self):
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdksfsturbo.v1 import SFSTurboClient, ListSharesRequest
        from huaweicloudsdksfsturbo.v1.region.sfsturbo_region import SFSTurboRegion
        for obj in (BasicCredentials, Region, HttpConfig,
                    SFSTurboClient, ListSharesRequest, SFSTurboRegion):
            self.assertTrue(callable(obj), obj)

    def test_sdk_fallback_returns_shares_with_env_credentials(self):
        self._fake_client.list_shares.return_value = _FakeSdkResponse(
            [_FakeSdkShare(SHARE_1), _FakeSdkShare(SHARE_2)], 2)
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak",
                   HUAWEI_SECRET_KEY="test-sk")
        with mock.patch.dict(os.environ, env, clear=True):
            shares = list_shares_via_sdk("cn-north-4")
        self.assertEqual(len(shares), 2)
        self.assertEqual(shares[0]["name"], "sfs-demo-01")
        credentials = self._captured_credentials
        self.assertIsNotNone(credentials)
        self.assertEqual(getattr(credentials, "ak", None), "test-ak")
        self.assertEqual(getattr(credentials, "sk", None), "test-sk")
        self.assertEqual(getattr(self._captured_region, "id", None), "cn-north-4")

    def test_sdk_fallback_missing_env_credentials_raises_config(self):
        with mock.patch.dict(os.environ, self._clean_credential_env(), clear=True):
            with self.assertRaises(ConfigError) as ctx:
                list_shares_via_sdk("cn-north-4")
        message = str(ctx.exception)
        self.assertIn("AK/SK", message)
        self.assertNotIn("未安装", message)


class _FakeSdkResponse:
    def __init__(self, shares, count):
        self.shares = shares
        self.count = count


class _FakeSdkShare:
    def __init__(self, payload):
        self._payload = payload

    def to_dict(self):
        return self._payload


class _FakeSdkBuilder:
    def __init__(self, test):
        self._test = test

    def with_credentials(self, credentials):
        self._test._captured_credentials = credentials
        return self

    def with_region(self, region):
        self._test._captured_region = region
        return self

    def with_http_config(self, config):
        return self

    def build(self):
        return self._test._fake_client


class TestErrorHierarchy(unittest.TestCase):
    def test_subclasses(self):
        for exc in (GuardError, ConfigError, AuthError, ApiError):
            self.assertTrue(issubclass(exc, SfsExportError))


if __name__ == "__main__":
    unittest.main()