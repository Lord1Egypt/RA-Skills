#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


MAX_SCAN_BYTES = 1_000_000
MAX_FILES = 400

SECRET_PATTERNS = [
    ("openai_key", re.compile(r"\bsk-[A-Za-z0-9]{20,}\b")),
    ("github_token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("anthropic_key", re.compile(r"\bsk-ant-[A-Za-z0-9\-_]{20,}\b")),
    ("generic_api_key", re.compile(r"(?i)(api[_-]?key|token|secret)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}")),
]

LOCAL_PATH_PATTERNS = [
    re.compile(r"/Users/[^/\s]+"),
    re.compile(r"/home/[^/\s]+"),
    re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+"),
]

MODEL_NAMES = ["claude", "gpt-4", "gpt-5", "openai", "qwen", "deepseek", "gemini", "codex"]
IGNORED_DIRS = {".git", "node_modules", "dist", "build", "__pycache__", ".venv", "venv"}
TEXT_EXTS = {
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".sh",
    ".env",
    ".toml",
    ".ini",
    ".cfg",
}
DOC_LIKE_EXTS = {
    ".md",
    ".txt",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".cfg",
}

README_EN_FILES = ("README.md", "README")
README_ZH_FILES = ("README.zh-CN.md", "README_zh-CN.md", "README.zh.md")


def is_text_candidate(path: Path) -> bool:
    if path.name.startswith(".env"):
        return True
    return path.suffix.lower() in TEXT_EXTS or path.name in {"SKILL.md", "README", "README.md", "_meta.json", "skill.json"}


def iter_files(root: Path):
    count = 0
    for path in root.rglob("*"):
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        if path.is_file():
            yield path
            count += 1
            if count >= MAX_FILES:
                return


def read_text(path: Path) -> str | None:
    try:
        if path.stat().st_size > MAX_SCAN_BYTES:
            return None
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None


def check_skill_metadata(root: Path, findings: list[dict]) -> None:
    skill = root / "SKILL.md"
    if skill.exists():
        text = read_text(skill) or ""
        if not text.startswith("---"):
            findings.append({"severity": "medium", "type": "skill_frontmatter", "message": "SKILL.md is missing YAML frontmatter."})
        if "homepage:" not in text:
            findings.append({"severity": "low", "type": "skill_homepage", "message": "SKILL.md frontmatter does not declare a homepage."})
    if (root / "skill.json").exists() and not (root / "SKILL.md").exists():
        findings.append({"severity": "medium", "type": "skill_missing_markdown", "message": "skill.json exists but SKILL.md is missing."})
    if (root / "SKILL.md").exists() and not (root / "skill.json").exists():
        findings.append({"severity": "low", "type": "skill_missing_json", "message": "SKILL.md exists but skill.json is missing."})
    if (root / "_meta.json").exists() is False and "skills" in root.parts:
        findings.append({"severity": "low", "type": "skill_meta", "message": "No _meta.json found for a skills-style directory."})


def find_first_existing(root: Path, names: tuple[str, ...]) -> Path | None:
    for name in names:
        path = root / name
        if path.exists():
            return path
    return None


def check_docs_governance(root: Path, findings: list[dict]) -> None:
    readme_en = find_first_existing(root, README_EN_FILES)
    readme_zh = find_first_existing(root, README_ZH_FILES)

    if not readme_en:
        findings.append({"severity": "medium", "type": "readme_missing", "message": "README.md is missing."})
    else:
        text = read_text(readme_en) or ""
        if "README.zh-CN.md" not in text and "中文" not in text and "Chinese" not in text:
            findings.append({
                "severity": "low",
                "type": "readme_bilingual_link",
                "message": "README.md does not clearly link to a Chinese README or mention localization."
            })

    if not readme_zh:
        findings.append({
            "severity": "low",
            "type": "readme_zh_missing",
            "message": "No Chinese README found. Consider adding README.zh-CN.md for bilingual public repos."
        })
    else:
        text = read_text(readme_zh) or ""
        if "README.md" not in text and "English" not in text:
            findings.append({
                "severity": "low",
                "type": "readme_en_link",
                "message": f"{readme_zh.name} does not clearly link back to the English README."
            })

    if not (root / "CHANGELOG.md").exists():
        findings.append({
            "severity": "low",
            "type": "changelog_missing",
            "message": "CHANGELOG.md is missing. Public package-style repos should document visible upgrades."
        })


def should_skip_self_reference_checks(path: Path) -> bool:
    return path.name in {"repo_commander_audit.py", ".project_root"}


def should_check_model_specificity(path: Path) -> bool:
    if path.name.startswith(".env"):
        return False
    return path.suffix.lower() in DOC_LIKE_EXTS or path.name in {"SKILL.md", "README", "README.md"}


def audit_repo(root: Path) -> dict:
    findings: list[dict] = []
    stats = {"filesScanned": 0}

    sensitive_files = [".env", ".env.local", ".env.production", "config.json", "secrets.json"]
    for name in sensitive_files:
        path = root / name
        if path.exists():
            findings.append({"severity": "high", "type": "sensitive_file", "message": f"Sensitive file present: {path.name}"})

    check_docs_governance(root, findings)

    check_skill_metadata(root, findings)

    for path in iter_files(root):
        stats["filesScanned"] += 1
        if not is_text_candidate(path):
            continue
        text = read_text(path)
        if not text:
            continue

        for name, pattern in SECRET_PATTERNS:
            if pattern.search(text):
                findings.append({
                    "severity": "high",
                    "type": "secret_like_string",
                    "message": f"Potential {name} exposed in {path.relative_to(root)}",
                })

        if not should_skip_self_reference_checks(path):
            for pattern in LOCAL_PATH_PATTERNS:
                if pattern.search(text):
                    findings.append({
                        "severity": "high",
                        "type": "local_path_leak",
                        "message": f"Local machine path found in {path.relative_to(root)}",
                    })
                    break

        if not should_skip_self_reference_checks(path):
            lowered = text.lower()
            model_hits = [name for name in MODEL_NAMES if name in lowered]
            if len(model_hits) >= 2 and should_check_model_specificity(path) and path.name not in {"README.md", "README"}:
                findings.append({
                    "severity": "low",
                    "type": "model_specificity",
                    "message": f"Model-specific wording found in {path.relative_to(root)}: {', '.join(sorted(set(model_hits)))}",
                })

    severities = {"high": 0, "medium": 0, "low": 0}
    for finding in findings:
        severities[finding["severity"]] += 1

    return {
        "repo": str(root),
        "summary": {
            "high": severities["high"],
            "medium": severities["medium"],
            "low": severities["low"],
            "filesScanned": stats["filesScanned"],
        },
        "findings": findings,
    }


def print_text_report(report: dict, strict: bool) -> int:
    summary = report["summary"]
    print(f"Repo: {report['repo']}")
    print(f"Findings: high={summary['high']} medium={summary['medium']} low={summary['low']} files={summary['filesScanned']}")
    if not report["findings"]:
        print("No obvious blockers found.")
        return 0

    for finding in report["findings"]:
        print(f"[{finding['severity'].upper()}] {finding['type']}: {finding['message']}")

    if strict and summary["high"] > 0:
        return 2
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit a GitHub repository for privacy, packaging, and skill-compliance issues.")
    parser.add_argument("repo_path")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    root = Path(args.repo_path).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Error: repo path not found: {root}")

    report = audit_repo(root)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 2 if args.strict and report["summary"]["high"] > 0 else 0
    return print_text_report(report, args.strict)


if __name__ == "__main__":
    raise SystemExit(main())
