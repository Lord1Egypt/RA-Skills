#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Offline unit tests for huawei-cloud-iam-user-manage.

No credentials and no network are used: the execution backend is replaced by a
duck-typed fake implementing the same ``call(operation, params)`` contract, and
the CLI backend is exercised through an injected command runner.

Run:
    python3 -m unittest discover -s tests -v
"""

import importlib.util
import io
import pathlib
import unittest
from contextlib import redirect_stderr, redirect_stdout

HERE = pathlib.Path(__file__).resolve().parent
MOD_PATH = HERE.parent / "scripts" / "iam_user_manage.py"

_spec = importlib.util.spec_from_file_location("iam_user_manage", MOD_PATH)
iam = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(iam)


# --------------------------------------------------------------------------
# Fakes
# --------------------------------------------------------------------------

class FakeBackend(object):
    """In-memory implementation of the backend call contract."""

    name = "fake"

    def __init__(self, users=None, groups=None, policies=None, errors=None):
        self.users = list(users or [])
        self.groups = list(groups or [])
        self.policies = list(policies or [])
        self.errors = errors or {}       # operation -> IamError to raise once
        self.calls = []

    def _maybe_raise(self, operation):
        exc = self.errors.pop(operation, None)
        if exc is not None:
            raise exc

    def call(self, operation, params):
        self.calls.append((operation, params))
        self._maybe_raise(operation)
        if operation == "ListUsersV5":
            return {"users": self.users}
        if operation == "ListGroupsV5":
            return {"groups": self.groups}
        if operation == "ListPoliciesV5":
            return {"policies": self.policies}
        if operation == "ShowUserV5":
            for user in self.users:
                if user.get("user_id") == params["user_id"]:
                    return {"user": user}
            raise iam.IamError("not found", code="404")
        if operation == "CreateUserV5":
            user = {"user_id": "uid-%d" % (len(self.users) + 1),
                    "user_name": params["name"],
                    "enabled": params.get("enabled", True),
                    "description": params.get("description")}
            self.users.append(user)
            return {"user": user}
        if operation == "CreateGroupV5":
            group = {"group_id": "gid-%d" % (len(self.groups) + 1),
                     "group_name": params["group_name"],
                     "description": params.get("description")}
            self.groups.append(group)
            return {"group": group}
        if operation == "AddUserToGroupV5":
            return {}
        if operation == "AttachUserPolicyV5":
            return {}
        raise AssertionError("unexpected operation %s" % operation)


def make_manager(backend, as_json=False):
    out = (lambda data: iam._emit(None, data, True)) if as_json else iam._default_out
    return iam.Manager(backend, out)


def run_main(argv):
    """Run main(argv), returning (exit_code, stdout, stderr)."""
    stdout, stderr = io.StringIO(), io.StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        code = iam.main(argv)
    return code, stdout.getvalue(), stderr.getvalue()


# --------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------

class ValidationTests(unittest.TestCase):
    def test_valid_user_names(self):
        for name in ("alice", "ops_user", "svc-01", "a.b"):
            self.assertEqual(iam.validate_user_name(name), name)

    def test_user_name_rejects_leading_digit(self):
        with self.assertRaises(iam.ValidationError):
            iam.validate_user_name("1alice")

    def test_user_name_rejects_illegal_char(self):
        with self.assertRaises(iam.ValidationError):
            iam.validate_user_name("al ice!")  # space allowed, '!' not

    def test_user_name_rejects_overlength(self):
        with self.assertRaises(iam.ValidationError):
            iam.validate_user_name("a" * 65)

    def test_description_forbidden_chars(self):
        with self.assertRaises(iam.ValidationError):
            iam.validate_description("bad@desc")

    def test_description_length_limit(self):
        with self.assertRaises(iam.ValidationError):
            iam.validate_description("x" * 256)
        self.assertEqual(iam.validate_description("ok"), "ok")

    def test_iam_id_validation(self):
        self.assertEqual(iam.validate_iam_id("abc-123", "用户ID"), "abc-123")
        with self.assertRaises(iam.ValidationError):
            iam.validate_iam_id("bad id", "用户ID")


# --------------------------------------------------------------------------
# Manager behaviour
# --------------------------------------------------------------------------

class ManagerTests(unittest.TestCase):
    def test_create_user_returns_id_and_name(self):
        backend = FakeBackend()
        manager = make_manager(backend)
        user = manager.create_user("alice", "ops")
        self.assertEqual(user["user_name"], "alice")
        self.assertTrue(user["user_id"])
        self.assertFalse(user["reused"])

    def test_create_user_idempotent_on_conflict(self):
        backend = FakeBackend(
            users=[{"user_id": "uid-1", "user_name": "alice", "enabled": True}],
            errors={"CreateUserV5": iam.IamError("already exists", code="409")})
        manager = make_manager(backend)
        user = manager.create_user("alice")
        self.assertEqual(user["user_id"], "uid-1")
        self.assertTrue(user["reused"])

    def test_resolve_group_existing(self):
        backend = FakeBackend(groups=[{"group_id": "gid-9", "group_name": "ops"}])
        manager = make_manager(backend)
        group = manager.resolve_group(group_name="ops")
        self.assertEqual(group["group_id"], "gid-9")
        self.assertTrue(group["reused"])
        self.assertFalse(group["created"])

    def test_resolve_group_create_when_missing(self):
        backend = FakeBackend()
        manager = make_manager(backend)
        group = manager.resolve_group(group_name="ops", create=True, description="d")
        self.assertTrue(group["created"])
        self.assertFalse(group["reused"])
        self.assertEqual(group["group_name"], "ops")

    def test_resolve_group_missing_without_create_errors(self):
        manager = make_manager(FakeBackend())
        with self.assertRaises(iam.IamError):
            manager.resolve_group(group_name="nope")

    def test_resolve_policy_by_name(self):
        backend = FakeBackend(policies=[{"policy_id": "pid-1", "policy_name": "ReadOnlyAccess"}])
        manager = make_manager(backend)
        policy = manager.resolve_policy(policy_name="ReadOnlyAccess")
        self.assertEqual(policy["policy_id"], "pid-1")

    def test_resolve_policy_ambiguous(self):
        backend = FakeBackend(policies=[
            {"policy_id": "pid-1", "policy_name": "dup"},
            {"policy_id": "pid-2", "policy_name": "dup"}])
        manager = make_manager(backend)
        with self.assertRaises(iam.IamError):
            manager.resolve_policy(policy_name="dup")

    def test_resolve_policy_not_found(self):
        manager = make_manager(FakeBackend())
        with self.assertRaises(iam.IamError):
            manager.resolve_policy(policy_name="missing")

    def test_add_user_to_group_conflict_is_tolerated(self):
        backend = FakeBackend(errors={"AddUserToGroupV5":
                                      iam.IamError("user already in group", code="409")})
        manager = make_manager(backend)
        outcome = manager.add_user_to_group("uid-1", "gid-1")
        self.assertTrue(outcome["already_member"])

    def test_attach_policy_conflict_is_tolerated(self):
        backend = FakeBackend(errors={"AttachUserPolicyV5":
                                      iam.IamError("policy already attached", code="409")})
        manager = make_manager(backend)
        outcome = manager.attach_policy("uid-1", "pid-1")
        self.assertTrue(outcome["already_attached"])

    def test_authorize_combines_group_and_policies(self):
        backend = FakeBackend()
        manager = make_manager(backend)
        user = manager.create_user("alice")
        group = manager.resolve_group(group_name="ops", create=True)
        policy = {"policy_id": "pid-1", "policy_name": "ReadOnlyAccess"}
        result = manager.authorize(user, group, [policy])
        self.assertEqual(result["user_name"], "alice")
        self.assertEqual(result["group"]["group_id"], group["group_id"])
        self.assertEqual(result["policies"][0]["policy_id"], "pid-1")

    def test_authorize_without_targets(self):
        backend = FakeBackend()
        manager = make_manager(backend)
        user = {"user_id": "uid-1", "user_name": "alice"}
        result = manager.authorize(user, None, [])
        self.assertIsNone(result["group"])
        self.assertEqual(result["policies"], [])


# --------------------------------------------------------------------------
# CLI backend command construction
# --------------------------------------------------------------------------

class CliBackendTests(unittest.TestCase):
    def test_build_cmd_create_user(self):
        backend = iam.CliBackend("cn-north-4")
        cmd = backend.build_cmd("CreateUserV5",
                                {"name": "alice", "description": "ops", "enabled": True})
        self.assertIn("IAM", cmd)
        self.assertIn("CreateUserV5", cmd)
        self.assertIn("--cli-region=cn-north-4", cmd)
        self.assertIn("--name=alice", cmd)
        self.assertIn("--enabled=true", cmd)
        self.assertTrue(cmd[0] in ("hcloud", "skill-quality-cli"))

    def test_build_cmd_add_user_to_group(self):
        backend = iam.CliBackend("cn-north-4")
        cmd = backend.build_cmd("AddUserToGroupV5", {"user_id": "uid-1", "group_id": "gid-1"})
        self.assertIn("--user_id=uid-1", cmd)
        self.assertIn("--group_id=gid-1", cmd)

    def test_build_cmd_attach_policy(self):
        backend = iam.CliBackend("cn-north-4")
        cmd = backend.build_cmd("AttachUserPolicyV5", {"user_id": "uid-1", "policy_id": "pid-1"})
        self.assertIn("--policy_id=pid-1", cmd)
        self.assertIn("--user_id=uid-1", cmd)

    def test_cli_runner_parses_json(self):
        captured = {}

        def runner(cmd):
            captured["cmd"] = cmd
            return {"user": {"user_id": "uid-1", "user_name": "alice"}}

        backend = iam.CliBackend("cn-north-4", runner=runner)
        payload = backend.call("CreateUserV5", {"name": "alice"})
        self.assertEqual(payload["user"]["user_id"], "uid-1")
        self.assertIn("--name=alice", captured["cmd"])

    def test_cli_runner_maps_failure(self):
        def runner(cmd):
            raise iam.IamError("KooCLI 调用失败：boom")

        backend = iam.CliBackend("cn-north-4", runner=runner)
        with self.assertRaises(iam.IamError):
            backend.call("CreateUserV5", {"name": "alice"})

    def test_extract_json_from_noisy_output(self):
        self.assertEqual(iam._extract_json('log line\n{"a": 1}'), {"a": 1})
        with self.assertRaises(iam.IamError):
            iam._extract_json("plain text without json")

    def test_extract_json_tolerates_trailing_diagnostics(self):
        noisy = ('{"error_code": "PAP5.0001", "error_msg": "access denied"}\n'
                 'Failed to get terminal width, using a default of 80.')
        payload = iam._extract_json(noisy)
        self.assertEqual(payload["error_code"], "PAP5.0001")
        self.assertEqual(payload["error_msg"], "access denied")

    def test_extract_json_handles_nested_and_braces_in_strings(self):
        text = 'log\n{"a": {"b": "}"}, "c": [1, 2]}\ntrailing diagnostic'
        self.assertEqual(iam._extract_json(text), {"a": {"b": "}"}, "c": [1, 2]})

    def test_extract_json_handles_leading_noise_and_array(self):
        self.assertEqual(iam._extract_json('noise [1, 2] tail'), [1, 2])

    def test_default_runner_surfaces_api_error(self):
        from unittest import mock
        stdout = ('{"error_code": "PAP5.0001", "error_msg": "access denied"}\n'
                  'Failed to get terminal width, using a default of 80.')
        proc = mock.Mock(returncode=0, stdout=stdout, stderr="")
        backend = iam.CliBackend("cn-north-4")
        with mock.patch("subprocess.run", return_value=proc):
            with self.assertRaises(iam.IamError) as ctx:
                backend.call("CreateUserV5", {"name": "bob"})
        self.assertEqual(ctx.exception.code, "PAP5.0001")
        self.assertIn("access denied", ctx.exception.message)

    def test_default_runner_maps_nonzero_exit(self):
        from unittest import mock
        proc = mock.Mock(returncode=1, stdout="", stderr="boom")
        backend = iam.CliBackend("cn-north-4")
        with mock.patch("subprocess.run", return_value=proc):
            with self.assertRaises(iam.IamError) as ctx:
                backend.call("ListUsersV5", {"limit": 100})
        self.assertIn("boom", ctx.exception.message)

    def test_default_runner_reads_error_json_from_stderr(self):
        from unittest import mock
        proc = mock.Mock(returncode=1, stdout="",
                         stderr='{"error_code": "IAM.0202", "error_msg": "user exists"}')
        backend = iam.CliBackend("cn-north-4")
        with mock.patch("subprocess.run", return_value=proc):
            with self.assertRaises(iam.IamError) as ctx:
                backend.call("CreateUserV5", {"name": "bob"})
        self.assertEqual(ctx.exception.code, "IAM.0202")

    def test_default_runner_returns_payload_on_success(self):
        from unittest import mock
        proc = mock.Mock(returncode=0,
                         stdout='{"user": {"user_id": "uid-1", "user_name": "alice"}}',
                         stderr="")
        backend = iam.CliBackend("cn-north-4")
        with mock.patch("subprocess.run", return_value=proc):
            payload = backend.call("CreateUserV5", {"name": "alice"})
        self.assertEqual(payload["user"]["user_id"], "uid-1")


# --------------------------------------------------------------------------
# SDK backend construction (the CLI-free fallback path)
# --------------------------------------------------------------------------

def _sdk_available():
    try:
        import huaweicloudsdkiam.v5  # noqa: F401
        import huaweicloudsdkcore  # noqa: F401
        return True
    except ImportError:
        return False


@unittest.skipUnless(_sdk_available(), "huaweicloudsdkiam (SDK fallback) is not installed")
class SdkBackendTests(unittest.TestCase):
    def test_iam_region_lives_in_region_submodule(self):
        # Regression guard: IamRegion is NOT exported from the v5 top-level
        # package (huaweicloudsdkiam 3.1.219), so the import must use the
        # region submodule.
        import huaweicloudsdkiam.v5 as v5
        from huaweicloudsdkiam.v5.region.iam_region import IamRegion
        self.assertFalse(hasattr(v5, "IamRegion"))
        self.assertTrue(hasattr(v5, "IamClient"))
        self.assertTrue(callable(IamRegion.value_of))
        self.assertIsNotNone(IamRegion.value_of("cn-north-4"))

    def test_build_client_resolves_region_import(self):
        from unittest import mock
        from huaweicloudsdkiam.v5 import IamClient
        sentinel = object()
        with mock.patch.object(IamClient, "new_builder") as builder:
            chain = builder.return_value
            for method in ("with_credentials", "with_http_config", "with_region"):
                getattr(chain, method).return_value = chain
            chain.build.return_value = sentinel
            backend = iam.SdkBackend("cn-north-4", "ak", "sk")
            client = backend._build_client()
        self.assertIs(client, sentinel)
        chain.with_region.assert_called_once()

    def test_sdk_backend_available_when_sdk_installed(self):
        backend = iam.SdkBackend("cn-north-4", "ak", "sk")
        self.assertTrue(backend.available())


# --------------------------------------------------------------------------
# main() end-to-end (offline paths)
# --------------------------------------------------------------------------

class MainCliTests(unittest.TestCase):
    def setUp(self):
        import os
        self._saved = {}
        for key in list(os.environ):
            if key.startswith(("HUAWEI", "HW_", "HWC", "HUAWEICLOUD")):
                self._saved[key] = os.environ.pop(key)
        self.addCleanup(self._restore)

    def _restore(self):
        import os
        for key, value in self._saved.items():
            os.environ[key] = value

    def test_dry_run_needs_no_credentials(self):
        code, out, _ = run_main(["create-user", "--name", "alice", "--dry-run", "--json"])
        self.assertEqual(code, 0)
        self.assertIn("alice", out)

    def test_dry_run_text_output_create_user_offline(self):
        code, out, err = run_main([
            "create-user", "--name", "alice", "--group-name", "ops",
            "--policy-name", "ReadOnlyAccess", "--dry-run"])
        self.assertEqual(code, 0)
        self.assertEqual(err, "")
        self.assertIn("create-user", out)
        self.assertIn("ReadOnlyAccess", out)
        self.assertIn("未调用后端", out)

    def test_dry_run_authorize_offline(self):
        code, out, err = run_main([
            "authorize", "--user-name", "hwtest-demo", "--group-name", "demo-group",
            "--policy-name", "ReadOnlyAccess", "--dry-run"])
        self.assertEqual(code, 0)
        self.assertEqual(err, "")
        self.assertIn("authorize", out)
        self.assertIn("hwtest-demo", out)

    def test_dry_run_attach_policy_offline(self):
        code, out, err = run_main([
            "attach-policy", "--user-id", "uid-1",
            "--policy-name", "ReadOnlyAccess", "--dry-run"])
        self.assertEqual(code, 0)
        self.assertEqual(err, "")
        self.assertIn("attach-policy", out)

    def test_dry_run_invalid_name_still_rejected(self):
        code, _, err = run_main(["create-user", "--name", "1demo", "--dry-run"])
        self.assertEqual(code, 2)
        self.assertIn("参数校验失败", err)

    def test_write_requires_confirmation(self):
        code, _, err = run_main(["create-group", "--name", "ops", "--json"])
        self.assertEqual(code, 2)
        self.assertIn("CONFIRM", err)

    def test_invalid_name_exit_code(self):
        code, _, err = run_main(["create-user", "--name", "1bad", "--confirm"])
        self.assertEqual(code, 2)
        self.assertIn("参数校验失败", err)

    def test_missing_credentials_hint(self):
        code, _, err = run_main(["list-users", "--json"])
        self.assertEqual(code, 1)
        self.assertIn("AK/SK", err)

    def test_cli_executor_without_hcloud(self):
        import shutil
        from unittest import mock
        with mock.patch.object(shutil, "which", return_value=None):
            code, _, err = run_main(["list-users", "--executor", "cli", "--json"])
        self.assertEqual(code, 1)
        self.assertIn("hcloud", err)


if __name__ == "__main__":
    unittest.main()