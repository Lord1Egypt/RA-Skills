#!/usr/bin/env python3
"""All-projects health check for project-scaffold."""

from __future__ import annotations
import json as _json
import subprocess
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[3] / "projects"


def check_project(project_dir: Path) -> dict:
    key = project_dir.name
    findings = {
        "key": key,
        "has_project_md": (project_dir / "PROJECT.md").exists(),
        "has_runtime_env": (project_dir / "config" / "runtime.env").exists(),
        "has_run_script": bool(list((project_dir / "scripts").glob("run_*.sh"))),
        "has_sources_json": (project_dir / "sources.json").exists(),
        "has_summary_json": (project_dir / "logs" / "latest_run_summary.json").exists(),
        "fail_count": 0,
        "warn_count": 0,
        "errors": [],
        "warnings": [],
    }

    # runtime.env content check
    if findings["has_runtime_env"]:
        env = {}
        for ln in (project_dir / "config" / "runtime.env").read_text().splitlines():
            ln = ln.strip()
            if "=" in ln and not ln.startswith("#"):
                k, v = ln.split("=", 1)
                env[k.strip()] = v.strip()
        missing = [
            v for v in ["PROJECT_KEY", "CHAT_ID", "BOT_TOKEN"]
            if v not in env or env[v] in ("", "TODO", "YOUR_" + v)
        ]
        if missing:
            findings["fail_count"] += len(missing)
            findings["errors"].append(f"runtime.env missing/placeholder: {missing}")

    # sources.json check
    if findings["has_sources_json"]:
        try:
            data = _json.loads((project_dir / "sources.json").read_text())
            if not data.get("sources"):
                findings["warn_count"] += 1
                findings["warnings"].append("sources.json is empty")
        except Exception as e:
            findings["fail_count"] += 1
            findings["errors"].append(f"sources.json malformed: {e}")
    else:
        findings["warn_count"] += 1
        findings["warnings"].append("sources.json missing")

    # Python syntax check (fast)
    py_scripts = sorted((project_dir / "scripts").glob("*.py"))
    if py_scripts:
        result = subprocess.run(
            [sys.executable, "-m", "py_compile"] + [str(p) for p in py_scripts],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            findings["fail_count"] += 1
            findings["errors"].append(f"py_compile error: {result.stderr.strip().splitlines()[0]}")

    return findings


def run_all_projects() -> None:
    projects_root = WORKSPACE
    print(f"\n\U0001f4ca Scanning all projects under: {projects_root}\n")

    rows = []
    for project_dir in sorted(projects_root.iterdir()):
        if not project_dir.is_dir():
            continue
        if project_dir.name.startswith(".") or project_dir.name == "shared":
            continue
        f = check_project(project_dir)
        status = (
            "OK" if f["fail_count"] == 0 and f["warn_count"] == 0
            else "WARNINGS" if f["fail_count"] == 0
            else "FAIL"
        )
        detail = f["errors"][0] if f["errors"] else (f["warnings"][0] if f["warnings"] else "")
        rows.append({**f, "status": status, "detail": detail[:70]})

    if not rows:
        print("  No projects found.")
        return

    print(f"  {'PROJECT':<30} {'STATUS':<10} {'FAIL':<5} {'WARN':<5} DETAILS")
    print(f"  {'-'*30} {'-'*10} {'-'*5} {'-'*5} {'-'*50}")

    for r in rows:
        icon = {"OK": "\u2705", "WARNINGS": "\u26a0\ufe0f", "FAIL": "\u274c"}.get(r["status"], "?")
        print(f"  {r['key']:<30} {icon} {r['status']:<8} {r['fail_count']:<5} {r['warn_count']:<5} {r['detail']}")

    total_fail = sum(r["fail_count"] for r in rows)
    total_warn = sum(r["warn_count"] for r in rows)
    fail_proj  = sum(1 for r in rows if r["fail_count"] > 0)
    warn_proj  = sum(1 for r in rows if r["warn_count"] > 0 and r["fail_count"] == 0)

    print()
    print(f"  Projects scanned: {len(rows)}")
    if total_fail:
        print(f"  \u274c {total_fail} FAIL(s) across {fail_proj} project(s)")
    if total_warn:
        print(f"  \u26a0\ufe0f {total_warn} WARNING(s) across {warn_proj} project(s)")
    if total_fail == 0 and total_warn == 0:
        print(f"  \u2705 All projects healthy.")

    print()
    if fail_proj > 0:
        print("  Run for a specific project:")
        print(f"    python3 scripts/bootstrap_project.py --validate-only projects/<key> --fix-suggestions")
    elif warn_proj > 0:
        print("  Run with --fix-suggestions for fix hints:")
        print(f"    python3 scripts/bootstrap_project.py --validate-only projects/<key> --fix-suggestions")


if __name__ == "__main__":
    run_all_projects()
