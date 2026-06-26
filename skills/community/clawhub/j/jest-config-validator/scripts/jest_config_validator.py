#!/usr/bin/env python3
"""
jest-config-validator — Validate jest.config.ts/js/json and package.json#jest
for deprecated options, transform conflicts, and best practices.

Usage:
    python3 jest_config_validator.py validate <file> [--format text|json|summary] [--strict]
    python3 jest_config_validator.py check <file>   [--format text|json|summary] [--strict]
    python3 jest_config_validator.py explain <file>
    python3 jest_config_validator.py suggest <file> [--format text|json|summary] [--strict]

Exit codes:
    0 — No errors
    1 — Errors found
    2 — File not found or parse error
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

SEVERITY_ERROR = "error"
SEVERITY_WARNING = "warning"
SEVERITY_INFO = "info"

SEVERITY_ORDER = {SEVERITY_ERROR: 0, SEVERITY_WARNING: 1, SEVERITY_INFO: 2}


@dataclass
class Finding:
    rule: str
    severity: str
    message: str
    line: Optional[int] = None


@dataclass
class ValidationResult:
    file: str
    findings: List[Finding] = field(default_factory=list)

    def add(self, rule: str, severity: str, message: str, line: Optional[int] = None):
        self.findings.append(Finding(rule=rule, severity=severity, message=message, line=line))

    @property
    def errors(self) -> List[Finding]:
        return [f for f in self.findings if f.severity == SEVERITY_ERROR]

    @property
    def warnings(self) -> List[Finding]:
        return [f for f in self.findings if f.severity == SEVERITY_WARNING]

    @property
    def infos(self) -> List[Finding]:
        return [f for f in self.findings if f.severity == SEVERITY_INFO]

    def has_errors(self) -> bool:
        return len(self.errors) > 0


# ---------------------------------------------------------------------------
# Known Jest config keys (Jest 27–30 range)
# ---------------------------------------------------------------------------

KNOWN_JEST_KEYS = {
    "automock", "bail", "cacheDirectory", "clearMocks", "collectCoverage",
    "collectCoverageFrom", "coverageDirectory", "coveragePathIgnorePatterns",
    "coverageProvider", "coverageReporters", "coverageThreshold",
    "dependencyExtractor", "displayName", "extensionsToTreatAsEsm",
    "fakeTimers", "forceCoverageMatch", "globalSetup", "globalTeardown",
    "globals", "haste", "injectGlobals", "maxConcurrency", "maxWorkers",
    "moduleDirectories", "moduleFileExtensions", "moduleNameMapper",
    "modulePathIgnorePatterns", "modulePaths", "notify", "notifyMode",
    "openHandlesTimeout", "preset", "prettierPath", "projects",
    "reporters", "resetMocks", "resetModules", "resolver", "restoreMocks",
    "rootDir", "roots", "runner", "setupFiles", "setupFilesAfterFramework",
    "setupFilesAfterFramework", "slowTestThreshold", "snapshotFormat",
    "snapshotResolver", "snapshotSerializers", "testEnvironment",
    "testEnvironmentOptions", "testFailureExitCode", "testLocationInResults",
    "testMatch", "testNamePattern", "testPathIgnorePatterns",
    "testPathPattern", "testRegex", "testResultsProcessor", "testRunner",
    "testSequencer", "testTimeout", "transform", "transformIgnorePatterns",
    "unmockedModulePathPatterns", "verbose", "watchPathIgnorePatterns",
    "watchPlugins", "watchman", "workerIdleMemoryLimit", "workerThreads",
    # Deprecated but still seen
    "extraGlobals", "testURL", "timers",
    # package.json wrapper key (not a real jest key but allowed at top level)
    "jest",
}

DEPRECATED_OPTIONS = {
    # testURL is handled by T3 (check_test_environment) to avoid duplicate findings
    "extraGlobals": (
        "D1",
        "extraGlobals is deprecated since Jest 28. Use globals instead.",
    ),
    "timers": (
        "D3",
        "timers: 'fake' is deprecated syntax. Use fakeTimers: { enableGlobally: true } instead.",
    ),
    "preprocessorIgnorePatterns": (
        "D1",
        "preprocessorIgnorePatterns is deprecated. Use transformIgnorePatterns instead.",
    ),
    "scriptPreprocessor": (
        "D1",
        "scriptPreprocessor is deprecated. Use transform instead.",
    ),
    "moduleLoader": (
        "D1",
        "moduleLoader is deprecated. Use runner instead.",
    ),
    "testPathDirs": (
        "D1",
        "testPathDirs is deprecated. Use roots instead.",
    ),
    "mapCoverage": (
        "D1",
        "mapCoverage is deprecated and has no effect since Jest 23.",
    ),
    "browser": (
        "D1",
        "browser is deprecated since Jest 28. Use testEnvironment: 'jsdom' instead.",
    ),
}

DEPRECATED_COVERAGE_REPORTERS = {"lcovonly", "teamcity", "clover"}

VALID_TEST_ENVIRONMENTS = {"jsdom", "node", "node:experimental"}


# ---------------------------------------------------------------------------
# Regex helpers for JS/TS parsing
# ---------------------------------------------------------------------------

# Strip single-line comments (// ...) but not inside strings — approximate
_RE_SINGLE_COMMENT = re.compile(r"//[^\n]*")
# Strip multi-line comments
_RE_MULTI_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)

# Detect module.exports = { ... } or export default { ... }
_RE_MODULE_EXPORTS = re.compile(
    r"module\s*\.\s*exports\s*=|export\s+default\s+", re.MULTILINE
)

# Detect key: value pairs (approximate, handles quoted and unquoted keys)
_RE_KEY_VALUE = re.compile(
    r"""(?:^|[,{]\s*)["']?(\w+)["']?\s*:\s*(.+?)(?=\s*[,}\n]|$)""",
    re.MULTILINE,
)

# Detect string values (single or double quoted)
_RE_STRING_VALUE = re.compile(r"""^["'](.+?)["']$""")

# Detect testEnvironment value
_RE_TEST_ENV = re.compile(r"""testEnvironment\s*:\s*["']([^"']+)["']""")

# Detect testURL
_RE_TEST_URL = re.compile(r"""testURL\s*:\s*["']""")

# Detect timers: 'fake'
_RE_TIMERS_FAKE = re.compile(r"""timers\s*:\s*["']fake["']""")

# Detect transform block (rough extraction)
_RE_TRANSFORM_BLOCK = re.compile(
    r"transform\s*:\s*\{([^}]*)\}", re.DOTALL
)

# Detect transform patterns (each line inside transform block)
_RE_TRANSFORM_ENTRY = re.compile(
    r"""["']([^"']+)["']\s*:\s*["']([^"']+)["']"""
)

# transformIgnorePatterns
_RE_TRANSFORM_IGNORE = re.compile(
    r"""transformIgnorePatterns\s*:\s*\[([^\]]*)\]""", re.DOTALL
)

# collectCoverage
_RE_COLLECT_COVERAGE = re.compile(
    r"""collectCoverage\s*:\s*(true|false)"""
)

# collectCoverageFrom
_RE_COLLECT_FROM_BLOCK = re.compile(
    r"""collectCoverageFrom\s*:\s*\[([^\]]*)\]""", re.DOTALL
)

# coverageThreshold
_RE_COVERAGE_THRESHOLD = re.compile(
    r"""coverageThreshold\s*:\s*\{"""
)

# coverageReporters
_RE_COVERAGE_REPORTERS = re.compile(
    r"""coverageReporters\s*:\s*\[([^\]]*)\]""", re.DOTALL
)

# testMatch / testRegex
_RE_TEST_MATCH = re.compile(
    r"""testMatch\s*:\s*\[([^\]]*)\]""", re.DOTALL
)
_RE_TEST_PATH_PATTERN = re.compile(
    r"""testPathPattern\s*:\s*["']([^"']*)["']"""
)

# maxWorkers
_RE_MAX_WORKERS = re.compile(
    r"""maxWorkers\s*:\s*(\d+|["'][^"']+["'])"""
)

# roots
_RE_ROOTS = re.compile(r"""roots\s*:\s*\[([^\]]*)\]""", re.DOTALL)

# preset
_RE_PRESET = re.compile(r"""preset\s*:\s*["']([^"']+)["']""")

# globals key present
_RE_GLOBALS = re.compile(r"""(?<![a-zA-Z])globals\s*:""")

# moduleNameMapper block
_RE_MNM_BLOCK = re.compile(
    r"""moduleNameMapper\s*:\s*\{([^}]*)\}""", re.DOTALL
)

# setupFiles / setupFilesAfterFramework
_RE_SETUP_FILES = re.compile(
    r"""setupFiles(?:AfterFramework)?\s*:\s*\[([^\]]*)\]""", re.DOTALL
)

# verbose
_RE_VERBOSE = re.compile(r"""verbose\s*:\s*(true|false)""")

# reporters
_RE_REPORTERS = re.compile(r"""reporters\s*:\s*\[""")

# jest.fn() usage
_RE_JEST_FN = re.compile(r"""jest\.fn\s*\(""")

# React / JSX detection
_RE_JSX_TRANSFORM = re.compile(
    r"""["'][^"']*\.jsx?["']\s*:|jsx|react""", re.IGNORECASE
)

# ts-jest and babel-jest patterns
_RE_TS_JEST = re.compile(r"""ts-jest""")
_RE_BABEL_JEST = re.compile(r"""babel-jest""")


# ---------------------------------------------------------------------------
# Config file loader
# ---------------------------------------------------------------------------


def _strip_comments(text: str) -> str:
    """Remove JS-style comments (approximate, not full parser)."""
    text = _RE_MULTI_COMMENT.sub(" ", text)
    text = _RE_SINGLE_COMMENT.sub("", text)
    return text


def load_file(path: str) -> Tuple[Optional[str], Optional[dict], Optional[str]]:
    """
    Load a Jest config file. Returns (raw_text, json_data, error).
    json_data is only populated for .json files.
    """
    if not os.path.exists(path):
        return None, None, f"File not found: {path}"
    try:
        with open(path, "r", encoding="utf-8") as fh:
            raw = fh.read()
    except OSError as exc:
        return None, None, f"Cannot read file: {exc}"

    ext = os.path.splitext(path)[1].lower()

    if ext == ".json":
        # For package.json, extract #jest if present
        if os.path.basename(path) == "package.json":
            try:
                pkg = json.loads(raw)
            except json.JSONDecodeError as exc:
                return raw, None, f"Invalid JSON in package.json: {exc}"
            jest_cfg = pkg.get("jest")
            if jest_cfg is None:
                return raw, None, "No 'jest' key found in package.json"
            return raw, jest_cfg, None
        else:
            try:
                data = json.loads(raw)
            except json.JSONDecodeError as exc:
                return raw, None, f"Invalid JSON: {exc}"
            return raw, data, None

    # .js / .ts / .cjs / .mjs
    return raw, None, None


def detect_jest_config_files(directory: str = ".") -> List[str]:
    """Find Jest config files in a directory (for S3 multi-config check)."""
    candidates = [
        "jest.config.js", "jest.config.ts", "jest.config.cjs",
        "jest.config.mjs", "jest.config.json",
    ]
    found = []
    for name in candidates:
        p = os.path.join(directory, name)
        if os.path.exists(p):
            found.append(p)
    return found


# ---------------------------------------------------------------------------
# Individual rule checks
# ---------------------------------------------------------------------------


def check_structure(path: str, raw: str, json_data: Optional[dict], result: ValidationResult):
    """S1-S5: Structure rules."""

    # S2: empty config
    if not raw or not raw.strip():
        result.add("S2", SEVERITY_ERROR, "Config file is empty.")
        return

    ext = os.path.splitext(path)[1].lower()
    basename = os.path.basename(path)

    if basename == "package.json" or ext == ".json":
        # S5 is handled at load time (json parse error)
        if json_data is None and ext == ".json" and basename != "package.json":
            result.add("S5", SEVERITY_ERROR, "Invalid JSON syntax in config file.")
            return
        if json_data is not None:
            # S4: unknown keys
            unknown = set(json_data.keys()) - KNOWN_JEST_KEYS
            if unknown:
                result.add(
                    "S4", SEVERITY_WARNING,
                    f"Unknown top-level config key(s): {', '.join(sorted(unknown))}. "
                    "These will be ignored by Jest.",
                )
    else:
        # JS/TS: check for module.exports or export default
        stripped = _strip_comments(raw)
        if not _RE_MODULE_EXPORTS.search(stripped):
            result.add(
                "S2", SEVERITY_ERROR,
                "No module.exports or export default found. Jest will not load this config.",
            )

        # S4: detect unknown keys from JS (approximate)
        found_keys = set()
        for m in _RE_KEY_VALUE.finditer(stripped):
            found_keys.add(m.group(1))
        unknown = found_keys - KNOWN_JEST_KEYS
        # Filter out common JS words that regex picks up
        noise = {
            "global", "branches", "functions", "lines", "statements",
            "require", "path", "process", "env", "exports", "default",
            "module", "true", "false", "null", "const", "let", "var",
            "return", "from", "import", "type", "interface",
        }
        unknown -= noise
        if unknown:
            result.add(
                "S4", SEVERITY_WARNING,
                f"Possible unknown top-level config key(s): {', '.join(sorted(unknown))}. "
                "Verify these are valid Jest options.",
            )


def check_multi_config(path: str, result: ValidationResult):
    """S3: Check if both jest.config.* and package.json#jest exist."""
    directory = os.path.dirname(os.path.abspath(path))
    pkg_path = os.path.join(directory, "package.json")
    basename = os.path.basename(path)

    if basename == "package.json":
        # Check if any jest.config.* also exists
        others = detect_jest_config_files(directory)
        if others:
            result.add(
                "S3", SEVERITY_WARNING,
                f"package.json#jest is configured, but jest.config file(s) also exist: "
                f"{', '.join(os.path.basename(p) for p in others)}. "
                "Jest will prefer the config file over package.json#jest.",
            )
    elif os.path.exists(pkg_path):
        try:
            with open(pkg_path, "r", encoding="utf-8") as fh:
                pkg = json.load(fh)
            if "jest" in pkg:
                result.add(
                    "S3", SEVERITY_WARNING,
                    f"Both {basename} and package.json#jest are present. "
                    "Jest will use the config file and ignore package.json#jest.",
                )
        except (OSError, json.JSONDecodeError):
            pass


def check_test_environment(raw: str, json_data: Optional[dict], result: ValidationResult):
    """T1-T4: Test environment rules."""
    if json_data is not None:
        env = json_data.get("testEnvironment")
        if env is not None:
            if env not in VALID_TEST_ENVIRONMENTS and not env.startswith("<") and "/" not in env and "\\" not in env:
                result.add(
                    "T1", SEVERITY_ERROR,
                    f"Invalid testEnvironment: '{env}'. Expected 'jsdom', 'node', or a custom module path.",
                )
            if env == "jsdom":
                result.add(
                    "T2", SEVERITY_WARNING,
                    "testEnvironment: 'jsdom' requires the 'jest-environment-jsdom' package (Jest 28+). "
                    "Install it separately: npm install --save-dev jest-environment-jsdom",
                )
        # T3: testURL
        if "testURL" in json_data:
            result.add(
                "T3", SEVERITY_WARNING,
                "testURL is deprecated since Jest 28. Use testEnvironmentOptions: { url: '...' } instead.",
            )
        # T4: empty testMatch
        tm = json_data.get("testMatch")
        if tm is not None and (not tm or tm == []):
            result.add("T4", SEVERITY_WARNING, "testMatch is set but empty — no tests will be found.")
        tp = json_data.get("testPathPattern")
        if tp is not None and tp == "":
            result.add("T4", SEVERITY_WARNING, "testPathPattern is set but empty — no tests will be found.")
    else:
        # JS/TS parsing
        m = _RE_TEST_ENV.search(raw)
        if m:
            env = m.group(1)
            if env not in VALID_TEST_ENVIRONMENTS and "/" not in env and "\\" not in env and not env.startswith("<"):
                result.add(
                    "T1", SEVERITY_ERROR,
                    f"Invalid testEnvironment: '{env}'. Expected 'jsdom', 'node', or a custom module path.",
                )
            if env == "jsdom":
                result.add(
                    "T2", SEVERITY_WARNING,
                    "testEnvironment: 'jsdom' requires the 'jest-environment-jsdom' package (Jest 28+). "
                    "Install it separately: npm install --save-dev jest-environment-jsdom",
                )
        if _RE_TEST_URL.search(raw):
            result.add(
                "T3", SEVERITY_WARNING,
                "testURL is deprecated since Jest 28. Use testEnvironmentOptions: { url: '...' } instead.",
            )
        # T4: empty testMatch
        tm = _RE_TEST_MATCH.search(raw)
        if tm and not tm.group(1).strip():
            result.add("T4", SEVERITY_WARNING, "testMatch is set but empty — no tests will be found.")
        tp = _RE_TEST_PATH_PATTERN.search(raw)
        if tp and not tp.group(1).strip():
            result.add("T4", SEVERITY_WARNING, "testPathPattern is set but empty — no tests will be found.")


def check_transforms(raw: str, json_data: Optional[dict], result: ValidationResult):
    """X1-X4: Transform rules."""
    if json_data is not None:
        transform = json_data.get("transform", {})
        transform_ignore = json_data.get("transformIgnorePatterns", [])
        patterns = list(transform.keys()) if isinstance(transform, dict) else []
        transformers = list(transform.values()) if isinstance(transform, dict) else []
    else:
        patterns = []
        transformers = []
        transform_ignore = []

        block_m = _RE_TRANSFORM_BLOCK.search(raw)
        if block_m:
            block = block_m.group(1)
            for em in _RE_TRANSFORM_ENTRY.finditer(block):
                patterns.append(em.group(1))
                transformers.append(em.group(2))

        ig_m = _RE_TRANSFORM_IGNORE.search(raw)
        if ig_m:
            for s in re.findall(r"""["']([^"']+)["']""", ig_m.group(1)):
                transform_ignore.append(s)

    # X1: overlapping patterns
    if len(patterns) > 1:
        for i in range(len(patterns)):
            for j in range(i + 1, len(patterns)):
                # Check for obvious overlap (one is substring/superset of other)
                pi, pj = patterns[i], patterns[j]
                # Both match .ts — heuristic: same extension group
                exts_i = re.findall(r"\.\w+", pi)
                exts_j = re.findall(r"\.\w+", pj)
                overlap = set(exts_i) & set(exts_j)
                if overlap and transformers[i] != transformers[j]:
                    result.add(
                        "X1", SEVERITY_WARNING,
                        f"Transform patterns may overlap: '{pi}' and '{pj}' both match extension(s) "
                        f"{overlap}. Files may be processed by the wrong transformer.",
                    )

    # X2: ts-jest + babel-jest together
    has_ts_jest = any(_RE_TS_JEST.search(t) for t in transformers)
    has_babel_jest = any(_RE_BABEL_JEST.search(t) for t in transformers)
    if not transformers:
        has_ts_jest = bool(_RE_TS_JEST.search(raw))
        has_babel_jest = bool(_RE_BABEL_JEST.search(raw))
    if has_ts_jest and has_babel_jest:
        result.add(
            "X2", SEVERITY_WARNING,
            "Both ts-jest and babel-jest are configured as transformers. "
            "Ensure patterns are strictly separated to avoid conflicts (e.g., .ts files only to ts-jest).",
        )

    # X3: transformIgnorePatterns too broad
    for pat in transform_ignore:
        if pat in ("", ".*", ".+", "node_modules") or pat == "/node_modules/":
            # /node_modules/ is the default and fine; flag only truly broad ones
            if pat in ("", ".*", ".+"):
                result.add(
                    "X3", SEVERITY_WARNING,
                    f"transformIgnorePatterns includes overly broad pattern '{pat}'. "
                    "This may prevent necessary transforms from running.",
                )
        elif re.search(r"\.\*$|\.\+$", pat) and "node_modules" not in pat:
            result.add(
                "X3", SEVERITY_WARNING,
                f"transformIgnorePatterns pattern '{pat}' may be too broad and skip needed transforms.",
            )

    # X4: missing transform for JSX/TSX when React is detected
    raw_lower = raw.lower()
    has_react = "react" in raw_lower or "jsx" in raw_lower
    if has_react and patterns:
        has_jsx_transform = any(re.search(r"jsx|tsx", p) for p in patterns) or any(
            re.search(r"jsx|tsx", t) for t in transformers
        )
        if not has_jsx_transform:
            result.add(
                "X4", SEVERITY_WARNING,
                "React/JSX usage detected but no transform pattern covers .jsx/.tsx files. "
                "Add a transform for '^.+\\.tsx?$' or '^.+\\.jsx?$'.",
            )


def check_coverage(raw: str, json_data: Optional[dict], result: ValidationResult):
    """V1-V3: Coverage rules."""
    if json_data is not None:
        collect = json_data.get("collectCoverage", None)
        collect_from = json_data.get("collectCoverageFrom", None)
        threshold = json_data.get("coverageThreshold", None)
        reporters = json_data.get("coverageReporters", [])

        # V1
        if collect_from is not None:
            if not collect_from:
                result.add(
                    "V1", SEVERITY_WARNING,
                    "collectCoverageFrom is empty — no files will be included in coverage.",
                )
            elif collect_from == ["**/*"] or collect_from == ["**"]:
                result.add(
                    "V1", SEVERITY_WARNING,
                    "collectCoverageFrom is too broad ('**/*'). "
                    "Restrict to source directories (e.g., ['src/**/*.ts']).",
                )

        # V2
        if threshold and collect is False:
            result.add(
                "V2", SEVERITY_WARNING,
                "coverageThreshold is configured but collectCoverage is false. "
                "Thresholds will never be checked. Set collectCoverage: true.",
            )

        # V3
        for rep in reporters:
            if isinstance(rep, str) and rep in DEPRECATED_COVERAGE_REPORTERS:
                result.add(
                    "V3", SEVERITY_WARNING,
                    f"Deprecated coverageReporter: '{rep}'. "
                    "Use 'lcov', 'text', 'html', or 'cobertura' instead.",
                )
    else:
        collect_m = _RE_COLLECT_COVERAGE.search(raw)
        collect = None
        if collect_m:
            collect = collect_m.group(1) == "true"

        # V1
        cf_m = _RE_COLLECT_FROM_BLOCK.search(raw)
        if cf_m:
            content = cf_m.group(1).strip()
            if not content:
                result.add(
                    "V1", SEVERITY_WARNING,
                    "collectCoverageFrom is empty — no files will be included in coverage.",
                )
            elif re.search(r"""["']\*\*/\*["']|["']\*\*["']""", content):
                result.add(
                    "V1", SEVERITY_WARNING,
                    "collectCoverageFrom is too broad ('**/*'). "
                    "Restrict to source directories (e.g., ['src/**/*.ts']).",
                )

        # V2
        has_threshold = bool(_RE_COVERAGE_THRESHOLD.search(raw))
        if has_threshold and collect is False:
            result.add(
                "V2", SEVERITY_WARNING,
                "coverageThreshold is configured but collectCoverage is false. "
                "Thresholds will never be checked. Set collectCoverage: true.",
            )

        # V3
        rep_m = _RE_COVERAGE_REPORTERS.search(raw)
        if rep_m:
            for rep in re.findall(r"""["']([^"']+)["']""", rep_m.group(1)):
                if rep in DEPRECATED_COVERAGE_REPORTERS:
                    result.add(
                        "V3", SEVERITY_WARNING,
                        f"Deprecated coverageReporter: '{rep}'. "
                        "Use 'lcov', 'text', 'html', or 'cobertura' instead.",
                    )


def check_deprecated(raw: str, json_data: Optional[dict], result: ValidationResult):
    """D1-D3: Deprecated / migration rules."""
    if json_data is not None:
        for opt, (rule, msg) in DEPRECATED_OPTIONS.items():
            if opt in json_data:
                if opt == "timers":
                    val = json_data[opt]
                    if val == "fake":
                        result.add(rule, SEVERITY_WARNING, msg)
                else:
                    result.add(rule, SEVERITY_WARNING, msg)
    else:
        for opt, (rule, msg) in DEPRECATED_OPTIONS.items():
            if opt == "timers":
                if _RE_TIMERS_FAKE.search(raw):
                    result.add(rule, SEVERITY_WARNING, msg)
            else:
                pat = re.compile(rf"""(?<![a-zA-Z]){re.escape(opt)}\s*:""")
                if pat.search(raw):
                    result.add(rule, SEVERITY_WARNING, msg)

    # D2: jest.fn() in config file
    if _RE_JEST_FN.search(raw):
        result.add(
            "D2", SEVERITY_WARNING,
            "jest.fn() detected in config file. Config files should not contain mocks. "
            "Move mocks to setupFiles or individual test files.",
        )

    # D1 extra: verbose + custom reporters (verbose is ignored when reporters is set)
    verbose_m = _RE_VERBOSE.search(raw)
    has_reporters = bool(_RE_REPORTERS.search(raw))
    if verbose_m and verbose_m.group(1) == "true" and has_reporters:
        result.add(
            "D1", SEVERITY_WARNING,
            "verbose: true has no effect when a custom reporters array is configured. "
            "Add '@jest/reporters' to the reporters array if verbose output is needed.",
        )


def check_best_practices(raw: str, json_data: Optional[dict], result: ValidationResult):
    """B1-B6: Best practice rules."""
    if json_data is not None:
        # B1
        has_clear = json_data.get("clearMocks") or json_data.get("resetMocks") or json_data.get("restoreMocks")
        if not has_clear:
            result.add(
                "B1", SEVERITY_INFO,
                "None of clearMocks/resetMocks/restoreMocks is set. "
                "Consider enabling clearMocks: true to avoid mock state leaking between tests.",
            )

        # B2
        roots = json_data.get("roots", [])
        for r in roots:
            if isinstance(r, str) and r.startswith(".."):
                result.add(
                    "B2", SEVERITY_WARNING,
                    f"roots entry '{r}' points outside the project directory. "
                    "This may cause unexpected test discovery.",
                )

        # B3
        for key in ("setupFiles", "setupFilesAfterFramework"):
            for sf in json_data.get(key, []):
                if isinstance(sf, str) and not (sf.startswith("<") or sf.startswith(".") or sf.startswith("/")):
                    result.add(
                        "B3", SEVERITY_WARNING,
                        f"{key} entry '{sf}' does not look like a relative path or module. "
                        "Use '<rootDir>/path/to/setup.ts' or a relative path.",
                    )

        # B4
        mnm = json_data.get("moduleNameMapper", {})
        if isinstance(mnm, dict):
            for pattern in mnm.keys():
                if len(pattern) > 30 and not pattern.startswith("^"):
                    result.add(
                        "B4", SEVERITY_INFO,
                        f"moduleNameMapper pattern '{pattern[:40]}...' is complex. "
                        "Consider adding a comment above it explaining its purpose.",
                    )

        # B5
        preset = json_data.get("preset")
        if preset:
            overlap_keys = {
                "transform", "testEnvironment", "moduleFileExtensions",
                "moduleNameMapper", "globals",
            }
            overlap = overlap_keys & set(json_data.keys()) - {"preset"}
            if overlap:
                result.add(
                    "B5", SEVERITY_WARNING,
                    f"preset '{preset}' is set alongside keys that presets typically configure: "
                    f"{', '.join(sorted(overlap))}. This may cause unexpected overrides.",
                )

        # B6
        max_workers = json_data.get("maxWorkers")
        ci_env = os.environ.get("CI") or os.environ.get("CONTINUOUS_INTEGRATION")
        if max_workers == 1 and not ci_env:
            result.add(
                "B6", SEVERITY_WARNING,
                "maxWorkers: 1 disables parallelism. "
                "This is only recommended in CI environments. "
                "Remove or increase maxWorkers for local development.",
            )
    else:
        # B1
        has_clear = (
            re.search(r"""clearMocks\s*:\s*true""", raw)
            or re.search(r"""resetMocks\s*:\s*true""", raw)
            or re.search(r"""restoreMocks\s*:\s*true""", raw)
        )
        if not has_clear:
            result.add(
                "B1", SEVERITY_INFO,
                "None of clearMocks/resetMocks/restoreMocks is set. "
                "Consider enabling clearMocks: true to avoid mock state leaking between tests.",
            )

        # B2
        roots_m = _RE_ROOTS.search(raw)
        if roots_m:
            for r in re.findall(r"""["']([^"']+)["']""", roots_m.group(1)):
                if r.startswith(".."):
                    result.add(
                        "B2", SEVERITY_WARNING,
                        f"roots entry '{r}' points outside the project directory.",
                    )

        # B3
        setup_m = _RE_SETUP_FILES.search(raw)
        if setup_m:
            for sf in re.findall(r"""["']([^"']+)["']""", setup_m.group(1)):
                if not (sf.startswith("<") or sf.startswith(".") or sf.startswith("/")):
                    result.add(
                        "B3", SEVERITY_WARNING,
                        f"setupFiles entry '{sf}' does not look like a relative path or <rootDir> reference.",
                    )

        # B4
        mnm_m = _RE_MNM_BLOCK.search(raw)
        if mnm_m:
            for pattern in re.findall(r"""["']([^"']+)["']\s*:""", mnm_m.group(1)):
                if len(pattern) > 30 and not pattern.startswith("^"):
                    result.add(
                        "B4", SEVERITY_INFO,
                        f"moduleNameMapper pattern '{pattern[:40]}' is complex without a leading anchor. "
                        "Consider adding a comment explaining its purpose.",
                    )

        # B5
        preset_m = _RE_PRESET.search(raw)
        if preset_m:
            preset = preset_m.group(1)
            overlap_keys = ["transform", "testEnvironment", "moduleFileExtensions", "moduleNameMapper"]
            found_overlap = []
            for k in overlap_keys:
                if re.search(rf"""(?<![a-zA-Z]){re.escape(k)}\s*:""", raw):
                    found_overlap.append(k)
            if found_overlap:
                result.add(
                    "B5", SEVERITY_WARNING,
                    f"preset '{preset}' is set alongside keys that presets typically configure: "
                    f"{', '.join(found_overlap)}. This may cause unexpected overrides.",
                )

        # B6
        mw_m = _RE_MAX_WORKERS.search(raw)
        if mw_m:
            val = mw_m.group(1).strip("\"'")
            ci_env = os.environ.get("CI") or os.environ.get("CONTINUOUS_INTEGRATION")
            if val == "1" and not ci_env:
                result.add(
                    "B6", SEVERITY_WARNING,
                    "maxWorkers: 1 disables parallelism. "
                    "This is only recommended in CI environments.",
                )


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def run_validate(path: str, strict: bool = False, structure_only: bool = False) -> ValidationResult:
    """Full validation (or structure-only for 'check' command)."""
    result = ValidationResult(file=path)

    # S1: file existence is checked in load_file
    raw, json_data, err = load_file(path)
    if err and raw is None:
        result.add("S1", SEVERITY_ERROR, err)
        return result
    if err:
        # JSON parse error — still report it
        result.add("S5", SEVERITY_ERROR, err)
        if structure_only:
            return result

    raw = raw or ""

    check_structure(path, raw, json_data, result)
    check_multi_config(path, result)

    if not structure_only:
        if json_data is not None or raw:
            check_test_environment(raw, json_data, result)
            check_transforms(raw, json_data, result)
            check_coverage(raw, json_data, result)
            check_deprecated(raw, json_data, result)
            check_best_practices(raw, json_data, result)

    if strict:
        for f in result.findings:
            if f.severity == SEVERITY_WARNING:
                f.severity = SEVERITY_ERROR

    return result


def run_explain(path: str) -> str:
    """Explain the config in human-readable form."""
    raw, json_data, err = load_file(path)
    if err and raw is None:
        return f"Error: {err}"

    raw = raw or ""
    lines = [f"Config file: {path}", ""]

    def get_val(key: str, default="(not set)") -> str:
        if json_data is not None:
            return str(json_data.get(key, default))
        m = re.search(rf"""(?<![a-zA-Z]){re.escape(key)}\s*:\s*["']?([^"',\n\}}]+)["']?""", raw)
        return m.group(1).strip() if m else default

    lines.append(f"  Test environment : {get_val('testEnvironment')}")
    lines.append(f"  Preset           : {get_val('preset')}")
    lines.append(f"  Max workers      : {get_val('maxWorkers')}")
    lines.append(f"  Collect coverage : {get_val('collectCoverage')}")
    lines.append(f"  Clear mocks      : {get_val('clearMocks')}")
    lines.append(f"  Reset mocks      : {get_val('resetMocks')}")
    lines.append(f"  Restore mocks    : {get_val('restoreMocks')}")
    lines.append(f"  Verbose          : {get_val('verbose')}")
    lines.append("")

    # Transforms
    if json_data is not None:
        transform = json_data.get("transform", {})
        if transform:
            lines.append("  Transforms:")
            for pat, transformer in transform.items():
                lines.append(f"    {pat!r:40s} -> {transformer}")
        else:
            lines.append("  Transforms: (none configured — using Jest defaults)")
    else:
        block_m = _RE_TRANSFORM_BLOCK.search(raw)
        if block_m:
            lines.append("  Transforms:")
            for em in _RE_TRANSFORM_ENTRY.finditer(block_m.group(1)):
                lines.append(f"    {em.group(1)!r:40s} -> {em.group(2)}")
        else:
            lines.append("  Transforms: (none configured — using Jest defaults)")

    lines.append("")

    # Coverage
    if json_data is not None:
        cf = json_data.get("collectCoverageFrom", [])
        if cf:
            lines.append("  Coverage from:")
            for p in cf:
                lines.append(f"    {p}")
        th = json_data.get("coverageThreshold")
        if th:
            lines.append(f"  Coverage threshold: {json.dumps(th)}")
    else:
        cf_m = _RE_COLLECT_FROM_BLOCK.search(raw)
        if cf_m:
            lines.append("  Coverage from:")
            for p in re.findall(r"""["']([^"']+)["']""", cf_m.group(1)):
                lines.append(f"    {p}")

    return "\n".join(lines)


def run_suggest(path: str, strict: bool = False) -> ValidationResult:
    """Run full validation and present results as suggestions."""
    return run_validate(path, strict=strict)


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------


def format_text(result: ValidationResult, command: str = "validate") -> str:
    """Human-readable text output."""
    lines = [f"jest-config-validator — {result.file}", ""]

    if not result.findings:
        lines.append("  No issues found.")
        return "\n".join(lines)

    SEV_LABEL = {SEVERITY_ERROR: "ERROR  ", SEVERITY_WARNING: "WARNING", SEVERITY_INFO: "INFO   "}
    for f in sorted(result.findings, key=lambda x: SEVERITY_ORDER[x.severity]):
        loc = f" (line {f.line})" if f.line else ""
        lines.append(f"  [{SEV_LABEL[f.severity]}] [{f.rule}]{loc} {f.message}")

    lines.append("")
    lines.append(
        f"  {len(result.errors)} error(s), "
        f"{len(result.warnings)} warning(s), "
        f"{len(result.infos)} info(s)"
    )
    return "\n".join(lines)


def format_summary(result: ValidationResult) -> str:
    """One-line summary."""
    status = "FAIL" if result.has_errors() else "PASS"
    return (
        f"[{status}] {result.file}: "
        f"{len(result.errors)} error(s), "
        f"{len(result.warnings)} warning(s), "
        f"{len(result.infos)} info(s)"
    )


def format_json(result: ValidationResult) -> str:
    """JSON output."""
    data = {
        "file": result.file,
        "summary": {
            "errors": len(result.errors),
            "warnings": len(result.warnings),
            "infos": len(result.infos),
            "pass": not result.has_errors(),
        },
        "findings": [
            {
                "rule": f.rule,
                "severity": f.severity,
                "message": f.message,
                "line": f.line,
            }
            for f in sorted(result.findings, key=lambda x: SEVERITY_ORDER[x.severity])
        ],
    }
    return json.dumps(data, indent=2)


def format_explain(text: str) -> str:
    return text


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="jest_config_validator",
        description="Validate Jest configuration files for errors, deprecated options, and best practices.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    def add_common(p):
        p.add_argument("file", help="Path to jest.config.js/ts/json or package.json")
        p.add_argument(
            "--format",
            choices=["text", "json", "summary"],
            default="text",
            help="Output format (default: text)",
        )
        p.add_argument(
            "--strict",
            action="store_true",
            help="Treat warnings as errors",
        )

    p_validate = sub.add_parser("validate", help="Full validation (all rules)")
    add_common(p_validate)

    p_check = sub.add_parser("check", help="Quick syntax/structure check only")
    add_common(p_check)

    p_explain = sub.add_parser("explain", help="Explain config in human-readable form")
    p_explain.add_argument("file", help="Path to Jest config file")

    p_suggest = sub.add_parser("suggest", help="Suggest improvements")
    add_common(p_suggest)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "explain":
        text = run_explain(args.file)
        print(text)
        sys.exit(0)

    structure_only = args.command == "check"

    result = run_validate(args.file, strict=args.strict, structure_only=structure_only)

    fmt = args.format
    if fmt == "json":
        print(format_json(result))
    elif fmt == "summary":
        print(format_summary(result))
    else:
        print(format_text(result, command=args.command))

    # Exit codes
    # 2 = file not found / parse error (S1 or S5 as only finding)
    if result.findings and all(f.rule in ("S1", "S5") for f in result.findings):
        sys.exit(2)
    sys.exit(1 if result.has_errors() else 0)


if __name__ == "__main__":
    main()
