import json
import os
import subprocess
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from list_obs_buckets import (  # noqa: E402
    ALLOWED_OPERATION,
    ApiError,
    AuthError,
    ConfigError,
    GuardError,
    ObsListError,
    bucket_names,
    build_command,
    classify_hcloud_failure,
    guard_operation,
    guard_write_intent,
    list_buckets,
    list_buckets_via_sdk,
    main,
    normalize_sdk_bucket,
    parse_cli_buckets,
    render_table,
)

CLI_OUTPUT = """Bucket number is: 2

  obs://bucket-alpha
  obs://bucket-beta
"""

CLI_OUTPUT_WITH_COLUMNS = """Bucket number is: 2

  obs://bucket-alpha  2024-01-02T03:04:05Z  cn-north-4  Standard
  obs://bucket-beta   2024-05-06T07:08:09Z  cn-south-1  Warm
"""


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
        self.assertFalse(guard_write_intent("--region cn-north-4 --output table"))
        self.assertFalse(guard_write_intent("list buckets show get describe"))

    def test_create_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("CreateBucket my-bucket")

    def test_delete_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--operation DeleteBucket")

    def test_mutating_verbs_blocked(self):
        for text in ("upload object", "download object", "copy object",
                     "remove bucket", "restore object", "abort upload",
                     "sync dir", "modify acl", "update policy"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_normalized_separators_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--create-bucket")
        with self.assertRaises(GuardError):
            guard_write_intent("update_bucket_policy")

    def test_operation_guard_rejects_non_ls(self):
        with self.assertRaises(GuardError):
            guard_operation("ListBuckets")
        with self.assertRaises(GuardError):
            guard_operation("mb")
        self.assertTrue(guard_operation(ALLOWED_OPERATION))


class TestBuildCommand(unittest.TestCase):
    def test_basic(self):
        argv = build_command("cn-north-4")
        self.assertEqual(argv[0], "OBS")
        self.assertEqual(argv[1], "ls")
        self.assertIn("-limit=1000", argv)
        self.assertIn("-e=obs.cn-north-4.myhuaweicloud.com", argv)

    def test_region_endpoint(self):
        argv = build_command("cn-south-1", limit=5)
        self.assertIn("-limit=5", argv)
        self.assertIn("-e=obs.cn-south-1.myhuaweicloud.com", argv)

    def test_custom_endpoint(self):
        argv = build_command("cn-north-4", endpoint="obs.custom.example.com")
        self.assertIn("-e=obs.custom.example.com", argv)

    def test_no_write_flags_ever_added(self):
        argv = build_command("cn-north-4")
        for flag in argv:
            self.assertFalse(
                flag.lower().lstrip("-").startswith(("create", "delete", "put", "rm")))


class TestParseCli(unittest.TestCase):
    def test_names_only_output(self):
        buckets = parse_cli_buckets(CLI_OUTPUT)
        self.assertEqual([b["name"] for b in buckets], ["bucket-alpha", "bucket-beta"])

    def test_bucket_number_line_ignored(self):
        buckets = parse_cli_buckets("Bucket number is: 0\n")
        self.assertEqual(buckets, [])

    def test_columns_extracted(self):
        buckets = parse_cli_buckets(CLI_OUTPUT_WITH_COLUMNS)
        self.assertEqual(buckets[0]["name"], "bucket-alpha")
        self.assertEqual(buckets[0]["creation_date"], "2024-01-02T03:04:05Z")
        self.assertEqual(buckets[0]["location"], "cn-north-4")
        self.assertEqual(buckets[1]["location"], "cn-south-1")

    def test_duplicates_collapse(self):
        text = "  obs://dup\n  obs://dup\n"
        buckets = parse_cli_buckets(text)
        self.assertEqual(len(buckets), 1)

    def test_empty_output(self):
        self.assertEqual(parse_cli_buckets(""), [])


class TestClassifyFailure(unittest.TestCase):
    def test_missing_credentials(self):
        err = classify_hcloud_failure(
            "", "Warn: Please set ak, sk and endpoint in the configuration file!", 3)
        self.assertIsInstance(err, ConfigError)
        self.assertIn("AK/SK", str(err))

    def test_invalid_ak(self):
        err = classify_hcloud_failure("", "InvalidAccessKeyId: bad key", 1)
        self.assertIsInstance(err, AuthError)

    def test_auth_403(self):
        err = classify_hcloud_failure("", "AccessDenied 403 Forbidden", 1)
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


class TestListBuckets(unittest.TestCase):
    def test_success(self):
        fake = FakeRunner([(CLI_OUTPUT, "", 0)])
        with mock.patch("list_obs_buckets.subprocess.run", fake):
            buckets = list_buckets("cn-north-4")
        self.assertEqual([b["name"] for b in buckets], ["bucket-alpha", "bucket-beta"])
        self.assertEqual(len(fake.calls), 1)
        self.assertIn("OBS", fake.calls[0])

    def test_empty(self):
        fake = FakeRunner([("Bucket number is: 0\n", "", 0)])
        with mock.patch("list_obs_buckets.subprocess.run", fake):
            buckets = list_buckets("cn-north-4")
        self.assertEqual(buckets, [])

    def test_missing_credentials_raises_config(self):
        fake = FakeRunner([("", "Warn: Please set ak, sk and endpoint", 3)])
        with mock.patch("list_obs_buckets.subprocess.run", fake):
            with self.assertRaises(ConfigError):
                list_buckets("cn-north-4")

    def test_auth_failure_raises_auth(self):
        fake = FakeRunner([("", "403 Forbidden", 1)])
        with mock.patch("list_obs_buckets.subprocess.run", fake):
            with self.assertRaises(AuthError):
                list_buckets("cn-north-4")

    def test_use_error_rc0_raises_api(self):
        fake = FakeRunner([("[USE_ERROR]Invalid parameter: foo", "", 0)])
        with mock.patch("list_obs_buckets.subprocess.run", fake):
            with self.assertRaises(ApiError):
                list_buckets("cn-north-4")

    def test_timeout(self):
        fake = FakeRunner([subprocess.TimeoutExpired(cmd="hcloud", timeout=120)])
        with mock.patch("list_obs_buckets.subprocess.run", fake):
            with self.assertRaises(ApiError):
                list_buckets("cn-north-4")

    def test_sdk_fallback_when_hcloud_missing(self):
        with mock.patch("list_obs_buckets.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_obs_buckets.list_buckets_via_sdk",
                           return_value=[{"name": "sdk-bucket"}]) as sdk_mock:
            buckets = list_buckets("cn-north-4")
        self.assertEqual(buckets, [{"name": "sdk-bucket"}])
        sdk_mock.assert_called_once()

    def test_sdk_fallback_unavailable_raises_config(self):
        with mock.patch("list_obs_buckets.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_obs_buckets.list_buckets_via_sdk",
                           side_effect=ConfigError("huaweicloudsdkobs 未安装")):
            with self.assertRaises(ConfigError):
                list_buckets("cn-north-4")


class TestSdkFallback(unittest.TestCase):
    def test_missing_env_credentials_raises_config(self):
        env = {k: v for k, v in os.environ.items()
               if not k.upper().startswith(("HW", "HUAWEI", "HWC"))}
        with mock.patch.dict(os.environ, env, clear=True):
            with self.assertRaises(ConfigError) as ctx:
                list_buckets_via_sdk("cn-north-4")
        self.assertIn("AK/SK", str(ctx.exception))

    def test_normalize_sdk_bucket(self):
        class B:
            name = "b1"
            creation_date = "2024-01-01T00:00:00Z"
            location = "cn-north-4"
            storage_class = "Standard"
        record = normalize_sdk_bucket(B())
        self.assertEqual(record["name"], "b1")
        self.assertEqual(record["creation_date"], "2024-01-01T00:00:00Z")
        self.assertEqual(record["location"], "cn-north-4")
        self.assertEqual(record["storage_class"], "Standard")

    def test_normalize_sdk_bucket_minimal(self):
        class B:
            pass
        self.assertEqual(normalize_sdk_bucket(B()), {"name": "-"})


class TestRenderAndNames(unittest.TestCase):
    def test_names(self):
        self.assertEqual(
            bucket_names([{"name": "a"}, {"name": "b"}]), ["a", "b"])

    def test_names_missing(self):
        self.assertEqual(bucket_names([{}]), ["-"])

    def test_table_contains_fields(self):
        buckets = parse_cli_buckets(CLI_OUTPUT_WITH_COLUMNS)
        table = render_table(buckets)
        for fragment in ("name", "creation_date", "location",
                         "bucket-alpha", "2024-01-02T03:04:05Z", "cn-north-4"):
            self.assertIn(fragment, table)

    def test_table_minimal(self):
        table = render_table([{"name": "only-name"}])
        self.assertIn("only-name", table)
        self.assertIn("name", table)


class TestMain(unittest.TestCase):
    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("list_obs_buckets.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            rc = main(argv)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    def test_table_output(self):
        rc, out, err = self._run(["--region", "cn-north-4"], [(CLI_OUTPUT, "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("OBS 桶列表", out)
        self.assertIn("bucket-alpha", out)
        self.assertEqual(err, "")

    def test_json_output(self):
        rc, out, err = self._run(["--json"], [(CLI_OUTPUT, "", 0)])
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual([b["name"] for b in payload], ["bucket-alpha", "bucket-beta"])

    def test_output_json_flag(self):
        rc, out, err = self._run(["--output", "json"], [(CLI_OUTPUT, "", 0)])
        self.assertEqual(rc, 0)
        self.assertEqual(len(json.loads(out)), 2)

    def test_names_output(self):
        rc, out, err = self._run(["--names-only"], [(CLI_OUTPUT, "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("bucket-alpha", out)
        self.assertNotIn("creation_date", out)

    def test_empty_message(self):
        rc, out, err = self._run(["--region", "cn-south-1"],
                                 [("Bucket number is: 0\n", "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("无 OBS 桶", out)
        self.assertIn("cn-south-1", out)

    def test_empty_json_output(self):
        rc, out, err = self._run(["--json"], [("Bucket number is: 0\n", "", 0)])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out), [])

    def test_empty_names_output(self):
        rc, out, err = self._run(["--names-only"], [("Bucket number is: 0\n", "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("共 0 个", out)
        self.assertNotIn("无 OBS 桶", out)

    def test_auth_error_message(self):
        rc, out, err = self._run([], [("", "403 Forbidden", 1)])
        self.assertEqual(rc, 1)
        self.assertIn("[错误]", err)
        self.assertIn("IAM", err)

    def test_missing_ak_sk_error_message(self):
        rc, out, err = self._run([], [("", "Please set ak, sk and endpoint", 3)])
        self.assertEqual(rc, 1)
        self.assertIn("AK/SK", err)

    def test_hcloud_not_installed(self):
        with mock.patch("list_obs_buckets.list_buckets_via_sdk",
                        side_effect=ConfigError("huaweicloudsdkobs 未安装")):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 1)
        self.assertIn("未安装", err)

    def test_hcloud_missing_falls_back_to_sdk(self):
        with mock.patch("list_obs_buckets.list_buckets_via_sdk",
                        return_value=[{"name": "sdk-bucket"}]):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 0)
        self.assertIn("sdk-bucket", out)

    def test_write_intent_operation_blocked(self):
        rc, out, err = self._run(["--operation", "CreateBucket"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)

    def test_write_keyword_argv_blocked(self):
        rc, out, err = self._run(["--region", "delete-me"], [])
        self.assertEqual(rc, 1)
        self.assertIn("守卫拦截", err)

    def test_region_with_create_substring_blocked(self):
        rc, out, err = self._run(["--page-size", "10", "--endpoint", "upload.example"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)


class TestErrorHierarchy(unittest.TestCase):
    def test_subclasses(self):
        for exc in (GuardError, ConfigError, AuthError, ApiError):
            self.assertTrue(issubclass(exc, ObsListError))


if __name__ == "__main__":
    unittest.main()