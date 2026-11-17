#!/usr/bin/env python3
"""Skill 结构与卫生自动预检。

Usage:
    python3 pre-check.py <skill-directory>
    python3 pre-check.py <skill-directory> --json
    python3 pre-check.py <skill-directory> --verbose

在 evaluator 的 Step 1 人工安全分级之前跑，快速排除结构性问题。
不替代安全红旗分级——只做"能不能进入评估"的门槛检查。
"""

import argparse
import ast
import json
import os
import re
import sys


# --- Check infrastructure ---

class CheckResult:
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"

    def __init__(self, name, status, message="", category=""):
        self.name = name
        self.status = status
        self.message = message
        self.category = category

    def to_dict(self):
        return {
            "name": self.name,
            "status": self.status,
            "message": self.message,
            "category": self.category,
        }


# --- Checks ---

def check_skill_md_exists(skill_path):
    path = os.path.join(skill_path, "SKILL.md")
    if os.path.isfile(path):
        return CheckResult("SKILL.md exists", CheckResult.PASS, category="structure")
    return CheckResult("SKILL.md exists", CheckResult.FAIL,
                       "SKILL.md is required", category="structure")


def check_frontmatter(skill_path):
    fm = _get_frontmatter(skill_path)
    if fm is None:
        path = os.path.join(skill_path, "SKILL.md")
        if not os.path.isfile(path):
            return CheckResult("Valid frontmatter", CheckResult.FAIL,
                               "SKILL.md not found", category="structure")
        return CheckResult("Valid frontmatter", CheckResult.FAIL,
                           "No YAML frontmatter (must start with ---)", category="structure")

    missing = []
    if not fm.get("name"):
        missing.append("name")
    if not fm.get("description"):
        missing.append("description")

    if missing:
        return CheckResult("Valid frontmatter", CheckResult.FAIL,
                           f"Missing required fields: {', '.join(missing)}", category="structure")
    return CheckResult("Valid frontmatter", CheckResult.PASS, category="structure")


def check_name_matches_dir(skill_path):
    dir_name = os.path.basename(os.path.abspath(skill_path))
    fm = _get_frontmatter(skill_path)
    if fm is None:
        return CheckResult("Name matches directory", CheckResult.WARN,
                           "No frontmatter to check", category="structure")

    name = fm.get("name", "")
    if name == dir_name:
        return CheckResult("Name matches directory", CheckResult.PASS, category="structure")
    return CheckResult("Name matches directory", CheckResult.WARN,
                       f"name='{name}' but directory='{dir_name}'", category="structure")


def check_no_extraneous(skill_path):
    bad_files = {"README.md", "CHANGELOG.md", "INSTALLATION_GUIDE.md",
                 "QUICK_REFERENCE.md", "LICENSE", "LICENSE.md"}
    found = []
    for f in os.listdir(skill_path):
        if f.upper() in {b.upper() for b in bad_files}:
            found.append(f)
    if found:
        return CheckResult("No extraneous files", CheckResult.WARN,
                           f"Found: {', '.join(found)}", category="structure")
    return CheckResult("No extraneous files", CheckResult.PASS, category="structure")


def check_resource_dirs(skill_path):
    empty = []
    for d in ("scripts", "references", "assets"):
        dp = os.path.join(skill_path, d)
        if os.path.isdir(dp):
            contents = [f for f in os.listdir(dp)
                        if not f.startswith(".") and f != "__pycache__"]
            if not contents:
                empty.append(d)
    if empty:
        return CheckResult("Resource dirs non-empty", CheckResult.WARN,
                           f"Empty: {', '.join(empty)}", category="structure")
    return CheckResult("Resource dirs non-empty", CheckResult.PASS, category="structure")


def check_description_length(skill_path):
    fm = _get_frontmatter(skill_path)
    if not fm:
        return CheckResult("Description length", CheckResult.FAIL,
                           "No frontmatter", category="trigger")
    desc = fm.get("description", "")
    words = len(desc.split())
    if words < 15:
        return CheckResult("Description length", CheckResult.FAIL,
                           f"{words} words — too short for reliable triggering", category="trigger")
    if words < 30:
        return CheckResult("Description length", CheckResult.WARN,
                           f"{words} words — consider adding trigger contexts", category="trigger")
    if words > 200:
        return CheckResult("Description length", CheckResult.WARN,
                           f"{words} words — may waste context in metadata", category="trigger")
    return CheckResult("Description length", CheckResult.PASS,
                       f"{words} words", category="trigger")


def check_trigger_contexts(skill_path):
    fm = _get_frontmatter(skill_path)
    if not fm:
        return CheckResult("Trigger contexts", CheckResult.FAIL,
                           "No frontmatter", category="trigger")
    desc = fm.get("description", "").lower()
    trigger_phrases = ["use when", "use for", "use if", "when the user",
                       "when asked", "when you need", "for tasks like",
                       "such as", "e.g.", "for example",
                       # Chinese equivalents
                       "当用户", "用于", "适用于", "使用场景"]
    found = [p for p in trigger_phrases if p in desc]
    if not found:
        return CheckResult("Trigger contexts", CheckResult.WARN,
                           "No trigger phrases — add 'Use when...' or '当用户...'",
                           category="trigger")
    return CheckResult("Trigger contexts", CheckResult.PASS,
                       f"Found: {', '.join(found[:3])}", category="trigger")


def check_body_length(skill_path):
    path = os.path.join(skill_path, "SKILL.md")
    if not os.path.isfile(path):
        return CheckResult("Body length", CheckResult.FAIL, "Not found", category="documentation")
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    in_fm = False
    body_lines = 0
    fm_ended = False
    for line in lines:
        if line.strip() == "---":
            if not fm_ended:
                in_fm = not in_fm
                if not in_fm:
                    fm_ended = True
                continue
        if fm_ended:
            body_lines += 1

    if body_lines < 10:
        return CheckResult("Body length", CheckResult.FAIL,
                           f"{body_lines} lines — too short", category="documentation")
    if body_lines > 500:
        return CheckResult("Body length", CheckResult.WARN,
                           f"{body_lines} lines — consider splitting into references",
                           category="documentation")
    return CheckResult("Body length", CheckResult.PASS,
                       f"{body_lines} lines", category="documentation")


def check_references_linked(skill_path):
    ref_dir = os.path.join(skill_path, "references")
    if not os.path.isdir(ref_dir):
        return CheckResult("References linked", CheckResult.PASS,
                           "No references/ directory", category="documentation")
    ref_files = [f for f in os.listdir(ref_dir) if not f.startswith(".")]
    if not ref_files:
        return CheckResult("References linked", CheckResult.PASS,
                           "No reference files", category="documentation")

    skill_md = os.path.join(skill_path, "SKILL.md")
    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read()

    unlinked = [f for f in ref_files if f not in content]
    if unlinked:
        return CheckResult("References linked", CheckResult.WARN,
                           f"Unlinked: {', '.join(unlinked)}", category="documentation")
    return CheckResult("References linked", CheckResult.PASS, category="documentation")


def check_python_syntax(skill_path):
    scripts_dir = os.path.join(skill_path, "scripts")
    if not os.path.isdir(scripts_dir):
        return CheckResult("Script syntax", CheckResult.PASS,
                           "No scripts/", category="scripts")

    errors = []
    checked = 0
    for f in os.listdir(scripts_dir):
        if f.endswith(".py"):
            checked += 1
            fpath = os.path.join(scripts_dir, f)
            try:
                with open(fpath, "r", encoding="utf-8") as fh:
                    ast.parse(fh.read(), filename=f)
            except SyntaxError as e:
                errors.append(f"{f}:{e.lineno}: {e.msg}")

    if not checked:
        return CheckResult("Script syntax", CheckResult.PASS,
                           "No Python scripts", category="scripts")
    if errors:
        return CheckResult("Script syntax", CheckResult.FAIL,
                           "\n".join(errors), category="scripts")
    return CheckResult("Script syntax", CheckResult.PASS,
                       f"{checked} script(s) OK", category="scripts")


def check_shell_syntax(skill_path):
    scripts_dir = os.path.join(skill_path, "scripts")
    if not os.path.isdir(scripts_dir):
        return CheckResult("Shell scripts", CheckResult.PASS,
                           "No scripts/", category="scripts")

    issues = []
    checked = 0
    for f in os.listdir(scripts_dir):
        if f.endswith(".sh"):
            checked += 1
            fpath = os.path.join(scripts_dir, f)
            with open(fpath, "r", encoding="utf-8", errors="ignore") as fh:
                content = fh.read()
            if not content.startswith("#!"):
                issues.append(f"{f}: missing shebang")
            if "eval " in content or "eval(" in content:
                issues.append(f"{f}: uses eval (potential injection)")

    if not checked:
        return CheckResult("Shell scripts", CheckResult.PASS,
                           "No shell scripts", category="scripts")
    if issues:
        return CheckResult("Shell scripts", CheckResult.WARN,
                           "\n".join(issues), category="scripts")
    return CheckResult("Shell scripts", CheckResult.PASS,
                       f"{checked} script(s) OK", category="scripts")


def check_referenced_scripts_exist(skill_path):
    skill_md = os.path.join(skill_path, "SKILL.md")
    if not os.path.isfile(skill_md):
        return CheckResult("Referenced scripts exist", CheckResult.FAIL,
                           "SKILL.md not found", category="scripts")

    # If the skill has no scripts/ directory at all, any `scripts/X` mention
    # in SKILL.md must be either an external path reference (e.g.,
    # `<other-skill>/scripts/foo.py`) or authoring guidance (e.g., a
    # documentation-only skill that teaches users how to organize *their*
    # scripts). Not a self-reference, so don't try to verify.
    if not os.path.isdir(os.path.join(skill_path, "scripts")):
        return CheckResult("Referenced scripts exist", CheckResult.PASS,
                           "No scripts/ directory; external references skipped",
                           category="scripts")

    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read()

    # Negative lookbehind excludes path-prefixed references like
    # `<evaluator-path>/scripts/pre-check.py` — those are external.
    referenced = re.findall(r'(?<![/\w-])scripts/([a-zA-Z0-9_.-]+)', content)
    if not referenced:
        return CheckResult("Referenced scripts exist", CheckResult.PASS,
                           "No script references in SKILL.md", category="scripts")

    missing = []
    for script in set(referenced):
        if not os.path.isfile(os.path.join(skill_path, "scripts", script)):
            missing.append(script)

    if missing:
        return CheckResult("Referenced scripts exist", CheckResult.FAIL,
                           f"Missing: {', '.join(missing)}", category="scripts")
    return CheckResult("Referenced scripts exist", CheckResult.PASS,
                       f"All {len(set(referenced))} referenced script(s) found", category="scripts")


def check_no_hardcoded_secrets(skill_path):
    patterns = [
        (r'[a-zA-Z0-9][a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', "email"),
        (r'(?:api[_-]?key|token|secret|password)\s*[=:]\s*["\'][^"\']{8,}', "credential"),
        (r'sk-[a-zA-Z0-9]{20,}', "OpenAI key"),
        (r'ghp_[a-zA-Z0-9]{36}', "GitHub PAT"),
        (r'AKIA[0-9A-Z]{16}', "AWS access key"),
    ]
    safe_email_domains = ("example.com", "example.org", "placeholder", "your",
                          "noreply", "users.noreply")
    findings = []

    for root, dirs, files in os.walk(skill_path):
        dirs[:] = [d for d in dirs if d not in ("__pycache__", ".git", "node_modules", "bak")]
        for f in files:
            if not f.endswith((".py", ".md", ".sh", ".js", ".ts", ".yaml", ".yml", ".json", ".toml")):
                continue
            fpath = os.path.join(root, f)
            rel = os.path.relpath(fpath, skill_path)
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as fh:
                    for i, line in enumerate(fh, 1):
                        for pattern, desc in patterns:
                            m = re.search(pattern, line)
                            if not m:
                                continue
                            if desc == "email":
                                email = m.group().lower()
                                if any(d in email for d in safe_email_domains):
                                    continue
                            findings.append(f"{rel}:{i}: {desc}")
            except (IOError, UnicodeDecodeError):
                pass

    if findings:
        unique = list(dict.fromkeys(findings))[:10]
        return CheckResult("No hardcoded secrets", CheckResult.WARN,
                           f"{len(findings)} potential issue(s):\n" + "\n".join(unique),
                           category="security")
    return CheckResult("No hardcoded secrets", CheckResult.PASS, category="security")


def check_env_vars_documented(skill_path):
    scripts_dir = os.path.join(skill_path, "scripts")
    if not os.path.isdir(scripts_dir):
        return CheckResult("Env vars documented", CheckResult.PASS,
                           "No scripts/", category="security")

    env_vars = set()
    shell_builtins = {"HOME", "PATH", "USER", "SHELL", "PWD", "OLDPWD", "TERM",
                      "LANG", "LC_ALL", "HOSTNAME", "LOGNAME", "TMPDIR"}
    for f in os.listdir(scripts_dir):
        fpath = os.path.join(scripts_dir, f)
        if f.endswith(".py"):
            with open(fpath, "r", encoding="utf-8", errors="ignore") as fh:
                for line in fh:
                    if line.lstrip().startswith("#"):
                        continue
                    for m in re.finditer(r'os\.environ(?:\.get)?\s*[\[(]\s*["\'](\w+)', line):
                        env_vars.add(m.group(1))
        elif f.endswith(".sh"):
            with open(fpath, "r", encoding="utf-8", errors="ignore") as fh:
                content = fh.read()
            for m in re.finditer(r'\$\{?(\w+)\}?', content):
                var = m.group(1)
                if var not in shell_builtins and not var.startswith("_"):
                    env_vars.add(var)
        else:
            continue

    if not env_vars:
        return CheckResult("Env vars documented", CheckResult.PASS,
                           "No env vars in scripts", category="security")

    skill_md = os.path.join(skill_path, "SKILL.md")
    with open(skill_md, "r", encoding="utf-8") as f:
        skill_content = f.read()

    undocumented = [v for v in sorted(env_vars) if v not in skill_content]
    if undocumented:
        return CheckResult("Env vars documented", CheckResult.WARN,
                           f"Undocumented: {', '.join(undocumented)}", category="security")
    return CheckResult("Env vars documented", CheckResult.PASS,
                       f"All {len(env_vars)} env var(s) documented", category="security")


# --- Helpers ---

def _get_frontmatter(skill_path):
    path = os.path.join(skill_path, "SKILL.md")
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return None
    fm = {}
    for line in match.group(1).split("\n"):
        line = line.strip()
        if ":" in line:
            key, val = line.split(":", 1)
            fm[key.strip()] = val.strip()
    return fm


# --- Runner ---

ALL_CHECKS = [
    check_skill_md_exists,
    check_frontmatter,
    check_name_matches_dir,
    check_no_extraneous,
    check_resource_dirs,
    check_description_length,
    check_trigger_contexts,
    check_body_length,
    check_references_linked,
    check_python_syntax,
    check_shell_syntax,
    check_referenced_scripts_exist,
    check_no_hardcoded_secrets,
    check_env_vars_documented,
]


def run_checks(skill_path):
    results = []
    for check_fn in ALL_CHECKS:
        try:
            result = check_fn(skill_path)
            results.append(result)
        except Exception as e:
            results.append(CheckResult(
                check_fn.__name__, CheckResult.FAIL,
                f"Check crashed: {e}", "internal"
            ))
    return results


def print_report(results, skill_path, verbose=False):
    counts = {CheckResult.PASS: 0, CheckResult.WARN: 0, CheckResult.FAIL: 0}
    by_category = {}

    for r in results:
        counts[r.status] += 1
        by_category.setdefault(r.category, []).append(r)

    skill_name = os.path.basename(os.path.abspath(skill_path))
    print(f"\n{'=' * 50}")
    print(f"  Pre-check: {skill_name}")
    print(f"{'=' * 50}")
    print(f"  Path: {os.path.abspath(skill_path)}")
    print()

    icons = {CheckResult.PASS: "  PASS", CheckResult.WARN: "  WARN", CheckResult.FAIL: "  FAIL"}

    for cat in ["structure", "trigger", "documentation", "scripts", "security"]:
        if cat not in by_category:
            continue
        print(f"  [{cat.upper()}]")
        for r in by_category[cat]:
            icon = icons[r.status]
            print(f"  {icon}  {r.name}")
            if r.message and (verbose or r.status != CheckResult.PASS):
                for line in r.message.split("\n"):
                    print(f"         {line}")
        print()

    print(f"{'=' * 50}")
    print(f"  PASS: {counts[CheckResult.PASS]}  "
          f"WARN: {counts[CheckResult.WARN]}  "
          f"FAIL: {counts[CheckResult.FAIL]}")

    total = len(results)
    if counts[CheckResult.FAIL] > 0:
        print(f"\n  Result: BLOCKED — {counts[CheckResult.FAIL]} check(s) failed, fix before evaluating")
    elif counts[CheckResult.WARN] > 2:
        print(f"\n  Result: CAUTION — {counts[CheckResult.WARN]} warnings, review before proceeding")
    else:
        print(f"\n  Result: CLEAR — ready for Step 1 evaluation")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Skill structure and hygiene pre-check")
    parser.add_argument("path", help="Path to skill directory")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show details for passing checks")
    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: '{args.path}' is not a directory", file=sys.stderr)
        sys.exit(1)

    results = run_checks(args.path)

    if args.json:
        fails = sum(1 for r in results if r.status == CheckResult.FAIL)
        warns = sum(1 for r in results if r.status == CheckResult.WARN)
        output = {
            "skill": os.path.basename(os.path.abspath(args.path)),
            "path": os.path.abspath(args.path),
            "verdict": "blocked" if fails > 0 else ("caution" if warns > 2 else "clear"),
            "checks": [r.to_dict() for r in results],
            "summary": {
                "pass": sum(1 for r in results if r.status == CheckResult.PASS),
                "warn": warns,
                "fail": fails,
            }
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print_report(results, args.path, verbose=args.verbose)

    sys.exit(1 if any(r.status == CheckResult.FAIL for r in results) else 0)


if __name__ == "__main__":
    main()
