from __future__ import annotations

import argparse
import json

import system_config as sc
from utils import json_fail, now_str


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def apply_operation(operation: dict) -> None:
    filename = operation["file"]
    key = operation["key"]
    record = operation["record"]
    mode = operation.get("mode", "replace")

    def mutate(current: dict) -> dict:
        if mode == "insert_if_absent" and key in current:
            return current
        current[key] = record
        return current

    sc.update_json(filename, mutate, default={})


def repair_one(error_id: str, item: dict) -> dict:
    if item.get("status") == "repaired":
        return {"error_id": error_id, "status": "already_repaired"}
    for operation in item.get("operations", []):
        apply_operation(operation)
    item["status"] = "repaired"
    item["repaired_at"] = now_str()
    return {"error_id": error_id, "status": "repaired"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--error_id", default="")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()

    errors = sc.read_json("provisioning_errors.json", {})
    if args.error_id:
        selected = {args.error_id: errors.get(args.error_id)}
        if not selected[args.error_id]:
            out(json_fail("recovery_not_found", "找不到该恢复记录。"))
            return
    elif args.all:
        selected = {k: v for k, v in errors.items() if v.get("status") == "pending"}
    else:
        out({"success": True, "pending": {k: v for k, v in errors.items() if v.get("status") == "pending"}})
        return

    results = []
    try:
        for error_id, item in selected.items():
            results.append(repair_one(error_id, item))

        def mutate(current: dict) -> dict:
            for error_id, item in selected.items():
                current[error_id] = item
            return current

        sc.update_json("provisioning_errors.json", mutate, default={})
    except Exception as exc:
        out(json_fail("repair_failed", str(exc)))
        return
    out({"success": True, "results": results})


if __name__ == "__main__":
    main()
