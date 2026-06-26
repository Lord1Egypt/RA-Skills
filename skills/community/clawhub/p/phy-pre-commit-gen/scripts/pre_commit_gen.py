#!/usr/bin/env python3
"""
phy-pre-commit-gen — .pre-commit-config.yaml generator
Analyzes your project's language stack and existing tools,
then generates a tailored pre-commit configuration.
Zero external dependencies — pure Python stdlib only.
"""
from __future__ import annotations
import re
import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

# ── Known hook registry (revs as of early 2026) ──────────────────────────────

HOOKS: dict[str, dict] = {
    # Universal quality hooks
    "pre-commit-hooks": {
        "repo": "https://github.com/pre-commit/pre-commit-hooks",
        "rev": "v4.6.0",
        "hooks": [],  # populated dynamically
    },
    # Security
    "detect-secrets": {
        "repo": "https://github.com/Yelp/detect-secrets",
        "rev": "v1.5.0",
        "hooks": [{"id": "detect-secrets", "args": ["--baseline", ".secrets.baseline"]}],
    },
    "gitleaks": {
        "repo": "https://github.com/gitleaks/gitleaks",
        "rev": "v8.18.4",
        "hooks": [{"id": "gitleaks"}],
    },
    # Python — Ruff (preferred, replaces black+isort+flake8)
    "ruff": {
        "repo": "https://github.com/astral-sh/ruff-pre-commit",
        "rev": "v0.4.7",
        "hooks": [
            {"id": "ruff", "args": ["--fix"]},
            {"id": "ruff-format"},
        ],
    },
    # Python — Black (fallback if ruff not detected)
    "black": {
        "repo": "https://github.com/psf/black",
        "rev": "24.4.2",
        "hooks": [{"id": "black"}],
    },
    # Python — isort
    "isort": {
        "repo": "https://github.com/PyCQA/isort",
        "rev": "5.13.2",
        "hooks": [{"id": "isort", "args": ["--profile", "black"]}],
    },
    # Python — flake8
    "flake8": {
        "repo": "https://github.com/PyCQA/flake8",
        "rev": "7.1.0",
        "hooks": [{"id": "flake8"}],
    },
    # Python — mypy
    "mypy": {
        "repo": "https://github.com/pre-commit/mirrors-mypy",
        "rev": "v1.10.1",
        "hooks": [{"id": "mypy", "additional_dependencies": ["types-all"]}],
    },
    # Python — bandit (security)
    "bandit": {
        "repo": "https://github.com/PyCQA/bandit",
        "rev": "1.7.9",
        "hooks": [{"id": "bandit", "args": ["-c", "pyproject.toml"]}],
    },
    # JavaScript/TypeScript — ESLint
    "eslint": {
        "repo": "https://github.com/pre-commit/mirrors-eslint",
        "rev": "v9.7.0",
        "hooks": [{"id": "eslint", "files": r"\.[jt]sx?$", "types": ["file"]}],
    },
    # JavaScript/TypeScript — Prettier
    "prettier": {
        "repo": "https://github.com/pre-commit/mirrors-prettier",
        "rev": "v3.3.2",
        "hooks": [{"id": "prettier"}],
    },
    # Go
    "golang": {
        "repo": "https://github.com/dnephin/pre-commit-golang",
        "rev": "v0.5.1",
        "hooks": [
            {"id": "go-fmt"},
            {"id": "go-vet"},
            {"id": "go-unit-tests"},
        ],
    },
    # Rust (local — no remote hook available)
    "rust-fmt": {
        "repo": "local",
        "hooks": [
            {
                "id": "rustfmt",
                "name": "rustfmt",
                "entry": "cargo fmt --",
                "language": "system",
                "types": ["rust"],
                "pass_filenames": False,
            }
        ],
    },
    "rust-clippy": {
        "repo": "local",
        "hooks": [
            {
                "id": "clippy",
                "name": "cargo clippy",
                "entry": "cargo clippy -- -D warnings",
                "language": "system",
                "types": ["rust"],
                "pass_filenames": False,
            }
        ],
    },
    # Terraform
    "terraform": {
        "repo": "https://github.com/antonbabenko/pre-commit-terraform",
        "rev": "v1.92.1",
        "hooks": [
            {"id": "terraform_fmt"},
            {"id": "terraform_validate"},
            {"id": "terraform_tflint"},
        ],
    },
    # Conventional commits
    "commitizen": {
        "repo": "https://github.com/commitizen-tools/commitizen",
        "rev": "v3.29.1",
        "hooks": [{"id": "commitizen", "stages": ["commit-msg"]}],
    },
    # Shell scripts
    "shellcheck": {
        "repo": "https://github.com/shellcheck-py/shellcheck-py",
        "rev": "v0.10.0.1",
        "hooks": [{"id": "shellcheck"}],
    },
    # YAML lint
    "yamllint": {
        "repo": "https://github.com/adrienverge/yamllint",
        "rev": "v1.35.1",
        "hooks": [{"id": "yamllint", "args": ["-d", "relaxed"]}],
    },
    # Markdown
    "markdownlint": {
        "repo": "https://github.com/igorshubovych/markdownlint-cli",
        "rev": "v0.41.0",
        "hooks": [{"id": "markdownlint"}],
    },
    # Docker
    "hadolint": {
        "repo": "https://github.com/hadolint/hadolint",
        "rev": "v2.13.0-beta",
        "hooks": [{"id": "hadolint-docker"}],
    },
    # SQL
    "sqlfluff": {
        "repo": "https://github.com/sqlfluff/sqlfluff",
        "rev": "3.1.0",
        "hooks": [{"id": "sqlfluff-lint"}],
    },
}

# ── Project detection ─────────────────────────────────────────────────────────

@dataclass
class ProjectProfile:
    languages: list[str] = field(default_factory=list)
    has_ruff: bool = False
    has_black: bool = False
    has_isort: bool = False
    has_flake8: bool = False
    has_mypy: bool = False
    has_eslint: bool = False
    has_prettier: bool = False
    has_terraform: bool = False
    has_docker: bool = False
    has_shell: bool = False
    has_sql: bool = False
    has_yaml_ci: bool = False
    has_conventional_commits: bool = False
    has_pre_commit_already: bool = False
    existing_hooks: list[str] = field(default_factory=list)
    package_manager: str = ""


def detect_project(root: Path) -> ProjectProfile:
    p = ProjectProfile()

    # Existing pre-commit config?
    if (root / ".pre-commit-config.yaml").exists():
        p.has_pre_commit_already = True
        existing = (root / ".pre-commit-config.yaml").read_text(errors="ignore")
        # Extract existing hook IDs
        p.existing_hooks = re.findall(r"id:\s*(\S+)", existing)

    # Language detection
    if (root / "package.json").exists():
        p.languages.append("javascript")
        try:
            pkg = json.loads((root / "package.json").read_text(errors="ignore"))
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            if any("typescript" in k for k in deps):
                if "typescript" not in p.languages:
                    p.languages.append("typescript")
            p.has_eslint = "eslint" in deps
            p.has_prettier = "prettier" in deps
            p.has_conventional_commits = any(
                k in deps for k in ("commitizen", "@commitlint/cli", "cz-conventional-changelog")
            )
            p.package_manager = "pnpm" if (root / "pnpm-lock.yaml").exists() else \
                                 "yarn" if (root / "yarn.lock").exists() else "npm"
        except Exception:
            pass

    if any(root.glob("*.py")) or (root / "pyproject.toml").exists() or \
       (root / "requirements.txt").exists() or (root / "setup.py").exists():
        p.languages.append("python")
        # Check for ruff
        p.has_ruff = (root / "ruff.toml").exists() or (root / ".ruff.toml").exists() or \
                     _has_section(root, "pyproject.toml", "ruff") or \
                     _has_in_file(root, "requirements*.txt", "ruff")
        p.has_black = _has_section(root, "pyproject.toml", "black") or \
                      _has_in_file(root, "requirements*.txt", "black")
        p.has_isort = (root / ".isort.cfg").exists() or \
                      _has_section(root, "pyproject.toml", "isort") or \
                      _has_section(root, "setup.cfg", "isort") or \
                      _has_in_file(root, "requirements*.txt", "isort")
        p.has_flake8 = (root / ".flake8").exists() or \
                       _has_section(root, "setup.cfg", "flake8") or \
                       _has_in_file(root, "requirements*.txt", "flake8")
        p.has_mypy = (root / "mypy.ini").exists() or \
                     _has_section(root, "pyproject.toml", "mypy") or \
                     _has_section(root, "setup.cfg", "mypy") or \
                     _has_in_file(root, "requirements*.txt", "mypy")

    if (root / "go.mod").exists():
        p.languages.append("go")

    if (root / "Cargo.toml").exists():
        p.languages.append("rust")

    # Infrastructure
    if list(root.rglob("*.tf")):
        p.has_terraform = True

    # Docker
    if list(root.rglob("Dockerfile*")) or list(root.rglob("*.dockerfile")):
        p.has_docker = True

    # Shell
    if list(root.rglob("*.sh")) or list(root.rglob("*.bash")):
        p.has_shell = True

    # SQL
    if list(root.rglob("*.sql")) or list(root.glob("migrations/")):
        p.has_sql = True

    # YAML/CI
    if (root / ".github" / "workflows").is_dir() or (root / ".gitlab-ci.yml").exists():
        p.has_yaml_ci = True

    return p


def _has_section(root: Path, filename: str, section: str) -> bool:
    path = root / filename
    if not path.exists():
        return False
    try:
        return f"[tool.{section}" in path.read_text(errors="ignore") or \
               f"[{section}" in path.read_text(errors="ignore")
    except Exception:
        return False


def _has_in_file(root: Path, glob: str, term: str) -> bool:
    for f in root.glob(glob):
        try:
            if term in f.read_text(errors="ignore"):
                return True
        except Exception:
            pass
    return False


# ── Config builder ────────────────────────────────────────────────────────────

def build_config(profile: ProjectProfile) -> tuple[str, list[str]]:
    """Returns (yaml_string, notes_list)."""
    notes: list[str] = []
    sections: list[str] = []

    # Header
    sections.append("# Generated by phy-pre-commit-gen")
    sections.append("# Run: pre-commit install && pre-commit autoupdate")
    sections.append("# Docs: https://pre-commit.com")
    sections.append("")
    sections.append("repos:")

    already_ids = set(profile.existing_hooks)

    def add_hook(key: str, comment: str = "") -> None:
        if key not in HOOKS:
            return
        h = HOOKS[key]
        block = []
        if comment:
            block.append(f"  # {comment}")
        block.append(f"  - repo: {h['repo']}")
        if h.get("rev"):
            block.append(f"    rev: {h['rev']}")
        block.append("    hooks:")
        for hook in h["hooks"]:
            block.append(f"      - id: {hook['id']}")
            for k, v in hook.items():
                if k == "id":
                    continue
                if isinstance(v, list):
                    block.append(f"        {k}:")
                    for item in v:
                        block.append(f"          - {item}")
                elif isinstance(v, bool):
                    block.append(f"        {k}: {'true' if v else 'false'}")
                else:
                    block.append(f"        {k}: {v}")
        sections.append("\n".join(block))

    # 1. Universal quality hooks
    universal_hooks = [
        "trailing-whitespace",
        "end-of-file-fixer",
        "check-yaml",
        "check-json",
        "check-toml",
        "check-merge-conflict",
        "check-added-large-files",
        "mixed-line-ending",
        "no-commit-to-branch",
    ]
    # Remove already existing
    universal_hooks = [h for h in universal_hooks if h not in already_ids]
    if universal_hooks:
        h = HOOKS["pre-commit-hooks"]
        block = ["  # Universal quality checks"]
        block.append(f"  - repo: {h['repo']}")
        block.append(f"    rev: {h['rev']}")
        block.append("    hooks:")
        for hid in universal_hooks:
            if hid == "no-commit-to-branch":
                block.append(f"      - id: {hid}")
                block.append("        args: [--branch, main, --branch, master]")
            elif hid == "check-added-large-files":
                block.append(f"      - id: {hid}")
                block.append("        args: [--maxkb=1000]")
            else:
                block.append(f"      - id: {hid}")
        sections.append("\n".join(block))

    # 2. Security
    add_hook("detect-secrets", "Secret detection — run once to create baseline:")
    notes.append("  Run: detect-secrets scan > .secrets.baseline  (first time)")

    # 3. Python hooks
    if "python" in profile.languages:
        if profile.has_ruff:
            add_hook("ruff", "Python — Ruff (linter + formatter, replaces black+isort+flake8)")
            notes.append("  Ruff config detected — using ruff hooks")
        elif profile.has_black:
            add_hook("black", "Python — Black formatter")
            if not profile.has_isort:
                notes.append("  Tip: add isort with --profile black for import sorting")
            if profile.has_isort:
                add_hook("isort")
            if profile.has_flake8:
                add_hook("flake8", "Python — Flake8 linter")
        else:
            add_hook("ruff", "Python — Ruff (recommended: fast linter + formatter)")
            notes.append("  No formatter detected — added Ruff as recommended default")
            notes.append("  Alternative: replace with black + isort + flake8 if preferred")

        if profile.has_mypy:
            add_hook("mypy", "Python — Type checking")

    # 4. JavaScript/TypeScript hooks
    if "javascript" in profile.languages or "typescript" in profile.languages:
        if profile.has_eslint:
            add_hook("eslint", "JS/TS — ESLint")
            notes.append(f"  ESLint detected. Add additional_dependencies for your ESLint plugins.")
        if profile.has_prettier:
            add_hook("prettier", "JS/TS — Prettier formatter")
        if not profile.has_eslint and not profile.has_prettier:
            add_hook("prettier", "JS/TS — Prettier (no ESLint/Prettier config detected, adding Prettier as baseline)")
            notes.append("  No JS formatter detected — added Prettier as default")

    # 5. Go
    if "go" in profile.languages:
        add_hook("golang", "Go — fmt + vet + tests")

    # 6. Rust
    if "rust" in profile.languages:
        add_hook("rust-fmt", "Rust — rustfmt")
        add_hook("rust-clippy", "Rust — Clippy linter")

    # 7. Terraform
    if profile.has_terraform:
        add_hook("terraform", "Terraform — fmt + validate + tflint")
        notes.append("  Terraform hooks require: terraform, tflint installed")

    # 8. Docker
    if profile.has_docker:
        add_hook("hadolint", "Dockerfile — Hadolint security linter")

    # 9. Shell
    if profile.has_shell:
        add_hook("shellcheck", "Shell — ShellCheck")

    # 10. SQL
    if profile.has_sql:
        add_hook("sqlfluff", "SQL — SQLFluff linter (set dialect in .sqlfluff)")
        notes.append("  SQLFluff: create .sqlfluff with [sqlfluff] dialect = postgres  (or your dialect)")

    # 11. YAML
    if profile.has_yaml_ci:
        add_hook("yamllint", "YAML — lint CI configs and GitHub Actions")

    # 12. Markdown
    add_hook("markdownlint", "Markdown — markdownlint-cli")

    # 13. Conventional commits
    if profile.has_conventional_commits:
        add_hook("commitizen", "Conventional commits enforcement")
        notes.append("  Commitizen detected — enforcing conventional commit format on commit-msg stage")

    yaml_output = "\n\n".join(sections)
    return yaml_output, notes


# ── Audit existing config ─────────────────────────────────────────────────────

def audit_existing(path: Path) -> list[str]:
    """Returns list of audit findings for an existing .pre-commit-config.yaml."""
    issues: list[str] = []
    try:
        content = path.read_text(errors="ignore")
    except Exception:
        return [f"Cannot read {path}"]

    # Check for pinned revs
    rev_lines = re.findall(r"rev:\s*(\S+)", content)
    for rev in rev_lines:
        if rev in ("latest", "main", "master", "HEAD"):
            issues.append(f"🔴 Unpinned rev '{rev}' — pre-commit hooks should be pinned to a specific tag")

    # Check for local hooks (may not be portable)
    if "repo: local" in content:
        issues.append("🟡 Has local hooks — these won't work out of the box for new contributors")

    # No detect-secrets
    if "detect-secrets" not in content and "gitleaks" not in content:
        issues.append("🟠 No secret detection hook — add detect-secrets or gitleaks")

    # No trailing-whitespace
    if "trailing-whitespace" not in content:
        issues.append("🔵 Missing trailing-whitespace hook from pre-commit-hooks")

    if not issues:
        issues.append("✅ Existing config looks healthy")
    return issues


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(
        description="phy-pre-commit-gen — .pre-commit-config.yaml generator",
    )
    ap.add_argument("target", nargs="?", default=".",
                    help="Project root directory (default: current directory)")
    ap.add_argument("--output", "-o", default=".pre-commit-config.yaml",
                    help="Output file (default: .pre-commit-config.yaml)")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print generated config without writing")
    ap.add_argument("--audit", action="store_true",
                    help="Audit existing .pre-commit-config.yaml instead of generating")
    ap.add_argument("--overwrite", action="store_true",
                    help="Overwrite existing .pre-commit-config.yaml")
    args = ap.parse_args()

    root = Path(args.target).resolve()
    if not root.is_dir():
        print(f"Error: not a directory: {root}", file=sys.stderr)
        sys.exit(2)

    existing = root / ".pre-commit-config.yaml"

    # Audit mode
    if args.audit:
        if not existing.exists():
            print("No .pre-commit-config.yaml found to audit.")
            sys.exit(0)
        print(f"\n📋  Auditing: {existing}\n")
        for issue in audit_existing(existing):
            print(f"  {issue}")
        print("\nRun with --dry-run to see what a fresh generated config would look like.")
        return

    # Generate mode
    print(f"\n🔍  Analyzing project: {root}")
    profile = detect_project(root)

    if profile.languages:
        print(f"   Languages detected: {', '.join(profile.languages)}")
    else:
        print("   No specific language detected — generating universal config")
    if profile.has_ruff:     print("   ✓ Ruff config detected")
    if profile.has_black:    print("   ✓ Black config detected")
    if profile.has_eslint:   print("   ✓ ESLint config detected")
    if profile.has_prettier: print("   ✓ Prettier config detected")
    if profile.has_terraform: print("   ✓ Terraform files detected")
    if profile.has_docker:   print("   ✓ Dockerfiles detected")
    if profile.has_shell:    print("   ✓ Shell scripts detected")

    yaml_output, notes = build_config(profile)

    if args.dry_run:
        print("\n" + "="*60)
        print(yaml_output)
        print("="*60)
    else:
        out_path = root / args.output
        if out_path.exists() and not args.overwrite:
            print(f"\n⚠️  {out_path} already exists.")
            print("   Use --overwrite to replace, or --audit to check the existing file.")
            print("   Use --dry-run to preview the generated config.")
            sys.exit(0)
        out_path.write_text(yaml_output + "\n", encoding="utf-8")
        print(f"\n✅  Written: {out_path}")

    if notes:
        print("\n📌  Notes:")
        for note in notes:
            print(f"  {note}")

    print("\n🚀  Next steps:")
    print("   1. pip install pre-commit   (if not installed)")
    print("   2. pre-commit install       (activate hooks for this repo)")
    print("   3. pre-commit autoupdate    (update hook revisions to latest)")
    print("   4. pre-commit run --all-files  (run all hooks on existing files)")


if __name__ == "__main__":
    main()
