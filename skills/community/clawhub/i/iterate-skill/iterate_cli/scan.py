"""Project scanner for onboarding.

Detects tech stack, directory structure, and key project features
to populate onboarding suggestions and the ITERATE.md knowledge base.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from iterate_cli.tui import tui

# Mapping from manifest file name to (language, package_manager).
MANIFEST_TO_LANG: dict[str, tuple[str, str]] = {
    "package.json": ("JavaScript/TypeScript", "npm"),
    "pyproject.toml": ("Python", "pip/poetry"),
    "setup.py": ("Python", "pip"),
    "requirements.txt": ("Python", "pip"),
    "Package.swift": ("Swift", "SwiftPM"),
    "go.mod": ("Go", "Go modules"),
    "Cargo.toml": ("Rust", "cargo"),
    "pom.xml": ("Java", "Maven"),
    "build.gradle": ("Java/Kotlin", "Gradle"),
    "build.gradle.kts": ("Kotlin", "Gradle"),
    "Gemfile": ("Ruby", "bundler"),
    "composer.json": ("PHP", "composer"),
    "mix.exs": ("Elixir", "mix"),
    "pubspec.yaml": ("Dart/Flutter", "pub"),
    "tsconfig.json": ("TypeScript", "npm"),
}

# Directories that indicate a frontend UI layer.
FRONTEND_DIR_INDICATORS: tuple[str, ...] = (
    "src/pages", "src/components", "src/views",
    "app/pages", "app/components",
    "components", "views", "pages",
)

# Directories to skip when building the top-level directory listing.
SKIP_DIRS: frozenset[str] = frozenset({
    ".git", "node_modules", "__pycache__", ".pytest_cache",
    ".mypy_cache", "venv", ".venv", "env", ".tox",
    "dist", "build", ".next", ".nuxt", "target",
    "coverage", "htmlcov", ".idea", ".vscode",
    "Pods", "DerivedData", ".build", ".cache",
})

# Spec directory candidates (checked relative to project root).
SPEC_DIR_CANDIDATES: tuple[str, ...] = ("specs", "spec", "docs/specs", "docs/spec")

# Test directory candidates. ``spec`` is deliberately NOT listed here: it is
# Ruby's test convention but also a *spec-documents* dir in other stacks, and
# listing it in both SPEC_DIR_CANDIDATES and TEST_DIR_CANDIDATES made a
# specs-only project report has_tests=True. Ruby projects are handled
# explicitly in _scan_features/_detect_test_dir.
TEST_DIR_CANDIDATES: tuple[str, ...] = ("tests", "test", "__tests__")

# CI config paths to check.
CI_PATHS: tuple[str, ...] = (
    ".github/workflows",
    ".gitlab-ci.yml",
    "Jenkinsfile",
    ".circleci",
    "azure-pipelines.yml",
)

# Directory names that indicate an API layer (used by suggest_dimensions).
API_LAYER_INDICATORS: frozenset[str] = frozenset({
    "api", "routes", "controllers", "handlers", "endpoints", "server",
})

# Nested API-layer paths. A standard ``src/api`` (or ``app/routes``) layout is
# invisible to a top-level-only check, so the scanner reported no API layer and
# never suggested the ``api``/``frontend-backend`` dimensions for exactly the
# layouts most projects use.
API_LAYER_PATHS: tuple[str, ...] = (
    "src/api", "src/routes", "src/controllers", "src/handlers",
    "app/api", "app/routes", "app/controllers", "app/handlers",
)


@dataclass
class ScanResult:
    """Result of scanning a project directory for onboarding."""

    manifests: list[str] = field(default_factory=list)
    top_level_dirs: list[str] = field(default_factory=list)
    detected_languages: list[str] = field(default_factory=list)
    detected_package_managers: list[str] = field(default_factory=list)
    has_specs: bool = False
    has_tests: bool = False
    has_ci: bool = False
    has_frontend: bool = False
    has_api: bool = False


def scan_project(project_root: Path) -> ScanResult:
    """Scan a project directory and return structured findings.

    This is a read-only operation. It never reads file contents — only
    checks existence and lists directories. It is safe to run on any project.

    Args:
        project_root: The project root directory to scan.

    Returns:
        ScanResult with detected manifests, languages, directories, and features.
    """
    result = ScanResult()

    _scan_manifests(project_root, result)
    _scan_top_level_dirs(project_root, result)
    _scan_features(project_root, result)

    return result


def _scan_manifests(project_root: Path, result: ScanResult) -> None:
    """Detect manifest files and derive languages / package managers."""
    from iterate_cli.fingerprint import MANIFEST_FILES

    for name in MANIFEST_FILES:
        if (project_root / name).is_file():
            result.manifests.append(name)
            mapping = MANIFEST_TO_LANG.get(name)
            if mapping is not None:
                lang, pm = mapping
                if lang not in result.detected_languages:
                    result.detected_languages.append(lang)
                if pm not in result.detected_package_managers:
                    result.detected_package_managers.append(pm)


def _scan_top_level_dirs(project_root: Path, result: ScanResult) -> None:
    """List top-level directories, skipping common non-source dirs."""
    try:
        for entry in sorted(project_root.iterdir(), key=lambda e: e.name):
            # A symlinked directory pointing outside the project (e.g.
            # `vendor -> /srv/shared`) is not part of the project and would
            # leak an out-of-tree name into ITERATE.md / scan --json. Count a
            # top-level entry as a source dir only when it is a REAL directory
            # (not a symlink): is_symlink() works on every supported Python
            # (is_dir(follow_symlinks=False) is 3.13+).
            if (
                entry.is_dir()
                and not entry.is_symlink()
                and entry.name not in SKIP_DIRS
                and not entry.name.startswith(".")
            ):
                result.top_level_dirs.append(entry.name)
    except OSError as exc:
        # 目录列表失败（如权限不足、目录在扫描过程中被删除、挂载点出错）
        # 不阻断扫描，但经 tui 记录到 stderr 以便排查（所有面向用户的输出
        # 都必须走 iterate_cli.tui，保持 --json 的 stdout 纯净）。
        tui.warning(f"scan: cannot list directories in {project_root}: {exc}")


def _scan_features(project_root: Path, result: ScanResult) -> None:
    """Detect specs, tests, CI, context files, and frontend indicators."""
    for candidate in SPEC_DIR_CANDIDATES:
        if (project_root / candidate).is_dir():
            result.has_specs = True
            break

    for candidate in TEST_DIR_CANDIDATES:
        if (project_root / candidate).is_dir():
            result.has_tests = True
            break
    # Ruby's test dir is ``spec/`` (kept out of TEST_DIR_CANDIDATES so it is not
    # misread as tests for other stacks).
    if (
        not result.has_tests
        and "Ruby" in result.detected_languages
        and (project_root / "spec").is_dir()
    ):
        result.has_tests = True

    for ci_path in CI_PATHS:
        if (project_root / ci_path).exists():
            result.has_ci = True
            break

    for indicator in FRONTEND_DIR_INDICATORS:
        if (project_root / indicator).is_dir():
            result.has_frontend = True
            break

    result.has_api = any(
        d in API_LAYER_INDICATORS for d in result.top_level_dirs
    )
    if not result.has_api:
        for indicator in API_LAYER_PATHS:
            if (project_root / indicator).is_dir():
                result.has_api = True
                break


def suggest_dimensions(scan: ScanResult) -> list[str]:
    """Suggest review dimensions based on scan results.

    Returns a list of dimension keys suitable for iterate.config.yaml.
    The caller should let the user confirm or adjust the selection.

    Args:
        scan: The ScanResult from scan_project().

    Returns:
        List of recommended dimension keys.
    """
    # Base dimensions always recommended.
    dims: list[str] = [
        "correctness",
        "security",
        "performance",
        "architecture",
        "style-tests",
        "tech-debt",
    ]

    if scan.has_specs:
        dims.append("spec-compliance")
    if scan.has_frontend:
        dims.append("frontend-backend")
        dims.append("ui-ux")
    elif _has_api_layer(scan):
        dims.append("frontend-backend")

    return dims


def _has_api_layer(scan: ScanResult) -> bool:
    """Heuristic: check if the project likely has an API layer.

    Considers both the dedicated flag (top-level AND nested paths such as
    ``src/api``) and the top-level listing, so a ``ScanResult`` built by hand
    (older callers/tests) keeps working.
    """
    return scan.has_api or any(
        d in API_LAYER_INDICATORS for d in scan.top_level_dirs
    )


def _detect_test_dir(scan: ScanResult) -> str:
    """Return the detected test directory, or ``""`` when none exists.

    ``tests/`` used to be the unconditional fallback, so a flat Python project
    (``app.py`` + ``test_app.py`` at the root) was told to run
    ``pytest tests/ -x -q`` and the very first validation failed with
    "file or directory not found". An empty string means "no explicit path":
    pytest then collects the project's default layout.
    """
    for candidate in TEST_DIR_CANDIDATES:
        if candidate in scan.top_level_dirs:
            return candidate
    # ``spec/`` is Ruby's test directory; for every other stack it is treated as
    # a spec-documents dir (see TEST_DIR_CANDIDATES), so only honour it for Ruby
    # — otherwise a specs-only project would be told to run `pytest spec`.
    if "spec" in scan.top_level_dirs and "Ruby" in scan.detected_languages:
        return "spec"
    return ""


def _detect_src_root(scan: ScanResult) -> str:
    """Return the path prefix for lint/type-check commands.

    A ``src/`` layout is common but far from universal — a flat project
    (``app.py`` at the repo root, or a package directory like ``mypkg/``)
    made the old hardcoded ``ruff check src/`` / ``mypy src/`` suggestions
    fail on the very first validation run with "path does not exist". Fall
    back to ``.`` (the project root) when no ``src`` directory was detected.
    """
    return "src/" if "src" in scan.top_level_dirs else "."


def suggest_validation_commands(scan: ScanResult) -> dict[str, list[str]]:
    """Suggest validation commands based on detected languages.

    Returns a dict mapping module keys to command lists, mirroring the
    ``validation.commands`` structure in iterate.config.yaml.
    These are starting points — the user must confirm they match the project.

    Args:
        scan: The ScanResult from scan_project().

    Returns:
        Dict of module → list of command strings.
    """
    commands: dict[str, list[str]] = {}

    # Java tooling spans up to three detected-language entries ("Java",
    # "Java/Kotlin", "Kotlin") that all map to the same "java" module; process
    # it once so a project with both pom.xml and build.gradle(.kts) does not
    # execute the branch twice and overwrite the build-tool choice.
    java_handled = False
    test_dir = _detect_test_dir(scan)
    src_root = _detect_src_root(scan)
    for lang in scan.detected_languages:
        if lang == "Python":
            commands["python"] = [
                f"ruff check {src_root}",
                f"mypy {src_root} --ignore-missing-imports",
                f"pytest {test_dir + ' ' if test_dir else ''}-x -q",
            ]
        elif lang in ("JavaScript/TypeScript", "TypeScript"):
            commands["typescript"] = [
                "npm run lint",
                "npm run build",
                "npm test",
            ]
        elif lang == "Swift":
            commands["swift"] = ["swift build -c debug"]
        elif lang == "Go":
            commands["go"] = ["go vet ./...", "go test ./..."]
        elif lang == "Rust":
            commands["rust"] = ["cargo clippy", "cargo test"]
        elif lang in ("Java", "Java/Kotlin", "Kotlin"):
            if java_handled:
                continue
            java_handled = True
            # Prefer Maven when pom.xml exists; otherwise Gradle (from either
            # build.gradle or build.gradle.kts). Decided once, so a project
            # with both manifests never has the Gradle suggestion overwritten
            # by the Maven one (or vice-versa).
            build_tool = "mvn" if "pom.xml" in scan.manifests else "gradle"
            commands["java"] = [f"{build_tool} compile", f"{build_tool} test"]
        elif lang == "Dart/Flutter":
            commands["dart"] = ["dart analyze", "dart test"]
        elif lang == "Elixir":
            commands["elixir"] = ["mix test", "mix format --check-formatted"]
        elif lang == "Ruby":
            commands["ruby"] = ["bundle exec rubocop", "bundle exec rspec"]

    return commands


def suggest_command_whitelist(scan: ScanResult) -> list[str]:
    """Suggest a command whitelist based on detected languages.

    Args:
        scan: The ScanResult from scan_project().

    Returns:
        List of command prefix strings.
    """
    base: list[str] = ["python", "python3"]
    for lang in scan.detected_languages:
        if lang == "Python":
            base.extend(["ruff", "mypy", "pytest"])
        elif lang in ("JavaScript/TypeScript", "TypeScript"):
            # ``npm test`` is not a prefix of ``npm run``; include the bare
            # ``npm`` prefix so both ``npm run X`` and ``npm test`` match.
            # ``npx`` is deliberately absent: it downloads and runs an
            # arbitrary package, so it must never be suggested into the
            # persistent command whitelist (matches personalize.py).
            base.extend(["npm", "npm run", "yarn", "pnpm"])
        elif lang == "Swift":
            base.append("swift")
        elif lang == "Go":
            # "go" (not "go test") so `go vet ./...` is covered as well:
            # _command_is_whitelisted only matches prefix + space, so the
            # narrower "go test" would leave "go vet ./..." un-whitelisted
            # and doctor would flag it.
            base.append("go")
        elif lang == "Rust":
            base.append("cargo")
        elif lang in ("Java", "Java/Kotlin", "Kotlin"):
            base.extend(["mvn", "gradle"])
        elif lang == "Dart/Flutter":
            base.append("dart")
        elif lang == "Elixir":
            base.append("mix")
        elif lang == "Ruby":
            base.append("bundle")
    # Deduplicate while preserving order.
    seen: set[str] = set()
    result: list[str] = []
    for item in base:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


# ---------------------------------------------------------------------------
# ``iterate scan`` — read-only export of the scanner's view
# ---------------------------------------------------------------------------

#: Feature flags rendered on the one-line summary, in display order. Keys mirror
#: the ``ScanResult`` attribute names exactly so the JSON report and the TUI
#: line can never disagree about which flag is which.
_SCAN_FEATURE_KEYS: tuple[tuple[str, str], ...] = (
    ("has_tests", "tests"),
    ("has_ci", "ci"),
    ("has_specs", "specs"),
    ("has_frontend", "frontend"),
    ("has_api", "api"),
)


def collect_scan_data(project_root: Path) -> dict[str, Any]:
    """Collect the report behind ``iterate scan``.

    This is the read-only export of :func:`scan_project` plus the suggestions
    derived from it. Before this existed the scan result was reachable only by
    walking the interactive wizard, so a user (or CI job) could make the tool
    scan a project but had no way to read the result back out.

    Args:
        project_root: Project root directory (must exist; the CLI validates it).

    Returns:
        A JSON-serialisable dict. The four ``has_*`` keys keep the
        ``ScanResult`` field names verbatim, and the suggestion keys mirror the
        corresponding ``suggest_*`` function names.
    """
    from iterate_cli.dimension_sets import suggest_dimension_sets

    result = scan_project(project_root)
    return {
        "project": str(project_root),
        "manifests": list(result.manifests),
        "top_level_dirs": list(result.top_level_dirs),
        "detected_languages": list(result.detected_languages),
        "detected_package_managers": list(result.detected_package_managers),
        "has_specs": result.has_specs,
        "has_tests": result.has_tests,
        "has_ci": result.has_ci,
        "has_frontend": result.has_frontend,
        "has_api": result.has_api,
        "suggested_dimensions": suggest_dimensions(result),
        "suggested_dimension_sets": suggest_dimension_sets(result),
        "suggested_validation_commands": {
            module: list(commands)
            for module, commands in suggest_validation_commands(result).items()
        },
        "suggested_command_whitelist": suggest_command_whitelist(result),
    }


def _join_or_none(values: list[str]) -> str:
    """Render a list for a key/value row, or an explicit empty marker.

    ``", ".join([])`` produced a blank right-hand side that reads like a
    rendering bug rather than "nothing was found", so the empty case gets its
    own string instead of an empty one.
    """
    return ", ".join(values) if values else "— (none detected)"


def render_scan(data: dict[str, Any], json_output: bool = False) -> int:
    """Render an ``iterate scan`` report.

    Read-only and non-gating: the scan only asserts what files exist, so a
    project that matches nothing recognisable is a normal outcome, not a
    failure. This always returns 0 so a CI caller can use the command purely
    for its ``--json`` payload without special-casing the exit code.

    Args:
        data: Structured dict from :func:`collect_scan_data`.
        json_output: When True, emit exactly one JSON document instead of TUI
            output.

    Returns:
        Always 0.
    """
    if json_output:
        print(json.dumps(data, ensure_ascii=False, indent=2, default=str))
        return 0

    tui.intro("Iterate Skill — Scan")

    manifests = [str(m) for m in data.get("manifests", [])]
    languages = [str(lang) for lang in data.get("detected_languages", [])]
    managers = [str(pm) for pm in data.get("detected_package_managers", [])]
    dirs = [str(d) for d in data.get("top_level_dirs", [])]

    tui.key_value("Project", str(data.get("project", "")))
    tui.key_value("Manifests", _join_or_none(manifests))
    tui.key_value("Languages", _join_or_none(languages))
    tui.key_value("Package managers", _join_or_none(managers))
    tui.key_value("Top-level dirs", _join_or_none(dirs))

    features = "  ".join(
        f"{label} {'✓' if data.get(key) else '✗'}"
        for key, label in _SCAN_FEATURE_KEYS
    )
    tui.key_value("Features", features)

    dimensions = [str(d) for d in data.get("suggested_dimensions", [])]
    tui.section("Suggested dimensions / 建议维度")
    if dimensions:
        for name in dimensions:
            tui.bullet(name)
    else:
        tui.hint("(none — no language was detected)", indent=4)

    sets = data.get("suggested_dimension_sets") or {}
    tui.section("Suggested scope sets / 建议范围维度集")
    if sets:
        for name in sorted(sets):
            dims = sets[name].get("dimensions", [])
            tui.bullet(f"{name}: {', '.join(str(d) for d in dims)}")
    else:
        tui.hint("(none suggested)", indent=4)

    commands = data.get("suggested_validation_commands") or {}
    tui.section("Suggested validation commands / 建议校验命令")
    if commands:
        for module in sorted(commands):
            for command in commands[module]:
                tui.bullet(f"{module}: {command}")
    else:
        tui.hint("(none — no language was detected)", indent=4)

    tui.empty_line()
    if not manifests and not languages:
        # The only genuinely surprising outcome: nothing recognisable at all.
        # Say so and point at the escape hatch instead of leaving the user to
        # wonder whether the scan silently failed. Split across two lines
        # because a single line would exceed 80 columns and, once the terminal
        # wrapped it, the continuation would lose its left margin.
        tui.warning("No recognised tech-stack manifest found.")
        tui.hint(
            "`iterate onboard` will ask for the stack instead of suggesting one.",
            indent=4,
        )
    # Kept short on purpose: `tui.hint` indents only the first line, so a
    # message that overflows the terminal width continues at column 0 and
    # reads as if it belonged to the block above.
    tui.hint("Read-only: nothing was written.")
    tui.hint(
        "Apply with `iterate init --yes`, `iterate onboard`, or "
        "`iterate config set <key> <value>`."
    )
    tui.hint("Machine-readable: `iterate scan --json`")
    return 0
