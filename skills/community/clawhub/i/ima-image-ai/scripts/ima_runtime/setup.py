from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

from ima_runtime.shared.config import DEFAULT_BASE_URL

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
REQUIREMENTS_PATH = REPO_ROOT / "requirements.txt"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="IMA Image AI Setup — bootstrap dependencies and verify local readiness",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--api-key", required=False, help="IMA Open API key. Can also use IMA_API_KEY env var")
    parser.add_argument("--install", action="store_true", help="Install missing Python dependencies from requirements.txt")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="API base URL")
    parser.add_argument("--language", default="en", help="Language for product labels (en/zh)")
    parser.add_argument("--output-json", action="store_true", help="Output setup report as JSON")
    return parser


def _requests_available() -> bool:
    return importlib.util.find_spec("requests") is not None


def _install_requirements() -> None:
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", str(REQUIREMENTS_PATH)],
        check=True,
    )


def _collect_diagnostics(api_key: str | None, base_url: str, language: str, include_network: bool) -> dict:
    doctor_module = importlib.import_module("ima_runtime.doctor")
    return doctor_module.collect_diagnostics(
        api_key=api_key,
        base_url=base_url,
        language=language,
        include_network=include_network,
    )


def collect_setup_report(api_key: str | None, install: bool, base_url: str, language: str) -> dict:
    report = {
        "dependencies": {
            "ok": True,
            "status": "ok",
            "requirements_file": str(REQUIREMENTS_PATH),
        },
        "doctor": None,
        "next_steps": [],
    }

    if not _requests_available():
        if install:
            _install_requirements()
            if not _requests_available():
                report["dependencies"]["ok"] = False
                report["dependencies"]["status"] = "install_failed"
                report["next_steps"].append("Dependency installation did not make `requests` importable. Check pip output.")
                return report
            report["dependencies"]["status"] = "installed"
        else:
            report["dependencies"]["ok"] = False
            report["dependencies"]["status"] = "missing"
            report["next_steps"].append(
                f"Run `python3 scripts/ima_runtime_setup.py --install{' --api-key <key>' if not api_key else ''}` to install dependencies."
            )
            return report

    doctor_report = _collect_diagnostics(
        api_key=api_key,
        base_url=base_url,
        language=language,
        include_network=False,
    )
    report["doctor"] = doctor_report

    if not api_key:
        report["next_steps"].append('Export `IMA_API_KEY=\"ima_your_key_here\"` and rerun `python3 scripts/ima_runtime_setup.py`.')
    else:
        report["next_steps"].append("Run `python3 scripts/ima_runtime_cli.py --task-type text_to_image --prompt \"a cinematic mountain sunset\" --output-json`.")
        report["next_steps"].append("Optionally run `python3 scripts/ima_runtime_doctor.py` for a full network/API diagnostic.")

    return report


def _print_text_report(report: dict) -> None:
    print("IMA Image AI Setup")
    print(f"Dependencies: {report['dependencies']['status']}")
    if report["doctor"] is not None:
        doctor_report = report["doctor"]
        print(f"API key: {'OK' if doctor_report['api_key']['ok'] else 'MISSING'} ({doctor_report['api_key']['message']})")
        print(f"Network: {doctor_report['network']['status']}")
    print("Next steps:")
    for step in report["next_steps"]:
        print(f"  - {step}")


def run_setup(api_key: str | None, install: bool, base_url: str, language: str, output_json: bool) -> int:
    report = collect_setup_report(api_key=api_key, install=install, base_url=base_url, language=language)
    success = bool(report["dependencies"]["ok"])
    if report["doctor"] is not None:
        success = success and bool(report["doctor"]["requests"]["ok"])

    if output_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if success else 1

    _print_text_report(report)
    return 0 if success else 1


def main() -> int:
    args = build_parser().parse_args()
    api_key = args.api_key or os.getenv("IMA_API_KEY")
    return run_setup(
        api_key=api_key,
        install=args.install,
        base_url=args.base_url,
        language=args.language,
        output_json=args.output_json,
    )


if __name__ == "__main__":
    sys.exit(main())
