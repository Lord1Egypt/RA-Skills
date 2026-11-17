import json
import os
import subprocess
import sys
import types
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from list_cbr_backups import (  # noqa: E402
    ALLOWED_OPERATION,
    ApiError,
    AuthError,
    CbrListError,
    ConfigError,
    GuardError,
    active_filter_descriptions,
    backup_names,
    backup_summary_lines,
    build_command,
    classify_hcloud_failure,
    extract_backups,
    extract_json,
    filter_backups,
    guard_operation,
    guard_text_from_argv,
    guard_write_intent,
    list_backups,
    list_backups_via_sdk,
    main,
    normalize_backup,
    render_table,
    sdk_backup_to_dict,
)

CLI_OUTPUT = json.dumps({
    "backups": [
        {
            "id": "b-1111",
            "name": "backup-alpha",
            "status": "available",
            "resource_id": "res-1111",
            "resource_name": "ecs-alpha",
            "resource_type": "OS::Nova::Server",
            "resource_size": 40,
            "vault_id": "vault-1",
            "image_type": "backup",
            "created_at": "2026-01-01T00:00:00Z",
        },
        {
            "id": "b-2222",
            "name": "backup-beta",
            "status": "error",
            "resource_id": "res-2222",
            "resource_name": "evs-beta",
            "resource_type": "OS::Cinder::Volume",
            "resource_size": 100,
            "vault_id": "vault-2",
            "image_type": "backup",
            "created_at": "2026-01-02T00:00:00Z",
        },
    ],
    "count": 2,
    "offset": 0,
    "limit": 1000,
})

CLI_OUTPUT_EMPTY = json.dumps({"backups": [], "count": 0, "offset": 0, "limit": 1000})


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
        self.assertFalse(guard_write_intent("--region cn-north-4 --json"))
        self.assertFalse(guard_write_intent("list backups show get describe"))

    def test_listbackups_operation_not_blocked(self):
        # "ListBackups" must NOT trip the guard (bare "backup" is not a keyword).
        self.assertFalse(guard_write_intent("--operation ListBackups"))

    def test_offsets_and_filters_do_not_trip(self):
        self.assertFalse(guard_write_intent(
            "--offset 20 --limit 10 --status available"))

    def test_create_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("CreateBackup my-ecs")

    def test_delete_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--operation DeleteBackup")

    def test_mutating_verbs_blocked(self):
        for text in ("restore backup", "copy backup", "import backup",
                     "update backup", "replicate backup", "migrate vault resource",
                     "associate vault policy", "add vault resource",
                     "delete vault", "change charge mode"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_normalized_separators_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--delete-backup")
        with self.assertRaises(GuardError):
            guard_write_intent("restore_backup")

    def test_filter_values_stripped(self):
        # A backup literally named "delete-me" must not trip the guard.
        self.assertFalse(guard_write_intent(
            guard_text_from_argv(["--name", "delete-me", "--region", "cn-north-4"])))

    def test_operation_guard_rejects_non_listbackups(self):
        with self.assertRaises(GuardError):
            guard_operation("CreateBackup")
        with self.assertRaises(GuardError):
            guard_operation("RestoreBackup")
        self.assertTrue(guard_operation(ALLOWED_OPERATION))


class TestBuildCommand(unittest.TestCase):
    def test_basic(self):
        argv = build_command("cn-north-4")
        self.assertEqual(argv[0], "CBR")
        self.assertEqual(argv[1], "ListBackups")
        self.assertIn("--cli-region=cn-north-4", argv)
        self.assertIn("--limit=1000", argv)
        self.assertIn("--offset=0", argv)

    def test_region_and_offsets(self):
        argv = build_command("cn-south-1", limit=5, offset=10)
        self.assertIn("--cli-region=cn-south-1", argv)
        self.assertIn("--limit=5", argv)
        self.assertIn("--offset=10", argv)

    def test_native_filters_passed(self):
        argv = build_command("cn-north-4", filters={
            "name": "backup-x", "status": "available", "vault_id": "vault-1",
            "resource_id": "res-1", "resource_name": "ecs-1",
            "resource_type": "OS::Nova::Server", "image_type": "backup",
        })
        self.assertIn("--name=backup-x", argv)
        self.assertIn("--status=available", argv)
        self.assertIn("--vault_id=vault-1", argv)
        self.assertIn("--resource_id=res-1", argv)
        self.assertIn("--resource_name=ecs-1", argv)
        self.assertIn("--resource_type=OS::Nova::Server", argv)
        self.assertIn("--image_type=backup", argv)

    def test_filters_use_koolcli_underscore_form(self):
        # KooCLI CBR ListBackups only accepts underscore params; the hyphenated
        # form is rejected with [USE_ERROR]Invalid parameter. build_command must
        # never emit a hyphenated filter flag.
        argv = build_command("cn-north-4", filters={
            "resource_id": "res-1", "resource_name": "ecs-1",
            "resource_type": "OS::Nova::Server", "vault_id": "vault-1",
            "image_type": "backup",
        })
        for flag in ("--resource-id=", "--resource-name=", "--resource-type=",
                     "--vault-id=", "--image-type="):
            self.assertFalse(any(a.startswith(flag) for a in argv), flag)

    def test_empty_filters_omitted(self):
        argv = build_command("cn-north-4", filters={"name": None, "status": ""})
        self.assertFalse(any(a.startswith("--name=") for a in argv))
        self.assertFalse(any(a.startswith("--status=") for a in argv))

    def test_no_write_flags_ever_added(self):
        argv = build_command("cn-north-4")
        for flag in argv:
            self.assertFalse(
                flag.lower().lstrip("-").startswith(("create", "delete", "restore")))


class TestParsing(unittest.TestCase):
    def test_extract_json_plain(self):
        self.assertEqual(extract_json('{"count": 0}'), {"count": 0})

    def test_extract_json_wrapped(self):
        self.assertEqual(extract_json('noise {"a": 1} tail'), {"a": 1})

    def test_extract_json_list(self):
        self.assertEqual(extract_json('[{"a": 1}]'), [{"a": 1}])

    def test_extract_json_invalid(self):
        with self.assertRaises(ApiError):
            extract_json("not json at all")

    def test_extract_backups_key(self):
        payload = {"backups": [{"id": "1"}]}
        self.assertEqual(extract_backups(payload), [{"id": "1"}])

    def test_extract_backup_list_key(self):
        payload = {"backup_list": [{"id": "2"}]}
        self.assertEqual(extract_backups(payload), [{"id": "2"}])

    def test_extract_bare_list(self):
        self.assertEqual(extract_backups([{"id": "3"}]), [{"id": "3"}])

    def test_extract_empty(self):
        self.assertEqual(extract_backups({"count": 0}), [])

    def test_normalize_backup_datetime(self):
        flat = normalize_backup({"name": "x", "created_at": "2026-01-01T00:00:00Z"})
        self.assertEqual(flat["created_at"], "2026-01-01T00:00:00Z")

    def test_normalize_backup_az_fallback(self):
        flat = normalize_backup({"name": "x", "az_name": "cn-north-4a"})
        self.assertEqual(flat["resource_az"], "cn-north-4a")


class TestClassifyFailure(unittest.TestCase):
    def test_missing_credentials(self):
        err = classify_hcloud_failure(
            "", "Error: CLI credential is not configured, please run configure", 3)
        self.assertIsInstance(err, ConfigError)
        self.assertIn("AK/SK", str(err))

    def test_auth_403(self):
        err = classify_hcloud_failure("", "403 Forbidden", 1)
        self.assertIsInstance(err, AuthError)
        self.assertIn("IAM", str(err))

    def test_generic_api_error(self):
        err = classify_hcloud_failure("", "boom", 2)
        self.assertIsInstance(err, ApiError)

    def test_use_error_marker_with_zero_rc(self):
        err = classify_hcloud_failure(
            "[USE_ERROR]Invalid parameter: foo", "", 0)
        self.assertIsInstance(err, ApiError)
        self.assertIn("参数错误", str(err))


class TestListBackups(unittest.TestCase):
    def test_success(self):
        fake = FakeRunner([(CLI_OUTPUT, "", 0)])
        with mock.patch("list_cbr_backups.subprocess.run", fake):
            backups = list_backups("cn-north-4")
        self.assertEqual([b["name"] for b in backups],
                         ["backup-alpha", "backup-beta"])
        self.assertEqual(fake.calls[0][0:3], ["hcloud", "CBR", "ListBackups"])

    def test_empty(self):
        fake = FakeRunner([(CLI_OUTPUT_EMPTY, "", 0)])
        with mock.patch("list_cbr_backups.subprocess.run", fake):
            backups = list_backups("cn-north-4")
        self.assertEqual(backups, [])

    def test_paging_uses_count(self):
        page1 = json.dumps({"backups": [{"id": "1"}, {"id": "2"}], "count": 3})
        page2 = json.dumps({"backups": [{"id": "3"}], "count": 3})
        fake = FakeRunner([(page1, "", 0), (page2, "", 0)])
        with mock.patch("list_cbr_backups.subprocess.run", fake):
            backups = list_backups("cn-north-4", limit=2)
        self.assertEqual(len(backups), 3)
        self.assertEqual(len(fake.calls), 2)
        self.assertIn("--offset=0", fake.calls[0])
        self.assertIn("--offset=2", fake.calls[1])

    def test_filters_are_passed_to_command(self):
        fake = FakeRunner([(CLI_OUTPUT, "", 0)])
        with mock.patch("list_cbr_backups.subprocess.run", fake):
            list_backups("cn-north-4", filters={"status": "available"})
        self.assertIn("--status=available", fake.calls[0])

    def test_missing_credentials_raises_config(self):
        fake = FakeRunner([("", "CLI credential is not configured", 3)])
        with mock.patch("list_cbr_backups.subprocess.run", fake):
            with self.assertRaises(ConfigError):
                list_backups("cn-north-4")

    def test_auth_failure_raises_auth(self):
        fake = FakeRunner([("", "403 Forbidden", 1)])
        with mock.patch("list_cbr_backups.subprocess.run", fake):
            with self.assertRaises(AuthError):
                list_backups("cn-north-4")

    def test_use_error_rc0_raises_api(self):
        fake = FakeRunner([("[USE_ERROR]Invalid parameter: foo", "", 0)])
        with mock.patch("list_cbr_backups.subprocess.run", fake):
            with self.assertRaises(ApiError):
                list_backups("cn-north-4")

    def test_timeout(self):
        fake = FakeRunner([subprocess.TimeoutExpired(cmd="hcloud", timeout=120)])
        with mock.patch("list_cbr_backups.subprocess.run", fake):
            with self.assertRaises(ApiError):
                list_backups("cn-north-4")

    def test_sdk_fallback_when_hcloud_missing(self):
        with mock.patch("list_cbr_backups.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_cbr_backups.list_backups_via_sdk",
                           return_value=[{"name": "sdk-backup"}]) as sdk_mock:
            backups = list_backups("cn-north-4")
        self.assertEqual(backups, [{"name": "sdk-backup"}])
        sdk_mock.assert_called_once()

    def test_sdk_fallback_unavailable_raises_config(self):
        with mock.patch("list_cbr_backups.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_cbr_backups.list_backups_via_sdk",
                           side_effect=ConfigError("huaweicloudsdkcbr 未安装")):
            with self.assertRaises(ConfigError):
                list_backups("cn-north-4")


def _fake_sdk_modules():
    """Minimal fake huaweicloudsdk modules so the SDK import block succeeds."""
    core = types.ModuleType("huaweicloudsdkcore")
    creds = types.ModuleType("huaweicloudsdkcore.auth.credentials")
    creds.BasicCredentials = object
    region_mod = types.ModuleType("huaweicloudsdkcore.region.region")
    region_mod.Region = object
    http = types.ModuleType("huaweicloudsdkcore.http.http_config")
    http.HttpConfig = object
    v1 = types.ModuleType("huaweicloudsdkcbr.v1")
    v1.CbrClient = object
    v1.ListBackupsRequest = object
    v1.BackupResp = object
    reg = types.ModuleType("huaweicloudsdkcbr.v1.region.cbr_region")
    reg.CbrRegion = object
    return {
        "huaweicloudsdkcore": core,
        "huaweicloudsdkcore.auth": types.ModuleType("huaweicloudsdkcore.auth"),
        "huaweicloudsdkcore.auth.credentials": creds,
        "huaweicloudsdkcore.region": types.ModuleType("huaweicloudsdkcore.region"),
        "huaweicloudsdkcore.region.region": region_mod,
        "huaweicloudsdkcore.http": types.ModuleType("huaweicloudsdkcore.http"),
        "huaweicloudsdkcore.http.http_config": http,
        "huaweicloudsdkcbr": types.ModuleType("huaweicloudsdkcbr"),
        "huaweicloudsdkcbr.v1": v1,
        "huaweicloudsdkcbr.v1.region": types.ModuleType("huaweicloudsdkcbr.v1.region"),
        "huaweicloudsdkcbr.v1.region.cbr_region": reg,
    }


class TestSdkFallback(unittest.TestCase):
    def test_missing_env_credentials_raises_config(self):
        credential_vars = (
            "HW_ACCESS_KEY", "HUAWEI_ACCESS_KEY", "HUAWEICLOUD_SDK_AK",
            "HUAWEI_CLOUD_ACCESS_KEY", "HW_SECRET_KEY", "HUAWEI_SECRET_KEY",
            "HUAWEICLOUD_SDK_SK", "HUAWEI_CLOUD_SECRET_KEY",
        )
        env = {name: "" for name in credential_vars}
        with mock.patch.dict(sys.modules, _fake_sdk_modules()), \
                mock.patch.dict(os.environ, env):
            with self.assertRaises(ConfigError) as ctx:
                list_backups_via_sdk("cn-north-4")
        self.assertIn("AK/SK", str(ctx.exception))

    def test_sdk_backup_to_dict_remaps_wire_names(self):
        class Backup:
            def to_dict(self):
                return {"name": "b", "resource_size": 40}

        class BackupResp:
            attribute_map = {"name": "name", "resource_size": "resourceSize"}

        fake_mod = types.ModuleType("huaweicloudsdkcbr.v1")
        fake_mod.BackupResp = BackupResp
        with mock.patch.dict(sys.modules, {
                "huaweicloudsdkcbr": types.ModuleType("huaweicloudsdkcbr"),
                "huaweicloudsdkcbr.v1": fake_mod}):
            record = sdk_backup_to_dict(Backup())
        self.assertEqual(record["name"], "b")
        self.assertEqual(record["resourceSize"], 40)

    def test_sdk_backup_to_dict_plain_dict(self):
        self.assertEqual(sdk_backup_to_dict({"name": "b"}), {"name": "b"})


class TestFiltering(unittest.TestCase):
    BACKUPS = [
        {"id": "b1", "name": "backup-prod", "status": "available",
         "resource_id": "res-1", "resource_name": "ecs-prod",
         "resource_type": "OS::Nova::Server", "vault_id": "vault-1",
         "image_type": "backup"},
        {"id": "b2", "name": "backup-dev", "status": "error",
         "resource_id": "res-2", "resource_name": "evs-dev",
         "resource_type": "OS::Cinder::Volume", "vault_id": "vault-2",
         "image_type": "backup"},
    ]

    def test_filter_by_name(self):
        self.assertEqual(
            [b["name"] for b in filter_backups(self.BACKUPS, name="prod")],
            ["backup-prod"])

    def test_filter_by_status(self):
        self.assertEqual(
            [b["name"] for b in filter_backups(self.BACKUPS, status="error")],
            ["backup-dev"])

    def test_filter_by_resource_id(self):
        self.assertEqual(
            [b["id"] for b in filter_backups(self.BACKUPS, resource_id="res-2")],
            ["b2"])

    def test_filter_by_resource_name(self):
        self.assertEqual(
            [b["name"] for b in filter_backups(self.BACKUPS, resource_name="evs")],
            ["backup-dev"])

    def test_filter_by_resource_type(self):
        self.assertEqual(
            [b["name"] for b in filter_backups(
                self.BACKUPS, resource_type="OS::Nova::Server")],
            ["backup-prod"])

    def test_filter_by_vault_id(self):
        self.assertEqual(
            [b["name"] for b in filter_backups(self.BACKUPS, vault_id="vault-1")],
            ["backup-prod"])

    def test_filter_descriptions(self):
        desc = active_filter_descriptions(
            name="b", status="available", vault_id="vault-1")
        self.assertEqual(desc, ["name=b", "status=available", "vault_id=vault-1"])


class TestRenderAndNames(unittest.TestCase):
    def test_names(self):
        self.assertEqual(
            backup_names([{"name": "a"}, {"name": "b"}]), ["a", "b"])

    def test_names_fallback_to_id(self):
        self.assertEqual(backup_names([{"id": "only-id"}]), ["only-id"])

    def test_summary_lines(self):
        lines = backup_summary_lines([{"name": "a", "id": "1"}])
        self.assertEqual(lines, ["a  (id: 1)"])

    def test_table_contains_fields(self):
        backups = extract_backups(json.loads(CLI_OUTPUT))
        table = render_table(backups)
        for fragment in ("name", "id", "status", "resource_name", "resource_id",
                         "resource_type", "vault_id", "backup-alpha", "ecs-alpha"):
            self.assertIn(fragment, table)

    def test_table_minimal(self):
        table = render_table([{"name": "only-name"}])
        self.assertIn("only-name", table)
        self.assertIn("name", table)


class TestMain(unittest.TestCase):
    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("list_cbr_backups.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            rc = main(argv)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    def test_table_output(self):
        rc, out, err = self._run(["--region", "cn-north-4"], [(CLI_OUTPUT, "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("CBR 备份列表", out)
        self.assertIn("backup-alpha", out)
        self.assertEqual(err, "")

    def test_json_output(self):
        rc, out, err = self._run(["--json"], [(CLI_OUTPUT, "", 0)])
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual([b["name"] for b in payload],
                         ["backup-alpha", "backup-beta"])

    def test_names_output(self):
        rc, out, err = self._run(["--names-only"], [(CLI_OUTPUT, "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("backup-alpha", out)
        self.assertNotIn("resource_type", out)

    def test_name_filter_applied(self):
        rc, out, err = self._run(["--names-only", "--name", "alpha"],
                                 [(CLI_OUTPUT, "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("backup-alpha", out)
        self.assertNotIn("backup-beta", out)

    def test_underscore_filter_flag_forwarded_to_koolcli(self):
        fake = FakeRunner([(CLI_OUTPUT, "", 0)])
        with mock.patch("list_cbr_backups.subprocess.run", fake), \
                mock.patch("sys.stdout"), mock.patch("sys.stderr"):
            rc = main(["--names-only", "--resource_type", "OS::Nova::Server"])
        self.assertEqual(rc, 0)
        self.assertIn("--resource_type=OS::Nova::Server", fake.calls[0])
        self.assertFalse(any(a.startswith("--resource-type=") for a in fake.calls[0]))

    def test_hyphen_filter_flag_alias_still_accepted(self):
        fake = FakeRunner([(CLI_OUTPUT, "", 0)])
        with mock.patch("list_cbr_backups.subprocess.run", fake), \
                mock.patch("sys.stdout"), mock.patch("sys.stderr"):
            rc = main(["--names-only", "--resource-type", "OS::Nova::Server"])
        self.assertEqual(rc, 0)
        self.assertIn("--resource_type=OS::Nova::Server", fake.calls[0])

    def test_empty_message(self):
        rc, out, err = self._run(["--region", "cn-south-1"],
                                 [(CLI_OUTPUT_EMPTY, "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("无 CBR 备份", out)
        self.assertIn("cn-south-1", out)

    def test_empty_json_output(self):
        rc, out, err = self._run(["--json"], [(CLI_OUTPUT_EMPTY, "", 0)])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out), [])

    def test_auth_error_message(self):
        rc, out, err = self._run([], [("", "403 Forbidden", 1)])
        self.assertEqual(rc, 1)
        self.assertIn("[错误]", err)
        self.assertIn("IAM", err)

    def test_missing_ak_sk_error_message(self):
        rc, out, err = self._run([], [("", "CLI credential is not configured", 3)])
        self.assertEqual(rc, 1)
        self.assertIn("AK/SK", err)

    def test_hcloud_not_installed(self):
        with mock.patch("list_cbr_backups.list_backups_via_sdk",
                        side_effect=ConfigError("huaweicloudsdkcbr 未安装")):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 1)
        self.assertIn("未安装", err)

    def test_hcloud_missing_falls_back_to_sdk(self):
        with mock.patch("list_cbr_backups.list_backups_via_sdk",
                        return_value=[{"name": "sdk-backup", "id": "x"}]):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 0)
        self.assertIn("sdk-backup", out)

    def test_write_intent_operation_blocked(self):
        rc, out, err = self._run(["--operation", "CreateBackup"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)

    def test_write_keyword_argv_blocked(self):
        rc, out, err = self._run(["--delete-backup"], [])
        self.assertEqual(rc, 1)
        self.assertIn("守卫拦截", err)


class TestErrorHierarchy(unittest.TestCase):
    def test_subclasses(self):
        for exc in (GuardError, ConfigError, AuthError, ApiError):
            self.assertTrue(issubclass(exc, CbrListError))


if __name__ == "__main__":
    unittest.main()