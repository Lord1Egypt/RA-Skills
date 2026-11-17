import json
import os
import sys
import types
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from list_cbr_vaults import (  # noqa: E402
    ALLOWED_OPERATION,
    ApiError,
    AuthError,
    CbrVaultListError,
    ConfigError,
    GuardError,
    active_filter_descriptions,
    build_command,
    classify_hcloud_failure,
    classify_payload_error,
    extract_json,
    extract_vaults,
    filter_vaults,
    guard_operation,
    guard_text_from_argv,
    guard_write_intent,
    list_vaults,
    list_vaults_via_sdk,
    main,
    normalize_vault,
    render_table,
    sdk_vault_to_dict,
    vault_summary_lines,
)

CLI_OUTPUT = json.dumps({
    "vaults": [
        {
            "id": "vault-1111",
            "name": "vault-alpha",
            "project_id": "proj-1",
            "enterprise_project_id": "0",
            "created_at": "2026-01-01T00:00:00Z",
            "billing": {
                "status": "available",
                "size": 100,
                "used": 20,
                "allocated": 80,
                "charging_mode": "pre_paid",
                "object_type": "server",
                "protect_type": "backup",
                "spec_code": "vault.backup.server.normal",
                "cloud_type": "public",
                "storage_unit": "unit-1",
            },
        },
        {
            "id": "vault-2222",
            "name": "vault-beta",
            "project_id": "proj-1",
            "enterprise_project_id": "0",
            "created_at": "2026-01-02T00:00:00Z",
            "billing": {
                "status": "error",
                "size": 200,
                "used": 0,
                "allocated": 0,
                "charging_mode": "post_paid",
                "object_type": "disk",
                "protect_type": "replication",
                "spec_code": "vault.replication.server.normal",
                "cloud_type": "public",
                "storage_unit": "unit-2",
            },
        },
    ],
    "count": 2,
    "offset": 0,
    "limit": 100,
})

CLI_OUTPUT_EMPTY = json.dumps({"vaults": [], "count": 0, "offset": 0, "limit": 100})


def hcloud_result(stdout="", stderr="", returncode=0):
    return (stdout, stderr, returncode)


class FakeRunner:
    """subprocess.run fake returning canned hcloud outputs per call."""

    def __init__(self, outputs):
        self.outputs = list(outputs)
        self.calls = []

    def __call__(self, cmd, **kwargs):
        self.calls.append(cmd)
        if not self.outputs:
            raise AssertionError("unexpected extra hcloud call: %r" % (cmd,))
        return self.outputs.pop(0)


class GuardTests(unittest.TestCase):
    def test_read_operation_passes(self):
        self.assertFalse(guard_write_intent("--region cn-north-4 --status available"))
        self.assertTrue(guard_operation(ALLOWED_OPERATION))

    def test_mutating_intents_blocked(self):
        for intent in ("create", "delete", "update", "restore", "copy",
                       "import", "replicate", "migrate", "associate",
                       "bind", "remove", "add"):
            with self.assertRaises(GuardError):
                guard_write_intent("--%s-vault" % intent)

    def test_cbr_operation_names_blocked(self):
        for name in ("CreateVault", "DeleteVault", "UpdateVault",
                     "BatchUpdateVault", "AddVaultResource",
                     "RemoveVaultResource", "MigrateVaultResource",
                     "AssociateVaultPolicy", "ChangeVaultChargeMode"):
            with self.assertRaises(GuardError):
                guard_write_intent(name)

    def test_operation_whitelist(self):
        with self.assertRaises(GuardError):
            guard_operation("ListVaults")
        with self.assertRaises(GuardError):
            guard_operation("ShowVault")
        self.assertTrue(guard_operation("ListVault"))

    def test_list_vault_not_blocked(self):
        self.assertFalse(guard_write_intent("CBR ListVault --cli-region=cn-north-4"))

    def test_filter_values_not_blocked(self):
        # A vault literally named "delete-me" must not trip the guard.
        argv = ["--name", "delete-me", "--status", "available"]
        self.assertFalse(guard_write_intent(guard_text_from_argv(argv)))

    def test_vault_id_and_offset_not_blocked(self):
        argv = ["--vault-id=delete-me", "--offset", "20"]
        self.assertFalse(guard_write_intent(guard_text_from_argv(argv)))

    def test_operation_value_scanned(self):
        argv = ["--operation", "DeleteVault"]
        self.assertRaises(GuardError, guard_write_intent, guard_text_from_argv(argv))


class BuildCommandTests(unittest.TestCase):
    def test_base_command(self):
        argv = build_command("cn-north-4", limit=50, offset=10)
        self.assertEqual(argv[:5], ["CBR", "ListVault",
                                    "--cli-region=cn-north-4",
                                    "--limit=50", "--offset=10"])

    def test_native_filters_use_underscore_form(self):
        filters = {
            "name": "vault-prod",
            "status": "available",
            "object_type": "server",
            "protect_type": "backup",
            "enterprise_project_id": "0",
        }
        argv = build_command("cn-north-4", filters=filters, limit=10, offset=0)
        joined = " ".join(argv)
        self.assertIn("--name=vault-prod", joined)
        self.assertIn("--status=available", joined)
        self.assertIn("--object_type=server", joined)
        self.assertIn("--protect_type=backup", joined)
        self.assertIn("--enterprise_project_id=0", joined)

    def test_vault_id_uses_array_form(self):
        argv = build_command("cn-north-4", filters={"vault_id": "vault-1"},
                             limit=10, offset=0)
        self.assertIn("--id.1=vault-1", argv)
        self.assertNotIn("--vault_id", " ".join(argv))

    def test_no_write_flags(self):
        joined = " ".join(build_command("cn-north-4"))
        for flag in ("create", "delete", "update", "restore", "copy"):
            self.assertNotIn(flag, joined.lower())


class JsonTests(unittest.TestCase):
    def test_extract_json_plain(self):
        self.assertEqual(extract_json('{"a": 1}'), {"a": 1})

    def test_extract_json_wrapped(self):
        self.assertEqual(extract_json('noise\n{"a": 1}\nnoise'), {"a": 1})

    def test_extract_json_list(self):
        self.assertEqual(extract_json('noise [1, 2] noise'), [1, 2])

    def test_extract_json_invalid(self):
        with self.assertRaises(ApiError):
            extract_json("not-json")

    def test_extract_vaults_variants(self):
        self.assertEqual(len(extract_vaults({"vaults": [1]})), 1)
        self.assertEqual(len(extract_vaults({"vault_list": [1, 2]})), 2)
        self.assertEqual(extract_vaults([3, 4]), [3, 4])
        self.assertEqual(extract_vaults({"other": []}), [])


class FailureClassificationTests(unittest.TestCase):
    def test_use_error(self):
        err = classify_hcloud_failure(
            "[USE_ERROR]Operation ListVaults is not supported.", "", 0)
        self.assertIsInstance(err, ApiError)
        self.assertIn("参数错误", str(err))

    def test_missing_credentials(self):
        err = classify_hcloud_failure("", "please configure cli-ak first", 1)
        self.assertIsInstance(err, ConfigError)

    def test_403(self):
        err = classify_hcloud_failure(
            "", "403 Forbidden: not authorized to perform cbr:vaults:list", 1)
        self.assertIsInstance(err, AuthError)

    def test_generic_api_error(self):
        err = classify_hcloud_failure("boom", "network down", 2)
        self.assertIsInstance(err, ApiError)

    def test_payload_error_403(self):
        err = classify_payload_error(
            "BackupService.0403",
            "not authorized to perform: cbr:vaults:list")
        self.assertIsInstance(err, AuthError)
        self.assertIn("IAM", str(err))

    def test_payload_error_generic(self):
        err = classify_payload_error("BackupService.0500", "internal error")
        self.assertIsInstance(err, ApiError)


class PagingTests(unittest.TestCase):
    def test_paging_by_count(self):
        page1 = json.dumps({"vaults": [{"id": "v1"}, {"id": "v2"}],
                            "count": 3, "limit": 2, "offset": 0})
        page2 = json.dumps({"vaults": [{"id": "v3"}],
                            "count": 3, "limit": 2, "offset": 2})
        runner = FakeRunner([hcloud_result(page1), hcloud_result(page2)])
        with mock.patch("list_cbr_vaults.run_hcloud", runner):
            vaults = list_vaults("cn-north-4", limit=2)
        self.assertEqual([v["id"] for v in vaults], ["v1", "v2", "v3"])
        self.assertEqual(len(runner.calls), 2)
        self.assertIn("--offset=0", runner.calls[0])
        self.assertIn("--offset=2", runner.calls[1])

    def test_stops_on_short_page_without_count(self):
        page1 = json.dumps({"vaults": [{"id": "v1"}]})
        runner = FakeRunner([hcloud_result(page1)])
        with mock.patch("list_cbr_vaults.run_hcloud", runner):
            vaults = list_vaults("cn-north-4", limit=10)
        self.assertEqual(len(vaults), 1)
        self.assertEqual(len(runner.calls), 1)

    def test_deduplicates_repeated_ids(self):
        page1 = json.dumps({"vaults": [{"id": "v1"}], "count": 5, "limit": 1,
                            "offset": 0})
        page2 = json.dumps({"vaults": [{"id": "v1"}], "count": 5, "limit": 1,
                            "offset": 1})
        runner = FakeRunner([hcloud_result(page1), hcloud_result(page2)])
        with mock.patch("list_cbr_vaults.run_hcloud", runner):
            vaults = list_vaults("cn-north-4", limit=1)
        self.assertEqual([v["id"] for v in vaults], ["v1"])

    def test_payload_error_raised_from_cli(self):
        error = json.dumps({"error_code": "BackupService.0403",
                            "error_msg": "not authorized to perform cbr:vaults:list"})
        runner = FakeRunner([hcloud_result(error)])
        with mock.patch("list_cbr_vaults.run_hcloud", runner):
            with self.assertRaises(AuthError):
                list_vaults("cn-north-4")


class SdkFallbackTests(unittest.TestCase):
    def test_fallback_when_hcloud_missing(self):
        def missing(*_a, **_k):
            raise ConfigError("hcloud missing")
        with mock.patch("list_cbr_vaults.run_hcloud", side_effect=missing), \
                mock.patch("list_cbr_vaults.list_vaults_via_sdk",
                           return_value=[{"id": "v1"}]) as sdk:
            vaults = list_vaults("cn-north-4")
        self.assertEqual(vaults, [{"id": "v1"}])
        sdk.assert_called_once()

    def test_sdk_unavailable(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ConfigError):
                list_vaults_via_sdk("cn-north-4")

    def test_sdk_request_construction(self):
        captured = {}

        class FakeRequest:
            def __init__(self, **kwargs):
                captured.update(kwargs)

        class FakeResponse:
            def __init__(self):
                self.vaults = [{"id": "v1", "name": "n1"}]
                self.count = 1

        class FakeClient:
            def list_vault(self, request):
                return FakeResponse()

        core = types.ModuleType("huaweicloudsdkcore")
        auth = types.ModuleType("huaweicloudsdkcore.auth")
        credentials_mod = types.ModuleType("huaweicloudsdkcore.auth.credentials")
        credentials_mod.BasicCredentials = lambda **kw: ("creds", kw)
        region_mod = types.ModuleType("huaweicloudsdkcore.region.region")
        region_mod.Region = lambda rid, endpoint: ("region", rid)
        http_mod = types.ModuleType("huaweicloudsdkcore.http.http_config")
        http_mod.HttpConfig = mock.Mock()
        http_mod.HttpConfig.get_default_config = lambda: "httpcfg"
        cbr = types.ModuleType("huaweicloudsdkcbr")
        cbr_v1 = types.ModuleType("huaweicloudsdkcbr.v1")
        cbr_v1.CbrClient = mock.Mock()
        cbr_v1.CbrClient.new_builder.return_value = (
            mock.Mock(with_credentials=mock.Mock(return_value=mock.Mock(
                with_region=mock.Mock(return_value=mock.Mock(
                    with_http_config=mock.Mock(return_value=mock.Mock(
                        build=mock.Mock(return_value=FakeClient())))))))))
        cbr_v1.ListVaultRequest = FakeRequest
        cbr_region = types.ModuleType("huaweicloudsdkcbr.v1.region")
        cbr_region_mod = types.ModuleType("huaweicloudsdkcbr.v1.region.cbr_region")
        cbr_region_mod.CbrRegion = mock.Mock()
        cbr_region_mod.CbrRegion.value_of = lambda region: ("region", region)
        cbr_region.cbr_region = cbr_region_mod

        modules = {
            "huaweicloudsdkcore": core,
            "huaweicloudsdkcore.auth": auth,
            "huaweicloudsdkcore.auth.credentials": credentials_mod,
            "huaweicloudsdkcore.region": types.ModuleType("huaweicloudsdkcore.region"),
            "huaweicloudsdkcore.region.region": region_mod,
            "huaweicloudsdkcore.http": types.ModuleType("huaweicloudsdkcore.http"),
            "huaweicloudsdkcore.http.http_config": http_mod,
            "huaweicloudsdkcbr": cbr,
            "huaweicloudsdkcbr.v1": cbr_v1,
            "huaweicloudsdkcbr.v1.region": cbr_region,
            "huaweicloudsdkcbr.v1.region.cbr_region": cbr_region_mod,
        }
        with mock.patch.dict(sys.modules, modules), \
                mock.patch.dict(os.environ,
                                {"HUAWEI_ACCESS_KEY": "ak-value",
                                 "HUAWEI_SECRET_KEY": "sk-value"}, clear=False):
            vaults = list_vaults_via_sdk(
                "cn-north-4",
                filters={"status": "available", "vault_id": "vault-1"},
                limit=5)
        self.assertEqual(vaults, [{"id": "v1", "name": "n1"}])
        self.assertEqual(captured["limit"], 5)
        self.assertEqual(captured["offset"], 0)
        self.assertEqual(captured["status"], "available")
        self.assertEqual(captured["id"], ["vault-1"])

    def test_vault_remap_with_billing(self):
        class FakeBilling:
            def to_dict(self):
                return {"status": "available", "size": 100,
                        "charging_mode": "pre_paid"}

        class FakeVault:
            def __init__(self):
                self._values = {"id": "v1", "name": "n1", "billing": FakeBilling()}

            def to_dict(self):
                return dict(self._values)

        record = sdk_vault_to_dict(FakeVault())
        self.assertEqual(record["id"], "v1")
        self.assertEqual(record["billing"]["status"], "available")
        self.assertEqual(record["billing"]["charging_mode"], "pre_paid")


class FilterTests(unittest.TestCase):
    def setUp(self):
        self.vaults = extract_vaults(json.loads(CLI_OUTPUT))

    def test_name_substring(self):
        result = filter_vaults(self.vaults, name="alpha")
        self.assertEqual([v["id"] for v in result], ["vault-1111"])

    def test_status_from_billing(self):
        result = filter_vaults(self.vaults, status="available")
        self.assertEqual([v["id"] for v in result], ["vault-1111"])

    def test_object_type(self):
        result = filter_vaults(self.vaults, object_type="disk")
        self.assertEqual([v["id"] for v in result], ["vault-2222"])

    def test_protect_type(self):
        result = filter_vaults(self.vaults, protect_type="replication")
        self.assertEqual([v["id"] for v in result], ["vault-2222"])

    def test_enterprise_project_id(self):
        result = filter_vaults(self.vaults, enterprise_project_id="0")
        self.assertEqual(len(result), 2)

    def test_vault_id(self):
        result = filter_vaults(self.vaults, vault_id="vault-1111")
        self.assertEqual([v["id"] for v in result], ["vault-1111"])


class RenderingTests(unittest.TestCase):
    def setUp(self):
        self.vaults = extract_vaults(json.loads(CLI_OUTPUT))

    def test_normalize_flattens_billing(self):
        flat = normalize_vault(self.vaults[0])
        self.assertEqual(flat["status"], "available")
        self.assertEqual(flat["size"], 100)
        self.assertEqual(flat["charging_mode"], "pre_paid")
        self.assertEqual(flat["object_type"], "server")

    def test_table_preferred_columns(self):
        table = render_table(self.vaults)
        header = table.splitlines()[0]
        for column in ("name", "id", "status", "size", "charging_mode"):
            self.assertIn(column, header)

    def test_table_missing_field_dash(self):
        table = render_table([{"id": "v1"}])
        self.assertIn("v1", table)
        self.assertIn("-", table)

    def test_summary_lines(self):
        lines = vault_summary_lines(self.vaults)
        self.assertIn("vault-alpha", lines[0])
        self.assertIn("vault-1111", lines[0])
        self.assertIn("pre_paid", lines[0])

    def test_active_filters(self):
        filters = active_filter_descriptions(name="a", status="available")
        self.assertEqual(filters, ["name=a", "status=available"])


class MainTests(unittest.TestCase):
    def _run(self, argv, vaults):
        import io
        from contextlib import redirect_stdout, redirect_stderr
        with mock.patch("list_cbr_vaults.list_vaults", return_value=vaults):
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                rc = main(argv)
            return rc, out.getvalue(), err.getvalue()

    def test_default_table(self):
        rc, out, _ = self._run(["--region", "cn-north-4"],
                               extract_vaults(json.loads(CLI_OUTPUT)))
        self.assertEqual(rc, 0)
        self.assertIn("CBR 存储库列表", out)
        self.assertIn("vault-alpha", out)
        self.assertIn("charging_mode", out)

    def test_json_mode(self):
        rc, out, _ = self._run(["--json"],
                               extract_vaults(json.loads(CLI_OUTPUT)))
        payload = json.loads(out)
        self.assertEqual(len(payload), 2)
        self.assertEqual(payload[0]["id"], "vault-1111")

    def test_names_only(self):
        rc, out, _ = self._run(["--names-only"],
                               extract_vaults(json.loads(CLI_OUTPUT)))
        self.assertIn("CBR 存储库清单", out)
        self.assertIn("vault-alpha", out)

    def test_empty(self):
        rc, out, _ = self._run([], [])
        self.assertEqual(rc, 0)
        self.assertIn("无 CBR 存储库", out)

    def test_empty_with_filter_suffix(self):
        rc, out, _ = self._run(["--status", "available"], [])
        self.assertIn("过滤条件", out)

    def test_error_path(self):
        with mock.patch("list_cbr_vaults.list_vaults",
                        side_effect=AuthError("no permission")):
            import io
            from contextlib import redirect_stderr
            err = io.StringIO()
            with redirect_stderr(err):
                rc = main(["--json"])
        self.assertEqual(rc, 1)
        self.assertIn("no permission", err.getvalue())

    def test_guard_path(self):
        import io
        from contextlib import redirect_stderr
        err = io.StringIO()
        with redirect_stderr(err):
            rc = main(["--delete-vault"])
        self.assertEqual(rc, 1)
        self.assertIn("守卫", err.getvalue())


if __name__ == "__main__":
    unittest.main()