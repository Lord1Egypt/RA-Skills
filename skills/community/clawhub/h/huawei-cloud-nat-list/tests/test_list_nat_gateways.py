import json
import os
import subprocess
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from list_nat_gateways import (  # noqa: E402
    ALLOWED_OPERATION,
    ApiError,
    AuthError,
    ConfigError,
    GuardError,
    NatListError,
    _payload_error,
    _sdk_auth_error,
    build_command,
    classify_hcloud_failure,
    extract_gateways,
    extract_json,
    gateway_names,
    guard_operation,
    guard_write_intent,
    list_nat_gateways,
    list_nat_gateways_via_sdk,
    main,
    render_table,
)

GATEWAY_1 = {
    "id": "nat-0001",
    "tenant_id": "proj-0001",
    "name": "nat-demo-01",
    "description": "demo gateway one",
    "spec": "1",
    "status": "ACTIVE",
    "admin_state_up": True,
    "created_at": "2024-01-01 00:00:00.000000",
    "router_id": "router-0001",
    "internal_network_id": "network-0001",
    "enterprise_project_id": "0",
    "ngport_ip_address": "192.168.10.5",
    "billing_info": "order-0001",
    "dnat_rules_limit": 200,
    "snat_rule_public_ip_limit": 20,
    "pps_max": 10000,
    "bps_max": 5000,
}
GATEWAY_2 = {
    "id": "nat-0002",
    "name": "nat-demo-02",
    "spec": "3",
    "status": "ACTIVE",
    "router_id": "router-0002",
    "created_at": "2024-02-02 00:00:00.000000",
}
GATEWAY_3 = {
    "id": "nat-0003",
    "name": "nat-inactive-03",
    "spec": "2",
    "status": "INACTIVE",
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
        self.assertFalse(guard_write_intent("--region cn-north-4 --json list nat gateways"))
        self.assertFalse(guard_write_intent("show nat gateway details"))

    def test_create_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("CreateNatGateway nat-new")

    def test_delete_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--operation DeleteNatGateway")

    def test_snat_dnat_blocked(self):
        for text in ("create snat rule", "delete dnat rule",
                     "update snat rule", "batch create dnat rules"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_mutating_verbs_blocked(self):
        for text in ("update nat gateway spec", "release nat-01",
                     "change gateway spec", "modify nat description"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_normalized_separators_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--create-nat")
        with self.assertRaises(GuardError):
            guard_write_intent("create_nat_gateway")

    def test_read_filter_value_passes(self):
        self.assertFalse(guard_write_intent("--name my-nat"))
        self.assertFalse(guard_write_intent("--spec 1"))
        self.assertFalse(guard_write_intent("--status ACTIVE"))
        self.assertFalse(guard_write_intent("--vpc router-123"))

    def test_operation_guard_rejects_non_list(self):
        with self.assertRaises(GuardError):
            guard_operation("ShowNatGateway")
        self.assertTrue(guard_operation(ALLOWED_OPERATION))


class TestBuildCommand(unittest.TestCase):
    def test_basic(self):
        argv = build_command("cn-north-4")
        self.assertEqual(argv[0], "NAT")
        self.assertEqual(argv[1], "ListNatGateways")
        self.assertIn("--cli-region=cn-north-4", argv)
        self.assertIn("--limit=2000", argv)
        self.assertFalse(any(flag.startswith("--marker") for flag in argv))

    def test_marker_appended(self):
        argv = build_command("cn-north-4", marker="tok-123", limit=10)
        self.assertIn("--marker=tok-123", argv)
        self.assertIn("--limit=10", argv)

    def test_filters_forwarded_server_side(self):
        argv = build_command("cn-south-1", name="my-nat", spec="2",
                             status="ACTIVE", router_id="router-9", limit=10)
        self.assertIn("--name=my-nat", argv)
        self.assertIn("--spec.1=2", argv)
        self.assertIn("--status.1=ACTIVE", argv)
        self.assertIn("--router_id=router-9", argv)
        self.assertNotIn("--spec=2", argv)
        self.assertNotIn("--status=ACTIVE", argv)
        self.assertIn("--limit=10", argv)

    def test_no_write_flags_ever_added(self):
        argv = build_command("cn-north-4", status="ACTIVE")
        for flag in argv:
            self.assertFalse(flag.lower().lstrip("-").startswith(
                ("create", "delete", "update", "modify")))


class TestExtract(unittest.TestCase):
    def test_extract_json_plain(self):
        data = extract_json(json.dumps({"nat_gateways": []}))
        self.assertEqual(data, {"nat_gateways": []})

    def test_extract_json_with_noise(self):
        data = extract_json("WARNING some noise\n{\"a\": 1}\n")
        self.assertEqual(data, {"a": 1})

    def test_extract_json_invalid(self):
        with self.assertRaises(ApiError):
            extract_json("<html>not json</html>")

    def test_extract_gateways_known_keys(self):
        for key in ("nat_gateways", "natGateways"):
            self.assertEqual(extract_gateways({key: [GATEWAY_1]}), [GATEWAY_1])
        self.assertEqual(extract_gateways([GATEWAY_1]), [GATEWAY_1])
        self.assertEqual(extract_gateways({"page_info": {}}), [])

    def test_payload_error_root_envelope(self):
        payload = {"error_code": "SYS.0403",
                   "error_msg": "user is not authorized to perform nat:natGateways:list"}
        text = _payload_error(payload)
        self.assertIn("SYS.0403", text)
        self.assertIn("not authorized", text)

    def test_payload_error_nested_envelope(self):
        payload = {"error": {"error_code": "NAT.0001", "error_msg": "internal error"}}
        self.assertEqual(_payload_error(payload), "NAT.0001 internal error")

    def test_payload_error_none_for_real_list_payload(self):
        self.assertIsNone(_payload_error({"nat_gateways": []}))
        self.assertIsNone(_payload_error({"natGateways": [GATEWAY_1]}))
        self.assertIsNone(_payload_error([GATEWAY_1]))
        self.assertIsNone(_payload_error({}))


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
        self.assertIn("nat:natGateways:list", str(err))

    def test_auth_unauthorized(self):
        err = classify_hcloud_failure("", "Unauthorized: invalid AK", 1)
        self.assertIsInstance(err, AuthError)

    def test_generic_api_error(self):
        err = classify_hcloud_failure("", "boom", 2)
        self.assertIsInstance(err, ApiError)

    def test_use_error_marker_with_zero_rc(self):
        err = classify_hcloud_failure(
            "[USE_ERROR]Invalid parameter: spec\n\n"
            "Run `hcloud NAT ListNatGateways --help` for details.", "", 0)
        self.assertIsInstance(err, ApiError)
        self.assertIn("参数错误", str(err))
        self.assertIn("--help", str(err))

    def test_auth_401_is_reported_as_invalid_credentials(self):
        err = classify_hcloud_failure("", "401 Unauthorized: invalid AK", 1)
        self.assertIsInstance(err, AuthError)
        self.assertIn("401", str(err))
        self.assertIn("凭证无效", str(err))
        self.assertNotIn("403", str(err))

    def test_auth_error_envelope_rc0_is_403(self):
        err = classify_hcloud_failure(
            "SYS.0403 user is not authorized to perform nat:natGateways:list", "", 0)
        self.assertIsInstance(err, AuthError)
        self.assertIn("无权限访问公网NAT网关", str(err))
        self.assertIn("nat:natGateways:list", str(err))

    def test_sdk_auth_error_distinguishes_401_and_403(self):
        class _Unauthorized(Exception):
            status_code = 401

        class _Forbidden(Exception):
            status_code = 403

        unauthorized = _sdk_auth_error(_Unauthorized("401 Unauthorized"))
        self.assertIn("凭证无效", str(unauthorized))
        self.assertNotIn("无权限访问", str(unauthorized))
        forbidden = _sdk_auth_error(_Forbidden("403 Forbidden"))
        self.assertIn("无权限访问公网NAT网关", str(forbidden))


class TestListNatGateways(unittest.TestCase):
    def test_single_page(self):
        fake = FakeRunner([(
            json.dumps({"nat_gateways": [GATEWAY_1, GATEWAY_2]}), "", 0)])
        with mock.patch("list_nat_gateways.subprocess.run", fake):
            gateways = list_nat_gateways("cn-north-4")
        self.assertEqual(gateways, [GATEWAY_1, GATEWAY_2])
        self.assertEqual(len(fake.calls), 1)

    def test_pagination_uses_last_gateway_id_as_marker(self):
        page1 = {"nat_gateways": [GATEWAY_1, GATEWAY_2]}
        page2 = {"nat_gateways": [GATEWAY_3]}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("list_nat_gateways.subprocess.run", fake):
            gateways = list_nat_gateways("cn-north-4", limit=2)
        self.assertEqual(gateways, [GATEWAY_1, GATEWAY_2, GATEWAY_3])
        self.assertEqual(len(fake.calls), 2)
        self.assertIn("--marker=nat-0002", fake.calls[1])

    def test_pagination_ignores_unsupported_next_marker_field(self):
        page1 = {"nat_gateways": [GATEWAY_1, GATEWAY_2], "next_marker": "tok-2"}
        page2 = {"nat_gateways": [GATEWAY_3]}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("list_nat_gateways.subprocess.run", fake):
            gateways = list_nat_gateways("cn-north-4", limit=2)
        self.assertEqual(gateways, [GATEWAY_1, GATEWAY_2, GATEWAY_3])
        self.assertIn("--marker=nat-0002", fake.calls[1])
        self.assertFalse(any("tok-2" in part for part in fake.calls[1]))

    def test_pagination_stops_on_short_page(self):
        page1 = {"nat_gateways": [GATEWAY_1, GATEWAY_2]}
        fake = FakeRunner([(json.dumps(page1), "", 0)])
        with mock.patch("list_nat_gateways.subprocess.run", fake):
            gateways = list_nat_gateways("cn-north-4", limit=3)
        self.assertEqual(gateways, [GATEWAY_1, GATEWAY_2])
        self.assertEqual(len(fake.calls), 1)

    def test_pagination_via_full_page_until_empty(self):
        page1 = {"nat_gateways": [GATEWAY_1]}
        page2 = {"nat_gateways": []}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("list_nat_gateways.subprocess.run", fake):
            gateways = list_nat_gateways("cn-north-4", limit=1)
        self.assertEqual(gateways, [GATEWAY_1])
        self.assertIn("--marker=nat-0001", fake.calls[1])

    def test_pagination_boundary_exact_full_page_then_empty(self):
        # Boundary: the final page holds exactly `limit` items, so the next
        # request is required and must return an empty page that terminates
        # paging without duplicating or dropping gateways.
        page1 = {"nat_gateways": [GATEWAY_1, GATEWAY_2]}
        page2 = {"nat_gateways": []}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("list_nat_gateways.subprocess.run", fake):
            gateways = list_nat_gateways("cn-north-4", limit=2)
        self.assertEqual(gateways, [GATEWAY_1, GATEWAY_2])
        self.assertEqual(len(fake.calls), 2)
        self.assertIn("--marker=nat-0002", fake.calls[1])

    def test_pagination_chains_marker_across_three_pages(self):
        # Boundary: every full page hands its own last gateway id to the next
        # request (marker is not a fixed cursor), and the short final page stops.
        page1 = {"nat_gateways": [{"id": "nat-a1"}, {"id": "nat-a2"}]}
        page2 = {"nat_gateways": [{"id": "nat-a3"}, {"id": "nat-a4"}]}
        page3 = {"nat_gateways": [{"id": "nat-a5"}]}
        fake = FakeRunner([
            (json.dumps(page1), "", 0),
            (json.dumps(page2), "", 0),
            (json.dumps(page3), "", 0),
        ])
        with mock.patch("list_nat_gateways.subprocess.run", fake):
            gateways = list_nat_gateways("cn-north-4", limit=2)
        self.assertEqual([g["id"] for g in gateways],
                         ["nat-a1", "nat-a2", "nat-a3", "nat-a4", "nat-a5"])
        self.assertEqual(len(fake.calls), 3)
        self.assertIn("--marker=nat-a2", fake.calls[1])
        self.assertIn("--marker=nat-a4", fake.calls[2])

    def test_pagination_stops_when_marker_repeats(self):
        # Infinite-loop guard: a server repeating the same page must not cause
        # an unbounded request loop.
        page = {"nat_gateways": [GATEWAY_1]}
        fake = FakeRunner([(json.dumps(page), "", 0), (json.dumps(page), "", 0)])
        with mock.patch("list_nat_gateways.subprocess.run", fake):
            gateways = list_nat_gateways("cn-north-4", limit=1)
        self.assertEqual(gateways, [GATEWAY_1, GATEWAY_1])
        self.assertEqual(len(fake.calls), 2)

    def test_empty_region(self):
        fake = FakeRunner([(json.dumps({"nat_gateways": []}), "", 0)])
        with mock.patch("list_nat_gateways.subprocess.run", fake):
            gateways = list_nat_gateways("cn-north-4")
        self.assertEqual(gateways, [])

    def test_filters_forwarded_to_cli(self):
        fake = FakeRunner([(
            json.dumps({"nat_gateways": [GATEWAY_1]}), "", 0)])
        with mock.patch("list_nat_gateways.subprocess.run", fake):
            list_nat_gateways("cn-north-4", name="my-nat", spec="1",
                              status="ACTIVE", router_id="router-0001")
        call = fake.calls[0]
        self.assertTrue(any("--name=my-nat" in part for part in call))
        self.assertTrue(any("--spec.1=1" in part for part in call))
        self.assertTrue(any("--status.1=ACTIVE" in part for part in call))
        self.assertTrue(any("--router_id=router-0001" in part for part in call))

    def test_use_error_rc0_raises_api_error(self):
        fake = FakeRunner([(
            "[USE_ERROR]Invalid parameter: spec\n\n"
            "Run `hcloud NAT ListNatGateways --help` for details.", "", 0)])
        with mock.patch("list_nat_gateways.subprocess.run", fake):
            with self.assertRaises(ApiError) as ctx:
                list_nat_gateways("cn-north-4")
        self.assertIn("参数错误", str(ctx.exception))

    def test_error_envelope_rc0_auth_is_not_empty_list(self):
        # Regression (PR #117 R1): KooCLI returns HTTP API errors as a JSON
        # envelope on stdout with exit code 0; it must raise, never become an
        # empty gateway list.
        envelope = json.dumps({
            "error_code": "SYS.0403",
            "error_msg": "user is not authorized to perform nat:natGateways:list",
        })
        fake = FakeRunner([(envelope, "", 0)])
        with mock.patch("list_nat_gateways.subprocess.run", fake):
            with self.assertRaises(AuthError) as ctx:
                list_nat_gateways("cn-north-4")
        self.assertIn("无权限访问公网NAT网关", str(ctx.exception))
        self.assertIn("nat:natGateways:list", str(ctx.exception))

    def test_error_envelope_rc0_nested_generic(self):
        envelope = json.dumps(
            {"error": {"error_code": "NAT.0001", "error_msg": "internal error"}})
        fake = FakeRunner([(envelope, "", 0)])
        with mock.patch("list_nat_gateways.subprocess.run", fake):
            with self.assertRaises(ApiError) as ctx:
                list_nat_gateways("cn-north-4")
        message = str(ctx.exception)
        self.assertIn("NAT.0001", message)
        self.assertIn("internal error", message)

    def test_list_payload_with_message_is_not_an_error(self):
        # A successful page that happens to carry other keys must still be
        # parsed as a gateway list, not as an error envelope.
        payload = {"nat_gateways": [GATEWAY_1], "message": "ok"}
        fake = FakeRunner([(json.dumps(payload), "", 0)])
        with mock.patch("list_nat_gateways.subprocess.run", fake):
            gateways = list_nat_gateways("cn-north-4")
        self.assertEqual(gateways, [GATEWAY_1])

    def test_nonzero_exit_403(self):
        fake = FakeRunner([("", "403 Forbidden", 1)])
        with mock.patch("list_nat_gateways.subprocess.run", fake):
            with self.assertRaises(AuthError):
                list_nat_gateways("cn-north-4")

    def test_nonzero_exit_credentials(self):
        fake = FakeRunner([("", "ERROR: no AK configured", 1)])
        with mock.patch("list_nat_gateways.subprocess.run", fake):
            with self.assertRaises(ConfigError):
                list_nat_gateways("cn-north-4")

    def test_timeout(self):
        fake = FakeRunner([subprocess.TimeoutExpired(cmd="hcloud", timeout=120)])
        with mock.patch("list_nat_gateways.subprocess.run", fake):
            with self.assertRaises(ApiError):
                list_nat_gateways("cn-north-4")

    def test_sdk_fallback_when_hcloud_missing(self):
        with mock.patch("list_nat_gateways.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_nat_gateways.list_nat_gateways_via_sdk",
                           return_value=[GATEWAY_1, GATEWAY_2]) as sdk_mock:
            gateways = list_nat_gateways("cn-north-4", name="my-nat",
                                         spec="1", status="ACTIVE",
                                         router_id="router-1",
                                         project_id="proj-1")
        self.assertEqual(gateways, [GATEWAY_1, GATEWAY_2])
        self.assertEqual(sdk_mock.call_args.kwargs.get("name"), "my-nat")
        self.assertEqual(sdk_mock.call_args.kwargs.get("spec"), "1")
        self.assertEqual(sdk_mock.call_args.kwargs.get("status"), "ACTIVE")
        self.assertEqual(sdk_mock.call_args.kwargs.get("router_id"), "router-1")
        self.assertEqual(sdk_mock.call_args.kwargs.get("project_id"), "proj-1")

    def test_sdk_fallback_unavailable_raises_config(self):
        with mock.patch("list_nat_gateways.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_nat_gateways.list_nat_gateways_via_sdk",
                           side_effect=ConfigError("huaweicloudsdknat 未安装")):
            with self.assertRaises(ConfigError):
                list_nat_gateways("cn-north-4")

    def test_sdk_request_signature(self):
        # Regression guard: the real huaweicloudsdknat ListNatGatewaysRequest
        # must be constructible with exactly the kwargs the fallback path sends.
        try:
            from huaweicloudsdknat.v2 import ListNatGatewaysRequest
        except ImportError:
            self.skipTest("huaweicloudsdknat not installed")
        request = ListNatGatewaysRequest(
            limit=100, marker=None, name="my-nat", spec=["1"],
            status=["ACTIVE"], router_id="router-9",
        )
        self.assertEqual(request.name, "my-nat")
        self.assertEqual(request.spec, ["1"])
        self.assertEqual(request.status, ["ACTIVE"])
        self.assertEqual(request.router_id, "router-9")
        with self.assertRaises(TypeError):
            ListNatGatewaysRequest(no_such_param=1)


class _FakeSdkResponse:
    def __init__(self, gateways, next_marker):
        self.nat_gateways = gateways
        self._next_marker = next_marker

    def to_dict(self):
        if self._next_marker:
            return {"nat_gateways": [], "next_marker": self._next_marker}
        return {"nat_gateways": []}


class _FakeSdkGateway:
    def __init__(self, payload):
        self._payload = payload

    @property
    def id(self):
        return self._payload.get("id")

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
    """The SDK fallback must use modules that exist in the official
    huaweicloudsdknat package and wire credentials (including the project id
    required by /v2/{project_id}/nat_gateways) from environment variables
    (BasicCredentials has no env auto-discovery)."""

    def setUp(self):
        self._captured_credentials = None
        self._captured_region = None
        self._fake_client = mock.Mock()
        self._fake_client.list_nat_gateways.return_value = _FakeSdkResponse(
            [_FakeSdkGateway(GATEWAY_1), _FakeSdkGateway(GATEWAY_2)], None)
        try:
            import huaweicloudsdknat.v2 as nat_v2
            from huaweicloudsdknat.v2 import NatClient
        except ImportError:
            self.skipTest("huaweicloudsdknat not installed")
        self._builder_patch = mock.patch.object(
            NatClient, "new_builder",
            classmethod(lambda cls: _FakeSdkBuilder(self)))
        self._builder_patch.start()
        self.addCleanup(self._builder_patch.stop)
        self._nat_v2 = nat_v2

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
        from huaweicloudsdknat.v2 import ListNatGatewaysRequest, NatClient
        from huaweicloudsdknat.v2.region.nat_region import NatRegion
        for obj in (BasicCredentials, Region, HttpConfig,
                    NatClient, ListNatGatewaysRequest, NatRegion):
            self.assertTrue(callable(obj), obj)

    def test_sdk_fallback_returns_gateways_with_env_credentials(self):
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak",
                   HUAWEI_SECRET_KEY="test-sk",
                   HUAWEI_PROJECT_ID="test-project")
        with mock.patch.dict(os.environ, env, clear=True):
            gateways = list_nat_gateways_via_sdk("cn-north-4")
        self.assertEqual(gateways, [GATEWAY_1, GATEWAY_2])
        credentials = self._captured_credentials
        self.assertIsNotNone(credentials)
        self.assertEqual(getattr(credentials, "ak", None), "test-ak")
        self.assertEqual(getattr(credentials, "sk", None), "test-sk")
        self.assertEqual(getattr(credentials, "project_id", None), "test-project")
        self.assertEqual(getattr(self._captured_region, "id", None), "cn-north-4")

    def test_sdk_request_filters_forwarded(self):
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak",
                   HUAWEI_SECRET_KEY="test-sk",
                   HUAWEI_PROJECT_ID="test-project")
        with mock.patch.dict(os.environ, env, clear=True):
            list_nat_gateways_via_sdk("cn-north-4", name="my-nat", spec="2",
                                      status="ACTIVE", router_id="router-9")
        request = self._fake_client.list_nat_gateways.call_args[0][0]
        self.assertEqual(request.name, "my-nat")
        self.assertEqual(request.spec, ["2"])
        self.assertEqual(request.status, ["ACTIVE"])
        self.assertEqual(request.router_id, "router-9")

    def test_explicit_project_id_overrides_env(self):
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak",
                   HUAWEI_SECRET_KEY="test-sk",
                   HUAWEI_PROJECT_ID="env-project")
        with mock.patch.dict(os.environ, env, clear=True):
            list_nat_gateways_via_sdk("cn-north-4", project_id="cli-project")
        self.assertEqual(
            getattr(self._captured_credentials, "project_id", None), "cli-project")

    def test_sdk_fallback_missing_env_credentials_raises_config(self):
        env = dict(self._clean_credential_env(), HUAWEI_PROJECT_ID="test-project")
        with mock.patch.dict(os.environ, env, clear=True):
            with self.assertRaises(ConfigError) as ctx:
                list_nat_gateways_via_sdk("cn-north-4")
        message = str(ctx.exception)
        self.assertIn("AK/SK", message)
        self.assertNotIn("未安装", message)

    def test_sdk_fallback_missing_project_id_raises_config(self):
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak", HUAWEI_SECRET_KEY="test-sk")
        with mock.patch.dict(os.environ, env, clear=True):
            with self.assertRaises(ConfigError) as ctx:
                list_nat_gateways_via_sdk("cn-north-4")
        self.assertIn("project_id", str(ctx.exception))

    def test_sdk_pagination_uses_last_gateway_id_as_marker(self):
        first = _FakeSdkResponse(
            [_FakeSdkGateway(GATEWAY_1), _FakeSdkGateway(GATEWAY_2)], None)
        second = _FakeSdkResponse([_FakeSdkGateway(GATEWAY_3)], None)
        self._fake_client.list_nat_gateways.side_effect = [first, second]
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak",
                   HUAWEI_SECRET_KEY="test-sk",
                   HUAWEI_PROJECT_ID="test-project")
        with mock.patch.dict(os.environ, env, clear=True):
            gateways = list_nat_gateways_via_sdk("cn-north-4", limit=2)
        self.assertEqual(gateways, [GATEWAY_1, GATEWAY_2, GATEWAY_3])
        second_request = self._fake_client.list_nat_gateways.call_args_list[1][0][0]
        self.assertEqual(second_request.marker, "nat-0002")

    def _env(self):
        return dict(self._clean_credential_env(),
                    HUAWEI_ACCESS_KEY="test-ak",
                    HUAWEI_SECRET_KEY="test-sk",
                    HUAWEI_PROJECT_ID="test-project")

    def test_sdk_401_reports_invalid_credentials_not_403(self):
        class _Unauthorized(Exception):
            status_code = 401

        self._fake_client.list_nat_gateways.side_effect = _Unauthorized(
            "401 Unauthorized: invalid AK")
        with mock.patch.dict(os.environ, self._env(), clear=True):
            with self.assertRaises(AuthError) as ctx:
                list_nat_gateways_via_sdk("cn-north-4")
        message = str(ctx.exception)
        self.assertIn("401", message)
        self.assertIn("凭证无效", message)
        self.assertNotIn("无权限访问", message)

    def test_sdk_403_reports_iam_permission_error(self):
        class _Forbidden(Exception):
            status_code = 403

        self._fake_client.list_nat_gateways.side_effect = _Forbidden("403 Forbidden")
        with mock.patch.dict(os.environ, self._env(), clear=True):
            with self.assertRaises(AuthError) as ctx:
                list_nat_gateways_via_sdk("cn-north-4")
        self.assertIn("无权限访问公网NAT网关", str(ctx.exception))

    def test_sdk_pagination_stops_when_marker_repeats(self):
        repeated = _FakeSdkResponse([_FakeSdkGateway(GATEWAY_1)], None)
        self._fake_client.list_nat_gateways.side_effect = [repeated, repeated]
        with mock.patch.dict(os.environ, self._env(), clear=True):
            gateways = list_nat_gateways_via_sdk("cn-north-4", limit=1)
        self.assertEqual(gateways, [GATEWAY_1, GATEWAY_1])
        self.assertEqual(self._fake_client.list_nat_gateways.call_count, 2)


class TestRenderAndNames(unittest.TestCase):
    def test_table_contains_basic_info(self):
        table = render_table([GATEWAY_1, GATEWAY_2, GATEWAY_3])
        for fragment in ("nat-0001", "nat-demo-01", "1", "ACTIVE",
                         "router-0001", "network-0001",
                         "2024-01-01 00:00:00.000000", "nat-inactive-03", "INACTIVE"):
            self.assertIn(fragment, table)

    def test_table_union_extra_fields(self):
        table = render_table([{"id": "nat-x", "custom_field": "cf-value"}])
        self.assertIn("custom_field", table)
        self.assertIn("cf-value", table)

    def test_names(self):
        self.assertEqual(
            gateway_names([GATEWAY_1, GATEWAY_2]),
            ["nat-demo-01", "nat-demo-02"])

    def test_names_fallback_to_id(self):
        self.assertEqual(gateway_names([{"id": "nat-9"}]), ["nat-9"])


class TestMain(unittest.TestCase):
    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("list_nat_gateways.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            rc = main(argv)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    def test_table_output(self):
        rc, out, err = self._run(
            ["--region", "cn-north-4"],
            [(json.dumps({"nat_gateways": [GATEWAY_1, GATEWAY_2]}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("公网NAT网关列表", out)
        self.assertIn("nat-0001", out)
        self.assertIn("ACTIVE", out)
        self.assertEqual(err, "")

    def test_json_output(self):
        rc, out, err = self._run(
            ["--json"],
            [(json.dumps({"nat_gateways": [GATEWAY_1]}), "", 0)])
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual(payload, [GATEWAY_1])

    def test_names_only_output(self):
        rc, out, err = self._run(
            ["--names-only"],
            [(json.dumps({"nat_gateways": [GATEWAY_1, GATEWAY_2]}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("nat-demo-01", out)
        self.assertIn("nat-demo-02", out)
        self.assertNotIn("router_id", out)

    def test_empty_gateways_message(self):
        rc, out, err = self._run(
            ["--region", "cn-south-1"],
            [(json.dumps({"nat_gateways": []}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("当前区域（cn-south-1）无公网NAT网关。", out)
        self.assertNotIn("网关 。", out)
        self.assertNotIn("网关  ", out)

    def test_error_envelope_rc0_exits_1_without_empty_hint(self):
        # Regression (PR #117 R1): an rc=0 API error envelope must never be
        # rendered as 「当前区域无公网NAT网关」 with exit code 0.
        envelope = json.dumps({
            "error_code": "SYS.0403",
            "error_msg": "user is not authorized to perform nat:natGateways:list",
        })
        rc, out, err = self._run(["--region", "cn-north-4"], [(envelope, "", 0)])
        self.assertEqual(rc, 1)
        self.assertIn("无权限访问公网NAT网关", err)
        self.assertNotIn("无公网NAT网关", out)
        self.assertNotIn("公网NAT网关列表", out)

    def test_empty_with_filter_message(self):
        rc, out, _ = self._run(
            ["--name", "my-nat", "--status", "ACTIVE"],
            [(json.dumps({"nat_gateways": []}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("name=my-nat", out)
        self.assertIn("status=ACTIVE", out)

    def test_filters_main_forwarded(self):
        fake = FakeRunner([
            (json.dumps({"nat_gateways": [GATEWAY_1]}), "", 0)])
        with mock.patch("list_nat_gateways.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr"):
            rc = main(["--name", "my-nat", "--spec", "2",
                       "--status", "ACTIVE", "--vpc", "router-7"])
        self.assertEqual(rc, 0)
        self.assertTrue(any("--name=my-nat" in part for part in fake.calls[0]))
        self.assertTrue(any("--spec.1=2" in part for part in fake.calls[0]))
        self.assertTrue(any("--status.1=ACTIVE" in part for part in fake.calls[0]))
        self.assertTrue(any("--router_id=router-7" in part for part in fake.calls[0]))

    def test_page_size_out_of_range_rejected(self):
        for bad in ("0", "2001"):
            with mock.patch("sys.stderr"):
                with self.assertRaises(SystemExit):
                    main(["--page-size", bad])

    def test_empty_json_output(self):
        rc, out, err = self._run(
            ["--json"],
            [(json.dumps({"nat_gateways": []}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out), [])

    def test_empty_names_only_output(self):
        rc, out, err = self._run(
            ["--names-only"],
            [(json.dumps({"nat_gateways": []}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("共 0 个", out)

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
        with mock.patch("list_nat_gateways.list_nat_gateways_via_sdk",
                        side_effect=ConfigError("huaweicloudsdknat 未安装")):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 1)
        self.assertIn("未安装", err)

    def test_hcloud_missing_falls_back_to_sdk(self):
        with mock.patch("list_nat_gateways.list_nat_gateways_via_sdk",
                        return_value=[GATEWAY_1]):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 0)
        self.assertIn("nat-0001", out)

    def test_project_id_forwarded_to_sdk(self):
        with mock.patch("list_nat_gateways.list_nat_gateways_via_sdk",
                        return_value=[GATEWAY_1]) as sdk_mock:
            rc, out, err = self._run(["--project-id", "proj-9"],
                                     [FileNotFoundError()])
        self.assertEqual(rc, 0)
        self.assertEqual(sdk_mock.call_args.kwargs.get("project_id"), "proj-9")

    def test_write_intent_argv_blocked(self):
        rc, out, err = self._run(["--operation", "DeleteNatGateway"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)

    def test_filter_values_with_write_words_are_not_blocked(self):
        # Regression: a gateway named "prod-start" / status "deleting-now" is
        # legitimate read-only filter input and must reach the API.
        results = [
            (json.dumps({"nat_gateways": [GATEWAY_1]}), "", 0),
            (json.dumps({"nat_gateways": [GATEWAY_1]}), "", 0),
        ]
        rc, out, err = self._run(
            ["--name=create-me", "--status", "deleting-now"], results)
        self.assertEqual(rc, 0)
        self.assertNotIn("守卫拦截", err)
        self.assertNotIn("写操作意图", err)


class TestErrorHierarchy(unittest.TestCase):
    def test_subclasses(self):
        for exc in (GuardError, ConfigError, AuthError, ApiError):
            self.assertTrue(issubclass(exc, NatListError))


if __name__ == "__main__":
    unittest.main()
