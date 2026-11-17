#!/usr/bin/env python3
"""Write a viewable recovery package instead of ending a failed score run with an error."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


def copy_artifact(source: Path, destination_dir: Path, prefix: str) -> str:
    if not source.is_file():
        raise ValueError(f"artifact not found: {source}")
    destination_dir.mkdir(parents=True, exist_ok=True)
    target = destination_dir / f"{prefix}-{source.name}"
    if target.exists():
        raise ValueError(f"refusing to overwrite recovery artifact: {target}")
    shutil.copyfile(source, target)
    return str(target.relative_to(destination_dir.parent))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--reason", required=True, help="specific failed check or unresolved score fact")
    parser.add_argument("--scope", default="unknown", help="affected page/measure/hand scope")
    parser.add_argument("--source-image", type=Path, action="append", default=[])
    parser.add_argument("--crop", type=Path, action="append", default=[])
    parser.add_argument("--current-output", type=Path, action="append", default=[])
    parser.add_argument("--plan", type=Path, help="current plan; copies it and its bound rendered pages into the recovery bundle")
    parser.add_argument("--question", action="append", default=[])
    args = parser.parse_args()

    out_dir = args.out_dir
    if out_dir.exists():
        raise ValueError(f"recovery output directory already exists: {out_dir}")
    source_images = list(args.source_image)
    current_outputs = list(args.current_output)
    if args.plan:
        if not args.plan.is_file():
            raise ValueError(f"plan not found: {args.plan}")
        current_outputs.append(args.plan)
        try:
            plan = json.loads(args.plan.read_text(encoding="utf-8"))
            assets = plan.get("recognition", {}).get("source_assets", [])
            for asset in assets:
                if isinstance(asset, dict) and asset.get("role") == "rendered_page":
                    path = Path(str(asset.get("path", "")))
                    if path.is_file():
                        source_images.append(path)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid plan JSON: {args.plan}") from exc
    # A plan can reference a source page more than once through a review crop.
    # Copy it once so recovery never fails merely due to duplicate arguments.
    source_images = list(dict.fromkeys(source_images))
    current_outputs = list(dict.fromkeys(current_outputs))
    source_items = [copy_artifact(path, out_dir / "source", "source") for path in source_images]
    crop_items = [copy_artifact(path, out_dir / "crops", "crop") for path in args.crop]
    output_items = [copy_artifact(path, out_dir / "current-output", "current") for path in current_outputs]
    questions = list(args.question)
    if not questions:
        questions = ["Please confirm pitches, durations, rests, or ties in the listed source scopes."]
    manifest = {
        "status": "needs_user_confirmation",
        "reason": args.reason,
        "scope": args.scope,
        "source_images": source_items,
        "crops": crop_items,
        "current_outputs": output_items,
        "questions": questions,
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "recovery-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Piano Fingering Review Bundle", "", f"- Issue scope: {args.scope}", f"- Current issue: {args.reason}",
        "", "## Please confirm", "", *[f"- {question}" for question in questions], "",
        "## Attached files", "",
        *[f"- Source page: `{item}`" for item in source_items],
        *[f"- Issue crop: `{item}`" for item in crop_items],
        *[f"- Current result: `{item}`" for item in output_items],
        "", "After confirmation, repair the listed scopes and resume recognition, fingering, and layout checks. Preserve already accepted measures.", "",
    ]
    (out_dir / "recovery-report.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Created recovery package: {out_dir}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as exc:
        raise SystemExit(f"ERROR: {exc}")
