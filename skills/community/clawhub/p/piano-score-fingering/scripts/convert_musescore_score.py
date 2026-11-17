#!/usr/bin/env python3
"""Convert a local MuseScore score to a new MusicXML file with a bounded CLI call.

MuseScore (.mscz/.mscx) is not MusicXML.  This helper deliberately relies only
on a separately installed, local MuseScore command and never downloads or
uploads a score.  Its output can then enter the ordinary structured-score
fingering path.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

from safe_xml import load_musicxml


COMMAND_NAMES = ("mscore", "musescore", "MuseScore")
MACOS_APP_COMMANDS = (
    Path("/Applications/MuseScore 4.app/Contents/MacOS/mscore"),
    Path("/Applications/MuseScore 3.app/Contents/MacOS/mscore"),
)


def discover_renderer(explicit: str | None = None) -> str | None:
    if explicit:
        candidate = Path(explicit).expanduser()
        if candidate.is_file():
            return str(candidate.resolve())
        resolved = shutil.which(explicit)
        return resolved
    for name in COMMAND_NAMES:
        resolved = shutil.which(name)
        if resolved:
            return resolved
    for candidate in MACOS_APP_COMMANDS:
        if candidate.is_file():
            return str(candidate)
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, nargs="?")
    parser.add_argument("-o", "--output", type=Path)
    parser.add_argument("--renderer", help="optional path/name of a locally installed MuseScore CLI")
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--report", type=Path, help="optional local JSON receipt")
    parser.add_argument("--probe", action="store_true", help="only report whether a local MuseScore CLI is available")
    args = parser.parse_args()
    if args.timeout < 10 or args.timeout > 600:
        parser.error("--timeout must be between 10 and 600 seconds")
    renderer = discover_renderer(args.renderer)
    if args.probe:
        payload = {"available": bool(renderer), "renderer": renderer, "remote_upload": False}
        print(json.dumps(payload, ensure_ascii=False))
        return 0 if renderer else 2
    if args.input is None or args.output is None:
        parser.error("input and --output are required unless --probe is used")
    if args.input.suffix.lower() not in {".mscz", ".mscx"}:
        parser.error("input must be a .mscz or .mscx MuseScore score")
    if not args.input.is_file():
        parser.error(f"input not found: {args.input}")
    if args.output.suffix.lower() not in {".musicxml", ".xml"}:
        parser.error("output must be a .musicxml or .xml file")
    if args.output.resolve() == args.input.resolve():
        parser.error("output must not overwrite the input MuseScore score")
    receipt: dict[str, object] = {
        "input": str(args.input.resolve()),
        "output": str(args.output.resolve()),
        "renderer": renderer,
        "remote_upload": False,
        "timeout_seconds": args.timeout,
    }
    if not renderer:
        receipt.update({"status": "renderer_unavailable", "next_action": "Install MuseScore locally or provide MusicXML/MXL."})
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("ERROR: no local MuseScore CLI found; install MuseScore locally or provide MusicXML/MXL", file=sys.stderr)
        return 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    command = [renderer, "-o", str(args.output), str(args.input)]
    started = time.monotonic()
    try:
        completed = subprocess.run(command, capture_output=True, text=True, timeout=args.timeout)
        receipt.update({"return_code": completed.returncode, "stdout": completed.stdout[-12000:], "stderr": completed.stderr[-12000:]})
    except subprocess.TimeoutExpired as exc:
        receipt.update({"status": "timed_out", "stdout": (exc.stdout or "")[-12000:] if isinstance(exc.stdout, str) else "", "stderr": (exc.stderr or "")[-12000:] if isinstance(exc.stderr, str) else ""})
    receipt["elapsed_seconds"] = round(time.monotonic() - started, 3)
    try:
        if receipt.get("status") != "timed_out" and receipt.get("return_code") == 0 and args.output.is_file():
            load_musicxml(args.output, allow_mxl=False)
            receipt["status"] = "converted"
        elif receipt.get("status") != "timed_out":
            receipt["status"] = "conversion_failed"
    except (OSError, ValueError) as exc:
        receipt["status"] = "invalid_musicxml_output"
        receipt["validation_error"] = str(exc)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False))
    return 0 if receipt.get("status") == "converted" else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
