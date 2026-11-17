import json
import os
import subprocess
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from list_cci import (  # noqa: E402
    ALLOWED_OPERATIONS,
    ApiError,
    AuthError,
    CciListError,
    ConfigError,
    GuardError,
    build_command,
    classify_hcloud_failure,
    collect,
    extract_items,
    extract_json,
    filter_by_name,
    guard_operation,
    guard_text_from_argv,
    guard_write_intent,
    item_summary_lines,
    main,
    next_continue_token,
    normalize_item,
    render_table,
)

NAMESPACE_1 = {
    "apiVersion": "v1",
    "kind": "Namespace",
    "metadata": {
        "name": "default",
        "uid": "ns-uid-1",
        "creationTimestamp": "2024-01-01T00:00:00Z",
        "labels": {"env": "prod"},
    },
    "status": {"phase": "Active"},
}
NAMESPACE_2 = {
    "apiVersion": "v1",
    "kind": "Namespace",
    "metadata": {"name": "test-ns", "uid": "ns-uid-2"},
    "status": {"phase": "Active"},
}
POD_1 = {
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {
        "name": "web-0",
        "namespace": "default",
        "uid": "pod-uid-1",
        "creationTimestamp": "2024-02-01T00:00:00Z",
    },
    "spec": {"nodeName": "node-a",
             "containers": [{"name": "web", "image": "nginx:1.25"}]},
    "status": {"phase": "Running", "podIP": "10.0.0.7"},
}
POD_2 = {
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {"name": "web-1", "namespace": "default", "uid": "pod-uid-2"},
    "spec": {"containers": [{"name": "web", "image": "nginx:1.25"}]},
    "status": {"phase": "Pending"},
}
DEPLOY_1 = {
    "apiVersion": "apps/v1",
    "kind": "Deployment",
    "metadata": {
        "name": "web",
        "namespace": "default",
        "uid": "dep-uid-1",
        "creationTimestamp": "2024-03-01T00:00:00Z",
    },
    "spec": {"replicas": 3},
    "status": {"readyReplicas": 2},
}

NS_LIST = {"apiVersion": "v1", "kind": "NamespaceList", "metadata": {},
           "items": [NAMESPACE_1, NAMESPACE_2]}
POD_LIST = {"apiVersion": "v1", "kind": "PodList", "metadata": {},
            "items": [POD_1, POD_2]}
DEPLOY_LIST = {"apiVersion": "apps/v1", "kind": "DeploymentList",
               "metadata": {}, "items": [DEPLOY_1]}


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
        self.assertFalse(guard_write_intent("--region cn-north-4 --json list cci pods"))
        self.assertFalse(guard_write_intent("show pod details"))

    def test_create_namespace_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("CreateCoreV1Namespace cci-new")

    def test_delete_pod_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--operation DeleteCoreV1NamespacedPod")

    def test_pod_exec_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("ConnectCoreV1PostNamespacedPodExec")

    def test_mutating_verbs_blocked(self):
        for text in ("update deployment", "patch pod", "replace pod",
                     "restart deployment", "scale deployment", "evict pod",
                     "drain node", "delete collection"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_normalized_separators_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--create-namespace")
        with self.assertRaises(GuardError):
            guard_write_intent("delete_pod")

    def test_read_filter_value_passes(self):
        self.assertFalse(guard_write_intent("--name demo-01"))
        self.assertFalse(guard_write_intent("--names-only"))
        self.assertFalse(guard_write_intent("cn-north-4"))

    def test_guard_text_strips_filter_values_keeps_operation(self):
        text = guard_text_from_argv(
            ["--resource", "pod", "--name", "delete-me", "--namespace", "create-ns",
             "--operation=ListCoreV1PodForAllNamespaces"])
        self.assertNotIn("delete-me", text)
        self.assertNotIn("create-ns", text)
        self.assertIn("ListCoreV1PodForAllNamespaces", text)

    def test_operation_guard(self):
        with self.assertRaises(GuardError):
            guard_operation("ShowPod")
        with self.assertRaises(GuardError):
            guard_operation("DeleteCoreV1Namespace")
        self.assertTrue(guard_operation("ListCoreV1Namespace"))
        self.assertTrue(guard_operation("ListCoreV1PodForAllNamespaces"))

    def test_operation_resource_mismatch(self):
        with self.assertRaises(GuardError):
            guard_operation("ListCoreV1Namespace", resource="pod")


class TestBuildCommand(unittest.TestCase):
    def test_namespace_default(self):
        argv = build_command("namespace", "cn-north-4")
        self.assertEqual(argv[0], "CCI")
        self.assertEqual(argv[1], "ListCoreV1Namespace")
        self.assertIn("--cli-region=cn-north-4", argv)
        self.assertIn("--limit=100", argv)
        self.assertNotIn("--namespace=default", argv)

    def test_pod_all_namespaces(self):
        argv = build_command("pod", "cn-north-4")
        self.assertEqual(argv[1], "ListCoreV1PodForAllNamespaces")

    def test_pod_namespaced(self):
        argv = build_command("pod", "cn-north-4", namespace="default")
        self.assertEqual(argv[1], "ListCoreV1NamespacedPod")
        self.assertIn("--namespace=default", argv)

    def test_deployment_variants(self):
        self.assertEqual(build_command("deployment", "cn-north-4")[1],
                         "ListAppsV1DeploymentForAllNamespaces")
        self.assertEqual(
            build_command("deployment", "cn-north-4", namespace="default")[1],
            "ListAppsV1NamespacedDeployment")

    def test_continue_token(self):
        argv = build_command("pod", "cn-north-4", continue_token="tok-2")
        self.assertIn("--continue=tok-2", argv)

    def test_no_write_flags_ever_added(self):
        for resource in ("namespace", "pod", "deployment"):
            for flag in build_command(resource, "cn-north-4"):
                self.assertFalse(flag.lower().lstrip("-").startswith(
                    ("create", "delete", "update", "patch", "replace")))


class TestExtract(unittest.TestCase):
    def test_extract_json_plain(self):
        self.assertEqual(extract_json(json.dumps({"items": []})), {"items": []})

    def test_extract_json_with_noise(self):
        self.assertEqual(extract_json("WARNING noise\n{\"a\": 1}\n"), {"a": 1})

    def test_extract_json_bare_array(self):
        self.assertEqual(extract_json("[{\"a\": 1}]"), [{"a": 1}])

    def test_extract_json_invalid(self):
        with self.assertRaises(ApiError):
            extract_json("<html>not json</html>")

    def test_extract_items(self):
        self.assertEqual(extract_items({"items": [POD_1]}), [POD_1])
        self.assertEqual(extract_items([POD_1]), [POD_1])
        self.assertEqual(extract_items({"metadata": {}}), [])

    def test_next_continue_token(self):
        self.assertIsNone(next_continue_token({"metadata": {}}))
        self.assertEqual(next_continue_token({"metadata": {"continue": "tok"}}), "tok")
        self.assertIsNone(next_continue_token({"metadata": {"continue": ""}}))
        self.assertIsNone(next_continue_token(None))


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
            "[USE_ERROR]Invalid parameter: limit\n\n"
            "Run `hcloud CCI ListCoreV1Namespace --help` for details.", "", 0)
        self.assertIsInstance(err, ApiError)
        self.assertIn("参数错误", str(err))
        self.assertIn("--help", str(err))


class TestCollect(unittest.TestCase):
    def test_single_call(self):
        fake = FakeRunner([(json.dumps(NS_LIST), "", 0)])
        with mock.patch("list_cci.subprocess.run", fake):
            items = collect("namespace", "cn-north-4")
        self.assertEqual(items, [NAMESPACE_1, NAMESPACE_2])
        self.assertEqual(len(fake.calls), 1)
        self.assertIn("CCI", fake.calls[0])
        self.assertIn("ListCoreV1Namespace", fake.calls[0])

    def test_empty(self):
        fake = FakeRunner([(json.dumps({"items": []}), "", 0)])
        with mock.patch("list_cci.subprocess.run", fake):
            self.assertEqual(collect("namespace", "cn-north-4"), [])

    def test_continue_paging(self):
        page1 = {"metadata": {"continue": "tok-2"}, "items": [POD_1]}
        page2 = {"metadata": {}, "items": [POD_2]}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("list_cci.subprocess.run", fake):
            items = collect("pod", "cn-north-4")
        self.assertEqual(items, [POD_1, POD_2])
        self.assertEqual(len(fake.calls), 2)
        self.assertIn("--continue=tok-2", fake.calls[1])

    def test_name_filter_client_side(self):
        fake = FakeRunner([(json.dumps(NS_LIST), "", 0)])
        with mock.patch("list_cci.subprocess.run", fake):
            items = collect("namespace", "cn-north-4", name="TEST-Ns")
        self.assertEqual(items, [NAMESPACE_2])

    def test_namespaced_command(self):
        fake = FakeRunner([(json.dumps(POD_LIST), "", 0)])
        with mock.patch("list_cci.subprocess.run", fake):
            collect("pod", "cn-north-4", namespace="default")
        self.assertIn("ListCoreV1NamespacedPod", fake.calls[0])
        self.assertIn("--namespace=default", fake.calls[0])

    def test_label_selector_forwarded(self):
        fake = FakeRunner([(json.dumps(POD_LIST), "", 0)])
        with mock.patch("list_cci.subprocess.run", fake):
            collect("pod", "cn-north-4", label_selector="app=web")
        self.assertIn("--labelSelector=app=web", fake.calls[0])

    def test_use_error_rc0_raises(self):
        fake = FakeRunner([("[USE_ERROR]Invalid parameter: x\n"
                            "Run `hcloud CCI ListCoreV1Namespace --help` for details.",
                            "", 0)])
        with mock.patch("list_cci.subprocess.run", fake):
            with self.assertRaises(ApiError) as ctx:
                collect("namespace", "cn-north-4")
        self.assertIn("参数错误", str(ctx.exception))

    def test_nonzero_exit_403(self):
        fake = FakeRunner([("", "403 Forbidden", 1)])
        with mock.patch("list_cci.subprocess.run", fake):
            with self.assertRaises(AuthError):
                collect("namespace", "cn-north-4")

    def test_nonzero_exit_credentials(self):
        fake = FakeRunner([("", "ERROR: no AK configured", 1)])
        with mock.patch("list_cci.subprocess.run", fake):
            with self.assertRaises(ConfigError):
                collect("namespace", "cn-north-4")

    def test_timeout(self):
        fake = FakeRunner([subprocess.TimeoutExpired(cmd="hcloud", timeout=120)])
        with mock.patch("list_cci.subprocess.run", fake):
            with self.assertRaises(ApiError):
                collect("namespace", "cn-north-4")

    def test_hcloud_missing_raises_config_no_fallback(self):
        fake = FakeRunner([FileNotFoundError()])
        with mock.patch("list_cci.subprocess.run", fake):
            with self.assertRaises(ConfigError) as ctx:
                collect("namespace", "cn-north-4")
        self.assertIn("KooCLI", str(ctx.exception))


class TestFiltering(unittest.TestCase):
    def test_name_substring_case_insensitive(self):
        self.assertEqual(filter_by_name([NAMESPACE_1, NAMESPACE_2], name="DEFAULT"),
                         [NAMESPACE_1])

    def test_no_filter_returns_all(self):
        self.assertEqual(filter_by_name([NAMESPACE_1, NAMESPACE_2], name=None), [NAMESPACE_1, NAMESPACE_2])


class TestNormalizeAndRender(unittest.TestCase):
    def test_normalize_namespace(self):
        flat = normalize_item(NAMESPACE_1, "namespace")
        self.assertEqual(flat["name"], "default")
        self.assertEqual(flat["status"], "Active")
        self.assertEqual(flat["creation_timestamp"], "2024-01-01T00:00:00Z")
        self.assertEqual(flat["labels"], "env=prod")

    def test_normalize_pod(self):
        flat = normalize_item(POD_1, "pod")
        self.assertEqual(flat["name"], "web-0")
        self.assertEqual(flat["namespace"], "default")
        self.assertEqual(flat["status"], "Running")
        self.assertEqual(flat["pod_ip"], "10.0.0.7")
        self.assertEqual(flat["node_name"], "node-a")
        self.assertEqual(flat["images"], "nginx:1.25")

    def test_normalize_deployment(self):
        flat = normalize_item(DEPLOY_1, "deployment")
        self.assertEqual(flat["replicas"], 3)
        self.assertEqual(flat["ready_replicas"], 2)
        self.assertEqual(flat["status"], "2/3")

    def test_normalize_missing_labels_dash(self):
        flat = normalize_item(NAMESPACE_2, "namespace")
        self.assertNotIn("labels", flat)

    def test_table_contains_key_fields(self):
        table = render_table([POD_1, POD_2], "pod")
        for fragment in ("web-0", "default", "Running", "10.0.0.7", "nginx:1.25"):
            self.assertIn(fragment, table)

    def test_names_summary_namespaced(self):
        self.assertEqual(item_summary_lines([POD_1, POD_2], "pod"),
                         ["default/web-0", "default/web-1"])
        self.assertEqual(item_summary_lines([NAMESPACE_1], "namespace"), ["default"])


class TestMain(unittest.TestCase):
    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("list_cci.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            rc = main(argv)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    def test_table_output_default_namespace(self):
        rc, out, err = self._run(["--region", "cn-north-4"],
                                 [(json.dumps(NS_LIST), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("CCI 命名空间", out)
        self.assertIn("default", out)
        self.assertIn("Active", out)
        self.assertEqual(err, "")

    def test_pod_table_output(self):
        rc, out, err = self._run(["--resource", "pod"],
                                 [(json.dumps(POD_LIST), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("CCI Pod", out)
        self.assertIn("Running", out)

    def test_json_output(self):
        rc, out, err = self._run(["--json"], [(json.dumps(POD_LIST), "", 0)])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out), [POD_1, POD_2])

    def test_names_only_output(self):
        rc, out, err = self._run(["--resource", "pod", "--names-only"],
                                 [(json.dumps(POD_LIST), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("default/web-0", out)
        self.assertNotIn("nginx", out)

    def test_name_filter_applied(self):
        rc, out, err = self._run(["--name", "test-ns"],
                                 [(json.dumps(NS_LIST), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("test-ns", out)
        self.assertNotIn("default", out)

    def test_empty_message(self):
        rc, out, err = self._run(
            ["--resource", "pod", "--namespace", "nope"],
            [(json.dumps({"items": []}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("无 CCI 资源", out)
        self.assertIn("namespace=nope", out)

    def test_empty_json_output(self):
        rc, out, err = self._run(["--json"],
                                 [(json.dumps({"items": []}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out), [])

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
        rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 1)
        self.assertIn("KooCLI", err)

    def test_write_intent_operation_blocked(self):
        rc, out, err = self._run(["--operation", "DeleteCoreV1NamespacedPod"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)

    def test_page_size_out_of_range(self):
        rc, out, err = self._run(["--page-size", "5000"], [])
        self.assertEqual(rc, 1)
        self.assertIn("page-size", err)


class TestErrorHierarchy(unittest.TestCase):
    def test_subclasses(self):
        for exc in (GuardError, ConfigError, AuthError, ApiError):
            self.assertTrue(issubclass(exc, CciListError))

    def test_allowed_operations(self):
        self.assertEqual(len(ALLOWED_OPERATIONS), 5)


if __name__ == "__main__":
    unittest.main()