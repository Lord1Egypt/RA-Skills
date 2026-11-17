import json
import os
import subprocess
import sys
import types
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from collect_obs_stats import (  # noqa: E402
    ALLOWED_OPERATION,
    ApiError,
    AuthError,
    ConfigError,
    GuardError,
    ObsStatsError,
    _human_size,
    _normalize_storage_class,
    aggregate,
    build_bucket_command,
    build_object_command,
    classify_hcloud_failure,
    collect_buckets_cli,
    collect_objects_cli,
    collect_stats,
    guard_operation,
    guard_write_intent,
    list_objects_via_sdk,
    main,
    parse_cli_buckets,
    parse_cli_objects,
    render_markdown,
    render_table,
    resolve_listers,
)

CLI_BUCKETS = """Bucket number is: 2

  obs://bucket-alpha  2024-01-02T03:04:05Z  cn-north-4
  obs://bucket-beta   2024-05-06T07:08:09Z  cn-south-1
"""

CLI_OBJECTS = """obs://bucket-alpha/

obs://bucket-alpha/logs/a.txt   1024  2024-01-01T00:00:00Z  STANDARD
obs://bucket-alpha/logs/b.log   2048  2024-01-02T00:00:00Z  WARM
obs://bucket-alpha/logs/sub/     0    2024-01-03T00:00:00Z  STANDARD
"""


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


class TestWriteIntentGuard(unittest.TestCase):
    def test_read_intent_passes(self):
        self.assertFalse(guard_write_intent("--region cn-north-4 --output table"))
        self.assertFalse(guard_write_intent("list buckets show get describe ls"))

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
    def test_bucket_command(self):
        argv = build_bucket_command("cn-north-4")
        self.assertEqual(argv[0], "OBS")
        self.assertEqual(argv[1], "ls")
        self.assertIn("-limit=1000", argv)
        self.assertIn("-e=obs.cn-north-4.myhuaweicloud.com", argv)

    def test_object_command(self):
        argv = build_object_command("my-bucket", prefix="logs",
                                    region="cn-south-1", limit=10)
        self.assertIn("obs://my-bucket/logs/", argv)
        self.assertIn("-limit=10", argv)
        self.assertIn("-e=obs.cn-south-1.myhuaweicloud.com", argv)

    def test_object_command_no_prefix(self):
        argv = build_object_command("my-bucket")
        self.assertIn("obs://my-bucket/", argv)

    def test_no_write_flags_ever_added(self):
        for argv in (build_bucket_command("cn-north-4"),
                     build_object_command("b", prefix="p")):
            for flag in argv:
                self.assertFalse(
                    flag.lower().lstrip("-").startswith(("create", "delete", "put", "upload")))


class TestParseCli(unittest.TestCase):
    def test_buckets(self):
        buckets = parse_cli_buckets(CLI_BUCKETS)
        self.assertEqual([b["name"] for b in buckets], ["bucket-alpha", "bucket-beta"])
        self.assertEqual(buckets[0]["location"], "cn-north-4")
        self.assertEqual(buckets[1]["location"], "cn-south-1")

    def test_buckets_skips_object_lines(self):
        buckets = parse_cli_buckets(CLI_OBJECTS)
        self.assertEqual(buckets, [])

    def test_buckets_dedupe_and_empty(self):
        self.assertEqual(len(parse_cli_buckets("  obs://dup\n  obs://dup\n")), 1)
        self.assertEqual(parse_cli_buckets("Bucket number is: 0\n"), [])

    def test_objects(self):
        objs = parse_cli_objects(CLI_OBJECTS, "bucket-alpha")
        self.assertEqual([o["key"] for o in objs], ["logs/a.txt", "logs/b.log"])
        self.assertEqual(objs[0]["size"], 1024)
        self.assertEqual(objs[0]["storage_class"], "STANDARD")
        self.assertEqual(objs[1]["storage_class"], "WARM")

    def test_objects_filter_bucket(self):
        self.assertEqual(parse_cli_objects(CLI_OBJECTS, "other-bucket"), [])

    def test_storage_class_normalization(self):
        self.assertEqual(_normalize_storage_class(None), "STANDARD")
        self.assertEqual(_normalize_storage_class("Warm"), "WARM")
        self.assertEqual(_normalize_storage_class("deep archive"), "DEEP_ARCHIVE")
        self.assertEqual(_normalize_storage_class("Cold"), "COLD")
        self.assertEqual(_normalize_storage_class("weird"), "UNKNOWN")


class TestHumanSize(unittest.TestCase):
    def test_bytes(self):
        self.assertEqual(_human_size(0), "0 B")
        self.assertEqual(_human_size(512), "512 B")

    def test_kb_mb(self):
        self.assertEqual(_human_size(1024), "1.00 KB")
        self.assertEqual(_human_size(1024 * 1024), "1.00 MB")


class TestClassifyFailure(unittest.TestCase):
    def test_missing_credentials(self):
        err = classify_hcloud_failure(
            "", "Warn: Please set ak, sk and endpoint in the configuration file!", 3)
        self.assertIsInstance(err, ConfigError)

    def test_invalid_ak(self):
        self.assertIsInstance(
            classify_hcloud_failure("", "InvalidAccessKeyId: bad key", 1), AuthError)

    def test_auth_403(self):
        err = classify_hcloud_failure("", "AccessDenied 403 Forbidden", 1)
        self.assertIsInstance(err, AuthError)
        self.assertIn("IAM", str(err))

    def test_generic(self):
        self.assertIsInstance(classify_hcloud_failure("", "boom", 2), ApiError)

    def test_use_error_rc0(self):
        err = classify_hcloud_failure("[USE_ERROR]Invalid parameter: foo", "", 0)
        self.assertIsInstance(err, ApiError)
        self.assertIn("参数错误", str(err))


class TestCollectors(unittest.TestCase):
    def test_bucket_cli_success(self):
        fake = FakeRunner([(CLI_BUCKETS, "", 0)])
        with mock.patch("collect_obs_stats.subprocess.run", fake):
            buckets = collect_buckets_cli("cn-north-4")
        self.assertEqual([b["name"] for b in buckets], ["bucket-alpha", "bucket-beta"])

    def test_bucket_cli_missing_credentials(self):
        fake = FakeRunner([("", "Please set ak, sk and endpoint", 3)])
        with mock.patch("collect_obs_stats.subprocess.run", fake):
            with self.assertRaises(ConfigError):
                collect_buckets_cli("cn-north-4")

    def test_bucket_cli_auth_failure(self):
        fake = FakeRunner([("", "403 Forbidden", 1)])
        with mock.patch("collect_obs_stats.subprocess.run", fake):
            with self.assertRaises(AuthError):
                collect_buckets_cli("cn-north-4")

    def test_bucket_cli_hcloud_missing(self):
        fake = FakeRunner([FileNotFoundError()])
        with mock.patch("collect_obs_stats.subprocess.run", fake):
            with self.assertRaises(ConfigError):
                collect_buckets_cli("cn-north-4")

    def test_objects_cli_success(self):
        fake = FakeRunner([(CLI_OBJECTS, "", 0)])
        with mock.patch("collect_obs_stats.subprocess.run", fake):
            objs = collect_objects_cli("bucket-alpha", "logs", "cn-north-4")
        self.assertEqual(len(objs), 2)


class TestAggregate(unittest.TestCase):
    def _buckets(self):
        return [{"name": "a", "location": "cn-north-4"},
                {"name": "b", "location": "cn-south-1"}]

    def _objects(self):
        return {
            "a": [{"key": "x", "size": 100, "storage_class": "STANDARD"},
                  {"key": "y", "size": 200, "storage_class": "WARM"}],
            "b": [{"key": "z", "size": 50, "storage_class": "STANDARD"}],
        }

    def test_totals(self):
        stats = aggregate(self._buckets(), self._objects(), "cn-north-4")
        self.assertEqual(stats["summary"]["bucket_count"], 2)
        self.assertEqual(stats["summary"]["object_count"], 3)
        self.assertEqual(stats["summary"]["total_size_bytes"], 350)
        self.assertEqual(stats["storage_class_distribution"], {"STANDARD": 2, "WARM": 1})
        self.assertEqual(stats["storage_class_size_bytes"], {"STANDARD": 150, "WARM": 200})
        self.assertEqual(stats["region_distribution"], {"cn-north-4": 1, "cn-south-1": 1})

    def test_region_fallback_when_unknown(self):
        buckets = [{"name": "a"}, {"name": "b"}]
        stats = aggregate(buckets, {"a": [], "b": []}, "cn-north-4")
        self.assertEqual(stats["region_distribution"], {"cn-north-4": 2})
        self.assertTrue(any("区域分布按请求" in w for w in stats["warnings"]))

    def test_empty(self):
        stats = aggregate([], {}, "cn-north-4")
        self.assertEqual(stats["summary"]["object_count"], 0)
        self.assertEqual(stats["summary"]["total_size_bytes"], 0)


class TestCollectStats(unittest.TestCase):
    def _listers(self):
        buckets = [{"name": "b1", "location": "cn-north-4"},
                   {"name": "b2", "location": "cn-north-4"}]
        objects = {
            "b1": [{"key": "k1", "size": 10, "storage_class": "STANDARD"}],
            "b2": [{"key": "k2", "size": 20, "storage_class": "WARM"},
                   {"key": "k3", "size": 30, "storage_class": "STANDARD"}],
        }
        return (lambda region: list(buckets),
                lambda bucket, prefix: (list(objects.get(bucket, [])), False))

    def test_scope_all(self):
        bl, ol = self._listers()
        stats = collect_stats("cn-north-4", bucket_lister=bl, object_lister=ol)
        self.assertEqual(stats["summary"]["bucket_count"], 2)
        self.assertEqual(stats["summary"]["object_count"], 3)
        self.assertEqual(stats["summary"]["total_size_bytes"], 60)

    def test_scope_single_bucket(self):
        bl, ol = self._listers()
        stats = collect_stats("cn-north-4", bucket="b1",
                              bucket_lister=bl, object_lister=ol)
        self.assertEqual(stats["summary"]["bucket_count"], 1)
        self.assertEqual(stats["summary"]["object_count"], 1)
        self.assertEqual(stats["buckets"][0]["name"], "b1")
        self.assertEqual(stats["buckets"][0]["location"], "cn-north-4")

    def test_truncated_flag(self):
        buckets = [{"name": "b1", "location": "cn-north-4"}]

        def object_lister(bucket, prefix):
            return [{"key": "k", "size": 1, "storage_class": "STANDARD"}], True

        stats = collect_stats("cn-north-4",
                              bucket_lister=lambda region: list(buckets),
                              object_lister=object_lister)
        self.assertTrue(stats["truncated"])
        self.assertTrue(any("截断" in w or "上限" in w for w in stats["warnings"]))

    def test_max_objects_cap_truncates(self):
        bl, ol = self._listers()
        stats = collect_stats("cn-north-4", max_objects=1,
                              bucket_lister=bl, object_lister=ol)
        self.assertTrue(stats["truncated"])


def _install_fake_obs_model():
    """Register a minimal huaweicloudsdkobs.v1.model so SDK tests run offline."""
    obs_pkg = types.ModuleType("huaweicloudsdkobs")
    obs_v1 = types.ModuleType("huaweicloudsdkobs.v1")
    model = types.ModuleType("huaweicloudsdkobs.v1.model")

    class ListObjectsRequest:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    model.ListObjectsRequest = ListObjectsRequest
    obs_v1.model = model
    obs_pkg.v1 = obs_v1
    patcher = mock.patch.dict(sys.modules, {
        "huaweicloudsdkobs": obs_pkg,
        "huaweicloudsdkobs.v1": obs_v1,
        "huaweicloudsdkobs.v1.model": model,
    })
    patcher.start()
    return patcher


class TestSdkObjects(unittest.TestCase):
    def setUp(self):
        self._pkg_patcher = _install_fake_obs_model()
        self.addCleanup(self._pkg_patcher.stop)

    class _Resp:
        def __init__(self, payload):
            self._p = payload

        def to_dict(self):
            return self._p

    class _Client:
        def __init__(self, pages):
            self.pages = list(pages)

        def list_objects(self, request):
            return TestSdkObjects._Resp(self.pages.pop(0))

    def test_pagination_and_sizes(self):
        client = self._Client([
            {"contents": [{"key": "logs/a", "size": 100, "storage_class": "STANDARD"},
                          {"key": "logs/sub/", "size": 0}],
             "is_truncated": True, "next_marker": "m1"},
            {"contents": [{"key": "logs/b", "size": 250, "storage_class": "WARM"}],
             "is_truncated": False},
        ])
        objs, truncated = list_objects_via_sdk(client, "b", prefix="logs")
        self.assertEqual([o["key"] for o in objs], ["logs/a", "logs/b"])
        self.assertEqual(objs[0]["size"], 100)
        self.assertEqual(objs[1]["storage_class"], "WARM")
        self.assertFalse(truncated)

    def test_max_objects_truncates(self):
        client = self._Client([
            {"contents": [{"key": "a", "size": 1}, {"key": "b", "size": 1}],
             "is_truncated": True, "next_marker": "m1"},
        ])
        objs, truncated = list_objects_via_sdk(client, "b", max_objects=1)
        self.assertEqual(len(objs), 1)
        self.assertTrue(truncated)


class TestResolveListersFallback(unittest.TestCase):
    def test_auto_falls_back_to_sdk(self):
        with mock.patch("collect_obs_stats.collect_buckets_cli",
                        side_effect=ConfigError("hcloud missing")), \
                mock.patch("collect_obs_stats.list_buckets_via_sdk",
                           return_value=[{"name": "sdk"}]) as sdk:
            bl, _ = resolve_listers("cn-north-4", "auto")
            buckets = bl("cn-north-4")
        self.assertEqual(buckets, [{"name": "sdk"}])
        sdk.assert_called_once()


class TestRender(unittest.TestCase):
    def _stats(self):
        return aggregate(
            [{"name": "a", "location": "cn-north-4"}],
            {"a": [{"key": "x", "size": 1024, "storage_class": "STANDARD"}]},
            "cn-north-4")

    def test_table(self):
        table = render_table(self._stats())
        for frag in ("桶数量", "对象数量", "总容量", "存储类别", "区域", "bucket_count"):
            self.assertIn(frag, table)

    def test_markdown(self):
        md = render_markdown(self._stats())
        self.assertIn("# 华为云 OBS 聚合统计", md)
        self.assertIn("| 桶数量 | 1 |", md)
        self.assertIn("STANDARD", md)


class TestMain(unittest.TestCase):
    def _stats(self):
        return aggregate(
            [{"name": "a", "location": "cn-north-4"}],
            {"a": [{"key": "x", "size": 1024, "storage_class": "STANDARD"}]},
            "cn-north-4")

    def _run(self, argv, stats=None, error=None):
        target = "collect_obs_stats.collect_stats"
        if error is not None:
            patcher = mock.patch(target, side_effect=error)
        else:
            patcher = mock.patch(target, return_value=stats if stats else self._stats())
        with patcher, mock.patch("sys.stdout") as stdout, mock.patch("sys.stderr") as stderr:
            rc = main(argv)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    def test_table_output(self):
        rc, out, err = self._run(["--region", "cn-north-4"])
        self.assertEqual(rc, 0)
        self.assertIn("桶数量", out)
        self.assertEqual(err, "")

    def test_json_output(self):
        rc, out, err = self._run(["--json"])
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual(payload["summary"]["object_count"], 1)
        self.assertEqual(payload["summary"]["total_size_bytes"], 1024)

    def test_output_json_flag(self):
        rc, out, err = self._run(["--output", "json"])
        self.assertEqual(rc, 0)
        self.assertIn("storage_class_distribution", json.loads(out))

    def test_md_output(self):
        rc, out, err = self._run(["--output", "md"])
        self.assertEqual(rc, 0)
        self.assertIn("# 华为云 OBS 聚合统计", out)

    def test_error_message(self):
        rc, out, err = self._run([], error=AuthError("无权限"))
        self.assertEqual(rc, 1)
        self.assertIn("[错误]", err)

    def test_write_intent_blocked(self):
        rc, out, err = self._run(["--bucket", "delete-me"])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)

    def test_operation_blocked(self):
        rc, out, err = self._run(["--operation", "CreateBucket"])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)


class TestErrorHierarchy(unittest.TestCase):
    def test_subclasses(self):
        for exc in (GuardError, ConfigError, AuthError, ApiError):
            self.assertTrue(issubclass(exc, ObsStatsError))


if __name__ == "__main__":
    unittest.main()