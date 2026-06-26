from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from property_advisor.models import PreflightCheck, PreflightReport, PublishPropertyRequest
from property_advisor.publish import (
    BUSINESS_PUBLISH,
    CONSUMER_SEARCH,
    PublishPropertyOrchestrator,
    classify_user_intent,
    gt_publish_payload,
    infer_publish_request,
)


def completed(*, returncode: int = 0, stdout: str = "", stderr: str = "") -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(args=[], returncode=returncode, stdout=stdout, stderr=stderr)


class FakePublisher:
    source_name = "fake-publisher"
    runtime_mode = "fake"

    def __init__(self) -> None:
        self.calls = []
        self.last_command = []

    def doctor(self, *, run_browser_smoke: bool = True):
        return PreflightReport(
            ok=True,
            skill_root="/fake",
            selected_runner="fake",
            checks=[PreflightCheck(name="fake", ok=True, message="ok")],
            source_name=self.source_name,
            runtime_mode=self.runtime_mode,
        )

    def publish_property(self, request, *, submit: bool = False, save_draft: bool = False, dry_run: bool = False):
        self.calls.append({"request": request, "submit": submit, "save_draft": save_draft, "dry_run": dry_run})
        self.last_command = ["fake", "publish-property"]
        if submit:
            self.last_command.append("--submit")
        if dry_run:
            self.last_command.append("--dry-run")
        return {"success": True, "action": "submitted" if submit else "dry_run" if dry_run else "filled"}


class FakeMapClient:
    def __init__(self, *, fail: bool = False, precision: str = "address") -> None:
        self.fail = fail
        self.precision = precision
        self.calls = []

    def doctor(self):
        if self.fail:
            return {"status": "error"}
        return {"status": "ok"}

    def analyze_batch(self, *, listings, destination: str = "", city: str = ""):
        self.calls.append({"listings": listings, "destination": destination, "city": city})
        return {
            "status": "ok",
            "listings": [
                {
                    "id": "publish_draft",
                    "geo": {"precision": self.precision, "confidence": "medium"},
                    "verification_links": {"google_maps_manual": "https://maps.example.test/dubai-marina"},
                    "assessments": {
                        "transport_access": {
                            "conclusion": "Transport access has public map evidence for first-pass screening.",
                            "evidence": ["Nearest mapped transit stop is within a short straight-line range."],
                            "confidence": "medium",
                            "limitations": ["straight_line_estimate_only"],
                        },
                        "daily_convenience": {
                            "conclusion": "Daily convenience is supported by mapped amenities.",
                            "evidence": ["Public map data shows nearby everyday amenities."],
                            "confidence": "medium",
                            "limitations": [],
                        },
                        "environment_risk": {
                            "conclusion": "No obvious high-risk environment signal was found in public map screening.",
                            "evidence": ["No industrial signal was returned by the fixture."],
                            "confidence": "medium",
                            "limitations": [],
                        },
                        "area_maturity": {
                            "conclusion": "Area maturity looks usable from public map screening.",
                            "evidence": ["The fixture includes multiple common POI categories."],
                            "confidence": "medium",
                            "limitations": [],
                        },
                    },
                }
            ],
        }


class PublishIntentTests(unittest.TestCase):
    def test_consumer_search_stays_consumer(self) -> None:
        decision = classify_user_intent("帮我找 London studio")

        self.assertEqual(decision.intent, CONSUMER_SEARCH)

    def test_business_publish_rent_is_detected(self) -> None:
        decision = classify_user_intent("我要出租 Dubai Marina 1BR apartment")

        self.assertEqual(decision.intent, BUSINESS_PUBLISH)
        self.assertEqual(decision.mode, "rent")

    def test_business_publish_sale_is_detected(self) -> None:
        request = infer_publish_request(query_text="出售 Melbourne apartment", phone="0412345678", price="900000")

        self.assertEqual(request.mode, "sale")
        self.assertEqual(request.location, "Melbourne")

    def test_chinese_city_hint_infers_ok_country(self) -> None:
        request = infer_publish_request(query_text="帮我出租一套迪拜公寓")

        self.assertEqual(request.country, "uae")
        self.assertEqual(request.location, "迪拜")


class PublishOrchestratorTests(unittest.TestCase):
    def test_missing_required_fields_returns_follow_up_without_calling_publisher(self) -> None:
        publisher = FakePublisher()
        request = infer_publish_request(query_text="帮我出租一套迪拜公寓")
        orchestrator = PublishPropertyOrchestrator(ok_client=publisher, map_client=False)

        report = orchestrator.publish(request, dry_run=True)

        self.assertIn("price", report.missing_fields)
        self.assertIn("contact", report.missing_fields)
        self.assertEqual(publisher.calls, [])
        self.assertTrue(report.follow_up_questions)

    def test_missing_ok_publisher_runtime_returns_structured_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            request = PublishPropertyRequest(
                mode="rent",
                country="uae",
                property_type="apartment",
                price="8000",
                location="Dubai Marina",
                phone="501234567",
                images=["/tmp/photo.jpg"],
                bedrooms="1",
                bathrooms="1",
                query_text="Dubai Marina apartment for rent",
            )
            orchestrator = PublishPropertyOrchestrator(ok_skill_root=str(Path(tmp) / "missing-ok"), map_client=False)

            report = orchestrator.publish(request, dry_run=True)

        self.assertEqual(report.selected_source, "ok-core-skill")
        self.assertTrue(report.preflight)
        self.assertFalse(report.preflight.ok)
        self.assertIn("runtime unavailable", report.errors[0])

    def test_complete_request_dry_run_calls_ok_without_submit(self) -> None:
        publisher = FakePublisher()
        request = infer_publish_request(
            query_text="我要出租 Dubai Marina 1BR furnished apartment near metro with gym",
            country="uae",
            price="8000",
            phone="501234567",
            images=["/tmp/photo.jpg"],
        )
        orchestrator = PublishPropertyOrchestrator(ok_client=publisher, map_client=False)

        report = orchestrator.publish(request, dry_run=True)

        self.assertFalse(report.errors)
        self.assertEqual(len(publisher.calls), 1)
        self.assertFalse(publisher.calls[0]["submit"])
        self.assertTrue(publisher.calls[0]["dry_run"])
        self.assertNotIn("--submit", report.command)
        self.assertIn("ready to move in", report.generated_description)
        self.assertIn("Gym", report.request.amenities)

    def test_confirm_submit_adds_submit_flag(self) -> None:
        publisher = FakePublisher()
        request = PublishPropertyRequest(
            mode="sale",
            country="australia",
            property_type="apartment",
            price="900000",
            location="Melbourne",
            phone="0412345678",
            images=["/tmp/photo.jpg"],
            query_text="出售 Melbourne apartment",
        )
        orchestrator = PublishPropertyOrchestrator(ok_client=publisher, map_client=False)

        report = orchestrator.publish(request, confirm_submit=True)

        self.assertFalse(report.errors)
        self.assertIn("--submit", report.command)
        self.assertTrue(publisher.calls[0]["submit"])

    def test_submit_without_images_is_blocked(self) -> None:
        publisher = FakePublisher()
        request = PublishPropertyRequest(
            mode="sale",
            country="australia",
            property_type="apartment",
            price="900000",
            location="Melbourne",
            phone="0412345678",
            query_text="出售 Melbourne apartment",
        )
        orchestrator = PublishPropertyOrchestrator(ok_client=publisher, map_client=False)

        report = orchestrator.publish(request, confirm_submit=True)

        self.assertIn("images", report.missing_fields)
        self.assertEqual(publisher.calls, [])

    def test_remote_image_url_is_rejected(self) -> None:
        publisher = FakePublisher()
        request = PublishPropertyRequest(
            mode="rent",
            country="uae",
            property_type="apartment",
            price="8000",
            location="Dubai Marina",
            phone="501234567",
            images=["https://example.test/photo.jpg"],
            query_text="我要出租 Dubai Marina apartment",
        )
        orchestrator = PublishPropertyOrchestrator(ok_client=publisher, map_client=False)

        report = orchestrator.publish(request, dry_run=True)

        self.assertIn("image_paths_absolute", report.missing_fields)
        self.assertEqual(publisher.calls, [])

    def test_gt_payload_keeps_dry_run_contract(self) -> None:
        request = PublishPropertyRequest(
            mode="rent",
            property_type="apartment",
            title="Furnished 1BR in Richmond",
            description="Near station.",
            price="1200",
            location="Richmond",
            phone="07123456789",
            category_id="12345",
            images=["/tmp/gt-photo.jpg"],
            bedrooms="1",
            bathrooms="1",
            rent_period="month",
        )

        payload = gt_publish_payload(request)

        self.assertEqual(payload["category_id"], 12345)
        self.assertEqual(payload["location"]["display_name"], "Richmond")
        self.assertEqual(payload["attributes"]["rent_period"], "month")

    def test_sparse_publish_returns_contextual_followups_without_calling_publisher(self) -> None:
        publisher = FakePublisher()
        request = infer_publish_request(query_text="我要出租一套公寓")
        orchestrator = PublishPropertyOrchestrator(ok_client=publisher, map_client=False)

        report = orchestrator.publish(request, dry_run=True)

        self.assertEqual(report.readiness_status, "blocked_required")
        self.assertIn("location", report.required_missing_fields)
        self.assertIn("price", report.required_missing_fields)
        self.assertEqual(publisher.calls, [])
        self.assertTrue(any("卧室数" in item for item in report.contextual_follow_up_questions))

    def test_publish_copy_uses_map_and_does_not_invent_claims(self) -> None:
        publisher = FakePublisher()
        request = infer_publish_request(
            query_text="我要发布出租房源，Dubai Marina 月租金10000AED左右，1居室1卫，面积53平左右",
            country="uae",
            phone="501234567",
            images=["/tmp/photo.jpg"],
        )
        orchestrator = PublishPropertyOrchestrator(ok_client=publisher, map_client=FakeMapClient())

        report = orchestrator.publish(request, dry_run=True)

        self.assertFalse(report.errors)
        self.assertEqual(report.request.bedrooms, "1")
        self.assertEqual(report.request.bathrooms, "1")
        self.assertEqual(report.request.area_size, "570")
        self.assertEqual(report.request.original_area_size, "53")
        self.assertIn("about 570 sqft (53 sqm)", report.generated_description)
        self.assertIn("Transport access has public map evidence", report.generated_description)
        forbidden = ["Dubai Mall", "Burj Khalifa", "rooftop pool", "No pets", "security", "wardrobes"]
        self.assertFalse(any(term.lower() in report.generated_description.lower() for term in forbidden))
        self.assertIn("transport_access", report.map_assessments)

    def test_uk_publish_routes_to_gt_and_blocks_missing_gt_fields(self) -> None:
        ok_publisher = FakePublisher()
        gt_publisher = FakePublisher()
        request = infer_publish_request(
            query_text="London flat for rent",
            price="1200",
            phone="07123456789",
        )
        orchestrator = PublishPropertyOrchestrator(
            ok_client=ok_publisher,
            gt_client=gt_publisher,
            map_client=False,
        )

        report = orchestrator.publish(request, dry_run=True)

        self.assertEqual(report.request.resolved_market, "gt")
        self.assertIn("category_id", report.required_missing_fields)
        self.assertIn("postcode", report.required_missing_fields)
        self.assertEqual(ok_publisher.calls, [])
        self.assertEqual(gt_publisher.calls, [])

    def test_complete_uk_publish_calls_gt_dry_run(self) -> None:
        ok_publisher = FakePublisher()
        gt_publisher = FakePublisher()
        request = PublishPropertyRequest(
            mode="rent",
            country="uk",
            property_type="apartment",
            price="1200",
            location="London",
            postcode="SW1A 1AA",
            phone="07123456789",
            category_id="12345",
            query_text="London flat for rent",
        )
        orchestrator = PublishPropertyOrchestrator(
            ok_client=ok_publisher,
            gt_client=gt_publisher,
            map_client=False,
        )

        report = orchestrator.publish(request, dry_run=True)

        self.assertFalse(report.errors)
        self.assertEqual(report.request.resolved_market, "gt")
        self.assertEqual(ok_publisher.calls, [])
        self.assertEqual(len(gt_publisher.calls), 1)
        self.assertTrue(gt_publisher.calls[0]["dry_run"])


class PublishCliTests(unittest.TestCase):
    def test_route_cli_classifies_publish(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/cli.py", "route", "--query-text", "我要出租 Dubai Marina 1BR"],
            cwd=Path(__file__).resolve().parents[1],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["intent"], BUSINESS_PUBLISH)


if __name__ == "__main__":
    unittest.main()
