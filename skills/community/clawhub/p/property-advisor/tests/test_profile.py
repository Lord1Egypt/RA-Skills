from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from property_advisor.models import PreflightCheck, PreflightReport, SearchRequest
from property_advisor.profile import ProfileStore, UserProfile
from property_advisor.orchestrator import PropertyAdvisorOrchestrator


class EmptyClient:
    source_name = "ok-core-skill"
    runtime_mode = "ok"

    def doctor(self, *, run_browser_smoke: bool = True):
        return PreflightReport(
            ok=True,
            skill_root="/fake/ok-core-skill",
            selected_runner="uv",
            checks=[PreflightCheck(name="doctor", ok=True, message="ok")],
            source_name=self.source_name,
            runtime_mode=self.runtime_mode,
        )

    def search_property(self, **kwargs):
        return []

    def browse_property(self, **kwargs):
        return []

    def get_listing_detail(self, *, url: str):
        return {}


class ProfileStoreTests(unittest.TestCase):
    def test_profile_defaults_fill_missing_search_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = ProfileStore(tmp)
            store.save(
                UserProfile(
                    country="united kingdom",
                    city="London",
                    destination="King's Cross London",
                    budget_max=1800,
                    bedrooms=1,
                    preferred_sources=["gt"],
                    hard_requirements=["near tube"],
                )
            )

            request = SearchRequest(query_text="继续按我的偏好找", country_is_default=True, city_is_default=True)
            applied = store.apply_to_request(request)

        self.assertEqual(applied.country, "united kingdom")
        self.assertEqual(applied.city, "London")
        self.assertEqual(applied.destination, "King's Cross London")
        self.assertEqual(applied.budget_max, 1800)
        self.assertEqual(applied.bedrooms, 1)
        self.assertEqual(applied.source_hint, "gt")
        self.assertIn("near tube", applied.user_priorities)

    def test_current_request_overwrites_profile_when_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = ProfileStore(tmp)
            profile = UserProfile(country="australia", city="melbourne", budget_max=3000)
            request = SearchRequest(
                country="united kingdom",
                city="London",
                budget_max=2200,
                source_hint="gt",
                country_is_default=False,
                city_is_default=False,
            )

            updated = store.update_from_request(profile, request)
            reloaded = store.load()

        self.assertEqual(updated.country, "united kingdom")
        self.assertEqual(updated.city, "London")
        self.assertEqual(updated.budget_max, 2200)
        self.assertEqual(reloaded.preferred_sources[0], "gt")

    def test_profile_source_preference_does_not_override_explicit_country(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = ProfileStore(tmp)
            store.save(UserProfile(country="united kingdom", city="London", preferred_sources=["gt"]))

            applied = store.apply_to_request(
                SearchRequest(
                    country="australia",
                    city="melbourne",
                    country_is_default=False,
                    city_is_default=False,
                )
            )

        self.assertEqual(applied.country, "australia")
        self.assertEqual(applied.source_hint, "auto")

    def test_search_history_and_watch_files_are_written_locally(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = ProfileStore(tmp)
            request = SearchRequest(keyword="southbank", resolved_source_id="ok", resolved_market="ok")
            report = PropertyAdvisorOrchestrator(EmptyClient()).search(request)
            search_path = store.record_search(request, report)
            watch_path = store.watch_listing(
                url="https://example.test/listing",
                title="Example Listing",
                source_id="ok",
                note="interesting",
            )

            search_payload = json.loads(Path(search_path).read_text(encoding="utf-8"))
            watch_payload = json.loads(Path(watch_path).read_text(encoding="utf-8"))

        self.assertEqual(search_payload["selected_source"], "ok-core-skill")
        self.assertEqual(watch_payload["source_id"], "ok")
        self.assertEqual(watch_payload["note"], "interesting")

    def test_cli_explicit_default_country_and_city_are_saved(self) -> None:
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(
                [
                    sys.executable,
                    "scripts/cli.py",
                    "search",
                    "--keyword",
                    "southbank",
                    "--country",
                    "australia",
                    "--city",
                    "melbourne",
                    "--skip-map",
                    "--memory-dir",
                    tmp,
                ],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            profile = ProfileStore(tmp).load()

        self.assertEqual(profile.country, "australia")
        self.assertEqual(profile.city, "melbourne")


if __name__ == "__main__":
    unittest.main()
