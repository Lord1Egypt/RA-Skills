from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INV = ROOT / "tests" / "fixtures" / "inventory.fixture.json"
spec = importlib.util.spec_from_file_location("mosobleirc_cli_safety", ROOT / "scripts" / "mosobleirc.py")
cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cli)
core = importlib.util.module_from_spec(
    importlib.util.spec_from_file_location("mosobleirc_core_safety", ROOT / "scripts" / "mosobleirc_core.py")
)
# Use the exact core module already imported by CLI to avoid duplicate exception classes.
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _posix import requires_fcntl
core = sys.modules["mosobleirc_core"]


class CoreBoundaryRegressionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_relay_client_rejects_plain_http_and_embedded_credentials(self):
        key = self.root / "key"
        key.write_text("secret", encoding="utf-8")
        key.chmod(0o600)
        with self.assertRaises(core.MosOblEIRCError):
            core.RelayClient("http://example.invalid/relay", key)
        credential_url = "https://" + "user" + ":" + "pass" + "@" + "example.invalid/relay"
        with self.assertRaises(core.MosOblEIRCError):
            core.RelayClient(credential_url, key)

    def test_inventory_missing_meter_id_fails_closed(self):
        p = self.root / "inventory.fixture.json"
        p.write_text(json.dumps([{"item_id": 1, "meters": [{"type": "ColdWater"}]}]), encoding="utf-8")
        with self.assertRaises(core.MosOblEIRCError):
            core.load_inventory(p)

    def test_inventory_duplicate_meter_id_across_items_fails_closed(self):
        p = self.root / "inventory.fixture.json"
        p.write_text(json.dumps([
            {"item_id": 1, "meters": [{"meter_id": 10}]},
            {"item_id": 2, "meters": [{"meter_id": 10}]},
        ]), encoding="utf-8")
        with self.assertRaises(core.MosOblEIRCError):
            core.load_inventory(p)

    @requires_fcntl
    def test_meter_lock_rejects_second_writer(self):
        store1 = core.StateStore(self.root / "data")
        store2 = core.StateStore(self.root / "data")
        with store1.exclusive_meter_locks([1003]):
            with self.assertRaises(core.MosOblEIRCError):
                with store2.exclusive_meter_locks([1003]):
                    pass

    @requires_fcntl
    def test_verified_history_and_operation_status_commit_atomically(self):
        store = core.StateStore(self.root / "data")
        store.initialize(core.load_inventory(INV))
        store.prepare_operation(
            "op-atomic-regression", meter_id=1003, value=881,
            observed_at="2026-09-15T09:00:00Z",
            provider_snapshot={"provider_value": 865},
            consumption={"status": "NORMAL"}, ready=True,
            created_at="2026-09-15T09:00:00Z", photo_value=881.95,
        )
        store.update_operation("op-atomic-regression", "EXECUTING", updated_at="2026-09-15T09:01:00Z")
        with store._connect() as conn:
            conn.execute("""
                CREATE TRIGGER abort_verified_update
                BEFORE UPDATE OF status ON operations
                WHEN NEW.status='VERIFIED'
                BEGIN SELECT RAISE(ABORT, 'simulated crash boundary'); END
            """)
        readback = {
            "meter": {
                "id": 1003,
                "lastValue": {
                    "id": 999,
                    "total": {"value": 881, "consumptionValue": 16},
                    "receivedDate": "2026-09-15T15:10:00Z",
                    "status": "PROCESSED",
                    "settlementPeriod": {"year": 2026, "month": 9},
                },
            },
            "valueSendInfo": {"isValueSentForCurrentPeriod": True},
        }
        with self.assertRaises(sqlite3.IntegrityError):
            store.commit_verified_submission(
                "op-atomic-regression", readback,
                fetched_at="2026-09-15T15:10:00Z",
                final_status="VERIFIED",
                result={"ok": True, "status": "VERIFIED"},
                updated_at="2026-09-15T15:10:00Z",
            )
        self.assertEqual(store.get_operation("op-atomic-regression")["status"], "EXECUTING")
        self.assertEqual(store.photo_history(1003), [])
        self.assertEqual(store.provider_history(1003), [])


class WorkflowSafetyRegressionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.data = Path(self.tmp.name) / "data"

    def run_cli(self, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = cli.main(["--data-root", str(self.data), "--inventory", str(INV), *args])
        return rc, json.loads(out.getvalue())

    @staticmethod
    def entry(meter_id, value, *, sent=False, status="PROCESSED", year=2026, month=9):
        return {
            "meter": {
                "id": meter_id,
                "lastValue": {
                    "id": 10000 + meter_id,
                    "total": {"value": value, "consumptionValue": 1},
                    "receivedDate": f"{year:04d}-{month:02d}-15T10:00:00Z",
                    "status": status,
                    "settlementPeriod": {"year": year, "month": month},
                },
            },
            "valueSendInfo": {
                "isAbleToSendMeterValues": True,
                "isInAllowedPeriod": True,
                "isValueSentForCurrentPeriod": sent,
            },
        }

    @requires_fcntl
    def test_partial_results_survive_network_error_during_second_preflight(self):
        before1 = self.entry(1001, 100, sent=False)
        after1 = self.entry(1001, 101, sent=True)
        class Relay:
            def call(_, action, **payload):
                if action == "meters" and int(payload["item_id"]) == 9001:
                    return {"ok": True, "data": [before1]}
                if action == "submit" and int(payload["meter_id"]) == 1001:
                    return {
                        "ok": True, "provider_contacted": True,
                        "operation_id": payload["operation_id"], "status": "VERIFIED",
                        "value": 101, "readback_meter": after1,
                    }
                if action == "meters" and int(payload["item_id"]) == 9002:
                    raise cli.RelayNetworkError("preflight down")
                raise AssertionError((action, payload))
        old = cli._relay
        cli._relay = lambda args: Relay()
        self.addCleanup(lambda: setattr(cli, "_relay", old))
        rc, payload = self.run_cli(
            "send", "readings",
            "--reading", "1001:101:101",
            "--reading", "1003:881:881",
            "--observed-at", "2026-09-15T09:00:00Z",
            "--confirmed-by-user",
        )
        self.assertNotEqual(rc, 0)
        self.assertEqual([x["status"] for x in payload["results"]], ["VERIFIED", "PREFLIGHT_NETWORK_ERROR"])
        self.assertEqual(len(cli.StateStore(self.data).photo_history(1001)), 1)

    @requires_fcntl
    def test_parallel_send_readings_same_meter_second_writer_never_reaches_provider(self):
        import threading

        before = self.entry(1003, 865, sent=False)
        after = self.entry(1003, 881, sent=True)
        entered = threading.Event()
        release = threading.Event()
        calls = []
        call_lock = threading.Lock()

        class Relay:
            def call(_, action, **payload):
                with call_lock:
                    calls.append(action)
                if action == "meters":
                    entered.set()
                    release.wait(timeout=5)
                    return {"ok": True, "data": [before]}
                if action == "submit":
                    return {
                        "ok": True, "provider_contacted": True,
                        "operation_id": payload["operation_id"],
                        "status": "VERIFIED", "value": 881,
                        "readback_meter": after,
                    }
                raise AssertionError(action)

        old = cli._relay
        cli._relay = lambda args: Relay()
        self.addCleanup(lambda: setattr(cli, "_relay", old))

        outputs = []
        errors = []

        def first():
            try:
                rc, payload = self.run_cli(
                    "send", "readings",
                    "--reading", "1003:881:881",
                    "--observed-at", "2026-09-23T10:00:00Z",
                    "--confirmed-by-user",
                )
                outputs.append(("first", rc, payload))
            except Exception as exc:
                errors.append(("first", type(exc).__name__, str(exc)))

        def second():
            try:
                rc, payload = self.run_cli(
                    "send", "readings",
                    "--reading", "1003:881:881",
                    "--observed-at", "2026-09-23T10:00:01Z",
                    "--confirmed-by-user",
                )
                outputs.append(("second", rc, payload))
            except Exception as exc:
                errors.append(("second", type(exc).__name__, str(exc)))

        t1 = threading.Thread(target=first)
        t1.start()
        self.assertTrue(entered.wait(timeout=5))

        t2 = threading.Thread(target=second)
        t2.start()
        t2.join(timeout=5)
        release.set()
        t1.join(timeout=5)

        self.assertFalse(t1.is_alive())
        self.assertFalse(t2.is_alive())
        self.assertEqual(calls.count("submit"), 1)
        self.assertEqual(calls.count("meters"), 1)
        self.assertEqual(errors, [])
        second_result = next(item for item in outputs if item[0] == "second")
        self.assertNotEqual(second_result[1], 0)
        self.assertEqual(second_result[2]["error"], "MosOblEIRCError")
        self.assertIn("another submit is active for meter 1003", second_result[2]["message"])

    @requires_fcntl
    def test_legacy_accepted_not_verified_is_normalized_to_uncertain(self):
        before = self.entry(1003, 865, sent=False)
        class Relay:
            def call(_, action, **payload):
                if action == "meters":
                    return {"ok": True, "data": [before]}
                if action == "submit":
                    return {
                        "ok": False, "provider_contacted": True,
                        "operation_id": payload["operation_id"],
                        "status": "ACCEPTED_NOT_YET_VERIFIED", "value": 881,
                    }
                raise AssertionError(action)
        old = cli._relay
        cli._relay = lambda args: Relay()
        self.addCleanup(lambda: setattr(cli, "_relay", old))
        rc, payload = self.run_cli(
            "send", "readings", "--reading", "1003:881:881",
            "--observed-at", "2026-09-15T09:00:00Z", "--confirmed-by-user",
        )
        self.assertNotEqual(rc, 0)
        self.assertEqual(payload["results"][0]["status"], "UNCERTAIN_NO_RETRY")
        op = cli.StateStore(self.data).find_open_submit(1003, None, statuses=("UNCERTAIN_NO_RETRY",))
        self.assertIsNotNone(op)

    @requires_fcntl
    def test_unresolved_old_value_blocks_new_value_until_reconcile(self):
        store = cli.StateStore(self.data)
        store.initialize(cli.load_inventory(INV))
        store.prepare_operation(
            "op-old-value", meter_id=1003, value=880,
            observed_at="2026-09-15T09:00:00Z",
            provider_snapshot={"provider_value": 865},
            consumption={"status": "NORMAL"}, ready=True,
            created_at="2026-09-15T09:00:00Z", photo_value=880,
        )
        store.update_operation("op-old-value", "UNCERTAIN_NO_RETRY",
                               result={"ok": False, "status": "UNCERTAIN_NO_RETRY"},
                               updated_at="2026-09-15T09:01:00Z")
        before = self.entry(1003, 865, sent=False)
        calls = []
        class Relay:
            def call(_, action, **payload):
                calls.append(action)
                if action == "meters":
                    return {"ok": True, "data": [before]}
                raise AssertionError("submit must not be called")
        old = cli._relay
        cli._relay = lambda args: Relay()
        self.addCleanup(lambda: setattr(cli, "_relay", old))
        rc, payload = self.run_cli(
            "send", "readings", "--reading", "1003:881:881",
            "--observed-at", "2026-09-15T10:00:00Z", "--confirmed-by-user",
        )
        self.assertNotEqual(rc, 0)
        self.assertEqual(calls, ["meters"])
        self.assertEqual(payload["results"][0]["status"], "RECONCILE_REQUIRED")
        self.assertEqual(store.get_operation("op-old-value")["status"], "UNCERTAIN_NO_RETRY")

    @requires_fcntl
    def test_prepare_rejects_second_prepared_operation_for_same_meter(self):
        before = self.entry(1003, 865, sent=False)
        calls = []
        class Relay:
            def call(_, action, **payload):
                calls.append(action)
                if action == "meters":
                    return {"ok": True, "data": [before]}
                raise AssertionError(action)
        old = cli._relay
        cli._relay = lambda args: Relay()
        self.addCleanup(lambda: setattr(cli, "_relay", old))
        rc1, _ = self.run_cli(
            "send", "prepare", "--meter-id", "1003", "--value", "881",
            "--observed-at", "2026-09-15T09:00:00Z", "--operation-id", "op-prepared-1",
            "--confirmed-by-user",
        )
        rc2, p2 = self.run_cli(
            "send", "prepare", "--meter-id", "1003", "--value", "882",
            "--observed-at", "2026-09-15T09:01:00Z", "--operation-id", "op-prepared-2",
            "--confirmed-by-user",
        )
        self.assertEqual(rc1, 0)
        self.assertNotEqual(rc2, 0)
        self.assertEqual(p2["error"], "PREPARE_EXISTS")
        self.assertEqual(p2["existing_operation_id"], "op-prepared-1")
        self.assertEqual(calls, ["meters"])

    @requires_fcntl
    def test_execute_performs_fresh_preflight_and_skips_post_if_already_applied(self):
        before = self.entry(1003, 865, sent=False)
        after = self.entry(1003, 881, sent=True, status="PROCESSED")
        phase = {"prepared": False}
        calls = []
        class Relay:
            def call(_, action, **payload):
                calls.append(action)
                if action == "meters" and not phase["prepared"]:
                    phase["prepared"] = True
                    return {"ok": True, "data": [before]}
                if action == "meters":
                    return {"ok": True, "data": [after]}
                raise AssertionError("submit must not be called after fresh preflight proves applied")
        old = cli._relay
        cli._relay = lambda args: Relay()
        self.addCleanup(lambda: setattr(cli, "_relay", old))
        rc1, _ = self.run_cli(
            "send", "prepare", "--meter-id", "1003", "--value", "881",
            "--observed-at", "2026-09-15T09:00:00Z", "--operation-id", "op-fresh",
            "--confirmed-by-user",
        )
        rc2, p2 = self.run_cli(
            "send", "execute", "--meter-id", "1003", "--value", "881",
            "--operation-id", "op-fresh", "--confirmed-by-user",
        )
        self.assertEqual(rc1, 0)
        self.assertEqual(rc2, 0)
        self.assertEqual(p2["status"], "VERIFIED")
        self.assertFalse(p2["post_attempted"])
        self.assertEqual(calls, ["meters", "meters"])
        self.assertEqual(cli.StateStore(self.data).get_operation("op-fresh")["status"], "VERIFIED")

    @requires_fcntl
    def test_reconcile_previous_month_uses_settlement_period_not_current_flag(self):
        store = cli.StateStore(self.data)
        store.initialize(cli.load_inventory(INV))
        store.prepare_operation(
            "op-september", meter_id=1003, value=881,
            observed_at="2026-09-23T23:59:00Z",
            provider_snapshot={"provider_value": 865},
            consumption={"status": "NORMAL"}, ready=True,
            created_at="2026-09-23T23:59:00Z", photo_value=881,
        )
        store.update_operation("op-september", "UNCERTAIN_NO_RETRY",
                               result={"ok": False, "status": "UNCERTAIN_NO_RETRY"},
                               updated_at="2026-09-23T23:59:30Z")
        old_period = self.entry(1003, 881, sent=False, status="PROCESSED", year=2026, month=9)
        class Relay:
            def call(_, action, **payload):
                self.assertEqual(action, "meters")
                return {"ok": True, "data": [old_period]}
        old = cli._relay
        cli._relay = lambda args: Relay()
        self.addCleanup(lambda: setattr(cli, "_relay", old))
        rc, payload = self.run_cli("send", "reconcile", "--operation-id", "op-september")
        self.assertEqual(rc, 0)
        self.assertEqual(payload["status"], "VERIFIED")
        self.assertEqual(store.get_operation("op-september")["status"], "VERIFIED")


    def _seed_uncertain_for_resolution(self, opid="op-resolve", value=881):
        store = cli.StateStore(self.data)
        store.initialize(cli.load_inventory(INV))
        store.prepare_operation(
            opid, meter_id=1003, value=value,
            observed_at="2026-09-15T09:00:00Z",
            provider_snapshot={"provider_value": 865},
            consumption={"status": "NORMAL"}, ready=True,
            created_at="2026-09-15T09:00:00Z", photo_value=value,
        )
        store.update_operation(
            opid, "UNCERTAIN_NO_RETRY",
            result={"ok": False, "status": "UNCERTAIN_NO_RETRY"},
            updated_at="2026-09-15T09:01:00Z",
        )
        return store

    @requires_fcntl
    def test_resolve_requires_explicit_user_confirmation_before_provider_contact(self):
        store = self._seed_uncertain_for_resolution()
        class NeverRelay:
            def call(self, *a, **k):
                raise AssertionError("provider must not be contacted without resolution consent")
        old = cli._relay
        cli._relay = lambda args: NeverRelay()
        self.addCleanup(lambda: setattr(cli, "_relay", old))
        rc, payload = self.run_cli("send", "resolve-not-applied", "--operation-id", "op-resolve")
        self.assertNotEqual(rc, 0)
        self.assertEqual(payload["error"], "RESOLUTION_CONFIRMATION_REQUIRED")
        self.assertFalse(payload["provider_contacted"])
        self.assertEqual(store.get_operation("op-resolve")["status"], "UNCERTAIN_NO_RETRY")

    @requires_fcntl
    def test_resolve_blocked_on_preflight_network_error(self):
        store = self._seed_uncertain_for_resolution()
        class Relay:
            def call(self, action, **payload):
                self_outer.assertEqual(action, "meters")
                raise cli.RelayNetworkError("provider unavailable")
        self_outer = self
        old = cli._relay
        cli._relay = lambda args: Relay()
        self.addCleanup(lambda: setattr(cli, "_relay", old))
        rc, payload = self.run_cli(
            "send", "resolve-not-applied", "--operation-id", "op-resolve",
            "--confirmed-not-applied-by-user",
        )
        self.assertNotEqual(rc, 0)
        self.assertEqual(payload["error"], "RESOLUTION_PREFLIGHT_NETWORK_ERROR")
        self.assertEqual(store.get_operation("op-resolve")["status"], "UNCERTAIN_NO_RETRY")

    @requires_fcntl
    def test_resolve_transitions_to_verified_if_fresh_get_proves_success(self):
        store = self._seed_uncertain_for_resolution()
        applied = self.entry(1003, 881, sent=True, status="PROCESSED", year=2026, month=9)
        calls = []
        class Relay:
            def call(_, action, **payload):
                calls.append(action)
                if action == "meters":
                    return {"ok": True, "data": [applied]}
                raise AssertionError("resolve must never POST")
        old = cli._relay
        cli._relay = lambda args: Relay()
        self.addCleanup(lambda: setattr(cli, "_relay", old))
        rc, payload = self.run_cli(
            "send", "resolve-not-applied", "--operation-id", "op-resolve",
            "--confirmed-not-applied-by-user",
        )
        self.assertEqual(rc, 0)
        self.assertEqual(payload["status"], "VERIFIED")
        self.assertFalse(payload["post_attempted"])
        self.assertEqual(calls, ["meters"])
        self.assertEqual(store.get_operation("op-resolve")["status"], "VERIFIED")

    @requires_fcntl
    def test_resolve_allows_explicit_no_history_new_meter_after_user_confirmation(self):
        store = self._seed_uncertain_for_resolution()
        new_meter = {
            "meter": {"id": 1003},
            "valueSendInfo": {
                "isAbleToSendMeterValues": True,
                "isInAllowedPeriod": True,
                "isValueSentForCurrentPeriod": False,
            },
        }
        calls = []
        class Relay:
            def call(_, action, **payload):
                calls.append(action)
                if action == "meters":
                    return {"ok": True, "data": [new_meter]}
                raise AssertionError("resolve must never POST")
        old = cli._relay
        cli._relay = lambda args: Relay()
        self.addCleanup(lambda: setattr(cli, "_relay", old))
        rc, payload = self.run_cli(
            "send", "resolve-not-applied", "--operation-id", "op-resolve",
            "--confirmed-not-applied-by-user",
        )
        self.assertEqual(rc, 0)
        self.assertEqual(payload["status"], "NOT_APPLIED")
        self.assertIsNone(payload["provider_value"])
        self.assertIsNone(payload["provider_status"])
        self.assertTrue(payload["manual_resolution"])
        self.assertEqual(calls, ["meters"])
        self.assertEqual(store.get_operation("op-resolve")["status"], "NOT_APPLIED")

    @requires_fcntl
    def test_new_meter_manual_resolution_unblocks_fresh_send_with_one_post(self):
        store = self._seed_uncertain_for_resolution()
        no_history = {
            "meter": {"id": 1003},
            "valueSendInfo": {
                "isAbleToSendMeterValues": True,
                "isInAllowedPeriod": True,
                "isValueSentForCurrentPeriod": False,
            },
        }
        class ResolveRelay:
            def call(_, action, **payload):
                if action == "meters":
                    return {"ok": True, "data": [no_history]}
                raise AssertionError("manual resolution must never POST")
        old = cli._relay
        cli._relay = lambda args: ResolveRelay()
        self.addCleanup(lambda: setattr(cli, "_relay", old))
        rc1, p1 = self.run_cli(
            "send", "resolve-not-applied", "--operation-id", "op-resolve",
            "--confirmed-not-applied-by-user",
        )
        self.assertEqual(rc1, 0)
        self.assertEqual(p1["status"], "NOT_APPLIED")
        self.assertEqual(p1["provider_state_kind"], "NO_HISTORY")

        applied = self.entry(1003, 881, sent=True, status="PROCESSED", year=2026, month=9)
        calls = []
        class SendRelay:
            def call(_, action, **payload):
                calls.append(action)
                if action == "meters":
                    return {"ok": True, "data": [no_history]}
                if action == "submit":
                    return {
                        "ok": True,
                        "provider_contacted": True,
                        "operation_id": payload["operation_id"],
                        "status": "VERIFIED",
                        "value": 881,
                        "readback_meter": applied,
                    }
                raise AssertionError(action)
        cli._relay = lambda args: SendRelay()
        rc2, p2 = self.run_cli(
            "send", "readings", "--reading", "1003:881:881",
            "--observed-at", "2026-09-23T10:05:00Z", "--confirmed-by-user",
        )
        self.assertEqual(rc2, 0)
        self.assertEqual(p2["results"][0]["status"], "VERIFIED")
        self.assertEqual(calls, ["meters", "submit"])
        self.assertEqual(store.get_operation("op-resolve")["status"], "NOT_APPLIED")

    @requires_fcntl
    def test_resolve_rejects_malformed_empty_last_value(self):
        store = self._seed_uncertain_for_resolution()
        malformed = {
            "meter": {"id": 1003, "lastValue": {}},
            "valueSendInfo": {"isValueSentForCurrentPeriod": False},
        }
        class Relay:
            def call(_, action, **payload):
                return {"ok": True, "data": [malformed]}
        old = cli._relay
        cli._relay = lambda args: Relay()
        self.addCleanup(lambda: setattr(cli, "_relay", old))
        rc, payload = self.run_cli(
            "send", "resolve-not-applied", "--operation-id", "op-resolve",
            "--confirmed-not-applied-by-user",
        )
        self.assertNotEqual(rc, 0)
        self.assertEqual(payload["error"], "PROVIDER_STATE_AMBIGUOUS")
        self.assertEqual(store.get_operation("op-resolve")["status"], "UNCERTAIN_NO_RETRY")

    @requires_fcntl
    def test_resolve_refuses_pending_provider_state(self):
        store = self._seed_uncertain_for_resolution()
        pending = self.entry(1003, 881, sent=False, status="WAITING", year=2026, month=9)
        class Relay:
            def call(_, action, **payload):
                self.assertEqual(action, "meters")
                return {"ok": True, "data": [pending]}
        old = cli._relay
        cli._relay = lambda args: Relay()
        self.addCleanup(lambda: setattr(cli, "_relay", old))
        rc, payload = self.run_cli(
            "send", "resolve-not-applied", "--operation-id", "op-resolve",
            "--confirmed-not-applied-by-user",
        )
        self.assertNotEqual(rc, 0)
        self.assertEqual(payload["error"], "PROVIDER_STATE_AMBIGUOUS")
        self.assertEqual(payload["status"], "UNCERTAIN_NO_RETRY")
        self.assertEqual(store.get_operation("op-resolve")["status"], "UNCERTAIN_NO_RETRY")

    @requires_fcntl
    def test_successful_manual_resolution_unblocks_new_send_and_preserves_audit_trail(self):
        store = self._seed_uncertain_for_resolution()
        stale = self.entry(1003, 865, sent=False, status="PROCESSED", year=2026, month=8)
        class ResolveRelay:
            def call(_, action, **payload):
                if action == "meters":
                    return {"ok": True, "data": [stale]}
                raise AssertionError("manual resolution must never POST")
        old = cli._relay
        cli._relay = lambda args: ResolveRelay()
        self.addCleanup(lambda: setattr(cli, "_relay", old))
        rc, payload = self.run_cli(
            "send", "resolve-not-applied", "--operation-id", "op-resolve",
            "--confirmed-not-applied-by-user",
        )
        self.assertEqual(rc, 0)
        self.assertEqual(payload["status"], "NOT_APPLIED")
        self.assertTrue(payload["manual_resolution"])
        self.assertTrue(payload["user_confirmed_provider_absence"])
        op = store.get_operation("op-resolve")
        self.assertEqual(op["status"], "NOT_APPLIED")
        audit = op["details"]["execute_result"]
        self.assertEqual(audit["resolution_basis"], "fresh_provider_negative_plus_user_confirmation")
        self.assertTrue(str(audit["resolved_at"]).endswith("Z"))

        after = self.entry(1003, 881, sent=True, status="PROCESSED", year=2026, month=9)
        calls = []
        class SendRelay:
            def call(_, action, **payload):
                calls.append(action)
                if action == "meters":
                    return {"ok": True, "data": [stale]}
                if action == "submit":
                    return {
                        "ok": True, "provider_contacted": True,
                        "operation_id": payload["operation_id"], "status": "VERIFIED",
                        "value": 881, "readback_meter": after,
                    }
                raise AssertionError(action)
        cli._relay = lambda args: SendRelay()
        rc2, payload2 = self.run_cli(
            "send", "readings", "--reading", "1003:881:881",
            "--observed-at", "2026-09-23T10:01:00Z", "--confirmed-by-user",
        )
        self.assertEqual(rc2, 0)
        self.assertEqual(payload2["results"][0]["status"], "VERIFIED")
        self.assertEqual(calls, ["meters", "submit"])

    @requires_fcntl
    def test_resolved_operation_id_cannot_be_reused(self):
        store = self._seed_uncertain_for_resolution()
        stale = self.entry(1003, 865, sent=False, status="PROCESSED", year=2026, month=8)
        class ResolveRelay:
            def call(_, action, **payload):
                return {"ok": True, "data": [stale]}
        old = cli._relay
        cli._relay = lambda args: ResolveRelay()
        self.addCleanup(lambda: setattr(cli, "_relay", old))
        rc, _ = self.run_cli(
            "send", "resolve-not-applied", "--operation-id", "op-resolve",
            "--confirmed-not-applied-by-user",
        )
        self.assertEqual(rc, 0)
        class NeverRelay:
            def call(self, *a, **k):
                raise AssertionError("reused operation_id must be rejected before provider contact")
        cli._relay = lambda args: NeverRelay()
        rc2, payload2 = self.run_cli(
            "send", "prepare", "--meter-id", "1003", "--value", "881",
            "--observed-at", "2026-09-23T10:02:00Z", "--operation-id", "op-resolve",
            "--confirmed-by-user",
        )
        self.assertNotEqual(rc2, 0)
        self.assertEqual(payload2["error"], "OPERATION_ID_ALREADY_EXISTS")
        rc3, payload3 = self.run_cli(
            "send", "execute", "--meter-id", "1003", "--value", "881",
            "--operation-id", "op-resolve", "--confirmed-by-user",
        )
        self.assertNotEqual(rc3, 0)
        self.assertEqual(payload3["error"], "PREPARE_REQUIRED")

    @requires_fcntl
    def test_duplicate_meter_argument_is_rejected_before_provider(self):
        class NeverRelay:
            def call(self, *a, **k):
                raise AssertionError("provider must not be contacted")
        old = cli._relay
        cli._relay = lambda args: NeverRelay()
        self.addCleanup(lambda: setattr(cli, "_relay", old))
        rc, payload = self.run_cli(
            "send", "readings",
            "--reading", "1003:881:881",
            "--reading", "1003:882:882",
            "--observed-at", "2026-09-15T09:00:00Z",
            "--confirmed-by-user",
        )
        self.assertNotEqual(rc, 0)
        self.assertEqual(payload["error"], "MosOblEIRCError")

    @requires_fcntl
    def test_reconcile_without_positive_proof_stays_uncertain(self):
        store = cli.StateStore(self.data)
        store.initialize(cli.load_inventory(INV))
        store.prepare_operation(
            "op-stale", meter_id=1003, value=881,
            observed_at="2026-09-15T09:00:00Z",
            provider_snapshot={"provider_value": 865},
            consumption={"status": "NORMAL"}, ready=True,
            created_at="2026-09-15T09:00:00Z", photo_value=881,
        )
        store.update_operation("op-stale", "EXECUTING", updated_at="2026-09-15T09:01:00Z")
        stale = self.entry(1003, 865, sent=False, status="PROCESSED", year=2026, month=8)
        class Relay:
            def call(_, action, **payload):
                self.assertEqual(action, "meters")
                return {"ok": True, "data": [stale]}
        old = cli._relay
        cli._relay = lambda args: Relay()
        self.addCleanup(lambda: setattr(cli, "_relay", old))
        rc, payload = self.run_cli("send", "reconcile", "--operation-id", "op-stale")
        self.assertNotEqual(rc, 0)
        self.assertEqual(payload["status"], "UNCERTAIN_NO_RETRY")
        self.assertEqual(store.get_operation("op-stale")["status"], "UNCERTAIN_NO_RETRY")

    @requires_fcntl
    def test_provider_success_with_local_commit_failure_stays_recoverable(self):
        before = self.entry(1003, 865, sent=False)
        after = self.entry(1003, 881, sent=True)
        class Relay:
            def call(_, action, **payload):
                if action == "meters":
                    return {"ok": True, "data": [before]}
                if action == "submit":
                    return {
                        "ok": True, "provider_contacted": True,
                        "operation_id": payload["operation_id"],
                        "status": "VERIFIED", "value": 881,
                        "readback_meter": after,
                    }
                raise AssertionError(action)
        old_relay = cli._relay
        old_commit = cli.StateStore.commit_verified_submission
        cli._relay = lambda args: Relay()
        def fail_commit(self, *a, **k):
            raise sqlite3.OperationalError("disk full")
        cli.StateStore.commit_verified_submission = fail_commit
        self.addCleanup(lambda: setattr(cli, "_relay", old_relay))
        self.addCleanup(lambda: setattr(cli.StateStore, "commit_verified_submission", old_commit))
        rc, payload = self.run_cli(
            "send", "readings", "--reading", "1003:881:881",
            "--observed-at", "2026-09-15T09:00:00Z", "--confirmed-by-user",
        )
        self.assertNotEqual(rc, 0)
        self.assertEqual(payload["results"][0]["status"], "UNCERTAIN_NO_RETRY")
        self.assertEqual(payload["results"][0]["error"], "LOCAL_COMMIT_FAILED")
        open_op = cli.StateStore(self.data).find_open_submit(1003, None, statuses=("EXECUTING",))
        self.assertIsNotNone(open_op)


if __name__ == "__main__":
    unittest.main(verbosity=2)
