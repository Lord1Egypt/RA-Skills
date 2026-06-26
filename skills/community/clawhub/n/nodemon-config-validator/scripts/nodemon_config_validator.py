#!/usr/bin/env python3
"""Nodemon Config Validator — validate nodemon.json, .nodemonrc, .nodemonrc.json, package.json#nodemonConfig."""

import json
import os
import re
import sys
from pathlib import Path

VALID_TOP_KEYS = {
    "restartable", "ignore", "verbose", "execMap", "watch", "stdin",
    "runOnChangeOnly", "ext", "delay", "legacyWatch", "colours", "cwd",
    "exec", "script", "args", "nodeArgs", "events", "signal", "env",
    "pollingInterval", "dump", "spawn", "quiet",
}

# Extensions typically expected per inferred project type
COMMON_EXTENSIONS_BY_TYPE = {
    "typescript": {"ts", "tsx"},
    "react": {"jsx", "tsx"},
    "javascript": {"js", "mjs", "cjs"},
}

SHELL_INJECTION_PATTERNS = re.compile(
    r'(\$\(|`[^`]+`|&&|\|\||\||;|\beval\b|\bexec\b)',
)


def load_config(filepath):
    path = Path(filepath)
    if not path.exists():
        return None, f"File not found: {filepath}"
    try:
        text = path.read_text(encoding="utf-8").strip()
    except Exception as e:
        return None, f"Cannot read file: {e}"
    if not text:
        return None, "File is empty"

    if path.name == "package.json":
        try:
            pkg = json.loads(text)
            if "nodemonConfig" not in pkg:
                return None, "No 'nodemonConfig' key in package.json"
            return pkg["nodemonConfig"], None
        except json.JSONDecodeError as e:
            return None, f"Invalid JSON: {e}"
    else:
        # .nodemonrc may be JSON with comments stripped
        comment_re = re.compile(r'//.*?$|/\*.*?\*/', re.MULTILINE | re.DOTALL)
        cleaned = comment_re.sub('', text)
        cleaned = re.sub(r',(\s*[}\]])', r'\1', cleaned)
        try:
            return json.loads(cleaned), None
        except json.JSONDecodeError as e:
            return None, f"Invalid JSON: {e}"


def find_sibling_nodemon_configs(filepath):
    """Return other nodemon config files found in the same directory."""
    directory = Path(filepath).parent
    names = ["nodemon.json", ".nodemonrc", ".nodemonrc.json"]
    siblings = []
    for name in names:
        p = directory / name
        if p.exists() and str(p.resolve()) != str(Path(filepath).resolve()):
            siblings.append(name)
    pkg = directory / "package.json"
    if pkg.exists() and Path(filepath).name != "package.json":
        try:
            d = json.loads(pkg.read_text(encoding="utf-8"))
            if "nodemonConfig" in d:
                siblings.append("package.json#nodemonConfig")
        except Exception:
            pass
    return siblings


class Finding:
    def __init__(self, rule_id, severity, message, detail=None):
        self.rule_id = rule_id
        self.severity = severity
        self.message = message
        self.detail = detail

    def to_dict(self):
        d = {"rule": self.rule_id, "severity": self.severity, "message": self.message}
        if self.detail:
            d["detail"] = self.detail
        return d

    def to_text(self):
        icon = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}.get(self.severity, "•")
        s = f"{icon} [{self.rule_id}] {self.message}"
        if self.detail:
            s += f"\n   → {self.detail}"
        return s


# ---------------------------------------------------------------------------
# Rule implementations
# ---------------------------------------------------------------------------

def _check_structure(config, filepath, findings):
    """S1-S5: Structural checks."""
    # S4: Unknown top-level keys
    unknown = set(config.keys()) - VALID_TOP_KEYS
    if unknown:
        findings.append(Finding("S4", "warning",
            f"Unknown top-level keys: {', '.join(sorted(unknown))}",
            f"Valid keys: {', '.join(sorted(VALID_TOP_KEYS))}"))

    # S5: Conflicting config files in same directory
    siblings = find_sibling_nodemon_configs(filepath)
    if siblings:
        findings.append(Finding("S5", "warning",
            f"Multiple nodemon configs detected: {', '.join(siblings)}",
            "Nodemon merges configs in a defined priority order which can cause unexpected behavior"))


def _check_watch(config, findings):
    """W1-W4: Watch-related checks."""
    watch = config.get("watch")

    # W1: Empty watch array
    if watch is not None and isinstance(watch, list) and len(watch) == 0:
        findings.append(Finding("W1", "warning",
            "Empty watch array",
            "An empty watch array means nodemon won't watch anything; omit it or add paths"))

    # W2: Watch paths not using relative paths
    if watch and isinstance(watch, list):
        for wp in watch:
            if isinstance(wp, str) and wp.startswith("/"):
                findings.append(Finding("W2", "info",
                    f"Watch path is absolute: '{wp}'",
                    "Prefer relative paths (e.g. 'src', './lib') for portability"))

    # W3: Watching node_modules
    if watch and isinstance(watch, list):
        for wp in watch:
            if isinstance(wp, str) and "node_modules" in wp:
                findings.append(Finding("W3", "error",
                    f"Watching node_modules: '{wp}'",
                    "Watching node_modules causes massive performance degradation and rapid restart loops"))

    # W4: No watch or ext — relying on defaults
    ext = config.get("ext")
    if not watch and not ext:
        findings.append(Finding("W4", "info",
            "No watch or ext specified — relying on nodemon defaults",
            "Defaults watch CWD and extensions js,mjs,cjs,json; be explicit for large projects"))


def _check_extensions(config, findings):
    """E1-E3: Extension-related checks."""
    ext = config.get("ext")

    # E1: Empty ext string
    if ext is not None and isinstance(ext, str) and ext.strip() == "":
        findings.append(Finding("E1", "warning",
            "Empty ext string",
            "An empty ext means no file extension filter; remove it or add extensions like 'js,ts,json'"))

    if ext and isinstance(ext, str):
        parts = [e.strip().lstrip(".") for e in ext.split(",") if e.strip()]

        # E2: Too many extensions
        if len(parts) > 10:
            findings.append(Finding("E2", "warning",
                f"Watching too many extensions ({len(parts)})",
                "Watching >10 extensions increases filesystem watcher overhead; narrow down to what you use"))

        # E3: Missing common extensions for inferred project type
        ext_set = set(parts)
        watch = config.get("watch", [])
        exec_cmd = config.get("exec", "")
        exec_map = config.get("execMap", {})

        is_ts = "ts" in ext_set or "ts" in str(exec_cmd) or "ts-node" in str(exec_cmd)
        is_react = "jsx" in ext_set or "tsx" in ext_set or "react" in str(exec_cmd).lower()

        if is_ts and "ts" not in ext_set:
            findings.append(Finding("E3", "info",
                "TypeScript usage detected but 'ts' not in ext",
                "Add 'ts' to ext to watch TypeScript files"))
        if is_react and "tsx" not in ext_set and "jsx" not in ext_set:
            findings.append(Finding("E3", "info",
                "React usage detected but 'jsx'/'tsx' not in ext",
                "Add 'tsx' or 'jsx' to ext"))


def _check_ignore(config, findings):
    """I1-I3: Ignore-related checks."""
    ignore = config.get("ignore")

    # I1: Empty ignore array
    if ignore is not None and isinstance(ignore, list) and len(ignore) == 0:
        findings.append(Finding("I1", "warning",
            "Empty ignore array",
            "An empty ignore array serves no purpose; omit it or add patterns to exclude"))

    # I2: Not ignoring node_modules explicitly
    if ignore is not None and isinstance(ignore, list):
        has_node_modules = any(
            "node_modules" in str(p) for p in ignore
        )
        if not has_node_modules:
            findings.append(Finding("I2", "info",
                "node_modules not explicitly ignored",
                "Add 'node_modules' to ignore to prevent accidental watches if watch globs are broad"))

    # I3: Overly broad ignore patterns
    if ignore and isinstance(ignore, list):
        for pattern in ignore:
            if pattern in ("*", "**", "**/*", "."):
                findings.append(Finding("I3", "warning",
                    f"Overly broad ignore pattern: '{pattern}'",
                    "This will ignore all files and nodemon won't trigger on any changes"))


def _check_exec(config, findings):
    """X1-X3: Exec/script checks."""
    exec_cmd = config.get("exec")
    script = config.get("script")
    exec_map = config.get("execMap", {})

    # X1: Shell injection risk in exec
    if exec_cmd and isinstance(exec_cmd, str):
        if SHELL_INJECTION_PATTERNS.search(exec_cmd):
            findings.append(Finding("X1", "warning",
                f"Possible shell injection risk in exec: '{exec_cmd[:60]}'",
                "Avoid shell operators in exec; use a script file or wrap in a safe command"))

    # X2: Both exec and script specified
    if exec_cmd and script:
        findings.append(Finding("X2", "warning",
            "Both exec and script are specified",
            "exec takes precedence over script; remove one to avoid confusion"))

    # X3: execMap with unknown/unusual extensions
    if exec_map and isinstance(exec_map, dict):
        known_exts = {"js", "ts", "mjs", "cjs", "coffee", "py", "rb", "sh", "jsx", "tsx"}
        for ext_key in exec_map:
            if ext_key not in known_exts:
                findings.append(Finding("X3", "info",
                    f"execMap has unusual extension: '{ext_key}'",
                    "Verify the extension is correct and the mapped command is available"))


def _check_delay(config, findings):
    """D1-D2: Delay checks."""
    delay = config.get("delay")
    if delay is None:
        return

    # Nodemon accepts delay as number (ms) or string like "2500ms" or "2.5"
    delay_ms = None
    if isinstance(delay, (int, float)):
        delay_ms = float(delay)
    elif isinstance(delay, str):
        m = re.match(r'^(\d+(?:\.\d+)?)\s*(ms|s)?$', delay.strip())
        if m:
            val = float(m.group(1))
            unit = m.group(2) or "ms"
            delay_ms = val * 1000 if unit == "s" else val

    if delay_ms is not None:
        # D1: Too low
        if delay_ms < 100:
            findings.append(Finding("D1", "warning",
                f"Delay too low: {delay} (< 100ms)",
                "Very short delays can cause rapid restart loops before your code is ready"))
        # D2: Too high
        if delay_ms > 10000:
            findings.append(Finding("D2", "warning",
                f"Delay too high: {delay} (> 10000ms)",
                "Very long delays make feedback slow; consider a value under 5000ms"))


def _check_best_practices(config, findings):
    """B1-B2: Best practices."""
    # B1: Missing verbose for debugging
    if not config.get("verbose"):
        findings.append(Finding("B1", "info",
            "verbose is not set",
            "Set verbose: true during development to see which files triggered a restart"))

    # B2: No ignore patterns at all
    ignore = config.get("ignore")
    if ignore is None:
        findings.append(Finding("B2", "warning",
            "No ignore patterns defined",
            "Without ignore patterns, test output dirs, logs, and build artifacts may trigger restarts"))


def validate(config, filepath):
    findings = []
    _check_structure(config, filepath, findings)
    _check_watch(config, findings)
    _check_extensions(config, findings)
    _check_ignore(config, findings)
    _check_exec(config, findings)
    _check_delay(config, findings)
    _check_best_practices(config, findings)
    return findings


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

def format_text(findings, filepath):
    if not findings:
        return f"✅ {filepath}: No issues found"
    lines = [f"📋 {filepath}: {len(findings)} issue(s) found\n"]
    for f in findings:
        lines.append(f.to_text())
    errors = sum(1 for f in findings if f.severity == "error")
    warnings = sum(1 for f in findings if f.severity == "warning")
    infos = sum(1 for f in findings if f.severity == "info")
    icon = "❌" if errors else ("⚠️" if warnings else "ℹ️")
    lines.append(f"\n{icon} {errors} error(s), {warnings} warning(s), {infos} info(s)")
    return "\n".join(lines)


def format_json(findings, filepath):
    return json.dumps({
        "file": filepath,
        "findings": [f.to_dict() for f in findings],
        "summary": {
            "errors": sum(1 for f in findings if f.severity == "error"),
            "warnings": sum(1 for f in findings if f.severity == "warning"),
            "infos": sum(1 for f in findings if f.severity == "info"),
            "total": len(findings),
        }
    }, indent=2)


def format_summary(findings, filepath):
    errors = sum(1 for f in findings if f.severity == "error")
    warnings = sum(1 for f in findings if f.severity == "warning")
    infos = sum(1 for f in findings if f.severity == "info")
    status = "FAIL" if errors else ("WARN" if warnings else "PASS")
    return f"{status} | {filepath} | {errors} errors, {warnings} warnings, {infos} infos"


# ---------------------------------------------------------------------------
# Explain / Suggest
# ---------------------------------------------------------------------------

def explain_config(config, filepath):
    lines = [f"📖 Nodemon Config Explanation: {filepath}\n"]

    watch = config.get("watch")
    if watch:
        lines.append(f"Watch paths: {', '.join(watch) if isinstance(watch, list) else watch}")
    else:
        lines.append("Watch paths: (default — current working directory)")

    ext = config.get("ext")
    if ext:
        lines.append(f"Extensions: {ext}")
    else:
        lines.append("Extensions: (default — js,mjs,cjs,json)")

    ignore = config.get("ignore")
    if ignore:
        lines.append(f"Ignore patterns: {', '.join(ignore) if isinstance(ignore, list) else ignore}")
    else:
        lines.append("Ignore patterns: (none set)")

    exec_cmd = config.get("exec")
    script = config.get("script")
    if exec_cmd:
        lines.append(f"Exec command: {exec_cmd}")
    if script:
        lines.append(f"Script: {script}")

    delay = config.get("delay")
    if delay is not None:
        lines.append(f"Restart delay: {delay}ms")

    exec_map = config.get("execMap", {})
    if exec_map:
        lines.append("ExecMap (extension → command):")
        for ext_key, cmd in exec_map.items():
            lines.append(f"  • .{ext_key} → {cmd}")

    events = config.get("events", {})
    if events:
        lines.append(f"Events hooked: {', '.join(events.keys()) if isinstance(events, dict) else events}")

    env = config.get("env", {})
    if env:
        lines.append(f"Environment vars: {', '.join(str(k) for k in env.keys())}")

    signal = config.get("signal")
    if signal:
        lines.append(f"Restart signal: {signal}")

    verbose = config.get("verbose")
    if verbose:
        lines.append("Verbose mode: enabled")

    legacy_watch = config.get("legacyWatch")
    if legacy_watch:
        lines.append("Legacy watch (polling): enabled")

    return "\n".join(lines)


def suggest_improvements(config, filepath):
    lines = [f"💡 Suggestions for {filepath}\n"]
    suggestions = []

    watch = config.get("watch")
    ignore = config.get("ignore", [])

    # Suggest explicit watch
    if not watch:
        suggestions.append("Add an explicit watch list (e.g. ['src', 'config']) to limit filesystem scope")

    # Suggest ignoring node_modules if not present
    ignore_strs = [str(p) for p in (ignore if isinstance(ignore, list) else [])]
    if not any("node_modules" in p for p in ignore_strs):
        suggestions.append("Add 'node_modules' to ignore to be safe if watch paths are broad")

    # Suggest ignoring build/test output directories
    common_noise_dirs = ["dist", "build", "coverage", ".nyc_output", "out"]
    missing_noise = [d for d in common_noise_dirs if not any(d in p for p in ignore_strs)]
    if missing_noise:
        suggestions.append(
            f"Consider ignoring build/output dirs: {', '.join(missing_noise[:3])}"
        )

    # Suggest verbose for debugging
    if not config.get("verbose"):
        suggestions.append("Set verbose: true to see which files trigger restarts (great for debugging watch issues)")

    # Suggest explicit ext
    if not config.get("ext"):
        suggestions.append("Set ext explicitly (e.g. 'js,json,ts') rather than relying on defaults")

    # Suggest signal for graceful shutdown
    if not config.get("signal"):
        suggestions.append("Set signal: 'SIGUSR2' for graceful shutdown support (e.g. with cluster mode or --inspect)")

    # Suggest delay if missing
    if config.get("delay") is None:
        suggestions.append("Consider setting delay: 500 to debounce rapid file saves and reduce unnecessary restarts")

    if not suggestions:
        lines.append("No suggestions — config looks good!")
    else:
        for s in suggestions:
            lines.append(f"  • {s}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 3:
        print("Usage: nodemon_config_validator.py <command> <file> [--format text|json|summary] [--strict]")
        print("Commands: validate, check, explain, suggest")
        sys.exit(2)

    command = sys.argv[1]
    filepath = sys.argv[2]
    fmt = "text"
    strict = False
    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == "--format" and i + 1 < len(sys.argv):
            fmt = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--strict":
            strict = True
            i += 1
        else:
            i += 1

    config, error = load_config(filepath)
    if error:
        if command in ("validate", "check"):
            finding = Finding(
                "S1" if "not found" in error else ("S2" if "empty" in error.lower() else "S3"),
                "error", error
            )
            if fmt == "json":
                print(format_json([finding], filepath))
            elif fmt == "summary":
                print(format_summary([finding], filepath))
            else:
                print(finding.to_text())
            sys.exit(2 if "not found" in error else 1)
        else:
            print(f"❌ {error}")
            sys.exit(2)

    if not isinstance(config, dict):
        print("❌ Config must be a JSON object")
        sys.exit(1)

    if command == "explain":
        print(explain_config(config, filepath))
        sys.exit(0)

    if command == "suggest":
        print(suggest_improvements(config, filepath))
        sys.exit(0)

    findings = validate(config, filepath)

    if command == "check":
        # check = structural rules only (S*)
        findings = [f for f in findings if f.rule_id.startswith("S")]

    if strict:
        for f in findings:
            if f.severity in ("warning", "info"):
                f.severity = "error"

    if fmt == "json":
        print(format_json(findings, filepath))
    elif fmt == "summary":
        print(format_summary(findings, filepath))
    else:
        print(format_text(findings, filepath))

    errors = sum(1 for f in findings if f.severity == "error")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
