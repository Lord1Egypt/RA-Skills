#!/usr/bin/env python3
"""Re-run frozen local editorial anchors without repeating OMR or data collection.

The suite file is deliberately maintained outside the distributable Skill.
Each fixture is a previously reviewed OMR candidate plan, and each anchor file
is a manually read partial editorial reference. This measures only changes in
the fingering solver; it neither claims visual-recognition accuracy nor copies
or uploads source scores.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from time import monotonic


SCRIPT_DIR = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def load_object(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return data


def resolve(base: Path, raw: object) -> Path:
    if not isinstance(raw, str) or not raw:
        raise ValueError("suite path is missing")
    path = Path(raw)
    return path if path.is_absolute() else base / path


def run(command: list[str], timeout: int) -> dict:
    started = monotonic()
    try:
        completed = subprocess.run(command, text=True, capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        return {
            "status": "timed_out", "elapsed_seconds": round(monotonic() - started, 3),
            "stdout": (exc.stdout or "")[-2000:] if isinstance(exc.stdout, str) else "",
            "stderr": (exc.stderr or "")[-2000:] if isinstance(exc.stderr, str) else "",
        }
    return {
        "status": "passed" if completed.returncode == 0 else "failed",
        "return_code": completed.returncode,
        "elapsed_seconds": round(monotonic() - started, 3),
        "stdout": completed.stdout[-2000:], "stderr": completed.stderr[-2000:],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("suite", type=Path, help="private-anchor-suite-v1 JSON outside the Skill")
    parser.add_argument("--out-dir", type=Path, required=True, help="new directory for generated plans and reports")
    parser.add_argument("--minimum", type=float, default=0.80, help="diagnostic exact-match target (default: 0.80)")
    parser.add_argument("--minimum-holdout-pieces", type=int, default=0)
    parser.add_argument("--minimum-holdout-anchors", type=int, default=0)
    parser.add_argument("--hand-size", default="M", choices=("XXS", "XS", "S", "M", "L", "XL", "XXL"))
    parser.add_argument("--max-auto-depth", type=int, default=4, choices=range(4, 8), metavar="4-7")
    parser.add_argument("--timeout", type=int, default=180, help="per-piece solver timeout in seconds")
    args = parser.parse_args()
    if (
        not 0 < args.minimum <= 1 or args.timeout < 10
        or args.minimum_holdout_pieces < 0 or args.minimum_holdout_anchors < 0
    ):
        parser.error("--minimum must be in (0, 1] and --timeout must be at least 10")
    if args.out_dir.exists():
        parser.error("--out-dir must be a new directory")

    suite_path = args.suite.resolve()
    suite = load_object(suite_path)
    if suite.get("schema_version") != "private-anchor-suite-v1":
        raise ValueError("suite.schema_version must be private-anchor-suite-v1")
    pieces = suite.get("pieces")
    if not isinstance(pieces, list) or not pieces:
        raise ValueError("suite.pieces must be a non-empty list")

    args.out_dir.mkdir(parents=True)
    base = suite_path.parent
    rows: list[dict] = []
    total_anchors = total_matches = total_noteheads = 0
    roles = {
        "development": {"pieces": 0, "anchors": 0, "matches": 0},
        "holdout": {"pieces": 0, "anchors": 0, "matches": 0},
    }
    complete = True
    for raw_piece in pieces:
        if not isinstance(raw_piece, dict):
            raise ValueError("every suite piece must be an object")
        identifier = str(raw_piece.get("id", ""))
        if not identifier:
            raise ValueError("suite piece id is missing")
        fixture, anchors = resolve(base, raw_piece.get("fixture")), resolve(base, raw_piece.get("anchors"))
        expected = int(raw_piece.get("expected_anchors", 0))
        role = str(raw_piece.get("benchmark_role", "development")).lower()
        if role not in roles:
            raise ValueError(f"{identifier}: benchmark_role must be development or holdout")
        if not fixture.is_file() or not anchors.is_file():
            raise ValueError(f"{identifier}: fixture or anchor file is missing")
        anchor_data = load_object(anchors)
        actual_anchor_count = len(anchor_data.get("anchors", [])) if isinstance(anchor_data.get("anchors"), list) else 0
        if expected < 1 or actual_anchor_count != expected:
            raise ValueError(f"{identifier}: expected {expected} anchors, found {actual_anchor_count}")

        generated = args.out_dir / f"{identifier}-generated-plan.json"
        comparison = args.out_dir / f"{identifier}-comparison.json"
        generate = run([
            sys.executable, str(SCRIPT_DIR / "generate_fingering_plan.py"), str(fixture),
            "-o", str(generated), "--provisional-omr", "--ignore-existing", "--quiet",
            "--hand-size", args.hand_size, "--max-auto-depth", str(args.max_auto_depth),
        ], args.timeout)
        compare = {"status": "skipped", "reason": "generation unavailable"}
        report: dict | None = None
        if generate["status"] == "passed":
            compare = run([
                sys.executable, str(SCRIPT_DIR / "compare_editorial_pdf_anchors.py"), str(generated), str(anchors),
                "-o", str(comparison),
            ], args.timeout)
            if compare["status"] == "passed":
                report = load_object(comparison)
        if report is None:
            complete = False
            row = {
                "id": identifier, "status": "unavailable", "anchors": expected,
                "fixture_sha256": digest(fixture), "anchors_sha256": digest(anchors),
                "generate": generate, "compare": compare,
            }
        else:
            anchors_count = int(report["anchors"])
            matched = int(report["matched_noteheads"])
            matches = int(report["finger_matches"])
            total_anchors += anchors_count
            total_noteheads += matched
            total_matches += matches
            roles[role]["pieces"] += 1
            roles[role]["anchors"] += anchors_count
            roles[role]["matches"] += matches
            row = {
                "id": identifier, "benchmark_role": role, "status": "measured", "anchors": anchors_count,
                "matched_noteheads": matched, "finger_matches": matches,
                "notehead_match_accuracy": round(matched / anchors_count, 6),
                "fingering_accuracy": round(matches / anchors_count, 6),
                "fixture_sha256": digest(fixture), "anchors_sha256": digest(anchors),
                "generated_plan": generated.name, "comparison": comparison.name,
                "generate_seconds": generate["elapsed_seconds"], "compare_seconds": compare["elapsed_seconds"],
            }
        rows.append(row)

    accuracy = total_matches / total_anchors if total_anchors else None
    holdout = roles["holdout"]
    holdout_accuracy = holdout["matches"] / holdout["anchors"] if holdout["anchors"] else None
    holdout_required = args.minimum_holdout_pieces > 0 or args.minimum_holdout_anchors > 0
    holdout_passed = (
        not holdout_required or (
            holdout["pieces"] >= args.minimum_holdout_pieces
            and holdout["anchors"] >= args.minimum_holdout_anchors
            and holdout_accuracy is not None and holdout_accuracy >= args.minimum
        )
    )
    result = {
        "metric": "exact agreement with frozen partial editorial PDF anchors",
        "scope": "fingering-solver regression only; candidate OMR semantics and visual placement are not scored",
        "suite": str(suite_path), "hand_size": args.hand_size, "max_auto_depth": args.max_auto_depth,
        "minimum": args.minimum, "pieces": rows,
        "by_role": {
            role: values | {"fingering_accuracy": values["matches"] / values["anchors"] if values["anchors"] else None}
            for role, values in roles.items()
        },
        "holdout": {"required": holdout_required, "passed": holdout_passed},
        "overall": {
            "anchors": total_anchors, "matched_noteheads": total_noteheads, "finger_matches": total_matches,
            "notehead_match_accuracy": total_noteheads / total_anchors if total_anchors else None,
            "fingering_accuracy": accuracy, "all_pieces_measured": complete,
            "passed": bool(complete and accuracy is not None and accuracy >= args.minimum and holdout_passed),
        },
    }
    (args.out_dir / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["overall"]["passed"] else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        raise SystemExit(1)
