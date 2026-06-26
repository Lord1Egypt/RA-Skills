#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from profile_to_json import to_profile


def main():
    if len(sys.argv) != 3:
        print("Usage: score_vacancy_from_project.py <project-dir> <vacancy.json>", file=sys.stderr)
        sys.exit(2)

    project_dir, vacancy_json = sys.argv[1], sys.argv[2]
    profile = to_profile(project_dir)

    with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as tmp:
        json.dump(profile, tmp, ensure_ascii=False, indent=2)
        tmp_path = tmp.name

    try:
        script = Path(__file__).with_name("job_match_score.py")
        subprocess.run([sys.executable, str(script), tmp_path, vacancy_json], check=True)
    finally:
        Path(tmp_path).unlink(missing_ok=True)


if __name__ == "__main__":
    main()
