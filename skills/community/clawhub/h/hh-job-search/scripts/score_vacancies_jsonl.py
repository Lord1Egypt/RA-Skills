#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from profile_to_json import to_profile


def main():
    if len(sys.argv) != 4:
        print("Usage: score_vacancies_jsonl.py <project-dir> <in.jsonl> <out.jsonl>", file=sys.stderr)
        sys.exit(2)

    project_dir, in_path, out_path = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
    profile = to_profile(project_dir)
    score_script = Path(__file__).with_name("job_match_score.py")

    with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as pf:
        json.dump(profile, pf, ensure_ascii=False, indent=2)
        profile_path = pf.name

    out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with in_path.open(encoding="utf-8") as src, out_path.open("w", encoding="utf-8") as dst:
            for line in src:
                line = line.strip()
                if not line:
                    continue
                vacancy = json.loads(line)
                with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as vf:
                    json.dump(vacancy, vf, ensure_ascii=False, indent=2)
                    vacancy_path = vf.name
                proc = subprocess.run([sys.executable, str(score_script), profile_path, vacancy_path], capture_output=True, text=True, check=True)
                score = json.loads(proc.stdout)
                vacancy.update(score)
                dst.write(json.dumps(vacancy, ensure_ascii=False) + "\n")
                Path(vacancy_path).unlink(missing_ok=True)
    finally:
        Path(profile_path).unlink(missing_ok=True)

    print(f"Scored vacancies -> {out_path}")


if __name__ == "__main__":
    main()
