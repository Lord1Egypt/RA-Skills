from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from property_advisor.ok_client import OKCoreSkillClient, resolve_ok_skill_root
from property_advisor.models import PublishPropertyRequest


def completed(*, returncode: int = 0, stdout: str = "", stderr: str = "") -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(args=[], returncode=returncode, stdout=stdout, stderr=stderr)


class OKCoreSkillClientTests(unittest.TestCase):
    def test_resolve_ok_skill_root_prefers_env_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "preferred-ok"
            (root / "scripts").mkdir(parents=True)
            (root / "scripts" / "cli.py").write_text("#!/usr/bin/env python3\n", encoding="utf-8")

            resolved = resolve_ok_skill_root(env={"OK_CORE_SKILL_ROOT": str(root)})

        self.assertEqual(resolved, root)

    def test_doctor_prefers_uv_runtime_when_smoke_passes(self) -> None:
        calls = []

        def runner(command, **kwargs):
            calls.append(command)
            if command[:5] == ["uv", "run", "python", "scripts/cli.py", "list-countries"]:
                return completed(stdout=json.dumps({"countries": [{"name": "australia"}]}))
            if command[:5] == ["uv", "run", "python", "scripts/cli.py", "check-login"]:
                return completed(stdout=json.dumps({"logged_in": True}))
            return completed(returncode=1, stderr="unexpected command")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "scripts").mkdir()
            (root / "scripts" / "cli.py").write_text("#!/usr/bin/env python3\n", encoding="utf-8")
            (root / ".venv" / "bin").mkdir(parents=True)
            (root / ".venv" / "bin" / "python").write_text("#!/usr/bin/env python3\n", encoding="utf-8")

            client = OKCoreSkillClient(
                skill_root=root,
                runner=runner,
                which=lambda command: "/usr/bin/uv" if command == "uv" else None,
                env={},
            )
            report = client.doctor(run_browser_smoke=True)

        self.assertTrue(report.ok)
        self.assertEqual(report.selected_runner, "uv")
        self.assertIn(["uv", "run", "python", "scripts/cli.py", "list-countries"], calls)
        self.assertNotIn([str(root / ".venv" / "bin" / "python"), "scripts/cli.py", "list-countries"], calls)

    def test_doctor_falls_back_to_project_venv(self) -> None:
        calls = []

        def runner(command, **kwargs):
            calls.append(command)
            if command[:5] == ["uv", "run", "python", "scripts/cli.py", "list-countries"]:
                return completed(returncode=1, stderr="uv runtime broken")
            if command[:3] == [str(root / ".venv" / "bin" / "python"), "scripts/cli.py", "list-countries"]:
                return completed(stdout=json.dumps({"countries": [{"name": "australia"}]}))
            if command[:3] == [str(root / ".venv" / "bin" / "python"), "scripts/cli.py", "check-login"]:
                return completed(stdout=json.dumps({"logged_in": True}))
            return completed(returncode=1, stderr="unexpected")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "scripts").mkdir()
            (root / "scripts" / "cli.py").write_text("#!/usr/bin/env python3\n", encoding="utf-8")
            (root / ".venv" / "bin").mkdir(parents=True)
            (root / ".venv" / "bin" / "python").write_text("#!/usr/bin/env python3\n", encoding="utf-8")

            client = OKCoreSkillClient(
                skill_root=root,
                runner=runner,
                which=lambda command: "/usr/bin/uv" if command == "uv" else None,
                env={},
            )
            report = client.doctor(run_browser_smoke=True)

        self.assertTrue(report.ok)
        self.assertEqual(report.selected_runner, "venv")
        self.assertTrue(any(command[0] == str(root / ".venv" / "bin" / "python") for command in calls))

    def test_doctor_fails_when_browser_smoke_fails(self) -> None:
        def runner(command, **kwargs):
            if command[:5] == ["uv", "run", "python", "scripts/cli.py", "list-countries"]:
                return completed(stdout=json.dumps({"countries": [{"name": "australia"}]}))
            if command[:5] == ["uv", "run", "python", "scripts/cli.py", "check-login"]:
                return completed(returncode=1, stderr="bridge unavailable")
            return completed(returncode=1, stderr="unexpected")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "scripts").mkdir()
            (root / "scripts" / "cli.py").write_text("#!/usr/bin/env python3\n", encoding="utf-8")

            client = OKCoreSkillClient(
                skill_root=root,
                runner=runner,
                which=lambda command: "/usr/bin/uv" if command == "uv" else None,
                env={},
            )
            report = client.doctor(run_browser_smoke=True)

        self.assertFalse(report.ok)
        browser_check = next(check for check in report.checks if check.name == "browser_smoke")
        self.assertFalse(browser_check.ok)

    def test_publish_property_builds_safe_dry_run_command(self) -> None:
        calls = []

        def runner(command, **kwargs):
            calls.append(command)
            if command[:5] == ["uv", "run", "python", "scripts/cli.py", "list-countries"]:
                return completed(stdout=json.dumps({"countries": [{"name": "uae"}]}))
            if command[:5] == ["uv", "run", "python", "scripts/cli.py", "publish-property"]:
                return completed(stdout=json.dumps({"success": True, "action": "dry_run"}))
            return completed(returncode=1, stderr="unexpected")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "scripts").mkdir()
            (root / "scripts" / "cli.py").write_text("#!/usr/bin/env python3\n", encoding="utf-8")

            client = OKCoreSkillClient(
                skill_root=root,
                runner=runner,
                which=lambda command: "/usr/bin/uv" if command == "uv" else None,
                env={},
            )
            result = client.publish_property(
                PublishPropertyRequest(
                    mode="rent",
                    country="uae",
                    property_type="apartment",
                    title="Furnished 1BR in Dubai Marina",
                    description="Near metro.",
                    price="8000",
                    location="Dubai Marina",
                    images=["/tmp/photo.jpg"],
                    bedrooms="1",
                    bathrooms="1",
                    phone="501234567",
                    rent_period="month",
                ),
                dry_run=True,
            )

        publish_call = calls[-1]
        self.assertTrue(result["success"])
        self.assertIn("--dry-run", publish_call)
        self.assertNotIn("--submit", publish_call)
        self.assertIn("--rent-period", publish_call)
        self.assertIn("/tmp/photo.jpg", publish_call)

    def test_publish_property_only_submits_when_requested(self) -> None:
        def runner(command, **kwargs):
            if command[:5] == ["uv", "run", "python", "scripts/cli.py", "list-countries"]:
                return completed(stdout=json.dumps({"countries": [{"name": "australia"}]}))
            if command[:5] == ["uv", "run", "python", "scripts/cli.py", "publish-property"]:
                return completed(stdout=json.dumps({"success": True, "action": "submitted"}))
            return completed(returncode=1, stderr="unexpected")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "scripts").mkdir()
            (root / "scripts" / "cli.py").write_text("#!/usr/bin/env python3\n", encoding="utf-8")

            client = OKCoreSkillClient(
                skill_root=root,
                runner=runner,
                which=lambda command: "/usr/bin/uv" if command == "uv" else None,
                env={},
            )
            client.publish_property(
                PublishPropertyRequest(
                    mode="sale",
                    country="australia",
                    property_type="apartment",
                    title="Apartment in Melbourne",
                    description="Bright apartment.",
                    price="900000",
                    location="Melbourne",
                    images=["/tmp/photo.jpg"],
                    phone="0412345678",
                ),
                submit=True,
            )

        self.assertIn("--submit", client.last_command)


if __name__ == "__main__":
    unittest.main()
