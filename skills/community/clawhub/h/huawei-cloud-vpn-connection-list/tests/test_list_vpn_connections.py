"""Offline unit tests for huawei-cloud-vpn-connection-list.

No credentials, no network, no cloud resources: the hcloud subprocess and the
SDK client are both faked.
"""

import io
import json
import os
import subprocess
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest import mock

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from list_vpn_connections import (  # noqa: E402
    ALLOWED_OPERATIONS,
    ApiError,
    AuthError,
    ConfigError,
    GuardError,
    NotFoundError,
    VpnListError,
    _payload_error,
    _sdk_auth_error,
    _sdk_client,
    build_connection_command,
    build_gateway_command,
    build_hcloud_command,
    classify_hcloud_failure,
    extract_connections,
    extract_gateways,
    extract_json,
    extract_next_marker,
    filter_inventory,
    guard_operation,
    guard_scan_text,
    guard_write_intent,
    is_not_up,
    is_up,
    list_vpn_connections,
    list_vpn_connections_via_sdk,
    list_vpn_gateways,
    list_vpn_gateways_via_sdk,
    main,
    render_default,
    render_gateway_table,
    render_connection_table,
    render_tables,
    strip_secrets,
    summarize,
)

GATEWAY_1 = {
    "id": "vgw-0001",
    "name": "vpn-prod",
    "status": "ACTIVE",
    "flavor": "Professional1",
    "attachment_type": "vpc",
    "vpc_id": "vpc-0001",
    "local_subnets": ["192.168.0.0/24", "10.0.0.0/24"],
    "eip1": {"ip_address": "1.2.3.4"},
    "eip2": {"ip_address": "5.6.7.8"},
    "connection_number": 10,
    "used_connection_number": 2,
    "created_at": "2025-01-01T00:00:00Z",
}
GATEWAY_2 = {
    "id": "vgw-0002",
    "name": "vpn-dr",
    "status": "PENDING_CREATE",
    "flavor": "Professional1",
    "attachment_type": "er",
    "er_id": "er-0001",
    "local_subnets": [],
    "eip1": None,
    "connection_number": 10,
    "used_connection_number": 0,
}
CONN_UP = {
    "id": "conn-0001",
    "name": "to-dc",
    "status": "ACTIVE",
    "vgw_id": "vgw-0001",
    "vgw_ip": "1.2.3.4",
    "peer_subnets": ["172.16.0.0/16"],
    "tunnel_local_address": "169.254.1.1",
    "tunnel_peer_address": "169.254.1.2",
    "created_at": "2025-01-02T00:00:00Z",
}
CONN_DOWN = {
    "id": "conn-0002",
    "name": "to-branch",
    "status": "DOWN",
    "vgw_id": "vgw-0001",
    "vgw_ip": "1.2.3.4",
    "peer_subnets": ["10.10.0.0/16"],
    "tunnel_local_address": "169.254.1.5",
    "tunnel_peer_address": "169.254.1.6",
    "created_at": "2025-01-03T00:00:00Z",
}
CONN_ERROR = {
    "id": "conn-0003",
    "name": "to-plant",
    "status": "ERROR",
    "vgw_id": "vgw-0002",
    "peer_subnets": ["10.20.0.0/16"],
}
CONN_NO_STATUS = {
    "id": "conn-0004",
    "name": "to-new-site",
    "vgw_id": "vgw-0002",
    "peer_subnets": [],
}


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


class FakeGateway:
    """Fake SDK gateway model exposing to_dict()."""

    def __init__(self, data):
        self._data = data

    def to_dict(self):
        return dict(self._data)


class FakeConnection(FakeGateway):
    pass


class FakeResponse:
    def __init__(self, gateways=None, connections=None, next_marker=None):
        self.vpn_gateways = [FakeGateway(g) for g in (gateways or [])]
        self.vpn_connections = [FakeConnection(c) for c in (connections or [])]
        self.page_info = ({"next_marker": next_marker}
                          if next_marker is not None else None)


class FakeClient:
    def __init__(self, gateway_pages=None, connection_pages=None):
        self.gateway_pages = list(gateway_pages or [])
        self.connection_pages = list(connection_pages or [])
        self.gateway_requests = []
        self.connection_requests = []

    def list_vgws(self, request):
        self.gateway_requests.append(request)
        if not self.gateway_pages:
            raise AssertionError("unexpected extra list_vgws call")
        return self.gateway_pages.pop(0)

    def list_vpn_connections(self, request):
        self.connection_requests.append(request)
        if not self.connection_pages:
            raise AssertionError("unexpected extra list_vpn_connections call")
        return self.connection_pages.pop(0)


class FakeRequest:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __repr__(self):
        return "FakeRequest(%s)" % self.kwargs


class TestWriteIntentGuard(unittest.TestCase):
    def test_read_intent_passes(self):
        for text in ("--region cn-north-4 --table list vpn gateways",
                     "show ipsec connections", "list-vpn-connections"):
            self.assertFalse(guard_write_intent(text))

    def test_gateway_lifecycle_blocked(self):
        for text in ("CreateVgw", "DeleteVgw", "UpdateVgw",
                     "UpdatePostpaidVgwSpecification"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_connection_lifecycle_blocked(self):
        for text in ("CreateVpnConnection", "BatchCreateVpnConnection",
                     "DeleteVpnConnection", "ResetVpnConnection",
                     "create vpn connection", "delete vpn-connection"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_psk_change_blocked(self):
        for text in ("UpdatePsk", "--update-psk", "update_psk"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_restart_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("restart vpn connection")

    def test_ssl_vpn_and_tagging_blocked(self):
        for text in ("CreateVpnServer", "CreateP2cVgw", "BatchCreateResourceTags",
                     "ImportClientCa", "ExportClientConfig"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_read_filter_values_are_not_scanned(self):
        argv = ["--name", "prod-create-gateway", "--status", "DOWN",
                "--gateway-id", "vgw-0001"]
        self.assertFalse(guard_write_intent(guard_scan_text(argv)))

    def test_equals_form_filter_value_is_not_scanned(self):
        argv = ["--name=delete-me", "--region=cn-north-4"]
        self.assertFalse(guard_write_intent(guard_scan_text(argv)))

    def test_operation_value_is_scanned(self):
        argv = ["--operation=DeleteVgw"]
        with self.assertRaises(GuardError):
            guard_write_intent(guard_scan_text(argv))

    def test_guard_operation_whitelist(self):
        for operation in ALLOWED_OPERATIONS:
            self.assertTrue(guard_operation(operation))
        with self.assertRaises(GuardError):
            guard_operation("CreateVgw")

    def test_guard_is_case_and_separator_insensitive(self):
        for text in ("CREATE_VGW", "create-Vgw", "Create Vgw"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)


class TestCommandConstruction(unittest.TestCase):
    def test_gateway_command(self):
        argv = build_gateway_command("cn-north-4")
        self.assertEqual(argv[:3], ["VPN", "ListVgws", "--cli-region=cn-north-4"])
        self.assertNotIn("--limit=100", argv)
        self.assertFalse(any(part.startswith("--marker") for part in argv))

    def test_gateway_command_with_drilldown(self):
        argv = build_gateway_command("cn-south-1", gateway_id="vgw-0001")
        self.assertIn("--cli-region=cn-south-1", argv)
        self.assertIn("--vgw_id=vgw-0001", argv)

    def test_connection_command_first_page(self):
        argv = build_connection_command("cn-north-4", limit=50)
        self.assertEqual(argv[:4], [
            "VPN", "ListVpnConnections", "--cli-region=cn-north-4", "--limit=50"])
        self.assertFalse(any(part.startswith("--marker") for part in argv))

    def test_connection_command_next_page(self):
        argv = build_connection_command(
            "cn-north-4", gateway_id="vgw-0001", limit=100,
            marker="2025-01-03T00:00:00Z")
        self.assertIn("--marker=2025-01-03T00:00:00Z", argv)
        self.assertIn("--vgw_id=vgw-0001", argv)


class TestParsing(unittest.TestCase):
    def test_extract_json_plain(self):
        self.assertEqual(extract_json('{"a": 1}'), {"a": 1})

    def test_extract_json_with_wrapper_noise(self):
        self.assertEqual(
            extract_json('some warning\n{"a": 1}\n'), {"a": 1})

    def test_extract_json_invalid(self):
        with self.assertRaises(ApiError):
            extract_json("not json at all")

    def test_extract_gateways_variants(self):
        self.assertEqual(extract_gateways({"vpn_gateways": [GATEWAY_1]}), [GATEWAY_1])
        self.assertEqual(extract_gateways({"vpnGateways": [GATEWAY_1]}), [GATEWAY_1])
        self.assertEqual(extract_gateways([GATEWAY_1]), [GATEWAY_1])
        self.assertEqual(extract_gateways({"other": []}), [])
        self.assertEqual(extract_gateways(None), [])

    def test_extract_connections_variants(self):
        self.assertEqual(
            extract_connections({"vpn_connections": [CONN_UP]}), [CONN_UP])
        self.assertEqual(
            extract_connections({"vpnConnections": [CONN_UP]}), [CONN_UP])
        self.assertEqual(extract_connections({}), [])

    def test_extract_next_marker(self):
        self.assertEqual(
            extract_next_marker({"page_info": {"next_marker": "tok"}}), "tok")
        self.assertEqual(
            extract_next_marker({"pageInfo": {"nextMarker": "tok2"}}), "tok2")
        self.assertIsNone(extract_next_marker({"page_info": {}}))
        self.assertIsNone(extract_next_marker({}))

    def test_payload_error_recognizes_real_vpn_403_envelope(self):
        payload = {
            "error_code": "VPN.0007",
            "error_msg": "User: x is not authorized to perform: "
                         "vpn:vpnGateways:list",
        }
        text = _payload_error(payload)
        self.assertIn("VPN.0007", text)

    def test_payload_error_ignores_successful_page(self):
        self.assertIsNone(_payload_error({"vpn_gateways": [], "error_code": ""}))
        self.assertIsNone(_payload_error({"vpn_connections": []}))

    def test_strip_secrets_removes_psk(self):
        payload = {"id": "c1", "psk": "secret", "ikepolicy": {"psk": "s2", "x": 1}}
        clean = strip_secrets(payload)
        self.assertNotIn("psk", clean)
        self.assertNotIn("psk", clean["ikepolicy"])
        self.assertEqual(clean["ikepolicy"]["x"], 1)

    def test_status_helpers(self):
        self.assertTrue(is_up(CONN_UP))
        self.assertFalse(is_not_up(CONN_UP))
        self.assertTrue(is_not_up(CONN_DOWN))
        self.assertTrue(is_not_up(CONN_ERROR))
        self.assertFalse(is_up(CONN_NO_STATUS))
        self.assertFalse(is_not_up(CONN_NO_STATUS))


class TestClassifyFailure(unittest.TestCase):
    def test_missing_credentials(self):
        err = classify_hcloud_failure(
            "", "ERROR: cli-ak is empty, please run hcloud configure", 1)
        self.assertIsInstance(err, ConfigError)
        self.assertIn("AK/SK", str(err))

    def test_permission_denied_envelope_rc0_is_403(self):
        err = classify_hcloud_failure(
            '{"error_code":"VPN.0007","error_msg":"User: x is not authorized '
            'to perform: vpn:vpnGateways:list"}', "", 0)
        self.assertIsInstance(err, AuthError)
        self.assertIn("403", str(err))
        self.assertIn("vpn:vpnGateways:list", str(err))

    def test_401_is_reported_as_invalid_credentials(self):
        err = classify_hcloud_failure("", "401 Unauthorized: invalid AK", 1)
        self.assertIsInstance(err, AuthError)
        self.assertIn("401", str(err))
        self.assertIn("凭证无效", str(err))
        self.assertNotIn("vpn:vpnGateways:list", str(err))

    def test_generic_api_error(self):
        err = classify_hcloud_failure("", "boom", 2)
        self.assertIsInstance(err, ApiError)

    def test_use_error_marker_with_zero_rc(self):
        err = classify_hcloud_failure(
            "[USE_ERROR]Invalid parameter: marker\n\n"
            "Run `hcloud VPN ListVpnConnections --help` for details.", "", 0)
        self.assertIsInstance(err, ApiError)
        self.assertIn("参数错误", str(err))
        self.assertIn("--help", str(err))

    def test_sdk_auth_error_distinguishes_401_and_403(self):
        class _Unauthorized(Exception):
            status_code = 401

        class _Forbidden(Exception):
            status_code = 403

        unauthorized = _sdk_auth_error(_Unauthorized("401 Unauthorized"))
        self.assertIn("凭证无效", str(unauthorized))
        self.assertNotIn("vpn:vpnGateways:list", str(unauthorized))
        forbidden = _sdk_auth_error(_Forbidden("VPN.0007 not authorized"))
        self.assertIn("vpn:vpnGateways:list", str(forbidden))


class TestListVpnGateways(unittest.TestCase):
    def test_single_call_no_paging(self):
        fake = FakeRunner([(json.dumps({"vpn_gateways": [GATEWAY_1, GATEWAY_2]}),
                            "", 0)])
        with mock.patch("list_vpn_connections.subprocess.run", fake):
            gateways = list_vpn_gateways("cn-north-4")
        self.assertEqual(gateways, [GATEWAY_1, GATEWAY_2])
        self.assertEqual(len(fake.calls), 1)
        self.assertIn("ListVgws", fake.calls[0])

    def test_drilldown_forwards_vgw_id(self):
        fake = FakeRunner([(json.dumps({"vpn_gateways": [GATEWAY_1]}), "", 0)])
        with mock.patch("list_vpn_connections.subprocess.run", fake):
            list_vpn_gateways("cn-north-4", gateway_id="vgw-0001")
        self.assertIn("--vgw_id=vgw-0001", fake.calls[0])

    def test_permission_envelope_rc0_raises_auth_error(self):
        envelope = json.dumps({
            "error_code": "VPN.0007",
            "error_msg": "not authorized to perform vpn:vpnGateways:list"})
        fake = FakeRunner([(envelope, "", 0)])
        with mock.patch("list_vpn_connections.subprocess.run", fake):
            with self.assertRaises(AuthError):
                list_vpn_gateways("cn-north-4")

    def test_missing_hcloud_falls_back_to_sdk(self):
        fake = FakeRunner([FileNotFoundError()])
        with mock.patch("list_vpn_connections.subprocess.run", fake):
            with mock.patch(
                    "list_vpn_connections.list_vpn_gateways_via_sdk",
                    return_value=[GATEWAY_1]) as sdk:
                gateways = list_vpn_gateways("cn-north-4")
        self.assertEqual(gateways, [GATEWAY_1])
        sdk.assert_called_once_with(
            "cn-north-4", gateway_id=None, project_id=None)

    def test_psk_is_stripped_from_cli_output(self):
        raw = dict(GATEWAY_1, psk="secret-value")
        fake = FakeRunner([(json.dumps({"vpn_gateways": [raw]}), "", 0)])
        with mock.patch("list_vpn_connections.subprocess.run", fake):
            gateways = list_vpn_gateways("cn-north-4")
        self.assertNotIn("psk", gateways[0])


class TestListVpnConnections(unittest.TestCase):
    def test_single_page_without_next_marker(self):
        payload = {"vpn_connections": [CONN_UP]}
        fake = FakeRunner([(json.dumps(payload), "", 0)])
        with mock.patch("list_vpn_connections.subprocess.run", fake):
            connections = list_vpn_connections("cn-north-4", limit=1)
        self.assertEqual(connections, [CONN_UP])
        self.assertEqual(len(fake.calls), 1)

    def test_pagination_follows_page_info_next_marker(self):
        page1 = {"vpn_connections": [CONN_UP],
                 "page_info": {"next_marker": "2025-01-02T00:00:00Z"}}
        page2 = {"vpn_connections": [CONN_DOWN], "page_info": {"next_marker": ""}}
        fake = FakeRunner([(json.dumps(page1), "", 0),
                           (json.dumps(page2), "", 0)])
        with mock.patch("list_vpn_connections.subprocess.run", fake):
            connections = list_vpn_connections("cn-north-4", limit=1)
        self.assertEqual(connections, [CONN_UP, CONN_DOWN])
        self.assertEqual(len(fake.calls), 2)
        self.assertIn("--marker=2025-01-02T00:00:00Z", fake.calls[1])

    def test_pagination_stops_on_repeated_marker(self):
        page = {"vpn_connections": [CONN_UP],
                "page_info": {"next_marker": "same-token"}}
        fake = FakeRunner([(json.dumps(page), "", 0),
                           (json.dumps(page), "", 0)])
        with mock.patch("list_vpn_connections.subprocess.run", fake):
            connections = list_vpn_connections("cn-north-4", limit=1)
        self.assertEqual(len(connections), 2)
        self.assertEqual(len(fake.calls), 2)

    def test_pagination_stops_on_short_page(self):
        page = {"vpn_connections": [CONN_UP, CONN_DOWN],
                "page_info": {"next_marker": "tok"}}
        fake = FakeRunner([(json.dumps(page), "", 0)])
        with mock.patch("list_vpn_connections.subprocess.run", fake):
            connections = list_vpn_connections("cn-north-4", limit=10)
        self.assertEqual(connections, [CONN_UP, CONN_DOWN])
        self.assertEqual(len(fake.calls), 1)

    def test_empty_list(self):
        fake = FakeRunner([(json.dumps({"vpn_connections": []}), "", 0)])
        with mock.patch("list_vpn_connections.subprocess.run", fake):
            connections = list_vpn_connections("cn-north-4")
        self.assertEqual(connections, [])

    def test_drilldown_forwards_vgw_id(self):
        fake = FakeRunner([(json.dumps({"vpn_connections": [CONN_UP]}), "", 0)])
        with mock.patch("list_vpn_connections.subprocess.run", fake):
            list_vpn_connections("cn-north-4", gateway_id="vgw-0001")
        self.assertIn("--vgw_id=vgw-0001", fake.calls[0])

    def test_max_pages_guard(self):
        page = {"vpn_connections": [CONN_UP],
                "page_info": {"next_marker": "tok-%d"}}
        results = [(json.dumps(dict(page, page_info={"next_marker": "tok-%d" % i})),
                    "", 0) for i in range(3)]
        fake = FakeRunner(results)
        with mock.patch("list_vpn_connections.subprocess.run", fake):
            with self.assertRaises(ApiError):
                list_vpn_connections("cn-north-4", limit=1, max_pages=2)

    def test_permission_envelope_rc0_raises_auth_error(self):
        envelope = json.dumps({
            "error_code": "VPN.0007",
            "error_msg": "not authorized to perform vpn:vpnConnections:list"})
        fake = FakeRunner([(envelope, "", 0)])
        with mock.patch("list_vpn_connections.subprocess.run", fake):
            with self.assertRaises(AuthError):
                list_vpn_connections("cn-north-4")

    def test_missing_hcloud_falls_back_to_sdk(self):
        fake = FakeRunner([FileNotFoundError()])
        with mock.patch("list_vpn_connections.subprocess.run", fake):
            with mock.patch(
                    "list_vpn_connections.list_vpn_connections_via_sdk",
                    return_value=[CONN_UP]) as sdk:
                connections = list_vpn_connections(
                    "cn-north-4", gateway_id="vgw-0001", limit=50)
        self.assertEqual(connections, [CONN_UP])
        sdk.assert_called_once_with(
            "cn-north-4", gateway_id="vgw-0001", limit=50,
            project_id=None, max_pages=100)


class TestSdkFallback(unittest.TestCase):
    def _patch_sdk(self, client):
        requests = (FakeRequest, FakeRequest)
        return (
            mock.patch("list_vpn_connections._sdk_client", return_value=client),
            mock.patch("list_vpn_connections._sdk_request_classes",
                       return_value=requests),
        )

    def test_gateways_via_sdk(self):
        client = FakeClient(gateway_pages=[
            FakeResponse(gateways=[GATEWAY_1, GATEWAY_2])])
        client_patch, req_patch = self._patch_sdk(client)
        with client_patch, req_patch:
            gateways = list_vpn_gateways_via_sdk("cn-north-4", project_id="p1")
        self.assertEqual(gateways, [GATEWAY_1, GATEWAY_2])
        self.assertEqual(client.gateway_requests[0].kwargs["vgw_id"], None)

    def test_gateways_via_sdk_drilldown(self):
        client = FakeClient(gateway_pages=[FakeResponse(gateways=[GATEWAY_1])])
        client_patch, req_patch = self._patch_sdk(client)
        with client_patch, req_patch:
            list_vpn_gateways_via_sdk(
                "cn-north-4", gateway_id="vgw-0001", project_id="p1")
        self.assertEqual(
            client.gateway_requests[0].kwargs["vgw_id"], "vgw-0001")

    def test_connections_via_sdk_pages(self):
        client = FakeClient(connection_pages=[
            FakeResponse(connections=[CONN_UP], next_marker="tok-1"),
            FakeResponse(connections=[CONN_DOWN],
                         next_marker="tok-2".replace("tok-2", "")),
        ])
        client_patch, req_patch = self._patch_sdk(client)
        with client_patch, req_patch:
            connections = list_vpn_connections_via_sdk(
                "cn-north-4", limit=1, project_id="p1")
        self.assertEqual(connections, [CONN_UP, CONN_DOWN])
        self.assertEqual(len(client.connection_requests), 2)
        self.assertEqual(client.connection_requests[1].kwargs["marker"], "tok-1")

    def test_connections_via_sdk_auth_error(self):
        class _Forbidden(Exception):
            status_code = 403

        client = mock.Mock()
        client.list_vpn_connections.side_effect = _Forbidden("403 Forbidden")
        client_patch, req_patch = self._patch_sdk(client)
        with client_patch, req_patch:
            with self.assertRaises(AuthError):
                list_vpn_connections_via_sdk("cn-north-4", project_id="p1")

    def test_sdk_missing_credentials(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ConfigError) as ctx:
                _sdk_client("cn-north-4", None)
        self.assertIn("AK/SK", str(ctx.exception))

    def test_sdk_missing_project_id(self):
        env = {"HUAWEI_ACCESS_KEY": "ak", "HUAWEI_SECRET_KEY": "sk"}
        with mock.patch.dict(os.environ, env, clear=True):
            with self.assertRaises(ConfigError) as ctx:
                _sdk_client("cn-north-4", None)
        self.assertIn("project_id", str(ctx.exception))

    def test_sdk_psk_stripped(self):
        raw = dict(CONN_UP, psk="secret")
        client = FakeClient(connection_pages=[
            FakeResponse(connections=[raw], next_marker="")])
        client_patch, req_patch = self._patch_sdk(client)
        with client_patch, req_patch:
            connections = list_vpn_connections_via_sdk(
                "cn-north-4", project_id="p1")
        self.assertNotIn("psk", connections[0])


class TestFilters(unittest.TestCase):
    def setUp(self):
        self.gateways = [GATEWAY_1, GATEWAY_2]
        self.connections = [CONN_UP, CONN_DOWN, CONN_ERROR, CONN_NO_STATUS]

    def test_no_filters(self):
        gateways, connections = filter_inventory(
            self.gateways, self.connections)
        self.assertEqual(len(gateways), 2)
        self.assertEqual(len(connections), 4)

    def test_gateway_id_drilldown(self):
        gateways, connections = filter_inventory(
            self.gateways, self.connections, gateway_id="vgw-0001")
        self.assertEqual([g["id"] for g in gateways], ["vgw-0001"])
        self.assertEqual([c["id"] for c in connections], ["conn-0001", "conn-0002"])

    def test_gateway_id_not_found_raises(self):
        with self.assertRaises(NotFoundError) as ctx:
            filter_inventory(self.gateways, self.connections,
                             gateway_id="vgw-9999", region="cn-north-4")
        self.assertIn("vgw-9999", str(ctx.exception))
        self.assertIn("cn-north-4", str(ctx.exception))

    def test_status_filter_narrows_gateways(self):
        gateways, connections = filter_inventory(
            self.gateways, self.connections, status="down")
        self.assertEqual([c["id"] for c in connections], ["conn-0002"])
        self.assertEqual([g["id"] for g in gateways], ["vgw-0001"])

    def test_status_filter_is_case_insensitive(self):
        _, connections = filter_inventory(
            self.gateways, self.connections, status="Error")
        self.assertEqual([c["id"] for c in connections], ["conn-0003"])

    def test_name_exact_gateway(self):
        gateways, connections = filter_inventory(
            self.gateways, self.connections, name="vpn-prod")
        self.assertEqual([g["id"] for g in gateways], ["vgw-0001"])
        self.assertEqual([c["id"] for c in connections], ["conn-0001", "conn-0002"])

    def test_name_match_on_connection_keeps_its_gateway(self):
        gateways, connections = filter_inventory(
            self.gateways, self.connections, name="to-plant")
        self.assertEqual([g["id"] for g in gateways], ["vgw-0002"])
        # The matched gateway keeps all of its connections (its orphan-free view).
        self.assertEqual([c["id"] for c in connections], ["conn-0003", "conn-0004"])

    def test_fuzzy_name(self):
        gateways, _ = filter_inventory(
            self.gateways, self.connections, name="prod", fuzzy=True)
        self.assertEqual([g["id"] for g in gateways], ["vgw-0001"])
        gateways, _ = filter_inventory(
            self.gateways, self.connections, name="prod")
        self.assertEqual(gateways, [])

    def test_unknown_name_returns_empty(self):
        gateways, connections = filter_inventory(
            self.gateways, self.connections, name="nope")
        self.assertEqual(gateways, [])
        self.assertEqual(connections, [])


class TestRendering(unittest.TestCase):
    def test_summary_counts(self):
        summary = summarize(
            [GATEWAY_1, GATEWAY_2],
            [CONN_UP, CONN_DOWN, CONN_ERROR, CONN_NO_STATUS])
        self.assertEqual(summary["gateway_count"], 2)
        self.assertEqual(summary["connection_count"], 3)
        self.assertEqual(summary["up_count"], 1)
        self.assertEqual(summary["not_up_count"], 2)
        self.assertEqual(summary["unknown_status_count"], 1)

    def test_default_renders_not_up_section_separately(self):
        lines = render_default(
            "cn-north-4", [GATEWAY_1, GATEWAY_2],
            [CONN_UP, CONN_DOWN, CONN_ERROR])
        text = "\n".join(lines)
        self.assertIn("⚠ 非 UP 连接（2 条", text)
        section = text.split("⚠ 非 UP 连接")[1]
        self.assertIn("conn-0002", section)
        self.assertIn("conn-0003", section)
        self.assertNotIn("conn-0001", section)

    def test_default_all_up(self):
        lines = render_default("cn-north-4", [GATEWAY_1], [CONN_UP])
        self.assertIn("✓ 无非 UP 连接", "\n".join(lines))

    def test_default_empty_region(self):
        self.assertEqual(render_default("cn-north-4", [], []),
                         ["当前区域（cn-north-4）无 VPN 网关。"])

    def test_gateway_table_has_nine_columns(self):
        table = "\n".join(render_gateway_table([GATEWAY_1, GATEWAY_2], [CONN_UP]))
        header = table.splitlines()[0]
        for title in ("网关ID", "名称", "状态", "规格", "接入类型", "VPC",
                      "本端子网", "EIP", "连接数"):
            self.assertIn(title, header)
        self.assertEqual(len(header.split()), 9)

    def test_connection_table_has_seven_columns(self):
        table = "\n".join(render_connection_table([CONN_UP]))
        header = table.splitlines()[0]
        for title in ("连接ID", "名称", "状态", "网关ID", "网关IP",
                      "对端网段", "创建时间"):
            self.assertIn(title, header)
        self.assertEqual(len(header.split()), 7)

    def test_tables_split_up_and_not_up(self):
        lines = render_tables(
            "cn-north-4", [GATEWAY_1], [CONN_UP, CONN_DOWN])
        text = "\n".join(lines)
        self.assertIn("【IPSec 连接 · UP】共 1 条", text)
        self.assertIn("⚠【IPSec 连接 · 非 UP】共 1 条", text)
        up_section = text.split("【IPSec 连接 · UP】")[1].split("⚠")[0]
        self.assertIn("conn-0001", up_section)
        self.assertNotIn("conn-0002", up_section)

    def test_missing_fields_render_as_dash(self):
        table = "\n".join(render_connection_table([CONN_NO_STATUS]))
        self.assertIn("-", table)


class TestMain(unittest.TestCase):
    def _run(self, argv, gateways, connections):
        out = io.StringIO()
        err = io.StringIO()
        with mock.patch("list_vpn_connections.list_vpn_gateways",
                        return_value=gateways):
            with mock.patch("list_vpn_connections.list_vpn_connections",
                            return_value=connections):
                with redirect_stdout(out), redirect_stderr(err):
                    code = main(argv)
        return code, out.getvalue(), err.getvalue()

    def test_default_output(self):
        code, out, _ = self._run(
            [], [GATEWAY_1], [CONN_UP, CONN_DOWN])
        self.assertEqual(code, 0)
        self.assertIn("VPN 网关", out)
        self.assertIn("⚠ 非 UP 连接", out)

    def test_table_output(self):
        code, out, _ = self._run(
            ["--table"], [GATEWAY_1], [CONN_UP, CONN_DOWN])
        self.assertEqual(code, 0)
        self.assertIn("【VPN 网关】", out)
        self.assertIn("【IPSec 连接 · UP】", out)

    def test_json_output(self):
        raw = [dict(CONN_UP, psk="secret")]
        code, out, _ = self._run(["--json"], [GATEWAY_1], raw)
        self.assertEqual(code, 0)
        payload = json.loads(out)
        self.assertEqual(payload["region"], "cn-north-4")
        self.assertEqual(len(payload["vpn_gateways"]), 1)
        self.assertEqual(payload["summary"]["up_count"], 1)
        self.assertNotIn("secret", out)
        self.assertNotIn('"psk"', out)

    def test_status_down_filter(self):
        code, out, _ = self._run(
            ["--status", "DOWN"], [GATEWAY_1, GATEWAY_2],
            [CONN_UP, CONN_DOWN])
        self.assertEqual(code, 0)
        self.assertIn("conn-0002", out)
        self.assertNotIn("conn-0001", out)
        self.assertIn("status=DOWN", out)

    def test_gateway_id_drilldown(self):
        code, out, _ = self._run(
            ["--gateway-id", "vgw-0001"], [GATEWAY_1, GATEWAY_2],
            [CONN_UP, CONN_ERROR])
        self.assertEqual(code, 0)
        self.assertIn("vgw-0001", out)
        self.assertNotIn("vgw-0002", out)

    def test_invalid_gateway_id_fails(self):
        code, _, err = self._run(
            ["--gateway-id", "vgw-9999"], [GATEWAY_1], [CONN_UP])
        self.assertEqual(code, 1)
        self.assertIn("未找到 VPN 网关", err)
        self.assertIn("vgw-9999", err)

    def test_write_intent_blocked(self):
        code, _, err = self._run(["--operation", "DeleteVgw"], [GATEWAY_1], [])
        self.assertEqual(code, 1)
        self.assertIn("写操作意图", err)
        self.assertIn("守卫拦截", err)

    def test_empty_region(self):
        code, out, _ = self._run([], [], [])
        self.assertEqual(code, 0)
        self.assertIn("无 VPN 网关", out)

    def test_name_filter_no_match(self):
        code, out, _ = self._run(["--name", "nope"], [GATEWAY_1], [CONN_UP])
        self.assertEqual(code, 0)
        self.assertIn("无匹配的 VPN 网关", out)

    def test_api_error_exit_code(self):
        out = io.StringIO()
        err = io.StringIO()
        with mock.patch("list_vpn_connections.list_vpn_gateways",
                        side_effect=AuthError("无权限访问")):
            with mock.patch("list_vpn_connections.list_vpn_connections",
                            return_value=[]):
                with redirect_stdout(out), redirect_stderr(err):
                    code = main([])
        self.assertEqual(code, 1)
        self.assertIn("无权限访问", err.getvalue())

    def test_limit_out_of_range_rejected(self):
        with self.assertRaises(SystemExit):
            main(["--limit", "101"])
        with self.assertRaises(SystemExit):
            main(["--limit", "0"])

    def test_limit_upper_bound_accepted(self):
        code, _, _ = self._run(["--limit", "100"], [GATEWAY_1], [CONN_UP])
        self.assertEqual(code, 0)


class TestSkillQualityWrapper(unittest.TestCase):
    """The script path must obey the same skill-quality-cli wrapping rule as
    the documented direct commands; it degrades to bare hcloud only when the
    telemetry CLI is missing / disabled, or when hcloud itself is resolvable
    through the offline test override."""

    ARGV = ["VPN", "ListVgws", "--cli-region=cn-north-4"]

    def test_wrapped_when_quality_cli_available(self):
        env = {"VPN_LIST_SQC_BIN": "/fake/skill-quality-cli"}
        with mock.patch.dict(os.environ, env, clear=True), mock.patch(
                "list_vpn_connections._hcloud_resolvable", return_value=True):
            cmd = build_hcloud_command(list(self.ARGV))
        self.assertEqual(cmd, [
            "/fake/skill-quality-cli", "run", "--skill-name",
            "huawei-cloud-vpn-connection-list", "--",
            "hcloud", "VPN", "ListVgws", "--cli-region=cn-north-4",
        ])

    def test_hcloud_bin_override_runs_verbatim(self):
        env = {"VPN_LIST_SQC_BIN": "/fake/skill-quality-cli",
               "VPN_LIST_HCLOUD_BIN": "/fake/hcloud"}
        with mock.patch.dict(os.environ, env, clear=True), mock.patch(
                "list_vpn_connections._hcloud_resolvable", return_value=True):
            cmd = build_hcloud_command(list(self.ARGV))
        self.assertEqual(cmd, ["/fake/hcloud"] + self.ARGV)

    def test_quality_report_disabled_degrades_to_bare_hcloud(self):
        env = {"VPN_LIST_SQC_BIN": "/fake/skill-quality-cli",
               "SKILL_QUALITY_REPORT": "0"}
        with mock.patch.dict(os.environ, env, clear=True), mock.patch(
                "list_vpn_connections._hcloud_resolvable", return_value=True):
            cmd = build_hcloud_command(list(self.ARGV))
        self.assertEqual(cmd, ["hcloud"] + self.ARGV)

    def test_missing_hcloud_skips_wrapper_for_sdk_fallback(self):
        env = {"VPN_LIST_SQC_BIN": "/fake/skill-quality-cli"}
        with mock.patch.dict(os.environ, env, clear=True), mock.patch(
                "list_vpn_connections._hcloud_resolvable", return_value=False):
            cmd = build_hcloud_command(list(self.ARGV))
        self.assertEqual(cmd, ["hcloud"] + self.ARGV)

    def test_run_hcloud_actually_wraps(self):
        fake = FakeRunner([(json.dumps({"vpn_gateways": [GATEWAY_1]}), "", 0)])
        env = {"VPN_LIST_SQC_BIN": "/fake/skill-quality-cli"}
        with mock.patch.dict(os.environ, env, clear=True), mock.patch(
                "list_vpn_connections._hcloud_resolvable", return_value=True), \
                mock.patch("list_vpn_connections.subprocess.run", fake):
            list_vpn_gateways("cn-north-4")
        self.assertEqual(fake.calls[0][:5], [
            "/fake/skill-quality-cli", "run", "--skill-name",
            "huawei-cloud-vpn-connection-list", "--",
        ])
        self.assertEqual(fake.calls[0][5], "hcloud")
        self.assertIn("ListVgws", fake.calls[0])


class TestReadOnlySurface(unittest.TestCase):
    def test_no_mutating_operation_is_ever_constructed(self):
        # Only the two read-only operations exist in the allowed whitelist.
        self.assertEqual(ALLOWED_OPERATIONS, ("ListVgws", "ListVpnConnections"))

    def test_all_errors_derive_from_base(self):
        for cls in (GuardError, ConfigError, AuthError, ApiError, NotFoundError):
            self.assertTrue(issubclass(cls, VpnListError))


if __name__ == "__main__":
    unittest.main()