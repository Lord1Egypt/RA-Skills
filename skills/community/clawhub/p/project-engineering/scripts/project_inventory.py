#!/usr/bin/env python3
"""生成跨技术栈的软件仓库只读画像，不执行项目代码或构建插件。"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import stat
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10 及更早版本仍可完成基础扫描。
    tomllib = None


SCHEMA_VERSION = 1
MAX_MANIFEST_BYTES = 1024 * 1024
DEFAULT_MAX_FILES = 100_000
DEFAULT_MAX_DEPTH = 24
IGNORED_DIRECTORIES = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    ".venv",
    "venv",
    "node_modules",
    "vendor",
    "target",
    "build",
    "dist",
    "out",
    "coverage",
    ".next",
    ".nuxt",
    ".turbo",
    ".gradle",
    ".mypy_cache",
    ".pytest_cache",
    "__pycache__",
}
LANGUAGES = {
    ".java": "Java",
    ".kt": "Kotlin",
    ".kts": "Kotlin",
    ".scala": "Scala",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".mjs": "JavaScript",
    ".cjs": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".py": "Python",
    ".go": "Go",
    ".rs": "Rust",
    ".cs": "C#",
    ".fs": "F#",
    ".vb": "Visual Basic",
    ".c": "C",
    ".h": "C/C++ Header",
    ".cc": "C++",
    ".cpp": "C++",
    ".cxx": "C++",
    ".hpp": "C/C++ Header",
    ".rb": "Ruby",
    ".php": "PHP",
    ".swift": "Swift",
    ".dart": "Dart",
    ".sh": "Shell",
    ".bash": "Shell",
    ".zsh": "Shell",
    ".ps1": "PowerShell",
    ".sql": "SQL",
    ".html": "HTML",
    ".htm": "HTML",
    ".css": "CSS",
    ".scss": "CSS",
    ".vue": "Vue",
    ".svelte": "Svelte",
}
INSTRUCTION_NAMES = {
    "agents.md": "agent-instructions",
    "claude.md": "agent-instructions",
    "gemini.md": "agent-instructions",
    ".cursorrules": "agent-instructions",
    ".windsurfrules": "agent-instructions",
    "contributing.md": "contributing",
    "development.md": "development",
    "architecture.md": "architecture",
    "security.md": "security",
    "codeowners": "ownership",
    ".editorconfig": "editor-config",
}


def configure_output() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def run_git(root: Path, arguments: list[str]) -> tuple[int, bytes]:
    environment = os.environ.copy()
    environment["GIT_OPTIONAL_LOCKS"] = "0"
    try:
        completed = subprocess.run(
            ["git", "--no-pager", "-c", "core.fsmonitor=false", "-C", str(root), *arguments],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
            env=environment,
        )
    except FileNotFoundError:
        return 127, b""
    return completed.returncode, completed.stdout


def decode(value: bytes) -> str:
    return value.decode("utf-8", errors="replace").strip()


def resolve_root(start: Path) -> tuple[Path, bool]:
    if not start.exists():
        raise ValueError(f"路径不存在：{start}")
    candidate = start if start.is_dir() else start.parent
    code, output = run_git(candidate, ["rev-parse", "--show-toplevel"])
    if code == 0 and output:
        return Path(decode(output)).resolve(), True
    return candidate.resolve(), False


def is_link_or_reparse(path: Path) -> bool:
    try:
        if path.is_symlink():
            return True
        attributes = getattr(path.stat(follow_symlinks=False), "st_file_attributes", 0)
        return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))
    except OSError:
        return True


def safe_relative(root: Path, raw_path: str) -> str | None:
    normalized = raw_path.replace("\\", "/").strip("/")
    if not normalized or "\x00" in normalized:
        return None
    parts = Path(normalized).parts
    if Path(normalized).is_absolute() or ".." in parts:
        return None
    if any(part.lower() in IGNORED_DIRECTORIES for part in parts[:-1]):
        return None
    candidate = root.joinpath(*parts)
    try:
        candidate.resolve().relative_to(root.resolve())
    except (OSError, ValueError):
        return None
    return Path(*parts).as_posix()


def build_file_index(
    root: Path,
    git_available: bool,
    max_files: int,
    max_depth: int,
) -> tuple[list[str], bool, str]:
    files: list[str] = []
    truncated = False
    source = "filesystem"

    if git_available:
        code, output = run_git(root, ["ls-files", "-z", "--cached", "--others", "--exclude-standard"])
        if code == 0:
            source = "git-index"
            for raw in output.split(b"\0"):
                if not raw:
                    continue
                relative = safe_relative(root, raw.decode("utf-8", errors="replace"))
                if relative is None or len(Path(relative).parts) > max_depth:
                    continue
                path = root / relative
                if is_link_or_reparse(path):
                    continue
                files.append(relative)
                if len(files) >= max_files:
                    truncated = True
                    break
            return sorted(set(files)), truncated, source

    for current, directories, names in os.walk(root, followlinks=False):
        current_path = Path(current)
        try:
            depth = len(current_path.relative_to(root).parts)
        except ValueError:
            continue
        directories[:] = [
            name
            for name in directories
            if name.lower() not in IGNORED_DIRECTORIES
            and depth < max_depth
            and not is_link_or_reparse(current_path / name)
        ]
        for name in names:
            path = current_path / name
            if is_link_or_reparse(path):
                continue
            relative = safe_relative(root, path.relative_to(root).as_posix())
            if relative:
                files.append(relative)
            if len(files) >= max_files:
                truncated = True
                return sorted(set(files)), truncated, source
    return sorted(set(files)), truncated, source


def add_warning(warnings: list[dict[str, str]], code: str, path: str, message: str) -> None:
    warning = {"code": code, "path": path, "message": message}
    if warning not in warnings:
        warnings.append(warning)


def read_manifest(root: Path, relative: str, warnings: list[dict[str, str]]) -> bytes | None:
    path = root / relative
    try:
        resolved = path.resolve(strict=True)
        resolved.relative_to(root.resolve())
        if is_link_or_reparse(path) or not resolved.is_file():
            add_warning(warnings, "unsafe-manifest-path", relative, "清单是链接、重解析点或非常规文件")
            return None
        size = resolved.stat().st_size
        if size > MAX_MANIFEST_BYTES:
            add_warning(warnings, "manifest-too-large", relative, "清单超过 1 MiB，未解析")
            return None
        return resolved.read_bytes()
    except (OSError, ValueError):
        add_warning(warnings, "manifest-read-failed", relative, "清单无法安全读取")
        return None


def safe_members(root: Path, base: Path, declarations: list[str]) -> list[str]:
    members: set[str] = set()
    root_resolved = root.resolve()
    for declaration in declarations:
        value = declaration.strip().replace(":", "/").strip("/")
        if (
            not value
            or "${" in value
            or "://" in value
            or any(ord(character) < 32 for character in value)
            or Path(value).is_absolute()
        ):
            continue
        patterns = [value]
        if any(character in value for character in "*?["):
            try:
                patterns = [path.relative_to(base).as_posix() for path in base.glob(value)]
            except (OSError, ValueError):
                continue
        for pattern in patterns:
            candidate = (base / pattern).resolve()
            try:
                candidate.relative_to(root_resolved)
            except ValueError:
                continue
            if candidate.is_dir() and not is_link_or_reparse(candidate):
                members.add(candidate.relative_to(root_resolved).as_posix())
    return sorted(members)


def manifest_paths(files: list[str], names: set[str]) -> list[str]:
    lowered = {name.lower() for name in names}
    return [path for path in files if Path(path).name.lower() in lowered]


def detect_maven(root: Path, files: list[str], warnings: list[dict[str, str]]) -> dict[str, Any] | None:
    manifests = manifest_paths(files, {"pom.xml"})
    wrappers = manifest_paths(files, {"mvnw", "mvnw.cmd"})
    if not manifests:
        return None
    members: set[str] = set()
    for relative in manifests[:50]:
        content = read_manifest(root, relative, warnings)
        if content is None:
            continue
        if b"<!DOCTYPE" in content.upper() or b"<!ENTITY" in content.upper():
            add_warning(warnings, "unsafe-xml", relative, "XML 含 DTD/ENTITY，未解析")
            continue
        try:
            document = ET.fromstring(content)
            namespace_match = re.match(r"\{([^}]+)\}", document.tag)
            prefix = f"{{{namespace_match.group(1)}}}" if namespace_match else ""
            declarations = [
                node.text.strip()
                for node in document.findall(f"{prefix}modules/{prefix}module")
                if node.text and node.text.strip()
            ]
            members.update(safe_members(root, (root / relative).parent, declarations))
        except ET.ParseError:
            add_warning(warnings, "manifest-parse-failed", relative, "Maven XML 无法解析")
    return {"name": "maven", "manifests": manifests, "wrappers": wrappers, "members": sorted(members)}


def quoted_literals(text: str) -> list[str]:
    return [match[1] for match in re.findall(r"(['\"])(.*?)\1", text)]


def detect_gradle(root: Path, files: list[str], warnings: list[dict[str, str]]) -> dict[str, Any] | None:
    settings = manifest_paths(files, {"settings.gradle", "settings.gradle.kts"})
    builds = manifest_paths(files, {"build.gradle", "build.gradle.kts"})
    wrappers = manifest_paths(files, {"gradlew", "gradlew.bat"})
    if not settings and not builds:
        return None
    members: set[str] = set()
    for relative in settings[:20]:
        content = read_manifest(root, relative, warnings)
        if content is None:
            continue
        text = content.decode("utf-8", errors="replace")
        declarations: list[str] = []
        for line in text.splitlines():
            stripped = line.strip()
            if re.match(r"^(include|includeBuild)\b", stripped):
                declarations.extend(quoted_literals(stripped))
        members.update(safe_members(root, (root / relative).parent, declarations))
    return {
        "name": "gradle",
        "manifests": sorted(set(settings + builds)),
        "wrappers": wrappers,
        "members": sorted(members),
    }


def detect_node(root: Path, files: list[str], warnings: list[dict[str, str]]) -> dict[str, Any] | None:
    manifests = manifest_paths(files, {"package.json"})
    lockfiles = manifest_paths(
        files,
        {"package-lock.json", "npm-shrinkwrap.json", "pnpm-lock.yaml", "yarn.lock", "bun.lock", "bun.lockb"},
    )
    workspace_files = manifest_paths(files, {"pnpm-workspace.yaml"})
    if not manifests:
        return None
    members: set[str] = set()
    for relative in manifests[:100]:
        content = read_manifest(root, relative, warnings)
        if content is None:
            continue
        try:
            document = json.loads(content)
        except (json.JSONDecodeError, UnicodeDecodeError):
            add_warning(warnings, "manifest-parse-failed", relative, "package.json 无法解析")
            continue
        workspaces = document.get("workspaces") if isinstance(document, dict) else None
        declarations: list[str] = []
        if isinstance(workspaces, list):
            declarations = [value for value in workspaces if isinstance(value, str)]
        elif isinstance(workspaces, dict) and isinstance(workspaces.get("packages"), list):
            declarations = [value for value in workspaces["packages"] if isinstance(value, str)]
        members.update(safe_members(root, (root / relative).parent, declarations))
    return {
        "name": "node",
        "manifests": manifests,
        "lockfiles": lockfiles,
        "workspaceFiles": workspace_files,
        "members": sorted(members),
    }


def detect_python(root: Path, files: list[str], warnings: list[dict[str, str]]) -> dict[str, Any] | None:
    manifests = manifest_paths(files, {"pyproject.toml", "setup.cfg", "setup.py"})
    lockfiles = manifest_paths(files, {"uv.lock", "poetry.lock", "pdm.lock", "requirements.txt"})
    if not manifests and not lockfiles:
        return None
    members: set[str] = set()
    if tomllib is not None:
        for relative in [path for path in manifests if Path(path).name.lower() == "pyproject.toml"][:50]:
            content = read_manifest(root, relative, warnings)
            if content is None:
                continue
            try:
                document = tomllib.loads(content.decode("utf-8"))
                declarations = document.get("tool", {}).get("uv", {}).get("workspace", {}).get("members", [])
                if isinstance(declarations, list):
                    members.update(
                        safe_members(
                            root,
                            (root / relative).parent,
                            [value for value in declarations if isinstance(value, str)],
                        )
                    )
            except (UnicodeDecodeError, tomllib.TOMLDecodeError):
                add_warning(warnings, "manifest-parse-failed", relative, "pyproject.toml 无法解析")
    return {"name": "python", "manifests": manifests, "lockfiles": lockfiles, "members": sorted(members)}


def detect_go(root: Path, files: list[str], warnings: list[dict[str, str]]) -> dict[str, Any] | None:
    modules = manifest_paths(files, {"go.mod"})
    workspaces = manifest_paths(files, {"go.work"})
    if not modules and not workspaces:
        return None
    members: set[str] = set()
    for relative in workspaces[:20]:
        content = read_manifest(root, relative, warnings)
        if content is None:
            continue
        text = content.decode("utf-8", errors="replace")
        declarations: list[str] = []
        inside_use = False
        for raw_line in text.splitlines():
            line = raw_line.split("//", 1)[0].strip()
            if line.startswith("use ("):
                inside_use = True
                continue
            if inside_use and line == ")":
                inside_use = False
                continue
            if inside_use and line:
                declarations.append(line.strip('"'))
            elif line.startswith("use "):
                declarations.append(line[4:].strip().strip('"'))
        members.update(safe_members(root, (root / relative).parent, declarations))
    return {"name": "go", "manifests": modules, "workspaceFiles": workspaces, "members": sorted(members)}


def detect_rust(root: Path, files: list[str], warnings: list[dict[str, str]]) -> dict[str, Any] | None:
    manifests = manifest_paths(files, {"cargo.toml"})
    lockfiles = manifest_paths(files, {"cargo.lock"})
    if not manifests:
        return None
    members: set[str] = set()
    if tomllib is not None:
        for relative in manifests[:50]:
            content = read_manifest(root, relative, warnings)
            if content is None:
                continue
            try:
                document = tomllib.loads(content.decode("utf-8"))
                declarations = document.get("workspace", {}).get("members", [])
                if isinstance(declarations, list):
                    members.update(
                        safe_members(
                            root,
                            (root / relative).parent,
                            [value for value in declarations if isinstance(value, str)],
                        )
                    )
            except (UnicodeDecodeError, tomllib.TOMLDecodeError):
                add_warning(warnings, "manifest-parse-failed", relative, "Cargo.toml 无法解析")
    return {"name": "rust", "manifests": manifests, "lockfiles": lockfiles, "members": sorted(members)}


def detect_dotnet(files: list[str]) -> dict[str, Any] | None:
    solutions = [path for path in files if Path(path).suffix.lower() in {".sln", ".slnx"}]
    projects = [path for path in files if Path(path).suffix.lower() in {".csproj", ".fsproj", ".vbproj"}]
    if not solutions and not projects:
        return None
    members = sorted({str(Path(path).parent.as_posix()) for path in projects})
    return {"name": "dotnet", "manifests": sorted(solutions + projects), "members": members}


def detect_other_builds(files: list[str]) -> list[dict[str, Any]]:
    definitions = {
        "make": {"makefile", "gnumakefile"},
        "cmake": {"cmakelists.txt"},
        "bazel": {"module.bazel", "workspace", "workspace.bazel"},
        "ruby": {"gemfile"},
        "php": {"composer.json"},
    }
    detected = []
    for name, filenames in definitions.items():
        manifests = manifest_paths(files, filenames)
        if manifests:
            detected.append({"name": name, "manifests": manifests, "members": []})
    return detected


def detect_ecosystems(root: Path, files: list[str], warnings: list[dict[str, str]]) -> list[dict[str, Any]]:
    candidates = [
        detect_maven(root, files, warnings),
        detect_gradle(root, files, warnings),
        detect_node(root, files, warnings),
        detect_python(root, files, warnings),
        detect_go(root, files, warnings),
        detect_rust(root, files, warnings),
        detect_dotnet(files),
    ]
    return [candidate for candidate in candidates if candidate is not None] + detect_other_builds(files)


def detect_instructions(files: list[str]) -> list[dict[str, str]]:
    results = []
    for relative in files:
        lowered = relative.lower()
        name = Path(relative).name.lower()
        kind = INSTRUCTION_NAMES.get(name)
        if lowered == ".github/copilot-instructions.md" or fnmatch.fnmatch(
            lowered, ".github/instructions/*.instructions.md"
        ):
            kind = "agent-instructions"
        elif lowered.startswith(".cursor/rules/"):
            kind = "agent-instructions"
        if kind:
            results.append({"kind": kind, "path": relative})
    return results


def detect_languages(files: list[str]) -> list[dict[str, Any]]:
    counts = Counter(LANGUAGES[Path(path).suffix.lower()] for path in files if Path(path).suffix.lower() in LANGUAGES)
    total = sum(counts.values())
    if total == 0:
        return []
    return [
        {"name": name, "files": count, "percent": round(count * 100 / total, 1)}
        for name, count in counts.most_common(8)
    ]


def common_roots(paths: list[str], marker_names: set[str]) -> list[str]:
    roots: set[str] = set()
    for relative in paths:
        parts = Path(relative).parts
        lowered = [part.lower() for part in parts]
        for index, part in enumerate(lowered[:-1]):
            if part in marker_names:
                roots.add(Path(*parts[: index + 1]).as_posix())
                break
    return sorted(roots)


def detect_test_signals(files: list[str]) -> dict[str, Any]:
    configs = {
        "pytest.ini",
        "tox.ini",
        "noxfile.py",
        "jest.config.js",
        "jest.config.ts",
        "vitest.config.js",
        "vitest.config.ts",
        "playwright.config.js",
        "playwright.config.ts",
    }
    test_files = []
    for relative in files:
        lowered = relative.lower()
        name = Path(relative).name.lower()
        suffixes = Path(relative).suffixes
        if (
            "/src/test/" in f"/{lowered}/"
            or "/tests/" in f"/{lowered}/"
            or "/test/" in f"/{lowered}/"
            or "/__tests__/" in f"/{lowered}/"
            or name.startswith("test_") and name.endswith(".py")
            or name.endswith("_test.py")
            or name.endswith("_test.go")
            or any(marker in lowered for marker in (".spec.", ".test."))
            or name.endswith("tests.csproj")
            or suffixes[-2:] in [[".spec", ".ts"], [".test", ".ts"]]
        ):
            test_files.append(relative)
    return {
        "files": len(set(test_files)),
        "roots": common_roots(test_files, {"test", "tests", "__tests__"}),
        "configs": manifest_paths(files, configs),
    }


def paths_matching(files: list[str], patterns: list[str]) -> list[str]:
    results = []
    for relative in files:
        lowered = relative.lower()
        if any(fnmatch.fnmatch(lowered, pattern) for pattern in patterns):
            results.append(relative)
    return sorted(set(results))


def detect_signals(files: list[str]) -> dict[str, Any]:
    return {
        "tests": detect_test_signals(files),
        "ci": paths_matching(
            files,
            [
                ".github/workflows/*.yml",
                ".github/workflows/*.yaml",
                ".gitlab-ci.yml",
                "jenkinsfile",
                "azure-pipelines.yml",
                ".circleci/config.yml",
                ".buildkite/pipeline.yml",
                "bitbucket-pipelines.yml",
                ".teamcity/*",
            ],
        ),
        "containers": paths_matching(
            files,
            [
                "dockerfile",
                "**/dockerfile",
                "dockerfile.*",
                "**/dockerfile.*",
                "docker-compose*.yml",
                "docker-compose*.yaml",
                "compose*.yml",
                "compose*.yaml",
                ".devcontainer/*",
                "**/helm/**",
                "**/charts/**",
                "**/k8s/**",
                "**/kubernetes/**",
                "**/kustomization.yaml",
            ],
        ),
        "migrations": paths_matching(
            files,
            [
                "**/db/migration/*.sql",
                "**/db/migrate/*",
                "**/migrations/*.sql",
                "**/migrations/*.py",
                "**/migrations/*.ts",
                "**/migrations/*.js",
                "**/alembic/**",
                "**/prisma/migrations/**",
                "**/liquibase/**",
                "docs/db/*.sql",
                "database/migrations/**",
            ],
        ),
        "documentation": paths_matching(
            files,
            ["readme", "readme.*", "docs/readme*", "**/adr/*.md", "**/adrs/*.md", "**/architecture*.md"],
        ),
    }


def git_status_summary(root: Path, available: bool) -> dict[str, Any]:
    if not available:
        return {"available": False}
    branch_code, branch_output = run_git(root, ["symbolic-ref", "--quiet", "--short", "HEAD"])
    _, head_output = run_git(root, ["rev-parse", "--short=12", "HEAD"])
    upstream_code, upstream_output = run_git(
        root, ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"]
    )
    upstream = decode(upstream_output) if upstream_code == 0 else None
    ahead = behind = None
    if upstream:
        count_code, count_output = run_git(root, ["rev-list", "--left-right", "--count", f"HEAD...{upstream}"])
        if count_code == 0:
            parts = decode(count_output).split()
            if len(parts) == 2 and all(part.isdigit() for part in parts):
                ahead, behind = int(parts[0]), int(parts[1])

    status_code, status_output = run_git(
        root,
        ["status", "--porcelain=v2", "-z", "--untracked-files=all", "--ignore-submodules=all"],
    )
    changes = {"staged": 0, "unstaged": 0, "untracked": 0, "conflicted": 0}
    if status_code == 0:
        records = status_output.split(b"\0")
        index = 0
        while index < len(records):
            record = records[index]
            if not record:
                index += 1
                continue
            prefix = record[:2]
            if prefix == b"? ":
                changes["untracked"] += 1
            elif prefix == b"u ":
                changes["conflicted"] += 1
            elif prefix in {b"1 ", b"2 "}:
                fields = record.split(b" ", 2)
                xy = fields[1] if len(fields) > 1 else b".."
                if len(xy) == 2:
                    if xy[0:1] != b".":
                        changes["staged"] += 1
                    if xy[1:2] != b".":
                        changes["unstaged"] += 1
                if prefix == b"2 ":
                    index += 1  # rename/copy 的下一个 NUL 字段是原路径，不是状态记录。
            index += 1
    return {
        "available": True,
        "branch": decode(branch_output) if branch_code == 0 else None,
        "detached": branch_code != 0,
        "head": decode(head_output) or None,
        "upstream": upstream,
        "ahead": ahead,
        "behind": behind,
        "clean": not any(changes.values()),
        "changes": changes,
    }


def classify_sensitive_name(relative: str) -> str | None:
    name = Path(relative).name.lower()
    if name.startswith(".env") and not any(marker in name for marker in ("example", "sample", "template")):
        return "environment-file"
    if Path(name).suffix in {".pem", ".key", ".p12", ".pfx", ".jks", ".keystore"}:
        return "key-or-keystore"
    if name in {"id_rsa", "id_ed25519", "credentials", "credentials.json", ".npmrc", ".pypirc"}:
        return "credential-file"
    return None


def tracked_sensitive_summary(root: Path, git_available: bool) -> dict[str, Any]:
    if not git_available:
        return {"available": False, "total": 0, "categories": {}}
    code, output = run_git(root, ["ls-files", "-z", "--cached"])
    if code != 0:
        return {"available": False, "total": 0, "categories": {}}
    categories = Counter()
    for raw in output.split(b"\0"):
        if not raw:
            continue
        category = classify_sensitive_name(raw.decode("utf-8", errors="replace"))
        if category:
            categories[category] += 1
    return {"available": True, "total": sum(categories.values()), "categories": dict(sorted(categories.items()))}


def infer_shape(ecosystems: list[dict[str, Any]]) -> list[str]:
    shape = []
    member_count = len({member for ecosystem in ecosystems for member in ecosystem.get("members", [])})
    if member_count > 1:
        shape.append("multi-module")
    else:
        shape.append("single-project")
    ecosystem_families = {
        {
            "maven": "jvm",
            "gradle": "jvm",
            "node": "node",
            "python": "python",
            "go": "go",
            "rust": "rust",
            "dotnet": "dotnet",
            "ruby": "ruby",
            "php": "php",
        }.get(ecosystem["name"])
        for ecosystem in ecosystems
    }
    ecosystem_families.discard(None)
    if len(ecosystem_families) > 1:
        shape.append("polyglot")
        shape.append("monorepo-candidate")
    return shape


def trim_paths(value: Any, limit: int) -> Any:
    if isinstance(value, list):
        if len(value) <= limit:
            return [trim_paths(item, limit) for item in value]
        return [trim_paths(item, limit) for item in value[:limit]] + [f"... {len(value) - limit} more"]
    if isinstance(value, dict):
        return {key: trim_paths(item, limit) for key, item in value.items()}
    return value


def build_inventory(args: argparse.Namespace) -> dict[str, Any]:
    root, git_available = resolve_root(args.repo.resolve())
    files, truncated, source = build_file_index(root, git_available, args.max_files, args.max_depth)
    warnings: list[dict[str, str]] = []
    if truncated:
        add_warning(warnings, "scan-truncated", "", "文件索引达到扫描上限，结果不完整")
    ecosystems = detect_ecosystems(root, files, warnings)
    return {
        "schemaVersion": SCHEMA_VERSION,
        "repository": {
            "root": root.as_posix(),
            "shape": infer_shape(ecosystems),
            "git": git_status_summary(root, git_available),
        },
        "instructions": detect_instructions(files),
        "ecosystems": ecosystems,
        "languages": detect_languages(files),
        "signals": detect_signals(files),
        "trackedSensitiveLookingNames": tracked_sensitive_summary(root, git_available),
        "scan": {"source": source, "files": len(files), "truncated": truncated},
        "warnings": warnings,
    }


def render_text(inventory: dict[str, Any], max_items: int) -> str:
    view = trim_paths(inventory, max_items)
    repository = view["repository"]
    git = repository["git"]
    lines = [
        "PROJECT ENGINEERING INVENTORY",
        f"root: {repository['root']}",
        f"shape: {', '.join(repository['shape'])}",
        f"scan: {view['scan']['source']}, files={view['scan']['files']}, truncated={view['scan']['truncated']}",
    ]
    if git.get("available"):
        changes = git["changes"]
        lines.append(
            "git: "
            f"branch={git.get('branch') or '(detached)'}, head={git.get('head')}, "
            f"upstream={git.get('upstream') or '(none)'}, ahead={git.get('ahead')}, behind={git.get('behind')}, "
            f"staged={changes['staged']}, unstaged={changes['unstaged']}, "
            f"untracked={changes['untracked']}, conflicted={changes['conflicted']}"
        )
    else:
        lines.append("git: unavailable")

    lines.append("instructions:")
    for item in view["instructions"]:
        lines.append(f"  {item['kind']}: {item['path']}")
    if not view["instructions"]:
        lines.append("  (none detected)")

    lines.append("ecosystems:")
    for ecosystem in view["ecosystems"]:
        lines.append(
            f"  {ecosystem['name']}: manifests={len(ecosystem.get('manifests', []))}, "
            f"members={len(ecosystem.get('members', []))}"
        )
        if ecosystem.get("members"):
            lines.append("    members: " + ", ".join(ecosystem["members"]))
    if not view["ecosystems"]:
        lines.append("  (none detected)")

    lines.append("languages (estimated by source-file count):")
    for language in view["languages"]:
        lines.append(f"  {language['name']}: {language['files']} ({language['percent']}%)")
    if not view["languages"]:
        lines.append("  (none detected)")

    signals = view["signals"]
    lines.append(
        "signals: "
        f"tests={signals['tests']['files']}, ci={len(signals['ci'])}, "
        f"containers={len(signals['containers'])}, migrations={len(signals['migrations'])}, "
        f"docs={len(signals['documentation'])}"
    )
    sensitive = view["trackedSensitiveLookingNames"]
    lines.append(
        "tracked-sensitive-looking-names (filename-only): "
        f"total={sensitive['total']}, categories={json.dumps(sensitive['categories'], ensure_ascii=False)}"
    )
    lines.append("warnings:")
    for warning in view["warnings"]:
        location = f" [{warning['path']}]" if warning["path"] else ""
        lines.append(f"  {warning['code']}{location}: {warning['message']}")
    if not view["warnings"]:
        lines.append("  (none)")
    return "\n".join(lines)


def main() -> int:
    configure_output()
    parser = argparse.ArgumentParser(description="生成通用软件仓库的只读工程画像")
    parser.add_argument("--repo", type=Path, default=Path.cwd(), help="仓库或项目内任意路径")
    parser.add_argument("--format", choices=("text", "json"), default="text", help="输出格式")
    parser.add_argument("--strict", action="store_true", help="扫描截断或清单解析告警时返回 1")
    parser.add_argument("--max-files", type=int, default=DEFAULT_MAX_FILES, help="最多索引的文件数")
    parser.add_argument("--max-depth", type=int, default=DEFAULT_MAX_DEPTH, help="非 Git 项目的最大扫描深度")
    parser.add_argument("--max-items", type=int, default=40, help="文本模式每类最多展示的条目数")
    args = parser.parse_args()
    if args.max_files <= 0 or args.max_depth <= 0 or args.max_items <= 0:
        parser.error("扫描上限必须是正整数")

    try:
        inventory = build_inventory(args)
    except ValueError as exception:
        print(f"ERROR: {exception}", file=sys.stderr)
        return 2

    if args.format == "json":
        print(json.dumps(inventory, ensure_ascii=False, indent=2))
    else:
        print(render_text(inventory, args.max_items))
    return 1 if args.strict and (inventory["scan"]["truncated"] or inventory["warnings"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
