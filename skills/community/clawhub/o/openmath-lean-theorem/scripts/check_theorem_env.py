#!/usr/bin/env python3
"""Post-download preflight checks for OpenMath Lean workspaces."""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_LEAN_REQUIRED_SKILLS = ("lean-proof", "mathlib-build")
DEFAULT_LEAN_OPTIONAL_SKILLS = (
    "lean-mwe",
    "lean-bisect",
    "nightly-testing",
    "mathlib-review",
    "mathlib-pr",
    "lean-pr",
    "lean-setup",
)
DEFAULT_LEAN_SKILL_REPO_URL = os.environ.get(
    "OPENMATH_LEAN_SKILL_REPO_URL",
    "https://github.com/leanprover/skills.git",
)
DEFAULT_LEAN_INSTALL_DIR = os.environ.get("OPENMATH_LEAN_SKILL_INSTALL_DIR", "").strip()
class PreflightError(RuntimeError):
    """Raised when the workspace preflight cannot continue."""


@dataclass(frozen=True)
class WorkspaceInfo:
    root: Path
    language: str
    theorem_json: Path | None


def print_status(kind: str, label: str, detail: str | None = None) -> None:
    suffix = f" - {detail}" if detail else ""
    print(f"[{kind}] {label}{suffix}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check OpenMath Lean workspace toolchains, skills, and build readiness."
    )
    parser.add_argument(
        "workspace",
        nargs="?",
        default=".",
        help="Path to the downloaded theorem workspace (default: current directory).",
    )
    parser.add_argument(
        "--auto-install-skills",
        action="store_true",
        help="Auto-install missing skills only when an explicit install dir is provided via --install-dir or OPENMATH_LEAN_SKILL_INSTALL_DIR.",
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Skip the compiler/build step and only check toolchains + skills.",
    )
    parser.add_argument(
        "--skills-dir",
        action="append",
        default=[],
        help="Additional skills directory to search. Can be passed multiple times.",
    )
    parser.add_argument(
        "--install-dir",
        help="Explicit skills directory to install missing Lean skills into when using --auto-install-skills.",
    )
    return parser


def run_command(
    args: list[str],
    cwd: Path | None = None,
    capture: bool = True,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=capture,
    )


def require_command(name: str) -> str:
    resolved = shutil.which(name)
    if not resolved:
        raise PreflightError(f"missing required command: {name}")
    return resolved


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def detect_language(workspace: Path) -> WorkspaceInfo:
    workspace = workspace.resolve()
    if workspace.is_file():
        workspace = workspace.parent

    theorem_json = workspace / "theorem.json"
    if theorem_json.is_file():
        payload = read_json(theorem_json)
        language = str(payload.get("language", "")).strip().lower()
        if language == "lean":
            return WorkspaceInfo(workspace, language, theorem_json)
        if language == "rocq":
            raise PreflightError(
                "detected a Rocq theorem workspace; use the openmath-rocq-theorem skill instead"
            )

    if (workspace / "lean-toolchain").is_file() or (workspace / "lakefile.lean").is_file():
        return WorkspaceInfo(workspace, "lean", theorem_json if theorem_json.is_file() else None)

    if (workspace / "_CoqProject").is_file() or any(workspace.glob("*.v")):
        raise PreflightError(
            "detected a Rocq/Coq workspace; use the openmath-rocq-theorem skill instead"
        )

    raise PreflightError(f"could not detect a Lean theorem workspace from: {workspace}")


def extract_expected_lean_version(workspace: Path) -> str | None:
    toolchain = workspace / "lean-toolchain"
    if not toolchain.is_file():
        return None
    raw = toolchain.read_text(encoding="utf-8").strip()
    match = re.search(r"v?(\d+\.\d+\.\d+)", raw)
    return match.group(1) if match else None


def extract_reported_lean_version(text: str) -> str | None:
    match = re.search(r"version\s+(\d+\.\d+\.\d+)", text)
    return match.group(1) if match else None


def default_skill_dirs() -> list[Path]:
    custom = os.environ.get("OPENMATH_SKILL_DIRS", "").strip()
    if custom:
        return [Path(item).expanduser() for item in custom.split(os.pathsep) if item.strip()]

    candidates = [
        Path.home() / ".agent" / "skills",
        Path.home() / ".agents" / "skills",
        Path.home() / ".codex" / "skills",
        Path.home() / ".claude" / "skills",
        Path.home() / ".cursor" / "skills",
        Path.home() / ".gemini" / "skills",
        REPO_ROOT / ".claude" / "skills",
        REPO_ROOT / ".cursor" / "skills",
        REPO_ROOT / ".codex" / "skills",
        REPO_ROOT / ".gemini" / "skills",
    ]
    return [path for path in candidates if path.exists()]


def find_skill(skill_name: str, search_dirs: list[Path]) -> Path | None:
    for directory in search_dirs:
        candidate = directory / skill_name
        if candidate.is_dir():
            return candidate
    return None


def skills_status(
    required: tuple[str, ...],
    optional: tuple[str, ...],
    search_dirs: list[Path],
) -> tuple[list[str], list[str]]:
    missing_required: list[str] = []
    missing_optional: list[str] = []

    for skill in required:
        location = find_skill(skill, search_dirs)
        if location:
            print_status("ok", f"skill {skill}", str(location))
        else:
            print_status("missing", f"skill {skill}")
            missing_required.append(skill)

    for skill in optional:
        location = find_skill(skill, search_dirs)
        if location:
            print_status("ok", f"optional skill {skill}", str(location))
        else:
            print_status("warn", f"optional skill {skill}", "not installed")
            missing_optional.append(skill)

    return missing_required, missing_optional


def choose_lean_install_dir(
    search_dirs: list[Path],
    install_dir_override: str | None = None,
) -> Path | None:
    if install_dir_override:
        return Path(install_dir_override).expanduser()

    if DEFAULT_LEAN_INSTALL_DIR:
        return Path(DEFAULT_LEAN_INSTALL_DIR).expanduser()
    return None


def print_lean_install_commands(missing_skills: list[str], install_dir: Path) -> None:
    print("Preferred manual install:")
    for skill in missing_skills:
        print(f"npx leanprover-skills install {shlex.quote(skill)}")
    print("")
    print("Source install into the explicit target dir:")
    print(
        "git clone --depth 1 "
        f"{shlex.quote(DEFAULT_LEAN_SKILL_REPO_URL)} /tmp/leanprover-skills"
    )
    for skill in missing_skills:
        print(
            "cp -R "
            f"/tmp/leanprover-skills/skills/{shlex.quote(skill)} "
            f"{shlex.quote(str(install_dir))}/"
        )


def maybe_install_lean_skills(
    missing_skills: list[str],
    search_dirs: list[Path],
    auto_install: bool,
    install_dir_override: str | None = None,
) -> bool:
    if not missing_skills:
        return True

    install_dir = choose_lean_install_dir(search_dirs, install_dir_override=install_dir_override)
    print_status("info", "lean skill source", DEFAULT_LEAN_SKILL_REPO_URL)
    if install_dir is not None:
        print_status("info", "lean skill install dir", str(install_dir))
        print_status(
            "warn",
            "lean skill install side effect",
            "clones the reviewed upstream repo and copies third-party skill directories into the explicit install dir",
        )
        print_lean_install_commands(missing_skills, install_dir)
    else:
        print_status(
            "missing",
            "lean skill install dir",
            "pass --install-dir <path> or set OPENMATH_LEAN_SKILL_INSTALL_DIR before using --auto-install-skills",
        )
        print("Preferred manual install:")
        for skill in missing_skills:
            print(f"npx leanprover-skills install {shlex.quote(skill)}")
    if not auto_install:
        return False

    if install_dir is None:
        print_status(
            "missing",
            "skill installation",
            "auto-install requires an explicit install dir; refusing to pick a shared home-directory skills folder automatically",
        )
        return False

    if not shutil.which("git"):
        print_status("missing", "skill installer", "command not found: git")
        return False

    print_status("info", "auto-installing missing skills", ", ".join(missing_skills))
    try:
        install_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print_status("missing", "skill installation", f"cannot create {install_dir}: {exc}")
        return False

    if install_dir not in search_dirs:
        search_dirs.append(install_dir)

    with tempfile.TemporaryDirectory(prefix="openmath-lean-skills-") as tmpdir:
        repo_dir = Path(tmpdir) / "leanprover-skills"
        clone = run_command(
            ["git", "clone", "--depth", "1", DEFAULT_LEAN_SKILL_REPO_URL, str(repo_dir)],
            cwd=REPO_ROOT,
        )
        if clone.returncode != 0:
            detail = clone.stderr.strip() or clone.stdout.strip() or "git clone failed"
            print_status("missing", "skill installation", detail)
            return False

        for skill in missing_skills:
            src = repo_dir / "skills" / skill
            dest = install_dir / skill
            if not src.is_dir():
                print_status("missing", "skill installation", f"missing in repo: {src}")
                return False
            try:
                shutil.copytree(src, dest, dirs_exist_ok=True)
            except OSError as exc:
                print_status("missing", "skill installation", f"copy failed for {skill}: {exc}")
                return False
            print_status("ok", f"installed skill {skill}", str(dest))

    print_status("ok", "skill installation", "completed")
    return True


def lean_needs_mathlib(workspace: Path) -> bool:
    lakefile = workspace / "lakefile.lean"
    if lakefile.is_file() and "require mathlib" in lakefile.read_text(encoding="utf-8"):
        return True

    for lean_file in workspace.glob("*.lean"):
        if "import Mathlib" in lean_file.read_text(encoding="utf-8"):
            return True
    return False


def check_lean_toolchain(workspace: Path) -> bool:
    ready = True
    try:
        lean_bin = require_command("lean")
        print_status("ok", "lean command", lean_bin)
    except PreflightError as exc:
        print_status("missing", "lean command", str(exc))
        return False

    try:
        lake_bin = require_command("lake")
        print_status("ok", "lake command", lake_bin)
    except PreflightError as exc:
        print_status("missing", "lake command", str(exc))
        return False

    elan_bin = shutil.which("elan")
    if elan_bin:
        print_status("ok", "elan command", elan_bin)
    else:
        print_status("warn", "elan command", "not found; lean-toolchain switching may not work")

    lean_version = run_command(["lean", "--version"])
    if lean_version.returncode != 0:
        print_status("missing", "lean --version", lean_version.stderr.strip() or "failed")
        return False

    actual = extract_reported_lean_version(lean_version.stdout)
    expected = extract_expected_lean_version(workspace)
    detail = lean_version.stdout.strip().splitlines()[0] if lean_version.stdout.strip() else "unknown"
    print_status("ok", "lean version", detail)

    if expected and actual and expected != actual:
        print_status("warn", "lean-toolchain version mismatch", f"expected {expected}, got {actual}")
        ready = False
    elif expected:
        print_status("ok", "lean-toolchain version", expected)

    lake_version = run_command(["lake", "--version"])
    if lake_version.returncode != 0:
        print_status("missing", "lake --version", lake_version.stderr.strip() or "failed")
        return False
    print_status("ok", "lake version", lake_version.stdout.strip().splitlines()[0])
    return ready


def run_lean_build(workspace: Path) -> bool:
    needs_mathlib = lean_needs_mathlib(workspace)
    if needs_mathlib:
        print_status("info", "mathlib dependency", "running `lake exe cache get`")
        cache = run_command(["lake", "exe", "cache", "get"], cwd=workspace)
        if cache.returncode != 0:
            detail = cache.stderr.strip() or cache.stdout.strip() or "cache fetch failed"
            print_status("missing", "lake exe cache get", detail)
            return False
        print_status("ok", "lake exe cache get")
    else:
        print_status("ok", "mathlib dependency", "not required")

    build = run_command(["lake", "build", "-q", "--log-level=info"], cwd=workspace)
    if build.returncode != 0:
        detail = build.stderr.strip() or build.stdout.strip() or "build failed"
        print_status("missing", "lake build", detail)
        return False

    print_status("ok", "lake build")
    return True


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv or sys.argv[1:])

    try:
        info = detect_language(Path(args.workspace))
    except PreflightError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    search_dirs = default_skill_dirs()
    search_dirs.extend(Path(path).expanduser() for path in args.skills_dir)

    print("Workspace:", info.root)
    print("Language:", info.language)
    if info.theorem_json:
        print("theorem.json:", info.theorem_json)
    print()
    print("Toolchain checks")

    ready = True
    ready = check_lean_toolchain(info.root) and ready

    print()
    print("Skill checks")

    missing_required, _ = skills_status(
        DEFAULT_LEAN_REQUIRED_SKILLS,
        DEFAULT_LEAN_OPTIONAL_SKILLS,
        search_dirs,
    )
    installed = maybe_install_lean_skills(
        missing_required,
        search_dirs,
        args.auto_install_skills,
        args.install_dir,
    )
    if missing_required and not installed:
        ready = False
    elif missing_required and installed:
        refreshed_missing, _ = skills_status(DEFAULT_LEAN_REQUIRED_SKILLS, (), search_dirs)
        if refreshed_missing:
            ready = False

    if args.skip_build:
        print()
        print("Build checks")
        print_status("warn", "build step", "skipped by --skip-build")
    else:
        print()
        print("Build checks")
        ready = run_lean_build(info.root) and ready

    print()
    if ready:
        print("Status: ready")
        return 0

    print("Status: not ready")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
