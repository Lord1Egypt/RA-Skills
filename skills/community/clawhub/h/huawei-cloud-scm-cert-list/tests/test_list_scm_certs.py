#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Offline unit tests for huawei-cloud-scm-cert-list.

No credentials and no network are used: the KooCLI subprocess is mocked with a
fake runner (and, for integration cases, a real mock executable injected via
``HUAWEI_CLOUD_SCM_CERT_LIST_HCLOUD_BIN``); the SDK fallback is driven by a fake
client injected through ``sdk_client``, plus one contract test that builds the
real SCM SDK client with ``GlobalCredentials`` (no network: a dummy domain id is
supplied so the IAM lookup is skipped).

Run:
    python3 -m unittest discover -s tests -v
"""

import importlib.util
import io
import json
import os
import pathlib
import stat
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timedelta, timezone

try:
    from huaweicloudsdkcore.auth.credentials import (
        BasicCredentials, GlobalCredentials)
    from huaweicloudsdkscm.v3 import ScmClient
    SDK_INSTALLED = True
except ImportError:
    BasicCredentials = GlobalCredentials = ScmClient = None
    SDK_INSTALLED = False

HERE = pathlib.Path(__file__).resolve().parent
MOD_PATH = HERE.parent / "scripts" / "list_scm_certs.py"

_spec = importlib.util.spec_from_file_location("list_scm_certs", MOD_PATH)
scm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(scm)


def iso_in(days, hours=0):
    moment = datetime.now(timezone.utc) + timedelta(days=days, hours=hours)
    return moment.strftime("%Y-%m-%d %H:%M:%S")


CERT_A = {
    "id": "aa1b2c3d-1111-2222-3333-444455556666",
    "name": "prod-web",
    "domain": "www.example.com",
    "sans": "api.example.com",
    "type": "OV_SSL_CERT",
    "brand": "GEOTRUST",
    "expire_time": iso_in(20),
    "domain_type": "MULTI_DOMAIN",
    "validity_period": 12,
    "status": "ISSUED",
    "deploy_support": True,
    "enterprise_project_id": "0",
}
CERT_B = {
    "id": "bb1b2c3d-1111-2222-3333-444455556666",
    "name": "legacy-upload",
    "domain": "legacy.example.com",
    "sans": "",
    "type": "DV_SSL_CERT_BASIC",
    "brand": "CFCA",
    "expire_time": iso_in(120),
    "domain_type": "SINGLE_DOMAIN",
    "validity_period": 12,
    "status": "UPLOAD",
    "deploy_support": False,
    "enterprise_project_id": "0",
}


def page(items, total=None):
    return {
        "certificates": [dict(item) for item in items],
        "total_count": len(items) if total is None else total,
    }


def many(count, prefix="c"):
    """Build ``count`` distinct certificates (for multi-page fixtures)."""
    items = []
    for index in range(count):
        item = dict(CERT_A)
        item["id"] = "{0}-{1}".format(prefix, index)
        item["name"] = "cert-{0}-{1}".format(prefix, index)
        items.append(item)
    return items


class FakeHcloud(object):
    """Replacement for ``list_scm_certs.run_hcloud``."""

    def __init__(self, pages=None, error=None, fail_op=None):
        self.pages = list(pages or [])
        self.error = error
        self.fail_op = fail_op
        self.calls = []

    def __call__(self, args, timeout=None):
        self.calls.append(list(args))
        operation = args[1] if len(args) > 1 else ""
        if self.error is not None and (self.fail_op is None
                                       or operation == self.fail_op):
            raise self.error
        if operation == "ListCertificates":
            index = len(self.list_calls()) - 1
            if index < len(self.pages):
                return self.pages[index]
            return page([])
        raise AssertionError("unexpected operation: {0}".format(operation))

    def list_calls(self):
        return [c for c in self.calls if len(c) > 1 and c[1] == "ListCertificates"]

    def arg_of(self, call, name):
        for item in call:
            if str(item).startswith("--{0}=".format(name)):
                return str(item).split("=", 1)[1]
        return None


class FakeSdkResponse(object):
    def __init__(self, data):
        self._data = data

    def to_dict(self):
        return dict(self._data)


class FakeSdkClient(object):
    def __init__(self, pages):
        self.pages = list(pages)
        self.requests = []

    def list_certificates(self, request):
        self.requests.append(request)
        index = len(self.requests) - 1
        data = dict(self.pages[index]) if index < len(self.pages) else page([])
        data["certificates"] = [dict(d) if isinstance(d, dict) else d
                                for d in data.get("certificates", [])]
        return FakeSdkResponse(data)


class Base(unittest.TestCase):
    def setUp(self):
        self._env = dict(os.environ)
        for name in scm.HCLOUD_BIN_ENV + ("HUAWEICLOUD_SDK_AK",
                                          "HUAWEICLOUD_SDK_SK",
                                          "HUAWEICLOUD_SDK_DOMAIN_ID",
                                          "HUAWEI_ACCESS_KEY",
                                          "HUAWEI_SECRET_KEY",
                                          "HUAWEI_DOMAIN_ID"):
            os.environ.pop(name, None)
        self._run_hcloud = scm.run_hcloud
        self._hcloud_binary = scm.hcloud_binary
        self._sdk_client = scm.sdk_client

    def tearDown(self):
        scm.run_hcloud = self._run_hcloud
        scm.hcloud_binary = self._hcloud_binary
        scm.sdk_client = self._sdk_client
        os.environ.clear()
        os.environ.update(self._env)

    def install_hcloud(self, fake):
        scm.run_hcloud = fake
        scm.hcloud_binary = lambda: "/usr/local/bin/hcloud"

    def run_main(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = scm.main(argv)
        return code, out.getvalue(), err.getvalue()


class TestOutputModes(Base):
    def test_default_compact_list(self):
        self.install_hcloud(FakeHcloud([page([CERT_A, CERT_B])]))
        code, out, _ = self.run_main(["--region", "cn-north-4"])
        self.assertEqual(code, 0)
        self.assertIn("证书名称", out)
        self.assertIn("绑定域名", out)
        self.assertIn("到期时间", out)
        self.assertNotIn("证书ID", out)
        self.assertNotIn("类型", out)
        self.assertIn("prod-web", out)
        self.assertIn("www.example.com", out)
        self.assertIn("legacy-upload", out)
        self.assertIn("共 2 个证书", out)
        self.assertIn("cn-north-4", out)

    def test_table_has_eight_columns(self):
        self.install_hcloud(FakeHcloud([page([CERT_A, CERT_B])]))
        code, out, _ = self.run_main(["--table", "--region", "cn-north-4"])
        self.assertEqual(code, 0)
        for header in ("证书ID", "名称", "域名", "类型", "状态", "到期时间",
                       "剩余天数", "region"):
            self.assertIn(header, out)
        self.assertIn(CERT_A["id"], out)
        self.assertIn("OV", out)
        self.assertIn("DV", out)
        self.assertIn("ISSUED", out)
        self.assertIn("UPLOAD", out)

    def test_json_raw_body(self):
        self.install_hcloud(FakeHcloud([page([CERT_A, CERT_B])]))
        code, out, _ = self.run_main(["--json", "--region", "cn-north-4"])
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertEqual(data["total_count"], 2)
        self.assertEqual(len(data["certificates"]), 2)
        self.assertEqual(data["region"], "cn-north-4")
        self.assertEqual(data["certificates"][0]["name"], "prod-web")

    def test_source_distribution_in_footer(self):
        self.install_hcloud(FakeHcloud([page([CERT_A, CERT_B])]))
        code, out, _ = self.run_main([])
        self.assertEqual(code, 0)
        self.assertIn("SCM签发 1", out)
        self.assertIn("上传托管 1", out)


class TestPagination(Base):
    def test_offset_increments(self):
        fake = FakeHcloud([
            page(many(10), total=11),
            page(many(1, "d"), total=11),
        ])
        self.install_hcloud(fake)
        # --limit 10 is a valid API page size; the fake returns a full first page.
        code, out, _ = self.run_main(["--limit", "10", "--region", "cn-north-4"])
        self.assertEqual(code, 0)
        self.assertIn("共 11 个证书", out)
        calls = fake.list_calls()
        self.assertEqual(len(calls), 2)
        self.assertEqual(fake.arg_of(calls[0], "offset"), "0")
        self.assertEqual(fake.arg_of(calls[1], "offset"), "10")
        self.assertEqual(fake.arg_of(calls[0], "limit"), "10")

    def test_stops_on_short_page(self):
        fake = FakeHcloud([page([CERT_A], total=100)])
        self.install_hcloud(fake)
        code, out, _ = self.run_main([])
        self.assertEqual(code, 0)
        self.assertEqual(len(fake.list_calls()), 1)

    def test_stops_when_offset_reaches_total(self):
        fake = FakeHcloud([
            page([CERT_A], total=1),
        ])
        self.install_hcloud(fake)
        code, out, _ = self.run_main(["--limit", "10"])
        self.assertEqual(code, 0)
        self.assertEqual(len(fake.list_calls()), 1)
        self.assertIn("共 1 个证书", out)

    def test_max_pages_cap(self):
        fake = FakeHcloud([
            page(many(10, "a"), total=999),
            page(many(10, "b"), total=999),
            page(many(10, "c"), total=999),
        ])
        self.install_hcloud(fake)
        code, _, _ = self.run_main(["--limit", "10", "--max-pages", "2"])
        self.assertEqual(code, 0)
        self.assertEqual(len(fake.list_calls()), 2)

    def test_duplicate_cert_deduped(self):
        first = many(10, "dup")
        second = [dict(item) for item in first] + many(1, "extra")
        fake = FakeHcloud([
            page(first, total=11),
            page(second, total=11),
            page([], total=11),
        ])
        self.install_hcloud(fake)
        code, out, _ = self.run_main(["--limit", "10"])
        self.assertEqual(code, 0)
        self.assertIn("共 11 个证书", out)

    def test_start_offset_passed(self):
        fake = FakeHcloud([page([CERT_A])])
        self.install_hcloud(fake)
        code, _, _ = self.run_main(["--offset", "20"])
        self.assertEqual(code, 0)
        self.assertEqual(fake.arg_of(fake.list_calls()[0], "offset"), "20")


class TestFilters(Base):
    def setUp(self):
        Base.setUp(self)
        self.fake = FakeHcloud([page([CERT_A, CERT_B])])
        self.install_hcloud(self.fake)

    def test_content_passed_to_cli(self):
        code, out, _ = self.run_main(["--content", "legacy"])
        self.assertEqual(code, 0)
        self.assertEqual(scm.hcloud_binary(), "/usr/local/bin/hcloud")
        self.assertEqual(self.fake.arg_of(self.fake.list_calls()[0], "content"),
                         "legacy")
        self.assertIn("legacy-upload", out)
        self.assertNotIn("prod-web", out)

    def test_content_matches_domain_and_sans(self):
        code, out, _ = self.run_main(["--content", "api.example.com"])
        self.assertEqual(code, 0)
        self.assertIn("prod-web", out)
        self.assertNotIn("legacy-upload", out)

    def test_expiring_client_filter(self):
        code, out, _ = self.run_main(["--expiring", "30"])
        self.assertEqual(code, 0)
        self.assertIn("prod-web", out)
        self.assertNotIn("legacy-upload", out)
        self.assertIn("共 1 个证书", out)

    def test_expiring_includes_expired(self):
        expired = dict(CERT_A, id="cc", name="expired-cert",
                       expire_time=iso_in(-2))
        self.install_hcloud(FakeHcloud([page([expired, CERT_B])]))
        code, out, _ = self.run_main(["--expiring", "10"])
        self.assertEqual(code, 0)
        self.assertIn("expired-cert", out)
        self.assertNotIn("legacy-upload", out)

    def test_expired_days_since_passed(self):
        code, _, _ = self.run_main(["--expired-days-since", "60"])
        self.assertEqual(code, 0)
        self.assertEqual(
            self.fake.arg_of(self.fake.list_calls()[0], "expired_days_since"), "60")

    def test_enterprise_project_passed(self):
        code, _, _ = self.run_main(["--enterprise-project-id", "0"])
        self.assertEqual(code, 0)
        self.assertEqual(
            self.fake.arg_of(self.fake.list_calls()[0], "enterprise_project_id"),
            "0")

    def test_region_passed(self):
        code, _, _ = self.run_main(["--region", "ap-southeast-1"])
        self.assertEqual(code, 0)
        self.assertEqual(self.fake.arg_of(self.fake.list_calls()[0], "cli-region"),
                         "ap-southeast-1")


class TestEmptyAndErrors(Base):
    def test_empty_list_hint(self):
        self.install_hcloud(FakeHcloud([page([])]))
        code, out, _ = self.run_main(["--region", "cn-north-4"])
        self.assertEqual(code, 0)
        self.assertIn("未找到 SSL 证书", out)
        self.assertIn("cn-north-4", out)

    def test_empty_filtered_hint(self):
        self.install_hcloud(FakeHcloud([page([CERT_A])]))
        code, out, _ = self.run_main(["--content", "no-such-name"])
        self.assertEqual(code, 0)
        self.assertIn("未找到匹配的 SSL 证书", out)

    def test_forbidden_hint(self):
        fake = FakeHcloud(error=scm.classify_cli_error(
            '{"error_code":"SCM.4002","error_msg":"Permission denied. '
            'not authorized to perform: scm:cert:list"}', 1))
        self.install_hcloud(fake)
        code, _, err = self.run_main(["--region", "cn-north-4"])
        self.assertEqual(code, 1)
        self.assertIn("scm:cert:list", err)
        self.assertNotIn("Traceback", err)

    def test_classify_403(self):
        exc = scm.classify_cli_error("ERROR: SCM.4002 Permission denied", 1)
        self.assertEqual(exc.kind, "forbidden")
        self.assertIn("scm:cert:list", exc.message)

    def test_classify_use_error(self):
        exc = scm.classify_cli_error("[USE_ERROR]--limit invalid", 1)
        self.assertEqual(exc.kind, "use_error")

    def test_classify_credentials(self):
        exc = scm.classify_cli_error("ERROR: no credential found, "
                                     "please configure AK/SK", 1)
        self.assertEqual(exc.kind, "credentials")

    def test_classify_network(self):
        exc = scm.classify_cli_error(
            "HTTPSConnectionPool: Max retries exceeded Connection timed out", 1)
        self.assertEqual(exc.kind, "network")

    def test_use_error_hint(self):
        fake = FakeHcloud(error=scm.ScmError(
            "use_error", "KooCLI 参数/用法错误（[USE_ERROR]）"))
        self.install_hcloud(fake)
        code, _, err = self.run_main([])
        self.assertEqual(code, 1)
        self.assertIn("[USE_ERROR]", err)

    def test_credentials_message(self):
        fake = FakeHcloud(error=scm.ScmError(
            "credentials", "缺少或无效的华为云凭据（AK/SK）"))
        self.install_hcloud(fake)
        code, _, err = self.run_main([])
        self.assertEqual(code, 1)
        self.assertIn("AK/SK", err)

    def test_network_message(self):
        fake = FakeHcloud(error=scm.ScmError("network", "网络异常/超时"))
        self.install_hcloud(fake)
        code, _, err = self.run_main([])
        self.assertEqual(code, 1)
        self.assertIn("网络异常", err)

    def test_invalid_limit_rejected(self):
        self.install_hcloud(FakeHcloud([page([])]))
        for bad in ("0", "30", "200"):
            code, _, err = self.run_main(["--limit", bad])
            self.assertEqual(code, 1)
            self.assertIn("--limit", err)

    def test_invalid_expiring_rejected(self):
        code, _, err = self.run_main(["--expiring", "-1"])
        self.assertEqual(code, 1)
        self.assertIn("--expiring", err)

    def test_cli_missing_with_cli_backend(self):
        scm.hcloud_binary = lambda: None
        code, _, err = self.run_main(["--backend", "cli"])
        self.assertEqual(code, 1)
        self.assertIn("hcloud", err)


class TestReadOnlyGuard(Base):
    def setUp(self):
        Base.setUp(self)
        self.fake = FakeHcloud([page([CERT_A])])
        scm.run_hcloud = self.fake
        scm.hcloud_binary = lambda: "/usr/local/bin/hcloud"

    def test_action_delete_blocked(self):
        code, out, _ = self.run_main(["--action", "delete"])
        self.assertEqual(code, 1)
        self.assertIn("只读", out)
        self.assertEqual(self.fake.calls, [])

    def test_action_import_blocked(self):
        code, _, _ = self.run_main(["--action", "import"])
        self.assertEqual(code, 1)
        self.assertEqual(self.fake.calls, [])

    def test_action_push_blocked(self):
        code, _, _ = self.run_main(["--action", "push"])
        self.assertEqual(code, 1)
        self.assertEqual(self.fake.calls, [])

    def test_action_create_blocked(self):
        code, _, _ = self.run_main(["--action", "create"])
        self.assertEqual(code, 1)
        self.assertEqual(self.fake.calls, [])

    def test_content_write_intent_blocked(self):
        code, out, _ = self.run_main(["--content", "delete"])
        self.assertEqual(code, 1)
        self.assertIn("只读", out)
        self.assertEqual(self.fake.calls, [])

    def test_action_list_allowed(self):
        code, _, _ = self.run_main(["--action", "list"])
        self.assertEqual(code, 0)
        self.assertNotEqual(self.fake.calls, [])

    def test_guard_unit(self):
        self.assertIsNotNone(scm.guard_write_intent("delete"))
        self.assertIsNotNone(scm.guard_write_intent("import"))
        self.assertIsNotNone(scm.guard_write_intent("list", "push"))
        self.assertIsNone(scm.guard_write_intent("list", "update.example.com"))
        self.assertIsNone(scm.guard_write_intent("list", "prod-web"))

    def test_only_readonly_operations_declared(self):
        self.assertEqual(set(scm.READONLY_OPERATIONS), {"ListCertificates"})


class TestSdkFallback(Base):
    def install_sdk(self, pages):
        client = FakeSdkClient(pages)
        scm.sdk_client = lambda region: client
        return client

    def test_sdk_backend(self):
        client = self.install_sdk([page([CERT_A, CERT_B])])
        code, out, _ = self.run_main(["--backend", "sdk", "--region", "cn-north-4"])
        self.assertEqual(code, 0)
        self.assertIn("prod-web", out)
        self.assertIn("共 2 个证书", out)
        self.assertIn("sdk", out)
        self.assertEqual(len(client.requests), 1)
        self.assertEqual(client.requests[0].limit, 50)

    def test_sdk_pagination(self):
        client = self.install_sdk([
            page(many(10), total=11),
            page(many(1, "d"), total=11),
        ])
        code, out, _ = self.run_main(["--backend", "sdk", "--limit", "10"])
        self.assertEqual(code, 0)
        self.assertIn("共 11 个证书", out)
        self.assertEqual(len(client.requests), 2)
        self.assertEqual(client.requests[1].offset, 10)

    def test_auto_falls_back_when_cli_fails(self):
        fake = FakeHcloud(error=scm.ScmError("cli_error", "hcloud blew up"))
        self.install_hcloud(fake)
        self.install_sdk([page([CERT_A])])
        code, out, err = self.run_main([])
        self.assertEqual(code, 0)
        self.assertIn("回退 SDK", err)
        self.assertIn("prod-web", out)
        self.assertIn("sdk", out)

    def test_auto_does_not_fall_back_on_403(self):
        fake = FakeHcloud(error=scm.classify_cli_error("ERROR: 403", 1))
        self.install_hcloud(fake)
        self.install_sdk([page([CERT_A])])
        code, _, err = self.run_main([])
        self.assertEqual(code, 1)
        self.assertIn("scm:cert:list", err)

    def test_auto_falls_back_when_cli_missing(self):
        scm.hcloud_binary = lambda: None
        self.install_sdk([page([CERT_A])])
        code, out, _ = self.run_main([])
        self.assertEqual(code, 0)
        self.assertIn("prod-web", out)

    def test_sdk_missing_credentials(self):
        scm.sdk_client = lambda region: scm.env_credentials()
        code, _, err = self.run_main(["--backend", "sdk"])
        self.assertEqual(code, 1)
        self.assertIn("HUAWEICLOUD_SDK_AK", err)

    def test_env_credentials_missing(self):
        with self.assertRaises(scm.ScmError) as ctx:
            scm.env_credentials()
        self.assertEqual(ctx.exception.kind, "credentials")


class TestSdkClientContract(Base):
    """Contract test against the real SDK client (never the injected fake).

    SCM is a global service: ``ScmClient.new_builder()`` only accepts
    ``GlobalCredentials``. Building with ``BasicCredentials`` fails before any
    request with "credential type error, supported credential type is
    GlobalCredentials", which used to break every real SDK fallback.
    """

    def setUp(self):
        if not SDK_INSTALLED:
            self.skipTest("huaweicloudsdkcore/huaweicloudsdkscm 未安装，跳过真实客户端契约测试")
        Base.setUp(self)
        os.environ["HUAWEICLOUD_SDK_AK"] = "test-ak"
        os.environ["HUAWEICLOUD_SDK_SK"] = "test-sk"
        os.environ["HUAWEICLOUD_SDK_DOMAIN_ID"] = "test-domain-id"

    def test_sdk_client_uses_global_credentials(self):
        client = scm.sdk_client("cn-north-4")
        credentials = client.get_credentials()
        self.assertIsInstance(credentials, GlobalCredentials)
        self.assertNotIsInstance(credentials, BasicCredentials)
        self.assertEqual(credentials.ak, "test-ak")
        self.assertEqual(credentials.sk, "test-sk")
        self.assertEqual(credentials.domain_id, "test-domain-id")
        self.assertEqual(client._endpoints,
                         ["https://scm.cn-north-4.myhuaweicloud.com"])

    def test_real_builder_rejects_basic_credentials(self):
        with self.assertRaises(TypeError):
            (ScmClient.new_builder()
             .with_credentials(BasicCredentials("test-ak", "test-sk"))
             .build())


class TestSubprocessIntegration(Base):
    """Exercise the real subprocess path through a mock hcloud executable."""

    def setUp(self):
        Base.setUp(self)
        self.tmp = tempfile.mkdtemp(prefix="scm-mock-")
        self.bin = os.path.join(self.tmp, "hcloud")
        self.payload = page([CERT_A])
        with open(self.bin, "w", encoding="utf-8") as handle:
            handle.write(
                "#!/usr/bin/env python3\n"
                "import json, sys\n"
                "print(json.dumps({0!r}))\n".format(self.payload)
            )
        os.chmod(self.bin, os.stat(self.bin).st_mode | stat.S_IEXEC)
        os.environ["HUAWEI_CLOUD_SCM_CERT_LIST_HCLOUD_BIN"] = self.bin
        scm.run_hcloud = self._run_hcloud
        scm.hcloud_binary = self._hcloud_binary

    def test_mock_binary_end_to_end(self):
        code, out, _ = self.run_main(["--table", "--region", "cn-north-4"])
        self.assertEqual(code, 0)
        self.assertIn("prod-web", out)
        self.assertIn("共 1 个证书", out)

    def test_mock_binary_json(self):
        code, out, _ = self.run_main(["--json"])
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertEqual(data["total_count"], 1)

    def test_env_override_used_as_binary(self):
        self.assertEqual(scm.hcloud_binary(), self.bin)


class TestSubprocessErrorPayload(Base):
    """KooCLI exits 0 even when the API returns an error body."""

    def setUp(self):
        Base.setUp(self)
        self.tmp = tempfile.mkdtemp(prefix="scm-mock-err-")
        self.bin = os.path.join(self.tmp, "hcloud")
        self.payload = {
            "error_code": "SCM.4002",
            "error_msg": "Permission denied. Policy does not allow action to be "
                         "performed ... not authorized to perform: scm:cert:list",
        }
        with open(self.bin, "w", encoding="utf-8") as handle:
            handle.write(
                "#!/usr/bin/env python3\n"
                "import json, sys\n"
                "print(json.dumps({0!r}))\n"
                "sys.exit(0)\n".format(self.payload)
            )
        os.chmod(self.bin, os.stat(self.bin).st_mode | stat.S_IEXEC)
        os.environ["HUAWEI_CLOUD_SCM_CERT_LIST_HCLOUD_BIN"] = self.bin
        scm.run_hcloud = self._run_hcloud
        scm.hcloud_binary = self._hcloud_binary

    def test_error_payload_is_not_an_empty_list(self):
        code, out, err = self.run_main(["--region", "cn-north-4"])
        self.assertEqual(code, 1)
        self.assertNotIn("未找到 SSL 证书", out)
        self.assertIn("scm:cert:list", err)
        self.assertNotIn("Traceback", err)

    def test_error_payload_does_not_fall_back_to_sdk(self):
        scm.sdk_client = lambda region: self.fail("SDK must not be used on 403")
        code, _, err = self.run_main([])
        self.assertEqual(code, 1)
        self.assertIn("scm:cert:list", err)


class TestHelpers(unittest.TestCase):
    def test_format_time_parses_space_format(self):
        self.assertEqual(scm.format_time("2026-12-31 08:00:00"),
                         "2026-12-31 08:00:00")

    def test_format_time_parses_iso_z(self):
        self.assertEqual(scm.format_time("2026-12-31T08:00:00Z"),
                         "2026-12-31 08:00:00")

    def test_format_time_epoch_ms(self):
        self.assertEqual(scm.format_time("1700000000000"),
                         "2023-11-14 22:13:20")

    def test_format_time_empty(self):
        self.assertEqual(scm.format_time(""), "")
        self.assertEqual(scm.format_time(None), "")

    def test_days_left_future(self):
        value = scm.days_left(iso_in(10, hours=1))
        self.assertIn(value, (9, 10))

    def test_days_left_expired_negative(self):
        value = scm.days_left(iso_in(-3, hours=-1))
        self.assertLess(value, 0)

    def test_days_left_empty(self):
        self.assertIsNone(scm.days_left(""))

    def test_type_family(self):
        self.assertEqual(scm.type_family("DV_SSL_CERT"), "DV")
        self.assertEqual(scm.type_family("OV_SSL_CERT_PRO"), "OV")
        self.assertEqual(scm.type_family("EV_SSL_CERT_PRO"), "EV")
        self.assertEqual(scm.type_family(""), "-")

    def test_cert_source(self):
        self.assertEqual(scm.cert_source(CERT_A), "SCM签发")
        self.assertEqual(scm.cert_source(CERT_B), "上传托管")
        self.assertEqual(scm.cert_source({"status": "REVOKED"}), "-")

    def test_normalize_certificates(self):
        certs = scm.normalize_certificates([page([CERT_A])])
        self.assertEqual(certs[0]["name"], "prod-web")
        self.assertEqual(certs[0]["type"], "OV")
        self.assertEqual(certs[0]["domain"], "www.example.com")
        self.assertIsNotNone(certs[0]["days_left"])

    def test_merge_pages(self):
        merged = scm.merge_pages([page([CERT_A], total=1)], "cn-north-4")
        self.assertEqual(merged["total_count"], 1)
        self.assertEqual(merged["region"], "cn-north-4")


if __name__ == "__main__":
    unittest.main()