from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from property_advisor.gt_client import (
    GTCoreSkillClient,
    GTCoreSkillError,
    GTPublishSkillClient,
    canonicalize_gumtree_url,
    extract_gumtree_listing_id,
)
from property_advisor.models import PublishPropertyRequest


def completed(*, returncode: int = 0, stdout: str = "", stderr: str = "") -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(args=[], returncode=returncode, stdout=stdout, stderr=stderr)


BRIDGE_HELP = "usage: cli.py [-h] {check-login,login,logout,search,home-recommend,detail} ..."
API_HELP = "usage: cli.py [-h] {check-login,login,show-session,delete-session,search-listings,publish-listing} ..."


class GTCoreSkillClientTests(unittest.TestCase):
    def test_bridge_doctor_is_ok_when_logged_out(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "scripts").mkdir()
            (root / "scripts" / "cli.py").write_text("#!/usr/bin/env python3\n", encoding="utf-8")

            def runner(command, **kwargs):
                cwd = kwargs.get("cwd")
                if cwd != str(root):
                    return completed(returncode=1, stderr="unexpected cwd")
                if command == [sys.executable, "-B", "scripts/cli.py", "--help"]:
                    return completed(stdout=BRIDGE_HELP)
                if command == ["uv", "run", "python", "scripts/cli.py", "--help"]:
                    return completed(stdout=BRIDGE_HELP)
                if command == ["uv", "run", "python", "scripts/cli.py", "check-login"]:
                    return completed(stdout=json.dumps({"ok": True, "logged_in": False}))
                return completed(returncode=1, stderr="unexpected command")

            client = GTCoreSkillClient(
                skill_root=root,
                runner=runner,
                which=lambda command: "/usr/bin/uv" if command == "uv" else "/usr/bin/python3",
                env={},
            )
            report = client.doctor(run_browser_smoke=True)

        self.assertTrue(report.ok)
        self.assertEqual(report.runtime_mode, "bridge")
        self.assertFalse(report.logged_in)
        self.assertIn("公开搜索与详情抓取仍可用", " ".join(report.warnings))

    def test_bridge_search_and_detail_are_normalized(self) -> None:
        search_payload = {
            "ok": True,
            "items": [
                {
                    "title": "Bridge Listing",
                    "description": None,
                    "price": None,
                    "location": "Heathrow, London",
                    "url": "https://gumtree.com/p/property-to-rent/bridge-listing/1511100050",
                    "age": "0 days",
                    "number_of_images": 13,
                    "promotions": ["FEATURED"],
                }
            ],
        }
        detail_payload = {
            "ok": True,
            "item": {
                "title": "Bridge Listing",
                "description": "Modern studio flat in London.",
                "price": "£1,000pm",
                "location": "Heathrow, London",
                "url": "https://www.gumtree.com/p/property-to-rent/bridge-listing/1511100050",
                "age": "0 days",
                "category": "To Rent",
                "seller_name": "Tanya",
                "image_urls": ["https://img.gumtree.com/sample/1"],
                "attributes": {
                    "Number Of Bedrooms": "Studio",
                    "Date Available": "31 Mar 2026",
                    "Seller Type": "Agency",
                },
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "scripts").mkdir()
            (root / "scripts" / "cli.py").write_text("#!/usr/bin/env python3\n", encoding="utf-8")

            def runner(command, **kwargs):
                cwd = kwargs.get("cwd")
                if cwd != str(root):
                    return completed(returncode=1, stderr="unexpected cwd")
                if command == [sys.executable, "-B", "scripts/cli.py", "--help"]:
                    return completed(stdout=BRIDGE_HELP)
                if command == ["uv", "run", "python", "scripts/cli.py", "--help"]:
                    return completed(stdout=BRIDGE_HELP)
                if command[:5] == ["uv", "run", "python", "scripts/cli.py", "search"]:
                    return completed(stdout=json.dumps(search_payload))
                if command[:5] == ["uv", "run", "python", "scripts/cli.py", "detail"]:
                    return completed(stdout=json.dumps(detail_payload))
                return completed(returncode=1, stderr="unexpected command")

            client = GTCoreSkillClient(
                skill_root=root,
                runner=runner,
                which=lambda command: "/usr/bin/uv" if command == "uv" else "/usr/bin/python3",
                env={},
            )
            listings = client.search_property(
                keyword="flat",
                country="united kingdom",
                city="London",
                lang="en",
                max_results=1,
                search_location="London",
            )
            detail = client.get_listing_detail(url=listings[0]["url"])

        self.assertEqual(listings[0]["listing_id"], "1511100050")
        self.assertEqual(listings[0]["url"], "https://www.gumtree.com/p/property-to-rent/bridge-listing/1511100050")
        self.assertEqual(detail["price"], "£1,000pm")
        self.assertEqual(detail["bedrooms_text"], "Studio")
        self.assertEqual(detail["seller_type"], "Agency")
        self.assertTrue(detail["detail_fetched"])

    def test_api_search_normalizes_and_detail_gracefully_degrades(self) -> None:
        search_payload = {
            "ok": True,
            "items": [
                {
                    "id": 1511100050,
                    "title": "API Listing",
                    "description": "Fallback result",
                    "price": 1000,
                    "primaryLocation": "Richmond",
                    "primaryCategory": "To Rent",
                    "publicWebsiteUrl": "https://gumtree.com/p/property-to-rent/api-listing/1511100050",
                    "primaryImageUrl": "https://img.gumtree.com/sample/1",
                    "publishedDate": 1769760599069,
                }
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "scripts").mkdir()
            (root / "scripts" / "cli.py").write_text("#!/usr/bin/env python3\n", encoding="utf-8")

            def runner(command, **kwargs):
                cwd = kwargs.get("cwd")
                if cwd != str(root):
                    return completed(returncode=1, stderr="unexpected cwd")
                if command == [sys.executable, "-B", "scripts/cli.py", "--help"]:
                    return completed(stdout=API_HELP)
                if command == ["python3", "scripts/cli.py", "--help"]:
                    return completed(stdout=API_HELP)
                if command[:3] == ["python3", "scripts/cli.py", "search-listings"]:
                    return completed(stdout=json.dumps(search_payload))
                return completed(returncode=1, stderr="unexpected command")

            client = GTCoreSkillClient(
                skill_root=root,
                runner=runner,
                which=lambda command: "/usr/bin/python3" if command == "python3" else None,
                env={},
            )
            listings = client.search_property(
                keyword="flat",
                country="united kingdom",
                city="London",
                lang="en",
                max_results=1,
            )
            detail = client.get_listing_detail(url=listings[0]["url"])

        self.assertEqual(listings[0]["price"], "£1,000")
        self.assertEqual(listings[0]["listing_id"], "1511100050")
        self.assertFalse(detail["detail_fetched"])
        self.assertEqual(detail["detail_degraded_reason"], "GT 当前运行模式不支持详情补全")

    def test_gumtree_url_is_canonicalized(self) -> None:
        self.assertEqual(
            canonicalize_gumtree_url("https://gumtree.com/p/property-to-rent/test/1511100050?foo=1"),
            "https://www.gumtree.com/p/property-to-rent/test/1511100050",
        )
        self.assertEqual(extract_gumtree_listing_id("https://gumtree.com/p/test/1511100050"), "1511100050")

    def test_publish_client_uses_publish_listing_dry_run(self) -> None:
        calls = []
        publish_response = {
            "ok": True,
            "dry_run": True,
            "message": "publish payload 校验通过，未实际发起发布请求",
        }

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "scripts").mkdir()
            (root / "scripts" / "cli.py").write_text("#!/usr/bin/env python3\n", encoding="utf-8")

            def runner(command, **kwargs):
                calls.append(command)
                cwd = kwargs.get("cwd")
                if cwd != str(root):
                    return completed(returncode=1, stderr="unexpected cwd")
                if command == [sys.executable, "-B", "scripts/cli.py", "--help"]:
                    return completed(stdout=API_HELP)
                if command == ["python3", "scripts/cli.py", "publish-listing", "--help"]:
                    return completed(stdout="usage: publish-listing --payload-file FILE [--dry-run]")
                if command[:3] == ["python3", "scripts/cli.py", "publish-listing"]:
                    return completed(stdout=json.dumps(publish_response))
                return completed(returncode=1, stderr=f"unexpected command: {command}")

            client = GTPublishSkillClient(
                skill_root=root,
                runner=runner,
                which=lambda command: "/usr/bin/python3" if command == "python3" else None,
                env={},
            )
            report = client.doctor()
            result = client.publish_property(
                PublishPropertyRequest(
                    mode="rent",
                    property_type="apartment",
                    title="Furnished 1BR in Richmond",
                    description="Near station.",
                    location="Richmond",
                    price="1200",
                    phone="07123456789",
                    category_id="12345",
                    images=["/tmp/photo.jpg"],
                    rent_period="month",
                )
            )

        self.assertTrue(report.ok)
        self.assertTrue(result["dry_run"])
        self.assertIn("--dry-run", client.last_command)
        self.assertIn("publish-listing", client.last_command)

    def test_publish_client_submit_uses_real_publish_with_endpoint(self) -> None:
        publish_response = {
            "ok": True,
            "status": 201,
            "message": "发布成功",
        }

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "scripts").mkdir()
            (root / "scripts" / "cli.py").write_text("#!/usr/bin/env python3\n", encoding="utf-8")

            def runner(command, **kwargs):
                cwd = kwargs.get("cwd")
                if cwd != str(root):
                    return completed(returncode=1, stderr="unexpected cwd")
                if command == [sys.executable, "-B", "scripts/cli.py", "--help"]:
                    return completed(stdout=API_HELP)
                if command == ["python3", "scripts/cli.py", "publish-listing", "--help"]:
                    return completed(stdout="usage: publish-listing --payload-file FILE [--endpoint ENDPOINT] [--dry-run]")
                if command[:3] == ["python3", "scripts/cli.py", "publish-listing"]:
                    return completed(stdout=json.dumps(publish_response))
                return completed(returncode=1, stderr=f"unexpected command: {command}")

            client = GTPublishSkillClient(
                skill_root=root,
                runner=runner,
                which=lambda command: "/usr/bin/python3" if command == "python3" else None,
                env={},
            )
            result = client.publish_property(
                PublishPropertyRequest(
                    mode="rent",
                    property_type="apartment",
                    title="Furnished 1BR in Richmond",
                    description="Near station.",
                    location="Richmond",
                    postcode="TW9 1EJ",
                    price="1200",
                    phone="07123456789",
                    category_id="12345",
                    rent_period="month",
                    publish_endpoint="https://example.test/publish",
                ),
                submit=True,
                dry_run=False,
            )

        self.assertTrue(result["ok"])
        self.assertNotIn("--dry-run", client.last_command)
        self.assertIn("--endpoint", client.last_command)
        self.assertIn("https://example.test/publish", client.last_command)

    def test_publish_client_submit_without_endpoint_surfaces_gt_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "scripts").mkdir()
            (root / "scripts" / "cli.py").write_text("#!/usr/bin/env python3\n", encoding="utf-8")

            def runner(command, **kwargs):
                cwd = kwargs.get("cwd")
                if cwd != str(root):
                    return completed(returncode=1, stderr="unexpected cwd")
                if command == [sys.executable, "-B", "scripts/cli.py", "--help"]:
                    return completed(stdout=API_HELP)
                if command == ["python3", "scripts/cli.py", "publish-listing", "--help"]:
                    return completed(stdout="usage: publish-listing --payload-file FILE [--endpoint ENDPOINT] [--dry-run]")
                if command[:3] == ["python3", "scripts/cli.py", "publish-listing"]:
                    return completed(
                        returncode=2,
                        stdout=json.dumps({"ok": False, "error": "未配置 publish endpoint"}),
                    )
                return completed(returncode=1, stderr=f"unexpected command: {command}")

            client = GTPublishSkillClient(
                skill_root=root,
                runner=runner,
                which=lambda command: "/usr/bin/python3" if command == "python3" else None,
                env={},
            )

            with self.assertRaisesRegex(GTCoreSkillError, "publish endpoint"):
                client.publish_property(
                    PublishPropertyRequest(
                        mode="rent",
                        property_type="apartment",
                        title="Furnished 1BR in Richmond",
                        description="Near station.",
                        location="Richmond",
                        postcode="TW9 1EJ",
                        price="1200",
                        phone="07123456789",
                        category_id="12345",
                        rent_period="month",
                    ),
                    submit=True,
                    dry_run=False,
                )


if __name__ == "__main__":
    unittest.main()
