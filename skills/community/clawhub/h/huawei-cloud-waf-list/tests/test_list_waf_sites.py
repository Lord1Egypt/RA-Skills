#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Offline unit tests for huawei-cloud-waf-list.

No credentials and no network are used: the hcloud subprocess is mocked with a
fake command runner returning canned WAF responses.

Run:
    python3 -m unittest discover -s tests -v
"""

import importlib.util
import io
import pathlib
import unittest
from contextlib import redirect_stderr, redirect_stdout

HERE = pathlib.Path(__file__).resolve().parent
MOD_PATH = HERE.parent / "scripts" / "list_waf_sites.py"

_spec = importlib.util.spec_from_file_location("list_waf_sites", MOD_PATH)
waf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(waf)


SAMPLE_HOST = {
    "hostname": "www.example.com",
    "hostid": "h-001",
    "id": "h-001",
    "protect_status": 1,
    "access_status": 1,
    "proxy": True,
    "exclusive_ip": False,
    "waf_type": "cloud",
    "policyid": "p-001",
    "web_tag": "demo",
    "server": [{"address": "1.2.3.4", "front_protocol": "HTTPS", "back_protocol": "HTTPS", "port": 443}],
}

SAMPLE_PREMIUM_HOST = {
    "hostname": "premium.example.org",
    "hostid": "h-002",
    "id": "h-002",
    "protect_status": 0,
    "access_status": 0,
    "proxy": False,
    "exclusive_ip": True,
    "waf_type": "premium",
    "policyid": "p-002",
    "web_tag": "",
    "server": [],
}


class FakeHcloud(object):
    """Mock hcloud subprocess: returns canned responses by operation."""

    def __init__(self, responses, failures=None):
        self.responses = responses        # operation-name -> json body
        self.failures = failures or {}    # operation-name -> error text
        self.calls = []

    def __call__(self, args, timeout=60):
        name = args[2] if len(args) > 2 else ""
        self.calls.append(args)
        if name in self.failures:
            raise RuntimeError(self.failures[name])
        resp = self.responses.get(name, {"items": []})
        return resp


def run_main(args, fake):
    """Run waf.main with the given args and fake hcloud binary."""
    with redirect_stdout(io.StringIO()) as out, redirect_stderr(io.StringIO()) as err:
        orig_hcloud = waf._hcloud
        waf._hcloud = fake
        try:
            code = waf.main(args)
        finally:
            waf._hcloud = orig_hcloud
    return code, out.getvalue(), err.getvalue()


class WafListTest(unittest.TestCase):

    def setUp(self):
        self.fake = FakeHcloud({
            "ListHost": {"items": [SAMPLE_HOST]},
            "ListCompositeHosts": {"items": [SAMPLE_HOST, SAMPLE_PREMIUM_HOST]},
        })

    def test_default_lists_cloud_hosts(self):
        code, out, _ = run_main(["--region", "cn-north-4"], self.fake)
        self.assertEqual(code, 0)
        self.assertIn("www.example.com", out)
        self.assertIn("防护域名", out)
        self.assertIn("共 1 个防护网站", out)
        # default should hit ListHost
        self.assertTrue(any(a[2] == "ListHost" for a in self.fake.calls))

    def test_all_modes_uses_composite(self):
        code, out, _ = run_main(["--all-modes", "--region", "cn-north-4"], self.fake)
        self.assertEqual(code, 0)
        self.assertIn("premium.example.org", out)
        self.assertIn("共 2 个防护网站", out)
        self.assertTrue(any(a[2] == "ListCompositeHosts" for a in self.fake.calls))

    def test_premium_mode_filters(self):
        code, out, _ = run_main(["--mode", "premium", "--region", "cn-north-4"], self.fake)
        self.assertEqual(code, 0)
        self.assertIn("premium.example.org", out)
        self.assertNotIn("www.example.com", out)

    def test_json_output(self):
        code, out, _ = run_main(["--all-modes", "--json", "--region", "cn-north-4"], self.fake)
        self.assertEqual(code, 0)
        import json as j
        parsed = j.loads(out)
        self.assertEqual(len(parsed["items"]), 2)
        self.assertEqual(parsed["items"][0]["waf_type"], "cloud")
        self.assertEqual(parsed["items"][1]["waf_type"], "premium")

    def test_names_only(self):
        code, out, _ = run_main(["--names-only", "--region", "cn-north-4"], self.fake)
        self.assertEqual(code, 0)
        lines = [l for l in out.splitlines() if l.strip()]
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0], "www.example.com")

    def test_protect_status_filter_passes_param(self):
        code, out, _ = run_main(["--all-modes", "--protect-status", "1",
                                 "--region", "cn-north-4"], self.fake)
        self.assertEqual(code, 0)
        cmd = self.fake.calls[-1]
        self.assertTrue(any("--protect_status=1" in a for a in cmd))

    def test_write_intent_guard(self):
        code, out, err = run_main(["--hostname", "delete www.example.com",
                                   "--region", "cn-north-4"], self.fake)
        self.assertEqual(code, 1)
        self.assertEqual(len(self.fake.calls), 0)
        self.assertIn("只读查询", out)

    def test_empty_list_hint(self):
        fake = FakeHcloud({"ListHost": {"items": []}})
        code, out, _ = run_main(["--region", "cn-north-4"], fake)
        self.assertEqual(code, 0)
        self.assertIn("当前区域无 WAF 防护网站", out)

    def test_permission_error_hint(self):
        fake = FakeHcloud(
            {"ListHost": {}},
            failures={"ListHost": '{"error_code": "WAF.00012006", "error_msg": "not authorized"}'},
        )
        code, out, err = run_main(["--region", "cn-north-4"], fake)
        self.assertEqual(code, 1)
        self.assertIn("无权限访问 WAF 防护网站列表", err)


if __name__ == "__main__":
    unittest.main()