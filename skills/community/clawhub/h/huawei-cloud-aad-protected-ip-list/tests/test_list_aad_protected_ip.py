#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Offline unit tests for huawei-cloud-aad-protected-ip-list.

No credentials and no network are used: the KooCLI subprocess is mocked with a
fake command runner and the SDK fallback is mocked with a canned response.

Run:
    python3 -m unittest discover -s tests -v
"""

import importlib.util
import io
import json
import os
import pathlib
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest import mock

HERE = pathlib.Path(__file__).resolve().parent
MOD_PATH = HERE.parent / "scripts" / "list_aad_protected_ip.py"

_spec = importlib.util.spec_from_file_location(
    "list_aad_protected_ip", MOD_PATH)
aad = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(aad)


def sample_item(ip="192.0.2.10", status=2):
    return {
        "id": "ip-" + ip,
        "ip": ip,
        "type": "EIP",
        "name": "demo-" + ip,
        "status": status,
        "status_detail": {"block_time": 1700000000000,
                          "unblock_time": 1700003600000},
        "policy_name": "default-policy",
        "region": "cn-north-4",
        "package_id": "pkg-001",
        "package_name": "AAD-Package",
        "tags": "tms:web",
        "tag": "web",
        "is_resale": False,
        "package_version": "cnad_pro",
    }


class FakeHcloud(object):
    """Mock KooCLI: paginates canned items according to offset/limit."""

    def __init__(self, items, failures=None, total=None):
        self.items = items
        self.failures = failures or {}
        self.total = total if total is not None else len(items)
        self.calls = []

    def __call__(self, args, timeout=60):
        self.calls.append(args)
        if self.failures.get("ListProtectedIp"):
            raise RuntimeError(self.failures["ListProtectedIp"])
        offset = 0
        limit = aad.DEFAULT_PAGE_SIZE
        for arg in args:
            if arg.startswith("--offset="):
                offset = int(arg.split("=", 1)[1])
            elif arg.startswith("--limit="):
                limit = int(arg.split("=", 1)[1])
        page = self.items[offset:offset + limit]
        return {"total": self.total, "items": page}


def run_main(args, fake=None, sdk_items=None, sdk_error=None,
             sdk_available=None):
    """Run aad.main with mocked CLI/SDK backends."""
    orig_hcloud = aad._hcloud
    orig_binary = aad._hcloud_binary
    orig_sdk_available = aad._sdk_available
    orig_list_sdk = aad._list_via_sdk

    if fake is not None:
        aad._hcloud = fake
        aad._hcloud_binary = lambda: "/usr/local/bin/hcloud"
    else:
        aad._hcloud_binary = lambda: None

    if sdk_available is not None:
        aad._sdk_available = lambda: sdk_available

    def fake_sdk(region, page_size, start_offset, filters, timeout=60):
        if sdk_error:
            raise sdk_error
        items = sdk_items if sdk_items is not None else []
        return len(items), items

    aad._list_via_sdk = fake_sdk

    with redirect_stdout(io.StringIO()) as out, redirect_stderr(io.StringIO()) as err:
        try:
            code = aad.main(args)
        finally:
            aad._hcloud = orig_hcloud
            aad._hcloud_binary = orig_binary
            aad._sdk_available = orig_sdk_available
            aad._list_via_sdk = orig_list_sdk
    return code, out.getvalue(), err.getvalue()


def cli_param(call, name):
    prefix = "--{0}=".format(name)
    for arg in call:
        if arg.startswith(prefix):
            return arg.split("=", 1)[1]
    return None


class AadListTest(unittest.TestCase):

    def test_default_concise_list(self):
        fake = FakeHcloud([sample_item("192.0.2.10"), sample_item("192.0.2.11", 0)])
        code, out, err = run_main(["--region", "cn-north-4"], fake)
        self.assertEqual(code, 0)
        self.assertIn("防护 IP", out)
        self.assertIn("192.0.2.10", out)
        self.assertIn("黑洞中（封堵中）", out)
        self.assertIn("共 2 个防护 IP", out)
        self.assertEqual(err, "")

    def test_table_columns(self):
        fake = FakeHcloud([sample_item()])
        code, out, _ = run_main(["--table", "--region", "cn-north-4"], fake)
        self.assertEqual(code, 0)
        for header in ("防护 IP", "状态", "绑定策略", "套餐", "region"):
            self.assertIn(header, out)
        self.assertIn("default-policy", out)
        self.assertIn("AAD-Package（专业版）", out)
        self.assertIn("cn-north-4", out)

    def test_json_output(self):
        fake = FakeHcloud([sample_item(), sample_item("192.0.2.11", 1)])
        code, out, _ = run_main(["--json", "--region", "cn-north-4"], fake)
        self.assertEqual(code, 0)
        parsed = json.loads(out)
        self.assertEqual(parsed["total"], 2)
        self.assertEqual(len(parsed["items"]), 2)
        self.assertEqual(parsed["items"][1]["status"], 1)

    def test_filters_passed_to_cli(self):
        fake = FakeHcloud([sample_item()])
        code, _, _ = run_main([
            "--ip", "192.0.2.10", "--policy-id", "policy-1",
            "--package-id", "pkg-1", "--tag", "web",
            "--region", "cn-north-4",
        ], fake)
        self.assertEqual(code, 0)
        call = fake.calls[0]
        self.assertEqual(cli_param(call, "ip"), "192.0.2.10")
        self.assertEqual(cli_param(call, "policy_id"), "policy-1")
        self.assertEqual(cli_param(call, "package_id"), "pkg-1")
        self.assertEqual(cli_param(call, "tag"), "web")
        self.assertEqual(cli_param(call, "cli-region"), "cn-north-4")

    def test_auto_pagination_fetches_all(self):
        items = [sample_item("192.0.2.{0}".format(i)) for i in range(250)]
        fake = FakeHcloud(items, total=250)
        code, out, _ = run_main(["--region", "cn-north-4"], fake)
        self.assertEqual(code, 0)
        self.assertIn("共 250 个防护 IP", out)
        self.assertEqual(len(fake.calls), 3)
        self.assertEqual([cli_param(c, "offset") for c in fake.calls],
                         ["0", "100", "200"])

    def test_pagination_respects_start_offset(self):
        items = [sample_item("192.0.2.{0}".format(i)) for i in range(250)]
        fake = FakeHcloud(items, total=250)
        code, _, _ = run_main(["--offset", "100", "--region", "cn-north-4"], fake)
        self.assertEqual(code, 0)
        self.assertEqual(cli_param(fake.calls[0], "offset"), "100")

    def test_limit_above_max_is_clamped(self):
        fake = FakeHcloud([sample_item()])
        code, _, err = run_main(["--limit", "500", "--region", "cn-north-4"], fake)
        self.assertEqual(code, 0)
        self.assertIn("收敛为 100", err)
        self.assertEqual(cli_param(fake.calls[0], "limit"), "100")

    def test_invalid_limit(self):
        fake = FakeHcloud([sample_item()])
        code, _, err = run_main(["--limit", "0", "--region", "cn-north-4"], fake)
        self.assertEqual(code, 1)
        self.assertIn("--limit", err)
        self.assertEqual(fake.calls, [])

    def test_empty_list_hint(self):
        fake = FakeHcloud([], total=0)
        code, out, _ = run_main(["--region", "cn-north-4"], fake)
        self.assertEqual(code, 0)
        self.assertIn("未找到 Anti-DDoS 防护 IP", out)

    def test_empty_filtered_list_hint(self):
        fake = FakeHcloud([], total=0)
        code, out, _ = run_main(["--ip", "192.0.2.99", "--region", "cn-north-4"], fake)
        self.assertEqual(code, 0)
        self.assertIn("未找到匹配的 Anti-DDoS 防护 IP", out)

    def test_permission_error_hint(self):
        fake = FakeHcloud([], failures={
            "ListProtectedIp": '{"error_code": "AAD.0401", "error_msg": "403 Forbidden"}',
        })
        code, _, err = run_main(["--region", "cn-north-4"], fake)
        self.assertEqual(code, 1)
        self.assertIn("无权限访问 Anti-DDoS 防护 IP 列表", err)
        self.assertNotIn("Traceback", err)

    def test_credential_error_hint(self):
        fake = FakeHcloud([], failures={
            "ListProtectedIp": "401 Unauthorized: AK/SK credential not found",
        })
        code, _, err = run_main(["--region", "cn-north-4"], fake)
        self.assertEqual(code, 1)
        self.assertIn("未找到可用的华为云凭据", err)
        self.assertNotIn("Traceback", err)

    def test_network_error_hint(self):
        fake = FakeHcloud([], failures={
            "ListProtectedIp": "HTTPSConnectionPool: connection timed out",
        })
        code, _, err = run_main(["--region", "cn-north-4"], fake, sdk_available=False)
        self.assertEqual(code, 1)
        self.assertIn("网络超时或不可达", err)
        self.assertNotIn("Traceback", err)

    def test_write_action_guard(self):
        fake = FakeHcloud([sample_item()])
        code, _, err = run_main(["--action", "unblock", "--region", "cn-north-4"], fake)
        self.assertEqual(code, 1)
        self.assertEqual(fake.calls, [])
        self.assertIn("只读查询", err)

    def test_write_filter_guard(self):
        fake = FakeHcloud([sample_item()])
        code, _, err = run_main(["--tag", "delete-this", "--region", "cn-north-4"], fake)
        self.assertEqual(code, 1)
        self.assertEqual(fake.calls, [])
        self.assertIn("只读查询", err)

    def test_read_action_is_allowed(self):
        fake = FakeHcloud([sample_item()])
        code, out, _ = run_main(["--action", "list", "--region", "cn-north-4"], fake)
        self.assertEqual(code, 0)
        self.assertIn("192.0.2.10", out)

    def test_sdk_fallback_when_hcloud_missing(self):
        code, out, err = run_main(
            ["--region", "cn-north-4"],
            fake=None,
            sdk_items=[sample_item("198.51.100.7")],
            sdk_available=True,
        )
        self.assertEqual(code, 0)
        self.assertIn("198.51.100.7", out)
        self.assertIn("已回退 SDK", err)

    def test_sdk_fallback_when_cli_operation_unsupported(self):
        fake = FakeHcloud([], failures={
            "ListProtectedIp": "[USE_ERROR] Operation AAD.ListProtectedIp is not supported",
        })
        code, out, err = run_main(
            ["--region", "cn-north-4"], fake,
            sdk_items=[sample_item("198.51.100.8")],
            sdk_available=True,
        )
        self.assertEqual(code, 0)
        self.assertIn("198.51.100.8", out)
        self.assertIn("已回退 SDK", err)

    def test_missing_cli_and_sdk_hint(self):
        code, _, err = run_main(["--region", "cn-north-4"], fake=None,
                                sdk_available=False)
        self.assertEqual(code, 1)
        self.assertIn("未找到 hcloud CLI", err)
        self.assertIn("huaweicloudsdkaad", err)
        self.assertNotIn("Traceback", err)


class CredentialWhitelistTest(unittest.TestCase):

    def test_reads_whitelisted_names(self):
        env = {
            "HUAWEICLOUD_SDK_AK": "ak-main",
            "HUAWEICLOUD_SDK_SK": "sk-main",
            "HUAWEICLOUD_SDK_SECURITY_TOKEN": "tok-main",
        }
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertEqual(
                aad._resolve_credentials(),
                ("ak-main", "sk-main", "tok-main"),
            )

    def test_alternate_names_are_supported(self):
        env = {"HW_ACCESS_KEY": "ak-hw", "HW_SECRET_KEY": "sk-hw"}
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertEqual(aad._resolve_credentials(), ("ak-hw", "sk-hw", ""))

    def test_unlisted_values_are_never_harvested(self):
        env = {
            "HUAWEI_ROGUE_ACCESS_KEY": "bad-ak",
            "HUAWEI_ROGUE_SECRET_KEY": "bad-sk",
            "HWC_ROGUE_SECURITY_TOKEN": "bad-tok",
            "OTHER_SECRET_KEY": "bad-other",
        }
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertEqual(aad._resolve_credentials(), ("", "", ""))


class ResponseConversionTest(unittest.TestCase):

    def test_to_json_object_wins(self):
        class Resp(object):
            def to_json_object(self):
                return {"total": 1, "items": []}

            def to_dict(self):  # pragma: no cover - must not be called
                raise AssertionError("to_dict should not be used")

        self.assertEqual(aad._response_to_dict(Resp()),
                         {"total": 1, "items": []})

    def test_to_dict_fallback(self):
        class Resp(object):
            def to_dict(self):
                return {"total": 2, "items": [{"ip": "192.0.2.1"}]}

        self.assertEqual(aad._response_to_dict(Resp()),
                         {"total": 2, "items": [{"ip": "192.0.2.1"}]})

    def test_to_str_fallback_parses_json(self):
        class Resp(object):
            def to_str(self):
                return json.dumps({"total": 0, "items": []})

        self.assertEqual(aad._response_to_dict(Resp()), {"total": 0, "items": []})

    def test_unknown_object_returns_empty_dict(self):
        self.assertEqual(aad._response_to_dict(object()), {})
        self.assertEqual(aad._response_to_dict({"total": 3}), {"total": 3})


if __name__ == "__main__":
    unittest.main()