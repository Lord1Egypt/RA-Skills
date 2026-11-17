import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from list_dns import (  # noqa: E402
    ALLOWED_OPERATIONS,
    ApiError,
    AuthError,
    ConfigError,
    GuardError,
    DnsListError,
    OP_LIST_PRIVATE_ZONES,
    OP_LIST_PUBLIC_ZONES,
    OP_LIST_RECORD_SETS,
    build_command,
    classify_hcloud_failure,
    extract_items,
    extract_json,
    guard_operation,
    guard_write_intent,
    item_names,
    list_dns,
    list_dns_via_sdk,
    main,
    render_markdown,
    render_table,
    resolve_operation,
    resolve_output_path,
    write_markdown,
    _strip_output_value,
    _table_columns,
    _payload_error,
    VIEW_RECORD_SETS,
    VIEW_ZONES,
)

ZONE_PUBLIC_1 = {
    "id": "zone-pub-0001",
    "name": "example.com.",
    "description": "demo public zone",
    "email": "admin@example.com",
    "zone_type": "public",
    "ttl": 300,
    "serial": 1,
    "status": "ACTIVE",
    "record_num": 5,
    "pool_id": "pool-1",
    "project_id": "proj-1",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-02T00:00:00",
    "enterprise_project_id": "0",
    "masters": ["ns1.example.com."],
}
ZONE_PUBLIC_2 = {
    "id": "zone-pub-0002",
    "name": "demo.cn.",
    "zone_type": "public",
    "status": "ACTIVE",
    "record_num": 2,
}
ZONE_PRIVATE_1 = {
    "id": "zone-prv-0001",
    "name": "internal.local.",
    "zone_type": "private",
    "status": "ACTIVE",
    "record_num": 3,
    "router_id": "vpc-router-1",
}
RECORDSET_1 = {
    "id": "rec-0001",
    "name": "www.example.com.",
    "type": "A",
    "ttl": 300,
    "records": ["1.2.3.4"],
    "zone_id": "zone-pub-0001",
    "zone_name": "example.com.",
    "status": "ACTIVE",
    "default": False,
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
        self.assertFalse(guard_write_intent("--region cn-north-4 --json list zones"))
        self.assertFalse(guard_write_intent("show public zone details"))
        self.assertFalse(guard_write_intent("--type public --name example.com"))

    def test_create_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("CreatePublicZone example.com")

    def test_delete_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--operation DeletePrivateZone")

    def test_recordset_mutations_blocked(self):
        for text in ("create record set", "DeleteRecordSet rec-1",
                     "UpdateRecordSet rec-1", "batch create recordsets"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_mutating_verbs_blocked(self):
        for text in ("associate zone", "disassociate zone",
                     "transfer out zone", "enable zone", "disable zone",
                     "bind router", "release zone", "change ttl"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_normalized_separators_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--create-zone")
        with self.assertRaises(GuardError):
            guard_write_intent("update_public_zone")

    def test_read_filter_value_passes(self):
        self.assertFalse(guard_write_intent("--type public"))
        self.assertFalse(guard_write_intent("--status ACTIVE"))
        self.assertFalse(guard_write_intent("--record-type CNAME"))

    def test_operation_guard_rejects_non_list(self):
        with self.assertRaises(GuardError):
            guard_operation("ShowPublicZone")
        with self.assertRaises(GuardError):
            guard_operation("CreatePublicZone")
        for op in ALLOWED_OPERATIONS:
            self.assertTrue(guard_operation(op))


class TestResolveOperation(unittest.TestCase):
    def test_public_default(self):
        self.assertEqual(resolve_operation("public", False), OP_LIST_PUBLIC_ZONES)

    def test_private(self):
        self.assertEqual(resolve_operation("private", False), OP_LIST_PRIVATE_ZONES)

    def test_recordsets_override(self):
        self.assertEqual(resolve_operation("public", True), OP_LIST_RECORD_SETS)
        self.assertEqual(resolve_operation("private", True), OP_LIST_RECORD_SETS)


class TestBuildCommand(unittest.TestCase):
    def test_public_zone_basic(self):
        argv = build_command("cn-north-4", OP_LIST_PUBLIC_ZONES)
        self.assertEqual(argv[0], "DNS")
        self.assertEqual(argv[1], "ListPublicZones")
        self.assertIn("--cli-region=cn-north-4", argv)
        self.assertIn("--limit=100", argv)
        self.assertFalse(any(flag.startswith("--marker") for flag in argv))
        self.assertFalse(any(flag.startswith("--zone_type") for flag in argv))

    def test_private_zone_operation(self):
        argv = build_command("cn-north-4", OP_LIST_PRIVATE_ZONES, zone_type="private")
        self.assertEqual(argv[1], "ListPrivateZones")

    def test_private_zone_forces_required_type(self):
        argv = build_command("cn-north-4", OP_LIST_PRIVATE_ZONES)
        self.assertIn("--type=private", argv)
        self.assertFalse(any(flag.startswith("--zone_type") for flag in argv))

    def test_private_zone_type_forced_even_for_public_caller(self):
        argv = build_command("cn-north-4", OP_LIST_PRIVATE_ZONES,
                             zone_type="public")
        self.assertIn("--type=private", argv)
        self.assertNotIn("--type=public", argv)

    def test_public_zone_has_no_required_type(self):
        argv = build_command("cn-north-4", OP_LIST_PUBLIC_ZONES,
                             zone_type="public")
        self.assertFalse(any(flag.startswith("--type") for flag in argv))

    def test_marker_appended(self):
        argv = build_command("cn-north-4", OP_LIST_PUBLIC_ZONES,
                             marker="tok-123", limit=10)
        self.assertIn("--marker=tok-123", argv)
        self.assertIn("--limit=10", argv)

    def test_filters_forwarded_server_side(self):
        argv = build_command("cn-south-1", OP_LIST_PUBLIC_ZONES,
                             item_id="zone-9", name="example.com", limit=10)
        self.assertIn("--id=zone-9", argv)
        self.assertIn("--name=example.com", argv)
        self.assertIn("--limit=10", argv)

    def test_recordsets_zone_type_and_record_type(self):
        argv = build_command("cn-north-4", OP_LIST_RECORD_SETS,
                             zone_type="private", record_type="A", limit=10)
        self.assertIn("--zone_type=private", argv)
        self.assertIn("--type=A", argv)

    def test_no_write_flags_ever_added(self):
        argv = build_command("cn-north-4", OP_LIST_PUBLIC_ZONES, name="x.com")
        for flag in argv:
            self.assertFalse(flag.lower().lstrip("-").startswith(
                ("create", "delete", "update", "associate", "release", "transfer")))


class TestExtract(unittest.TestCase):
    def test_extract_json_plain(self):
        self.assertEqual(extract_json(json.dumps({"zones": []})), {"zones": []})

    def test_extract_json_with_noise(self):
        self.assertEqual(extract_json("WARNING noise\n{\"a\": 1}\n"), {"a": 1})

    def test_extract_json_invalid(self):
        with self.assertRaises(ApiError):
            extract_json("<html>not json</html>")

    def test_extract_json_tolerates_text_after_envelope(self):
        raw = ('{"errCode": "DNS.1802", "externalMessage": "not authorized"}\n'
               "Retry after checking IAM policy\n-- cli trace --")
        self.assertEqual(
            extract_json(raw),
            {"errCode": "DNS.1802", "externalMessage": "not authorized"})

    def test_extract_items_known_keys(self):
        for key in ("zones", "recordsets", "record_sets"):
            self.assertEqual(extract_items({key: [ZONE_PUBLIC_1]}), [ZONE_PUBLIC_1])
        self.assertEqual(extract_items([ZONE_PUBLIC_1]), [ZONE_PUBLIC_1])
        self.assertEqual(extract_items({"metadata": {}}), [])


class TestPayloadError(unittest.TestCase):
    def test_err_envelope(self):
        text = _payload_error(
            {"errCode": "DNS.1802", "externalMessage": "not authorized"})
        self.assertIn("DNS.1802", text)
        self.assertIn("not authorized", text)

    def test_snake_error(self):
        text = _payload_error(
            {"error_code": "DNS.0009", "error_msg": "not found"})
        self.assertIn("DNS.0009", text)

    def test_camel_code_message(self):
        text = _payload_error({"code": "DNS.1802", "message": "policy denied"})
        self.assertIn("DNS.1802", text)

    def test_nested_error(self):
        text = _payload_error({"error": {"code": "403", "message": "denied"}})
        self.assertIn("403", text)

    def test_no_error(self):
        self.assertIsNone(_payload_error({"zones": []}))
        self.assertIsNone(_payload_error({"zones": [ZONE_PUBLIC_1], "metadata": {"total_count": 1}}))


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

    def test_dns_1802_not_authorized(self):
        err = classify_hcloud_failure(
            "", "DNS.1802 not authorized to perform dns:zone:list", 0)
        self.assertIsInstance(err, AuthError)
        self.assertIn("DNS", str(err))

    def test_dns_no_identity_based_policy(self):
        err = classify_hcloud_failure(
            "", "DNS.1802 The requested resource is not authorized because "
                "the policy does not allow it: no identity-based policy "
                "allows dns:zone:list", 0)
        self.assertIsInstance(err, AuthError)

    def test_generic_api_error(self):
        self.assertIsInstance(classify_hcloud_failure("", "boom", 2), ApiError)

    def test_use_error_marker_with_zero_rc(self):
        err = classify_hcloud_failure(
            "[USE_ERROR]Invalid parameter: zone_type\n\n"
            "Run `hcloud DNS ListPublicZones --help` for details.", "", 0)
        self.assertIsInstance(err, ApiError)
        self.assertIn("参数错误", str(err))
        self.assertIn("--help", str(err))


class TestListDns(unittest.TestCase):
    def test_single_page(self):
        fake = FakeRunner([(
            json.dumps({"zones": [ZONE_PUBLIC_1, ZONE_PUBLIC_2],
                        "metadata": {"total_count": 2}}), "", 0)])
        with mock.patch("list_dns.subprocess.run", fake):
            items = list_dns("cn-north-4", OP_LIST_PUBLIC_ZONES)
        self.assertEqual(items, [ZONE_PUBLIC_1, ZONE_PUBLIC_2])
        self.assertEqual(len(fake.calls), 1)

    def test_pagination_via_last_id_and_total(self):
        page1 = {"zones": [ZONE_PUBLIC_1], "metadata": {"total_count": 2}}
        page2 = {"zones": [ZONE_PUBLIC_2], "metadata": {"total_count": 2}}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("list_dns.subprocess.run", fake):
            items = list_dns("cn-north-4", OP_LIST_PUBLIC_ZONES, limit=1)
        self.assertEqual(items, [ZONE_PUBLIC_1, ZONE_PUBLIC_2])
        self.assertEqual(len(fake.calls), 2)
        self.assertIn("--marker=zone-pub-0001", fake.calls[1])

    def test_pagination_stops_on_empty_page(self):
        page1 = {"zones": [ZONE_PUBLIC_1]}
        page2 = {"zones": [ZONE_PUBLIC_2]}
        page3 = {"zones": []}
        fake = FakeRunner([(json.dumps(page1), "", 0),
                           (json.dumps(page2), "", 0),
                           (json.dumps(page3), "", 0)])
        with mock.patch("list_dns.subprocess.run", fake):
            items = list_dns("cn-north-4", OP_LIST_PUBLIC_ZONES, limit=1)
        self.assertEqual(items, [ZONE_PUBLIC_1, ZONE_PUBLIC_2])

    def test_empty_region(self):
        fake = FakeRunner([(json.dumps({"zones": []}), "", 0)])
        with mock.patch("list_dns.subprocess.run", fake):
            items = list_dns("cn-north-4", OP_LIST_PUBLIC_ZONES)
        self.assertEqual(items, [])

    def test_private_zone_operation_forwarded(self):
        fake = FakeRunner([(json.dumps({"zones": [ZONE_PRIVATE_1]}), "", 0)])
        with mock.patch("list_dns.subprocess.run", fake):
            list_dns("cn-north-4", OP_LIST_PRIVATE_ZONES, zone_type="private")
        self.assertIn("ListPrivateZones", fake.calls[0])
        self.assertTrue(any("--type=private" in part for part in fake.calls[0]))

    def test_recordsets_filters_forwarded_to_cli(self):
        fake = FakeRunner([(json.dumps({"recordsets": [RECORDSET_1]}), "", 0)])
        with mock.patch("list_dns.subprocess.run", fake):
            list_dns("cn-north-4", OP_LIST_RECORD_SETS, zone_type="public",
                     item_id="rec-1", name="www.example.com", record_type="A")
        call = fake.calls[0]
        self.assertTrue(any("--zone_type=public" in part for part in call))
        self.assertTrue(any("--type=A" in part for part in call))
        self.assertTrue(any("--id=rec-1" in part for part in call))
        self.assertTrue(any("--name=www.example.com" in part for part in call))

    def test_use_error_rc0_raises_api_error(self):
        fake = FakeRunner([(
            "[USE_ERROR]Invalid parameter: zone_type\n\n"
            "Run `hcloud DNS ListPublicZones --help` for details.", "", 0)])
        with mock.patch("list_dns.subprocess.run", fake):
            with self.assertRaises(ApiError) as ctx:
                list_dns("cn-north-4", OP_LIST_PUBLIC_ZONES)
        self.assertIn("参数错误", str(ctx.exception))

    def test_error_envelope_rc0_raises_auth(self):
        fake = FakeRunner([(
            json.dumps({"errCode": "DNS.1802",
                        "externalMessage": "not authorized"}), "", 0)])
        with mock.patch("list_dns.subprocess.run", fake):
            with self.assertRaises(AuthError):
                list_dns("cn-north-4", OP_LIST_PUBLIC_ZONES)
        self.assertEqual(len(fake.calls), 1)

    def test_error_envelope_with_trailing_text_rc0_raises(self):
        body = (json.dumps({"code": "DNS.1802", "message": "not authorized"})
                + "\n-- extra cli diagnostics --")
        fake = FakeRunner([(body, "", 0)])
        with mock.patch("list_dns.subprocess.run", fake):
            with self.assertRaises(AuthError):
                list_dns("cn-north-4", OP_LIST_PUBLIC_ZONES)

    def test_nonzero_exit_403(self):
        fake = FakeRunner([("", "403 Forbidden", 1)])
        with mock.patch("list_dns.subprocess.run", fake):
            with self.assertRaises(AuthError):
                list_dns("cn-north-4", OP_LIST_PUBLIC_ZONES)

    def test_nonzero_exit_credentials(self):
        fake = FakeRunner([("", "ERROR: no AK configured", 1)])
        with mock.patch("list_dns.subprocess.run", fake):
            with self.assertRaises(ConfigError):
                list_dns("cn-north-4", OP_LIST_PUBLIC_ZONES)

    def test_timeout(self):
        fake = FakeRunner([subprocess.TimeoutExpired(cmd="hcloud", timeout=120)])
        with mock.patch("list_dns.subprocess.run", fake):
            with self.assertRaises(ApiError):
                list_dns("cn-north-4", OP_LIST_PUBLIC_ZONES)

    def test_sdk_fallback_when_hcloud_missing(self):
        with mock.patch("list_dns.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_dns.list_dns_via_sdk",
                           return_value=[ZONE_PUBLIC_1, ZONE_PUBLIC_2]) as sdk_mock:
            items = list_dns("cn-north-4", OP_LIST_PUBLIC_ZONES,
                             zone_type="public", item_id="zone-1",
                             name="example.com", project_id="proj-1")
        self.assertEqual(items, [ZONE_PUBLIC_1, ZONE_PUBLIC_2])
        kwargs = sdk_mock.call_args.kwargs
        self.assertEqual(kwargs.get("project_id"), "proj-1")
        self.assertEqual(kwargs.get("name"), "example.com")
        self.assertEqual(sdk_mock.call_args.args[1], OP_LIST_PUBLIC_ZONES)

    def test_sdk_fallback_unavailable_raises_config(self):
        with mock.patch("list_dns.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_dns.list_dns_via_sdk",
                           side_effect=ConfigError("huaweicloudsdkdns 未安装")):
            with self.assertRaises(ConfigError):
                list_dns("cn-north-4", OP_LIST_PUBLIC_ZONES)

    def test_sdk_request_signature(self):
        # Regression guard: the official request models must be constructible
        # with exactly the kwargs the fallback path sends.
        try:
            from huaweicloudsdkdns.v2 import (
                ListPublicZonesRequest, ListPrivateZonesRequest,
                ListRecordSetsRequest,
            )
        except ImportError:
            self.skipTest("huaweicloudsdkdns not installed")
        pub = ListPublicZonesRequest(limit=100, marker=None, id="z1",
                                     name="example.com", type="public")
        self.assertEqual(pub.id, "z1")
        prv = ListPrivateZonesRequest(limit=100, marker=None, id="z1",
                                      name="x", type="private")
        self.assertEqual(prv.type, "private")
        rs = ListRecordSetsRequest(limit=100, marker=None, id="r1", name="x",
                                   zone_type="public", type="A")
        self.assertEqual(rs.zone_type, "public")
        self.assertEqual(rs.type, "A")
        with self.assertRaises(TypeError):
            ListPublicZonesRequest(no_such_param=1)


class _FakeSdkResponse:
    def __init__(self, items, total=None, key="zones"):
        setattr(self, key, items)
        if key != "zones":
            self.zones = None
        if key != "recordsets":
            self.recordsets = None
        self._total = total

    def to_dict(self):
        return {"metadata": {"total_count": self._total}}


class _FakeSdkZone:
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
    """The SDK fallback must use modules that exist in the official
    huaweicloudsdkdns package and wire credentials (including the project id)
    from environment variables (BasicCredentials has no env auto-discovery)."""

    def setUp(self):
        self._captured_credentials = None
        self._captured_region = None
        self._fake_client = mock.Mock()
        self._fake_client.list_public_zones.return_value = _FakeSdkResponse(
            [_FakeSdkZone(ZONE_PUBLIC_1), _FakeSdkZone(ZONE_PUBLIC_2)], total=2)
        try:
            import huaweicloudsdkdns.v2 as dns_v2
        except ImportError:
            self.skipTest("huaweicloudsdkdns not installed")
        self._builder_patch = mock.patch.object(
            dns_v2.DnsClient, "new_builder",
            classmethod(lambda cls: _FakeSdkBuilder(self)))
        self._builder_patch.start()
        self.addCleanup(self._builder_patch.stop)

    def _clean_credential_env(self):
        credential_vars = (
            "HW_ACCESS_KEY", "HUAWEI_ACCESS_KEY", "HUAWEICLOUD_SDK_AK",
            "HUAWEI_CLOUD_ACCESS_KEY", "HW_SECRET_KEY", "HUAWEI_SECRET_KEY",
            "HUAWEICLOUD_SDK_SK", "HUAWEI_CLOUD_SECRET_KEY", "HW_PROJECT_ID",
            "HUAWEI_PROJECT_ID", "HUAWEICLOUD_SDK_PROJECT_ID",
            "HUAWEI_CLOUD_PROJECT_ID",
        )
        return {name: "" for name in credential_vars}

    def test_official_sdk_imports_resolve(self):
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkdns.v2 import (
            DnsClient, ListPublicZonesRequest, ListPrivateZonesRequest,
            ListRecordSetsRequest,
        )
        from huaweicloudsdkdns.v2.region.dns_region import DnsRegion
        for obj in (BasicCredentials, Region, HttpConfig, DnsClient,
                    ListPublicZonesRequest, ListPrivateZonesRequest,
                    ListRecordSetsRequest, DnsRegion):
            self.assertTrue(callable(obj), obj)

    def test_sdk_fallback_returns_zones_with_env_credentials(self):
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak",
                   HUAWEI_SECRET_KEY="test-sk",
                   HUAWEI_PROJECT_ID="test-project")
        with mock.patch.dict(os.environ, env, clear=True):
            items = list_dns_via_sdk("cn-north-4", OP_LIST_PUBLIC_ZONES)
        self.assertEqual(items, [ZONE_PUBLIC_1, ZONE_PUBLIC_2])
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
            list_dns_via_sdk("cn-north-4", OP_LIST_PUBLIC_ZONES,
                             project_id="cli-project")
        self.assertEqual(
            getattr(self._captured_credentials, "project_id", None), "cli-project")

    def test_sdk_fallback_missing_env_credentials_raises_config(self):
        env = dict(self._clean_credential_env(), HUAWEI_PROJECT_ID="test-project")
        with mock.patch.dict(os.environ, env, clear=True):
            with self.assertRaises(ConfigError) as ctx:
                list_dns_via_sdk("cn-north-4", OP_LIST_PUBLIC_ZONES)
        message = str(ctx.exception)
        self.assertIn("AK/SK", message)
        self.assertNotIn("未安装", message)

    def test_sdk_fallback_missing_project_id_raises_config(self):
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak", HUAWEI_SECRET_KEY="test-sk")
        with mock.patch.dict(os.environ, env, clear=True):
            with self.assertRaises(ConfigError) as ctx:
                list_dns_via_sdk("cn-north-4", OP_LIST_PUBLIC_ZONES)
        self.assertIn("project_id", str(ctx.exception))

    def test_sdk_recordsets_uses_record_sets_client(self):
        self._fake_client.list_record_sets.return_value = _FakeSdkResponse(
            [_FakeSdkZone(RECORDSET_1)], total=1, key="recordsets")
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak", HUAWEI_SECRET_KEY="test-sk",
                   HUAWEI_PROJECT_ID="test-project")
        with mock.patch.dict(os.environ, env, clear=True):
            items = list_dns_via_sdk("cn-north-4", OP_LIST_RECORD_SETS,
                                     zone_type="public", record_type="A")
        self.assertEqual(items, [RECORDSET_1])
        request = self._fake_client.list_record_sets.call_args[0][0]
        self.assertEqual(request.zone_type, "public")
        self.assertEqual(request.type, "A")

    def test_sdk_private_zones_uses_private_client(self):
        self._fake_client.list_private_zones.return_value = _FakeSdkResponse(
            [_FakeSdkZone(ZONE_PRIVATE_1)], total=1)
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak", HUAWEI_SECRET_KEY="test-sk",
                   HUAWEI_PROJECT_ID="test-project")
        with mock.patch.dict(os.environ, env, clear=True):
            items = list_dns_via_sdk("cn-north-4", OP_LIST_PRIVATE_ZONES,
                                     zone_type="private")
        self.assertEqual(items, [ZONE_PRIVATE_1])
        request = self._fake_client.list_private_zones.call_args[0][0]
        self.assertEqual(request.type, "private")


class TestNormalizeAndRender(unittest.TestCase):
    def test_table_contains_basic_info(self):
        table = render_table([ZONE_PUBLIC_1, ZONE_PUBLIC_2])
        for fragment in ("zone-pub-0001", "example.com.", "public", "ACTIVE",
                         "admin@example.com", "5"):
            self.assertIn(fragment, table)

    def test_table_recordsets(self):
        table = render_table([RECORDSET_1])
        for fragment in ("rec-0001", "www.example.com.", "A", "1.2.3.4"):
            self.assertIn(fragment, table)

    def test_table_missing_field_rendered_dash(self):
        table = render_table([ZONE_PUBLIC_2])
        self.assertIn("-", table)

    def test_names(self):
        self.assertEqual(
            item_names([ZONE_PUBLIC_1, ZONE_PUBLIC_2]), ["example.com.", "demo.cn."])

    def test_names_fallback_to_id(self):
        self.assertEqual(item_names([{"id": "zone-9"}]), ["zone-9"])


class TestMain(unittest.TestCase):
    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("list_dns.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            rc = main(argv)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    def test_table_output(self):
        rc, out, err = self._run(
            ["--region", "cn-north-4"],
            [(json.dumps({"zones": [ZONE_PUBLIC_1, ZONE_PUBLIC_2]}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("DNS 公网域名", out)
        self.assertIn("zone-pub-0001", out)
        self.assertEqual(err, "")

    def test_private_table_output(self):
        rc, out, _ = self._run(
            ["--type", "private"],
            [(json.dumps({"zones": [ZONE_PRIVATE_1]}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("DNS 私网域名", out)
        self.assertIn("internal.local.", out)

    def test_private_argv_sends_required_type(self):
        fake = FakeRunner([(json.dumps({"zones": [ZONE_PRIVATE_1]}), "", 0)])
        with mock.patch("list_dns.subprocess.run", fake), \
                mock.patch("sys.stdout"), mock.patch("sys.stderr"):
            rc = main(["--type", "private"])
        self.assertEqual(rc, 0)
        self.assertTrue(any("ListPrivateZones" in part
                            for part in fake.calls[0]))
        self.assertTrue(any("--type=private" in part
                            for part in fake.calls[0]))

    def test_recordsets_table_output(self):
        rc, out, _ = self._run(
            ["--recordsets"],
            [(json.dumps({"recordsets": [RECORDSET_1]}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("DNS 记录集", out)
        self.assertIn("rec-0001", out)

    def test_json_output(self):
        rc, out, err = self._run(
            ["--json"],
            [(json.dumps({"zones": [ZONE_PUBLIC_1]}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out), [ZONE_PUBLIC_1])

    def test_names_only_output(self):
        rc, out, err = self._run(
            ["--names-only"],
            [(json.dumps({"zones": [ZONE_PUBLIC_1, ZONE_PUBLIC_2]}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("example.com.", out)
        self.assertIn("demo.cn.", out)
        self.assertNotIn("admin@example.com", out)

    def test_empty_zone_message(self):
        rc, out, err = self._run(
            ["--region", "cn-south-1"],
            [(json.dumps({"zones": []}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("无 DNS 公网域名", out)
        self.assertIn("cn-south-1", out)

    def test_empty_recordsets_with_filter_message(self):
        rc, out, _ = self._run(
            ["--recordsets", "--type", "private", "--name", "x.local"],
            [(json.dumps({"recordsets": []}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("无 DNS 记录集", out)
        self.assertIn("name=x.local", out)

    def test_name_filter_forwarded(self):
        fake = FakeRunner([(json.dumps({"zones": [ZONE_PUBLIC_1]}), "", 0)])
        with mock.patch("list_dns.subprocess.run", fake), \
                mock.patch("sys.stdout"), mock.patch("sys.stderr"):
            rc = main(["--name", "example.com"])
        self.assertEqual(rc, 0)
        self.assertTrue(any("--name=example.com" in part for part in fake.calls[0]))

    def test_empty_json_output(self):
        rc, out, err = self._run(
            ["--json"], [(json.dumps({"zones": []}), "", 0)])
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
        with mock.patch("list_dns.list_dns_via_sdk",
                        side_effect=ConfigError("huaweicloudsdkdns 未安装")):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 1)
        self.assertIn("未安装", err)

    def test_hcloud_missing_falls_back_to_sdk(self):
        with mock.patch("list_dns.list_dns_via_sdk",
                        return_value=[ZONE_PUBLIC_1]):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 0)
        self.assertIn("zone-pub-0001", out)

    def test_project_id_forwarded_to_sdk(self):
        with mock.patch("list_dns.list_dns_via_sdk",
                        return_value=[ZONE_PUBLIC_1]) as sdk_mock:
            rc, out, err = self._run(["--project-id", "proj-9"],
                                     [FileNotFoundError()])
        self.assertEqual(rc, 0)
        self.assertEqual(sdk_mock.call_args.kwargs.get("project_id"), "proj-9")

    def test_write_intent_argv_blocked(self):
        rc, out, err = self._run(["--operation", "DeletePublicZone"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)

    def test_write_keyword_argv_blocked(self):
        rc, out, err = self._run(["--id", "release-me"], [])
        self.assertEqual(rc, 1)
        self.assertIn("守卫拦截", err)


class TestOutputValueStripping(unittest.TestCase):
    def test_strips_long_and_short_forms(self):
        cases = [
            (["--output", "./delete-report.md"], []),
            (["-o", "./delete-report.md"], []),
            (["--output=./delete-report.md"], []),
            (["-o"], []),
            (["--recordsets", "--output", "a.md", "--name", "x.com"],
             ["--recordsets", "--name", "x.com"]),
        ]
        for argv, expected in cases:
            self.assertEqual(_strip_output_value(argv), expected)

    def test_keeps_flag_after_valueless_output(self):
        self.assertEqual(
            _strip_output_value(["-o", "--recordsets"]), ["--recordsets"])

    def test_attached_short_value_stripped(self):
        self.assertEqual(
            _strip_output_value(["-o./delete-report.md"]), [])

    def test_write_intent_outside_output_still_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent(" ".join(
                _strip_output_value(["--output", "out.md",
                                     "--operation", "DeletePublicZone"])))


class TestMarkdownRender(unittest.TestCase):
    def test_header_only_when_empty(self):
        columns = _table_columns([], VIEW_ZONES)
        md = render_markdown([], columns)
        lines = md.strip().splitlines()
        self.assertEqual(len(lines), 2)
        self.assertIn("name", lines[0])
        self.assertIn("zone_type", lines[0])
        self.assertIn("ttl", lines[0])
        self.assertTrue(lines[1].startswith("| ---"))

    def test_zone_columns_match_preferred_order(self):
        columns = _table_columns([ZONE_PUBLIC_1, ZONE_PUBLIC_2], VIEW_ZONES)
        self.assertEqual(
            columns[:6],
            ["name", "zone_type", "status", "record_num", "email", "ttl"])

    def test_recordset_columns_match_preferred_order(self):
        columns = _table_columns([RECORDSET_1], VIEW_RECORD_SETS)
        self.assertEqual(
            columns[:5], ["name", "type", "ttl", "records", "zone_name"])

    def test_export_columns_equal_table_columns(self):
        for items, view in (([ZONE_PUBLIC_1, ZONE_PUBLIC_2], VIEW_ZONES),
                            ([RECORDSET_1], VIEW_RECORD_SETS)):
            self.assertEqual(
                _table_columns(items, view),
                _table_columns(items, view))
            md = render_markdown(items, _table_columns(items, view))
            header = md.splitlines()[0]
            table = render_table(items, view)
            table_header = table.splitlines()[0]
            for column in _table_columns(items, view):
                self.assertIn(column, header)
                self.assertIn(column, table_header)

    def test_missing_field_rendered_dash(self):
        columns = _table_columns([ZONE_PUBLIC_1, ZONE_PUBLIC_2], VIEW_ZONES)
        row = render_markdown([ZONE_PUBLIC_2], columns).splitlines()[2]
        cells = [cell.strip() for cell in row.strip("|").split("|")]
        email_index = columns.index("email")
        self.assertEqual(cells[email_index], "-")

    def test_nested_fields_compact_json(self):
        item = dict(ZONE_PUBLIC_1)
        item["tags"] = {"a": 1, "b": [2, 3]}
        columns = _table_columns([item], VIEW_ZONES)
        md = render_markdown([item], columns)
        self.assertIn('{"a":1,"b":[2,3]}', md)

    def test_pipe_and_newline_escaped(self):
        item = {"name": "a|b.example.com.", "zone_type": "public",
                "status": "ACTIVE\nMULTI", "record_num": 1,
                "email": "x@y.z", "ttl": 300}
        columns = _table_columns([item], VIEW_ZONES)
        md = render_markdown([item], columns)
        self.assertIn("a\\|b.example.com.", md)
        self.assertIn("ACTIVE<br>MULTI", md)

    def test_recordset_values_rendered(self):
        md = render_markdown([RECORDSET_1],
                             _table_columns([RECORDSET_1], VIEW_RECORD_SETS))
        self.assertIn("www.example.com.", md)
        self.assertIn("A", md)
        self.assertIn('["1.2.3.4"]', md)
        self.assertIn("example.com.", md)


class TestWriteMarkdown(unittest.TestCase):
    def test_writes_utf8_and_no_residue(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "zones.md")
            write_markdown(target, "| 名称 | 类型 |\n| --- | --- |\n| 例子 | A |\n")
            with open(target, encoding="utf-8") as handle:
                content = handle.read()
            self.assertIn("例子", content)
            leftovers = [name for name in os.listdir(tmp)
                         if name != "zones.md"]
            self.assertEqual(leftovers, [])

    def test_missing_directory_raises_without_creating(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = os.path.join(tmp, "nope", "zones.md")
            with self.assertRaises(ApiError) as ctx:
                write_markdown(missing, "x")
            self.assertIn("Markdown 文件写出失败", str(ctx.exception))
            self.assertFalse(os.path.exists(os.path.join(tmp, "nope")))

    def test_unwritable_directory_raises_and_cleans_up(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "zones.md")
            with mock.patch("list_dns.tempfile.NamedTemporaryFile",
                            side_effect=OSError("permission denied")):
                with self.assertRaises(ApiError) as ctx:
                    write_markdown(target, "x")
            self.assertIn("Markdown 文件写出失败", str(ctx.exception))
            self.assertEqual(os.listdir(tmp), [])

    def test_replace_failure_leaves_no_temp(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "zones.md")
            with mock.patch("list_dns.os.replace",
                            side_effect=OSError("disk full")):
                with self.assertRaises(ApiError):
                    write_markdown(target, "x")
            self.assertFalse(os.path.exists(target))
            self.assertEqual(os.listdir(tmp), [])

    def test_resolve_output_path(self):
        self.assertIsNone(resolve_output_path(None, VIEW_ZONES))
        self.assertEqual(
            os.path.basename(resolve_output_path(True, VIEW_ZONES)),
            "dns_zones.md")
        self.assertEqual(
            os.path.basename(resolve_output_path(True, VIEW_RECORD_SETS)),
            "dns_recordsets.md")
        self.assertEqual(resolve_output_path("/tmp/a.md", VIEW_ZONES),
                         "/tmp/a.md")


class TestMainExport(unittest.TestCase):
    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("list_dns.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            rc = main(argv)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    def test_explicit_output_zone(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "out.md")
            rc, out, err = self._run(
                ["--output", target],
                [(json.dumps({"zones": [ZONE_PUBLIC_1, ZONE_PUBLIC_2]}), "", 0)])
            self.assertEqual(rc, 0)
            self.assertIn(os.path.abspath(target), out)
            self.assertTrue(os.path.exists(target))
            with open(target, encoding="utf-8") as handle:
                content = handle.read()
            self.assertIn("| name |", content)
            self.assertIn("example.com.", content)
            self.assertIn("admin@example.com", content)
            self.assertTrue(content.endswith("\n"))

    def test_explicit_output_recordsets(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "rs.md")
            rc, out, err = self._run(
                ["--recordsets", "--output", target],
                [(json.dumps({"recordsets": [RECORDSET_1]}), "", 0)])
            self.assertEqual(rc, 0)
            self.assertTrue(os.path.exists(target))
            with open(target, encoding="utf-8") as handle:
                content = handle.read()
            self.assertIn("| zone_name |", content)
            self.assertIn("www.example.com.", content)

    def test_default_zone_filename(self):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch("list_dns.os.getcwd", return_value=tmp):
                rc, out, err = self._run(
                    ["-o"],
                    [(json.dumps({"zones": [ZONE_PUBLIC_1]}), "", 0)])
            self.assertEqual(rc, 0)
            self.assertTrue(os.path.exists(os.path.join(tmp, "dns_zones.md")))

    def test_default_recordsets_filename(self):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch("list_dns.os.getcwd", return_value=tmp):
                rc, out, err = self._run(
                    ["--recordsets", "-o"],
                    [(json.dumps({"recordsets": [RECORDSET_1]}), "", 0)])
            self.assertEqual(rc, 0)
            self.assertTrue(os.path.exists(
                os.path.join(tmp, "dns_recordsets.md")))

    def test_private_zone_export_sends_required_type(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "private.md")
            fake = FakeRunner([(json.dumps({"zones": [ZONE_PRIVATE_1]}),
                                "", 0)])
            with mock.patch("list_dns.subprocess.run", fake), \
                    mock.patch("sys.stdout"), mock.patch("sys.stderr"):
                rc = main(["--type", "private", "-o", target])
            self.assertEqual(rc, 0)
            self.assertTrue(any("ListPrivateZones" in part
                                for part in fake.calls[0]))
            self.assertTrue(any("--type=private" in part
                                for part in fake.calls[0]))
            self.assertTrue(os.path.exists(target))
            with open(target, encoding="utf-8") as handle:
                content = handle.read()
            self.assertIn("internal.local.", content)

    def test_empty_result_writes_header_only_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "empty.md")
            rc, out, err = self._run(
                ["--output", target],
                [(json.dumps({"zones": []}), "", 0)])
            self.assertEqual(rc, 0)
            self.assertIn("无 DNS 公网域名", out)
            with open(target, encoding="utf-8") as handle:
                lines = handle.read().strip().splitlines()
            self.assertEqual(len(lines), 2)
            self.assertIn("zone_type", lines[0])

    def test_error_envelope_with_output_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "dns_zones.md")
            rc, out, err = self._run(
                ["--output", target],
                [(json.dumps({"errCode": "DNS.1802",
                              "externalMessage": "not authorized"}), "", 0)])
            self.assertEqual(rc, 1)
            self.assertIn("无权限访问云解析服务", err)
            self.assertNotIn("无 DNS 公网域名", out)
            self.assertFalse(os.path.exists(target))

    def test_filters_apply_to_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "filtered.md")
            fake = FakeRunner([(json.dumps({"recordsets": [RECORDSET_1]}),
                                "", 0)])
            with mock.patch("list_dns.subprocess.run", fake), \
                    mock.patch("sys.stdout"), mock.patch("sys.stderr"):
                rc = main(["--recordsets", "--record-type", "A",
                           "--name", "www.example.com", "--output", target])
            self.assertEqual(rc, 0)
            call = fake.calls[0]
            self.assertTrue(any("--type=A" in part for part in call))
            self.assertTrue(any("--name=www.example.com" in part for part in call))
            with open(target, encoding="utf-8") as handle:
                content = handle.read()
            self.assertIn("www.example.com.", content)
            self.assertNotIn("a|b", content)

    def test_output_path_with_delete_word_not_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "delete-report.md")
            rc, out, err = self._run(
                ["--output", target],
                [(json.dumps({"zones": [ZONE_PUBLIC_1]}), "", 0)])
            self.assertEqual(rc, 0)
            self.assertEqual(err, "")
            self.assertTrue(os.path.exists(target))

    def test_real_write_intent_still_blocked_with_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "out.md")
            rc, out, err = self._run(
                ["--output", target, "--operation", "DeletePublicZone"], [])
            self.assertEqual(rc, 1)
            self.assertIn("写操作意图", err)
            self.assertFalse(os.path.exists(target))

    def test_output_equals_form(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "eq.md")
            rc, out, err = self._run(
                ["--output=%s" % target],
                [(json.dumps({"zones": [ZONE_PUBLIC_1]}), "", 0)])
            self.assertEqual(rc, 0)
            self.assertTrue(os.path.exists(target))

    def test_json_mode_does_not_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "json.md")
            rc, out, err = self._run(
                ["--json", "--output", target],
                [(json.dumps({"zones": [ZONE_PUBLIC_1]}), "", 0)])
            self.assertEqual(rc, 0)
            self.assertFalse(os.path.exists(target))
            self.assertEqual(json.loads(out), [ZONE_PUBLIC_1])

    def test_names_only_does_not_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "names.md")
            rc, out, err = self._run(
                ["--names-only", "--output", target],
                [(json.dumps({"zones": [ZONE_PUBLIC_1]}), "", 0)])
            self.assertEqual(rc, 0)
            self.assertFalse(os.path.exists(target))

    def test_unwritable_output_returns_exit_1(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "nope", "out.md")
            rc, out, err = self._run(
                ["--output", target],
                [(json.dumps({"zones": [ZONE_PUBLIC_1]}), "", 0)])
            self.assertEqual(rc, 1)
            self.assertIn("Markdown 文件写出失败", err)
            self.assertFalse(os.path.exists(os.path.join(tmp, "nope")))

    def test_export_fields_equal_terminal_table(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "out.md")
            rc, out, err = self._run(
                ["--output", target],
                [(json.dumps({"zones": [ZONE_PUBLIC_1, ZONE_PUBLIC_2]}),
                  "", 0)])
            self.assertEqual(rc, 0)
            with open(target, encoding="utf-8") as handle:
                md_header = handle.readline().strip()
            terminal_header = render_table(
                [ZONE_PUBLIC_1, ZONE_PUBLIC_2], VIEW_ZONES).splitlines()[0]
            md_columns = [cell.strip() for cell in
                          md_header.strip("|").split("|")]
            for column in md_columns:
                self.assertIn(column, terminal_header)


class TestErrorHierarchy(unittest.TestCase):
    def test_subclasses(self):
        for exc in (GuardError, ConfigError, AuthError, ApiError):
            self.assertTrue(issubclass(exc, DnsListError))


if __name__ == "__main__":
    unittest.main()