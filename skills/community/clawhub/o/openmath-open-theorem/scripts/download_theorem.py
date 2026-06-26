#!/usr/bin/env python3
"""Download an OpenMath theorem and scaffold a local proof environment."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

from openmath_api import TheoremRecord, fetch_theorem_detail, format_datetime
from openmath_env_config import (
    OpenMathEnvConfigError,
    load_openmath_preferences,
    resolve_openmath_site_url,
)


LEAN_TOOLCHAIN = "leanprover/lean4:v4.28.0"
MATHLIB_TAG = "v4.28.0"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "theorem"


def default_output_dir(theorem: TheoremRecord) -> Path:
    language = theorem.language.lower()
    return Path("tmp") / f"openmath-theorem-{theorem.theorem_id}-{language}"


def lean_module_name(theorem_id: int) -> str:
    return f"OpenMathTheorem{theorem_id}"


def render_readme(theorem: TheoremRecord, project_dir: Path, entrypoint: str) -> str:
    title_slug = slugify(theorem.title)
    try:
        openmath_site_url = resolve_openmath_site_url()
    except OpenMathEnvConfigError as exc:
        raise RuntimeError(str(exc)) from exc
    lines = [
        f"# {theorem.title}",
        "",
        f"- Theorem ID: `{theorem.theorem_id}`",
        f"- Language: `{theorem.language}`",
        f"- Reward: `{theorem.reward}`",
        f"- Status: `{theorem.status}`",
        f"- Expires: `{format_datetime(theorem.expire_time)}`",
        f"- Project directory: `{project_dir.name}`",
        f"- Suggested entry file: `{entrypoint}`",
        f"- OpenMath URL: `{openmath_site_url}/theorem/{theorem.theorem_id}`",
        "",
        "## Description",
        "",
        theorem.description,
        "",
        "## Next Steps",
        "",
        "1. Run `python3 scripts/check_theorem_env.py <workspace>` before proving anything.",
        "2. Read the generated theorem source and confirm imports / dependencies.",
        "3. Use the `lean-proof` skill if you need help formalizing or debugging the local proof.",
        "4. Replace placeholders or incomplete proof bodies with your actual proof.",
        "5. After verification, use `openmath-submit-theorem` to generate submission commands.",
        "",
        "## Notes",
        "",
        f"- This scaffold was generated from OpenMath theorem `{theorem.theorem_id}` (`{title_slug}`).",
        "- You may need to adjust dependency versions to match the exact OpenMath sandbox.",
    ]
    return "\n".join(lines) + "\n"


def needs_mathlib(theorem_code: str) -> bool:
    for line in theorem_code.splitlines():
        stripped = line.strip()
        if stripped.startswith("import Mathlib"):
            return True
    return False


def render_lean_lakefile(package_name: str, with_mathlib: bool = True) -> str:
    mathlib_block = f"""
require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "{MATHLIB_TAG}"
""" if with_mathlib else "\n"
    return f"""import Lake
open Lake DSL

package «{package_name}» where
{mathlib_block}
lean_lib «{package_name}» where
"""


def write_common_files(project_dir: Path, theorem: TheoremRecord, entrypoint: str) -> None:
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "theorem.json").write_text(
        json.dumps(theorem.raw, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (project_dir / "README.md").write_text(
        render_readme(theorem, project_dir, entrypoint),
        encoding="utf-8",
    )
    (project_dir / ".gitignore").write_text(".lake/\n.lean/\nbuild/\n*.aux\n*.glob\n", encoding="utf-8")


def scaffold_lean(project_dir: Path, theorem: TheoremRecord) -> str:
    module_name = lean_module_name(theorem.theorem_id)
    theorem_file = project_dir / f"{module_name}.lean"
    theorem_code = theorem.theorem_code or f"-- TODO: Fill in theorem {theorem.theorem_id}\n"
    theorem_file.write_text(theorem_code.rstrip() + "\n", encoding="utf-8")

    with_mathlib = needs_mathlib(theorem_code)

    (project_dir / "Main.lean").write_text(
        f'import {module_name}\n',
        encoding="utf-8",
    )
    (project_dir / "lakefile.lean").write_text(
        render_lean_lakefile(module_name, with_mathlib=with_mathlib),
        encoding="utf-8",
    )
    (project_dir / "lean-toolchain").write_text(f"{LEAN_TOOLCHAIN}\n", encoding="utf-8")
    return theorem_file.name


def scaffold_rocq(project_dir: Path, theorem: TheoremRecord) -> str:
    theorem_file = project_dir / f"Theorem_{theorem.theorem_id}.v"
    theorem_code = theorem.theorem_code or f"(* TODO: Fill in theorem {theorem.theorem_id} *)\n"
    theorem_file.write_text(theorem_code.rstrip() + "\n", encoding="utf-8")

    (project_dir / "_CoqProject").write_text(
        f"-Q . OpenMath\n{theorem_file.name}\n",
        encoding="utf-8",
    )
    return theorem_file.name


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Download an OpenMath theorem and scaffold a local proof workspace."
    )
    parser.add_argument("theorem_id", type=int, help="OpenMath theorem ID")
    parser.add_argument(
        "--output-dir",
        help="Target directory for the generated project. Defaults to openmath-theorem-<id>-<language>.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace the target directory if it already exists.",
    )
    parser.add_argument(
        "--config",
        default=None,
        help="Explicit config path. Default: auto-discover from ./.openmath-skills or ~/.openmath-skills.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv or sys.argv[1:])

    try:
        load_openmath_preferences(
            args.config,
            require_preferred_language=True,
        )
    except OpenMathEnvConfigError as exc:
        print(exc, file=sys.stderr)
        return 1

    try:
        theorem = fetch_theorem_detail(args.theorem_id)
    except RuntimeError as exc:
        print(f"Failed to download theorem: {exc}", file=sys.stderr)
        return 1

    project_dir = Path(args.output_dir) if args.output_dir else default_output_dir(theorem)
    if project_dir.exists():
        if not args.force:
            print(
                f"Error: output directory already exists: {project_dir}. Use --force to replace it.",
                file=sys.stderr,
            )
            return 1
        shutil.rmtree(project_dir)

    project_dir.mkdir(parents=True, exist_ok=True)

    language = theorem.language.lower()
    if language == "lean":
        entrypoint = scaffold_lean(project_dir, theorem)
    elif language == "rocq":
        entrypoint = scaffold_rocq(project_dir, theorem)
    else:
        print(f"Error: unsupported theorem language: {theorem.language}", file=sys.stderr)
        return 1

    try:
        write_common_files(project_dir, theorem, entrypoint)
    except RuntimeError as exc:
        print(f"Failed to write scaffold files: {exc}", file=sys.stderr)
        return 1

    print(f"Created project: {project_dir}")
    print(f"Language: {theorem.language}")
    print(f"Entry file: {entrypoint}")
    print("Files:")
    for path in sorted(project_dir.rglob("*")):
        if path.is_file():
            print(f"  - {path.relative_to(project_dir)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
