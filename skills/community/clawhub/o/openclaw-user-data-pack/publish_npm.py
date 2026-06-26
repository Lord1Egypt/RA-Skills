#!/usr/bin/env python3
"""
Publish this skill to npm (and optionally ClawHub).

Before publish:
1. Aligns local package.json to npm if registry is ahead
2. Bumps patch version (x.y.z -> x.y.(z+1))
3. Syncs version to package.json, SKILL.md frontmatter, scripts/__init__.py
4. Runs npm publish
5. If `clawhub` is on PATH and SKIP_CLAWHUB is not set: clawhub publish
6. Optional hook: skill.ps1 / skill.cmd / skill.bat (Windows) or skill.sh (Unix)

Usage:
  python publish_npm.py
  python publish_npm.py "changelog text"

Prerequisites: npm login; clawhub login (for step 5). On Windows, use plain python from repo root.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from typing import Optional

ROOT = os.path.dirname(os.path.abspath(__file__))
PACKAGE_JSON = os.path.join(ROOT, "package.json")
SKILL_MD = os.path.join(ROOT, "SKILL.md")
INIT_PY = os.path.join(ROOT, "scripts", "__init__.py")


def bump_patch_version(version: str) -> str:
    parts = version.strip().split(".")
    if len(parts) < 3:
        return f"{version}.1" if len(parts) == 1 else f"{version}.0"
    try:
        parts[2] = str(int(parts[2]) + 1)
        return ".".join(parts)
    except ValueError:
        return version


def get_npm_version(package_name: str) -> Optional[str]:
    try:
        result = subprocess.run(
            ["npm", "view", package_name, "version"],
            capture_output=True,
            text=True,
            cwd=ROOT,
            shell=(os.name == "nt"),
            timeout=15,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def sync_skill_md(new_version: str) -> bool:
    if not os.path.isfile(SKILL_MD):
        return False
    with open(SKILL_MD, encoding="utf-8") as f:
        content = f.read()
    new_content, n = re.subn(r"(version:\s*)[\d.]+", r"\g<1>" + new_version, content, count=1)
    if n == 0:
        new_content, m = re.subn(
            r"(name:\s*\S+\n)",
            r"\1version: " + new_version + "\n",
            content,
            count=1,
        )
        if m == 0:
            return False
    with open(SKILL_MD, "w", encoding="utf-8") as f:
        f.write(new_content)
    return True


def sync_init_py(new_version: str) -> bool:
    if not os.path.isfile(INIT_PY):
        return False
    with open(INIT_PY, encoding="utf-8") as f:
        content = f.read()
    new_content, n = re.subn(
        r'(__version__\s*=\s*")[\d.]+(")',
        r"\g<1>" + new_version + r"\2",
        content,
        count=1,
    )
    if n == 0:
        return False
    with open(INIT_PY, "w", encoding="utf-8") as f:
        f.write(new_content)
    return True


def run_optional_hook(version: str, changelog: str) -> None:
    if os.name == "nt":
        for name in ("skill.ps1", "skill.cmd", "skill.bat"):
            p = os.path.join(ROOT, name)
            if os.path.isfile(p):
                if name.endswith(".ps1"):
                    subprocess.run(
                        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", p, version, changelog],
                        cwd=ROOT,
                        shell=False,
                    )
                else:
                    subprocess.run([p, version, changelog], cwd=ROOT, shell=True)
                print(f"ran hook: {name}")
                return
    else:
        p = os.path.join(ROOT, "skill.sh")
        if os.path.isfile(p) and os.access(p, os.X_OK):
            subprocess.run([p, version, changelog], cwd=ROOT)
            print("ran hook: skill.sh")


def clawhub_publish(version: str, changelog: str) -> int:
    exe = shutil.which("clawhub")
    if not exe:
        print("clawhub not on PATH — skip (install: npm i -g clawhub)")
        return 0
    slug = os.environ.get("CLAWHUB_SLUG", "openclaw-user-data-pack")
    name = os.environ.get("CLAWHUB_NAME", "OpenClaw User Data Pack")
    cmd = [
        exe,
        "publish",
        ".",
        "--slug",
        slug,
        "--name",
        name,
        "--version",
        version,
        "--changelog",
        changelog,
        "--tags",
        "latest",
    ]
    return subprocess.run(cmd, cwd=ROOT, shell=(os.name == "nt")).returncode


def main() -> None:
    changelog = sys.argv[1] if len(sys.argv) > 1 else None

    if not os.path.isfile(SKILL_MD):
        print("SKILL.md not found in project root", file=sys.stderr)
        sys.exit(1)
    if not os.path.isfile(PACKAGE_JSON):
        print("package.json not found in project root", file=sys.stderr)
        sys.exit(1)

    with open(PACKAGE_JSON, encoding="utf-8") as f:
        pkg = json.load(f)
    pkg_name = pkg.get("name", "")
    local_version = pkg.get("version", "1.0.0")
    npm_version = get_npm_version(pkg_name) if pkg_name else None

    if npm_version:
        print(f"npm current version: {npm_version}")

    base = npm_version if npm_version else local_version
    if npm_version and local_version != npm_version:
        pkg["version"] = npm_version
        with open(PACKAGE_JSON, "w", encoding="utf-8") as f:
            json.dump(pkg, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"Local synced to npm version: {npm_version}")

    new_version = bump_patch_version(base)
    pkg["version"] = new_version
    with open(PACKAGE_JSON, "w", encoding="utf-8") as f:
        json.dump(pkg, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"Version bumped: {base} -> {new_version}")

    if sync_skill_md(new_version):
        print(f"SKILL.md version synced: {new_version}")
    else:
        print("Warning: SKILL.md version not updated", file=sys.stderr)

    if sync_init_py(new_version):
        print(f"scripts/__init__.py version synced: {new_version}")
    else:
        print("Warning: scripts/__init__.py version not updated", file=sys.stderr)

    msg = changelog if changelog else f"Release {new_version}"

    if os.environ.get("SKIP_NPM") == "1":
        print("[SKIP_NPM=1] skip npm publish")
    else:
        result = subprocess.run(["npm", "publish", "--access", "public"], cwd=ROOT, shell=(os.name == "nt"))
        if result.returncode != 0:
            print(
                "npm publish failed. Try: npm login. 403: enable 2FA or granular token.",
                file=sys.stderr,
            )
            sys.exit(result.returncode)
        print(f"Published to npm: {new_version}")

    if os.environ.get("SKIP_CLAWHUB") == "1":
        print("[SKIP_CLAWHUB=1] skip clawhub")
    else:
        rc = clawhub_publish(new_version, msg)
        if rc != 0:
            print("clawhub publish failed", file=sys.stderr)
            sys.exit(rc)
        print(f"Published to ClawHub: {new_version}")

    run_optional_hook(new_version, msg)
    print(f"Done: {new_version}")


if __name__ == "__main__":
    main()
