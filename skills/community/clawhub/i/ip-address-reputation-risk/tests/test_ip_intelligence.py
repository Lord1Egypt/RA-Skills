import importlib.util
import io
import os
import sys
import json
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).parents[1] / "scripts" / "ip_intelligence.py"
SPEC = importlib.util.spec_from_file_location("ip_intelligence", SCRIPT)
intel = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = intel
SPEC.loader.exec_module(intel)


def result(provider_id, data, status="success"):
    return intel.ProviderResult(provider_id, provider_id, "risk", status, data=data)


class InputTests(unittest.TestCase):
    def test_normalizes_public_ipv6(self):
        self.assertEqual(intel.public_ip("2606:4700:4700:0:0:0:0:1111"), "2606:4700:4700::1111")

    def test_rejects_non_public_and_hostnames(self):
        for value in ("127.0.0.1", "10.0.0.1", "example.com", "::1", "2001:db8::1"):
            with self.subTest(value=value), self.assertRaises(intel.LookupError):
                intel.public_ip(value)

    def test_unknown_provider_is_rejected(self):
        with self.assertRaises(intel.LookupError):
            intel.select_providers("rdap,unknown", None)

    def test_nullish_provider_strings_are_empty(self):
        for value in ("nil", "NULL", " n/a ", "unknown"):
            with self.subTest(value=value):
                self.assertIsNone(intel.text_value(value))

    def test_profiles_select_expected_provider_sets(self):
        default = [provider.id for provider in intel.select_providers(None, None)]
        fast = [provider.id for provider in intel.select_providers(None, None, "fast")]
        resilient = [provider.id for provider in intel.select_providers(None, None, "resilient")]
        self.assertEqual(default, fast)
        self.assertEqual(fast, list(intel.PROFILE_PROVIDER_IDS["fast"]))
        self.assertNotIn("ip-api", resilient)
        self.assertNotIn("ping0", resilient)

    def test_default_cli_mode_writes_report_bundle(self):
        args = intel.parser().parse_args(["8.8.8.8"])
        self.assertIsNone(args.format)
        self.assertIsNone(args.report_dir)

    def test_include_raw_is_not_a_supported_option(self):
        with self.assertRaises(SystemExit):
            intel.parser().parse_args(["8.8.8.8", "--include-raw"])


class NetworkRetryTests(unittest.TestCase):
    class Response:
        headers = {"Content-Type": "application/json"}

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self, size):
            return b"{}"

        def geturl(self):
            return "https://get.geojs.io/"

    def test_transient_failure_is_retried_and_counted(self):
        provider = intel.Provider("retry", "Retry", "test", lambda ip, timeout: {
            "data": {"country_code": "US"},
            "raw": intel.request_json("https://get.geojs.io/", timeout),
        })
        with mock.patch.object(intel, "open_external_request", side_effect=[
                urllib.error.URLError("temporary"), self.Response()]), \
                mock.patch.object(intel.time, "sleep"):
            actual = intel.run_provider(provider, "8.8.8.8", 2, retries=2)
        self.assertEqual(actual.status, "success")
        self.assertEqual(actual.attempts, 2)

    def test_non_retryable_http_error_stops_immediately(self):
        error = urllib.error.HTTPError("https://get.geojs.io/", 404, "Not Found", {}, io.BytesIO())
        intel.REQUEST_STATE.retries = 2
        intel.REQUEST_STATE.attempts = 0
        with mock.patch.object(intel, "open_external_request", side_effect=error) as opener, \
                mock.patch.object(intel.time, "sleep"):
            with self.assertRaises(urllib.error.HTTPError):
                intel.request_bytes("https://get.geojs.io/", 2)
        self.assertEqual(opener.call_count, 1)

    def test_retry_after_is_capped_by_timeout_budget(self):
        error = urllib.error.HTTPError(
            "https://get.geojs.io/", 429, "Too Many Requests", {"Retry-After": "999"}, io.BytesIO())
        intel.REQUEST_STATE.retries = 1
        intel.REQUEST_STATE.attempts = 0
        intel.REQUEST_LAST_BY_HOST.clear()
        with mock.patch.object(intel, "open_external_request", side_effect=[error, self.Response()]), \
                mock.patch.object(intel.time, "sleep") as sleeper:
            intel.request_bytes("https://get.geojs.io/", 1)
        self.assertGreaterEqual(sleeper.call_count, 1)
        self.assertLessEqual(max(call.args[0] for call in sleeper.call_args_list), 1.0)


class ExternalPolicyTests(unittest.TestCase):
    def test_external_url_requires_allowlisted_https_without_credentials(self):
        accepted = intel.validate_external_url("https://api.ipapi.is/?q=8.8.8.8")
        self.assertEqual(accepted.hostname, "api.ipapi.is")
        for url in (
            "http://api.ipapi.is/?q=8.8.8.8",
            "https://evil.example/?q=8.8.8.8",
            "https://api.ipapi.is:8443/?q=8.8.8.8",
            "https://user:password@api.ipapi.is/?q=8.8.8.8",
            "https://api.ipapi.is/?q=8.8.8.8&token=secret",
            "https://api.ipapi.is/?q=8.8.8.8&api_key=secret",
        ):
            with self.subTest(url=url), self.assertRaises(intel.LookupError):
                intel.validate_external_url(url)

    def test_redirect_destination_is_validated_before_following(self):
        handler = intel.ApprovedRedirectHandler()
        with self.assertRaises(intel.LookupError):
            handler.redirect_request(mock.Mock(), None, 302, "Found", {}, "https://evil.example/next")

    def test_final_response_url_is_validated(self):
        class Response(NetworkRetryTests.Response):
            def geturl(self):
                return "https://evil.example/redirected"

        with mock.patch.object(intel, "open_external_request", return_value=Response()):
            with self.assertRaises(intel.LookupError):
                intel.request_bytes("https://api.ipapi.is/?q=8.8.8.8", 1)

    def test_provider_request_is_limited_to_its_approved_domains(self):
        provider = intel.Provider(
            "rdap", "RDAP", "registry",
            lambda ip, timeout: {"data": intel.request_json("https://get.geojs.io/", timeout)},
        )
        with mock.patch.object(intel, "open_external_request") as opener:
            actual = intel.run_provider(provider, "8.8.8.8", 1, retries=0)
        self.assertEqual(actual.status, "error")
        opener.assert_not_called()
        self.assertEqual(actual.request_domains, ())

    def test_policy_records_only_domains_that_received_a_request(self):
        class Response:
            headers = {"Content-Type": "application/json"}

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self, size):
                return b"{}"

            def geturl(self):
                return "https://rdap.org/"

        provider = intel.Provider(
            "rdap", "RDAP", "registry",
            lambda ip, timeout: {
                "data": {"country_code": "US"},
                "source_url": "https://rdap.org/",
                "payload": intel.request_json("https://rdap.org/", timeout),
            },
        )
        with mock.patch.object(intel, "open_external_request", return_value=Response()):
            actual = intel.run_provider(provider, "8.8.8.8", 1, retries=0)
        self.assertEqual(actual.status, "success")
        self.assertEqual(actual.request_domains, ("rdap.org",))
        self.assertEqual(intel.observed_provider_domains([provider], [actual]), ["rdap.org"])

    def test_confirmation_requires_flag_non_interactively(self):
        providers = [next(item for item in intel.PROVIDERS if item.id == "rdap")]
        with mock.patch.object(intel.sys.stdin, "isatty", return_value=False):
            with self.assertRaises(intel.LookupError):
                intel.confirm_external_access("8.8.8.8", providers, False)

    def test_interactive_confirmation_always_prompts(self):
        providers = [next(item for item in intel.PROVIDERS if item.id == "rdap")]
        with mock.patch.object(intel.sys.stdin, "isatty", return_value=True), \
                mock.patch("builtins.input", return_value="YES") as answer:
            mode = intel.confirm_external_access("8.8.8.8", providers, True)
        self.assertEqual(mode, "interactive")
        answer.assert_called_once()


class CliSafetyTests(unittest.TestCase):
    def test_default_mode_never_opens_network(self):
        stdout = io.StringIO()
        with mock.patch.object(intel.urllib.request, "urlopen") as urlopen, \
                mock.patch.object(intel, "open_external_request") as opener, \
                mock.patch.object(intel.sys, "stdout", stdout):
            exit_code = intel.main(["8.8.8.8", "--format", "json"])
        self.assertEqual(exit_code, 0)
        self.assertEqual(json.loads(stdout.getvalue())["policy"]["network_mode"], "local-only")
        urlopen.assert_not_called()
        opener.assert_not_called()

    def test_local_evidence_is_reported_without_network(self):
        stdout = io.StringIO()
        evidence_path = Path(__file__).parent / "fixtures" / "public-page-evidence-8.8.8.8.json"
        with mock.patch.object(intel, "open_external_request") as opener, \
                mock.patch.object(intel.sys, "stdout", stdout):
            exit_code = intel.main([
                "8.8.8.8", "--evidence", str(evidence_path), "--format", "json",
            ])
        report = json.loads(stdout.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertEqual(report["policy"]["network_mode"], "local-only")
        self.assertEqual(report["sources"][-1]["status"], "success")
        self.assertEqual(report["coverage"]["success"], 5)
        self.assertEqual(report["coverage"]["not-requested"], 5)
        opener.assert_not_called()

    def test_self_requires_external_confirmation_before_resolution(self):
        stderr = io.StringIO()
        with mock.patch.object(intel, "resolve_self_ip") as resolver, \
                mock.patch.object(intel.sys, "stderr", stderr):
            exit_code = intel.main(["--self", "--format", "json"])
        self.assertEqual(exit_code, 2)
        resolver.assert_not_called()
        self.assertIn("requires --external", stderr.getvalue())

    def test_external_noninteractive_without_flag_fails_before_request(self):
        stderr = io.StringIO()
        with mock.patch.object(intel.sys.stdin, "isatty", return_value=False), \
                mock.patch.object(intel, "open_external_request") as opener, \
                mock.patch.object(intel.sys, "stderr", stderr):
            exit_code = intel.main(["8.8.8.8", "--external", "--providers", "rdap", "--format", "json"])
        self.assertEqual(exit_code, 2)
        opener.assert_not_called()
        self.assertIn("requires --confirm-external", stderr.getvalue())

    def test_interactive_external_confirmation_allows_lookup(self):
        fake_report = intel.build_report("8.8.8.8", [], {
            "network_mode": "external-confirmed", "confirmation_mode": "interactive",
            "provider_domains": ["rdap.org"], "sent_fields": ["public_ip"],
            "policy_version": intel.POLICY_VERSION,
        })
        stdout = io.StringIO()
        with mock.patch.object(intel.sys.stdin, "isatty", return_value=True), \
                mock.patch("builtins.input", return_value="YES"), \
                mock.patch.object(intel, "lookup", return_value=fake_report) as lookup, \
                mock.patch.object(intel.sys, "stdout", stdout):
            exit_code = intel.main(["8.8.8.8", "--external", "--providers", "rdap", "--format", "json"])
        self.assertEqual(exit_code, 0)
        lookup.assert_called_once()
        self.assertEqual(json.loads(stdout.getvalue())["policy"]["network_mode"], "external-confirmed")


class ProviderIsolationTests(unittest.TestCase):
    def test_missing_credentials_are_visible(self):
        provider = intel.Provider("paid", "Paid", "risk", lambda ip, timeout: {}, ("TEST_SECRET",))
        with mock.patch.dict(os.environ, {}, clear=True):
            actual = intel.run_provider(provider, "8.8.8.8", 1)
        self.assertEqual(actual.status, "skipped")
        self.assertIn("TEST_SECRET", actual.message)

    def test_unexpected_failure_does_not_escape(self):
        def explode(ip, timeout):
            raise RuntimeError("secret at https://api.example.test/?key=super-secret")
        provider = intel.Provider("broken", "Broken", "risk", explode)
        actual = intel.run_provider(provider, "8.8.8.8", 1)
        self.assertEqual(actual.status, "error")
        self.assertNotIn("super-secret", actual.message)
        self.assertIn("<upstream-url>", actual.message)

    def test_experimental_failure_is_unavailable(self):
        def unavailable(ip, timeout):
            raise intel.LookupError("layout changed")
        provider = intel.Provider("page", "Page", "risk", unavailable, experimental=True)
        actual = intel.run_provider(provider, "8.8.8.8", 1)
        self.assertEqual(actual.status, "unavailable")

    def test_compliance_disabled_provider_is_not_requested(self):
        provider = next(item for item in intel.PROVIDERS if item.id == "ipqs")
        with mock.patch.object(intel, "request_json") as requester:
            actual = intel.run_provider(provider, "8.8.8.8", 1)
        self.assertEqual(actual.status, "not-requested")
        self.assertEqual(actual.collection_method, "disabled")
        self.assertIn("public-page evidence", actual.message)
        requester.assert_not_called()


class PublicPageEvidenceTests(unittest.TestCase):
    def write_evidence(self, item):
        handle = tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False)
        json.dump({"evidence": [item]}, handle)
        handle.close()
        self.addCleanup(lambda: Path(handle.name).unlink(missing_ok=True))
        return handle.name

    def test_valid_evidence_is_loaded_and_weight_discounted(self):
        path = self.write_evidence({
            "provider": "ipqs", "target_ip": "8.8.8.8",
            "source_url": "https://www.ipqualityscore.com/free-ip-lookup-proxy-vpn-test/lookup/8.8.8.8",
            "observed_at": "2026-08-12T03:00:00Z",
            "data": {"risk_score": 80, "asn": "15169", "is_proxy": True},
        })
        evidence = intel.load_public_page_evidence([path], "8.8.8.8")
        actual = evidence["ipqs"]
        self.assertEqual(actual.collection_method, "browser-public-page")
        self.assertEqual(actual.data["asn"], "AS15169")
        self.assertEqual(intel.provider_risk_estimate(actual)["weight"], 0.9)

    def test_ipdata_trust_score_converts_to_risk(self):
        path = self.write_evidence({
            "provider": "ipdata", "target_ip": "8.8.8.8",
            "source_url": "https://ipdata.co/8.8.8.8",
            "data": {"trust_score": 33},
        })
        actual = intel.load_public_page_evidence([path], "8.8.8.8")["ipdata"]
        self.assertEqual(actual.data["risk_score"], 67)

    def test_wrong_domain_and_target_are_rejected(self):
        cases = [
            {"provider": "ipqs", "target_ip": "8.8.8.8",
             "source_url": "https://evil.example/8.8.8.8", "data": {"risk_score": 0}},
            {"provider": "ipqs", "target_ip": "1.1.1.1",
             "source_url": "https://www.ipqualityscore.com/lookup/1.1.1.1", "data": {"risk_score": 0}},
        ]
        for item in cases:
            with self.subTest(item=item):
                path = self.write_evidence(item)
                with self.assertRaises(intel.LookupError):
                    intel.load_public_page_evidence([path], "8.8.8.8")

    def test_api_success_wins_over_public_page(self):
        api = intel.ProviderResult("ipqs", "IPQualityScore", "risk", "success",
                                   data={"risk_score": 10})
        page = intel.ProviderResult("ipqs", "IPQualityScore", "risk", "success",
                                    data={"risk_score": 90}, collection_method="browser-public-page")
        self.assertEqual(intel.merge_evidence([api], {"ipqs": page})[0].data["risk_score"], 10)

    def test_public_page_replaces_not_requested_ipqs(self):
        skipped = intel.ProviderResult("ipqs", "IPQualityScore", "risk", "not-requested",
                                       message="Official API disabled in compliance mode")
        page = intel.ProviderResult("ipqs", "IPQualityScore", "risk", "success",
                                    data={"risk_score": 23}, collection_method="browser-public-page")
        actual = intel.merge_evidence([skipped], {"ipqs": page})[0]
        self.assertEqual(actual.status, "success")
        self.assertEqual(actual.data["risk_score"], 23)
        self.assertEqual(actual.collection_method, "browser-public-page")

    def test_synthetic_public_page_fixture_loads(self):
        path = Path(__file__).parent / "fixtures" / "public-page-evidence-8.8.8.8.json"
        actual = intel.load_public_page_evidence([str(path)], "8.8.8.8")
        self.assertEqual(set(actual), {"ipinfo", "scamalytics", "ipqs", "ipdata", "ping0"})
        self.assertEqual(actual["ipdata"].data["risk_score"], 67)


class KeyedAdapterTests(unittest.TestCase):
    def test_rdap_keeps_registration_fields_without_contacts(self):
        payload = {
            "country": "US",
            "cidr0_cidrs": [{"v4prefix": "8.8.8.0", "length": 24}],
            "entities": [{"vcardArray": ["vcard", [
                ["fn", {}, "text", "Individual Name"],
                ["org", {}, "text", "Example Registry Organization"],
                ["email", {}, "text", "person@example.com"],
            ]]}],
        }
        with mock.patch.object(intel, "request_json", return_value=payload):
            actual = intel.lookup_rdap("8.8.8.8", 1)["data"]
        self.assertEqual(actual["organization"], "Example Registry Organization")
        self.assertEqual(actual["allocation_prefix"], "8.8.8.0/24")
        self.assertEqual(actual["registry_country"], "US")
        self.assertNotIn("fn", actual)
        self.assertNotIn("email", actual)

    def test_ipapi_is_flat_shape_and_target_validation(self):
        payload = {
            "ip": "8.8.8.8", "company_name": "Example Network", "asn_num": 15169,
            "asn_org": "Example ASN", "cc": "US", "lat": 37.4, "lon": -122.1,
            "is_proxy": False, "is_vpn": False, "is_tor": False,
            "is_datacenter": False, "is_abuser": True,
        }
        with mock.patch.object(intel, "request_json", return_value=payload):
            actual = intel.lookup_ipapi_is("8.8.8.8", 1)["data"]
        self.assertEqual(actual["asn"], "AS15169")
        self.assertEqual(actual["organization"], "Example ASN")
        self.assertEqual(actual["isp"], "Example Network")
        self.assertEqual(actual["country_code"], "US")
        self.assertEqual(actual["latitude"], 37.4)
        self.assertTrue(actual["is_abuser"])

        with mock.patch.object(intel, "request_json", return_value={**payload, "ip": "1.1.1.1"}):
            with self.assertRaises(intel.LookupError):
                intel.lookup_ipapi_is("8.8.8.8", 1)
        without_ip = {key: value for key, value in payload.items() if key != "ip"}
        with mock.patch.object(intel, "request_json", return_value=without_ip):
            with self.assertRaises(intel.LookupError):
                intel.lookup_ipapi_is("8.8.8.8", 1)

    def test_ipapi_is_nested_shape_remains_supported(self):
        payload = {
            "ip": "8.8.8.8",
            "company": {"name": "Nested ISP", "type": "hosting"},
            "asn": {"asn": 15169, "org": "Nested ASN", "route": "8.8.8.0/24"},
            "location": {"country_code": "US", "country": "United States",
                         "state": "California", "city": "Mountain View"},
            "is_proxy": "no", "is_vpn": "no", "is_tor": "no", "is_datacenter": "yes",
        }
        with mock.patch.object(intel, "request_json", return_value=payload):
            actual = intel.lookup_ipapi_is("8.8.8.8", 1)["data"]
        self.assertEqual(actual["asn"], "AS15169")
        self.assertEqual(actual["route_prefix"], "8.8.8.0/24")
        self.assertEqual(actual["region"], "California")
        self.assertTrue(actual["is_hosting"])

    def test_ipinfo_lite_shape(self):
        payload = {"ip": "8.8.8.8", "asn": "AS15169", "as_name": "Google LLC",
                   "as_type": "hosting", "country_code": "US", "country_name": "United States"}
        with mock.patch.object(intel, "request_json", return_value=payload), \
             mock.patch.dict(os.environ, {"IPINFO_TOKEN": "secret"}):
            actual = intel.lookup_ipinfo("8.8.8.8", 1)["data"]
        self.assertEqual(actual["asn"], "AS15169")
        self.assertEqual(actual["network_type"], "hosting")

    def test_ipinfo_token_uses_header_and_never_url(self):
        payload = {"ip": "8.8.8.8", "asn": "AS15169", "country_code": "US"}
        with mock.patch.object(intel, "request_json", return_value=payload) as requester, \
                mock.patch.dict(os.environ, {"IPINFO_TOKEN": "secret-token"}):
            intel.lookup_ipinfo("8.8.8.8", 1)
        url, timeout, headers = requester.call_args.args
        self.assertNotIn("secret-token", url)
        self.assertNotIn("token=", url)
        self.assertEqual(headers["Authorization"], "Bearer secret-token")

    def test_public_page_only_adapters_have_no_api_lookup(self):
        for provider_id in ("ipqs", "ipdata", "scamalytics"):
            with self.subTest(provider=provider_id):
                provider = next(item for item in intel.PROVIDERS if item.id == provider_id)
                self.assertFalse(provider.api_enabled)
                self.assertEqual(intel.run_provider(provider, "8.8.8.8", 1).status, "not-requested")


class Ping0ParserTests(unittest.TestCase):
    def test_label_alone_does_not_claim_native_ip(self):
        page = ("8.8.8.8 IP 类型 (说明?) IDC机房 IP 为什么 风控值 20% "
                "原生 IP (说明?) 未知 大模型检测 AS15169")
        headers = {"Content-Type": "text/html; charset=utf-8"}
        with mock.patch.object(intel, "request_bytes", return_value=(page.encode(), headers)):
            data = intel.lookup_ping0("8.8.8.8", 1)["data"]
        self.assertNotIn("native_ip", data)
        self.assertEqual(data["native_classification"], "未知")


class FusionTests(unittest.TestCase):
    def test_fact_consensus_and_disagreement_are_preserved(self):
        results = [
            result("one", {"country_code": "US", "city": "New York"}),
            result("two", {"country_code": "us", "city": "New York"}),
            result("three", {"country_code": "CA", "city": "Toronto"}),
        ]
        facts = intel.fuse_facts(results)
        self.assertEqual(facts["country_code"]["status"], "consensus")
        self.assertEqual(set(facts["country_code"]["sources"]), {"one", "two"})
        self.assertEqual(facts["country_code"]["alternatives"][0]["value"], "CA")

    def test_tied_fact_is_disputed(self):
        facts = intel.fuse_facts([
            result("one", {"city": "A"}), result("two", {"city": "B"}),
        ])
        self.assertEqual(facts["city"]["status"], "disputed")

    def test_locality_granularity_is_compatible(self):
        facts = intel.fuse_facts([
            result("one", {"city": "Berkeley"}),
            result("two", {"city": "Berkeley (North Berkeley)"}),
        ])
        self.assertEqual(facts["city"]["status"], "consensus")
        self.assertEqual(set(facts["city"]["sources"]), {"one", "two"})

    def test_risk_uses_only_numeric_scores_for_weighting(self):
        risk = intel.fuse_risk([
            result("ipqs", {"risk_score": 80}),
            result("scamalytics", {"risk_score": 75}),
            result("ipdata", {"is_abuser": True}),
        ])
        self.assertEqual(risk["score"], 85.6)
        self.assertEqual(risk["corroboration_uplift"], 8)
        self.assertEqual(risk["level"], "critical")
        self.assertEqual([item["provider"] for item in risk["estimates"]], ["ipqs", "scamalytics"])
        self.assertEqual(risk["unscored_signals"][0]["state"], "single-source")

    def test_boolean_signals_never_change_an_existing_score(self):
        baseline = intel.fuse_risk([result("ipqs", {"risk_score": 20})])
        actual = intel.fuse_risk([
            result("ipqs", {"risk_score": 20, "recent_abuse": True}),
            result("ipapi-is", {"is_abuser": True, "is_bot": True}),
        ])
        self.assertEqual(actual["score"], baseline["score"])
        self.assertEqual({item["signal"] for item in actual["unscored_signals"]},
                         {"abuser", "recent_abuse", "bot"})

    def test_unscored_signal_states(self):
        risk = intel.fuse_risk([
            result("ipapi-is", {"is_abuser": True}),
            result("ipqs", {"is_abuser": True, "recent_abuse": False}),
            result("scamalytics", {"recent_abuse": True}),
        ])
        by_signal = {item["signal"]: item for item in risk["unscored_signals"]}
        self.assertEqual(by_signal["abuser"]["state"], "corroborated")
        self.assertEqual(by_signal["recent_abuse"]["state"], "disputed")

    def test_score_origin_distinguishes_native_and_derived(self):
        risk = intel.fuse_risk([
            result("ipqs", {"risk_score": 12}),
            result("ipdata", {"risk_score": 40, "trust_score": 60}),
        ])
        origins = {item["provider"]: item["score_origin"] for item in risk["estimates"]}
        self.assertEqual(origins, {"ipqs": "native", "ipdata": "derived-from-trust-score"})

    def test_no_risk_evidence_is_unknown_not_low(self):
        risk = intel.fuse_risk([result("rdap", {"organization": "Example"})])
        self.assertIsNone(risk["score"])
        self.assertEqual(risk["level"], "unknown")

    def test_single_negative_boolean_does_not_create_zero_score(self):
        risk = intel.fuse_risk([result("ipapi-is", {"is_proxy": False, "is_vpn": False})])
        self.assertEqual(risk["level"], "unknown")

    def test_hosting_and_vpn_are_exposure_not_reputation(self):
        rows = [result("ipapi-is", {"is_hosting": True, "is_vpn": True})]
        self.assertEqual(intel.fuse_risk(rows)["level"], "unknown")
        exposure = intel.fuse_exposure(rows)
        self.assertEqual(exposure["level"], "elevated")
        self.assertEqual(set(exposure["positive_indicators"]), {"hosting", "vpn"})

    def test_contradicted_exposure_is_disputed(self):
        rows = [
            result("ipdata", {"is_tor": True, "is_hosting": True}),
            result("ipqs", {"is_tor": False}),
            result("scamalytics", {"is_tor": False}),
        ]
        exposure = intel.fuse_exposure(rows)
        self.assertEqual(exposure["positive_indicators"], ["hosting"])
        self.assertEqual(exposure["disputed_indicators"], ["tor"])
        self.assertEqual(exposure["level"], "notable")


class RenderingTests(unittest.TestCase):
    def test_provider_risk_states_distinguish_missing_and_unscored(self):
        cases = [
            (intel.ProviderResult("ipqs", "IPQualityScore", "risk", "not-requested",
                                  message="Official API disabled in compliance mode"),
             "public-page-score-unavailable"),
            (intel.ProviderResult("abuseipdb", "AbuseIPDB", "abuse", "skipped",
                                  message="Missing credentials: ABUSEIPDB_API_KEY"),
             "credential-required"),
            (result("ipapi-is", {"is_abuser": True}), "boolean-only"),
            (result("ipapi-is", {"country_code": "US"}), "no-numeric-score"),
            (result("ipqs", {"risk_score": 12}), "numeric"),
            (result("ping0", {}, status="unavailable"), "unavailable"),
            (result("proxycheck", {}, status="error"), "error"),
        ]
        for source, expected in cases:
            with self.subTest(source=source.id, expected=expected):
                self.assertEqual(intel.provider_risk_state(source), expected)

    def test_report_exposes_risk_provider_presentation_states(self):
        report = intel.build_report("8.8.8.8", [
            intel.ProviderResult("ipqs", "IPQualityScore", "risk", "not-requested",
                                 message="Official API disabled in compliance mode"),
            intel.ProviderResult("abuseipdb", "AbuseIPDB", "abuse", "skipped",
                                 message="Missing credentials: ABUSEIPDB_API_KEY"),
            result("ipapi-is", {"is_abuser": True}),
            result("scamalytics", {"risk_score": 0}),
        ])
        self.assertEqual(report["presentation"]["risk_provider_states"], {
            "ipqs": "public-page-score-unavailable",
            "abuseipdb": "credential-required",
            "ipapi-is": "boolean-only",
            "scamalytics": "numeric",
        })

    def test_markdown_contains_composite_and_every_source(self):
        report = intel.build_report("8.8.8.8", [
            intel.ProviderResult("ipqs", "IPQualityScore", "risk", "success",
                                 data={"risk_score": 10, "country_code": "US"}),
            intel.ProviderResult("ipdata", "ipdata", "risk", "not-requested",
                                 message="Official API disabled in compliance mode"),
        ])
        markdown = intel.render_markdown(report)
        self.assertIn("# IP Intelligence Report: 8.8.8.8", markdown)
        self.assertIn("## Comprehensive assessment", markdown)
        self.assertIn("IPQualityScore", markdown)
        self.assertIn("Official API disabled", markdown)
        self.assertIn("## Source details", markdown)

    def test_presentation_order_is_stable(self):
        report = intel.build_report("8.8.8.8", [
            result("ping0", {"risk_score": 99}),
            result("ipqs", {"risk_score": 1}),
            result("ipapi-is", {"is_abuser": True}),
            result("proxycheck", {"country_code": "US"}),
            result("ping0", {}, status="unavailable"),
            result("scamalytics", {}, status="error"),
        ])
        self.assertEqual(report["presentation"]["risk_provider_order"], list(intel.RISK_PROVIDER_ORDER))
        self.assertEqual([item["provider"] for item in report["assessment"]["risk"]["estimates"]],
                         ["ipqs", "ping0"])

    def test_html_is_self_contained_escaped_and_has_all_provider_tabs(self):
        dangerous = "</script><img src=x onerror=alert(1)>"
        report = intel.build_report("8.8.8.8", [
            intel.ProviderResult("ipqs", "IPQualityScore", "risk", "success",
                                 data={"risk_score": 10, "organization": dangerous}),
            intel.ProviderResult("abuseipdb", "AbuseIPDB", "abuse", "skipped",
                                 message="Missing credentials"),
            intel.ProviderResult("ipapi-is", "ipapi.is", "risk", "success",
                                 data={"is_abuser": True}),
        ])
        rendered = intel.render_html(report, "en")
        self.assertIn("<!doctype html>", rendered.lower())
        self.assertNotIn("src=\"http", rendered)
        self.assertNotIn("href=\"http", rendered)
        self.assertNotIn(dangerous, rendered)
        self.assertIn("type=\"application/octet-stream\"", rendered)
        self.assertIn("risk_provider_order", json.loads(
            __import__("base64").b64decode(
                rendered.split('id="report-data">', 1)[1].split("</script>", 1)[0]
            ).decode("utf-8")
        )["presentation"])
        self.assertIn("Evidence comparison matrix", rendered)
        self.assertIn("证据对比矩阵", rendered)
        self.assertIn("source.attempts", rendered)

    def test_html_contains_distinct_english_and_chinese_risk_states(self):
        report = intel.build_report("8.8.8.8", [
            intel.ProviderResult("ipqs", "IPQualityScore", "risk", "not-requested",
                                 message="Official API disabled in compliance mode"),
            intel.ProviderResult("abuseipdb", "AbuseIPDB", "abuse", "skipped",
                                 message="Missing credentials: ABUSEIPDB_API_KEY"),
            result("ipapi-is", {"is_abuser": True}),
        ])
        for language in ("en", "zh-CN"):
            with self.subTest(language=language):
                rendered = intel.render_html(report, language)
                self.assertIn(f'<html lang="{language}">', rendered)
                self.assertIn("Public-page score not obtained", rendered)
                self.assertIn("未获取到公开页评分", rendered)
                self.assertIn("Official API requires credentials", rendered)
                self.assertIn("官方接口需要凭据", rendered)
                self.assertIn("Boolean risk signals only", rendered)
                self.assertIn("仅返回布尔风险信号", rendered)
                self.assertIn("No numeric score returned", rendered)
                self.assertIn("未返回数值评分", rendered)
                self.assertIn("Provider unavailable", rendered)
                self.assertIn("渠道不可用", rendered)
                self.assertIn("Provider failed", rendered)
                self.assertIn("渠道失败", rendered)
                self.assertNotIn('barFill.style.width=`${source', rendered)

    def test_report_schema_version(self):
        report = intel.build_report("8.8.8.8", [])
        self.assertEqual(report["schema_version"], "2.0")
        self.assertEqual(report["tool_version"], "2.0.0")

    def test_not_requested_is_visible_in_json_markdown_and_html(self):
        report = intel.build_report("8.8.8.8", [
            intel.ProviderResult("geojs", "GeoJS", "geo", "not-requested",
                                 message="External queries are disabled"),
        ])
        serialized = json.dumps(report, ensure_ascii=False)
        self.assertIn('"not-requested"', serialized)
        self.assertIn("not requested", intel.render_markdown(report))
        self.assertIn("not-requested", intel.render_html(report, "en"))

    def test_reports_drop_raw_contacts_hostnames_and_credentials(self):
        report = intel.build_report("8.8.8.8", [
            intel.ProviderResult(
                "test", "Test", "test", "success",
                source_url="https://api.ipapi.is/?key=super-secret",
                data={
                    "risk_score": 4, "raw": {"secret": "raw-secret"},
                    "email": "person@example.com", "abuse_contacts": ["person@example.com"],
                    "reverse_dns": "private-host.example", "organization": "contact@example.com",
                },
                message="Authorization: Bearer super-secret; contact@example.com",
            ),
        ])
        serialized = json.dumps(report, ensure_ascii=False)
        for forbidden in ("raw-secret", "person@example.com", "private-host.example", "super-secret"):
            self.assertNotIn(forbidden, serialized)
        self.assertNotIn('"raw":', serialized)
        self.assertNotIn("email", serialized)
        self.assertNotIn("abuse_contacts", serialized)


if __name__ == "__main__":
    unittest.main()
