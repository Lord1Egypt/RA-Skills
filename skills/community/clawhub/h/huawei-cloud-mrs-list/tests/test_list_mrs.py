import json
import os
import subprocess
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from list_mrs import (  # noqa: E402
    ALLOWED_OPERATION,
    ApiError,
    AuthError,
    ConfigError,
    GuardError,
    MrsListError,
    build_command,
    classify_hcloud_failure,
    cluster_names,
    extract_clusters,
    extract_json,
    guard_operation,
    guard_write_intent,
    list_clusters,
    main,
    render_table,
)

CLUSTER_1 = {
    "clusterId": "c-0001",
    "clusterName": "mrs-demo-01",
    "clusterState": "running",
    "billingType": "billing",
    "version": "MRS 3.1.0",
    "masterNodeNum": 2,
    "coreNodeNum": 3,
    "enterpriseProjectId": "0",
}
CLUSTER_2 = {
    "clusterId": "c-0002",
    "clusterName": "mrs-demo-02",
    "clusterState": "terminated",
    "billingType": "billing",
    "version": "MRS 2.1.0",
    "tags": {"env": "test"},
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
        self.assertFalse(guard_write_intent("--region cn-north-4 --json list clusters"))
        self.assertFalse(guard_write_intent("show cluster details nodes jobs"))

    def test_create_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("CreateCluster mrs-new")

    def test_delete_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--operation DeleteCluster")

    def test_scale_and_restart_blocked(self):
        for text in ("scale-out the cluster", "restart mrs-01", "terminate cluster"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_normalized_separators_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--create-cluster")
        with self.assertRaises(GuardError):
            guard_write_intent("update_cluster_name")

    def test_operation_guard_rejects_non_list(self):
        with self.assertRaises(GuardError):
            guard_operation("ShowClusterDetails")
        self.assertTrue(guard_operation(ALLOWED_OPERATION))


class TestBuildCommand(unittest.TestCase):
    def test_basic(self):
        argv = build_command("cn-north-4")
        self.assertEqual(argv[0], "MRS")
        self.assertEqual(argv[1], "ListClusters")
        self.assertIn("--cli-region=cn-north-4", argv)
        self.assertIn("--pageSize=10", argv)
        self.assertIn("--currentPage=1", argv)

    def test_filters_appended(self):
        argv = build_command("cn-south-1", cluster_state="running",
                             cluster_name="mrs-01", page_size=5, current_page=2)
        self.assertIn("--clusterState=running", argv)
        self.assertIn("--clusterName=mrs-01", argv)
        self.assertIn("--pageSize=5", argv)
        self.assertIn("--currentPage=2", argv)

    def test_no_write_flags_ever_added(self):
        argv = build_command("cn-north-4", cluster_state="failed")
        for flag in argv:
            self.assertFalse(flag.lower().lstrip("-").startswith(("create", "delete", "update")))


class TestExtract(unittest.TestCase):
    def test_extract_json_plain(self):
        data = extract_json(json.dumps({"cluster_infos": []}))
        self.assertEqual(data, {"cluster_infos": []})

    def test_extract_json_with_noise(self):
        data = extract_json("WARNING some noise\n{\"a\": 1}\n")
        self.assertEqual(data, {"a": 1})

    def test_extract_json_invalid(self):
        with self.assertRaises(ApiError):
            extract_json("<html>not json</html>")

    def test_extract_clusters_known_keys(self):
        for key in ("cluster_infos", "clusters"):
            self.assertEqual(extract_clusters({key: [CLUSTER_1]}), [CLUSTER_1])
        self.assertEqual(extract_clusters([CLUSTER_1]), [CLUSTER_1])
        self.assertEqual(extract_clusters({"total": 0}), [])


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
        self.assertIn("403", str(err))

    def test_auth_unauthorized(self):
        err = classify_hcloud_failure("", "Unauthorized: invalid AK", 1)
        self.assertIsInstance(err, AuthError)

    def test_generic_api_error(self):
        err = classify_hcloud_failure("", "boom", 2)
        self.assertIsInstance(err, ApiError)

    def test_hcloud_binary_missing(self):
        with mock.patch("list_mrs.subprocess.run", FakeRunner([FileNotFoundError()])):
            with self.assertRaises(ConfigError):
                list_clusters("cn-north-4")

    def test_timeout(self):
        with mock.patch("list_mrs.subprocess.run",
                        FakeRunner([subprocess.TimeoutExpired(cmd="hcloud", timeout=120)])):
            with self.assertRaises(ApiError):
                list_clusters("cn-north-4")


class TestListClusters(unittest.TestCase):
    def test_single_page(self):
        fake = FakeRunner([(
            json.dumps({"cluster_infos": [CLUSTER_1, CLUSTER_2], "total": 2}), "", 0)])
        with mock.patch("list_mrs.subprocess.run", fake):
            clusters = list_clusters("cn-north-4")
        self.assertEqual(clusters, [CLUSTER_1, CLUSTER_2])
        self.assertEqual(len(fake.calls), 1)

    def test_pagination_via_total(self):
        page1 = {"cluster_infos": [CLUSTER_1], "total": 2}
        page2 = {"cluster_infos": [CLUSTER_2], "total": 2}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("list_mrs.subprocess.run", fake):
            clusters = list_clusters("cn-north-4", page_size=1)
        self.assertEqual(clusters, [CLUSTER_1, CLUSTER_2])
        self.assertEqual(len(fake.calls), 2)
        self.assertIn("--currentPage=2", fake.calls[1])

    def test_pagination_via_full_page_without_total(self):
        page1 = {"cluster_infos": [CLUSTER_1]}
        page2 = {"cluster_infos": []}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("list_mrs.subprocess.run", fake):
            clusters = list_clusters("cn-north-4", page_size=1)
        self.assertEqual(clusters, [CLUSTER_1])

    def test_is_finished_stops(self):
        fake = FakeRunner([(
            json.dumps({"cluster_infos": [CLUSTER_1], "isFinished": True}), "", 0)])
        with mock.patch("list_mrs.subprocess.run", fake):
            clusters = list_clusters("cn-north-4")
        self.assertEqual(clusters, [CLUSTER_1])
        self.assertEqual(len(fake.calls), 1)

    def test_empty_region(self):
        fake = FakeRunner([(json.dumps({"cluster_infos": [], "total": 0}), "", 0)])
        with mock.patch("list_mrs.subprocess.run", fake):
            clusters = list_clusters("cn-north-4")
        self.assertEqual(clusters, [])

    def test_cluster_state_filter_forwarded(self):
        fake = FakeRunner([(json.dumps({"cluster_infos": [CLUSTER_1], "total": 1}), "", 0)])
        with mock.patch("list_mrs.subprocess.run", fake):
            list_clusters("cn-north-4", cluster_state="running")
        self.assertTrue(any("--clusterState=running" in " ".join(c) for c in fake.calls))

    def test_nonzero_exit_403(self):
        fake = FakeRunner([("", "403 Forbidden", 1)])
        with mock.patch("list_mrs.subprocess.run", fake):
            with self.assertRaises(AuthError):
                list_clusters("cn-north-4")

    def test_nonzero_exit_credentials(self):
        fake = FakeRunner([("", "ERROR: no AK configured", 1)])
        with mock.patch("list_mrs.subprocess.run", fake):
            with self.assertRaises(ConfigError):
                list_clusters("cn-north-4")


class TestRender(unittest.TestCase):
    def test_table_contains_all_fields(self):
        table = render_table([CLUSTER_1, CLUSTER_2])
        for fragment in ("mrs-demo-01", "c-0001", "running", "MRS 3.1.0",
                         "mrs-demo-02", "terminated", "enterpriseProjectId", "tags"):
            self.assertIn(fragment, table)

    def test_table_missing_value_dash(self):
        table = render_table([CLUSTER_1, CLUSTER_2])
        # CLUSTER_1 lacks "tags" — rendered as '-'
        self.assertIn("-", table)

    def test_names(self):
        self.assertEqual(
            cluster_names([CLUSTER_1, CLUSTER_2]), ["mrs-demo-01", "mrs-demo-02"])

    def test_names_fallback_to_id(self):
        self.assertEqual(cluster_names([{"clusterId": "c-9"}]), ["c-9"])


class TestMain(unittest.TestCase):
    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("list_mrs.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            rc = main(argv)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    def test_table_output(self):
        rc, out, err = self._run(
            ["--region", "cn-north-4"],
            [(json.dumps({"cluster_infos": [CLUSTER_1, CLUSTER_2], "total": 2}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("MRS 集群列表", out)
        self.assertIn("mrs-demo-01", out)
        self.assertIn("running", out)
        self.assertEqual(err, "")

    def test_json_output(self):
        rc, out, err = self._run(
            ["--json"],
            [(json.dumps({"cluster_infos": [CLUSTER_1], "total": 1}), "", 0)])
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual(payload, [CLUSTER_1])

    def test_names_only_output(self):
        rc, out, err = self._run(
            ["--names-only"],
            [(json.dumps({"cluster_infos": [CLUSTER_1, CLUSTER_2], "total": 2}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("mrs-demo-01", out)
        self.assertIn("mrs-demo-02", out)
        self.assertNotIn("clusterState", out)

    def test_empty_clusters_message(self):
        rc, out, err = self._run(
            ["--region", "cn-south-1"],
            [(json.dumps({"cluster_infos": [], "total": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("暂无 MRS 集群", out)
        self.assertIn("cn-south-1", out)

    def test_empty_with_state_filter_message(self):
        rc, out, _ = self._run(
            ["--cluster-state", "running"],
            [(json.dumps({"cluster_infos": [], "total": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("clusterState=running", out)

    def test_empty_json_output(self):
        rc, out, err = self._run(
            ["--json"],
            [(json.dumps({"cluster_infos": [], "total": 0}), "", 0)])
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual(payload, [])

    def test_empty_names_only_output(self):
        rc, out, err = self._run(
            ["--names-only"],
            [(json.dumps({"cluster_infos": [], "total": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("共 0 个", out)
        self.assertNotIn("暂无", out)

    def test_auth_error_message(self):
        rc, out, err = self._run([], [("", "403 Forbidden", 1)])
        self.assertEqual(rc, 1)
        self.assertIn("[错误]", err)
        self.assertIn("403", err)

    def test_missing_ak_sk_error_message(self):
        rc, out, err = self._run([], [("", "ERROR: cli-ak empty", 1)])
        self.assertEqual(rc, 1)
        self.assertIn("AK/SK", err)

    def test_hcloud_not_installed(self):
        rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 1)
        self.assertIn("hcloud", err)

    def test_write_intent_argv_blocked(self):
        rc, out, err = self._run(["--operation", "DeleteCluster"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)

    def test_write_keyword_argv_blocked(self):
        rc, out, err = self._run(["--cluster-name", "restart-me"], [])
        self.assertEqual(rc, 1)
        self.assertIn("守卫拦截", err)

    def test_cluster_state_write_word_blocked(self):
        rc, out, err = self._run(["--cluster-state", "deleting-now"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)


class TestErrorHierarchy(unittest.TestCase):
    def test_subclasses(self):
        for exc in (GuardError, ConfigError, AuthError, ApiError):
            self.assertTrue(issubclass(exc, MrsListError))


if __name__ == "__main__":
    unittest.main()
