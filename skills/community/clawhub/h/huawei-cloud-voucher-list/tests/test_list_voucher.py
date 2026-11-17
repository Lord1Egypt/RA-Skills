import json
import os
import subprocess
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from list_voucher import (  # noqa: E402
    ALLOWED_OPERATION,
    ApiError,
    AuthError,
    ConfigError,
    GuardError,
    VoucherListError,
    build_command,
    classify_hcloud_failure,
    coupon_names,
    extract_coupons,
    extract_json,
    filter_by_name,
    filter_by_status,
    guard_operation,
    guard_write_intent,
    list_coupons,
    list_coupons_via_sdk,
    main,
    normalize_coupon,
    normalize_operation,
    parse_status,
    render_table,
)

COUPON_1 = {
    "coupon_id": "CP0001",
    "coupon_code": "CODE-0001",
    "status": 2,
    "coupon_type": 1,
    "face_value": 100.0,
    "balance": 80.0,
    "currency": "CNY",
    "plan_name": "spring-voucher",
    "valid_time": "2026-01-01T00:00:00Z",
    "expire_time": "2026-12-31T23:59:59Z",
    "order_id": "ORD1",
    "promotion_plan_id": "PLAN1",
    "customer_id": "CUST1",
    "source_id": "SRC1",
    "use_limits": [{"limit_key": "service", "limit_value": "ECS"}],
}
COUPON_2 = {
    "coupon_id": "CP0002",
    "coupon_code": "CODE-0002",
    "status": 3,
    "coupon_type": 2,
    "face_value": 50.0,
    "balance": 0.0,
    "plan_name": "discount-A",
    "expire_time": "2026-06-30T00:00:00Z",
}


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
        self.assertFalse(guard_write_intent("--region cn-north-1 --json list coupons"))
        self.assertFalse(guard_write_intent("show voucher details"))

    def test_status_label_reclaimed_not_blocked(self):
        # "reclaimed" is a legitimate read-only status label and must NOT trip
        # the guard even though "reclaim*" operations are mutating.
        self.assertFalse(guard_write_intent("--status reclaimed"))
        self.assertFalse(guard_write_intent("--status used"))
        self.assertFalse(guard_write_intent("--status available"))

    def test_create_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("CreatePartnerCoupons")

    def test_reclaim_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--operation ReclaimPartnerCoupons")

    def test_mutating_verbs_blocked(self):
        for text in ("update coupon quotas", "transfer coupon",
                     "retrieve coupon", "adjust quota", "send coupon",
                     "freeze coupon", "delete coupon"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_normalized_separators_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--create-coupon")
        with self.assertRaises(GuardError):
            guard_write_intent("update_coupon_quotas")

    def test_operation_alias_maps_to_real(self):
        self.assertEqual(normalize_operation("ListCoupons"), ALLOWED_OPERATION)
        self.assertEqual(
            normalize_operation("ListSubCustomerCoupons"), ALLOWED_OPERATION)
        self.assertTrue(guard_operation("ListCoupons"))

    def test_operation_guard_rejects_non_list(self):
        with self.assertRaises(GuardError):
            guard_operation("ShowCoupon")
        with self.assertRaises(GuardError):
            guard_operation("CreatePartnerCoupons")
        self.assertTrue(guard_operation(ALLOWED_OPERATION))


class TestParseStatus(unittest.TestCase):
    def test_numeric(self):
        self.assertEqual(parse_status(2), 2)
        self.assertEqual(parse_status("3"), 3)

    def test_aliases(self):
        self.assertEqual(parse_status("available"), 2)
        self.assertEqual(parse_status("USED"), 3)
        self.assertEqual(parse_status("expired"), 4)
        self.assertEqual(parse_status("reclaimed"), 5)
        self.assertEqual(parse_status("recycled"), 5)

    def test_unknown_returns_none(self):
        self.assertIsNone(parse_status("nonsense"))
        self.assertIsNone(parse_status(None))
        self.assertIsNone(parse_status(9))


class TestBuildCommand(unittest.TestCase):
    def test_basic(self):
        argv = build_command("cn-north-1")
        self.assertEqual(argv[0], "BSS")
        self.assertEqual(argv[1], "ListSubCustomerCoupons")
        self.assertIn("--cli-region=cn-north-1", argv)
        self.assertIn("--limit=100", argv)
        self.assertIn("--offset=0", argv)

    def test_filters_appended(self):
        argv = build_command("cn-north-1", coupon_id="CP9", status=2,
                             limit=10, offset=20)
        self.assertIn("--coupon_id=CP9", argv)
        self.assertIn("--status=2", argv)
        self.assertIn("--limit=10", argv)
        self.assertIn("--offset=20", argv)

    def test_no_status_when_none(self):
        argv = build_command("cn-north-1")
        self.assertFalse(any(flag.startswith("--status") for flag in argv))

    def test_name_never_sent_to_server(self):
        # coupon-list API has no `name` parameter — it must never appear.
        argv = build_command("cn-north-1", coupon_id="CP1", status=3)
        self.assertFalse(any(flag.startswith("--name") for flag in argv))

    def test_no_write_flags_ever_added(self):
        argv = build_command("cn-north-1", coupon_id="CP1", status=2)
        for flag in argv:
            self.assertFalse(
                flag.lower().lstrip("-").startswith(("create", "delete", "update", "reclaim")))


class TestExtract(unittest.TestCase):
    def test_extract_json_plain(self):
        data = extract_json(json.dumps({"user_coupons": []}))
        self.assertEqual(data, {"user_coupons": []})

    def test_extract_json_with_noise(self):
        data = extract_json("WARNING some noise\n{\"a\": 1}\n")
        self.assertEqual(data, {"a": 1})

    def test_extract_json_invalid(self):
        with self.assertRaises(ApiError):
            extract_json("<html>not json</html>")

    def test_extract_coupons_known_keys(self):
        for key in ("user_coupons", "coupons", "coupon_infos", "coupon_list"):
            self.assertEqual(extract_coupons({key: [COUPON_1]}), [COUPON_1])
        self.assertEqual(extract_coupons([COUPON_1]), [COUPON_1])
        self.assertEqual(extract_coupons({"count": 0}), [])


class TestClassifyFailure(unittest.TestCase):
    def test_missing_credentials(self):
        err = classify_hcloud_failure(
            "", "ERROR: cli-ak is empty, please run hcloud configure", 1)
        self.assertIsInstance(err, ConfigError)
        self.assertIn("AK/SK", str(err))

    def test_auth_403(self):
        err = classify_hcloud_failure(
            "", '{"error_code":"ApiGW.0301","error_msg":"403 Forbidden"}', 1)
        self.assertIsInstance(err, AuthError)
        self.assertIn("IAM", str(err))

    def test_auth_unauthorized(self):
        err = classify_hcloud_failure("", "Unauthorized: invalid AK", 1)
        self.assertIsInstance(err, AuthError)

    def test_generic_api_error(self):
        err = classify_hcloud_failure("", "boom", 2)
        self.assertIsInstance(err, ApiError)

    def test_use_error_marker_with_zero_rc(self):
        err = classify_hcloud_failure(
            "[USE_ERROR]Invalid parameter: status\n\n"
            "Run `hcloud BSS ListSubCustomerCoupons --help` for details.", "", 0)
        self.assertIsInstance(err, ApiError)
        self.assertIn("参数错误", str(err))
        self.assertIn("--help", str(err))


class TestListCoupons(unittest.TestCase):
    def test_single_page(self):
        fake = FakeRunner([(
            json.dumps({"user_coupons": [COUPON_1, COUPON_2], "count": 2}), "", 0)])
        with mock.patch("list_voucher.subprocess.run", fake):
            coupons = list_coupons("cn-north-1")
        self.assertEqual(coupons, [COUPON_1, COUPON_2])
        self.assertEqual(len(fake.calls), 1)

    def test_pagination_via_count(self):
        page1 = {"user_coupons": [COUPON_1], "count": 2}
        page2 = {"user_coupons": [COUPON_2], "count": 2}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("list_voucher.subprocess.run", fake):
            coupons = list_coupons("cn-north-1", limit=1)
        self.assertEqual(coupons, [COUPON_1, COUPON_2])
        self.assertEqual(len(fake.calls), 2)
        self.assertIn("--offset=1", fake.calls[1])

    def test_pagination_via_full_page_without_total(self):
        page1 = {"user_coupons": [COUPON_1]}
        page2 = {"user_coupons": []}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("list_voucher.subprocess.run", fake):
            coupons = list_coupons("cn-north-1", limit=1)
        self.assertEqual(coupons, [COUPON_1])

    def test_empty_region(self):
        fake = FakeRunner([(json.dumps({"user_coupons": [], "count": 0}), "", 0)])
        with mock.patch("list_voucher.subprocess.run", fake):
            coupons = list_coupons("cn-north-1")
        self.assertEqual(coupons, [])

    def test_status_numeric_forwarded_server_side(self):
        fake = FakeRunner([(
            json.dumps({"user_coupons": [COUPON_1, COUPON_2], "count": 2}), "", 0)])
        with mock.patch("list_voucher.subprocess.run", fake):
            coupons = list_coupons("cn-north-1", status="available")
        self.assertTrue(fake.calls)
        for call in fake.calls:
            self.assertTrue(any("--status=2" in part for part in call))

    def test_status_unrecognised_value_client_side(self):
        # A status value that is not a numeric code / known alias falls back
        # to a local label filter and is never forwarded to the server.
        fake = FakeRunner([(
            json.dumps({"user_coupons": [COUPON_1, COUPON_2], "count": 2}), "", 0)])
        with mock.patch("list_voucher.subprocess.run", fake):
            coupons = list_coupons("cn-north-1", status="USED(3)")
        self.assertEqual(coupons, [COUPON_2])
        for call in fake.calls:
            self.assertFalse(any("--status" in part for part in call))

    def test_name_filter_client_side(self):
        fake = FakeRunner([(
            json.dumps({"user_coupons": [COUPON_1, COUPON_2], "count": 2}), "", 0)])
        with mock.patch("list_voucher.subprocess.run", fake):
            coupons = list_coupons("cn-north-1", name="spring")
        self.assertEqual(coupons, [COUPON_1])
        for call in fake.calls:
            self.assertFalse(any("--name" in part for part in call))

    def test_coupon_id_forwarded(self):
        fake = FakeRunner([(
            json.dumps({"user_coupons": [COUPON_1], "count": 1}), "", 0)])
        with mock.patch("list_voucher.subprocess.run", fake):
            list_coupons("cn-north-1", coupon_id="CP0001")
        self.assertTrue(any("--coupon_id=CP0001" in part for part in fake.calls[0]))

    def test_use_error_rc0_raises_api_error(self):
        fake = FakeRunner([(
            "[USE_ERROR]Invalid parameter: status\n\n"
            "Run `hcloud BSS ListSubCustomerCoupons --help` for details.", "", 0)])
        with mock.patch("list_voucher.subprocess.run", fake):
            with self.assertRaises(ApiError) as ctx:
                list_coupons("cn-north-1")
        self.assertIn("参数错误", str(ctx.exception))

    def test_nonzero_exit_403(self):
        fake = FakeRunner([("", "403 Forbidden", 1)])
        with mock.patch("list_voucher.subprocess.run", fake):
            with self.assertRaises(AuthError):
                list_coupons("cn-north-1")

    def test_nonzero_exit_credentials(self):
        fake = FakeRunner([("", "ERROR: no AK configured", 1)])
        with mock.patch("list_voucher.subprocess.run", fake):
            with self.assertRaises(ConfigError):
                list_coupons("cn-north-1")

    def test_timeout(self):
        fake = FakeRunner([subprocess.TimeoutExpired(cmd="hcloud", timeout=120)])
        with mock.patch("list_voucher.subprocess.run", fake):
            with self.assertRaises(ApiError):
                list_coupons("cn-north-1")

    def test_sdk_fallback_when_hcloud_missing(self):
        with mock.patch("list_voucher.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_voucher.list_coupons_via_sdk",
                           return_value=[COUPON_1, COUPON_2]) as sdk_mock:
            coupons = list_coupons("cn-north-1", status="USED(3)")
        # an unrecognised status degrades to a client-side label filter even
        # on the SDK fallback path (and is not forwarded to the SDK).
        self.assertEqual(coupons, [COUPON_2])
        self.assertIsNone(sdk_mock.call_args.kwargs.get("status"))

    def test_sdk_fallback_unavailable_raises_config(self):
        with mock.patch("list_voucher.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_voucher.list_coupons_via_sdk",
                           side_effect=ConfigError("huaweicloudsdkbss 未安装")):
            with self.assertRaises(ConfigError):
                list_coupons("cn-north-1")


class _FakeSdkResponse:
    def __init__(self, coupons, count):
        self.user_coupons = coupons
        self.count = count


class _FakeSdkCoupon:
    def __init__(self, payload):
        self._payload = payload

    def to_dict(self):
        return self._payload


class _FakeSdkBuilder:
    def __init__(self, test):
        self._test = test
        self._credentials = None

    def with_credentials(self, credentials):
        self._test._captured_credentials = credentials
        return self

    def with_http_config(self, config):
        return self

    def with_endpoints(self, endpoints):
        self._test._captured_endpoints = endpoints
        return self

    def build(self):
        return self._test._fake_client


class TestSdkFallback(unittest.TestCase):
    """The SDK fallback must use the official huaweicloudsdkbss client with
    GlobalCredentials + with_endpoints (BSS is a global service)."""

    def setUp(self):
        self._captured_credentials = None
        self._captured_endpoints = None
        self._fake_client = mock.Mock()
        self._fake_client.list_sub_customer_coupons.return_value = _FakeSdkResponse(
            [_FakeSdkCoupon(COUPON_1), _FakeSdkCoupon(COUPON_2)], 2)
        try:
            import huaweicloudsdkbss.v2 as bss_v2
        except ImportError:
            self.skipTest("huaweicloudsdkbss not installed")
        self._builder_patch = mock.patch.object(
            bss_v2.BssClient, "new_builder",
            classmethod(lambda cls: _FakeSdkBuilder(self)))
        self._builder_patch.start()
        self.addCleanup(self._builder_patch.stop)

    def _clean_credential_env(self):
        return {
            key: value for key, value in os.environ.items()
            if not key.upper().startswith(("HUAWEI", "HW_", "HWC"))
        }

    def test_official_sdk_imports_resolve(self):
        from huaweicloudsdkcore.auth.credentials import GlobalCredentials
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkbss.v2 import BssClient, ListSubCustomerCouponsRequest
        for obj in (GlobalCredentials, HttpConfig, BssClient,
                    ListSubCustomerCouponsRequest):
            self.assertTrue(callable(obj), obj)

    def test_fallback_uses_global_credentials_and_endpoints(self):
        env = dict(self._clean_credential_env(),
                   HUAWEICLOUD_SDK_AK="test-ak",
                   HUAWEICLOUD_SDK_SK="test-sk")
        with mock.patch.dict(os.environ, env, clear=True):
            coupons = list_coupons_via_sdk("cn-north-1")
        self.assertEqual(coupons, [COUPON_1, COUPON_2])
        credentials = self._captured_credentials
        self.assertIsNotNone(credentials)
        self.assertEqual(getattr(credentials, "ak", None), "test-ak")
        self.assertEqual(getattr(credentials, "sk", None), "test-sk")
        self.assertEqual(self._captured_endpoints, ["https://bss.myhuaweicloud.com"])

    def test_fallback_missing_env_credentials_raises_config(self):
        with mock.patch.dict(os.environ, self._clean_credential_env(), clear=True):
            with self.assertRaises(ConfigError) as ctx:
                list_coupons_via_sdk("cn-north-1")
        message = str(ctx.exception)
        self.assertIn("AK/SK", message)
        self.assertNotIn("未安装", message)

    def test_fallback_alternative_env_prefixes(self):
        env = dict(self._clean_credential_env(),
                   HW_ACCESS_KEY="alt-ak", HW_SECRET_KEY="alt-sk")
        with mock.patch.dict(os.environ, env, clear=True):
            list_coupons_via_sdk("cn-north-1")
        self.assertEqual(getattr(self._captured_credentials, "ak", None), "alt-ak")

    def test_request_has_no_name_attribute(self):
        # Regression guard: the real ListSubCustomerCouponsRequest has no
        # `name` attribute (the API has no name parameter).
        try:
            from huaweicloudsdkbss.v2 import ListSubCustomerCouponsRequest
        except ImportError:
            self.skipTest("huaweicloudsdkbss not installed")
        request = ListSubCustomerCouponsRequest(
            coupon_id="CP1", status=2, offset=0, limit=100)
        self.assertIsNone(getattr(request, "name", None))
        with self.assertRaises(TypeError):
            ListSubCustomerCouponsRequest(name="x")


class TestFilters(unittest.TestCase):
    def test_filter_by_name(self):
        self.assertEqual(filter_by_name([COUPON_1, COUPON_2], "spring"), [COUPON_1])
        self.assertEqual(filter_by_name([COUPON_1, COUPON_2], "discount"), [COUPON_2])
        self.assertEqual(filter_by_name([COUPON_1, COUPON_2], "CODE-0002"), [COUPON_2])
        self.assertEqual(filter_by_name([COUPON_1, COUPON_2], None),
                         [COUPON_1, COUPON_2])

    def test_filter_by_status_numeric(self):
        self.assertEqual(filter_by_status([COUPON_1, COUPON_2], 3), [COUPON_2])

    def test_filter_by_status_text(self):
        self.assertEqual(filter_by_status([COUPON_1, COUPON_2], "used"), [COUPON_2])
        self.assertEqual(filter_by_status([COUPON_1, COUPON_2], "AVAILABLE"),
                         [COUPON_1])

    def test_filter_input_not_mutated(self):
        source = [COUPON_1, COUPON_2]
        filter_by_name(source, "spring")
        self.assertEqual(source, [COUPON_1, COUPON_2])


class TestNormalizeAndRender(unittest.TestCase):
    def test_normalize_adds_labels(self):
        flat = normalize_coupon(COUPON_1)
        self.assertEqual(flat["statusText"], "AVAILABLE(2)")
        self.assertEqual(flat["couponTypeText"], "VOUCHER(1)")
        self.assertIn("service", flat["useLimits"])

    def test_normalize_missing_labels(self):
        flat = normalize_coupon({"coupon_id": "CPX"})
        self.assertEqual(flat["statusText"], "-")
        self.assertEqual(flat["couponTypeText"], "-")

    def test_table_contains_basic_info(self):
        table = render_table([COUPON_1, COUPON_2])
        for fragment in ("CP0001", "CODE-0001", "AVAILABLE(2)", "VOUCHER(1)",
                         "spring-voucher", "100.0", "CNY", "CP0002",
                         "discount-A"):
            self.assertIn(fragment, table)

    def test_names(self):
        self.assertEqual(coupon_names([COUPON_1, COUPON_2]),
                         ["spring-voucher", "discount-A"])

    def test_names_fallback_to_id(self):
        self.assertEqual(coupon_names([{"coupon_id": "CP9"}]), ["CP9"])


class TestMain(unittest.TestCase):
    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("list_voucher.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            rc = main(argv)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    def test_table_output(self):
        rc, out, err = self._run(
            ["--region", "cn-north-1"],
            [(json.dumps({"user_coupons": [COUPON_1, COUPON_2], "count": 2}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("BSS 代金券列表", out)
        self.assertIn("CP0001", out)
        self.assertIn("AVAILABLE(2)", out)
        self.assertEqual(err, "")

    def test_json_output(self):
        rc, out, err = self._run(
            ["--json"],
            [(json.dumps({"user_coupons": [COUPON_1], "count": 1}), "", 0)])
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual(payload, [COUPON_1])

    def test_names_only_output(self):
        rc, out, err = self._run(
            ["--names-only"],
            [(json.dumps({"user_coupons": [COUPON_1, COUPON_2], "count": 2}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("spring-voucher", out)
        self.assertIn("discount-A", out)
        self.assertNotIn("face_value", out)

    def test_empty_message(self):
        rc, out, err = self._run(
            ["--region", "cn-north-1"],
            [(json.dumps({"user_coupons": [], "count": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("无 BSS 代金券", out)
        self.assertIn("cn-north-1", out)

    def test_empty_with_filter_message(self):
        rc, out, _ = self._run(
            ["--status", "used"],
            [(json.dumps({"user_coupons": [], "count": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("status=used", out)

    def test_empty_json_output(self):
        rc, out, err = self._run(
            ["--json"],
            [(json.dumps({"user_coupons": [], "count": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out), [])

    def test_empty_names_only_output(self):
        rc, out, err = self._run(
            ["--names-only"],
            [(json.dumps({"user_coupons": [], "count": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("共 0 张", out)
        self.assertNotIn("无 BSS 代金券", out)

    def test_auth_error_message(self):
        rc, out, err = self._run([], [("", "403 Forbidden", 1)])
        self.assertEqual(rc, 1)
        self.assertIn("[错误]", err)
        self.assertIn("IAM", err)

    def test_missing_ak_sk_error_message(self):
        rc, out, err = self._run([], [("", "ERROR: cli-ak empty", 1)])
        self.assertEqual(rc, 1)
        self.assertIn("AK/SK", err)

    def test_hcloud_not_installed(self):
        with mock.patch("list_voucher.list_coupons_via_sdk",
                        side_effect=ConfigError("huaweicloudsdkbss 未安装")):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 1)
        self.assertIn("未安装", err)

    def test_hcloud_missing_falls_back_to_sdk(self):
        with mock.patch("list_voucher.list_coupons_via_sdk",
                        return_value=[COUPON_1]):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 0)
        self.assertIn("CP0001", out)

    def test_write_intent_argv_blocked(self):
        rc, out, err = self._run(["--operation", "ReclaimPartnerCoupons"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)

    def test_write_keyword_name_blocked(self):
        rc, out, err = self._run(["--name", "transfer-me"], [])
        self.assertEqual(rc, 1)
        self.assertIn("守卫拦截", err)

    def test_status_label_not_blocked_readonly(self):
        rc, out, err = self._run(
            ["--status", "reclaimed"],
            [(json.dumps({"user_coupons": [], "count": 0}), "", 0)])
        self.assertEqual(rc, 0)

    def test_operation_alias_listcoupons_accepted(self):
        rc, out, err = self._run(
            ["--operation", "ListCoupons"],
            [(json.dumps({"user_coupons": [COUPON_1], "count": 1}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("CP0001", out)


class TestErrorHierarchy(unittest.TestCase):
    def test_subclasses(self):
        for exc in (GuardError, ConfigError, AuthError, ApiError):
            self.assertTrue(issubclass(exc, VoucherListError))


if __name__ == "__main__":
    unittest.main()
