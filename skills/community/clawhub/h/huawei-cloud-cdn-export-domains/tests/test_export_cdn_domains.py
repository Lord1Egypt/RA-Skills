import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

# Never emit __pycache__/*.pyc for the bundled scripts module.
sys.dont_write_bytecode = True

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from export_cdn_domains import (  # noqa: E402
    ALLOWED_OPERATION,
    ApiError,
    AuthError,
    CdnExportError,
    ConfigError,
    ExportError,
    GuardError,
    MD_HEADERS,
    active_filter_descriptions,
    build_command,
    build_hcloud_command,
    classify_hcloud_failure,
    default_output_path,
    domain_names,
    export_report,
    extract_domains,
    extract_json,
    guard_operation,
    guard_text_from_argv,
    guard_write_intent,
    list_domains,
    list_domains_via_sdk,
    main,
    normalize_domain,
    render_csv,
    render_json,
    render_markdown,
    render_table,
    run_hcloud,
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
        self.assertFalse(guard_write_intent("--domain-status online --format csv download cdn domains"))
        self.assertFalse(guard_write_intent("query accelerated domains table"))

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

    def test_guard_text_strips_output_and_filter_values(self):
        text = guard_text_from_argv(
            ["--format", "csv", "--output", "cdn-delete-report.csv",
             "--domain-name", "refresh.example.com", "--region", "cn-north-1"])
        self.assertNotIn("cdn-delete-report.csv", text)
        self.assertNotIn("refresh.example.com", text)
        self.assertFalse(guard_write_intent(text))

    def test_guard_text_scans_following_flags(self):
        text = guard_text_from_argv(["--output", "--create-domain"])
        with self.assertRaises(GuardError):
            guard_write_intent(text)


class TestBuildCommand(unittest.TestCase):
    def test_basic(self):
        argv = build_command("cn-north-1")
        self.assertEqual(argv[0], "CDN")
        self.assertEqual(argv[1], "ListDomains")
        self.assertIn("--cli-region=cn-north-1", argv)
        self.assertIn("--page_size=100", argv)
        self.assertIn("--page_number=1", argv)

    def test_page_number_appended(self):
        argv = build_command("cn-north-1", page_number=3, limit=10)
        self.assertIn("--page_number=3", argv)
        self.assertIn("--page_size=10", argv)

    def test_filters_forwarded_server_side(self):
        argv = build_command("ap-southeast-1", domain_name="www.example.com",
                             business_type="web", domain_status="online",
                             service_area="mainland_china",
                             enterprise_project_id="0", exact_match=True,
                             show_tags=True, limit=10)
        self.assertIn("--domain_name=www.example.com", argv)
        self.assertIn("--business_type=web", argv)
        self.assertIn("--domain_status=online", argv)
        self.assertIn("--service_area=mainland_china", argv)
        self.assertIn("--enterprise_project_id=0", argv)
        self.assertIn("--exact_match=true", argv)
        self.assertIn("--show_tags=true", argv)

    def test_no_write_flags_ever_added(self):
        argv = build_command("cn-north-1", domain_status="online")
        for flag in argv:
            self.assertFalse(flag.lower().lstrip("-").startswith(
                ("create", "delete", "update", "enable", "disable", "refresh")))


class TestQualityWrapper(unittest.TestCase):
    def test_wrapped_with_quality_cli(self):
        with mock.patch.dict(os.environ, {"CDN_EXPORT_DOMAINS_SQC_BIN": "/fake/sqc"}, clear=False), \
                mock.patch("export_cdn_domains._hcloud_resolvable", return_value=True):
            os.environ.pop("CDN_EXPORT_DOMAINS_HCLOUD_BIN", None)
            os.environ.pop("SKILL_QUALITY_REPORT", None)
            cmd = build_hcloud_command(["CDN", "ListDomains", "--cli-region=cn-north-1"])
        self.assertEqual(cmd[0], "/fake/sqc")
        self.assertIn("--skill-name", cmd)
        self.assertIn("huawei-cloud-cdn-export-domains", cmd)
        self.assertIn("hcloud", cmd)

    def test_not_wrapped_when_hcloud_missing(self):
        with mock.patch.dict(os.environ, {"CDN_EXPORT_DOMAINS_SQC_BIN": "/fake/sqc"}, clear=False), \
                mock.patch("export_cdn_domains._hcloud_resolvable", return_value=False):
            os.environ.pop("CDN_EXPORT_DOMAINS_HCLOUD_BIN", None)
            os.environ.pop("SKILL_QUALITY_REPORT", None)
            cmd = build_hcloud_command(["CDN", "ListDomains"])
        self.assertEqual(cmd[0], "hcloud")

    def test_bare_override_runs_verbatim(self):
        with mock.patch.dict(os.environ,
                             {"CDN_EXPORT_DOMAINS_HCLOUD_BIN": "/fake/hcloud"},
                             clear=False):
            cmd = build_hcloud_command(["CDN", "ListDomains"])
        self.assertEqual(cmd[0], "/fake/hcloud")

    def test_report_toggle_disables_wrapper(self):
        with mock.patch.dict(os.environ,
                             {"SKILL_QUALITY_REPORT": "0",
                              "CDN_EXPORT_DOMAINS_SQC_BIN": "/fake/sqc"},
                             clear=False):
            os.environ.pop("CDN_EXPORT_DOMAINS_HCLOUD_BIN", None)
            cmd = build_hcloud_command(["CDN", "ListDomains"])
        self.assertEqual(cmd[0], "hcloud")


class TestExtract(unittest.TestCase):
    def test_extract_json_plain(self):
        self.assertEqual(extract_json(json.dumps({"domains": []})), {"domains": []})

    def test_extract_json_with_noise(self):
        self.assertEqual(extract_json("WARNING noise\n{\"a\": 1}\n"), {"a": 1})

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
            "", '{"error_code":"CDN.0004","error_msg":"not authorized"}', 1)
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
        with mock.patch("export_cdn_domains.subprocess.run", fake):
            domains = list_domains("cn-north-1")
        self.assertEqual(domains, [DOMAIN_1, DOMAIN_2])
        self.assertEqual(len(fake.calls), 1)

    def test_pagination_via_total(self):
        page1 = {"domains": [DOMAIN_1], "total": 2}
        page2 = {"domains": [DOMAIN_2], "total": 2}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("export_cdn_domains.subprocess.run", fake):
            domains = list_domains("cn-north-1", limit=1)
        self.assertEqual(domains, [DOMAIN_1, DOMAIN_2])
        self.assertEqual(len(fake.calls), 2)
        self.assertTrue(any("--page_number=2" in p for p in fake.calls[1]))

    def test_pagination_via_full_page_without_total(self):
        page1 = {"domains": [DOMAIN_1]}
        page2 = {"domains": []}
        fake = FakeRunner([(json.dumps(page1), "", 0), (json.dumps(page2), "", 0)])
        with mock.patch("export_cdn_domains.subprocess.run", fake):
            domains = list_domains("cn-north-1", limit=1)
        self.assertEqual(domains, [DOMAIN_1])

    def test_empty_region(self):
        fake = FakeRunner([(json.dumps({"domains": [], "total": 0}), "", 0)])
        with mock.patch("export_cdn_domains.subprocess.run", fake):
            domains = list_domains("cn-north-1")
        self.assertEqual(domains, [])

    def test_filters_forwarded_to_cli(self):
        fake = FakeRunner([(
            json.dumps({"domains": [DOMAIN_1], "total": 1}), "", 0)])
        with mock.patch("export_cdn_domains.subprocess.run", fake):
            list_domains("cn-north-1", domain_status="online",
                         business_type="web", domain_name="www.example.com")
        call = fake.calls[0]
        self.assertTrue(any("--domain_status=online" in part for part in call))
        self.assertTrue(any("--business_type=web" in part for part in call))
        self.assertTrue(any("--domain_name=www.example.com" in part for part in call))

    def test_use_error_rc0_raises_api_error(self):
        fake = FakeRunner([(
            "[USE_ERROR]Invalid parameter: domain_status\n\n"
            "Run `hcloud CDN ListDomains --help` for details.", "", 0)])
        with mock.patch("export_cdn_domains.subprocess.run", fake):
            with self.assertRaises(ApiError) as ctx:
                list_domains("cn-north-1")
        self.assertIn("参数错误", str(ctx.exception))

    def test_nonzero_exit_403(self):
        fake = FakeRunner([("", "403 Forbidden", 1)])
        with mock.patch("export_cdn_domains.subprocess.run", fake):
            with self.assertRaises(AuthError):
                list_domains("cn-north-1")

    def test_nonzero_exit_credentials(self):
        fake = FakeRunner([("", "ERROR: no AK configured", 1)])
        with mock.patch("export_cdn_domains.subprocess.run", fake):
            with self.assertRaises(ConfigError):
                list_domains("cn-north-1")

    def test_timeout(self):
        fake = FakeRunner([subprocess.TimeoutExpired(cmd="hcloud", timeout=120)])
        with mock.patch("export_cdn_domains.subprocess.run", fake):
            with self.assertRaises(ApiError):
                list_domains("cn-north-1")

    def test_sdk_fallback_when_hcloud_missing(self):
        with mock.patch("export_cdn_domains.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("export_cdn_domains.list_domains_via_sdk",
                           return_value=[DOMAIN_1, DOMAIN_2]) as sdk_mock:
            domains = list_domains("cn-north-1", domain_status="online",
                                   business_type="web", domain_name="example")
        self.assertEqual(domains, [DOMAIN_1, DOMAIN_2])
        self.assertEqual(sdk_mock.call_args.kwargs.get("domain_status"), "online")

    def test_sdk_fallback_unavailable_raises_config(self):
        with mock.patch("export_cdn_domains.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("export_cdn_domains.list_domains_via_sdk",
                           side_effect=ConfigError("huaweicloudsdkcdn 未安装")):
            with self.assertRaises(ConfigError):
                list_domains("cn-north-1")

    def test_sdk_request_signature(self):
        try:
            from huaweicloudsdkcdn.v1 import ListDomainsRequest
        except ImportError:
            self.skipTest("huaweicloudsdkcdn not installed")
        request = ListDomainsRequest(
            domain_name="www.example.com", business_type="web",
            domain_status="online", service_area="mainland_china",
            enterprise_project_id="0", page_size=100, page_number=1)
        self.assertEqual(request.domain_name, "www.example.com")
        self.assertEqual(request.page_number, 1)
        with self.assertRaises(TypeError):
            ListDomainsRequest(no_such_param=1)

    def test_error_envelope_403_raises_auth_error(self):
        # KooCLI returns API errors on stdout with rc=0 — they must not be
        # mistaken for an empty domain list.
        envelope = json.dumps({"error": {
            "error_code": "CDN.0004",
            "error_msg": "not authorized to perform: cdn:configuration:queryDomainList"}})
        fake = FakeRunner([(envelope, "", 0)])
        with mock.patch("export_cdn_domains.subprocess.run", fake):
            with self.assertRaises(AuthError):
                list_domains("cn-north-1")

    def test_error_envelope_generic_raises_api_error(self):
        envelope = json.dumps({"error_code": "CDN.9999", "error_msg": "boom"})
        fake = FakeRunner([(envelope, "", 0)])
        with mock.patch("export_cdn_domains.subprocess.run", fake):
            with self.assertRaises(ApiError):
                list_domains("cn-north-1")

    def test_use_error_notice_not_treated_as_error(self):
        # The multi-version notice prefix + a valid domains payload must parse.
        stdout = ("ListDomains is a multi-version API, where the version (v2) is default.\n"
                  + json.dumps({"domains": [DOMAIN_1], "total": 1}))
        fake = FakeRunner([(stdout, "", 0)])
        with mock.patch("export_cdn_domains.subprocess.run", fake):
            domains = list_domains("cn-north-1")
        self.assertEqual(domains, [DOMAIN_1])


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
    """Regression: the SDK fallback must use modules that exist in the official
    huaweicloudsdkcdn package and wire credentials from environment variables
    (GlobalCredentials has no env auto-discovery; CDN is a global service)."""

    _CREDENTIAL_ENV_KEYS = (
        "HUAWEICLOUD_SDK_AK", "HUAWEICLOUD_SDK_SK",
        "HUAWEI_ACCESS_KEY", "HUAWEI_SECRET_KEY",
        "HW_ACCESS_KEY", "HW_SECRET_KEY",
        "HUAWEI_AK", "HUAWEI_SK", "HW_AK", "HW_SK",
    )

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

    def _clean_credential_env(self):
        env = dict(os.environ)
        for name in self._CREDENTIAL_ENV_KEYS:
            env.pop(name, None)
        return env

    def test_sdk_fallback_returns_domains_with_env_credentials(self):
        env = dict(self._clean_credential_env(),
                   HUAWEI_ACCESS_KEY="test-ak", HUAWEI_SECRET_KEY="test-sk")
        with mock.patch.dict(os.environ, env, clear=True):
            domains = list_domains_via_sdk("cn-north-1")
        self.assertEqual(domains, [DOMAIN_1, DOMAIN_2])
        credentials = self._captured_credentials
        self.assertIsNotNone(credentials)
        self.assertEqual(getattr(credentials, "ak", None), "test-ak")

    def test_sdk_fallback_missing_env_credentials_raises_config(self):
        with mock.patch.dict(os.environ, self._clean_credential_env(), clear=True):
            with self.assertRaises(ConfigError) as ctx:
                list_domains_via_sdk("cn-north-1")
        message = str(ctx.exception)
        self.assertIn("AK/SK", message)
        self.assertNotIn("未安装", message)


class TestRender(unittest.TestCase):
    def test_normalize_flattens_tags(self):
        self.assertEqual(normalize_domain(DOMAIN_1)["tags"], "env=test")

    def test_normalize_missing_tags_dash(self):
        self.assertEqual(normalize_domain(DOMAIN_2)["tags"], "-")

    def test_table_contains_basic_info(self):
        table = render_table([DOMAIN_1, DOMAIN_2])
        for fragment in ("www.example.com", "cdn-0001", "online", "web",
                         "www.example.com.c.cdnhwc1.com", "download", "env=test"):
            self.assertIn(fragment, table)

    def test_table_keeps_key_columns_first(self):
        header = render_table([DOMAIN_1]).splitlines()[0]
        self.assertTrue(header.startswith("domain_name"))
        self.assertIn("cname", header)
        self.assertIn("business_type", header)

    def test_markdown_headers_and_rows(self):
        text = render_markdown([DOMAIN_1, DOMAIN_2], region="cn-north-1")
        self.assertIn("| " + " | ".join(MD_HEADERS) + " |", text)
        self.assertIn("www.example.com", text)
        self.assertIn("online", text)

    def test_markdown_empty_header_only(self):
        text = render_markdown([], region="cn-north-1")
        self.assertIn(MD_HEADERS[0], text)
        self.assertEqual(len(text.splitlines()), 2)

    def test_markdown_summary_line(self):
        text = render_markdown([DOMAIN_1], summary=True, region="cn-north-1")
        self.assertIn("共 1 个 CDN 加速域名", text)

    def test_markdown_pipe_escaping(self):
        text = render_markdown([{"domain_name": "a|b"}])
        self.assertIn("a\\|b", text)

    def test_csv_header_and_rows(self):
        text = render_csv([DOMAIN_1, DOMAIN_2])
        lines = text.splitlines()
        self.assertTrue(lines[0].startswith("domain_name"))
        self.assertIn("www.example.com", text)
        self.assertIn("static.example.com", text)

    def test_csv_empty_header_only(self):
        text = render_csv([])
        lines = text.splitlines()
        self.assertEqual(len(lines), 1)
        self.assertIn("domain_name", lines[0])

    def test_json_is_array(self):
        payload = json.loads(render_json([DOMAIN_1]))
        self.assertEqual(payload, [DOMAIN_1])

    def test_domain_names(self):
        self.assertEqual(domain_names([DOMAIN_1, DOMAIN_2]),
                         ["www.example.com", "static.example.com"])

    def test_default_output_path_extension(self):
        self.assertTrue(default_output_path("cn-north-1", "csv").endswith(".csv"))
        self.assertTrue(default_output_path("cn-north-1", "markdown").endswith(".md"))
        self.assertTrue(default_output_path("cn-north-1", "json").endswith(".json"))


class TestExport(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_csv_file_written(self):
        path = os.path.join(self.tmp, "out.csv")
        written = export_report([DOMAIN_1, DOMAIN_2], path, "csv", region="cn-north-1")
        self.assertTrue(os.path.isfile(written))
        content = open(written, encoding="utf-8").read()
        self.assertIn("www.example.com", content)

    def test_markdown_file_written_with_summary(self):
        path = os.path.join(self.tmp, "out.md")
        written = export_report([DOMAIN_1], path, "markdown", summary=True,
                                region="cn-north-1")
        content = open(written, encoding="utf-8").read()
        self.assertIn("共 1 个 CDN 加速域名", content)

    def test_json_file_written(self):
        path = os.path.join(self.tmp, "out.json")
        written = export_report([DOMAIN_1], path, "json", region="cn-north-1")
        self.assertEqual(json.loads(open(written, encoding="utf-8").read()), [DOMAIN_1])

    def test_empty_writes_header_only(self):
        path = os.path.join(self.tmp, "empty.csv")
        export_report([], path, "csv", region="cn-north-1")
        content = open(path, encoding="utf-8").read()
        self.assertIn("domain_name", content)

    def test_missing_dir_created(self):
        path = os.path.join(self.tmp, "sub", "deeper", "out.csv")
        written = export_report([DOMAIN_1], path, "csv", region="cn-north-1")
        self.assertTrue(os.path.isfile(written))

    def test_bad_path_raises_export_error(self):
        # A path whose parent is an existing *file* cannot be a directory.
        blocker = os.path.join(self.tmp, "blocker")
        open(blocker, "w").close()
        path = os.path.join(blocker, "out.csv")
        with self.assertRaises(ExportError):
            export_report([DOMAIN_1], path, "csv", region="cn-north-1")


class TestMain(unittest.TestCase):
    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("export_cdn_domains.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            rc = main(argv)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    def test_table_output(self):
        rc, out, err = self._run(
            ["--region", "cn-north-1", "--format", "table"],
            [(json.dumps({"domains": [DOMAIN_1, DOMAIN_2], "total": 2}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("CDN 加速域名列表", out)
        self.assertIn("www.example.com", out)
        self.assertEqual(err, "")

    def test_table_empty_message(self):
        rc, out, _ = self._run(
            ["--region", "cn-north-1", "--format", "table"],
            [(json.dumps({"domains": [], "total": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("无 CDN 加速域名", out)

    def test_csv_export_default_path_message(self):
        tmp = tempfile.mkdtemp()
        out_path = os.path.join(tmp, "o.csv")
        rc, out, err = self._run(
            ["--region", "cn-north-1", "--output", out_path],
            [(json.dumps({"domains": [DOMAIN_1], "total": 1}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn(out_path, out)
        self.assertTrue(os.path.isfile(out_path))
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)

    def test_empty_export_message(self):
        tmp = tempfile.mkdtemp()
        out_path = os.path.join(tmp, "e.csv")
        rc, out, _ = self._run(
            ["--region", "cn-north-1", "--output", out_path],
            [(json.dumps({"domains": [], "total": 0}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("无 CDN 加速域名", out)
        self.assertIn("空文件", out)
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)

    def test_auth_error_message(self):
        rc, out, err = self._run(["--format", "table"], [("", "403 Forbidden", 1)])
        self.assertEqual(rc, 1)
        self.assertIn("[错误]", err)
        self.assertIn("IAM", err)

    def test_missing_ak_sk_error_message(self):
        rc, out, err = self._run(["--format", "table"], [("", "ERROR: cli-ak empty", 1)])
        self.assertEqual(rc, 1)
        self.assertIn("AK/SK", err)

    def test_write_intent_argv_blocked(self):
        rc, out, err = self._run(["--operation", "DeleteDomain"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)

    def test_write_keyword_in_filter_value_passes(self):
        # "refresh.example.com" is a legit domain name; its value is excluded.
        rc, out, err = self._run(
            ["--format", "table", "--domain-name", "refresh.example.com"],
            [(json.dumps({"domains": [DOMAIN_1], "total": 1}), "", 0)])
        self.assertEqual(rc, 0)

    def test_page_size_out_of_range(self):
        rc, out, err = self._run(["--format", "table", "--page-size", "0"], [])
        self.assertEqual(rc, 1)
        self.assertIn("--page-size", err)


class TestErrorHierarchy(unittest.TestCase):
    def test_subclasses(self):
        for exc in (GuardError, ConfigError, AuthError, ApiError, ExportError):
            self.assertTrue(issubclass(exc, CdnExportError))


if __name__ == "__main__":
    unittest.main()