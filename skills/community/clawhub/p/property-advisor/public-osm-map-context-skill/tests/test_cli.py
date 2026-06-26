from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "cli.py"
FIXTURES = ROOT / "tests" / "fixtures"

sys.path.insert(0, str(ROOT / "scripts"))

from cli import JsonCache, PublicOsmClient, analyze_batch, extract_address_from_text, geocode_listing  # noqa: E402


class FakeGeocoder:
    def geocode(self, query: str):
        if query == "205 Normanby Rd, Southbank VIC 3006, Australia":
            return {
                "lat": -37.8252,
                "lng": 144.9558,
                "display_name": query,
                "source": "fixture_nominatim",
            }
        return None


class CliEndToEndTest(unittest.TestCase):
    def test_fixture_analyze_batch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            proc = subprocess.run(
                [
                    sys.executable,
                    str(CLI),
                    "--cache-dir",
                    tmp,
                    "analyze-batch",
                    "--input",
                    str(FIXTURES / "melbourne_listings.json"),
                    "--destination",
                    "Melbourne CBD VIC",
                    "--city",
                    "melbourne",
                    "--incremental",
                    "--fixture-dir",
                    str(FIXTURES / "osm"),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["provider"], "public_osm_fixture")
        self.assertTrue(payload["incremental"])
        self.assertEqual(len(payload["listings"]), 2)

        by_id = {item["id"]: item for item in payload["listings"]}
        archive = by_id["listing_archive"]
        for item in payload["listings"]:
            self.assertIn("listing_ref", item)
            self.assertTrue(item["listing_ref"]["url"])
            self.assertIn("google_maps_manual", item["verification_links"])

        archive_ref = archive["listing_ref"]
        self.assertEqual(archive_ref["id"], "listing_archive")
        self.assertEqual(archive_ref["title"], "The Archive, Southbank")
        self.assertEqual(archive_ref["price"], "A$786/wk")
        self.assertEqual(archive_ref["location"], "Southbank VIC")
        self.assertEqual(archive_ref["url"], "https://example.test/archive")
        self.assertEqual(archive_ref["image_url"], "https://example.test/archive.jpg")
        self.assertNotIn("description", archive_ref)
        self.assertEqual(archive["geo"]["precision"], "address")
        self.assertGreaterEqual(archive["amenities"]["supermarket_count"], 1)
        self.assertIsNotNone(archive["transit_access"])
        self.assertIn("origin", archive["transit_access"])
        self.assertEqual(archive["transit_access"]["distance_type"], "straight_line_estimate")
        self.assertFalse(archive["destination_access"]["verified_route"])
        self.assertIn("origin", archive["destination_access"])
        self.assertEqual(archive["destination_access"]["distance_type"], "straight_line_estimate")
        self.assertIn("not_google_maps_verified", archive["limitations"])
        self.assertIn("assessments", archive)
        self.assertIn("transport_access", archive["assessments"])
        self.assertIn("daily_convenience", archive["assessments"])
        self.assertIn("environment_risk", archive["assessments"])
        self.assertIn("area_maturity", archive["assessments"])
        self.assertTrue(archive["assessments"]["transport_access"]["conclusion"])
        self.assertTrue(archive["assessments"]["daily_convenience"]["evidence"])

        area = by_id["listing_area_only"]
        self.assertEqual(area["geo"]["precision"], "area")
        self.assertIn("area_level_location", area["limitations"])
        self.assertIn("precision_note", area["amenities"])
        self.assertIn("precision_note", area["destination_access"])
        self.assertIn("precision_note", area["risk_signals"])
        self.assertNotIn("near_primary_road_meters", area["risk_signals"])
        self.assertNotIn("distance_meters_range", area["transit_access"])
        self.assertEqual(area["transit_access"]["distance_type"], "not_available_for_area_level_location")
        self.assertIn("片区", area["assessments"]["transport_access"]["conclusion"])

    def test_doctor(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(CLI), "doctor"],
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["status"], "ok")
        self.assertFalse(payload["requires_api_key"])
        self.assertFalse(payload["requires_local_database"])

    def test_runtime_budget_exhaustion_is_fast_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            client = PublicOsmClient(JsonCache(Path(tmp)), max_live_seconds=1)
            client.started_at = time.monotonic() - 2

            timeout = client._request_timeout("overpass", bbox="test")

        self.assertIsNone(timeout)
        self.assertEqual(client.usage["errors"][0]["error"], "runtime_budget_exhausted")

    def test_missing_original_listing_url_is_marked(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "listings.json"
            input_path.write_text(
                json.dumps(
                    {
                        "listings": [
                            {
                                "id": "missing_url",
                                "title": "Apartment in Southbank",
                                "price": "A$500/wk",
                                "location": "Southbank VIC",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            args = argparse.Namespace(
                input=str(input_path),
                fixture_dir=str(FIXTURES / "osm"),
                cache_dir=tmp,
                cache_ttl_days=30,
                timeout=8,
                max_live_seconds=45,
                overpass_retries=1,
                geocode_strategy="photon-first",
                destination="Melbourne CBD VIC",
                city="melbourne",
                incremental=True,
                cluster_padding_km=1.0,
                level="deep",
            )

            payload = analyze_batch(args)

        item = payload["listings"][0]
        self.assertIsNone(item["listing_ref"]["url"])
        self.assertIn("original_listing_url_missing", item["limitations"])
        self.assertIn("assessments", item)

    def test_extracts_ok_com_concatenated_australian_address(self) -> None:
        title = "The Archive, Melbourne205 Normanby Rd, Southbank VIC 3006, Australia"

        address = extract_address_from_text(title)

        self.assertEqual(address, "205 Normanby Rd, Southbank VIC 3006, Australia")

    def test_title_address_is_used_when_structured_location_is_missing(self) -> None:
        listing = {
            "title": "The Archive, Melbourne205 Normanby Rd, Southbank VIC 3006, Australia",
            "price": "A$645 per week",
            "url": "https://example.test/archive",
        }

        geo = geocode_listing(FakeGeocoder(), listing)

        self.assertEqual(geo["precision"], "address")
        self.assertEqual(geo["geocode_query_used"], "205 Normanby Rd, Southbank VIC 3006, Australia")
        self.assertEqual(geo["address_extraction_source"], "title")

    def test_title_address_beats_area_only_location(self) -> None:
        listing = {
            "title": "The Archive, Melbourne205 Normanby Rd, Southbank VIC 3006, Australia",
            "location": "Melbourne",
            "price": "A$645 per week",
        }

        geo = geocode_listing(FakeGeocoder(), listing)

        self.assertEqual(geo["precision"], "address")
        self.assertEqual(geo["geocode_query_used"], "205 Normanby Rd, Southbank VIC 3006, Australia")
        self.assertEqual(geo["address_extraction_source"], "title")

    def test_ok_com_title_fixture_does_not_degrade_all_listings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            proc = subprocess.run(
                [
                    sys.executable,
                    str(CLI),
                    "--cache-dir",
                    tmp,
                    "analyze-batch",
                    "--input",
                    str(FIXTURES / "ok_com_melbourne_titles.json"),
                    "--destination",
                    "Melbourne CBD VIC",
                    "--city",
                    "melbourne",
                    "--incremental",
                    "--fixture-dir",
                    str(FIXTURES / "osm"),
                ],
                check=True,
                capture_output=True,
                text=True,
            )

        payload = json.loads(proc.stdout)
        self.assertEqual(len(payload["listings"]), 14)
        self.assertTrue(any(item["geo"]["precision"] != "missing" for item in payload["listings"]))
        for item in payload["listings"]:
            self.assertIn("listing_ref", item)
            self.assertTrue(item["listing_ref"]["url"])
            self.assertIn("google_maps_manual", item["verification_links"])
        archive = next(item for item in payload["listings"] if item["id"] == "ok_title_archive")
        self.assertEqual(archive["listing_ref"]["url"], "https://example.test/archive")
        self.assertEqual(archive["geo"]["geocode_query_used"], "205 Normanby Rd, Southbank VIC 3006, Australia")
        self.assertEqual(archive["geo"]["address_extraction_source"], "title")


if __name__ == "__main__":
    unittest.main()
