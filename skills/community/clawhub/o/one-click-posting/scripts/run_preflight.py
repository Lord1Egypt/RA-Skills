#!/usr/bin/env python3
import argparse
import json
from datetime import datetime
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run preflight checks on a publish packet")
    parser.add_argument("--packet", required=True, help="Path to packet JSON")
    parser.add_argument("--write-back", action="store_true", help="Write check results back to packet")
    parser.add_argument("--json", action="store_true", help="Print JSON report")
    parser.add_argument("--allow-unapproved", action="store_true", help="Allow pass even when approval.granted=false")
    return parser.parse_args()


def load_packet(path_text: str):
    path = Path(path_text).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"Packet not found: {path}")

    packet = json.loads(path.read_text(encoding="utf-8"))
    return path, packet


def evaluate(packet: dict, require_approval: bool):
    preflight = packet.get("preflight", {})
    approval = packet.get("approval", {})
    publish = packet.get("publish", {})
    content = packet.get("content", {})

    quality = preflight.get("quality_checks", {})
    checks = {
        "deai_checked": bool(preflight.get("deai_checked")),
        "risk_reviewed": bool(preflight.get("risk_reviewed")),
        "source_traceable": bool(preflight.get("source_traceable")),
        "platforms_present": bool(publish.get("platforms", [])),
        "title_present": bool(content.get("title")),
        "approval_granted": (not require_approval) or bool(approval.get("granted")),
    }

    for key, value in quality.items():
        checks[f"quality_{key}"] = bool(value)

    failed = [name for name, passed in checks.items() if not passed]
    warnings = preflight.get("warnings", [])

    return {
        "checked_at": datetime.now().isoformat(timespec="seconds"),
        "status": "pass" if not failed else "fail",
        "failed_checks": failed,
        "warnings": warnings,
        "checks": checks,
    }


def write_back(path: Path, packet: dict, report: dict) -> None:
    packet.setdefault("preflight", {})["last_checked_at"] = report["checked_at"]
    packet["preflight"]["last_report"] = report
    path.write_text(json.dumps(packet, ensure_ascii=False, indent=2), encoding="utf-8")


def print_report(report: dict, as_json: bool) -> None:
    if as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    print(f"status: {report['status']}")
    if report["failed_checks"]:
        print("failed_checks:")
        for item in report["failed_checks"]:
            print(f"- {item}")
    if report["warnings"]:
        print("warnings:")
        for item in report["warnings"]:
            print(f"- {item}")


def main() -> None:
    args = parse_args()
    path, packet = load_packet(args.packet)
    report = evaluate(packet, require_approval=not args.allow_unapproved)

    if args.write_back:
        write_back(path, packet, report)

    print_report(report, as_json=args.json)
    if report["status"] == "fail":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
