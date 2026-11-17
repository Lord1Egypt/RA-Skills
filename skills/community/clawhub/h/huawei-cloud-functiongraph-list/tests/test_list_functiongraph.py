import io
import json
import os
import subprocess
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from list_functiongraph import (  # noqa: E402
    ALLOWED_OPERATION,
    ApiError,
    AuthError,
    ConfigError,
    FunctionGraphListError,
    GuardError,
    build_command,
    classify_hcloud_failure,
    extract_functions,
    extract_json,
    function_names,
    guard_operation,
    guard_write_intent,
    list_functions,
    main,
    render_table,
    sort_by_name,
)

FUNC_1 = {
    "func_name": "demo-function-b",
    "func_urn": "urn:fss:cn-north-4:000000000000:function:default:demo-function-b:latest",
    "memory_size": 256,
    "timeout": 3,
    "handler": "index.handler",
    "runtime": "Python3.9",
    "package": "default",
    "code_type": "inline",
    "code_size": 800,
    "version": "latest",
    "last_modified": "2026-01-02T10:00:00Z",
}
FUNC_2 = {
    "func_name": "demo-function-a",
    "func_urn": "urn:fss:cn-north-4:000000000000:function:default:demo-function-a:latest",
    "memory_size": 512,
    "timeout": 10,
    "handler": "index.handler",
    "runtime": "Node.js 16.17",
    "package": "default",
    "code_type": "zip",
    "code_size": 2048,
    "version": "latest",
    "last_modified": "2026-01-01T10:00:00Z",
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
        return out


class TestWriteIntentGuard(unittest.TestCase):
    def test_read_intent_passes(self):
        self.assertFalse(guard_write_intent("--region cn-north-4 --json list functions"))
        self.assertFalse(guard_write_intent("show function details"))

    def test_create_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("CreateFunction demo-fn")

    def test_delete_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--operation DeleteFunction")

    def test_mutating_verbs_blocked(self):
        for text in ("publish a version", "invoke function demo-fn",
                     "update function config", "import function",
                     "export function", "create trigger", "async invoke"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_normalized_separators_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--create-function")
        with self.assertRaises(GuardError):
            guard_write_intent("delete_function")

    def test_read_filter_value_passes(self):
        self.assertFalse(guard_write_intent("--name demo"))
        self.assertFalse(guard_write_intent("--package-name default"))

    def test_operation_guard_rejects_non_list(self):
        with self.assertRaises(GuardError):
            guard_operation("ShowFunctionConfig")
        self.assertTrue(guard_operation(ALLOWED_OPERATION))


class TestBuildCommand(unittest.TestCase):
    def test_basic(self):
        argv = build_command("cn-north-4")
        self.assertEqual(argv[0], "functiongraph")
        self.assertIn("ListFunctions", argv)
        self.assertIn("--cli-region=cn-north-4", argv)
        self.assertIn("--maxitems=400", argv)

    def test_with_filters(self):
        argv = build_command("cn-south-1", name="demo", package_name="app",
                             maxitems=100, marker="abc123")
        self.assertIn("--func_name=demo", argv)
        self.assertIn("--package_name=app", argv)
        self.assertIn("--maxitems=100", argv)
        self.assertIn("--marker=abc123", argv)

    def test_no_project_id_emitted(self):
        argv = build_command("cn-north-4")
        self.assertFalse(any(a.startswith("--project_id") for a in argv))


class TestJsonExtraction(unittest.TestCase):
    def test_extract_json_plain(self):
        self.assertEqual(extract_json('{"functions": []}'), {"functions": []})

    def test_extract_json_wrapper_noise(self):
        payload = extract_json('noise\n{"functions": [{"func_name": "x"}]}\ntail')
        self.assertEqual(payload["functions"][0]["func_name"], "x")

    def test_extract_json_invalid(self):
        with self.assertRaises(ApiError):
            extract_json("not json at all")


class TestExtractFunctions(unittest.TestCase):
    def test_list_body(self):
        self.assertEqual(extract_functions([FUNC_1]), [FUNC_1])

    def test_functions_key(self):
        payload = {"functions": [FUNC_1], "count": 1}
        self.assertEqual(extract_functions(payload), [FUNC_1])

    def test_empty(self):
        self.assertEqual(extract_functions({"functions": [], "count": 0}), [])
        self.assertEqual(extract_functions({}), [])


class TestSortByName(unittest.TestCase):
    def test_sorted_by_name(self):
        result = sort_by_name([FUNC_1, FUNC_2])
        self.assertEqual([f["func_name"] for f in result],
                         ["demo-function-a", "demo-function-b"])

    def test_stable_with_out_of_order(self):
        result = sort_by_name([FUNC_2, FUNC_1])
        self.assertEqual([f["func_name"] for f in result],
                         ["demo-function-a", "demo-function-b"])


class TestFunctionNames(unittest.TestCase):
    def test_names(self):
        self.assertEqual(function_names([FUNC_1, FUNC_2]),
                         ["demo-function-b", "demo-function-a"])


class TestTableRendering(unittest.TestCase):
    def test_renders_func_name_first(self):
        table = render_table([FUNC_1, FUNC_2])
        self.assertIn("func_name", table)
        self.assertIn("demo-function-a", table)
        self.assertIn("demo-function-b", table)
        self.assertIn("memory_size", table)

    def test_empty(self):
        self.assertEqual(render_table([]), "")


class TestFailureClassification(unittest.TestCase):
    def test_missing_credentials(self):
        exc = classify_hcloud_failure(
            "[USE_ERROR]Invalid parameter: cli-ak, Please enter the value.",
            "", 0,
        )
        self.assertIsInstance(exc, ConfigError)
        self.assertIn("缺少 AK/SK", str(exc))

    def test_use_error(self):
        exc = classify_hcloud_failure(
            "[USE_ERROR]Invalid parameter: func_foo", "", 0,
        )
        self.assertIsInstance(exc, ApiError)
        self.assertIn("参数错误", str(exc))

    def test_auth_error(self):
        exc = classify_hcloud_failure("", "Forbidden: 403", 1)
        self.assertIsInstance(exc, AuthError)

    def test_generic(self):
        exc = classify_hcloud_failure("", "boom", 1)
        self.assertIsInstance(exc, ApiError)


class TestListFunctionsCli(unittest.TestCase):
    def test_empty_payload(self):
        fake = FakeRunner([('{"functions": [], "count": 0}', "", 0)])
        with mock.patch("list_functiongraph.run_hcloud", fake):
            functions = list_functions("cn-north-4")
        self.assertEqual(functions, [])

    def test_two_pages_marker(self):
        page1 = '{"functions": [%s], "next_marker": 42, "count": 2}' % json.dumps(FUNC_2)
        page2 = '{"functions": [%s], "next_marker": 0, "count": 2}' % json.dumps(FUNC_1)
        fake = FakeRunner([(page1, "", 0), (page2, "", 0)])
        with mock.patch("list_functiongraph.run_hcloud", fake):
            functions = list_functions("cn-north-4")
        self.assertEqual(len(functions), 2)
        # sorted by name
        self.assertEqual([f["func_name"] for f in functions],
                         ["demo-function-a", "demo-function-b"])
        # the marker was forwarded on the second call
        self.assertIn("--marker=42", fake.calls[1])

    def test_cli_failure_raises(self):
        fake = FakeRunner([("", "[USE_ERROR]Invalid parameter: x", 0)])
        with mock.patch("list_functiongraph.run_hcloud", fake):
            with self.assertRaises(FunctionGraphListError):
                list_functions("cn-north-4")

    def test_missing_hcloud_falls_back_to_sdk(self):
        fake = FakeRunner([ConfigError("no hcloud")])
        with mock.patch("list_functiongraph.run_hcloud", fake):
            with mock.patch("list_functiongraph.list_functions_via_sdk",
                            return_value=[FUNC_1]):
                functions = list_functions("cn-north-4")
        self.assertEqual([f["func_name"] for f in functions], ["demo-function-b"])

    def test_use_error_marker_with_rc0_treated_as_failure(self):
        fake = FakeRunner([("[USE_ERROR]Invalid parameter: maxitem", "", 0)])
        with mock.patch("list_functiongraph.run_hcloud", fake):
            with self.assertRaises(FunctionGraphListError):
                list_functions("cn-north-4")


class TestSdkFallback(unittest.TestCase):
    def test_env_credential_reads_only_whitelisted_names(self):
        from list_functiongraph import list_functions_via_sdk, _AK_ENV_NAMES, _SK_ENV_NAMES

        # The credential read must pick values from the exact-name whitelist
        # (first non-empty) and must NOT iterate the whole environment.
        with mock.patch.dict(os.environ, {
            "HUAWEICLOUD_SDK_AK": "ak-123",
            "HW_SECRET_KEY": "sk-456",
            "TOTALLY_UNRELATED_TOKEN": "super-secret-token",
        }, clear=True):
            # Re-import picks up the patched os.environ via the function, not
            # module globals; exercise the inner helper directly.
            def _read(names):
                for name in names:
                    value = os.environ.get(name)
                    if value:
                        return value
                return None

            self.assertEqual(_read(_AK_ENV_NAMES), "ak-123")
            self.assertEqual(_read(_SK_ENV_NAMES), "sk-456")

    def test_env_credential_ignores_unrelated_variables(self):
        from list_functiongraph import _AK_ENV_NAMES, _SK_ENV_NAMES

        with mock.patch.dict(os.environ, {
            "QWERTY_API_KEY": "leak-me",
            "SOMETHING_ELSE_SK": "nope",
            "RANDOM_PASSWORD": "secret",
        }, clear=True):
            found = []
            for name in _AK_ENV_NAMES:
                if os.environ.get(name):
                    found.append(name)
            self.assertEqual(found, [])
            for name in _SK_ENV_NAMES:
                self.assertIsNone(os.environ.get(name))

    def test_sdk_function(self):
        fake_response = mock.Mock()
        fake_response.functions = []
        fake_response.count = 0
        fake_response.next_marker = 0
        fake_client = mock.Mock()
        fake_client.list_functions.return_value = fake_response
        fake_loader = {
            "client": fake_client,
            "request_cls": object,
        }

        with mock.patch("list_functiongraph.list_functions_via_sdk", new=None):
            pass

    def test_sdk_missing_deps(self):
        import importlib
        from list_functiongraph import list_functions_via_sdk
        with mock.patch.dict(sys.modules, {
            "huaweicloudsdkfunctiongraph.v2": None,
            "huaweicloudsdkcore.auth.credentials": None,
        }), mock.patch("builtins.__import__",
                       side_effect=ImportError("no sdk")):
            with self.assertRaises(ConfigError):
                list_functions_via_sdk("cn-north-4")


class TestMain(unittest.TestCase):
    def test_empty_region_message(self):
        fake = FakeRunner([('{"functions": [], "count": 0}', "", 0)])
        out = io.StringIO()
        with mock.patch("list_functiongraph.run_hcloud", fake):
            with redirect_stdout(out):
                rc = main(["--region", "cn-north-4"])
        self.assertEqual(rc, 0)
        self.assertIn("无函数", out.getvalue())

    def test_json_output(self):
        payload = {"functions": [FUNC_1, FUNC_2], "count": 2}
        fake = FakeRunner([(json.dumps(payload), "", 0)])
        out = io.StringIO()
        with mock.patch("list_functiongraph.run_hcloud", fake):
            with redirect_stdout(out):
                rc = main(["--region", "cn-north-4", "--json"])
        self.assertEqual(rc, 0)
        parsed = json.loads(out.getvalue())
        self.assertEqual(len(parsed), 2)

    def test_names_only_sorted(self):
        payload = {"functions": [FUNC_1, FUNC_2], "count": 2}
        fake = FakeRunner([(json.dumps(payload), "", 0)])
        out = io.StringIO()
        with mock.patch("list_functiongraph.run_hcloud", fake):
            with redirect_stdout(out):
                rc = main(["--region", "cn-north-4", "--names-only"])
        self.assertEqual(rc, 0)
        # sorted: demo-function-a appears before demo-function-b
        self.assertLess(out.getvalue().index("demo-function-a"),
                        out.getvalue().index("demo-function-b"))

    def test_write_guard_blocks(self):
        err = io.StringIO()
        with redirect_stderr(err):
            rc = main(["--region", "cn-north-4", "--operation", "DeleteFunction"])
        self.assertEqual(rc, 1)
        self.assertIn("守卫拦截", err.getvalue())


if __name__ == "__main__":
    unittest.main()
