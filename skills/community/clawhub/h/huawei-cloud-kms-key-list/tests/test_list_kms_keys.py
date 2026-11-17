#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Offline unit tests for huawei-cloud-kms-key-list.

No credentials and no network are used: the KooCLI subprocess is mocked with a
fake runner (and, for one integration case, a real mock executable injected via
``HUAWEI_CLOUD_KMS_KEY_LIST_HCLOUD_BIN``); the SDK fallback is driven by a fake
client injected through ``sdk_client``.

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

HERE = pathlib.Path(__file__).resolve().parent
MOD_PATH = HERE.parent / "scripts" / "list_kms_keys.py"

_spec = importlib.util.spec_from_file_location("list_kms_keys", MOD_PATH)
kms = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(kms)


KEY_A = {
    "key_id": "0d0466b0-e727-4d9c-b35d-f84bb474a37f",
    "key_alias": "prod-db",
    "key_state": "2",
    "key_usage": "ENCRYPT_DECRYPT",
    "key_spec": "AES_256",
    "key_type": "1",
    "key_rotation_enabled": "true",
    "creation_date": "1502799822000",
}
KEY_B = {
    "key_id": "2e258389-bb1e-4568-a1d5-e1f50adf70ea",
    "key_alias": "dev-sign",
    "key_state": "3",
    "key_usage": "SIGN_VERIFY",
    "key_spec": "RSA_2048",
    "key_type": "1",
    "key_rotation_enabled": "false",
    "creation_date": "1600000000000",
}


def page(details, total=None, truncated="false", next_marker=""):
    return {
        "keys": [d["key_id"] for d in details],
        "key_details": detail_copy(details),
        "total": len(details) if total is None else total,
        "truncated": truncated,
        "next_marker": next_marker,
    }


def detail_copy(details):
    return [dict(d) for d in details]


class FakeHcloud(object):
    """Replacement for ``list_kms_keys.run_hcloud``."""

    def __init__(self, pages=None, rotation=None, error=None, fail_op=None):
        self.pages = list(pages or [])
        self.rotation = dict(rotation or {})
        self.error = error
        self.fail_op = fail_op
        self.calls = []

    def __call__(self, args, timeout=None):
        self.calls.append(list(args))
        operation = args[1] if len(args) > 1 else ""
        if self.error is not None and (self.fail_op is None
                                       or operation == self.fail_op):
            raise self.error
        if operation == "ListKeys":
            index = len([c for c in self.calls if c[1] == "ListKeys"]) - 1
            if index < len(self.pages):
                return self.pages[index]
            return page([])
        if operation == "ShowKeyRotationStatus":
            key_id = ""
            for item in args:
                if str(item).startswith("--key_id="):
                    key_id = str(item).split("=", 1)[1]
            payload = self.rotation.get(key_id)
            if payload is None:
                raise kms.KmsError("forbidden", "no rotation permission")
            return payload
        raise AssertionError("unexpected operation: {0}".format(operation))

    def list_calls(self):
        return [c for c in self.calls if len(c) > 1 and c[1] == "ListKeys"]

    def marker_of(self, call):
        for item in call:
            if str(item).startswith("--marker="):
                return str(item).split("=", 1)[1]
        return None


class FakeSdkResponse(object):
    def __init__(self, data):
        self._data = data

    def to_dict(self):
        return dict(self._data)


class FakeSdkClient(object):
    def __init__(self, pages, rotation=None):
        self.pages = list(pages)
        self.rotation = dict(rotation or {})
        self.requests = []
        self.rotation_requests = []

    def list_keys(self, request):
        self.requests.append(request)
        index = len(self.requests) - 1
        data = dict(self.pages[index]) if index < len(self.pages) else page([])
        data["keys"] = [dict(d) if isinstance(d, dict) else d
                        for d in data.get("keys", [])]
        return FakeSdkResponse(data)


class Base(unittest.TestCase):
    def setUp(self):
        self._env = dict(os.environ)
        for name in kms.HCLOUD_BIN_ENV + ("HUAWEICLOUD_SDK_AK",
                                          "HUAWEICLOUD_SDK_SK",
                                          "HUAWEI_ACCESS_KEY",
                                          "HUAWEI_SECRET_KEY"):
            os.environ.pop(name, None)
        self._run_hcloud = kms.run_hcloud
        self._hcloud_binary = kms.hcloud_binary
        self._sdk_client = kms.sdk_client

    def tearDown(self):
        kms.run_hcloud = self._run_hcloud
        kms.hcloud_binary = self._hcloud_binary
        kms.sdk_client = self._sdk_client
        os.environ.clear()
        os.environ.update(self._env)

    def install_hcloud(self, fake):
        kms.run_hcloud = fake
        kms.hcloud_binary = lambda: "/usr/local/bin/hcloud"

    def run_main(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = kms.main(argv)
        return code, out.getvalue(), err.getvalue()


class TestOutputModes(Base):
    def test_default_compact_list(self):
        self.install_hcloud(FakeHcloud([page([KEY_A, KEY_B])]))
        code, out, _ = self.run_main(["--region", "cn-north-4"])
        self.assertEqual(code, 0)
        self.assertIn("别名", out)
        self.assertIn("密钥ID", out)
        self.assertIn("状态", out)
        self.assertNotIn("密钥用途", out)
        self.assertIn("prod-db", out)
        self.assertIn(KEY_A["key_id"], out)
        self.assertIn("启用(2)", out)
        self.assertIn("禁用(3)", out)
        self.assertIn("共 2 个密钥", out)
        self.assertIn("cn-north-4", out)

    def test_table_has_eight_columns(self):
        self.install_hcloud(FakeHcloud(
            [page([KEY_A, KEY_B])],
            rotation={KEY_A["key_id"]: {"key_rotation_enabled": True,
                                       "rotation_interval": 90}}))
        code, out, _ = self.run_main(["--table", "--region", "cn-north-4"])
        self.assertEqual(code, 0)
        for header in ("密钥ID", "别名", "状态", "密钥用途", "密钥类型",
                       "轮转周期", "创建时间", "region"):
            self.assertIn(header, out)
        self.assertIn("ENCRYPT_DECRYPT", out)
        self.assertIn("AES_256", out)
        self.assertIn("RSA_2048", out)
        self.assertIn("开启(90天)", out)
        self.assertIn("关闭", out)
        self.assertIn("2017-08-15", out)

    def test_table_no_rotation_detail_skips_lookups(self):
        fake = FakeHcloud([page([KEY_A])])
        self.install_hcloud(fake)
        code, out, _ = self.run_main(["--table", "--no-rotation-detail"])
        self.assertEqual(code, 0)
        self.assertIn("开启", out)
        self.assertNotIn("ShowKeyRotationStatus",
                         [c[1] for c in fake.calls])

    def test_table_rotation_failure_degrades(self):
        fake = FakeHcloud([page([KEY_A])], rotation={})
        self.install_hcloud(fake)
        code, out, _ = self.run_main(["--table"])
        self.assertEqual(code, 0)
        self.assertIn("开启", out)

    def test_json_raw_body(self):
        self.install_hcloud(FakeHcloud([page([KEY_A, KEY_B])]))
        code, out, _ = self.run_main(["--json", "--region", "cn-north-4"])
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertEqual(data["total"], 2)
        self.assertEqual(len(data["key_details"]), 2)
        self.assertEqual(len(data["keys"]), 2)
        self.assertEqual(data["region"], "cn-north-4")
        self.assertEqual(data["truncated"], "false")


class TestPagination(Base):
    def test_follows_next_marker(self):
        fake = FakeHcloud([
            page([KEY_A], total=2, truncated="true", next_marker="m1"),
            page([KEY_B], total=2),
        ])
        self.install_hcloud(fake)
        code, out, _ = self.run_main(["--region", "cn-north-4"])
        self.assertEqual(code, 0)
        self.assertIn("共 2 个密钥", out)
        calls = fake.list_calls()
        self.assertEqual(len(calls), 2)
        self.assertIsNone(fake.marker_of(calls[0]))
        self.assertEqual(fake.marker_of(calls[1]), "m1")
        self.assertTrue(any(str(a) == "--limit=100" for a in calls[0]))
        self.assertTrue(any(str(a) == "--key_spec=ALL" for a in calls[0]))

    def test_stops_without_marker(self):
        fake = FakeHcloud([
            page([KEY_A], truncated="true", next_marker=""),
        ])
        self.install_hcloud(fake)
        code, out, _ = self.run_main([])
        self.assertEqual(code, 0)
        self.assertEqual(len(fake.list_calls()), 1)

    def test_duplicate_key_deduped(self):
        fake = FakeHcloud([
            page([KEY_A], truncated="true", next_marker="m1"),
            page([KEY_A, KEY_B]),
        ])
        self.install_hcloud(fake)
        code, out, _ = self.run_main([])
        self.assertEqual(code, 0)
        self.assertIn("共 2 个密钥", out)

    def test_max_pages_cap(self):
        fake = FakeHcloud([
            page([KEY_A], truncated="true", next_marker="m1"),
            page([KEY_A], truncated="true", next_marker="m2"),
            page([KEY_A], truncated="true", next_marker="m3"),
        ])
        self.install_hcloud(fake)
        code, _, _ = self.run_main(["--max-pages", "2"])
        self.assertEqual(code, 0)
        self.assertEqual(len(fake.list_calls()), 2)


class TestFilters(Base):
    def setUp(self):
        Base.setUp(self)
        self.install_hcloud(FakeHcloud([page([KEY_A, KEY_B])]))

    def test_alias_exact(self):
        code, out, _ = self.run_main(["--alias", "prod-db"])
        self.assertEqual(code, 0)
        self.assertIn("prod-db", out)
        self.assertNotIn("dev-sign", out)

    def test_alias_exact_is_not_substring(self):
        code, out, _ = self.run_main(["--alias", "prod"])
        self.assertEqual(code, 0)
        self.assertIn("未找到匹配的 KMS 密钥", out)

    def test_alias_fuzzy(self):
        code, out, _ = self.run_main(["--alias", "prod", "--fuzzy"])
        self.assertEqual(code, 0)
        self.assertIn("prod-db", out)
        self.assertNotIn("dev-sign", out)

    def test_key_id_substring(self):
        code, out, _ = self.run_main(["--key-id", "2e258389"])
        self.assertEqual(code, 0)
        self.assertIn("dev-sign", out)
        self.assertNotIn("prod-db", out)

    def test_state_numeric(self):
        code, out, _ = self.run_main(["--state", "3"])
        self.assertEqual(code, 0)
        self.assertIn("dev-sign", out)
        self.assertNotIn("prod-db", out)

    def test_state_name(self):
        code, out, _ = self.run_main(["--state", "enabled"])
        self.assertEqual(code, 0)
        self.assertIn("prod-db", out)
        self.assertNotIn("dev-sign", out)

    def test_state_pending_deletion(self):
        key = dict(KEY_A, key_state="4", key_alias="doomed")
        self.install_hcloud(FakeHcloud([page([key])]))
        code, out, _ = self.run_main(["--state", "pending-deletion"])
        self.assertEqual(code, 0)
        self.assertIn("doomed", out)
        self.assertIn("计划删除", out)

    def test_invalid_state_rejected(self):
        code, _, err = self.run_main(["--state", "bogus"])
        self.assertEqual(code, 1)
        self.assertIn("--state", err)


class TestEmptyAndErrors(Base):
    def test_empty_list_hint(self):
        self.install_hcloud(FakeHcloud([page([])]))
        code, out, _ = self.run_main(["--region", "cn-north-4"])
        self.assertEqual(code, 0)
        self.assertIn("当前区域无 KMS 密钥", out)
        self.assertIn("cn-north-4", out)

    def test_forbidden_hint(self):
        fake = FakeHcloud(error=kms.classify_cli_error(
            "ERROR: KMS.0301 not authorized", 1))
        self.install_hcloud(fake)
        code, _, err = self.run_main(["--region", "cn-north-4"])
        self.assertEqual(code, 1)
        self.assertIn("kms:cmk:list", err)

    def test_use_error_hint(self):
        fake = FakeHcloud(error=kms.KmsError(
            "use_error", "KooCLI 参数/用法错误（[USE_ERROR]）"))
        self.install_hcloud(fake)
        code, _, err = self.run_main([])
        self.assertEqual(code, 1)
        self.assertIn("[USE_ERROR]", err)

    def test_classify_403(self):
        exc = kms.classify_cli_error("ERROR: KMS.0301 not authorized", 1)
        self.assertEqual(exc.kind, "forbidden")
        self.assertIn("kms:cmk:list", exc.message)

    def test_classify_use_error(self):
        exc = kms.classify_cli_error("[USE_ERROR]--limit invalid", 1)
        self.assertEqual(exc.kind, "use_error")

    def test_classify_credentials(self):
        exc = kms.classify_cli_error("ERROR: no credential found, "
                                     "please configure AK/SK", 1)
        self.assertEqual(exc.kind, "credentials")

    def test_limit_out_of_range(self):
        self.install_hcloud(FakeHcloud([page([])]))
        for bad in ("0", "201"):
            code, _, err = self.run_main(["--limit", bad])
            self.assertEqual(code, 1)
            self.assertIn("1~200", err)

    def test_cli_missing_with_cli_backend(self):
        kms.hcloud_binary = lambda: None
        code, _, err = self.run_main(["--backend", "cli"])
        self.assertEqual(code, 1)
        self.assertIn("hcloud", err)


class TestReadOnlyGuard(Base):
    def setUp(self):
        Base.setUp(self)
        self.fake = FakeHcloud([page([KEY_A])])
        kms.run_hcloud = self.fake
        kms.hcloud_binary = lambda: "/usr/local/bin/hcloud"

    def test_alias_write_intent(self):
        code, out, _ = self.run_main(["--alias", "create-me"])
        self.assertEqual(code, 1)
        self.assertIn("只读", out)
        self.assertEqual(self.fake.calls, [])

    def test_action_write_intent(self):
        code, out, _ = self.run_main(["--action", "rotate"])
        self.assertEqual(code, 1)
        self.assertIn("只读", out)
        self.assertEqual(self.fake.calls, [])

    def test_action_schedule_deletion(self):
        code, _, _ = self.run_main(["--action", "schedule-deletion"])
        self.assertEqual(code, 1)
        self.assertEqual(self.fake.calls, [])

    def test_key_id_write_intent(self):
        code, _, _ = self.run_main(["--key-id", "delete-0d0466b0"])
        self.assertEqual(code, 1)
        self.assertEqual(self.fake.calls, [])

    def test_action_list_allowed(self):
        code, _, _ = self.run_main(["--action", "list"])
        self.assertEqual(code, 0)
        self.assertNotEqual(self.fake.calls, [])

    def test_guard_unit(self):
        self.assertIsNotNone(kms.guard_write_intent("list", "create-me", None))
        self.assertIsNotNone(kms.guard_write_intent("rotate", None, None))
        self.assertIsNotNone(kms.guard_write_intent("list", None, "x-delete"))
        self.assertIsNone(kms.guard_write_intent("list", "prod-db", None))


class TestSdkFallback(Base):
    def install_sdk(self, pages, rotation=None):
        client = FakeSdkClient(pages, rotation)
        kms.sdk_client = lambda region: client
        return client

    def test_sdk_backend(self):
        client = self.install_sdk([page([KEY_A, KEY_B])])
        code, out, _ = self.run_main(["--backend", "sdk", "--region", "cn-north-4"])
        self.assertEqual(code, 0)
        self.assertIn("prod-db", out)
        self.assertIn("共 2 个密钥", out)
        self.assertIn("sdk", out)
        self.assertEqual(len(client.requests), 1)
        self.assertEqual(client.requests[0].limit, "100")
        self.assertEqual(client.requests[0].key_spec, "ALL")

    def test_sdk_pagination(self):
        client = self.install_sdk([
            page([KEY_A], truncated="true", next_marker="m1"),
            page([KEY_B]),
        ])
        code, out, _ = self.run_main(["--backend", "sdk"])
        self.assertEqual(code, 0)
        self.assertIn("共 2 个密钥", out)
        self.assertEqual(len(client.requests), 2)
        self.assertEqual(client.requests[1].marker, "m1")

    def test_auto_falls_back_when_cli_fails(self):
        fake = FakeHcloud(error=kms.KmsError("cli_error", "hcloud blew up"))
        self.install_hcloud(fake)
        self.install_sdk([page([KEY_A])])
        code, out, err = self.run_main([])
        self.assertEqual(code, 0)
        self.assertIn("回退 SDK", err)
        self.assertIn("prod-db", out)
        self.assertIn("sdk", out)

    def test_auto_does_not_fall_back_on_403(self):
        fake = FakeHcloud(error=kms.classify_cli_error(
            "ERROR: 403 not authorized", 1))
        self.install_hcloud(fake)
        self.install_sdk([page([KEY_A])])
        code, _, err = self.run_main([])
        self.assertEqual(code, 1)
        self.assertIn("kms:cmk:list", err)

    def test_auto_falls_back_when_cli_missing(self):
        kms.hcloud_binary = lambda: None
        self.install_sdk([page([KEY_A])])
        code, out, _ = self.run_main([])
        self.assertEqual(code, 0)
        self.assertIn("prod-db", out)

    def test_sdk_missing_credentials(self):
        kms.sdk_client = lambda region: kms.env_credentials()
        code, _, err = self.run_main(["--backend", "sdk"])
        self.assertEqual(code, 1)
        self.assertIn("HUAWEICLOUD_SDK_AK", err)

    def test_env_credentials_missing(self):
        with self.assertRaises(kms.KmsError) as ctx:
            kms.env_credentials()
        self.assertEqual(ctx.exception.kind, "credentials")

    def test_rotation_detail_via_sdk(self):
        client = self.install_sdk([page([KEY_A])])
        sdk_rotation = {"key_rotation_enabled": True, "rotation_interval": 180}
        client.show_key_rotation_status = lambda req: FakeSdkResponse(sdk_rotation)
        code, out, _ = self.run_main(["--backend", "sdk", "--table"])
        self.assertEqual(code, 0)
        self.assertIn("开启(180天)", out)


class TestSubprocessIntegration(Base):
    """Exercise the real subprocess path through a mock hcloud executable."""

    def setUp(self):
        Base.setUp(self)
        self.tmp = tempfile.mkdtemp(prefix="kms-mock-")
        self.bin = os.path.join(self.tmp, "hcloud")
        self.payload = {
            "keys": [KEY_A["key_id"]],
            "key_details": [detail_copy([KEY_A])[0]],
            "total": 1,
            "truncated": "false",
            "next_marker": "",
        }
        with open(self.bin, "w", encoding="utf-8") as handle:
            handle.write(
                "#!/usr/bin/env python3\n"
                "import json, sys\n"
                "payload = json.loads({0!r})\n"
                "if len(sys.argv) > 2 and sys.argv[2] == 'ShowKeyRotationStatus':\n"
                "    print(json.dumps({{'key_rotation_enabled': True, "
                "'rotation_interval': 30}}))\n"
                "else:\n"
                "    print(json.dumps(payload))\n".format(json.dumps(self.payload))
            )
        os.chmod(self.bin, os.stat(self.bin).st_mode | stat.S_IEXEC)
        os.environ["HUAWEI_CLOUD_KMS_KEY_LIST_HCLOUD_BIN"] = self.bin
        kms.run_hcloud = self._run_hcloud
        kms.hcloud_binary = self._hcloud_binary

    def test_mock_binary_end_to_end(self):
        code, out, _ = self.run_main(["--table", "--region", "cn-north-4"])
        self.assertEqual(code, 0)
        self.assertIn("prod-db", out)
        self.assertIn("开启(30天)", out)
        self.assertIn("共 1 个密钥", out)

    def test_mock_binary_json(self):
        code, out, _ = self.run_main(["--json"])
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertEqual(data["total"], 1)

    def test_env_override_used_as_binary(self):
        self.assertEqual(kms.hcloud_binary(), self.bin)


class TestHelpers(unittest.TestCase):
    def test_format_timestamp_ms(self):
        self.assertEqual(kms.format_timestamp("1502799822000"),
                         "2017-08-15 12:23:42")

    def test_format_timestamp_seconds(self):
        self.assertEqual(kms.format_timestamp("1502799822"),
                         "2017-08-15 12:23:42")

    def test_format_timestamp_empty(self):
        self.assertEqual(kms.format_timestamp(""), "")
        self.assertEqual(kms.format_timestamp(None), "")

    def test_format_timestamp_passthrough(self):
        self.assertEqual(kms.format_timestamp("2024-01-01T00:00:00Z"),
                         "2024-01-01T00:00:00Z")

    def test_normalize_state(self):
        self.assertEqual(kms.normalize_state("2"), "2")
        self.assertEqual(kms.normalize_state("enabled"), "2")
        self.assertEqual(kms.normalize_state("PENDING-DELETION"), "4")
        self.assertIsNone(kms.normalize_state("nope"))

    def test_normalize_keys_falls_back_to_ids(self):
        keys = kms.normalize_keys([{"keys": ["a", "b"], "key_details": []}])
        self.assertEqual([k["key_id"] for k in keys], ["a", "b"])

    def test_normalize_keys_prefers_details(self):
        keys = kms.normalize_keys([page([KEY_A])])
        self.assertEqual(keys[0]["key_alias"], "prod-db")
        self.assertIs(keys[0]["key_rotation_enabled"], True)

    def test_only_readonly_operations_declared(self):
        self.assertEqual(set(kms.READONLY_OPERATIONS),
                         {"ListKeys", "ShowKeyRotationStatus"})


if __name__ == "__main__":
    unittest.main()