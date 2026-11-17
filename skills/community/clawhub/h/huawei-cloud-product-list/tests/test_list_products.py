import json
import os
import subprocess
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from list_products import (  # noqa: E402
    ALLOWED_OPERATION,
    ApiError,
    AuthError,
    ConfigError,
    GuardError,
    ProductListError,
    build_command,
    classify_hcloud_failure,
    extract_json,
    extract_products,
    filter_by_code,
    guard_operation,
    guard_write_intent,
    is_service_unsupported,
    list_products,
    list_products_via_sdk,
    main,
    product_names,
    render_table,
    standardize_products,
)

PRODUCT_1 = {
    "service_type_name": "弹性云服务器",
    "service_type_code": "hws.service.type.ec2",
    "abbreviation": "ECS",
}
PRODUCT_2 = {
    "service_type_name": "对象存储服务",
    "service_type_code": "hws.service.type.obs",
    "abbreviation": "OBS",
}

# Fixed credential variable names the SDK fallback reads (kept in sync with
# scripts/list_products.py); removed from the environment in the tests below so
# no ambient credential leaks into the fallback path.
_CREDENTIAL_ENV_KEYS = (
    "HUAWEICLOUD_SDK_AK",
    "HUAWEICLOUD_SDK_SK",
    "HUAWEI_ACCESS_KEY",
    "HUAWEI_SECRET_KEY",
    "HW_ACCESS_KEY",
    "HW_SECRET_KEY",
)


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
        self.assertFalse(guard_write_intent("--region cn-north-1 --json list products"))
        self.assertFalse(guard_write_intent("show service types"))

    def test_create_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("CreatePartnerCoupons")

    def test_mutating_verbs_blocked(self):
        for text in ("update coupon quotas", "transfer coupon",
                     "retrieve coupon", "adjust quota", "send coupon",
                     "freeze coupon", "delete coupon", "reclaim coupon"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_normalized_separators_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--create-coupon")
        with self.assertRaises(GuardError):
            guard_write_intent("update_coupon_quotas")

    def test_chinese_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("删除产品")

    def test_operation_guard(self):
        with self.assertRaises(GuardError):
            guard_operation("ShowServiceTypes")
        with self.assertRaises(GuardError):
            guard_operation("CreatePartnerCoupons")
        self.assertTrue(guard_operation(ALLOWED_OPERATION))


class TestBuildCommand(unittest.TestCase):
    def test_basic(self):
        argv = build_command("cn-north-1")
        self.assertEqual(argv[0], "BSS")
        self.assertEqual(argv[1], "ListServiceTypes")
        self.assertIn("--cli-region=cn-north-1", argv)
        self.assertIn("--limit=100", argv)
        self.assertIn("--offset=0", argv)

    def test_name_forwarded_server_side(self):
        argv = build_command("cn-north-1", name="弹性", limit=10, offset=20)
        self.assertIn("--service_type_name=弹性", argv)
        self.assertIn("--limit=10", argv)
        self.assertIn("--offset=20", argv)

    def test_no_name_when_none(self):
        argv = build_command("cn-north-1")
        self.assertFalse(any(flag.startswith("--service_type_name") for flag in argv))

    def test_no_write_flags_ever_added(self):
        argv = build_command("cn-north-1", name="x")
        for flag in argv:
            self.assertFalse(
                flag.lower().lstrip("-").startswith(
                    ("create", "delete", "update", "reclaim", "transfer")))


class TestExtract(unittest.TestCase):
    def test_extract_json_plain(self):
        data = extract_json(json.dumps({"service_types": []}))
        self.assertEqual(data, {"service_types": []})

    def test_extract_json_with_noise(self):
        data = extract_json("WARNING some noise\n{\"a\": 1}\n")
        self.assertEqual(data, {"a": 1})

    def test_extract_json_invalid(self):
        with self.assertRaises(ApiError):
            extract_json("<html>not json</html>")

    def test_extract_products_known_keys(self):
        for key in ("service_types", "serviceTypes", "products", "services"):
            self.assertEqual(extract_products({key: [PRODUCT_1]}), [PRODUCT_1])
        self.assertEqual(extract_products([PRODUCT_1]), [PRODUCT_1])
        self.assertEqual(extract_products({"total_count": 0}), [])


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

    def test_generic_api_error(self):
        err = classify_hcloud_failure("", "boom", 2)
        self.assertIsInstance(err, ApiError)

    def test_use_error_marker_with_zero_rc(self):
        err = classify_hcloud_failure(
            "[USE_ERROR]Invalid parameter: service_type_name\n\n"
            "Run `hcloud BSS ListServiceTypes --help` for details.", "", 0)
        self.assertIsInstance(err, ApiError)
        self.assertIn("参数错误", str(err))
        self.assertIn("--help", str(err))


class TestListProducts(unittest.TestCase):
    def test_single_page(self):
        fake = FakeRunner([(
            json.dumps({"service_types": [PRODUCT_1, PRODUCT_2], "total_count": 2}), "", 0)])
        with mock.patch("list_products.subprocess.run", fake):
            products = list_products("cn-north-1")
        self.assertEqual(products, [PRODUCT_1, PRODUCT_2])
        self.assertEqual(len(fake.calls), 1)

    def test_pagination_via_total_count(self):
        page1 = {"service_types": [PRODUCT_1], "total_count": 2}
        page2 = {"service_types": [PRODUCT_2], "total_count": 2}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("list_products.subprocess.run", fake):
            products = list_products("cn-north-1", limit=1)
        self.assertEqual(products, [PRODUCT_1, PRODUCT_2])
        self.assertEqual(len(fake.calls), 2)
        self.assertIn("--offset=1", fake.calls[1])

    def test_pagination_via_full_page_without_total(self):
        page1 = {"service_types": [PRODUCT_1]}
        page2 = {"service_types": []}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("list_products.subprocess.run", fake):
            products = list_products("cn-north-1", limit=1)
        self.assertEqual(products, [PRODUCT_1])

    def test_empty(self):
        fake = FakeRunner([(json.dumps({"service_types": [], "total_count": 0}), "", 0)])
        with mock.patch("list_products.subprocess.run", fake):
            products = list_products("cn-north-1")
        self.assertEqual(products, [])

    def test_name_forwarded_server_side(self):
        fake = FakeRunner([(
            json.dumps({"service_types": [PRODUCT_1], "total_count": 1}), "", 0)])
        with mock.patch("list_products.subprocess.run", fake):
            list_products("cn-north-1", name="弹性")
        self.assertTrue(any("--service_type_name=弹性" in part for part in fake.calls[0]))

    def test_use_error_rc0_raises_api_error(self):
        fake = FakeRunner([(
            "[USE_ERROR]Invalid parameter: service_type_name\n\n"
            "Run `hcloud BSS ListServiceTypes --help` for details.", "", 0)])
        with mock.patch("list_products.subprocess.run", fake):
            with self.assertRaises(ApiError) as ctx:
                list_products("cn-north-1")
        self.assertIn("参数错误", str(ctx.exception))

    def test_nonzero_exit_403(self):
        fake = FakeRunner([("", "403 Forbidden", 1)])
        with mock.patch("list_products.subprocess.run", fake):
            with self.assertRaises(AuthError):
                list_products("cn-north-1")

    def test_nonzero_exit_credentials(self):
        fake = FakeRunner([("", "ERROR: no AK configured", 1)])
        with mock.patch("list_products.subprocess.run", fake):
            with self.assertRaises(ConfigError):
                list_products("cn-north-1")

    def test_timeout(self):
        fake = FakeRunner([subprocess.TimeoutExpired(cmd="hcloud", timeout=120)])
        with mock.patch("list_products.subprocess.run", fake):
            with self.assertRaises(ApiError):
                list_products("cn-north-1")

    def test_sdk_fallback_when_hcloud_missing(self):
        with mock.patch("list_products.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_products.list_products_via_sdk",
                           return_value=[PRODUCT_1, PRODUCT_2]) as sdk_mock:
            products = list_products("cn-north-1")
        self.assertEqual(products, [PRODUCT_1, PRODUCT_2])
        self.assertEqual(sdk_mock.call_args.kwargs.get("name"), None)

    def test_sdk_fallback_unavailable_raises_config(self):
        with mock.patch("list_products.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_products.list_products_via_sdk",
                           side_effect=ConfigError("huaweicloudsdkbss 未安装")):
            with self.assertRaises(ConfigError):
                list_products("cn-north-1")

    def test_sdk_fallback_when_service_unsupported(self):
        fake = FakeRunner([("[USE_ERROR]Unsupported service: BSS.", "", 0)])
        with mock.patch("list_products.subprocess.run", fake), \
                mock.patch("list_products.list_products_via_sdk",
                           return_value=[PRODUCT_1, PRODUCT_2]) as sdk_mock:
            products = list_products("cn-north-1")
        self.assertEqual(products, [PRODUCT_1, PRODUCT_2])
        self.assertEqual(sdk_mock.call_count, 1)

    def test_unsupported_service_keeps_cli_error_without_sdk(self):
        fake = FakeRunner([("[USE_ERROR]Unsupported service: BSS.", "", 0)])
        with mock.patch("list_products.subprocess.run", fake), \
                mock.patch("list_products.list_products_via_sdk",
                           side_effect=ConfigError("huaweicloudsdkbss 未安装")):
            with self.assertRaises(ApiError) as ctx:
                list_products("cn-north-1")
        self.assertIn("参数错误", str(ctx.exception))


class TestServiceUnsupported(unittest.TestCase):
    def test_detects_unsupported_service_marker(self):
        self.assertTrue(is_service_unsupported(
            "[USE_ERROR]Unsupported service: BSS.", ""))
        self.assertTrue(is_service_unsupported("", "Unknown service BSS"))
        self.assertTrue(is_service_unsupported("不支持的服务", ""))

    def test_other_errors_not_flagged(self):
        self.assertFalse(is_service_unsupported("", "403 Forbidden"))
        self.assertFalse(is_service_unsupported("ERROR: cli-ak empty", ""))


class _FakeSdkResponse:
    def __init__(self, products, total_count):
        self.service_types = products
        self.total_count = total_count


class _FakeSdkProduct:
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
        self._fake_client.list_service_types.return_value = _FakeSdkResponse(
            [_FakeSdkProduct(PRODUCT_1), _FakeSdkProduct(PRODUCT_2)], 2)
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
        env = dict(os.environ)
        for key in _CREDENTIAL_ENV_KEYS:
            env.pop(key, None)
        return env

    def test_official_sdk_imports_resolve(self):
        from huaweicloudsdkcore.auth.credentials import GlobalCredentials
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkbss.v2 import BssClient, ListServiceTypesRequest
        for obj in (GlobalCredentials, HttpConfig, BssClient,
                    ListServiceTypesRequest):
            self.assertTrue(callable(obj), obj)

    def test_fallback_uses_global_credentials_and_endpoints(self):
        env = dict(self._clean_credential_env(),
                   HUAWEICLOUD_SDK_AK="test-ak",
                   HUAWEICLOUD_SDK_SK="test-sk")
        with mock.patch.dict(os.environ, env, clear=True):
            products = list_products_via_sdk("cn-north-1")
        self.assertEqual(products, [PRODUCT_1, PRODUCT_2])
        credentials = self._captured_credentials
        self.assertIsNotNone(credentials)
        self.assertEqual(getattr(credentials, "ak", None), "test-ak")
        self.assertEqual(getattr(credentials, "sk", None), "test-sk")
        self.assertEqual(self._captured_endpoints, ["https://bss.myhuaweicloud.com"])

    def test_fallback_missing_env_credentials_raises_config(self):
        with mock.patch.dict(os.environ, self._clean_credential_env(), clear=True):
            with self.assertRaises(ConfigError) as ctx:
                list_products_via_sdk("cn-north-1")
        message = str(ctx.exception)
        self.assertIn("AK/SK", message)
        self.assertNotIn("未安装", message)

    def test_fallback_alternative_env_prefixes(self):
        env = dict(self._clean_credential_env(),
                   HW_ACCESS_KEY="alt-ak", HW_SECRET_KEY="alt-sk")
        with mock.patch.dict(os.environ, env, clear=True):
            list_products_via_sdk("cn-north-1")
        self.assertEqual(getattr(self._captured_credentials, "ak", None), "alt-ak")

    def test_request_signature_matches_official_model(self):
        # Regression guard: the real ListServiceTypesRequest accepts exactly
        # service_type_name / offset / limit (and x_language) — nothing else.
        try:
            from huaweicloudsdkbss.v2 import ListServiceTypesRequest
        except ImportError:
            self.skipTest("huaweicloudsdkbss not installed")
        request = ListServiceTypesRequest(
            service_type_name="弹性", offset=0, limit=100)
        self.assertEqual(request.service_type_name, "弹性")
        self.assertEqual(request.limit, 100)
        with self.assertRaises(TypeError):
            ListServiceTypesRequest(nonexistent_param="x")


class TestFiltersAndRender(unittest.TestCase):
    def test_filter_by_code(self):
        self.assertEqual(filter_by_code([PRODUCT_1, PRODUCT_2], "obs"), [PRODUCT_2])
        self.assertEqual(filter_by_code([PRODUCT_1, PRODUCT_2], "hws.service.type.ec2"),
                         [PRODUCT_1])
        self.assertEqual(filter_by_code([PRODUCT_1, PRODUCT_2], None),
                         [PRODUCT_1, PRODUCT_2])

    def test_filter_input_not_mutated(self):
        source = [PRODUCT_1, PRODUCT_2]
        filter_by_code(source, "obs")
        self.assertEqual(source, [PRODUCT_1, PRODUCT_2])

    def test_standardize(self):
        rows = standardize_products([PRODUCT_1, {"service_type_code": "X"}])
        self.assertEqual(rows[0], {"name": "弹性云服务器",
                                   "code": "hws.service.type.ec2",
                                   "abbreviation": "ECS"})
        self.assertEqual(rows[1], {"name": "-", "code": "X", "abbreviation": "-"})

    def test_table_contains_info(self):
        table = render_table([PRODUCT_1, PRODUCT_2])
        for fragment in ("名称", "编码", "缩写", "弹性云服务器",
                         "hws.service.type.ec2", "ECS", "对象存储服务", "OBS"):
            self.assertIn(fragment, table)

    def test_names(self):
        self.assertEqual(product_names([PRODUCT_1, PRODUCT_2]),
                         ["弹性云服务器", "对象存储服务"])


class TestMain(unittest.TestCase):
    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("list_products.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            rc = main(argv)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    def test_table_output(self):
        rc, out, err = self._run(
            ["--region", "cn-north-1"],
            [(json.dumps({"service_types": [PRODUCT_1, PRODUCT_2], "total_count": 2}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("华为云产品", out)
        self.assertIn("弹性云服务器", out)
        self.assertEqual(err, "")

    def test_json_output(self):
        rc, out, err = self._run(
            ["--json"],
            [(json.dumps({"service_types": [PRODUCT_1], "total_count": 1}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out), [PRODUCT_1])

    def test_names_only_output(self):
        rc, out, err = self._run(
            ["--names-only"],
            [(json.dumps({"service_types": [PRODUCT_1, PRODUCT_2], "total_count": 2}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("弹性云服务器", out)
        self.assertIn("对象存储服务", out)
        self.assertNotIn("hws.service.type.ec2", out)

    def test_code_filter_client_side(self):
        rc, out, err = self._run(
            ["--names-only", "--code", "obs"],
            [(json.dumps({"service_types": [PRODUCT_1, PRODUCT_2], "total_count": 2}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("对象存储服务", out)
        self.assertNotIn("弹性云服务器", out)

    def test_empty_message(self):
        rc, out, err = self._run(
            ["--region", "cn-north-1"],
            [(json.dumps({"service_types": [], "total_count": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("未查询到华为云产品", out)

    def test_empty_json_output(self):
        rc, out, err = self._run(
            ["--json"],
            [(json.dumps({"service_types": [], "total_count": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out), [])

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
        with mock.patch("list_products.list_products_via_sdk",
                        side_effect=ConfigError("huaweicloudsdkbss 未安装")):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 1)
        self.assertIn("未安装", err)

    def test_hcloud_missing_falls_back_to_sdk(self):
        with mock.patch("list_products.list_products_via_sdk",
                        return_value=[PRODUCT_1]):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 0)
        self.assertIn("弹性云服务器", out)

    def test_write_intent_argv_blocked(self):
        rc, out, err = self._run(["--operation", "CreatePartnerCoupons"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)

    def test_write_keyword_name_blocked(self):
        rc, out, err = self._run(["--name", "delete-me"], [])
        self.assertEqual(rc, 1)
        self.assertIn("守卫拦截", err)


class TestErrorHierarchy(unittest.TestCase):
    def test_subclasses(self):
        for exc in (GuardError, ConfigError, AuthError, ApiError):
            self.assertTrue(issubclass(exc, ProductListError))


if __name__ == "__main__":
    unittest.main()