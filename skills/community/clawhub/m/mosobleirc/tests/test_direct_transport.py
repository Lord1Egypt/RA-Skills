import http.client
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tests"))

from _posix import requires_posix
from direct_transport import DirectClient, provider_base_url, read_token
from mosobleirc_core import MosOblEIRCError


class DirectTransportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.token = self.root / "provider_token"
        self.token.write_text("test-secret", encoding="utf-8")
        self.token.chmod(0o600)
        self.inventory = self.root / "inventory.json"
        self.inventory.write_text(
            json.dumps([{"item_id": 101, "meters": [{"meter_id": 201}]}]),
            encoding="utf-8",
        )
        self.opener = Mock()
        self.client = DirectClient(
            self.token,
            self.inventory,
            opener=self.opener,
            sleep=lambda _: None,
        )

    @staticmethod
    def response(data, status=200):
        response = Mock(status=status)
        response.read.return_value = json.dumps(data).encode()
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)
        return response

    @staticmethod
    def meter_entry(value, *, sent):
        return {
            "meter": {
                "id": 201,
                "lastValue": {
                    "total": {"value": value},
                    "receivedDate": "2026-09-24T09:00:00Z",
                    "status": "PROCESSED",
                    "settlementPeriod": {"year": 2026, "month": 9},
                },
            },
            "valueSendInfo": {
                "isValueSentForCurrentPeriod": sent,
                "isAbleToSendMeterValues": True,
                "isInAllowedPeriod": True,
            },
        }

    def test_get_contract_and_token_header(self):
        self.opener.return_value = self.response([])
        result = self.client.call("items")
        self.assertEqual(result, {"ok": True, "provider_contacted": True, "data": []})
        request = self.opener.call_args.args[0]
        self.assertEqual(request.get_header("X-auth-tenant-token"), "test-secret")
        self.assertEqual(request.method, "GET")

    @requires_posix
    def test_read_network_failure_has_bounded_retry(self):
        self.opener.side_effect = http.client.RemoteDisconnected("sensitive")
        result = self.client.call("items")
        self.assertEqual(result["error"], "RETRYABLE_EGRESS")
        self.assertEqual(self.opener.call_count, 2)
        self.assertNotIn("sensitive", str(result))

    def test_successful_post_requires_matching_current_period_readback(self):
        self.opener.side_effect = [
            self.response({}, 200),
            self.response([self.meter_entry(321, sent=True)], 200),
        ]
        result = self.client.call(
            "submit", operation_id="op-1", item_id=101, meter_id=201, value=321
        )
        self.assertEqual(result["status"], "VERIFIED")
        self.assertEqual(
            [x.args[0].method for x in self.opener.call_args_list], ["POST", "GET"]
        )

    def test_successful_post_without_proof_is_uncertain(self):
        self.opener.side_effect = [
            self.response({}, 200),
            self.response([self.meter_entry(320, sent=False)], 200),
        ]
        result = self.client.call(
            "submit", operation_id="op-2", item_id=101, meter_id=201, value=321
        )
        self.assertEqual(result["status"], "UNCERTAIN_NO_RETRY")
        self.assertEqual(self.opener.call_count, 2)

    def test_uncertain_post_is_never_retried_and_can_verify_by_readback(self):
        errors = [
            TimeoutError("sensitive"),
            http.client.IncompleteRead(b"sensitive"),
            http.client.RemoteDisconnected("sensitive"),
        ]
        for error in errors:
            with self.subTest(error=type(error)):
                self.opener.reset_mock()
                self.opener.side_effect = [
                    error,
                    self.response([self.meter_entry(321, sent=True)], 200),
                ]
                result = self.client.call(
                    "submit",
                    operation_id="op-u",
                    item_id=101,
                    meter_id=201,
                    value=321,
                )
                self.assertEqual(
                    result["status"], "VERIFIED_AFTER_UNCERTAIN_RESPONSE"
                )
                self.assertEqual(
                    [x.args[0].method for x in self.opener.call_args_list],
                    ["POST", "GET"],
                )
                self.assertNotIn("sensitive", str(result))

    def test_transient_write_status_does_readback_but_no_second_post(self):
        self.opener.side_effect = [
            urllib_error(503),
            self.response([self.meter_entry(320, sent=False)], 200),
        ]
        result = self.client.call(
            "submit", operation_id="op-503", item_id=101, meter_id=201, value=321
        )
        self.assertEqual(result["status"], "UNCERTAIN_NO_RETRY")
        self.assertEqual(
            [x.args[0].method for x in self.opener.call_args_list], ["POST", "GET"]
        )

    def test_auth_failure_is_not_retried(self):
        self.opener.side_effect = urllib_error(401)
        result = self.client.call(
            "submit", operation_id="op-auth", item_id=101, meter_id=201, value=321
        )
        self.assertEqual(result["status"], "AUTH_REQUIRED")
        self.assertEqual(self.opener.call_count, 1)

    def test_binding_rejected_without_network(self):
        result = self.client.call(
            "submit", operation_id="op-x", item_id=101, meter_id=999, value=3
        )
        self.assertEqual(result["error"], "METER_BINDING_MISMATCH")
        self.opener.assert_not_called()

    def test_local_actions_do_not_read_process_secrets_or_network(self):
        with patch.dict(
            os.environ,
            {"MOSOBLEIRC_TOKEN": "wrong", "ALLOW_WRITES": "false"},
            clear=False,
        ):
            self.assertTrue(self.client.call("write-status")["writes_enabled"])
            self.assertTrue(self.client.call("ping")["ok"])
            self.assertTrue(self.client.call("inventory")["ok"])
        self.opener.assert_not_called()

    @requires_posix
    def test_secret_permissions_and_symlink_are_rejected(self):
        self.token.chmod(0o644)
        with self.assertRaises(MosOblEIRCError):
            read_token(self.token)
        self.token.chmod(0o600)
        link = self.root / "token-link"
        link.symlink_to(self.token)
        with self.assertRaises(MosOblEIRCError):
            read_token(link)

    def test_provider_origin_rejects_credentials_paths_and_nonstandard_ports(self):
        for value in (
            "http://lkk.mosobleirc.ru",
            "https://" + "user" + ":" + "pass" + "@" + "lkk.mosobleirc.ru",
            "https://example.invalid/path",
            "https://example.invalid:8443",
        ):
            with self.subTest(value=value), self.assertRaises(MosOblEIRCError):
                provider_base_url(value)

    @requires_posix
    def test_direct_bundle_is_independent_from_yandex_relay_source(self):
        bundle = self.root / "bundle"
        shutil.copytree(
            ROOT / "scripts",
            bundle / "scripts",
            ignore=shutil.ignore_patterns("__pycache__"),
        )
        result = subprocess.run(
            [
                sys.executable,
                str(bundle / "scripts" / "mosobleirc.py"),
                "--data-root",
                str(self.root / "data"),
                "--transport",
                "direct",
                "--inventory",
                str(self.inventory),
                "--provider-token-file",
                str(self.token),
                "relay",
                "ping",
            ],
            cwd=self.root,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(json.loads(result.stdout)["provider_contacted"])


def urllib_error(code):
    import urllib.error
    return urllib.error.HTTPError(
        "https://lkk.mosobleirc.ru/test", code, "error", {}, None
    )


if __name__ == "__main__":
    unittest.main(verbosity=2)
