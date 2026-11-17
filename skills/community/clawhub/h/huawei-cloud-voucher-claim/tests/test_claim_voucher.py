import json
import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest import mock

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from claim_voucher import (  # noqa: E402
    CLAIM_OPERATION,
    ApiError,
    AuthError,
    ClaimVoucherError,
    ConfirmationRequired,
    ConfigError,
    ValidationError,
    build_command,
    build_list_command,
    claim_voucher,
    classify_hcloud_failure,
    derive_trans_id,
    extract_coupons,
    extract_json,
    filter_coupons,
    guard_operation,
    idempotency_key,
    load_ledger,
    main,
    normalize_operation,
    parse_amount,
    parse_claim_response,
    save_ledger,
    validate_inputs,
)


class TestValidation(unittest.TestCase):
    def test_amount_valid(self):
        self.assertEqual(parse_amount("100"), "100.00")
        self.assertEqual(parse_amount("99.5"), "99.50")
        self.assertEqual(parse_amount("0.01"), "0.01")

    def test_amount_missing(self):
        with self.assertRaises(ValidationError):
            parse_amount("")
        with self.assertRaises(ValidationError):
            parse_amount(None)

    def test_amount_non_positive(self):
        with self.assertRaises(ValidationError):
            parse_amount("0")
        with self.assertRaises(ValidationError):
            parse_amount("-5")

    def test_amount_scale(self):
        with self.assertRaises(ValidationError):
            parse_amount("1.234")

    def test_amount_non_numeric(self):
        with self.assertRaises(ValidationError):
            parse_amount("abc")

    def test_validate_inputs(self):
        self.assertTrue(validate_inputs("C1", "CP1", "1.00"))
        with self.assertRaises(ValidationError):
            validate_inputs("", "CP1", "1.00")
        with self.assertRaises(ValidationError):
            validate_inputs("C1", "", "1.00")

    def test_derive_trans_id(self):
        a = derive_trans_id("C1", "CP1", "10.00")
        b = derive_trans_id("C1", "CP1", "10.00")
        c = derive_trans_id("C1", "CP2", "10.00")
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertEqual(len(a), 32)


class TestOperationGuard(unittest.TestCase):
    def test_aliases(self):
        self.assertEqual(normalize_operation("ClaimEnterpriseMultiAccountCoupon"),
                         CLAIM_OPERATION)
        self.assertEqual(normalize_operation("claim-coupon"), CLAIM_OPERATION)
        self.assertEqual(normalize_operation("ClaimVoucher"), CLAIM_OPERATION)

    def test_unknown_passthrough(self):
        self.assertEqual(normalize_operation("ReclaimEnterpriseMultiAccountCoupon"),
                         "ReclaimEnterpriseMultiAccountCoupon")

    def test_guard_blocks_others(self):
        with self.assertRaises(ValidationError):
            guard_operation("ReclaimEnterpriseMultiAccountCoupon")
        self.assertEqual(guard_operation("ClaimCoupon"), CLAIM_OPERATION)


class TestBuildCommand(unittest.TestCase):
    def test_basic(self):
        argv = build_command("cn-north-1", "C1", "CP1", "10.00")
        self.assertEqual(argv[0], "BSS")
        self.assertEqual(argv[1], "ClaimEnterpriseMultiAccountCoupon")
        self.assertIn("--cli-region=cn-north-1", argv)
        self.assertIn("--customer_id=C1", argv)
        self.assertIn("--coupon_id=CP1", argv)
        self.assertIn("--amount=10.00", argv)

    def test_trans_id_optional(self):
        argv = build_command("cn-north-1", "C1", "CP1", "10.00",
                             trans_id="T123")
        self.assertIn("--trans_id=T123", argv)
        argv2 = build_command("cn-north-1", "C1", "CP1", "10.00")
        self.assertFalse(any(f.startswith("--trans_id") for f in argv2))

    def test_no_face_value_parameter(self):
        # The claim API takes amount (总划拨金额), never a face_value/quota.
        argv = build_command("cn-north-1", "C1", "CP1", "10.00")
        self.assertFalse(any(f.startswith("--face_value") for f in argv))
        self.assertFalse(any(f.startswith("--quota_id") for f in argv))

    def test_list_command(self):
        argv = build_list_command("cn-north-1", coupon_id="CP1", limit=50,
                                  offset=100)
        self.assertEqual(argv[0], "BSS")
        self.assertEqual(argv[1], "ListSubCustomerCoupons")
        self.assertIn("--cli-region=cn-north-1", argv)
        self.assertIn("--offset=100", argv)
        self.assertIn("--limit=50", argv)
        self.assertIn("--coupon_id=CP1", argv)


class TestClassifyFailure(unittest.TestCase):
    def test_missing_credentials(self):
        err = classify_hcloud_failure(
            "", "ERROR: cli-ak is empty, please run hcloud configure", 1)
        self.assertIsInstance(err, ConfigError)

    def test_auth_403(self):
        err = classify_hcloud_failure(
            "", '{"error_code":"ApiGW.0301","error_msg":"403 Forbidden"}', 1)
        self.assertIsInstance(err, AuthError)
        self.assertIn("IAM", str(err))

    def test_generic(self):
        self.assertIsInstance(classify_hcloud_failure("", "boom", 2), ApiError)

    def test_use_error_zero_rc(self):
        err = classify_hcloud_failure(
            "[USE_ERROR]Invalid parameter: amount\n", "", 0)
        self.assertIsInstance(err, ApiError)
        self.assertIn("参数错误", str(err))

    def test_duplicate_trans_id(self):
        err = classify_hcloud_failure(
            "", '{"error_code":"CBC.99007009","error_msg":"交易事务ID重复"}', 1)
        self.assertIsInstance(err, ApiError)
        self.assertIn("trans_id", str(err))

    def test_unsupported_service_is_config_error(self):
        # KooCLI has no BSS service -> CLI unavailable -> SDK fallback path.
        err = classify_hcloud_failure(
            "[USE_ERROR]Unsupported service: BSS.", "", 1)
        self.assertIsInstance(err, ConfigError)


class TestExtractJson(unittest.TestCase):
    def test_plain_and_noisy(self):
        self.assertEqual(extract_json('{"a":1}'), {"a": 1})
        self.assertEqual(extract_json('noise\n{"a":1}\n'), {"a": 1})

    def test_invalid(self):
        with self.assertRaises(ApiError):
            extract_json("<html>nope</html>")

    def test_empty(self):
        self.assertEqual(extract_json(""), {})


class TestParseResponse(unittest.TestCase):
    def test_claim_response(self):
        self.assertEqual(parse_claim_response({"sub_coupon_id": "CP9"}), "CP9")
        self.assertIsNone(parse_claim_response({}))
        self.assertIsNone(parse_claim_response(None))

    def test_extract_coupons(self):
        self.assertEqual(extract_coupons({"user_coupons": [{"coupon_id": "x"}]}),
                         [{"coupon_id": "x"}])
        self.assertEqual(extract_coupons([]), [])
        self.assertEqual(extract_coupons({"other": 1}), [])

    def test_filter_coupons(self):
        coupons = [
            {"coupon_id": "CP1", "customer_id": "C1"},
            {"coupon_id": "CP2", "customer_id": "C2"},
        ]
        self.assertEqual(len(filter_coupons(coupons, coupon_id="CP1")), 1)
        self.assertEqual(len(filter_coupons(coupons, customer_id="C2")), 1)
        self.assertEqual(len(filter_coupons(coupons)), 2)


class TestIdempotency(unittest.TestCase):
    def test_key_stable_and_distinct(self):
        a = idempotency_key("C1", "CP1", "10.00")
        b = idempotency_key("C1", "CP1", "10.00")
        c = idempotency_key("C1", "CP2", "10.00")
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)

    def test_load_save_and_prune(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "ledger.json")
            now = 1000.0
            save_ledger(path, {
                "fresh": {"at": now - 10},
                "stale": {"at": now - 100000},
            })
            loaded = load_ledger(path, window=100, now=now)
            self.assertIn("fresh", loaded)
            self.assertNotIn("stale", loaded)

    def test_load_missing_is_empty(self):
        self.assertEqual(load_ledger("/no/such/ledger.json"), {})


class TestClaimVoucher(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.ledger = os.path.join(self.tmp.name, "ledger.json")

    def _call(self, **overrides):
        kwargs = dict(
            region="cn-north-1", customer_id="C1", coupon_id="CP1",
            amount="10.00", confirm=True, ledger_path=self.ledger,
            list_after=False)
        kwargs.update(overrides)
        return claim_voucher(**kwargs)

    def test_dry_run_no_call(self):
        with mock.patch("claim_voucher.run_hcloud") as runner:
            result = self._call(dry_run=True)
        runner.assert_not_called()
        self.assertTrue(result["dry_run"])
        self.assertIn("--coupon_id=CP1", result["command"])
        self.assertFalse(os.path.exists(self.ledger))

    def test_confirm_required(self):
        with mock.patch("claim_voucher.run_hcloud") as runner:
            with self.assertRaises(ConfirmationRequired):
                self._call(confirm=False)
        runner.assert_not_called()

    def test_success_records_ledger_and_skips(self):
        payload = json.dumps({"sub_coupon_id": "SUB1"})
        with mock.patch("claim_voucher.run_hcloud", return_value=(payload, "", 0)):
            first = self._call()
        self.assertTrue(first["claimed"])
        self.assertEqual(first["sub_coupon_id"], "SUB1")
        self.assertTrue(os.path.exists(self.ledger))

        with mock.patch("claim_voucher.run_hcloud") as runner:
            second = self._call()
        runner.assert_not_called()
        self.assertTrue(second["skipped"])
        self.assertEqual(second["reason"], "already_claimed_in_window")
        self.assertEqual(second["sub_coupon_id"], "SUB1")

    def test_force_resends(self):
        payload = json.dumps({"sub_coupon_id": "SUB1"})
        with mock.patch("claim_voucher.run_hcloud", return_value=(payload, "", 0)):
            self._call()
        with mock.patch("claim_voucher.run_hcloud",
                        return_value=(payload, "", 0)) as runner:
            result = self._call(force=True)
        runner.assert_called_once()
        self.assertTrue(result["claimed"])

    def test_list_after_claim(self):
        claim_payload = json.dumps({"sub_coupon_id": "SUB1"})
        list_payload = json.dumps({"user_coupons": [
            {"coupon_id": "CP1", "coupon_code": "CP1", "status": 2,
             "face_value": "100", "balance": "100", "customer_id": "C1"},
        ]})

        def fake_run(argv):
            if argv[1] == "ClaimEnterpriseMultiAccountCoupon":
                return claim_payload, "", 0
            return list_payload, "", 0

        with mock.patch("claim_voucher.run_hcloud", side_effect=fake_run):
            result = self._call(list_after=True)
        self.assertEqual(len(result["coupons"]), 1)
        self.assertEqual(result["list_used_cli"], True)

    def test_sdk_fallback_when_hcloud_missing(self):
        with mock.patch("claim_voucher.run_hcloud",
                        side_effect=ConfigError("hcloud missing")), \
                mock.patch("claim_voucher.claim_via_sdk",
                           return_value={"sub_coupon_id": "SUB9"}) as sdk:
            result = self._call()
        sdk.assert_called_once()
        self.assertEqual(result["sub_coupon_id"], "SUB9")

    def test_sdk_fallback_when_service_unsupported(self):
        # hcloud exists but reports "Unsupported service: BSS" (rc != 0).
        with mock.patch("claim_voucher.run_hcloud",
                        return_value=("[USE_ERROR]Unsupported service: BSS.",
                                      "", 1)), \
                mock.patch("claim_voucher.claim_via_sdk",
                           return_value={"sub_coupon_id": "SUB7"}) as sdk:
            result = self._call()
        sdk.assert_called_once()
        self.assertEqual(result["sub_coupon_id"], "SUB7")

    def test_auth_error_propagates(self):
        with mock.patch("claim_voucher.run_hcloud",
                        return_value=("", "403 Forbidden", 1)):
            with self.assertRaises(AuthError):
                self._call()


class TestMain(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.ledger = os.path.join(self.tmp.name, "ledger.json")

    def _argv(self, *extra):
        return ["--customer-id", "C1", "--coupon-id", "CP1",
                "--amount", "10.00", "--ledger", self.ledger,
                "--no-list"] + list(extra)

    def test_dry_run_exit_zero(self):
        buf = io.StringIO()
        with mock.patch("claim_voucher.run_hcloud") as runner, \
                redirect_stdout(buf):
            rc = main(self._argv("--dry-run"))
        self.assertEqual(rc, 0)
        runner.assert_not_called()
        self.assertIn("DRY-RUN", buf.getvalue())

    def test_confirm_required_exit_two(self):
        with mock.patch("claim_voucher.run_hcloud") as runner:
            rc = main(self._argv())
        self.assertEqual(rc, 2)
        runner.assert_not_called()

    def test_success_exit_zero(self):
        payload = json.dumps({"sub_coupon_id": "SUB1"})
        with mock.patch("claim_voucher.run_hcloud", return_value=(payload, "", 0)):
            rc = main(self._argv("--confirm"))
        self.assertEqual(rc, 0)

    def test_validation_error_exit_one(self):
        rc = main(["--customer-id", "C1", "--coupon-id", "CP1",
                   "--amount", "0", "--confirm"])
        self.assertEqual(rc, 1)

    def test_json_output(self):
        payload = json.dumps({"sub_coupon_id": "SUB1"})
        buf = io.StringIO()
        with mock.patch("claim_voucher.run_hcloud",
                        return_value=(payload, "", 0)), redirect_stdout(buf):
            rc = main(self._argv("--confirm", "--json"))
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(buf.getvalue())["sub_coupon_id"], "SUB1")


class TestErrorHierarchy(unittest.TestCase):
    def test_subclasses(self):
        for exc in (ConfigError, AuthError, ApiError, ConfirmationRequired):
            self.assertTrue(issubclass(exc, ClaimVoucherError))
        self.assertTrue(issubclass(ValidationError, ConfigError))


if __name__ == "__main__":
    unittest.main()