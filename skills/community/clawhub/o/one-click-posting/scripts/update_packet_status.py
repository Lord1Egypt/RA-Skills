#!/usr/bin/env python3
import argparse
import json
from datetime import datetime
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update one-click posting packet status fields")
    parser.add_argument("--packet", required=True, help="Path to packet JSON")

    parser.add_argument("--deai-checked", action="store_true", help="Set preflight.deai_checked=true")
    parser.add_argument("--deai-unchecked", action="store_true", help="Set preflight.deai_checked=false")
    parser.add_argument("--risk-reviewed", action="store_true", help="Set preflight.risk_reviewed=true")
    parser.add_argument("--risk-unreviewed", action="store_true", help="Set preflight.risk_reviewed=false")

    parser.add_argument("--approve", metavar="APPROVER", help="Grant approval with approver name")
    parser.add_argument("--revoke-approval", action="store_true", help="Revoke approval")

    parser.add_argument("--set-publish-status", choices=["draft", "publishing", "published", "reviewing", "failed"], help="Update publish.status")
    parser.add_argument("--note", default="", help="Append one execution note")
    parser.add_argument("--json", action="store_true", help="Print full packet JSON after update")
    return parser.parse_args()


def load_packet(path_text: str):
    path = Path(path_text).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"Packet not found: {path}")
    packet = json.loads(path.read_text(encoding="utf-8"))
    return path, packet


def apply_updates(packet: dict, args: argparse.Namespace) -> None:
    preflight = packet.setdefault("preflight", {})
    approval = packet.setdefault("approval", {})
    publish = packet.setdefault("publish", {})
    execution = packet.setdefault("execution", {})
    notes = execution.setdefault("notes", [])

    if args.deai_checked:
        preflight["deai_checked"] = True
    if args.deai_unchecked:
        preflight["deai_checked"] = False

    if args.risk_reviewed:
        preflight["risk_reviewed"] = True
    if args.risk_unreviewed:
        preflight["risk_reviewed"] = False

    now_text = datetime.now().isoformat(timespec="seconds")

    if args.approve:
        approval["granted"] = True
        approval["approver"] = args.approve.strip()
        approval["approved_at"] = now_text
    if args.revoke_approval:
        approval["granted"] = False
        approval["approver"] = ""
        approval["approved_at"] = ""

    if args.set_publish_status:
        publish["status"] = args.set_publish_status

    if args.note.strip():
        notes.append({"at": now_text, "text": args.note.strip()})


def print_summary(path: Path, packet: dict, as_json: bool) -> None:
    if as_json:
        print(json.dumps(packet, ensure_ascii=False, indent=2))
        return

    approval = packet.get("approval", {})
    preflight = packet.get("preflight", {})
    publish = packet.get("publish", {})

    print(f"packet: {path}")
    print(f"publish.status: {publish.get('status', '')}")
    print(f"preflight.deai_checked: {preflight.get('deai_checked', False)}")
    print(f"preflight.risk_reviewed: {preflight.get('risk_reviewed', False)}")
    print(f"approval.granted: {approval.get('granted', False)}")
    if approval.get("granted"):
        print(f"approval.approver: {approval.get('approver', '')}")
        print(f"approval.approved_at: {approval.get('approved_at', '')}")


def main() -> None:
    args = parse_args()
    path, packet = load_packet(args.packet)
    apply_updates(packet, args)
    path.write_text(json.dumps(packet, ensure_ascii=False, indent=2), encoding="utf-8")
    print_summary(path, packet, as_json=args.json)


if __name__ == "__main__":
    main()
