import importlib.util
import os
import sys
import json
import tempfile
import unittest
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

    def test_public_page_replaces_skipped_ipqs(self):
        skipped = intel.ProviderResult("ipqs", "IPQualityScore", "risk", "skipped",
                                       message="Missing credentials: IPQS_API_KEY")
        page = intel.ProviderResult("ipqs", "IPQualityScore", "risk", "success",
                                    data={"risk_score": 23}, collection_method="browser-public-page")
        actual = intel.merge_evidence([skipped], {"ipqs": page})[0]
        self.assertEqual(actual.status, "success")
        self.assertEqual(actual.data["risk_score"], 23)
        self.assertEqual(actual.collection_method, "browser-public-page")

    def test_real_public_page_fixture_loads(self):
        path = Path(__file__).parent / "fixtures" / "public-page-evidence-8.8.8.8.json"
        actual = intel.load_public_page_evidence([str(path)], "8.8.8.8")
        self.assertEqual(set(actual), {"ipinfo", "scamalytics", "ipqs", "ipdata", "ping0"})
        self.assertEqual(actual["ipdata"].data["risk_score"], 67)


class KeyedAdapterTests(unittest.TestCase):
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

    def test_ipqualityscore_shape(self):
        payload = {"success": True, "fraud_score": 88, "proxy": True, "vpn": False,
                   "tor": False, "hosting": True, "recent_abuse": True, "ASN": 64500}
        with mock.patch.object(intel, "request_json", return_value=payload), \
             mock.patch.dict(os.environ, {"IPQS_API_KEY": "secret"}):
            actual = intel.lookup_ipqs("203.0.113.1", 1)["data"]
        self.assertEqual(actual["risk_score"], 88)
        self.assertTrue(actual["is_abuser"])
        self.assertEqual(actual["asn"], "AS64500")

    def test_ipdata_threat_shape(self):
        payload = {"ip": "8.8.8.8", "country_code": "US",
                   "asn": {"asn": "AS15169", "name": "Google", "type": "hosting", "route": "8.8.8.0/24"},
                   "threat": {"is_proxy": False, "is_datacenter": True,
                              "is_known_abuser": False, "scores": {"threat": 12}}}
        with mock.patch.object(intel, "request_json", return_value=payload), \
             mock.patch.dict(os.environ, {"IPDATA_API_KEY": "secret"}):
            actual = intel.lookup_ipdata("8.8.8.8", 1)["data"]
        self.assertEqual(actual["risk_score"], 12)
        self.assertTrue(actual["is_hosting"])

    def test_scamalytics_nested_shape(self):
        payload = {"scamalytics": {"scamalytics_score": 77,
                   "scamalytics_proxy": {"is_vpn": "yes", "is_tor": "no", "is_datacenter": "yes"}},
                   "external_datasources": {"ipinfo": {"asn": "AS64500"}}}
        env = {"SCAMALYTICS_API_URL": "https://example.test/check", "SCAMALYTICS_API_KEY": "secret"}
        with mock.patch.object(intel, "request_json", return_value=payload), mock.patch.dict(os.environ, env):
            actual = intel.lookup_scamalytics("203.0.113.1", 1)["data"]
        self.assertEqual(actual["risk_score"], 77)
        self.assertTrue(actual["is_vpn"])
        self.assertFalse(actual["is_tor"])
        self.assertEqual(actual["asn"], "AS64500")


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
            (intel.ProviderResult("ipqs", "IPQualityScore", "risk", "skipped",
                                  message="Missing credentials: IPQS_API_KEY"),
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
            intel.ProviderResult("ipqs", "IPQualityScore", "risk", "skipped",
                                 message="Missing credentials: IPQS_API_KEY"),
            intel.ProviderResult("abuseipdb", "AbuseIPDB", "abuse", "skipped",
                                 message="Missing credentials: ABUSEIPDB_API_KEY"),
            result("ipapi-is", {"is_abuser": True}),
            result("scamalytics", {"risk_score": 0}),
        ], False)
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
            intel.ProviderResult("ipdata", "ipdata", "risk", "skipped", message="Missing credentials"),
        ], False)
        markdown = intel.render_markdown(report)
        self.assertIn("# IP Intelligence Report: 8.8.8.8", markdown)
        self.assertIn("## Comprehensive assessment", markdown)
        self.assertIn("IPQualityScore", markdown)
        self.assertIn("Missing credentials", markdown)
        self.assertIn("## Source details", markdown)

    def test_presentation_order_is_stable(self):
        report = intel.build_report("8.8.8.8", [
            result("ping0", {"risk_score": 99}),
            result("ipqs", {"risk_score": 1}),
            result("ipapi-is", {"is_abuser": True}),
            result("proxycheck", {"country_code": "US"}),
            result("ping0", {}, status="unavailable"),
            result("scamalytics", {}, status="error"),
        ], False)
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
        ], False)
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

    def test_html_contains_distinct_english_and_chinese_risk_states(self):
        report = intel.build_report("8.8.8.8", [
            intel.ProviderResult("ipqs", "IPQualityScore", "risk", "skipped",
                                 message="Missing credentials: IPQS_API_KEY"),
            intel.ProviderResult("abuseipdb", "AbuseIPDB", "abuse", "skipped",
                                 message="Missing credentials: ABUSEIPDB_API_KEY"),
            result("ipapi-is", {"is_abuser": True}),
        ], False)
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
        report = intel.build_report("8.8.8.8", [], False)
        self.assertEqual(report["schema_version"], "1.1")
        self.assertEqual(report["tool_version"], "1.3.1")


if __name__ == "__main__":
    unittest.main()
