import json
import os
import subprocess
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from list_codearts import (  # noqa: E402
    ALLOWED_OPERATIONS,
    ApiError,
    AuthError,
    CodeArtsListError,
    ConfigError,
    GuardError,
    ProjectResolutionError,
    RESOURCES,
    _build_sdk_request,
    build_command,
    classify_hcloud_failure,
    extract_items,
    extract_json,
    filter_by_name,
    filter_by_status,
    guard_operation,
    guard_text_from_argv,
    guard_write_intent,
    item_summary_lines,
    list_codearts,
    list_resource_via_sdk,
    main,
    normalize_item,
    render_table,
    resolve_project_id,
)

PROJECT_1 = {
    "project_id": "p-0001", "project_name": "proj-alpha",
    "project_type": "scrum", "created_time": 1700000000000,
}
PROJECT_2 = {
    "project_id": "p-0002", "project_name": "proj-beta",
    "project_type": "xboard", "created_time": 1700000001000,
}
REPO_1 = {"id": 101, "name": "repo-alpha", "visibility": "private", "status": "0"}
REPO_2 = {"id": 102, "name": "repo-beta", "visibility": "public", "status": "1"}
PIPELINE_1 = {
    "pipeline_id": "pl-1", "name": "pipe-alpha", "project_name": "proj-alpha",
    "latest_run": {"status": "COMPLETED"}, "create_time": 1700000002000,
}
PIPELINE_2 = {"pipeline_id": "pl-2", "name": "pipe-beta", "status": "RUNNING"}
DEPLOY_1 = {"id": "d-1", "name": "task-alpha", "state": "failed", "project_name": "proj-alpha"}
DEPLOY_2 = {"id": "d-2", "name": "task-beta", "state": "initialized", "project_name": "proj-alpha"}


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
        for text in ("--region cn-north-4 --resource pipelines list",
                     "list projects repositories pipelines",
                     "show get describe search archive"):
            self.assertFalse(guard_write_intent(text))

    def test_create_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("CreateProjectV4")

    def test_delete_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--operation DeleteRepository")

    def test_mutating_verbs_blocked(self):
        for text in ("RunPipeline", "StartDeployTask", "StopPipelineNew",
                     "UpdateProjectV4", "MergeMergeRequest", "CreatePipelineNew"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_normalized_separators_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--create-project")
        with self.assertRaises(GuardError):
            guard_write_intent("delete_repository")

    def test_resource_values_not_blocked(self):
        # --resource values and other selectors are read data, never scanned
        self.assertFalse(guard_write_intent("deploy-tasks"))
        self.assertFalse(guard_write_intent("pipelines"))

    def test_filter_values_not_blocked(self):
        # Filter/selector *values* are read data; the guard only scans flag
        # names and positional tokens (stripped via guard_text_from_argv).
        self.assertFalse(guard_write_intent(
            guard_text_from_argv(["--name", "restart-me", "--status", "running"])))

    def test_operation_guard(self):
        self.assertTrue(guard_operation("ListProjectsV4", "ListProjectsV4"))
        with self.assertRaises(GuardError):
            guard_operation("ListProjectsV4", "ListPipelines")
        with self.assertRaises(GuardError):
            guard_operation("DeleteProjectV4", "DeleteProjectV4")

    def test_guard_text_strips_values(self):
        text = guard_text_from_argv(
            ["--resource", "deploy-tasks", "--name", "restart-me",
             "--project-id", "delete-it", "--region", "cn-north-4", "--json"])
        self.assertNotIn("restart-me", text)
        self.assertNotIn("delete-it", text)
        self.assertNotIn("deploy-tasks", text)
        self.assertIn("--json", text)


class TestBuildCommand(unittest.TestCase):
    def test_projects(self):
        argv = build_command("projects", "cn-north-4", limit=50, offset=0)
        self.assertEqual(argv[0], "ProjectMan")
        self.assertEqual(argv[1], "ListProjectsV4")
        self.assertIn("--cli-region=cn-north-4", argv)
        self.assertIn("--limit=50", argv)
        self.assertIn("--offset=0", argv)

    def test_projects_name_uses_search(self):
        argv = build_command("projects", "cn-north-4", name="alpha")
        self.assertIn("--search=alpha", argv)
        self.assertFalse(any(p.startswith("--name=") for p in argv))

    def test_repos(self):
        argv = build_command("repos", "cn-north-4", project_id="p-1",
                             name="alpha", limit=100, offset=20)
        self.assertEqual(argv[:2], ["CodeArtsRepo", "ListProjectRepositories"])
        self.assertIn("--project_id=p-1", argv)
        self.assertIn("--search=alpha", argv)
        self.assertIn("--offset=20", argv)

    def test_pipelines(self):
        argv = build_command("pipelines", "cn-north-4", project_id="p-1",
                             name="alpha", limit=100, offset=0)
        self.assertEqual(argv[:2], ["CodeArtsPipeline", "ListPipelines"])
        self.assertIn("--project_id=p-1", argv)
        self.assertIn("--name=alpha", argv)
        self.assertIn("--limit=100", argv)
        self.assertIn("--offset=0", argv)

    def test_deploy_tasks_page_based(self):
        argv = build_command("deploy-tasks", "cn-north-4", project_id="p-1",
                             name="alpha", limit=100, offset=100)
        self.assertEqual(argv[:2], ["CodeArtsDeploy", "ListDeployTasks"])
        self.assertIn("--page=2", argv)
        self.assertIn("--size=100", argv)
        # ListDeployTasks has no name query parameter -> never forwarded
        self.assertFalse(any(p.startswith("--name=") for p in argv))
        self.assertFalse(any(p.startswith("--search") for p in argv))
        self.assertFalse(any(p.startswith("--offset") for p in argv))

    def test_no_write_flags(self):
        for resource in RESOURCES:
            argv = build_command(resource, "cn-north-4", project_id="p-1")
            for flag in argv:
                stripped = flag.lower().lstrip("-")
                self.assertFalse(stripped.startswith(("create", "delete", "update")))


class TestExtract(unittest.TestCase):
    def test_extract_json_object(self):
        self.assertEqual(extract_json('{"a": 1}'), {"a": 1})

    def test_extract_json_array(self):
        self.assertEqual(extract_json('[{"id": 1}]'), [{"id": 1}])

    def test_extract_json_with_noise(self):
        self.assertEqual(extract_json('WARNING\n[{"id": 1}]\n'), [{"id": 1}])
        self.assertEqual(extract_json('INFO\n{"a": 1}\n'), {"a": 1})

    def test_extract_json_invalid(self):
        with self.assertRaises(ApiError):
            extract_json("<html>not json</html>")

    def test_extract_items_per_resource(self):
        self.assertEqual(extract_items({"projects": [PROJECT_1]}, "projects"), [PROJECT_1])
        self.assertEqual(extract_items([REPO_1], "repos"), [REPO_1])
        self.assertEqual(extract_items({"pipelines": [PIPELINE_1]}, "pipelines"), [PIPELINE_1])
        self.assertEqual(extract_items({"result": [DEPLOY_1]}, "deploy-tasks"), [DEPLOY_1])

    def test_extract_items_generic_and_empty(self):
        self.assertEqual(extract_items({"data": [REPO_1]}, "repos"), [REPO_1])
        self.assertEqual(extract_items({"total": 0}, "projects"), [])
        self.assertEqual(extract_items(None, "projects"), [])


class TestClassifyFailure(unittest.TestCase):
    def test_missing_credentials(self):
        err = classify_hcloud_failure(
            "", "ERROR: cli-ak is empty, please run hcloud configure", 1)
        self.assertIsInstance(err, ConfigError)
        self.assertIn("AK/SK", str(err))

    def test_missing_profile(self):
        err = classify_hcloud_failure(
            "[USE_ERROR]The configuration file does not contain profile.", "", 0)
        self.assertIsInstance(err, ApiError)
        self.assertIn("参数错误", str(err))

    def test_auth_403(self):
        err = classify_hcloud_failure(
            "", '{"error_code":"ApiGW.0301","error_msg":"403 Forbidden"}', 1)
        self.assertIsInstance(err, AuthError)
        self.assertIn("IAM", str(err))

    def test_generic_api_error(self):
        err = classify_hcloud_failure("", "boom", 2)
        self.assertIsInstance(err, ApiError)

    def test_use_error_rc0(self):
        err = classify_hcloud_failure(
            "[USE_ERROR]Invalid parameter: foo\nRun `hcloud X Y --help`", "", 0,
            "CodeArtsDeploy", "ListDeployTasks")
        self.assertIsInstance(err, ApiError)
        self.assertIn("参数错误", str(err))
        self.assertIn("--help", str(err))


class TestFiltering(unittest.TestCase):
    def test_filter_by_name(self):
        items = [REPO_1, REPO_2]
        self.assertEqual(filter_by_name(items, "alpha", "repos"), [REPO_1])
        self.assertEqual(filter_by_name(items, "ALPHA", "repos"), [REPO_1])
        self.assertEqual(filter_by_name(items, "nope", "repos"), [])
        self.assertEqual(filter_by_name(items, None, "repos"), items)

    def test_filter_by_name_deploy_uses_name_key(self):
        self.assertEqual(filter_by_name([DEPLOY_1, DEPLOY_2], "beta", "deploy-tasks"),
                         [DEPLOY_2])

    def test_filter_by_status(self):
        self.assertEqual(filter_by_status([REPO_1, REPO_2], "0", "repos"), [REPO_1])
        self.assertEqual(filter_by_status([DEPLOY_1, DEPLOY_2], "failed", "deploy-tasks"),
                         [DEPLOY_1])
        self.assertEqual(filter_by_status([DEPLOY_1], "succeeded", "deploy-tasks"), [])

    def test_filter_by_status_projects_matches_type(self):
        self.assertEqual(filter_by_status([PROJECT_1, PROJECT_2], "xboard", "projects"),
                         [PROJECT_2])

    def test_input_not_mutated(self):
        src = [REPO_1, REPO_2]
        filter_by_status(src, "0", "repos")
        filter_by_name(src, "alpha", "repos")
        self.assertEqual(src, [REPO_1, REPO_2])


class TestCollectAndResolve(unittest.TestCase):
    def test_projects_single_page(self):
        fake = FakeRunner([(json.dumps({"projects": [PROJECT_1, PROJECT_2], "total": 2}), "", 0)])
        with mock.patch("list_codearts.subprocess.run", fake):
            items, resolved = list_codearts("projects", "cn-north-4")
        self.assertEqual(items, [PROJECT_1, PROJECT_2])
        self.assertIsNone(resolved)
        self.assertEqual(len(fake.calls), 1)

    def test_projects_pagination_via_total(self):
        fake = FakeRunner([
            (json.dumps({"projects": [PROJECT_1], "total": 2}), "", 0),
            (json.dumps({"projects": [PROJECT_2], "total": 2}), "", 0),
        ])
        with mock.patch("list_codearts.subprocess.run", fake):
            items, _ = list_codearts("projects", "cn-north-4", limit=1)
        self.assertEqual(items, [PROJECT_1, PROJECT_2])
        self.assertIn("--offset=1", fake.calls[1])

    def test_repos_pagination_full_page(self):
        fake = FakeRunner([
            (json.dumps([REPO_1]), "", 0),
            (json.dumps([REPO_2]), "", 0),
            (json.dumps([]), "", 0),
        ])
        with mock.patch("list_codearts.subprocess.run", fake):
            items, _ = list_codearts("repos", "cn-north-4", project_id="p-1", limit=1)
        self.assertEqual(items, [REPO_1, REPO_2])

    def test_deploy_page_pagination(self):
        fake = FakeRunner([
            (json.dumps({"result": [DEPLOY_1], "total_num": 2}), "", 0),
            (json.dumps({"result": [DEPLOY_2], "total_num": 2}), "", 0),
        ])
        with mock.patch("list_codearts.subprocess.run", fake):
            items, _ = list_codearts("deploy-tasks", "cn-north-4",
                                     project_id="p-1", limit=1)
        self.assertEqual(items, [DEPLOY_1, DEPLOY_2])
        self.assertIn("--page=2", fake.calls[1])

    def test_pipelines_name_forwarded_server_side(self):
        fake = FakeRunner([
            (json.dumps({"pipelines": [PIPELINE_1, PIPELINE_2], "total": 2}), "", 0)])
        with mock.patch("list_codearts.subprocess.run", fake):
            items, _ = list_codearts("pipelines", "cn-north-4",
                                     project_id="p-1", name="pipe")
        self.assertTrue(any("--name=pipe" in p for p in fake.calls[0]))

    def test_deploy_name_filtered_client_side(self):
        fake = FakeRunner([
            (json.dumps({"result": [DEPLOY_1, DEPLOY_2], "total_num": 2}), "", 0)])
        with mock.patch("list_codearts.subprocess.run", fake):
            items, _ = list_codearts("deploy-tasks", "cn-north-4",
                                     project_id="p-1", name="alpha")
        self.assertEqual(items, [DEPLOY_1])
        self.assertFalse(any("--name" in p for p in fake.calls[0]))

    def test_status_filter_client_side(self):
        fake = FakeRunner([
            (json.dumps({"result": [DEPLOY_1, DEPLOY_2], "total_num": 2}), "", 0)])
        with mock.patch("list_codearts.subprocess.run", fake):
            items, _ = list_codearts("deploy-tasks", "cn-north-4",
                                     project_id="p-1", status="failed")
        self.assertEqual(items, [DEPLOY_1])

    def test_explicit_project_id_skips_resolution(self):
        fake = FakeRunner([
            (json.dumps({"pipelines": [PIPELINE_1], "total": 1}), "", 0)])
        with mock.patch("list_codearts.subprocess.run", fake):
            items, resolved = list_codearts("pipelines", "cn-north-4",
                                            project_id="p-9")
        self.assertEqual(resolved, "p-9")
        self.assertEqual(len(fake.calls), 1)
        self.assertIn("--project_id=p-9", fake.calls[0])

    def test_auto_resolve_single_project(self):
        fake = FakeRunner([
            (json.dumps({"projects": [PROJECT_1], "total": 1}), "", 0),
            (json.dumps([REPO_1]), "", 0),
        ])
        with mock.patch("list_codearts.subprocess.run", fake):
            items, resolved = list_codearts("repos", "cn-north-4")
        self.assertEqual(resolved, "p-0001")
        self.assertEqual(items, [REPO_1])
        self.assertIn("--project_id=p-0001", fake.calls[1])

    def test_auto_resolve_multiple_projects_raises(self):
        fake = FakeRunner([
            (json.dumps({"projects": [PROJECT_1, PROJECT_2], "total": 2}), "", 0)])
        with mock.patch("list_codearts.subprocess.run", fake):
            with self.assertRaises(ProjectResolutionError) as ctx:
                list_codearts("repos", "cn-north-4")
        self.assertIn("--project-id", str(ctx.exception))

    def test_auto_resolve_zero_projects_raises(self):
        fake = FakeRunner([(json.dumps({"projects": [], "total": 0}), "", 0)])
        with mock.patch("list_codearts.subprocess.run", fake):
            with self.assertRaises(ProjectResolutionError):
                resolve_project_id("cn-north-4")

    def test_resolve_explicit(self):
        self.assertEqual(resolve_project_id("cn-north-4", explicit="p-x"), "p-x")

    def test_auth_error(self):
        fake = FakeRunner([("", "403 Forbidden", 1)])
        with mock.patch("list_codearts.subprocess.run", fake):
            with self.assertRaises(AuthError):
                list_codearts("projects", "cn-north-4")

    def test_config_error_missing_credentials(self):
        fake = FakeRunner([("", "no ak configured", 1)])
        with mock.patch("list_codearts.subprocess.run", fake):
            with self.assertRaises(ConfigError):
                list_codearts("projects", "cn-north-4")

    def test_timeout(self):
        fake = FakeRunner([subprocess.TimeoutExpired(cmd="hcloud", timeout=120)])
        with mock.patch("list_codearts.subprocess.run", fake):
            with self.assertRaises(ApiError):
                list_codearts("projects", "cn-north-4")

    def test_use_error_rc0(self):
        fake = FakeRunner([("[USE_ERROR]Invalid parameter: foo", "", 0)])
        with mock.patch("list_codearts.subprocess.run", fake):
            with self.assertRaises(ApiError):
                list_codearts("projects", "cn-north-4")


class TestSdkFallback(unittest.TestCase):
    def test_fallback_when_hcloud_missing(self):
        with mock.patch("list_codearts.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_codearts.list_resource_via_sdk",
                           return_value=[REPO_1]) as sdk:
            items, _ = list_codearts("repos", "cn-north-4", project_id="p-1")
        self.assertEqual(items, [REPO_1])
        self.assertEqual(sdk.call_args.kwargs.get("project_id"), "p-1")
        self.assertEqual(sdk.call_args.args[0], "repos")

    def test_fallback_unavailable_raises_config(self):
        with mock.patch("list_codearts.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_codearts.list_resource_via_sdk",
                           side_effect=ConfigError("SDK 未安装")):
            with self.assertRaises(ConfigError):
                list_codearts("projects", "cn-north-4")

    def test_sdk_missing_import_raises_config(self):
        for resource in RESOURCES:
            with mock.patch("importlib.import_module",
                            side_effect=ImportError("no sdk")):
                with self.assertRaises(ConfigError):
                    list_resource_via_sdk(resource, "cn-north-4", project_id="p-1")

    def test_sdk_missing_credentials_surfaces_aksk_hint(self):
        clean_env = {k: v for k, v in os.environ.items()
                     if not k.upper().startswith(("HUAWEI", "HW_", "HWC"))}
        with mock.patch.dict(os.environ, clean_env, clear=True), \
                mock.patch("list_codearts.subprocess.run",
                           FakeRunner([FileNotFoundError()])):
            # Skip if a real SDK happens to be installed (import path differs);
            # the assertion targets the environment-credential contract.
            try:
                list_resource_via_sdk("projects", "cn-north-4")
            except ConfigError as exc:
                self.assertTrue(
                    "AK/SK" in str(exc) or "未安装" in str(exc), str(exc))
            else:
                self.fail("expected ConfigError when neither hcloud nor credentials exist")


class TestBuildSdkRequest(unittest.TestCase):
    class FakeQuery:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

    class FakeRequest:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

    def test_projects(self):
        req = _build_sdk_request("projects", self.FakeRequest, None,
                                 None, "alpha", 100, 0)
        self.assertEqual(req.kwargs, {"limit": 100, "offset": 0, "search": "alpha"})

    def test_repos(self):
        req = _build_sdk_request("repos", self.FakeRequest, None,
                                 "p-1", "alpha", 100, 20)
        self.assertEqual(req.kwargs, {"project_id": "p-1", "limit": 100,
                                      "offset": 20, "search": "alpha"})

    def test_pipelines_wraps_body(self):
        req = _build_sdk_request("pipelines", self.FakeRequest, self.FakeQuery,
                                 "p-1", "alpha", 100, 0)
        self.assertEqual(req.kwargs["project_id"], "p-1")
        self.assertIsInstance(req.kwargs["body"], self.FakeQuery)
        self.assertEqual(req.kwargs["body"].kwargs,
                         {"limit": 100, "offset": 0, "name": "alpha"})

    def test_deploy_page_number(self):
        req = _build_sdk_request("deploy-tasks", self.FakeRequest, None,
                                 "p-1", "alpha", 100, 100)
        self.assertEqual(req.kwargs, {"project_id": "p-1", "page": 2, "size": 100})


class TestRender(unittest.TestCase):
    def test_normalize_pipeline_status_from_latest_run(self):
        flat = normalize_item(PIPELINE_1, "pipelines")
        self.assertEqual(flat["status"], "COMPLETED")

    def test_table_projects(self):
        table = render_table([PROJECT_1, PROJECT_2], "projects")
        for frag in ("proj-alpha", "p-0001", "scrum", "proj-beta", "xboard"):
            self.assertIn(frag, table)

    def test_table_repos(self):
        table = render_table([REPO_1, REPO_2], "repos")
        for frag in ("repo-alpha", "101", "private", "repo-beta"):
            self.assertIn(frag, table)

    def test_table_pipelines_shows_status(self):
        table = render_table([PIPELINE_1, PIPELINE_2], "pipelines")
        self.assertIn("COMPLETED", table)
        self.assertIn("RUNNING", table)

    def test_table_deploy(self):
        table = render_table([DEPLOY_1, DEPLOY_2], "deploy-tasks")
        for frag in ("task-alpha", "d-1", "failed", "initialized"):
            self.assertIn(frag, table)

    def test_summary_lines(self):
        lines = item_summary_lines([REPO_1, REPO_2], "repos")
        self.assertEqual(lines, ["repo-alpha  (id: 101)", "repo-beta  (id: 102)"])

    def test_summary_lines_fallback_to_id(self):
        lines = item_summary_lines([{"id": "x"}], "repos")
        self.assertEqual(lines, ["x  (id: x)"])


class TestMain(unittest.TestCase):
    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("list_codearts.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            rc = main(argv)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    def test_projects_table(self):
        rc, out, err = self._run(
            ["--resource", "projects", "--region", "cn-north-4"],
            [(json.dumps({"projects": [PROJECT_1], "total": 1}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("proj-alpha", out)
        self.assertIn("CodeArts 项目", out)
        self.assertEqual(err, "")

    def test_json_output(self):
        rc, out, err = self._run(
            ["--resource", "repos", "--project-id", "p-1", "--json"],
            [(json.dumps([REPO_1]), "", 0)])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out), [REPO_1])

    def test_names_only_output(self):
        rc, out, err = self._run(
            ["--resource", "pipelines", "--project-id", "p-1", "--names-only"],
            [(json.dumps({"pipelines": [PIPELINE_1], "total": 1}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("pipe-alpha", out)
        self.assertIn("pl-1", out)

    def test_empty_message(self):
        rc, out, err = self._run(
            ["--resource", "projects", "--region", "cn-south-1"],
            [(json.dumps({"projects": [], "total": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("无 CodeArts 资源", out)
        self.assertIn("cn-south-1", out)

    def test_empty_message_scoped_to_project(self):
        rc, out, err = self._run(
            ["--resource", "deploy-tasks", "--project-id", "p-1"],
            [(json.dumps({"result": [], "total_num": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("无 CodeArts 资源", out)
        self.assertIn("p-1", out)

    def test_empty_with_filter(self):
        rc, out, _ = self._run(
            ["--resource", "repos", "--project-id", "p-1", "--name", "zzz"],
            [(json.dumps([]), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("name=zzz", out)

    def test_403_message(self):
        rc, out, err = self._run(["--resource", "projects"], [("", "403 Forbidden", 1)])
        self.assertEqual(rc, 1)
        self.assertIn("[错误]", err)
        self.assertIn("IAM", err)

    def test_missing_ak_sk_message(self):
        rc, out, err = self._run(["--resource", "projects"],
                                 [("", "ERROR: cli-ak empty", 1)])
        self.assertEqual(rc, 1)
        self.assertIn("AK/SK", err)

    def test_hcloud_not_installed(self):
        with mock.patch("list_codearts.list_resource_via_sdk",
                        side_effect=ConfigError("CodeArts SDK 未安装")):
            rc, out, err = self._run(["--resource", "projects"], [FileNotFoundError()])
        self.assertEqual(rc, 1)
        self.assertIn("未安装", err)

    def test_hcloud_missing_falls_back_to_sdk(self):
        with mock.patch("list_codearts.list_resource_via_sdk",
                        return_value=[PROJECT_1]):
            rc, out, err = self._run(["--resource", "projects"], [FileNotFoundError()])
        self.assertEqual(rc, 0)
        self.assertIn("proj-alpha", out)

    def test_write_intent_operation_blocked(self):
        rc, out, err = self._run(["--resource", "projects",
                                  "--operation", "DeleteProjectV4"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)

    def test_write_keyword_argv_blocked(self):
        rc, out, err = self._run(["--resource", "repos", "--create-repository"], [])
        self.assertEqual(rc, 1)
        self.assertIn("守卫拦截", err)

    def test_write_intent_resource_value_not_blocked(self):
        # a read-only resource name/selector value must not trip the guard
        rc, out, err = self._run(
            ["--resource", "deploy-tasks", "--project-id", "p-1", "--json"],
            [(json.dumps({"result": [DEPLOY_1], "total_num": 1}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("task-alpha", out)

    def test_multiple_projects_error(self):
        rc, out, err = self._run(
            ["--resource", "repos"],
            [(json.dumps({"projects": [PROJECT_1, PROJECT_2], "total": 2}), "", 0)])
        self.assertEqual(rc, 1)
        self.assertIn("--project-id", err)


class TestErrorHierarchy(unittest.TestCase):
    def test_subclasses(self):
        for exc in (GuardError, ConfigError, AuthError, ApiError,
                    ProjectResolutionError):
            self.assertTrue(issubclass(exc, CodeArtsListError))

    def test_allowed_operations(self):
        self.assertEqual(
            ALLOWED_OPERATIONS,
            {"ListProjectsV4", "ListProjectRepositories",
             "ListPipelines", "ListDeployTasks"})


if __name__ == "__main__":
    unittest.main()
