import argparse
import json
import subprocess
from datetime import datetime
from pathlib import Path


def run_git(repo: Path, args: list[str]) -> str:
    p = subprocess.run(
        ["git", *args],
        cwd=str(repo),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if p.returncode != 0:
        raise SystemExit(p.stderr.strip() or f"git {' '.join(args)} failed")
    return p.stdout


def detect_platform(repo: Path) -> str:
    ios_markers = ["*.xcodeproj", "*.xcworkspace", "Podfile", "Package.swift"]
    android_markers = ["build.gradle", "build.gradle.kts", "settings.gradle", "settings.gradle.kts", "AndroidManifest.xml", "gradlew", "gradlew.bat"]
    for pat in ios_markers:
        if list(repo.glob(pat)):
            return "ios"
    for name in android_markers:
        if list(repo.rglob(name)):
            return "android"
    return "general"


def parse_numstat(numstat_text: str) -> tuple[int, int, int]:
    added = 0
    removed = 0
    files = set()
    for line in numstat_text.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        a, r, path = parts[0], parts[1], parts[2]
        if a.isdigit():
            added += int(a)
        if r.isdigit():
            removed += int(r)
        files.add(path)
    return len(files), added, removed


def commit_files_changed(repo: Path, sha: str) -> int:
    out = run_git(repo, ["show", "--name-only", "--pretty=format:", sha])
    return len([x for x in out.splitlines() if x.strip()])


def list_commits(repo: Path, rng: str) -> list[dict]:
    out = run_git(repo, ["log", "--pretty=format:%H%x09%an%x09%ad%x09%s", "--date=short", rng])
    commits = []
    for line in out.splitlines():
        parts = line.split("\t", 3)
        if len(parts) != 4:
            continue
        sha, author, date, subject = parts
        commits.append(
            {
                "sha": sha,
                "subject": subject,
                "author": author,
                "date": date,
                "files_changed": commit_files_changed(repo, sha),
                "findings": [],
                "passed": [],
            }
        )
    commits.reverse()
    return commits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--range", dest="rng", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    out_path = Path(args.out).resolve()
    platform = detect_platform(repo)

    rng = args.rng.strip()
    mode = "range" if (".." in rng) else "single"

    if mode == "single":
        numstat = run_git(repo, ["show", "--numstat", "--pretty=format:", rng])
    else:
        numstat = run_git(repo, ["diff", "--numstat", rng])

    files_changed, added, removed = parse_numstat(numstat)

    if mode == "single":
        commits = list_commits(repo, rng)
        if not commits:
            commits = [
                {
                    "sha": rng,
                    "subject": "",
                    "author": "",
                    "date": "",
                    "files_changed": commit_files_changed(repo, rng),
                    "findings": [],
                    "passed": [],
                }
            ]
    else:
        commits = list_commits(repo, rng)

    data = {
        "repo": str(repo),
        "platform": platform,
        "mode": mode,
        "range": rng,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "stats": {"files_changed": files_changed, "added": added, "removed": removed},
        "summary": "Auto-generated review JSON template. Fill `findings` per commit if you want HTML to show issues.",
        "commits": commits,
        "overall": {
            "patterns": [],
            "blockers": [],
            "next_steps": [],
            "matrix": [],
            "verdict": "",
        },
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(str(out_path))


if __name__ == "__main__":
    main()
