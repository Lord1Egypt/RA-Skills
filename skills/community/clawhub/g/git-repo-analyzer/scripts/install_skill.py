#!/usr/bin/env python3
"""Install a staged Skill into ~/.openclaw/skills/installed/."""
import sys, os, shutil, json, re, pathlib


def install(tmp_dir: str, repo_name: str, url: str):
    install_dir = pathlib.Path.home() / ".openclaw" / "skills" / "installed" / repo_name
    install_dir.parent.mkdir(parents=True, exist_ok=True)

    if install_dir.exists():
        shutil.rmtree(install_dir)
    shutil.copytree(tmp_dir, install_dir)

    # Clean up staging
    shutil.rmtree(tmp_dir, ignore_errors=True)

    skill_md = install_dir / "SKILL.md"
    skill_name = repo_name
    if skill_md.exists():
        m = re.search(r"^name:\s*(.+)$", skill_md.read_text(encoding="utf-8"), re.M)
        if m:
            skill_name = m.group(1).strip()

    return {
        "name": skill_name,
        "installDir": str(install_dir),
        "url": url,
    }


if __name__ == "__main__":
    tmp_dir = sys.argv[1] if len(sys.argv) > 1 else ""
    repo_name = sys.argv[2] if len(sys.argv) > 2 else "repo"
    url = sys.argv[3] if len(sys.argv) > 3 else ""
    if not tmp_dir or not repo_name:
        print(json.dumps({"error": "tmp_dir and repo_name required"}), file=sys.stderr)
        sys.exit(1)
    print(json.dumps(install(tmp_dir, repo_name, url), ensure_ascii=False))
