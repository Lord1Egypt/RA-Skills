import json
import os
import subprocess
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from list_hss import (  # noqa: E402
    ALLOWED_OPERATION,
    ApiError,
    AuthError,
    ConfigError,
    GuardError,
    HssListError,
    build_command,
    classify_hcloud_failure,
    extract_hosts,
    extract_json,
    guard_operation,
    guard_write_intent,
    host_names,
    list_hosts,
    list_hosts_via_sdk,
    main,
    normalize_host,
    render_table,
)

HOST_1 = {
    "host_name": "web-01",
    "host_id": "2d8d24c0-8a3a-4b11-8b1f-000000000001",
    "agent_id": "agent-0001",
    "private_ip": "192.168.1.10",
    "public_ip": "1.2.3.4",
    "os_name": "CentOS 7.6",
    "os_type": "Linux",
    "os_bit": "64",
    "host_status": "ACTIVE",
    "agent_status": "online",
    "version": "hss.version.enterprise",
    "protect_status": "opened",
    "detect_result": "clean",
    "group_name": "default",
    "enterprise_project_name": "default",
    "asset": {"important_asset": False},
}
HOST_2 = {
    "host_name": "db-02",
    "host_id": "2d8d24c0-8a3a-4b11-8b1f-000000000002",
    "agent_id": "agent-0002",
    "private_ip": "192.168.1.11",
    "public_ip": "",
    "os_name": "Ubuntu 20.04",
    "os_type": "Linux",
    "os_bit": "64",
    "host_status": "SHUTOFF",
    "agent_status": "offline",
    "version": "hss.version.basic",
    "protect_status": "opened",
    "detect_result": "undetected",
}

HOSTS_RESPONSE = {
    "total_num": 2,
    "data_list": [HOST_1, HOST_2],
}


def hcloud_result(stdout="", stderr="", returncode=0):
    return (stdout, stderr, returncode)


class GuardTest(unittest.TestCase):
    def test_reject_write_intents(self):
        for bad in ("create", "ChangeEvent", "--update-host", "install_agent",
                    "delete", "remove", "ChangeVulStatus", "isolate"):
            with self.assertRaises(GuardError, msg=bad):
                guard_write_intent(bad)

    def test_allow_readonly_vocabulary(self):
        for ok in ("ListHostStatus", "show list", "查询主机", "list", "--host-name",
                    "online", "opened"):
            self.assertFalse(guard_write_intent(ok))

    def test_guard_operation(self):
        self.assertTrue(guard_operation("ListHostStatus"))
        with self.assertRaises(GuardError):
            guard_operation("ChangeEvent")


class BuildCommandTest(unittest.TestCase):
    def test_minimal(self):
        argv = build_command("cn-north-4", limit=10)
        self.assertEqual(argv, [
            "HSS", "ListHostStatus",
            "--cli-region=cn-north-4", "--limit=10", "--offset=0",
        ])

    def test_filters(self):
        argv = build_command(
            "cn-north-4", host_name="web-01", agent_status="online",
            host_status="ACTIVE", protect_status="opened", os_type="Linux",
            ip_addr="192.168.1.10", version="hss.version.enterprise",
            enterprise_project_id="0", limit=20, offset=40,
        )
        for arg in (
            "--host_name=web-01",
            "--agent_status=online",
            "--host_status=ACTIVE",
            "--protect_status=opened",
            "--os_type=Linux",
            "--ip_addr=192.168.1.10",
            "--version=hss.version.enterprise",
            "--enterprise_project_id=0",
            "--limit=20",
            "--offset=40",
        ):
            self.assertIn(arg, argv, arg)


class ExtractionTest(unittest.TestCase):
    def test_extract_json(self):
        payload = extract_json(json.dumps(HOSTS_RESPONSE))
        self.assertEqual(payload["total_num"], 2)

    def test_extract_json_wrapped(self):
        payload = extract_json("noise\n" + json.dumps(HOSTS_RESPONSE) + "\n")
        self.assertEqual(len(extract_hosts(payload)), 2)

    def test_extract_json_invalid(self):
        with self.assertRaises(ApiError):
            extract_json("not json at all")

    def test_extract_hosts(self):
        self.assertEqual(extract_hosts(HOSTS_RESPONSE), [HOST_1, HOST_2])
        self.assertEqual(extract_hosts({"data_list": []}), [])
        self.assertEqual(extract_hosts([HOST_1]), [HOST_1])

    def test_normalize_host_compacts_nested(self):
        flat = normalize_host(HOST_1)
        self.assertIn("asset", flat)
        self.assertIsInstance(flat["asset"], str)


class ClassifyFailureTest(unittest.TestCase):
    def test_use_error(self):
        exc = classify_hcloud_failure(
            "[USE_ERROR]Invalid parameter: --limit=1", "", 0)
        self.assertIsInstance(exc, ApiError)
        self.assertIn("参数错误", str(exc))

    def test_credential_missing(self):
        exc = classify_hcloud_failure(
            "", "The cli-ak or cli-sk is not configured", 1)
        self.assertIsInstance(exc, ConfigError)
        self.assertIn("AK/SK", str(exc))

    def test_auth_403(self):
        blob = json.dumps({
            "error_code": "common.01010013",
            "error_msg": "not authorized to perform: hss:host:listHostStatus",
        })
        exc = classify_hcloud_failure(blob, "", 0)
        self.assertIsInstance(exc, AuthError)

    def test_unknown(self):
        exc = classify_hcloud_failure("boom", "", 1)
        self.assertIsInstance(exc, ApiError)


@mock.patch("list_hss.run_hcloud")
class ListHostsTest(unittest.TestCase):
    def test_paging_until_total(self, run_hcloud):
        run_hcloud.side_effect = [
            hcloud_result(json.dumps({"total_num": 25, "data_list": ["h%d" % i for i in range(8)]})),
            hcloud_result(json.dumps({"total_num": 25, "data_list": ["h%d" % i for i in range(8, 16)]})),
            hcloud_result(json.dumps({"total_num": 25, "data_list": ["h%d" % i for i in range(16, 25)]})),
        ]
        hosts = list_hosts("cn-north-4", limit=10)
        self.assertEqual(len(hosts), 25)
        self.assertEqual(run_hcloud.call_count, 3)

    def test_single_page(self, run_hcloud):
        run_hcloud.return_value = hcloud_result(json.dumps(HOSTS_RESPONSE))
        hosts = list_hosts("cn-north-4", limit=10)
        self.assertEqual(len(hosts), 2)
        self.assertEqual(run_hcloud.call_count, 1)

    def test_empty(self, run_hcloud):
        run_hcloud.return_value = hcloud_result(
            json.dumps({"total_num": 0, "data_list": []}))
        hosts = list_hosts("cn-north-4")
        self.assertEqual(hosts, [])

    def test_auth_failure(self, run_hcloud):
        run_hcloud.return_value = hcloud_result(
            json.dumps({"error_code": "common.01010013",
                        "error_msg": "not authorized"}))
        with self.assertRaises(AuthError):
            list_hosts("cn-north-4")

    def test_use_error_hardfail(self, run_hcloud):
        run_hcloud.return_value = hcloud_result("[USE_ERROR]bad param", "", 0)
        with self.assertRaises(ApiError):
            list_hosts("cn-north-4")


class SdkFallbackTest(unittest.TestCase):
    def test_missing_sdk(self):
        with mock.patch.dict(os.environ, {
            "HUAWEICLOUD_SDK_AK": "ak", "HUAWEICLOUD_SDK_SK": "sk",
            "HUAWEICLOUD_SDK_PROJECT_ID": "p1"}):
            with mock.patch.dict("sys.modules", {"huaweicloudsdkcore": None}):
                # ImportError on huaweicloudsdkcore surface is masked here;
                # just ensure a ConfigError is raised (SDK absent).
                pass
        # Direct check: with nonexistent modules, ConfigError must be raised.
        from importlib import reload
        from list_hss import list_hosts_via_sdk as fn
        with mock.patch("builtins.__import__",
                        side_effect=ImportError("no sdk")):
            with self.assertRaises(ConfigError):
                fn("cn-north-4")

    def test_env_project_id_resolution(self):
        with mock.patch.dict(os.environ, {
            "HW_ACCESS_KEY": "ak", "HW_SECRET_KEY": "sk"}):
            with mock.patch("builtins.__import__",
                            side_effect=ImportError("no sdk")):
                # Still a ConfigError but mentioning SDK missing, not project.
                try:
                    list_hosts_via_sdk("cn-north-4")
                    self.fail("expected ConfigError")
                except ConfigError as e:
                    self.assertIn("SDK", str(e))


class MainTest(unittest.TestCase):
    @mock.patch("list_hss.run_hcloud")
    def test_table_output(self, run_hcloud):
        run_hcloud.return_value = hcloud_result(json.dumps(HOSTS_RESPONSE))
        rc = main(["--region", "cn-north-4"])
        self.assertEqual(rc, 0)

    @mock.patch("list_hss.run_hcloud")
    def test_json_output(self, run_hcloud):
        run_hcloud.return_value = hcloud_result(json.dumps(HOSTS_RESPONSE))
        rc = main(["--region", "cn-north-4", "--json"])
        self.assertEqual(rc, 0)

    @mock.patch("list_hss.run_hcloud")
    def test_names_only(self, run_hcloud):
        run_hcloud.return_value = hcloud_result(json.dumps(HOSTS_RESPONSE))
        rc = main(["--region", "cn-north-4", "--names-only"])
        self.assertEqual(rc, 0)

    def test_write_intent_from_main(self):
        with mock.patch("list_hss.run_hcloud") as run_hcloud:
            run_hcloud.return_value = hcloud_result("{}")
            rc = main(["--region", "cn-north-4", "--host-name", "remove-me"])
            self.assertEqual(rc, 1)
            run_hcloud.assert_not_called()


class TableRenderTest(unittest.TestCase):
    def test_render_table_has_hosts(self):
        out = render_table([HOST_1, HOST_2])
        self.assertIn("host_name", out)
        self.assertIn("web-01", out)
        self.assertIn("db-02", out)

    def test_host_names(self):
        self.assertEqual(host_names([HOST_1, HOST_2]), ["web-01", "db-02"])


if __name__ == "__main__":
    unittest.main()