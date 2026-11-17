import json
import os
import subprocess
import sys
import types
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from list_sfs import (  # noqa: E402
    ALLOWED_OPERATION,
    ApiError,
    AuthError,
    ConfigError,
    GuardError,
    MAX_PAGE_SIZE,
    SfsListError,
    active_filter_descriptions,
    build_command,
    clamp_page_size,
    classify_hcloud_failure,
    extract_json,
    extract_shares,
    filter_shares,
    guard_operation,
    guard_text_from_argv,
    guard_write_intent,
    list_shares,
    list_shares_via_sdk,
    main,
    normalize_share,
    render_table,
    sdk_share_to_dict,
    share_names,
    share_summary_lines,
)

CLI_OUTPUT = json.dumps({
    "shares": [
        {
            "id": "8be2f1a3-1111",
            "name": "fs-alpha",
            "status": "available",
            "share_proto": "NFS",
            "size": "500",
            "availability_zone": "cn-north-4a",
            "share_type": "STANDARD",
        },
        {
            "id": "8be2f1a3-2222",
            "name": "fs-beta",
            "status": "creating",
            "share_proto": "CIFS",
            "size": "1024",
            "availability_zone": "cn-north-4b",
            "share_type": "PERFORMANCE",
        },
    ],
    "count": 2,
})

CLI_OUTPUT_EMPTY = json.dumps({"shares": [], "count": 0})


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
        self.assertFalse(guard_write_intent("--region cn-north-4 --json"))
        self.assertFalse(guard_write_intent("list shares show get describe"))

    def test_offsets_and_filters_do_not_trip(self):
        # "--offset" normalizes to "offset" — must not match a write keyword.
        self.assertFalse(guard_write_intent("--offset 20 --limit 10 --status available"))

    def test_az_and_count_flags_do_not_trip(self):
        # "--az"/"--count-only" values are read-only query data, not intents.
        self.assertFalse(guard_write_intent(
            guard_text_from_argv(["--az", "cn-north-4a", "--count-only"])))
        self.assertFalse(guard_write_intent("--count-only --az cn-north-4a"))

    def test_create_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("CreateShare my-fs")

    def test_delete_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--operation DeleteShare")

    def test_mutating_verbs_blocked(self):
        for text in ("expand share", "shrink share", "resize share",
                     "mount share", "unmount share", "attach target",
                     "detach target", "restore backup", "reboot share",
                     "change charge mode", "set acl"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_normalized_separators_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--create-share")
        with self.assertRaises(GuardError):
            guard_write_intent("expand_share")

    def test_filter_values_stripped(self):
        # A file system literally named "delete-me" must not trip the guard.
        self.assertFalse(guard_write_intent(
            guard_text_from_argv(["--name", "delete-me", "--region", "cn-north-4"])))

    def test_operation_guard_rejects_non_listshares(self):
        with self.assertRaises(GuardError):
            guard_operation("CreateShare")
        with self.assertRaises(GuardError):
            guard_operation("ListFileSystems")
        self.assertTrue(guard_operation(ALLOWED_OPERATION))


class TestBuildCommand(unittest.TestCase):
    def test_basic(self):
        argv = build_command("cn-north-4")
        self.assertEqual(argv[0], "SFSTurbo")
        self.assertEqual(argv[1], "ListShares")
        self.assertIn("--cli-region=cn-north-4", argv)
        self.assertIn("--limit=200", argv)
        self.assertIn("--offset=0", argv)

    def test_region_and_offsets(self):
        argv = build_command("cn-south-1", limit=5, offset=10)
        self.assertIn("--cli-region=cn-south-1", argv)
        self.assertIn("--limit=5", argv)
        self.assertIn("--offset=10", argv)

    def test_no_write_flags_ever_added(self):
        argv = build_command("cn-north-4")
        for flag in argv:
            self.assertFalse(
                flag.lower().lstrip("-").startswith(("create", "delete", "expand")))

    def test_default_limit_within_api_max(self):
        # SFS Turbo ListShares rejects limit > 200; the default must be <= 200.
        self.assertLessEqual(MAX_PAGE_SIZE, 200)
        self.assertIn("--limit=%d" % MAX_PAGE_SIZE, build_command("cn-north-4"))

    def test_clamp_page_size(self):
        self.assertEqual(clamp_page_size(1000), 200)
        self.assertEqual(clamp_page_size(201), 200)
        self.assertEqual(clamp_page_size(200), 200)
        self.assertEqual(clamp_page_size(100), 100)
        self.assertEqual(clamp_page_size(0), 1)
        self.assertEqual(clamp_page_size(-5), 1)
        self.assertEqual(clamp_page_size(None), 200)
        self.assertEqual(clamp_page_size("abc"), 200)

    def test_clamp_applied_in_list_shares(self):
        fake = FakeRunner([(CLI_OUTPUT_EMPTY, "", 0)])
        with mock.patch("list_sfs.subprocess.run", fake):
            list_shares("cn-north-4", limit=5000)
        limit_arg = next(a for a in fake.calls[0] if a.startswith("--limit="))
        self.assertEqual(limit_arg, "--limit=200")

    def test_clamp_applied_in_sdk_fallback(self):
        with mock.patch("list_sfs.subprocess.run", FakeRunner([FileNotFoundError()])), \
                mock.patch("list_sfs.list_shares_via_sdk",
                           return_value=[{"name": "sdk-fs"}]) as sdk_mock:
            list_shares("cn-north-4", limit=999)
        self.assertEqual(sdk_mock.call_args.kwargs.get("limit"), 200)


class TestParsing(unittest.TestCase):
    def test_extract_json_plain(self):
        self.assertEqual(extract_json('{"count": 0}'), {"count": 0})

    def test_extract_json_wrapped(self):
        self.assertEqual(extract_json('noise {"a": 1} tail'), {"a": 1})

    def test_extract_json_list(self):
        self.assertEqual(extract_json('[{"a": 1}]'), [{"a": 1}])

    def test_extract_json_invalid(self):
        with self.assertRaises(ApiError):
            extract_json("not json at all")

    def test_extract_shares_key(self):
        payload = {"shares": [{"id": "1"}]}
        self.assertEqual(extract_shares(payload), [{"id": "1"}])

    def test_extract_file_systems_key(self):
        payload = {"file_systems": [{"id": "2"}]}
        self.assertEqual(extract_shares(payload), [{"id": "2"}])

    def test_extract_bare_list(self):
        self.assertEqual(extract_shares([{"id": "3"}]), [{"id": "3"}])

    def test_extract_empty(self):
        self.assertEqual(extract_shares({"count": 0}), [])

    def test_normalize_share_az_fallback(self):
        flat = normalize_share({"name": "x", "az_name": "cn-north-4a"})
        self.assertEqual(flat["availability_zone"], "cn-north-4a")

    def test_normalize_share_metadata_flattened(self):
        flat = normalize_share({"name": "x", "metadata": {"expand_type": "hpc"}})
        self.assertEqual(flat["metadata"], {"expand_type": "hpc"})


class TestClassifyFailure(unittest.TestCase):
    def test_missing_credentials(self):
        err = classify_hcloud_failure(
            "", "Error: CLI credential is not configured, please run configure", 3)
        self.assertIsInstance(err, ConfigError)
        self.assertIn("AK/SK", str(err))

    def test_auth_403(self):
        err = classify_hcloud_failure("", "403 Forbidden", 1)
        self.assertIsInstance(err, AuthError)
        self.assertIn("IAM", str(err))

    def test_generic_api_error(self):
        err = classify_hcloud_failure("", "boom", 2)
        self.assertIsInstance(err, ApiError)

    def test_use_error_marker_with_zero_rc(self):
        err = classify_hcloud_failure(
            "[USE_ERROR]Invalid parameter: foo", "", 0)
        self.assertIsInstance(err, ApiError)
        self.assertIn("参数错误", str(err))


class TestListShares(unittest.TestCase):
    def test_success(self):
        fake = FakeRunner([(CLI_OUTPUT, "", 0)])
        with mock.patch("list_sfs.subprocess.run", fake):
            shares = list_shares("cn-north-4")
        self.assertEqual([s["name"] for s in shares], ["fs-alpha", "fs-beta"])
        self.assertEqual(fake.calls[0][0:3], ["hcloud", "SFSTurbo", "ListShares"])

    def test_empty(self):
        fake = FakeRunner([(CLI_OUTPUT_EMPTY, "", 0)])
        with mock.patch("list_sfs.subprocess.run", fake):
            shares = list_shares("cn-north-4")
        self.assertEqual(shares, [])

    def test_paging_uses_count(self):
        page1 = json.dumps({"shares": [{"id": "1"}, {"id": "2"}], "count": 3})
        page2 = json.dumps({"shares": [{"id": "3"}], "count": 3})
        fake = FakeRunner([(page1, "", 0), (page2, "", 0)])
        with mock.patch("list_sfs.subprocess.run", fake):
            shares = list_shares("cn-north-4", limit=2)
        self.assertEqual(len(shares), 3)
        self.assertEqual(len(fake.calls), 2)
        self.assertIn("--offset=0", fake.calls[0])
        self.assertIn("--offset=2", fake.calls[1])

    def test_missing_credentials_raises_config(self):
        fake = FakeRunner([("", "CLI credential is not configured", 3)])
        with mock.patch("list_sfs.subprocess.run", fake):
            with self.assertRaises(ConfigError):
                list_shares("cn-north-4")

    def test_auth_failure_raises_auth(self):
        fake = FakeRunner([("", "403 Forbidden", 1)])
        with mock.patch("list_sfs.subprocess.run", fake):
            with self.assertRaises(AuthError):
                list_shares("cn-north-4")

    def test_use_error_rc0_raises_api(self):
        fake = FakeRunner([("[USE_ERROR]Invalid parameter: foo", "", 0)])
        with mock.patch("list_sfs.subprocess.run", fake):
            with self.assertRaises(ApiError):
                list_shares("cn-north-4")

    def test_timeout(self):
        fake = FakeRunner([subprocess.TimeoutExpired(cmd="hcloud", timeout=120)])
        with mock.patch("list_sfs.subprocess.run", fake):
            with self.assertRaises(ApiError):
                list_shares("cn-north-4")

    def test_sdk_fallback_when_hcloud_missing(self):
        with mock.patch("list_sfs.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_sfs.list_shares_via_sdk",
                           return_value=[{"name": "sdk-fs"}]) as sdk_mock:
            shares = list_shares("cn-north-4")
        self.assertEqual(shares, [{"name": "sdk-fs"}])
        sdk_mock.assert_called_once()

    def test_sdk_fallback_unavailable_raises_config(self):
        with mock.patch("list_sfs.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_sfs.list_shares_via_sdk",
                           side_effect=ConfigError("huaweicloudsdksfsturbo 未安装")):
            with self.assertRaises(ConfigError):
                list_shares("cn-north-4")


def _fake_sdk_modules():
    """Minimal fake huaweicloudsdk modules so the SDK import block succeeds."""
    core = types.ModuleType("huaweicloudsdkcore")
    creds = types.ModuleType("huaweicloudsdkcore.auth.credentials")
    creds.BasicCredentials = object
    region_mod = types.ModuleType("huaweicloudsdkcore.region.region")
    region_mod.Region = object
    http = types.ModuleType("huaweicloudsdkcore.http.http_config")
    http.HttpConfig = object
    v1 = types.ModuleType("huaweicloudsdksfsturbo.v1")
    v1.SFSTurboClient = object
    v1.ListSharesRequest = object
    v1.ShareInfo = object
    reg = types.ModuleType("huaweicloudsdksfsturbo.v1.region.sfsturbo_region")
    reg.SFSTurboRegion = object
    return {
        "huaweicloudsdkcore": core,
        "huaweicloudsdkcore.auth": types.ModuleType("huaweicloudsdkcore.auth"),
        "huaweicloudsdkcore.auth.credentials": creds,
        "huaweicloudsdkcore.region": types.ModuleType("huaweicloudsdkcore.region"),
        "huaweicloudsdkcore.region.region": region_mod,
        "huaweicloudsdkcore.http": types.ModuleType("huaweicloudsdkcore.http"),
        "huaweicloudsdkcore.http.http_config": http,
        "huaweicloudsdksfsturbo": types.ModuleType("huaweicloudsdksfsturbo"),
        "huaweicloudsdksfsturbo.v1": v1,
        "huaweicloudsdksfsturbo.v1.region": types.ModuleType("huaweicloudsdksfsturbo.v1.region"),
        "huaweicloudsdksfsturbo.v1.region.sfsturbo_region": reg,
    }


class TestSdkFallback(unittest.TestCase):
    def test_missing_env_credentials_raises_config(self):
        credential_vars = (
            "HW_ACCESS_KEY", "HUAWEI_ACCESS_KEY", "HUAWEICLOUD_SDK_AK",
            "HUAWEI_CLOUD_ACCESS_KEY", "HW_SECRET_KEY", "HUAWEI_SECRET_KEY",
            "HUAWEICLOUD_SDK_SK", "HUAWEI_CLOUD_SECRET_KEY",
        )
        env = {name: "" for name in credential_vars}
        with mock.patch.dict(sys.modules, _fake_sdk_modules()), \
                mock.patch.dict(os.environ, env):
            with self.assertRaises(ConfigError) as ctx:
                list_shares_via_sdk("cn-north-4")
        self.assertIn("AK/SK", str(ctx.exception))

    def test_sdk_share_to_dict_remaps_wire_names(self):
        class Share:
            def to_dict(self):
                return {"name": "fs", "instance_id": "inst-1"}

        class ShareInfo:
            attribute_map = {"name": "name", "instance_id": "instanceId"}

        fake_mod = types.ModuleType("huaweicloudsdksfsturbo.v1")
        fake_mod.ShareInfo = ShareInfo
        with mock.patch.dict(sys.modules, {"huaweicloudsdksfsturbo.v1": fake_mod}):
            record = sdk_share_to_dict(Share())
        self.assertEqual(record["name"], "fs")
        self.assertEqual(record["instanceId"], "inst-1")

    def test_sdk_share_to_dict_plain_dict(self):
        self.assertEqual(sdk_share_to_dict({"name": "fs"}), {"name": "fs"})


class TestFiltering(unittest.TestCase):
    SHARES = [
        {"id": "aaa-111", "name": "fs-prod", "status": "available",
         "share_proto": "NFS"},
        {"id": "bbb-222", "name": "fs-dev", "status": "creating",
         "share_proto": "CIFS"},
    ]

    def test_filter_by_name(self):
        self.assertEqual(
            [s["name"] for s in filter_shares(self.SHARES, name="prod")],
            ["fs-prod"])

    def test_filter_by_id(self):
        self.assertEqual(
            [s["id"] for s in filter_shares(self.SHARES, share_id="bbb")],
            ["bbb-222"])

    def test_filter_by_status(self):
        self.assertEqual(
            [s["name"] for s in filter_shares(self.SHARES, status="creating")],
            ["fs-dev"])

    def test_filter_by_proto(self):
        self.assertEqual(
            [s["name"] for s in filter_shares(self.SHARES, share_proto="nfs")],
            ["fs-prod"])

    def test_filter_by_az(self):
        shares = [
            {"name": "a", "availability_zone": "cn-north-4a"},
            {"name": "b", "az_name": "cn-north-4b"},
        ]
        self.assertEqual(
            [s["name"] for s in filter_shares(shares, az="north-4a")],
            ["a"])
        self.assertEqual(
            [s["name"] for s in filter_shares(shares, az="north-4b")],
            ["b"])

    def test_filter_descriptions(self):
        desc = active_filter_descriptions(name="fs", share_id="a", status="available")
        self.assertEqual(desc, ["name=fs", "id=a", "status=available"])

    def test_filter_descriptions_include_az(self):
        desc = active_filter_descriptions(name="fs", az="cn-north-4a")
        self.assertEqual(desc, ["name=fs", "az=cn-north-4a"])


class TestRenderAndNames(unittest.TestCase):
    def test_names(self):
        self.assertEqual(
            share_names([{"name": "a"}, {"name": "b"}]), ["a", "b"])

    def test_names_fallback_to_id(self):
        self.assertEqual(share_names([{"id": "only-id"}]), ["only-id"])

    def test_summary_lines(self):
        lines = share_summary_lines([{"name": "a", "id": "1"}])
        self.assertEqual(lines, ["a  (id: 1)"])

    def test_table_contains_fields(self):
        shares = extract_shares(json.loads(CLI_OUTPUT))
        table = render_table(shares)
        for fragment in ("name", "id", "status", "share_proto", "size",
                         "availability_zone", "fs-alpha", "NFS"):
            self.assertIn(fragment, table)

    def test_table_minimal(self):
        table = render_table([{"name": "only-name"}])
        self.assertIn("only-name", table)
        self.assertIn("name", table)


class TestMain(unittest.TestCase):
    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("list_sfs.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            rc = main(argv)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    def test_table_output(self):
        rc, out, err = self._run(["--region", "cn-north-4"], [(CLI_OUTPUT, "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("SFS 文件系统列表", out)
        self.assertIn("fs-alpha", out)
        self.assertEqual(err, "")

    def test_json_output(self):
        rc, out, err = self._run(["--json"], [(CLI_OUTPUT, "", 0)])
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual([s["name"] for s in payload], ["fs-alpha", "fs-beta"])

    def test_names_output(self):
        rc, out, err = self._run(["--names-only"], [(CLI_OUTPUT, "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("fs-alpha", out)
        self.assertNotIn("share_proto", out)

    def test_name_filter_applied(self):
        rc, out, err = self._run(["--names-only", "--name", "alpha"],
                                 [(CLI_OUTPUT, "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("fs-alpha", out)
        self.assertNotIn("fs-beta", out)

    def test_az_filter_applied(self):
        rc, out, err = self._run(["--names-only", "--az", "north-4a"],
                                 [(CLI_OUTPUT, "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("fs-alpha", out)
        self.assertNotIn("fs-beta", out)

    def test_count_only_output(self):
        rc, out, err = self._run(["--count-only"], [(CLI_OUTPUT, "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("数量：2", out)
        self.assertNotIn("fs-alpha", out)

    def test_count_only_with_filter(self):
        rc, out, err = self._run(["--count-only", "--name", "alpha"],
                                 [(CLI_OUTPUT, "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("数量：1", out)
        self.assertIn("过滤条件", out)

    def test_empty_message(self):
        rc, out, err = self._run(["--region", "cn-south-1"],
                                 [(CLI_OUTPUT_EMPTY, "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("无 SFS 文件系统", out)
        self.assertIn("cn-south-1", out)

    def test_empty_json_output(self):
        rc, out, err = self._run(["--json"], [(CLI_OUTPUT_EMPTY, "", 0)])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out), [])

    def test_auth_error_message(self):
        rc, out, err = self._run([], [("", "403 Forbidden", 1)])
        self.assertEqual(rc, 1)
        self.assertIn("[错误]", err)
        self.assertIn("IAM", err)

    def test_missing_ak_sk_error_message(self):
        rc, out, err = self._run([], [("", "CLI credential is not configured", 3)])
        self.assertEqual(rc, 1)
        self.assertIn("AK/SK", err)

    def test_hcloud_not_installed(self):
        with mock.patch("list_sfs.list_shares_via_sdk",
                        side_effect=ConfigError("huaweicloudsdksfsturbo 未安装")):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 1)
        self.assertIn("未安装", err)

    def test_hcloud_missing_falls_back_to_sdk(self):
        with mock.patch("list_sfs.list_shares_via_sdk",
                        return_value=[{"name": "sdk-fs", "id": "x"}]):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 0)
        self.assertIn("sdk-fs", out)

    def test_write_intent_operation_blocked(self):
        rc, out, err = self._run(["--operation", "CreateShare"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)

    def test_write_keyword_argv_blocked(self):
        rc, out, err = self._run(["--expand-share"], [])
        self.assertEqual(rc, 1)
        self.assertIn("守卫拦截", err)


class TestErrorHierarchy(unittest.TestCase):
    def test_subclasses(self):
        for exc in (GuardError, ConfigError, AuthError, ApiError):
            self.assertTrue(issubclass(exc, SfsListError))


if __name__ == "__main__":
    unittest.main()