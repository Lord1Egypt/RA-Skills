#!/usr/bin/env python3
"""End-to-end verification for Pet Companion Journal."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
TZ = timezone(timedelta(hours=8))


def run(script: str, args: list[str], env: dict[str, str], parse_json: bool = True):
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise SystemExit(result.returncode)
    return json.loads(result.stdout) if parse_json else result.stdout


def main():
    skill_json = json.loads((ROOT / "skill.json").read_text(encoding="utf-8"))
    clawhub_json = json.loads((ROOT / "clawhub.json").read_text(encoding="utf-8"))
    skill_md = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    if f"version: {skill_json['version']}" not in skill_md:
        raise SystemExit("SKILL.md frontmatter version must match skill.json")
    if clawhub_json["version"] != skill_json["version"]:
        raise SystemExit("clawhub.json version must match skill.json")

    with tempfile.TemporaryDirectory() as tmp:
        env = os.environ.copy()
        env["PET_COMPANION_HOME"] = str(Path(tmp) / "pet-data")

        print("[verify] creating pet profile")
        created = run("pet_manager.py", [
            "create",
            "--pet-id",
            "tofu",
            "--name",
            "Tofu",
            "--species",
            "cat",
            "--breed",
            "Ragdoll",
            "--birthday",
            "2022-05-01",
            "--personality-tags",
            "gentle",
            "sleepy",
        ], env)
        assert created["status"] == "created"

        print("[verify] adding health record")
        health = run("record_add.py", [
            "--pet-id",
            "tofu",
            "--type",
            "health",
            "--title",
            "Annual checkup",
            "--body",
            "Vet said overall condition looked normal; follow up on dental cleaning.",
            "--tags",
            "vet",
            "dental",
            "--extra",
            '{"clinic":"Demo Vet","follow_up":"dental cleaning quote"}',
        ], env)
        assert health["status"] == "created"

        print("[verify] querying record")
        query = run("record_query.py", [
            "--pet-id",
            "tofu",
            "--type",
            "health",
            "--keyword",
            "dental",
        ], env)
        assert query["count"] == 1
        assert query["records"][0]["extra"]["follow_up"] == "dental cleaning quote"

        print("[verify] adding reminder")
        due_at = (datetime.now(TZ) + timedelta(days=3)).replace(microsecond=0).isoformat()
        reminder = run("reminder_manage.py", [
            "add",
            "--pet-id",
            "tofu",
            "--title",
            "Dental cleaning follow-up",
            "--reminder-type",
            "follow-up",
            "--due-at",
            due_at,
            "--notes",
            "Call the clinic for an estimate.",
        ], env)
        assert reminder["status"] == "created"

        print("[verify] checking upcoming reminders")
        reminders = run("reminder_check.py", ["--pet-id", "tofu", "--days", "7"], env)
        assert len(reminders["upcoming"]) == 1

        print("[verify] exporting report")
        report = run("export_report.py", ["--pet-id", "tofu"], env, parse_json=False)
        assert "Tofu" in report
        assert "health: 1" in report

    print("[verify] ok")


if __name__ == "__main__":
    main()
