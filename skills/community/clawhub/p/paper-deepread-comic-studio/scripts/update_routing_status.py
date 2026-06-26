from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


def unique_extend(current: list[str], values: list[str]) -> list[str]:
    result = list(current)
    for value in values:
        if value and value not in result:
            result.append(value)
    return result


def load_status(path: Path, template_path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return json.loads(template_path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("status_file", type=Path)
    parser.add_argument("--current-stage", default="")
    parser.add_argument("--next-stage", default="")
    parser.add_argument("--possible-user-input", action="append", default=[])
    parser.add_argument("--stage-delivery-report", default="")
    parser.add_argument("--delivery-bundle-zip", default="")
    parser.add_argument("--last-user-request", default="")
    parser.add_argument("--last-assistant-action", default="")
    parser.add_argument("--required-paper-count", type=int)
    parser.add_argument("--remaining-paper-without-report", action="append", default=[])
    parser.add_argument("--completed-stage", action="append", default=[])
    parser.add_argument("--routing-tag", action="append", default=[])
    parser.add_argument("--status-artifact", action="append", default=[])
    parser.add_argument("--directory-description-artifact", action="append", default=[])
    parser.add_argument("--authoritative-handoff-artifact", action="append", default=[])
    parser.add_argument("--artifact", action="append", default=[])
    parser.add_argument("--blocker", action="append", default=[])
    args = parser.parse_args()

    template_path = Path(__file__).resolve().parents[1] / "schemas" / "routing_status_template.json"
    data = load_status(args.status_file, template_path)
    data["updated_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
    if args.current_stage:
        data["current_stage"] = args.current_stage
    if args.next_stage:
        data["next_stage"] = args.next_stage
    data["possible_user_inputs_for_next_stage"] = unique_extend(
        data.get("possible_user_inputs_for_next_stage", []), args.possible_user_input
    )
    if args.stage_delivery_report:
        data["stage_delivery_report"] = args.stage_delivery_report
    if args.delivery_bundle_zip:
        data["delivery_bundle_zip"] = args.delivery_bundle_zip
    if args.last_user_request:
        data["last_user_request"] = args.last_user_request
    if args.last_assistant_action:
        data["last_assistant_action"] = args.last_assistant_action
    if args.required_paper_count is not None:
        data["required_paper_count"] = args.required_paper_count
    data["completed_stages"] = unique_extend(data.get("completed_stages", []), args.completed_stage)
    data["routing_tags"] = unique_extend(data.get("routing_tags", []), args.routing_tag)
    data["status_artifacts"] = unique_extend(data.get("status_artifacts", []), args.status_artifact)
    data["directory_description_artifacts"] = unique_extend(
        data.get("directory_description_artifacts", []), args.directory_description_artifact
    )
    data["authoritative_handoff_artifacts"] = unique_extend(
        data.get("authoritative_handoff_artifacts", []), args.authoritative_handoff_artifact
    )
    data["remaining_papers_without_authoritative_reports"] = unique_extend(
        data.get("remaining_papers_without_authoritative_reports", []), args.remaining_paper_without_report
    )
    data["key_artifacts"] = unique_extend(data.get("key_artifacts", []), args.artifact)
    data["blockers"] = unique_extend(data.get("blockers", []), args.blocker)
    args.status_file.parent.mkdir(parents=True, exist_ok=True)
    args.status_file.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status_file": str(args.status_file), "updated_at": data["updated_at"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
