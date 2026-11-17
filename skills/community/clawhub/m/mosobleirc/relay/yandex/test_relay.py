from __future__ import annotations

import importlib.util
import os
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().with_name("index.py")
spec = importlib.util.spec_from_file_location("relay_write_test", SRC)
relay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(relay)


class RelayWriteTests(unittest.TestCase):
    def setUp(self):
        self.old_writes = os.environ.get("ALLOW_WRITES")
        self.old_token = os.environ.get("MOSOBLEIRC_TOKEN")
        self.old_inventory = relay._load_inventory
        os.environ["ALLOW_WRITES"] = "true"
        os.environ["MOSOBLEIRC_TOKEN"] = "test-token"
        relay._load_inventory = lambda strict=False: [
            {"item_id": 9001, "meters": [{"meter_id": 1001}]}
        ]
        self.addCleanup(self.restore)

    def restore(self):
        if self.old_writes is None:
            os.environ.pop("ALLOW_WRITES", None)
        else:
            os.environ["ALLOW_WRITES"] = self.old_writes
        if self.old_token is None:
            os.environ.pop("MOSOBLEIRC_TOKEN", None)
        else:
            os.environ["MOSOBLEIRC_TOKEN"] = self.old_token
        relay._load_inventory = self.old_inventory

    def payload(self, **kw):
        p = {"action": "submit", "operation_id": "op-123", "item_id": 9001, "meter_id": 1001, "value": 881}
        p.update(kw)
        return p

    @staticmethod
    def entry(value=881, *, sent=True, status="PROCESSED"):
        return {
            "meter": {
                "id": 1001,
                "lastValue": {
                    "id": 77,
                    "total": {"value": value},
                    "status": status,
                    "settlementPeriod": {"year": 2026, "month": 9},
                },
            },
            "valueSendInfo": {"isValueSentForCurrentPeriod": sent},
        }

    def patch_io(self, write, read):
        old_write = relay._write_once
        old_get = relay._live_get
        relay._write_once = write
        relay._live_get = read
        self.addCleanup(lambda: setattr(relay, "_write_once", old_write))
        self.addCleanup(lambda: setattr(relay, "_live_get", old_get))

    def test_write_status_is_local_and_reflects_env(self):
        status, r = relay.dispatch({"action": "write-status"})
        self.assertEqual(status, 200)
        self.assertTrue(r["ok"])
        self.assertTrue(r["writes_enabled"])
        self.assertFalse(r["provider_contacted"])

    def test_submit_requires_operation_id(self):
        status, r = relay.dispatch(self.payload(operation_id=""))
        self.assertEqual(status, 400)
        self.assertEqual(r["error"], "OPERATION_ID_REQUIRED")

    def test_submit_rejects_non_integer_value(self):
        status, r = relay.dispatch(self.payload(value=881.5))
        self.assertEqual(status, 400)
        self.assertEqual(r["error"], "INVALID_VALUE")

    def test_submit_rejects_meter_not_bound_to_item_in_deployment_inventory(self):
        status, r = relay.dispatch(self.payload(item_id=9999))
        self.assertEqual(status, 400)
        self.assertEqual(r["error"], "METER_BINDING_MISMATCH")
        self.assertFalse(r["provider_contacted"])

    def test_successful_post_is_called_once_then_verified_by_strong_readback(self):
        calls = {"post": 0, "get": 0}
        def write(path, token, payload, timeout=10):
            calls["post"] += 1
            return 200, {"ok": True}
        def read(path):
            calls["get"] += 1
            return [self.entry()]
        self.patch_io(write, read)
        status, r = relay.dispatch(self.payload())
        self.assertEqual(status, 200)
        self.assertEqual(r["status"], "VERIFIED")
        self.assertEqual(calls, {"post": 1, "get": 1})

    def test_timeout_never_reposts_and_strong_readback_can_verify(self):
        calls = {"post": 0, "get": 0}
        def write(path, token, payload, timeout=10):
            calls["post"] += 1
            raise relay.NetworkError("lost response")
        def read(path):
            calls["get"] += 1
            return [self.entry()]
        self.patch_io(write, read)
        status, r = relay.dispatch(self.payload())
        self.assertEqual(status, 200)
        self.assertEqual(r["status"], "VERIFIED_AFTER_UNCERTAIN_RESPONSE")
        self.assertEqual(calls, {"post": 1, "get": 1})

    def test_timeout_same_old_value_from_previous_period_is_not_verified(self):
        calls = {"post": 0, "get": 0}
        def write(path, token, payload, timeout=10):
            calls["post"] += 1
            raise relay.NetworkError("lost response")
        def read(path):
            calls["get"] += 1
            return [self.entry(881, sent=False, status="PROCESSED")]
        self.patch_io(write, read)
        status, r = relay.dispatch(self.payload())
        self.assertEqual(status, 202)
        self.assertEqual(r["status"], "UNCERTAIN_NO_RETRY")
        self.assertEqual(calls, {"post": 1, "get": 1})

    def test_http_504_after_post_uses_readback_instead_of_failed(self):
        calls = {"post": 0, "get": 0}
        def write(path, token, payload, timeout=10):
            calls["post"] += 1
            return 504, {"raw": "gateway timeout"}
        def read(path):
            calls["get"] += 1
            return [self.entry()]
        self.patch_io(write, read)
        status, r = relay.dispatch(self.payload())
        self.assertEqual(status, 200)
        self.assertEqual(r["status"], "VERIFIED_AFTER_UNCERTAIN_RESPONSE")
        self.assertEqual(r["upstream_status"], 504)
        self.assertEqual(calls, {"post": 1, "get": 1})

    def test_http_504_without_proof_stays_uncertain(self):
        def write(path, token, payload, timeout=10):
            return 504, {"raw": "gateway timeout"}
        def read(path):
            return [self.entry(865, sent=False)]
        self.patch_io(write, read)
        status, r = relay.dispatch(self.payload())
        self.assertEqual(status, 202)
        self.assertEqual(r["status"], "UNCERTAIN_NO_RETRY")

    def test_http_200_application_error_without_proof_stays_uncertain(self):
        def write(path, token, payload, timeout=10):
            return 200, {"success": False, "error": "Validation failed"}
        def read(path):
            return [self.entry(865, sent=False)]
        self.patch_io(write, read)
        status, r = relay.dispatch(self.payload())
        self.assertEqual(status, 202)
        self.assertEqual(r["status"], "UNCERTAIN_NO_RETRY")

    def test_same_value_waiting_status_is_not_verified(self):
        def write(path, token, payload, timeout=10):
            return 200, {"ok": True}
        def read(path):
            return [self.entry(881, sent=True, status="WAITING")]
        self.patch_io(write, read)
        status, r = relay.dispatch(self.payload())
        self.assertEqual(status, 202)
        self.assertEqual(r["status"], "UNCERTAIN_NO_RETRY")

    def test_missing_deployment_inventory_fails_closed_before_post(self):
        relay._load_inventory = lambda strict=False: (_ for _ in ()).throw(
            relay.ApiError(503, {"errorCode": "INVENTORY_NOT_CONFIGURED"})
        ) if strict else []
        called = {"post": 0}
        old_write = relay._write_once
        relay._write_once = lambda *a, **k: called.__setitem__("post", called["post"] + 1)
        self.addCleanup(lambda: setattr(relay, "_write_once", old_write))
        status, r = relay.dispatch(self.payload())
        self.assertEqual(status, 503)
        self.assertEqual(r["error"], "INVENTORY_NOT_CONFIGURED")
        self.assertFalse(r["provider_contacted"])
        self.assertEqual(called["post"], 0)

    def test_handler_scrubs_unexpected_exception_and_does_not_echo_token(self):
        old_dispatch = relay.dispatch
        relay.dispatch = lambda payload: (_ for _ in ()).throw(RuntimeError(os.environ["MOSOBLEIRC_TOKEN"]))
        self.addCleanup(lambda: setattr(relay, "dispatch", old_dispatch))
        response = relay.handler({"action": "status"}, None)
        self.assertEqual(response["statusCode"], 500)
        self.assertNotIn(os.environ["MOSOBLEIRC_TOKEN"], response["body"])
        self.assertIn("INTERNAL_ERROR", response["body"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
