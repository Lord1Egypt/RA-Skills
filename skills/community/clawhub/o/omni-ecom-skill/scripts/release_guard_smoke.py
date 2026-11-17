#!/usr/bin/env python3
"""Regression check: clean release passes and avatars/.gitkeep is blocked."""

from __future__ import annotations

import json
import hashlib
import sys
import tempfile
import zipfile
from pathlib import Path

from release_guard import validate


ROOT = Path(__file__).resolve().parents[1]


def build_zip(source: Path, output: Path, add_gitkeep: bool = False, released: bool = False) -> None:
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(item for item in source.rglob("*") if item.is_file()):
            relative = path.relative_to(source)
            # importing release_guard writes __pycache__ into the very tree we
            # zip, so byte-code must be filtered or the smoke fails on itself
            if "__pycache__" in relative.parts or path.suffix == ".pyc":
                continue
            name=(Path("omni-ecom") / relative).as_posix()
            if released and relative.as_posix() in ('.codebuddy-plugin/plugin.json','version-info.json'):
                value=json.loads(path.read_text(encoding='utf-8-sig'))
                if relative.as_posix()=='.codebuddy-plugin/plugin.json': value['version']='2.0.3'
                else: value.update(team_version='2.0.3',release_status='released',release_ready=True,release_date='2026-09-08')
                archive.writestr(name,json.dumps(value,ensure_ascii=False))
            else: archive.write(path,name)
        if add_gitkeep:
            archive.writestr("omni-ecom/avatars/.gitkeep", "")
        if released:
            domains = ["workbuddy_native_multi_agent_pdf", "codex_native_multi_agent_pdf"]
            receipt = {
                "artifact_type": "omni-ecom.release-acceptance-receipt@2.0",
                "status": "release_acceptance_verified",
                "target_version": "2.0.3",
                "verified_at": "2026-09-08T00:00:00+00:00",
                "ledger_sha256": hashlib.sha256(b"synthetic-release-guard-contract").hexdigest(),
                "domains": domains,
                "optional_capabilities": {
                    "platform_api_read": "not_enabled",
                    "controlled_action_readback": "not_enabled",
                    "live_model_route_baseline": "not_enabled"
                },
                "evidence_fingerprints": [{"domain": domain, "sha256": hashlib.sha256(domain.encode()).hexdigest()} for domain in domains],
                "errors": [],
            }
            archive.writestr("omni-ecom/release-acceptance.json", json.dumps(receipt, ensure_ascii=False))


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="omni-ecom-release-guard-") as temp:
        temp_path = Path(temp)
        candidate = temp_path / "candidate.zip"
        clean = temp_path / "released.zip"
        bad = temp_path / "bad.zip"
        build_zip(ROOT,candidate)
        build_zip(ROOT, clean, released=True)
        build_zip(ROOT, bad, add_gitkeep=True, released=True)
        candidate_result = validate(candidate)
        clean_result = validate(clean)
        bad_result = validate(bad)
        cases = [
            {"name": "candidate_zip_is_not_releasable", "pass": candidate_result.get("status") == "FAIL"
             and "release_not_ready" in candidate_result.get("errors", [])},
            {"name": "clean_zip_passes", "pass": clean_result.get("status") == "PASS"},
            {
                "name": "gitkeep_is_blocked",
                "pass": bad_result.get("status") == "FAIL"
                and any(".gitkeep" in item for item in bad_result.get("errors", [])),
            },
        ]
    result = {
        "status": "PASS" if all(item["pass"] for item in cases) else "FAIL",
        "checks": f"{sum(bool(item['pass']) for item in cases)}/{len(cases)}",
        "cases": cases,
    }
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
