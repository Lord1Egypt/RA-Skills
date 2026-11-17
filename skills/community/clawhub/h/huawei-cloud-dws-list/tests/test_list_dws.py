import json
import os
import subprocess
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from list_dws import (  # noqa: E402
    ALLOWED_OPERATION,
    ApiError,
    AuthError,
    ConfigError,
    DwsListError,
    GuardError,
    build_command,
    classify_hcloud_failure,
    cluster_names,
    extract_clusters,
    extract_json,
    filter_clusters,
    guard_operation,
    guard_write_intent,
    list_clusters,
    list_clusters_via_sdk,
    main,
    normalize_cluster,
    paginate,
    render_table,
)

CLUSTER_1 = {
    "id": "dws-0001",
    "name": "dws-demo-01",
    "status": "AVAILABLE",
    "version": "8.1.3",
    "node_type": "dwsk2.xlarge",
    "number_of_node": 3,
    "availability_zone": "cn-north-4a",
    "port": 8000,
    "user_name": "dbadmin",
    "endpoints": [{"connect_info": "dws-demo-01.internal", "jdbc_url": "jdbc:postgresql://x"}],
    "public_ip": {"eip_address": "1.2.3.4", "public_bind_type": "auto"},
    "vpc_id": "vpc-1",
    "enterprise_project_id": "0",
}
CLUSTER_2 = {
    "id": "dws-0002",
    "name": "dws-demo-02",
    "status": "CREATING",
    "version": "8.1.3",
    "node_type": "dwsk2.large",
    "number_of_node": 3,
    "availability_zone": "cn-north-4b",
    "tags": [{"key": "env", "value": "test"}],
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
        self.assertFalse(guard_write_intent("show cluster details"))

    def test_create_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("CreateCluster dws-new")

    def test_delete_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--operation DeleteCluster")

    def test_mutating_verbs_blocked(self):
        for text in ("resize cluster", "restart dws-01", "stop cluster",
                     "update cluster name", "restore snapshot",
                     "upgrade cluster", "reboot node"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_normalized_separators_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--create-cluster")
        with self.assertRaises(GuardError):
            guard_write_intent("update_cluster_name")

    def test_readonly_filter_value_passes(self):
        self.assertFalse(guard_write_intent("--status AVAILABLE"))
        self.assertFalse(guard_write_intent("--name dws-analytics"))

    def test_operation_guard_rejects_non_list(self):
        with self.assertRaises(GuardError):
            guard_operation("ShowCluster")
        self.assertTrue(guard_operation(ALLOWED_OPERATION))


class TestBuildCommand(unittest.TestCase):
    def test_basic(self):
        argv = build_command("cn-north-4")
        self.assertEqual(argv[0], "DWS")
        self.assertEqual(argv[1], "ListClusters")
        self.assertIn("--cli-region=cn-north-4", argv)

    def test_enterprise_project_appended(self):
        argv = build_command("cn-south-1", enterprise_project_id="eps-9")
        self.assertIn("--cli-region=cn-south-1", argv)
        self.assertIn("--enterprise_project_id=eps-9", argv)

    def test_no_unsupported_filters_on_server(self):
        # The real ListClusters API has no name/id/status/limit/offset params —
        # none of these may ever be sent to the CLI.
        argv = build_command("cn-north-4")
        for flag in argv:
            self.assertFalse(flag.startswith(("--name", "--status", "--id",
                                              "--limit", "--offset")))

    def test_no_write_flags_ever_added(self):
        argv = build_command("cn-north-4", enterprise_project_id="eps-9")
        for flag in argv:
            self.assertFalse(flag.lower().lstrip("-").startswith(("create", "delete", "update")))


class TestExtract(unittest.TestCase):
    def test_extract_json_plain(self):
        data = extract_json(json.dumps({"clusters": []}))
        self.assertEqual(data, {"clusters": []})

    def test_extract_json_with_noise(self):
        data = extract_json("WARNING some noise\n{\"a\": 1}\n")
        self.assertEqual(data, {"a": 1})

    def test_extract_json_invalid(self):
        with self.assertRaises(ApiError):
            extract_json("<html>not json</html>")

    def test_extract_clusters_known_keys(self):
        for key in ("clusters", "cluster_list"):
            self.assertEqual(extract_clusters({key: [CLUSTER_1]}), [CLUSTER_1])
        self.assertEqual(extract_clusters([CLUSTER_1]), [CLUSTER_1])
        self.assertEqual(extract_clusters({"count": 0}), [])


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
        # KooCLI usage errors exit rc=0 with [USE_ERROR] on stdout — must be
        # classified as an explicit parameter error, not a JSON parse issue.
        err = classify_hcloud_failure(
            "[USE_ERROR]Invalid parameter: limit\n\n"
            "Run `hcloud DWS ListClusters --help` for details.", "", 0)
        self.assertIsInstance(err, ApiError)
        self.assertIn("参数错误", str(err))
        self.assertIn("--help", str(err))


class TestListClusters(unittest.TestCase):
    def test_single_call(self):
        fake = FakeRunner([(
            json.dumps({"clusters": [CLUSTER_1, CLUSTER_2], "count": 2}), "", 0)])
        with mock.patch("list_dws.subprocess.run", fake):
            clusters = list_clusters("cn-north-4")
        self.assertEqual(clusters, [CLUSTER_1, CLUSTER_2])
        self.assertEqual(len(fake.calls), 1)

    def test_enterprise_project_forwarded(self):
        fake = FakeRunner([(
            json.dumps({"clusters": [CLUSTER_1], "count": 1}), "", 0)])
        with mock.patch("list_dws.subprocess.run", fake):
            list_clusters("cn-north-4", enterprise_project_id="eps-9")
        self.assertIn("--enterprise_project_id=eps-9", fake.calls[0])

    def test_empty_region(self):
        fake = FakeRunner([(json.dumps({"clusters": [], "count": 0}), "", 0)])
        with mock.patch("list_dws.subprocess.run", fake):
            clusters = list_clusters("cn-north-4")
        self.assertEqual(clusters, [])

    def test_use_error_rc0_raises_api_error(self):
        fake = FakeRunner([(
            "[USE_ERROR]Invalid parameter: status\n\n"
            "Run `hcloud DWS ListClusters --help` for details.", "", 0)])
        with mock.patch("list_dws.subprocess.run", fake):
            with self.assertRaises(ApiError) as ctx:
                list_clusters("cn-north-4")
        self.assertIn("参数错误", str(ctx.exception))

    def test_nonzero_exit_403(self):
        fake = FakeRunner([("", "403 Forbidden", 1)])
        with mock.patch("list_dws.subprocess.run", fake):
            with self.assertRaises(AuthError):
                list_clusters("cn-north-4")

    def test_nonzero_exit_credentials(self):
        fake = FakeRunner([("", "ERROR: no AK configured", 1)])
        with mock.patch("list_dws.subprocess.run", fake):
            with self.assertRaises(ConfigError):
                list_clusters("cn-north-4")

    def test_timeout(self):
        fake = FakeRunner([subprocess.TimeoutExpired(cmd="hcloud", timeout=120)])
        with mock.patch("list_dws.subprocess.run", fake):
            with self.assertRaises(ApiError):
                list_clusters("cn-north-4")

    def test_sdk_fallback_when_hcloud_missing(self):
        with mock.patch("list_dws.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_dws.list_clusters_via_sdk",
                           return_value=[CLUSTER_1, CLUSTER_2]) as sdk_mock:
            clusters = list_clusters("cn-north-4", enterprise_project_id="eps-9")
        self.assertEqual(clusters, [CLUSTER_1, CLUSTER_2])
        self.assertEqual(
            sdk_mock.call_args.kwargs.get("enterprise_project_id"), "eps-9")

    def test_sdk_fallback_unavailable_raises_config(self):
        with mock.patch("list_dws.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_dws.list_clusters_via_sdk",
                           side_effect=ConfigError("huaweicloudsdkdws 未安装")):
            with self.assertRaises(ConfigError):
                list_clusters("cn-north-4")

    def test_sdk_request_signature(self):
        # Regression guard: the real huaweicloudsdkdws ListClustersRequest must
        # accept exactly the kwarg the fallback path sends, and reject unknown
        # kwargs such as limit= / status=.
        try:
            from huaweicloudsdkdws.v2 import ListClustersRequest
        except ImportError:
            self.skipTest("huaweicloudsdkdws not installed")
        request = ListClustersRequest(enterprise_project_id="eps-9")
        self.assertEqual(request.enterprise_project_id, "eps-9")
        self.assertIsNone(getattr(request, "limit", None))
        with self.assertRaises(TypeError):
            ListClustersRequest(limit=100)
        with self.assertRaises(TypeError):
            ListClustersRequest(status="AVAILABLE")


class _FakeSdkResponse:
    def __init__(self, clusters, count):
        self.clusters = clusters
        self.count = count


class _FakeSdkCluster:
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


class TestSdkFallback(unittest.TestCase):
    """The SDK fallback must use modules that exist in the official SDK and
    wire credentials from environment variables (no env auto-discovery)."""

    def setUp(self):
        self._captured_credentials = None
        self._captured_region = None
        self._fake_client = mock.Mock()
        self._fake_client.list_clusters.return_value = _FakeSdkResponse(
            [_FakeSdkCluster(CLUSTER_1), _FakeSdkCluster(CLUSTER_2)], 2)
        try:
            import huaweicloudsdkdws.v2 as dws_v2
        except ImportError:
            self.skipTest("huaweicloudsdkdws not installed")
        self._builder_patch = mock.patch.object(
            dws_v2.DwsClient, "new_builder",
            classmethod(lambda cls: _FakeSdkBuilder(self)))
        self._builder_patch.start()
        self.addCleanup(self._builder_patch.stop)

    def _clean_credential_env(self):
        return {
            key: value for key, value in os.environ.items()
            if not key.upper().startswith(("HUAWEI", "HW_", "HWC"))
        }

    def test_official_sdk_imports_resolve(self):
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkdws.v2 import DwsClient, ListClustersRequest
        from huaweicloudsdkdws.v2.region.dws_region import DwsRegion
        for obj in (BasicCredentials, Region, HttpConfig,
                    DwsClient, ListClustersRequest, DwsRegion):
            self.assertTrue(callable(obj), obj)

    def test_sdk_fallback_returns_clusters_with_env_credentials(self):
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak",
                   HUAWEI_SECRET_KEY="test-sk")
        with mock.patch.dict(os.environ, env, clear=True):
            clusters = list_clusters_via_sdk("cn-north-4")
        self.assertEqual(clusters, [CLUSTER_1, CLUSTER_2])
        credentials = self._captured_credentials
        self.assertIsNotNone(credentials)
        self.assertEqual(getattr(credentials, "ak", None), "test-ak")
        self.assertEqual(getattr(credentials, "sk", None), "test-sk")
        self.assertEqual(getattr(self._captured_region, "id", None), "cn-north-4")

    def test_sdk_fallback_missing_env_credentials_raises_config(self):
        with mock.patch.dict(os.environ, self._clean_credential_env(),
                             clear=True):
            with self.assertRaises(ConfigError) as ctx:
                list_clusters_via_sdk("cn-north-4")
        message = str(ctx.exception)
        self.assertIn("AK/SK", message)
        # Must not mislead the user into thinking the SDK is missing.
        self.assertNotIn("未安装", message)

    def test_sdk_fallback_alternative_env_prefixes(self):
        env = dict(self._clean_credential_env(),
                   HW_ACCESS_KEY="alt-ak", HW_SECRET_KEY="alt-sk")
        with mock.patch.dict(os.environ, env, clear=True):
            list_clusters_via_sdk("cn-north-4")
        self.assertEqual(getattr(self._captured_credentials, "ak", None), "alt-ak")


class TestFilterClusters(unittest.TestCase):
    def test_no_filters_returns_all(self):
        result = filter_clusters([CLUSTER_1, CLUSTER_2])
        self.assertEqual(result, [CLUSTER_1, CLUSTER_2])

    def test_name_substring_case_insensitive(self):
        self.assertEqual(filter_clusters([CLUSTER_1, CLUSTER_2], name="DEMO-01"),
                         [CLUSTER_1])
        self.assertEqual(filter_clusters([CLUSTER_1, CLUSTER_2], name="dws-demo"),
                         [CLUSTER_1, CLUSTER_2])

    def test_status_exact_case_insensitive(self):
        self.assertEqual(filter_clusters([CLUSTER_1, CLUSTER_2], status="available"),
                         [CLUSTER_1])
        self.assertEqual(filter_clusters([CLUSTER_1, CLUSTER_2], status="CREATING"),
                         [CLUSTER_2])

    def test_cluster_id_exact(self):
        self.assertEqual(filter_clusters([CLUSTER_1, CLUSTER_2], cluster_id="dws-0002"),
                         [CLUSTER_2])
        self.assertEqual(filter_clusters([CLUSTER_1, CLUSTER_2], cluster_id="dws-00"),
                         [])

    def test_no_match_returns_empty(self):
        self.assertEqual(filter_clusters([CLUSTER_1, CLUSTER_2], status="FAILED"), [])

    def test_missing_status_field_excluded(self):
        self.assertEqual(filter_clusters([{"id": "dws-x"}], status="AVAILABLE"), [])

    def test_input_not_mutated(self):
        source = [CLUSTER_1, CLUSTER_2]
        filter_clusters(source, status="AVAILABLE")
        self.assertEqual(source, [CLUSTER_1, CLUSTER_2])


class TestPaginate(unittest.TestCase):
    def _many(self, n):
        return [{"id": "dws-%d" % i, "name": "dws-%d" % i} for i in range(n)]

    def test_no_limit_returns_all(self):
        data = self._many(5)
        self.assertEqual(paginate(data, limit=0, offset=0), data)

    def test_limit_only(self):
        data = self._many(5)
        self.assertEqual(paginate(data, limit=2), data[:2])

    def test_offset_only(self):
        data = self._many(5)
        self.assertEqual(paginate(data, offset=2), data[2:])

    def test_limit_and_offset(self):
        data = self._many(5)
        self.assertEqual(paginate(data, limit=2, offset=1), data[1:3])

    def test_offset_beyond_end_returns_empty(self):
        self.assertEqual(paginate(self._many(3), offset=10), [])


class TestNormalizeAndRender(unittest.TestCase):
    def test_normalize_flattens_endpoints_and_public_ip(self):
        flat = normalize_cluster(CLUSTER_1)
        self.assertEqual(flat["endpoint"], "dws-demo-01.internal")
        self.assertEqual(flat["publicIp"], "1.2.3.4")

    def test_normalize_missing_fields(self):
        flat = normalize_cluster({"id": "dws-x"})
        self.assertNotIn("endpoint", flat)
        self.assertNotIn("publicIp", flat)

    def test_table_contains_basic_info(self):
        table = render_table([CLUSTER_1, CLUSTER_2])
        for fragment in ("dws-demo-01", "dws-0001", "AVAILABLE", "8.1.3",
                         "dwsk2.xlarge", "cn-north-4a", "dws-demo-01.internal",
                         "1.2.3.4", "dws-demo-02", "CREATING"):
            self.assertIn(fragment, table)

    def test_names(self):
        self.assertEqual(
            cluster_names([CLUSTER_1, CLUSTER_2]), ["dws-demo-01", "dws-demo-02"])

    def test_names_fallback_to_id(self):
        self.assertEqual(cluster_names([{"id": "dws-9"}]), ["dws-9"])


class TestMain(unittest.TestCase):
    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("list_dws.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            rc = main(argv)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    def test_table_output(self):
        rc, out, err = self._run(
            ["--region", "cn-north-4"],
            [(json.dumps({"clusters": [CLUSTER_1, CLUSTER_2], "count": 2}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("DWS 集群列表", out)
        self.assertIn("dws-demo-01", out)
        self.assertIn("AVAILABLE", out)
        self.assertEqual(err, "")

    def test_json_output(self):
        rc, out, err = self._run(
            ["--json"],
            [(json.dumps({"clusters": [CLUSTER_1], "count": 1}), "", 0)])
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual(payload, [CLUSTER_1])

    def test_names_only_output(self):
        rc, out, err = self._run(
            ["--names-only"],
            [(json.dumps({"clusters": [CLUSTER_1, CLUSTER_2], "count": 2}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("dws-demo-01", out)
        self.assertIn("dws-demo-02", out)
        self.assertNotIn("node_type", out)

    def test_empty_clusters_message(self):
        rc, out, err = self._run(
            ["--region", "cn-south-1"],
            [(json.dumps({"clusters": [], "count": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("无 DWS 集群", out)
        self.assertIn("cn-south-1", out)

    def test_empty_with_filter_message(self):
        rc, out, _ = self._run(
            ["--status", "AVAILABLE"],
            [(json.dumps({"clusters": [], "count": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("status=AVAILABLE", out)

    def test_name_filter_main(self):
        # --name filters client-side; the CLI argv never carries --name.
        fake = FakeRunner([
            (json.dumps({"clusters": [CLUSTER_1, CLUSTER_2], "count": 2}), "", 0)])
        with mock.patch("list_dws.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr"):
            rc = main(["--name", "demo-01"])
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        self.assertEqual(rc, 0)
        self.assertIn("dws-demo-01", out)
        self.assertNotIn("dws-demo-02", out)
        for call in fake.calls:
            self.assertFalse(any("--name" in part for part in call))

    def test_limit_pagination_main(self):
        rc, out, err = self._run(
            ["--json", "--limit", "1"],
            [(json.dumps({"clusters": [CLUSTER_1, CLUSTER_2], "count": 2}), "", 0)])
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual(payload, [CLUSTER_1])

    def test_offset_pagination_main(self):
        rc, out, err = self._run(
            ["--json", "--offset", "1"],
            [(json.dumps({"clusters": [CLUSTER_1, CLUSTER_2], "count": 2}), "", 0)])
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual(payload, [CLUSTER_2])

    def test_empty_json_output(self):
        rc, out, err = self._run(
            ["--json"],
            [(json.dumps({"clusters": [], "count": 0}), "", 0)])
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual(payload, [])

    def test_empty_names_only_output(self):
        rc, out, err = self._run(
            ["--names-only"],
            [(json.dumps({"clusters": [], "count": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("共 0 个", out)
        self.assertNotIn("无 DWS 集群", out)

    def test_auth_error_message(self):
        rc, out, err = self._run([], [("", "403 Forbidden", 1)])
        self.assertEqual(rc, 1)
        self.assertIn("[错误]", err)
        self.assertIn("IAM", err)

    def test_missing_ak_sk_error_message(self):
        rc, out, err = self._run([], [("", "ERROR: cli-ak empty", 1)])
        self.assertEqual(rc, 1)
        self.assertIn("AK/SK", err)

    def test_hcloud_not_installed(self):
        with mock.patch("list_dws.list_clusters_via_sdk",
                        side_effect=ConfigError("huaweicloudsdkdws 未安装")):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 1)
        self.assertIn("未安装", err)

    def test_hcloud_missing_falls_back_to_sdk(self):
        with mock.patch("list_dws.list_clusters_via_sdk",
                        return_value=[CLUSTER_1]):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 0)
        self.assertIn("dws-demo-01", out)

    def test_write_intent_argv_blocked(self):
        rc, out, err = self._run(["--operation", "DeleteCluster"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)

    def test_write_keyword_argv_blocked(self):
        rc, out, err = self._run(["--name", "restart-me"], [])
        self.assertEqual(rc, 1)
        self.assertIn("守卫拦截", err)

    def test_status_write_word_blocked(self):
        rc, out, err = self._run(["--status", "deleting-now"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)


class TestErrorHierarchy(unittest.TestCase):
    def test_subclasses(self):
        for exc in (GuardError, ConfigError, AuthError, ApiError):
            self.assertTrue(issubclass(exc, DwsListError))


if __name__ == "__main__":
    unittest.main()