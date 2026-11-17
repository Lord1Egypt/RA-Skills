#!/usr/bin/env python3
"""Apply only explicit, scoped musical fingering decisions to a generated plan."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from plan_io import load_plan, save_plan


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("decisions", type=Path, help="model/human decisions matching manifest.decision_output_format")
    parser.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args()
    plan = load_plan(args.plan)
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    decision_payload = json.loads(args.decisions.read_text(encoding="utf-8"))
    if manifest.get("plan_fact_lock") != plan.get("recognition", {}).get("fact_lock", {}):
        raise ValueError("manifest does not belong to this locked score plan")
    allowed: dict[str, set[int]] = {}
    task_options: dict[str, dict[str, list[dict]]] = {}
    for task in manifest.get("tasks", []):
        task_id = str(task.get("task_id", ""))
        options = {
            str(option.get("option_id", "")): list(option.get("assignments", []))
            for option in task.get("candidate_options", [])
            if isinstance(option, dict) and str(option.get("option_id", ""))
        }
        if task_id and options:
            task_options[task_id] = options
        for candidate in task.get("alternatives", []):
            note_id = str(candidate.get("note_id", ""))
            values = candidate.get("allowed_fingers")
            if not isinstance(values, list):
                values = [candidate.get("current_finger"), candidate.get("shallow_finger"), candidate.get("deep_finger")]
            allowed[note_id] = {int(value) for value in values if int(value or 0) in {1, 2, 3, 4, 5}}
    decisions = decision_payload.get("decisions", [])
    if not isinstance(decisions, list):
        raise ValueError("decisions must be an array")
    by_id = {str(note["note_id"]): note for note in plan.get("notes", [])}
    applied = 0
    unresolved = []
    seen: set[str] = set()
    seen_tasks: set[str] = set()
    for row in decisions:
        if not isinstance(row, dict):
            raise ValueError("each decision must be an object")
        task_id = str(row.get("task_id", ""))
        if task_id:
            if task_id in seen_tasks or task_id not in task_options:
                raise ValueError(f"decision is outside the review manifest: {task_id}")
            seen_tasks.add(task_id)
            if row.get("resolved") is not True:
                unresolved.append(task_id)
                continue
            option_id = str(row.get("option_id", ""))
            assignments = task_options[task_id].get(option_id)
            if not assignments:
                raise ValueError(f"{task_id}: option must be one of {sorted(task_options[task_id])}")
            for assignment in assignments:
                note_id = str(assignment.get("note_id", ""))
                finger = int(assignment.get("finger", 0))
                if note_id in seen or note_id not in allowed or note_id not in by_id:
                    raise ValueError(f"{task_id}: assignment is outside the review manifest: {note_id}")
                if finger not in allowed[note_id]:
                    raise ValueError(f"{task_id}: {note_id} is not one of its candidate fingers")
                note = by_id[note_id]
                if bool(note.get("locked")) and int(note.get("finger", 0)) != finger:
                    raise ValueError(f"{note_id}: an existing editorial fingering is locked and cannot be overwritten")
                seen.add(note_id)
                note["finger"] = finger
                note["source"] = "musical_review"
                note["review_decision"] = str(row.get("reason", "targeted phrase review"))
                applied += 1
            continue
        note_id = str(row.get("note_id", ""))
        if task_options:
            raise ValueError("this manifest requires whole-phrase task_id/option_id decisions; do not mix candidate fingers")
        if note_id in seen or note_id not in allowed or note_id not in by_id:
            raise ValueError(f"decision is outside the review manifest: {note_id}")
        seen.add(note_id)
        if row.get("resolved") is not True:
            unresolved.append(note_id)
            continue
        finger = int(row.get("finger", 0))
        if finger not in {1, 2, 3, 4, 5}:
            raise ValueError(f"{note_id}: finger must be 1..5")
        if finger not in allowed[note_id]:
            raise ValueError(f"{note_id}: finger must be one of this task's existing candidates: {sorted(allowed[note_id])}")
        note = by_id[note_id]
        if bool(note.get("locked")) and int(note.get("finger", 0)) != finger:
            raise ValueError(f"{note_id}: an existing editorial fingering is locked and cannot be overwritten")
        note["finger"] = finger
        note["source"] = "musical_review"
        note["review_decision"] = str(row.get("reason", "targeted phrase review"))
        applied += 1
    plan.setdefault("fingering_review", {})["latest"] = {
        "manifest": str(args.manifest), "applied": applied, "unresolved_note_ids": unresolved,
    }
    save_plan(args.output, plan)
    print(f"Applied {applied} reviewed fingering decision(s); unresolved {len(unresolved)}: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
