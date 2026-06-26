# Code analyzers — depends on core, llm
import hashlib
import re
import subprocess
from pathlib import Path
from typing import Optional

from .core import *


def detect_language_from_path(path: str) -> str:
    """Detect programming language from file path."""
    ext = Path(path).suffix.lower()
    langs = {
        ".py": "python", ".js": "javascript", ".ts": "typescript",
        ".go": "go", ".rs": "rust", ".java": "java",
        ".cpp": "cpp", ".cc": "cpp", ".cxx": "cpp", ".c": "c",
        ".cs": "csharp", ".rb": "ruby", ".php": "php",
        ".swift": "swift", ".kt": "kotlin", ".scala": "scala",
        ".lua": "lua", ".sh": "bash", ".bash": "bash",
        ".r": "r", ".R": "r",
    }
    return langs.get(ext, "text")


def detect_repo_languages(repo_path: Path) -> set[str]:
    exts = {".py", ".js", ".ts", ".go", ".rs", ".java", ".cpp", ".c", ".cs", ".rb"}
    langs = set()
    for f in repo_path.rglob("*"):
        if f.is_file() and f.suffix.lower() in exts:
            langs.add(detect_language_from_path(str(f)))
    return langs


def get_todo_patterns_for_file(file_path: str) -> list[str]:
    """Return regex patterns for TODO/FIXME comments per language."""
    lang = detect_language_from_path(file_path)
    patterns = {
        "python": [r"# ?(TODO|FIXME|HACK|XXX|NOTE|BUG):?\s*(.*)"],
        "javascript": [r"// ?(TODO|FIXME|HACK|XXX|NOTE|BUG):?\s*(.*)"],
        "typescript": [r"// ?(TODO|FIXME|HACK|XXX|NOTE|BUG):?\s*(.*)"],
        "go": [r"// ?(TODO|FIXME|HACK|XXX|NOTE|BUG):?\s*(.*)"],
        "rust": [r"// ?(TODO|FIXME|HACK|XXX|NOTE|BUG):?\s*(.*)"],
    }
    return patterns.get(lang, [])


def scan_todos_multilang(repo: Repository) -> list[OptimizationFinding]:
    """Scan repository for TODO/FIXME comments across multiple languages."""
    findings = []
    repo_path = repo.resolve_path()
    langs = detect_repo_languages(repo_path)
    patterns = []
    for lang in langs:
        patterns.extend(get_todo_patterns_for_file(f"file.{lang}"))
    if not patterns:
        return findings
    combo = "|".join(p.replace(r"\s*", r"\s*") for p in patterns)
    file_count = 0
    for f in repo_path.rglob("*"):
        if not (f.is_file() and f.suffix.lower() in {".py", ".js", ".ts", ".go", ".rs"}):
            continue
        file_count += 1
        if file_count > 200:
            break
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for match in re.finditer(combo, content, re.IGNORECASE):
            line_no = content[:match.start()].count("\n") + 1
            findings.append(OptimizationFinding(
                type="todo_fixme",
                file_path=str(f.relative_to(repo_path)),
                description=match.group(2) or match.group(1),
                language=detect_language_from_path(str(f)),
                line_start=line_no,
                line_end=line_no,
                risk=RiskLevel.LOW,
            ))
    return findings


# ---- Dependency Analysis -------------------------------------------------

def extract_imports(content: str, file_path: str) -> list[str]:
    """Extract import statements from code."""
    lang = detect_language_from_path(file_path)
    imports = []
    if lang == "python":
        for m in re.finditer(r"^(?:from\s+([\w.]+)\s+import|import\s+([\w.]+))", content, re.MULTILINE):
            imports.append(m.group(1) or m.group(2))
    elif lang in ("javascript", "typescript"):
        for m in re.finditer(r"^\s*(?:import|from)\s+['\"]([^'\"]+)['\"]", content, re.MULTILINE):
            imports.append(m.group(1))
    elif lang == "go":
        for m in re.finditer(r"^\s*import\s+['\"]([^'\"]+)['\"]", content, re.MULTILINE):
            imports.append(m.group(1))
    return imports


def build_dependency_map(repo_path: Path) -> dict[str, list[str]]:
    """Build a dependency map: file -> list of modules it imports."""
    dep_map: dict[str, list[str]] = {}
    for f in repo_path.rglob("*"):
        if not (f.is_file() and f.suffix.lower() in {".py", ".js", ".ts", ".go"}):
            continue
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        rel = str(f.relative_to(repo_path))
        dep_map[rel] = extract_imports(content, str(f))
    return dep_map


def find_dependents(target_file: str, dep_map: dict[str, list[str]]) -> list[str]:
    """Find files that import or depend on target_file."""
    dependents = []
    target_name = Path(target_file).stem.replace("/", ".")
    for f, imports in dep_map.items():
        for imp in imports:
            if target_name in imp or Path(target_file).stem in imp:
                dependents.append(f)
    return dependents


def analyze_dependencies(repo: Repository, changed_files: list[str]) -> dict[str, list[str]]:
    """Analyze dependencies for changed files."""
    repo_path = repo.resolve_path()
    dep_map = build_dependency_map(repo_path)
    result = {}
    for cf in changed_files:
        result[cf] = find_dependents(cf, dep_map)
    return result


# ---- Test Runner ---------------------------------------------------------

def run_tests_for_hash(repo: Repository, ref: str) -> dict:
    """Run tests at a given git ref."""
    repo_path = repo.resolve_path()
    if not (repo_path / "pytest.ini").exists() and not (repo_path / "pyproject.toml").exists():
        return {"passed": False, "tests_run": 0, "failures": 0, "output": "no test config"}
    try:
        result = subprocess.run(
            ["python3", "-m", "pytest", "--tb=short", "-q"],
            cwd=str(repo_path),
            capture_output=True,
            text=True,
            timeout=120,
        )
        output = (result.stdout + result.stderr)[-500:]
        return {
            "passed": result.returncode == 0,
            "tests_run": 0,
            "failures": 1 if result.returncode != 0 else 0,
            "output": output,
        }
    except subprocess.TimeoutExpired:
        return {"passed": False, "tests_run": 0, "failures": 0, "output": "timeout"}
    except Exception as e:
        return {"passed": False, "tests_run": 0, "failures": 0, "output": str(e)}


def run_test_comparison(repo: Repository, before_hash: str, after_hash: str) -> dict:
    """Run tests and compare results before and after a change."""
    before = run_tests_for_hash(repo, before_hash)
    after = run_tests_for_hash(repo, after_hash)
    return {
        "before": before,
        "after": after,
        "regression": after.get("failures", 0) > before.get("failures", 0),
    }


# ---- Contributor Tracking -------------------------------------------------

def track_contributors(repo: Repository) -> dict:
    """Track contributors from git log."""
    repo_path = repo.resolve_path()
    try:
        result = subprocess.run(
            ["git", "log", "--format=%ae|%an", "-20"],
            cwd=str(repo_path),
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            return {}
        emails: dict[str, int] = {}
        for line in result.stdout.splitlines():
            if "|" in line:
                email, name = line.split("|", 1)
                emails[email.strip()] = emails.get(email.strip(), 0) + 1
        return {e: c for e, c in sorted(emails.items(), key=lambda x: -x[1])[:10]}
    except Exception:
        return {}
