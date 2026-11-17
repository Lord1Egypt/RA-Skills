#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from _common import load_manifest, save_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Add a minimal agent context capsule to a run.")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--lane-id", required=True)
    parser.add_argument("--role", choices=["explorer", "worker", "qa"], required=True)
    parser.add_argument("--model-tier", choices=["fast", "balanced", "frontier"], default="balanced")
    parser.add_argument("--objective", required=True)
    parser.add_argument("--input", action="append", default=[])
    parser.add_argument("--ownership", action="append", default=[])
    parser.add_argument("--deliverable", required=True)
    parser.add_argument("--acceptance", action="append", default=[])
    parser.add_argument("--exclusion", action="append", default=[])
    parser.add_argument("--deadline-minutes", type=int, default=30)
    args = parser.parse_args()

    manifest_path, manifest = load_manifest(args.manifest)
    if any(lane["lane_id"] == args.lane_id for lane in manifest["lanes"]):
        parser.error(f"lane already exists: {args.lane_id}")
    if len(manifest["lanes"]) >= manifest["limits"]["total_agents"]:
        parser.error("run has reached the total agent lane limit")
    qa_count = sum(lane["role"] == "qa" for lane in manifest["lanes"])
    wave1_count = len(manifest["lanes"]) - qa_count
    if args.role == "qa":
        if qa_count >= manifest["limits"]["qa_agents"]:
            parser.error("run has reached the QA agent limit")
        if not manifest["build"]["id"]:
            parser.error("QA capsules require a registered build")
    elif wave1_count >= manifest["limits"]["wave1_agents"]:
        parser.error("run has reached the first-wave agent limit")

    artifact_hashes = manifest["build"].get("artifacts", []) if args.role == "qa" else []
    capsule = {
        "run_id": manifest["run_id"],
        "lane_id": args.lane_id,
        "role": args.role,
        "model_tier": args.model_tier,
        "objective": args.objective,
        "inputs": [str(Path(value).expanduser().resolve()) for value in args.input],
        "ownership": args.ownership,
        "deliverable": args.deliverable,
        "acceptance": args.acceptance,
        "exclusions": args.exclusion,
        "build_id": manifest["build"]["id"],
        "artifact_hashes": artifact_hashes,
        "deadline_at": (datetime.now(timezone.utc) + timedelta(minutes=args.deadline_minutes)).isoformat(),
    }
    encoded = json.dumps(capsule, ensure_ascii=False, indent=2).encode("utf-8")
    if len(encoded) > manifest["limits"]["capsule_bytes"]:
        parser.error(f"capsule is {len(encoded)} bytes; limit is {manifest['limits']['capsule_bytes']}")

    capsule_path = manifest_path.parent / "capsules" / f"{args.lane_id}.json"
    save_json(capsule_path, capsule)
    manifest["lanes"].append({
        "lane_id": args.lane_id,
        "role": args.role,
        "capsule_path": str(capsule_path),
        "status": "planned",
    })
    manifest["status"] = "qa" if args.role == "qa" else "running"
    save_json(manifest_path, manifest)
    print(capsule_path)


if __name__ == "__main__":
    main()
