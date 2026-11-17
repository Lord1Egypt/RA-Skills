import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from show_ecs import (  # noqa: E402
    ALLOWED_OPERATION,
    ApiError,
    AuthError,
    ConfigError,
    GuardError,
    NotFoundError,
    EcsShowError,
    build_command,
    classify_hcloud_failure,
    extract_server,
    extract_json,
    guard_operation,
    guard_text_from_argv,
    guard_write_intent,
    main,
    normalize_server,
    render_detail,
    render_markdown,
    sdk_server_to_dict,
    show_server,
    show_server_via_sdk,
    to_jsonable,
    validate_instance_id,
    write_markdown,
)

SERVER = {
    "id": "ecs-0001",
    "name": "ecs-web-01",
    "status": "ACTIVE",
    "flavor": {"id": "s6.large.2", "name": "s6.large.2", "vcpus": "2", "ram": "4096"},
    "addresses": {
        "vpc-subnet": [
            {"addr": "192.168.0.10", "OS-EXT-IPS:type": "fixed", "version": 4}
        ]
    },
    "OS-EXT-AZ:availability_zone": "cn-north-4a",
    "image": {"id": "img-0001"},
    "created": "2026-10-20T09:00:00Z",
    "tags": ["env:test"],
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
        self.assertFalse(guard_write_intent("--region cn-north-4 --json show server"))
        self.assertFalse(guard_write_intent("show server details"))

    def test_create_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("CreateServers ecs-new")

    def test_delete_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--operation DeleteServers")

    def test_mutating_verbs_blocked(self):
        for text in ("resize flavor", "reboot ecs-01", "stop server",
                     "update server name", "attach volume", "server-action"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_normalized_separators_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--create-server")
        with self.assertRaises(GuardError):
            guard_write_intent("delete_server")

    def test_operation_guard_rejects_non_show(self):
        with self.assertRaises(GuardError):
            guard_operation("ListServersDetails")
        with self.assertRaises(GuardError):
            guard_operation("DeleteServers")
        self.assertTrue(guard_operation(ALLOWED_OPERATION))

    def test_guard_text_strips_data_values(self):
        self.assertEqual(guard_text_from_argv(["--instance-id", "abc-123"]), "")
        self.assertEqual(guard_text_from_argv(["--instance-id=abc-123"]), "")
        self.assertEqual(guard_text_from_argv(["--region", "cn-north-4"]), "")
        self.assertEqual(guard_text_from_argv(["--project-id", "p-1"]), "")
        # Operation name is still scanned (defense in depth).
        self.assertIn("DeleteServers",
                      guard_text_from_argv(["--operation", "DeleteServers"]))
        # Flag names are scanned.
        self.assertIn("--create-server",
                      guard_text_from_argv(["--create-server"]))

    def test_md_file_path_value_not_scanned(self):
        # The export path is local query data; a write-looking directory/file
        # name must not trip the read-only guard.
        self.assertEqual(
            guard_text_from_argv(["--md-file", "/tmp/create-delete-server.md"]),
            "")
        self.assertEqual(
            guard_text_from_argv(["--output-md=/tmp/stop-me.md"]), "")
        self.assertFalse(guard_write_intent(
            guard_text_from_argv(["--instance-id", "ecs-0001",
                                  "--md-file", "/tmp/delete-report.md"])))

    def test_instance_id_write_word_not_blocked(self):
        # A value that happens to contain a write word is data, not an intent.
        self.assertFalse(
            guard_write_intent(guard_text_from_argv(["--instance-id", "stop-me"])))

    def test_flag_after_data_value_still_scanned(self):
        self.assertIn("--create-server",
                      guard_text_from_argv(["--instance-id", "--create-server"]))
        self.assertIn("DeleteServers",
                      guard_text_from_argv(["--region", "--operation",
                                            "DeleteServers"]))


class TestValidateInstanceId(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(validate_instance_id("abc-123"), "abc-123")
        self.assertEqual(validate_instance_id("  abc-123  "), "abc-123")

    def test_empty_rejected(self):
        for bad in (None, "", "   "):
            with self.assertRaises(ConfigError):
                validate_instance_id(bad)

    def test_whitespace_rejected(self):
        with self.assertRaises(ConfigError):
            validate_instance_id("abc 123")


class TestBuildCommand(unittest.TestCase):
    def test_basic(self):
        argv = build_command("cn-north-4", "ecs-0001")
        self.assertEqual(argv[0], "ECS")
        self.assertEqual(argv[1], "ShowServer")
        self.assertIn("--cli-region=cn-north-4", argv)
        self.assertIn("--server_id=ecs-0001", argv)

    def test_no_write_flags_ever_added(self):
        argv = build_command("cn-north-4", "ecs-0001")
        for flag in argv:
            self.assertFalse(
                flag.lower().lstrip("-").startswith(
                    ("create", "delete", "update", "reboot", "resize")))


class TestExtract(unittest.TestCase):
    def test_extract_json_plain(self):
        data = extract_json(json.dumps({"server": SERVER}))
        self.assertEqual(data, {"server": SERVER})

    def test_extract_json_with_noise(self):
        data = extract_json("WARNING noise\n{\"server\": {}}\n")
        self.assertEqual(data, {"server": {}})

    def test_extract_json_invalid(self):
        with self.assertRaises(ApiError):
            extract_json("<html>not json</html>")

    def test_extract_server_nested(self):
        self.assertEqual(extract_server({"server": SERVER}), SERVER)

    def test_extract_server_flat(self):
        self.assertEqual(extract_server(SERVER), SERVER)

    def test_extract_server_absent(self):
        self.assertIsNone(extract_server({"count": 0}))
        self.assertIsNone(extract_server([]))


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

    def test_not_found_404(self):
        err = classify_hcloud_failure(
            "", '{"error_code":"ECS.0401","error_msg":"server not found, 404"}', 1)
        self.assertIsInstance(err, NotFoundError)

    def test_not_found_message_zh(self):
        err = classify_hcloud_failure("", "实例不存在", 1)
        self.assertIsInstance(err, NotFoundError)

    def test_generic_api_error(self):
        err = classify_hcloud_failure("", "boom", 2)
        self.assertIsInstance(err, ApiError)

    def test_use_error_marker_with_zero_rc(self):
        err = classify_hcloud_failure(
            "[USE_ERROR]Invalid parameter: xxx\n\n"
            "Run `hcloud ECS ShowServer --help` for details.", "", 0)
        self.assertIsInstance(err, ApiError)
        self.assertIn("参数错误", str(err))
        self.assertIn("--help", str(err))


class TestShowServer(unittest.TestCase):
    def test_single_call_success(self):
        fake = FakeRunner([(json.dumps({"server": SERVER}), "", 0)])
        with mock.patch("show_ecs.subprocess.run", fake):
            server = show_server("cn-north-4", "ecs-0001")
        self.assertEqual(server, SERVER)
        self.assertEqual(len(fake.calls), 1)
        self.assertIn("--server_id=ecs-0001", fake.calls[0])

    def test_empty_id_raises_config_before_call(self):
        fake = FakeRunner([])
        with mock.patch("show_ecs.subprocess.run", fake):
            with self.assertRaises(ConfigError):
                show_server("cn-north-4", "")
        self.assertEqual(fake.calls, [])

    def test_not_found_404(self):
        fake = FakeRunner([("", '{"error_msg":"404 not found"}', 1)])
        with mock.patch("show_ecs.subprocess.run", fake):
            with self.assertRaises(NotFoundError):
                show_server("cn-north-4", "ecs-missing")

    def test_missing_server_payload_raises_notfound(self):
        fake = FakeRunner([(json.dumps({"count": 0}), "", 0)])
        with mock.patch("show_ecs.subprocess.run", fake):
            with self.assertRaises(NotFoundError):
                show_server("cn-north-4", "ecs-missing")

    def test_use_error_rc0_raises_api_error(self):
        fake = FakeRunner([(
            "[USE_ERROR]Invalid parameter: xxx\n\n"
            "Run `hcloud ECS ShowServer --help` for details.", "", 0)])
        with mock.patch("show_ecs.subprocess.run", fake):
            with self.assertRaises(ApiError) as ctx:
                show_server("cn-north-4", "ecs-0001")
        self.assertIn("参数错误", str(ctx.exception))

    def test_nonzero_exit_403(self):
        fake = FakeRunner([("", "403 Forbidden", 1)])
        with mock.patch("show_ecs.subprocess.run", fake):
            with self.assertRaises(AuthError):
                show_server("cn-north-4", "ecs-0001")

    def test_nonzero_exit_credentials(self):
        fake = FakeRunner([("", "ERROR: no AK configured", 1)])
        with mock.patch("show_ecs.subprocess.run", fake):
            with self.assertRaises(ConfigError):
                show_server("cn-north-4", "ecs-0001")

    def test_timeout(self):
        fake = FakeRunner([subprocess.TimeoutExpired(cmd="hcloud", timeout=120)])
        with mock.patch("show_ecs.subprocess.run", fake):
            with self.assertRaises(ApiError):
                show_server("cn-north-4", "ecs-0001")

    def test_sdk_fallback_when_hcloud_missing(self):
        with mock.patch("show_ecs.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("show_ecs.show_server_via_sdk",
                           return_value=SERVER) as sdk_mock:
            server = show_server("cn-north-4", "ecs-0001", project_id="p-1")
        self.assertEqual(server, SERVER)
        self.assertEqual(sdk_mock.call_args.kwargs.get("project_id"), "p-1")

    def test_sdk_fallback_unavailable_raises_config(self):
        with mock.patch("show_ecs.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("show_ecs.show_server_via_sdk",
                           side_effect=ConfigError("huaweicloudsdkecs 未安装")):
            with self.assertRaises(ConfigError):
                show_server("cn-north-4", "ecs-0001")

    def test_sdk_request_accepts_server_id(self):
        # Regression guard: the real huaweicloudsdkecs ShowServerRequest must be
        # constructible with exactly the kwarg the fallback path sends.
        try:
            from huaweicloudsdkecs.v2 import ShowServerRequest
        except ImportError:
            self.skipTest("huaweicloudsdkecs not installed")
        request = ShowServerRequest(server_id="ecs-0001")
        self.assertEqual(request.server_id, "ecs-0001")


class TestSdkServerToDict(unittest.TestCase):
    def test_remaps_python_attr_names_to_wire_names(self):
        try:
            from huaweicloudsdkecs.v2 import ServerDetail
        except ImportError:
            self.skipTest("huaweicloudsdkecs not installed")
        detail = ServerDetail(
            id="ecs-9", name="ecs-live", status="ACTIVE",
            access_i_pv4="1.2.3.4",
            os_ext_a_zavailability_zone="cn-north-4a",
            flavor={"id": "s6.large.2", "name": "s6.large.2", "vcpus": "2", "ram": "4096"},
        )
        flat = sdk_server_to_dict(detail)
        self.assertEqual(flat["id"], "ecs-9")
        self.assertEqual(flat["name"], "ecs-live")
        self.assertEqual(flat["accessIPv4"], "1.2.3.4")
        self.assertEqual(flat["OS-EXT-AZ:availability_zone"], "cn-north-4a")
        # None-valued SDK fields must be dropped.
        self.assertNotIn("user_id", flat)

    def test_wire_name_dict_passes_through(self):
        flat = sdk_server_to_dict(dict(SERVER))
        self.assertEqual(flat["name"], "ecs-web-01")
        self.assertEqual(flat["OS-EXT-AZ:availability_zone"], "cn-north-4a")


class _FakeSdkResponse:
    def __init__(self, server):
        self.server = server


class _FakeSdkServer:
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


class TestSdkFallbackPath(unittest.TestCase):
    """Regression: the SDK fallback must use modules that exist in the official
    huaweicloudsdk packages and wire credentials from environment variables
    (BasicCredentials has no env auto-discovery)."""

    def setUp(self):
        self._captured_credentials = None
        self._captured_region = None
        self._fake_client = mock.Mock()
        self._fake_client.show_server.return_value = _FakeSdkResponse(
            _FakeSdkServer(SERVER))
        try:
            import huaweicloudsdkecs.v2 as ecs_v2
        except ImportError:
            self.skipTest("huaweicloudsdkecs not installed")
        self._builder_patch = mock.patch.object(
            ecs_v2.EcsClient, "new_builder",
            classmethod(lambda cls: _FakeSdkBuilder(self)))
        self._builder_patch.start()
        self.addCleanup(self._builder_patch.stop)

    def _clean_credential_env(self):
        credential_vars = (
            "HW_ACCESS_KEY",
            "HUAWEI_ACCESS_KEY",
            "HUAWEICLOUD_SDK_AK",
            "HUAWEI_CLOUD_ACCESS_KEY",
            "HW_SECRET_KEY",
            "HUAWEI_SECRET_KEY",
            "HUAWEICLOUD_SDK_SK",
            "HUAWEI_CLOUD_SECRET_KEY",
        )
        return {name: "" for name in credential_vars}

    def test_official_sdk_imports_resolve(self):
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkecs.v2 import EcsClient, ShowServerRequest
        from huaweicloudsdkecs.v2.region.ecs_region import EcsRegion
        for obj in (BasicCredentials, Region, HttpConfig,
                    EcsClient, ShowServerRequest, EcsRegion):
            self.assertTrue(callable(obj), obj)

    def test_sdk_fallback_returns_server_with_env_credentials(self):
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak",
                   HUAWEI_SECRET_KEY="test-sk")
        with mock.patch.dict(os.environ, env, clear=True):
            server = show_server_via_sdk("cn-north-4", "ecs-0001")
        self.assertEqual(server, SERVER)
        credentials = self._captured_credentials
        self.assertIsNotNone(credentials)
        self.assertEqual(getattr(credentials, "ak", None), "test-ak")
        self.assertEqual(getattr(credentials, "sk", None), "test-sk")
        self.assertEqual(getattr(self._captured_region, "id", None), "cn-north-4")

    def test_sdk_fallback_missing_env_credentials_raises_config(self):
        with mock.patch.dict(os.environ, self._clean_credential_env(),
                             clear=True):
            with self.assertRaises(ConfigError) as ctx:
                show_server_via_sdk("cn-north-4", "ecs-0001")
        message = str(ctx.exception)
        self.assertIn("AK/SK", message)
        self.assertNotIn("未安装", message)

    def test_sdk_fallback_alternative_env_prefixes(self):
        env = dict(self._clean_credential_env(),
                   HW_ACCESS_KEY="alt-ak", HW_SECRET_KEY="alt-sk")
        with mock.patch.dict(os.environ, env, clear=True):
            show_server_via_sdk("cn-north-4", "ecs-0001")
        self.assertEqual(getattr(self._captured_credentials, "ak", None), "alt-ak")


class TestNormalizeAndRender(unittest.TestCase):
    def test_normalize_flattens_flavor_az_and_ips(self):
        flat = normalize_server(SERVER)
        self.assertEqual(flat["flavor"], "s6.large.2")
        self.assertEqual(flat["vcpus"], "2")
        self.assertEqual(flat["ram"], "4096")
        self.assertEqual(flat["availability_zone"], "cn-north-4a")
        self.assertEqual(flat["privateIps"], "192.168.0.10")
        self.assertEqual(flat["publicIps"], "-")
        self.assertEqual(flat["image_id"], "img-0001")

    def test_normalize_public_and_private_ips(self):
        server = dict(SERVER)
        server["addresses"] = {"vpc-subnet": [
            {"addr": "192.168.0.11", "OS-EXT-IPS:type": "fixed"},
            {"addr": "10.0.0.5", "OS-EXT-IPS:type": "floating"},
        ]}
        flat = normalize_server(server)
        self.assertEqual(flat["privateIps"], "192.168.0.11")
        self.assertEqual(flat["publicIps"], "10.0.0.5")

    def test_normalize_missing_fields_dash(self):
        flat = normalize_server({"id": "ecs-x"})
        self.assertEqual(flat["availability_zone"], "-")
        self.assertEqual(flat["privateIps"], "-")
        self.assertEqual(flat["publicIps"], "-")
        self.assertEqual(flat["tags"], "-")

    def test_normalize_sdk_attr_names(self):
        flat = normalize_server({
            "id": "ecs-y",
            "os_ext_a_zavailability_zone": "cn-north-4c",
            "access_i_pv4": "9.9.9.9",
        })
        self.assertEqual(flat["availability_zone"], "cn-north-4c")
        self.assertEqual(flat["publicIps"], "9.9.9.9")

    def test_render_detail_contains_key_fields(self):
        detail = render_detail(SERVER)
        for fragment in ("实例 ID", "ecs-0001", "ecs-web-01", "ACTIVE",
                         "s6.large.2", "img-0001", "cn-north-4a",
                         "192.168.0.10", "创建时间", "标签"):
            self.assertIn(fragment, detail)


class TestRenderMarkdown(unittest.TestCase):
    def test_markdown_contains_key_fields(self):
        md = render_markdown(SERVER)
        self.assertTrue(md.startswith("# ECS 实例详情"))
        # A Markdown table header + separator are present.
        self.assertIn("| 字段 | 值 |", md)
        self.assertIn("| --- | --- |", md)
        for fragment in ("实例 ID", "ecs-0001", "ecs-web-01", "ACTIVE",
                         "s6.large.2", "img-0001", "cn-north-4a",
                         "192.168.0.10", "创建时间", "标签"):
            self.assertIn(fragment, md)
        # Ends with a trailing newline (well-formed text file).
        self.assertTrue(md.endswith("\n"))

    def test_markdown_explicitly_lists_public_ips(self):
        server = dict(SERVER)
        server["addresses"] = {"vpc-subnet": [
            {"addr": "192.168.0.11", "OS-EXT-IPS:type": "fixed"},
            {"addr": "10.0.0.5", "OS-EXT-IPS:type": "floating"},
        ]}
        md = render_markdown(server)
        self.assertIn("私网 IP", md)
        self.assertIn("公网 IP", md)
        self.assertIn("192.168.0.11", md)
        self.assertIn("10.0.0.5", md)

    def test_markdown_region_line(self):
        md = render_markdown(SERVER, region="cn-south-1")
        self.assertIn("- Region: cn-south-1", md)

    def test_markdown_missing_fields_dash(self):
        md = render_markdown({"id": "ecs-x"})
        self.assertIn("| 实例 ID | ecs-x |", md)
        self.assertIn("| 可用区 | - |", md)

    def test_markdown_escapes_pipe_in_values(self):
        server = dict(SERVER)
        server["name"] = "web|broken"
        md = render_markdown(server)
        self.assertIn("web\\|broken", md)
        self.assertNotIn("| web|broken |", md)

    def test_markdown_extra_fields_section(self):
        md = render_markdown(SERVER)
        self.assertIn("## 其他字段", md)
        # The raw `addresses` container is surfaced as an extra field.
        self.assertIn("addresses", md)

    def test_markdown_sdk_objects_do_not_crash(self):
        server = {
            "id": "ecs-sdk-1",
            "name": "ecs-sdk-web",
            "addresses": {"vpc-subnet": [
                _FakeSdkModel(addr="192.168.0.10", os_ext_ip_stype="fixed")]},
        }
        md = render_markdown(server)
        self.assertIn("ecs-sdk-1", md)
        self.assertIn("192.168.0.10", md)


class TestWriteMarkdown(unittest.TestCase):
    def test_writes_file_with_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "ecs.md")
            target = write_markdown(path, "hello\n")
            self.assertEqual(target, os.path.abspath(path))
            with open(path, encoding="utf-8") as handle:
                self.assertEqual(handle.read(), "hello\n")

    def test_overwrites_existing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "ecs.md")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("old content that is longer")
            write_markdown(path, "new\n")
            with open(path, encoding="utf-8") as handle:
                self.assertEqual(handle.read(), "new\n")

    def test_empty_path_rejected(self):
        for bad in (None, "", "   "):
            with self.assertRaises(ConfigError):
                write_markdown(bad, "x")

    def test_missing_parent_dir_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "no-such-dir", "ecs.md")
            with self.assertRaises(ConfigError) as ctx:
                write_markdown(path, "x")
            self.assertIn("上级目录不存在", str(ctx.exception))

    def test_directory_target_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ConfigError) as ctx:
                write_markdown(tmp, "x")
            self.assertIn("目录", str(ctx.exception))

    def test_expands_user_home(self):
        with tempfile.TemporaryDirectory() as tmp, \
                mock.patch.dict(os.environ, {"HOME": tmp}):
            target = write_markdown("~/ecs.md", "x")
            self.assertEqual(target, os.path.join(os.path.abspath(tmp), "ecs.md"))


class TestMain(unittest.TestCase):
    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("show_ecs.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            rc = main(argv)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    def test_detail_output(self):
        rc, out, err = self._run(
            ["--instance-id", "ecs-0001"],
            [(json.dumps({"server": SERVER}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("ECS 实例详情", out)
        self.assertIn("ecs-web-01", out)
        self.assertIn("ACTIVE", out)
        self.assertEqual(err, "")

    def test_json_output(self):
        rc, out, err = self._run(
            ["--instance-id", "ecs-0001", "--json"],
            [(json.dumps({"server": SERVER}), "", 0)])
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual(payload, SERVER)

    def test_region_forwarded(self):
        fake = FakeRunner([(json.dumps({"server": SERVER}), "", 0)])
        with mock.patch("show_ecs.subprocess.run", fake), \
                mock.patch("sys.stdout"), mock.patch("sys.stderr"):
            rc = main(["--instance-id", "ecs-0001", "--region", "cn-south-1"])
        self.assertEqual(rc, 0)
        self.assertIn("--cli-region=cn-south-1", fake.calls[0])

    def test_requires_instance_id(self):
        with mock.patch("sys.stderr"):
            with self.assertRaises(SystemExit):
                main([])

    def test_auth_error_message(self):
        rc, out, err = self._run(["--instance-id", "ecs-0001"],
                                 [("", "403 Forbidden", 1)])
        self.assertEqual(rc, 1)
        self.assertIn("[错误]", err)
        self.assertIn("IAM", err)

    def test_not_found_error_message(self):
        rc, out, err = self._run(["--instance-id", "ecs-missing"],
                                 [("", "404 server not found", 1)])
        self.assertEqual(rc, 1)
        self.assertIn("未找到", err)

    def test_missing_ak_sk_error_message(self):
        rc, out, err = self._run(["--instance-id", "ecs-0001"],
                                 [("", "ERROR: cli-ak empty", 1)])
        self.assertEqual(rc, 1)
        self.assertIn("AK/SK", err)

    def test_hcloud_not_installed(self):
        with mock.patch("show_ecs.show_server_via_sdk",
                        side_effect=ConfigError("huaweicloudsdkecs 未安装")):
            rc, out, err = self._run(["--instance-id", "ecs-0001"],
                                     [FileNotFoundError()])
        self.assertEqual(rc, 1)
        self.assertIn("未安装", err)

    def test_hcloud_missing_falls_back_to_sdk(self):
        with mock.patch("show_ecs.show_server_via_sdk",
                        return_value=SERVER):
            rc, out, err = self._run(["--instance-id", "ecs-0001"],
                                     [FileNotFoundError()])
        self.assertEqual(rc, 0)
        self.assertIn("ecs-web-01", out)

    def test_write_intent_argv_blocked(self):
        rc, out, err = self._run(["--instance-id", "ecs-0001",
                                  "--operation", "DeleteServers"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)

    def test_write_flag_argv_blocked(self):
        rc, out, err = self._run(["--instance-id", "ecs-0001",
                                  "--create-server"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)

    def test_instance_id_write_word_not_blocked(self):
        rc, out, err = self._run(
            ["--instance-id", "stop-me"],
            [(json.dumps({"server": SERVER}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertNotIn("写操作意图", err)

    def test_md_file_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "ecs.md")
            rc, out, err = self._run(
                ["--instance-id", "ecs-0001", "--md-file", path],
                [(json.dumps({"server": SERVER}), "", 0)])
            self.assertEqual(rc, 0)
            self.assertEqual(err, "")
            self.assertIn("已导出", out)
            with open(path, encoding="utf-8") as handle:
                content = handle.read()
        self.assertIn("ecs-web-01", content)
        self.assertIn("| 字段 | 值 |", content)

    def test_output_md_alias_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "ecs.md")
            rc, out, err = self._run(
                ["--instance-id", "ecs-0001", "--output-md", path],
                [(json.dumps({"server": SERVER}), "", 0)])
            self.assertEqual(rc, 0)
            self.assertTrue(os.path.exists(path))

    def test_md_file_takes_precedence_over_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "ecs.md")
            rc, out, err = self._run(
                ["--instance-id", "ecs-0001", "--json", "--md-file", path],
                [(json.dumps({"server": SERVER}), "", 0)])
            self.assertEqual(rc, 0)
            self.assertIn("已导出", out)
            with self.assertRaises(json.JSONDecodeError):
                json.loads(out)

    def test_md_file_invalid_parent_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "missing-dir", "ecs.md")
            rc, out, err = self._run(
                ["--instance-id", "ecs-0001", "--md-file", path],
                [(json.dumps({"server": SERVER}), "", 0)])
            self.assertEqual(rc, 1)
            self.assertIn("[错误]", err)
            self.assertIn("上级目录不存在", err)
            self.assertFalse(os.path.exists(path))


class _FakeSdkModel:
    """Stand-in for a non-JSON-serializable huaweicloudsdk* model object."""

    def __init__(self, **fields):
        self._fields = fields

    def to_dict(self):
        return dict(self._fields)


class _FakeServerDetail:
    """Mimics the official SDK `ServerDetail.to_dict()` quirk (inner list
    objects in `addresses` stay SDK model objects)."""

    def __init__(self, payload):
        self._payload = payload

    def to_dict(self):
        return dict(self._payload)


class TestSdkObjectSerialization(unittest.TestCase):
    """Regression: the SDK fallback must never leak SDK model objects into the
    detail / JSON renderers — they are not JSON-serializable and crash
    json.dumps with `TypeError: Object of type ServerAddress is not JSON
    serializable`."""

    def _sdk_fixture(self):
        return {
            "id": "ecs-sdk-1",
            "name": "ecs-sdk-web",
            "status": "ACTIVE",
            "flavor": {"id": "s6.large.2", "name": "s6.large.2",
                       "vcpus": "2", "ram": "4096"},
            "addresses": {
                "vpc-subnet": [
                    _FakeSdkModel(addr="192.168.0.10", os_ext_ip_stype="fixed"),
                    _FakeSdkModel(addr="10.0.0.5", os_ext_ip_stype="floating"),
                ]
            },
            "OS-EXT-AZ:availability_zone": "cn-north-4a",
        }

    def test_to_jsonable_recurses_into_nested_containers(self):
        value = _FakeSdkModel(server=[_FakeSdkModel(addr="10.0.0.5")])
        json.dumps(to_jsonable(value))
        self.assertEqual(
            to_jsonable(value), {"server": [{"addr": "10.0.0.5"}]})

    def test_sdk_server_to_dict_converts_nested_sdk_objects(self):
        flat = sdk_server_to_dict(_FakeServerDetail(self._sdk_fixture()))
        json.dumps(flat)
        addresses = flat["addresses"]["vpc-subnet"]
        self.assertEqual(addresses[0]["addr"], "192.168.0.10")
        self.assertEqual(addresses[1]["addr"], "10.0.0.5")
        normal = normalize_server(flat)
        self.assertEqual(normal["privateIps"], "192.168.0.10")
        self.assertEqual(normal["publicIps"], "10.0.0.5")

    def test_render_detail_with_sdk_objects_does_not_crash(self):
        server = sdk_server_to_dict(_FakeServerDetail(self._sdk_fixture()))
        detail = render_detail(server)
        self.assertIn("ecs-sdk-web", detail)
        self.assertIn("192.168.0.10", detail)

    def test_cell_defensive_on_raw_sdk_object(self):
        detail = render_detail(self._sdk_fixture())
        self.assertIn("ecs-sdk-web", detail)

    def test_main_json_with_sdk_objects(self):
        servers = [self._sdk_fixture()]
        fake = FakeRunner([FileNotFoundError()])
        with mock.patch("show_ecs.subprocess.run", fake), \
                mock.patch("show_ecs.show_server_via_sdk", return_value=servers[0]), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr"):
            rc = main(["--instance-id", "ecs-sdk-1", "--json"])
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual(payload["addresses"]["vpc-subnet"][0]["addr"],
                         "192.168.0.10")


class TestErrorHierarchy(unittest.TestCase):
    def test_subclasses(self):
        for exc in (GuardError, ConfigError, AuthError, NotFoundError, ApiError):
            self.assertTrue(issubclass(exc, EcsShowError))

    def test_not_found_is_api_like_but_distinct(self):
        self.assertFalse(issubclass(NotFoundError, AuthError))


if __name__ == "__main__":
    unittest.main()