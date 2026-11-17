import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(
    0,
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                 "scripts"),
)

import list_vpcep  # noqa: E402
from list_vpcep import (  # noqa: E402
    ALLOWED_OPERATIONS,
    OP_LIST_ENDPOINTS,
    OP_LIST_ENDPOINT_SERVICE,
    OP_LIST_SERVICE_PUBLIC_DETAILS,
    ApiError,
    AuthError,
    ConfigError,
    GuardError,
    InvalidRequestError,
    VpcepListError,
    build_command,
    classify_hcloud_failure,
    classify_payload_error,
    extract_items,
    extract_json,
    filter_items,
    guard_argv,
    guard_operation,
    guard_write_intent,
    is_available,
    is_non_available,
    item_name,
    list_vpcep,
    list_vpcep_via_sdk,
    main,
    render_markdown,
    render_table,
    resolve_operation,
    write_markdown_atomic,
)

ENDPOINT_AVAILABLE = {
    "id": "ep-0001",
    "endpoint_service_name": "vpcep-svc-alpha",
    "status": "available",
    "endpoint_service_id": "svc-0001",
    "service_type": "interface",
    "ip": "192.168.1.10",
    "vpc_id": "vpc-0001",
    "enable_dns": True,
    "enable_whitelist": False,
    "created_at": "2024-01-01T00:00:00Z",
}
ENDPOINT_FAILED = {
    "id": "ep-0002",
    "endpoint_service_name": "vpcep-svc-beta",
    "status": "failed",
    "endpoint_service_id": "svc-0002",
    "service_type": "interface",
    "ip": "192.168.1.11",
    "vpc_id": "vpc-0002",
    "enable_dns": False,
    "enable_whitelist": True,
    "created_at": "2024-01-02T00:00:00Z",
}
ENDPOINT_CREATING = {
    "id": "ep-0003",
    "endpoint_service_name": "vpcep-svc-gamma",
    "status": "creating",
    "endpoint_service_id": "svc-0003",
    "service_type": "interface",
    "ip": "192.168.1.12",
    "vpc_id": "vpc-0003",
    "enable_dns": True,
    "enable_whitelist": True,
    "created_at": "2024-01-03T00:00:00Z",
}
SERVICE_ITEM = {
    "id": "svc-0001",
    "service_name": "my-endpoint-service",
    "status": "available",
    "server_type": "vlan",
    "service_type": "interface",
    "created_at": "2024-01-01T00:00:00Z",
}
SERVICE_FAILED = {
    "id": "svc-0002",
    "service_name": "broken-endpoint-service",
    "status": "failed",
    "server_type": "vxlan",
    "service_type": "interface",
    "created_at": "2024-01-02T00:00:00Z",
}
PUBLIC_ITEM = {
    "id": "pub-0001",
    "service_name": "obs",
    "service_type": "interface",
    "created_at": "2024-01-01T00:00:00Z",
}
PUBLIC_ITEM_DNS = {
    "id": "pub-0002",
    "service_name": "dns",
    "service_type": "interface",
    "created_at": "2024-01-02T00:00:00Z",
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
        self.assertFalse(guard_write_intent("--view endpoint --limit 100 list"))
        self.assertFalse(guard_write_intent("show endpoint services"))
        self.assertFalse(guard_write_intent("--name vpcep-svc-alpha"))

    def test_create_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("CreateEndpoint ep-1")
        with self.assertRaises(GuardError):
            guard_write_intent("--name create-me")

    def test_delete_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--action delete")
        with self.assertRaises(GuardError):
            guard_write_intent("DeleteEndpointService svc-1")

    def test_update_and_batch_blocked(self):
        for text in ("UpdateEndpoint ep-1", "batch add permissions",
                     "batch-remove permissions", "add-whitelist ep-1",
                     "remove-whitelist ep-1", "accept endpoint",
                     "reject endpoint", "bind routetable", "unbind routetable"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_normalized_separators_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--create-endpoint")
        with self.assertRaises(GuardError):
            guard_write_intent("update_endpoint_service")

    def test_status_filter_value_is_exempt(self):
        self.assertFalse(guard_argv(["--status", "rejected"]))
        self.assertFalse(guard_argv(["--status=creating"]))
        self.assertFalse(guard_argv(["--status", "deleting"]))

    def test_sort_key_values_exempt(self):
        self.assertFalse(guard_argv(["--sort-key", "update_at"]))
        self.assertFalse(guard_argv(["--sort-key=create_at"]))

    def test_non_exempt_tokens_still_blocked(self):
        with self.assertRaises(GuardError):
            guard_argv(["--view", "endpoint", "--name", "create-me"])
        with self.assertRaises(GuardError):
            guard_argv(["--id", "delete-me"])
        with self.assertRaises(GuardError):
            guard_argv(["--action", "delete"])

    def test_operation_guard_rejects_non_list(self):
        with self.assertRaises(GuardError):
            guard_operation("ShowEndpoint")
        with self.assertRaises(GuardError):
            guard_operation("CreateEndpoint")
        for operation in ALLOWED_OPERATIONS:
            self.assertTrue(guard_operation(operation))

class TestResolveOperation(unittest.TestCase):
    def test_default_and_views(self):
        self.assertEqual(resolve_operation("endpoint"), OP_LIST_ENDPOINTS)
        self.assertEqual(resolve_operation("service"), OP_LIST_ENDPOINT_SERVICE)
        self.assertEqual(resolve_operation("public"),
                         OP_LIST_SERVICE_PUBLIC_DETAILS)
        self.assertEqual(resolve_operation(None), OP_LIST_ENDPOINTS)

    def test_explicit_operation_wins(self):
        self.assertEqual(
            resolve_operation("public", OP_LIST_ENDPOINTS), OP_LIST_ENDPOINTS)


class TestBuildCommand(unittest.TestCase):
    def test_endpoint_basic(self):
        argv = build_command("cn-north-4", OP_LIST_ENDPOINTS)
        self.assertEqual(argv[0], "VPCEP")
        self.assertEqual(argv[1], "ListEndpoints")
        self.assertIn("--cli-region=cn-north-4", argv)
        self.assertIn("--limit=100", argv)
        self.assertIn("--offset=0", argv)

    def test_endpoint_filters_forwarded(self):
        argv = build_command(
            "cn-south-1", OP_LIST_ENDPOINTS, view="endpoint",
            service_name="vpcep-svc", item_id="ep-1", vpc_id="vpc-1",
            limit=10, offset=20, sort_key="create_at", sort_dir="asc")
        self.assertIn("--endpoint_service_name=vpcep-svc", argv)
        self.assertIn("--id=ep-1", argv)
        self.assertIn("--vpc_id=vpc-1", argv)
        self.assertIn("--offset=20", argv)
        self.assertIn("--sort_key=create_at", argv)
        self.assertIn("--sort_dir=asc", argv)

    def test_service_status_forwarded(self):
        argv = build_command(
            "cn-north-4", OP_LIST_ENDPOINT_SERVICE, view="service",
            status="failed")
        self.assertIn("--status=failed", argv)

    def test_endpoint_does_not_forward_status(self):
        argv = build_command(
            "cn-north-4", OP_LIST_ENDPOINTS, view="endpoint",
            status="failed")
        self.assertFalse(any(flag.startswith("--status") for flag in argv))

    def test_vpc_id_only_for_endpoint_view(self):
        argv = build_command(
            "cn-north-4", OP_LIST_SERVICE_PUBLIC_DETAILS, view="public",
            vpc_id="vpc-1")
        self.assertFalse(any(flag.startswith("--vpc_id") for flag in argv))

    def test_no_write_flags_ever_added(self):
        for view, operation in (
                ("endpoint", OP_LIST_ENDPOINTS),
                ("service", OP_LIST_ENDPOINT_SERVICE),
                ("public", OP_LIST_SERVICE_PUBLIC_DETAILS)):
            argv = build_command("cn-north-4", operation, view=view,
                                 name="x")
            for flag in argv:
                self.assertFalse(flag.lower().lstrip("-").startswith(
                    ("create", "delete", "update", "accept", "reject")))


class TestExtractAndClassify(unittest.TestCase):
    def test_extract_json_plain(self):
        self.assertEqual(extract_json(json.dumps({"endpoints": []})),
                         {"endpoints": []})

    def test_extract_json_with_noise(self):
        self.assertEqual(extract_json("WARNING noise\n{\"a\": 1}\n"), {"a": 1})

    def test_extract_json_invalid(self):
        with self.assertRaises(ApiError):
            extract_json("<html>not json</html>")

    def test_extract_items_keys(self):
        self.assertEqual(extract_items({"endpoints": [ENDPOINT_AVAILABLE]}),
                         [ENDPOINT_AVAILABLE])
        self.assertEqual(
            extract_items({"endpoint_services": [SERVICE_ITEM]},
                          view="service"), [SERVICE_ITEM])
        self.assertEqual(extract_items([PUBLIC_ITEM]), [PUBLIC_ITEM])
        self.assertEqual(extract_items({"total_count": 0}), [])

    def test_payload_403_is_auth_error_with_zero_rc(self):
        payload = {
            "error_code": "common.01010013",
            "error_msg": "User is not authorized to perform: "
                         "vpcep:endpoints:list on resource: vpcep:*",
        }
        error = classify_payload_error(payload, view="endpoint")
        self.assertIsInstance(error, AuthError)
        self.assertIn("IAM", str(error))

    def test_payload_invalid_id(self):
        payload = {"error_code": "common.01010003",
                   "error_msg": "Invalid id: not-a-uuid"}
        error = classify_payload_error(payload, item_id="not-a-uuid")
        self.assertIsInstance(error, InvalidRequestError)
        self.assertIn("not-a-uuid", str(error))

    def test_payload_bad_request_invalid_id(self):
        error = classify_payload_error(
            {"error_code": "SYS.0400",
             "error_msg": "Bad request: id must be an string size must be "
                          "between 36 and 36"},
            item_id="not-a-uuid")
        self.assertIsInstance(error, InvalidRequestError)
        self.assertIn("ID", str(error))

    def test_payload_generic(self):
        error = classify_payload_error(
            {"error_code": "SVC.0001", "error_msg": "boom"})
        self.assertIsInstance(error, ApiError)

    def test_missing_credentials(self):
        error = classify_hcloud_failure(
            "", "ERROR: cli-ak is empty, please run hcloud configure", 1)
        self.assertIsInstance(error, ConfigError)
        self.assertIn("AK/SK", str(error))

    def test_auth_403(self):
        error = classify_hcloud_failure(
            "", '{"error_code":"ApiGW.0301","error_msg":"403 Forbidden"}', 1)
        self.assertIsInstance(error, AuthError)
        self.assertIn("IAM", str(error))

    def test_use_error_marker_with_zero_rc(self):
        error = classify_hcloud_failure(
            "[USE_ERROR]Invalid parameter: vpc_id\n"
            "Run `hcloud VPCEP ListEndpoints --help` for details.", "", 0)
        self.assertIsInstance(error, ApiError)
        self.assertIn("参数错误", str(error))
        self.assertIn("--help", str(error))

    def test_generic_api_error(self):
        self.assertIsInstance(
            classify_hcloud_failure("", "boom", 2), ApiError)


class TestListVpcep(unittest.TestCase):
    def test_single_page(self):
        fake = FakeRunner([(
            json.dumps({"endpoints": [ENDPOINT_AVAILABLE],
                        "total_count": 1}), "", 0)])
        with mock.patch("list_vpcep.subprocess.run", fake):
            items = list_vpcep("endpoint", "cn-north-4")
        self.assertEqual(items, [ENDPOINT_AVAILABLE])
        self.assertEqual(len(fake.calls), 1)

    def test_pagination_offset_increment(self):
        page1 = {"endpoints": [ENDPOINT_AVAILABLE], "total_count": 2}
        page2 = {"endpoints": [ENDPOINT_FAILED], "total_count": 2}
        fake = FakeRunner([(json.dumps(page1), "", 0),
                           (json.dumps(page2), "", 0)])
        with mock.patch("list_vpcep.subprocess.run", fake):
            items = list_vpcep("endpoint", "cn-north-4", limit=1)
        self.assertEqual(items, [ENDPOINT_AVAILABLE, ENDPOINT_FAILED])
        self.assertEqual(len(fake.calls), 2)
        self.assertTrue(any("--offset=1" in part for part in fake.calls[1]))

    def test_pagination_stops_on_partial_page(self):
        page1 = {"endpoints": [ENDPOINT_AVAILABLE, ENDPOINT_FAILED]}
        fake = FakeRunner([(json.dumps(page1), "", 0)])
        with mock.patch("list_vpcep.subprocess.run", fake):
            items = list_vpcep("endpoint", "cn-north-4", limit=10)
        self.assertEqual(len(items), 2)
        self.assertEqual(len(fake.calls), 1)

    def test_empty_page(self):
        fake = FakeRunner([(json.dumps({"endpoints": [], "total_count": 0}),
                            "", 0)])
        with mock.patch("list_vpcep.subprocess.run", fake):
            items = list_vpcep("endpoint", "cn-north-4")
        self.assertEqual(items, [])

    def test_service_view_operation_forwarded(self):
        fake = FakeRunner([(json.dumps({"endpoint_services": [SERVICE_ITEM],
                                        "total_count": 1}), "", 0)])
        with mock.patch("list_vpcep.subprocess.run", fake):
            items = list_vpcep("service", "cn-north-4")
        self.assertEqual(items, [SERVICE_ITEM])
        self.assertIn("ListEndpointService", fake.calls[0])

    def test_public_view_operation_forwarded(self):
        fake = FakeRunner([(json.dumps({"endpoint_services": [PUBLIC_ITEM],
                                        "total_count": 1}), "", 0)])
        with mock.patch("list_vpcep.subprocess.run", fake):
            items = list_vpcep("public", "cn-north-4")
        self.assertEqual(items, [PUBLIC_ITEM])
        self.assertIn("ListServicePublicDetails", fake.calls[0])

    def test_error_payload_with_zero_rc_raises(self):
        payload = {"error_code": "common.01010013",
                   "error_msg": "not authorized to perform "
                                "vpcep:endpoints:list"}
        fake = FakeRunner([(json.dumps(payload), "", 0)])
        with mock.patch("list_vpcep.subprocess.run", fake):
            with self.assertRaises(AuthError):
                list_vpcep("endpoint", "cn-north-4")

    def test_nonzero_exit_403(self):
        fake = FakeRunner([("", "403 Forbidden", 1)])
        with mock.patch("list_vpcep.subprocess.run", fake):
            with self.assertRaises(AuthError):
                list_vpcep("endpoint", "cn-north-4")

    def test_nonzero_exit_credentials(self):
        fake = FakeRunner([("", "ERROR: no AK configured", 1)])
        with mock.patch("list_vpcep.subprocess.run", fake):
            with self.assertRaises(ConfigError):
                list_vpcep("endpoint", "cn-north-4")

    def test_timeout(self):
        fake = FakeRunner([subprocess.TimeoutExpired(cmd="hcloud", timeout=120)])
        with mock.patch("list_vpcep.subprocess.run", fake):
            with self.assertRaises(ApiError):
                list_vpcep("endpoint", "cn-north-4")

    def test_sdk_fallback_when_hcloud_missing(self):
        with mock.patch("list_vpcep.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_vpcep.list_vpcep_via_sdk",
                           return_value=[ENDPOINT_AVAILABLE]) as sdk_mock:
            items = list_vpcep("endpoint", "cn-north-4", name="vpcep-svc",
                               item_id="ep-1", vpc_id="vpc-1",
                               project_id="proj-1")
        self.assertEqual(items, [ENDPOINT_AVAILABLE])
        kwargs = sdk_mock.call_args.kwargs
        self.assertEqual(kwargs.get("project_id"), "proj-1")
        self.assertEqual(kwargs.get("name"), "vpcep-svc")
        self.assertEqual(sdk_mock.call_args.args[0], "endpoint")

    def test_sdk_fallback_unavailable_raises_config(self):
        with mock.patch("list_vpcep.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_vpcep.list_vpcep_via_sdk",
                           side_effect=ConfigError("huaweicloudsdkvpcep 未安装")):
            with self.assertRaises(ConfigError):
                list_vpcep("endpoint", "cn-north-4")

    def test_page_size_clamped_to_view_max(self):
        fake = FakeRunner([(json.dumps({"endpoints": []}), "", 0)])
        with mock.patch("list_vpcep.subprocess.run", fake):
            list_vpcep("endpoint", "cn-north-4", limit=9999)
        self.assertTrue(any("--limit=500" in part for part in fake.calls[0]))


class _FakeCredentials:
    def __init__(self, ak=None, sk=None, project_id=None):
        self.ak = ak
        self.sk = sk
        self.project_id = project_id


class _FakeHttpConfig:
    @staticmethod
    def get_default_config():
        return "http-config"


class _FakeRegion:
    def __init__(self, region_id, endpoint):
        self.id = region_id
        self.endpoint = endpoint


class _FakeRegionCatalog:
    @staticmethod
    def value_of(region):
        if region == "unknown-region":
            raise ValueError(region)
        return _FakeRegion(region, "https://vpcep.%s.myhuaweicloud.com" % region)


class _FakeRequest:
    def __init__(self, **kwargs):
        self.kwargs = kwargs


class _FakeSdkItem:
    def __init__(self, payload):
        self._payload = payload

    def to_dict(self):
        return self._payload


class _FakeSdkResponse:
    def __init__(self, items, key, total):
        setattr(self, key, [_FakeSdkItem(item) for item in items])
        if key != "endpoints":
            self.endpoints = None
        if key != "endpoint_services":
            self.endpoint_services = None
        self._total = total

    def to_dict(self):
        return {"total_count": self._total}


class _FakeSdkClient:
    def __init__(self):
        self.calls = []
        self.endpoints = [ENDPOINT_AVAILABLE]
        self.endpoint_services = [SERVICE_ITEM]
        self.public_services = [PUBLIC_ITEM]
        self.raise_error = None

    def list_endpoints(self, request):
        self.calls.append(("list_endpoints", request))
        if self.raise_error:
            raise self.raise_error
        return _FakeSdkResponse(self.endpoints, "endpoints",
                                len(self.endpoints))

    def list_endpoint_service(self, request):
        self.calls.append(("list_endpoint_service", request))
        if self.raise_error:
            raise self.raise_error
        return _FakeSdkResponse(self.endpoint_services, "endpoint_services",
                                len(self.endpoint_services))

    def list_service_public_details(self, request):
        self.calls.append(("list_service_public_details", request))
        if self.raise_error:
            raise self.raise_error
        return _FakeSdkResponse(self.public_services, "endpoint_services",
                                len(self.public_services))


class _FakeBuilder:
    def __init__(self, client, captured):
        self._client = client
        self._captured = captured

    def with_credentials(self, credentials):
        self._captured["credentials"] = credentials
        return self

    def with_region(self, region):
        self._captured["region"] = region
        return self

    def with_http_config(self, config):
        self._captured["http_config"] = config
        return self

    def build(self):
        return self._client


class _FakeVpcepClient:
    client = None
    captured = {}

    @classmethod
    def new_builder(cls):
        return _FakeBuilder(cls.client, cls.captured)


def _fake_sdk(client=None):
    _FakeVpcepClient.client = client or _FakeSdkClient()
    _FakeVpcepClient.captured = {}
    return {
        "BasicCredentials": _FakeCredentials,
        "HttpConfig": _FakeHttpConfig,
        "Region": _FakeRegion,
        "VpcepClient": _FakeVpcepClient,
        "VpcepRegion": _FakeRegionCatalog,
        "ListEndpointsRequest": _FakeRequest,
        "ListEndpointServiceRequest": _FakeRequest,
        "ListServicePublicDetailsRequest": _FakeRequest,
        "version": "v1",
    }


class TestSdkFallback(unittest.TestCase):
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
        from huaweicloudsdkvpcep.v1 import (
            VpcepClient, ListEndpointsRequest, ListEndpointServiceRequest,
            ListServicePublicDetailsRequest,
        )
        from huaweicloudsdkvpcep.v1.region.vpcep_region import VpcepRegion
        for obj in (BasicCredentials, Region, HttpConfig, VpcepClient,
                    ListEndpointsRequest, ListEndpointServiceRequest,
                    ListServicePublicDetailsRequest, VpcepRegion):
            self.assertTrue(callable(obj), obj)

    def test_endpoint_view_uses_env_credentials(self):
        sdk = _fake_sdk()
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak",
                   HUAWEI_SECRET_KEY="test-sk",
                   HUAWEI_PROJECT_ID="test-project")
        with mock.patch.dict(os.environ, env, clear=True), \
                mock.patch("list_vpcep._load_sdk", return_value=sdk):
            items = list_vpcep_via_sdk(
                "endpoint", "cn-north-4", vpc_id="vpc-1",
                item_id="ep-1", name="vpcep-svc", limit=10)
        self.assertEqual(items, [ENDPOINT_AVAILABLE])
        credentials = _FakeVpcepClient.captured["credentials"]
        self.assertEqual(credentials.ak, "test-ak")
        self.assertEqual(credentials.sk, "test-sk")
        self.assertEqual(credentials.project_id, "test-project")
        self.assertEqual(_FakeVpcepClient.captured["region"].id, "cn-north-4")
        request = _FakeVpcepClient.client.calls[0][1]
        self.assertEqual(request.kwargs["endpoint_service_name"], "vpcep-svc")
        self.assertEqual(request.kwargs["vpc_id"], "vpc-1")
        self.assertEqual(request.kwargs["id"], "ep-1")

    def test_service_view_request(self):
        sdk = _fake_sdk()
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="ak", HUAWEI_SECRET_KEY="sk",
                   HUAWEI_PROJECT_ID="proj")
        with mock.patch.dict(os.environ, env, clear=True), \
                mock.patch("list_vpcep._load_sdk", return_value=sdk):
            items = list_vpcep_via_sdk(
                "service", "cn-north-4", status="failed", item_id="svc-1")
        self.assertEqual(items, [SERVICE_ITEM])
        method, request = _FakeVpcepClient.client.calls[0]
        self.assertEqual(method, "list_endpoint_service")
        self.assertEqual(request.kwargs["status"], "failed")
        self.assertEqual(request.kwargs["id"], "svc-1")

    def test_public_view_request(self):
        sdk = _fake_sdk()
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="ak", HUAWEI_SECRET_KEY="sk",
                   HUAWEI_PROJECT_ID="proj")
        with mock.patch.dict(os.environ, env, clear=True), \
                mock.patch("list_vpcep._load_sdk", return_value=sdk):
            items = list_vpcep_via_sdk(
                "public", "cn-north-4", name="obs")
        self.assertEqual(items, [PUBLIC_ITEM])
        method, request = _FakeVpcepClient.client.calls[0]
        self.assertEqual(method, "list_service_public_details")
        self.assertEqual(request.kwargs["endpoint_service_name"], "obs")

    def test_unknown_region_uses_explicit_endpoint(self):
        sdk = _fake_sdk()
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="ak", HUAWEI_SECRET_KEY="sk",
                   HUAWEI_PROJECT_ID="proj")
        with mock.patch.dict(os.environ, env, clear=True), \
                mock.patch("list_vpcep._load_sdk", return_value=sdk):
            list_vpcep_via_sdk("endpoint", "unknown-region")
        region = _FakeVpcepClient.captured["region"]
        self.assertEqual(
            region.endpoint,
            "https://vpcep.unknown-region.myhuaweicloud.com")

    def test_missing_env_credentials_raises_config(self):
        env = dict(self._clean_credential_env(),
                   HUAWEI_PROJECT_ID="test-project")
        with mock.patch.dict(os.environ, env, clear=True), \
                mock.patch("list_vpcep._load_sdk", return_value=_fake_sdk()):
            with self.assertRaises(ConfigError) as ctx:
                list_vpcep_via_sdk("endpoint", "cn-north-4")
        self.assertIn("AK/SK", str(ctx.exception))

    def test_missing_project_id_raises_config(self):
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="ak", HUAWEI_SECRET_KEY="sk")
        with mock.patch.dict(os.environ, env, clear=True), \
                mock.patch("list_vpcep._load_sdk", return_value=_fake_sdk()):
            with self.assertRaises(ConfigError) as ctx:
                list_vpcep_via_sdk("endpoint", "cn-north-4")
        self.assertIn("project_id", str(ctx.exception))

    def test_explicit_project_id_overrides_env(self):
        sdk = _fake_sdk()
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="ak", HUAWEI_SECRET_KEY="sk",
                   HUAWEI_PROJECT_ID="env-proj")
        with mock.patch.dict(os.environ, env, clear=True), \
                mock.patch("list_vpcep._load_sdk", return_value=sdk):
            list_vpcep_via_sdk("endpoint", "cn-north-4",
                               project_id="cli-proj")
        self.assertEqual(
            _FakeVpcepClient.captured["credentials"].project_id, "cli-proj")

    def test_sdk_auth_failure(self):
        client = _FakeSdkClient()
        client.raise_error = Exception("403 Forbidden: not authorized")
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="ak", HUAWEI_SECRET_KEY="sk",
                   HUAWEI_PROJECT_ID="proj")
        with mock.patch.dict(os.environ, env, clear=True), \
                mock.patch("list_vpcep._load_sdk",
                           return_value=_fake_sdk(client)):
            with self.assertRaises(AuthError):
                list_vpcep_via_sdk("endpoint", "cn-north-4")

    def test_sdk_invalid_id(self):
        client = _FakeSdkClient()
        client.raise_error = Exception("Invalid id: not-a-uuid")
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="ak", HUAWEI_SECRET_KEY="sk",
                   HUAWEI_PROJECT_ID="proj")
        with mock.patch.dict(os.environ, env, clear=True), \
                mock.patch("list_vpcep._load_sdk",
                           return_value=_fake_sdk(client)):
            with self.assertRaises(InvalidRequestError):
                list_vpcep_via_sdk("endpoint", "cn-north-4",
                                   item_id="not-a-uuid")


class TestFiltering(unittest.TestCase):
    def test_exact_name_case_insensitive(self):
        items = filter_items([ENDPOINT_AVAILABLE, ENDPOINT_FAILED],
                             name="VPCEP-SVC-ALPHA")
        self.assertEqual(items, [ENDPOINT_AVAILABLE])

    def test_fuzzy_name(self):
        items = filter_items([ENDPOINT_AVAILABLE, ENDPOINT_FAILED],
                             name="SVC-B", fuzzy=True)
        self.assertEqual(items, [ENDPOINT_FAILED])

    def test_fuzzy_service_name(self):
        items = filter_items([ENDPOINT_AVAILABLE, ENDPOINT_FAILED],
                             service_name="alpha", fuzzy=True)
        self.assertEqual(items, [ENDPOINT_AVAILABLE])

    def test_id_filter(self):
        items = filter_items([ENDPOINT_AVAILABLE, ENDPOINT_FAILED],
                             item_id="ep-0002")
        self.assertEqual(items, [ENDPOINT_FAILED])

    def test_vpc_filter(self):
        items = filter_items([ENDPOINT_AVAILABLE, ENDPOINT_FAILED],
                             vpc_id="vpc-0001")
        self.assertEqual(items, [ENDPOINT_AVAILABLE])

    def test_status_filter_case_insensitive(self):
        items = filter_items([ENDPOINT_AVAILABLE, ENDPOINT_FAILED],
                             status="FAILED")
        self.assertEqual(items, [ENDPOINT_FAILED])

    def test_public_name_filter(self):
        items = filter_items([PUBLIC_ITEM, PUBLIC_ITEM_DNS],
                             view="public", name="DNS")
        self.assertEqual(items, [PUBLIC_ITEM_DNS])


class TestRendering(unittest.TestCase):
    def test_status_helpers(self):
        self.assertTrue(is_available(ENDPOINT_AVAILABLE))
        self.assertTrue(is_non_available(ENDPOINT_FAILED))
        self.assertTrue(is_non_available(ENDPOINT_CREATING))
        self.assertFalse(is_non_available({"status": ""}))

    def test_item_name_endpoint(self):
        self.assertEqual(item_name(ENDPOINT_AVAILABLE, "endpoint"),
                         "vpcep-svc-alpha")

    def test_item_name_service_fallback(self):
        self.assertEqual(item_name({"id": "svc-9"}, "service"), "svc-9")

    def test_endpoint_table_fixed_columns(self):
        table = render_table([ENDPOINT_AVAILABLE], "endpoint", "cn-north-4")
        for fragment in ("终端节点ID", "名称", "状态", "所属服务名", "服务ID",
                         "服务类型", "IP", "VPC ID", "是否启用DNS",
                         "是否启用白名单", "创建时间", "region"):
            self.assertIn(fragment, table)
        self.assertIn("ep-0001", table)
        self.assertIn("是", table)
        self.assertIn("否", table)
        self.assertIn("cn-north-4", table)

    def test_service_table_columns(self):
        table = render_table([SERVICE_ITEM], "service")
        for fragment in ("服务ID", "名称", "状态", "后端类型", "创建时间"):
            self.assertIn(fragment, table)
        self.assertIn("vlan", table)

    def test_public_table_columns(self):
        table = render_table([PUBLIC_ITEM], "public")
        for fragment in ("服务ID", "名称", "服务类型", "创建时间"):
            self.assertIn(fragment, table)

    def test_missing_field_rendered_dash(self):
        table = render_table([{"id": "ep-1"}], "endpoint")
        self.assertIn("-", table)

    def test_abnormal_status_marked(self):
        table = render_table([ENDPOINT_FAILED], "endpoint")
        self.assertIn("[异常] failed", table)

    def test_markdown_fixed_columns(self):
        content = render_markdown([ENDPOINT_AVAILABLE], "endpoint",
                                  "cn-north-4")
        self.assertIn("| 终端节点ID | 名称 | 状态 |", content)
        self.assertIn("ep-0001", content)
        self.assertIn("cn-north-4", content)

    def test_markdown_empty_has_header(self):
        content = render_markdown([], "endpoint", "cn-north-4")
        self.assertIn("当前过滤条件下无 终端节点", content)
        self.assertIn("| 终端节点ID |", content)

    def test_markdown_splits_abnormal(self):
        content = render_markdown(
            [ENDPOINT_AVAILABLE, ENDPOINT_FAILED], "endpoint")
        self.assertIn("AVAILABLE（1 个）", content)
        self.assertIn("非 AVAILABLE（1 个，需关注）", content)
        self.assertIn("[异常] failed", content)

    def test_atomic_write(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = os.path.join(tmp_dir, "report.md")
            result = write_markdown_atomic(path, "# hello\n")
            self.assertEqual(result, path)
            with open(path, encoding="utf-8") as handle:
                self.assertEqual(handle.read(), "# hello\n")
            self.assertEqual(
                [name for name in os.listdir(tmp_dir) if name.endswith(".tmp")],
                [])


class TestMain(unittest.TestCase):
    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("list_vpcep.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            rc = main(argv)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    def test_default_concise_output(self):
        rc, out, err = self._run(
            ["--region", "cn-north-4"],
            [(json.dumps({"endpoints": [ENDPOINT_AVAILABLE],
                          "total_count": 1}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("VPCEP 终端节点列表", out)
        self.assertIn("vpcep-svc-alpha", out)
        self.assertEqual(err, "")

    def test_abnormal_separate_section(self):
        rc, out, _ = self._run(
            [],
            [(json.dumps({"endpoints": [ENDPOINT_AVAILABLE,
                                        ENDPOINT_FAILED],
                          "total_count": 2}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("异常（非 AVAILABLE，1 个，需关注）", out)
        self.assertIn("[!] vpcep-svc-beta", out)

    def test_table_output_splits_abnormal(self):
        rc, out, _ = self._run(
            ["--table"],
            [(json.dumps({"endpoints": [ENDPOINT_AVAILABLE,
                                        ENDPOINT_FAILED],
                          "total_count": 2}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("终端节点ID", out)
        self.assertIn("异常（非 AVAILABLE，共 1 个，需关注）", out)

    def test_status_failed_filter_lists_only_abnormal(self):
        fake = FakeRunner([(json.dumps({"endpoints": [ENDPOINT_AVAILABLE,
                                                      ENDPOINT_FAILED],
                                        "total_count": 2}), "", 0)])
        with mock.patch("list_vpcep.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, mock.patch("sys.stderr"):
            rc = main(["--status", "failed"])
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        self.assertEqual(rc, 0)
        self.assertIn("vpcep-svc-beta", out)
        self.assertNotIn("vpcep-svc-alpha", out)

    def test_status_rejected_filter_not_blocked(self):
        rc, out, err = self._run(
            ["--status", "rejected"],
            [(json.dumps({"endpoints": [ENDPOINT_FAILED]}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertEqual(err, "")

    def test_service_view_output(self):
        rc, out, _ = self._run(
            ["--view", "service"],
            [(json.dumps({"endpoint_services": [SERVICE_ITEM]}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("VPCEP 终端节点服务列表", out)
        self.assertIn("my-endpoint-service", out)

    def test_public_view_output(self):
        rc, out, _ = self._run(
            ["--view", "public"],
            [(json.dumps({"endpoint_services": [PUBLIC_ITEM]}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("VPCEP 公共终端节点服务列表", out)
        self.assertIn("obs", out)

    def test_json_output(self):
        rc, out, err = self._run(
            ["--json"],
            [(json.dumps({"endpoints": [ENDPOINT_AVAILABLE]}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out), [ENDPOINT_AVAILABLE])

    def test_empty_json_output(self):
        rc, out, _ = self._run(
            ["--json"],
            [(json.dumps({"endpoints": [], "total_count": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out), [])

    def test_empty_list_message(self):
        rc, out, _ = self._run(
            ["--region", "cn-south-1", "--name", "x"],
            [(json.dumps({"endpoints": [], "total_count": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("无 VPCEP 终端节点", out)
        self.assertIn("cn-south-1", out)
        self.assertIn("name=x", out)

    def test_name_filter_forwarded(self):
        fake = FakeRunner([(json.dumps({"endpoints": [ENDPOINT_AVAILABLE]}),
                            "", 0)])
        with mock.patch("list_vpcep.subprocess.run", fake), \
                mock.patch("sys.stdout"), mock.patch("sys.stderr"):
            rc = main(["--name", "vpcep-svc-alpha", "--fuzzy"])
        self.assertEqual(rc, 0)
        self.assertTrue(
            any("--endpoint_service_name=vpcep-svc-alpha" in part
                for part in fake.calls[0]))

    def test_auth_error_message(self):
        rc, out, err = self._run([], [("", "403 Forbidden", 1)])
        self.assertEqual(rc, 1)
        self.assertIn("[错误]", err)
        self.assertIn("IAM", err)

    def test_payload_auth_error_zero_rc(self):
        payload = {"error_code": "common.01010013",
                   "error_msg": "not authorized to perform "
                                "vpcep:endpoints:list"}
        rc, out, err = self._run([], [(json.dumps(payload), "", 0)])
        self.assertEqual(rc, 1)
        self.assertIn("无权限访问", err)
        self.assertNotIn("Traceback", err)

    def test_invalid_id_message(self):
        payload = {"error_code": "common.01010003",
                   "error_msg": "Invalid id: not-a-uuid"}
        rc, out, err = self._run(["--id", "not-a-uuid"],
                                 [(json.dumps(payload), "", 0)])
        self.assertEqual(rc, 1)
        self.assertIn("ID", err)
        self.assertNotIn("Traceback", err)

    def test_missing_ak_sk_error_message(self):
        rc, out, err = self._run([], [("", "ERROR: cli-ak empty", 1)])
        self.assertEqual(rc, 1)
        self.assertIn("AK/SK", err)

    def test_hcloud_missing_falls_back_to_sdk(self):
        with mock.patch("list_vpcep.list_vpcep_via_sdk",
                        return_value=[ENDPOINT_AVAILABLE]):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 0)
        self.assertIn("vpcep-svc-alpha", out)

    def test_write_intent_argv_blocked(self):
        rc, out, err = self._run(["--action", "delete"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)

    def test_write_name_blocked(self):
        rc, out, err = self._run(["--name", "create-me"], [])
        self.assertEqual(rc, 1)
        self.assertIn("守卫拦截", err)

    def test_markdown_export(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = os.path.join(tmp_dir, "vpcep.md")
            fake = FakeRunner([(json.dumps({"endpoints": [ENDPOINT_AVAILABLE]}),
                                "", 0)])
            with mock.patch("list_vpcep.subprocess.run", fake), \
                    mock.patch("sys.stdout") as stdout, \
                    mock.patch("sys.stderr"):
                rc = main(["--format", "md", "--output", path])
            out = "".join(c[0][0] for c in stdout.write.call_args_list)
            self.assertEqual(rc, 0)
            self.assertIn("已导出", out)
            with open(path, encoding="utf-8") as handle:
                content = handle.read()
            self.assertIn("| 终端节点ID |", content)
            self.assertIn("ep-0001", content)

    def test_markdown_export_empty_header(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = os.path.join(tmp_dir, "empty.md")
            fake = FakeRunner([(json.dumps({"endpoints": []}), "", 0)])
            with mock.patch("list_vpcep.subprocess.run", fake), \
                    mock.patch("sys.stdout"), mock.patch("sys.stderr"):
                rc = main(["--format", "md", "--output", path])
            self.assertEqual(rc, 0)
            with open(path, encoding="utf-8") as handle:
                content = handle.read()
            self.assertIn("| 终端节点ID |", content)


class TestErrorHierarchy(unittest.TestCase):
    def test_subclasses(self):
        for exc in (GuardError, ConfigError, AuthError, InvalidRequestError,
                    ApiError):
            self.assertTrue(issubclass(exc, VpcepListError))


if __name__ == "__main__":
    unittest.main()