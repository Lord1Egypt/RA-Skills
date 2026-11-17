import json
import os
import subprocess
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from list_cdn import (  # noqa: E402
    ALLOWED_OPERATION,
    ApiError,
    AuthError,
    ConfigError,
    GuardError,
    CdnListError,
    build_command,
    classify_hcloud_failure,
    domain_names,
    extract_domains,
    extract_json,
    guard_operation,
    guard_write_intent,
    list_domains,
    list_domains_via_sdk,
    main,
    normalize_domain,
    render_table,
)

DOMAIN_1 = {
    "id": "cdn-0001",
    "domain_name": "www.example.com",
    "business_type": "web",
    "domain_status": "online",
    "cname": "www.example.com.c.cdnhwc1.com",
    "service_area": "mainland_china",
    "https_status": 1,
    "disabled": 0,
    "locked": 0,
    "origin_status": "online",
    "enterprise_project_id": "0",
    "tags": [{"key": "env", "value": "test"}],
    "create_time": 1704067200000,
    "modify_time": 1704153600000,
}
DOMAIN_2 = {
    "id": "cdn-0002",
    "domain_name": "static.example.com",
    "business_type": "download",
    "domain_status": "offline",
    "cname": "static.example.com.c.cdnhwc1.com",
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
        self.assertFalse(guard_write_intent("--domain-status online --json list cdn domains"))
        self.assertFalse(guard_write_intent("show cdn domain details"))

    def test_create_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("CreateDomain example.com")

    def test_delete_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--operation DeleteDomain")

    def test_mutating_verbs_blocked(self):
        for text in ("update domain origin", "modify domain config",
                     "enable domain example.com", "disable domain cdn-01",
                     "refresh task", "preheating task"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_normalized_separators_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--create-domain")
        with self.assertRaises(GuardError):
            guard_write_intent("update_domain_name")

    def test_read_filter_values_pass(self):
        self.assertFalse(guard_write_intent("--domain-status online"))
        self.assertFalse(guard_write_intent("--business-type web"))
        self.assertFalse(guard_write_intent("--business-type download"))
        self.assertFalse(guard_write_intent("--domain-status configuring"))

    def test_operation_guard_rejects_non_list(self):
        with self.assertRaises(GuardError):
            guard_operation("ShowDomainDetail")
        self.assertTrue(guard_operation(ALLOWED_OPERATION))


class TestBuildCommand(unittest.TestCase):
    def test_basic(self):
        argv = build_command("cn-north-4")
        self.assertEqual(argv[0], "CDN")
        self.assertEqual(argv[1], "ListDomains")
        self.assertIn("--cli-region=cn-north-4", argv)
        self.assertIn("--page_size=100", argv)
        self.assertIn("--page_number=1", argv)

    def test_page_number_appended(self):
        argv = build_command("cn-north-4", page_number=3, limit=10)
        self.assertIn("--page_number=3", argv)
        self.assertIn("--page_size=10", argv)

    def test_filters_forwarded_server_side(self):
        argv = build_command("cn-south-1", domain_name="www.example.com",
                             business_type="web", domain_status="online",
                             service_area="mainland_china",
                             enterprise_project_id="0", limit=10)
        self.assertIn("--domain_name=www.example.com", argv)
        self.assertIn("--business_type=web", argv)
        self.assertIn("--domain_status=online", argv)
        self.assertIn("--service_area=mainland_china", argv)
        self.assertIn("--enterprise_project_id=0", argv)

    def test_no_write_flags_ever_added(self):
        argv = build_command("cn-north-4", domain_status="online")
        for flag in argv:
            self.assertFalse(flag.lower().lstrip("-").startswith(
                ("create", "delete", "update", "enable", "disable", "refresh")))


class TestExtract(unittest.TestCase):
    def test_extract_json_plain(self):
        data = extract_json(json.dumps({"domains": []}))
        self.assertEqual(data, {"domains": []})

    def test_extract_json_with_noise(self):
        data = extract_json("WARNING some noise\n{\"a\": 1}\n")
        self.assertEqual(data, {"a": 1})

    def test_extract_json_invalid(self):
        with self.assertRaises(ApiError):
            extract_json("<html>not json</html>")

    def test_extract_domains_known_keys(self):
        self.assertEqual(extract_domains({"domains": [DOMAIN_1]}), [DOMAIN_1])
        self.assertEqual(extract_domains([DOMAIN_1]), [DOMAIN_1])
        self.assertEqual(extract_domains({"total": 0}), [])


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
            "[USE_ERROR]Invalid parameter: domain_status\n\n"
            "Run `hcloud CDN ListDomains --help` for details.", "", 0)
        self.assertIsInstance(err, ApiError)
        self.assertIn("参数错误", str(err))
        self.assertIn("--help", str(err))


class TestListDomains(unittest.TestCase):
    def test_single_page(self):
        fake = FakeRunner([(
            json.dumps({"domains": [DOMAIN_1, DOMAIN_2], "total": 2}), "", 0)])
        with mock.patch("list_cdn.subprocess.run", fake):
            domains = list_domains("cn-north-4")
        self.assertEqual(domains, [DOMAIN_1, DOMAIN_2])
        self.assertEqual(len(fake.calls), 1)

    def test_pagination_via_total(self):
        page1 = {"domains": [DOMAIN_1], "total": 2}
        page2 = {"domains": [DOMAIN_2], "total": 2}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("list_cdn.subprocess.run", fake):
            domains = list_domains("cn-north-4", limit=1)
        self.assertEqual(domains, [DOMAIN_1, DOMAIN_2])
        self.assertEqual(len(fake.calls), 2)
        self.assertIn("--page_number=2", fake.calls[1])

    def test_pagination_via_full_page_without_total(self):
        page1 = {"domains": [DOMAIN_1]}
        page2 = {"domains": []}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("list_cdn.subprocess.run", fake):
            domains = list_domains("cn-north-4", limit=1)
        self.assertEqual(domains, [DOMAIN_1])

    def test_empty_region(self):
        fake = FakeRunner([(json.dumps({"domains": [], "total": 0}), "", 0)])
        with mock.patch("list_cdn.subprocess.run", fake):
            domains = list_domains("cn-north-4")
        self.assertEqual(domains, [])

    def test_filters_forwarded_to_cli(self):
        fake = FakeRunner([(
            json.dumps({"domains": [DOMAIN_1], "total": 1}), "", 0)])
        with mock.patch("list_cdn.subprocess.run", fake):
            list_domains("cn-north-4", domain_status="online",
                         business_type="web", domain_name="www.example.com")
        call = fake.calls[0]
        self.assertTrue(any("--domain_status=online" in part for part in call))
        self.assertTrue(any("--business_type=web" in part for part in call))
        self.assertTrue(any("--domain_name=www.example.com" in part for part in call))

    def test_use_error_rc0_raises_api_error(self):
        fake = FakeRunner([(
            "[USE_ERROR]Invalid parameter: domain_status\n\n"
            "Run `hcloud CDN ListDomains --help` for details.", "", 0)])
        with mock.patch("list_cdn.subprocess.run", fake):
            with self.assertRaises(ApiError) as ctx:
                list_domains("cn-north-4")
        self.assertIn("参数错误", str(ctx.exception))

    def test_nonzero_exit_403(self):
        fake = FakeRunner([("", "403 Forbidden", 1)])
        with mock.patch("list_cdn.subprocess.run", fake):
            with self.assertRaises(AuthError):
                list_domains("cn-north-4")

    def test_nonzero_exit_credentials(self):
        fake = FakeRunner([("", "ERROR: no AK configured", 1)])
        with mock.patch("list_cdn.subprocess.run", fake):
            with self.assertRaises(ConfigError):
                list_domains("cn-north-4")

    def test_timeout(self):
        fake = FakeRunner([subprocess.TimeoutExpired(cmd="hcloud", timeout=120)])
        with mock.patch("list_cdn.subprocess.run", fake):
            with self.assertRaises(ApiError):
                list_domains("cn-north-4")

    def test_sdk_fallback_when_hcloud_missing(self):
        with mock.patch("list_cdn.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_cdn.list_domains_via_sdk",
                           return_value=[DOMAIN_1, DOMAIN_2]) as sdk_mock:
            domains = list_domains("cn-north-4", domain_status="online",
                                   business_type="web", domain_name="example")
        self.assertEqual(domains, [DOMAIN_1, DOMAIN_2])
        self.assertEqual(sdk_mock.call_args.kwargs.get("domain_status"), "online")

    def test_sdk_fallback_unavailable_raises_config(self):
        with mock.patch("list_cdn.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_cdn.list_domains_via_sdk",
                           side_effect=ConfigError("huaweicloudsdkcdn 未安装")):
            with self.assertRaises(ConfigError):
                list_domains("cn-north-4")

    def test_sdk_request_signature(self):
        # Regression guard: the real huaweicloudsdkcdn ListDomainsRequest must be
        # constructible with exactly the kwargs the fallback path sends.
        try:
            from huaweicloudsdkcdn.v1 import ListDomainsRequest
        except ImportError:
            self.skipTest("huaweicloudsdkcdn not installed")
        request = ListDomainsRequest(
            domain_name="www.example.com", business_type="web",
            domain_status="online", service_area="mainland_china",
            enterprise_project_id="0", page_size=100, page_number=1,
        )
        self.assertEqual(request.domain_name, "www.example.com")
        self.assertEqual(request.domain_status, "online")
        self.assertEqual(request.business_type, "web")
        self.assertEqual(request.page_number, 1)
        with self.assertRaises(TypeError):
            ListDomainsRequest(no_such_param=1)


class _FakeSdkResponse:
    def __init__(self, domains, total):
        self.domains = domains
        self.total = total


class _FakeSdkDomain:
    def __init__(self, payload):
        self._payload = payload

    def to_dict(self):
        return self._payload


class _FakeSdkBuilder:
    def __init__(self, test):
        self._test = test

    def with_credentials(self, credentials):
        self._test._captured_credentials = credentials
        return self

    def with_region(self, region):
        self._test._captured_region = region
        return self

    def with_http_config(self, config):
        return self

    def build(self):
        return self._test._fake_client


class TestSdkFallback(unittest.TestCase):
    """P2 regression: the SDK fallback must use modules that exist in the
    official huaweicloudsdkcdn package and wire credentials from environment
    variables (GlobalCredentials has no env auto-discovery; CDN is a global
    service and requires GlobalCredentials)."""

    def setUp(self):
        self._captured_credentials = None
        self._captured_region = None
        self._fake_client = mock.Mock()
        self._fake_client.list_domains.return_value = _FakeSdkResponse(
            [_FakeSdkDomain(DOMAIN_1), _FakeSdkDomain(DOMAIN_2)], 2)
        try:
            import huaweicloudsdkcdn.v1 as cdn_v1
        except ImportError:
            self.skipTest("huaweicloudsdkcdn not installed")
        self._builder_patch = mock.patch.object(
            cdn_v1.CdnClient, "new_builder",
            classmethod(lambda cls: _FakeSdkBuilder(self)))
        self._builder_patch.start()
        self.addCleanup(self._builder_patch.stop)

    # Explicit credential env-var whitelist (mirrors list_cdn.AK_ENV_KEYS /
    # SK_ENV_KEYS); removal targets exact key names, the environment is never
    # filtered by prefix.
    _CREDENTIAL_ENV_KEYS = (
        "HUAWEICLOUD_SDK_AK", "HUAWEICLOUD_SDK_SK",
        "HUAWEI_ACCESS_KEY", "HUAWEI_SECRET_KEY",
        "HW_ACCESS_KEY", "HW_SECRET_KEY",
        "HUAWEI_AK", "HUAWEI_SK",
        "HW_AK", "HW_SK",
    )

    def _clean_credential_env(self):
        env = dict(os.environ)
        for name in self._CREDENTIAL_ENV_KEYS:
            env.pop(name, None)
        return env

    def test_official_sdk_imports_resolve(self):
        from huaweicloudsdkcore.auth.credentials import GlobalCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkcdn.v1 import CdnClient, ListDomainsRequest
        from huaweicloudsdkcdn.v1.region.cdn_region import CdnRegion
        for obj in (GlobalCredentials, Region, HttpConfig,
                    CdnClient, ListDomainsRequest, CdnRegion):
            self.assertTrue(callable(obj), obj)

    def test_sdk_fallback_returns_domains_with_env_credentials(self):
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak",
                   HUAWEI_SECRET_KEY="test-sk")
        with mock.patch.dict(os.environ, env, clear=True):
            domains = list_domains_via_sdk("cn-north-4")
        self.assertEqual(domains, [DOMAIN_1, DOMAIN_2])
        credentials = self._captured_credentials
        self.assertIsNotNone(credentials)
        self.assertEqual(getattr(credentials, "ak", None), "test-ak")
        self.assertEqual(getattr(credentials, "sk", None), "test-sk")

    def test_sdk_fallback_missing_env_credentials_raises_config(self):
        with mock.patch.dict(os.environ, self._clean_credential_env(), clear=True):
            with self.assertRaises(ConfigError) as ctx:
                list_domains_via_sdk("cn-north-4")
        message = str(ctx.exception)
        self.assertIn("AK/SK", message)
        self.assertNotIn("未安装", message)

    def test_sdk_pagination_via_total(self):
        first = _FakeSdkResponse([_FakeSdkDomain(DOMAIN_1)], 2)
        second = _FakeSdkResponse([_FakeSdkDomain(DOMAIN_2)], 2)
        self._fake_client.list_domains.side_effect = [first, second]
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak", HUAWEI_SECRET_KEY="test-sk")
        with mock.patch.dict(os.environ, env, clear=True):
            domains = list_domains_via_sdk("cn-north-4", limit=1)
        self.assertEqual(domains, [DOMAIN_1, DOMAIN_2])
        second_request = self._fake_client.list_domains.call_args_list[1][0][0]
        self.assertEqual(second_request.page_number, 2)


class TestNormalizeAndRender(unittest.TestCase):
    def test_normalize_flattens_tags(self):
        flat = normalize_domain(DOMAIN_1)
        self.assertEqual(flat["tags"], "env=test")

    def test_normalize_missing_tags_dash(self):
        flat = normalize_domain(DOMAIN_2)
        self.assertEqual(flat["tags"], "-")

    def test_table_contains_basic_info(self):
        table = render_table([DOMAIN_1, DOMAIN_2])
        for fragment in ("www.example.com", "cdn-0001", "online", "web",
                         "www.example.com.c.cdnhwc1.com", "download",
                         "env=test"):
            self.assertIn(fragment, table)

    def test_table_keeps_key_columns_first(self):
        table = render_table([DOMAIN_1])
        header = table.splitlines()[0]
        self.assertTrue(header.startswith("domain_name"))
        self.assertIn("cname", header)
        self.assertIn("business_type", header)

    def test_names(self):
        self.assertEqual(
            domain_names([DOMAIN_1, DOMAIN_2]),
            ["www.example.com", "static.example.com"])

    def test_names_fallback_to_id(self):
        self.assertEqual(domain_names([{"id": "cdn-9"}]), ["cdn-9"])


class TestMain(unittest.TestCase):
    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("list_cdn.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            rc = main(argv)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    def test_table_output(self):
        rc, out, err = self._run(
            ["--region", "cn-north-4"],
            [(json.dumps({"domains": [DOMAIN_1, DOMAIN_2], "total": 2}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("CDN 加速域名列表", out)
        self.assertIn("www.example.com", out)
        self.assertIn("online", out)
        self.assertEqual(err, "")

    def test_json_output(self):
        rc, out, err = self._run(
            ["--json"],
            [(json.dumps({"domains": [DOMAIN_1], "total": 1}), "", 0)])
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual(payload, [DOMAIN_1])

    def test_names_only_output(self):
        rc, out, err = self._run(
            ["--names-only"],
            [(json.dumps({"domains": [DOMAIN_1, DOMAIN_2], "total": 2}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("www.example.com", out)
        self.assertIn("static.example.com", out)
        self.assertNotIn("cname", out)

    def test_empty_instances_message(self):
        rc, out, err = self._run(
            ["--region", "cn-south-1"],
            [(json.dumps({"domains": [], "total": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("无 CDN 加速域名", out)
        self.assertIn("cn-south-1", out)

    def test_empty_with_filter_message(self):
        rc, out, _ = self._run(
            ["--domain-status", "online"],
            [(json.dumps({"domains": [], "total": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("domain_status=online", out)

    def test_status_filter_main_forwarded(self):
        fake = FakeRunner([
            (json.dumps({"domains": [DOMAIN_1], "total": 1}), "", 0)])
        with mock.patch("list_cdn.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr"):
            rc = main(["--domain-status", "online"])
        self.assertEqual(rc, 0)
        self.assertTrue(any("--domain_status=online" in part for part in fake.calls[0]))

    def test_empty_json_output(self):
        rc, out, err = self._run(
            ["--json"],
            [(json.dumps({"domains": [], "total": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out), [])

    def test_empty_names_only_output(self):
        rc, out, err = self._run(
            ["--names-only"],
            [(json.dumps({"domains": [], "total": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("共 0 个", out)

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
        with mock.patch("list_cdn.list_domains_via_sdk",
                        side_effect=ConfigError("huaweicloudsdkcdn 未安装")):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 1)
        self.assertIn("未安装", err)

    def test_hcloud_missing_falls_back_to_sdk(self):
        with mock.patch("list_cdn.list_domains_via_sdk",
                        return_value=[DOMAIN_1]):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 0)
        self.assertIn("www.example.com", out)

    def test_write_intent_argv_blocked(self):
        rc, out, err = self._run(["--operation", "DeleteDomain"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)

    def test_write_keyword_argv_blocked(self):
        rc, out, err = self._run(["--domain-name", "update-me"], [])
        self.assertEqual(rc, 1)
        self.assertIn("守卫拦截", err)

    def test_status_write_word_blocked(self):
        rc, out, err = self._run(["--business-type", "refresh-now"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)


class TestErrorHierarchy(unittest.TestCase):
    def test_subclasses(self):
        for exc in (GuardError, ConfigError, AuthError, ApiError):
            self.assertTrue(issubclass(exc, CdnListError))


if __name__ == "__main__":
    unittest.main()