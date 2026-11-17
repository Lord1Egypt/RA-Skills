import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

_SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_SKILL_DIR, "scripts"))

import cdn_export_obs  # noqa: E402
import export_results  # noqa: E402
import list_cdn  # noqa: E402
import upload_obs  # noqa: E402

DOMAIN_1 = {
    "id": "cdn-0001",
    "domain_name": "www.example.com",
    "business_type": "web",
    "domain_status": "online",
    "cname": "www.example.com.c.cdnhwc1.com",
    "service_area": "mainland_china",
    "https_status": 1,
    "tags": [{"key": "env", "value": "test"}],
}
DOMAIN_2 = {
    "id": "cdn-0002",
    "domain_name": "static.example.com",
    "business_type": "download",
    "domain_status": "offline",
    "cname": "static.example.com.c.cdnhwc1.com",
}


class FakeHcloud:
    """subprocess.run fake: dispatches on the hcloud argv."""

    def __init__(self, handler):
        self._handler = handler
        self.calls = []

    def __call__(self, cmd, **kwargs):
        self.calls.append(cmd)
        out = self._handler(cmd)
        if isinstance(out, Exception):
            raise out
        stdout, stderr, returncode = out
        return subprocess.CompletedProcess(cmd, returncode, stdout, stderr)

    @property
    def cdn_calls(self):
        return [c for c in self.calls if "CDN" in c]

    @property
    def obs_calls(self):
        return [c for c in self.calls if "OBS" in c]


def obs_subop(cmd):
    return cmd[cmd.index("OBS") + 1]


def cdn_page(cmd):
    for part in cmd:
        if part.startswith("--page_number="):
            return int(part.split("=", 1)[1])
    return 1


# --------------------------------------------------------------------------
# list_cdn
# --------------------------------------------------------------------------

class TestListCdnGuard(unittest.TestCase):
    def test_read_passes(self):
        self.assertFalse(list_cdn.guard_write_intent("ListDomains --domain-status online"))

    def test_create_blocked(self):
        with self.assertRaises(list_cdn.GuardError):
            list_cdn.guard_write_intent("CreateDomain example.com")

    def test_delete_blocked(self):
        with self.assertRaises(list_cdn.GuardError):
            list_cdn.guard_write_intent("--operation DeleteDomain")

    def test_normalized_separators_blocked(self):
        with self.assertRaises(list_cdn.GuardError):
            list_cdn.guard_write_intent("--refresh-task")

    def test_operation_guard(self):
        self.assertTrue(list_cdn.guard_operation("ListDomains"))
        with self.assertRaises(list_cdn.GuardError):
            list_cdn.guard_operation("ShowDomainDetail")


class TestListCdnCommand(unittest.TestCase):
    def test_basic(self):
        argv = list_cdn.build_command("cn-north-4")
        self.assertEqual(argv[0:2], ["CDN", "ListDomains"])
        self.assertIn("--cli-region=cn-north-4", argv)
        self.assertIn("--page_size=100", argv)
        self.assertIn("--page_number=1", argv)

    def test_filters_forwarded(self):
        argv = list_cdn.build_command("cn-south-1", domain_name="www.example.com",
                                      business_type="web", domain_status="online")
        self.assertIn("--domain_name=www.example.com", argv)
        self.assertIn("--business_type=web", argv)
        self.assertIn("--domain_status=online", argv)


class TestListCdnExtract(unittest.TestCase):
    def test_extract_json_noise(self):
        self.assertEqual(list_cdn.extract_json("noise\n{\"a\": 1}\n"), {"a": 1})

    def test_extract_json_invalid(self):
        with self.assertRaises(list_cdn.ApiError):
            list_cdn.extract_json("<html>")

    def test_extract_domains(self):
        self.assertEqual(list_cdn.extract_domains({"domains": [DOMAIN_1]}), [DOMAIN_1])
        self.assertEqual(list_cdn.extract_domains({"total": 0}), [])


class TestListCdnFailure(unittest.TestCase):
    def test_credentials(self):
        err = list_cdn.classify_hcloud_failure("", "cli-ak is empty", 1)
        self.assertIsInstance(err, list_cdn.ConfigError)

    def test_auth(self):
        err = list_cdn.classify_hcloud_failure("", "403 Forbidden", 1)
        self.assertIsInstance(err, list_cdn.AuthError)

    def test_generic(self):
        err = list_cdn.classify_hcloud_failure("", "boom", 2)
        self.assertIsInstance(err, list_cdn.ApiError)

    def test_use_error_rc0(self):
        err = list_cdn.classify_hcloud_failure("[USE_ERROR]bad param", "", 0)
        self.assertIsInstance(err, list_cdn.ApiError)
        self.assertIn("参数错误", str(err))


class TestListCdnPaging(unittest.TestCase):
    def test_single_page(self):
        fake = FakeHcloud(lambda cmd: (json.dumps({"domains": [DOMAIN_1], "total": 1}), "", 0))
        with mock.patch("subprocess.run", fake):
            domains = list_cdn.list_domains("cn-north-4")
        self.assertEqual(domains, [DOMAIN_1])
        self.assertEqual(len(fake.cdn_calls), 1)

    def test_total_paging(self):
        def handler(cmd):
            page = cdn_page(cmd)
            if page == 1:
                return (json.dumps({"domains": [DOMAIN_1], "total": 2}), "", 0)
            return (json.dumps({"domains": [DOMAIN_2], "total": 2}), "", 0)
        fake = FakeHcloud(handler)
        with mock.patch("subprocess.run", fake):
            domains = list_cdn.list_domains("cn-north-4", limit=1)
        self.assertEqual(domains, [DOMAIN_1, DOMAIN_2])
        self.assertIn("--page_number=2", fake.cdn_calls[1])

    def test_empty(self):
        fake = FakeHcloud(lambda cmd: (json.dumps({"domains": [], "total": 0}), "", 0))
        with mock.patch("subprocess.run", fake):
            self.assertEqual(list_cdn.list_domains("cn-north-4"), [])

    def test_sdk_fallback(self):
        with mock.patch("subprocess.run", FakeHcloud(lambda cmd: FileNotFoundError())), \
                mock.patch("list_cdn.list_domains_via_sdk", return_value=[DOMAIN_1]) as sdk:
            domains = list_cdn.list_domains("cn-north-4", domain_status="online")
        self.assertEqual(domains, [DOMAIN_1])
        self.assertEqual(sdk.call_args.kwargs.get("domain_status"), "online")


# --------------------------------------------------------------------------
# export_results
# --------------------------------------------------------------------------

class TestExport(unittest.TestCase):
    def test_json_roundtrip(self):
        self.assertEqual(json.loads(export_results.to_json([DOMAIN_1])), [DOMAIN_1])

    def test_csv_header_and_tags(self):
        text = export_results.to_csv([DOMAIN_1, DOMAIN_2])
        lines = text.strip().splitlines()
        self.assertIn("domain_name", lines[0])
        self.assertIn("www.example.com", lines[1])
        self.assertIn("env=test", text)
        # DOMAIN_2 lacks tags -> flattened to '-'
        self.assertIn("static.example.com", text)

    def test_csv_empty_header_only(self):
        lines = export_results.to_csv([]).strip().splitlines()
        self.assertEqual(len(lines), 1)

    def test_markdown_first_column_domain(self):
        md = export_results.to_markdown([DOMAIN_1, DOMAIN_2], region="cn-north-4")
        header = md.splitlines()[0]
        self.assertTrue(header.startswith("| 域名 |"))
        self.assertIn("www.example.com", md)
        self.assertIn("加速域名状态", header)

    def test_markdown_empty_header_table(self):
        md = export_results.to_markdown([], region="cn-north-4")
        lines = md.strip().splitlines()
        self.assertEqual(len(lines), 2)
        self.assertIn("域名", lines[0])

    def test_markdown_pipe_escape(self):
        md = export_results.to_markdown([{"domain_name": "a|b"}])
        self.assertIn("a\\|b", md)

    def test_markdown_summary(self):
        md = export_results.to_markdown([DOMAIN_1], region="cn-north-4", summary=True)
        self.assertIn("共 1 个", md)
        self.assertIn("cn-north-4", md)

    def test_unknown_format(self):
        with self.assertRaises(export_results.ExportError):
            export_results.serialize([], fmt="xlsx")

    def test_default_output_path(self):
        path = export_results.default_output_path("cn-north-4", fmt="csv",
                                                  timestamp="20260101T000000Z")
        self.assertEqual(path, "cdn_domains_cn-north-4_20260101T000000Z.csv")

    def test_write_atomic_creates_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "nested", "out.json")
            export_results.write_text_atomic(target, "{}\n")
            with open(target, encoding="utf-8") as handle:
                self.assertEqual(handle.read(), "{}\n")

    def test_write_atomic_bad_path_raises(self):
        with self.assertRaises(export_results.ExportError):
            export_results.write_text_atomic("", "data")

    def test_export_returns_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "out.md")
            path, content = export_results.export([DOMAIN_1], "md", output=target,
                                                  region="cn-north-4")
            self.assertEqual(path, target)
            self.assertTrue(os.path.isfile(target))
            self.assertIn("www.example.com", content)


# --------------------------------------------------------------------------
# upload_obs
# --------------------------------------------------------------------------

class TestUploadHelpers(unittest.TestCase):
    def test_parse_obs_url(self):
        self.assertEqual(upload_obs.parse_obs_url("obs://b/k"), ("b", "k"))
        self.assertEqual(upload_obs.parse_obs_url("obs://b/a/b/c.txt"), ("b", "a/b/c.txt"))
        with self.assertRaises(upload_obs.ObsError):
            upload_obs.parse_obs_url("http://x")

    def test_build_cp_argv(self):
        argv = upload_obs.build_cp_argv("cn-north-4", "/tmp/a.json", "bk", "k/a.json")
        self.assertEqual(argv[0:2], ["OBS", "cp"])
        self.assertIn("/tmp/a.json", argv)
        self.assertIn("obs://bk/k/a.json", argv)
        self.assertIn("-e=obs.cn-north-4.myhuaweicloud.com", argv)

    def test_build_stat_argv(self):
        argv = upload_obs.build_stat_argv("cn-south-1", "bk", "k")
        self.assertEqual(argv[0:2], ["OBS", "stat"])
        self.assertIn("obs://bk/k", argv)
        self.assertIn("-e=obs.cn-south-1.myhuaweicloud.com", argv)

    def test_guard_operation(self):
        self.assertTrue(upload_obs.guard_operation("cp"))
        self.assertTrue(upload_obs.guard_operation("stat"))
        for bad in ("rm", "mb", "mv", "sync"):
            with self.assertRaises(upload_obs.ObsError):
                upload_obs.guard_operation(bad)

    def test_parse_stat_output(self):
        info = upload_obs.parse_stat_output("Size: 123\nETag: abcdef0123456789")
        self.assertEqual(info.get("size"), 123)
        self.assertEqual(info.get("etag"), "abcdef0123456789")

    def test_looks_like_not_found(self):
        self.assertTrue(upload_obs.looks_like_not_found("NoSuchKey"))
        self.assertTrue(upload_obs.looks_like_not_found("404 Not Found"))
        self.assertFalse(upload_obs.looks_like_not_found("Upload successfully"))


class TestObjectExists(unittest.TestCase):
    def test_exists(self):
        fake = FakeHcloud(lambda cmd: ("Key: k\nSize: 10\n", "", 0))
        with mock.patch("subprocess.run", fake):
            self.assertTrue(upload_obs.object_exists("cn-north-4", "b", "k"))

    def test_not_found(self):
        fake = FakeHcloud(lambda cmd: ("", "NoSuchKey: the object does not exist", 1))
        with mock.patch("subprocess.run", fake):
            self.assertFalse(upload_obs.object_exists("cn-north-4", "b", "k"))

    def test_auth_error(self):
        fake = FakeHcloud(lambda cmd: ("", "403 Forbidden", 1))
        with mock.patch("subprocess.run", fake):
            with self.assertRaises(upload_obs.AuthError):
                upload_obs.object_exists("cn-north-4", "b", "k")

    def test_hcloud_missing_sdk_fallback(self):
        with mock.patch("subprocess.run", FakeHcloud(lambda cmd: FileNotFoundError())), \
                mock.patch("upload_obs.sdk_object_exists", return_value=True) as sdk:
            self.assertTrue(upload_obs.object_exists("cn-north-4", "b", "k"))
        sdk.assert_called_once()


class TestUpload(unittest.TestCase):
    def _handler(self, exists, cp_ok=True, verify_size=10):
        state = {"stat": 0}

        def handler(cmd):
            sub = obs_subop(cmd)
            if sub == "stat":
                state["stat"] += 1
                if exists:
                    return ("Key: k\nSize: %s\n" % verify_size, "", 0)
                if state["stat"] == 1:
                    return ("", "NoSuchKey", 1)
                return ("Key: k\nSize: %s\n" % verify_size, "", 0)
            if sub == "cp":
                if cp_ok:
                    return ("Upload successfully", "", 0)
                return ("", "boom", 2)
            raise AssertionError("unexpected OBS op %s" % sub)
        return handler

    def test_upload_new_object(self):
        with tempfile.TemporaryDirectory() as tmp:
            local = os.path.join(tmp, "a.json")
            with open(local, "w") as handle:
                handle.write("{}")
            size = os.path.getsize(local)
            fake = FakeHcloud(self._handler(exists=False, verify_size=size))
            with mock.patch("subprocess.run", fake):
                result = upload_obs.upload_file(
                    "cn-north-4", local, "bk", "k", verify=True)
        self.assertFalse(result["existed_before"])
        self.assertEqual(result["uploaded_via"], "cli")
        self.assertTrue(result["verified"]["exists"])
        self.assertTrue(result["verified"]["size_match"])

    def test_refuse_overwrite_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            local = os.path.join(tmp, "a.json")
            with open(local, "w") as handle:
                handle.write("{}")
            fake = FakeHcloud(self._handler(exists=True))
            with mock.patch("subprocess.run", fake):
                with self.assertRaises(upload_obs.OverwriteError):
                    upload_obs.upload_file("cn-north-4", local, "bk", "k")
        # no cp issued
        self.assertTrue(all(obs_subop(c) != "cp" for c in fake.obs_calls))

    def test_overwrite_allowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            local = os.path.join(tmp, "a.json")
            with open(local, "w") as handle:
                handle.write("{}")
            size = os.path.getsize(local)
            fake = FakeHcloud(self._handler(exists=True, verify_size=size))
            with mock.patch("subprocess.run", fake):
                result = upload_obs.upload_file(
                    "cn-north-4", local, "bk", "k", overwrite=True)
        self.assertTrue(result["existed_before"])
        self.assertTrue(result["overwritten"])

    def test_verify_size_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            local = os.path.join(tmp, "a.json")
            with open(local, "w") as handle:
                handle.write("{}")

            def handler(cmd):
                sub = obs_subop(cmd)
                if sub == "stat":
                    # first probe: not found; verification: wrong size
                    if getattr(handler, "seen", 0) == 0:
                        handler.seen = 1
                        return ("", "NoSuchKey", 1)
                    return ("Key: k\nSize: 999999\n", "", 0)
                return ("Upload successfully", "", 0)
            fake = FakeHcloud(handler)
            with mock.patch("subprocess.run", fake):
                with self.assertRaises(upload_obs.ObsError) as ctx:
                    upload_obs.upload_file("cn-north-4", local, "bk", "k")
        self.assertIn("大小", str(ctx.exception))

    def test_missing_local_file(self):
        with self.assertRaises(upload_obs.ObsError):
            upload_obs.upload_file("cn-north-4", "/no/such/file", "bk", "k")

    def test_sdk_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            local = os.path.join(tmp, "a.json")
            with open(local, "w") as handle:
                handle.write("{}")
            with mock.patch("subprocess.run", FakeHcloud(lambda cmd: FileNotFoundError())), \
                    mock.patch("upload_obs.sdk_object_exists",
                               side_effect=[False, True]), \
                    mock.patch("upload_obs.sdk_put_object",
                               return_value={"etag": "x", "size": 2}) as put:
                result = upload_obs.upload_file("cn-north-4", local, "bk", "k")
        self.assertEqual(result["uploaded_via"], "sdk")
        put.assert_called_once()

    def test_upload_error_propagated(self):
        with tempfile.TemporaryDirectory() as tmp:
            local = os.path.join(tmp, "a.json")
            with open(local, "w") as handle:
                handle.write("{}")
            fake = FakeHcloud(self._handler(exists=False, cp_ok=False))
            with mock.patch("subprocess.run", fake):
                with self.assertRaises(upload_obs.ApiError):
                    upload_obs.upload_file("cn-north-4", local, "bk", "k", verify=False)


# --------------------------------------------------------------------------
# cdn_export_obs (end-to-end)
# --------------------------------------------------------------------------

class TestOrchestrator(unittest.TestCase):
    def _router(self, domains, obs_exists=False, cp_ok=True):
        state = {"stat": 0, "local": None}

        def handler(cmd):
            if "CDN" in cmd:
                return (json.dumps({"domains": domains, "total": len(domains)}), "", 0)
            sub = obs_subop(cmd)
            if sub == "stat":
                state["stat"] += 1
                if obs_exists and state["local"] is None:
                    return ("Key: k\nSize: 0\n", "", 0)
                if state["local"] is None:
                    return ("", "NoSuchKey", 1)
                return ("Key: k\nSize: %d\n" % os.path.getsize(state["local"]), "", 0)
            if sub == "cp":
                state["local"] = cmd[3]
                if cp_ok:
                    return ("Upload successfully", "", 0)
                return ("", "boom", 2)
            raise AssertionError(sub)
        return handler

    def _run(self, argv, handler):
        fake = FakeHcloud(handler)
        with mock.patch("subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr, \
                tempfile.TemporaryDirectory() as tmp:
            out_path = os.path.join(tmp, "cdn_domains_cn-north-4.json")
            rc = cdn_export_obs.main(argv + ["--output", out_path])
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    def test_export_and_upload_json(self):
        rc, out, err = self._run(
            ["--region", "cn-north-4", "--bucket", "bk", "--json"],
            self._router([DOMAIN_1, DOMAIN_2]))
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual(payload["domain_count"], 2)
        self.assertEqual(payload["upload"]["uploaded_via"], "cli")
        self.assertTrue(payload["upload"]["verified"]["exists"])
        self.assertEqual(err, "")

    def test_export_only(self):
        rc, out, err = self._run(
            ["--export-only", "--format", "md", "--json"],
            self._router([DOMAIN_1]))
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertTrue(payload["upload"]["skipped"])

    def test_no_bucket_skips_upload(self):
        rc, out, err = self._run(["--json"], self._router([DOMAIN_1]))
        self.assertEqual(rc, 0)
        self.assertTrue(json.loads(out)["upload"]["skipped"])

    def test_overwrite_refused(self):
        rc, out, err = self._run(
            ["--bucket", "bk", "--json"],
            self._router([DOMAIN_1], obs_exists=True))
        self.assertEqual(rc, 1)
        self.assertIn("已存在", err)

    def test_overwrite_allowed(self):
        rc, out, err = self._run(
            ["--bucket", "bk", "--overwrite", "--json"],
            self._router([DOMAIN_1], obs_exists=True))
        self.assertEqual(rc, 0)
        self.assertTrue(json.loads(out)["upload"]["overwritten"])

    def test_empty_domains_still_exports(self):
        rc, out, err = self._run(
            ["--bucket", "bk", "--json"],
            self._router([]))
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out)["domain_count"], 0)

    def test_guard_blocks_write_operation(self):
        rc, out, err = self._run(
            ["--operation", "DeleteDomain"], self._router([DOMAIN_1]))
        self.assertEqual(rc, 1)
        self.assertIn("不允许的操作", err)

    def test_output_path_with_write_word_not_blocked(self):
        # local path containing a write word must not trip the CDN guard
        fake = FakeHcloud(self._router([DOMAIN_1]))
        with mock.patch("subprocess.run", fake), \
                mock.patch("sys.stdout"), mock.patch("sys.stderr"), \
                tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "cdn-delete-report.json")
            rc = cdn_export_obs.main(
                ["--export-only", "--output", target, "--json"])
        self.assertEqual(rc, 0)

    def test_default_key_is_basename(self):
        fake = FakeHcloud(self._router([DOMAIN_1]))
        with mock.patch("subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr"), \
                tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "my_domains.json")
            rc = cdn_export_obs.main(
                ["--bucket", "bk", "--output", target, "--json"])
        self.assertEqual(rc, 0)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        self.assertEqual(json.loads(out)["upload"]["key"], "my_domains.json")


if __name__ == "__main__":
    unittest.main()