import json
import os
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from send_voucher import (  # noqa: E402
    ALLOWED_OPERATION,
    ApiError,
    AuthError,
    ConfirmationRequired,
    ConfigError,
    SendVoucherError,
    ValidationError,
    build_command,
    classify_hcloud_failure,
    extract_json,
    idempotency_key,
    load_ledger,
    main,
    normalize_customer_ids,
    normalize_operation,
    parse_face_value,
    parse_response,
    read_customers_file,
    save_ledger,
    send_coupons,
    validate_inputs,
    validate_time,
)


class TestValidation(unittest.TestCase):
    def test_face_value_valid(self):
        self.assertEqual(parse_face_value("100"), "100.00")
        self.assertEqual(parse_face_value("99.5"), "99.50")
        self.assertEqual(parse_face_value("0.01"), "0.01")

    def test_face_value_missing(self):
        with self.assertRaises(ValidationError):
            parse_face_value("")
        with self.assertRaises(ValidationError):
            parse_face_value(None)

    def test_face_value_non_positive(self):
        with self.assertRaises(ValidationError):
            parse_face_value("0")
        with self.assertRaises(ValidationError):
            parse_face_value("-5")

    def test_face_value_scale(self):
        with self.assertRaises(ValidationError):
            parse_face_value("1.234")

    def test_face_value_non_numeric(self):
        with self.assertRaises(ValidationError):
            parse_face_value("abc")

    def test_time_validation(self):
        self.assertEqual(validate_time("2026-01-01T00:00:00Z", "valid-time"),
                         "2026-01-01T00:00:00Z")
        self.assertIsNone(validate_time("", "valid-time"))
        with self.assertRaises(ValidationError):
            validate_time("2026-01-01", "valid-time")

    def test_normalize_customer_ids(self):
        ids = normalize_customer_ids(["a,b", "c", "a", ""])
        self.assertEqual(ids, ["a", "b", "c"])

    def test_read_customers_file(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as fh:
            fh.write("# comment\nCUST1\n\nCUST2\n")
            path = fh.name
        try:
            self.assertEqual(read_customers_file(path), ["CUST1", "CUST2"])
        finally:
            os.unlink(path)

    def test_read_customers_file_missing(self):
        with self.assertRaises(ValidationError):
            read_customers_file("/no/such/file")

    def test_validate_inputs(self):
        self.assertTrue(validate_inputs("Q1", ["C1"], "1.00"))
        with self.assertRaises(ValidationError):
            validate_inputs("", ["C1"], "1.00")
        with self.assertRaises(ValidationError):
            validate_inputs("Q1", [], "1.00")


class TestOperationGuard(unittest.TestCase):
    def test_aliases(self):
        self.assertEqual(normalize_operation("CreatePartnerCoupons"),
                         ALLOWED_OPERATION)
        self.assertEqual(normalize_operation("send-sub-customer-coupons"),
                         ALLOWED_OPERATION)
        self.assertEqual(normalize_operation("SendCoupons"), ALLOWED_OPERATION)

    def test_unknown_passthrough(self):
        self.assertEqual(normalize_operation("ReclaimPartnerCoupons"),
                         "ReclaimPartnerCoupons")


class TestBuildCommand(unittest.TestCase):
    def test_basic(self):
        argv = build_command("cn-north-1", "Q1", ["C1", "C2"], "10.00")
        self.assertEqual(argv[0], "BSS")
        self.assertEqual(argv[1], "CreatePartnerCoupons")
        self.assertIn("--cli-region=cn-north-1", argv)
        self.assertIn("--quota_id=Q1", argv)
        self.assertIn("--customer_ids.1=C1", argv)
        self.assertIn("--customer_ids.2=C2", argv)
        self.assertIn("--face_value=10.00", argv)

    def test_optional_fields(self):
        argv = build_command(
            "cn-north-1", "Q1", ["C1"], "10.00",
            valid_time="2026-01-01T00:00:00Z",
            expire_time="2026-12-31T23:59:59Z",
            cloud_service_types=["ECS", "OBS"], product_ids=["P1"],
            memo="promo", indirect_partner_id="IP1")
        self.assertIn("--valid_time=2026-01-01T00:00:00Z", argv)
        self.assertIn("--expire_time=2026-12-31T23:59:59Z", argv)
        self.assertIn("--cloud_service_types.1=ECS", argv)
        self.assertIn("--cloud_service_types.2=OBS", argv)
        self.assertIn("--product_ids.1=P1", argv)
        self.assertIn("--memo=promo", argv)
        self.assertIn("--indirect_partner_id=IP1", argv)

    def test_no_coupon_code_parameter(self):
        # A new coupon has no code before issuance; the API never takes one.
        argv = build_command("cn-north-1", "Q1", ["C1"], "10.00")
        self.assertFalse(any(flag.startswith("--coupon_code") for flag in argv))


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
            "[USE_ERROR]Invalid parameter: face_value\n", "", 0)
        self.assertIsInstance(err, ApiError)
        self.assertIn("参数错误", str(err))


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
    def test_dict(self):
        issued, errors = parse_response({
            "coupon_infos": [{"id": "C1", "coupon_id": "CP1"}],
            "error_details": [{"id": "C2", "error_code": "x", "error_msg": "y"}],
        })
        self.assertEqual(issued, [{"id": "C1", "coupon_id": "CP1"}])
        self.assertEqual(len(errors), 1)

    def test_empty_and_list(self):
        self.assertEqual(parse_response({}), ([], []))
        self.assertEqual(parse_response([{"id": "C1"}]), ([{"id": "C1"}], []))


class TestIdempotency(unittest.TestCase):
    def test_key_stable_and_distinct(self):
        a = idempotency_key("Q1", "C1", "10.00")
        b = idempotency_key("Q1", "C1", "10.00")
        c = idempotency_key("Q1", "C2", "10.00")
        d = idempotency_key("Q1", "C1", "11.00")
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertNotEqual(a, d)

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


class TestSendCoupons(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.ledger = os.path.join(self.tmp.name, "ledger.json")

    def _call(self, **overrides):
        kwargs = dict(
            region="cn-north-1", quota_id="Q1", customer_ids=["C1", "C2"],
            face_value="10.00", confirm=True, ledger_path=self.ledger)
        kwargs.update(overrides)
        return send_coupons(**kwargs)

    def test_dry_run_no_call(self):
        with mock.patch("send_voucher.run_hcloud") as runner:
            result = self._call(dry_run=True)
        runner.assert_not_called()
        self.assertTrue(result["dry_run"])
        self.assertIn("--quota_id=Q1", result["command"])
        self.assertFalse(os.path.exists(self.ledger))

    def test_confirm_required(self):
        with mock.patch("send_voucher.run_hcloud") as runner:
            with self.assertRaises(ConfirmationRequired):
                self._call(confirm=False)
        runner.assert_not_called()

    def test_success_records_ledger_and_skips(self):
        payload = json.dumps({"coupon_infos": [
            {"id": "C1", "coupon_id": "CP1"},
            {"id": "C2", "coupon_id": "CP2"},
        ], "error_details": []})
        with mock.patch("send_voucher.run_hcloud", return_value=(payload, "", 0)):
            first = self._call()
        self.assertEqual(len(first["issued"]), 2)
        self.assertEqual(first["errors"], [])
        self.assertTrue(os.path.exists(self.ledger))

        with mock.patch("send_voucher.run_hcloud") as runner:
            second = self._call()
        runner.assert_not_called()
        self.assertEqual(len(second["skipped"]), 2)
        self.assertEqual(second["reason"], "all_skipped_by_idempotency")

    def test_force_resends(self):
        payload = json.dumps({"coupon_infos": [{"id": "C1", "coupon_id": "CP1"}],
                              "error_details": []})
        with mock.patch("send_voucher.run_hcloud", return_value=(payload, "", 0)):
            self._call(customer_ids=["C1"])
        with mock.patch("send_voucher.run_hcloud",
                        return_value=(payload, "", 0)) as runner:
            result = self._call(customer_ids=["C1"], force=True)
        runner.assert_called_once()
        self.assertEqual(len(result["issued"]), 1)

    def test_partial_errors_captured(self):
        payload = json.dumps({
            "coupon_infos": [{"id": "C1", "coupon_id": "CP1"}],
            "error_details": [{"id": "C2", "error_code": "BSS.001",
                               "error_msg": "quota not enough"}],
        })
        with mock.patch("send_voucher.run_hcloud", return_value=(payload, "", 0)):
            result = self._call()
        self.assertEqual(len(result["issued"]), 1)
        self.assertEqual(len(result["errors"]), 1)

    def test_sdk_fallback_when_hcloud_missing(self):
        with mock.patch("send_voucher.run_hcloud",
                        side_effect=ConfigError("hcloud missing")), \
                mock.patch("send_voucher.send_via_sdk",
                           return_value={"coupon_infos": [{"id": "C1",
                                                           "coupon_id": "CP1"}],
                                         "error_details": []}) as sdk:
            result = self._call(customer_ids=["C1"])
        sdk.assert_called_once()
        self.assertEqual(len(result["issued"]), 1)

    def test_auth_error_propagates(self):
        with mock.patch("send_voucher.run_hcloud",
                        return_value=("", "403 Forbidden", 1)):
            with self.assertRaises(AuthError):
                self._call()


class TestMain(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.ledger = os.path.join(self.tmp.name, "ledger.json")

    def _argv(self, *extra):
        return ["--quota-id", "Q1", "--face-value", "10.00",
                "--customer-id", "C1", "--ledger", self.ledger] + list(extra)

    def test_dry_run_exit_zero(self):
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with mock.patch("send_voucher.run_hcloud") as runner, \
                redirect_stdout(buf):
            rc = main(self._argv("--dry-run"))
        self.assertEqual(rc, 0)
        runner.assert_not_called()
        self.assertIn("DRY-RUN", buf.getvalue())

    def test_confirm_required_exit_two(self):
        with mock.patch("send_voucher.run_hcloud") as runner:
            rc = main(self._argv())
        self.assertEqual(rc, 2)
        runner.assert_not_called()

    def test_success_exit_zero(self):
        payload = json.dumps({"coupon_infos": [{"id": "C1", "coupon_id": "CP1"}],
                              "error_details": []})
        with mock.patch("send_voucher.run_hcloud", return_value=(payload, "", 0)):
            rc = main(self._argv("--confirm"))
        self.assertEqual(rc, 0)

    def test_partial_error_exit_one(self):
        payload = json.dumps({"coupon_infos": [],
                              "error_details": [{"id": "C1",
                                                 "error_code": "x",
                                                 "error_msg": "y"}]})
        with mock.patch("send_voucher.run_hcloud", return_value=(payload, "", 0)):
            rc = main(self._argv("--confirm"))
        self.assertEqual(rc, 1)

    def test_validation_error_exit_one(self):
        rc = main(["--quota-id", "Q1", "--face-value", "0",
                   "--customer-id", "C1", "--confirm"])
        self.assertEqual(rc, 1)

    def test_json_output(self):
        import io
        from contextlib import redirect_stdout
        payload = json.dumps({"coupon_infos": [{"id": "C1", "coupon_id": "CP1"}],
                              "error_details": []})
        buf = io.StringIO()
        with mock.patch("send_voucher.run_hcloud",
                        return_value=(payload, "", 0)), redirect_stdout(buf):
            rc = main(self._argv("--confirm", "--json"))
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(buf.getvalue())["issued"][0]["coupon_id"],
                         "CP1")


class TestErrorHierarchy(unittest.TestCase):
    def test_subclasses(self):
        for exc in (ConfigError, AuthError, ApiError, ConfirmationRequired):
            self.assertTrue(issubclass(exc, SendVoucherError))
        self.assertTrue(issubclass(ValidationError, ConfigError))


if __name__ == "__main__":
    unittest.main()