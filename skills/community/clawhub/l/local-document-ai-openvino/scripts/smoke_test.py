#!/usr/bin/env python3
"""
Run the implemented skill modes against local smoke fixtures.
"""

from __future__ import annotations

import json
import importlib.util
import subprocess
import sys
import shutil
from pathlib import Path
from typing import Any


def run_cmd(cmd: list[str], cwd: Path) -> dict[str, Any]:
    proc = subprocess.run(
        cmd,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    status = None
    stdout = proc.stdout or ""
    stderr = proc.stderr or ""
    stream = stdout if stdout.strip() else stderr
    lines = [line.strip() for line in stream.splitlines() if line.strip()]
    if lines:
        try:
            status = json.loads(lines[-1])
        except json.JSONDecodeError:
            status = None
    return {
        "cmd": cmd,
        "returncode": proc.returncode,
        "ok": proc.returncode == 0,
        "status": status,
        "stdout": stdout,
        "stderr": stderr,
    }


def ensure_fixture(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def ensure_pdf_fixture(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if importlib.util.find_spec("fitz") is None:
        if not path.exists():
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return

    import fitz  # type: ignore

    if path.exists():
        try:
            with fitz.open(str(path)) as existing:
                if existing.page_count > 0:
                    return
        except Exception:
            pass

    doc = fitz.open()
    page = doc.new_page()
    y = 72
    for line in lines:
        page.insert_text((72, y), line)
        y += 36
    doc.save(str(path))
    doc.close()


def main() -> int:
    skill_dir = Path(__file__).resolve().parent.parent
    test_inputs = skill_dir / "test_inputs"

    ensure_pdf_fixture(
        test_inputs / "report.pdf",
        [
            "Smoke Test Report",
            "This report verifies parser artifact generation.",
        ],
    )
    ensure_pdf_fixture(
        test_inputs / "invoice.pdf",
        [
            "Invoice",
            "Invoice Number: INV-001",
            "Amount Due: 123.45",
            "Email: billing@example.com",
        ],
    )
    ensure_fixture(
        test_inputs / "signup_form.png",
        "Signup Form\nName:\nEmail:\nPhone:\n",
    )

    for artifact_dir in (
        skill_dir / "artifacts" / "smoke_report",
        skill_dir / "artifacts" / "smoke_signup_form",
        skill_dir / "artifacts" / "smoke_invoice",
    ):
        if artifact_dir.exists():
            shutil.rmtree(artifact_dir)

    commands = [
        [
            sys.executable,
            "scripts/run_skill.py",
            "--mode",
            "parse",
            "--file",
            "./test_inputs/report.pdf",
            "--out",
            "./artifacts/smoke_report",
        ],
        [
            sys.executable,
            "scripts/run_skill.py",
            "--mode",
            "to-code",
            "--file",
            "./test_inputs/signup_form.png",
            "--out",
            "./artifacts/smoke_signup_form",
            "--target",
            "react",
        ],
        [
            sys.executable,
            "scripts/run_skill.py",
            "--mode",
            "to-data",
            "--file",
            "./test_inputs/invoice.pdf",
            "--out",
            "./artifacts/smoke_invoice",
            "--extract",
            "tables,entities,kv_pairs",
        ],
    ]

    results = [run_cmd(cmd, skill_dir) for cmd in commands]
    payload = {
        "ok": all(result["ok"] for result in results),
        "skill_dir": str(skill_dir),
        "results": [
            {
                "cmd": " ".join(result["cmd"]),
                "returncode": result["returncode"],
                "ok": result["ok"],
                "status": result["status"],
            }
            for result in results
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
