#!/usr/bin/env python3
"""
makefile-linter — Lint Makefiles for common issues.
Pure stdlib, no external dependencies.
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import List, Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SEVERITY_ORDER = {"error": 0, "warning": 1, "info": 2}

COMMON_PHONY = {
    "all", "clean", "install", "uninstall", "test", "check", "dist",
    "distclean", "build", "run", "help", "deploy", "lint", "format",
    "docs", "coverage",
}

# Built-in / automatic Make variables — exclude from "undefined" check
BUILTIN_MAKE_VARS = {
    "@", "<", "^", "?", "*", "(@D)", "(@F)", "(<D)", "(<F)", "(^D)", "(^F)",
    "CC", "CXX", "CFLAGS", "CXXFLAGS", "LDFLAGS", "LDLIBS", "LIBS",
    "MAKE", "MAKEFLAGS", "MAKECMDGOALS", "MAKEFILE_LIST", "MAKEOVERRIDES",
    "SHELL", "AR", "AS", "RM", "INSTALL", "ARFLAGS",
    "prefix", "exec_prefix", "bindir", "libdir", "includedir", "datarootdir",
    "datadir", "sysconfdir", "mandir", "infodir",
    "srcdir", "top_srcdir", "builddir", "top_builddir",
    "PATH", "HOME", "USER", "PWD", "CURDIR",
    "OUTPUT_OPTION", "COMPILE.c", "COMPILE.cc", "LINK.c", "LINK.cc",
    ".DEFAULT_GOAL", "VPATH", "SUFFIXES",
}

# Bash-specific patterns that flag shell-portability
BASH_PATTERNS = [
    r"\[\[",           # [[ ... ]]
    r"&>>",            # append-redirect stderr+stdout
    r"<<<",            # here-string
    r"\$\{[^}]*:[-=?+#%]",  # bash parameter expansion modifiers
    r"local\s+\w",    # local keyword in functions
    r"\bsource\b",    # source builtin (not POSIX)
    r"\barray\b\[",   # bash arrays
]

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class Issue:
    rule: str
    severity: str        # "error" | "warning" | "info"
    line: int
    message: str
    context: str = ""

    def as_text(self) -> str:
        ctx = f"  → {self.context}" if self.context else ""
        return f"  [{self.severity.upper()}] line {self.line}: ({self.rule}) {self.message}{ctx}"

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class LintResult:
    filename: str
    issues: List[Issue] = field(default_factory=list)

    def filtered(self, min_severity: str, ignore: List[str]) -> List[Issue]:
        threshold = SEVERITY_ORDER[min_severity]
        return [
            i for i in self.issues
            if SEVERITY_ORDER[i.severity] <= threshold and i.rule not in ignore
        ]

    @property
    def errors(self) -> int:
        return sum(1 for i in self.issues if i.severity == "error")

    @property
    def warnings(self) -> int:
        return sum(1 for i in self.issues if i.severity == "warning")

    @property
    def infos(self) -> int:
        return sum(1 for i in self.issues if i.severity == "info")


# ---------------------------------------------------------------------------
# Parser helpers
# ---------------------------------------------------------------------------

def read_file(path: str) -> List[str]:
    """Return lines (with newlines stripped) from path."""
    p = Path(path)
    if not p.exists():
        print(f"error: file not found: {path}", file=sys.stderr)
        sys.exit(2)
    return p.read_text(errors="replace").splitlines()


def parse_makefile(lines: List[str]):
    """
    Return a structured representation:
      targets: list of {name, line, recipe_lines: [(lineno, text)], phony: bool}
      variables: dict of name -> {line, value}
      phony_decls: set of declared .PHONY targets
      shell_set: bool (SHELL := ... present)
      raw_lines: the original lines
    """
    targets = []
    variables = {}
    phony_decls = set()
    shell_set = False
    current_target = None
    in_define = False

    target_re = re.compile(r'^([^#\s][^:=]*?)\s*:(?![:=])(.*)')
    var_re = re.compile(r'^([A-Za-z_][A-Za-z0-9_.-]*)\s*(?::=|=|\?=|\+=)\s*(.*)')
    phony_re = re.compile(r'^\.PHONY\s*:(.*)')
    shell_re = re.compile(r'^SHELL\s*(:=|=)\s*/bin/bash')
    define_re = re.compile(r'^define\s+')
    endef_re = re.compile(r'^endef\b')

    for lineno, raw in enumerate(lines, 1):
        line = raw

        # Track multi-line define blocks
        if define_re.match(line):
            in_define = True
            continue
        if endef_re.match(line):
            in_define = False
            continue
        if in_define:
            continue

        # Skip comments and blank lines for structural parsing
        stripped = line.rstrip()

        # .PHONY declaration
        m = phony_re.match(stripped)
        if m:
            for t in m.group(1).split():
                phony_decls.add(t.strip())
            continue

        # SHELL := /bin/bash
        if shell_re.match(stripped):
            shell_set = True

        # Variable assignment (not inside a recipe)
        if not line.startswith('\t'):
            m = var_re.match(stripped)
            if m:
                name = m.group(1)
                value = m.group(2)
                if name not in variables:
                    variables[name] = {"line": lineno, "value": value}

        # Target definition
        if not line.startswith('\t') and not line.startswith('#'):
            m = target_re.match(stripped)
            if m:
                raw_targets = m.group(1)
                # Could be multiple targets (e.g. foo bar: dep)
                for tname in raw_targets.split():
                    tname = tname.strip()
                    if tname and not tname.startswith('.') or tname in ('.PHONY', '.SUFFIXES', '.DEFAULT'):
                        entry = {
                            "name": tname,
                            "line": lineno,
                            "recipe_lines": [],
                            "phony": tname in phony_decls,
                            "prereqs": m.group(2).strip(),
                        }
                        targets.append(entry)
                current_target = targets[-1] if targets else None
                continue

        # Recipe line
        if line.startswith('\t') and current_target is not None:
            current_target["recipe_lines"].append((lineno, line[1:]))  # strip leading tab

    # Second pass: mark phony from phony_decls (collected after targets may appear)
    phony_set = phony_decls
    for t in targets:
        if t["name"] in phony_set:
            t["phony"] = True

    return {
        "targets": targets,
        "variables": variables,
        "phony_decls": phony_decls,
        "shell_set": shell_set,
        "raw_lines": lines,
    }


# ---------------------------------------------------------------------------
# Lint rules
# ---------------------------------------------------------------------------

def rule_spaces_not_tabs(parsed, lines) -> List[Issue]:
    """Recipe lines must use tabs, not spaces."""
    issues = []
    in_recipe = False
    # A recipe line immediately follows a target line; lines starting with space(s)
    # but not tab suggest the user used spaces.
    target_re = re.compile(r'^([^#\s][^:=]*?)\s*:(?![:=])')
    for lineno, raw in enumerate(lines, 1):
        if target_re.match(raw.rstrip()):
            in_recipe = True
            continue
        if raw == '' or raw.startswith('#'):
            in_recipe = False
            continue
        if not raw.startswith('\t') and in_recipe and raw.startswith('    '):
            issues.append(Issue(
                rule="spaces-not-tabs",
                severity="error",
                line=lineno,
                message="Recipe line indented with spaces instead of tab",
                context=raw[:80],
            ))
    return issues


def rule_trailing_whitespace(lines) -> List[Issue]:
    issues = []
    for lineno, raw in enumerate(lines, 1):
        if raw != raw.rstrip(' \t'):
            issues.append(Issue(
                rule="trailing-whitespace",
                severity="warning",
                line=lineno,
                message="Trailing whitespace",
                context=repr(raw[-10:]),
            ))
    return issues


def rule_long_lines(lines, limit=120) -> List[Issue]:
    issues = []
    for lineno, raw in enumerate(lines, 1):
        if len(raw) > limit:
            issues.append(Issue(
                rule="long-lines",
                severity="info",
                line=lineno,
                message=f"Line is {len(raw)} characters (limit {limit})",
                context=raw[:80] + "…",
            ))
    return issues


def rule_duplicate_targets(parsed) -> List[Issue]:
    seen = {}
    issues = []
    for t in parsed["targets"]:
        name = t["name"]
        if name in seen:
            issues.append(Issue(
                rule="duplicate-targets",
                severity="error",
                line=t["line"],
                message=f"Target '{name}' defined more than once (first at line {seen[name]})",
            ))
        else:
            seen[name] = t["line"]
    return issues


def rule_missing_phony(parsed) -> List[Issue]:
    issues = []
    phony_set = parsed["phony_decls"]
    # Collect targets that have recipe lines and whose name looks like a phony target
    for t in parsed["targets"]:
        name = t["name"]
        if name.startswith("."):
            continue
        if name in COMMON_PHONY and name not in phony_set:
            issues.append(Issue(
                rule="missing-phony",
                severity="warning",
                line=t["line"],
                message=f"Target '{name}' looks like a phony target but is not in .PHONY",
            ))
    return issues


def rule_missing_default_target(parsed) -> List[Issue]:
    targets = parsed["targets"]
    if not targets:
        return []
    names = {t["name"] for t in targets}
    if "all" not in names:
        first = targets[0]["name"]
        if first not in ("all",):
            return [Issue(
                rule="missing-default-target",
                severity="info",
                line=targets[0]["line"],
                message=f"No 'all' target found; first target is '{first}'",
            )]
    return []


def rule_missing_clean(parsed) -> List[Issue]:
    names = {t["name"] for t in parsed["targets"]}
    if "clean" not in names:
        return [Issue(
            rule="missing-clean",
            severity="info",
            line=1,
            message="No 'clean' target defined",
        )]
    return []


def rule_hardcoded_paths(parsed) -> List[Issue]:
    issues = []
    abs_path_re = re.compile(r'(?<!\$\()\b(/(?:usr|etc|var|opt|home|tmp|bin|lib|sbin|srv)[^\s\'";,)]*)')
    for t in parsed["targets"]:
        for lineno, recipe in t["recipe_lines"]:
            # Strip variable refs before checking
            cleaned = re.sub(r'\$\([^)]+\)', '', recipe)
            m = abs_path_re.search(cleaned)
            if m:
                issues.append(Issue(
                    rule="hardcoded-paths",
                    severity="warning",
                    line=lineno,
                    message=f"Hardcoded absolute path: {m.group(1)!r}",
                    context=recipe.strip()[:80],
                ))
    return issues


def rule_recursive_make(parsed, lines) -> List[Issue]:
    issues = []
    rec_re = re.compile(r'\$\(MAKE\)\s+-C|\bmake\s+-C')
    for lineno, raw in enumerate(lines, 1):
        if rec_re.search(raw):
            issues.append(Issue(
                rule="recursive-make",
                severity="info",
                line=lineno,
                message="Recursive make detected ($(MAKE) -C or make -C)",
                context=raw.strip()[:80],
            ))
    return issues


def rule_unused_variables(parsed, lines) -> List[Issue]:
    variables = parsed["variables"]
    if not variables:
        return []
    # These special variables are consumed implicitly by Make itself — never
    # explicitly referenced with $(VAR) in user recipes.
    implicit_use = {"SHELL", "MAKEFLAGS", "MAKEOVERRIDES", ".DEFAULT_GOAL", "VPATH",
                    "SUFFIXES", "ARFLAGS", "OUTPUT_OPTION"}
    full_text = "\n".join(lines)
    issues = []
    for name, info in variables.items():
        if name in implicit_use or name in BUILTIN_MAKE_VARS:
            continue
        # Look for $(NAME) or ${NAME} usage anywhere in the file
        pattern = re.compile(r'\$[({]' + re.escape(name) + r'[)}]')
        if not pattern.search(full_text):
            issues.append(Issue(
                rule="unused-variables",
                severity="warning",
                line=info["line"],
                message=f"Variable '{name}' is defined but never referenced",
            ))
    return issues


def rule_undefined_variables(parsed, lines) -> List[Issue]:
    variables = parsed["variables"]
    defined = set(variables.keys()) | BUILTIN_MAKE_VARS
    issues = []
    seen_undefined = set()
    ref_re = re.compile(r'\$[({]([A-Za-z_][A-Za-z0-9_.-]*)[)}]')
    for lineno, raw in enumerate(lines, 1):
        for m in ref_re.finditer(raw):
            name = m.group(1)
            if name not in defined and name not in seen_undefined:
                seen_undefined.add(name)
                issues.append(Issue(
                    rule="undefined-variables",
                    severity="warning",
                    line=lineno,
                    message=f"Variable '{name}' referenced but never defined",
                    context=raw.strip()[:80],
                ))
    return issues


def rule_shell_portability(parsed, lines) -> List[Issue]:
    if parsed["shell_set"]:
        return []
    issues = []
    patterns = [(re.compile(p), p) for p in BASH_PATTERNS]
    for t in parsed["targets"]:
        for lineno, recipe in t["recipe_lines"]:
            for pat, desc in patterns:
                if pat.search(recipe):
                    issues.append(Issue(
                        rule="shell-portability",
                        severity="warning",
                        line=lineno,
                        message="Bash-specific syntax used without 'SHELL := /bin/bash'",
                        context=recipe.strip()[:80],
                    ))
                    break  # one issue per recipe line
    return issues


# ---------------------------------------------------------------------------
# Core commands
# ---------------------------------------------------------------------------

def cmd_lint(path: str, args) -> LintResult:
    lines = read_file(path)
    parsed = parse_makefile(lines)
    result = LintResult(filename=path)

    result.issues += rule_spaces_not_tabs(parsed, lines)
    result.issues += rule_trailing_whitespace(lines)
    result.issues += rule_long_lines(lines)
    result.issues += rule_duplicate_targets(parsed)
    result.issues += rule_missing_phony(parsed)
    result.issues += rule_missing_default_target(parsed)
    result.issues += rule_missing_clean(parsed)
    result.issues += rule_hardcoded_paths(parsed)
    result.issues += rule_recursive_make(parsed, lines)
    result.issues += rule_unused_variables(parsed, lines)
    result.issues += rule_undefined_variables(parsed, lines)
    result.issues += rule_shell_portability(parsed, lines)

    # Sort by line number
    result.issues.sort(key=lambda i: i.line)
    return result


def cmd_targets(path: str) -> dict:
    lines = read_file(path)
    parsed = parse_makefile(lines)
    out = []
    for t in parsed["targets"]:
        if t["name"].startswith("."):
            continue
        # Try to extract a description from a comment on the preceding line
        lineno = t["line"] - 2  # 0-indexed
        desc = ""
        if 0 <= lineno < len(lines):
            prev = lines[lineno].strip()
            if prev.startswith("#"):
                desc = prev.lstrip("#").strip()
        out.append({
            "name": t["name"],
            "line": t["line"],
            "phony": t["name"] in parsed["phony_decls"],
            "prereqs": t["prereqs"],
            "description": desc,
        })
    return {"filename": path, "targets": out}


def cmd_vars(path: str) -> dict:
    lines = read_file(path)
    parsed = parse_makefile(lines)
    out = []
    for name, info in parsed["variables"].items():
        out.append({"name": name, "line": info["line"], "value": info["value"]})
    out.sort(key=lambda v: v["line"])
    return {"filename": path, "variables": out}


def cmd_audit(path: str, args) -> dict:
    lint_result = cmd_lint(path, args)
    targets_result = cmd_targets(path)
    vars_result = cmd_vars(path)
    return {
        "filename": path,
        "lint": {
            "total": len(lint_result.issues),
            "errors": lint_result.errors,
            "warnings": lint_result.warnings,
            "infos": lint_result.infos,
            "issues": [i.as_dict() for i in lint_result.issues],
        },
        "targets": targets_result["targets"],
        "variables": vars_result["variables"],
    }


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

def format_lint_text(result: LintResult, filtered: List[Issue]) -> str:
    lines = [f"Linting: {result.filename}"]
    if not filtered:
        lines.append("  No issues found.")
    else:
        for issue in filtered:
            lines.append(issue.as_text())
    total = len(filtered)
    e = sum(1 for i in filtered if i.severity == "error")
    w = sum(1 for i in filtered if i.severity == "warning")
    n = sum(1 for i in filtered if i.severity == "info")
    lines.append(f"\n{total} issue(s): {e} error(s), {w} warning(s), {n} info(s)")
    return "\n".join(lines)


def format_lint_json(result: LintResult, filtered: List[Issue]) -> str:
    data = {
        "filename": result.filename,
        "issues": [i.as_dict() for i in filtered],
        "summary": {
            "total": len(filtered),
            "errors": sum(1 for i in filtered if i.severity == "error"),
            "warnings": sum(1 for i in filtered if i.severity == "warning"),
            "infos": sum(1 for i in filtered if i.severity == "info"),
        },
    }
    return json.dumps(data, indent=2)


def format_lint_markdown(result: LintResult, filtered: List[Issue]) -> str:
    lines = [f"# Lint Report: `{result.filename}`\n"]
    if not filtered:
        lines.append("No issues found.")
    else:
        lines.append("| Line | Severity | Rule | Message |")
        lines.append("|------|----------|------|---------|")
        for issue in filtered:
            lines.append(f"| {issue.line} | {issue.severity} | `{issue.rule}` | {issue.message} |")
    e = sum(1 for i in filtered if i.severity == "error")
    w = sum(1 for i in filtered if i.severity == "warning")
    n = sum(1 for i in filtered if i.severity == "info")
    lines.append(f"\n**{len(filtered)} issue(s):** {e} error(s), {w} warning(s), {n} info(s)")
    return "\n".join(lines)


def format_targets_text(data: dict) -> str:
    lines = [f"Targets in: {data['filename']}\n"]
    for t in data["targets"]:
        phony_marker = "[PHONY]" if t["phony"] else "       "
        desc = f"  # {t['description']}" if t["description"] else ""
        prereqs = f" <- {t['prereqs']}" if t["prereqs"] else ""
        lines.append(f"  {phony_marker} {t['name']}{prereqs}{desc}  (line {t['line']})")
    lines.append(f"\n{len(data['targets'])} target(s)")
    return "\n".join(lines)


def format_targets_json(data: dict) -> str:
    return json.dumps(data, indent=2)


def format_targets_markdown(data: dict) -> str:
    lines = [f"# Targets: `{data['filename']}`\n"]
    lines.append("| Target | Line | Phony | Prereqs | Description |")
    lines.append("|--------|------|-------|---------|-------------|")
    for t in data["targets"]:
        lines.append(f"| `{t['name']}` | {t['line']} | {'yes' if t['phony'] else 'no'} | {t['prereqs']} | {t['description']} |")
    return "\n".join(lines)


def format_vars_text(data: dict) -> str:
    lines = [f"Variables in: {data['filename']}\n"]
    for v in data["variables"]:
        lines.append(f"  line {v['line']:4d}  {v['name']} = {v['value'][:60]}")
    lines.append(f"\n{len(data['variables'])} variable(s)")
    return "\n".join(lines)


def format_vars_json(data: dict) -> str:
    return json.dumps(data, indent=2)


def format_vars_markdown(data: dict) -> str:
    lines = [f"# Variables: `{data['filename']}`\n"]
    lines.append("| Variable | Line | Value |")
    lines.append("|----------|------|-------|")
    for v in data["variables"]:
        lines.append(f"| `{v['name']}` | {v['line']} | `{v['value'][:60]}` |")
    return "\n".join(lines)


def format_audit_text(data: dict) -> str:
    parts = []
    # Lint summary
    s = data["lint"]
    parts.append(f"=== Audit: {data['filename']} ===\n")
    parts.append(f"Lint: {s['total']} issue(s) — {s['errors']} error(s), {s['warnings']} warning(s), {s['infos']} info(s)")
    for issue in s["issues"]:
        ctx = f"  → {issue['context']}" if issue.get("context") else ""
        parts.append(f"  [{issue['severity'].upper()}] line {issue['line']}: ({issue['rule']}) {issue['message']}{ctx}")
    # Targets
    parts.append(f"\nTargets ({len(data['targets'])}):")
    for t in data["targets"]:
        phony = "[PHONY]" if t["phony"] else "       "
        desc = f"  # {t['description']}" if t["description"] else ""
        parts.append(f"  {phony} {t['name']}{desc}")
    # Variables
    parts.append(f"\nVariables ({len(data['variables'])}):")
    for v in data["variables"]:
        parts.append(f"  {v['name']} = {v['value'][:60]}")
    return "\n".join(parts)


def format_audit_json(data: dict) -> str:
    return json.dumps(data, indent=2)


def format_audit_markdown(data: dict) -> str:
    s = data["lint"]
    lines = [f"# Audit Report: `{data['filename']}`\n"]
    lines.append(f"## Lint Summary\n**{s['total']} issue(s):** {s['errors']} error(s), {s['warnings']} warning(s), {s['infos']} info(s)\n")
    if s["issues"]:
        lines.append("| Line | Severity | Rule | Message |")
        lines.append("|------|----------|------|---------|")
        for issue in s["issues"]:
            lines.append(f"| {issue['line']} | {issue['severity']} | `{issue['rule']}` | {issue['message']} |")
    lines.append(f"\n## Targets ({len(data['targets'])})\n")
    lines.append("| Target | Phony | Description |")
    lines.append("|--------|-------|-------------|")
    for t in data["targets"]:
        lines.append(f"| `{t['name']}` | {'yes' if t['phony'] else 'no'} | {t['description']} |")
    lines.append(f"\n## Variables ({len(data['variables'])})\n")
    lines.append("| Variable | Value |")
    lines.append("|----------|-------|")
    for v in data["variables"]:
        lines.append(f"| `{v['name']}` | `{v['value'][:60]}` |")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser():
    # Shared options parent — added to every subcommand so flags can appear
    # either before or after the subcommand name.
    shared = argparse.ArgumentParser(add_help=False)
    shared.add_argument("--format", choices=["text", "json", "markdown"], default="text",
                        help="Output format (default: text)")
    shared.add_argument("--strict", action="store_true",
                        help="Exit 1 on any issue (regardless of severity filter)")
    shared.add_argument("--ignore", action="append", default=[], metavar="RULE",
                        help="Ignore a specific rule (repeatable)")
    shared.add_argument("--min-severity", choices=["error", "warning", "info"], default="info",
                        dest="min_severity",
                        help="Minimum severity to report (default: info)")

    parser = argparse.ArgumentParser(
        prog="makefile-linter",
        description="Lint Makefiles for common issues — tabs, .PHONY, unused vars, portability, and best practices.",
        parents=[shared],
    )

    sub = parser.add_subparsers(dest="command", required=True)

    lint_p = sub.add_parser("lint", help="Lint a Makefile for common issues", parents=[shared])
    lint_p.add_argument("file", help="Path to Makefile")

    targets_p = sub.add_parser("targets", help="List all targets with descriptions", parents=[shared])
    targets_p.add_argument("file", help="Path to Makefile")

    vars_p = sub.add_parser("vars", help="List all variable definitions", parents=[shared])
    vars_p.add_argument("file", help="Path to Makefile")

    audit_p = sub.add_parser("audit", help="Full audit (lint + targets + vars summary)", parents=[shared])
    audit_p.add_argument("file", help="Path to Makefile")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    fmt = args.format

    if args.command == "lint":
        result = cmd_lint(args.file, args)
        filtered = result.filtered(args.min_severity, args.ignore)
        if fmt == "json":
            print(format_lint_json(result, filtered))
        elif fmt == "markdown":
            print(format_lint_markdown(result, filtered))
        else:
            print(format_lint_text(result, filtered))
        if args.strict and filtered:
            sys.exit(1)
        if result.errors:
            sys.exit(1)

    elif args.command == "targets":
        data = cmd_targets(args.file)
        if fmt == "json":
            print(format_targets_json(data))
        elif fmt == "markdown":
            print(format_targets_markdown(data))
        else:
            print(format_targets_text(data))

    elif args.command == "vars":
        data = cmd_vars(args.file)
        if fmt == "json":
            print(format_vars_json(data))
        elif fmt == "markdown":
            print(format_vars_markdown(data))
        else:
            print(format_vars_text(data))

    elif args.command == "audit":
        data = cmd_audit(args.file, args)
        if fmt == "json":
            print(format_audit_json(data))
        elif fmt == "markdown":
            print(format_audit_markdown(data))
        else:
            print(format_audit_text(data))
        # Apply strict/error exit for audit too
        lint = data["lint"]
        filtered_count = sum(
            1 for i in lint["issues"]
            if SEVERITY_ORDER[i["severity"]] <= SEVERITY_ORDER[args.min_severity]
            and i["rule"] not in args.ignore
        )
        if args.strict and filtered_count:
            sys.exit(1)
        if lint["errors"]:
            sys.exit(1)


if __name__ == "__main__":
    main()
