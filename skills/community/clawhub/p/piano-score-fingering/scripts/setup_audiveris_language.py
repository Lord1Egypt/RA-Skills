#!/usr/bin/env python3
"""Probe or explicitly install one official Audiveris OCR language file.

Audiveris installers intentionally ship without tessdata.  This helper never
downloads on its own: callers must pass ``--install <language-code>`` after a
user has approved the one-time network download.  It writes only the
Audiveris user config folder, never a score or the Skill package.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path


LANGUAGE_URL = "https://github.com/tesseract-ocr/tessdata/raw/main/{code}.traineddata"


def config_dir() -> Path:
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "AudiverisLtd" / "audiveris"
    if os.name == "nt":
        root = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
        return root / "AudiverisLtd" / "audiveris"
    root = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return root / "AudiverisLtd" / "audiveris"


def payload(folder: Path, *, status: str, detail: str | None = None) -> dict:
    installed = sorted(item.stem for item in folder.glob("*.traineddata")) if folder.is_dir() else []
    result = {
        "status": status,
        "tessdata_dir": str(folder),
        "installed_languages": installed,
        "network_downloaded": status == "installed",
        "next_action": (
            "Audiveris OCR language files are ready for a separately approved local OMR attempt."
            if installed else
            "Ask the user whether to install the official English language file (eng) before retrying local OMR."
        ),
    }
    if detail:
        result["detail"] = detail
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--probe", action="store_true", help="report the Audiveris tessdata folder without downloading")
    parser.add_argument("--install", metavar="LANG", help="explicitly download one official Tesseract language file")
    parser.add_argument("--timeout", type=int, default=90)
    args = parser.parse_args()
    if args.probe == bool(args.install):
        parser.error("choose exactly one of --probe or --install LANG")
    if args.timeout < 10:
        parser.error("--timeout must be at least 10 seconds")
    folder = config_dir() / "tessdata"
    if args.probe:
        print(json.dumps(payload(folder, status="ready" if folder.glob("*.traineddata") else "missing"), ensure_ascii=False, indent=2))
        return 0
    code = str(args.install).lower()
    if not re.fullmatch(r"[a-z0-9_]{3,20}", code):
        parser.error("LANG must be a Tesseract language code, for example eng or chi_sim")
    target = folder / f"{code}.traineddata"
    if target.is_file() and target.stat().st_size > 0:
        print(json.dumps(payload(folder, status="already_installed"), ensure_ascii=False, indent=2))
        return 0
    folder.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(".traineddata.download")
    request = urllib.request.Request(LANGUAGE_URL.format(code=code), headers={"User-Agent": "piano-score-fingering"})
    try:
        with urllib.request.urlopen(request, timeout=args.timeout) as response, temporary.open("wb") as output:
            while chunk := response.read(1024 * 1024):
                output.write(chunk)
    except (OSError, urllib.error.URLError, urllib.error.HTTPError) as exc:
        temporary.unlink(missing_ok=True)
        print(json.dumps(payload(folder, status="failed", detail=str(exc)), ensure_ascii=False, indent=2))
        return 2
    if not temporary.is_file() or temporary.stat().st_size < 1024:
        temporary.unlink(missing_ok=True)
        print(json.dumps(payload(folder, status="failed", detail="downloaded language file is unexpectedly small"), ensure_ascii=False, indent=2))
        return 2
    temporary.replace(target)
    print(json.dumps(payload(folder, status="installed"), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
