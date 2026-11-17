import glob
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from list_eip import (  # noqa: E402
    ALLOWED_OPERATION,
    ApiError,
    AuthError,
    ConfigError,
    ExportError,
    GuardError,
    EipListError,
    build_command,
    classify_hcloud_failure,
    default_output_path,
    export_markdown,
    extract_json,
    extract_publicips,
    guard_operation,
    guard_text_from_argv,
    guard_write_intent,
    list_publicips,
    list_publicips_via_sdk,
    main,
    normalize_publicip,
    publicip_names,
    render_markdown,
    render_table,
)

PUBLICIP_1 = {
    "id": "eip-0001",
    "alias": "eip-demo-01",
    "public_ip_address": "1.2.3.4",
    "status": "ACTIVE",
    "type": "EIP",
    "ip_version": 4,
    "bandwidth": {
        "id": "bw-0001",
        "name": "bw-demo",
        "size": 5,
        "share_type": "PER",
        "charge_mode": "traffic",
    },
    "vnic": {
        "private_ip_address": "192.168.0.10",
        "device_id": "dev-0001",
        "vpc_id": "vpc-0001",
        "port_id": "port-0001",
    },
    "associate_instance_type": "PORT",
    "associate_instance_id": "port-0001",
    "enterprise_project_id": "0",
    "publicip_pool_name": "5_bgp",
    "lock_status": "unlock",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-02T00:00:00",
}
PUBLICIP_2 = {
    "id": "eip-0002",
    "alias": "eip-demo-02",
    "public_ip_address": "5.6.7.8",
    "status": "DOWN",
    "type": "EIP",
    "ip_version": 4,
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
        self.assertFalse(guard_write_intent("--region cn-north-4 --json list eips"))
        self.assertFalse(guard_write_intent("show public ip details"))

    def test_create_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("CreatePublicip eip-new")

    def test_delete_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--operation DeletePublicip")

    def test_mutating_verbs_blocked(self):
        for text in ("associate public ips", "disassociate eip",
                     "detach eip from server", "release eip-01",
                     "change bandwidth", "update public ip alias",
                     "bind bandwidth"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_normalized_separators_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--create-eip")
        with self.assertRaises(GuardError):
            guard_write_intent("update_publicip_alias")

    def test_read_filter_value_passes(self):
        self.assertFalse(guard_write_intent("--status ACTIVE"))
        self.assertFalse(guard_write_intent("--public-ip 1.2.3.4"))
        self.assertFalse(guard_write_intent("--alias my-eip"))

    def test_operation_guard_rejects_non_list(self):
        with self.assertRaises(GuardError):
            guard_operation("ShowPublicip")
        self.assertTrue(guard_operation(ALLOWED_OPERATION))


class TestBuildCommand(unittest.TestCase):
    def test_basic(self):
        argv = build_command("cn-north-4")
        self.assertEqual(argv[0], "EIP")
        self.assertEqual(argv[1], "ListPublicips")
        self.assertIn("--cli-region=cn-north-4", argv)
        self.assertIn("--limit=100", argv)
        self.assertFalse(any(flag.startswith("--marker") for flag in argv))

    def test_marker_appended(self):
        argv = build_command("cn-north-4", marker="tok-123", limit=10)
        self.assertIn("--marker=tok-123", argv)
        self.assertIn("--limit=10", argv)

    def test_filters_forwarded_server_side(self):
        argv = build_command("cn-south-1", eip_id="eip-9", status="ACTIVE",
                             public_ip="1.2.3.4", limit=10)
        self.assertIn("--id.1=eip-9", argv)
        self.assertIn("--status.1=ACTIVE", argv)
        self.assertIn("--public_ip_address.1=1.2.3.4", argv)
        self.assertIn("--limit=10", argv)

    def test_filters_use_koocli_array_syntax(self):
        # Regression: EIP ListPublicips declares id/status/public_ip_address as
        # array<string> params in KooCLI 7.x — the scalar form is rejected with
        # [USE_ERROR]Invalid parameter, so every filter must carry the `.1` index.
        argv = build_command("cn-north-4", eip_id="eip-9", status="ACTIVE",
                             public_ip="1.2.3.4")
        self.assertIn("--id.1=eip-9", argv)
        self.assertIn("--status.1=ACTIVE", argv)
        self.assertIn("--public_ip_address.1=1.2.3.4", argv)
        for scalar in ("--id=eip-9", "--status=ACTIVE",
                       "--public_ip_address=1.2.3.4"):
            self.assertNotIn(scalar, argv)

    def test_no_write_flags_ever_added(self):
        argv = build_command("cn-north-4", status="ACTIVE")
        for flag in argv:
            self.assertFalse(flag.lower().lstrip("-").startswith(
                ("create", "delete", "update", "associate", "release")))


class TestExtract(unittest.TestCase):
    def test_extract_json_plain(self):
        data = extract_json(json.dumps({"publicips": []}))
        self.assertEqual(data, {"publicips": []})

    def test_extract_json_with_noise(self):
        data = extract_json("WARNING some noise\n{\"a\": 1}\n")
        self.assertEqual(data, {"a": 1})

    def test_extract_json_invalid(self):
        with self.assertRaises(ApiError):
            extract_json("<html>not json</html>")

    def test_extract_publicips_known_keys(self):
        for key in ("publicips", "public_ips"):
            self.assertEqual(extract_publicips({key: [PUBLICIP_1]}), [PUBLICIP_1])
        self.assertEqual(extract_publicips([PUBLICIP_1]), [PUBLICIP_1])
        self.assertEqual(extract_publicips({"page_info": {}}), [])


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
        err = classify_hcloud_failure(
            "[USE_ERROR]Invalid parameter: status\n\n"
            "Run `hcloud EIP ListPublicips --help` for details.", "", 0)
        self.assertIsInstance(err, ApiError)
        self.assertIn("参数错误", str(err))
        self.assertIn("--help", str(err))


class TestListPublicips(unittest.TestCase):
    def test_single_page(self):
        fake = FakeRunner([(
            json.dumps({"publicips": [PUBLICIP_1, PUBLICIP_2]}), "", 0)])
        with mock.patch("list_eip.subprocess.run", fake):
            publicips = list_publicips("cn-north-4")
        self.assertEqual(publicips, [PUBLICIP_1, PUBLICIP_2])
        self.assertEqual(len(fake.calls), 1)

    def test_pagination_via_next_marker(self):
        page1 = {"publicips": [PUBLICIP_1],
                 "page_info": {"next_marker": "tok-2", "current_count": 1}}
        page2 = {"publicips": [PUBLICIP_2],
                 "page_info": {"next_marker": None, "current_count": 1}}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("list_eip.subprocess.run", fake):
            publicips = list_publicips("cn-north-4", limit=1)
        self.assertEqual(publicips, [PUBLICIP_1, PUBLICIP_2])
        self.assertEqual(len(fake.calls), 2)
        self.assertIn("--marker=tok-2", fake.calls[1])

    def test_pagination_via_full_page_without_marker(self):
        page1 = {"publicips": [PUBLICIP_1]}
        page2 = {"publicips": []}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("list_eip.subprocess.run", fake):
            publicips = list_publicips("cn-north-4", limit=1)
        self.assertEqual(publicips, [PUBLICIP_1])

    def test_empty_region(self):
        fake = FakeRunner([(json.dumps({"publicips": []}), "", 0)])
        with mock.patch("list_eip.subprocess.run", fake):
            publicips = list_publicips("cn-north-4")
        self.assertEqual(publicips, [])

    def test_filters_forwarded_to_cli(self):
        fake = FakeRunner([(
            json.dumps({"publicips": [PUBLICIP_1]}), "", 0)])
        with mock.patch("list_eip.subprocess.run", fake):
            list_publicips("cn-north-4", status="ACTIVE", eip_id="eip-0001",
                           public_ip="1.2.3.4")
        call = fake.calls[0]
        self.assertTrue(any("--status.1=ACTIVE" in part for part in call))
        self.assertTrue(any("--id.1=eip-0001" in part for part in call))
        self.assertTrue(any("--public_ip_address.1=1.2.3.4" in part for part in call))

    def test_use_error_rc0_raises_api_error(self):
        fake = FakeRunner([(
            "[USE_ERROR]Invalid parameter: status\n\n"
            "Run `hcloud EIP ListPublicips --help` for details.", "", 0)])
        with mock.patch("list_eip.subprocess.run", fake):
            with self.assertRaises(ApiError) as ctx:
                list_publicips("cn-north-4")
        self.assertIn("参数错误", str(ctx.exception))

    def test_nonzero_exit_403(self):
        fake = FakeRunner([("", "403 Forbidden", 1)])
        with mock.patch("list_eip.subprocess.run", fake):
            with self.assertRaises(AuthError):
                list_publicips("cn-north-4")

    def test_nonzero_exit_credentials(self):
        fake = FakeRunner([("", "ERROR: no AK configured", 1)])
        with mock.patch("list_eip.subprocess.run", fake):
            with self.assertRaises(ConfigError):
                list_publicips("cn-north-4")

    def test_timeout(self):
        fake = FakeRunner([subprocess.TimeoutExpired(cmd="hcloud", timeout=120)])
        with mock.patch("list_eip.subprocess.run", fake):
            with self.assertRaises(ApiError):
                list_publicips("cn-north-4")

    def test_sdk_fallback_when_hcloud_missing(self):
        with mock.patch("list_eip.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_eip.list_publicips_via_sdk",
                           return_value=[PUBLICIP_1, PUBLICIP_2]) as sdk_mock:
            publicips = list_publicips("cn-north-4", status="ACTIVE",
                                       eip_id="eip-1", public_ip="1.2.3.4",
                                       project_id="proj-1")
        self.assertEqual(publicips, [PUBLICIP_1, PUBLICIP_2])
        self.assertEqual(sdk_mock.call_args.kwargs.get("status"), "ACTIVE")
        self.assertEqual(sdk_mock.call_args.kwargs.get("project_id"), "proj-1")

    def test_sdk_fallback_unavailable_raises_config(self):
        with mock.patch("list_eip.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_eip.list_publicips_via_sdk",
                           side_effect=ConfigError("huaweicloudsdkeip 未安装")):
            with self.assertRaises(ConfigError):
                list_publicips("cn-north-4")

    def test_sdk_request_signature(self):
        # Regression guard: the real huaweicloudsdkeip ListPublicipsRequest
        # must be constructible with exactly the kwargs the fallback path sends.
        try:
            from huaweicloudsdkeip.v3 import ListPublicipsRequest
        except ImportError:
            self.skipTest("huaweicloudsdkeip not installed")
        request = ListPublicipsRequest(
            limit=100, marker=None, id=["eip-9"], status=["ACTIVE"],
            public_ip_address=["1.2.3.4"],
        )
        self.assertEqual(request.id, ["eip-9"])
        self.assertEqual(request.status, ["ACTIVE"])
        self.assertEqual(request.public_ip_address, ["1.2.3.4"])
        with self.assertRaises(TypeError):
            ListPublicipsRequest(no_such_param=1)


class _FakeSdkResponse:
    def __init__(self, publicips, next_marker):
        self.publicips = publicips

        class _PageInfo:
            pass

        page = _PageInfo()
        page.next_marker = next_marker
        self.page_info = page


class _FakeSdkPublicip:
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
    """P2 regression: the SDK fallback must use modules that exist in the
    official huaweicloudsdkeip package and wire credentials (including the
    project id required by /v3/{project_id}/...) from environment variables
    (BasicCredentials has no env auto-discovery)."""

    def setUp(self):
        self._captured_credentials = None
        self._captured_region = None
        self._fake_client = mock.Mock()
        self._fake_client.list_publicips.return_value = _FakeSdkResponse(
            [_FakeSdkPublicip(PUBLICIP_1), _FakeSdkPublicip(PUBLICIP_2)], None)
        try:
            import huaweicloudsdkeip.v3 as eip_v3
        except ImportError:
            self.skipTest("huaweicloudsdkeip not installed")
        self._builder_patch = mock.patch.object(
            eip_v3.EipClient, "new_builder",
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
            "HW_PROJECT_ID",
            "HUAWEI_PROJECT_ID",
            "HUAWEICLOUD_SDK_PROJECT_ID",
            "HUAWEI_CLOUD_PROJECT_ID",
        )
        return {name: "" for name in credential_vars}

    def test_official_sdk_imports_resolve(self):
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkeip.v3 import EipClient, ListPublicipsRequest
        from huaweicloudsdkeip.v3.region.eip_region import EipRegion
        for obj in (BasicCredentials, Region, HttpConfig,
                    EipClient, ListPublicipsRequest, EipRegion):
            self.assertTrue(callable(obj), obj)

    def test_sdk_fallback_returns_publicips_with_env_credentials(self):
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak",
                   HUAWEI_SECRET_KEY="test-sk",
                   HUAWEI_PROJECT_ID="test-project")
        with mock.patch.dict(os.environ, env, clear=True):
            publicips = list_publicips_via_sdk("cn-north-4")
        self.assertEqual(publicips, [PUBLICIP_1, PUBLICIP_2])
        credentials = self._captured_credentials
        self.assertIsNotNone(credentials)
        self.assertEqual(getattr(credentials, "ak", None), "test-ak")
        self.assertEqual(getattr(credentials, "sk", None), "test-sk")
        self.assertEqual(getattr(credentials, "project_id", None), "test-project")
        self.assertEqual(getattr(self._captured_region, "id", None), "cn-north-4")

    def test_explicit_project_id_overrides_env(self):
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak",
                   HUAWEI_SECRET_KEY="test-sk",
                   HUAWEI_PROJECT_ID="env-project")
        with mock.patch.dict(os.environ, env, clear=True):
            list_publicips_via_sdk("cn-north-4", project_id="cli-project")
        self.assertEqual(
            getattr(self._captured_credentials, "project_id", None), "cli-project")

    def test_sdk_fallback_missing_env_credentials_raises_config(self):
        env = dict(self._clean_credential_env(), HUAWEI_PROJECT_ID="test-project")
        with mock.patch.dict(os.environ, env, clear=True):
            with self.assertRaises(ConfigError) as ctx:
                list_publicips_via_sdk("cn-north-4")
        message = str(ctx.exception)
        self.assertIn("AK/SK", message)
        self.assertNotIn("未安装", message)

    def test_sdk_fallback_missing_project_id_raises_config(self):
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak", HUAWEI_SECRET_KEY="test-sk")
        with mock.patch.dict(os.environ, env, clear=True):
            with self.assertRaises(ConfigError) as ctx:
                list_publicips_via_sdk("cn-north-4")
        self.assertIn("project_id", str(ctx.exception))

    def test_sdk_pagination_via_next_marker(self):
        first = _FakeSdkResponse([_FakeSdkPublicip(PUBLICIP_1)], "tok-2")
        second = _FakeSdkResponse([_FakeSdkPublicip(PUBLICIP_2)], None)
        self._fake_client.list_publicips.side_effect = [first, second]
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak",
                   HUAWEI_SECRET_KEY="test-sk",
                   HUAWEI_PROJECT_ID="test-project")
        with mock.patch.dict(os.environ, env, clear=True):
            publicips = list_publicips_via_sdk("cn-north-4")
        self.assertEqual(publicips, [PUBLICIP_1, PUBLICIP_2])
        second_request = self._fake_client.list_publicips.call_args_list[1][0][0]
        self.assertEqual(second_request.marker, "tok-2")


class TestNormalizeAndRender(unittest.TestCase):
    def test_normalize_expands_bandwidth(self):
        flat = normalize_publicip(PUBLICIP_1)
        self.assertEqual(flat["bandwidth_name"], "bw-demo")
        self.assertEqual(flat["bandwidth_size"], 5)
        self.assertEqual(flat["bandwidth_share_type"], "PER")
        self.assertEqual(flat["bandwidth_charge_mode"], "traffic")
        self.assertNotIn("bandwidth", flat)

    def test_normalize_expands_vnic(self):
        flat = normalize_publicip(PUBLICIP_1)
        self.assertEqual(flat["vnic_private_ip_address"], "192.168.0.10")
        self.assertEqual(flat["vnic_device_id"], "dev-0001")
        self.assertNotIn("vnic", flat)

    def test_normalize_missing_nested(self):
        flat = normalize_publicip(PUBLICIP_2)
        self.assertNotIn("bandwidth_name", flat)
        self.assertNotIn("vnic_device_id", flat)

    def test_table_contains_basic_info(self):
        table = render_table([PUBLICIP_1, PUBLICIP_2])
        for fragment in ("eip-0001", "1.2.3.4", "ACTIVE", "bw-demo", "5",
                         "PORT", "port-0001", "192.168.0.10", "eip-demo-01"):
            self.assertIn(fragment, table)

    def test_names(self):
        self.assertEqual(
            publicip_names([PUBLICIP_1, PUBLICIP_2]), ["eip-demo-01", "eip-demo-02"])

    def test_names_fallback_to_public_ip_then_id(self):
        self.assertEqual(publicip_names([{"public_ip_address": "9.9.9.9"}]), ["9.9.9.9"])
        self.assertEqual(publicip_names([{"id": "eip-9"}]), ["eip-9"])


class TestMain(unittest.TestCase):
    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("list_eip.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            rc = main(argv)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    def test_table_output(self):
        rc, out, err = self._run(
            ["--region", "cn-north-4"],
            [(json.dumps({"publicips": [PUBLICIP_1, PUBLICIP_2]}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("弹性公网IP（EIP）列表", out)
        self.assertIn("eip-0001", out)
        self.assertIn("ACTIVE", out)
        self.assertEqual(err, "")

    def test_json_output(self):
        rc, out, err = self._run(
            ["--json"],
            [(json.dumps({"publicips": [PUBLICIP_1]}), "", 0)])
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual(payload, [PUBLICIP_1])

    def test_names_only_output(self):
        rc, out, err = self._run(
            ["--names-only"],
            [(json.dumps({"publicips": [PUBLICIP_1, PUBLICIP_2]}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("eip-demo-01", out)
        self.assertIn("eip-demo-02", out)
        self.assertNotIn("bandwidth_name", out)

    def test_empty_instances_message(self):
        rc, out, err = self._run(
            ["--region", "cn-south-1"],
            [(json.dumps({"publicips": []}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("无弹性公网IP（EIP）", out)
        self.assertIn("cn-south-1", out)

    def test_empty_with_filter_message(self):
        rc, out, _ = self._run(
            ["--status", "ACTIVE"],
            [(json.dumps({"publicips": []}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("status=ACTIVE", out)

    def test_status_filter_main_forwarded(self):
        fake = FakeRunner([
            (json.dumps({"publicips": [PUBLICIP_1]}), "", 0)])
        with mock.patch("list_eip.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr"):
            rc = main(["--status", "ACTIVE"])
        self.assertEqual(rc, 0)
        self.assertTrue(any("--status.1=ACTIVE" in part for part in fake.calls[0]))

    def test_empty_json_output(self):
        rc, out, err = self._run(
            ["--json"],
            [(json.dumps({"publicips": []}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out), [])

    def test_empty_names_only_output(self):
        rc, out, err = self._run(
            ["--names-only"],
            [(json.dumps({"publicips": []}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("共 0 个", out)
        self.assertNotIn("无弹性公网IP（EIP）", out)

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
        with mock.patch("list_eip.list_publicips_via_sdk",
                        side_effect=ConfigError("huaweicloudsdkeip 未安装")):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 1)
        self.assertIn("未安装", err)

    def test_hcloud_missing_falls_back_to_sdk(self):
        with mock.patch("list_eip.list_publicips_via_sdk",
                        return_value=[PUBLICIP_1]):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 0)
        self.assertIn("eip-0001", out)

    def test_project_id_forwarded_to_sdk(self):
        with mock.patch("list_eip.list_publicips_via_sdk",
                        return_value=[PUBLICIP_1]) as sdk_mock:
            rc, out, err = self._run(["--project-id", "proj-9"],
                                     [FileNotFoundError()])
        self.assertEqual(rc, 0)
        self.assertEqual(sdk_mock.call_args.kwargs.get("project_id"), "proj-9")

    def test_write_intent_argv_blocked(self):
        rc, out, err = self._run(["--operation", "DeletePublicip"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)

    def test_write_keyword_argv_blocked(self):
        rc, out, err = self._run(["--id", "release-me"], [])
        self.assertEqual(rc, 1)
        self.assertIn("守卫拦截", err)

    def test_status_write_word_blocked(self):
        rc, out, err = self._run(["--status", "deleting-now"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)


class TestRenderMarkdown(unittest.TestCase):
    def test_title_metadata_and_full_header(self):
        md = render_markdown([PUBLICIP_1, PUBLICIP_2], region="cn-north-4",
                             generated_at="2026-11-10T00:00:00Z")
        self.assertIn("# 华为云 EIP 列表", md)
        self.assertIn("查询区域：cn-north-4", md)
        self.assertIn("生成时间：2026-11-10T00:00:00Z", md)
        self.assertIn("记录数：2", md)
        for header in ("公网IP", "EIP ID", "别名", "状态", "类型",
                       "绑定实例类型", "绑定实例 ID", "带宽名称", "带宽大小",
                       "计费方式", "企业项目 ID", "创建时间"):
            self.assertIn("| %s |" % header, md)

    def test_rows_and_flat_bandwidth_fields(self):
        md = render_markdown([PUBLICIP_1], region="cn-north-4",
                             generated_at="2026-11-10T00:00:00Z")
        for fragment in ("1.2.3.4", "eip-0001", "eip-demo-01", "ACTIVE",
                         "PORT", "port-0001", "bw-demo", "5", "traffic", "0",
                         "2024-01-01T00:00:00"):
            self.assertIn(fragment, md)

    def test_missing_fields_use_dash(self):
        md = render_markdown([{"id": "eip-9", "public_ip_address": "9.9.9.9"}],
                             region="cn-north-4")
        row = [line for line in md.splitlines() if "| eip-9 |" in line][0]
        cells = [cell.strip() for cell in row.strip("|").split("|")]
        self.assertTrue(all(cell for cell in cells))
        self.assertGreaterEqual(cells.count("-"), 10)

    def test_empty_list_still_valid_with_no_data_note(self):
        md = render_markdown([], region="cn-south-1",
                             generated_at="2026-11-10T00:00:00Z")
        self.assertIn("# 华为云 EIP 列表", md)
        self.assertIn("记录数：0", md)
        self.assertIn("| 公网IP |", md)
        self.assertIn("无数据", md)

    def test_filters_rendered(self):
        md = render_markdown([], region="cn-north-4",
                             filters=["status=ACTIVE", "id=eip-1"])
        self.assertIn("过滤条件：status=ACTIVE, id=eip-1", md)


class TestExportMarkdown(unittest.TestCase):
    def test_creates_parent_directories_and_returns_abspath(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "nested", "reports", "eip.md")
            written = export_markdown([PUBLICIP_1], target,
                                      region="cn-north-4")
            self.assertEqual(written, os.path.abspath(target))
            self.assertTrue(os.path.isfile(written))
            with open(written, encoding="utf-8") as handle:
                self.assertIn("eip-demo-01", handle.read())

    def test_atomic_write_leaves_no_temp_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "eip.md")
            export_markdown([PUBLICIP_1, PUBLICIP_2], target,
                            region="cn-north-4")
            self.assertEqual(sorted(os.listdir(tmp)), ["eip.md"])

    def test_overwrites_existing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "eip.md")
            with open(target, "w", encoding="utf-8") as handle:
                handle.write("stale")
            export_markdown([PUBLICIP_1], target, region="cn-north-4")
            with open(target, encoding="utf-8") as handle:
                content = handle.read()
            self.assertNotIn("stale", content)
            self.assertIn("eip-0001", content)

    def test_empty_list_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "empty.md")
            export_markdown([], target, region="cn-south-1")
            with open(target, encoding="utf-8") as handle:
                content = handle.read()
            self.assertIn("无数据", content)

    def test_unwritable_parent_raises_export_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            blocker = os.path.join(tmp, "not-a-dir")
            with open(blocker, "w", encoding="utf-8") as handle:
                handle.write("x")
            with self.assertRaises(ExportError):
                export_markdown([], os.path.join(blocker, "eip.md"))

    def test_default_output_path_shape(self):
        name = default_output_path("cn-north-4")
        self.assertTrue(name.startswith("eip_list_cn-north-4_"))
        self.assertTrue(name.endswith(".md"))


class TestMarkdownMain(unittest.TestCase):
    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("list_eip.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            rc = main(argv)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    def test_output_flag_writes_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "eip.md")
            rc, out, err = self._run(
                ["-o", target],
                [(json.dumps({"publicips": [PUBLICIP_1]}), "", 0)])
            self.assertEqual(rc, 0)
            self.assertEqual(err, "")
            self.assertTrue(os.path.isfile(target))
            self.assertIn(os.path.abspath(target), out)
            self.assertIn("共 1 条", out)
            with open(target, encoding="utf-8") as handle:
                self.assertIn("eip-demo-01", handle.read())

    def test_markdown_flag_uses_default_filename_in_cwd(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = os.getcwd()
            os.chdir(tmp)
            try:
                rc, out, err = self._run(
                    ["--markdown", "--region", "cn-north-4"],
                    [(json.dumps({"publicips": [PUBLICIP_1]}), "", 0)])
            finally:
                os.chdir(cwd)
            self.assertEqual(rc, 0)
            self.assertEqual(err, "")
            files = glob.glob(os.path.join(tmp, "eip_list_cn-north-4_*.md"))
            self.assertEqual(len(files), 1)
            self.assertIn(os.path.abspath(files[0]), out)

    def test_empty_result_still_writes_markdown_and_exits_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "empty.md")
            rc, out, err = self._run(
                ["--markdown", "-o", target, "--region", "cn-south-1"],
                [(json.dumps({"publicips": []}), "", 0)])
            self.assertEqual(rc, 0)
            self.assertEqual(err, "")
            self.assertTrue(os.path.isfile(target))
            self.assertIn("无数据", out)
            self.assertIn("共 0 条", out)
            with open(target, encoding="utf-8") as handle:
                self.assertIn("无数据", handle.read())

    def test_export_precedence_over_json_and_names_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "eip.md")
            rc, out, err = self._run(
                ["--json", "--names-only", "--markdown", "-o", target],
                [(json.dumps({"publicips": [PUBLICIP_1]}), "", 0)])
            self.assertEqual(rc, 0)
            self.assertEqual(err, "")
            self.assertTrue(os.path.isfile(target))
            with self.assertRaises(json.JSONDecodeError):
                json.loads(out)

    def test_output_path_containing_write_word_is_not_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "eip-release-report.md")
            rc, out, err = self._run(
                ["-o", target],
                [(json.dumps({"publicips": [PUBLICIP_1]}), "", 0)])
            self.assertEqual(rc, 0)
            self.assertEqual(err, "")
            self.assertTrue(os.path.isfile(target))

    def test_write_flags_still_blocked_with_export_args(self):
        rc, out, err = self._run(["--markdown", "--operation", "DeletePublicip"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)


class TestGuardTextFromArgv(unittest.TestCase):
    def test_output_value_stripped(self):
        text = guard_text_from_argv(["-o", "eip-release-report.md"])
        self.assertNotIn("release", text)
        self.assertEqual(text, "")

    def test_output_equals_form_stripped(self):
        self.assertNotIn("delete", guard_text_from_argv(
            ["--output=delete-report.md"]))

    def test_other_values_still_scanned(self):
        self.assertIn("release-me", guard_text_from_argv(["--id", "release-me"]))

    def test_following_flag_not_swallowed(self):
        text = guard_text_from_argv(["-o", "--create-eip"])
        self.assertIn("--create-eip", text)


class TestErrorHierarchy(unittest.TestCase):
    def test_subclasses(self):
        for exc in (GuardError, ConfigError, AuthError, ApiError, ExportError):
            self.assertTrue(issubclass(exc, EipListError))


if __name__ == "__main__":
    unittest.main()