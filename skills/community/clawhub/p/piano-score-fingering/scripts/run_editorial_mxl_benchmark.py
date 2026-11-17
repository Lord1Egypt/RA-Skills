#!/usr/bin/env python3
"""Run an explicit, local MXL/MusicXML editorial-fingering diagnostic suite.

The caller supplies the score files.  This script never downloads, copies into
the Skill, or modifies them.  Each source's existing fingerings become a
read-only comparison set; generation itself runs with ``--ignore-existing``.
It always writes a summary and per-piece artifacts, including for failed
pieces, so a low score cannot disappear from the denominator.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def score_argument(value: str) -> tuple[str, Path]:
    identifier, separator, raw_path = value.partition("=")
    path = Path(raw_path).expanduser()
    if not separator or not identifier or not raw_path:
        raise argparse.ArgumentTypeError("--score must use ID=/absolute/or/relative/path.mxl")
    if not path.is_file():
        raise argparse.ArgumentTypeError(f"score not found: {path}")
    if path.suffix.lower() not in {".mxl", ".xml", ".musicxml"}:
        raise argparse.ArgumentTypeError("score must be MXL or MusicXML")
    return identifier, path.resolve()


def part_argument(value: str) -> tuple[str, str]:
    identifier, separator, part_id = value.partition("=")
    if not separator or not identifier or not part_id:
        raise argparse.ArgumentTypeError("--part-id must use the matching SCORE_ID=MUSICXML_PART_ID form")
    return identifier, part_id


def execute(command: list[str], timeout: int) -> dict:
    started = time.monotonic()
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
        return {
            "status": "passed" if result.returncode == 0 else "failed",
            "return_code": result.returncode,
            "stdout": result.stdout[-4000:], "stderr": result.stderr[-4000:],
            "elapsed_seconds": round(time.monotonic() - started, 3),
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "status": "timed_out", "return_code": None,
            "stdout": (exc.stdout or "")[-4000:] if isinstance(exc.stdout, str) else "",
            "stderr": (exc.stderr or "")[-4000:] if isinstance(exc.stderr, str) else "",
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "timeout_seconds": timeout,
        }


def read_report(path: Path) -> dict | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return payload if isinstance(payload, dict) else None
    except (OSError, ValueError, json.JSONDecodeError):
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--score", action="append", type=score_argument, required=True,
        metavar="ID=PATH", help="repeat for every editor-fingered MXL/MusicXML score",
    )
    parser.add_argument(
        "--part-id", action="append", type=part_argument, default=[], metavar="SCORE_ID=PART_ID",
        help="optionally select an explicitly verified keyboard part for one --score input",
    )
    parser.add_argument(
        "--rh-part-id", action="append", type=part_argument, default=[], metavar="SCORE_ID=PART_ID",
        help="right-hand part for an explicitly verified split-staff piano score; requires matching --lh-part-id",
    )
    parser.add_argument(
        "--lh-part-id", action="append", type=part_argument, default=[], metavar="SCORE_ID=PART_ID",
        help="left-hand part for an explicitly verified split-staff piano score; requires matching --rh-part-id",
    )
    parser.add_argument("--out-dir", type=Path, required=True, help="a new result directory")
    parser.add_argument("--hand-size", default="M", choices=("XXS", "XS", "S", "M", "L", "XL", "XXL"))
    parser.add_argument(
        "--max-auto-depth", type=int, default=4, choices=range(4, 8), metavar="4-7",
        help="maximum dynamic-search look-ahead used for every generated comparison (default: 4)",
    )
    parser.add_argument("--timeout", type=int, default=180, help="per deterministic stage limit in seconds")
    args = parser.parse_args()
    if args.timeout < 10:
        parser.error("--timeout must be at least 10 seconds")
    if args.out_dir.exists():
        parser.error("--out-dir must be a new directory")
    identifiers = [identifier for identifier, _ in args.score]
    if len(set(identifiers)) != len(identifiers):
        parser.error("each --score ID must be unique")
    selected_parts = dict(args.part_id)
    if len(selected_parts) != len(args.part_id):
        parser.error("each --part-id SCORE_ID may appear at most once")
    unknown = sorted(set(selected_parts) - set(identifiers))
    if unknown:
        parser.error("--part-id references an unknown --score ID: " + ", ".join(unknown))
    rh_parts, lh_parts = dict(args.rh_part_id), dict(args.lh_part_id)
    if len(rh_parts) != len(args.rh_part_id) or len(lh_parts) != len(args.lh_part_id):
        parser.error("each split-hand part selector may appear at most once per score")
    if set(rh_parts) != set(lh_parts):
        parser.error("every --rh-part-id needs a matching --lh-part-id for the same score")
    if set(selected_parts) & set(rh_parts):
        parser.error("a score may use --part-id or a split RH/LH pair, not both")
    unknown = sorted((set(rh_parts) | set(lh_parts)) - set(identifiers))
    if unknown:
        parser.error("split-hand selector references an unknown --score ID: " + ", ".join(unknown))

    args.out_dir.mkdir(parents=True)
    summary_rows: list[dict] = []
    total_matches = total_anchors = 0
    for identifier, source in args.score:
        directory = args.out_dir / identifier
        directory.mkdir()
        reference = directory / "reference-plan.json"
        generated = directory / "generated-plan.json"
        agreement = directory / "editorial-agreement.json"
        extract = [sys.executable, str(SCRIPT_DIR / "create_plan_from_musicxml.py"), str(source), "-o", str(reference)]
        if identifier in selected_parts:
            extract.extend(["--part-id", selected_parts[identifier]])
        elif identifier in rh_parts:
            extract.extend(["--rh-part-id", rh_parts[identifier], "--lh-part-id", lh_parts[identifier]])
        commands = {
            "extract_reference": extract,
            "generate_without_source_fingers": [sys.executable, str(SCRIPT_DIR / "generate_fingering_plan.py"), str(reference), "-o", str(generated), "--ignore-existing", "--hand-size", args.hand_size, "--max-auto-depth", str(args.max_auto_depth), "--quiet"],
            "compare_editorial_anchors": [sys.executable, str(SCRIPT_DIR / "compare_reference_fingerings.py"), str(reference), str(generated), "--minimum", "0", "-o", str(agreement)],
        }
        logs: dict[str, dict] = {}
        for stage, command in commands.items():
            if stage == "generate_without_source_fingers" and not reference.is_file():
                logs[stage] = {"status": "skipped", "reason": "reference plan unavailable"}
            elif stage == "compare_editorial_anchors" and not (reference.is_file() and generated.is_file()):
                logs[stage] = {"status": "skipped", "reason": "reference or generated plan unavailable"}
            else:
                logs[stage] = execute(command, args.timeout)
        report = read_report(agreement)
        matches = int(report.get("matches", 0)) if report else 0
        anchors = int(report.get("anchors", 0)) if report else 0
        if report:
            total_matches += matches
            total_anchors += anchors
        row = {
            "id": identifier,
            "source": str(source), "source_sha256": digest(source),
            "source_bytes": source.stat().st_size,
            "selected_part_id": selected_parts.get(identifier),
            "selected_split_parts": ({"rh": rh_parts[identifier], "lh": lh_parts[identifier]} if identifier in rh_parts else None),
            "reference_anchors": anchors, "matches": matches,
            "accuracy": matches / anchors if anchors else None,
            "per_hand": report.get("per_hand", {}) if report else {},
            "stages": {stage: value.get("status") for stage, value in logs.items()},
            "artifact_dir": str(directory),
        }
        (directory / "run-receipt.json").write_text(
            json.dumps({"piece": row, "commands": commands, "logs": logs}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        summary_rows.append(row)

    summary = {
        "metric": "exact agreement with each supplied score's explicit editor fingering anchors",
        "scope": "diagnostic evidence only; a different playable editorial choice is not automatically a musical error",
        "hand_size": args.hand_size,
        "max_auto_depth": args.max_auto_depth,
        "pieces": summary_rows,
        "total_matches": total_matches, "total_anchors": total_anchors,
        "overall_accuracy": total_matches / total_anchors if total_anchors else None,
        "failed_or_missing_pieces": [
            row["id"] for row in summary_rows
            if row["accuracy"] is None or any(status != "passed" for status in row["stages"].values())
        ],
    }
    (args.out_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if total_anchors and not summary["failed_or_missing_pieces"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
